
from iconify.core import QtCore, QtGui, QtSvg


def icon(path, color=None, anim=None):
    _pixmapGenerator = pixmapGenerator(path, color=color, anim=anim)
    _iconEngine = _IconEngine(_pixmapGenerator)
    return _Icon(_iconEngine, _pixmapGenerator)


def pixmapGenerator(path, color=None, anim=None):
    return _PixmapGenerator(path, color=color, anim=anim)


def setButtonIcon(button, icon):
    button.setIcon(icon)
    anim = icon.anim()
    if anim is not None:
        anim.tick.connect(button.update)


class _Icon(QtGui.QIcon):

    def __init__(self, iconEngine, pixmapGenerator):
        super(_Icon, self).__init__(iconEngine)
        self._pixmapGenerator = pixmapGenerator

    def pixmapGenerator(self):
        return self._pixmapGenerator

    def anim(self):
        return self._pixmapGenerator.anim()


class _IconEngine(QtGui.QIconEngine):

    def __init__(self, pixmapGenerator):
        super(_IconEngine, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def pixmap(self, size, mode, state):
        return self._pixmapGenerator.pixmap(size)


CACHE = {}


class _PixmapGenerator(QtCore.QObject):

    def __init__(self, path, color=None, anim=None, parent=None):

        self._path = path
        self._color = color
        self._anim = anim

        self._renderer = QtSvg.QSvgRenderer(self._path)

    def anim(self):
        return self._anim

    def pixmap(self, size):

        if self._anim:
            # print self._anim._frame
            key = (self._path, self._anim.__class__, self._anim._frame, size)
        else:
            key = (self._path, size)

        global CACHE

        if key in CACHE:
            return CACHE[key]

        image = QtGui.QImage(
            size,
            QtGui.QImage.Format_ARGB32_Premultiplied,
        )
        image.fill(QtCore.Qt.transparent)

        # Use the QSvgRenderer to draw the image
        painter = QtGui.QPainter(image)

        if self._anim:
            # Rotate the painter's co-ordinate space so
            # the image is correctly positioned.
            xfm = self._anim.transform(size)
            painter.setTransform(xfm)

        self._renderer.render(painter)
        painter.end()

        if self._color is not None:
            # Use the alpha channel on a solid colour image
            colorImage = QtGui.QImage(
                size,
                QtGui.QImage.Format_ARGB32_Premultiplied,
            )
            colorImage.fill(QtGui.QColor(self._color))
            colorImage.setAlphaChannel(image.alphaChannel())
            image = colorImage

        pixmap = QtGui.QPixmap.fromImage(image)

        CACHE[key] = pixmap

        return pixmap
