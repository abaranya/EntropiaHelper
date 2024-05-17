from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton


class MaterialSelectionDialog(QDialog):
    def __init__(self, materials):
        super().__init__()
        self.materials = materials

        self.setWindowTitle("Select Material")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
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