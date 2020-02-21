
import iconify as ico
from PySide2 import QtCore, QtGui, QtWidgets

app = QtWidgets.QApplication([])



frame = QtWidgets.QFrame()
frame.setStyleSheet('background-color: hsv(0, 0, 220)')

lyt = QtWidgets.QVBoxLayout()

button = QtWidgets.QPushButton()
button.setIconSize(QtCore.QSize(64, 64))
button.setFlat(True)
lyt.addWidget(button)

f = "/Users/jasong/Code/iconify/spinner.svg"
anim = ico.anim.SpinningIconAnim()


icon = ico.icon(f, QtGui.QColor(145, 85, 85, 255), anim=anim)

button.setIcon(icon)
anim.tick.connect(button.update)


button = QtWidgets.QPushButton()
button.setIconSize(QtCore.QSize(32, 32))
button.setFlat(True)
lyt.addWidget(button)



button.setIcon(icon)
anim.tick.connect(button.update)



button2 = QtWidgets.QPushButton()
button2.setIconSize(QtCore.QSize(64, 64))
lyt.addWidget(button2)
button2.setFlat(True)

button2.clicked.connect(anim.toggle)

f = "/Users/jasong/Code/iconify/delete.svg"
icon = ico.icon(f, QtGui.QColor(25, 25, 200, 200), anim=anim)
button2.setIcon(icon)

anim.tick.connect(button2.update)

frame.setLayout(lyt)
frame.show()

import sys
sys.exit(app.exec_())
