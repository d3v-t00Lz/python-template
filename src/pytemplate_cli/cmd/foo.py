"""

"""

from pytemplate.cmd.foo import foo, Strings
from pytemplate_cli.util import arg_force


def wrapper(*args, **kwargs):
    return 0, foo(*args, **kwargs)

def subcommand(
    subparsers,
    func=wrapper,
):
    parser = subparsers.add_parser(
        'foo',
        description=Strings.description,
    )
    parser.set_defaults(func=func)
    # All of the arguments should line up 1-to-1 with the
    # function arguments to mycmd(...)
    parser.add_argument(
        'foo',  # notice this lines up to 'foo' of mycmd()
        help=Strings.foo,
    )
    parser.add_argument(
        '-s',
        '--something',
        default=123,
        dest='something',  # notice this lines up to 'something' of mycmd()
        type=int,
        help=Strings.something,
    )
    arg_force(parser, _help=Strings.force)

