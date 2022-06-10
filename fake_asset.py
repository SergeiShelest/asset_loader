import enum

import bpy


LoadStatusEnum = enum.Enum(
    value="LoadStatus",
    names="LOADED NOT_LOADED",
)


class FakeAsset:
    def __init__(self, id_name: str, id_stock: str):
        self.__load_status = LoadStatusEnum.NOT_LOADED
        self.__id_name: str = id_name
        self.__id_stock: str = id_stock
        self.__title: str = id_name
        self.__authors: list[str] = []
        self.__tags: list[str] = []
        self.__image_preview_path: str = ""

    @property
    def id_name(self):
        return self.__id_name

    @property
    def id_stock(self):
        return self.__id_stock

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def authors(self):
        return self.__authors

    @authors.setter
    def authors(self, authors: list[str]):
        self.__authors = authors

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags: list[str]):
        self.__tags = tags

    @property
    def image_preview_path(self):
        return self.__image_preview_path

    @image_preview_path.setter
    def image_preview_path(self, path: str):
        self.__image_preview_path = path

    def create(self):
        mat = bpy.data.materials.new(name=self.__title)
        mat.use_nodes = True
        mat.asset_mark()

        bpy.ops.ed.lib_id_load_custom_preview(
            {"id": mat},
            filepath=self.__image_preview_path
        )

        mat.asset_data.author = ", ".join(self.__authors)

        for tag in self.__tags:
            mat.asset_data.tags.new(tag, skip_if_exists=True)

        mat.asset_data.id_data["fake_asset_data"] = {
            "load_status": self.__load_status.name,
            "id_name": self.__id_name,
            "id_stock": self.__id_stock,
        }
