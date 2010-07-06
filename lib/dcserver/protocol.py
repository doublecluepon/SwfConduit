
import pyamf
from twisted.internet.protocol import Protocol
from dcserver.event import Event

# Register class so we can read objects of this class
pyamf.register_class( Event, "dcserver.event" )

class Protocol( Protocol ):
    encoding    = pyamf.AMF3

    def __init__( self ):
        self.encoder    = pyamf.get_encoder( self.encoding )
        self.ostream    = self.encoder.stream
        self.decoder    = pyamf.get_decoder( self.encoding )
        self.istream    = self.decoder.stream

    def connectionMade( self ):
        """ Initialize a new user session """
        print "Connection Made"
        pass

    def connectionLost( self, reason ):
        """ Deinit a session """
        print "Connection Lost"
        pass

    def dataReceived( self, data ):
        """ Read an event from the data """
        self.istream.append( data )

        # Read all the objects from the data
        while ( not self.istream.at_eof() ):
            event = self.decoder.readObject()
            if not isinstance( event, Event ):
                # Why do we always receive a None object? Connection?
                print "Unknown event: %s" % event
            else:
                print "Event %s" % event
                # Write an "ack" event
                ack = Event()
                ack.type = "Ack"
                ack.timestamp = "234567890"

                self.encoder.writeObject( ack )
                self.transport.write( self.ostream.getvalue() )
                self.ostream.truncate()

                # Pass the event to the session?
                # Pass the event to the server?
                # BAIL OUT!
        print "Done!"
        pass



