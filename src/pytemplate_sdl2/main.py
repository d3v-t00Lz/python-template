import argparse
from platform import platform
import os
import sys


EV = 'PYSDL2_DLL_PATH'

def parse_args():
    parser = argparse.ArgumentParser("pytemplate SDL2 application")
    return parser.parse_args()

def platform_check():
    """ On Windows, we copy the SDL2 dlls to the same folder as the executable
        therefore we must set the environment variable to that path before
        importing PySDL2
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
        if (
            platform().lower().startswith('windows')
            and
            EV not in os.environ
        ):
            os.environ[EV] = os.path.dirname(sys.executable)

parse_args()
platform_check()

# Now import this with EV set if needed

def main():
    from .pong import main as _main
    _main()

