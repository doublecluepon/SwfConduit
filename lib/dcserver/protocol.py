"""

dcserver.protocol -- Handle AMF in and out.

A single Protocol object is created for every client connection. When a 
connection is made, the Protocol asks the Server to open a new Session.

As events are received from the client, the Protocol sends the event to
the Session to be processed.

"""

import pyamf
from twisted.internet.protocol import Protocol
from dcserver.event import Event

class Protocol( Protocol ):
    encoding    = pyamf.AMF3

    def __init__( self ):
        # Prepare the encoder and decoder
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
        # Add the data to the input stream
        self.istream.append( data )

        # Read all the objects from the data
        while ( not self.istream.at_eof() ):
            # Read the element from the decoder
            event = self.decoder.readElement()
            if not isinstance( event, Event ):
                print "Unknown event: %s" % event
            else:
                print "Event {}: {}" % event, event.timestamp
                # Pass the event to the Session for handling
                self.session.fireEvent( event )

    def sendEvent( self, event ):
        """ Send an event object to the client """
        # Clear the context to avoid RangeError #2006 from AS3 client
        self.encoder.context.clear()
        # Encode the object
        self.encoder.writeObject( event )
        # Get the object from the output stream and write to the socket
        self.transport.write( self.ostream.getvalue() )
        # Clear the output stream
        self.ostream.truncate()


