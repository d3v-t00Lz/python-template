import os
import sys
import tempfile

from pytemplate.log import setup_logging

def test_setup_logging():
    for kwargs in (
        {
            'log_file': os.path.join(
                tempfile.gettempdir(),
                'pytemplate_test_log_file_setup_logging.log',
            ),
        },
        {
            'structured': False,
        },
    ):
        setup_logging(**kwargs)

