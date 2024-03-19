import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class Item:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category
        }

class ItemWindow(QMainWindow):
    items = {}  # Dictionary to store items

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

        # Name
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # Description
        description_label = QLabel("Description:")
        self.description_edit = QLineEdit()
        layout.addWidget(description_label)
        layout.addWidget(self.description_edit)

        # Category
        category_label = QLabel("Category:")
        self.category_edit = QLineEdit()
        layout.addWidget(category_label)
        layout.addWidget(self.category_edit)

        # Search and Save buttons
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_item)  # Connect save button to save_item function
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def load_items(self):
        if os.path.exists('items.json'):  # Check if the file exists
            with open('items.json', 'r') as f:
                self.items = json.load(f)  # Load items from file
            print("Items loaded successfully:", self.items)
        else:
            print("No items file found, starting with an empty item set")

    def save_item(self):
        name = self.name_edit.text()
        description = self.description_edit.text()
        category = self.category_edit.text()

        item = Item(name, description, category)
        self.items[name] = item  # Add item to the dictionary

        # Save the items dictionary to a file
        with open('items.json', 'w') as f:
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
