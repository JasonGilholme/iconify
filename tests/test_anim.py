
import inspect

import pytest

import iconify
import iconify.qt


ANIM_CLASSES = [
    m for _, m in inspect.getmembers(iconify.anim) if
    isinstance(m, type) and
    issubclass(m, iconify.anim.BaseAnimation) and
    m is not iconify.anim.BaseAnimation and
    not m.__name__.startswith('_')
]


@pytest.mark.parametrize("animCls", ANIM_CLASSES)
def test_animSmokeTests(animCls):
    anim = animCls()

    size = iconify.qt.QtCore.QSize(64, 64)

    initXfm = anim.transform(size)

    for i in range(anim._maxFrame + 5):
        anim.forceTick()

    nextXfm = anim.transform(size)

    assert initXfm != nextXfm


def test_animStartStop():
    anim = iconify.anim.BaseAnimation()

    initFrame = anim.frame()

    for i in range(5):
        anim.forceTick()

    currFrame = anim.frame()

    assert currFrame > initFrame


def test_concatAnim():
    anim = iconify.anim.Spin() + iconify.anim.Breathe()

    size = iconify.qt.QtCore.QSize(64, 64)

    initXfm = anim.transform(size)

    for i in range(anim._maxFrame + 5):
        anim.forceTick()

    nextXfm = anim.transform(size)

    assert initXfm != nextXfm
    assert anim.active() is False

    frameA = anim.frame()
    anim.start()
    assert anim.active() is True
    anim.stop()
    frameB = anim.frame()

    assert frameA != frameB
    assert anim.active() is False

    anim.toggle()
    assert anim.active() is True
    anim.pause()
    frameC = anim.frame()

    # assert frameB != frameC
    # assert anim.active() is False