import json

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
