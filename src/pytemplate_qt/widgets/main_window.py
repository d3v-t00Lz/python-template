import os
import sys

from pytemplate_qt.qt import (
    QGridLayout,
    QIcon,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)
from .icon import set_icon
from pytemplate.cmd.version import version, Strings as VersionStrings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pytemplate')
        set_icon(self)
        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)
        main_layout = QGridLayout(cen_widget)
        version_button = QPushButton("Version")
        version_button.pressed.connect(self.on_version)
        version_button.setToolTip(VersionStrings.description)
        main_layout.addWidget(version_button, 0, 0)

    def on_version(self):
        QMessageBox.information(self, "Version", version(None))

