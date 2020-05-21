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

        layout = self.comp.createVbox(widget)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        login_gp = self.comp.creategroupbox(widget.width() * 0.4, widget.height() * 0.25, "Login Page")
        login_gp_l = self.comp.createVbox(login_gp)

        login_items = ["UserName", "Password"]
        len1= len(login_items)

        Vbox = self.comp.createVbox()
        login_gp_l.addLayout(Vbox)

        hbox = self.comp.createHbox()
        vbox1 = self.comp.createVbox()
        vbox2 = self.comp.createVbox()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        Vbox.addLayout(hbox)

        self.login_list = []
        for i in range(len1):
            username = self.comp.createlabel(login_gp.width() * 0.3, login_gp.height() * 0.18, login_items[i])
            lineedit = self.comp.createlineedit(login_gp.width() * 0.3, login_gp.height() * 0.18, -1, self.st.line1)
            self.login_list.append(lineedit)
            vbox1.addWidget(username)
            vbox2.addWidget(lineedit)

        self.login_list[1].setEchoMode(QtGui.QLineEdit.Password)
        button_login = self.comp.createpushbutton(login_gp.width() * 0.35, login_gp.height() * 0.25, "Login")
        QtCore.QObject.connect(button_login, QtCore.SIGNAL("clicked()"),
                        lambda a=self.login_list : self.check_password(a))

        hbox = self.comp.createHbox()
        hbox.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        hbox.addWidget(button_login)
        login_gp_l.addWidget(self.comp.createVSpliter())
        login_gp_l.addLayout(hbox)

        layout.addWidget(login_gp)


    def check_password(self, list1):
        #print 'at check passwod callback', username.text(), '----', passwd.text()
        if list1[0].text() == self.ot.username and list1[1].text() == self.ot.password :
            self.ot.stackwidget.setCurrentIndex(1)
            self.ot.notifyStatus(" Login Successs.... ", 1)
        else:
            self.ot.notifyStatus(" login failed !!!!  credentials are " + list1[0].text() + '   ' + list1[1].text(), 2)
