# Exporta, por vértice de la cabeza, cuánto lo mueve cada blendshape útil para
# ubicar las zonas de maquillaje (labios, párpados, mejillas) y su UV.
# blender -b --python zonas.py -- avatar_facial.fbx salida.npz
import bpy, sys, numpy as np
fbx, salida = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
m = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
me = m.data; kb = me.shape_keys.key_blocks
base = np.array([v.co[:] for v in kb[0].data])
def desp(sub):
    ks = [k for k in kb if k.name.lower().endswith(sub.lower())]
    if not ks: print('FALTA', sub); return np.zeros(len(base))
    return np.linalg.norm(np.array([v.co[:] for v in ks[0].data]) - base, axis=1)
claves = ['MouthPucker', 'MouthRollLower', 'MouthRollUpper', 'EyeBlinkLeft', 'EyeBlinkRight', 'CheekPuff', 'CheekSquintLeft', 'CheekSquintRight', 'MouthSmileLeft', 'JawOpen', 'MouthClose', 'MouthFunnel']
D = {k: desp(k) for k in claves}
print('KEYS', [k.name for k in kb][:5], len(kb))
uv = me.uv_layers.active.data
mats = [s.material.name.lower() for s in m.material_slots]
tris, tuv = [], []
me.calc_loop_triangles()
for t in me.loop_triangles:
    if 'head' not in mats[t.material_index] or 'opacity' in mats[t.material_index]: continue
    tris.append(t.vertices[:]); tuv.append([uv[l].uv[:] for l in t.loops])
np.savez(salida, tris=np.array(tris), tuv=np.array(tuv), base=base, **D)
print('LISTO', len(tris), {k: round(float(v.max()), 4) for k, v in D.items()})
