"""
A module for fetching common image libraries and installing them into
your iconify installation
"""

import distutils.dir_util
import io
import os
import tempfile
import zipfile
from typing import Optional, Union

import iconify as ico

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen


_FONT_AWESOME_URL = "https://github.com/FortAwesome/Font-Awesome/releases/" \
                    "download/{0}/fontawesome-free-{0}-desktop.zip"
_MATERIAL_DESIGN_URL = "https://github.com/Templarian/MaterialDesign-SVG/" \
                       "archive/v{0}.zip"
_ELUSIVE_ICONS_URL = "https://github.com/reduxframework/elusive-icons/" \
                     "archive/master.zip"


def fetch():
    # type: () -> None
    """
    Fetch all the available icon sets.
    """
    fontAwesome()
    materialDesign()
    elusiveIcons()


def fontAwesome(version=None, urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str], Optional[str]) -> None
    """
    Download the FontAwesome images for iconify.

    When called with no arguments, version 5.12.1 will be downloaded into the
    first directory on the iconify path, throwing an EnvironmentError if no
    path is set.

    Provide the version argument to pull a specific version of the icons.

    You can use the url argument to download the zip file from an alternative
    location or also pass it a zip file on the local disk to use instead.

    Parameters
    ----------
    version : Optional[str]
    url : Optional[str]
    installLocation : Optional[str]
    """
    version = version or '5.12.1'
    installLocation = installLocation or _getInstallLocation('fa')
    urlOrFile = urlOrFile or _FONT_AWESOME_URL.format(version)

    filename, ext = os.path.splitext(os.path.basename(urlOrFile))
    zipFilePath = os.path.join(filename, 'svgs')

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath=zipFilePath,
    )


def materialDesign(version=None, urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str], Optional[str]) -> None
    version = version or '4.9.95'
    installLocation = installLocation or _getInstallLocation('mdi')
    urlOrFile = urlOrFile or _MATERIAL_DESIGN_URL.format(version)

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='MaterialDesign-SVG-{}/svg'.format(version),
    )


def elusiveIcons(urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str]) -> None
    installLocation = installLocation or _getInstallLocation('ei')
    urlOrFile = urlOrFile or _ELUSIVE_ICONS_URL

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='elusive-icons-master/dev/icons-svg',
    )


def _installZipFile(urlOrFilePath, installLocation, zipFilePath=None):
    # type: (str, str, Optional[str]) -> None
    if not os.path.isdir(installLocation):
        os.makedirs(installLocation)

    if os.path.isfile(urlOrFilePath):
        zipFile = urlOrFilePath  # type: Union[str, io.BytesIO]
    else:
        print('Downloading file: {}'.format(urlOrFilePath))
        zipFile = _downloadFile(urlOrFilePath)

    tmpdir = os.path.join(tempfile.gettempdir(), 'iconfiyTempDownload')

    if os.path.isdir(tmpdir):
        distutils.dir_util.remove_tree(tmpdir)

    print('Extracting to: {}'.format(installLocation))
    with zipfile.ZipFile(zipFile) as zipData:
        zipData.extractall(tmpdir)

        if zipFilePath:
            source = os.path.join(tmpdir, zipFilePath)
        else:
            source = tmpdir

        distutils.dir_util.copy_tree(source, installLocation)


def _downloadFile(url):
    # type: (str) -> io.BytesIO
    response = urlopen(url)
    return io.BytesIO(response.read())


def _getInstallLocation(suffix):
    # type: (str) -> str
    iconPath = ico.path._ICON_PATH
    if not iconPath:
        raise EnvironmentError(
            "Please set the ICONIFY_PATH environment variable or "
            "provide the 'installLocation' argument..."
        )

    return os.path.join(iconPath[0], suffix)
