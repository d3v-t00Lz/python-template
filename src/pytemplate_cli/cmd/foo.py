"""

"""

from pytemplate.cmd.foo import foo, FooStrings
from pytemplate_cli.util import arg_force
from pytemplate.types import Foo


def parse_foo(
    subparsers,
    func=foo,
):
    parser = subparsers.add_parser(
        'foo',
        description=FooStrings.description,
    )
    parser.set_defaults(func=func)
    # All of the arguments should line up 1-to-1 with the
    # function arguments to mycmd(...)
    parser.add_argument(
        'foo',  # notice this lines up to 'foo' of mycmd()
        type=Foo.factory,
        help=FooStrings.foo,
    )
    parser.add_argument(
        '-s',
        '--something',
        default=123,
        dest='something',  # notice this lines up to 'something' of mycmd()
        type=int,
        help=FooStrings.something,
    )
    arg_force(parser, _help=FooStrings.force)

