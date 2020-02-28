
import os
import sys

import pytest

import iconify.qt


def _reloadQt():
    if sys.version_info[0] == 3:
        import importlib
        importlib.reload(iconify.qt)
    else:
        reload(iconify.qt)


def test_locateInvalidQtlib(monkeypatch):
    os.environ['ICONIFY_QTLIB'] = 'Invalid'

    with pytest.raises(ImportError):
        _reloadQt()

    os.environ.pop('ICONIFY_QTLIB')

    _reloadQt()
