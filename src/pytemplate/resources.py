try:
    from importlib.resources import files
except ImportError:  # pragma: no cover
    from importlib_resources import files


def get_resource_path(*files_path: str):
    """ Return the path to a package data file that can be opened and read

        @files_path: Iterable of path sections
    """
    path = files('pytemplate').joinpath('files', *files_path)
    if path.exists():
        return str(path)
    raise FileNotFoundError

