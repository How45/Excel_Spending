import os
import shutil

from PyQt6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QWidget

import script as run
from qt_windows.qt_create import QTcreate
from qt_windows.qt_json_edits import QTJsonEdits
from qt_windows.qt_load import QTload
from qt_windows.qt_update import QTupdate


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spreadsheet App")
        self.resize(250,200)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        title_groupbox = QGroupBox('SpreadSheet')
        inner_layout = QVBoxLayout()
        title_groupbox.setLayout(inner_layout)

        title_button = ['Create a new', 'Load', 'Update']
        buttons = [QPushButton(t, title_groupbox) for t in title_button]

        inner_layout.addStretch()
        for b in buttons:
            inner_layout.addWidget(b)

        inner_layout.addStretch()
        layout.addWidget(title_groupbox)

        buttons[0].clicked.connect(self.open_create)
        buttons[1].clicked.connect(self.open_load)
        buttons[2].clicked.connect(self.open_update)

    def open_create(self) -> None:
        self.create_window = QTcreate()
        self.create_window.data_sent.connect(self.receive_data)
        self.create_window.show()

    def receive_data(self, statement_files: list[str], file_name: str, start_amount: int) -> None:
        current_path: str = os.getcwd()
        try:
            print(not os.path.isdir(f"{current_path}\\spreadsheets"))
            if not os.path.isdir(f"{current_path}\\spreadsheets"):
                raise FileNotFoundError
        except FileNotFoundError:
            os.mkdir(f"{current_path}\\spreadsheets")

        new_directory: str = f"{current_path}\\spreadsheets\\{file_name}"
        statement_directory: str = f"{new_directory}\\statements"

        os.mkdir(new_directory)
        # os.rename(json_files, f"{new_directory}\\{json_files}")
        shutil.copy2("template_memo.json",f"{new_directory}\\{file_name}_memo.json")
        shutil.copy2("template_bank.json",f"{new_directory}\\{file_name}_bank.json")

        os.mkdir(statement_directory)
        for statement in statement_files:
            split_name = statement.split('statements')[-1]
            shutil.copy2(statement,f"{statement_directory}{split_name}")

        # self.edit_json = QTJsonEdits()
        # self.edit_json.show()

        run.create(new_directory, start_amount)

    def open_load(self):
        self.load_window = QTload()
        self.load_window.show()

    def open_update(self):
        self.update_window = QTupdate()
        self.update_window.show()
