"""

"""

from pytemplate.cmd.bar.baz import bar_baz, BazStrings


def parse_baz(
    subparsers,
    func=bar_baz,
):
    parser = subparsers.add_parser(
        'baz',
        description=BazStrings.main,
    )
    # main will call func() if this command is selected
    parser.set_defaults(func=func)
