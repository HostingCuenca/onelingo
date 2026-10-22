# Convierte un avatar Microsoft Rocketbox (MIT, *_facial.fbx con visemas Oculus
# y 52 ARKit de HeadBox) al formato de TalkingHead: esqueleto con los ejes
# exactos de la plantilla (avaturn.glb, convención Mixamo/RPM) en las
# articulaciones del avatar, malla llevada a la pose T de la plantilla y
# blendshapes con los nombres viseme_* / ARKit.
#
# blender -b --python convertir.py -- plantilla.glb avatar_facial.fbx carpeta_texturas salida.glb
import bpy, sys, os, re
from mathutils import Vector, Matrix

plantilla, fbx, texdir, salida = sys.argv[sys.argv.index('--') + 1:][:4]
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------- plantilla ----------
bpy.ops.import_scene.gltf(filepath=plantilla, bone_heuristic='BLENDER')
tpl = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE'][0]
for o in list(bpy.context.scene.objects):
    if o is not tpl: bpy.data.objects.remove(o, do_unlink=True)
tpl.name = 'Armature'
T = {b.name: (tpl.matrix_world @ b.head_local, (tpl.matrix_world.to_3x3() @ b.matrix_local.to_3x3())) for b in tpl.data.bones}

# ---------- Rocketbox ----------
bpy.ops.import_scene.fbx(filepath=fbx)
rb = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE' and o is not tpl][0]
malla = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]

# QUITAR_CAPUCHA=<m>: borra la ropa (material body) por encima de la base de la
# cabeza + <m> (negativo = más abajo); deja la cabeza sin capucha.
if os.environ.get('QUITAR_CAPUCHA'):
    import bmesh
    zh = (rb.matrix_world @ rb.data.bones['Bip01 Head'].head_local).z + float(os.environ['QUITAR_CAPUCHA'])
    bm = bmesh.new(); bm.from_mesh(malla.data); mw = malla.matrix_world
    mats = malla.data.materials
    fuera = [f for f in bm.faces if 'body' in mats[f.material_index].name.lower() and (mw @ f.calc_center_median()).z > zh]
    bmesh.ops.delete(bm, geom=fuera, context='FACES'); bm.to_mesh(malla.data); bm.free()
    print('CAPUCHA caras borradas', len(fuera))

LADOS = {'L': 'Left', 'R': 'Right'}
MAPA = {'Bip01 Pelvis': 'Hips', 'Bip01 Spine': 'Spine', 'Bip01 Spine1': 'Spine1', 'Bip01 Spine2': 'Spine2',
        'Bip01 Neck': 'Neck', 'Bip01 Head': 'Head', 'Bip01 LEye': 'LeftEye', 'Bip01 REye': 'RightEye'}
DEDOS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
for s, lado in LADOS.items():
    MAPA.update({f'Bip01 {s} Clavicle': f'{lado}Shoulder', f'Bip01 {s} UpperArm': f'{lado}Arm', f'Bip01 {s} Forearm': f'{lado}ForeArm',
                 f'Bip01 {s} Hand': f'{lado}Hand', f'Bip01 {s} Thigh': f'{lado}UpLeg', f'Bip01 {s} Calf': f'{lado}Leg',
                 f'Bip01 {s} Foot': f'{lado}Foot', f'Bip01 {s} Toe0': f'{lado}ToeBase'})
    for i, d in enumerate(DEDOS):
        MAPA[f'Bip01 {s} Finger{i}'] = f'{lado}Hand{d}1'
        MAPA[f'Bip01 {s} Finger{i}1'] = f'{lado}Hand{d}2'
        MAPA[f'Bip01 {s} Finger{i}2'] = f'{lado}Hand{d}3'
INV = {v: k for k, v in MAPA.items()}

def cabeza(nombre_tpl):
    """Posición actual (posada) en el mundo de la articulación Rocketbox equivalente."""
    return rb.matrix_world @ rb.pose.bones[INV[nombre_tpl]].head

def girar(nombre_tpl, q):
    """Rota el hueso Rocketbox (y sus hijos) alrededor de su articulación con q en el mundo."""
    pb = rb.pose.bones[INV[nombre_tpl]]
    mw = rb.matrix_world
    h = mw @ pb.head
    m = mw.inverted() @ Matrix.Translation(h) @ q.to_matrix().to_4x4() @ Matrix.Translation(-h) @ mw @ pb.matrix
    pb.matrix = m
    bpy.context.view_layer.update()

def dir_tpl(a, b):
    return (T[b][0] - T[a][0]).normalized()

def alinear(a, b):
    v = (cabeza(b) - cabeza(a)).normalized()
    girar(a, v.rotation_difference(dir_tpl(a, b)))

def alinear_mano(lado):
    # Dirección (muñeca → base del medio) y giro (índice → meñique) como en la plantilla.
    m, i, p = f'{lado}Hand', f'{lado}HandIndex1', f'{lado}HandPinky1'
    alinear(m, f'{lado}HandMiddle1')
    eje = dir_tpl(m, f'{lado}HandMiddle1')
    lat_t = (T[p][0] - T[i][0]); lat_t = (lat_t - eje * lat_t.dot(eje)).normalized()
    lat_r = cabeza(p) - cabeza(i); lat_r = (lat_r - eje * lat_r.dot(eje)).normalized()
    girar(m, lat_r.rotation_difference(lat_t))

bpy.context.view_layer.objects.active = rb
bpy.ops.object.mode_set(mode='POSE')
for lado in LADOS.values():
    alinear(f'{lado}Shoulder', f'{lado}Arm')
    alinear(f'{lado}Arm', f'{lado}ForeArm')
    alinear(f'{lado}ForeArm', f'{lado}Hand')
    alinear_mano(lado)
    for d in DEDOS:
        alinear(f'{lado}Hand{d}1', f'{lado}Hand{d}2')
        alinear(f'{lado}Hand{d}2', f'{lado}Hand{d}3')
    alinear(f'{lado}UpLeg', f'{lado}Leg')
    alinear(f'{lado}Leg', f'{lado}Foot')
    alinear(f'{lado}Foot', f'{lado}ToeBase')
bpy.ops.object.mode_set(mode='OBJECT')

# Malla a la pose T: el desplazamiento de la base se suma a cada blendshape
# (la cara no se mueve, así que los visemas siguen siendo válidos).
dg = bpy.context.evaluated_depsgraph_get()
for kb in malla.data.shape_keys.key_blocks: kb.value = 0
dg.update()
ev = malla.evaluated_get(dg).to_mesh()
mw = malla.matrix_world
base = malla.data.shape_keys.key_blocks[0]
delta = [mw.inverted() @ (mw @ ev.vertices[i].co) - base.data[i].co for i in range(len(base.data))]
malla.evaluated_get(dg).to_mesh_clear()
for kb in malla.data.shape_keys.key_blocks:
    for i, d in enumerate(delta): kb.data[i].co += d
# Juntas posadas (mundo) antes de quitar el esqueleto original.
J = {n: cabeza(n) for n in INV}
for m in list(malla.modifiers): malla.modifiers.remove(m)
malla.parent = None
malla.data.transform(mw, shape_keys=True)
malla.matrix_world = Matrix()
bpy.data.objects.remove(rb, do_unlink=True)

# ---------- esqueleto nuevo: ejes de la plantilla, posiciones del avatar ----------
bpy.context.view_layer.objects.active = tpl
bpy.ops.object.mode_set(mode='EDIT')
for eb in tpl.data.edit_bones:
    eb.use_connect = False
for eb in tpl.data.edit_bones:
    if eb.name not in J: continue
    largo = eb.length * (J['Head'].z / T['Head'][0].z)
    rot = T[eb.name][1]
    eb.head = J[eb.name]
    eb.tail = J[eb.name] + rot.col[1].normalized() * largo
    eb.align_roll(rot.col[2])
bpy.ops.object.mode_set(mode='OBJECT')

# ---------- pesos: huesos del cuerpo renombrados, los de la cara a Head ----------
vg = malla.vertex_groups
cabeza_vg = vg.get('Bip01 Head')
for g in list(vg):
    if g.name in MAPA: continue
    if g.name.startswith('Bip01 ') and cabeza_vg:
        idx = g.index
        for v in malla.data.vertices:
            for e in v.groups:
                if e.group == idx and e.weight > 0: cabeza_vg.add([v.index], e.weight, 'ADD')
    vg.remove(g)
for g in vg: g.name = MAPA[g.name]
malla.parent = tpl
mod = malla.modifiers.new('Armature', 'ARMATURE'); mod.object = tpl

# ---------- blendshapes ----------
VIS = {'Sil': 'sil', 'PP': 'PP', 'FF': 'FF', 'TH': 'TH', 'DD': 'DD', 'KK': 'kk', 'CH': 'CH', 'SS': 'SS', 'nn': 'nn', 'RR': 'RR', 'aa': 'aa', 'E': 'E', 'I': 'I', 'O': 'O', 'U': 'U'}
for kb in list(malla.data.shape_keys.key_blocks)[1:]:
    m = re.match(r'AA_VI_\d+_(\w+)$', kb.name)
    a = re.match(r'AK_\d+_(\w+)$', kb.name)
    if m and m.group(1) in VIS: kb.name = 'viseme_' + VIS[m.group(1)]
    elif a: kb.name = a.group(1)[0].lower() + a.group(1)[1:]
    else: malla.shape_key_remove(kb)

# ---------- materiales ----------
def textura(nombre, lado=1024):
    # La cara a 2048 (se ve de cerca); el resto a 1024 para que el GLB pese poco.
    for f in os.listdir(texdir):
        if f.lower().endswith(nombre):
            img = bpy.data.images.load(os.path.join(texdir, f))
            if img.size[0] > lado: img.scale(lado, lado)
            return img
    return None

def material(nombre, color, normal=None, alfa=None, rugosidad=0.6, relieve=1.0):
    mat = bpy.data.materials.new(nombre); mat.use_nodes = True
    nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = rugosidad
    tc = nt.nodes.new('ShaderNodeTexImage'); tc.image = color
    nt.links.new(tc.outputs['Color'], bsdf.inputs['Base Color'])
    if alfa is not None:
        nt.links.new(tc.outputs['Alpha'], bsdf.inputs['Alpha'])
        mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
    if normal:
        tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = normal; tn.image.colorspace_settings.name = 'Non-Color'
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = relieve; nt.links.new(tn.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

nuevos = []
for slot in malla.material_slots:
    n = slot.material.name.lower()
    if 'opacity' in n:
        slot.material = material('hair_opacity', textura('opacity_color.tga'), alfa=True, rugosidad=0.7)
    elif 'head' in n:
        slot.material = material('head', textura('head_color.tga', 2048), textura('head_normal.tga'), rugosidad=0.55,
                                relieve=float(os.environ.get('RELIEVE_CARA', '1')))  # <1 suaviza arrugas (se ve más joven)
    else:
        slot.material = material('body', textura('body_color.tga'), textura('body_normal.tga'), rugosidad=0.75)

malla.name = 'Avatar'
bpy.ops.object.select_all(action='DESELECT')
tpl.select_set(True); malla.select_set(True)
bpy.ops.export_scene.gltf(filepath=salida, export_format='GLB', use_selection=True, export_skins=True, export_morph=True,
                          export_morph_normal=False, export_animations=False, export_image_format='JPEG', export_jpeg_quality=85,
                          export_yup=True, export_apply=False)
print('LISTO', salida, 'huesos', len(tpl.data.bones), 'blendshapes', len(malla.data.shape_keys.key_blocks) - 1,
      'altura cabeza', round(J['Head'].z, 3))
