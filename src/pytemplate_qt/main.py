import argparse
import sys

from . import global_vars
from pytemplate.resources import get_resource_path
from pytemplate.setup import setup
from pytemplate.setup.excepthook import add_excepthook
from pytemplate.log import LOG
from .qt import (
    QApplication,
    QGuiApplication,
    QPixmap,
    QSplashScreen,
    QtCore,
)

def parse_args():
    parser = argparse.ArgumentParser("pytemplate Qt application")
    parser.add_argument(
        '--system-tray',
        '-s',
        action='store_true',
        default=False,
        dest='systray',
        help='Run as a background service in the system tray',
    )
    return parser.parse_args()

def _main_window():
    global TIMER
    from .widgets.main_window import MainWindow
    logo_path = get_resource_path('icons', 'pytemplate.png')
    pixmap = QPixmap(logo_path).scaled(
        600,
        600,
        transformMode=QtCore.Qt.TransformationMode.SmoothTransformation,
    )
    global_vars.SPLASH = QSplashScreen(pixmap)
    global_vars.SPLASH.show()
    QApplication.processEvents()
    global_vars.MAIN_WINDOW = MainWindow()
    TIMER = QtCore.QTimer()
    TIMER.setSingleShot(True)
    TIMER.timeout.connect(
        lambda: show_main_window(
            global_vars.MAIN_WINDOW,
            global_vars.SPLASH,
        )
    )
    TIMER.start(1500)

def _systray():
    QApplication.setQuitOnLastWindowClosed(False)
    from .widgets.systray import SystemTray
    global_vars.SYSTEM_TRAY = SystemTray()
    global_vars.SYSTEM_TRAY.show()

def _main(*args, **kwargs):
    args = parse_args()
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

    app = QApplication(sys.argv)

    if args.systray:
        _systray()
    else:
        _main_window()
    sys.exit(app.exec())

def show_main_window(window, splash):
    window.show()
    splash.finish(window)

def main():
    setup()
    _main()

