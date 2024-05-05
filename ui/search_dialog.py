from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QListWidgetItem


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

        self.layout.addWidget(self.list_widget)
        self.select_button = QPushButton("Select", self)
        self.layout.addWidget(self.select_button)
        self.select_button.clicked.connect(self.select_item)

    def select_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            self.selected_name = selected_item.text()
            self.accept()

    def get_selected_name(self):
        return getattr(self, 'selected_name', None)
