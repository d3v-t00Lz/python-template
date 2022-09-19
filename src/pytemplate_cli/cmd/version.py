"""

"""

from pytemplate.cmd.version import version


def _cli_version(
    subparsers,
    func=version,
):
    parser = subparsers.add_parser(
        'version',
        help='Print the package version and exit.'
    )
    parser.set_defaults(func=func)
