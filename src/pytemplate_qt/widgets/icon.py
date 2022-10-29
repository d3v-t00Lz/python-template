from pytemplate.resources import get_resource_path
from pytemplate.log import LOG
from pytemplate_qt.qt import (
    QIcon,
)


def set_icon(window):
    try:
        path = get_resource_path('icons', 'pytemplate.ico')
        window.setWindowIcon(QIcon(path))
    except FileNotFoundError:
        LOG.warning('Could not fine pytemplate.ico')

