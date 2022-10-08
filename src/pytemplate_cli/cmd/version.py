"""

"""

from pytemplate.cmd.version import version, VersionStrings


def parse_version(
    subparsers,
    func=version,
):
    parser = subparsers.add_parser(
        'version',
        description=VersionStrings.description,
    )
    parser.set_defaults(func=func)

