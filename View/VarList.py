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

            self.logfd = open("../out/app-log" + self.gettimedate() + ".log", "w+")
            print 'login fd ****' ,self.logfd

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

        #self.status_timer.start(1000)


class TWDL:
    def __init__(self):

        # flag for OBC or without OBC
        self.obc_flag = 1
        self.msg_seq_number = 0
        self.twdl_gbox_name = ["Configuration Command", "PA Config", "TX Antenna", "Version Details", "Status--Health"]
        self.second_word = [0x5443, 0x5450, 0x5458, 0x5456, 0x5448, 0x5454]

        self.message_id = [0x7, 0xA, 0xB, 0xC, 0x9, 0x8, 0xD]
        self.config_cmd_field = ["Missile Id", "Uplink Freq", "Dnlink Freq", "Uplink CDMA", "Dnlink CDMA",
                                 "Up & Dn FEC",
                                 "PA Mode", "TX Antn"]

        self.config_cmd_fmt = "=I8HH"
        self.config_cmd_items = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8],
                                 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA],
                                 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA], ["ON &OFF", "ON & ON", "OFF & ON", "OFF & OFF"],
                                 ["OFF", "1 watt", "5 watt", "10 watt", "15 watt"], ["Port1", "Port2"]]
        self.config_cmd_items_value = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8],
                                       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC],
                                       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA],
                                       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xA], [0xff00, 0xffff, 0x00ff, 0x0000],
                                       [0x0000, 0xFF01, 0xff02, 0xff03, 0xff04], [0, 0xffff]]

        self.pa_cmd_field = ["Power MODE"]
        self.pa_cmd_items = [["OFF", "1 watt", "5 watt", "10 watt", "15 watt"]]
        self.pa_cmd_items_value = [[0x0000, 0xFF01, 0xff02, 0xff03, 0xff04]]
        self.pa_cmd_fmt = "=I3HH"

        self.tx_switchover_cmd_field = ["Tx Antn"]
        self.tx_switchover_cmd_items = [["Port1", "Port2"]]
        self.tx_switchover_cmd_items_value = [[0, 0xffff]]
        self.tx_switchover_cmd_fmt = "=I3HH"

        self.version_details_field = ["MissileId", "Checksum"]
        self.version_cmd_fmt = '=IHHH'

        self.combo_item_list = []
        self.combo_item_list.append(self.config_cmd_items)
        self.combo_item_list.append(self.pa_cmd_items)
        self.combo_item_list.append(self.tx_switchover_cmd_items)

        # self.config_rsp_field = ["Missile Id", "Uplink Freq", "Dnlink Freq","Uplink CDMA", "Dnlink CDMA", "PA Status", "RF status", "TX Power Mode", "RSSI-RX1", "RSSI-RX2", "Synthesizer Lock", "Uplink FEC", "Dnlink FEC"]
        self.config_onboard_rsp_field = ["Missile Id", "UL-Freq", "DL-Freq", "UL-CDMA", "DL-CDMA", "TX Ant",
                                         "PA Status", "RSSI-RX1", "RSSI-RX2", "RX1 Lock", "RX2 Lock", "Tx Lock",
                                         "RX1-Dec",
                                         "RX2-Dec", "Dnlink FEC", "Uplink FEC", "RX1-Dopp",
                                         "RX2 Dopp", "RX1-Corr", "RX2-Corr"]


        if self.obc_flag == 1:
            self.config_rsp_fmt = "=HHI2BH2BHHHH8BH16H"
            self.version_rsp_fmt = '=HHI2BH3H23H'
            self.onboard_config_rsp_ui_offset = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]
            self.config_rsp_field_index = [3, 6, 7, 8, 9, 12, 13, '14|1', '14|2', '15|1']

        else:
            self.config_rsp_fmt = "=I2BH2BHHHH8BH18H"
            self.version_rsp_fmt = '=I2BH3H23H'
            self.config_rsp_field_index = [1, 4, 5, 6, 7, 8, 9, 10, 11, '12|1', '12|2', '13|1', 14, 15, 16, 17]

        self.pastatus_map = {}

        self.config_rsp_alias_map = {}

        if self.obc_flag == 1:
            self.health_rsp_fmt = "=HHIBBH2BBBBB6H17H"
            # self.health_rsp_field_index = ['6|1', '6|2', '7|1', 8, 9, 13, 14, 15, 16] #merged the fields to status and health
            self.health_rsp_field_index = [13, 14, 15, 16]
        else:
            self.health_rsp_fmt = "=IBBH2BBBBB6H19H"
            self.health_rsp_field_index = ['4|1', '4|2', '5|1', 6, 7, 10, 11, 12, 13]

        self.comm_test_resp1 = ["Tx Cmd Flag", "Target Id", "Target Type"]
        self.comm_test_resp2 = ["Pos", "Vel"]
        self.comm_test_resp_fmt = "=HHI2BHH2B3f3hH14H"
        self.comm_test_resp_index = [6, 7, 8, 9, 10, 11, 12, 13, 14]

        self.content_list = []
        self.content_list.append(self.config_cmd_field)
        self.content_list.append(self.pa_cmd_field)
        self.content_list.append(self.tx_switchover_cmd_field)
        self.content_list.append(self.version_details_field)
        self.content_list.append(self.config_onboard_rsp_field)
        self.content_list.append(self.comm_test_resp1)

        self.content_fmt_list = []
        self.content_fmt_list.append(self.config_cmd_fmt)
        self.content_fmt_list.append(self.pa_cmd_fmt)
        self.content_fmt_list.append(self.tx_switchover_cmd_fmt)
        self.content_fmt_list.append(self.version_cmd_fmt)

        self.cmd_items_value = []
        self.cmd_items_value.append(self.config_cmd_items_value)
        self.cmd_items_value.append(self.pa_cmd_items_value)
        self.cmd_items_value.append(self.tx_switchover_cmd_items_value)

        if self.obc_flag == 1:
            self.subaddr_list = [4, 4, 4, 6]
            self.rt_address = 1
            self.health_data_subadd = 12
            self.status_data_subadd = 13
            self.data_subaddr = [14, 4, 15]
            self.version_subaddr = 6

        else:
            self.subaddr_list = [1, 4, 5, 10]
            self.rt_address = 2
            self.health_data_subadd = 7
            self.status_data_subadd = 8
            self.data_subaddr = [1, 2, 3]
            self.version_subaddr = 6

        self.health_data = []
        self.status_data = []

        self.crc16 = crcmod.mkCrcFun(0x11021, 0x1d0f, 0, 0)
        self.ground_msg_id = [4, 0xc, 0xd, 0xe, 8, 7]

        self.ground_content_fmt_list = []
        self.ground_content_fmt_list.append('>I2BHH12B11H3H')
        self.ground_content_fmt_list.append('=I2BHHHHH')
        self.ground_content_fmt_list.append('=I2BHHHH')
        self.ground_content_fmt_list.append('=I2BHHHHH')

        self.config_ground_rsp_field = ["UL-Freq", "DL-Freq", "UL-CDMA", "DL-CDMA", "TX Ant",
                                        "PA Status", "RSSI-RX1", "RSSI-RX2", "Tx1 Lock", "Tx2 Lock", "Rx Lock",
                                        "RX1-Dec", "RX2-Dec", "Dnlink FEC", "Uplink FEC", "RX1-Dopp",
                                        "RX2 Dopp", "RX1-Corr", "RX2-Corr"]

        self.ground_config_rsp_bytes_status_offset = [6, 8, 18, 19, 31, 32]
        self.ground_config_rsp_ui_status_offset = [1, 2, 3, 4, 7, 8]

        self.ground_config_rsp_ui_health_offset = [0, 1, 2, 3]
        self.ground_config_rsp_bytes_health_offset = [13, 14, 15, 16]


        #added on 20-05-2020

        self.ground_config_req_items = ["UL-Freq1", "UL-Freq2", "DL-CDMA", "UL-FEC", "DL-FEC", "PA MODE", "Ant Selection"]
        self.ground_config_req_items_values = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa],
                                               ["ON", "OFF"], ["ON", "OFF"], ["OFF", "Low Power", "Medium Power", "High Power"], ["Port1", "Port2"]]
        self.ground_config_req_items_values_default = [0, 0, 1, 1, 1, 0, 0]

        self.ground_config_req_table_vheader = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]

        self.ground_dl_version_items = ["DL-Checksum", "APP SIZE", "Date", "Major-Minor"]

        self.ground_dl_status_items = [" Dual RX Index", "Seq No", "UL-Freq1", "UL-Freq2", "DL-CDMA",
                                       "TX Antenna", "PA MODE", "RX1-RSSI", "RX2-RSSI", "RX1-PLL",
                                       "RX2-PLL", "TX LOCK", "Decoder-1", "Decoder-2", "DL-FEC", "UL-FEC"]

        self.ground_dl_status_items_list_offset = [5, 3, 6, 7, 18, 29, 30, 31, 32, 35, 36, 37, 38 ]

        self.ground_rsp_status_map = {}
        self.ground_rsp_status_map[29][0xffff] = "Port2"
        self.ground_rsp_status_map[29][0x0] = "Port1"

        self.ground_rsp_status_map[30][0] = "OFF"
        self.ground_rsp_status_map[30][0xff01] = "1 Watt"
        self.ground_rsp_status_map[30][0xff02] = "5 Watt"
        self.ground_rsp_status_map[30][0xff03] = "15 Watt"
        self.ground_rsp_status_map[30][0xff04] = "25 Watt"

        self.ground_rsp_status_map[30][0xff01] = "1 Watt"

        self.ground_rsp_status_map[35][0x00] = "ACQ"
        self.ground_rsp_status_map[35][0xff] = "TRACK"

        self.ground_rsp_status_map[36][0x00] = "ACQ"
        self.ground_rsp_status_map[36][0xff] = "TRACK"

        self.ground_rsp_status_map[37][0x00] = "OFF"
        self.ground_rsp_status_map[37][0xff] = "ON"

        self.ground_rsp_status_map[38][0x00] = "OFF"
        self.ground_rsp_status_map[38][0xff] = "ON"

        self.ground_dl_health_items = ["Dual RX index", "SeqNo", "RX1-PLL", "RX2-PLL", "TX-PLL", "Decoder-1",
                                       "Decoder-2", "RX1-RSSI", "RX2-RSSI", "PA MODE", "RX1-Doppler",
                                       "Rx2-Doppler", "Tx Antenna"]
        self.ground_dl_health_offset = [5, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

        self.ground_dl_health_items_map = { }
        self.ground_dl_health_items_map[8][0x0] = "ACQ"
        self.ground_dl_health_items_map[8][0xff] = "TRACK"

        self.ground_dl_health_items_map[9][0] = "ACQ"
        self.ground_dl_health_items_map[9][0xff] = "TRACK"

        self.ground_dl_health_items_map[12][0] = "OFF"
        self.ground_dl_health_items_map[12][0xff01] = "1 watt"
        self.ground_dl_health_items_map[12][0xff02] = "5 watt"
        self.ground_dl_health_items_map[12][0xff03] = "15 watt"
        self.ground_dl_health_items_map[12][0xff04] = "25 watt"

        self.ground_dl_health_items_map[13][0] = "OFF"
        self.ground_dl_health_items_map[13][0xff] = "ON"

        self.ground_dl_health_items_map[14][0] = "OFF"
        self.ground_dl_health_items_map[14][0xff] = "ON"

        self.ground_dl_health_items_map[15][0] = "ON"
        self.ground_dl_health_items_map[15][0xff] = "OFF"

        self.ground_dl_health_items_map[16][0] = "ON"
        self.ground_dl_health_items_map[16][0xff] = "OFF"

        self.ground_dl_health_items_map[17][0] = "PORT1"
        self.ground_dl_health_items_map[17][0xffff] = "PORT2"

class FIFO:
    def __init__(self):
        pass

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

        self.hils_frame_label_stop = '''
        
        QLabel{
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
            
            QPushButton:hover
            {
                   background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0      #BDB76B stop: 1 #FFDAB9);
                   color:#000000;
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
            border: 1px dashed rgb(100, 100, 100);
        }
        .QTabWidget::tab-bar {
            top: -0.2em; /* move to the right by 5px */
        }
        /* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QTabWidget */
        .QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 1.0 #D3D3D3);
            border: 1px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }
        .QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        .QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }
        .QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
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


