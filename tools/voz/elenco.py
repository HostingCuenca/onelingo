#!/usr/bin/env python3
"""Elenco de voces por idioma: assets/contenido/<idioma>/elenco.json.

Cada hablante de los diálogos («hablante» en dialogo[]) recibe un rol de voz:
narradora, narrador, mujer_b, hombre_b o lumo (backend/src/lib/voz.ts, NATIVAS).

  python3 tools/voz/elenco.py                 # los 10 idiomas
  python3 tools/voz/elenco.py --idiomas ja,zh
  python3 tools/voz/elenco.py --informe       # no escribe; solo cuenta

Reglas (en este orden):
1. «Lumo» → lumo. «Tú» (el alumno) → narradora (es la voz que modela lo que dirá el
   alumno; si en el diálogo ya habla otra mujer con esa voz, la app la cambia).
   Documentos y avisos (artículo, correo, Durchsage, Aviso…) → narradora.
2. Género por título (Herr/Frau, Monsieur/Madame, Seu/Dona, Signor/Signora,
   Don/Doña, Dra.), patronímico ruso (-ич / -на), artículo o terminación del
   oficio (Kellnerin, vendedora, la/une, L’employée) y listas de nombres (las de
   tools/ia/idiomas/<idioma>.md y los nombres frecuentes del contenido).
3. Dentro de cada género, narradora/mujer_b (o narrador/hombre_b) por coloreo
   estable: de más a menos líneas, cada hablante toma la voz que menos comparte
   diálogo con los ya asignados, para que dos mujeres de un mismo diálogo suenen
   distintas. Además, la app resuelve en cada diálogo los choques que queden
   (lib/core/elenco.dart).
4. Lo que no se puede inferir con seguridad (apellidos japoneses, «Dr. Weber»,
   «Turista», «Paul und Mia») NO entra: la app aplica el respaldo por orden de
   aparición en el diálogo (alterna narradora / narrador).

Idempotente: las entradas que ya existen en elenco.json se conservan (también
las corregidas a mano) y solo se añaden hablantes nuevos. Para recalcular una,
bórrala del archivo y vuelve a ejecutar.
"""
import argparse
import collections
import glob
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDIOMAS = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh']
F, M, LUMO, TU, DOC = 'f', 'm', 'lumo', 'tu', 'doc'

TU_NOMBRES = {'tú', 'tu', 'you', 'du', 'você', 'ты', 'вы', 'あなた', 'わたし', '你', '我', '너', '나'}

# Nombres de pila. Las listas cerradas de ja, ko, ru y zh vienen de tools/ia/idiomas/<idioma>.md.
NOMBRES = {
    'en': {F: 'Mia Ana Sara Luna Rita Mar Sol Mamá Emma Lucía', M: 'Leo Tom Carlos Papá'},
    'es': {F: 'Emma Daniela Sofía Inés Valentina Rosa Martina Lucía Ana Carmen Mamá Abuela Chica',
           M: 'Mateo Kenji Andrés Jorge Tom Carlos Papá Abuelo Chico'},
    'fr': {F: 'Ana Léa Emma Chloé Sophie Aïssatou Inès Margaux Élodie Secretaria Profesora Vendedora',
           M: 'Hugo Karim Lucas Léo Clément Bastien Mateo Martin Mathieu Olivier Julien Thomas Paul Camarero Señor'},
    'de': {F: 'Anna Lena Mia Lea Sara Nina Eva Ana Anja Lara Mara Sofía Carla Carmen Lucía Sophie Oma Mutter Tante',
           M: 'Jonas Tom Tim Max Paul Felix Ben Jan Kai Leo Carlos Diego Opa Onkel Vater'},
    'pt': {F: ('Camila Ana Iara Yasmin Bia Renata Larissa Carolina Luana Júlia Gloria Helga Joana Elaine Valentina '
               'Lia Marta Sônia Wanda Daniela Carla Natalia Patrícia Fernanda Paula Valeria Elisa Letícia Beatriz '
               'Silvana Luciana Marcela Michele'),
           M: ('Lucas Bruno Tomás Diego Rafael Otávio Rui Henrique Marcos Nilton Murilo Davi Jaime Jonas Thiago '
               'Fábio Gustavo Caio Rodrigo Lauro Felipe Mateus Heitor Luis Paulo Ivo Leo Moacir Tiago')},
    'it': {F: 'Elena Chiara Francesca Sara Martina Sofia Giulia Anna', M: 'Davide Matteo Alessandro Paolo Giorgio Luca Marco'},
    'ru': {F: 'Анна Мария Елена Ольга Наталья Татьяна Ирина Светлана', M: 'Иван Александр Дмитрий Сергей Андрей Михаил Максим'},
    'ko': {F: '김지은 박서연 최민지 정수빈 강하윤 조예린 윤소희 장유진 마리아', M: '김민준 박도윤 최지훈 정현우 강준호 홍성민 송동현'},
    'ja': {F: 'さくら ゆき あおい めぐみ ようこ みさき あやか ななこ', M: 'けんた たくや ゆうた だいすけ りょう しょうた ひろし'},
    'zh': {F: '王芳 李梅 张丽 刘敏 陈静 杨雪 黄婷 周英', M: '赵伟 吴强 王磊 李涛 张浩 刘军 陈亮'},
}
NOMBRES = {i: {g: set(v.split()) for g, v in d.items()} for i, d in NOMBRES.items()}
# Apellidos sueltos que la terminación confundiría («Almeida» no es femenino).
APELLIDOS = {'pt': {'Almeida'}, 'es': {'Paredes'}}

# Títulos y palabras que fijan el género cuando abren el nombre.
TITULOS = {
    'es': {F: 'doña señora sra. dra. doctora mamá abuela otra primera segunda una la', M: 'don señor sr. dr. papá abuelo otro primer primero segundo un el'},
    'fr': {F: 'madame mme la une', M: 'monsieur m. le un'},
    'de': {F: 'frau oma mutter tante', M: 'herr opa vater onkel'},
    'pt': {F: 'dona senhora sra. dra. doutora a uma', M: 'seu senhor sr. dr. doutor o um'},
    'it': {F: 'signora la una', M: 'signor signore il un lo'},
    'en': {F: 'mrs. ms. miss', M: 'mr.'},
}
TITULOS = {i: {g: set(v.split()) for g, v in d.items()} for i, d in TITULOS.items()}

# Documentos, avisos e instituciones: los lee la narradora.
DOCS = re.compile(
    r"^(?:l[ea] |l[’']|les |un |une |o |a )?(?:(?:premier|première|deuxième|troisième|second|seconde) )?(?:article|courriel|courrier|rapport|dépliant|annonce|note|notes|rédaction|"
    r"procès-verbal|récit|conditions|contrat|règlement|chronique|quotidien|hebdo|journal|message|notice|version|fiche|"
    r"panneau|offre|brochure|lettre|ordonnance|agence|préfecture|compagnie|serveur vocal|voix off|première version|"
    r"premier message|réponse|deuxième panneau|troisième panneau|"
    r"durchsage|zeitungsartikel|aushang|aviso|e-mail|artigo|anúncio|painel|insumo|notícia|companhia|mensagem|folheto|"
    r"biografia|lista|notificação|edital|poema|coluna|resposta|registro|coordenação|acta|voz de megafonía|recepción)\b",
    re.I)

# Oficios con terminación ambigua (no se infieren: respaldo de la app).
AMBIGUOS = re.compile(r"(ista|ante|ente|policía|guía|guia|âncora|cliente|oficial|receptionist|policial|plateia)$", re.I)
# Oficios cuyo género gramatical es claro aunque no termine en -a/-o.
OFICIOS = {
    'de': {M: 'polizist verkäufer kellner dozent erzähler zeuge zugbegleiter sanitäter kunde rezeptionist techniker'},
    'ru': {F: 'сотрудница продавщица', M: 'продавец администратор преподаватель'},
    'it': {F: 'commessa cameriera impiegata', M: 'commesso cameriere impiegato'},
    'es': {M: 'chofer conductor actor presidente', F: 'actriz'},
    'pt': {M: 'garçom'},
    'en': {M: 'mesero', F: 'mesera'},
}
OFICIOS = {i: {g: set(v.split()) for g, v in d.items()} for i, d in OFICIOS.items()}


def base(nombre):
    """Sin anotaciones entre paréntesis: «Paul Brandt (E-Mail)» → «Paul Brandt»."""
    return re.sub(r'\s*[(（][^)）]*[)）]', '', nombre).strip()


def por_terminacion(palabra, idioma):
    p = palabra.lower()
    if AMBIGUOS.search(p):
        return None
    if idioma == 'de':
        return F if p.endswith('in') and len(p) > 4 else None
    if idioma == 'fr':
        if p.endswith(('ée', 'trice', 'esse', 'euse', 'ière', 'ienne', 'erte', 'ante')):
            return F
        if p.endswith(('é', 'eur', 'ent', 'ert', 'ier', 'ien', 'oncle', 'ant')) or p in ('agent', 'invité'):
            return M
        return None
    if idioma in ('es', 'pt', 'it'):
        if p.endswith(('ora', 'era', 'iva', 'ia', 'ña', 'ga', 'da', 'ta', 'na', 'ca', 'sa', 'ra', 'la', 'ma', 'essa')):
            return F
        if p.endswith(('o', 'or', 'ero', 'ário', 'ario', 'ño', 'ere', 'ore')):
            return M
    return None


def genero(nombre, idioma):
    """f, m, lumo, tu, doc o None (sin inferencia segura)."""
    n = base(nombre)
    bajo = n.lower()
    if bajo == 'lumo':
        return LUMO
    if bajo in TU_NOMBRES:
        return TU
    if DOCS.search(n):
        return DOC
    if re.search(r'\b(und|y|e|et|and)\b|&', n) and idioma not in ('ja', 'zh', 'ko'):
        return None  # dos personas a la vez
    if n in APELLIDOS.get(idioma, ()):
        return None
    nombres = NOMBRES.get(idioma, {})
    compacto = n.replace(' ', '')
    for g in (F, M):
        if n in nombres.get(g, ()) or compacto in nombres.get(g, ()):
            return g
    if idioma == 'ja':
        # «ひろしさん» → nombre de pila conocido; apellidos y せんせい/ぶちょう: sin género.
        raiz = re.sub(r'(さん|ちゃん|くん|せんせい|ぶちょう)$', '', n)
        for g in (F, M):
            if raiz in nombres.get(g, ()):
                return g
        return None
    if idioma == 'ru':
        partes = n.split()
        if len(partes) > 1:
            if re.search(r'(вич|ич)$', partes[-1]):
                return M
            if re.search(r'(вна|чна|ична)$', partes[-1]):
                return F
        for g in (F, M):
            if partes[0] in nombres.get(g, ()) or bajo in OFICIOS['ru'].get(g, ()):
                return g
        return None
    palabras = re.split(r"\s+|(?<=[’'])", n)
    primera = palabras[0].lower()
    for g in (F, M):
        if primera in TITULOS.get(idioma, {}).get(g, ()):
            # «Frau Dr. Weber», «La professeure Lambert», «Le directeur», «Una invitada».
            return g
        if palabras[0] in nombres.get(g, ()):
            return g  # «Anna Berger», «Inés Cárdenas»
        if primera in OFICIOS.get(idioma, {}).get(g, ()):
            return g
    if idioma == 'fr' and primera in ("l’", "l'") and len(palabras) > 1:
        return por_terminacion(palabras[1], idioma)
    g = por_terminacion(palabras[0], idioma)
    if g is None and idioma in ('es', 'pt', 'it') and len(palabras) > 1 and palabras[1].lower() not in ('de', 'do', 'da', 'di', 'del'):
        g = por_terminacion(palabras[1], idioma)  # «Agente inmobiliaria»
    return g


def dialogos(idioma):
    """Listas de líneas {hablante, texto} de todo el contenido del idioma."""
    salida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, 'assets', 'contenido', idioma, '**', '*.json'), recursive=True)):
        if os.path.basename(f) == 'elenco.json':
            continue
        try:
            datos = json.load(open(f, encoding='utf8'))
        except (OSError, ValueError):
            continue

        def recorrer(x):
            if isinstance(x, list):
                lineas = [e['hablante'] for e in x if isinstance(e, dict) and isinstance(e.get('hablante'), str) and 'texto' in e]
                if lineas:
                    salida.append(lineas)
                for e in x:
                    recorrer(e)
            elif isinstance(x, dict):
                for v in x.values():
                    recorrer(v)
        recorrer(datos)
    return salida


def asignar(idioma, existente):
    dias = dialogos(idioma)
    lineas = collections.Counter(h for d in dias for h in d)
    juntos = collections.Counter()
    for d in dias:
        hs = sorted(set(d))
        for i, a in enumerate(hs):
            for b in hs[i + 1:]:
                juntos[(a, b)] += 1
                juntos[(b, a)] += 1
    elenco = dict(existente)
    informe = {'hablantes': len(lineas), 'conservados': 0, 'por_regla': 0, 'sin_inferir': []}
    voces = {F: ('narradora', 'mujer_b'), M: ('narrador', 'hombre_b')}
    carga = collections.Counter()  # líneas por rol, para equilibrar empates
    for h, r in elenco.items():
        carga[r] += lineas.get(h, 0)
    for h, _ in sorted(lineas.items(), key=lambda kv: (-kv[1], kv[0])):
        if h in elenco:
            informe['conservados'] += 1
            continue
        if base(h) != h and base(h) in elenco:
            # «Camila (reflexão)», «Herr Wolf (E-Mail)»: la misma voz que el personaje.
            elenco[h] = elenco[base(h)]
            informe['por_regla'] += 1
            continue
        g = genero(h, idioma)
        if g is None:
            informe['sin_inferir'].append(h)
            continue
        informe['por_regla'] += 1
        if g == LUMO:
            rol = 'lumo'
        elif g in (TU, DOC):
            rol = 'narradora'
        else:
            a, b = voces[g]
            peso = {r: sum(juntos[(h, o)] for o, ro in elenco.items() if ro == r) for r in (a, b)}
            rol = min((a, b), key=lambda r: (peso[r], carga[r], r != a))
        elenco[h] = rol
        carga[rol] += lineas[h]
    orden = {h: i for i, (h, _) in enumerate(sorted(lineas.items(), key=lambda kv: (-kv[1], kv[0])))}
    elenco = dict(sorted(elenco.items(), key=lambda kv: (orden.get(kv[0], len(orden)), kv[0])))
    return elenco, informe


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--idiomas', default=','.join(IDIOMAS))
    ap.add_argument('--informe', action='store_true', help='no escribe; solo muestra el resultado')
    args = ap.parse_args()
    resumen = {}
    for idioma in args.idiomas.split(','):
        ruta = os.path.join(RAIZ, 'assets', 'contenido', idioma, 'elenco.json')
        existente = json.load(open(ruta, encoding='utf8')) if os.path.exists(ruta) else {}
        elenco, informe = asignar(idioma, existente)
        informe['roles'] = dict(collections.Counter(elenco.values()))
        resumen[idioma] = informe
        if not args.informe:
            with open(ruta, 'w', encoding='utf8') as f:
                json.dump(elenco, f, ensure_ascii=False, indent=1)
                f.write('\n')
    print(json.dumps(resumen, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
