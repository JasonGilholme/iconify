
from iconify.core import QtCore, QtGui


class AbstractAnimation(QtCore.QObject):

    tick = QtCore.Signal()

    def __init__(self):
        # type: () -> None
        super(AbstractAnimation, self).__init__()
        self._frame = 0

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.setInterval(16)  # 60 fps

    def start(self):
        self._timer.start()

    def stop(self):
        self._frame = 0
        self._timer.stop()

    def pause(self):
        self._timer.stop()

    def toggle(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()

    def _tick(self):
        self._frame += 1
        self.tick.emit()

    def transform(self, rect):
        return QtGui.QTransform()


class SpinningIconAnim(AbstractAnimation):

    CLOCKWISE = 0
    ANTI_CLOCKWISE = 1

    def __init__(self, direction=CLOCKWISE):
        super(SpinningIconAnim, self).__init__()
        self._direction = direction

    def transform(self, size):
        halfSize = size / 2

        rotation = 6 if self._direction == SpinningIconAnim.CLOCKWISE else -6

        xfm = QtGui.QTransform()
        xfm = xfm.translate(halfSize.width(), halfSize.height())
        xfm = xfm.scale(0.8, 0.8)
        xfm = xfm.rotate(rotation * self._frame)
        xfm = xfm.translate(-halfSize.width(), -halfSize.height())

        if self._frame >= 59:
            self._frame = -1

        return xfm


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
