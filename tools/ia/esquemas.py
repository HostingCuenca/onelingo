"""Esquemas JSON (modo estricto de OpenAI) de lo que escribe el modelo.

El modelo solo escribe contenido lingüístico. Lo mecánico lo pone el programa
(`openai_contenido.py`): ids, orden, prerrequisitos, nivel, claves y repasos.
En modo estricto todo campo es obligatorio; lo opcional se declara anulable
y el programa quita los null antes de guardar.
`rom` = romanización (solo idiomas sin escritura latina: ru, ko, ja, zh); en el resto va null.
"""

S = {'type': 'string'}
I = {'type': 'integer'}
B = {'type': 'boolean'}


def nulo(t):
    return {'anyOf': [t, {'type': 'null'}]}


def obj(**props):
    return {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}


def lista(t):
    return {'type': 'array', 'items': t}


BI = obj(es=S, en=S)
FORMATO = lambda f: {'type': 'string', 'enum': [f]}  # noqa: E731
OPCIONES = {'anyOf': [lista(S), lista(BI)]}

ITEM = {'anyOf': [
    obj(formato=FORMATO('completar'), consigna=BI, feedback=BI, pista=nulo(BI), texto=S, respuesta=S,
        opciones=nulo(lista(S)), aceptadas=nulo(lista(S))),
    obj(formato=FORMATO('elegir'), consigna=BI, feedback=BI, pista=nulo(BI), opciones=OPCIONES, respuesta=I),
    obj(formato=FORMATO('escuchar'), consigna=BI, feedback=BI, pista=nulo(BI), audio=S, opciones=OPCIONES, respuesta=I),
    obj(formato=FORMATO('ordenar'), consigna=BI, feedback=BI, pista=nulo(BI), tokens=lista(S), respuesta=S,
        aceptadas=nulo(lista(S))),
    obj(formato=FORMATO('relacionar'), consigna=BI, feedback=BI, pista=nulo(BI),
        pares=lista(obj(izquierda=S, derecha=BI))),
    obj(formato=FORMATO('escribir'), consigna=BI, feedback=BI, pista=nulo(BI), respuesta=S, aceptadas=nulo(lista(S)),
        abierta=B, minimoPalabras=nulo(I), maximoPalabras=nulo(I)),
]}

TIPO = lambda t: {'type': 'string', 'enum': [t]}  # noqa: E731
CELDA = {'anyOf': [obj(texto=S, rom=nulo(S)), obj(apoyo=BI)]}
PASO = {'anyOf': [
    obj(tipo=TIPO('explicacion'), icono={'type': 'string', 'enum': ['gramatica', 'sonido', 'cultura', 'consejo']},
        titulo=BI, texto=BI),
    obj(tipo=TIPO('ejemplos'), items=lista(obj(texto=S, rom=nulo(S), traduccion=BI, nota=nulo(BI)))),
    obj(tipo=TIPO('vocabulario')),
    obj(tipo=TIPO('tabla'), titulo=BI, texto=nulo(BI), columnas=lista(BI), filas=lista(lista(CELDA))),
    obj(tipo={'type': 'string', 'enum': ['practica_guiada', 'practica_independiente', 'evaluacion']},
        items=lista(ITEM)),
    obj(tipo=TIPO('situacion'), contexto=BI, dialogo=lista(obj(hablante=S, texto=S, rom=nulo(S), traduccion=BI)),
        items=lista(ITEM)),
]}

CLASE = obj(
    vocabulario=lista(obj(texto=S, rom=nulo(S), traduccion=BI, nota=nulo(BI))),
    erroresFrecuentes=lista(obj(incorrecto=S, correcto=S, explicacion=BI)),
    pasos=lista(PASO),
)

REVISION = obj(
    veredicto={'type': 'string', 'enum': ['GO', 'REVISE']},
    problemas=lista(obj(gravedad={'type': 'string', 'enum': ['alta', 'media', 'baja']},
                        donde=S, antes=S, despues=S, motivo=S)),
    clase=CLASE,
)

MAPA = obj(claves=lista(obj(clase=S, bloque=I, clave=S, gramatica=lista(S), funcion=S, depende_de=lista(S))))

OUTLINE = obj(clases=lista(obj(
    clase=S, titulo=BI, objetivo=BI, gramatica=lista(S),
    vocabulario=obj(campo=BI, palabras=lista(S)), sonido=S, situacion=I, tarea=BI,
)))

_EJ = obj(formato={'type': 'string', 'enum': ['completar', 'elegir', 'escuchar', 'ordenar', 'relacionar', 'escribir']},
          clave=S, consigna=S, ejemplo=S)
FICHAS = obj(fichas=lista(obj(id=S, ejercicios=obj(
    guiada=lista(_EJ), independiente=lista(_EJ),
    situacion=obj(texto=S, preguntas=lista(_EJ)), evaluacion=lista(_EJ),
))))


# ---------------------------------------------------------------- romanización de los ítems
# Solo los idiomas sin alfabeto latino llevan textoRom/opcionesRom/tokensRom/paresRom en los
# ítems (docs/claude-educacion/ROMANIZACION.md). Para el resto, clase(idi) y revision(idi)
# devuelven CLASE y REVISION tal cual: su esquema no cambia.
NO_LATINOS = {'ru', 'ko', 'ja', 'zh'}
_ROM_TRAS = {'texto': 'textoRom', 'opciones': 'opcionesRom', 'tokens': 'tokensRom', 'pares': 'paresRom'}


def _con_rom(rama):
    props = {}
    for k, v in rama['properties'].items():
        props[k] = v
        if k in _ROM_TRAS:
            props[_ROM_TRAS[k]] = nulo(S) if k == 'texto' else nulo(lista(S))
    return obj(**props)


ITEM_ROM = {'anyOf': [_con_rom(r) for r in ITEM['anyOf']]}
PASO_ROM = {'anyOf': [obj(**{k: (lista(ITEM_ROM) if v == lista(ITEM) else v) for k, v in r['properties'].items()})
                      for r in PASO['anyOf']]}
CLASE_ROM = obj(**{k: (lista(PASO_ROM) if k == 'pasos' else v) for k, v in CLASE['properties'].items()})
REVISION_ROM = obj(**{k: (CLASE_ROM if k == 'clase' else v) for k, v in REVISION['properties'].items()})


def clase(idi):
    return CLASE_ROM if idi in NO_LATINOS else CLASE


def revision(idi):
    return REVISION_ROM if idi in NO_LATINOS else REVISION
