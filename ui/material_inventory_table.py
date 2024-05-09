from PyQt6.QtCore import QFile, QIODevice, QTextStream
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from entity.material_pack import MaterialPack


class MaterialInventoryTable(QTableWidget):
    def __init__(self, parent=None):
        super(MaterialInventoryTable, self).__init__(parent)
        self.setColumnCount(9)  # Set the number of columns to match MaterialPack fields
        self.setHorizontalHeaderLabels(
            ['Pack', 'Item Type', 'Name', 'Quantity', 'Price', 'Markup', 'Since Date', 'Sold Price', 'Sold Date'])
        self.verticalHeader().setDefaultSectionSize(10)  # Standard row height
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # Stretch columns to fill the table width

        self.load_style_sheet()

        # Assign tooltips only after headers have been confirmed set
        for i, title in enumerate(
                ["Pack", "Item Type", "Name of the item", 'Quantity in Pack', "Price of the item", 'Markup',
                 "Selling Since", "Sold Price", "Sold Date"]):
            self.horizontalHeaderItem(i).setToolTip(title)

        self.setSortingEnabled(True)

    def add_material(self, package: str, material: MaterialPack):
        row_count = self.rowCount()
        self.insertRow(row_count)

        # Create and set a QTableWidgetItem for the package
        self.setItem(row_count, 0, QTableWidgetItem(str(package)))

        # Start from column 1 because column 0 is the 'package' already set
        for col, value in enumerate(material.field_list(), start=1):
            self.setItem(row_count, col, QTableWidgetItem(str(value)))

        # Optionally scroll to the new row and select it
        self.scrollToItem(self.item(row_count, 0))
        self.selectRow(row_count)

    def clear_materials(self):
        """Clears all rows from the table."""
        self.setRowCount(0)

    def load_style_sheet(self):
        file = QFile("resources/styles.qss")
        if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
        file.close()

    def update_table(self, inventory):
        self.clearContents()
        self.setRowCount(0)

        for package, material in inventory.items():
            self.add_material(package, material)
