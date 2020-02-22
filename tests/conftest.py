
import os

import pytest

import iconify.path


@pytest.fixture
def validIconPath():
    initIconPath = iconify.path._ICON_PATH

    iconDir = os.path.join(os.path.dirname(__file__), "icons")

    iconify.path._ICON_PATH = [iconDir]
    iconify.path.findIcon.cache_clear()

    yield

    iconify.path._ICON_PATH = initIconPath
    iconify.path.findIcon.cache_clear()


@pytest.fixture
def invalidIconPath():
    initIconPath = iconify.path._ICON_PATH

    iconify.path._ICON_PATH = []
    iconify.path.findIcon.cache_clear()

    yield

    iconify.path._ICON_PATH = initIconPath
    iconify.path.findIcon.cache_clear()
