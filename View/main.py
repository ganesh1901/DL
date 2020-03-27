import sys
from PyQt4 import QtGui
from VarList import Others

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()

    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            sys.exit(0)

if __name__ == '__main__':

    ot = Others()

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

