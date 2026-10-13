#!/usr/bin/env python3
"""Pregenera y verifica los audios cortos (letras, sílabas, palabras de 1–2 letras).

Aisladas, la voz las corta o las cambia («A» muda, «R» → «É, hein?», 马 → 妈).
Para cada caso del manifiesto (tools/voz/manifiesto_cortos.mts) se prueban tomas
con distintos modelos, se transcriben de vuelta (scribe_v1) y se guarda la
primera que coincide como <hash>.mp3: la clave es la que usaría `/voz`, así que
basta copiar los archivos al AUDIO_DIR del servidor.

  python3 tools/voz/pregenerar_cortos.py manifiesto.json salida/ [--idiomas es,pt]

Lee ELEVENLABS_API_KEY de backend/.env sin imprimirla. Deja salida/informe.json.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.request
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOMAS = [('eleven_flash_v2_5', 0), ('eleven_v3', 0), ('eleven_flash_v2_5', 1), ('eleven_v3', 1), ('eleven_multilingual_v2', 0)]
# Una vocal suelta sale a menudo como interjección («Ah?», «Hã?») u otra palabra («Okey»):
# más tomas, y solo vale la vocal tal cual.
TOMAS_VOCAL = TOMAS + [('eleven_flash_v2_5', 2), ('eleven_v3', 2), ('eleven_flash_v2_5', 3)]
# Lo corto se sintetiza estable y sin estilo: menos entonación de pregunta o sorpresa.
AJUSTES = {'stability': 1.0, 'similarity_boost': 0.8, 'style': 0.0, 'use_speaker_boost': True}
VOCALES = set('aeiouyáéíóúàèìòùâêîôûäöüãõ')


def clave():
    with open(os.path.join(RAIZ, 'backend', '.env'), encoding='utf8') as f:
        for linea in f:
            if linea.startswith('ELEVENLABS_API_KEY='):
                return linea.split('=', 1)[1].strip().strip('"\'')
    raise SystemExit('falta ELEVENLABS_API_KEY en backend/.env')


KEY = clave()


def pedir(req, intentos=5):
    for i in range(intentos):
        try:
            return urllib.request.urlopen(req, timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < intentos - 1:
                time.sleep(2 + 3 * i)
                continue
            raise


def sintetizar(texto, voz, idioma, modelo):
    cuerpo = {'text': texto, 'model_id': modelo, 'voice_settings': AJUSTES}
    if 'v2_5' in modelo or 'v3' in modelo:
        cuerpo['language_code'] = idioma
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format=mp3_44100_128',
        data=json.dumps(cuerpo).encode(), headers={'xi-api-key': KEY, 'content-type': 'application/json'})
    return pedir(req)


def transcribir(mp3, idioma):
    b = uuid.uuid4().hex
    partes = [
        f'--{b}\r\nContent-Disposition: form-data; name="model_id"\r\n\r\nscribe_v1\r\n'.encode(),
        f'--{b}\r\nContent-Disposition: form-data; name="language_code"\r\n\r\n{idioma}\r\n'.encode(),
        f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode() + mp3 + b'\r\n',
        f'--{b}--\r\n'.encode(),
    ]
    req = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text', data=b''.join(partes),
                                 headers={'xi-api-key': KEY, 'content-type': f'multipart/form-data; boundary={b}'})
    return json.loads(pedir(req)).get('text', '').strip()


def comparable(s):
    s = unicodedata.normalize('NFC', s.lower())
    s = ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)  # katakana → hiragana
    return re.sub(r'[\s\W_]', '', s)


def sin_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def aceptables(caso):
    acept = {comparable(e) for e in caso['esperado']}
    for e in list(acept):
        if len(e) == 1 and e in VOCALES:  # la vocal tal cual: «a», «ah»
            base = sin_acento(e)
            acept |= {base, base + 'h'}
    return acept


def coincide(caso, oido):
    # Pregunta, exclamación o palabras de más: no es la vocal o la letra tal cual.
    if re.search(r'[?!¿¡？！]', oido):
        return False
    if len(oido.split()) > max(len(e.split()) for e in caso['esperado']):
        return False
    o = comparable(oido)
    return bool(o) and (o in aceptables(caso) or sin_acento(o) in aceptables(caso))


def es_vocal(caso):
    n = comparable(caso['normalizado'])
    return len(n) == 1 and (n in VOCALES or n in 'аеёиоуыэюяアイウエオあいうえお아어오우으이애에')


def procesar(caso, salida):
    destino = os.path.join(salida, caso['hash'] + '.mp3')
    tomas = []
    for modelo, n in (TOMAS_VOCAL if es_vocal(caso) else TOMAS):
        try:
            mp3 = sintetizar(caso['normalizado'], caso['voz_id'], caso['idioma'], modelo)
            oido = transcribir(mp3, caso['idioma'])
        except Exception as e:  # noqa: BLE001 — se informa y se prueba la siguiente toma
            tomas.append({'modelo': modelo, 'error': str(e)[:120]})
            continue
        tomas.append({'modelo': modelo, 'toma': n, 'oido': oido, 'mp3': mp3})
        # La API no guarda semilla: cada llamada es una toma distinta aunque el texto se repita.
        # Las cifras se transcriben como cifra o como palabra: basta la primera toma.
        if coincide(caso, oido) or re.fullmatch(r'\d+', comparable(caso['normalizado'])):
            break
    buenas = [t for t in tomas if 'mp3' in t]
    if not buenas:
        return {**caso, 'estado': 'error', 'tomas': tomas}
    elegida = next((t for t in buenas if coincide(caso, t['oido'])), None)
    estado = 'verificado' if elegida else 'sin_verificar'
    # Sin coincidencia: una sin tono de pregunta, mejor de v3 (pronuncia mejor las sílabas sueltas).
    # Nunca ruido ni silencio («[música]», «[clic]», vacío): antes una toma dudosa pero hablada.
    habladas = [t for t in buenas if t['oido'] and '[' not in t['oido']] or buenas
    llanas = [t for t in habladas if not re.search(r'[?!¿¡？！]', t['oido'])] or habladas
    elegida = elegida or next((t for t in llanas if t['modelo'] == 'eleven_v3'), llanas[0])
    with open(destino, 'wb') as f:
        f.write(elegida['mp3'])
    resumen = [{k: v for k, v in t.items() if k != 'mp3'} for t in tomas]
    return {**caso, 'estado': estado, 'modelo': elegida['modelo'], 'oido': elegida['oido'], 'tomas': resumen}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifiesto')
    ap.add_argument('salida')
    ap.add_argument('--idiomas', default='')
    ap.add_argument('--hilos', type=int, default=4)
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    casos = json.load(open(a.manifiesto, encoding='utf8'))
    if a.idiomas:
        casos = [c for c in casos if c['idioma'] in a.idiomas.split(',')]
    informe_ruta = os.path.join(a.salida, 'informe.json')
    hechos = {}
    if os.path.exists(informe_ruta):
        hechos = {r['hash']: r for r in json.load(open(informe_ruta, encoding='utf8')) if r['estado'] != 'error'}
    pendientes = [c for c in casos if c['hash'] not in hechos]
    print(f'{len(casos)} casos, {len(pendientes)} pendientes', flush=True)
    with cf.ThreadPoolExecutor(a.hilos) as ex:
        for i, r in enumerate(ex.map(lambda c: procesar(c, a.salida), pendientes), 1):
            hechos[r['hash']] = r
            if i % 50 == 0:
                json.dump(list(hechos.values()), open(informe_ruta, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
                print(i, flush=True)
    informe = list(hechos.values())
    json.dump(informe, open(informe_ruta, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    por = {}
    for r in informe:
        por.setdefault(r['idioma'], {}).setdefault(r['estado'], 0)
        por[r['idioma']][r['estado']] += 1
    for idioma, est in sorted(por.items()):
        print(idioma, est)


if __name__ == '__main__':
    main()
