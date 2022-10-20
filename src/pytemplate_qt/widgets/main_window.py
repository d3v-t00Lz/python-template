import os
import sys

from pytemplate_qt.qt import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)
from pytemplate.cmd.version import version, VersionStrings

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('pytemplate')
        self.set_icon()
        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)
        main_layout = QGridLayout(cen_widget)
        version_button = QPushButton("Version")
        version_button.pressed.connect(self.on_version)
        version_button.setToolTip(VersionStrings.description)
        main_layout.addWidget(version_button, 0, 0)

    def on_version(self):
        QMessageBox.information(self, "Version", version(None))

    def set_icon(self):
        try:
            import importlib.resources as importlib_resources
        except ImportError:
            import importlib_resources
        # setuptools package
        path = importlib_resources.files(
            'pytemplate'
        ) / 'files' / 'icons' / 'pytemplate.ico'
        path = str(path)
        print(path)
        if os.path.exists(path):
            self.setWindowIcon(QIcon(path))
            return
        for path in (
            # Windows
            os.path.join(
                os.path.dirname(sys.executable),
                'pytemplate.ico',
            ),
            # MacOS
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'Resources',
                'files',
                'icons',
                'pytemplate.ico',
            ),
            # Devel
            os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                '..',
                'files',
                'icons',
                'pytemplate.ico',
            ),
        ):
            path = os.path.abspath(path)
            if os.path.exists(path):
                self.setWindowIcon(path)
                return

