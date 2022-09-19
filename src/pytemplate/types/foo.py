"""

"""

from pytemplate.exc import BadArgsError


class Foo:
    """ non-sensical example class for an argparse argument type

        There is no requirement to use a class where it
        doesn't make sense, this is just for demonstration.
    """
    def __init__(
        self,
        a: str,
        b: str,
        c: str,
    ):
        self.a = a
        self.b = b
        self.c = c

    def mymethod(
        self,
        something,
    ):
        return (
            self.a,
            self.b,
            self.c,
            something,
        )

    @staticmethod
    def factory(foo: str):
        """
            @foo: str, a 3 section, ':' delimited string in the
                    format of "a:b:c"
        """
        split = foo.split(':')
        if len(split) != 3:
            raise BadArgsError(
                "'{}' was not 3 ':' delimited sections".format(foo),
            )
        a, b, c = split
        return Foo(a, b, c)

    def __eq__(self, other):
        #  Used for the unit tests
        return self.__dict__ == other.__dict__
