
import sys
import ConfigParser
import twisted.application.internet
import dcserver.factory
import dcserver.socketpolicy
from twisted.python import log

cfg = ConfigParser.SafeConfigParser()

def _get_mod(modulePath):
    try:
        aMod = sys.modules[modulePath]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        aMod = __import__(modulePath, globals(), locals(), [''])
        sys.modules[modulePath] = aMod
    return aMod

def add_services( service_parent ):
    """ Add services to the given twisted service_parent """

    # Create the service to serve the socket policy
    dcserver.socketpolicy.add_service( service_parent )

    # Each section defines a plugin
    for sect in cfg.sections():
        # Start the appropriate listeners and set up connection handlers
        port    = cfg.getint( sect, "port" )
        proto   = cfg.get( sect, "proto" )

        module  = _get_mod( cfg.get( sect, "package" ) )

        # Collect all the configuration
        server_config = {}
        for key, value in cfg.items( sect ):
            server_config[key] = value

        # Init a new server
        server  = module.Server(server_config)

        # Initialize a new factory for every server
        factory = dcserver.factory.Factory(server)

        if "tcp" in proto:
            # Add a TCP listener to our server
            twisted.application.internet.TCPServer( port, factory ).setServiceParent( service_parent )


def load_config(filename):
    """ Load the configuration file """
    cfg.readfp( open( filename ) )


