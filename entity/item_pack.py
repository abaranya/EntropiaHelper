from datetime import datetime

class ItemPack:
    def __init__(self, item_type,  name, price, tt, since_date, sold_price=None, sold_date=None):
        self.item_type = item_type
        self.name = name
        self.price = price
        self.tt = tt
        self.since_date = datetime.strptime(since_date, '%Y-%m-%d') if isinstance(since_date, str) else since_date
        self.sold_price = float(sold_price) if sold_price is not None else None
        self.sold_date = datetime.strptime(sold_date, '%Y-%m-%d') if isinstance(sold_date, str) and sold_date else None

    def to_dict(self):
        return {
            "item_type": self.item_type,
            "name": self.name,
            "price": self.price,
            "tt": self.tt,
            "since_date": self.since_date.strftime('%Y-%m-%d') if isinstance(self.since_date, datetime) else self.since_date,
            "sold_price": self.sold_price,
            "sold_date": self.sold_date.strftime('%Y-%m-%d') if self.sold_date else None
        }

    @classmethod
    def from_dict(cls, json_data):
        return cls(
            item_type=json_data['item_type'],
            name=json_data['name'],
            price=json_data['price'],
            tt=json_data['tt'],
            since_date=json_data['since_date'],
            sold_price=json_data.get('sold_price'),
            sold_date=json_data.get('sold_date')
        )

    def field_list(self):
        """Returns a list of fields representing the item's data."""
        return [
            self.item_type,
            self.name,
            "{:.2f}".format(self.price),
            "{:.2f}".format(self.tt),
            self.since_date.strftime('%Y-%m-%d'),
            "{:.2f}".format(self.sold_price) if self.sold_price is not None else "N/A",
            self.sold_date.strftime('%Y-%m-%d') if self.sold_date else "N/A"
        ]
