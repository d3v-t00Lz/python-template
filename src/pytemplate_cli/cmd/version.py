"""

"""

from pytemplate.cmd.version import version, VersionStrings


def _cli_version(
    subparsers,
    func=version,
):
    parser = subparsers.add_parser(
        'version',
        description=VersionStrings.main,
    )
    parser.set_defaults(func=func)

