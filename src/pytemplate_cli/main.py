"""

"""

import copy
import sys
from typing import List, Optional

# For the singleton config access pattern
# from pytemplate.config import load_config

from pytemplate.setup import setup

def main(
    _args: Optional[List[str]]=None,
):
    setup()
    # After calling setup
    from .args import parse_args
    args = parse_args(_args)
    kwargs = copy.copy(args.__dict__)
    # For the singleton config access pattern
    # config_path = kwargs.pop('config')
    # load_config(config_path)
    func = kwargs.pop('func')
    retcode, result = func(**kwargs)
    if result:
        print(result)
    sys.exit(retcode)

