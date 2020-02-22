
from typing import TYPE_CHECKING

from iconify.qt import QtCore, QtGui, QtSvg
from iconify.path import findIcon

if TYPE_CHECKING:
    from typing import *
    from iconify.anim import BaseAnimation
    from iconify.qt import QtWidgets
    PixmapCacheKey = Tuple[str, QtCore.QSize, Optional[Type[BaseAnimation]], Optional[int]]


_PIXMAP_CACHE = {}  # type: MutableMapping[PixmapCacheKey, QtGui.QPixmap]


def icon(path, color=None, anim=None):
    # type: (str, Optional[QtGui.QColor], Optional[BaseAnimation]) -> _Icon
    _pixmapGenerator = pixmapGenerator(path, color=color, anim=anim)
    _iconEngine = _IconEngine(_pixmapGenerator)
    return _Icon(_iconEngine, _pixmapGenerator)


def pixmapGenerator(path, color=None, anim=None):
    # type: (str, Optional[QtGui.QColor], Optional[BaseAnimation]) -> _Icon
    path = findIcon(path)
    return _PixmapGenerator(path, color=color, anim=anim)


def setButtonIcon(button, icon):
    # type: (QtWidgets.QAbstractButton, _Icon) -> None
    button.setIcon(icon)
    anim = icon.anim()
    if anim is not None:
        anim.tick.connect(button.update)


class _Icon(QtGui.QIcon):

    def __init__(self, iconEngine, pixmapGenerator):
        # type: (_IconEngine, _PixmapGenerator) -> None
        super(_Icon, self).__init__(iconEngine)
        self._pixmapGenerator = pixmapGenerator

    def pixmapGenerator(self):
        # type: () -> _PixmapGenerator
        return self._pixmapGenerator

    def anim(self):
        # type: () -> Optional[BaseAnimation]
        return self._pixmapGenerator.anim()


class _IconEngine(QtGui.QIconEngine):

    def __init__(self, pixmapGenerator):
        # type: (_PixmapGenerator) -> None
        super(_IconEngine, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def pixmap(self, size, mode, state):
        # type: (QtCore.QSize, Any, Any) -> QtGui.QPixmap
        return self._pixmapGenerator.pixmap(size)


class _PixmapGenerator(QtCore.QObject):

    def __init__(self, path, color=None, anim=None, parent=None):
        # type: (str, Optional[QtGui.QColor], Optional[BaseAnimation], Optional[QtCore.QObject]) -> None
        super(_PixmapGenerator, self).__init__(parent=parent)
        self._path = path
        self._color = color
        self._anim = anim

        self._renderer = QtSvg.QSvgRenderer(self._path)

    def anim(self):
        # type: () -> Optional[BaseAnimation]
        return self._anim

    def pixmap(self, size):
        # type: (QtCore.QSize) -> QtGui.QPixmap
        if self._anim is not None:
            key = (self._path, size, self._anim.__class__, self._anim._frame)  # type: PixmapCacheKey
        else:
            key = (self._path, size, None, None)

        if key in _PIXMAP_CACHE:
            return _PIXMAP_CACHE[key]

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
        _PIXMAP_CACHE[key] = pixmap
        return pixmap
