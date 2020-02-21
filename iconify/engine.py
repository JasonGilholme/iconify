
import attr
from typing import *

from PySide2 import QtCore, QtGui, QtSvg


def icon(path, color, anim=None):
    _pixmapGenerator = pixmapGenerator(path, color, anim=anim)
    _iconEngine = _IconEngine(_pixmapGenerator)
    return _Icon(_iconEngine, _pixmapGenerator)


def pixmapGenerator(path, color, anim=None):
    return _PixmapGenerator(path, color, anim=anim)


class _Icon(QtGui.QIcon):

    def __init__(self, iconEngine, pixmapGenerator):
        super(_Icon, self).__init__(iconEngine)
        self._pixmapGenerator = pixmapGenerator

    def pixmapGenerator(self):
        return self._pixmapGenerator


class _IconEngine(QtGui.QIconEngine):

    def __init__(self, pixmapGenerator):
        super(_IconEngine, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def pixmap(self, size, mode, state):
        return self._pixmapGenerator.pixmap(size)


class _PixmapGenerator(QtCore.QObject):

    def __init__(self, path, color, anim=None, parent=None):

        self._path = path
        self._color = color
        self._anim = anim

        self._renderer = QtSvg.QSvgRenderer(self._path)

    def anim(self):
        return self._anim

    def pixmap(self, size):
        alphaImage = QtGui.QImage(size,
                                  QtGui.QImage.Format_ARGB32_Premultiplied)
        alphaImage.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(alphaImage)

        if self._anim:
            xfm = self._anim.transform(size)
            painter.setTransform(xfm)

        self._renderer.render(painter)

        painter.end()

        # Use the alpha channel on a solid colour image
        colorImage = QtGui.QImage(size,
                                  QtGui.QImage.Format_ARGB32_Premultiplied)
        colorImage.fill(QtGui.QColor(self._color))
        colorImage.setAlphaChannel(alphaImage.alphaChannel())

        return QtGui.QPixmap.fromImage(colorImage)
