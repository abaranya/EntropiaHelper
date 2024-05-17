from functools import partial

from PyQt6.QtCore import Qt, QFile, QIODevice, QTextStream, QDate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QDoubleSpinBox, QDateEdit, QMessageBox, \
    QWidget, QHBoxLayout, QVBoxLayout

from entity.material_pack import MaterialPack
from entity.shop_inventory import ShopInventory

COLUMNS = 9
SOLD_DATE_COLUMN = COLUMNS - 1
SOLD_PRICE_COLUMN = COLUMNS - 2

class MaterialInventoryTable(QTableWidget):
    def __init__(self, parent=None, shop_inventory=None):
        super(MaterialInventoryTable, self).__init__(parent)
        self.shop_inventory = shop_inventory
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
        self.setRowHeight(row_count, 10)  # Set to an appropriate value that fits the content
        self.setItem(row_count, 0, QTableWidgetItem(str(package)))

        # Initialize other non-widget columns
        for col, value in enumerate(material.field_list(), start=1):
            if col not in [SOLD_PRICE_COLUMN, SOLD_DATE_COLUMN]:  # Exclude columns that will use widgets
                self.setItem(row_count, col, QTableWidgetItem(str(value)))

        # Set widgets with centering adjustment
        self.setCellWidget(row_count, SOLD_PRICE_COLUMN, self.create_double_spin_box(material.sold_price))
        self.setCellWidget(row_count, SOLD_DATE_COLUMN, self.create_date_edit(material.sold_date))

        self.connect_row_signals()

    def clear_materials(self):
        """Clears all rows from the table."""
        self.setRowCount(0)

    def load_style_sheet(self):
        file = QFile("resources/styles.qss")
        if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
        file.close()

    def update_table(self, inventory: ShopInventory):
        self.clearContents()
        self.setRowCount(0)
        self.shop_inventory = inventory

        for package, material in inventory.get_materials().items():
            self.add_material(package, material)
        self.setup_editable_cells()  # Re-setup editable cells every time the table is updated

    def setup_editable_cells(self):
        for row in range(self.rowCount()):
            # Check if the widget already exists
            price_editor = self.cellWidget(row, 7)
            date_editor = self.cellWidget(row, 8)

            # Only create and set if not already present
            if not price_editor:
                price_editor = self.create_double_spin_box()
                self.setCellWidget(row, 7, price_editor)
                price_editor.editingFinished.connect(partial(self.commit_price_change, row))

            if not date_editor:
                date_editor = self.create_date_edit()
                self.setCellWidget(row, 8, date_editor)
                date_editor.editingFinished.connect(partial(self.commit_date_change, row))

    def connect_row_signals(self):
        for row in range(self.rowCount()):
            # Retrieve the widgets directly if not contained, or from the layout if contained
            price_editor = self.cellWidget(row, 7)  # Assuming this directly returns the QDoubleSpinBox
            date_editor = self.cellWidget(row, 8)  # Assuming this directly returns the QDateEdit

            if isinstance(price_editor, QWidget):  # Check if it's the correct widget type
                # Disconnect possible existing connections to avoid multiple triggerings
                try:
                    price_editor.editingFinished.disconnect()
                except TypeError:
                    pass  # No previous connections
                # Connect with partial to correctly handle the row reference
                price_editor.editingFinished.connect(partial(self.commit_price_change, row))

            if isinstance(date_editor, QWidget):
                try:
                    date_editor.editingFinished.disconnect()
                except TypeError:
                    pass  # No previous connections
                date_editor.editingFinished.connect(partial(self.commit_date_change, row))

    def create_double_spin_box(self, initial_value=None):
        editor = QDoubleSpinBox()
        editor.setDecimals(2)
        editor.setMaximum(99999999.99)
        editor.setPrefix("PED ")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editor.setValue(0.0 if initial_value is None else initial_value)
        return editor

    def create_date_edit(self, initial_date=None):
        editor = QDateEdit()
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("yyyy-MM-dd")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editor.setDate(QDate.currentDate() if initial_date is None else initial_date)
        return editor

    def commit_price_change(self, row):
        package = self.item(row, 0).text()
        new_price = self.cellWidget(row, 7).value()
        try:
            self.shop_inventory.update_field_value("materials", package, "sold_price", new_price)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to update sold price for {package}: {str(e)}")

    def commit_date_change(self, row):
        package = self.item(row, 0).text()
        new_date = self.cellWidget(row, 8).date().toString("yyyy-MM-dd")
        try:
            self.shop_inventory.update_field_value("materials", package, "sold_date", new_date)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to update sold date for {package}: {str(e)}")
