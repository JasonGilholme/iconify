
import os

import iconify as ico


def test_fetchRemote(tmpIconPath):
    ico.fetch.fetch()


def test_fetchLocal(tmpIconPath):
    zipFileDir = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "fetchFiles",
    )

    fontAwesomePath = os.path.join(zipFileDir, 'fontawesome-free-5.12.1-desktop.zip')
    ico.fetch.fontAwesome(urlOrFile=fontAwesomePath)

    materialDesignPath = os.path.join(zipFileDir, 'MaterialDesign-SVG-4.9.95.zip')
    ico.fetch.materialDesign(urlOrFile=materialDesignPath)

    elusiveIconsPath = os.path.join(zipFileDir, 'elusive-icons-master.zip')
    ico.fetch.elusiveIcons(urlOrFile=elusiveIconsPath)

    dashIconsPath = os.path.join(zipFileDir, 'dashicons-master.zip')
    ico.fetch.dashIcons(urlOrFile=dashIconsPath)

    feathericonsPath = os.path.join(zipFileDir, 'feather-4.26.0.zip')
    ico.fetch.featherIcons(urlOrFile=feathericonsPath)

    googleEmojiPath = os.path.join(zipFileDir, 'noto-emoji-2019-11-19-unicode12.zip')
    googleEmojiMapPath = os.path.join(zipFileDir, 'emoji-test.txt')
    ico.fetch.googleEmojis(urlOrFile=googleEmojiPath, emojiMapUrlOrFile=googleEmojiMapPath)
