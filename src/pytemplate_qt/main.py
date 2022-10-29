import argparse
import sys

from . import global_vars
from pytemplate.resources import get_resource_path
from pytemplate.setup import setup
from pytemplate.setup.excepthook import add_excepthook
from pytemplate.log import LOG

def parse_args():
    parser = argparse.ArgumentParser("pytemplate Qt application")
    return parser.parse_args()

def _main(*args, **kwargs):
    # Before Qt imports, to ensure that we can log the outcome
    from .qt import (
        QApplication,
        QGuiApplication,
        QPixmap,
        QSplashScreen,
        QtCore,
    )
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

    logo_path = get_resource_path('icons', 'pytemplate.png')
    pixmap = QPixmap(logo_path).scaled(
        600,
        600,
        transformMode=QtCore.Qt.TransformationMode.SmoothTransformation,
    )
    splash = QSplashScreen(pixmap)
    splash.show()
    QApplication.processEvents()
    window = MainWindow()
    timer = QtCore.QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(
        lambda: show_main_window(window, splash)
    )
    timer.start(2000)
    global_vars.MAIN_WINDOW = window
    sys.exit(app.exec())

def show_main_window(window, splash):
    window.show()
    splash.finish(window)

def main():
    parse_args()
    setup()
    _main()

