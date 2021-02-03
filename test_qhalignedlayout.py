#!/usr/bin/env python
import sys
import random
import string

from qhalignedlayout import *

from PySide2 import QtCore, QtGui, QtWidgets

def random_string():
    return "".join(
        random.choice(string.ascii_lowercase + " ")
        for _ in
        range(random.randint(1, 20))
    )

class BorderedWidget(QtWidgets.QWidget):
    def __init__(self, widg):
        super(BorderedWidget, self).__init__(parent=widg.parent())
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(widg)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    #"""
    def paintEvent(self, event):
        super(BorderedWidget, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.drawRect(0, 0, self.geometry().width() - 1, self.geometry().height() - 1)
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)
        painter.drawText(self.geometry().width() - 50, 10, "{}x{}".format(self.geometry().width(), self.geometry().height()))
    #"""


class SpecialWidget(QtWidgets.QWidget):
    def __init__(self, group, *args, **kwargs):
        super(SpecialWidget, self).__init__(*args, **kwargs)

        layout = QHAlignedLayout(group)
        self.setLayout(layout)

        layout.addWidget(BorderedWidget(QtWidgets.QLabel(random_string(), self)))
        layout.addWidget(BorderedWidget(QtWidgets.QLabel(random_string(), self)))
        butt = BorderedWidget(QtWidgets.QPushButton(random_string(), self))
        layout.addWidget(butt)
        before = layout.count()
        butt.setVisible(random.randint(0, 1))
        layout.addWidget(BorderedWidget(QtWidgets.QLabel(random_string(), self)))

        layout.setStretch(0, 1)


class TestQAL(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(TestQAL, self).__init__(*args, **kwargs)

        group = QHAlignedLayoutGroup(self)

        layout = QtWidgets.QVBoxLayout()

        self.setLayout(layout)

        self.make_group()

        for i in range(10):
            sw = SpecialWidget(group, self)
            self.group_box.layout().addWidget(BorderedWidget(sw))

            if random.randint(0, 1):
                self.make_group()
        layout.addStretch()

    def make_group(self):
        self.group_box = QtWidgets.QGroupBox(self)
        self.group_box.setTitle(random_string())
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.group_box.setLayout(layout)
        self.layout().addWidget(self.group_box)

if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)

    window = TestQAL()
    window.setVisible(True)

    sys.exit(qapp.exec_())

