"""

"""

from pytemplate.config import Config


class Strings:
    description = "Do the foo thing"
    foo = 'Some required argument, in the format something:something:something'
    something = "Some integer number"
    force = "Foo no matter what"

# Note that if the command line parser specifies any global arguments,
# those too must be represented in the arguments of mycmd()
def foo(
    foo: str,
    something: int,
    config: Config,
    force: bool,
):
    """
        @foo:       some string
        @something: some integer
        @config:    the configuration file
        @force:     foo regardless of any bar baz
    """
    return f'{foo} {something}'
