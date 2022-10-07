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
        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)
        main_layout = QGridLayout(cen_widget)
        version_button = QPushButton("Version")
        version_button.pressed.connect(self.on_version)
        version_button.setToolTip(VersionStrings.main)
        main_layout.addWidget(version_button, 0, 0)

    def on_version(self):
        QMessageBox.information(self, "Version", version(None))


