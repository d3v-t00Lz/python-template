"""

"""

from pytemplate.cmd.version import version, Strings


def subcommand(
    subparsers,
    func=version,
):
    parser = subparsers.add_parser(
        'version',
        description=Strings.description,
    )
    parser.set_defaults(func=func)

