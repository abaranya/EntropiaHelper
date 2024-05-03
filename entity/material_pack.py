import json
from datetime import datetime


class MaterialPack:
    def __init__(self, name: str, quantity: int, price: float, since_date: str, sold_price: str = None,
                 sold_date: str = None):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.since_date = datetime.strptime(since_date, '%Y-%m-%d')
        self.sold_price = sold_price
        self.sold_date = datetime.strptime(sold_date, '%Y-%m-%d') if sold_date else None

        if price < 0:
            raise ValueError("Price cannot be negative")

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "since_date": self.since_date.strftime('%Y-%m-%d'),
            "sold_price": self.sold_price,
            "sold_date": self.sold_date.strftime('%Y-%m-%d') if self.sold_date else None
        }

    @classmethod
    def from_dict(cls, json_data):
        # Parse the JSON dictionary into constructor parameters
        name = json_data.get('name')
        quantity = json_data.get('quantity', 0)  # Default quantity to 0 if not specified
        price = json_data.get('price', 0.0)  # Default price to 0.0 if not specified
        since_date = json_data.get('since_date', '1970-01-01')  # Provide a default date if missing

        # Optional fields
        sold_price = json_data.get('sold_price')
        sold_date = json_data.get('sold_date')

        return cls(name, quantity, price, since_date, sold_price, sold_date)