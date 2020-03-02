"""
A module for fetching common image libraries and installing them into
your iconify installation
"""

import distutils.dir_util
import glob
import io
import os
import re
import sys
import tempfile
import zipfile
from typing import IO, Any, List, Mapping, Optional, Union

import iconify as ico
from iconify.qt import QtCore, QtXml

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
_DASH_ICONS_URL = "https://github.com/WordPress/dashicons/archive/master.zip"
_FEATHER_ICONS_URL = "https://github.com/feathericons/feather/archive/v{}.zip"
_GOOGLE_EMOJIS_URL = "https://github.com/googlefonts/noto-emoji/archive/" \
                     "v2019-11-19-unicode12.zip"
_UNICODE_EMOJIS_URL = "https://unicode.org/Public/emoji/13.0/emoji-test.txt"
_EMOJIONE_LEGACY_URL = "https://github.com/joypixels/emojione-legacy/" \
                       "archive/master.zip"


def fetch():
    # type: () -> None
    """
    Fetch all the available icon sets.
    """
    fontAwesome()
    materialDesign()
    elusiveIcons()
    dashIcons()
    featherIcons()
    googleEmojis()
    emojioneLegacy()


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
    installLocation = installLocation or _getInstallLocation('font-awesome')
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
    installLocation = installLocation or _getInstallLocation('material-design')
    urlOrFile = urlOrFile or _MATERIAL_DESIGN_URL.format(version)

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='MaterialDesign-SVG-{}/svg'.format(version),
    )


def elusiveIcons(urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str]) -> None
    installLocation = installLocation or _getInstallLocation('elusive')
    urlOrFile = urlOrFile or _ELUSIVE_ICONS_URL

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='elusive-icons-master/dev/icons-svg',
    )


def dashIcons(urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str]) -> None
    installLocation = installLocation or _getInstallLocation('dash')
    urlOrFile = urlOrFile or _DASH_ICONS_URL

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='dashicons-master/sources/svg',
    )


def featherIcons(version=None, urlOrFile=None, installLocation=None):
    # type: (Optional[str], Optional[str], Optional[str]) -> None
    version = version or '4.26.0'
    installLocation = installLocation or _getInstallLocation('feather')
    urlOrFile = urlOrFile or _FEATHER_ICONS_URL.format(version)

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='feather-{}/icons'.format(version),
    )


def googleEmojis(urlOrFile=None, installLocation=None, emojiMapUrlOrFile=None):
    # type: (Optional[str], Optional[str], Optional[str]) -> None
    installLocation = installLocation or _getInstallLocation('google-emojis')
    urlOrFile = urlOrFile or _GOOGLE_EMOJIS_URL
    emojiMapUrlOrFile = emojiMapUrlOrFile or _UNICODE_EMOJIS_URL

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='noto-emoji-2019-11-19-unicode12/svg',
    )

    _renameEmojiFiles(installLocation, emojiMapUrlOrFile)
    _removeUnsupportedNodes(installLocation)

    _installZipFile(
        urlOrFile,
        os.path.join(installLocation, 'flags'),
        zipFilePath='noto-emoji-2019-11-19-unicode12/'
        'third_party/region-flags/svg',
    )


def emojioneLegacy(
    urlOrFile=None, installLocation=None, emojiMapUrlOrFile=None
):
    # type: (Optional[str], Optional[str], Optional[str]) -> None
    installLocation = installLocation or _getInstallLocation('emojione-legacy')
    urlOrFile = urlOrFile or _EMOJIONE_LEGACY_URL
    emojiMapUrlOrFile = emojiMapUrlOrFile or _UNICODE_EMOJIS_URL

    _installZipFile(
        urlOrFile,
        installLocation,
        zipFilePath='emojione-legacy-master/svg',
    )

    _renameEmojiOneFiles(installLocation, emojiMapUrlOrFile)


def _getEmojiMap(emojiMapUrlOrFile):
    # type: (str) -> Mapping[str, str]
    """
    Create a map of emoji codes to names for file renaming.

    Parameters
    ----------
    emojiMapUrlOrFile : str

    Returns
    -------
    Mapping[str, str]
    """
    emojiMap = {'200d': 'and'}

    if os.path.isfile(emojiMapUrlOrFile):
        with _openFile(emojiMapUrlOrFile) as infile:
            emojiDataLines = infile.readlines()  # type: List[bytes]
    else:
        print('Downloading file: {}'.format(emojiMapUrlOrFile))
        emojiDataLines = _downloadFile(emojiMapUrlOrFile).readlines()

    for line in emojiDataLines:
        match = re.match(
            r"^(.*);.*E[0-9\.]+(.*)$",
            str(line),
        )
        if not match:
            continue

        code, name = match.groups()

        codes = code.strip().split(' ')
        names = name.strip().split(':')

        if len(codes) == 1:
            names = [name.strip()]

        for i, name in enumerate(names):
            code = codes[i].strip().lower()
            if code in emojiMap:
                continue
            emojiMap[code.strip().lower()] = _cleanName(name)

    return emojiMap


def _cleanName(name):
    # type: (str) -> str
    name = name.strip()
    name = name.replace(' ', '-').replace(':', '')
    stripped = (c for c in name if 0 < ord(c) < 127)
    name = ''.join(stripped)
    return name.lower()


def _openFile(filePath):
    # type: (str) -> IO[Any]
    if sys.version_info[0] == 3:
        return open(filePath, 'r', encoding='utf-8')
    else:
        return open(filePath, 'r')


def _renameEmojiOneFiles(installLocation, emojiMapUrlOrFile):
    # type: (str, str) -> None
    """
    Rename emojione files by replacing the emoji code with the nice name.

    Parameters
    ----------
    installLocation : str
    emojiMapUrlOrFile : str
    """
    emojiMap = _getEmojiMap(emojiMapUrlOrFile)

    for svg in glob.glob(os.path.join(installLocation, '*.svg')):
        basename = os.path.basename(svg)
        basename, ext = os.path.splitext(basename)

        newParts = []

        for part in basename.split('-'):
            alias = emojiMap.get(part.lower())
            if alias:
                newParts.append(alias)

        if not newParts or all([a == 'and' for a in newParts]):
            continue

        alias = '-'.join(newParts).replace(':', '')
        if basename != alias:
            os.rename(svg, svg.replace(basename, alias))


def _renameEmojiFiles(installLocation, emojiMapUrlOrFile):
    # type: (str, str) -> None
    """
    Rename google emoji files by replacing the emoji code with the nice name.

    Parameters
    ----------
    installLocation : str
    emojiMapUrlOrFile : str
    """
    emojiMap = _getEmojiMap(emojiMapUrlOrFile)

    for svg in glob.glob(os.path.join(installLocation, '*.svg')):
        basename = os.path.basename(svg)
        basename, ext = os.path.splitext(basename)

        newParts = []

        for part in basename.replace('emoji_u', '').split('_'):
            alias = emojiMap.get(part)
            if alias:
                newParts.append(alias)

        if not newParts or all([a == 'and' for a in newParts]):
            continue

        alias = '-'.join(newParts).replace(':', '')
        if basename != alias:
            os.rename(svg, svg.replace(basename, alias))


def _removeUnsupportedNodes(installLocation):
    # type: (str) -> None
    for svg in glob.glob(os.path.join(installLocation, '*.svg')):

        dom = QtXml.QDomDocument("initData")

        svgFile = QtCore.QFile(svg)
        svgFile.open(QtCore.QIODevice.ReadOnly)
        dom.setContent(svgFile)
        svgFile.close()

        defNodes = dom.elementsByTagName('defs')
        for i in range(defNodes.count()):
            node = defNodes.item(0)
            node.parentNode().removeChild(node)

        symbolNodes = dom.elementsByTagName('symbol')
        for i in range(symbolNodes.count()):
            node = symbolNodes.item(0)
            node.parentNode().removeChild(node)

        byteArray = QtCore.QByteArray()
        textStream = QtCore.QTextStream(byteArray)
        dom.save(textStream, 0)

        svgFile = QtCore.QFile(svg)
        svgFile.open(QtCore.QIODevice.WriteOnly)
        svgFile.write(byteArray)
        svgFile.close()


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
