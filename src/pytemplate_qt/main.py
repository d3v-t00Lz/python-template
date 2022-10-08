import argparse
import sys

from . import global_vars
from pytemplate.setup import setup
from pytemplate.setup.excepthook import add_excepthook
from pytemplate.log import LOG

def parse_args():
    parser = argparse.ArgumentParser("pytemplate Qt application")
    return parser.parse_args()

def main():
    parse_args()
    # Before Qt imports, to ensure that we can log the outcome
    setup()
    from .qt import QApplication, QGuiApplication, QtCore
    try:
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
            QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
        )
    except Exception as ex:
        LOG.warning(
            "Unable to set "
            "QGuiApplication.setHighDpiScaleFactorRoundingPolicy"
            f" {ex}"
        )
    from .widgets.excepthook import qt_excepthook
    add_excepthook(qt_excepthook)

    from .widgets.main_window import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    global_vars.MAIN_WINDOW = window
    sys.exit(app.exec())
