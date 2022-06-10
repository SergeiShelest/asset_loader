from abc import ABCMeta, abstractmethod

from .fake_asset import FakeAsset


class AssetNotFound(Exception):
    pass


class AssetAccessDenied(Exception):
    pass


class AssetHttpError(Exception):
    pass


class AssetDownloadError(Exception):
    pass


class IStock:
    __metaclass__ = ABCMeta

    name: str
    title: str

    @abstractmethod
    def download_asset(self, id_name):
        pass

    @abstractmethod
    def generate_fake_assets(self) -> list[FakeAsset]:
        pass
