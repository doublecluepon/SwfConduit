
# First, load our server module
from swfconduit.server import Server


# Give our server module to swfconduit and start the server
from swfconduit.loader import Loader

loader  = Loader()
loader.add_server(
    {
        "port": 8000,
        "proto": "tcp",
        "server": Server(),
    }
)
application = loader.get_application()

