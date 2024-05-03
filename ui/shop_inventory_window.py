from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QWidget, QPushButton, QComboBox


class InventoryWindow(QMainWindow):
    def __init__(self, shop_manager, shop_name="Shop 2"):
        super().__init__()
        self.shop_manager = shop_manager  # This is the centralized manager for all shops
        self.initUI(shop_name)

    def initUI(self, initial_shop):
        self.setWindowTitle(f"Inventory Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create layout and central widget
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Shop selector setup
        self.shop_selector = QComboBox()
        self.shop_selector.addItems(self.shop_manager.shop_inventory.keys())  # Populate from ShopManager
        self.shop_selector.setCurrentText(initial_shop)
        self.shop_selector.currentTextChanged.connect(self.changeShop)  # Handler for changing shop

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Type", "Name", "Price", "TT", "Since Date", "Sold Date"])

        layout.addWidget(self.shop_selector)
        layout.addWidget(self.table)

        self.loadInventory(initial_shop)

    def loadInventory(self, shop_name):
        inventory = self.shop_manager.shop_inventory.get(shop_name)
        self.updateTable(inventory)

    def changeShop(self, shop_name):
        self.setWindowTitle(f"Inventory for {shop_name}")
        self.loadInventory(shop_name)

    def updateTable(self, inventory):
        self.table.clearContents()
        self.table.setRowCount(0)
        if inventory:
            self.table.setRowCount(len(inventory.items) + len(inventory.materials))
            row = 0
            for item in inventory.items.values():
                self.addItemToTable(item, row, "Item")
                row += 1
            for material in inventory.materials.values():
                self.addItemToTable(material, row, "Material")
                row += 1

    def addItemToTable(self, item, row, item_type):
        self.table.setItem(row, 0, QTableWidgetItem(item_type))
        self.table.setItem(row, 1, QTableWidgetItem(item.name))
        self.table.setItem(row, 2, QTableWidgetItem(f"{item.price}"))
        self.table.setItem(row, 3, QTableWidgetItem(item.tt))
        self.table.setItem(row, 4, QTableWidgetItem(item.since_date.strftime('%Y-%m-%d') if item.since_date else ""))
        self.table.setItem(row, 5, QTableWidgetItem(item.sold_date.strftime('%Y-%m-%d') if item.sold_date else ""))
