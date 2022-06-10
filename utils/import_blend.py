import bpy


class BlendAppendingError(Exception):
    pass


def append_material(blend_file: str, name: str, link=False):
    with bpy.data.libraries.load(blend_file, link=link) as (data_from, data_to):
        for material_name in data_from.materials:
            if material_name == name:
                data_to.materials = [name]
                return

    raise BlendAppendingError("Appending material error. There is no {0} in the '{1}' file".format(name, blend_file))
