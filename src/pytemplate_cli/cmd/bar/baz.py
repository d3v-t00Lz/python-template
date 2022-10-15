"""

"""

from pytemplate.cmd.bar.baz import bar_baz, BazStrings


def subcommand(
    subparsers,
    func=bar_baz,
):
    parser = subparsers.add_parser(
        'baz',
        description=BazStrings.description,
    )
    parser.set_defaults(func=func)
