from pytemplate.types.foo import Foo

def test_foo_mymethod():
    f = Foo.factory('a:b:c')
    assert f.mymethod('d') == ('a', 'b', 'c', 'd')

def test_foo_eq():
    f1 = Foo.factory('a:b:c')
    f2 = Foo.factory('a:b:c')
    assert f1 == f2, (f1.__dict__, f2.__dict__)

