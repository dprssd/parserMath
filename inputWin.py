import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from pymongo import MongoClient


class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.input_label = None
        self.input_field = None
        self.ok_button = None
        self.initUI()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['math']

    def initUI(self):
        layout = QVBoxLayout()

        self.input_label = QLabel('Введите текст:')
        layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.on_ok_button_click)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        self.setWindowTitle('Добавить новую запись')
        self.show()

    def on_ok_button_click(self):
        print('clicked')
        input_text = self.input_field.text()
        try:
            # self.collection.create_index(["name"], unique=True)
            self.collection.insert_one({'name': input_text, 'formula': '', 'variables': '', 'out_value': ''})
            self.close()
        except Exception as ex:
            print("[create_record] Some problem...")
            print(ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputWindow()
    sys.exit(app.exec_())