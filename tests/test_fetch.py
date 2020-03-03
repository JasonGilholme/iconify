
import os

import iconify as ico


def test_fetchRemote(tmpIconPath):
    ico.fetch.fetch()


def test_fetchLocal(tmpIconPath, monkeypatch):
    zipFileDir = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "fetchFiles",
    )

    fontAwesomePath = os.path.join(zipFileDir, 'fontawesome-free-5.12.1-desktop.zip')
    ico.fetch.FontAwesome.fetch(urlOrFile=fontAwesomePath)

    materialDesignPath = os.path.join(zipFileDir, 'MaterialDesign-SVG-4.9.95.zip')
    ico.fetch.MaterialDesign.fetch(urlOrFile=materialDesignPath)

    elusiveIconsPath = os.path.join(zipFileDir, 'elusive-icons-master.zip')
    ico.fetch.Elusive.fetch(urlOrFile=elusiveIconsPath)

    dashIconsPath = os.path.join(zipFileDir, 'dashicons-master.zip')
    ico.fetch.Dash.fetch(urlOrFile=dashIconsPath)

    feathericonsPath = os.path.join(zipFileDir, 'feather-4.26.0.zip')
    ico.fetch.Feather.fetch(urlOrFile=feathericonsPath)

    monkeypatch.setattr(
        ico.fetch.EmojiFetcher,
        "EMOJI_MAP_URL",
        os.path.join(zipFileDir, 'emoji-test.txt')
    )

    googleEmojiPath = os.path.join(zipFileDir, 'noto-emoji-2019-11-19-unicode12.zip')
    ico.fetch.GoogleEmojis.fetch(urlOrFile=googleEmojiPath)

    emojioneLegacyPath = os.path.join(zipFileDir, 'emojione-legacy-master.zip')
    ico.fetch.EmojioneLegacy.fetch(urlOrFile=emojioneLegacyPath)
