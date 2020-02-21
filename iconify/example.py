
import iconify as ico
from PySide2 import QtCore, QtGui, QtWidgets

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
buttonTwo.setIconSize(QtCore.QSize(32, 32))
buttonTwo.setFlat(True)
lyt.addWidget(buttonTwo)

buttonThree = QtWidgets.QPushButton()
buttonThree.setIconSize(QtCore.QSize(64, 64))
buttonThree.setFlat(True)
lyt.addWidget(buttonThree)

frame.setLayout(lyt)
frame.show()


# Apply iconify icons
spinnerSvg = "/Users/jasong/Code/iconify/spinner.svg"
deleteSvg = "/Users/jasong/Code/iconify/delete.svg"

spinningAnim = ico.anim.SpinningIconAnim()

spinnerIcon = ico.icon(spinnerSvg, QtGui.QColor.fromHsv(0, 0, 150), anim=spinningAnim)
deleteIcon = ico.icon(deleteSvg, QtGui.QColor.fromHsv(5, 200, 200))

buttonOne.setIcon(deleteIcon)
buttonOne.clicked.connect(spinningAnim.toggle)

buttonTwo.setIcon(spinnerIcon)
spinningAnim.tick.connect(buttonTwo.update)

buttonThree.setIcon(spinnerIcon)
spinningAnim.tick.connect(buttonThree.update)


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


label = Label(spinnerIcon.pixmapGenerator())
lyt.addWidget(label)

import sys
sys.exit(app.exec_())
