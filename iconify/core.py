from typing import TYPE_CHECKING

from iconify.path import findIcon
from iconify.qt import QtCore, QtGui, QtSvg

if TYPE_CHECKING:
    from typing import *
    from iconify.anim import BaseAnimation
    from iconify.qt import QtWidgets
    PixmapCacheKey = Tuple[str, QtCore.QSize, Optional[Type[BaseAnimation]],
                           Optional[int]]

_PIXMAP_CACHE = {}  # type: MutableMapping[PixmapCacheKey, QtGui.QPixmap]


class Icon(QtGui.QIcon):

    def __init__(self, path, color=None, anim=None):
        # type: (str, Optional[QtGui.QColor], Optional[BaseAnimation]) -> None
        _pixmapGenerator = PixmapGenerator(path, color=color, anim=anim)
        _iconEngine = _IconEngine(_pixmapGenerator)

        super(Icon, self).__init__(_iconEngine)
        self._pixmapGenerator = _pixmapGenerator

    def setAsButtonIcon(self, button):
        # type: (QtWidgets.QAbstractButton) -> None
        button.setIcon(self)
        anim = self.anim()
        if anim is not None:
            anim.tick.connect(button.update)

    def pixmapGenerator(self):
        # type: () -> PixmapGenerator
        return self._pixmapGenerator

    def anim(self):
        # type: () -> Optional[BaseAnimation]
        return self._pixmapGenerator.anim()


class _IconEngine(QtGui.QIconEngine):

    def __init__(self, pixmapGenerator):
        # type: (PixmapGenerator) -> None
        super(_IconEngine, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def pixmap(self, size, mode, state):
        # type: (QtCore.QSize, Any, Any) -> QtGui.QPixmap
        return self._pixmapGenerator.pixmap(size)


class PixmapGenerator(QtCore.QObject):

    def __init__(self, path, color=None, anim=None, parent=None):
        # type: (str, Optional[QtGui.QColor], Optional[BaseAnimation], Optional[QtCore.QObject]) -> None
        super(PixmapGenerator, self).__init__(parent=parent)
        self._path = findIcon(path)
        self._color = color
        self._anim = anim

        self._renderer = QtSvg.QSvgRenderer(self._path)

    def anim(self):
        # type: () -> Optional[BaseAnimation]
        return self._anim

    def pixmap(self, size):
        # type: (QtCore.QSize) -> QtGui.QPixmap
        if self._anim is not None:
            key = (
                self._path, size, self._anim.__class__, self._anim._frame
            )  # type: PixmapCacheKey
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
