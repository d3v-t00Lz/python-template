import sys

from pytemplate.setup import setup

def main():
    # Before Qt imports, to ensure that we can log the outcome
    setup()
    from .qt import QApplication
    from .widgets.main_window import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
