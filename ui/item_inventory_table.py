from functools import partial

from PyQt6.QtCore import QFile, QTextStream, QIODevice, Qt, QDate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QDoubleSpinBox, QDateEdit, QMessageBox

from entity.item_pack import ItemPack
from entity.shop_inventory import ShopInventory
from utils.formatter import Formatter

COLUMNS = 9
SOLD_DATE_COLUMN = COLUMNS - 1
SOLD_PRICE_COLUMN = COLUMNS - 2


class ItemInventoryTable(QTableWidget):
    def __init__(self, parent=None, shop_inventory=None):
        super(ItemInventoryTable, self).__init__(parent)
        self.formatter = Formatter()
        self.shop_inventory = shop_inventory
        self.setColumnCount(COLUMNS)

        self.setHorizontalHeaderLabels(
            ["Pack", "Type", "Name", "Price", "TT", "Markup", "Since Date", "Sold Price", "Sold Date"])

        self.formatter.setLayout([
            self.formatter.format_text,
            self.formatter.format_text,
            self.formatter.format_text,
            self.formatter.format_currency,
            self.formatter.format_currency,
            self.formatter.format_currency,
            self.formatter.format_date,
            self.formatter.format_currency,
            self.formatter.format_date
        ])

        self.verticalHeader().setDefaultSectionSize(10)  # Standard row height
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # Stretch columns to fill the table width

        self.load_style_sheet()

        # Assign tooltips only after headers have been confirmed set
        for i, title in enumerate(
                ["Pack", "Item Type", "Name of the item", "Price of the item", "TT", "Markup", "Selling Since",
                 "Sold Price", "Sold Date"]):
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
        self.setRowHeight(row_count, 10)  # Set to an appropriate value that fits the content
        # Create and set a QTableWidgetItem for the package
        self.setItem(row_count, 0, QTableWidgetItem(str(package)))

        # Initialize other non-widget columns
        for col, value in enumerate(item.field_list(), start=1):
            if col not in [SOLD_DATE_COLUMN, SOLD_PRICE_COLUMN]:  # Exclude columns that will use widgets
                self.setItem(row_count, col, QTableWidgetItem(self.formatter.format(value, col)))

        # Set widgets with centering adjustment
        self.setCellWidget(row_count, SOLD_PRICE_COLUMN, self.create_double_spin_box(item.sold_price))
        self.setCellWidget(row_count, SOLD_DATE_COLUMN, self.create_date_edit(item.sold_date))

        self.connect_row_signals()

    def delete_selected_item(self):
        current_row = self.currentRow()
        if current_row != -1:
            self.removeRow(current_row)

    def setup_editable_cells(self):
        for row in range(self.rowCount()):
            # Check if the widget already exists
            price_editor = self.cellWidget(row, SOLD_PRICE_COLUMN)
            date_editor = self.cellWidget(row, SOLD_DATE_COLUMN)

            # Only create and set if not already present
            if not price_editor:
                price_editor = self.create_double_spin_box()
                self.setCellWidget(row, SOLD_PRICE_COLUMN, price_editor)
                price_editor.editingFinished.connect(partial(self.commit_price_change, row))

            if not date_editor:
                date_editor = self.create_date_edit()
                self.setCellWidget(row, SOLD_DATE_COLUMN, date_editor)
                date_editor.editingFinished.connect(partial(self.commit_date_change, row))

    def update_table(self, inventory: ShopInventory):
        self.clearContents()
        self.setRowCount(0)
        self.shop_inventory = inventory

        for package, item in inventory.get_items().items():
            self.add_item(package, item)
        self.setup_editable_cells()  # Re-setup editable cells every time the table is updated

    def create_double_spin_box(self, initial_value=None):
        editor = QDoubleSpinBox()
        editor.setDecimals(2)
        editor.setMaximum(999999999999.99)  # Increased max value to ensure it's not a limiting factor
        editor.setPrefix("PED ")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editor.setValue(initial_value if initial_value is not None else 0.0)
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
        new_price = self.cellWidget(row, SOLD_PRICE_COLUMN).value() if self.cellWidget(row, SOLD_PRICE_COLUMN) else None
        try:
            self.shop_inventory.update_field_value("items", package, "sold_price", new_price)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to update sold price for {package}: {str(e)}")

    def commit_date_change(self, row):
        package = self.item(row, 0).text()
        new_date = self.cellWidget(row, SOLD_DATE_COLUMN).date().toString("yyyy-MM-dd") \
            if self.cellWidget(row, SOLD_DATE_COLUMN) else None
        try:
            self.shop_inventory.update_field_value("items", package, "sold_date", new_date)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to update sold date for {package}: {str(e)}")

    def connect_row_signals(self):
        for row in range(self.rowCount()):
            # Retrieve the widgets from the cell widgets if they are containers
            # or directly if they are not wrapped in another widget.
            price_editor = self.cellWidget(row, SOLD_PRICE_COLUMN)  # Assuming column 6 is the Sold Price
            date_editor = self.cellWidget(row, SOLD_DATE_COLUMN)  # Assuming column 7 is the Sold Date

            # If the editors are placed directly without container, retrieve directly
            if isinstance(price_editor, QDoubleSpinBox):
                # Disconnect existing connections to avoid duplicates
                try:
                    price_editor.editingFinished.disconnect()
                except TypeError:
                    # No connections exist yet, so nothing to disconnect
                    pass
                # Connect the editingFinished signal to the commit_price_change method
                price_editor.editingFinished.connect(partial(self.commit_price_change, row))

            if isinstance(date_editor, QDateEdit):
                # Disconnect existing connections to avoid duplicates
                try:
                    date_editor.editingFinished.disconnect()
                except TypeError:
                    # No connections exist yet, so nothing to disconnect
                    pass
                # Connect the editingFinished signal to the commit_date_change method
                date_editor.editingFinished.connect(partial(self.commit_date_change, row))

