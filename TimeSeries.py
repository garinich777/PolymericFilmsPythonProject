import numpy as np
import tsfresh.feature_extraction.feature_calculators
import threading
import MainApp


def threads(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()
    return wrapper


@threads
def absEnergyCalc(param):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.abs_energy(df)
    MainApp.MainApp.absEnergy = tsf


@threads
def absMax(param):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.maximum(df)
    MainApp.MainApp.absMax = tsf

@threads
def autocorrelation(param, lag):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.autocorrelation(df, lag)
    MainApp.MainApp.autocorrelation = tsf

@threads
def complexity(param, lag):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.c3(df, lag)
    MainApp.MainApp.complexity = tsf

@threads
def countAbove(param, n):
    df = np.array(param);
    tsf = tsfresh.feature_extraction.feature_calculators.count_above(df, n)
    MainApp.MainApp.countAbove = tsf