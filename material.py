import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, QDoubleSpinBox, QDateTimeEdit, QMessageBox
from PyQt6.QtCore import Qt, QDate

class Material:
    def __init__(self, name, tt_value, markup_value, entry_date):
        self.name = name
        self.tt_value = tt_value
        self.markup_value = markup_value
        self.entry_date = entry_date

    def to_dict(self):
        return {
            "name": self.name,
            "tt_value": self.tt_value,
            "markup_value": self.markup_value,
            "entry_date": self.entry_date
        }

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
        self.markup_spinbox.setDecimals(2)
        self.markup_spinbox.setMaximum(9999999.99)
        layout.addWidget(markup_label)
        layout.addWidget(self.markup_spinbox)

        # Entry Date
        entry_label = QLabel("Entry Date (yyyy-mm-dd):")
        self.entry_edit = QDateTimeEdit()
        self.entry_edit.setDisplayFormat("yyyy-MM-dd")
        self.entry_edit.setDate(QDate.currentDate())  # Set default date to today's date
        layout.addWidget(entry_label)
        layout.addWidget(self.entry_edit)

        # Search and Save buttons
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        search_button.clicked.connect(self.search_material)
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_material)  # Connect save button to save_material function
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def load_materials(self):
        if os.path.exists('materials.json'):  # Check if the file exists
            with open('materials.json', 'r') as f:
                materials_data = json.load(f)  # Load materials data from file
                for name, material_data in materials_data.items():
                    material = Material(material_data["name"], material_data["tt_value"],
                                        material_data["markup_value"], material_data["entry_date"])
                    self.materials[name] = material  # Add material to the dictionary
            print("Materials loaded successfully:", self.materials)
        else:
            print("No materials file found, starting with an empty material set")


    def save_material(self):
        if self.validate():
            name = self.name_edit.text()
            tt_value = self.tt_edit.value()
            markup_value = self.markup_spinbox.value()
            entry_date = self.entry_edit.date().toString("yyyy-MM-dd")
            material = Material(name, tt_value, markup_value, entry_date)

            # Check if the material already exists in the dictionary
            if name in self.materials:
                print("Material already exists, updating...")

            # Add or update the material in the dictionary
            self.materials[name] = material  # Add or update material

            # Save the materials dictionary to a file
            with open('materials.json', 'w') as f:
                json.dump({name: material.to_dict() for name, material in self.materials.items()}, f)

            print("Material saved successfully:", material.__dict__)
        else:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields correctly.")

    def search_material(self):
        search_text = self.name_edit.text().strip()
        if search_text:
            # Search for materials whose name contains the search text
            found_materials = [material for material in self.materials.values() if search_text in material.name]
            if found_materials:
                # If found, display the first found material in the window fields
                material = found_materials[0]
                self.name_edit.setText(material.name)
                self.tt_edit.setValue(material.tt_value)
                self.markup_spinbox.setValue(material.markup_value)
                entry_date = QDate.fromString(material.entry_date, "yyyy-MM-dd")
                self.entry_edit.setDate(entry_date)
            else:
                QMessageBox.warning(self, "Search Result", "No materials found matching the search criteria.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a search text.")

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
