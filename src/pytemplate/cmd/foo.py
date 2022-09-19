"""

"""

from pytemplate.config import Config
from pytemplate.types import Foo


# Note that if the command line parser specifies any global arguments,
# those too must be represented in the arguments of mycmd()
def foo(
    foo: Foo,
    something: int,
    config: Config,
    force: bool,
):
    """
        @foo:       a class instance of Foo
        @something: some integer value
        @config:    the configuration file
        @force:     foo regardless of any bar baz
    """
    return foo.mymethod(something)

