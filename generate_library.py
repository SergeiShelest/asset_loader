from bpy.types import Operator
from .asset_stocks import stocks


class GenerateLibrary(Operator):
    bl_idname = "asset_loader.generate_library"
    bl_label = "Create asset library"

    def execute(self, context):
        if "asset_loader" not in context.scene.keys():
            context.scene["asset_loader"] = dict()

        context.scene["asset_loader"]["asset_library"] = True

        for stock in stocks.items():
            fake_assets = stock[1].generate_fake_assets()

            for fake_asset in fake_assets:
                fake_asset.create()

        return {'FINISHED'}
