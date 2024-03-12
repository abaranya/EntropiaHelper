from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

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

        # Add widgets
        self.blueprint_combo = QComboBox()
        layout.addWidget(QLabel("Select Blueprint:"))
        layout.addWidget(self.blueprint_combo)

        self.attempts_edit = QLineEdit()
        layout.addWidget(QLabel("Number of Attempts:"))
        layout.addWidget(self.attempts_edit)

        self.cost_per_attempt_label = QLabel("Cost per Attempt:")
        layout.addWidget(self.cost_per_attempt_label)

        self.total_cost_label = QLabel("Total Cost:")
        layout.addWidget(self.total_cost_label)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_cost)
        layout.addWidget(self.calculate_button)

    def calculate_cost(self):
        # Implement cost calculation logic here
        pass
