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

swfconduit.session -- A single client connection to a server

A new Session is spawned by a Server when a client connects. The Session 
stores persistent data about the client connected, like user, character, 
current task, etc...

The Session delegates all event handling to the Protocol (client) or the
Server (server).

"""

from uuid import uuid4

class Session(object):
    protocol    = None
    server      = None
    id          = None

    def __init__( self, server, protocol ):
        """ Initialize a new session """
        self.server     = server
        self.protocol   = protocol
        self.id         = uuid4()

    def close( self ):
        """ Close the session """
        self.server.closeSession( self )

    def fireEvent( self, event ):
        """ Fire off the event to the local server """
        self.server.fireEvent( event, self )

    def open( self ):
        """ Open the session """
        pass

    def sendEvent( self, event ):
        """ Send an event to the remote client """
        self.protocol.sendEvent( event )




