from PyQt4 import QtCore
from PyQt4 import QtGui
from VarList import TWDL


class page1:
    def __init__(self, ot, st, comp, widget):
        self.ot = ot
        self.st = st
        self.comp = comp
        self.twdl = TWDL()
        self.widget = widget

        tabwidget = QtGui.QTabWidget(widget)
        tabwidget.setFixedSize(widget.width() - 5, widget.height() - 5)
        tabwidget.setStyleSheet(self.st.tabWidget)


        tab1 = QtGui.QWidget()
        tab2 = QtGui.QWidget()
        tabwidget.addTab(tab1, " Config ")
        tabwidget.addTab(tab2, " Data ")

        self.configPage(tab1)

    def configPage(self, widget):

        Hbox = self.comp.createHbox(widget)

        config_req_gb = self.configurationRequest()

        vbox = self.comp.createVbox()
        version_gb = self.groundDLVersion()
        config_restable_gb = self.configurationResponseTable()
        #vbox.addWidget(version_gb)
        #vbox.addWidget(config_restable_gb)

        status_gb = self.statusResponse()
        health_res_gb = self.healthResponse()


        Hbox.addWidget(config_req_gb)
        Hbox.addWidget(version_gb)
        Hbox.addWidget(health_res_gb)
        Hbox.addWidget(status_gb)
        Hbox.addWidget(config_restable_gb)



    def statusResponse(self):
        status_gb = self.comp.creategroupbox(self.widget.width() * 0.20, -1, " DL Status")
        status_gb_l = self.comp.createHbox(status_gb)
        len1 = len(self.twdl.ground_dl_status_items)

        li = []
        vbox1 = self.comp.createVbox()
        vbox2 = self.comp.createVbox()
        for i in range(len1):
            label = self.comp.createlabel(status_gb.width() * 0.35, -1, self.twdl.ground_dl_status_items[i])
            lineedit = self.comp.createlineedit(status_gb.width() * 0.4, -1, False, self.st.line_readonly)
            vbox1.addWidget(label)
            vbox2.addWidget(lineedit)
            li.append(lineedit)
        status_gb_l.addLayout(vbox1)
        status_gb_l.addLayout(vbox2)

        return status_gb


    def healthResponse(self):
        health_gb = self.comp.creategroupbox(self.widget.width() * 0.20, -1, " DL Health")
        health_gb_l = self.comp.createHbox(health_gb)
        len1 = len(self.twdl.ground_dl_health_items)

        li = []
        vbox1 = self.comp.createVbox()
        vbox2 = self.comp.createVbox()
        for i in range(len1):
            label = self.comp.createlabel(health_gb.width() * 0.35, -1, self.twdl.ground_dl_health_items[i])
            lineedit = self.comp.createlineedit(health_gb.width() * 0.4, -1, False, self.st.line_readonly)
            vbox1.addWidget(label)
            vbox2.addWidget(lineedit)
            li.append(lineedit)
        health_gb_l.addLayout(vbox1)
        health_gb_l.addLayout(vbox2)

        return health_gb


    def groundDLVersion(self):
        version_gb = self.comp.creategroupbox(self.widget.width() * 0.20, -1, "Version Details")
        version_gb_l = self.comp.createVbox(version_gb)
        len1 = len(self.twdl.ground_dl_version_items)

        li = []
        Hbox = self.comp.createHbox()
        vbox1 = self.comp.createVbox()
        vbox2 = self.comp.createVbox()
        for i in range(len1):
            label = self.comp.createlabel(version_gb.width() * 0.35, -1, self.twdl.ground_dl_version_items[i])
            lineedit = self.comp.createlineedit(version_gb.width() * 0.4, -1, False, self.st.line_readonly)
            vbox1.addWidget(label)
            vbox2.addWidget(lineedit)
            li.append(lineedit)
        Hbox.addLayout(vbox1)
        Hbox.addLayout(vbox2)

        hbox = self.comp.createHbox()
        hbox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        button = self.comp.createpushbutton(version_gb.width() * 0.4, version_gb.height() * 0.05, "Request")
        QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), lambda a=0xe: self.proceedNext(a))
        hbox.addWidget(button)

        version_gb_l.addLayout(Hbox)
        version_gb_l.addLayout(hbox)

        return version_gb

    def configurationResponseTable(self):

        configrestable = self.comp.creategroupbox(self.widget.width() * .20, -1, "Response Table")
        configrestable_l = self.comp.createHbox(configrestable)


        # creating the table with DL FREQ and UL CDMA code selection
        hbox1 = self.comp.createHbox()
        v1 = self.comp.createVbox()
        v1.setAlignment(QtCore.Qt.AlignTop)
        v2 = self.comp.createVbox()
        v2.setAlignment(QtCore.Qt.AlignTop)
        v3 = self.comp.createVbox()
        v3.setAlignment(QtCore.Qt.AlignTop)
        hbox1.addLayout(v1)
        hbox1.addLayout(v2)
        hbox1.addLayout(v3)

        v1.addWidget(self.comp.createlabel(configrestable.width() * 0.35, 30, "Missile"))
        v1.addWidget(self.comp.createVSpliter())
        v2.addWidget(self.comp.createlabel(configrestable.width() * 0.35, 30, "DL_FREQ"))
        v2.addWidget(self.comp.createVSpliter())
        v3.addWidget(self.comp.createlabel(configrestable.width() * 0.35, 30, "UL-CDMA"))
        v3.addWidget(self.comp.createVSpliter())

        len1 = len(self.twdl.ground_config_req_table_vheader)
        li1 = []
        li2 = []
        for i in range(len1):
            label = self.comp.createlabel(configrestable.width() * 0.35, 25, self.twdl.ground_config_req_table_vheader[i])
            dl_freq = self.comp.createlineedit(configrestable.width() * 0.3, 25, False, self.st.line_readonly)
            li1.append(dl_freq)
            ul_cdma = self.comp.createlineedit(configrestable.width() * 0.3, 25, False, self.st.line_readonly)
            li2.append(ul_cdma)
            v1.addWidget(label)
            v2.addWidget(dl_freq)
            v3.addWidget(ul_cdma)

        configrestable_l.addLayout(hbox1)
        return configrestable

    def configurationRequest(self):
        config_gb = self.comp.creategroupbox( self.widget.width() * 0.20, -1, " Configuration ")
        config_gb_l = self.comp.createVbox(config_gb)

        # normal input fields without table
        hbox = self.comp.createHbox()
        vbox1 = self.comp.createVbox()
        vbox2 = self.comp.createVbox()

        len1 = len(self.twdl.ground_config_req_items)
        li = []
        for i in range(len1):
            label = self.comp.createlabel(config_gb.width() * 0.35, 30, self.twdl.ground_config_req_items[i])
            combo = self.comp.createcombobox(config_gb.width() * 0.3, 30, self.twdl.ground_config_req_items_values[i], self.twdl.ground_config_req_items_values_default[i])
            vbox1.addWidget(label)
            vbox2.addWidget(combo)
            li.append(combo)

        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        # creating the table with DL FREQ and UL CDMA code selection
        hbox1 = self.comp.createHbox()
        v1 = self.comp.createVbox()
        v2 = self.comp.createVbox()
        v3 = self.comp.createVbox()
        hbox1.addLayout(v1)
        hbox1.addLayout(v2)
        hbox1.addLayout(v3)

        v1.addWidget(self.comp.createlabel(config_gb.width() * 0.35, 25, "Missile"))
        v1.addWidget(self.comp.createVSpliter())
        v2.addWidget(self.comp.createlabel(config_gb.width() * 0.35, 25, "DL_FREQ"))
        v2.addWidget(self.comp.createVSpliter())
        v3.addWidget(self.comp.createlabel(config_gb.width() * 0.35, 25, "UL-CDMA"))
        v3.addWidget(self.comp.createVSpliter())

        len1 = len(self.twdl.ground_config_req_table_vheader)
        for i in range(len1):
            label = self.comp.createlabel(config_gb.width() * 0.35, 25, self.twdl.ground_config_req_table_vheader[i])
            dl_freq_combo = self.comp.createcombobox(config_gb.width() * 0.3, 20, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa, 0xb, 0xc], i)
            ul_cdma_combo = self.comp.createcombobox(config_gb.width() * 0.3, 20, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa], i)
            v1.addWidget(label)
            v2.addWidget(dl_freq_combo)
            v3.addWidget(ul_cdma_combo)

        #button for send a request
        vvbox = self.comp.createHbox()
        vvbox.setAlignment( QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom )
        button = self.comp.createpushbutton(config_gb.width() * 0.6, 25, "Config Request")
        QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"),
                               lambda a=1: self.proceedNext(a))
        vvbox.addWidget(button)


        config_gb_l.addLayout(hbox)
        config_gb_l.addLayout(hbox1)
        config_gb_l.addWidget(self.comp.createVSpliter())
        config_gb_l.addLayout(vvbox)

        return config_gb


    def proceedNext(self, a):
        if a == 0xe:
            pass
        elif a == 4:
            print 'config command'



class page2:
    def __init__(self, ot, st, comp, widget):
        self.ot = ot
        self.st = st
        self.comp = comp


class page3:
    def __init__(self, ot, st, comp, widget):
        self.ot = ot
        self.st = st
        self.comp = comp

