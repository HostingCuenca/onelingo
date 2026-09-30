import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
PROJECT = ROOT.parents[3]
scale = json.loads((ROOT / 'escala-cliente.json').read_text(encoding='utf-8'))
levels = {entry['level']: entry for entry in scale['levels']}
source = json.loads(
    (PROJECT / 'assets/contenido/en/curriculo-master.json').read_text(encoding='utf-8')
)
all_levels = []
for level in range(2, 11):
    scale_level = levels[level]
    classes=[]
    for i, lesson in enumerate(source['levels'][level-1]['lecciones'], 1):
        block=(i-1)//5+1
        prereq = [f'en.n{level}.l{i-1:03d}'] if i>1 else ([f'en.n{level-1}.l100'] if level>2 else ['en.n1.l100'])
        claims = bool(re.search(r'native-like|bilingual|\bC2\b', json.dumps(lesson), re.I))
        classes.append({'id':f'en.n{level}.l{i:03d}','nivel':level,'banda_mcer':scale_level['cefrBand'],'etiqueta_nivel':scale_level['label'],'bloque':block,'clase_en_bloque':(i-1)%5+1,'titulo_fuente':lesson['titulo'],'tema_fuente':lesson['tema'],'resultado_fuente':lesson['resultado'],'tratamiento_editorial':lesson.get('practicaEditorial','')+'; '+lesson.get('aplicacionReal',''),'skills':{'vocabulario':lesson.get('vocabularioObjetivo',''),'estructura':lesson.get('estructuraObjetivo',''),'produccion':lesson.get('practicaEditorial','')},'prerrequisitos':prereq,'requiere_reescritura_claims':claims,'estado':'planificado'})
    doc={'schema':'onelingo.editorial-plan.v1','idioma':'en','curriculumScale':scale['id'],'nivel':level,'banda_mcer':scale_level['cefrBand'],'etiqueta_nivel':scale_level['label'],'total_clases':100,'total_bloques':20,'estado':'planificado','nota':'Mapa editorial de respaldo; no constituye contenido publicable ni activa la ruta.','clases':classes}
    (ROOT/f'mapa-n{level}.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    all_levels.extend(classes)
master={'schema':'onelingo.editorial-plan.v1','idioma':'en','niveles':'N2-N10','curriculumScale':scale['id'],'escala_cliente':levels,'total_clases':900,'total_bloques':180,'estado':'planificado','nota':'Fuente editorial estática derivada del currículo fuente. No activa contenido ni declara publicabilidad.','clases':all_levels}
(ROOT/'mapa-ingles-n2-n10.json').write_text(json.dumps(master,ensure_ascii=False,indent=2)+'\n')
