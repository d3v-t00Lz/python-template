"""
    Module for operating system specific quirks
"""

from enum import Enum
import platform


class OperatingSystem(Enum):
    """ Enum of supported OS for this project """
    LINUX = 0
    WINDOWS = 1
    MACOS = 2

def get_os(
    _platform: str = platform.platform(),
) -> OperatingSystem:
    _platform = _platform.lower()
    if _platform.startswith('linux'):
        return OperatingSystem.LINUX
    if _platform.startswith('windows'):
        return OperatingSystem.WINDOWS
    if _platform.startswith('macos'):
        return OperatingSystem.MACOS
    raise NotImplementedError(_platform)


# Add your own quirks here

__all__ = [
    'OperatingSystem',
    'get_os',
]

