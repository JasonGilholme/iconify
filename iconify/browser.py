"""
A browser for exploring the available images and possible options.
"""

import os
import sys

os.environ["ICONIFY_QTLIB"] = "PySide2"
os.environ["ICONIFY_PATH"] = os.path.dirname(__file__) + "/../examples/icons"

import iconify as ico
from iconify.qt import QtCore, QtGui, QtSvg, QtWidgets


class IconifyBrowser(QtWidgets.QMainWindow):

    def __init__(self):
        super(IconifyBrowser, self).__init__()

        self._pixmapGenerator = ico.PixmapGenerator()

        self._frame = QtWidgets.QFrame(self)

        self.setCentralWidget(self._frame)

        lyt = QtWidgets.QHBoxLayout(self)

        self._iconModel = IconModel(self)
        self._iconModel.setStringList(('delete', 'github'))
        self._iconView = QtWidgets.QListView(self)
        self._iconView.setUniformItemSizes(True)
        self._iconView.setViewMode(QtWidgets.QListView.IconMode)
        self._iconView.setGridSize(QtCore.QSize(80, 80))
        self._iconView.setIconSize(QtCore.QSize(48, 48))

        self._iconView.setModel(self._iconModel)

        sidePanel = QtWidgets.QFrame(self)
        sidePanel.setFixedWidth(200)

        sideLayout = QtWidgets.QVBoxLayout(sidePanel)

        self._previewLabel = Label(self._pixmapGenerator)
        self._previewLabel.setStyleSheet('border: 1px solid black')

        sideLayout.addWidget(self._previewLabel)

        sidePanel.setLayout(sideLayout)

        lyt.addWidget(self._iconView)
        lyt.addWidget(sidePanel)

        self._frame.setLayout(lyt)

        self._iconView.selectionModel().selectionChanged.connect(self._updateImage)

    def _updateImage(self):
        index = self._iconView.selectionModel().currentIndex()

        self._pixmapGenerator.setPath(index.data())

class IconModel(QtCore.QStringListModel):

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DecorationRole:
            return ico.Icon(self.data(index, role=QtCore.Qt.DisplayRole))
        return super(IconModel, self).data(index, role=role)


class Label(QtWidgets.QLabel):

    def __init__(self, pixmapGenerator=None):
        super(Label, self).__init__()
        self._pixmapGenerator = pixmapGenerator

    def setPixmapGenerator(self, pixmapGenerator):
        self._pixmapGenerator = pixmapGenerator
        self.update()

    def paintEvent(self, event):
        super(Label, self).paintEvent(event)

        if self._pixmapGenerator is None:
            return

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



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    browser = IconifyBrowser()
    browser.show()

    sys.exit(app.exec_())
