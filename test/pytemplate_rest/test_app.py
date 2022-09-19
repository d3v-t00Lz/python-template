from pytemplate_rest.app import APP

def test_version():
    request, response = APP.test_client.get('/version')
    assert 'version' in response.json
