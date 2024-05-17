import json
import os
from entity.item import Item

class ItemManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename='items.json'):
        if self._initialized:
            return

        script_dir = os.path.dirname(__file__)
        self.items_path = os.path.join(script_dir, '..', 'data', 'items.json')

        self.categories = [
            "Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator",
            "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer",
            "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign",
            "Storage Container", "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"
        ]
        self._initialized = True
        self.filename = self.items_path
        self.items = {}  # Dictionary to store items
        self.load_items()

    def load_items(self):
        if os.path.exists(self.filename):  # Check if the file exists
            with open(self.filename, 'r') as f:
                loaded_items = json.load(f)  # Load items from file
                self.items = {name: Item(**item_data) for name, item_data in loaded_items.items()}
            print("Items loaded successfully:", self.items)
        else:
            print("No items file found, starting with an empty item set")

    def save_items(self):
        data = {item.name: item.to_dict() for item in self.items.values()}
        with open(self.filename, 'w') as f:
            json.dump(data, f)
        print("Items saved successfully")

    def item_search(self, search_query):
        search_query = search_query.lower()
        matching_items = [item for item in self.items.values() if search_query in item.name.lower()]
        return matching_items

    def search(self, search_query):
        return [item.name for item in self.item_search(search_query)]

    def add_item(self, item):
        if item.name not in self.items:
            self.items[item.name] = item
            print(f"Item '{item.name}' added successfully.")
        else:
            existing_item = self.items[item.name]
            existing_item.description = item.description
            existing_item.category = item.category
            existing_item.value = item.value
            existing_item.markup = item.markup
            existing_item.tt_cost = item.tt_cost
            existing_item.full_cost = item.full_cost
            existing_item.cost_markup = item.cost_markup
            print(f"Item '{item.name}' updated successfully.")

    def get_item(self, name):
        return self.items.get(name)

    def delete_item(self, name):
        if name in self.items:
            del self.items[name]
            print(f"Item '{name}' deleted successfully.")
        else:
            print(f"Item '{name}' does not exist in the item manager.")

    def get_categories(self):
        return self.categories
