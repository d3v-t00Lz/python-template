import sys
import traceback

from pytemplate.log import LOG

def add_excepthook(hook):
    if hook:
        EXCEPTHOOKS.append(hook)

def _excepthook(exc_type, exc_value, tb):
    for hook in EXCEPTHOOKS:
        try:
            hook(exc_type, exc_value, tb)
        except Exception as ex:
            LOG.exception(ex)

sys.excepthook = _excepthook

def log_excepthook(exc_type, exc_value, tb):
    exc = traceback.format_exception(exc_type, exc_value, tb)
    LOG.error("\n".join(exc))

EXCEPTHOOKS = [
    log_excepthook,
]

__all__ = [
    'add_excepthook',
]
