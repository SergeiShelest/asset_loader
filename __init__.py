import threading

import bpy

from .generate_library import GenerateLibrary
from .asset_stocks import stocks
from .fake_asset import LoadStatusEnum

bl_info = {
    "name": "Asset loader",
    "author": "Sergey Ragulev",
    "description": "Simple asset loader.",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "",
    "url": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User"
}


def load_fake_asset(material):
    id_name = material["fake_asset_data"]["id_name"]
    id_stock = material["fake_asset_data"]["id_stock"]

    rep_mat = stocks[id_stock].download_asset(id_name)

    old_name = material.name
    material.user_remap(rep_mat)

    rep_mat.id_data["fake_asset_data"] = material.id_data["fake_asset_data"]
    rep_mat.name = old_name

    bpy.data.materials.remove(material)


@bpy.app.handlers.persistent
def find_fake_asset(_):
    if "asset_loader" in bpy.context.scene.keys():
        if bpy.context.scene["asset_loader"]["asset_library"]:
            return

    materials = bpy.data.materials

    for material in materials:
        if "fake_asset_data" in material.keys():
            asset_data = material["fake_asset_data"]

            if asset_data["load_status"] == LoadStatusEnum.NOT_LOADED.name:
                asset_data["load_status"] = LoadStatusEnum.LOADED.name

                thread = threading.Thread(target=load_fake_asset, args=[material])
                thread.start()

                return


def register():
    bpy.utils.register_class(GenerateLibrary)
    bpy.app.handlers.depsgraph_update_pre.append(find_fake_asset)


def unregister():
    bpy.utils.unregister_class(GenerateLibrary)
