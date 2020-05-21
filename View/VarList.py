import struct
import re
from PyQt4 import QtGui, QtCore
import os
import select
import crcmod
import socket
import math
import datetime


class Others:
    def __init__(self):
        try:
            self.app = ''
            self.widget = ''
            self.app_name = ' Radar Computer Simulator '
            self.version = '1.0'
            self.dated = '20-05-2020'

            self.desktop_width = 0
            self.desktop_height = 0

            self.status_timer = QtCore.QTimer()
            self.status_timer.timeout.connect(self.status_timeout)

            self.username = 'Akashng'
            self.password = '12345'

            self.stackwidget = ''

            self.statusbar = ''
            self.network_status = ''
            self.datapoll = []

            self.logfd = open("../out/app-log" + self.gettimedate() + ".log", "w+")
            print 'login fd ****', self.logfd

            self.pipe_data = []
            self.st = StyleSheet()
        except IOError:
            print 'IOError ---', IOError.filename

    def getchecksum(self):
        cwd = os.getenv('PWD')
        os.system('../run_scripts/checksum.sh')
        f = open('/tmp/cfg', 'r')
        buf = ''
        if f:
            buf = f.readline()
            print 'Data', buf
            f.close()
        return str(buf.split(' ')[0][-8:])

    def getappsize(self):
        return str(os.stat('../APP.tar').st_size) + str('  in bytes')

    def gettimedate(self):
        curr_time_object = datetime.datetime.now()
        curr_time = "-%02d-%02d-%04d-%02d-%02d-%02d" % (
            curr_time_object.day, curr_time_object.month, curr_time_object.year, curr_time_object.hour,
            curr_time_object.minute, curr_time_object.second)
        return curr_time

    def logDebug(self, text):
        self.logfd.write(self.gettimedate()[1:] + '\t')
        self.logfd.write("Debug:\t")
        self.logfd.write(text)
        self.logfd.write("\n")

    def logWarning(self, text):
        self.logfd.write(self.gettimedate() + '\t')
        self.logfd.write("Warning:\t")
        self.logfd.write(text)
        self.logfd.write("\n")

    def status_timeout(self):
        self.status_timer.stop()
        self.statusbar.setText('')

    def notifyStatus(self, notify_text, notify_type):

        if notify_type == 1:
            self.statusbar.setText(notify_text)
            self.statusbar.setStyleSheet(self.st.valid_label)
            self.logDebug(notify_text)
        elif notify_type == 2:
            self.statusbar.setText(notify_text)
            self.statusbar.setStyleSheet(self.st.notvalid_label)
            self.logWarning(notify_text)
        else:
            self.statusbar.setText(notify_text)
            self.statusbar.setStyleSheet(self.st.default_label)
            self.logDebug(notify_text)

        # self.status_timer.start(1000)


class TWDL:
    def __init__(self):
        self.crc16 = crcmod.mkCrcFun(0x11021, 0x1d0f, 0, 0)
        self.ground_msg_id = [4, 0xc, 0xd, 0xe, 8, 7]

        self.ground_content_fmt_list = []
        self.ground_content_fmt_list.append('>I2BHH12B11H3H')
        self.ground_content_fmt_list.append('=I2BHHHHH')
        self.ground_content_fmt_list.append('=I2BHHHH')
        self.ground_content_fmt_list.append('=I2BHHHHH')

        # added on 20-05-2020

        self.ground_config_req_items = ["UL-Freq1", "UL-Freq2", "DL-CDMA", "UL-FEC", "DL-FEC", "PA MODE", "Ant Selection"]
        self.ground_config_req_items_values = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa],
                                               ["ON", "OFF"], ["ON", "OFF"], ["OFF", "Low Power", "Medium Power", "High Power"], ["Port1", "Port2"]]
        self.ground_config_req_items_values_default = [0, 0, 1, 1, 1, 0, 0]

        self.ground_config_req_table_vheader = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]

        self.ground_dl_version_items = ["DL-Checksum", "APP SIZE", "Date", "Major-Minor"]

        self.ground_dl_status_items = [" Dual RX Index", "Seq No", "UL-Freq1", "UL-Freq2", "DL-CDMA",
                                       "TX Antenna", "PA MODE", "RX1-RSSI", "RX2-RSSI", "RX1-PLL",
                                       "RX2-PLL", "TX LOCK", "Decoder-1", "Decoder-2", "DL-FEC", "UL-FEC"]

        self.ground_dl_status_items_list_offset = [5, 3, 6, 7, 18, 29, 30, 31, 32, 35, 36, 37, 38]

        self.ground_dl_health_items = ["Dual RX index", "SeqNo", "RX1-PLL", "RX2-PLL", "TX-PLL", "Decoder-1",
                                       "Decoder-2", "RX1-RSSI", "RX2-RSSI", "PA MODE", "RX1-Doppler",
                                       "Rx2-Doppler", "Tx Antenna"]
        self.ground_dl_health_offset = [5, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        self.ground_dl_health_rspfmt = ''

        self.pa_show_map = {}
        self.pa_show_map[0] = "OFF"
        self.pa_show_map[0xff01] = "1 watt"
        self.pa_show_map[0xff02] = "5 watt"
        self.pa_show_map[0xff03] = "15 watt"
        self.pa_show_map[0xff04] = "25 watt"

        self.antenna_show_map = {}
        self.antenna_show_map[0xffff] = "PORT 2"
        self.antenna_show_map[0] = "PORT 1"

        self.fec_show_map = {}
        self.fec_show_map[0xff] = "ON"
        self.fec_show_map[0] = "OFF"

        self.decoder_show_map = {}
        self.decoder_show_map[0xff] = "TRACK"
        self.decoder_show_map[0] = "ACQ"

        self.ground_rsp_status_map = {}
        self.ground_rsp_status_map[29] = self.antenna_show_map
        self.ground_rsp_status_map[30] = self.pa_show_map
        self.ground_rsp_status_map[35] = self.decoder_show_map
        self.ground_rsp_status_map[36] = self.decoder_show_map
        self.ground_rsp_status_map[37] = self.fec_show_map
        self.ground_rsp_status_map[37] = self.fec_show_map

        self.ground_dl_health_items_map = {}
        self.ground_dl_health_items_map[8] = self.decoder_show_map
        self.ground_dl_health_items_map[9] = self.decoder_show_map
        self.ground_dl_health_items_map[12] = self.pa_show_map
        self.ground_dl_health_items_map[13] = self.fec_show_map
        self.ground_dl_health_items_map[14] = self.fec_show_map
        self.ground_dl_health_items_map[15] = self.fec_show_map
        self.ground_dl_health_items_map[16] = self.fec_show_map
        self.ground_dl_health_items_map[17] = self.antenna_show_map


class FIFO:
    def __init__(self):
        try:
            self.host = '0.0.0.0'
            self.port = 6511

            self.udpconn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udpconn.bind((self.host, self.port))
            self.max_fifo_size = 512


        except IOError as IE:
            print 'IOError', IE


class StyleSheet:
    def __init__(self):
        self.frame = '''
            .QFrame{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dae3de, stop: 1#dae3de); 
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#000000;
                border: 2px solid rgb(0, 0, 0) ;
            }
            '''

        self.frame1 = '''
                 .QFrame{
                     background-color:rgb(255, 255, 255); 
                     font-family:Georgia;
                     font-size :18px;
                     font-weight:bold;
                     color:#000000;
                     border: 2px solid rgb(0, 0, 0) ;
                 }
                 '''
        self.frame_noborder = '''
            .QFrame{
              background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dae3de, stop: 1#dae3de); 
              font-family:Georgia;
              font-size :14px;
              font-weight:bold;
              color:#000000;
              border: 1px dotted rgb(255, 255, 255) ;                      
            }
            '''
        self.header_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :22px;
             font-weight:bold;
             color:#000000;
            }
            '''
        self.cmd_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :16px;
             font-weight:bold;
             color:#a0522d;
            }
            '''
        self.rsp_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :14px;
             font-weight:bold;
             color:rgb(200,145,12);
            }
            '''

        self.default_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :16px;
             font-weight:bold;
             color:rgb(169, 169, 169);
            }
            '''

        self.statusbar = '''
          .QStatusBar{
            border: 2px solid black;
          }
          '''

        self.notvalid_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :20px;
             font-weight:bold;
             color:rgb(255, 0, 0);
            }
            '''

        self.valid_label = '''
            .QLabel{
             font-family:Times New Roman;
             font-size :20px;
             font-weight:bold;
             color:rgb(0, 0, 255);
            }
            '''

        self.default_status = '''
            .QStatusBar{
             font-family:Times New Roman;
             font-size :16px;
             font-weight:bold;
             color:rgb(169, 169, 169);
            }
            '''

        self.notvalid_status = '''
            .QStatusBar{
             font-family:Times New Roman;
             font-size :20px;
             font-weight:bold;
             color:rgb(255, 0, 0);
            }
            '''

        self.valid_status = '''
            .QStatusBar{
             font-family:Times New Roman;
             font-size :20px;
             font-weight:bold;
             color:rgb(0, 0, 255);
            }
            '''

        self.status_label = '''
            .QLabel{
                     font-family:Times New Roman;
                     font-size :14px;
                     font-weight:bold;
                     color:rgb(0, 0, 255);
                    }
            '''

        self.gbox = """
            .QGroupBox {
                font: bold"Times New Roman";    
                font-size:19px;
                border: 3px solid gray;
                border-radius:2px;
                margin-top:0.7em;
                left:0.01em;
                top:-2em;
                background-color : rgb(255, 255, 255);                
            }
            .QGroupBox::title{
                subcontrol-origin:margin;
                padding:0 1px 0 3px;
                subcontrol-position: top center; /* position at the top center */
            }
            
            .QLabel{
                font-family:Georgia;
                font-size :14px;
                font-weight:bold;
                color:#a0522d;
                text-align:justify; 
                border:none;          
            }
            .QLineEdit{
                background-color : rgb(255, 255, 255); 
                font-family:Georgia;
                font-size :16px;
                font-weight:bold;
                text-align: justify;
                right:0.1em;
                color:#000000;     
                border:2px solid green;
            }
            
            .QLineEdit:read-only {
                background-color: rgb(255, 0, 0);
                border:2px solid red;
            }
            .QTextEdit{
                background-color : rgb(255, 255, 255); 
                font-family:Georgia;
                font-size :16px;
                font-weight:bold;
                color:#000000;     
                border:2px dashed gray;
            }            
            
            .QCheckBox{
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#a0522d;
                text-align:justify; 
                border:none; 
            
            }
            
            .QRadioButton{
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#a0522d;
                text-align:justify; 
                border:none; 
            
            }
            
            .QPushButton{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #666600 stop: 1 #9ACD32);    
                font-family:Georgia;
                font-size :14px;
                font-weight:bold;
                color:#ffffff;
                border-radius: 5;
            }
            
            QPushButton:hover
            {
                   background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0      #BDB76B stop: 1 #FFDAB9);
                   color:#000000;
            }
            """
        self.line1 = """
                .QLineEdit{
                        background-color : rgb(255, 255, 255); 
                        font-family:Georgia;
                        font-size :16px;
                        font-weight:bold;
                        text-align: justify;
                        right:0.1em;
                        color:#000000;     
                        border:2px solid green;
                    }
                """

        self.line_readonly = """
            .QLineEdit{
                background-color : rgb(255, 255, 255); 
                font-family:Georgia;
                font-size :16px;
                font-weight:bold;
                text-align: justify;
                right:0.1em;
                color:#000000;     
                border:2px solid black;
            }
            """

        self.line_OK = """
        	.QLineEdit{
                background-color : rgb(255, 255, 255); 
                font-family:Georgia;
                font-size :16px;
                font-weight:bold;
                text-align: justify;
                right:0.1em;
                color:#0000ff;     
                border:2px solid green;
            }
        	"""
        self.line_notok = """
            .QLineEdit{
                background-color : rgb(255, 255, 255); 
                font-family:Georgia;
                font-size :16px;
                font-weight:bold;
                text-align: justify;
                right:0.1em;
                color:#ff0000;     
                border:2px solid green;
            }
            """
        self.label = '''
            .QLabel{
                font-family:Times New Roman;
                font-size :18px;
                font-weight:bold;
                color:#006600;
            }
            '''

        self.hils_frame_label_start = '''
                QLabel{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fdf5e6 stop: 1 #fdf5e6);	
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#000000;
                border-radius: 10;
            }
            '''

        self.dialog = '''
            .QDialog{
                background-color:rgb(255, 255, 255);
                font-family:Georgia;
                font-size:18px;
                color:#000000;
                border-radius:10;
            }
            '''

        self.hils_frame_label_stop = '''
            .QLabel{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #3cb371 stop: 1 #3cb371);	
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#ffffff;
                border-radius: 10;
            }
            '''

        self.table_header_style = "::section {""background-color: #808b96; color: #4b0082; font-size:20px; font-family:Times New Roman; font-weight:bold;}"

        self.table_header_style1 = "::section {""background-color: #808b96; color:#4b0082 ; font-size:15px; font-family:Times New Roman; font-weight:bold;}"

        self.table_style = '''
            QTableView{
                border: 2px solid;
                background:#fffafa;
                color:sienna;
                gridline-color: solid black;
            }   
            '''

        self.tree_view_style_sheet = '''
            
            QTreeView{
                color:#800080;
            }
            
            
            QTreeView::item:hover{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1 stop: 1 #00bfff);
                border: 1px solid #000;
                color: #ffffff;
            }
            
            QTreeView::item:selected{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1 stop: 1 #567dbc);
            }
            
            QTreeView::item:selected !active{
                background-color:red;
            }
            '''

        self.treeview_font = QtGui.QFont("Georgia", 12, QtGui.QFont.Bold)

        self.push_button = '''
            .QPushButton{
                background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #666600 stop: 1 #9ACD32);    
                font-family:Georgia;
                font-size :18px;
                font-weight:bold;
                color:#ffffff;
                border-radius: 10;
            }
            
            .QPushButton:hover
            {
                   background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0      #BDB76B stop: 1 #FFDAB9);
                   color:#000000;
            }
            '''
        self.table_header_style = "::section {""background-color: #808b96; color: #4b0082; font-size:20px; font-family:Times New Roman; font-weight:bold;}"

        self.table_header_style1 = "::section {""background-color: #808b96; color:#4b0082 ; font-size:15px; font-family:Times New Roman; font-weight:bold;}"

        self.table_style = '''
            .QTableView{
                border: 2px solid;
                background:#fffafa;
                color:sienna;
                gridline-color: solid black;
            }
            '''
        self.textedit = """
            .QTextEdit
            {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fffafa, stop: 1 #fffafa);
                font-family:Georgia;
                font-size:16px;
                font-weight:bold;
                color:#000000;
                border:1px solid;
                border-radius: 5;    
            }
            """
        self.tabWidget = '''
            .QTabWidget::pane { /* The tab widget frame */
                border: 2px dashed rgb(0, 0, 0);
            }
           
            /* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QTabWidget */
            .QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 1.0 #D3D3D3);
                border: 1px solid #C4C4C3;
            }
            .QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }
            
            .QTabBar::tab {
                background-color: rgb(169, 169, 169);	
                height:20px;
                width: 70px;
                border: 3px solid black;
            }
        '''

        self.tabWidget1 = '''
            .QTabWidget::pane{ /* The tab widget frame */
                border:1px dashed  #C337CB;
                top: -0.2em;
                left: 0.2em;
            }   
            '''

        self.stack_widget = '''
            .QStackedWidget{
                border: 2px solid rgb(0, 0, 0) 
            }
            
            '''
