from pytemplate_qt import global_vars
from pytemplate_qt.qt import QMessageBox

_ERROR_COUNT = 0

def qt_excepthook(exc_type, exc_value, tb):
    global _ERROR_COUNT
    _ERROR_COUNT += 1
    if _ERROR_COUNT > 5:
        return
    exc = traceback.format_exception(exc_type, exc_value, tb)
    QMessageBox.warning(
        global_vars.MAIN_WINDOW,
        "Unhandled Error",
        str(exc),
    )

__all__ = [
    'qt_excepthook',
]
