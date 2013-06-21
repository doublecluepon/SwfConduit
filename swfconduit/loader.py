#-----------------------------------------------------------------------------
# Copyright (c) 2010 Double Cluepon Software

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

"""
Load all the swfconduit plugins and prepare for running

The loader reads the config file, loads the server packages, creates the 
swfconduit Server and Twisted Factory, and sets everything up for the 
twistd daemon.
"""

import sys, types
import ConfigParser
import twisted.application.internet
import twisted.application.service
import swfconduit.server
import swfconduit.socketpolicy
from twisted.python import log

def _get_mod(modulePath):
    """ Load and return the given module """
    try:
        # Check if it's already loaded
        aMod = sys.modules[modulePath]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # Not loaded, load it
        # The last [''] is very important!
        aMod = __import__(modulePath, globals(), locals(), [''])
        sys.modules[modulePath] = aMod
    return aMod

class Loader( object ):
    """ Load up a swfconduit 

    This class creates all the Twisted services needed to run the SwfConduit server.
    """

    servers = []
    """ The list of servers we made """

    def add_server( self, config ):
        """Create the server from the given config

        Valid configuration keys are:

        * server    The swfconduit.server.Server instance to add.
        * proto     The protocol this server uses. Currently only "tcp" is supported.
        * port      The port this server should listen on.
        """
        # Start the appropriate listeners and set up connection handlers
        if "package" in config: # package is deprecated and will be removed
            module  = _get_mod( config["package"] )
            cls = module.Server
            # Init a new server
            server = cls(config)
        elif "server" in config:
            assert isinstance( config['server'], swfconduit.server.Server )
            server = config["server"]
        self.servers.append( {
            "port": config['port'],
            "proto": config['proto'],
            "server": server,
        } )

    def add_services( self, service_parent ):
        """ Add services to the given twisted service_parent.

        This method is called automatically by get_application().
        """

        # Create the service to serve the socket policy
        swfconduit.socketpolicy.add_service( service_parent, './socket-policy.xml' )

        for server in self.servers:
            port    = int(server["port"])
            proto   = server["proto"]
            if "tcp" in proto:
                # Add a TCP listener to our server
                twisted.application.internet.TCPServer( port, server['server'] ).setServiceParent( service_parent )

    def load_from_config( self, filename ):
        """ Load settings from the configuration file """
        cfg = ConfigParser.SafeConfigParser()
        cfg.readfp( open( filename ) )

        # Each section defines a plugin
        for sect in cfg.sections():
            # Collect all the configuration
            config  = {}
            for key, value in cfg.items( sect ):
                config[key] = value
            self.add_server( config )

    def get_application( self ):
        """ Get the twisted application with all the plugin services added.

        This should be the last thing you do in your twisted.tac file.
        """
        service_parent = twisted.application.service.MultiService()

        self.add_services( service_parent )

        application = twisted.application.service.Application( "SwfConduit" )
        service_parent.setServiceParent( application )
        return application

