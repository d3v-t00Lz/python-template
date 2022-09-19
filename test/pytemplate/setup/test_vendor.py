import os
import tempfile

from pytemplate.setup.vendor import setup_vendor

def test_dev():
    with tempfile.TemporaryDirectory() as d:
        current = os.path.join(d, '0', '1')
        vendor = os.path.join(d, 'vendor')
        os.makedirs(current)
        os.makedirs(vendor)
        result = setup_vendor(current)
        assert result == 'dev', (result, current, vendor)

def test_system():
    with tempfile.TemporaryDirectory() as d:
        current = os.path.join(d, '0', '1', '2', '3', '4')
        vendor = os.path.join(d, 'pytemplate', 'vendor')
        os.makedirs(current)
        os.makedirs(vendor)
        result = setup_vendor(current)
        assert result == 'system', (result, current, vendor)

def test_none():
    result = setup_vendor('/')
    assert result is None, result

