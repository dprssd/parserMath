from pymongo import MongoClient
from PyQt5 import QtWidgets, QtCore


class InputWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['math']
        self.setWindowTitle("Добавить name")

        self.name_label = QtWidgets.QLabel("Имя:")
        self.name_input = QtWidgets.QLineEdit()
        self.addButton = QtWidgets.QPushButton("Добавить")
        self.cancelButton = QtWidgets.QPushButton("Отмена")

        self.addButton.clicked.connect(self.addRecord)
        self.cancelButton.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.addButton)
        layout.addWidget(self.cancelButton)

        self.setLayout(layout)

    def addRecord(self):

        input_text = self.name_input.text()
        try:
            self.collection.insert_one({'name': input_text, 'formula': '', 'variables_list': '', 'const': '',
                                        f'variables': '', 'out_value': ''})
        except Exception as ex:
            print("[create_record] Some problem...")
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Такое name есть!")
            print(ex)
        self.accept()
