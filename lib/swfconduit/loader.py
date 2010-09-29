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

The loader reads the config file, loads the plugin packages, creates the 
swfconduit Server and Twisted Factory, and sets everything up for the 
twistd daemon.

"""

import sys
import ConfigParser
import twisted.application.internet
import twisted.application.service
import swfconduit.server
import swfconduit.socketpolicy
from twisted.python import log

cfg = ConfigParser.SafeConfigParser()

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

def add_services( service_parent ):
    """ Add services to the given twisted service_parent """

    # Create the service to serve the socket policy
    swfconduit.socketpolicy.add_service( service_parent )

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
        print "Adding %s" % module
        server  = module.Server(server_config)

        if "tcp" in proto:
            # Add a TCP listener to our server
            twisted.application.internet.TCPServer( port, server ).setServiceParent( service_parent )


def load_config(filename):
    """ Load the configuration file """
    cfg.readfp( open( filename ) )


def start( ):
    """ Start the conduit """
    service_parent = twisted.application.service.MultiService()

    add_services( service_parent )

    application = twisted.application.service.Application( "SwfConduit" )
    service_parent.setServiceParent( application )
    return application

