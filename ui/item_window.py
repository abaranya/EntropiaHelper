import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, \
    QComboBox, QMessageBox, QDoubleSpinBox
from PyQt6.QtCore import QDate, QStringListModel

from entity.item import Item
from manager.item_manager import ItemManager
from PyQt6.QtWidgets import QDialog, QListView, QDialogButtonBox

class ItemWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()

        self.setWindowTitle("Item Window")
        self.item_manager = ItemManager()
        self.load_items()

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
        self.category_combo.addItems(self.item_manager.categories)
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
        save_button.clicked.connect(self.save_item)
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

    def search_item(self):
        search_query = self.name_edit.text().strip()
        if search_query:
            found_items = self.item_manager.item_search(search_query)
            if found_items:
                if len(found_items) == 1:
                    # If only one item is found, update fields with its details
                    found_item = found_items[0]
                    self.populate_item_fields(found_item)
                    # Update other fields...
                    QMessageBox.information(self, "Search Result", "Item found and details updated.")
                else:
                    # If multiple items are found, show a selection dialog
                    self.show_selection_dialog([item.name for item in found_items])
            else:
                QMessageBox.information(self, "Search Result", "No item found matching the search query.")
        else:
            QMessageBox.warning(self, "Search Error", "Please enter a search query.")

    def show_selection_dialog(self, matching_names):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Item")
        dialog_layout = QVBoxLayout()

        list_view = QListView()
        model = QStringListModel()
        model.setStringList(matching_names)
        list_view.setModel(model)

        dialog_layout.addWidget(list_view)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_index = list_view.currentIndex()
            selected_name = model.data(selected_index)
            item = self.item_manager.get_item(selected_name)
            if item:
                self.populate_item_fields(item)
            else:
                QMessageBox.warning(self, "Item Not Found", "The selected item could not be found.")

    def populate_item_fields(self, item):
        self.name_edit.setText(item.name)
        self.description_edit.setText(item.description)
        self.category_combo.setCurrentText(item.category)
        self.value_edit.setValue(item.value)
        self.markup_edit.setValue(item.markup)
        self.tt_cost_edit.setValue(item.tt_cost)
        self.full_cost_edit.setValue(item.full_cost)
        self.cost_markup_edit.setValue(item.cost_markup)

    def load_items(self):
        self.item_manager.load_items()

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
        self.item_manager.add_item(item)

        print("Item saved successfully:", item.__dict__)

    def validate(self):
        # Add validation logic if needed
        return True

