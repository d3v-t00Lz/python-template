"""

"""

from pytemplate.cmd.version import version, Strings


def wrapper(*args, **kwargs):
    return 0, version(*args, **kwargs)

def subcommand(
    subparsers,
    func=wrapper,
):
    parser = subparsers.add_parser(
        'version',
        description=Strings.description,
    )
    parser.set_defaults(func=func)

