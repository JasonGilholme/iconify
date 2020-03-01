"""
A browser for exploring the available images and possible options.
"""

import os
import sys
from typing import Any, NoReturn, Optional

import iconify as ico
from iconify.qt import QtCore, QtGui, QtWidgets

VIEW_COLUMNS = 5
AUTO_SEARCH_TIMEOUT = 500
ALL_COLLECTIONS = 'All'
NO_COLOR = 'No Color'
NO_ANIM = 'No Anim'


class Browser(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        # type: (Optional[QtWidgets.QWidget]) -> None
        super(Browser, self).__init__(parent=parent)
        self.setMinimumSize(1024, 576)
        self.setWindowTitle('Iconify Browser')

        self._currentIcon = None
        self._currentAnim = None
        self._currentColor = None

        iconNames = ico.path.listIcons()

        self._filterTimer = QtCore.QTimer(self)
        self._filterTimer.setSingleShot(True)
        self._filterTimer.setInterval(AUTO_SEARCH_TIMEOUT)
        self._filterTimer.timeout.connect(self._updateFilter)

        model = Model()
        model.setStringList(sorted(iconNames))

        self._proxyModel = QtCore.QSortFilterProxyModel()
        self._proxyModel.setSourceModel(model)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._listView = View(self)
        self._listView.setUniformItemSizes(True)
        self._listView.setViewMode(QtWidgets.QListView.IconMode)
        self._listView.setModel(self._proxyModel)
        self._listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._listView.doubleClicked.connect(self._copyIconText)
        self._listView.selectionModel().currentChanged.connect(self._selectionChanged)

        self._lineEdit = QtWidgets.QLineEdit(self)
        self._lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self._lineEdit.textChanged.connect(self._triggerDelayedUpdate)
        self._lineEdit.returnPressed.connect(self._triggerImmediateUpdate)

        collections = []
        for iconName in iconNames:
            if ':' not in iconName:
                continue
            collections.append(iconName.split(':', 1)[0])
        collections = sorted(set(collections))

        self._collectionsCombo = QtWidgets.QComboBox(self)
        self._collectionsCombo.addItems([ALL_COLLECTIONS] + collections)
        self._collectionsCombo.currentIndexChanged.connect(self._triggerImmediateUpdate)

        lyt = QtWidgets.QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(self._collectionsCombo)
        lyt.addWidget(self._lineEdit)

        searchBarFrame = QtWidgets.QFrame(self)
        searchBarFrame.setLayout(lyt)

        self._copyButton = QtWidgets.QPushButton('Copy Name', self)
        self._copyButton.clicked.connect(self._copyIconText)

        lyt = QtWidgets.QVBoxLayout()
        lyt.addWidget(searchBarFrame)
        lyt.addWidget(self._listView)
        lyt.addWidget(self._copyButton)

        iconFrame = QtWidgets.QFrame(self)
        iconFrame.setLayout(lyt)

        lyt = QtWidgets.QVBoxLayout()

        self._previewImage = PixmapGeneratorLabel()
        self._previewImage.setFixedSize(QtCore.QSize(200, 200))

        self._animCombo = QtWidgets.QComboBox(self)
        self._animCombo.addItems((NO_ANIM, 'Spin', 'Breathe'))
        self._animCombo.currentIndexChanged.connect(self._animChanged)

        self._colorCombo = QtWidgets.QComboBox(self)
        self._colorCombo.addItems([NO_COLOR] + sorted(QtGui.QColor.colorNames()))
        self._colorCombo.currentIndexChanged.connect(self._colorChanged)

        self._previewFrame = QtWidgets.QFrame(self)
        self._previewFrame.setFixedWidth(200)

        lyt.addWidget(self._previewImage)
        lyt.addWidget(self._animCombo)
        lyt.addWidget(self._colorCombo)
        lyt.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self._previewFrame.setLayout(lyt)

        lyt = QtWidgets.QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(iconFrame)
        lyt.addWidget(self._previewFrame)

        centralFrame = QtWidgets.QFrame(self)
        centralFrame.setLayout(lyt)
        self.setCentralWidget(centralFrame)

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Return),
            self,
            self._copyIconText,
        )

        self._lineEdit.setFocus()

        geo = self.geometry()
        desktop = QtWidgets.QApplication.desktop()
        screen = desktop.screenNumber(desktop.cursor().pos())
        centerPoint = desktop.screenGeometry(screen).center()
        geo.moveCenter(centerPoint)
        self.setGeometry(geo)

    def _selectionChanged(self, currentIndex, previousIndex):
        currentIcon = currentIndex.data()
        self._currentIcon = currentIcon
        self._updatePixmapGenerator()

    def _animChanged(self):
        currentAnim = self._animCombo.currentText()
        if currentAnim == NO_ANIM:
            self._currentAnim = None
        else:
            self._currentAnim = getattr(ico.anim, currentAnim)()
            self._currentAnim.start()
        self._updatePixmapGenerator()

    def _colorChanged(self):
        currentColor = self._colorCombo.currentText()
        if currentColor == NO_COLOR:
            self._currentColor = None
        else:
            self._currentColor = QtGui.QColor(currentColor)
        self._updatePixmapGenerator()

    def _updatePixmapGenerator(self):
        if self._currentIcon is None:
            pixmapGenerator = None
        else:
            pixmapGenerator = ico.PixmapGenerator(self._currentIcon, self._currentColor, self._currentAnim)

        self._previewImage.setPixmapGenerator(pixmapGenerator)

    def _updateFilter(self):
        # type: () -> None
        """
        Update the string used for filtering in the proxy model with the
        current text from the line edit.
        """
        reString = ""

        group = self._collectionsCombo.currentText()
        if group != ALL_COLLECTIONS:
            reString += "^%s:" % group

        searchTerm = self._lineEdit.text()
        if searchTerm:
            reString += ".*%s.*$" % searchTerm

        self._proxyModel.setFilterRegExp(reString)

    def _triggerDelayedUpdate(self):
        # type: () -> None
        """
        Reset the timer used for committing the search term to the proxy model.
        """
        self._filterTimer.stop()
        self._filterTimer.start()

    def _triggerImmediateUpdate(self):
        # type: () -> None
        """
        Stop the timer used for committing the search term and update the
        proxy model immediately.
        """
        self._filterTimer.stop()
        self._updateFilter()

    def _copyIconText(self):
        # type: () -> None
        """
        Copy the name of the currently selected icon to the clipboard.
        """
        indexes = self._listView.selectedIndexes()
        if not indexes:
            return

        clipboard = QtWidgets.QApplication.instance().clipboard()
        clipboard.setText(indexes[0].data())


class View(QtWidgets.QListView):
    """
    A QListView that scales it's grid size to ensure the same number of
    columns are always drawn.
    """

    def __init__(self, parent=None):
        # type: (Optional[QtWidgets.QWidget]) -> None
        super(View, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def resizeEvent(self, event):
        # type: (QtCore.QEvent) -> bool
        """
        Re-implemented to re-calculate the grid size to provide scaling icons

        Parameters
        ----------
        event : QtCore.QEvent
        """
        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tileWidth = width / VIEW_COLUMNS
        iconWidth = int(tileWidth * 0.8)

        self.setGridSize(QtCore.QSize(tileWidth, tileWidth))
        self.setIconSize(QtCore.QSize(iconWidth, iconWidth))

        return super(View, self).resizeEvent(event)


class Model(QtCore.QStringListModel):

    def flags(self, index):
        # type: (QtCore.QModelIndex) -> QtCore.QItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        # type: (QtCore.QModelIndex, QtCore.Qt.ItemRole) -> Any
        """
        Re-implemented to return the icon for the current index.

        Parameters
        ----------
        index : QtCore.QModelIndex
        role : int

        Returns
        -------
        Any
        """
        if role == QtCore.Qt.DecorationRole:
            iconString = self.data(index, role=QtCore.Qt.DisplayRole)
            return ico.Icon(iconString)
        return super(Model, self).data(index, role)


class PixmapGeneratorLabel(QtWidgets.QLabel):

    def __init__(self, pixmapGenerator=None):
        super(PixmapGeneratorLabel, self).__init__()
        self._pixmapGenerator = None
        self.setPixmapGenerator(pixmapGenerator)

    def setPixmapGenerator(self, pixmapGenerator):
        if self._pixmapGenerator:
            anim = self._pixmapGenerator.anim()
            if anim:
                anim.tick.disconnect(self.update)

        self._pixmapGenerator = pixmapGenerator

        if self._pixmapGenerator:
            anim = self._pixmapGenerator.anim()
            if anim:
                anim.tick.connect(self.update)

        self.update()

    def paintEvent(self, event):
        super(PixmapGeneratorLabel, self).paintEvent(event)

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


def run():
    # type: () -> NoReturn
    """
    Start the Iconify Browser and block until the process exits.
    """
    app = QtWidgets.QApplication([])

    browser = Browser()
    browser.show()

    sys.exit(app.exec_())
