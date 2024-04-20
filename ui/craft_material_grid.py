from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QGroupBox, QPushButton, \
    QMessageBox, QSizePolicy, QStyle, QDoubleSpinBox

from manager.material_manager import MaterialManager
from ui.material_selection_dialog import MaterialSelectionDialog


class CraftMaterialGrid(QGroupBox):
    def __init__(self):
        super().__init__("Crafing Materials")

        self.material_manager = MaterialManager()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add header row
        header_layout = QHBoxLayout()
        headers = [("Qty", 1), ("Material", 260), ("Find", 1), ("TT Value", 10), ("Markup", 80), ("Total Cost", 80),
                   ("add qty", 10), ("add value", 10), ("result qty", 10),("result value", 10)]
        for (header_text, header_size) in headers:
            header_label = QLabel(header_text)
            header_label.setMinimumWidth(header_size)
            header_layout.addWidget(header_label)
        self.layout.addLayout(header_layout)

        # Add initial row
        # self.add_row()

        # Add a layout for the add row button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Add stretch to push button to the right
        self.add_row_button = QPushButton("+")
        self.add_row_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Set fixed size policy
        self.add_row_button.setFixedSize(30, 30)  # Set fixed size for the button
        self.add_row_button.clicked.connect(self.add_row)
        button_layout.addWidget(self.add_row_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

    def get_data(self):
        data = []
        for row_index in range(1, self.layout.count() - 1):  # Skip header row and button row
            row_layout = self.layout.itemAt(row_index).layout()
            row_data = {
                "qty": row_layout.itemAt(0).widget().text(),
                "material": row_layout.itemAt(1).widget().currentText(),
                "tt_value": row_layout.itemAt(2).widget().text(),
                "markup": row_layout.itemAt(3).widget().text(),
                "total_cost": row_layout.itemAt(4).widget().text()
            }
            data.append(row_data)
        return data

    def add_row(self):
        row_layout = QHBoxLayout()
        qty_edit = QDoubleSpinBox()
        qty_edit.setDecimals(0)
        material_edit = QLineEdit()
        material_edit.setMinimumWidth(280)
        search_button = QPushButton("")
        search_button.clicked.connect(
            lambda checked, material_name=material_edit.text: self.search_material(material_edit))
        search_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        tt_value_edit = QDoubleSpinBox()
        tt_value_edit.setDecimals(2)
        tt_value_edit.setSuffix(" PED")
        tt_value_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        markup_edit = QDoubleSpinBox()
        markup_edit.setDecimals(2)
        markup_edit.setSuffix(" %")
        markup_edit.setMaximum(9999999.99)
        markup_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_cost_edit = QDoubleSpinBox()
        total_cost_edit.setDecimals(2)
        total_cost_edit.setSuffix(" PED")
        total_cost_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        add_qty_edit = QDoubleSpinBox()
        add_qty_edit.setDecimals(0)
        add_value_edit = QDoubleSpinBox()
        add_value_edit.setDecimals(2)
        add_value_edit.setSuffix(" PED")
        add_value_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        result_qty_edit = QDoubleSpinBox()
        result_qty_edit.setDecimals(0)
        result_value_edit = QDoubleSpinBox()
        result_value_edit.setDecimals(2)
        result_value_edit.setSuffix("PED")
        result_value_edit.setAlignment(Qt.AlignmentFlag.AlignRight)

        row_layout.addWidget(qty_edit)
        row_layout.addWidget(material_edit)
        row_layout.addWidget(search_button)
        row_layout.addWidget(tt_value_edit)
        row_layout.addWidget(markup_edit)
        row_layout.addWidget(total_cost_edit)
        row_layout.addWidget(add_qty_edit)
        row_layout.addWidget(add_value_edit)
        row_layout.addWidget(result_qty_edit)
        row_layout.addWidget(result_value_edit)

        # self.layout.addLayout(row_layout)
        self.layout.insertLayout(self.layout.count() - 1, row_layout)  # Insert before the button row

    def remove_row(self):
        if self.layout.count() > 1:  # Ensure there is at least one row
            item = self.layout.itemAt(self.layout.count() - 1)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()  # Delete the widget
                else:
                    layout = item.layout()
                    if layout is not None:
                        for i in reversed(range(layout.count())):
                            layout.itemAt(i).widget().deleteLater()  # Delete widgets in the layout
                    layout.deleteLater()  # Delete the layout

    def search_material(self, material_edit):
        material_name = material_edit.text().strip()
        if material_name:
            # Call the material manager to search for the material
            materials = self.material_manager.search_materials(material_name)
            if materials:
                dialog = MaterialSelectionDialog(materials)
                material = dialog.selected_material()
                material_edit.setText(material)
            else:
                QMessageBox.warning(self, "No Matches", "No matching materials found.")
        else:
            # Show a message if the material name is empty
            print("Please enter a material name to search.")
