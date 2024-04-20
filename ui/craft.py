from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QVBoxLayout, QGridLayout, QWidget, QHBoxLayout, \
    QPushButton, QStyle, QGroupBox, QInputDialog, QMessageBox, QDoubleSpinBox
from PyQt6.QtCore import Qt

from manager.blueprint_manager import BlueprintManager
from ui.action_panel import ActionPanel
from ui.craft_material_grid import CraftMaterialGrid


class CraftWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Crafting Window")
        self.setWindowOpacity(1.0)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        blueprint_groupbox = BlueprintGroupBox()
        layout.addWidget(blueprint_groupbox)

        self.craft_material_grid = CraftMaterialGrid()
        layout.addWidget(self.craft_material_grid)

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


class BlueprintGroupBox(QGroupBox):
    def __init__(self):
        super().__init__("Craft Blueprint")
        self.attempts_edit = None
        self.blueprint_name_edit = None
        self.search_button = None
        self.calculate_button = None
        self.blueprint_manager = BlueprintManager()
        self.blueprint = None
        self.init_ui()

    def init_ui(self):

        # Blueprint name
        blueprint_name_label = QLabel("Blueprint:")
        self.blueprint_name_edit = QLineEdit()

        # Search button
        self.search_button = QPushButton("")
        self.search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.search_button.clicked.connect(self.search_blueprint)

        # Number of attempts
        attempts_label = QLabel("Number of Attempts:")
        self.attempts_edit = QDoubleSpinBox()
        self.attempts_edit.setDecimals(0)
        self.attempts_edit.setRange(0, 10000)
        attempts_label.setBuddy(self.attempts_edit)

        self.calculate_button = QPushButton("")
        self.calculate_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        # self.calculate_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))
        self.calculate_button.clicked.connect(self.calculate_blueprint)

        # Layout for blueprint name and number of attempts
        layout = QVBoxLayout()
        blueprint_layout = QHBoxLayout()
        blueprint_layout.addWidget(blueprint_name_label)
        blueprint_layout.addWidget(self.blueprint_name_edit, 4)  # Blueprint occupies 66% of width
        blueprint_layout.addWidget(self.search_button)
        blueprint_layout.addWidget(attempts_label)
        blueprint_layout.addWidget(self.attempts_edit)  # Number of attempts occupies the remaining space
        blueprint_layout.addWidget(self.calculate_button)
        layout.addLayout(blueprint_layout)

        self.setLayout(layout)

    def search_blueprint(self):
        # Retrieve the substring entered in the blueprint name edit field
        blueprint_substring = self.blueprint_name_edit.text().strip()

        # Search for blueprints that match the substring
        matching_blueprints = self.blueprint_manager.search_blueprint(blueprint_substring)

        if matching_blueprints:
            if len(matching_blueprints) == 1:
                # If only one blueprint matches, automatically populate the edit field
                self.blueprint_name_edit.setText(matching_blueprints[0])
            else:
                # If multiple blueprints match, let the user pick one from a dialog
                selected_blueprint, ok_pressed = QInputDialog.getItem(self, "Select Blueprint", "Blueprints:",
                                                                      matching_blueprints, 0, False)

                if ok_pressed and selected_blueprint:
                    self.blueprint_name_edit.setText(selected_blueprint)
        else:
            QMessageBox.information(self, "Search Result", "No blueprints found matching the name substring.")

    def calculate_blueprint(self):
        pass

