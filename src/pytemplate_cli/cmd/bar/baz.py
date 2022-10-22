"""

"""

from pytemplate.cmd.bar.baz import bar_baz, Strings

def wrapper(*args, **kwargs):
    return 0, bar_baz(*args, **kwargs)

def subcommand(
    subparsers,
    func=wrapper,
):
    parser = subparsers.add_parser(
        'baz',
        description=Strings.description,
    )
    parser.set_defaults(func=func)
