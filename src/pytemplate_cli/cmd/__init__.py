"""
    Contains the commands, functions that perform an action

    Also contains parsers used by the 'cli' module, can contain other code
    required for other interfaces such as REST APIs

    Follows the general format:
    1. one function (or command) per submodule
    2. one parser-creating function per submodule

    Command function:
    1. Function arguments must match exactly the name of all argument
       fields created by the parser-creating function, including any
       fields created by parent parsers.  Specifically the 'dest' argument of
       parser.add_argument.
    2. Should make use of library classes and functions created elsewhere
       in new submodules of the package, the command function itself should
       be small.
    3. The submodule structure should follow the hierarchy of the command, ie:
           `myscript cmd1 cmd2 cmd3` -> `/cmd/cmd1/cmd2/cmd3.py`

    Parser-creating function:
    1. Must create all arguments to the command function with the exact
       same names and appropriate types (see Command function #1 above).
    2. Functions to create arguments that are re-usable should be created
       instead of creating global arguments in a parent parser that are not
       used globally among the children parsers.

"""

from .bar import _cli_bar
from .foo import _cli_foo
from .version import _cli_version

def cli_subcommands(subparsers):
    for func in (
        _cli_bar,
        _cli_foo,
        _cli_version,
    ):
        func(subparsers)

__all__ = [
    'subcommands',
]
