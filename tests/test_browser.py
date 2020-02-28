
import pytest

from iconify.browser import Browser
from iconify.qt import QtCore


@pytest.fixture
def browser(qtbot):
    browser = Browser()
    qtbot.add_widget(browser)
    browser.show()
    return browser


def test_browser_init(browser):
    """
    Ensure the browser opens without error
    """
    def close():
        browser.close()

    timer = QtCore.QTimer()
    timer.timeout.connect(close)
    timer.setSingleShot(2000)
    timer.start()
