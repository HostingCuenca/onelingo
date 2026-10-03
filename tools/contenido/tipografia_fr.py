#!/usr/bin/env python3
"""Normaliza la tipografía francesa de borradores de la ruta: U+202F antes de
? ! : ; y dentro de « », solo en campos en francés (no toca es/en ni traducciones).
Conserva el formato JSON del archivo.

Uso: python3 tools/contenido/tipografia_fr.py tools/contenido/ruta-fr/n10-b0*.json
"""
import json,re,sys
SKIP={'es','en','traduccion','apoyo','preguntaApoyo'}
n=0
def fix(s):
    global n
    t=re.sub(r'(?<=[\wÀ-ÿ»\)’]) (?=[?!:;](\s|$|»|"))','  '[1:],s)
    t=re.sub(r'(?<=[\wÀ-ÿ»\)’])(?=[?!;](\s|$))',' ',t)
    t=re.sub(r'« ?(?=\S)','« ',t); t=re.sub(r'(?<=\S) ?»',' »',t)
    t=t.replace('«  ','« ').replace('  »',' »')
    if t!=s: n+=1
    return t
def walk(o):
    if isinstance(o,dict): return {k:(v if k in SKIP else walk(v)) for k,v in o.items()}
    if isinstance(o,list): return [walk(v) for v in o]
    if isinstance(o,str): return fix(o)
    return o
for f in sys.argv[1:]:
    t=open(f).read();d=json.loads(t)
    ind=None
    for i in (2,1,None):
        if json.dumps(d,ensure_ascii=False,indent=i)+'\n'==t or json.dumps(d,ensure_ascii=False,indent=i)==t: ind=i;break
    else: print('formato no reproducible',f); continue
    n=0;d2=walk(d);out=json.dumps(d2,ensure_ascii=False,indent=ind)+('\n' if t.endswith('\n') else '')
    open(f,'w').write(out);print(f.split('/')[-1],'cadenas cambiadas',n)
