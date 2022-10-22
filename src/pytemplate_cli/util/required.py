"""

"""
import sys


_MSG = """
Error: you must select a subcommand.  See --help for available subcommands.
"""

def required_subcommand(**kwargs):
    print(_MSG)
    sys.exit(1)
