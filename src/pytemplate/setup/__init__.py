from pytemplate.config import load_config_from_file
from pytemplate.log import setup_logging
from .excepthook import add_excepthook
from .vendor import setup_vendor

def setup(excepthook=None):
    """ Global setup function for any client of the library """
    if excepthook:
        add_excepthook(excepthook)
    setup_logging()
    setup_vendor()
    # TODO: Change to from env vars if that makes sense for the application
    load_config_from_file(allow_default=True)
