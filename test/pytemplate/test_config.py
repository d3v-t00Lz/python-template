"""

"""

import os
import pytest
import tempfile

from pytemplate import config


def test_singleton_file():
    config.load_config_from_file(
        '/some/fake/path/13233243',
        allow_default=True,
    )

    cfg = config.get_config()
    assert isinstance(cfg, config.Config)

    option_a = config.get_option('option_a')
    assert option_a == 'something'

    with tempfile.NamedTemporaryFile() as t:
        cfg.save_to_file(t.name)

def test_singleton_env_vars():
    environ = os.environ
    os.environ = {'OPTION_A': 'lol', 'SOMEVAR': 'value'}
    try:
        config.load_config_from_env_vars()

        cfg = config.get_config()
        assert isinstance(cfg, config.Config)

        option_a = config.get_option('option_a')
        assert option_a == 'lol'
    finally:
        os.environ = environ

def test_config_load_not_exists_no_default():
    with pytest.raises(FileNotFoundError):
        config.Config.load_from_file(
            '/some/fake/path/13233243',
            allow_default=False,
        )


def test_config_load_exists():
    dirname = os.path.dirname(__file__)
    abspath = os.path.abspath(dirname)
    path = os.path.join(
        abspath,
        'files',
        'config.yml',
    )
    config.Config.load_from_file(
        path=path,
        allow_default=False,
    )

