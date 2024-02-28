from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
import pandas as pd

def populate_table(table, data):
    table.setRowCount(data.shape[0])
    table.setColumnCount(data.shape[1])
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            item = QTableWidgetItem(str(data.iloc[row, col]))
            table.setItem(row, col, item)

# Создайте экземпляр QApplication
app = QApplication([])

# Создайте экземпляр QTableWidget
table_widget = QTableWidget()

# Загрузите данные из таблицы Excel или CSV с помощью библиотеки pandas
data = pd.read_csv(r'D:\Users\Aleksey\Desktop\work\PyProject\parserMath\SunTable.csv')

# Заполните таблицу данными
populate_table(table_widget, data)

# Покажите таблицу
table_widget.show()

# Запустите главный цикл приложения
app.exec_()