from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QStyle, QGroupBox
from ui.blueprint_window import BlueprintWindow
from ui.item_window import ItemWindow
from ui.material_window import MaterialWindow


class ActionPanel(QGroupBox):
    def __init__(self):
        super().__init__("Manage")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        materials_button = QPushButton("Materials")
        materials_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        materials_button.clicked.connect(self.open_material_window)  # Connect to open_material_window method

        items_button = QPushButton("Items")
        items_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        items_button.clicked.connect(self.open_items_window)  # Connect to open_items_window method

        blueprint_button = QPushButton("Blueprint")
        blueprint_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        blueprint_button.clicked.connect(self.open_blueprint_window)  # Connect to open_blueprint_window method

        layout.addWidget(materials_button)
        layout.addWidget(items_button)
        layout.addWidget(blueprint_button)

        self.setLayout(layout)

    def open_material_window(self):
        self.material_window = MaterialWindow(self.windowOpacity())  # Pass transparency value to MaterialWindow
        self.material_window.show()

    def open_blueprint_window(self):
        self.blueprint_window = BlueprintWindow(self.windowOpacity())  # Pass transparency value to BlueprintWindow
        self.blueprint_window.show()

    def open_items_window(self):
        self.item_window = ItemWindow(self.windowOpacity())  # Pass transparency value to ItemsWindow
        self.item_window.show()

