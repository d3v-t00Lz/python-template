"""
Parse command line arguments using the subcommands defined in the cmd module
"""

import argparse
import sys
from typing import List, Optional

from pytemplate_cli.cmd import cli_subcommands
from pytemplate_cli.util import required_subcommand
from pytemplate.config import Config


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=required_subcommand)
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

    cli_subcommands(subparsers)
    return parser

def parse_args(
    _args: Optional[List[str]]=None,
):
    parser = arg_parser()
    return parser.parse_args(_args)

