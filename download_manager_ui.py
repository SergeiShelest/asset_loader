import bpy
from bpy.props import StringProperty, FloatProperty, CollectionProperty
from bpy.types import PropertyGroup, Panel

from .download_manager import IObserver, NotifyType


class AL_Download(PropertyGroup):
    title: StringProperty()
    progressbar: FloatProperty(
        name="Download",
        subtype="PERCENTAGE",
        soft_min=0,
        soft_max=100,
        precision=0
    )


class AL_DownloadGroup(PropertyGroup):
    title: StringProperty()
    downloads: CollectionProperty(
        type=AL_Download,
        name='group'
    )


class AL_PT_DownloadManager(Panel):
    bl_idname = "AL_PT_DownloadManager"
    bl_label = "Download Manager"
    bl_category = "Asset Loader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        for group in context.scene.asset_loader_data.downloadGroups:
            bx = layout.box()
            bx.label(text=group.title)

            for download in group.downloads:
                ly = bx.row()
                ly.label(text=download.title)
                ly.prop(download, "progressbar")


def refresh_all_areas():
    for wm in bpy.data.window_managers:
        for w in wm.windows:
            for area in w.screen.areas:
                area.tag_redraw()


class UpdateUiProperties(IObserver):
    def notify(self, type_, queue):

        if type_ == NotifyType.NEW:
            group = bpy.context.scene.asset_loader_data.downloadGroups.add()
            group.name = queue.uuid
            group.title = queue.title

            for file in queue.files:
                download = group.downloads.add()
                download.title = file.title

        elif type_ == NotifyType.UPDATE:
            group = bpy.context.scene.asset_loader_data.downloadGroups[queue.uuid]

            for i, download in enumerate(group.downloads):
                file = queue.files[i]

                if file.size != 0:
                    download.progressbar = 100 / file.size * file.loaded

        refresh_all_areas()
