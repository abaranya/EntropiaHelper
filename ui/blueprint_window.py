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
        self.setWindowTitle("Blueprint Window")
        self.blueprints = {}  # Initialize an empty dictionary to store blueprints
        self.load_blueprints()  # Load blueprints from file when the window is created

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # First Line: Name, Level, and Type Labels
        first_line_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        level_label = QLabel("Level:")
        type_label = QLabel("Type:")
        first_line_layout.addWidget(name_label)
        first_line_layout.addWidget(level_label)
        first_line_layout.addWidget(type_label)
        layout.addLayout(first_line_layout)

        # Second Line: Name, Level, and Type Fields
        second_line_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.level_edit = QSpinBox()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Unlimited", "Limited"])
        second_line_layout.addWidget(self.name_edit)
        second_line_layout.addWidget(self.level_edit)
        second_line_layout.addWidget(self.type_combo)
        layout.addLayout(second_line_layout)

        # Third Line: Crafted Item and Class Labels
        third_line_layout = QHBoxLayout()
        crafted_item_label = QLabel("Crafted Item:")
        class_label = QLabel("Class:")
        third_line_layout.addWidget(crafted_item_label)
        third_line_layout.addWidget(class_label)
        layout.addLayout(third_line_layout)

        # Fourth Line: Crafted Item and Class Fields
        fourth_line_layout = QHBoxLayout()
        self.crafted_item_edit = QLineEdit()
        self.class_combo = QComboBox()
        self.class_combo.addItems(
            ["Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator",
             "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer",
             "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign", "Storage Container",
             "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"])
        self.item_search_button = QPushButton()
        self.item_search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.item_search_button.clicked.connect(self.craft_item_search)
        fourth_line_layout.addWidget(self.crafted_item_edit)
        fourth_line_layout.addWidget(self.item_search_button)
        fourth_line_layout.addWidget(self.class_combo)
        layout.addLayout(fourth_line_layout)

        self.materials_container = MaterialWidget()
        layout.addWidget(self.materials_container)


        # # Fifth Line: Materials Label
        # materials_label = QLabel("Materials (Quantity):")
        # layout.addWidget(materials_label)
        #
        # # Materials Container
        # self.materials_container = QWidget()
        # material_layout = QVBoxLayout()
        # self.materials_container.setLayout(material_layout)
        # layout.addWidget(self.materials_container)
        #
        # # Sixth Line: Add Material Button
        # self.add_material_button = QPushButton("Add Material")
        # self.add_material_button.clicked.connect(self.add_material_row)
        # layout.addWidget(self.add_material_button)

        # Seventh Line: Search, and Save Buttons
        seventh_line_layout = QHBoxLayout()
        self.search_material_button = QPushButton("Search Material")
        self.search_material_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        self.search_material_button.clicked.connect(self.search_material)
        seventh_line_layout.addWidget(self.search_material_button)

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

    def search_material(self):
        last_row = self.materials_layout.rowCount() - 1
        if last_row > 0:
            print(f"looking for item at row {last_row}")
            curr_row_widget = self.materials_layout.itemAtPosition(last_row, 1)
            if curr_row_widget is not None:
                search_text = curr_row_widget.widget().text()  # Get text from the first material row
                # Implement your search logic here
                print("Searching material:", search_text)
            else:
                print("No widget found in the first row")
        else:
            print("No material rows added yet")

    def craft_item_search(self):
        print("item search function not yet implemented")

    def load_blueprints(self):
        if os.path.exists('blueprints.json'):  # Check if the file exists
            with open('blueprints.json', 'r') as f:
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
