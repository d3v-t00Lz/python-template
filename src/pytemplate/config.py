"""
    Implementation of a config file, with environment variable overrides,
    can be configured completely with env. vars. or with a file.
"""

import copy
import os
from typing import Optional

# JSON is compatible with YAML, you can use either format
from pymarshal.json import type_assert, unmarshal_json, marshal_json
import yaml


# CLI arg access:
__all__ = [
    'Config',
]

# Singleton access:
#__all__ = [
#    'get_config',
#    'get_option',
#]


class Config:
    def __init__(
        self,
        option_a: str="something",
    ):
        """ To load purely from environment variables, simply call Config()
            with no arguments.  Otherwise, call load_from_file() instead.
            All arguments should have a default value, or None for all
            mandatory config values, env_var='some_string', and
            allow_none=False.

            @option_a: some config file option
        """
        self.option_a = type_assert(
            option_a,
            str,
            env_var='OPTION_A',
            allow_none=False,
        )

    def save_to_file(self, path: str):
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        y = marshal_json(self)
        with open(path, 'w') as f:
            yaml.safe_dump(y, f)

    @staticmethod
    def load_from_file(
        path: str='/etc/pytemplate/config.yml',
        allow_default: bool=False,
    ):
        exists = os.path.exists(path)

        if not exists:
            if allow_default:
                return Config()  # default options
            else:
                raise FileNotFoundError(path)

        with open(path) as f:
            y = yaml.safe_load(f)
        assert isinstance(y, dict), y

        return unmarshal_json(y, Config)


_CONFIG: Optional[Config] = None

# Functions for the singleton access pattern

def load_config_from_file(
    path: str='/etc/pytemplate/config.yml',
    allow_default: bool=False,
):
    global _CONFIG
    _CONFIG = Config.load_from_file(
        path=path,
        allow_default=allow_default,
    )

def load_config_from_env_vars():
    global _CONFIG
    _CONFIG = Config()


def get_config():
    return copy.deepcopy(_CONFIG)


def get_option(name):
    attr = getattr(_CONFIG, name)
    return copy.deepcopy(attr)
