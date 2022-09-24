import importlib
import os
import sys
from typing import Optional

from pytemplate.log import LOG


def setup_vendor(module='pytemplate_vendor') -> bool:
    """ Setup Python module vendoring if present """
    try:
        vendor = importlib.import_module(module)
    except ModuleNotFoundError:
        return False

    path = vendor.__path__,
    sys.path.insert(0, path)
    LOG.info(f'Using vendored modules at {path}')
    return True

