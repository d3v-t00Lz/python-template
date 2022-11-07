import sys
from pytemplate.log import LOG
from pytemplate.resources import get_resource_path
from pytemplate_qt import global_vars
from pytemplate_qt.qt import (
    QIcon,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
)
from .main_window import MainWindow

class SystemTray(QSystemTrayIcon):
    def __init__(self):
        path = get_resource_path('icons', 'pytemplate-systray.png')
        self.icon = QIcon(path)
        super().__init__(self.icon)
        # This may not be reliably triggered on all platforms, a known
        # limitation of QSystemTrayIcon
        self.messageClicked.connect(self.message_clicked)
        self.activated.connect(self._activated)
        self.menu = QMenu()
        action = self.menu.addAction('Show a message')
        action.triggered.connect(
            lambda x: self.showMessage("pytemplate", "Hello!", self.icon)
        )
        action = self.menu.addAction('Show the main window')
        action.triggered.connect(
            lambda x: self.show_main_window()
        )
        action = self.menu.addAction('Close')
        action.triggered.connect(
            lambda x: sys.exit(0)
        )
        self.setContextMenu(self.menu)

    def show_main_window(self):
        # Must be assigned somewhere or it gets garbage collected immediately
        global_vars.MAIN_WINDOW = MainWindow()
        global_vars.MAIN_WINDOW.show()

    def _activated(self, reason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.Unknown,
        ):
            QMessageBox.information(
                None,
                "pytemplate",
                "You clicked the message or icon",
            )
        else:
            LOG.info(f'_activated({reason})')

    def message_clicked(self):
        QMessageBox.information(
            None,
            "pytemplate",
            "You clicked the message or icon",
        )

