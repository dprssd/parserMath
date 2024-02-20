import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
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
        self.y = False
        self.setupUi(self)
        self.tableWidget.setHorizontalHeaderLabels(['Key', 'Value', 'Type'])
        self.tableWidget.resizeColumnsToContents()
        self.name_comboBox.currentTextChanged.connect(self.click_combobox)
        self.delBtn.clicked.connect(self.delete_record)
        # self.name_comboBox.currentIndexChanged.connect(self.load_combobox)
        self.input_window = None
        self.addBtn.clicked.connect(self.open_input_window)
        self.load_combobox()

    def load_combobox(self):
        self.name_comboBox.clear()
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
        self.input_window = InputWindow()

    def showDialog(self):
        self.y = False
        reply = QMessageBox.question(self, 'Message', 'Are you sure?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.y = True
        else:
            pass

    def delete_record(self):
        name_document = self.name_comboBox.currentText()
        self.showDialog()
        if self.y:
            self.collection.delete_one({"name": name_document})
            self.load_combobox()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWin()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
