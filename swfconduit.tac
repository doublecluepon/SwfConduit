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

swfconduit.tac - Initialize the SwfConduit

"""

import os, sys, types

# Add current bin and lib directories
current_dir  = os.getcwd()
sys.path.append( current_dir )
sys.path.append( os.path.normpath( os.path.join( current_dir, "lib" ) ) )

import optparse
import twisted.application.service
import swfconduit.loader

# Pull the flags
parser = optparse.OptionParser()
parser.add_option( "-y" )       # Parse out the twistd flag
parser.add_option( "-n" )       # Parse out the twistd flag
parser.add_option( "-f", "--file",
    type    = "string",
    dest    = "cfg_filename",
    default = os.path.join( current_dir, "swfconduit.ini" ),
    help    = "Config filename",
    metavar = "FILE",
)
options, argv = parser.parse_args()

swfconduit.loader.load_config( options.cfg_filename )
application = swfconduit.start()

# vim: ft=python
