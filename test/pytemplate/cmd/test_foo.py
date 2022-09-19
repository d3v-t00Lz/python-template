"""

"""

import pytest

from pytemplate.cmd.foo import (
    Foo,
    foo,
)
from pytemplate.config import Config


def test_foo():
    foo(
        Foo(
            'blah',
            'blah',
            'blah',
        ),
        123,
        config=Config(),
        force=False,
    )
