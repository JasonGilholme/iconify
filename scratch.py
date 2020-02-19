

from PySide2 import QtCore, QtGui, QtWidgets, QtSvg

import attr
from typing import *

# TODO: Concatenation of animations


class IconAnim(object):

    def __init__(self, widget):
        # type: (QtWidgets.QAbstractButton) -> None
        self._widget = widget
        self._xfm = QtGui.QTransform()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.tick)
        self._timer.setInterval(10)
        self._timer.start()

        self._transform = self.initTransform()

    def initTransform(self):
        return QtGui.QTransform()

    def widget(self):
        return self._widget

    def transform(self):
        return self._transform

    def tick(self):
        self._transform = self.calculateTransform(self._transform)
        self._widget.update()

    def calculateTransform(self, currentTransform):
        return currentTransform


class SpinningIconAnim(IconAnim):

    def initTransform(self):
        halfSize = self._widget.iconSize() / 2
        xfm = QtGui.QTransform()
        xfm = xfm.translate(halfSize.width(), halfSize.height())
        xfm = xfm.scale(0.8, 0.8)
        xfm = xfm.translate(-halfSize.height(), -halfSize.width())
        return xfm

    def calculateTransform(self, xfm):
        halfSize = self._widget.iconSize() / 2

        xfm = xfm.translate(halfSize.width(), halfSize.height())
        xfm = xfm.rotate(-5)
        xfm = xfm.translate(-halfSize.height(), -halfSize.width())

        return xfm


class BreathingIconAnim(IconAnim):

    def __init__(self, widget):
        super(BreathingIconAnim, self).__init__(widget)

        self._scale = 0.995

    def calculateTransform(self, xfm):
        halfSize = self._widget.iconSize() / 2

        xfm = xfm.translate(halfSize.width(), halfSize.height())
        if xfm.m11() >= 0.9:
            self._scale = 0.995
        elif xfm.m11() <= 0.7:
            self._scale = 1.005

        xfm = xfm.scale(self._scale, self._scale)
        xfm = xfm.translate(-halfSize.height(), -halfSize.width())

        return xfm


@attr.s
class IconOptions(object):

    # TODO: converter to take 'foo/bar' and expand it to an absolute path based on what's found ont he path.
    path = attr.ib(type=str)
    color = attr.ib(type=QtGui.QColor)
    animation = attr.ib(type=Optional[IconAnim])


class IconEngine(QtGui.QIconEngine):

    def __init__(self, filepath, colour, animation=None):
        super(IconEngine, self).__init__()

        self._renderer = QtSvg.QSvgRenderer(filepath)
        self._colour = colour
        self._animation = animation

    def pixmap(self, size, mode, state):
        alphaImage = QtGui.QImage(size,
                                  QtGui.QImage.Format_ARGB32_Premultiplied)
        alphaImage.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(alphaImage)

        if self._animation:
            xfm = self._animation.transform()
            painter.setTransform(xfm)

        self._renderer.render(painter)

        painter.end()

        # Use the alpha channel on a solid colour image
        colorImage = QtGui.QImage(size,
                                  QtGui.QImage.Format_ARGB32_Premultiplied)
        colorImage.fill(QtGui.QColor(self._colour))
        colorImage.setAlphaChannel(alphaImage.alphaChannel())

        return QtGui.QPixmap.fromImage(colorImage)


def setIcon(widget, iconPath, colour, animation=None):
    if animation is not None:
        animation = animation(widget)
    engine = IconEngine(iconPath, colour, animation=animation)
    icon = QtGui.QIcon(engine)
    widget.setIcon(icon)
    return icon


app = QtWidgets.QApplication([])

frame = QtWidgets.QFrame()
frame.setStyleSheet('background-color: hsv(0, 0, 220)')

lyt = QtWidgets.QVBoxLayout()

button = QtWidgets.QPushButton()
button.setIconSize(QtCore.QSize(64, 64))
button.setFlat(True)
lyt.addWidget(button)

f = "/Users/jasong/Code/iconify/spinner.svg"
setIcon(button, f, QtGui.QColor(85, 85, 85, 255), animation=SpinningIconAnim)


button2 = QtWidgets.QPushButton()
button2.setIconSize(QtCore.QSize(64, 64))
lyt.addWidget(button2)
button2.setFlat(True)

f = "/Users/jasong/Code/iconify/delete.svg"
setIcon(button2, f, QtGui.QColor(200, 25, 25, 200), animation=BreathingIconAnim)


frame.setLayout(lyt)
frame.show()

import sys
sys.exit(app.exec_())

