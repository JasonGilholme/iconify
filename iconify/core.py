
import os
import pydoc

qtlib = os.environ.get("ICONIFY_QTLIB", "PySide2")

QtCore = pydoc.locate(qtlib + '.QtCore')
QtGui = pydoc.locate(qtlib + '.QtGui')
QtSvg = pydoc.locate(qtlib + '.QtSvg')
QtWidgets = pydoc.locate(qtlib + '.QtWidgets')

if QtCore is None:
    raise ImportError('Unable to import QtCore!')

if QtGui is None:
    raise ImportError('Unable to import QtGui!')

if QtSvg is None:
    raise ImportError('Unable to import QtSvg!')

if QtWidgets is None:
    raise ImportError('Unable to import QtWidgets!')


_ICON_PATH = os.environ.get('ICONIFY_PATH', os.getcwd()).split(os.pathsep)


def find_icon(icon_path):
    if os.path.isabs(icon_path):
        if not os.path.isfile(icon_path):
            raise RuntimeError("Unable to locate icon file: %s" % (icon_path,))
        return icon_path
    else:
        for dir_ in _ICON_PATH:
            abs_icon_path = os.path.join(dir_, icon_path)
            if os.path.isfile(abs_icon_path):
                return abs_icon_path

        raise Exception(
            "Unable to find an icon on the ICONIFY_PATH that matches '%s'" %
            (icon_path,)
        )
