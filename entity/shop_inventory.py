class ShopInventory:
    def __init__(self):

        self.items = {}
        self.materials = {}
        self.next_item_id = 1
        self.next_material_id = 1

    def to_json(self):
        return {
            "items": self.items,
            "materials": self.materials
        }

    @classmethod
    def from_json(cls, json_data):
        shop_inventory = cls()
        shop_inventory.items = json_data["items"]
        shop_inventory.materials = json_data["materials"]
        shop_inventory.next_item_id = len(shop_inventory.items) + 1
        shop_inventory.next_material_id = len(shop_inventory.materials) + 1
        return shop_inventory

    def add_item(self, item_name, price, since_date, sold_price=None, sold_date=None):
        item_id = self.next_item_id
        self.items[item_id] = {
            "name": item_name,
            "price": price,
            "since_date": since_date,
            "sold_price": sold_price,
            "sold_date": sold_date
        }
        self.next_item_id += 1
        return item_id

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
        else:
            raise ValueError("Item not found in inventory")

    def get_item(self, item_id):
        return self.items.get(item_id, None)

    def add_material(self, material_name, price, quantity, since_date, sold_price=None, sold_date=None):
        material_id = self.next_material_id
        self.materials[material_id] = {
            "name": material_name,
            "quantity": quantity,
            "price": price,
            "since_date": since_date,
            "sold_price": sold_price,
            "sold_date": sold_date
        }
        self.next_material_id += 1
        return material_id

    def remove_material(self, material_id):
        if material_id in self.materials:
            del self.materials[material_id]
        else:
            raise ValueError("Material not found in inventory")

    def get_material(self, material_id):
        return self.materials.get(material_id, None)
