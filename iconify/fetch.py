"""
A module for fetching common image libraries and installing them into
your iconify installation
"""

import distutils.dir_util
import io
import os
import tempfile
import zipfile

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

import iconify as ico


_FONT_AWESOME_URL = "https://github.com/FortAwesome/Font-Awesome/releases/download/{0}/fontawesome-free-{0}-desktop.zip"


def _downloadFile(url):
    response = urlopen(url)
    return io.BytesIO(response.read())


def fontAwesome(version=None, url=None, installLocation=None):
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
    if installLocation is None:
        iconPath = ico.path._ICON_PATH
        if not iconPath:
            raise EnvironmentError(
                "Please set the ICONIFY_PATH environment variable or provide the 'installLocation' argument..."
            )

        installLocation = os.path.join(iconPath[0], 'fa')

    if not os.path.isdir(installLocation):
        os.makedirs(installLocation)

    if url is None:
        if version is None:
            version = '5.12.1'
        url = _FONT_AWESOME_URL.format(version)

    print('Downloading file: {}'.format(url))
    if os.path.isfile(url):
        zipFile = url
    else:
        zipFile = _downloadFile(url)

    tmpdir = os.path.join(tempfile.gettempdir(), 'iconfiyTempDownload')

    if os.path.isdir(tmpdir):
        distutils.dir_util.remove_tree(tmpdir)

    print('Extracting to: {}'.format(installLocation))
    with zipfile.ZipFile(zipFile) as zipData:
        zipData.extractall(tmpdir)

        filename, ext = os.path.splitext(os.path.basename(url))

        source = os.path.join(tmpdir, filename, 'svgs')
        distutils.dir_util.copy_tree(source, installLocation)
