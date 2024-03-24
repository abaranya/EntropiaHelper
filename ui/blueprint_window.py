import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, \
    QComboBox, QSpinBox, QDoubleSpinBox

from entity.blueprint import Blueprint
from ui.blueprint_materials import MaterialWidget


class BlueprintWindow(QMainWindow):
    blueprints = {}  # Dictionary to store blueprints

    def __init__(self, transparency):
        super().__init__()

        script_dir = os.path.dirname(__file__)
        self.blueprints_path = os.path.join(script_dir, '..', 'data', 'blueprints.json')

        self.setWindowTitle("Blueprint Window")
        self.blueprints = {}  # Initialize an empty dictionary to store blueprints
        self.load_blueprints()  # Load blueprints from file when the window is created

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # First Panel: Name, Level, and Type Labels
        first_panel = FirstPanel()
        self.name_edit = first_panel.name_edit
        layout.addWidget(first_panel)

        layout.addWidget(SecondPanel())

        self.materials_container = MaterialWidget()
        layout.addWidget(self.materials_container)


        # Seventh Line: Search, and Save Buttons
        seventh_line_layout = QHBoxLayout()
        self.blueprint_search_button = QPushButton("Search Material")
        self.blueprint_search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        self.blueprint_search_button.clicked.connect(self.search_blueprint)
        seventh_line_layout.addWidget(self.blueprint_search_button)

        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_blueprint)  # Connect save button to save_blueprint function
        seventh_line_layout.addWidget(save_button)

        layout.addLayout(seventh_line_layout)

    def add_material_row(self):
        material_layout = QVBoxLayout()
        row = QHBoxLayout()
        qty_edit = QDoubleSpinBox()
        qty_edit.setDecimals(2)
        row.addWidget(qty_edit)
        material_edit = QLineEdit()
        row.addWidget(material_edit)
        material_layout.addLayout(row)
        self.materials_container.layout().addLayout(material_layout)

    def search_blueprint(self):
        if not self.blueprints:  # Check if blueprints dictionary is empty
            self.load_blueprints()  # Load blueprints if not already loaded

        name_substring = self.name_edit.text().strip()  # Get the name substring to search for

        if name_substring:
            found_blueprints = {name: blueprint for name, blueprint in self.blueprints.items() if
                                name_substring in name}
            if found_blueprints:
                # Assuming you want to handle only the first matching blueprint, you can take the first item
                name, blueprint = next(iter(found_blueprints.items()))

                # Update window fields with the found blueprint
                self.name_edit.setText(blueprint.name)
                self.level_edit.setValue(blueprint.level)
                index = self.type_combo.findText(blueprint.type)
                if index != -1:
                    self.type_combo.setCurrentIndex(index)
                index = self.class_combo.findText(blueprint.class_field)
                if index != -1:
                    self.class_combo.setCurrentIndex(index)

                # You may also need to populate materials and other fields based on your application logic
            else:
                print("No blueprint found matching the name substring.")
        else:
            print("Please enter a name substring to search.")

    def craft_item_search(self):
        print("item search function not yet implemented")

    def load_blueprints(self):
        if os.path.exists(self.blueprints_path):  # Check if the file exists
            with open(self.blueprints_path, 'r') as f:
                self.blueprints = json.load(f)  # Load blueprints from file
            print("Blueprints loaded successfully:", self.blueprints)
        else:
            print("No blueprints file found, starting with an empty blueprint set")

    def save_blueprint(self):
        name = self.name_edit.text()
        level = self.level_edit.value()
        type = self.type_combo.currentText()
        class_field = self.class_combo.currentText()

        materials = []
        for row in range(self.materials_layout.rowCount()):
            qty_edit = self.materials_layout.itemAtPosition(row, 0).widget()
            material_edit = self.materials_layout.itemAtPosition(row, 1).widget()
            materials.append((qty_edit.text(), material_edit.text()))

        is_limited = type == "Limited"
        attempts = self.attempts_edit.value() if is_limited else None

        blueprint = Blueprint(name, level, type, class_field, materials, is_limited, attempts)
        self.blueprints[name] = blueprint  # Add blueprint to the dictionary

        # Save the blueprints dictionary to a file
        with open('blueprints.json', 'w') as f:
            json.dump({name: blueprint.to_dict() for name, blueprint in self.blueprints.items()}, f)

        print("Blueprint saved successfully:", blueprint.__dict__)

    @classmethod
    def get_blueprint(cls, name):
        return cls.blueprints.get(name)

    def validate(self):
        # Add validation logic if needed
        return True


class FirstPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        name_layout = QVBoxLayout()
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)

        level_layout = QVBoxLayout()
        level_label = QLabel("Level:")
        self.level_edit = QSpinBox()
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_edit)

        type_layout = QVBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Unlimited", "Limited"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)

        layout.addLayout(name_layout)
        layout.addLayout(level_layout)
        layout.addLayout(type_layout)

        self.setLayout(layout)


class SecondPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        name_layout = QVBoxLayout()
        crafted_item_label = QLabel("Crafted Item:")
        self.crafted_item_edit = QLineEdit()
        name_layout.addWidget(crafted_item_label)
        name_layout.addWidget(self.crafted_item_edit)

        search_layout = QVBoxLayout()
        self.item_search_button = QPushButton()
        self.item_search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        # self.item_search_button.clicked.connect(self.craft_item_search)
        search_layout.addWidget(QLabel())
        search_layout.addWidget(self.item_search_button)

        class_layout = QVBoxLayout()
        class_label = QLabel("Class:")
        self.class_combo = QComboBox()
        self.class_combo.addItems(
            ["Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator",
             "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer",
             "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign", "Storage Container",
             "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"])

        class_layout.addWidget(class_label)
        class_layout.addWidget(self.class_combo)


        layout.addLayout(name_layout)
        layout.addLayout(search_layout)
        layout.addLayout(class_layout)

        self.setLayout(layout)

