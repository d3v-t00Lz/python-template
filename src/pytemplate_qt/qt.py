#  type: ignore
"""
    A module to provide common functionality across multiple
    versions (Qt5, Qt6) and implementations (PyQt, PySide)
    of Qt for Python.

    Note that there are some subtle API differences between PySide and PyQt
    that make supporting both simultaneously somewhere between difficult and
    impossible.  Using Qt5 and Qt6 in parallel is well supported, although
    the use of Qt6 exclusively is encouraged if possible.
"""

from pytemplate.log import LOG
from pymarshal.util.pm_assert import pm_assert
import os
import sys


if True:  # PyQt
    try:
        import PyQt6
        # default to PyQt5
        _PYQT5_ONLY = False
    except ImportError:
        try:
            import PyQt5
        except ImportError:
            LOG.error(f"Unable to Find PyQt5 or PyQt6 in {sys.path}")
            sys.exit(1)
        # default to PyQt6 if available, and PyQt5 is not
        _PYQT5_ONLY = True
    if (
        _PYQT5_ONLY
        or
        "_USE_PYQT5" in os.environ
    ):
        LOG.info("Using PyQt5")
        qt_event_pos = lambda x: x.pos()
        from PyQt5 import QtGui, QtWidgets, QtCore
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        from PyQt5.QtSvg import QSvgRenderer
        # Not needed on Qt6, is the default behavior
        try:
            QGuiApplication.setAttribute(
                QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling,
            )
        except Exception as ex:
            LOG.warning(
                f"The platform you are using does not support Qt HiDpi: {ex}",
            )
    else:
        LOG.info("Using PyQt6")
        def qt_event_pos(x):
            if hasattr(x, 'pos'):
                return x.pos()
            else:
                return x.position().toPoint()
        from PyQt6 import QtGui, QtWidgets, QtCore
        from PyQt6.QtQuick import QQuickView
        from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
        from PyQt6.QtGui import *
        from PyQt6.QtWidgets import *
        from PyQt6.QtSvg import QSvgRenderer

else:  # PySide
    LOG.info("Using PySide6")
    from PySide6 import QtGui, QtWidgets, QtCore
    from PySide6.QtQuick import QQuickView
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6.QtSvg import QSvgRenderer


def get_qml(path: str) -> QtCore.QUrl:
    """ Take a relative path in the qml directory and convert to a QUrl
        suitable for loading
    """
    pm_assert(
        '..' not in path,
        ValueError,
        path,
        f"Use of '..' in {path} is not allowed",
    )
    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(dirname, 'qml', path)
    pm_assert(
        os.path.isfile(path),
        FileNotFoundError,
        path,
        f'"{path}" does not exist',
    )
    return QtCore.QUrl(path)

