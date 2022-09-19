from pytemplate.log import _excepthook, setup_logging
import sys

def test_setup_logging():
    setup_logging()

def test_except_hook():
    try:
        raise Exception
    except:
        args = sys.exc_info()
        _excepthook(*args)

