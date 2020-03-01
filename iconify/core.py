"""
The primary objects for interfacing with iconify
"""

from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Tuple

from iconify.path import findIcon
from iconify.qt import QtCore, QtGui, QtSvg

if TYPE_CHECKING:
    from iconify.anim import BaseAnimation
    from iconify.qt import QtWidgets
    PixmapCacheKey = Tuple[Optional[str], QtCore.QSize, str, int, int]

_PIXMAP_CACHE = {}  # type: MutableMapping[PixmapCacheKey, QtGui.QPixmap]


class Icon(QtGui.QIcon):
    """
    The Iconify Icon which renders an svg image
    using the provided color & anim.
    """

    def __new__(
        cls,
        path,  # type: str
        color=None,  # type: Optional[QtGui.QColor]
        anim=None  # type: Optional[BaseAnimation]
    ):
        # type: (...) -> QtGui.QIcon
        """
        This returns a patched QtGui.QIcon object so that the QIcon has
        convenience functions for finding the animation and pixmap generator,
        but is also usable with Qt's model view framework.

        Parameters
        ----------
        path : str
        color : Optional[QtGui.QColor]
        anim : Optional[BaseAnimation]

        Returns
        -------
        QtGui.QIcon
        """
        pixmapGenerator = PixmapGenerator(path=path, color=color, anim=anim)
        iconEngine = _IconEngine(pixmapGenerator)
        icon = QtGui.QIcon(iconEngine)

        def _pixmapGenerator():
            # type: () -> PixmapGenerator
            return pixmapGenerator

        def _anim():
            # type: () -> Optional[BaseAnimation]
            return anim

        def _setAsButtonIcon(button):
            # type: (QtWidgets.QAbstractButton) -> None
            button.setIcon(icon)
            if anim is not None:
                anim.tick.connect(button.update)

        icon.pixmapGenerator = _pixmapGenerator
        icon.anim = _anim
        icon.setAsButtonIcon = _setAsButtonIcon

        return icon


class _IconEngine(QtGui.QIconEngine):
    """
    A QIconEngine which uses a PixmapGenerator for it's work.
    """

    def __init__(self, pixmapGenerator):
        # type: (PixmapGenerator) -> None
        super(_IconEngine, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def pixmap(self, size, mode, state):
        # type: (QtCore.QSize, Any, Any) -> QtGui.QPixmap
        return self._pixmapGenerator.pixmap(size)

    def paint(self, painter, rect, mode, state):
        # type: (QtCore.QPainter, QtCore.QRect, Any, Any) -> None
        painter.drawPixmap(
            rect.topLeft(), self.pixmap(rect.size(), mode, state)
        )


class PixmapGenerator(QtCore.QObject):
    """
    The PixmapGenerator is responsible for rendering the svg image and
    applying the transform from the animation during the process.

    It's backed by a cache to ensure that redundant rendering does not happen.
    """

    def __init__(
        self,
        path,  # type: str
        color=None,  # type: Optional[QtGui.QColor]
        anim=None,  # type: Optional[BaseAnimation]
        parent=None,  # type: Optional[QtCore.QObject]
    ):
        # type: (...) -> None
        super(PixmapGenerator, self).__init__(parent=parent)
        self._path = path
        self._color = None  # type: Optional[QtGui.QColor]
        self._anim = None  # type: Optional[BaseAnimation]

        self._renderer = QtSvg.QSvgRenderer(findIcon(self._path))

        self.setColor(color)
        self.setAnim(anim)

    def path(self):
        # type: () -> Optional[str]
        return self._path

    def color(self):
        # type: () -> Optional[QtGui.QColor]
        return self._color

    def setColor(self, color):
        # type: (Optional[QtGui.QColor]) -> None
        self._color = color

    def anim(self):
        # type: () -> Optional[BaseAnimation]
        """
        Return the animation used by this PixmapGenerator.

        Returns
        -------
        BaseAnimation
        """
        return self._anim

    def setAnim(self, anim):
        # type: (Optional[BaseAnimation]) -> None
        self._anim = anim

    def pixmap(self, size):
        # type: (QtCore.QSize) -> QtGui.QPixmap
        """
        Render the svg file, apply the color override and the animation
        transform and return it as a QPixmap.

        Parameters
        ----------
        size : QtCore.QSize

        Returns
        -------
        QtGui.QPixmap
        """
        color = self._color.rgb() if self._color else -1

        if self._anim is not None:
            key = (
                self._path, size, str(self._anim.__class__),
                self._anim.frame(), color
            )  # type: PixmapCacheKey
        else:
            key = (self._path, size, "", 0, color)

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
