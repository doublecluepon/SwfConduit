
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

import os, sys, types

# Add current bin and lib directories
current_dir  = os.getcwd()
sys.path.append( current_dir )
sys.path.append( os.path.normpath( os.path.join( current_dir, "..", "lib" ) ) )

import optparse
import twisted.application.service
import dcserver.loader

"""
Initialize the DCServer
"""

# Pull the flags
parser = optparse.OptionParser()
parser.add_option( "-y" )
parser.add_option( "-n" )
parser.add_option( "-f", "--file",
    type    = "string",
    dest    = "cfg_filename",
    default = os.path.join( current_dir, "..", "etc", "dcserver.ini" ),
    help    = "Config filename",
    metavar = "FILE",
)
options, argv = parser.parse_args()

dcserver.loader.load_config( options.cfg_filename )

# Initialize the services
service_parent = twisted.application.service.MultiService()

dcserver.loader.add_services( service_parent )

application = twisted.application.service.Application( "DCServer" )
service_parent.setServiceParent( application )


# vim: ft=python
