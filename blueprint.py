import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, QComboBox, QMessageBox, QSpinBox, QGridLayout, QDoubleSpinBox
from material import MaterialWindow

class Blueprint:
    def __init__(self, name, level, type, class_field, materials, is_limited=False, attempts=None):
        self.name = name
        self.level = level
        self.type = type
        self.class_field = class_field
        self.materials = materials
        self.is_limited = is_limited
        self.attempts = attempts

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "class_field": self.class_field,
            "materials": self.materials,
            "is_limited": self.is_limited,
            "attempts": self.attempts
        }

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

        # Name
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # Level
        level_label = QLabel("Level:")
        self.level_edit = QSpinBox()
        layout.addWidget(level_label)
        layout.addWidget(self.level_edit)

        # Type
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Unlimited", "Limited"])
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)

        # Class field
        class_label = QLabel("Class:")
        self.class_combo = QComboBox()
        self.class_combo.addItems(["Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator", "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer", "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign", "Storage Container", "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"])
        layout.addWidget(class_label)
        layout.addWidget(self.class_combo)

        # Materials
        materials_label = QLabel("Materials (Quantity):")
        layout.addWidget(materials_label)

        self.materials_layout = QGridLayout()
        self.add_material_row()
        layout.addLayout(self.materials_layout)

        # Add button to dynamically add material rows
        self.add_material_button = QPushButton("+")
        self.add_material_button.clicked.connect(self.add_material_row)
        layout.addWidget(self.add_material_button)

        # Search button for materials
        self.search_material_button = QPushButton("Search Material")
        self.search_material_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        self.search_material_button.clicked.connect(self.search_material)
        layout.addWidget(self.search_material_button)

        # Limited blueprint options
        self.limited_options = QWidget()
        layout.addWidget(self.limited_options)
        self.limited_options.hide()

        limited_layout = QHBoxLayout()
        self.limited_options.setLayout(limited_layout)

        attempts_label = QLabel("Attempts:")
        self.attempts_edit = QSpinBox()
        limited_layout.addWidget(attempts_label)
        limited_layout.addWidget(self.attempts_edit)

        # Save button
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_blueprint)  # Connect save button to save_blueprint function
        layout.addWidget(save_button)

    def add_material_row(self):
        row = self.materials_layout.rowCount()
        print(f"starting with row {row}")
        qty_edit = QDoubleSpinBox()
        qty_edit.setDecimals(2)
        self.materials_layout.addWidget(qty_edit, row, 0)
        material_edit = QLineEdit()
        self.materials_layout.addWidget(material_edit, row, 1)

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
