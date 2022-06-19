from . import polyhaven

from ..download_manager import DownloadManager
from ..download_manager_ui import UpdateUiProperties

__classes: list = [
    polyhaven.PolyHaven
]

dm = DownloadManager()
update_ui_props = UpdateUiProperties()
dm.subscribe(update_ui_props)

stocks: dict = {}

for stock in __classes:
    s = stock()
    s.dm = dm
    stocks.update({stock.name: s})
