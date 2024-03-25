import os

from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QHBoxLayout, QComboBox, \
    QSpinBox, QDoubleSpinBox, QMessageBox, QStyle
from entity.blueprint import Blueprint
from manager.item_manager import ItemManager
from ui.blueprint_materials import MaterialWidget
from manager.blueprint_manager import BlueprintManager


class BlueprintWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()

        script_dir = os.path.dirname(__file__)
        self.blueprint_manager = BlueprintManager(os.path.join(script_dir, '..', 'data', 'blueprints.json'))

        self.setWindowTitle("Blueprint Window")
        self.load_blueprints()

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        first_panel = FirstPanel()
        self.name_edit = first_panel.name_edit
        self.level_edit = first_panel.level_edit
        self.type_combo = first_panel.type_combo
        layout.addWidget(first_panel)

        layout.addWidget(SecondPanel())

        self.materials_container = MaterialWidget()
        layout.addWidget(self.materials_container)

        # Seventh Line: Search, and Save Buttons
        seventh_line_layout = QHBoxLayout()
        self.blueprint_search_button = QPushButton("Search Material")
        self.blueprint_search_button.clicked.connect(self.search_blueprint)
        seventh_line_layout.addWidget(self.blueprint_search_button)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_blueprint)
        seventh_line_layout.addWidget(save_button)

        layout.addLayout(seventh_line_layout)

    def add_material_row(self):
        self.materials_container.add_material_row()

    def search_blueprint(self):
        name_substring = self.name_edit.text().strip()
        if name_substring:
            found_blueprint = self.blueprint_manager.search_blueprint(name_substring)
            if found_blueprint:
                self.populate_blueprint_fields(found_blueprint)
            else:
                QMessageBox.information(self, "Search Result", "No blueprint found matching the name substring.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a name substring to search.")

    def populate_blueprint_fields(self, blueprint):
        self.name_edit.setText(blueprint.name)
        self.level_edit.setValue(blueprint.level)
        index = self.type_combo.findText(blueprint.type)
        if index != -1:
            self.type_combo.setCurrentIndex(index)

        # You may also need to populate materials and other fields based on your application logic

    def load_blueprints(self):
        self.blueprint_manager.load_blueprints()

    def save_blueprint(self):
        name = self.name_edit.text()
        level = self.level_edit.value()
        type = self.type_combo.currentText()

        # Assuming you have a method to retrieve materials from the material container
        materials = self.materials_container.get_materials()

        blueprint = Blueprint(name, level, type, materials)
        self.blueprint_manager.add_blueprint(blueprint)

        print("Blueprint saved successfully:", blueprint)

    def validate(self):
        return True


class FirstPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        name_layout = QVBoxLayout()
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)

        level_layout = QVBoxLayout()
        level_label = QLabel("Level:")
        self.level_edit = QSpinBox()
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_edit)

        type_layout = QVBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Unlimited", "Limited"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)

        layout.addLayout(name_layout)
        layout.addLayout(level_layout)
        layout.addLayout(type_layout)

        self.setLayout(layout)


from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QListView, QVBoxLayout, QMessageBox

class SecondPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        name_layout = QVBoxLayout()
        crafted_item_label = QLabel("Crafted Item:")
        self.crafted_item_edit = QLineEdit()
        name_layout.addWidget(crafted_item_label)
        name_layout.addWidget(self.crafted_item_edit)

        search_layout = QVBoxLayout()
        self.item_search_button = QPushButton()
        self.item_search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.item_search_button.clicked.connect(self.item_search)
        search_layout.addWidget(QLabel())
        search_layout.addWidget(self.item_search_button)

        class_layout = QVBoxLayout()
        class_label = QLabel("Class:")
        self.class_combo = QComboBox()
        self.class_combo.addItems(
            ["Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator",
             "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer",
             "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign", "Storage Container",
             "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"])

        class_layout.addWidget(class_label)
        class_layout.addWidget(self.class_combo)

        layout.addLayout(name_layout)
        layout.addLayout(search_layout)
        layout.addLayout(class_layout)

        self.setLayout(layout)

    def item_search(self):
        item_manager = ItemManager()  # Access the singleton instance of ItemManager
        search_text = self.crafted_item_edit.text().strip()  # Get the search text
        if search_text:
            matching_items = item_manager.item_search(search_text)
            if matching_items:
                self.show_selection_dialog(matching_items)
            else:
                QMessageBox.warning(self, "No Items Found", "No items found matching the search criteria.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a search query.")

    def show_selection_dialog(self, matching_items):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Item")
        dialog_layout = QVBoxLayout()

        list_view = QListView()

        # Extract names from Item objects and convert to strings
        item_names = [item.name for item in matching_items]

        model = QStringListModel(item_names)
        list_view.setModel(model)

        dialog_layout.addWidget(list_view)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_item_index = list_view.selectedIndexes()[0]
            selected_item = matching_items[selected_item_index.row()]
            self.crafted_item_edit.setText(selected_item.name)

