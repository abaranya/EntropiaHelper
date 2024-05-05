from PyQt6.QtWidgets import QDialog, QFormLayout, QPushButton, QComboBox, QDateEdit, QMessageBox, QDoubleSpinBox, \
    QLineEdit, QHBoxLayout
from PyQt6.QtCore import QDate

from entity.item_pack import ItemPack
from manager.item_manager import ItemManager
from ui.search_dialog import SearchResultsDialog


class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_manager = ItemManager()
        self.setWindowTitle("Add New Item")
        self.layout = QFormLayout(self)



        # ComboBox for item type selection
        self.package_name = QLineEdit(self)
        self.item_type = QComboBox(self)
        self.item_type.addItems(["Armour", "Weapons", "Amplifiers"])

        #name and search button
        self.name_layout = QHBoxLayout()
        self.name = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.name_layout.addWidget(self.name)
        self.name_layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.open_search_dialog)

        # SpinBoxes for currency fields
        self.price = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.price)

        self.tt = QDoubleSpinBox(self)
        self.setup_currency_spinbox(self.tt)

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
        self.layout.addRow("Price", self.price)
        self.layout.addRow("TT", self.tt)
        self.layout.addRow("Since Date", self.since_date)
        self.layout.addRow("Sold Price", self.sold_price)
        self.layout.addRow("Sold Date", self.sold_date)

        self.submit_button = QPushButton("Add Item", self)
        self.submit_button.clicked.connect(self.submit_item)
        self.layout.addRow(self.submit_button)

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
                self.tt.setValue(self.item_manager.get_item(selected_name).value)

    def submit_item(self):
        try:
            item = ItemPack(self.item_type.currentText(), self.name.text(), self.price.value(), self.tt.value(), self.since_date.date().toString("yyyy-MM-dd"))
            # item_details = {
            #     "item_type": self.item_type.currentText(),
            #     "name": self.name.text(),
            #     "price": self.price.value(),
            #     "tt": self.tt.value(),
            #     "since_date": self.since_date.date().toString("yyyy-MM-dd"),
            #     "sold_price": self.sold_price.value(),
            #     "sold_date": self.sold_date.date().toString("yyyy-MM-dd")
            # }
            package = self.package_name.text()
            self.accept()  # Closes the dialog if no error
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please check the entered values.")
            return  # Keeps the dialog open for correction

        return package, item  # Optionally process this further or adjust behavior based on needs