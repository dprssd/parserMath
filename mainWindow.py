# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 433)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 791, 381))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.name_comboBox = QtWidgets.QComboBox(self.tab)
        self.name_comboBox.setGeometry(QtCore.QRect(10, 40, 261, 21))
        self.name_comboBox.setObjectName("name_comboBox")
        self.addBtn = QtWidgets.QPushButton(self.tab)
        self.addBtn.setGeometry(QtCore.QRect(600, 270, 75, 23))
        self.addBtn.setObjectName("addBtn")
        self.delBtn = QtWidgets.QPushButton(self.tab)
        self.delBtn.setGeometry(QtCore.QRect(600, 300, 75, 23))
        self.delBtn.setObjectName("delBtn")
        self.saveBtn = QtWidgets.QPushButton(self.tab)
        self.saveBtn.setGeometry(QtCore.QRect(600, 240, 75, 23))
        self.saveBtn.setObjectName("saveBtn")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 551, 251))
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addBtn.setText(_translate("MainWindow", "Добавить"))
        self.delBtn.setText(_translate("MainWindow", "Удалить"))
        self.saveBtn.setText(_translate("MainWindow", "Сохранить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "DataBase"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
