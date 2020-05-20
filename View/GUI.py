
from PyQt4 import *
import datetime
import time

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from VarList import FIFO
from VarList import Others
from VarList import StyleSheet
from VarList import TWDL
from Listener import ReceiverHandler
from Component import Component
from mainPage import mainPage


class mainClass:
    def __init__(self):
        self.ot = Others()
        self.ot.logDebug(" Application Started !!!!")
        self.st = StyleSheet()
        self.ff = FIFO()
        self.twdl = TWDL()
        self.comp = Component()
        # self.flatc = FlatcOperations(self.ot, self.ff, self.twdl)
        # self.readconfig = ReadConfig(self.ot)

        self.ot.app = QtGui.QApplication([self.ot.app_name])

        self.ot.desktop_width = 1080
        self.ot.desktop_height = 640

        print 'desktop resolution -- ', self.ot.app.desktop().geometry().width(), self.ot.app.desktop().geometry().height()

        ret = GUI(self.ot, self.ff, self.st, self.comp)
        t1 = mainPage(self.ot, self.st, self.comp)

        self.initListener()
        sys.exit(self.ot.app.exec_())


    def initListener(self):
        # receiver object has to alive otherwise  variable scope problem will arise
        self.rt = ReceiverHandler(self.ot, self.ff)


class GUI(QtGui.QMainWindow):

    network_timer = QtCore.QTimer()

    def __init__(self, ot, ff, st, comp):
        super(GUI, self).__init__()
        self.ot = ot
        self.ff = ff
        self.st = st
        self.comp = comp
        self.initUI()
        self.statusbar = ''

    def initUI(self):
        #only close button enable
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.ot.desktop_width , self.ot.desktop_height)
        self.setWindowTitle(self.ot.app_name)
        self.setCentralWidget(QtGui.QWidget())
        self.ot.widget = self.centralWidget()
        self.show()

        print 'central widget resolution', self.ot.widget.width(), self.ot.widget.height()


        bar = self.menuBar()
        help = bar.addMenu("Help")
        about = bar.addMenu("&About")
        screenshot = bar.addMenu("&ScreenShot")

        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet(self.st.statusbar)
        self.ot.network_status = self.comp.createlabel(self.ot.desktop_width * 0.05, 30, "Network", self.st.valid_label)
        self.network_timer.timedout.connect(self.network_check)

        self.ot.statusbar = self.comp.createlabel(self.ot.desktop_width * 0.92, 30, '1235478', self.st.valid_label)
        self.statusbar.addPermanentWidget(self.ot.network_status)
        self.statusbar.addPermanentWidget(self.ot.statusbar)

        action_shot = QtGui.QAction("ScreenShot", self)
        action_shot.setShortcut("Ctrl+S")
        screenshot.addAction(action_shot)
        screenshot.triggered.connect(self.screenShot)

        action_help = QtGui.QAction("Help", self)
        action_help.setShortcut("Ctrl+H")
        help.addAction(action_help)
        action_help.triggered.connect(self.helpAction)

        action_gui = QtGui.QAction("Appliaction", self)
        about.addAction(action_gui)
        action_gui.triggered.connect(self.controllerApp)

    def network_check(self):
        
    def screenShot(self):
        QtGui.QPixmap.grabWindow(self.ot.app.desktop().winId()).save('../out/test'+self.ot.gettimedate()+'.png', 'png')

    def helpAction(self):
        dialog = QtGui.QDialog()
        dialog.setWindowTitle("Help")
        dialog.exec_()

    def controllerApp(self):
        dialog = QtGui.QDialog()
        dialog.setFixedSize(300, 300)
        dialog.setWindowTitle("Application")
        gridlayout = QtGui.QGridLayout(dialog)

        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.2, dialog.height() * 0.1, "Version"), 0, 0)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.2, dialog.height() * 0.1, "Date"), 1, 0)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.2, dialog.height() * 0.1, "Checksum"), 2, 0)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.2, dialog.height() * 0.1, "Size"), 3, 0)

        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.3, dialog.height() * 0.1, self.ot.version), 0, 1)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.3, dialog.height() * 0.1, self.ot.dated), 1, 1)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.3, dialog.height() * 0.1, self.ot.getchecksum()), 2, 1)
        gridlayout.addWidget(self.comp.createlabel(dialog.width() * 0.3, dialog.height() * 0.1, self.ot.getappsize()), 3, 1)

        dialog.exec_()

    '''
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.No |
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            self.ot.logDebug('**************** Application Closed **************')
        else:
            event.ignore()
    
    '''
    def initListener(self):
        rt = ReceiverHandler(self.ot, self.ff)
        rt.start()






