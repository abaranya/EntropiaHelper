from PyQt6.QtCore import QFile, QTextStream, QIODevice
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from entity.item_pack import ItemPack


class ItemInventoryTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(8)

        self.verticalHeader().setDefaultSectionSize(10)
        self.setHorizontalHeaderLabels(["Pack", "Type", "Name", "Price", "TT", "Since Date", "Sold Price", "Sold Date"])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # Stretch columns to fill the table width


        self.load_style_sheet()

        # Assign tooltips only after headers have been confirmed set
        for i, title in enumerate(
                ["Pack", "Item Type", "Name of the item", "Price of the item", "TT", "Selling Since", "Sold Price", "Sold Date"]):
            self.horizontalHeaderItem(i).setToolTip(title)

        self.setSortingEnabled(True)

    def load_style_sheet(self):
        file = QFile("resources/styles.qss")
        if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
        file.close()

    def add_item(self, package: str, item: ItemPack):
        row_count = self.rowCount()
        self.insertRow(row_count)

        # Create and set a QTableWidgetItem for the package
        self.setItem(row_count, 0, QTableWidgetItem(str(package)))

        # Start from column 1 because column 0 is the 'package' already set
        for col, value in enumerate(item.field_list(), start=1):
            self.setItem(row_count, col, QTableWidgetItem(str(value)))

        # Optionally scroll to the new row and select it
        self.scrollToItem(self.item(row_count, 0))
        self.selectRow(row_count)

    def delete_selected_item(self):
        current_row = self.currentRow()
        if current_row != -1:
            self.removeRow(current_row)

    def refresh_data(self, new_data):
        self.setRowCount(0)  # Clear existing rows
        for package, item in new_data.items():
            self.add_item(package, item)  # Assume new_data is a dict of {package: item}

    def update_table(self, inventory):
        # Clear the table before updating
        self.clearContents()
        self.setRowCount(0)

        # Iterate over items and add them to the table
        for key, item in inventory.items():
            self.add_item(key, item)
