"""
The animation objects for iconify
"""

from enum import Enum
from typing import TYPE_CHECKING

from iconify.qt import QtCore, QtGui

if TYPE_CHECKING:
    from typing import *


class GlobalTick(QtCore.QObject):
    """
    A singleton timer used to trigger all animation objects created by iconify
    """

    timeout = QtCore.Signal()

    _instance = None  # type: Optional[GlobalTick]

    def __init__(self):
        # type: () -> None
        # Note: No parent so it's owned by Qt
        super(GlobalTick, self).__init__()
        self._tick = QtCore.QTimer()
        self._tick.timeout.connect(self.timeout.emit)
        self._tick.setInterval(17)  # 60fps (ish)
        self._tick.start()

    @classmethod
    def instance(cls):
        # type: () -> GlobalTick
        """
        Return the global instance of the ticker.

        Returns
        -------
        GlobalTick
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class BaseAnimation(QtCore.QObject):
    """
    The base class that should be used for all animations.
    """

    # Emitted when the animation steps
    tick = QtCore.Signal()

    _minFrame = 0
    _maxFrame = 100

    def __init__(self, parent=None):
        # type: (Optional[QtCore.QObject]) -> None
        super(BaseAnimation, self).__init__(parent=parent)
        self._frame = self._minFrame
        self._active = False

    def transform(self, rect):
        # type: (QtCore.QRect) -> QtGui.QTransform
        """
        Return a QtGui.QTransform for the current frame that will be used
        when drawing an image in the provided QRect.

        Parameters
        ----------
        rect : QtCore.QRect

        Returns
        -------
        QtGui.QTransform
        """
        return QtGui.QTransform()

    def start(self):
        # type: () -> None
        """
        Start the animation.
        """
        GlobalTick.instance().timeout.connect(self._tick)
        self._active = True

    def stop(self):
        # type: () -> None
        """
        Stop the animation and reset the current frame back to the start.
        """
        self.pause()
        self._frame = self._minFrame

    def pause(self):
        # type: () -> None
        """
        Stop the animation and maintain the current frame
        """
        GlobalTick.instance().timeout.disconnect(self._tick)
        self._active = False

    def toggle(self):
        # type: () -> None
        """
        Start or stop the animation based on it's current state.
        """
        if self.active():
            self.pause()
        else:
            self.start()

    def active(self):
        # type: () -> bool
        """
        Indicate if the animation is currently playing.

        Returns
        -------
        bool
        """
        return self._active

    def frame(self):
        # type: () -> int
        """
        Return the current frame of the animation.

        Returns
        -------
        int
        """
        return self._frame

    def forceTick(self):
        # type: () -> None
        """
        Manually increment the current frame.
        """
        self._tick()

    def incrementFrame(self):
        # type: () -> None
        """
        Called when the animation is ticked allowing subclasses to provide
        custom frame step logic e.g. single shot animations.
        """
        if self._frame == self._maxFrame:
            self._frame = self._minFrame
        else:
            self._frame += 1

    def _tick(self):
        # type: () -> None
        self.incrementFrame()
        self.tick.emit()


class SingleShotMixin(object):
    """
    A mixin that overrides the incrementFrame logic so the
    animation loops once and then stops itself.
    """

    def incrementFrame(self):  # type: ignore[misc]
        # type: (BaseAnimation) -> None
        if self._frame == self._maxFrame:
            self._frame = self._minFrame
            self.stop()
        else:
            self._frame += 1


class Spin(BaseAnimation):
    """
    A simple spinning animation
    """

    _maxFrame = 59

    class Directions(Enum):

        CLOCKWISE = 0
        ANTI_CLOCKWISE = 1

    def __init__(self, direction=Directions.CLOCKWISE):
        # type: (Spin.Directions) -> None
        super(Spin, self).__init__()
        self._direction = direction

    def transform(self, size):
        # type: (QtCore.QSize) -> QtGui.QTransform
        halfSize = size / 2

        rotation = 6 if self._direction == Spin.Directions.CLOCKWISE else -6

        xfm = QtGui.QTransform()
        xfm = xfm.translate(halfSize.width(), halfSize.height())
        xfm = xfm.scale(0.8, 0.8)
        xfm = xfm.rotate(rotation * self._frame)
        xfm = xfm.translate(-halfSize.width(), -halfSize.height())

        return xfm


class SingleShotSpin(SingleShotMixin, Spin):
    """
    A single shot spinning animation
    """


#
# def parametricEase(t):
#     sqt = t * t
#     return sqt / (2.0 * (sqt - t) + 1.0)
#
#
# class Breathe(BaseAnimation):
#
#     _maxFrame = 30
#
#     keyframes = (
#         (0, 0.65),
#         (25, 0.9),
#         (60, 0.85),
#         (100, 0.65),
#     )
#
#     def transform(self, size):
#
#         currFrame = self.frame()
#         prevKey = None
#         nextKey = None
#         scale = None
#
#         for frame, value in keyFrames:
#             if frame == currFrame:
#                 scale = value
#                 break
#
#
#
#
#         t = float(self._frame) / self._maxFrame
#         m = parametricEase(t)
#
#         scale = 0.7 + (0.2 * m)
#
#         print(scale)
#
#         halfSize = size / 2
#
#         xfm = QtGui.QTransform()
#         xfm = xfm.translate(halfSize.width(), halfSize.height())
#
#         xfm = xfm.scale(scale, scale)
#         xfm = xfm.translate(-halfSize.height(), -halfSize.width())
#
#         return xfm
