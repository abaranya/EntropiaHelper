from datetime import datetime

from utils.formatter import Formatter


class ItemPack:
    def __init__(self, item_type,  name, price, tt, markup,since_date, sold_price= 0.00, sold_date= "1900-01-01"):
        self.formatter = Formatter()
        self.item_type = item_type
        self.name = name
        self.price = price
        self.tt = tt
        self.markup = markup
        self.since_date = datetime.strptime(since_date, '%Y-%m-%d') if isinstance(since_date, str) else since_date
        self.sold_price = float(sold_price) if sold_price is not None else None
        self.sold_date = datetime.strptime(sold_date, '%Y-%m-%d') if isinstance(sold_date, str) and sold_date else None

    def to_dict(self):
        return {
            "item_type": self.item_type,
            "name": self.name,
            "price": self.price,
            "tt": self.tt,
            "markup": self.markup,
            "since_date": self.since_date.strftime('%Y-%m-%d') if isinstance(self.since_date, datetime) else self.since_date,
            "sold_price": self.sold_price,
            "sold_date": self.sold_date.strftime('%Y-%m-%d') if self.sold_date else None
        }

    @classmethod
    def from_dict(cls, json_data):
        return cls(
            item_type=json_data['item_type'],
            name=json_data['name'],
            price=float(json_data.get('price', 0.0)),
            tt=float(json_data.get('tt', 0.0)),
            markup=float(json_data.get('markup', 100.0)),
            since_date=json_data['since_date'],
            sold_price=float(json_data.get('sold_price',100.0)) if json_data.get('sold_price') else 0.0,
            sold_date=json_data.get('sold_date') if json_data.get('sold_date') else datetime(1900, 1, 1)
        )

    def field_list(self):
        """Returns a list of fields representing the item's data."""
        return [
            self.item_type,
            self.name,
            self.formatter.format_currency(self.price),
            self.formatter.format_currency(self.tt),
            self.formatter.format_percentage(self.markup),
            self.since_date.strftime('%Y-%m-%d'),
            self.formatter.format_currency(self.sold_price) if self.sold_price else "0.00",
            self.sold_date.strftime('%Y-%m-%d') if self.sold_date else "1900-01-01"
        ]
