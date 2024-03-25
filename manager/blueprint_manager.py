import json
import os
from entity.blueprint import Blueprint

class BlueprintManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename='blueprints.json'):
        if self._initialized:
            return

        script_dir = os.path.dirname(__file__)
        self.blueprints_path = os.path.join(script_dir, '..', 'data', 'blueprints.json')

        self._initialized = True
        self.filename = self.blueprints_path
        self.blueprints = {}  # Dictionary to store blueprints
        self.load_blueprints()

    def load_blueprints(self):
        if os.path.exists(self.filename):  # Check if the file exists
            with open(self.filename, 'r') as f:
                loaded_blueprints = json.load(f)  # Load blueprints from file
                self.blueprints = {name: Blueprint(**blueprint_data) for name, blueprint_data in loaded_blueprints.items()}
            print("Blueprints loaded successfully:", self.blueprints)
        else:
            print("No blueprints file found, starting with an empty blueprint set")

    def save_blueprints(self):
        data = {blueprint.name: blueprint.to_dict() for blueprint in self.blueprints.values()}
        with open(self.filename, 'w') as f:
            json.dump(data, f)
        # print("Blueprints saved successfully")
        print(f'we are about to save {len(data)} materials as {data}')

    def add_blueprint(self, blueprint):
        if blueprint.name not in self.blueprints:
            self.blueprints[blueprint.name] = blueprint
            print(f"Blueprint '{blueprint.name}' added successfully.")
        else:
            existing_blueprint = self.blueprints[blueprint.name]
            # Update existing blueprint fields
            existing_blueprint.level = blueprint.level
            existing_blueprint.type = blueprint.type
            existing_blueprint.class_field = blueprint.class_field
            existing_blueprint.materials = blueprint.materials
            existing_blueprint.is_limited = blueprint.is_limited
            existing_blueprint.attempts = blueprint.attempts
            print(f"Blueprint '{blueprint.name}' updated successfully.")

    def get_blueprint(self, name):
        return self.blueprints.get(name)

    def delete_blueprint(self, name):
        if name in self.blueprints:
            del self.blueprints[name]
            print(f"Blueprint '{name}' deleted successfully.")
        else:
            print(f"Blueprint '{name}' does not exist in the blueprint manager.")

    def search_blueprint(self, name_substring):
        matching_blueprints = [name for name in self.blueprints if name_substring.lower() in name.lower()]
        return matching_blueprints
