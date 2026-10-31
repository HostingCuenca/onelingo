#!/usr/bin/env python3
"""Videollamada simulada: una IA hace de alumno y habla con el tutor real.

    python3 tools/pruebas/llamada_simulada.py [--turnos 6] [--nivel 1] [--salida informe.json]

Requisitos: emulador con la app abierta en una videollamada SIN contestar (botón
«Contestar» visible) y la depuración del WebView reenviada a 127.0.0.1:9333
(`adb forward tcp:9333 localabstract:webview_devtools_remote_<pid>`).

El script sustituye el micrófono de la página por un audio sintético: cada
respuesta del alumno (OpenAI, con pausas y titubeos de estudiante) se convierte
en voz con `/api/voz` (voz hispana hablando inglés, con acento) y entra por el
mismo camino que un micrófono real (WebSocket de transcripción en vivo). Mide,
por turno: lo que dijo frente a lo que se transcribió, cuántos envíos hizo la
página (cortes), y el tiempo desde que el alumno calla hasta que suena el tutor.
La clave de OpenAI se toma como en tools/ia/openai_contenido.py y nunca se imprime.
"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

import websocket

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ia'))
from openai_contenido import _clave  # noqa: E402

MODELO_ALUMNO = 'gpt-5.4-mini'

INYECTAR = r"""
(async () => {
  window.__log = []; const t0 = window.__t0 = performance.now();
  const L = window.__L = (tipo, datos = {}) => window.__log.push({t: +((performance.now() - t0) / 1000).toFixed(2), tipo, ...datos});
  const W = window.WebSocket;
  window.WebSocket = function (u, p) {
    L('ws_abre'); const w = new W(u, p);
    w.addEventListener('close', e => L('ws_cierra', {codigo: e.code, motivo: e.reason}));
    w.addEventListener('message', e => {
      let m; try { m = JSON.parse(e.data); } catch { return; }
      if (m.message_type === 'partial_transcript') { if (!window.__parcial && m.text) { window.__parcial = true; L('parcial', {texto: m.text}); } }
      else { window.__parcial = false; L(m.message_type, {texto: m.text ?? m.error ?? ''}); }
    });
    return w;
  };
  window.WebSocket.prototype = W.prototype;
  const F = window.fetch;
  window.fetch = async (u, o) => {
    const s = String(u), ruta = new URL(s, location.href).pathname.replace(/^\/api/, '');
    const vigilar = /^\/(chat|llamada|transcribir)/.test(ruta);
    if (vigilar) L('pide', {ruta, cuerpo: ruta === '/chat' && o?.body ? (JSON.parse(o.body).mensaje ?? '').slice(0, 200) : undefined});
    const r = await F(u, o);
    if (vigilar) L('responde', {ruta, estado: r.status});
    return r;
  };
  window.__marca = (tipo, x) => L('m_' + tipo, x == null ? {} : {texto: String(x)});
  const cw = console.warn; console.warn = (...a) => { L('aviso', {texto: a.map(String).join(' ')}); cw(...a); };
  const au = document.getElementById('audio');
  au.addEventListener('playing', () => { if (!au.src.startsWith('data:')) L('tutor_suena'); });
  au.addEventListener('ended', () => L('tutor_frase_fin'));
  new MutationObserver(() => L('fase', {fase: document.getElementById('stage').dataset.phase}))
    .observe(document.getElementById('stage'), {attributes: true, attributeFilter: ['data-phase']});
  const API = '__API__';
  const r = await F(API + '/usuarios/login', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({email: 'ana@onelingo.demo'})});
  window.__tok = (await r.json()).token;
  window.__ctx = new AudioContext({sampleRate: 48000});
  window.__dest = __ctx.createMediaStreamDestination();
  navigator.mediaDevices.getUserMedia = async () => __dest.stream;
  // Dice todos los trozos de un turno con sus pausas exactas (el audio se baja antes).
  window.__decir = async (trozos, idioma, voz) => {
    const bufs = await Promise.all(trozos.map(async x => __ctx.decodeAudioData(await (await F(API + '/voz?' + new URLSearchParams({texto: x.texto, idioma, voz, token: __tok}))).arrayBuffer())));
    await __ctx.resume();
    for (let i = 0; i < trozos.length; i++) {
      const s = __ctx.createBufferSource(); s.buffer = bufs[i]; s.connect(__dest);
      await new Promise(ok => { s.onended = ok; L('alumno_habla', {texto: trozos[i].texto}); s.start(); });
      L('alumno_calla');
      await new Promise(ok => setTimeout(ok, trozos[i].pausa_ms));
    }
    return 'ok';
  };
  return 'ok';
})()
"""


class Pagina:
    def __init__(self, puerto=9333):
        paginas = json.load(urllib.request.urlopen(f'http://127.0.0.1:{puerto}/json'))
        avatar = next(p for p in paginas if '/avatar/' in p['url'])
        self.ws = websocket.create_connection(avatar['webSocketDebuggerUrl'], timeout=120, suppress_origin=True)
        self.n = 0

    def js(self, expr):
        self.n += 1
        self.ws.send(json.dumps({'id': self.n, 'method': 'Runtime.evaluate',
                                 'params': {'expression': expr, 'awaitPromise': True, 'returnByValue': True}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get('id') == self.n:
                r = m.get('result', {})
                if 'exceptionDetails' in r:
                    raise RuntimeError(r['exceptionDetails'].get('exception', {}).get('description', 'error JS'))
                return r.get('result', {}).get('value')

    def fase(self):
        return self.js("document.getElementById('stage').dataset.phase")

    def esperar_turno(self, limite=60):
        """Espera a que el tutor termine y la fase quede en «ready» un momento."""
        fin = time.time() + limite
        listo_desde = None
        while time.time() < fin:
            if self.fase() == 'ready':
                listo_desde = listo_desde or time.time()
                if time.time() - listo_desde > 0.8:
                    return True
            else:
                listo_desde = None
            time.sleep(0.25)
        return False

    def ultimo_tutor(self):
        return self.js("[...document.querySelectorAll('#messages .bubble:not(.mine):not(.feedback)')].slice(-2).map(b => b.textContent).join(' ')")


ESQUEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['trozos'],
    'properties': {'trozos': {'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': {
        'type': 'object', 'additionalProperties': False, 'required': ['texto', 'pausa_ms'],
        'properties': {'texto': {'type': 'string'}, 'pausa_ms': {'type': 'integer'}}}}},
}


def alumno(historial, nivel):
    instrucciones = (
        f'Eres un alumno hispanohablante de inglés de nivel {nivel} (de 10) en una videollamada con su tutor. '
        'Responde SOLO a lo último que dijo el tutor, en inglés, como lo diría un estudiante real de ese nivel: '
        'frases cortas, algún error típico de hispanohablante (artículos, tiempos, "I have 20 years") y, a veces, '
        'un titubeo ("uh", "mmm") o una palabra en español que no sabes. Si el tutor te pide repetir, repite con la corrección. '
        'Divide lo que dices en 1 a 4 trozos tal como hablarías: pausa_ms es el silencio DESPUÉS de cada trozo '
        '(200–600 si sigues de corrido, 900–2000 si te quedas pensando a mitad de frase; el último trozo, 0).'
    )
    cuerpo = {'model': MODELO_ALUMNO, 'instructions': instrucciones, 'input': json.dumps(historial[-8:], ensure_ascii=False),
              'text': {'format': {'type': 'json_schema', 'name': 'alumno', 'schema': ESQUEMA, 'strict': True}}}
    req = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(cuerpo).encode(), method='POST',
                                 headers={'Authorization': f'Bearer {_clave()}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    texto = next(c['text'] for o in d['output'] if o.get('type') == 'message' for c in o['content'] if c.get('type') == 'output_text')
    return json.loads(texto)['trozos']


def analizar(log, turnos):
    """Reparte el registro por turnos y calcula tiempos y cortes."""
    informe = []
    for i, t in enumerate(turnos):
        ini, fin = t['inicio'], turnos[i + 1]['inicio'] if i + 1 < len(turnos) else 1e9
        ev = [e for e in log if ini <= e['t'] < fin]
        calla = max((e['t'] for e in ev if e['tipo'] == 'alumno_calla'), default=None)
        suena = next((e['t'] for e in ev if e['tipo'] == 'tutor_suena' and calla and e['t'] > calla), None)
        envios = [e.get('cuerpo') for e in ev if e['tipo'] == 'pide' and e.get('ruta') == '/chat']
        transcrito = [e['texto'] for e in ev if e['tipo'].startswith('committed_transcript') and e.get('texto')]
        interrumpe = [e['t'] for e in ev if e['tipo'] == 'tutor_suena' and calla and e['t'] < calla]
        informe.append({
            'dijo': ' '.join(x['texto'] for x in t['trozos']),
            'pausas_ms': [x['pausa_ms'] for x in t['trozos'][:-1]],
            'transcrito': ' | '.join(transcrito),
            'envios_chat': len(envios),
            'tutor_hablo_mientras_el_alumno_seguia': len(interrumpe) > 0,
            'segundos_hasta_que_suena_el_tutor': round(suena - calla, 2) if (suena and calla) else None,
            'cortes_ws': sum(1 for e in ev if e['tipo'] == 'ws_cierra'),
        })
    return informe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--turnos', type=int, default=6)
    ap.add_argument('--nivel', type=int, default=1)
    ap.add_argument('--voz', default='narrador', help='rol de voz del alumno en /api/voz (idioma es: acento hispano)')
    ap.add_argument('--salida')
    ap.add_argument('--api', default='https://onelingo.org/api', help='base de la API que usa la página (local: http://10.0.2.2:8091)')
    a = ap.parse_args()

    p = Pagina()
    # Con la llamada ya en curso el micrófono real está abierto y el alumno simulado no se oiría.
    if p.fase() != 'ringing':
        sys.exit(f'La llamada debe estar sonando sin contestar (fase actual: {p.fase()})')
    if p.js(INYECTAR.replace('__API__', a.api)) != 'ok':
        sys.exit('No se pudo preparar la página')
    p.js("document.getElementById('llamar').click()")
    if not p.esperar_turno(40):
        sys.exit('El tutor no terminó de saludar')
    historial, turnos = [], []
    for n in range(a.turnos):
        historial.append({'tutor': p.ultimo_tutor()})
        trozos = alumno(historial, a.nivel)
        inicio = p.js('+((performance.now() - __t0) / 1000).toFixed(2)')
        turnos.append({'inicio': inicio, 'trozos': trozos})
        p.js(f"__decir({json.dumps(trozos)}, 'es', {json.dumps(a.voz)})")
        historial.append({'alumno': ' '.join(x['texto'] for x in trozos)})
        print(f'turno {n + 1}: {historial[-1]["alumno"]}', flush=True)
        if not p.esperar_turno(60):
            print('  (el tutor no devolvió el turno en 60 s)', flush=True)
    log = p.js('window.__log')
    informe = analizar(log, turnos)
    for i, r in enumerate(informe, 1):
        print(f"\n#{i} dijo: {r['dijo']}\n   oyó: {r['transcrito']}\n   envíos /chat: {r['envios_chat']} · tutor encima: {r['tutor_hablo_mientras_el_alumno_seguia']}"
              f" · respuesta en {r['segundos_hasta_que_suena_el_tutor']} s · cortes ws: {r['cortes_ws']} · pausas {r['pausas_ms']}")
    if a.salida:
        Path(a.salida).write_text(json.dumps({'informe': informe, 'log': log}, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
