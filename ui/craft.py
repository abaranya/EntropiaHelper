from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, \
    QPushButton, QStyle, QGroupBox
from PyQt6.QtCore import Qt
from ui.action_panel import ActionPanel


class CraftWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Crafting Window")
        self.setWindowOpacity(transparency)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Blueprint selection
        blueprint_label = QLabel("Blueprint:")
        blueprint_edit = QLineEdit()
        layout.addWidget(blueprint_label)
        layout.addWidget(blueprint_edit)

        # Number of attempts
        attempts_label = QLabel("Number of Attempts:")
        attempts_edit = QLineEdit()
        attempts_edit.setMaximumWidth(50)
        attempts_label.setBuddy(attempts_edit)

        # Blueprint and Number of attempts layout
        blueprint_layout = QHBoxLayout()
        blueprint_layout.addWidget(blueprint_label)
        blueprint_layout.addWidget(blueprint_edit, 3)  # Blueprint occupies 75% of width
        blueprint_layout.addWidget(attempts_label)
        blueprint_layout.addWidget(attempts_edit)  # Number of attempts occupies the remaining space
        layout.addLayout(blueprint_layout)

        # Materials grid
        materials_label = QLabel("Materials:")
        materials_grid = QGridLayout()
        materials_grid.addWidget(QLabel("Qty"), 0, 0)
        materials_grid.addWidget(QLabel("Material"), 0, 1)
        materials_grid.addWidget(QLabel("TT Value"), 0, 2)
        materials_grid.addWidget(QLabel("Markup"), 0, 3)
        materials_grid.addWidget(QLabel("Total Cost"), 0, 4)

        # Dummy data for materials (replace with actual data)
        material_data = [
            {"qty": "", "material": "", "tt_value": "", "markup": "", "total_cost": ""},
            {"qty": "", "material": "", "tt_value": "", "markup": "", "total_cost": ""},
            {"qty": "", "material": "", "tt_value": "", "markup": "", "total_cost": ""},
        ]

        for row, material_info in enumerate(material_data, start=1):
            for col, (label, value) in enumerate(material_info.items()):
                widget = QLineEdit() if label != "Material" else QComboBox()  # Use QComboBox for Material column
                widget.setText(value)  # Set text for QLineEdit widgets
                materials_grid.addWidget(widget, row, col)

        layout.addWidget(materials_label)
        layout.addLayout(materials_grid)

        # Cost per attempt
        cost_per_attempt_label = QLabel("Cost per Attempt:")
        cost_per_attempt_value = QLineEdit()
        layout.addWidget(cost_per_attempt_label)
        layout.addWidget(cost_per_attempt_value)

        # Total cost
        total_cost_label = QLabel("Total Cost:")
        total_cost_value = QLineEdit()
        layout.addWidget(total_cost_label)
        layout.addWidget(total_cost_value)

        # Encapsulate buttons within a panel
        buttons_panel = ActionPanel()
        layout.addWidget(buttons_panel)