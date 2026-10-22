# Recuadros UV (en la textura del pelo) de los triángulos cercanos a los ojos:
# son las pestañas, que no se tiñen al cambiar el color del pelo.
import bpy, sys, json
fbx, salida = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
arm = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE'][0]
m = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
ojos = [arm.matrix_world @ arm.pose.bones[n].head for n in ('Bip01 LEye', 'Bip01 REye')]
mats = [s.material.name.lower() for s in m.material_slots]
uv = m.data.uv_layers.active.data; mw = m.matrix_world; cajas = []
for p in m.data.polygons:
    if 'opacity' not in mats[p.material_index]: continue
    c = mw @ p.center
    if min((c - o).length for o in ojos) < 0.02:  # m
        us = [uv[l].uv for l in p.loop_indices]
        cajas.append([min(u.x for u in us), min(u.y for u in us), max(u.x for u in us), max(u.y for u in us)])
json.dump(cajas, open(salida, 'w')); print('LISTO', len(cajas))
