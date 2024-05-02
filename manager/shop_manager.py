import json
import os
from entity.shop_inventory import ShopInventory

class ShopManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        script_dir = os.path.dirname(__file__)
        self.filename = os.path.join(script_dir, '..', 'data', 'shop_inventory.json')

        self._initialized = True
        self.shop_inventory = {'Shop 2': ShopInventory(), 'Shop 3': ShopInventory()}
        self.load_shop_inventory()

    def load_shop_inventory(self):
        if os.path.exists(self.filename):  # Check if the file exists
            with open(self.filename, 'r') as f:
                loaded_shop_inventory = json.load(f)  # Load shop inventory from file

                self.shop_inventory['Shop 2'] = ShopInventory.from_json(loaded_shop_inventory.get('Shop 2', {}))
                self.shop_inventory['Shop 3'] = ShopInventory.from_json(loaded_shop_inventory.get('Shop 3', {}))

            print("Shop inventory loaded successfully:", self.shop_inventory)
        else:
            print("No shop inventory file found, starting with an empty shop inventory")

    def save_shop_inventory(self):
        shop_inventory_data = {
            'Shop 2': self.shop_inventory['Shop 2'].to_json(),
            'Shop 3': self.shop_inventory['Shop 3'].to_json()
        }

        with open(self.filename, 'w') as f:
            json.dump(shop_inventory_data, f, indent=2)

        print("Shop inventory saved successfully")

    def add_material(self, shop, material_name, price, quantity, sold_price=None, sold_date=None):
        if shop not in self.shop_inventory:
            self.shop_inventory[shop] = {}
        else:
            self.shop_inventory[shop].add_material(material_name, price, quantity, sold_price, sold_date)
