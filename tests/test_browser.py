
import pytest

from iconify.browser import Browser
from iconify.qt import QtCore, QtWidgets


@pytest.fixture
def browser(qtbot, validIconPath):
    browser = Browser()
    qtbot.add_widget(browser)
    browser.show()
    yield browser
    browser.close()


def test_browser_init(qtbot, browser):
    """
    Ensure the browser opens without error
    """
    browser.close()


def test_copy(qtbot, browser):
    """
    Ensure the copy UX works
    """
    clipboard = QtWidgets.QApplication.instance().clipboard()

    clipboard.setText('')

    assert clipboard.text() == ""

    # Enter a search term and press enter
    qtbot.keyClicks(browser._lineEdit, 'delete')
    qtbot.keyPress(browser._lineEdit, QtCore.Qt.Key_Enter)

    # TODO: Figure out how to do this via a qtbot.mouseClick call
    # Select the first item in the list
    model = browser._listView.model()
    selectionModel = browser._listView.selectionModel()
    selectionModel.setCurrentIndex(model.index(0, 0),
                                   QtCore.QItemSelectionModel.ClearAndSelect)

    # Click the copy button
    qtbot.mouseClick(browser._copyButton, QtCore.Qt.LeftButton)

    clipboardText = clipboard.text()
    assert "delete" in clipboardText

    # Ensure copy with no selection doesn't break
    selectionModel.clear()

    qtbot.mouseClick(browser._copyButton, QtCore.Qt.LeftButton)

    # Make sure we don't erase any existing clipboard text.
    assert clipboardText == clipboard.text()


def test_filter(qtbot, browser):
    """
    Ensure the filter UX works
    """
    initRowCount = browser._listView.model().rowCount()
    assert initRowCount > 0

    # Enter a search term
    qtbot.keyClicks(browser._lineEdit, 'delete')

    # Press Enter to perform the filter
    qtbot.keyPress(browser._lineEdit, QtCore.Qt.Key_Enter)

    filteredRowCount = browser._listView.model().rowCount()
    assert initRowCount > filteredRowCount

    # Test supplying an empty search string and waiting
    # for the auto ommmit feature to trigger.
    waiting = qtbot.waitSignal(
        signal=browser._filterTimer.timeout,
        timeout=2000,
        raising=True,
    )

    with waiting:
        browser._lineEdit.selectAll()
        qtbot.keyPress(browser._lineEdit, QtCore.Qt.Key_Backspace)

    assert waiting.signal_triggered

    # Test that the filtering has been refreshed.
    filteredRowCount = browser._listView.model().rowCount()
    assert initRowCount == filteredRowCount
