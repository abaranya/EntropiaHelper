import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, \
    QDoubleSpinBox, QDateTimeEdit, QMessageBox, QComboBox, QDialog, QListView, QDialogButtonBox
from PyQt6.QtCore import QDate, QStringListModel
from entity.material import Material
from manager.material_manager import MaterialManager


class MaterialWindow(QMainWindow):
    material_manager = MaterialManager()  # Instantiate MaterialManager

    def __init__(self, transparency):
        super().__init__()

        self.setWindowTitle("Material Window")
        self.load_materials()  # Load materials from MaterialManager

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
        # Call MaterialManager to load materials
        self.material_manager.load_materials()

    def save_material(self):
        if self.validate():
            name = self.name_edit.text()
            tt_value = self.tt_edit.value()
            markup_value = self.markup_spinbox.value()
            category = self.category_combo.currentText()
            entry_date = self.entry_edit.text() if self.entry_edit.text() else QDate.currentDate().toString(
                "yyyy-MM-dd")

            # Create a Material object
            material = Material(name, tt_value, markup_value, category, entry_date)

            # Call MaterialManager to add or update material
            self.material_manager.add_material(material)

            print("Material saved successfully:", material.__dict__)
        else:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields correctly.")

    # def search_material(self):
    #     search_text = self.name_edit.text()  # Get the search text from the search box
    #
    #     # Call MaterialManager to search for material
    #     material_found = self.material_manager.get_material(search_text)
    #
    #     if material_found:
    #         # If a material is found, populate the fields in the material window with its data
    #         self.name_edit.setText(material_found.name)
    #         self.tt_edit.setValue(material_found.tt_value)
    #         self.markup_spinbox.setValue(material_found.markup_value)
    #         entry_date = QDate.fromString(material_found.entry_date, "yyyy-MM-dd")
    #         self.entry_edit.setDate(entry_date)
    #         self.category_combo.setCurrentText(material_found.category)
    #         print("Material found:", material_found.__dict__)
    #     else:
    #         # If no material is found, show a message box
    #         QMessageBox.warning(self, "Material Not Found", "No material found matching the search criteria.")

    def search_material(self):
        search_text = self.name_edit.text()  # Get the search text from the search box
        matching_names = self.material_manager.search_materials(search_text)

        if matching_names:
            if len(matching_names) == 1:
                material = self.material_manager.get_material(matching_names[0])
                self.populate_material_fields(material)
            else:
                self.show_selection_dialog(matching_names)
        else:
            QMessageBox.warning(self, "Material Not Found", "No material found matching the search criteria.")

    def populate_material_fields(self, material):
        self.name_edit.setText(material.name)
        self.tt_edit.setValue(material.tt_value)
        self.markup_spinbox.setValue(material.markup_value)
        self.entry_edit.setDate(QDate.fromString(material.entry_date, "yyyy-MM-dd"))
        self.category_combo.setCurrentText(material.category)

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

    def show_selection_dialog(self, matching_names):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Material")
        dialog_layout = QVBoxLayout()

        list_view = QListView()
        model = QStringListModel()
        model.setStringList(matching_names)
        list_view.setModel(model)

        dialog_layout.addWidget(list_view)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_index = list_view.currentIndex()
            selected_name = model.data(selected_index)
            material = self.material_manager.get_material(selected_name)
            self.populate_material_fields(material)