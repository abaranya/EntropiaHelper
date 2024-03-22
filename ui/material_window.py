import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, QDoubleSpinBox, QDateTimeEdit, QMessageBox, QComboBox
from PyQt6.QtCore import QDate

from entity.material import Material

class MaterialWindow(QMainWindow):
    materials = {}  # Dictionary to store materials

    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Material Window")
        self.materials = {}  # Initialize an empty dictionary to store materials
        self.load_materials()  # Load materials from file when the window is created

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

        # TT Value
        tt_label = QLabel("TT Value (PED):")
        self.tt_edit = QDoubleSpinBox()
        self.tt_edit.setSuffix(" PED")
        self.tt_edit.setDecimals(2)
        layout.addWidget(tt_label)
        layout.addWidget(self.tt_edit)

        # Markup value
        markup_label = QLabel("Markup Value (%):")
        self.markup_spinbox = QDoubleSpinBox()
        self.markup_spinbox.setSuffix("%")
        self.markup_spinbox.setDecimals(2)  # Set to allow four decimal places
        self.markup_spinbox.setMaximum(9999999.99)
        layout.addWidget(markup_label)
        layout.addWidget(self.markup_spinbox)

        # Category
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Ores", "Enmmater", "Residue", "Robot Parts", "Animal Parts", "Components"])
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)

        # Entry Date
        entry_label = QLabel("Entry Date:")
        self.entry_edit = QDateTimeEdit()
        self.entry_edit.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(entry_label)
        layout.addWidget(self.entry_edit)

        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        search_button.clicked.connect(self.search_material)  # Connect the button click event to search_material method
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_material)  # Connect save button to save_material function
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def load_materials(self):
        if os.path.exists('../data/materials.json'):  # Check if the file exists
            with open('../data/materials.json', 'r') as f:
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

    def save_material(self):
        if self.validate():
            name = self.name_edit.text()
            tt_value = self.tt_edit.value()
            markup_value = self.markup_spinbox.value()
            category = self.category_combo.currentText()
            entry_date = self.entry_edit.text() if self.entry_edit.text() else QDate.currentDate().toString("yyyy-MM-dd")

            material = Material(name, tt_value, markup_value, category, entry_date)
            self.materials[name] = material  # Add material to the dictionary

            # Check if the material already exists in the dictionary
            if name in self.materials:
                print("Material already exists, updating...")

            # Save the materials dictionary to a file
            with open('../data/materials.json', 'w') as f:
                json.dump({name: material.to_dict() for name, material in self.materials.items()}, f)

            print("Material saved successfully:", material.__dict__)
        else:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields correctly.")

    def search_material(self):
        search_text = self.name_edit.text()  # Get the search text from the search box
        material_found = None

        # Loop through the loaded materials to find a material that contains the search text
        for name, material in self.materials.items():
            if search_text.lower() in name.lower():
                material_found = material
                break

        if material_found:
            # If a material is found, populate the fields in the material window with its data
            self.name_edit.setText(material_found.name)
            self.tt_edit.setValue(material_found.tt_value)
            self.markup_spinbox.setValue(material_found.markup_value)
            entry_date = QDate.fromString(material_found.entry_date, "yyyy-MM-dd")
            self.entry_edit.setDate(entry_date)
            self.category_combo.setCurrentText(material_found.category)
            print("Material found:", material_found.__dict__)
        else:
            # If no material is found, show a message box
            QMessageBox.warning(self, "Material Not Found", "No material found matching the search criteria.")

    @classmethod
    def get_material(cls, name):
        return cls.materials.get(name)

    def validate(self):
        name = self.name_edit.text()
        tt_value = self.tt_edit.value()
        markup_value = self.markup_spinbox.value()

        # Check if all fields are filled correctly
        if name.strip() == "":
            return False
        if tt_value <= 0:
            return False
        if markup_value < 100:
            return False

        return True
