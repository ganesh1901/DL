from PyQt4 import QtCore

class ReceiverHandler(QtCore.QThread):
    def __init__(self, ot, ff):
        QtCore.QThread.__init__(self)
        self.ot = ot
        self.ff = ff

    def run(self):
        while True:
            pass
