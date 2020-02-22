
import os

import iconify
from iconify.qt import  QtCore, QtGui, QtWidgets


def test_icon(qtbot, validIconPath):

    anim = iconify.anim.Spin()
    icon = iconify.icon(
        'delete',
        color=QtGui.QColor('red'),
        anim=anim,
    )

    button = QtWidgets.QPushButton()
    button.setIcon(icon)
    button.clicked.connect(anim.toggle)

    button.show()

    qtbot.mouseClick(button, QtCore.Qt.LeftButton)
