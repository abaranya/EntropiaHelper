from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QComboBox, QDateEdit, QMessageBox, QDoubleSpinBox, \
    QLineEdit, QHBoxLayout, QSpinBox
from PyQt6.QtCore import QDate

from entity.material_pack import MaterialPack
from manager.material_manager import MaterialManager
from ui.search_dialog import SearchResultsDialog


class AddMaterialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.material = None
        self.item_manager = MaterialManager()
        self.setWindowTitle("Add New Material Pack")
        self.layout = QFormLayout(self)

        # ComboBox for item type selection
        self.package_name = QLineEdit(self)
        self.item_type = QComboBox(self)
        self.item_type.addItems(["Ores", "Enmatter", "Robot Parts", "Animal Oils"])

        # name and search button
        self.name_layout = QHBoxLayout()
        self.name = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.name_layout.addWidget(self.name)
        self.name_layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.open_search_dialog)

        # Add a quantity spin box
        self.quantity = QSpinBox(self)
        self.quantity.setMaximum(1000000)  # You can adjust max value as needed
        self.quantity.setSingleStep(1)
        self.quantity.valueChanged.connect(self.update_calculations)

        # Add a SpinBox for the markup percentage
        self.markup = QDoubleSpinBox(self)
        self.markup.setRange(100, 100000)  # Assuming markup ranges from 100% to 1000%
        self.markup.setSuffix("%")  # Add a suffix to denote percentage
        self.markup.setSingleStep(0.1)  # Allow fine control over the percentage
        self.markup.valueChanged.connect(self.update_calculations)

        # SpinBoxes for currency fields
        self.price = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.price)
        self.price.valueChanged.connect(self.update_markup_based_on_price)

        # DateEdit widgets for date fields
        self.since_date = QDateEdit(self)
        self.since_date.setCalendarPopup(True)
        self.since_date.setDate(QDate.currentDate())

        self.sold_price = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.sold_price)

        self.sold_date = QDateEdit(self)
        self.sold_date.setCalendarPopup(True)
        self.sold_date.setDate(QDate.currentDate())

        self.layout.addRow("Package Name", self.package_name)
        self.layout.addRow("Item Type", self.item_type)
        self.layout.addRow("Name", self.name_layout)
        self.layout.addRow("Quantity", self.quantity)
        self.layout.addRow("Price", self.price)
        self.layout.addRow("Markup", self.markup)
        self.layout.addRow("Since Date", self.since_date)
        self.layout.addRow("Sold Price", self.sold_price)
        self.layout.addRow("Sold Date", self.sold_date)

        self.submit_button = QPushButton("Add Material", self)
        self.submit_button.clicked.connect(self.submit_material)
        self.layout.addRow(self.submit_button)

    def setup_currency_spinbox(self, spinbox):
        spinbox.setDecimals(2)
        spinbox.setMaximum(999999999999.99)  # Max 12 digits, including 2 decimals
        spinbox.setPrefix("PED ")  # Prefix to display the currency type

    def open_search_dialog(self):
        if self.item_manager is None:
            self.item_manager = MaterialManager()

        search_term = self.name.text()
        dialog = SearchResultsDialog(search_term, self.item_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_name = dialog.get_selected_name()
            if selected_name:
                self.material = self.item_manager.get_material(selected_name)
                self.update_fields(self.material)

    def submit_material(self):
        if not self.validate_inputs():
            QMessageBox.critical(self, "Input Error", "Please check the entered values and fill all required fields.")
            return  # Keeps the dialog open for correction

        try:
            item = MaterialPack(
                item_type=self.item_type.currentText(),
                name=self.name.text(),
                quantity=self.quantity.value(),
                price=self.price.value(),
                markup=self.markup.value(),
                since_date=self.since_date.date().toString("yyyy-MM-dd")
            )
            package = self.package_name.text()
            self.accept()  # Closes the dialog if no error
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please check the entered values.")
            return  # Keeps the dialog open for correction

        return package, item  # Optionally process this further or adjust behavior based on needs

    def validate_inputs(self):
        # Check for required fields and ensure they contain valid data
        return all([
            self.package_name.text().strip(),
            self.name.text().strip(),
            self.item_type.currentText().strip(),
            self.price.value() > 0,  # Ensure price is more than zero
            self.quantity.value() > 0,  # Ensure quantity is more than zero
            self.markup.value() >= 100  # Ensure markup is at least 100%
        ])

    def update_fields(self, material):
        # Update the fields with the material details
        self.name.setText(material.name)
        self.item_type.setCurrentText(material.category)
        self.markup.setValue(material.markup_value)
        self.price.setValue(material.tt_value)

    def update_calculations(self):
        # Prevent recursive updates
        try:
            self.updating = True

            quantity = self.quantity.value()
            markup = self.markup.value() / 100  # Convert percentage to a multiplier
            tt_value = self.material.tt_value

            # Calculate the new price
            new_price = tt_value * quantity * markup
            self.price.setValue(new_price)

        finally:
            self.updating = False

    def update_markup_based_on_price(self):
        if self.updating:
            return  # Avoid recursion or unwanted updates

        try:
            self.updating = True

            # Calculate markup based on the current price and other fields
            actual_price = self.price.value()
            quantity = self.quantity.value()
            tt_value = self.material.tt_value

            if quantity * tt_value != 0:  # Prevent division by zero
                new_markup = (actual_price / (quantity * tt_value)) * 100  # Convert back to percentage
                self.markup.setValue(new_markup)

        finally:
            self.updating = False
