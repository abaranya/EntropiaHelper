import yaml, os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import Qt

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(__file__)
        self.config_path = os.path.join(script_dir, '..', 'config.yaml')

        self.setWindowTitle("Configuration")
        self.setStyleSheet("background-color: #202020; color: white;")
        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        config_data = self.load_config()

        file_path_layout = QHBoxLayout()
        layout.addLayout(file_path_layout)
        file_path_label = QLabel("File Path:")
        file_path_layout.addWidget(file_path_label)
        self.file_path_entry = QLineEdit()
        self.file_path_entry.setText(config_data.get('file_path', ''))
        layout.addWidget(self.file_path_entry)

        self.start_from_end_checkbox = QCheckBox("Start from End")
        self.start_from_end_checkbox.setChecked(config_data.get('start_from_end', True))
        file_path_layout.addWidget(self.start_from_end_checkbox)

        start_time_layout = QHBoxLayout()
        layout.addLayout(start_time_layout)
        start_date_label = QLabel("Start Date:")
        start_time_layout.addWidget(start_date_label)
        self.start_date_entry = QLineEdit()
        self.start_date_entry.setText(config_data.get('start_date', ''))
        start_time_layout.addWidget(self.start_date_entry)

        start_time_label = QLabel("Start Time:")
        start_time_layout.addWidget(start_time_label)
        self.start_time_entry = QLineEdit()
        self.start_time_entry.setText(config_data.get('start_time', ''))
        start_time_layout.addWidget(self.start_time_entry)

        transparency_layout = QHBoxLayout()
        layout.addLayout(transparency_layout)
        transparency_label = QLabel("Transparency:")
        transparency_layout.addWidget(transparency_label)
        self.transparency_entry = QLineEdit()
        self.transparency_entry.setText(str(config_data.get('transparency', 0.6)))
        transparency_layout.addWidget(self.transparency_entry)

        save_layout = QHBoxLayout()
        layout.addLayout(save_layout)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        save_layout.addWidget(save_button)

    def load_config(self):
        try:
            with open(self.config_path, "r") as file:
                config = yaml.safe_load(file)
                if config is None:
                    config = {}
                config.setdefault('transparency', 0.6)
                config.setdefault('file_path', '')
                config.setdefault('start_from_end', True)
                config.setdefault('start_date', '')
                config.setdefault('start_time', '')
                return config
        except FileNotFoundError:
            config = {
                'transparency': 0.6,
                'file_path': '',
                'start_from_end': True,
                'start_date': '',
                'start_time': ''
            }
            return config

    def save_config(self):
        config = {
            'file_path': self.file_path_entry.text(),
            'start_from_end': self.start_from_end_checkbox.isChecked(),
            'start_date': self.start_date_entry.text(),
            'start_time': self.start_time_entry.text(),
            'transparency': float(self.transparency_entry.text())
        }
        with open(self.config_path, "w") as file:
            yaml.dump(config, file)
