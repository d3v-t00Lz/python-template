from pytemplate.log import setup_logging
from .vendor import setup_vendor

def setup():
    """ Global setup function for any client of the library """
    setup_logging()
    setup_vendor()

