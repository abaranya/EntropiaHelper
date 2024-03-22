from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDoubleSpinBox, QLineEdit, QStyle


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
        print(f"Searching material for row in {row}")
        pass  # You can implement this method based on your requirements
