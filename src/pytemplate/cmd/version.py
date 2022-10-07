"""

"""

from pytemplate import __version__
from pytemplate.config import Config

class VersionStrings:
    main = 'Show the package version'

def version(
    config: Config,
):
    return __version__
