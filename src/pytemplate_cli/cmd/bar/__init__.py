"""

"""

from .baz import parse_baz
from pytemplate_cli.util import required_subcommand


def parse_bar(
   subparsers,
):
    parser = subparsers.add_parser(
        'bar',
        description='A subcommand that does something'
    )
    parser.set_defaults(func=required_subcommand)
    subparsers2 = parser.add_subparsers(
        description='Subcommands (required)',
    )
    parse_baz(subparsers2)
