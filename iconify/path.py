
import os
import pydoc

from kids.cache import cache


_ICON_PATH = os.environ.get('ICONIFY_PATH', os.getcwd()).split(os.pathsep)


class IconNotFoundError(Exception):
    pass


def addIconDirectory(directoryLocation):
    _ICON_PATH.append(directoryLocation)


@cache
def findIcon(iconPath):
    if os.path.isabs(iconPath):
        if not os.path.isfile(iconPath):
            raise IconNotFoundError("Unable to locate icon file: {}".format(iconPath))
        return iconPath
    else:
        iconPath = iconPath.replace(":", os.sep)
        for dir_ in _ICON_PATH:
            absIconPath = os.path.join(dir_, iconPath + ".svg")
            if os.path.isfile(absIconPath):
                return absIconPath

        raise IconNotFoundError(
            "Unable to find an icon on the ICONIFY_PATH that matches '{}'".format(iconPath)
        )
