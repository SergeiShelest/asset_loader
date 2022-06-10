import os
import requests

import bpy

from ..utils import temp, download, import_blend
from ..stock import IStock, AssetNotFound, AssetAccessDenied, AssetHttpError, AssetDownloadError
from ..fake_asset import FakeAsset


class PolyHaven(IStock):
    name = "polyhaven.com"
    title = "Poly Haven"

    API_URL = "https://api.polyhaven.com"
    TEMP_PATH = temp.get_temp_path()

    def download_asset(self, id_name):
        req = requests.request("GET", "{0}/files/{1}".format(self.API_URL, id_name))

        if req.status_code == 403:
            raise AssetAccessDenied("Failed loading material {0}. Http error: {1}.".format(id_name, req.status_code))

        if req.status_code == 404:
            raise AssetNotFound("Failed loading material {0}. Http error: {1}.".format(id_name, req.status_code))

        if req.status_code != 200:
            raise AssetHttpError("Failed loading material {0}. Http error: {1}.".format(id_name, req.status_code))

        req_data = req.json()["blend"]["4k"]["blend"]

        blend_url = req_data["url"]
        blend_path = os.path.join(self.TEMP_PATH, "{0}.blend".format(id_name))

        try:
            download.download_file(blend_url, blend_path)
        except Exception:
            raise AssetDownloadError

        textures = req_data["include"].items()

        for texture in textures:
            texture_url = texture[1]["url"]
            texture_path = os.path.join(self.TEMP_PATH, texture[0])

            os.makedirs(os.path.split(texture_path)[0], mode=0o775, exist_ok=True)

            try:
                download.download_file(texture_url, texture_path)
            except Exception:
                raise AssetDownloadError

        try:
            import_blend.append_material(blend_path, id_name)
        except import_blend.BlendAppendingError:
            raise import_blend.BlendAppendingError

        materials = bpy.data.materials
        mat = materials[id_name]

        return mat

    def generate_fake_assets(self):
        fake_assets = []
        req = requests.request("GET", "{0}/assets?t={1}".format(self.API_URL, "textures"))

        if req.status_code != 200:
            return fake_assets

        materials = req.json().items()
        count_materials = len(materials)

        for i, material in enumerate(materials):
            id_name = material[0]
            material_data = material[1]

            asset_image_preview = "https://cdn.polyhaven.com/asset_img/thumbs/{0}.png?height=256".format(id_name)
            asset_image_path = os.path.join(self.TEMP_PATH, "prw_{0}.png".format(id_name))

            download.download_file(asset_image_preview, asset_image_path)

            tags = material_data["tags"]
            categories = material_data["categories"]

            for category in categories:
                tags.append(category.replace(" ", "_"))

            fake_asset = FakeAsset(id_name, self.name)
            fake_asset.title = material_data["name"]
            fake_asset.authors = material_data["authors"].keys()
            fake_asset.tags = tags
            fake_asset.image_preview_path = asset_image_path

            fake_assets.append(fake_asset)

            print("Generating assets. [{0} / {1}]".format(i, count_materials))

        return fake_assets
