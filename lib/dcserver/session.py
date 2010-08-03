
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

"""

dcserver.session -- A single client connection to a server

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

    def sendEvent( self, event ):
        """ Send an event to the remote client """
        self.protocol.sendEvent( event )




