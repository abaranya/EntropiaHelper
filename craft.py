from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, QPushButton, QStyle
from PyQt6.QtCore import Qt
from material import MaterialWindow

class CraftWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Crafting Window")

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        # Set the window to stay on top of other windows
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Blueprint selection
        blueprint_label = QLabel("Blueprint:")
        blueprint_combo = QComboBox()
        layout.addWidget(blueprint_label)
        layout.addWidget(blueprint_combo)

        # Number of attempts
        attempts_label = QLabel("Number of Attempts:")
        attempts_edit = QLineEdit()
        attempts_edit.setMaximumWidth(50)
        attempts_label.setBuddy(attempts_edit)

        # Blueprint and Number of attempts layout
        blueprint_layout = QHBoxLayout()
        blueprint_layout.addWidget(blueprint_label)
        blueprint_layout.addWidget(blueprint_combo, 3)  # Blueprint occupies 75% of width
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

        # Buttons for materials and blueprint
        button_layout = QHBoxLayout()
        materials_button = QPushButton("Materials")
        materials_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        materials_button.clicked.connect(self.open_material_window)  # Connect the button click event to open_material_window method
        blueprint_button = QPushButton("Blueprint")
        blueprint_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        button_layout.addWidget(materials_button)
        button_layout.addWidget(blueprint_button)
        layout.addLayout(button_layout)

    def open_material_window(self):
        self.material_window = MaterialWindow(self.windowOpacity())  # Pass transparency value to MaterialWindow
        self.material_window.show()
