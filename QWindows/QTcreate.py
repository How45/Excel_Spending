from PyQt6.QtWidgets import (
    QFormLayout, QVBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QWidget, QFileDialog, QLabel
)

import os

class QTcreate(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Create New Spreadsheet")
        self.resize(500, 500)

        layout = QFormLayout(self)
        self.setLayout(layout)

        # Outer box (main)
        title_groupbox = QGroupBox('SpreadSheet')
        inner_layout = QVBoxLayout()
        title_groupbox.setLayout(inner_layout)
        layout.addWidget(title_groupbox)

        inner_layout.setContentsMargins(10, 10, 10, 10)
        inner_layout.setSpacing(5)

        # Text naming file feild
        name_folder = QLineEdit('Folder Name')
        inner_layout.addWidget(name_folder)


# / ----------------------------------------- /
        # Displays all files thats been added
        self.statement_files = []

        self.file_box = QGroupBox('Files:')
        self.list_files = QFormLayout()
        self.file_box.setLayout(self.list_files)
        inner_layout.addWidget(self.file_box)

        # Visable outside the file box feild
        add_button = QPushButton('Add file')
        inner_layout.addWidget(add_button)

        inner_layout.addSpacing(20)

        # Displays all files thats been added
        self.json_files = []

        self.json_file_box = QGroupBox('JSON Files:')
        self.json_list_files = QFormLayout()
        self.json_file_box.setLayout(self.json_list_files)
        inner_layout.addWidget(self.json_file_box)

        # Visable outside the file box feild
        add_json_button = QPushButton('Add JSON')
        inner_layout.addWidget(add_json_button)
        create_json_button = QPushButton('Create JSON')
        inner_layout.addWidget(create_json_button)

        inner_layout.addSpacing(20)

        name_file = QLineEdit('Excelsheet Name')
        inner_layout.addWidget(name_file)

        create_sheet = QPushButton('Create')
        inner_layout.addWidget(create_sheet)

        add_button.clicked.connect(self.adding_files)
        add_json_button.clicked.connect(self.adding_json)
        create_json_button.clicked.connect(self.creating_json)


    def adding_files(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path and file_path not in self.statement_files:
            self.statement_files.append(file_path)

            file_name = os.path.basename(file_path)

            file_label = QLabel(file_name)
            self.list_files.addRow(file_label)

        else:
            print('❗️ Either file doesnt exists or its the same one')

    def adding_json(self) -> None:

        if len(self.json_list_files) == 1:
            print('❗️ Cant have more then one file')

        file_path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
        if file_path:
            self.json_files.append(file_path)

            file_name = os.path.basename(file_path)

            file_label = QLabel(file_name)
            self.json_list_files.addRow(file_label)

        else:
            print('❗️ Either file doesnt exists or its the same one')

    def creating_json(self) -> None:
        pass
