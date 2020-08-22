import bpy

bl_info = {
    'name': 'Fit Lattice to Object',
    'author': 'Shulito',
    'version': (1, 0),
    'blender': (2, 90),
    'category': 'Object',
    'location': 'Operator Search (in Object Mode on a View 3D window)',
    'description': 'Fits a lattice object with a lattice modifier matching the dimensions and the rotation of the active object.'
}


class MESH_OT_fit_lattice_to_object(bpy.types.Operator):
    """Fit Lattice to Object"""
    bl_idname = "object.fit_lattice_to_object"
    bl_label = "Fit Lattice to Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.area.type == 'VIEW_3D'

    def execute(self, context: bpy.types.Context):
        if context.active_object is None:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to have an active object selected to fit the lattice.'
            )
            return {'CANCELLED'}

        to_fit: bpy.types.Object = context.active_object
        MESH_OT_fit_lattice_to_object.fit_lattice_to_object(context.scene.collection, to_fit, True)

        return {'FINISHED'}

    @staticmethod
    def fit_lattice_to_object(
        collection: bpy.types.Collection,
        to_fit: bpy.types.Object,
        add_modifier: bool
    ):
        lattice_data = bpy.data.lattices.new("Lattice")
        lattice: bpy.types.Lattice = bpy.data.objects.new("Lattice", lattice_data)

        lattice.location = to_fit.location.copy()
        lattice.rotation_euler = to_fit.rotation_euler.copy()
        lattice.name = 'lattice_' + to_fit.name
        lattice.dimensions = to_fit.dimensions.copy()

        collection.objects.link(lattice)

        source_lattice_modifier: bpy.types.LatticeModifier = None
        if add_modifier:
            source_lattice_modifier = to_fit.modifiers.new('Lattice', 'LATTICE')
            source_lattice_modifier.object = lattice

        return lattice, source_lattice_modifier


classes = [
    MESH_OT_fit_lattice_to_object
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
