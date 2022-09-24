import sys

from pytemplate.setup.vendor import setup_vendor

def test_found():
    try:
        result = setup_vendor('urllib3')
        assert result, result
    finally:
        sys.path.pop(0)

def test_not_found():
    result = setup_vendor('Faak3m0djuel')
    assert not result, result

