try:
    from importlib.resources import files
except ImportError:  # pragma: no cover
    from importlib_resources import files
import os


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
    ):
        if os.path.exists(path):
            return os.path.abspath(path)

    raise FileNotFoundError

