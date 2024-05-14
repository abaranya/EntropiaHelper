from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QDialog, QMessageBox

from entity.shop_inventory import ShopInventory
from manager.shop_manager import ShopManager
from ui.add_item_dialog import AddItemDialog
from ui.add_material_dialog import AddMaterialDialog
from ui.item_inventory_table import ItemInventoryTable
from ui.material_inventory_table import MaterialInventoryTable


class InventoryWindow(QMainWindow):
    def __init__(self, transparency, shop_name="Shop 2"):
        super().__init__()
        self.shop_name = shop_name
        self.shop_manager = ShopManager()  # This is the centralized manager for all shops
        self.current_inventory_type = 'Items'  # Default to 'Items'
        self.init_ui(shop_name)

    def init_ui(self, initial_shop):
        self.setWindowTitle(f"Inventory Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create layout and central widget
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Sets the spacing between widgets in the layout
        layout.setContentsMargins(10, 10, 10, 10)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Shop selector setup
        self.shop_selector = QComboBox()
        self.shop_selector.addItems(self.shop_manager.shop_inventory.keys())  # Populate from ShopManager
        self.shop_selector.setCurrentText(initial_shop)
        self.shop_selector.currentTextChanged.connect(self.change_shop)  # Handler for changing shop

        # Inventory type toggle button
        self.toggle_button = QPushButton("Switch to Materials", self)
        self.toggle_button.clicked.connect(self.toggle_inventory_type)
        layout.addWidget(self.toggle_button)

        # Add item button
        self.add_item_button = QPushButton("Add New Item")
        self.add_item_button.clicked.connect(self.on_add_item)
        layout.addWidget(self.add_item_button)

        # Save inventory button
        self.save_button = QPushButton("Save Inventory")
        self.save_button.clicked.connect(self.save_inventory)
        layout.addWidget(self.save_button)

        # Table setup
        self.item_table = ItemInventoryTable(
            shop_inventory=self.shop_manager.get_shop_inventory(self.shop_name))
        self.material_table = MaterialInventoryTable(
            shop_inventory=self.shop_manager.get_shop_inventory(self.shop_name))

        layout.addWidget(self.shop_selector)
        layout.addWidget(self.item_table)
        layout.addWidget(self.material_table)

        self.load_inventory(initial_shop)

    def load_inventory(self, shop_name):
        if self.current_inventory_type == 'Items':
            self.material_table.hide()
            self.item_table.show()
            inventory = self.shop_manager.get_shop_inventory(shop_name)
            self.update_item_table(inventory)
        else:
            self.item_table.hide()
            self.material_table.show()
            inventory = self.shop_manager.get_shop_inventory(shop_name)
            self.update_material_table(inventory)

    def change_shop(self, shop_name):
        self.shop_name = shop_name
        self.setWindowTitle(f"Inventory for {shop_name}")

        # Retrieve the inventory for the newly selected shop
        if self.current_inventory_type == 'Items':
            inventory = self.shop_manager.get_shop_inventory(shop_name)
            self.item_table.shop_inventory = inventory  # Assuming the table can directly handle inventory object
            self.item_table.update_table(inventory)
        else:
            inventory = self.shop_manager.get_shop_inventory(shop_name)
            self.material_table.shop_inventory = inventory  # Assuming the table can directly handle inventory object
            self.material_table.update_table(inventory)

        # Update the user interface to reflect the change
        self.load_inventory(shop_name)

    def on_add_item(self):
        try:
            if self.current_inventory_type == 'Items':
                dialog = AddItemDialog(self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    package, new_item = dialog.submit_item()
                    self.shop_manager.add_item(self.shop_name, package, new_item)
                    self.item_table.add_item(package, new_item)
            else:
                dialog = AddMaterialDialog(self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    package, new_material = dialog.submit_material()
                    self.shop_manager.add_material(self.shop_name, package, new_material)
                    self.material_table.add_material(package, new_material)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add item/material: {str(e)}")

    def toggle_inventory_type(self):
        if self.current_inventory_type == 'Items':
            self.current_inventory_type = 'Materials'
            self.toggle_button.setText("Switch to Items")
            self.add_item_button.setText("Add New Material")
        else:
            self.current_inventory_type = 'Items'
            self.toggle_button.setText("Switch to Materials")
            self.add_item_button.setText("Add New Item")
        self.load_inventory(self.shop_name)

    def update_item_table(self, inventory: ShopInventory):
        self.item_table.update_table(inventory)
        self.item_table.resizeColumnsToContents()

    def update_material_table(self, inventory: ShopInventory):
        self.material_table.update_table(inventory)
        self.material_table.resizeColumnsToContents()

    def save_inventory(self):
        try:
            # Assuming the ShopManager has a method to save all current inventory to a file or database
            self.shop_manager.save_shop_inventory()
            QMessageBox.information(self, "Save Successful", "The current inventory has been saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", f"Failed to save the inventory: {str(e)}")
