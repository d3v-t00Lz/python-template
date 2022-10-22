"""
Parse command line arguments using the subcommands defined in the cmd module
"""

import argparse
import importlib
import pkgutil
import sys
from typing import List, Optional

from pytemplate_cli.util import required_subcommand
from pytemplate.config import Config


def recurse_modules(
    subparsers,
    root_name: str='pytemplate_cli.cmd',
):
    """ Recursively add subcommands to an argparse.ArgumentParser
        Any submodules should have a function called subcommand that
        adds a parser to @subparsers.  Any folder should contain in
        it's __init__.py a function called subparsers that creates a
        parser and returns it's subparsers
    """
    root_mod = importlib.import_module(root_name)
    for sub_info in pkgutil.iter_modules(root_mod.__path__):
        sub_name = '.'.join((root_name, sub_info.name))
        sub_mod = importlib.import_module(sub_name)
        if sub_info.ispkg:
            child_subparsers = sub_mod.subparsers(subparsers)
            recurse_modules(child_subparsers, sub_name)
        else:
            sub_mod.subcommand(subparsers)

def arg_parser(
    default_func=required_subcommand,
):
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)
    subparsers = parser.add_subparsers(
        help='Subcommands',
    )
    # Any arguments created with parser.add_argument here must be consumed
    # by all cmd.* funcs
    parser.add_argument(
        '-c',
        '--config',
        default=Config(),
        dest='config',
        type=lambda x: Config.load_from_file(x, allow_default=True),
        # For the singleton config access pattern:
        # type=str,
        help=(
            'The path to a config file.  Default values will '
            'be used if it does not exist.'
        ),
    )

    recurse_modules(subparsers)
    return parser

def parse_args(
    _args: Optional[List[str]]=None,
    default_func=required_subcommand,
):
    """
    @default_func:
        The function to call when the CLI is invoked without a subcommand.
        Default: Show an error message.  To use this with other interfaces
        like the Qt GUI, pass in the main() function of that interface.
    """
    parser = arg_parser(default_func)
    return parser.parse_args(_args)

