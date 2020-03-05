
import os

import iconify
from iconify.qt import QtCore, QtGui, QtWidgets


def test_icon(qtbot, validIconPath):
    anim = iconify.anim.Spin()
    color = QtGui.QColor('red')

    icon = iconify.Icon(
        'delete',
        color=color,
        anim=anim,
    )

    pixmapGenerator = icon.pixmapGenerator()
    assert pixmapGenerator.anim() is anim
    assert pixmapGenerator.color() is color

    assert icon.anim() is anim

    button = QtWidgets.QPushButton()
    icon.setAsButtonIcon(button)

    button.show()


def test_pixmapGenerator(qtbot, validIconPath):
    size = QtCore.QSize(24, 24)
    color = QtGui.QColor('blue')
    anim = iconify.anim.Spin()

    basePixmapGen = iconify.core.PixmapGenerator('delete')

    assert os.path.isfile(basePixmapGen.path())
    assert basePixmapGen.color() is None
    assert basePixmapGen.anim() is None

    coloredPixmapGen = iconify.core.PixmapGenerator('delete', color=color)

    assert os.path.isfile(coloredPixmapGen.path())
    assert coloredPixmapGen.color() == color
    assert coloredPixmapGen.anim() is None

    animatedPixmapGen = iconify.core.PixmapGenerator('delete', anim=anim)

    assert os.path.isfile(animatedPixmapGen.path())
    assert animatedPixmapGen.color() is None
    assert animatedPixmapGen.anim() == anim

    baseImage = basePixmapGen.pixmap(size).toImage()
    coloredImage = coloredPixmapGen.pixmap(size).toImage()
    animatedImage = animatedPixmapGen.pixmap(size).toImage()

    assert baseImage.size() == size
    assert coloredImage.size() == size
    assert animatedImage.size() == size

    assert baseImage == baseImage
    assert baseImage != coloredImage
    assert baseImage != animatedImage


def test_pixmapGeneratorCache(qtbot, validIconPath):
    anim = iconify.anim.Spin()
    pixGen = iconify.core.PixmapGenerator('delete', color=QtGui.QColor('blue'), anim=anim)

    size = QtCore.QSize(24, 24)
    altSize = QtCore.QSize(32, 32)

    # Ensure that the pixmap generators cache is working as expected
    pixmapA = pixGen.pixmap(size)
    pixmapB = pixGen.pixmap(size)
    pixmapC = pixGen.pixmap(altSize)

    assert pixmapA is pixmapB
    assert pixmapA is not pixmapC


def test_multiState(qtbot, validIconPath):
    redColor = QtGui.QColor('red')
    blueColor = QtGui.QColor('blue')
    spinAnim = iconify.anim.Spin()
    breatheAnim = iconify.anim.Breathe()

    icon = iconify.Icon('delete', color=redColor, anim=breatheAnim)
    assert icon.animCount() == 1
    assert icon.color() == redColor
    assert icon.anim() is breatheAnim

    # Add a second state
    icon.addState(
        'spinners:dots', mode=QtGui.QIcon.Active,
    )
    assert icon.animCount() == 2
    # The color and anim kwargs are expected to fall back
    # to the values on the 'default' state when not provided.
    assert icon.anim(mode=QtGui.QIcon.Active) == breatheAnim
    assert icon.color(mode=QtGui.QIcon.Active) == redColor

    # Replace that state with something else
    icon.addState(
        'spinners:colored', anim=spinAnim, mode=QtGui.QIcon.Active,
    )
    assert icon.animCount() == 2
    assert icon.anim(mode=QtGui.QIcon.Active) == spinAnim
    assert icon.color(mode=QtGui.QIcon.Active) == redColor

    # Add a third state
    icon.addState(
        'spinners:dots', color=blueColor, mode=QtGui.QIcon.Selected,
    )
    assert icon.animCount() == 3
    assert icon.anim(mode=QtGui.QIcon.Selected) == breatheAnim
    assert icon.color(mode=QtGui.QIcon.Selected) == blueColor
