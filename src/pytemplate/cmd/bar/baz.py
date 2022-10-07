"""

"""

from pytemplate.config import Config

class BazStrings:
    main = 'It does something'

def bar_baz(
    config: Config,
):
    return "bar baz " + config.option_a

