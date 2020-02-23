"""
Expose Qt to iconify using the ICONIFY_QTLIB environment variable.
"""

import os
import pydoc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *
    from PySide2 import QtCore, QtGui, QtSvg, QtWidgets
    qtlib = 'PySide2'
else:
    qtlib = os.environ.get("ICONIFY_QTLIB", "PySide2")

    QtCore = pydoc.locate(qtlib + '.QtCore')
    QtGui = pydoc.locate(qtlib + '.QtGui')
    QtSvg = pydoc.locate(qtlib + '.QtSvg')
    QtWidgets = pydoc.locate(qtlib + '.QtWidgets')


_IMPORT_ERROR_MESSAGE = \
    "Unable to import {0}.{1}! Please set the 'ICONIFY_QTLIB' env var " \
    "to the location of the Qt binding you would like to use."

if QtCore is None:
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib, 'QtCore'))

if QtGui is None:
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib, 'QtGui'))

if QtSvg is None:
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib, 'QtSvg'))

if QtWidgets is None:
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib, 'QtWidgets'))
