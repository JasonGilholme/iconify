"""
Expose Qt to iconify using the ICONIFY_QTLIB environment variable.
"""

import os
import pydoc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide2 import QtCore, QtGui, QtSvg, QtWidgets, QtXml
    qtlib = 'PySide2'
else:
    qtlib = os.environ.get("ICONIFY_QTLIB", "PySide2")

    QtCore = pydoc.locate(qtlib + '.QtCore')
    QtGui = pydoc.locate(qtlib + '.QtGui')
    QtSvg = pydoc.locate(qtlib + '.QtSvg')
    QtWidgets = pydoc.locate(qtlib + '.QtWidgets')
    QtXml = pydoc.locate(qtlib + '.QtXml')


_IMPORT_ERROR_MESSAGE = \
    "Unable to import required Qt libraries from {0}! Please set the " \
    "'ICONIFY_QTLIB' env var to the location of a Qt5 compliant python " \
    "binding you would like to use."

if None in (QtCore, QtGui, QtSvg, QtWidgets, QtXml):
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib))
