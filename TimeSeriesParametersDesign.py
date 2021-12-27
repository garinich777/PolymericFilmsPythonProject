# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowTS(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(387, 484)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 0, 371, 421))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.AutocorrelationLagSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.AutocorrelationLagSpinbox.setGeometry(QtCore.QRect(220, 30, 141, 21))
        self.AutocorrelationLagSpinbox.setObjectName("AutocorrelationLagSpinbox")
        self.complexityLagSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.complexityLagSpinbox.setGeometry(QtCore.QRect(220, 60, 141, 21))
        self.complexityLagSpinbox.setObjectName("complexityLagSpinbox")
        self.countAboveTrSpinbox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.countAboveTrSpinbox.setGeometry(QtCore.QRect(220, 90, 141, 21))
        self.countAboveTrSpinbox.setObjectName("countAboveTrSpinbox")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(20, 30, 161, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 161, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 161, 21))
        self.label_3.setObjectName("label_3")
        self.confirmTSParamsButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmTSParamsButton.setGeometry(QtCore.QRect(10, 430, 361, 51))
        self.confirmTSParamsButton.setObjectName("confirmTSParamsButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Time series parameters"))
        self.label.setText(_translate("MainWindow", "Autocorrelation lag"))
        self.label_2.setText(_translate("MainWindow", "Complexity lag"))
        self.label_3.setText(_translate("MainWindow", "Count above treshold"))
        self.confirmTSParamsButton.setText(_translate("MainWindow", "PushButton"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindowTS = QtWidgets.QWidget()
    ui = Ui_MainWindowTS
    ui.setupUi(MainWindowTS)
    MainWindowTS.show()
    sys.exit(app.exec_())