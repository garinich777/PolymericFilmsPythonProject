from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeManager(object):

    def setupUi(self, TimeManager):
        TimeManager.setObjectName('TimeManager')
        TimeManager.resize(470, 371)
        self.calendarWidget = QtWidgets.QCalendarWidget(TimeManager)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 471, 371))
        self.calendarWidget.setObjectName('calendarWidget')
        self.timeEdit = QtWidgets.QTimeEdit(TimeManager)
        self.timeEdit.setGeometry(QtCore.QRect(0, 40, 61, 22))
        self.timeEdit.setObjectName('timeEdit')
        self.retranslateUi(TimeManager)
        QtCore.QMetaObject.connectSlotsByName(TimeManager)

    def retranslateUi(self, TimeManager):
        _translate = QtCore.QCoreApplication.translate
        TimeManager.setWindowTitle(_translate('Time Manager', 'Time Manager'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TimeManager = QtWidgets.QWidget()
    ui = Ui_TimeManager()
    ui.setupUi(TimeManager)
    TimeManager.show()
    sys.exit(app.exec_())