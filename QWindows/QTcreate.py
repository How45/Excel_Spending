from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLineEdit, QPushButton

class QTcreate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Spreadsheet")
        self.resize(500, 500)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Outer box (main)
        title_groupbox = QGroupBox('SpreadSheet')
        inner_layout = QVBoxLayout()
        title_groupbox.setLayout(inner_layout)

        # Text naming file feild
        name_file = QLineEdit()
        inner_layout.addWidget(name_file)
        layout.addWidget(title_groupbox)

        # Displays all files thats been added
        file_box = QGroupBox('Files:')
        list_files = QVBoxLayout()
        file_box.setLayout(list_files)

        # Visable outside the file box feild
        add_button = QPushButton('Add file', file_box)
        inner_layout.addWidget(add_button)

