"""

"""

from pytemplate_cli.util import required_subcommand


def subparsers(
   subparsers,
):
    parser = subparsers.add_parser(
        'bar',
        description='A subcommand that does something'
    )
    parser.set_defaults(func=required_subcommand)
    return parser.add_subparsers(
        description='Subcommands (required)',
    )
