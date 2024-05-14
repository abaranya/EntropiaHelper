import json
from datetime import datetime


class MaterialPack:
    def __init__(self, item_type: str, name: str, quantity: int, price: float, markup: float, since_date: str, sold_price: float = 0.00,
                 sold_date: str = "1900-01-01"):
        self.item_type = item_type
        self.name = name
        self.quantity = quantity
        self.markup = markup
        self.price = price
        self.since_date = datetime.strptime(since_date, '%Y-%m-%d')
        self.sold_price = sold_price
        self.sold_date = datetime.strptime(sold_date, '%Y-%m-%d') if sold_date else None

        if price < 0:
            raise ValueError("Price cannot be negative")

    def to_dict(self):
        return {
            "item_type": self.item_type,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "markup": self.markup,
            "since_date": self.since_date.strftime('%Y-%m-%d'),
            "sold_price": self.sold_price,
            "sold_date": self.sold_date.strftime('%Y-%m-%d') if self.sold_date else None
        }

    @classmethod
    def from_dict(cls, json_data):
        # Parse the JSON dictionary into constructor parameters
        item_type = json_data.get('item_type')
        name = json_data.get('name')
        quantity = json_data.get('quantity', 0)  # Default quantity to 0 if not specified
        price = json_data.get('price', 0.0)  # Default price to 0.0 if not specified
        markup = json_data.get('markup', 0.0)
        since_date = json_data.get('since_date', '1970-01-01')  # Provide a default date if missing

        # Optional fields
        sold_price = json_data.get('sold_price')
        sold_date = json_data.get('sold_date')

        return cls(item_type, name, quantity, price, markup, since_date, sold_price, sold_date)

    def field_list(self):
        """Returns a list of fields representing the item's data."""
        return [
            self.item_type,
            self.name,
            "{:d}".format(self.quantity),
            "{:.2f}".format(self.price),
            "{:.2f}".format(self.markup),
            self.since_date.strftime('%Y-%m-%d'),
            "{:.2f}".format(self.sold_price) if self.sold_price is not None else "N/A",
            self.sold_date.strftime('%Y-%m-%d') if self.sold_date is not None else "N/A"
        ]

    def days_on_market(self):
        """Returns the number of days the material was on the market. If not sold, calculates days until today."""
        if self.sold_date:
            if self.sold_date < self.since_date:
                raise ValueError("Sold date cannot be before since date.")
            return (self.sold_date - self.since_date).days
        else:
            # Calculate the days on market from since_date to today if not yet sold
            return (datetime.now() - self.since_date).days
