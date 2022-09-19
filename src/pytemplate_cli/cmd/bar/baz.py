"""

"""

from pytemplate.cmd.bar.baz import bar_baz


def _cli_bar_baz(
    subparsers,
    func=bar_baz,
):
    parser = subparsers.add_parser(
        'baz',
        help='A subcommand that does something'
    )
    # main will call func() if this command is selected
    parser.set_defaults(func=func)
