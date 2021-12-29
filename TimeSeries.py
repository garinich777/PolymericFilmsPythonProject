import numpy as np
import tsfresh.feature_extraction.feature_calculators
import threading
import MainApp
from PyQt5 import QtCore, QtWidgets

import design


def threads(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()
    return wrapper


@threads
def absEnergyCalc(param, main):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.abs_energy(df)
    MainApp.MainApp.absEnergy = tsf
    main.label_10.setText(str(round(tsf,3)))


@threads
def absMax(param, main):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.maximum(df)
    MainApp.MainApp.absMax = tsf
    main.label_12.setText(str(round(tsf, 3)))


@threads
def autocorrelation(param, lag, main):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.autocorrelation(df, lag)
    MainApp.MainApp.autocorrelation = tsf
    main.label_13.setText(str(round(tsf, 3)))

@threads
def complexity(param, lag, main):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.c3(df, lag)
    MainApp.MainApp.complexity = tsf
    main.label_18.setText(str(round(tsf, 3)))

@threads
def countAbove(param, n, main):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.count_above(df, n)
    MainApp.MainApp.countAbove = tsf
    main.label_20.setText(str(round(tsf, 3)))