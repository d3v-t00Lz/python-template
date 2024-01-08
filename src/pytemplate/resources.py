# type: ignore
try:
    from importlib.resources import files
except ImportError:  # pragma: no cover
    from importlib_resources import files
import os
import sys

FILES_DIR = None

def set_files_dir():
    global FILES_DIR
    path = files('pytemplate').joinpath('files')
    if path.exists():
        FILES_DIR = str(path)
        return
    for path in(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'files',
        ),
        os.path.join(
            os.path.dirname(sys.executable),
            'files',
        ),
        os.path.join(
            os.path.dirname(sys.executable),
            '..',
            'Resources',
            'files',
        ),
        # Running Nuitka build from the dist folder
        os.path.join(
            os.path.dirname(sys.executable),
            '..',
            '..',
            'files',
        ),
    ):
        print(path)
        if os.path.isdir(path):
            FILES_DIR = os.path.abspath(path)
            return
    raise FileNotFoundError

set_files_dir()

def get_resource_path(*files_path: str):
    """ Return the path to a package data file that can be opened and read

        @files_path: Iterable of path sections
    """
    path = files('pytemplate').joinpath('files', *files_path)
    if path.exists():
        return str(path)
    for path in(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'files',
            *files_path,
        ),
        os.path.join(
            os.path.dirname(sys.executable),
            'files',
            *files_path,
        ),
        os.path.join(
            os.path.dirname(sys.executable),
            '..',
            'Resources',
            'files',
            *files_path,
        ),
        # Running Nuitka build from the dist folder
        os.path.join(
            os.path.dirname(sys.executable),
            '..',
            '..',
            'files',
            *files_path,
        ),
    ):
        print(path)
        if os.path.exists(path):
            return os.path.abspath(path)

    raise FileNotFoundError

