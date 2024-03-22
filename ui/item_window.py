import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, \
    QComboBox,QMessageBox

from entity.item import Item
from PyQt6.QtWidgets import QDoubleSpinBox

class ItemWindow(QMainWindow):
    items = {}  # Dictionary to store items
    categories = ["Armor Enhancer", "Armor Part", "Armor Plating", "Clothes", "Decoration", "Excavator",
                  "Excavator Enhancer", "Finder", "Finder Amplifier", "Furniture", "Material", "Medical Enhancer",
                  "Medical Tool", "Misc. Tool", "Personal Effect", "Refiner", "Scanner", "Sign",
                  "Storage Container", "Vehicle", "Weapon", "Weapon Attachment", "Weapon Enhancer"]

    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Item Window")
        self.items = {}  # Initialize an empty dictionary to store items
        self.load_items()  # Load items from file when the window is created

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # First Line: Name and Category Labels
        first_line_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        category_label = QLabel("Category:")
        first_line_layout.addWidget(name_label)
        first_line_layout.addWidget(category_label)
        layout.addLayout(first_line_layout)

        # Second Line: Name and Category Fields
        second_line_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        second_line_layout.addWidget(self.name_edit)
        second_line_layout.addWidget(self.category_combo)
        layout.addLayout(second_line_layout)

        # Third Line: Description Label
        description_label = QLabel("Description:")
        layout.addWidget(description_label)

        # Fourth Line: Description Field
        self.description_edit = QLineEdit()
        layout.addWidget(self.description_edit)

        # Fifth Line: Value and Markup Labels
        fifth_line_layout = QHBoxLayout()
        value_label = QLabel("Value:")
        markup_label = QLabel("Markup:")
        fifth_line_layout.addWidget(value_label)
        fifth_line_layout.addWidget(markup_label)
        layout.addLayout(fifth_line_layout)

        # Sixth Line: Value and Markup Fields
        sixth_line_layout = QHBoxLayout()
        self.value_edit = QDoubleSpinBox()
        self.value_edit.setDecimals(2)
        self.value_edit.setSuffix(" PED")
        self.value_edit.setMaximum(9999999.99)
        self.markup_edit = QDoubleSpinBox()
        self.markup_edit.setDecimals(2)
        self.markup_edit.setSuffix(" %")
        self.markup_edit.setMaximum(9999999.99)

        sixth_line_layout.addWidget(self.value_edit)
        sixth_line_layout.addWidget(self.markup_edit)
        layout.addLayout(sixth_line_layout)

        # Seventh Line: TT Cost, Full Cost, and Cost Markup Labels
        seventh_line_layout = QHBoxLayout()
        tt_cost_label = QLabel("TT Cost:")
        full_cost_label = QLabel("Full Cost:")
        cost_markup_label = QLabel("Cost Markup:")
        seventh_line_layout.addWidget(tt_cost_label)
        seventh_line_layout.addWidget(full_cost_label)
        seventh_line_layout.addWidget(cost_markup_label)
        layout.addLayout(seventh_line_layout)

        # Eighth Line: TT Cost, Full Cost, and Cost Markup Fields
        eighth_line_layout = QHBoxLayout()
        self.tt_cost_edit = QDoubleSpinBox()
        self.tt_cost_edit.setDecimals(2)
        self.tt_cost_edit.setSuffix(" PED")
        self.tt_cost_edit.setMaximum(9999999.99)
        self.full_cost_edit = QDoubleSpinBox()
        self.full_cost_edit.setDecimals(2)
        self.full_cost_edit.setSuffix(" PED")
        self.full_cost_edit.setMaximum(9999999.99)
        self.cost_markup_edit = QDoubleSpinBox()
        self.cost_markup_edit.setDecimals(2)
        self.cost_markup_edit.setSuffix(" %")
        self.cost_markup_edit.setMaximum(9999999.99)
        eighth_line_layout.addWidget(self.tt_cost_edit)
        eighth_line_layout.addWidget(self.full_cost_edit)
        eighth_line_layout.addWidget(self.cost_markup_edit)
        layout.addLayout(eighth_line_layout)

        # Ninth Line: Search and Save buttons
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        search_button.clicked.connect(self.search_item)
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_item)  # Connect save button to save_item function
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def search_item(self):
        search_query = self.name_edit.text().strip()
        if search_query:
            found_items = [item for item in self.items.values() if search_query.lower() in item.name.lower()]
            if found_items:
                # For simplicity, let's just take the first found item
                found_item = found_items[0]
                # Update the fields with the details of the found item
                self.name_edit.setText(found_item.name)
                self.description_edit.setText(found_item.description)
                self.category_combo.setCurrentText(found_item.category)
                self.value_edit.setValue(found_item.value)
                self.markup_edit.setValue(found_item.markup)
                self.tt_cost_edit.setValue(found_item.tt_cost)
                self.full_cost_edit.setValue(found_item.full_cost)
                self.cost_markup_edit.setValue(found_item.cost_markup)

                QMessageBox.information(self, "Search Result", "Item found and details updated.")
            else:
                QMessageBox.information(self, "Search Result", "No item found matching the search query.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a search query.")

    def load_items(self):
        if os.path.exists('../data/items.json'):
            with open('../data/items.json', 'r') as f:
                items_data = json.load(f)
                for item_data in items_data.values():
                    item = Item(
                        name=item_data["name"],
                        description=item_data["description"],
                        category=item_data["category"],
                        value=item_data["value"],
                        markup=item_data["markup"],
                        tt_cost=item_data["tt_cost"],
                        full_cost=item_data["full_cost"],
                        cost_markup=item_data["cost_markup"]
                    )
                    self.items[item.name] = item
            print("Items loaded successfully:", self.items)
        else:
            print("No items file found, starting with an empty item set")

    def save_item(self):
        name = self.name_edit.text()
        description = self.description_edit.text()
        category = self.category_combo.currentText()
        value = self.value_edit.value()
        markup = self.markup_edit.value()
        tt_cost = self.tt_cost_edit.value()
        full_cost = self.full_cost_edit.value()
        cost_markup = self.cost_markup_edit.value()

        item = Item(name, description, category, value, markup, tt_cost, full_cost, cost_markup)
        self.items[name] = item  # Add item to the dictionary

        # Save the items dictionary to a file
        with open('../data/items.json', 'w') as f:
            json.dump({name: item.to_dict() for name, item in self.items.items()}, f)

        print("Item saved successfully:", item.__dict__)
    @classmethod
    def get_item(cls, name):
        return cls.items.get(name)

    def validate(self):
        # Add validation logic if needed
        return True

# Example usage:
# item_window = ItemWindow(transparency_value)
# item_window.show()
