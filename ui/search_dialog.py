from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox

class SearchResultsDialog(QDialog):
    def __init__(self, search_term, manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget(self)

        # Populate the list with search results
        results = manager.search(search_term)
        for result in results:
            QListWidgetItem(result, self.list_widget)

        # Automatically select the first item if there are results
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)  # Select the first item

        self.list_widget.itemDoubleClicked.connect(self.select_item)  # Add double-click to select

        self.layout.addWidget(self.list_widget)
        self.select_button = QPushButton("Select", self)
        self.layout.addWidget(self.select_button)
        self.select_button.clicked.connect(self.select_item)

    def select_item(self, item=None):
        selected_item = item if item else self.list_widget.currentItem()
        if selected_item:
            self.selected_name = selected_item.text()
            self.accept()
        else:
            QMessageBox.warning(self, "Selection Required", "Please select an item before continuing.")

    def get_selected_name(self):
        return getattr(self, 'selected_name', None)
