from threading import Thread

from pytemplate_rest import main

class MockApp:
    def __init__(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

def test_main():
    app = main.APP
    main.APP = MockApp()
    main.main()
    main.APP = app

