
class Session(object):
    protocol    = None
    server      = None

    def __init__( self, server, protocol ):
        """ Initialize a new session """
        self.server     = server
        self.protocol   = protocol

    def close( self ):
        """ Close the session """
        self.server.closeSession( self )

    def fireEvent( self, event ):
        """ Fire off the event to the local server """
        self.server.fireEvent( event, self )

    def sendEvent( self, event ):
        """ Send an event to the remote client """
        self.protocol.sendEvent( event )




