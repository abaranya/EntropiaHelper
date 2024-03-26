import json
import os
from entity.material import Material

class MaterialManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename='materials.json'):
        if self._initialized:
            return

        script_dir = os.path.dirname(__file__)
        self.materials_path = os.path.join(script_dir, '..', 'data', 'materials.json')

        self._initialized = True
        self.filename = filename
        self.materials = {}  # Dictionary to store materials
        self.load_materials()

    def load_materials(self):
        if os.path.exists(self.materials_path):  # Check if the file exists
            with open(self.materials_path, 'r') as f:
                loaded_materials = json.load(f)  # Load materials from file

                # Loop through loaded materials to check for missing category field
                for name, material_data in loaded_materials.items():
                    if 'category' not in material_data:
                        # If category field is missing, default it to "Ores"
                        material_data['category'] = "Ores"

                self.materials = {name: Material(**material_data) for name, material_data in loaded_materials.items()}

            print("Materials loaded successfully:", self.materials)
        else:
            print("No materials file found, starting with an empty material set")

    def save_materials(self):
        data = {material.name: material.to_dict() for material in self.materials.values()}
        with open(self.materials_path, 'w') as f:
            json.dump(data, f)
        print("Materials saved successfully")

    def add_material(self, material):
        if material.name not in self.materials:
            self.materials[material.name] = material
            print(f"Material '{material.name}' added successfully.")
        else:
            existing_material = self.materials[material.name]
            existing_material.tt_value = material.tt_value
            existing_material.markup_value = material.markup_value
            existing_material.category = material.category
            existing_material.entry_date = material.entry_date
            print(f"Material '{material.name}' updated successfully.")

    def get_material(self, name):
        return self.materials.get(name)

    def search_materials(self, name_substring):
        return [name for name in self.materials if name_substring.lower() in name.lower()]

    def delete_material(self, name):
        if name in self.materials:
            del self.materials[name]
            print(f"Material '{name}' deleted successfully.")
        else:
            print(f"Material '{name}' does not exist in the material manager.")

