
import pyamf
from twisted.internet.protocol import Protocol
from dcserver.event import Event

class Protocol( Protocol ):
    encoding    = pyamf.AMF3

    def __init__( self ):
        self.encoder    = pyamf.get_encoder( self.encoding )
        self.ostream    = self.encoder.stream
        self.decoder    = pyamf.get_decoder( self.encoding )
        self.istream    = self.decoder.stream

    def connectionMade( self ):
        """ Initialize a new user session """
        self.session    = self.factory.server.openSession( self )

    def connectionLost( self, reason ):
        """ Deinit a session """
        self.session.close()

    def dataReceived( self, data ):
        """ Read an event from the data """
        self.istream.append( data )

        # Read all the objects from the data
        while ( not self.istream.at_eof() ):
            self.decoder.context.clear()
            event = self.decoder.readElement()
            if not isinstance( event, Event ):
                print "Unknown event: %s" % event
            else:
                print "Event {}: {}" % event, event.timestamp
                self.session.fireEvent( event )

    def sendEvent( self, event ):
        """ Send an event object to the client """
        self.encoder.context.clear()
        # Encode the object
        self.encoder.writeObject( event )
        # Get the object from the output stream and write to the socket
        self.transport.write( self.ostream.getvalue() )
        # Clear the output stream
        self.ostream.truncate()


