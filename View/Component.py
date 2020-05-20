from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import *

from VarList import  StyleSheet

class Component:
    def __init__(self):
        # type: (object) -> object
        """

        :type st: object
        """
        self.st = StyleSheet()

    def createVbox(self, parent=-1):
        if parent != -1:
            box = QtGui.QVBoxLayout(parent)
        else:
            box = QtGui.QVBoxLayout()

        return box

    def createHbox(self, parent=-1):
        if parent != -1:
            box = QtGui.QHBoxLayout(parent)
        else:
            box = QtGui.QHBoxLayout()

        return box

    def createframe(self, width, height, stylesheet=-1, framestyle=-1):
        frame = QtGui.QFrame()
        frame.setLineWidth(2)
        frame.setMidLineWidth(1)

        if framestyle != -1:
            frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        else:
            frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)

        if stylesheet != -1:
            frame.setStyleSheet(stylesheet)

        if width != -1:
            frame.setFixedWidth(width)
        if height != -1:
            frame.setFixedHeight(height)
        return frame

    def createlabel(self, width, height, label_name, style=-1):
        label = QtGui.QLabel()
        if width != -1:
            label.setFixedWidth(width)
        if height != -1:
            label.setFixedHeight(height)
        if label_name != -1:
            label.setText(label_name)
        label.setWordWrap(True)
        if style != -1:
            label.setStyleSheet(style)
        return label

    def createlcddisplay(self, width=-1, height=-1, digits=-1):
        # type: (object, object) -> object
        """

        :param digits: no of digits to show on the display
        :param width: widget width
        :param height: widget height
        :return: object
        :rtype: object
        """
        lcd = QtGui.QLCDNumber()
        if width != -1:
            lcd.setFixedWidth(width)
        if height != -1:
            lcd.setFixedHeight(height)
        if digits != -1:
            lcd.setNumDigits(digits)
        lcd.setFrameShape(QtGui.QFrame.NoFrame)

        return lcd

    def creategroupbox(self, width, height, name=-1):
        """

        :param width:  width of the widget
        :param height: height of  the widget
        :param name: name of the widget
        :return: object
        """
        groupbox = QtGui.QGroupBox()
        if width != -1:
            groupbox.setFixedWidth(width)

        if height != -1:
            groupbox.setFixedHeight(height)

        if name != -1:
            groupbox.setTitle(name)

        groupbox.setStyleSheet(self.st.gbox)
        return groupbox

    def createlineedit(self, width, height, disable=-1, style=-1):
        line = QtGui.QLineEdit()

        if width != -1:
            line.setFixedWidth(width)

        if height != -1:
            line.setFixedHeight(height)

        if disable != -1:
            line.setDisabled(True)

        if style != -1:
            line.setStyleSheet(style)
        return line

    def createpushbutton(self, width=-1, height=-1, name=-1):
        button = QtGui.QPushButton()
        if width != -1:
            button.setFixedHeight(height)
        if height != -1:
            button.setFixedWidth(width)
        if name != -1:
            button.setText(name)

        return button

    def createcombobox(self, width=-1, height=-1, items=-1, default_item=-1):
        combo = QtGui.QComboBox()
        if width != -1:
            combo.setFixedWidth(width)

        if height != -1:
            combo.setFixedHeight(height)

        if items != -1:
            for i in range(len(items)):
                combo.addItem(str(items[i]))

        if default_item != -1:
            combo.setCurrentIndex(default_item)

        return combo

    def createTextEdit(self, width, height, editable, style):
        text = QtGui.QTextEdit()
        if width != -1:
            text.setFixedWidth(width)
        if height != -1:
            text.setFixedHeight(height)
        if editable != -1:
            text.setDisabled(True)
        if style != -1:
            text.setStyleSheet(style)

        return text

    def createRadioButton(self, text, flag):
        rb = QtGui.QRadioButton()
        rb.setText(text)
        rb.setFont(QtGui.QFont("Georgia", 12, QtGui.QFont.Bold))
        rb.setChecked(flag)
        return rb

    def getLabel(self, name, width, height):
        label = QtGui.QLabel()
        label.setText(name)
        label.setWordWrap(True)
        if width != -1:
            label.setFixedWidth(width)
        if height != -1:
            label.setFixedHeight(height)

        return label

    def getButton(self, name, width, height):
        btn = QtGui.QPushButton()
        btn.setStyleSheet(self.st.push_button)
        if width != -1:
            btn.setFixedWidth(width)
        if height != -1:
            btn.setFixedHeight(height)
        btn.setText(name)
        return btn

    def getLineEdit(self, flag, width, height):
        te = QtGui.QLineEdit()
        te.setEnabled(flag)
        if height != -1:
            te.setFixedHeight(height)
        if width != -1:
            te.setFixedWidth(width)
        return te

    def getFrame(self, style, width, height):
        frame = QtGui.QFrame()
        if width != -1:
            frame.setFixedWidth(width)

        if height != -1:
            frame.setFixedHeight(height)

        if style == "Sunken":
            frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        else:
            frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)

        frame.setLineWidth(1)
        frame.setMidLineWidth(1)
        return frame

    def getRadioButton(self, text, flag):
        rb = QtGui.QRadioButton()
        rb.setText(text)

        rb.setChecked(flag)
        return rb

    def getCheckBox(self, text):
        cb = QtGui.QCheckBox()
        cb.setText(text)

        return cb

    def getGroupBox(self, title, width, height):
        gb = QtGui.QGroupBox()
        gb.setTitle(title)
        gb.setStyleSheet(self.st.gbox)
        if width != -1:
            gb.setFixedWidth(width)
        if height != -1:
            gb.setFixedHeight(height)

        return gb

    def getComboBox(self, item_list, width=0, height=0):
        # print 'list length ', len(item_list), '  list ', item_list
        combo = QtGui.QComboBox()
        combo.setFixedHeight(height)
        combo.setFixedWidth(width)
        len1 = len(item_list)
        for i in range(len1):
            combo.addItem(str(item_list[i]))
        return combo

    def getLabel(self, title, width=0, height=0):
        label = QtGui.QLabel()
        label.setText(title)
        label.setFixedWidth(width)
        label.setFixedHeight(height)
        label.setWordWrap(True)
        return label
    
    def getLineEdit(self, active, width=0, height=0):
        line = QtGui.QLineEdit()
        line.setFixedHeight(height)
        line.setFixedWidth(width)
        line.setEnabled(active)
        return line


    def createVSpliter(self):
        splitter1 = QtGui.QSplitter()
        splitter1.setOrientation(QtCore.Qt.Vertical)
        return splitter1

    def createHSpliter(self):
        splitter1 = QtGui.QSplitter()
        splitter1.setOrientation(QtCore.Qt.Horizontal)





