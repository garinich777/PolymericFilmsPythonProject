from MainApp import MainApp
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
