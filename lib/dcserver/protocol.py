
import pyamf
from twisted.internet.protocol import Protocol

class Protocol( Protocol ):
    encoding    = pyamf.AMF3

    def __init__( self ):
        self.encoder    = pyamf.get_encoder( self.encoding )

    def connectionMade( self ):
        """ Initialize a new user session """
        pass

    def connectionLost( self ):
        """ Deinit a session """
        pass

    def dataRecieved( self, data ):
        """ Read an object from the data """
        pass



