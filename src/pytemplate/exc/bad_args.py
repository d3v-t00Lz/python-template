"""

"""
from typing import Union

class BadArgsError(Exception):
    """ Raised when bad arguments are given

    """
    def __init__(
        self,
        msg: Union[str, dict],
    ):
        """
            @msg:   str, A message describing why the CLI args were invalid
        """
        Exception.__init__(self)
        self.msg = msg

    def print_msg(self):
        print(
            "Invalid command line argument: {}".format(
                self.msg,
            )
        )
