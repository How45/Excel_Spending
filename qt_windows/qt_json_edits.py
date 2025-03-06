from PyQt6.QtWidgets import (
    QFormLayout, QWidget, QPlainTextEdit
)

class QTJsonEdits(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Add data to JSON files")
        self.resize(500, 500)

        layout = QFormLayout(self)
        self.setLayout(layout)

        text_edit = QPlainTextEdit()
        layout.addWidget(text_edit)

        text = open('spreadsheets\\test1\\test1_bank.json').read()
        text_edit.setPlainText(text)



    def display_file(self) -> None:
        pass
