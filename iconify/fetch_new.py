"""
A module for fetching common image libraries and installing them into
your iconify installation
"""

import distutils.dir_util
import os
import tempfile
import zipfile
import re
import glob

import inspect
import sys



import iconify as ico
from iconify.qt import QtCore, QtXml


try:
    # Python 2
    from urllib import urlretrieve
except ImportError:
    # Python 3
    from urllib.request import urlretrieve


def fetch():
    fetchers = []

    for _, member in inspect.getmembers(sys.modules[__name__]):
        if isinstance(member, type) and \
                issubclass(member, Fetcher) and \
                member not in (Fetcher, EmojiFetcher):
            fetchers.append(member)

    for fetcher in fetchers:
        fetcher.fetch()


class Fetcher(object):

    NAMESPACE = None  # type: str
    URL = None  # type: str
    ZIP_FILE_PATHS = None  # type: Tuple[str, ...]

    @classmethod
    def fetch(cls, urlOrFile=None, installLocation=None):
        print("Fetching {}...".format(cls.__name__))
        if not installLocation:
            iconPath = ico.path._ICON_PATH
            if not iconPath:
                raise EnvironmentError(
                    "Please set the ICONIFY_PATH environment variable or "
                    "provide the 'installLocation' argument..."
                )

            installLocation = os.path.join(iconPath[0], cls.NAMESPACE)

        if not urlOrFile:
            urlOrFile = cls.URL

        localFile = cls.downloadFile(urlOrFile)
        cls.installZipFile(localFile, installLocation)

    @classmethod
    def downloadFile(cls, urlOrFile):
        print 'download file:', urlOrFile
        if os.path.isfile(urlOrFile):
            return urlOrFile

        urlFile = os.path.basename(urlOrFile)
        downloadDest = os.path.join(
            tempfile.gettempdir(),
            'iconfiyTempDownload',
            cls.NAMESPACE,
            urlFile,
        )

        if not os.path.isfile(downloadDest):
            print('Downloading file: {}'.format(urlOrFile))
            destDir = os.path.dirname(downloadDest)
            if not os.path.isdir(destDir):
                os.makedirs(destDir)
            urlretrieve(urlOrFile, downloadDest)
        else:
            print("Found existing download: {}".format(downloadDest))

        return downloadDest

    @classmethod
    def installZipFile(cls, localFile, installLocation):
        tmpdir = os.path.join(tempfile.gettempdir(), 'iconfiyTempExtraction')
        if os.path.isdir(tmpdir):
            distutils.dir_util.remove_tree(tmpdir)

        print('Extracting to: {}'.format(installLocation))
        with zipfile.ZipFile(localFile) as zipData:
            zipData.extractall(tmpdir)

            cls.updateDataHook(installLocation)

            for zipFilePath in cls.ZIP_FILE_PATHS:
                source = os.path.join(tmpdir, zipFilePath)
                distutils.dir_util.copy_tree(source, installLocation)

    @classmethod
    def updateDataHook(cls, installLocation):
        """
        An optional hook that an be used to update the downloaded
        data prior to being installed on the host system.
        """


#
# Fetch Implementations
#
class FontAwesome(Fetcher):

    NAMESPACE = "font-awesome"
    URL = "https://github.com/FortAwesome/Font-Awesome/releases/" \
          "download/5.12.1/fontawesome-free-5.12.1-desktop.zip"
    ZIP_FILE_PATHS = ("fontawesome-free-5.12.1-desktop/svgs",)


class MaterialDesign(Fetcher):

    NAMESPACE = "material-design"
    URL = "https://github.com/Templarian/MaterialDesign-SVG/" \
          "archive/v4.9.95.zip"
    ZIP_FILE_PATHS = ("MaterialDesign-SVG-4.9.95/svg",)


class Elusive(Fetcher):

    NAMESPACE = "elusive"
    URL = "https://github.com/reduxframework/elusive-icons/" \
          "archive/master.zip"
    ZIP_FILE_PATHS = ("elusive-icons-master/dev/icons-svg",)


class Dash(Fetcher):

    NAMESPACE = "dash"
    URL = "https://github.com/WordPress/dashicons/archive/master.zip"
    ZIP_FILE_PATHS = ("dashicons-master/sources/svg",)


class Feather(Fetcher):

    NAMESPACE = "feather"
    URL = "https://github.com/feathericons/feather/archive/v4.26.0.zip"
    ZIP_FILE_PATHS = ("feather-4.26.0/icons",)


class EmojiFetcher(Fetcher):

    NAMESPACE = 'BaseEmoji'
    EMOJI_MAP_URL = "https://unicode.org/Public/emoji/13.0/emoji-test.txt"

    @classmethod
    def getEmojiMap(cls):
        # type: () -> Mapping[str, str]
        """
        Create a map of emoji codes to names for file renaming.

        Returns
        -------
        Mapping[str, str]
        """
        emojiMap = {'200d': 'and'}

        emojiMapUrlOrFile = Fetcher.downloadFile(cls.EMOJI_MAP_URL)

        with _openFile(emojiMapUrlOrFile) as infile:
            emojiDataLines = infile.readlines()  # type: List[str]

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


class GoogleEmojis(EmojiFetcher):

    NAMESPACE = "google-emojis"
    URL = "https://github.com/googlefonts/noto-emoji/archive/" \
          "v2019-11-19-unicode12.zip"
    ZIP_FILE_PATHS = ("noto-emoji-2019-11-19-unicode12/svg",)

    @classmethod
    def updateDataHook(cls, installLocation):
        emojiMap = cls.getEmojiMap()
        cls._renameEmojiFiles(installLocation, emojiMap)
        cls._removeUnsupportedNodes(installLocation)

    @classmethod
    def _renameEmojiFiles(cls, installLocation, emojiMap):
        # type: (str, Mapping[str, str]) -> None
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


class EmojioneLegacy(EmojiFetcher):

    NAMESPACE = "emojione-legacy"
    URL = "https://github.com/joypixels/emojione-legacy/archive/master.zip"
    ZIP_FILE_PATHS = ("emojione-legacy-master/svg",)

    @classmethod
    def updateDataHook(cls, installLocation):
        emojiMap = cls.getEmojiMap()
        cls._renameEmojiFiles(installLocation, emojiMap)

    @classmethod
    def _renameEmojiFiles(cls, installLocation, emojiMap):
        # type: (str, Mapping[str, str]) -> None
        """
        Rename emojione files by replacing the emoji code with the nice name.

        Parameters
        ----------
        installLocation : str
        emojiMap : Mapping[str, str]
        """
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


fetch()