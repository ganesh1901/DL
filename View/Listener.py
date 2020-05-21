from PyQt4 import QtCore
import select
import os


class ReceiverHandler(QtCore.QThread):
    receiver_signal = QtCore.pyqtSignal()
    def __init__(self, ot, ff):
        QtCore.QThread.__init__(self)
        self.ot = ot
        self.ff = ff
        self.sock_list = [self.ff.udpconn.fileno()]
        self.receiver_signal.connect(self.DecodeData)
        self.start()

    def run(self):
        while True:
            read_list, write_list, error_list = select.select(self.sock_list, [], [], 0)
            for fd in read_list:
                data = os.read(fd, self.ff.max_fifo_size)
                self.ot.datapoll.append(data)
                self.receiver_signal.emit()

    @QtCore.pyqtSlot()
    def DecodeData(self):
        data = self.ot.datapoll.pop()
        print 'data from the socket', data