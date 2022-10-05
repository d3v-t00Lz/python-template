from pytemplate.os import *
import pytest


def test_get_os():
    for _platform, expected in (
        ('linux', OperatingSystem.LINUX),
        ('macos', OperatingSystem.MACOS),
        ('windows', OperatingSystem.WINDOWS),
    ):
        result = get_os(_platform)
        assert result == expected, (result, expected)

def test_get_os_fail():
    with pytest.raises(NotImplementedError):
        get_os('freebsd-15.03')
