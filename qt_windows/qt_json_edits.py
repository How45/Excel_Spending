from PyQt6.QtWidgets import (
    QFormLayout, QWidget, QPlainTextEdit, QPushButton, QLabel
)

from PyQt6.QtGui import QFontMetricsF
from PyQt6.QtCore import pyqtSignal

class QTJsonEdits(QWidget):
    finished = pyqtSignal()

    def __init__(self, file) -> None:
        super().__init__()
        self.file = file

        self.setWindowTitle('Add data to JSON files')
        self.resize(500, 500)

        layout = QFormLayout(self)
        self.setLayout(layout)

        self.title = QLabel('Bank JSON:')
        self.text_bank = QPlainTextEdit()
        self.text_bank.setTabStopDistance(QFontMetricsF(
            self.text_bank.font()).horizontalAdvance(' ') * 4)
        layout.addWidget(self.title)
        layout.addWidget(self.text_bank)

        self.title2 = QLabel('Memo JSON:')
        self.text_memo = QPlainTextEdit()
        self.text_memo.setTabStopDistance(QFontMetricsF(
            self.text_memo.font()).horizontalAdvance(' ') * 4)
        layout.addWidget(self.title2)
        layout.addWidget(self.text_memo)

        text_file_bank: str = open(file=f'spreadsheets\\{self.file}\\{self.file}_bank.json',
                               mode='r', encoding="utf-8").read()
        self.text_bank.setPlainText(text_file_bank)

        text_file_memo: str = open(file=f'spreadsheets\\{self.file}\\{self.file}_memo.json',
                              mode='r', encoding="utf-8").read()
        self.text_memo.setPlainText(text_file_memo)

        layout.setSpacing(5)

        exit_button = QPushButton('Create')
        layout.addWidget(exit_button)
        exit_button.clicked.connect(self._save_and_exit)

    def _save_and_exit(self) -> None:
        with open(file=f'spreadsheets\\{self.file}\\{self.file}_bank.json',
                mode="r+", encoding="utf-8") as f:
            f.write(self.text_bank.toPlainText())
            f.close()
        with open(file=f'spreadsheets\\{self.file}\\{self.file}_memo.json',
                mode="r+", encoding="utf-8") as f:
            f.write(self.text_memo.toPlainText())
            f.close()
        self.finished.emit()
        self.close()
