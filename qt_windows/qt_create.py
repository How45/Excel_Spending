import os
import shutil

from PyQt6.QtWidgets import (
    QFormLayout, QVBoxLayout,
    QGroupBox, QLineEdit, QPushButton, QWidget, QFileDialog, QLabel, QDialog
)
from PyQt6.QtCore import pyqtSignal

class NewMemo(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("New Memo Name")
        self.setGeometry(300, 300, 300, 100)

        layout = QFormLayout(self)
        self.setLayout(layout)

        self.name_memo = QLineEdit()
        layout.addWidget(self.name_memo)

        self.create_memo = QPushButton('Create')
        layout.addWidget(self.create_memo)

        self.create_memo.clicked.connect(self.accept)

    def get_memo_name(self) -> str:
        return self.name_memo.text()

class QTcreate(QWidget):
    data_sent = pyqtSignal(list, str)

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

        # Text naming file field
        self.name_folder = QLineEdit('Folder Name')
        inner_layout.addWidget(self.name_folder)


# / ----------------------------------------- /
        # Displays all files that's been added
        self.statement_files = []

        self.file_box = QGroupBox('Files:')
        self.list_files = QFormLayout()
        self.file_box.setLayout(self.list_files)
        inner_layout.addWidget(self.file_box)

        # Visible outside the file box field
        add_button = QPushButton('Add file')
        inner_layout.addWidget(add_button)

        inner_layout.addSpacing(20)

        # Displays all files that's been added
        self.json_files = []

        self.json_file_box = QGroupBox('JSON Files:')
        self.json_list_files = QFormLayout()
        self.json_file_box.setLayout(self.json_list_files)
        inner_layout.addWidget(self.json_file_box)

        # Visible outside the file box field
        # add_json_button = QPushButton('Add JSON')
        # inner_layout.addWidget(add_json_button)
        # create_json_button = QPushButton('Create JSON')
        # inner_layout.addWidget(create_json_button)

        inner_layout.addSpacing(20)

        self.name_file = QLineEdit('Excelsheet Name')
        inner_layout.addWidget(self.name_file)

        create_sheet = QPushButton('Create')
        inner_layout.addWidget(create_sheet)

        add_button.clicked.connect(self.adding_files)
        # add_json_button.clicked.connect(self.adding_json)
        # create_json_button.clicked.connect(self.creating_json)
        create_sheet.clicked.connect(self.send_data)


    def adding_files(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path and file_path not in self.statement_files:
            self.statement_files.append(file_path)

            file_name = os.path.basename(file_path)

            file_label = QLabel(file_name)
            self.list_files.addRow(file_label)

        elif file_path in self.statement_files:
            print("❗️ Already added")

    def adding_json(self) -> None:
        if len(self.json_list_files) < 1:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
            if file_path:
                self.json_files.append(file_path)

                file_name = os.path.basename(file_path)

                file_label = QLabel(file_name)
                self.json_list_files.addRow(file_label)
        else:
            print("❗️Can't have more then one file")

    def creating_json(self) -> None:
        # Get a copy of a template called template_memo. Then ask them for name of memo
        if len(self.json_list_files) < 1:
            memo_name = ''
            while not memo_name:
                get_name = NewMemo()

                if get_name.exec():
                    memo_name = get_name.get_memo_name()

            shutil.copy2("template_memo.json",memo_name+".json")

            self.json_files.append(memo_name+".json")
            file_name = os.path.basename(memo_name+".json")

            file_label = QLabel(file_name)
            self.json_list_files.addRow(file_label)
        else:
            print("❗️Can't have more then one file")

    def send_data(self) -> tuple[list[str],str]:
        self.data_sent.emit(self.statement_files, self.name_file.text())
        self.close()
