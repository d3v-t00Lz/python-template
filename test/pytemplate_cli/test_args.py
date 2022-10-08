"""

"""

import pytest

from pytemplate_cli.args import parse_args


def test_parse_args():
    for _args, expected in [
        (
            [
                'foo',
                'some:value:blah',
            ],
            {
                'foo': 'some:value:blah',
            },
        ),
    ]:
        args = parse_args(
            _args=_args,
        )
        for k, v in expected.items():
            assert (
                getattr(args, k) == v
            ), (args.__dict__, k, v)


def test_parse_args_raises():
    for _args, exc in [
        (
            [
                'foo',
                'too',
                'many',
                'args',
            ],
            SystemExit,
        ),
    ]:
        with pytest.raises(exc):
            parse_args(
                _args=_args,
            )
