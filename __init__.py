import threading

import bpy
from bpy.app import handlers
from bpy.types import PropertyGroup, Scene
from bpy.props import CollectionProperty, PointerProperty
from bpy.utils import register_class, unregister_class

from .download_manager_ui import AL_DownloadGroup, AL_Download, AL_PT_DownloadManager
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


class AL_Data(PropertyGroup):
    downloadGroups: CollectionProperty(
        type=AL_DownloadGroup,
        name='downloads',
    )


def load_fake_asset(material):
    id_name = material["fake_asset_data"]["id_name"]
    id_stock = material["fake_asset_data"]["id_stock"]

    rep_mat = stocks[id_stock].download_asset(id_name)

    old_name = material.name
    material.user_remap(rep_mat)

    rep_mat.id_data["fake_asset_data"] = material.id_data["fake_asset_data"]
    rep_mat.name = old_name

    bpy.data.materials.remove(material)


@handlers.persistent
def find_fake_asset(scene):
    if "asset_loader" in scene.keys():
        if scene["asset_loader"]["asset_library"]:
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


classes = [
    AL_Download,
    AL_DownloadGroup,
    AL_Data,
    AL_PT_DownloadManager,
    GenerateLibrary
]


def register():
    for cl in classes:
        register_class(cl)

    handlers.depsgraph_update_pre.append(find_fake_asset)

    Scene.asset_loader_data = PointerProperty(type=AL_Data)


def unregister():
    for cl in classes.reverse():
        unregister_class(cl)
