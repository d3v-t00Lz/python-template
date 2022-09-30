from pytemplate.log import setup_logging
from .excepthook import add_excepthook
from .vendor import setup_vendor

def setup(excepthook=None):
    """ Global setup function for any client of the library """
    if excepthook:
        add_excepthook(excepthook)
    setup_logging()
    setup_vendor()

