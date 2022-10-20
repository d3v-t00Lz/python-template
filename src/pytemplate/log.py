"""
    Provides logging functionality
"""

import logging
import logging.handlers
import sys
from platform import platform



__all__ = [
    'LOG',
]

LOG: logging.Logger = logging.getLogger(__name__)
_FORMAT = (
    '[%(asctime)s] %(levelname)s %(pathname)-30s: %(lineno)s - %(message)s'
)

def setup_logging(
    format: str=_FORMAT,
    level: int=logging.INFO,
    log: logging.Logger=LOG,
    stream=sys.stdout,
    structured=True,
    log_file=None,
    log_file_max_bytes=1024*1024,
    log_file_backup_count=5,
):
    if structured:
        from pylogrus import PyLogrus, TextFormatter
        logging.setLoggerClass(PyLogrus)
        fmt = TextFormatter(
            datefmt='Z',
            colorize=not platform().startswith('Windows'),
        )
    else:
        fmt = logging.Formatter(format)

    log.setLevel(level)

    if stream:
        handler = logging.StreamHandler(
            stream=stream,
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

    if log_file:
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=log_file_max_bytes,
            backupCount=log_file_backup_count,
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

