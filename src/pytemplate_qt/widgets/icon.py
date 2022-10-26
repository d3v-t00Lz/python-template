import os
import sys

from pytemplate_qt.qt import (
    QIcon,
)


def set_icon(window):
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
        window.setWindowIcon(QIcon(path))
        return
    for path in (
        # Windows
        os.path.join(
            os.path.dirname(sys.executable),
            '..',
            'pytemplate.ico',
        ),
        # MacOS
        os.path.join(
            os.path.dirname(sys.executable),
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
            window.setWindowIcon(QIcon(path))
            return


