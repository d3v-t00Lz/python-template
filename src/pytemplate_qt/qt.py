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


from qtpy import QtGui, QtWidgets, QtCore
from qtpy.QtQuick import QQuickView
from qtpy.QtCore import Signal, Slot
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtSvg import QSvgRenderer


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

