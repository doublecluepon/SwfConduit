"""
-----------------------------------------------------------------------------
Copyright (c) 2010 Double Cluepon Software

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------

swfconduit.loader -- Load all the swfconduit plugins and prepare for running

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
    """ Load a swfconduit """

    servers = []
    """ The list of servers we made """

    def add_server( self, config ):
        """ Create the server from the given config """
        # Start the appropriate listeners and set up connection handlers
        module  = _get_mod( config["package"] )

        # Init a new server
        server  = module.Server(config)
        self.servers.append( server )

    def add_services( self, service_parent ):
        """ Add services to the given twisted service_parent """

        # Create the service to serve the socket policy
        swfconduit.socketpolicy.add_service( service_parent, './socket-policy.xml' )

        for server in self.servers:
            port    = int(server.config["port"])
            proto   = server.config["proto"]
            if "tcp" in proto:
                # Add a TCP listener to our server
                twisted.application.internet.TCPServer( port, server ).setServiceParent( service_parent )

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
        """ Get the twisted application with all the plugin services added """
        service_parent = twisted.application.service.MultiService()

        self.add_services( service_parent )

        application = twisted.application.service.Application( "SwfConduit" )
        service_parent.setServiceParent( application )
        return application

