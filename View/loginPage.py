from PyQt4 import QtGui
from PyQt4 import QtCore


class loginPage:
    def __init__(self, ot, st, comp, widget):

        self.ot = ot
        self.st = st
        self.comp = comp
        self.loginScreen(widget)

    def loginScreen(self, widget):

        print 'loginpage size', widget.width(), widget.height()

        widget.resize(400, 400)

        layout = QtGui.QGridLayout(widget)

        layout.setAlignment(QtCore.Qt.AlignCenter)

        label_name = QtGui.QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QtGui.QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QtGui.QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QtGui.QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QtGui.QPushButton('Login')
        QtCore.QObject.connect(button_login, QtCore.SIGNAL("clicked()"),
                        lambda a=self.lineEdit_username,b=self.lineEdit_password: self.check_password(a, b))
        #QtCore.Qt.Qobjectbutton_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 2, 1)
        layout.setRowMinimumHeight(2, 100)
        layout.setColumnMinimumWidth(2, 100)

    def check_password(self, username, passwd):
        #print 'at check passwod callback', username.text(), '----', passwd.text()
        if username.text() == self.ot.username and passwd.text() == self.ot.password :
            self.ot.stackwidget.setCurrentIndex(1)
            self.ot.notifyStatus(" Login Successs.... ", 1)
        else:
            self.ot.notifyStatus(" login failed !!!!  credentials are " + username.text() + '   ' + passwd.text(), 2)
