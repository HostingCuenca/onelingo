"""Romanización de los ítems de ejercicio (convención de docs/claude-educacion/ROMANIZACION.md).

Lo usan los validadores de ruta de ru, ko, ja y zh:

    errores = rom_items.errores(ruta_json, hay, comprobar)

- `hay(texto)` dice si un texto está en la escritura del idioma (cirílico, hangul…);
- `comprobar(texto, rom)` devuelve un mensaje si el `rom` no corresponde al texto (o None).

Reglas: `texto`/`pregunta` → `textoRom`/`preguntaRom`; `opciones`, `tokens` y la
izquierda de `pares` → `opcionesRom`, `tokensRom`, `paresRom` (listas paralelas,
"" en la posición que no lleva escritura del idioma). Los ítems no llevan `rom`
suelto, y `audio`, `respuesta` y `aceptadas` nunca llevan romanización.
"""

PROHIBIDAS = ('rom', 'audioRom', 'respuestaRom', 'aceptadasRom', 'romOpciones', 'romTokens', 'romPares')


def _items(x):
    if isinstance(x, dict):
        if 'formato' in x:
            yield x
        for v in x.values():
            yield from _items(v)
    elif isinstance(x, list):
        for v in x:
            yield from _items(v)


def errores(ruta_json, hay, comprobar=None):
    out = []
    for u in ruta_json.get('unidades', []):
        uid = u.get('id', '?')
        for it in _items(u.get('pasos', [])):
            donde = f'{uid}/{it.get("id", "?")}'
            for k in PROHIBIDAS:
                if k in it:
                    out.append(f'{donde}: el ítem lleva «{k}»; usa textoRom/preguntaRom/opcionesRom/tokensRom/paresRom '
                               '(audio y respuesta no llevan rom)')
            for campo in ('texto', 'pregunta'):
                valor, rom = it.get(campo), it.get(campo + 'Rom')
                if hay(valor):
                    if not isinstance(rom, str) or not rom.strip():
                        out.append(f'{donde}: {campo} sin {campo}Rom')
                    elif comprobar and (m := comprobar(valor, rom)):
                        out.append(f'{donde}: {campo}Rom: {m}')
                elif rom:
                    out.append(f'{donde}: {campo}Rom sin {campo} en la escritura del idioma')
            listas = {
                'opciones': [o if isinstance(o, str) else None for o in it.get('opciones') or []],
                'tokens': list(it.get('tokens') or []),
                'pares': [p[0] if isinstance(p, list) and p else None for p in it.get('pares') or []],
            }
            for campo, vals in listas.items():
                roms = it.get(campo + 'Rom')
                if not any(hay(v) for v in vals):
                    if roms and any(roms):
                        out.append(f'{donde}: {campo}Rom sin {campo} en la escritura del idioma')
                    continue
                if not isinstance(roms, list) or len(roms) != len(vals):
                    out.append(f'{donde}: {campo} sin {campo}Rom paralelo (misma longitud)')
                    continue
                for i, (v, r) in enumerate(zip(vals, roms)):
                    if hay(v):
                        if not isinstance(r, str) or not r.strip():
                            out.append(f'{donde}: {campo}Rom[{i}] vacío para «{v}»')
                        elif comprobar and (m := comprobar(v, r)):
                            out.append(f'{donde}: {campo}Rom[{i}]: {m}')
                    elif r:
                        out.append(f'{donde}: {campo}Rom[{i}] debe ir vacío («{v}» no lleva rom)')
    return out
