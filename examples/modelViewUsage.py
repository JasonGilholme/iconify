
import os


os.environ["ICONIFY_PATH"] = os.path.dirname(__file__) + "/icons"


import iconify as ico
from iconify.qt import QtCore, QtGui, QtSvg, QtWidgets





class Model(QtCore.QStringListModel):

    def __init__(self, anim):
        super(Model, self).__init__()

        self._icons = ("delete", "github")
        self.setStringList(self._icons)

        self.anim = anim

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._icons[index.row()]
        elif role == QtCore.Qt.DecorationRole:
            return ico.Icon(self.data(index, role=QtCore.Qt.DisplayRole), anim=anim)
        return None


app = QtWidgets.QApplication([])

anim = ico.anim.Spin()

model = Model(anim)

view = QtWidgets.QListView()
view.setUniformItemSizes(True)
view.setViewMode(QtWidgets.QListView.IconMode)



view.setGridSize(QtCore.QSize(80, 80))
view.setIconSize(QtCore.QSize(64, 64))

view.setModel(model)


anim.tick.connect(view.viewport().update)
anim.start()
view.show()



import sys
sys.exit(app.exec_())
