import design
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import calendarFormConnector
from datetime import datetime as dt
from DataReader import *
import threading
import ClusterView
import TimeSeries
import Compression as comp
import TimeSeriesParametersDesignConnector


def threads(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()

    return wrapper


class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    #TIME SERIES PARAMS
    absEnergy = 0
    absMax = 0
    autocorrelation = 0
    complexity = 0
    countAbove = 0
    #LoadButtonSomeInfo
    signal_progress_bar = QtCore.pyqtSignal(int, name='signal_progress_bar')
    signal_text = QtCore.pyqtSignal(str, name='signal_text')
    params_combobox = QtCore.pyqtSignal(name='params_combobox')
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.defects = []
        self.id_defects = {}
        self.params = []
        self.delay = {}
        self.allValuesList = []
        self.defectValuesList = {}
        self.adaboost = 0
        self.limits = {}
        self.nameUnit = {}
        # Default parameters
        self.progressBar.setValue(0)
        self.tab_2.setDisabled(True)
        self.openCalenderFrom.setDisabled(True)
        self.openCalenderTo.setDisabled(True)
        self.StartProccessButton.setDisabled(True)
        # Load db info
        self.dbPath = None
        self.selectDbFile.clicked.connect(self.getDbPath)
        self.loadDataButton.setDisabled(True)
        # Calender on LoadData tab
        self.openCalenderFrom.clicked.connect(self.makeDateFrom)
        self.openCalenderTo.clicked.connect(self.makeDateTo)
        self.dateEditTo.dateTimeChanged.connect(self.checkDateTimeToLoadModule)
        self.dateEditFrom.dateTimeChanged.connect(self.checkDateTimeToLoadModule)
        # Load db
        self.signal_progress_bar.connect(self.sh_update_prog_bar)
        self.signal_text.connect(self.sh_text_browser_update)
        self.params_combobox.connect(self.sh_select_params)
        self.loadDataButton.clicked.connect(
            lambda: self.load_data(self.signal_progress_bar, self.signal_text, self.params_combobox))
        # TimeSeries
        self.openCalenderFromTimeSeries.clicked.connect(self.makeDateFromTimeSeries)
        self.openCalenderToTimeSeries.clicked.connect(self.makeDateToTimeSeries)
        self.timeSeriesDateFrom.dateTimeChanged.connect(self.checkDateTimeFromLoadModuleTimeSeries)
        self.timeSeriesDateTo.dateTimeChanged.connect(self.checkDateTimeToLoadModuleTimeSeries)
        self.StartProccessButton.clicked.connect(self.startTimeSeriesCalculations)
        self.parametersComboBox.currentIndexChanged.connect(self.enableTSButton)
        self.TimeSeriesParametersButton.clicked.connect(self.openParametersForm)
        # Cluster module
        self.StartProccessButton_2.clicked.connect(self.getCluster)
        # self.doubleSpinBox.setMinimum(0)
        # self.doubleSpinBox.setMaximum(1)
        # self.doubleSpinBox.setSingleStep(0.01)

    # Calender form on LoadData
    def makeDateFrom(self, event):
        self.win_calendar_from = calendarFormConnector.Ui_TimeManagerController(self, self.dateEditFrom, 'min')
        self.win_calendar_from.show()

    def makeDateTo(self):
         self.win_calendar_to = calendarFormConnector.Ui_TimeManagerController(self, self.dateEditTo, 'max')
         self.win_calendar_to.show()

    # Limit calender on LoadData
    def limit_calendar(self):
        self.maxTime, self.minTime = findTimeRange(self.dbPath[0])
        self.dateEditFrom.setMinimumDate(dt.strptime(self.minTime, '%Y-%m-%d %H:%M:%S'))
        self.dateEditFrom.setMaximumDate(dt.strptime(self.maxTime, '%Y-%m-%d %H:%M:%S'))
        self.dateEditTo.setMinimumDate(dt.strptime(self.minTime, '%Y-%m-%d %H:%M:%S'))
        self.dateEditTo.setMaximumDate(dt.strptime(self.maxTime, '%Y-%m-%d %H:%M:%S'))

        self.dateEditFrom.setDateTime(dt.strptime(self.minTime, '%Y-%m-%d %H:%M:%S'))
        self.dateEditTo.setDateTime(dt.strptime(self.maxTime, '%Y-%m-%d %H:%M:%S'))

    def checkDateTimeToLoadModule(self):
        if self.dateEditTo.dateTime() < self.dateEditFrom.dateTime():
            self.dateEditTo.setDateTime(self.dateEditFrom.dateTime())

    def checkDateTimeFromLoadModule(self):
        if self.dateEditFrom.dateTime() > self.dateEditTo.dateTime():
            self.dateEditFrom.setDateTime(self.dateEditTo.dateTime())
    #db path
    def getDbPath(self):
        self.infoLog.append("Uploading DB path...\n")
        self.dbPath = QFileDialog.getOpenFileName(self, "Open Dialog", "", "*.db")
        if self.dbPath[0].__contains__("PolymericFilmsDb.db"):
            self.loadDataButton.setDisabled(False)
            self.limit_calendar()
            self.infoLog.append("Successfully uploaded. Now select the data loading range from the database and press 'Load Data'")
            self.openCalenderFrom.setDisabled(False)
            self.openCalenderTo.setDisabled(False)
        else:
            self.infoLog.append("Error. Filename must be 'PolymericFilmsDb.db'")

    #Cluster
    def getCluster(self):
        ClusterView.Start(comp.CompressingData(self.allValuesList), eps=self.doubleSpinBox.value(), min_samples=int(self.doubleSpinBox_2.value()))

    #Progress bar durning loading data
    def sh_update_prog_bar(self, data):
        self.progressBar.setValue(int(data))
        #self.progressBarModel.setValue(int(data))

    def sh_text_browser_update(self, data):
        if len(data) > 0:
            self.infoLog.append(data)

    def sh_select_params(self):
        if len(self.defects) != 0:
            self.parametersComboBox.setCurrentText(self.nameUnit[self.defects[0]][1])

    #LOAD DATA FROM DB
    def disabled(self, mod):
        self.centralwidget.setDisabled(mod)

    def delete_const(self):
        defect = self.defects
        i = 0
        while i < len(self.defects):
            maxd = max(self.defectValuesList[self.defects[i]])
            mind = min(self.defectValuesList[self.defects[i]])
            if maxd == mind:
                defect.remove(self.defects[i])
            else:
                i += 1
        self.defects = defect

    @threads
    def load_data(self, signal_pb, signal_text, signal_params_combobox):
        self.disabled(True)
        self.nameUnit = read_names(self.dbPath[0])
        self.limits = db_limits(self.dbPath[0])
        timeFrom = self.dateEditFrom.dateTime().toPyDateTime()
        timeTo = self.dateEditTo.dateTime().toPyDateTime()
        if timeTo < timeFrom:
            signal_text.emit('Wrong time interval.')
            self.disabled(False)
            return
        signal_text.emit("The process of loading production data has begun")
        self.allValuesList, self.defectValuesList, self.id_params, self.time_list = db_reader_from_to(str(timeFrom), str(timeTo), signal_pb, self.dbPath[0])
        try:
            self.parametersComboBox.clear()
            self.parameter = list(self.id_params.keys())
            self.defects = list(self.defectValuesList.keys())
            for i in range(len(self.parameter)):
                if not self.parameter[i] in self.defects:
                    self.params.append((self.parameter[i], i))
            self.delete_const()
            signal_params_combobox.emit()

            #Params time series
            for param in self.params:
                if self.nameUnit[param[0]][1] != 'nan':
                    self.parametersComboBox.addItem(
                        self.nameUnit[param[0]][1]
                    )
                    #Second param here is language

            signal_text.emit('Data download is complete.')
            self.tab_2.setDisabled(False)
            self.timeSeriesLimits()
        except:
            signal_text.emit("Invalid data content")
            self.tab_2.setDisabled(True)

        signal_pb.emit(100)
        signal_params_combobox.emit()
        self.disabled(False)

    # TimeSeries
    def enableTSButton(self):
        self.StartProccessButton.setDisabled(False)

    def timeSeriesLimits(self):
        self.minimumdatetimeseries = self.dateEditFrom.dateTime().toPyDateTime()
        self.maximumdatetimeseries = self.dateEditTo.dateTime().toPyDateTime()
        self.minimumtimetimeseries = self.dateEditFrom.dateTime().time().toPyTime()
        self.maximumtimetimeseries = self.dateEditTo.dateTime().time().toPyTime()
        self.timeSeriesDateFrom.setMinimumDateTime(self.minimumdatetimeseries)
        self.timeSeriesDateFrom.setMaximumDateTime(self.maximumdatetimeseries)
        self.timeSeriesDateTo.setMinimumDateTime(self.minimumdatetimeseries)
        self.timeSeriesDateTo.setMaximumDateTime(self.maximumdatetimeseries)

        self.timeSeriesDateTo.setDateTime(self.dateEditTo.dateTime())
        self.timeSeriesDateFrom.setDateTime(self.dateEditFrom.dateTime())

    def makeDateFromTimeSeries(self):
        self.win_calendar_from_ts = calendarFormConnector.Ui_TimeManagerController(self, self.timeSeriesDateFrom, 'min', True)
        self.win_calendar_from_ts.show()

    def makeDateToTimeSeries(self):
        self.win_calendar_to_ts = calendarFormConnector.Ui_TimeManagerController(self, self.timeSeriesDateTo,'max', True)
        self.win_calendar_to_ts.show()

    def checkDateTimeToLoadModuleTimeSeries(self):
        if self.timeSeriesDateTo.dateTime() < self.timeSeriesDateFrom.dateTime():
            self.timeSeriesDateTo.setDateTime(self.timeSeriesDateFrom.dateTime())

    def checkDateTimeFromLoadModuleTimeSeries(self):
        if self.timeSeriesDateFrom.dateTime() > self.timeSeriesDateTo.dateTime():
            self.timeSeriesDateFrom.setDateTime(self.timeSeriesDateTo.dateTime())

    def startTimeSeriesCalculations(self):
        #TimeSeriesArgs
        # self.i = 0
        self.indexOfChoosenParam = get_parameter_id_ts(self.dbPath[0], self.parametersComboBox.currentText())
        self.choosenParamTSList = get_parameter_values(self.dbPath[0], self.indexOfChoosenParam, self.timeSeriesDateFrom.dateTime().toPyDateTime(), self.timeSeriesDateTo.dateTime().toPyDateTime())
        # for i in range(len(self.allValuesList)):
        #     self.choosenParamTSList.append((self.allValuesList[i][self.indexOfChoosenParam]-1))
        if self.absEnergyCheck.isChecked():
            TimeSeries.absEnergyCalc(self.choosenParamTSList, self)
        if self.absMaxChange.isChecked():
            TimeSeries.absMax(self.choosenParamTSList, self)
        if self.autocorrelationCheck.isChecked():
            TimeSeries.autocorrelation(self.choosenParamTSList, 12, self)
        if self.complexityCheck.isChecked():
            TimeSeries.complexity(self.choosenParamTSList, 12, self)
        if self.countAboveCheck.isChecked():
            TimeSeries.countAbove(self.choosenParamTSList, 15, self)

    def openParametersForm(self):
        s = TimeSeriesParametersDesignConnector.Ui_TimeManagerController(self)




