
import os

import pytest

import iconify.path
import tempfile


@pytest.fixture
def validIconPath(monkeypatch):
    iconDir = os.path.join(os.path.dirname(__file__), "fixtures", "icons")
    monkeypatch.setattr(iconify.path, "_ICON_PATH", [iconDir])

    iconify.path.findIcon.cache_clear()
    yield
    iconify.path.findIcon.cache_clear()


@pytest.fixture
def invalidIconPath(monkeypatch):
    monkeypatch.setattr(iconify.path, '_ICON_PATH', [])

    iconify.path.findIcon.cache_clear()
    yield
    iconify.path.findIcon.cache_clear()


@pytest.fixture
def tmpIconPath():
    initIconPath = iconify.path._ICON_PATH

    iconDir = os.path.join(tempfile.gettempdir(), "icons")

    iconify.path._ICON_PATH = [iconDir]
    iconify.path.findIcon.cache_clear()

    yield

    iconify.path._ICON_PATH = initIconPath
    iconify.path.findIcon.cache_clear()
