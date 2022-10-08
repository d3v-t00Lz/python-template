"""

"""

import pytest

from pytemplate.cmd.foo import foo
from pytemplate.config import Config


def test_foo():
    foo(
        "blah",
        123,
        config=Config(),
        force=False,
    )
