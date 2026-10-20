#!/usr/bin/env python3
"""Elenco por clase: assets/contenido/<idioma>/elenco_clases.json.

elenco.json (tools/voz/elenco.py) da una voz global a cada hablante. Algunos no
tienen género fijo: los apellidos japoneses (たなか es hombre en una clase y mujer
en otra), los oficios invariables (Policía, Recepcionista, Atendente, 服务员,
Dr. Weber…). Este script decide su voz CLASE A CLASE:

  {"ja.n3.c06": {"なかむら": "narrador"}, …}       (id de la unidad → hablante → rol)

La app (lib/core/elenco.dart) aplica: elenco de la clase → elenco global →
respaldo por orden de aparición, y después resuelve los choques del diálogo.

  python3 tools/voz/elenco_clases.py                 # los 10 idiomas
  python3 tools/voz/elenco_clases.py --idiomas ja,es
  python3 tools/voz/elenco_clases.py --informe       # no escribe; cuenta y lista
  python3 tools/voz/elenco_clases.py --revisar ja    # pruebas de cada decisión
  python3 tools/voz/elenco_clases.py --rehacer       # ignora lo ya escrito

Cómo se decide el género de un hablante sin entrada en elenco.json:
1. REVISADOS (abajo): decisiones revisadas a mano leyendo la clase. Mandan.
2. Heurísticas sobre la clase entera, sin tocar su texto:
   - contexto de la situación en español: artículo, título o nombre de pila
     junto al nombre o al oficio («el profesor Tanaka», «la recepcionista»,
     «una empleada», «Tanaka, su jefa», «su jefe, Yamamoto», «Megumi Kobayashi»);
   - contexto en inglés: Mr./Ms., «(a man)», «(a woman)», «in his fifties»…;
   - traducciones y texto de las líneas: «señora Tanaka», «Ms. Suzuki»,
     tratamiento en vocativo en un diálogo de dos («Sí, señor.», «Bienvenida.»,
     «a senhora»), concordancia propia («obrigada», «estoy cansada», «yo mismo»).
   Gana un género si sus pruebas pesan al menos el doble que las del otro. Si
   se contradicen o no hay ninguna, NO se asigna: queda el respaldo de la app
   (alterna narradora / narrador por orden de aparición). Los casos dudosos se
   miran con --revisar y, leída la clase, se anotan en REVISADOS.
3. Voz dentro del diálogo: los personajes con voz global la conservan; los
   nuevos toman, del más al menos hablador, la voz de su género que nadie usa
   en ese diálogo (narradora/narrador primero, luego mujer_b/hombre_b). Así dos
   personas distintas del mismo género no comparten voz. Con tres del mismo
   género (solo hay dos voces) se comparte la del que menos habla.
   «Paul und Mia» y «Lucía und Diego» (dos personas a coro) y «Plateia» (el
   público) reciben una voz de mujer libre (decisión de diseño: una sola voz
   para el coro).

Ejecútalo después de tools/voz/elenco.py (usa el elenco global para saber
quién ya tiene voz) y cada vez que cambien los diálogos de una ruta.

Idempotente: las entradas que ya están en elenco_clases.json se conservan
(también las editadas a mano) mientras el hablante siga en esa clase; se
añaden las nuevas y se quitan las de hablantes que ya no aparecen. Para
recalcular una (p. ej. tras añadirla a REVISADOS), bórrala del archivo o usa
--rehacer (que también descarta lo editado a mano fuera de REVISADOS).
"""
import argparse
import collections
import glob
import json
import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDIOMAS = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh']
F, M, CORO = 'f', 'm', 'coro'
VOCES = {F: ('narradora', 'mujer_b'), M: ('narrador', 'hombre_b')}

# ---------------------------------------------------------------------------
# Decisiones revisadas a mano: {idioma: {id de clase: {hablante: f | m | coro | None}}}.
# None = revisado y sin pista: queda sin asignar (respaldo de la app).
REVISADOS = {
    'de': {
        # Coros: una sola voz (de mujer) para las dos personas.
        'de.n1.c03': {'Paul und Mia': CORO},
        'de.n1.c05': {'Lucía und Diego': CORO},
        'de.n10.c44': {'Dr. Weber': M},  # Lena: «Der Arzt möchte wissen…»
    },
    'pt': {
        'pt.n10.c16': {'Plateia': CORO},  # el público
        'pt.n10.c19': {'Plateia': CORO},
        'pt.n5.c10': {'Cronista': M},  # «acordei atrasado»
        'pt.n7.c35': {'Agente': M},  # «un representante de la agencia»
    },
    'es': {
        'es.n1.c32': {'Recepcionista': F},  # «asks the Receptionist if she has seen him»
        'es.n10.c12': {'Turista': F},  # Emma: «hay una turista en la mesa»
        'es.n10.c15': {'Turista': F},  # «one of the tourists, a woman»; la Guía la llama «señora»
        'es.n10.c16': {'Gerente': F},  # «she uses usted with them»
        'es.n3.c10': {'Policía': M},  # «At the end he gives Emma a copy»
        'es.n3.c18': {'Taxista': M},  # el mismo taxista de n3.c19-c20 («Gracias, señor»)
        'es.n3.c19': {'Taxista': M},  # Emma: «Disculpe, señor»
        'es.n3.c20': {'Taxista': M},  # Emma: «Gracias, señor»
        'es.n3.c21': {'Agente': M},  # el mismo agente del mostrador de n3.c22
        'es.n3.c22': {'Agente': M},  # Emma y Daniela: «señor»
        'es.n4.c32': {'Recepcionista': F},  # «She uses usted with both of them»
        'es.n4.c46': {'Taxista': M},  # «Emma uses usted with him»
        'es.n8.c17': {'Guía': M},  # «Buenos días, señor»; «mi abuelo era baqueano y yo aprendí de él»
        'es.n8.c18': {'Recepcionista': F},  # Martina: «cómo dijo… si ella dice»
        'es.n8.c32': {'Guía': F},  # «Emma and Mateo use usted with her»
        'es.n8.c36': {'Agente': F},  # Emma: «la Agente me prometió…»
        'es.n9.c32': {'Policía': M},  # Conductor: «Hay un policía… Voy a hablar con él»
    },
    'ja': {
        'ja.f0.yukkuri': {'すずき': M},  # «le pide al empleado»
        'ja.f0.watashi-wa': {'たなか': M},  # «un profesor y una alumna» (ゆき)
        'ja.f0.hai-iie': {'すずき': F},  # «una compañera pregunta a otra»
        'ja.n2.c12': {'すずき': M},  # «el administrador»
        'ja.n2.c37': {'たなかさん': M},  # «un amigo… tú le preguntas a él»
        'ja.n2.c38': {'かとうさん': F},  # «La enfermera te dice» (ひろしさん eres tú)
        'ja.n3.c04': {'なかむら': M},  # «trasladarlo… qué decidió hacer él»
        'ja.n3.c09': {'かとう': M},  # «El policía de tráfico Katō»
        'ja.n4.c21': {'わたなべ': F},  # «qué es importante para ella»
        'ja.n4.c25': {'たなか': F},  # «Tanaka, operadora del centro de atención»
        'ja.n4.c48': {'たかはし': M},  # «donde lo atiende Yoshida»
        'ja.n5.c50': {'たかはしさん': M},  # «el examinador recibe a Ryō»
        'ja.n6.c16': {'たなか': M},  # «propone que lo contacten»
        'ja.n7.c12': {'たかはしさん': M},  # «El agente de tránsito Takahashi»
        'ja.n8.c04': {'すずき': M},  # «repite los datos para estar seguro»
        'ja.n9.c24': {'やまもと': M},  # «Nakamura lo invita»
        'ja.n9.c44': {'たかはし': F, 'なかむら': M},  # «Ella lleva horas esperando… Él se disculpa»
        'ja.n9.c45': {'やまもと': F},  # «Ella expresa su molestia»
        'ja.n2.c40': {'いとうさん': M},  # el farmacéutico («¿Qué te pasa?»)
        'ja.n3.c37': {'こばやし': F},  # Watanabe: «Kobayashi, te ves un poco ocupada»
        'ja.n4.c46': {'かとう': M},  # el policía: «¿No estás herido?»
        'ja.n6.c04': {'たなか': M},  # «Ahora vivo solo con mi esposa» (妻)
        'ja.n9.c50': {'たなか': M},  # el examinador: «avanza tú solo»
        'ja.n2.c39': {'よしださん': M},  # el entrenador («él te dice qué ejercicio…»)
    },
}

# ---------------------------------------------------------------------------
# Léxico de género (español e inglés: los idiomas de contexto y traducciones).
LEX_ES = {
    F: ('la una señora sra. sra doña dña. profesora doctora dra. maestra jefa compañera vecina amiga '
        'dependienta empleada encargada clienta directora madre mamá abuela esposa tía hermana hija mujer '
        'chica señorita mesera camarera cajera vendedora conductora coordinadora alumna enfermera médica '
        'abogada presentadora invitada moderadora mediadora entrevistadora secretaria supervisora '
        'organizadora diseñadora gerenta funcionaria pasajera viajera '
        'expositora oradora locutora entrenadora operadora administradora farmacéutica técnica mecánica '
        'examinadora candidata casera dueña presidenta ingeniera cocinera fotógrafa reparadora'),
    M: ('el un del al señor sr. sr don profesor doctor maestro jefe compañero vecino amigo empleado '
        'encargado director padre papá abuelo esposo marido tío hermano hijo hombre chico mesero camarero '
        'cajero vendedor conductor coordinador alumno enfermero médico abogado presentador invitado '
        'moderador mediador entrevistador secretario supervisor organizador diseñador funcionario '
        'pasajero viajero expositor orador locutor dependiente chofer chófer entrenador operador '
        'administrador farmacéutico técnico mecánico examinador candidato casero dueño presidente '
        'ingeniero cocinero fotógrafo reparador'),
}
LEX_EN = {
    F: 'mrs. mrs ms. ms miss woman lady waitress hostess actress policewoman saleswoman businesswoman '
       'mother grandmother aunt sister wife daughter girl madam',
    M: 'mr. mr man gentleman waiter actor policeman salesman businessman father grandfather uncle '
       'brother husband son boy sir',
}
LEX_ES = {g: set(v.split()) for g, v in LEX_ES.items()}
LEX_EN = {g: set(v.split()) for g, v in LEX_EN.items()}
# Palabras que cortan la búsqueda hacia atrás del artículo («la oficina de Tanaka»).
CORTE = set('de a con para por en que y e o ni le les lo se entre sobre hacia según mientras cuando si '
            'final principio fin rato día momento lado entonces luego después ahí allí aquí'.split())

# Nombres en el contexto (es/en) de cada hablante sin género: romanización de
# los apellidos japoneses y chinos, y oficio en español / inglés.
APELLIDOS_JA = {
    'たなか': 'Tanaka', '田中': 'Tanaka', 'すずき': 'Suzuki', '鈴木': 'Suzuki', 'わたなべ': 'Watanabe',
    '渡辺': 'Watanabe', 'たかはし': 'Takahashi', '高橋': 'Takahashi', 'いとう': 'Ito', '伊藤': 'Ito',
    'やまもと': 'Yamamoto', '山本': 'Yamamoto', 'なかむら': 'Nakamura', '中村': 'Nakamura',
    'こばやし': 'Kobayashi', '小林': 'Kobayashi', 'かとう': 'Kato', '加藤': 'Kato', 'よしだ': 'Yoshida',
    '吉田': 'Yoshida',
}
# Nombres de pila de la lista cerrada, romanizados: «Megumi Kobayashi» → mujer.
NOMBRES_JA = {F: 'sakura yuki aoi megumi yoko misaki ayaka nanako',
              M: 'kenta takuya yuta daisuke ryo shota hiroshi'}
NOMBRES_JA = {g: set(v.split()) for g, v in NOMBRES_JA.items()}
SUFIJO_JA = re.compile(r'(さん|ちゃん|くん|せんせい|ぶちょう)$')
# hablante (sin sufijo, en minúsculas) → (formas en español, formas en inglés)
OFICIOS = {
    'policía': ('policía agente oficial', 'police officer policeman policewoman'),
    'policial': ('policía policial agente', 'police officer policeman policewoman'),
    'oficial': ('oficial agente policía', 'officer'),
    'recepcionista': ('recepcionista', 'receptionist'),
    'receptionist': ('recepcionista', 'receptionist'),
    'turista': ('turista', 'tourist'),
    'agente': ('agente', 'agent'),
    'agente de seguros': ('agente', 'agent insurance agent'),
    'agente de control de pasaportes': ('agente', 'agent'),
    'taxista': ('taxista conductor conductora chofer', 'taxi driver driver'),
    'motorista': ('motorista conductor conductora chofer', 'driver bus driver'),
    'guía': ('guía', 'guide'),
    'guia': ('guía', 'guide'),
    'dentista': ('dentista', 'dentist'),
    'gerente': ('gerente', 'manager'),
    'asistente': ('asistente agente', 'assistant agent'),
    'visitante': ('visitante', 'visitor'),
    'visitante de estados unidos': ('visitante', 'visitor'),
    'visitante de la paz': ('visitante', 'visitor'),
    'representante': ('representante', 'representative'),
    'estudiante': ('estudiante alumno alumna', 'student'),
    'atendente': ('atendente dependiente dependienta empleado empleada vendedor vendedora cajero cajera',
                  'attendant clerk employee'),
    'cliente': ('cliente clienta', 'customer client guest'),
    'finalista': ('finalista', 'finalist'),
    'panelista': ('panelista', 'panelist'),
    'cronista': ('cronista', 'columnist'),
    'âncora': ('presentador presentadora', 'anchor'),
    'palestrante': ('invitada invitado conferencista ponente', 'speaker'),
    'participante': ('participante', 'participant'),
    'barista': ('barista', 'barista'),
    'てんいん': ('dependiente dependienta empleado empleada vendedor vendedora cajero cajera',
               'clerk shop assistant employee'),
    'おきゃくさん': ('cliente clienta visitante', 'customer guest'),
    '服务员': ('mesero mesera camarero camarera dependiente dependienta', 'waiter waitress server'),
    '交警': ('agente policía', 'traffic officer officer'),
}
OFICIOS = {k: (v[0].split(), v[1].split()) for k, v in OFICIOS.items()}
ROM_ZH = {'王': 'Wang', '刘': 'Liu'}
TITULO_ZH = {'老师': ('profesor profesora maestro maestra', 'teacher')}
# Tratamientos en el texto y las traducciones de las líneas.
TRATO = {
    F: r"señora|señorita|doña|senhora|dona|madame|signora|ma'am|madam|bienvenida",
    M: r"señor|caballero|senhor|monsieur|signore|signor|sir|bienvenido",
}
# Solo en vocativo («Gracias, señora.», «Bienvenida.», «Sí, señor García.») o como tratamiento
# de usted en portugués («a senhora», «o senhor»): «una señora que estaba a su
# lado» habla de otra persona.
TRATO = {g: re.compile(rf"(?:^|[,;:¡¿!?.]\s*)(?:{t})(?:\s+[A-ZÁÉÍÓÚ][\w-]+)?\s*(?=[,;:.!?]|$)"
                       rf"|\b{'a senhora' if g == F else 'o senhor'}\b(?!\s+(?-i:[A-ZÁÉÍÓÚ]))", re.I)
         for g, t in TRATO.items()}
# Concordancia del propio hablante (texto o traducción): «obrigada», «estoy cansada».
ADJ = ('cansad preocupad ocupad nervios segur content emocionad sorprendid confundid aburrid enojad '
       'agradecid interesad decepcionad apenad avergonzad equivocad encantad satisfech convencid dispuest '
       'obligad casad solter nuev agotad enferm list orgullos asustad tranquil molest perdid').replace(' ', '|')
VERBO = r"(?:estoy|estaba|estuve|soy|era|fui|quedé|me quedé|me siento|me sentí|me sentía|sigo|ando)"
GRADO = r"(?:muy |tan |un poco |bastante |algo |realmente |tan |)"
PROPIO = {g: re.compile(rf"\b(?:{pt}|{VERBO} {GRADO}(?:{ADJ}){v}|yo mism{v})\b", re.I)
          for g, pt, v in ((F, 'obrigada|encantada|ravie|enchantée', 'a'),
                           (M, 'obrigado|encantado|ravi|enchanté', 'o'))}


def sin_acentos(s):
    """Sin tildes (Itō → Ito, Liú → Liu), pero conserva la ñ (señora)."""
    s = s.replace('ñ', '\0').replace('Ñ', '\1')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.replace('\0', 'ñ').replace('\1', 'Ñ')


def claves(h):
    """(nombres propios, oficios en español, oficios en inglés) con que el
    contexto puede mencionar a `h`."""
    nombres, es, en = {h}, [], []
    raiz = SUFIJO_JA.sub('', h)
    if raiz in APELLIDOS_JA:
        nombres.add(APELLIDOS_JA[raiz])
        if h.endswith('せんせい'):
            es += 'profesor profesora maestro maestra doctor doctora'.split()
            en += ['teacher', 'doctor']
        if h.endswith('ぶちょう'):
            es += ['jefe', 'jefa', 'gerente', 'director', 'directora']
            en += ['manager', 'boss', 'department head']
    partes = h.split()
    if len(partes) == 2 and partes[0] in ROM_ZH:
        nombres.add(ROM_ZH[partes[0]])
        e, i = TITULO_ZH.get(partes[1], ('', ''))
        es += e.split()
        en += i.split()
    clave = re.sub(r'\s*\(.*\)$', '', h).lower()
    if clave in OFICIOS:
        es += OFICIOS[clave][0]
        en += OFICIOS[clave][1]
    if not nombres - {h} and clave not in OFICIOS and h not in OFICIOS:
        # Nombre propio o apellido suelto («Almeida», «Paredes», «Camille», «Dr. Weber»).
        nombres.add(re.sub(r'^(Dr\.|Maître)\s+', '', h))
    return nombres, es, en


def tokens(texto):
    return re.findall(r"[\w.'’]+|[^\w\s]", texto or '')


def pruebas_contexto_es(texto, nombres, oficios):
    """Artículos / títulos junto a la mención de `h` en el contexto en español."""
    res = []
    if not texto:
        return res
    t = tokens(texto)
    norm = [sin_acentos(x).lower().rstrip('.') for x in t]
    nombres_n = {sin_acentos(n).lower() for n in nombres}
    oficios_n = {sin_acentos(o).lower() for o in oficios}
    for i, w in enumerate(norm):
        es_nombre = w in nombres_n or (i + 1 < len(norm) and f'{w} {norm[i + 1]}' in nombres_n)
        es_oficio = w in oficios_n
        if not (es_nombre or es_oficio):
            continue
        # Nombre de pila japonés delante del apellido («Megumi Kobayashi»).
        if es_nombre and i > 0:
            for g in (F, M):
                if norm[i - 1] in NOMBRES_JA[g]:
                    res.append((g, 3, f'contexto: «{t[i - 1]} {t[i]}»'))
        # La propia forma del oficio puede fijar el género (empleada, mesero).
        if es_oficio:
            for g in (F, M):
                if t[i].lower() in LEX_ES[g] and t[i].lower() not in ('la', 'el', 'un', 'una', 'del', 'al'):
                    res.append((g, 3, f'contexto: «{t[i]}»'))
        # Hacia atrás: hasta 3 palabras en la misma frase.
        for j in range(i - 1, max(-1, i - 4), -1):
            p = t[j].lower()
            if not re.match(r"\w", p) or p in CORTE or (j < i - 1 and t[j][:1].isupper() and j > 0
                                                           and not t[j - 1].endswith('.')):
                break  # puntuación, preposición, «Al final Itō» u otro nombre propio
            g = F if p in LEX_ES[F] else M if p in LEX_ES[M] else None
            if g:
                res.append((g, 3, f'contexto: «{" ".join(t[j:i + 1])}»'))
                break
            if p.endswith('.'):
                break  # fin de frase («… un árbol. Maître Fontaine»)
        # Aposición: «Tanaka, su jefa,» / «Tanaka, la profesora».
        # «su jefa, Katō» / «el encargado, Watanabe-san»: el cargo va antes de la coma.
        if es_nombre and i >= 2 and t[i - 1] == ',':
            for g in (F, M):
                if t[i - 2].lower() in LEX_ES[g] - {'la', 'una', 'el', 'un', 'del', 'al'}:
                    res.append((g, 3, f'contexto: «{" ".join(t[max(0, i - 3):i + 1])}»'))
        if es_nombre:
            # «Nakamura-san, la empleada»: salta el sufijo japonés.
            while i + 2 < len(t) and t[i + 1] == '-' and t[i + 2].lower() in ('san', 'sensei', 'kun', 'chan'):
                i += 2
        # «Weber, el señor Wolf y …» es una lista, no una aposición.
        enumeracion = i + 4 < len(t) and t[i + 4][:1].isupper() and not t[i + 3].endswith('.')
        if es_nombre and i + 3 < len(t) and t[i + 1] == ',' and not enumeracion:
            p1, p2 = t[i + 2].lower(), t[i + 3].lower()
            for g in (F, M):
                if p1 in ('la', 'una', 'el', 'un') and p1 in LEX_ES[g]:
                    res.append((g, 3, f'contexto: «{" ".join(t[i:i + 4])}»'))
                elif p1 in ('su', 'mi', 'tu', 'nuestra', 'nuestro') and p2 in LEX_ES[g]:
                    res.append((g, 3, f'contexto: «{" ".join(t[i:i + 4])}»'))
    return res


def pruebas_contexto_en(texto, nombres, oficios):
    res = []
    if not texto:
        return res
    nombres_n = '|'.join(re.escape(sin_acentos(n)) for n in nombres if re.match(r'[A-Za-z]', sin_acentos(n)))
    llano = sin_acentos(texto)
    if nombres_n:
        for m in re.finditer(rf"\b(Mr|Mrs|Ms|Miss)\.?\s+({nombres_n})\b", llano):
            res.append((M if m.group(1) == 'Mr' else F, 3, f'contexto: «{m.group(0)}»'))
    ofi = '|'.join(re.escape(o) for o in sorted(oficios, key=len, reverse=True))
    if ofi:
        for m in re.finditer(rf"\b({ofi})\b[^.;]{{0,30}}?\((a|an) (man|woman)\b", llano, re.I):
            res.append((F if m.group(3).lower() == 'woman' else M, 3, f'contexto: «{m.group(0)}»'))
        for m in re.finditer(rf"\b({ofi})\b,? (in|of) (his|her) (twenties|thirties|forties|fifties|sixties|seventies)",
                             llano, re.I):
            res.append((F if m.group(3).lower() == 'her' else M, 3, f'contexto: «{m.group(0)}»'))
    for o in oficios:
        if o.lower() in LEX_EN[F] | LEX_EN[M] and re.search(rf"\b{re.escape(o)}\b", llano, re.I):
            g = F if o.lower() in LEX_EN[F] else M
            res.append((g, 2, f'contexto: «{o}»'))
    return res


def pruebas_lineas(h, dialogo, nombres):
    """Tratamientos con el nombre en traducciones/texto, tratamiento en un diálogo
    de dos y concordancia propia."""
    res = []
    nombres_n = [sin_acentos(n) for n in nombres]
    hablantes = {l['hablante'] for l in dialogo}
    for l in dialogo:
        textos = [l.get('texto') or ''] + [v for v in (l.get('traduccion') or {}).values() if isinstance(v, str)]
        for tx in textos:
            llano = sin_acentos(tx)
            for n in nombres_n:
                if not n or not re.match(r'\w', n):
                    continue
                for m in re.finditer(rf"\b(señora|señor|sra\.|sr\.|profesora|profesor|doctora|doctor|dra\.|"
                                     rf"Mrs\.|Ms\.|Mr\.|senhora|senhor|madame|monsieur|signora|signor)\s+{re.escape(n)}\b",
                                     llano, re.I):
                    t = m.group(1).lower()
                    g = F if t in ('señora', 'sra.', 'profesora', 'doctora', 'dra.', 'mrs.', 'ms.', 'senhora',
                                   'madame', 'signora') else M
                    res.append((g, 3, f'línea: «{m.group(0)}»'))
            if l['hablante'] == h:
                for g in (F, M):
                    if PROPIO[g].search(tx):
                        res.append((g, 2, f'propia: «{PROPIO[g].search(tx).group(0)}»'))
            elif len(hablantes) == 2 and l['hablante'] != h:
                for g in (F, M):
                    m = TRATO[g].search(llano)
                    if m:
                        res.append((g, 2, f'trato {g}: «{m.group(0).strip(" ,.")}» ({l["hablante"]})'))
    return res


def unidades(idioma):
    for f in sorted(glob.glob(os.path.join(RAIZ, 'assets', 'contenido', idioma, 'ruta', '*.json'))):
        try:
            datos = json.load(open(f, encoding='utf8'))
        except (OSError, ValueError):
            continue
        for u in datos.get('unidades', []) if isinstance(datos, dict) else []:
            for p in u.get('pasos', []):
                dialogo = [l for l in p.get('dialogo', []) or []
                           if isinstance(l, dict) and isinstance(l.get('hablante'), str) and 'texto' in l]
                if dialogo:
                    yield u, p, dialogo


def inferir(h, u, p, dialogo, global_):
    """(género o None, pruebas)."""
    nombres, es, en = claves(h)
    ctx = p.get('contexto') or {}
    pruebas = pruebas_contexto_es(ctx.get('es'), nombres, es)
    pruebas += pruebas_contexto_en(ctx.get('en'), nombres, en + es)  # «the Gerente (a man)»
    pruebas += pruebas_lineas(h, dialogo, nombres)
    peso = collections.Counter()
    for g, w, _ in pruebas:
        peso[g] += w
    for g, o in ((F, M), (M, F)):
        # Gana un género si sus pruebas pesan al menos el doble que las del otro;
        # si no, contradicción: queda sin asignar (a revisar).
        if peso[g] >= 2 and peso[g] >= 2 * peso[o]:
            return g, pruebas
    return None, pruebas


def voces_del_dialogo(hablantes, elenco):
    """Copia de vocesDelDialogo (lib/core/elenco.dart) para comprobar choques."""
    otra = {'narradora': 'mujer_b', 'mujer_b': 'narradora', 'narrador': 'hombre_b', 'hombre_b': 'narrador'}
    orden = []
    for h in hablantes:
        if h and h not in orden:
            orden.append(h)
    usadas, voces = set(), {}
    for i, h in enumerate(orden):
        rol = elenco.get(h) or ('narradora' if i % 2 == 0 else 'narrador')
        if rol in usadas and otra.get(rol) and otra[rol] not in usadas:
            rol = otra[rol]
        voces[h] = rol
        usadas.add(rol)
    return voces


def procesar(idioma, existente, revisar=False):
    ruta_global = os.path.join(RAIZ, 'assets', 'contenido', idioma, 'elenco.json')
    global_ = json.load(open(ruta_global, encoding='utf8')) if os.path.exists(ruta_global) else {}
    revisados = REVISADOS.get(idioma, {})
    salida, informe = {}, {'lineas': 0, 'sin_voz_antes': 0, 'sin_voz_despues': 0, 'conservadas': 0,
                           'revisadas': 0, 'heuristica': 0, 'sin_asignar': [], 'choques': []}
    for u, p, dialogo in unidades(idioma):
        uid = u.get('id')
        lineas = collections.Counter(l['hablante'] for l in dialogo)
        presentes = set(lineas)
        clase = {h: r for h, r in (existente.get(uid) or {}).items() if h in presentes}
        informe['conservadas'] += len(clase)
        generos = {}
        for h in sorted(presentes - set(global_) - set(clase), key=lambda x: (-lineas[x], x)):
            if h in revisados.get(uid, {}):
                g, pr = revisados[uid][h], [('?', 0, 'REVISADOS')]
                informe['revisadas'] += 1
            else:
                g, pr = inferir(h, u, p, dialogo, global_)
                informe['heuristica'] += g is not None
            if revisar:
                print(f'{uid}\t{h}\t{g}\t' + ' | '.join(d for _, _, d in pr))
            if g is None:
                informe['sin_asignar'].append(f'{uid} {h}')
            else:
                generos[h] = g
        # Voz: los de voz fija (global o ya en el archivo) la conservan; los nuevos
        # toman la libre de su género, del más al menos hablador.
        fijos = {**global_, **clase}
        voz_de = voces_del_dialogo([l['hablante'] for l in dialogo if l['hablante'] in fijos], fijos)
        for h in sorted(generos, key=lambda x: (-lineas[x], x)):
            g = generos[h]
            opciones = VOCES[F] if g == CORO else VOCES[g]
            libre = [r for r in opciones if r not in voz_de.values()]
            if libre:
                rol = libre[0]
            else:
                # Tres personas del mismo género y solo dos voces: comparte la del
                # que menos habla.
                rol = min((o for o in voz_de if voz_de[o] in opciones), key=lambda o: (lineas[o], o))
                rol = voz_de[rol]
            clase[h] = rol
            voz_de[h] = rol
        if clase:
            salida[uid] = dict(sorted(clase.items(), key=lambda kv: (-lineas[kv[0]], kv[0])))
        voces = voces_del_dialogo([l['hablante'] for l in dialogo], {**global_, **clase})
        por_voz = collections.defaultdict(list)
        for h, r in voces.items():
            por_voz[r].append(h)
        for r, hs in por_voz.items():
            if len(hs) > 1 and r != 'lumo' and set(hs) & set(clase):
                informe['choques'].append(f'{uid} {r}: {", ".join(hs)}')
        for l in dialogo:
            informe['lineas'] += 1
            informe['sin_voz_antes'] += l['hablante'] not in global_
            informe['sin_voz_despues'] += l['hablante'] not in global_ and l['hablante'] not in clase
    return salida, informe


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--idiomas', default=','.join(IDIOMAS))
    ap.add_argument('--informe', action='store_true', help='no escribe; solo muestra el resultado')
    ap.add_argument('--rehacer', action='store_true', help='ignora elenco_clases.json existente')
    ap.add_argument('--revisar', metavar='IDIOMA', help='lista cada decisión con sus pruebas (no escribe)')
    args = ap.parse_args()
    idiomas = [args.revisar] if args.revisar else args.idiomas.split(',')
    resumen = {}
    for idioma in idiomas:
        ruta = os.path.join(RAIZ, 'assets', 'contenido', idioma, 'elenco_clases.json')
        existente = {}
        if os.path.exists(ruta) and not args.rehacer:
            existente = json.load(open(ruta, encoding='utf8'))
        salida, informe = procesar(idioma, existente, revisar=bool(args.revisar))
        n = max(informe['lineas'], 1)
        informe['sin_voz_antes'] = f"{informe['sin_voz_antes']} ({100 * informe['sin_voz_antes'] / n:.1f} %)"
        informe['sin_voz_despues'] = f"{informe['sin_voz_despues']} ({100 * informe['sin_voz_despues'] / n:.1f} %)"
        resumen[idioma] = informe
        if not args.informe and not args.revisar:
            with open(ruta, 'w', encoding='utf8') as f:
                json.dump(salida, f, ensure_ascii=False, indent=1)
                f.write('\n')
    if not args.revisar:
        print(json.dumps(resumen, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
