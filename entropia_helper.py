import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, \
    QStyle
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import qdarktheme

from manager.shop_manager import ShopManager
from ui.config import ConfigWindow
from ui.craft import CraftWindow
from ui.shop_inventory_window import InventoryWindow


class EntropiaHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entropia Helper")
        self.play_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.pause_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        self.setStyleSheet("background-color: #202020; color: white;")
        self.config_window = ConfigWindow()  # Initialize config_window to be used to load config_dta
        self.craft_window = None  # Initialize craft_window attribute
        self.shop_window = None

        self.create_widgets()
        self.load_config()  # Load configuration from file

    def create_widgets(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)) # Add spacer item to push everything to the right

        self.start_stop_button = QPushButton(self)
        self.start_stop_button.setStyleSheet("background-color: #404040; color: white;")
        self.start_stop_button.setIcon(self.play_icon)
        self.start_stop_button.state = "paused"
        self.start_stop_button.clicked.connect(self.toggle_start_stop)  # Connect the button click event to toggle_start_stop method
        layout.addWidget(self.start_stop_button)

        bold_font = QFont()
        bold_font.setBold(True)

        self.total_value_label = QLabel("Total Value:", self)
        layout.addWidget(self.total_value_label)

        self.total_value_value = QLabel("0 PED", self)
        self.total_value_value.setFont(bold_font)
        layout.addWidget(self.total_value_value)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.last_mob_loot_label = QLabel("Last Mob Loot Value:", self)
        layout.addWidget(self.last_mob_loot_label)

        self.last_mob_loot_value = QLabel("0 PED", self)
        self.last_mob_loot_value.setFont(bold_font)
        layout.addWidget(self.last_mob_loot_value)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.last_processed_label = QLabel("Last Processed Time:", self)
        layout.addWidget(self.last_processed_label)

        self.last_processed_value = QLabel("None", self)
        self.last_processed_value.setFont(bold_font)
        layout.addWidget(self.last_processed_value)

        # Set fixed height for the main window
        self.setFixedHeight(self.start_stop_button.sizeHint().height() + 20)  # Adding 20 pixels margin

        self.shop_button = QPushButton(self)
        self.shop_button.setStyleSheet("background-color: #404040; color: white;")
        # self.shop_button.clicked.connect(self.shop_button_clicked)  # Connect the button click event to a method
        self.shop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView))
        layout.addWidget(self.shop_button)

        # Add the "craft" button and connect it to open_craft_window method
        self.craft_button = QPushButton(self)
        self.craft_button.setStyleSheet("background-color: #404040; color: white;")
        self.craft_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_CommandLink))
        self.craft_button.clicked.connect(self.open_craft_window)
        layout.addWidget(self.craft_button)

        # Add the "craft" button and connect it to open_craft_window method
        self.shop_button = QPushButton(self)
        self.shop_button.setStyleSheet("background-color: #404040; color: white;")
        self.shop_button.setIcon(QIcon.fromTheme("weather-few-clouds"))
        self.shop_button.clicked.connect(self.open_shop_window)
        layout.addWidget(self.shop_button)

        # Add Config button at the end
        self.config_button = QPushButton(self)
        self.config_button.setStyleSheet("background-color: #404040; color: white;")
        self.config_button.clicked.connect(self.open_config_window)
        self.config_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)) # Set system default setting icon
        layout.addWidget(self.config_button)

        # Add minimize button
        self.minimize_button = QPushButton(self)
        self.minimize_button.setStyleSheet("background-color: #404040; color: white;")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton))
        layout.addWidget(self.minimize_button)

        # Add close button with close icon
        self.close_button = QPushButton(self)
        self.close_button.setStyleSheet("background-color: #404040; color: white;")
        self.close_button.setIcon(QIcon.fromTheme("window-close"))  # Use system default close icon
        if self.close_button.icon().isNull():  # If theme icon not available, use platform-specific icon
            self.close_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        # Make the window stay always on top
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)


    def toggle_start_stop(self):
        current_icon = self.start_stop_button.icon()
        if self.start_stop_button.state == "paused":
            # Start the application logic
            self.start_stop_button.state = "running"
            self.running = True
            self.start_reading()
            # Change icon to pause when clicked
            self.start_stop_button.setIcon(self.pause_icon)
        elif self.start_stop_button.state == "running":
            self.start_stop_button.state = "paused"
            # Stop the application logic
            self.running = False
            # Change icon to play when clicked
            self.start_stop_button.setIcon(self.play_icon)

    def open_config_window(self):
        if self.config_window is None:  # Check if config_window is already created
            self.config_window = ConfigWindow()
            self.config_window.show()
        else:
            self.config_window.show()

    def open_craft_window(self):
        if self.craft_window is None:  # Check if craft_window is already created
            self.craft_window = CraftWindow(self.transparency)
            self.craft_window.show()
        else:
            self.craft_window.show()

    def open_shop_window(self):
        if self.shop_window is None:  # Check if shop_window is already created
            self.shop_window = InventoryWindow(self.transparency)
            self.shop_window.show()
        else:
            self.shop_window.show()

    def start_reading(self):
        pass  # Placeholder for reading logic

    def load_config(self):
        config_data = self.config_window.load_config()
        self.transparency = config_data.get("transparency", 0.6)
        self.setWindowOpacity(float(self.transparency))

    def save_config(self):
        # Implement save_config logic if needed
        pass

    def closeEvent(self, event):
        # Implement closeEvent logic if needed
        pass

def main():
    app = QApplication(sys.argv)

    qdarktheme.setup_theme()
    entropia_helper_app = EntropiaHelperApp()
    entropia_helper_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
