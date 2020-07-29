
import os

import pydoc

os.environ["ICONIFY_PATH"] = os.path.dirname(__file__) + "/icons"

qtlib = os.environ.get("ICONIFY_QTLIB", "PySide2")
QtCore = pydoc.locate(qtlib + '.QtCore')
QtGui = pydoc.locate(qtlib + '.QtGui')
QtWidgets = pydoc.locate(qtlib + '.QtWidgets')


import iconify as ico


app = QtWidgets.QApplication([])

# Create some Qt buttons
frame = QtWidgets.QFrame()
frame.setStyleSheet('background-color: hsv(0, 0, 65)')

lyt = QtWidgets.QVBoxLayout()

buttonOne = QtWidgets.QPushButton()
buttonOne.setIconSize(QtCore.QSize(24, 24))
buttonOne.setFlat(True)
lyt.addWidget(buttonOne)

buttonTwo = QtWidgets.QPushButton()
buttonTwo.setIconSize(QtCore.QSize(64, 64))
buttonTwo.setFlat(True)
lyt.addWidget(buttonTwo)

buttonThree = QtWidgets.QPushButton()
buttonThree.setIconSize(QtCore.QSize(96, 96))
buttonThree.setFlat(True)
lyt.addWidget(buttonThree)

frame.setLayout(lyt)
frame.show()


# Apply iconify icons
spinnerSvg = "github"
spinnerTwoSvg = "spinners:colored"
deleteSvg = "delete"

clockwiseSpinningAnim = ico.anim.Spin(direction=ico.anim.Spin.Directions.CLOCKWISE)
antiClockwiseSpinningAnim = ico.anim.Spin() + ico.anim.Breathe()


spinnerIcon = ico.Icon(spinnerSvg, color=QtGui.QColor.fromHsv(65, 200, 200), anim=clockwiseSpinningAnim)
spinnerIconTwo = ico.Icon(spinnerTwoSvg, anim=clockwiseSpinningAnim)
spinnerIconTwoAlt = ico.Icon(spinnerTwoSvg, color=QtGui.QColor.fromHsv(300, 150, 200), anim=antiClockwiseSpinningAnim)
deleteIcon = ico.Icon(deleteSvg, color=QtGui.QColor.fromHsv(5, 200, 200))

buttonOne.setIcon(deleteIcon)
buttonOne.clicked.connect(clockwiseSpinningAnim.toggle)
buttonOne.clicked.connect(antiClockwiseSpinningAnim.toggle)

spinnerIcon.setAsButtonIcon(buttonTwo)
spinnerIconTwo.setAsButtonIcon(buttonThree)


#
# Pixmap Example
#
class Label(QtWidgets.QLabel):

    def __init__(self, pixmapGenerator):
        super(Label, self).__init__()
        self._pixmapGenerator = pixmapGenerator

        self._pixmapGenerator.anim().tick.connect(self.update)

    def paintEvent(self, event):
        super(Label, self).paintEvent(event)

        rect = event.rect()

        if rect.width() > rect.height():
            size = QtCore.QSize(rect.height(), rect.height())
        else:
            size = QtCore.QSize(rect.width(), rect.width())

        pixmap = self._pixmapGenerator.pixmap(size)

        painter = QtGui.QPainter(self)
        halfSize  = size / 2
        point = rect.center() - QtCore.QPoint(halfSize.width(), halfSize.height())
        painter.drawPixmap(point, pixmap)
        painter.end()


label = Label(spinnerIconTwoAlt.pixmapGenerator())
lyt.addWidget(label)

import sys
sys.exit(app.exec_())
