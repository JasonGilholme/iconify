
from iconify.qt import QtCore, QtGui


class _GlobalTicker(QtCore.QObject):

    timeout = QtCore.Signal()

    _instance = None

    def __init__(self):
        # Note: No parent so it's owned by Qt
        super(_GlobalTicker, self).__init__()
        self._tick = QtCore.QTimer()
        self._tick.timeout.connect(self.timeout.emit)
        self._tick.setInterval(17)  # 60fps (ish)
        self._tick.start()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class BaseAnimation(QtCore.QObject):

    tick = QtCore.Signal()

    def __init__(self, parent=None):
        # type: (Optional[QtCore.QObject]) -> None
        super(BaseAnimation, self).__init__(parent=parent)
        self._minFrame = 0
        self._maxFrame = 100

        self._frame = self._minFrame
        self._active = False

    def transform(self, rect):
        return QtGui.QTransform()

    def start(self):
        _GlobalTicker.instance().timeout.connect(self._tick)
        self._active = True

    def stop(self):
        self.pause()
        self._frame = self._minFrame

    def pause(self):
        _GlobalTicker.instance().timeout.disconnect(self._tick)
        self._active = False

    def toggle(self):
        if self._active:
            self.pause()
        else:
            self.start()

    def frame(self):
        return self._frame

    def forceTick(self):
        self._tick()

    def incrementFrame(self):
        if self._frame == self._maxFrame:
            self._frame = self._minFrame
        else:
            self._frame += 1

    def _tick(self):
        self.incrementFrame()
        self.tick.emit()


class SingleShotMixin(object):

    def incrementFrame(self):
        if self._frame == self._maxFrame:
            self._frame = self._minFrame
            self.stop()
        else:
            self._frame += 1


class Spin(BaseAnimation):

    CLOCKWISE = 0
    ANTI_CLOCKWISE = 1

    def __init__(self, direction=CLOCKWISE):
        super(Spin, self).__init__()
        self._direction = direction
        self._maxFrame = 59

    def transform(self, size):
        halfSize = size / 2

        rotation = 6 if self._direction == Spin.CLOCKWISE else -6

        xfm = QtGui.QTransform()
        xfm = xfm.translate(halfSize.width(), halfSize.height())
        xfm = xfm.scale(0.8, 0.8)
        xfm = xfm.rotate(rotation * self._frame)
        xfm = xfm.translate(-halfSize.width(), -halfSize.height())

        return xfm


class SingleShotSpin(SingleShotMixin, Spin):
    pass


# class BreathingIconAnim(IconAnim):
#
#     def __init__(self, widget):
#         super(BreathingIconAnim, self).__init__(widget)
#
#         self._scale = 0.995
#
#     def transform(self, size):
#         halfSize = size / 2
#
#         xfm = QtGui.QTransform()
#         xfm = xfm.translate(halfSize.width(), halfSize.height())
#         if xfm.m11() >= 0.9:
#             self._scale = 0.995
#         elif xfm.m11() <= 0.7:
#             self._scale = 1.005
#
#         xfm = xfm.scale(self._scale, self._scale)
#         xfm = xfm.translate(-halfSize.height(), -halfSize.width())
#
#         return xfm
