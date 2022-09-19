"""
    Provides logging functionality
"""

import logging
import sys
import traceback

from pylogrus import PyLogrus, TextFormatter


__all__ = [
    'LOG',
]

LOG: logging.Logger = logging.getLogger(__name__)
#_FORMAT = (
#    '[%(asctime)s] %(levelname)s %(pathname)-30s: %(lineno)s - %(message)s'
#)

def setup_logging(
    #format: str=_FORMAT,
    level: int=logging.INFO,
    log: logging.Logger=LOG,
    stream=sys.stdout,
):
    logging.setLoggerClass(PyLogrus)

    handler = logging.StreamHandler(
        stream=stream,
    )
    fmt = TextFormatter(datefmt='Z', colorize=True)
    # fmt = logging.Formatter(format)
    handler.setFormatter(fmt)
    log.addHandler(handler)
    log.setLevel(level)
    sys.excepthook = _excepthook

def _excepthook(exc_type, exc_value, tb):
    exc = traceback.format_exception(exc_type, exc_value, tb)
    LOG.error("\n".join(exc))

