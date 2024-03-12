from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QStyle, QWidget, QLineEdit, QHBoxLayout, QDoubleSpinBox, QDateTimeEdit
from PyQt6.QtCore import Qt, QDate

class MaterialWindow(QMainWindow):
    def __init__(self, transparency):
        super().__init__()
        self.setWindowTitle("Material Window")

        # Set window opacity based on the transparency value passed from the main application
        self.setWindowOpacity(transparency)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Name
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # TT Value
        tt_label = QLabel("TT Value (PED):")
        self.tt_edit = QDoubleSpinBox()
        self.tt_edit.setSuffix(" PED")
        self.tt_edit.setDecimals(2)
        layout.addWidget(tt_label)
        layout.addWidget(self.tt_edit)

        # Markup value
        markup_label = QLabel("Markup Value (%):")
        self.markup_spinbox = QDoubleSpinBox()
        self.markup_spinbox.setSuffix("%")
        self.markup_spinbox.setDecimals(2)
        layout.addWidget(markup_label)
        layout.addWidget(self.markup_spinbox)

        # Entry Date
        entry_label = QLabel("Entry Date (yyyy-mm-dd):")
        self.entry_edit = QDateTimeEdit()
        self.entry_edit.setDisplayFormat("yyyy-MM-dd")
        self.entry_edit.setDate(QDate.currentDate())  # Set default date to today's date
        layout.addWidget(entry_label)
        layout.addWidget(self.entry_edit)

        # Search and Save buttons
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView))
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        button_layout.addWidget(search_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)
