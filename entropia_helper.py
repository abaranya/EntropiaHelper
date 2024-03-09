import sys  # Import the sys module

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QCheckBox, QLineEdit
from PyQt6.QtGui import QFont, QCloseEvent
from PyQt6.QtCore import Qt  # Import the Qt module for flags
import json

class EntropiaHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entropia Helper")
        self.setStyleSheet("background-color: #202020; color: white;")
        self.config_window = None  # Initialize config_window as None

        self.create_widgets()
        self.load_config()  # Load configuration from file

    def create_widgets(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)) # Add spacer item to push everything to the right

        self.start_stop_button = QPushButton("Start", self)
        self.start_stop_button.setStyleSheet("background-color: #404040; color: white;")
        self.start_stop_button.clicked.connect(self.toggle_start_stop)
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

        # Add Config button at the end
        self.config_button = QPushButton("Config", self)
        self.config_button.setStyleSheet("background-color: #404040; color: white;")
        self.config_button.clicked.connect(self.open_config_window)
        layout.addWidget(self.config_button)

        # Add minimize button
        self.minimize_button = QPushButton("Minimize", self)
        self.minimize_button.setStyleSheet("background-color: #404040; color: white;")
        self.minimize_button.clicked.connect(self.showMinimized)
        layout.addWidget(self.minimize_button)

        # Add close button
        self.close_button = QPushButton("Close", self)
        self.close_button.setStyleSheet("background-color: #404040; color: white;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

    def toggle_start_stop(self):
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText("Stop")
            self.running = True
            self.start_reading()
        else:
            self.start_stop_button.setText("Start")
            self.running = False

    def open_config_window(self):
        if self.config_window is None:  # Check if config_window is already created
            self.config_window = QMainWindow()
            self.config_window.setWindowTitle("Configuration")
            self.config_window.setStyleSheet("background-color: #202020; color: white;")

            central_widget = QWidget()
            layout = QVBoxLayout()  # Use QVBoxLayout for vertical layout
            central_widget.setLayout(layout)
            self.config_window.setCentralWidget(central_widget)

           # File Path Entry
            file_path_label = QLabel("File Path:", self)
            layout.addWidget(file_path_label)
            self.file_path_entry = QLineEdit(self)
            layout.addWidget(self.file_path_entry)

            # Load configuration from file
            try:
                with open("config.json", "r") as file:
                    config = json.load(file)
                    transparency = config.get("transparency", 0.6)
                    file_path = config.get("file_path", "")
                    start_from_end = config.get("start_from_end", False)
                    start_date = config.get("start_date", "")
                    start_time = config.get("start_time", "")

            except FileNotFoundError:
                transparency = 0.6
                file_path = ""
                start_from_end = False
                start_date = ""
                start_time = ""

            # First Line: File Path and Start from End checkbox
            file_path_layout = QHBoxLayout()
            layout.addLayout(file_path_layout)

            file_path_label = QLabel("File Path:", self)
            file_path_layout.addWidget(file_path_label)
            self.file_path_entry = QLineEdit(self)
            self.file_path_entry.setText(file_path)
            self.file_path_entry.setStyleSheet("background-color: #303030; color: white;")
            file_path_layout.addWidget(self.file_path_entry)

            self.start_from_end_checkbox = QCheckBox("Start from End", self)
            self.start_from_end_checkbox.setStyleSheet("background-color: #202020; color: white;")
            self.start_from_end_checkbox.setChecked(start_from_end)
            file_path_layout.addWidget(self.start_from_end_checkbox)

            # Second Line: Start Date and Start Time
            start_time_layout = QHBoxLayout()
            layout.addLayout(start_time_layout)

            start_date_label = QLabel("Start Date:", self)
            start_time_layout.addWidget(start_date_label)
            self.start_date_entry = QLineEdit(self)
            self.start_date_entry.setText(start_date)
            self.start_date_entry.setStyleSheet("background-color: #303030; color: white;")
            start_time_layout.addWidget(self.start_date_entry)

            start_time_label = QLabel("Start Time:", self)
            start_time_layout.addWidget(start_time_label)
            self.start_time_entry = QLineEdit(self)
            self.start_time_entry.setText(start_time)
            self.start_time_entry.setStyleSheet("background-color: #303030; color: white;")
            start_time_layout.addWidget(self.start_time_entry)

            # Third Line: Transparency
            transparency_layout = QHBoxLayout()
            layout.addLayout(transparency_layout)

            transparency_label = QLabel("Transparency:", self)
            transparency_layout.addWidget(transparency_label)
            self.transparency_entry = QLineEdit(self)
            self.transparency_entry.setText(str(transparency))
            self.transparency_entry.setStyleSheet("background-color: #303030; color: white;")
            transparency_layout.addWidget(self.transparency_entry)

            # Fourth Line: Save Button
            save_layout = QHBoxLayout()
            layout.addLayout(save_layout)

            save_button = QPushButton("Save", self)
            save_button.setStyleSheet("background-color: #404040; color: white;")
            save_button.clicked.connect(self.save_config)
            save_layout.addWidget(save_button)

            self.config_window.show()
        else:
            self.config_window.show()

    def start_reading(self):
        pass  # Placeholder for reading logic

    def load_config(self):
        # Load configuration from file
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
                transparency = config.get("transparency", 0.6)
                self.setWindowOpacity(float(transparency))  # Set transparency of the main window
        except FileNotFoundError:
            pass  # Ignore if config file doesn't exist

    def save_config(self):
        # Save configuration to file
        config = {
            "file_path": self.file_path_entry.text(),
            "start_from_end": self.start_from_end_checkbox.isChecked(),
            "start_date": self.start_date_entry.text(),
            "start_time": self.start_time_entry.text(),
            "transparency": float(self.transparency_entry.text())  # Convert transparency to float
        }
        with open("config.json", "w") as file:
            json.dump(config, file)
        self.config_window.close()  # Close config window after saving

    def closeEvent(self, event: QCloseEvent):
        # Override close event to handle window closing
        # Save configuration before closing the main window
        self.save_config()
        event.accept()  # Accept the close event

def main():
    app = QApplication(sys.argv)
    entropia_helper_app = EntropiaHelperApp()
    entropia_helper_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
