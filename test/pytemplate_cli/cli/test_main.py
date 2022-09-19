"""

"""

import pytest

from pytemplate_cli.main import main


def test_main():
    for _args in (
        [
            'version',
        ],
    ):
        main(
            _args=_args,
        )


def test_main_raises():
    for _args, exc in [
        (
            [],  # require_subcommands should trigger exit(1)
            SystemExit,
        )
    ]:
        with pytest.raises(exc):
            main(_args=_args)
