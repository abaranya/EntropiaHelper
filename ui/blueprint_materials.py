from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDoubleSpinBox, QLineEdit, QStyle, QComboBox, QMessageBox, QDialog
from manager.material_manager import MaterialManager  # Import MaterialManager

class MaterialWidget(QWidget):
    material_rows = []

    def __init__(self):
        super().__init__()
        self.material_manager = MaterialManager()  # Get the singleton instance of MaterialManager

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

    def add_material_row(self, qty=0, name=None):
        # This method adds a new material row to the container
        row_layout = QHBoxLayout()
        qty_edit = QDoubleSpinBox()
        qty_edit.setDecimals(0)
        qty_edit.setValue(qty)
        row_layout.addWidget(qty_edit)
        material_edit = QLineEdit()
        material_edit.setText(name)
        row_layout.addWidget(material_edit)
        search_button = QPushButton()
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        search_button.clicked.connect(lambda checked, row=len(self.material_rows): self.search_material(row))
        row_layout.addWidget(search_button)

        # Add the row layout to the container layout
        self.material_rows.append((qty_edit, material_edit))  # Save references to spin box and line edit
        material_layout = self.materials_row_container.layout()
        material_layout.addLayout(row_layout)

    def search_material(self, row):
        search_text = self.material_rows[row][1].text().strip()  # Get the search text from line edit
        if search_text:
            matching_materials = self.material_manager.search_materials(search_text)
            if matching_materials:
                self.show_material_selection_dialog(row, matching_materials)
            else:
                QMessageBox.warning(self, "No Matches", "No matching materials found.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a search query.")

    def show_material_selection_dialog(self, row, matching_materials):
        dialog = MaterialSelectionDialog(matching_materials)
        if dialog.exec():
            selected_material = dialog.selected_material()
            self.material_rows[row][1].setText(selected_material)

    def get_materials(self):
        materials = []
        for qty_edit, material_edit in self.material_rows:
            name = material_edit.text().strip()
            if name and self.material_manager.get_material(name):
                materials.append({"quantity": qty_edit.value(), "name": name})
        return materials

    def clear_materials(self):
        # Remove all material rows from the layout
        for row_layout in self.material_rows:
            for widget in row_layout:
                widget.setParent(None)
        # Clear the list of material rows
        self.material_rows.clear()


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
