from . import polyhaven


__classes: list = [
    polyhaven.PolyHaven
]

stocks: dict = {}

for stock in __classes:
    stocks.update({stock.name: stock()})
