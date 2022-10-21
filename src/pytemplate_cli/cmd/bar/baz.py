"""

"""

from pytemplate.cmd.bar.baz import bar_baz, Strings


def subcommand(
    subparsers,
    func=bar_baz,
):
    parser = subparsers.add_parser(
        'baz',
        description=Strings.description,
    )
    parser.set_defaults(func=func)
