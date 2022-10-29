from pytemplate.resources import get_resource_path
import os
import pytest


def test_get_resource_path():
    path = get_resource_path('icons', 'pytemplate.ico')
    assert os.path.isfile(path)

def test_get_resource_path_not_found():
    with pytest.raises(FileNotFoundError):
        get_resource_path('fakedir', 'fakefile')

