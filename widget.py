import sys
import ast
import mainWindow
import pandas as pd
import os
from parseMath import pyParseMath
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QComboBox, QFileDialog
from bson.objectid import ObjectId
from pymongo import MongoClient
from inputWin import InputWindow


class mainWin(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.parseMath = pyParseMath()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['math']
        self.y = False
        self.table_change = False
        self.name = ''
        self.table_data = []
        self.setupUi(self)
        self.tableWidget.setHorizontalHeaderLabels(['Key', 'Value', 'Type', 'Delete'])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellChanged.connect(self.change_content)
        self.name_comboBox.currentTextChanged.connect(self.click_combobox)
        self.delBtn.clicked.connect(self.delete_record)
        self.saveBtn.clicked.connect(self.save_record)
        self.searchVarBtn.clicked.connect(self.search_variables)
        self.calcBtn.clicked.connect(self.calc_formula)
        self.pathSearchDataSet.clicked.connect(self.searchPath)
        self.openDataSet.clicked.connect(self.openDataSetFromPath)
        self.input_window = None
        self.addBtn.clicked.connect(self.open_input_window)
        self.load_combobox()

    # Tab_1--------------------------------------------------------------------------------------------------------------
    def load_combobox(self):
        current_text = ''
        all_documents = self.collection.find()
        if self.name_comboBox != '':
            current_text = self.name_comboBox.currentText()

        items = [str(document['name']) for document in all_documents]

        self.name_comboBox.clear()
        self.name_comboBox.addItems(items)
        if current_text != '':
            self.name_comboBox.setCurrentText(current_text)

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
                self.type_value(value, rowPosition, key)

        self.add_button_table()
        self.add_button_delete()
        self.table_change = False
        self.saveBtn.setEnabled(False)
        self.name = self.name_comboBox.currentText()

    def type_value(self, value, rowPosition, key):
        if isinstance(value, ObjectId):
            cell_widget = QtWidgets.QTableWidgetItem(str(type(value)))
            self.tableWidget.setItem(rowPosition, 2, cell_widget)
            for column in range(3):
                item = self.tableWidget.item(rowPosition, column)
                if item is not None:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            self.add_combobox_table(rowPosition, value)
            if str(key) == 'name':
                self.tableWidget.item(rowPosition, 0).setFlags(
                    self.tableWidget.item(rowPosition, 0).flags() & ~QtCore.Qt.ItemIsEditable)

    def add_combobox_table(self, rowPosition, value):
        combo_box = QtWidgets.QComboBox()
        combo_box.addItem("<class 'int'>")
        combo_box.addItem("<class 'str'>")
        combo_box.addItem("<class 'list'>")
        combo_box.addItem("<class 'dict'>")
        if isinstance(value, int):
            combo_box.setCurrentIndex(0)
        elif isinstance(value, str):
            combo_box.setCurrentIndex(1)
        elif isinstance(value, list):
            combo_box.setCurrentIndex(2)
        elif isinstance(value, dict):
            combo_box.setCurrentIndex(3)
        self.tableWidget.setCellWidget(rowPosition, 2, combo_box)

    def add_button_table(self):
        table_button = QtWidgets.QPushButton()
        table_button.setText('Add row')
        table_button.clicked.connect(self.add_row)
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setCellWidget(rowPosition, 0, table_button)
        self.tableWidget.resizeColumnsToContents()

    def add_row(self):
        rowPosition = self.tableWidget.rowCount() - 1
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(""))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(""))
        self.add_combobox_table(rowPosition, '')
        self.add_button_delete()

    def add_button_delete(self):
        rowPosition = self.tableWidget.rowCount() - 1
        self.saveBtn.setEnabled(True)
        for i in range(rowPosition):
            if self.tableWidget.item(i, 0).text() != 'name' and self.tableWidget.item(i, 0).text() != '_id':
                pushButton = QtWidgets.QPushButton(f'del')
                pushButton.clicked.connect(lambda ch, j=i: self.del_btn_line(j))
                self.tableWidget.setCellWidget(i, 3, pushButton)

    def del_btn_line(self, i):
        self.tableWidget.removeRow(i)
        self.buffer_table()
        self.enter_from_buffer()

    def click_combobox(self):
        if self.table_change:
            reply = QMessageBox.question(self, 'Сохранение', 'Are you sure?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_record()
            self.enter_key_value(str(self.name_comboBox.currentText()))
        else:
            self.enter_key_value(str(self.name_comboBox.currentText()))

    def change_content(self):

        self.table_change = True
        self.saveBtn.setEnabled(True)

    def open_input_window(self):

        self.input_window = InputWindow()
        self.input_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.load_combobox()
        if self.input_window.exec_() == QtWidgets.QDialog.Accepted:
            self.load_combobox()

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
            self.name_comboBox.clear()
            self.load_combobox()

    def save_record(self):
        data = {}
        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).text()
            value = self.tableWidget.item(row, 1).text()
            value = self.check_value(value, row)
            data[key] = value
        try:
            self.collection.replace_one({"name": self.name}, data, upsert=True)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Такое name есть!")
            return

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        QtWidgets.QMessageBox.information(self, "Сохранение", "Данные успешно сохранены!")

        self.enter_key_value(str(self.name_comboBox.currentText()))
        self.load_combobox()

    def check_value(self, value, row):
        cell_widget = self.tableWidget.cellWidget(row, 2)
        if isinstance(cell_widget, QComboBox):
            value_type = cell_widget.currentText()
        else:
            value_type = self.tableWidget.item(row, 2).text()

        if value_type == "<class 'bson.objectid.ObjectId'>":
            try:
                value = ObjectId(value)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' должно быть <class "
                                                              f"'bson.objectid.ObjectId'>.")
                return
        elif value_type == "<class 'int'>":
            try:
                value = int(value)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' должно быть <class 'int'>.")
                return
        elif value_type == "<class 'str'>":
            try:
                value = str(value)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' должно быть <class'str'>.")
                return
        elif value_type == "<class 'list'>":
            try:
                if value != '':
                    value = eval(value)
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' "
                                                                  f"должно быть <class 'list'> и не пустым.")
                    return
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' должно быть <class 'list'>.")
                return
        elif value_type == "<class 'dict'>":
            try:
                value = ast.literal_eval(value)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Значение '{value}' должно быть <class 'dict'>.")
                return
        return value

    def buffer_table(self):
        self.table_data = []
        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).text()
            value = self.tableWidget.item(row, 1).text()
            value = self.check_value(value, row)
            self.table_data.append([key, value])

    def enter_from_buffer(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for row in self.table_data:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.type_value(row[1], rowPosition, row[0])
        self.add_button_table()
        self.add_button_delete()

    def search_variables(self):
        var_list = []
        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).text()
            value = self.tableWidget.item(row, 1).text()
            if key == 'formula':

                var_list = self.parseMath.search_variables(value)
                if var_list:
                    break

        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).text()
            if key == 'variables_list':
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var_list)))
                self.add_combobox_table(row, var_list)
                break

    def calc_formula(self):
        var_dict = None
        const_dict = None
        formula = None
        out = None
        for row in range(self.tableWidget.rowCount() - 1):
            key = self.tableWidget.item(row, 0).text()
            value = self.tableWidget.item(row, 1).text()
            if key == 'variables':
                var_dict = ast.literal_eval(value)
                print(var_dict)
            elif key == 'const':
                const_dict = ast.literal_eval(value)
                print(const_dict)
            elif key == 'formula':
                formula = value
                print(formula)

        if var_dict is not None and const_dict is not None and formula is not None:
            all_dict = {**var_dict, **const_dict}
            print(formula, all_dict)
            out = self.parseMath.parse_and_evaluate_linear_formula(formula, all_dict)

        if out is not None:
            for row in range(self.tableWidget.rowCount() - 1):
                key = self.tableWidget.item(row, 0).text()
                if key == 'out_value':
                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(out)))
                    self.add_combobox_table(row, out)

    # Tab_2-------------------------------------------------------------------------------------------------------------
    def searchPath(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Файлы Excel (*.xlsx);;Файлы CSV (*.csv)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                self.linePath.setText(file)

    def openDataSetFromPath(self):
        file_path = self.linePath.text()
        try:
            if file_path.endswith('.csv'):
                dataset = pd.read_csv(file_path)
                self.populate_table(dataset)
            elif file_path.endswith('.xlsx'):
                dataset = pd.read_excel(file_path)
            else:
                print("Неподдерживаемый формат файла.")
                return None

            # Дополнительные действия с открытым датасетом
            print(f"Датасет {file_path} успешно открыт.")
            return None
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return None
        except pd.errors.ParserError:
            print(f"Не удалось прочитать файл {file_path}. Проверьте формат данных.")
            return None

    def populate_table(self, data):
        self.tableDataSet.setRowCount(data.shape[0])
        self.tableDataSet.setColumnCount(data.shape[1])
        column_names = data.columns.tolist()
        self.tableDataSet.setColumnCount(len(column_names))
        self.tableDataSet.setHorizontalHeaderLabels(column_names)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                self.tableDataSet.setItem(row, col, QtWidgets.QTableWidgetItem(str(data.iloc[row, col])))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWin()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
