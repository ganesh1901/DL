from PyQt4 import QtCore
from PyQt4 import QtGui
from loginPage import loginPage
from pages import *

class mainPage:
    display_time = ''
    display_timer = ''
    def __init__(self, ot, st, comp):
        """

        :rtype: object
        """
        # type: (others, stylesheet, component) -> object
        self.st = st
        self.ot = ot
        self.comp = comp

        self.display_timer = QtCore.QTimer()
        self.display_timer.timeout.connect(self.Update_timer)

        VBOX = self.comp.createVbox(self.ot.widget)

        frame1 = self.comp.createframe(self.ot.widget.width() * 0.99, self.ot.widget.height() * 0.1, self.st.frame)
        frame2 = self.comp.createframe(self.ot.widget.width() * 0.99, self.ot.widget.height() * 0.77, self.st.frame)

        VBOX.addWidget(frame1)
        VBOX.addWidget(frame2)

        self.display_time = self.comp.createlcddisplay(frame1.width() * 0.3, frame1.height(), 20)
        self.display_timer.start(1000)

        self.header(frame1)
        self.contentPage(frame2)


    def Update_timer(self):
        #print 'at timer callback'
        curr_time = self.ot.gettimedate()
        self.display_time.display(curr_time[1:])

    def header(self, widget):
        hbox = self.comp.createHbox(widget)
        hbox.addWidget(self.display_time)

    def contentPage(self, widget):
        stackwidget = QtGui.QStackedWidget(widget)
        stackwidget.resize(widget.width(), widget.height())
        self.ot.stackwidget = stackwidget

        stackpages = []
        for i in range(4):
            widget = QtGui.QWidget()
            widget.resize(stackwidget.width(), stackwidget.height())
            stackwidget.addWidget(widget)
            stackpages.append(widget)

        #testing purpose
        stackwidget.setCurrentIndex(1)

        loginPage(self.ot, self.st, self.comp, stackpages[0])

        page1(self.ot, self.st, self.comp, stackpages[1])


        '''
        
        page2(self.ot, self.st, self.comp, stackpages[2])
        page3(self.ot, self.st, self.comp, stackpages[3])
        '''


















