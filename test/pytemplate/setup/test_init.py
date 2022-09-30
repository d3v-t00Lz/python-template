from pytemplate.setup import setup

def test_setup():
    def fake_excepthook(*args, **kwargs):
        pass

    setup(fake_excepthook)
