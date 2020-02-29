
import os

import pytest

import iconify


def test_findIcon(validIconPath):
    # Simple icon path
    iconPath = iconify.path.findIcon('delete')
    assert os.path.isfile(iconPath)

    # Nested icon path
    iconPath = iconify.path.findIcon('spinners:dots')
    assert os.path.isfile(iconPath)

    # Invalid icon path
    with pytest.raises(iconify.path.IconNotFoundError):
        iconify.path.findIcon('invalid:icon:path')


def test_addIconDirectory(invalidIconPath):
    # Invalid icon path
    with pytest.raises(iconify.path.IconNotFoundError):
        iconify.path.findIcon('delete')

    iconDir = os.path.join(os.path.dirname(__file__), "fixtures", "icons")
    iconify.path.addIconDirectory(iconDir)

    iconPath = iconify.path.findIcon('delete')
    assert os.path.isfile(iconPath)


def test_listIcons():
    for iconName in iconify.path.listIcons():
        icon = iconify.path.findIcon(iconName)
        assert icon is not None
        assert os.path.isfile(icon)
