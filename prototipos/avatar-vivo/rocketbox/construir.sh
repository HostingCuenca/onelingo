#!/bin/bash
# Construye un tutor desde un Rocketbox: piel pareja, maquillaje opcional, bordes del pelo y GLB.
#   construir.sh <Nombre_Rocketbox> <salida> [labial|-] [extra env: QUITAR_CAPUCHA=..]
set -e
cd "$(dirname "$0")/.."
N=$1 OUT=$2 LAB=${3:--}
P=$(ls src/$N/Textures | grep head_color | cut -d_ -f1)
timeout 600 blender -b --python scripts/pestanas.py -- src/$N/${N}_facial.fbx maquillaje/${OUT}_pestanas.json 2>&1 | grep -iE "^LISTO|Error" || true
PELO=original PIEL=${PIEL:-auto} python3 scripts/recolorear.py src/$N/Textures $P maquillaje/${OUT}_pestanas.json maquillaje/tex_$OUT
if [ "$LAB" != "-" ]; then
  [ -s maquillaje/$N.npz ] || timeout 600 blender -b --python scripts/zonas.py -- src/$N/${N}_facial.fbx maquillaje/$N.npz 2>&1 | grep -iE "^LISTO|Error"
  python3 scripts/maquillar.py maquillaje/$N.npz maquillaje/tex_$OUT/${P}_head_color.tga maquillaje/${OUT}_head.png "$LAB"
  python3 -c "from PIL import Image; Image.open('maquillaje/${OUT}_head.png').save('maquillaje/tex_$OUT/${P}_head_color.tga')"
fi
[ -f maquillaje/tex_$OUT/${P}_opacity_color.tga ] && python3 scripts/sangrar.py maquillaje/tex_$OUT/${P}_opacity_color.tga
RELIEVE_CARA=${RELIEVE_CARA:-0.3} timeout 600 blender -b --python scripts/convertir.py -- ~/Documents/onelingo/prototipos/avatar-vivo/modelos/avaturn.glb src/$N/${N}_facial.fbx maquillaje/tex_$OUT out/$OUT.glb 2>&1 | grep -E "LISTO|CAPUCHA|Error"
cp out/$OUT.glb ~/Documents/onelingo/prototipos/avatar-vivo/modelos/
