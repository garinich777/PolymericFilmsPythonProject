from datetime import datetime
from PyQt5 import QtCore, QtWidgets
import TimeSeriesParametersDesign


def __init__form(self, form, parent=None):
    self.form = form


TimeSeriesParametersDesign.Ui_MainWindowTS.__init__ = __init__form

class Ui_TimeManagerController(QtWidgets.QWidget):

    def closeEvent(self, event):
        self.dateEdit.setDateTime(datetime.strptime(f"{str(self.ui.calendarWidget.selectedDate().toPyDate()).split(' ')[0]} {str(self.ui.timeEdit.time().toPyTime())}", '%Y-%m-%d %H:%M:%S'))

    def __init__(self, form, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.ui = TimeSeriesParametersDesign.Ui_MainWindowTS(form)
        self.ui.setupUi(self)
        # self.ui.set_limit_calendar(mod, istimeseries)
