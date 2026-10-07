#!/usr/bin/env python3
"""Control editorial estricto para un nivel ya poblado de ejercicios.

Uso:
  python3 tools/curriculo/validar_plan_detallado.py pt
  python3 tools/curriculo/validar_plan_detallado.py pt /tmp/plan.json
  python3 tools/curriculo/validar_plan_detallado.py pt /tmp/piloto.json --parcial
  python3 tools/curriculo/validar_plan_detallado.py de curriculo/de/n1.json --parcial

Por idioma (``POR_IDIOMA``): lengua exigida en la situación, regex de español
infiltrado, frases genéricas y control de la c50. El portugués es el valor por
defecto (fr/es heredan ese comportamiento tal cual). En ``de`` (método ligero,
sin reparto) y en ``it`` (igual que ``de``) la c50 de cada nivel es la prueba: sin ``introduce`` y con una
evaluación que repasa al menos 5 claves del nivel. Con ``--parcial`` las fichas
aún en ``esqueleto`` sin ``ejercicios`` se cuentan como pendientes y no se
validan (sirve para validar un nivel a medio planificar).

El nivel se infiere de ``nivel`` o del primer id de clase (por ejemplo,
``pt.n2.c01``). Sin ruta explícita se conserva N1 como valor predeterminado.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]
FORMATOS = {'elegir', 'escuchar', 'ordenar', 'completar', 'escribir', 'relacionar'}
PROHIBIDAS = re.compile(
    r'una opción que no corresponde|practicar [a-záéíóúñ -]+|respuesta principal|'
    r'dato que se confirma|texto en la ficha|en una situación cotidiana|respuesta modelo',
    re.IGNORECASE,
)
MAQUILLAJE = re.compile(
    r'\bcaso\s+\d+\b|\bdato\s+\d+\b|\bdetalle\s+\d+\b|'
    r'\bficha\s+c\d+\b|contexto:\s*una persona|mensaje posible|'
    r'la respuesta es|respuesta indicada|\bmodelo:|'
    r'usa la palabra «[^»]+» en la actividad|busca «[^»]+» en la escena|'
    r'otra informaci[oó]n|una frase diferente|\[respuesta\s*/\s*de|'
    r'\[a\s*/\s*frase\s*/\s*correta\s*/\s*[eé]\]|'
    r'pergunta:\s*[^?]+\?\s*a\)|pistas:\s*rita=|'
    r'\btema:|\b\d{2}-\d\b|pr[aá]ctica guiada|pr[aá]ctica independiente|'
    r'prueba final|resposta correta|resposta diferente|resposta portuguesa|'
    r'mensagem curta em portugu[eê]s|dados reais do cliente|frase del cliente|'
    r'dado do [aá]udio|outro dado|respuesta exacta|otra respuesta|respuesta del aviso|'
    r'\[mensagem\s*/\s*\d+\s*/\s*ordena\]|'
    r'\([^)]*ejercicio\s+(?:guiada|independiente|evaluacion)\s+\d+\)|'
    r'—[^—]+(?:guiada|independiente|evaluacion)\s*—|'
    r'a\)\s*dato exacto\s+b\)\s*dato distinto|frase:\s*___|'
    r'resp(?:uesta|osta) del di[aá]logo|elige el dato que aparece en la escena|'
    r'completa la respuesta usando el di[aá]logo',
    re.IGNORECASE,
)
ESPANOL_EN_SITUACION = re.compile(
    r'\b(en una|una nota|ayer|despu[eé]s|ambos|por la ma[nñ]ana|dice que|'
    r'ma[nñ]ana va|luego|finalmente|escribe su|pregunta c[oó]mo|'
    r'responde leyendo|seg[uú]n)\b',
    re.IGNORECASE,
)
SITUACION_GENERICA = re.compile(
    r'em uma situa[cç][aã]o real de atendimento|uma pessoa consulta um aviso|'
    r'ela precisa escolher uma op[cç][aã]o|o di[aá]logo informa claramente|'
    r'leia o di[aá]logo e responda conforme os dados',
    re.IGNORECASE,
)
# Alemán: palabras españolas frecuentes que no existen como palabra alemana
# (se evitan «die», «oder», «also», «es», «so», «den»: son alemán legítimo).
ESPANOL_EN_SITUACION_DE = re.compile(
    r'\b(el|la|los|las|que|pero|con|una|del|para|porque|tambi[eé]n|'
    r'despu[eé]s|luego|seg[uú]n|ayer|ma[nñ]ana|dice|pregunta|responde|'
    r'est[aá]|son|hay|muy|y)\b',
    re.IGNORECASE,
)
SITUACION_GENERICA_DE = re.compile(
    r'in einer (?:realen|allt[aä]glichen) situation|eine person liest eine nachricht|'
    r'lies den dialog und antworte|der dialog informiert|antworte nach den daten',
    re.IGNORECASE,
)
# Italiano: solo marcadores claramente españoles. «la», «che», «con», «per»,
# «come», «una», «del», «di», «dice», «son», «para» también son italiano y no
# cuentan; «pero» sin tilde no choca con «però» (la ò es parte de la palabra).
ESPANOL_EN_SITUACION_IT = re.compile(
    r'[ñ¿¡]|\b(el|los|las|pero|tambi[eé]n|est[aá]|qu[eé]|porque|muy|hay|ayer|'
    r'despu[eé]s|luego|seg[uú]n|ma[nñ]ana|pregunta|responde|usted|ustedes|'
    r'nosotros|hoy|gracias|hola|y)\b',
    re.IGNORECASE,
)
SITUACION_GENERICA_IT = re.compile(
    r'in una situazione (?:reale|quotidiana)|una persona legge un messaggio|'
    r'leggi il dialogo e rispondi|il dialogo informa|rispondi secondo i dati',
    re.IGNORECASE,
)
POR_IDIOMA = {
    # Valor por defecto = comportamiento histórico (pt; fr/es lo heredan sin cambios).
    'pt': {'lengua': 'pt-BR', 'espanol': ESPANOL_EN_SITUACION,
           'generica': SITUACION_GENERICA, 'c50': 'pt'},
    'de': {'lengua': 'alemán', 'espanol': ESPANOL_EN_SITUACION_DE,
           'generica': SITUACION_GENERICA_DE, 'c50': 'prueba'},
    'it': {'lengua': 'italiano', 'espanol': ESPANOL_EN_SITUACION_IT,
           'generica': SITUACION_GENERICA_IT, 'c50': 'prueba'},
}


def normalizar_firma(texto: str) -> str:
    """Quita numeración decorativa para descubrir plantillas disfrazadas."""
    texto = MAQUILLAJE.sub(' ', texto)
    texto = re.sub(r'\([^)]*\)', ' ', texto)
    texto = re.sub(r'\b\d+\b', '#', texto)
    return re.sub(r'\s+', ' ', texto).strip().lower()


def palabras(texto: str) -> list[str]:
    return [
        token.strip('.')
        for token in re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ@._-]+", texto.lower())
        if token.strip('.')
    ]


def normalizar_opcion(texto: str) -> str:
    return re.sub(r'\s+', ' ', texto).strip().strip('./').strip().lower()


def opciones_de(texto: str) -> dict[str, str]:
    """Extrae opciones A)–C) aunque estén separadas por barra o espacios."""
    marcas = list(re.finditer(r'(?<!\w)([A-C])\)\s*', texto))
    opciones: dict[str, str] = {}
    for indice, marca in enumerate(marcas):
        fin = marcas[indice + 1].start() if indice + 1 < len(marcas) else len(texto)
        valor = texto[marca.end():fin].strip().strip('/').strip()
        opciones[marca.group(1)] = valor
    return opciones


def pares_de(texto: str) -> list[tuple[str, str]]:
    pares: list[tuple[str, str]] = []
    for segmento in texto.split(';'):
        if '↔' not in segmento:
            continue
        izquierda, derecha = segmento.rsplit('↔', 1)
        pares.append((normalizar_opcion(izquierda), normalizar_opcion(derecha)))
    return pares


def main() -> None:
    idioma = sys.argv[1] if len(sys.argv) > 1 else 'pt'
    ruta = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / 'curriculo' / idioma / 'n1.json'
    parcial = '--parcial' in sys.argv[3:]
    conf = POR_IDIOMA.get(idioma, POR_IDIOMA['pt'])
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    clases = datos.get('clases', [])
    pendientes = 0
    if parcial:
        # Fichas aún sin plan de ejercicios: se validan cuando se planifiquen.
        planificadas = [x for x in clases if x.get('estado') != 'esqueleto' or x.get('ejercicios')]
        pendientes = len(clases) - len(planificadas)
        clases = planificadas
    nivel = datos.get('nivel')
    if not isinstance(nivel, int) and clases:
        coincidencia_nivel = re.fullmatch(
            rf'{re.escape(idioma)}\.n(\d+)\.c\d+', str(clases[0].get('id', ''))
        )
        if coincidencia_nivel:
            nivel = int(coincidencia_nivel.group(1))
    if not isinstance(nivel, int):
        nivel = 1
    outline_p = RAIZ / 'tools' / 'curriculo' / idioma / f'n{nivel}-outline.json'
    outline = json.loads(outline_p.read_text(encoding='utf-8'))
    errores: list[str] = []
    consignas: Counter[str] = Counter()
    ejemplos: Counter[str] = Counter()
    firmas: Counter[tuple[str, str, str]] = Counter()
    firmas_normalizadas: Counter[tuple[str, str, str]] = Counter()

    if not parcial and len(clases) != 50:
        errores.append(f'raíz: se esperan 50 clases, hay {len(clases)}')
    if not parcial and datos.get('previos') != outline.get('previos'):
        errores.append('raíz: previos distintos del outline aprobado')

    bases = {str(x.get('id')): x for x in outline.get('clases', [])}
    ids_vistos: set[str] = set()
    for indice, clase in enumerate(clases, 1):
        cid = str(clase.get('id', f'C{indice:02d}'))
        if cid in ids_vistos:
            errores.append(f'{cid}: id de clase repetido')
        ids_vistos.add(cid)
        base = bases.get(cid)
        if base is None:
            errores.append(f'{cid}: clase ausente del outline')
            continue
        for campo, valor in base.items():
            esperado = 'planificado' if campo == 'estado' else valor
            if clase.get(campo) != esperado:
                errores.append(f'{cid}: cambió el campo congelado {campo}')
        ejercicios = clase.get('ejercicios')
        if not isinstance(ejercicios, dict):
            errores.append(f'{cid}: faltan ejercicios')
            continue
        situacion = ejercicios.get('situacion')
        if not isinstance(situacion, dict):
            errores.append(f'{cid}: falta situación')
            situacion = {}
        texto = situacion.get('texto')
        if not isinstance(texto, str) or len(texto.split()) < 24:
            errores.append(f'{cid}: situación demasiado vaga')
        elif PROHIBIDAS.search(texto) or MAQUILLAJE.search(texto) or conf['generica'].search(texto):
            errores.append(f'{cid}: situación con texto plantilla')
        elif conf['espanol'].search(texto):
            errores.append(f'{cid}: situación no redactada íntegramente en {conf["lengua"]}')
        elif '\n' not in texto and texto.count('—') < 2 and texto.count(':') < 2:
            errores.append(f'{cid}: situación sin diálogo, mensaje, anuncio o datos concretos')

        grupos = (
            ('guiada', ejercicios.get('guiada'), 3, 3),
            ('independiente', ejercicios.get('independiente'), 3, 3),
            ('situacion', situacion.get('preguntas'), 1, 2),
            ('evaluacion', ejercicios.get('evaluacion'), 5, 8),
        )
        claves = set(clase.get('introduce', [])) | set(clase.get('recicla', []))
        ids_locales: set[tuple[str, str]] = set()
        evaluacion: list[dict] = []
        for grupo, items, minimo, maximo in grupos:
            if not isinstance(items, list) or not minimo <= len(items) <= maximo:
                cuantos = len(items) if isinstance(items, list) else 0
                errores.append(f'{cid}.{grupo}: {cuantos} ítems; se esperan {minimo}–{maximo}')
                items = items if isinstance(items, list) else []
            if grupo == 'evaluacion':
                evaluacion = items
            for n, item in enumerate(items, 1):
                donde = f'{cid}.{grupo}[{n}]'
                if not isinstance(item, dict):
                    errores.append(f'{donde}: ítem inválido')
                    continue
                formato = item.get('formato')
                consigna = item.get('consigna')
                ejemplo = item.get('ejemplo')
                if formato not in FORMATOS:
                    errores.append(f'{donde}: formato inválido {formato!r}')
                if item.get('clave') not in claves:
                    errores.append(f'{donde}: clave no disponible {item.get("clave")!r}')
                if not isinstance(consigna, str) or not consigna.strip():
                    errores.append(f'{donde}: falta consigna')
                    continue
                if formato == 'relacionar' and (
                    len(consigna.split()) < 5 or re.match(r'^\s*\d', consigna)
                ):
                    errores.append(f'{donde}: consigna de relacionar truncada o mecánica')
                if not isinstance(ejemplo, str) or '→' not in ejemplo:
                    errores.append(f'{donde}: ejemplo sin estímulo → respuesta')
                    continue
                if (PROHIBIDAS.search(consigna) or PROHIBIDAS.search(ejemplo)
                        or MAQUILLAJE.search(consigna) or MAQUILLAJE.search(ejemplo)):
                    errores.append(f'{donde}: contiene lenguaje plantilla/interno')
                for clave_visible in claves:
                    if '-' in clave_visible and (
                        clave_visible.lower() in consigna.lower()
                        or clave_visible.lower() in ejemplo.lower()
                    ):
                        errores.append(f'{donde}: expone la clave interna {clave_visible!r}')
                consignas[consigna] += 1
                ejemplos[ejemplo] += 1
                firmas[(str(formato), consigna, ejemplo)] += 1
                firmas_normalizadas[(
                    str(formato), normalizar_firma(consigna), normalizar_firma(ejemplo)
                )] += 1
                if (consigna, ejemplo) in ids_locales:
                    errores.append(f'{donde}: repite estímulo/respuesta dentro de la clase')
                ids_locales.add((consigna, ejemplo))

                previo = ejemplo.split('→', 1)[0]
                baja = consigna.lower()
                if formato == 'completar' and '___' not in previo:
                    errores.append(f'{donde}: completar sin hueco ___')
                elif formato in {'elegir', 'escuchar'}:
                    if formato == 'escuchar' and 'audio:' not in previo.lower():
                        errores.append(f'{donde}: escuchar sin audio')
                    opciones = opciones_de(previo)
                    if len(opciones) < 2 or len({normalizar_opcion(x) for x in opciones.values()}) < 2:
                        errores.append(f'{donde}: {formato} sin dos opciones reales y distintas')
                    else:
                        solucion = ejemplo.split('→', 1)[1].strip()
                        solucion_sin_letra = re.sub(r'^[A-C]\)\s*', '', solucion).strip()
                        valores = {normalizar_opcion(x) for x in opciones.values()}
                        if normalizar_opcion(solucion_sin_letra) not in valores:
                            errores.append(f'{donde}: la respuesta no coincide con ninguna opción')
                elif formato == 'ordenar':
                    coincidencia = re.search(r'\[([^]]+)\]', previo)
                    if not coincidencia:
                        errores.append(f'{donde}: ordenar sin tokens entre corchetes')
                    else:
                        origen = palabras(coincidencia.group(1).replace('/', ' '))
                        solucion = palabras(ejemplo.split('→', 1)[1])
                        if Counter(origen) != Counter(solucion):
                            errores.append(f'{donde}: la solución no es una permutación de los tokens')
                elif formato == 'relacionar':
                    solucion = ejemplo.split('→', 1)[1]
                    if not 3 <= previo.count('↔') <= 5:
                        errores.append(f'{donde}: estímulo de relacionar necesita 3–5 pares con ↔')
                    if not 3 <= solucion.count('↔') <= 5:
                        errores.append(f'{donde}: solución de relacionar necesita 3–5 pares correctos con ↔')
                    if solucion.strip().lower() in {
                        'respuesta indicada', 'la respuesta indicada', 'respuesta correcta'
                    }:
                        errores.append(f'{donde}: relacionar no explicita los pares correctos')
                    if normalizar_opcion(previo) == normalizar_opcion(solucion):
                        errores.append(f'{donde}: relacionar muestra la solución antes de responder')
                    pares_solucion = pares_de(solucion)
                    izquierdas = [x for x, _ in pares_solucion]
                    derechas = [x for _, x in pares_solucion]
                    if len(set(izquierdas)) != len(izquierdas) or len(set(derechas)) != len(derechas):
                        errores.append(f'{donde}: la solución de relacionar repite elementos')
                    previo_normalizado = normalizar_opcion(previo)
                    if any(x not in previo_normalizado or y not in previo_normalizado for x, y in pares_solucion):
                        errores.append(f'{donde}: la solución de relacionar inventa elementos')
                elif formato == 'escribir' and re.search(r'\b(escucha|elige|ordena|relaciona|completa)\b', baja):
                    errores.append(f'{donde}: consigna incompatible con escribir')
                elif formato == 'escribir':
                    solucion = ejemplo.split('→', 1)[1].strip()
                    if len(solucion.split()) >= 3 and normalizar_firma(solucion) in normalizar_firma(previo):
                        errores.append(f'{donde}: el estímulo de escribir ya entrega la respuesta')

        if len({x.get('formato') for x in evaluacion if isinstance(x, dict)}) < 3:
            errores.append(f'{cid}: evaluación con menos de 3 formatos')
        cubiertas = {x.get('clave') for x in evaluacion if isinstance(x, dict)}
        if set(clase.get('introduce', [])) - cubiertas:
            errores.append(f'{cid}: evaluación no cubre todas las claves nuevas')

    for etiqueta, contador in (('consigna', consignas), ('ejemplo', ejemplos), ('firma', firmas)):
        repetidos = sum(n - 1 for n in contador.values() if n > 1)
        total = sum(contador.values())
        if etiqueta in {'ejemplo', 'firma'} and repetidos:
            errores.append(f'raíz: {repetidos} {etiqueta}s exactos repetidos')
        elif total and (total - repetidos) / total < 0.85:
            errores.append(f'raíz: solo {(total - repetidos) / total:.1%} de {etiqueta}s únicos')

    repetidas_normalizadas = sum(n - 1 for n in firmas_normalizadas.values() if n > 1)
    if repetidas_normalizadas:
        errores.append(
            f'raíz: {repetidas_normalizadas} firmas repetidas tras quitar numeración decorativa'
        )

    clase_c50 = next((x for x in clases if x.get('id') == 'pt.n1.c50'), None)
    if conf['c50'] == 'prueba':
        # c50 genérica: prueba del nivel, sin claves nuevas y repasando el nivel.
        clase_c50 = None
        prueba = next((x for x in clases if str(x.get('id', '')).endswith('.c50')), None)
        if prueba is not None:
            ev = (prueba.get('ejercicios') or {}).get('evaluacion') or []
            claves_ev = {x.get('clave') for x in ev if isinstance(x, dict)}
            if prueba.get('introduce'):
                errores.append(f'{prueba["id"]}: la c50 es la prueba del nivel y no introduce claves')
            if len(ev) < 6 or len(claves_ev) < 5:
                errores.append(f'{prueba["id"]}: la prueba necesita ≥ 6 ítems de evaluación sobre ≥ 5 claves del nivel')
    if clase_c50 is not None:
        c50 = clase_c50.get('ejercicios', {}).get('evaluacion', [])
        requeridas = {
            'chamar-se', 'regular-present-transfer', 'age-ter', 'contact-spelling',
            'shopping-modal-transfer', 'routine-preferences', 'perfeito-irregular-core',
        }
        presentes = {x.get('clave') for x in c50 if isinstance(x, dict)}
        if len(c50) != 7 or not requeridas <= presentes:
            errores.append('pt.n1.c50: la evaluación no cubre las siete entradas A1')

    for error in errores:
        print('ERROR:', error)
    print(
        f'{len(errores)} errores · {len(clases)} clases · '
        f'{sum(consignas.values())} ejercicios · '
        f'{len(consignas)} consignas únicas · {len(ejemplos)} ejemplos únicos'
        + (f' · {pendientes} fichas en esqueleto sin validar' if pendientes else '')
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
