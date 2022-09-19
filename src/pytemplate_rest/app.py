from sanic import Sanic
from sanic.response import json
from pytemplate.cmd.version import version

APP = Sanic("pytemplate")

@APP.get("/version")
async def async_handler(request):
    return json({
        'version': version(None),
    })

