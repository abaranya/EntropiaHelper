import json


class MaterialPack:
    def __init__(self, name, quantity, price, since_date, sold_price=None, sold_date=None):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.since_date = since_date
        self.sold_price = sold_price
        self.sold_date = sold_date

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "since_date": self.since_date,
            "sold_price": self.sold_price,
            "sold_date": self.sold_date
        }

