import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from bson.objectid import ObjectId
from pymongo import MongoClient
import mainWindow
from inputWin import InputWindow


class mainWin(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['math']
        self.setupUi(self)
        self.tableWidget.setHorizontalHeaderLabels(['Key', 'Value', 'Type'])
        self.tableWidget.resizeColumnsToContents()
        self.name_comboBox.currentTextChanged.connect(self.click_combobox)
        self.input_window = None
        self.addBtn.clicked.connect(self.open_input_window)
        self.load_combobox()

    def load_combobox(self):
        all_documents = self.collection.find()
        for document in all_documents:
            self.name_comboBox.addItem(str(document['name']))

    def enter_key_value(self, name_document):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        record = self.collection.find_one({"name": name_document})

        if record:
            for key, value in record.items():
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(key)))
                self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(value)))
                self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(type(value))))
        self.tableWidget.resizeColumnsToContents()

    def click_combobox(self):
        print(self.name_comboBox.currentText())
        self.enter_key_value(str(self.name_comboBox.currentText()))

    def open_input_window(self):

        if self.input_window is None:
            self.input_window = InputWindow()
        self.input_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWin()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
