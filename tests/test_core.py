
import iconify
from iconify.qt import QtCore, QtGui, QtWidgets


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


def test_pixmapGenerator(validIconPath):
    iconPath = iconify.path.findIcon('delete')

    anim = iconify.anim.Spin()
    pixGen = iconify.core.pixmapGenerator(iconPath, color=QtGui.QColor('blue'), anim=anim)

    size = QtCore.QSize(24, 24)
    altSize = QtCore.QSize(32, 32)

    # Ensure that the pixmap generators cache is working as expected
    pixmapA = pixGen.pixmap(size)
    pixmapB = pixGen.pixmap(size)
    pixmapC = pixGen.pixmap(altSize)

    assert pixmapA is pixmapB
    assert pixmapA is not pixmapC
