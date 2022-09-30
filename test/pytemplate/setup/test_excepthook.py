import sys

from pytemplate.setup.excepthook import _excepthook, add_excepthook


def test_except_hook():
    def excepthook_raises(x, y, z):
        raise Exception((x, y, z))

    add_excepthook(excepthook_raises)
    try:
        raise Exception
    except:
        args = sys.exc_info()
        _excepthook(*args)

