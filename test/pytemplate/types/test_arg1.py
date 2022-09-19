"""

"""
import pytest

from pytemplate.types.foo import Foo
from pytemplate.exc import BadArgsError


def test_foo_mymethod():
    # Nonsensical unit test for a nonsensical class and method
    a = Foo('a', 'b', 'c')
    a.mymethod('lol')


def test_foo_factory_assertion_error():
    with pytest.raises(BadArgsError):
        Foo.factory('lol:only2')
