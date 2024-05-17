import uuid

from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QComboBox, QDateEdit, QMessageBox, QDoubleSpinBox, \
    QLineEdit, QHBoxLayout
from PyQt6.QtCore import QDate

from entity.item import Item
from entity.item_pack import ItemPack
from manager.item_manager import ItemManager
from ui.search_dialog import SearchResultsDialog


class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_manager = ItemManager()
        self.setWindowTitle("Add New Item")
        self.updating = False
        self.layout = QFormLayout(self)

        # ComboBox for item type selection
        self.package_name = QLineEdit(self)
        self.category = QComboBox(self)
        self.category.addItems(self.item_manager.get_categories())

        # name and search button
        self.name_layout = QHBoxLayout()
        self.name = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.name_layout.addWidget(self.name)
        self.name_layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.open_search_dialog)
        self.search_button.setDefault(True)

        # SpinBoxes for currency fields
        self.price = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.price)
        self.price.valueChanged.connect(self.update_markup_based_on_price)

        # Add a SpinBox for the markup percentage
        self.markup = QDoubleSpinBox(self)
        self.markup.setRange(100, 100000)  # Assuming markup ranges from 100% to 1000%
        self.markup.setSuffix("%")  # Add a suffix to denote percentage
        self.markup.setSingleStep(0.1)  # Allow fine control over the percentage
        self.markup.valueChanged.connect(self.update_price_based_on_markup)

        self.tt = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.tt)
        self.tt.valueChanged.connect(self.update_price_based_on_markup)

        # DateEdit widgets for date fields
        self.since_date = QDateEdit(self)
        self.since_date.setCalendarPopup(True)
        self.since_date.setDate(QDate.currentDate())

        self.sold_price = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.sold_price)

        self.sold_date = QDateEdit(self)
        self.sold_date.setCalendarPopup(True)
        self.sold_date.setDate(QDate(2024, 1, 1))

        self.layout.addRow("Package Name", self.package_name)
        self.layout.addRow("Item Type", self.category)
        self.layout.addRow("Name", self.name_layout)
        self.layout.addRow("Price", self.price)
        self.layout.addRow("Markup", self.markup)
        self.layout.addRow("TT", self.tt)
        self.layout.addRow("Since Date", self.since_date)
        self.layout.addRow("Sold Price", self.sold_price)
        self.layout.addRow("Sold Date", self.sold_date)

        self.submit_button = QPushButton("Add Item", self)
        self.submit_button.clicked.connect(self.submit_item)
        self.layout.addRow(self.submit_button)

        self.name.setFocus()

    def setup_currency_spinbox(self, spinbox):
        spinbox.setDecimals(2)
        spinbox.setMaximum(999999999999.99)  # Max 12 digits, including 2 decimals
        spinbox.setPrefix("PED ")  # Prefix to display the currency type

    def open_search_dialog(self):
        if self.item_manager is None:
            self.item_manager = ItemManager()

        search_term = self.name.text()
        dialog = SearchResultsDialog(search_term, self.item_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_name = dialog.get_selected_name()
            if selected_name:
                self.name.setText(selected_name)
                self.update_fields(self.item_manager.get_item(selected_name))
                self.submit_button.setDefault(True)



    def submit_item(self):
        if not self.validate_inputs():
            QMessageBox.critical(self, "Input Error", "Please check the entered values.")
            return  # Keeps the dialog open for correction
        try:
            item = ItemPack(
                category=self.category.currentText(),
                name=self.name.text(),
                price=self.price.value(),
                markup=self.markup.value(),
                tt=self.tt.value(),
                since_date=self.since_date.date().toString("yyyy-MM-dd"),
                sold_price=self.sold_price.value() if self.sold_price.value() > 0 else 0.0,
                sold_date=self.sold_date.date().toString(
                    "yyyy-MM-dd") if self.sold_date.date().isValid() else "2024-01-01"
            )
            package = self.package_name.text()
            self.accept()  # Closes the dialog if no error
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please check the entered values.")
            return  # Keeps the dialog open for correction

        return package, item  # Optionally process this further or adjust behavior based on needs

    def validate_inputs(self):
        return all([
            self.package_name.text().strip(),
            self.name.text().strip(),
            self.category.currentText().strip(),
            self.price.value() > 0,  # Ensure price is more than zero
            self.tt.value() > 0,  # Ensure quantity is more than zero
            self.markup.value() >= 100  # Ensure markup is at least 100%
        ])

    def update_markup_based_on_price(self):
        if self.updating:
            return  # Avoid recursion or unwanted updates

        try:
            self.updating = True
            actual_price = self.price.value()
            actual_tt = self.tt.value()

            if actual_price * actual_tt != 0:
                self.markup.setValue((actual_price / actual_tt) * 100)

        finally:
            self.updating = False

    def update_price_based_on_markup(self):
        if self.updating:
            return  # Avoid recursion or unwanted updates
        try:
            self.updating = True
            actual_tt = self.tt.value()
            actual_markup = self.markup.value() / 100
            if actual_tt * actual_markup != 0:
                self.price.setValue(actual_tt * actual_markup)
        finally:
            self.updating = False

    def update_fields(self, item: Item):
        # Update the fields with the item details
        if item is not None:
            self.name.setText(item.name)
            self.category.setCurrentText(item.category)
            self.markup.setValue(item.markup)
            self.tt.setValue(item.value)
            self.price.setValue(item.value*item.markup/100)

            # Automatically generate package name if not provided
            if not self.package_name.text().strip():  # Check if package name field is empty
                prefix = item.name.replace(" ", "")[:6]  # Use the first four letters of the name
                unique_number = uuid.uuid4().int % (10 ** 12)  # Generate an 8-digit number
                self.package_name.setText(f"{prefix}{unique_number:06d}")  # Set the package name
