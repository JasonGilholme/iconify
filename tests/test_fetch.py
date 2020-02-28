
import os

import iconify as ico


def test_fetchRemote(tmpIconPath):
    ico.fetch.fetch()


def test_fetchLocal(tmpIconPath):
    zipFileDir = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "zipFiles",
    )

    fontAwesomePath = os.path.join(zipFileDir, 'fontawesome-free-5.12.1-desktop.zip')
    ico.fetch.fontAwesome(urlOrFile=fontAwesomePath)

    materialDesignPath = os.path.join(zipFileDir, 'MaterialDesign-SVG-4.9.95.zip')
    ico.fetch.materialDesign(urlOrFile=materialDesignPath)

    elusiveIconsPath = os.path.join(zipFileDir, 'elusive-icons-master.zip')
    ico.fetch.elusiveIcons(urlOrFile=elusiveIconsPath)
