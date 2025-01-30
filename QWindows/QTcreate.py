from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLineEdit, QPushButton, QFormLayout, QTextEdit

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

        # Text naming file feild
        name_folder = QLineEdit('Folder Name')
        inner_layout.addWidget(name_folder)


# / ----------------------------------------- /
        # Displays all files thats been added
        file_box = QGroupBox('Files:')
        list_files = QFormLayout()
        file_box.setLayout(list_files)
        inner_layout.addWidget(file_box)


        # Visable outside the file box feild#e')
        add_button = QPushButton('Add file')
        inner_layout.addWidget(add_button)

        name_file = QLineEdit('excelsheet name')
        inner_layout.addWidget(name_file)

        json_create = 

        create_sheet = QPushButton('Create')
        inner_layout.addWidget(create_sheet)

        add_button.clicked.connect(self.adding_files)


    def adding_files(self) -> None:
        pass
