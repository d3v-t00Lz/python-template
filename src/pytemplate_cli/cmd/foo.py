"""

"""

from pytemplate.cmd.foo import foo
from pytemplate_cli.util import arg_force
from pytemplate.types import Foo


def _cli_foo(
    subparsers,
    func=foo,
):
    parser = subparsers.add_parser(
        'foo',
        help='A subcommand that does something'
    )
    # main will call func() if this command is selected
    parser.set_defaults(func=func)
    # All of the arguments should line up 1-to-1 with the
    # function arguments to mycmd(...)
    parser.add_argument(
        'foo',  # notice this lines up to 'foo' of mycmd()
        type=Foo.factory,
        help=(
            'Some required command line argument, in the format '
            'something:something:something'
        ),
    )
    parser.add_argument(
        '-s',
        '--something',
        default=123,
        dest='something',  # notice this lines up to 'something' of mycmd()
        type=int,
        help='Some command line option'
    )
    arg_force(
        parser,
    )
