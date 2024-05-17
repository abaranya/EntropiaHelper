import json
from datetime import datetime

from entity.item_pack import ItemPack
from entity.material_pack import MaterialPack


class ShopInventory:
    def __init__(self):

        self.items = {}
        self.materials = {}

    def to_json(self):
        return {
            "items": {key: value.to_dict() for key, value in self.items.items()},
            "materials": {key: value.to_dict() for key, value in self.materials.items()}
        }


    @classmethod
    def from_json(cls, json_data):
        shop_inventory = cls()
        shop_inventory.items = {key: ItemPack.from_dict(value) for key, value in json_data.get("items", {}).items()}
        shop_inventory.materials = {key: MaterialPack.from_dict(value) for key, value in
                                    json_data.get("materials", {}).items()}
        return shop_inventory

    def add_item(self, package, item_pack):

        self.items[package] = item_pack
        return package

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
        else:
            raise ValueError("Item not found in inventory")

    def get_item(self, package):
        return self.items.get(package, None)

    def get_items(self):
        return self.items

    def add_material(self, pack_name, package):
        self.materials[pack_name] = package
        return package

    def remove_material(self, package):
        if package in self.materials:
            del self.materials[package]
        else:
            raise ValueError("Material not found in inventory")

    def get_material(self, material_id):
        return self.materials.get(material_id, None)

    def get_materials(self):
        return self.materials

    def update_field_value(self, type, package, field_name, new_value):
        # Example implementation logic
        print(f"Updating {field_name} for {package} to {new_value}")
        # Implement the actual database update logic here
        # You might want to use a dictionary or a switch-case pattern based on field_name
        # For instance:
        if field_name == "sold_price":
            # Update sold price in database
            if type == "materials":
                self.materials[package].sold_price = new_value
            elif type == "items":
                self.items[package].sold_price = new_value
        elif field_name == "sold_date":
            # Update sold date in database
            if type == "materials":
                self.materials[package].sold_date = datetime.strptime(new_value, '%Y-%m-%d')
            elif type == "items":
                self.items[package].sold_date = datetime.strptime(new_value, '%Y-%m-%d')
