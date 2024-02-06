import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from bson.objectid import ObjectId
from pymongo import MongoClient
import mainWindow


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
        self.load_combobox()

    def load_combobox(self):
        all_documents = self.collection.find()
        for document in all_documents:
            self.name_comboBox.addItem(str(document['_id']))

    def enter_key_value(self, id_document):

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        record = self.collection.find_one({"_id": id_document})

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
        self.enter_key_value(ObjectId(self.name_comboBox.currentText()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWin()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
