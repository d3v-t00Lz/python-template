"""

"""

from pytemplate.config import Config

class Strings:
    description = 'It does something'

def bar_baz(
    config: Config,
):
    return "bar baz " + config.option_a

