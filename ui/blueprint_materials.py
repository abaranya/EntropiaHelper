from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDoubleSpinBox, QLineEdit, QStyle, QComboBox, QMessageBox, QDialog


class MaterialWidget(QWidget):
    material_rows = []

    def __init__(self):
        super().__init__()

        # Create the layout for the material widget
        layout = QVBoxLayout()

        # Material label
        labels_layout = QHBoxLayout()
        self.material_quantity = QLabel("Quantity:")
        self.material_label = QLabel("Material:")
        self.add_material_button = QPushButton("+")
        labels_layout.addWidget(self.material_quantity)
        labels_layout.addWidget(self.material_label)
        labels_layout.addWidget(self.add_material_button)
        layout.addLayout(labels_layout)

        # Container for adding material rows
        self.materials_row_container = QWidget()
        material_layout = QVBoxLayout()
        self.materials_row_container.setLayout(material_layout)
        layout.addWidget(self.materials_row_container)

        # Set the layout of the widget
        self.setLayout(layout)

        # Connect the add material button to add_material_row method
        self.add_material_button.clicked.connect(self.add_material_row)

    def add_material_row(self):
        # This method adds a new material row to the container
        row_layout = QHBoxLayout()
        qty_edit = QDoubleSpinBox()
        row_layout.addWidget(qty_edit)
        material_edit = QLineEdit()
        row_layout.addWidget(material_edit)
        search_button = QPushButton()
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        search_button.clicked.connect(lambda checked, row=len(self.material_rows): self.search_material(row))
        row_layout.addWidget(search_button)

        # Add the row layout to the container layout
        self.material_rows.append(row_layout)
        material_layout = self.materials_row_container.layout()
        material_layout.addLayout(row_layout)

    def search_material(self, row):
        matching_materials = [material for material in self.materials_dict if self.material_rows[row].lower() in material.lower()]

        if matching_materials:
            # If multiple materials are found, prompt the user to choose from a list
            if len(matching_materials) > 1:
                self.show_material_selection_dialog(row, matching_materials)
            else:
                # If only one material is found, set it directly in the QLineEdit
                self.material_rows[row].material_edit.setText(matching_materials[0])
        else:
            QMessageBox.information(self, "No Matches", "No matching materials found.")

    def show_material_selection_dialog(self, row, matching_materials):
        dialog = MaterialSelectionDialog(matching_materials)
        if dialog.exec():
            selected_material = dialog.selected_material()
            self.material_rows[row].material_edit.setText(selected_material)

    class MaterialSelectionDialog(QDialog):
        def __init__(self, materials):
            super().__init__()
            self.materials = materials

            self.setWindowTitle("Select Material")
            layout = QVBoxLayout()

            self.material_combo = QComboBox()
            self.material_combo.addItems(materials)
            layout.addWidget(self.material_combo)

            self.select_button = QPushButton("Select")
            self.select_button.clicked.connect(self.accept)
            layout.addWidget(self.select_button)

            self.setLayout(layout)

        def selected_material(self):
            return self.material_combo.currentText()