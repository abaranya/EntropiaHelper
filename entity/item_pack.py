import json


class ItemPack:
    def __init__(self, name, price, tt, since_date, sold_price=None, sold_date=None):
        self.name = name
        self.price = price
        self.tt = tt
        self.since_date = since_date
        self.sold_price = sold_price
        self.sold_date = sold_date

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "tt": self.tt,
            "since_date": self.since_date,
            "sold_price": self.sold_price,
            "sold_date": self.sold_date
        }
