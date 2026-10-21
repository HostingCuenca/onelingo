import bpy, sys, mathutils
args = sys.argv[sys.argv.index('--') + 1:]
glb, salida = args[0], args[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
cab = arm.pose.bones.get('mixamorig:Head') or arm.pose.bones.get('Head')
p = arm.matrix_world @ cab.head
malla = next(o for o in bpy.data.objects if o.type == 'MESH')
# cara: vértices por encima del cuello, el más adelantado da el frente (-Y en Blender para glTF)
vs = [malla.matrix_world @ v.co for v in malla.data.vertices if (malla.matrix_world @ v.co).z > p.z - 0.05]
frente = min(v.y for v in vs); alto = max(v.z for v in vs)
print('cabeza', tuple(round(x, 3) for x in p), 'frente_y', round(frente, 3), 'tope', round(alto, 3), 'verts_cabeza', len(vs))
centro = mathutils.Vector((p.x, frente + 0.05, p.z + 0.06))
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); bpy.context.scene.collection.objects.link(cam)
cam.location = centro + mathutils.Vector((0, -0.55, 0.0)); cam.data.lens = 85
cam.rotation_euler = (centro - cam.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam
for loc, e in [((0.5, -1.5, p.z + 0.4), 600), ((-0.8, -1, p.z + 0.2), 250)]:
    l = bpy.data.objects.new('l', bpy.data.lights.new('l', 'AREA')); l.data.energy = e; l.data.size = 1; l.location = loc
    l.rotation_euler = (centro - l.location).to_track_quat('-Z', 'Y').to_euler(); bpy.context.scene.collection.objects.link(l)
s = bpy.context.scene; s.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in s.render.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
s.render.resolution_x = s.render.resolution_y = 640; s.render.filepath = salida
w = bpy.data.worlds.new('w'); s.world = w; w.color = (0.9, 0.9, 0.92)
bpy.ops.render.render(write_still=True)
