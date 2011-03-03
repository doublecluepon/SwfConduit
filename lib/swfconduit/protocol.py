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

swfconduit.protocol -- Handle AMF in and out.

A single Protocol object is created for every client connection. When a 
connection is made, the Protocol asks the Server to open a new Session.

As events are received from the client, the Protocol sends the event to
the Session to be processed.

"""

import pyamf
from twisted.internet.protocol import Protocol
from swfconduit.event import Event

class Protocol( Protocol ):
    encoding    = pyamf.AMF3
    session     = None

    def __init__( self ):
        # Prepare the encoder and decoder
        self.encoder    = pyamf.get_encoder( self.encoding )
        self.ostream    = self.encoder.stream
        self.decoder    = pyamf.get_decoder( self.encoding )
        self.istream    = self.decoder.stream

    def connectionMade( self ):
        """ Initialize a new user session """
        self.session    = self.factory.openSession( self )

    def connectionLost( self, reason ):
        """ Deinit a session """
        self.session.close()

    def dataReceived( self, data ):
        """ Read an event from the data """
        # Add the data to the input stream
        print "RECV %i BYTES" % len( data )
        self.istream.append( data )

        # Read all the objects from the data
        while ( not self.istream.at_eof() ):
            # Read the element from the decoder
            try:
                event = self.decoder.readElement()
            except IOError as error:
                break # Not enough, wait for another dataReceived
            if not isinstance( event, Event ):
                print "Unknown event: %s" % event
            else:
                # Pass the event to the Session for handling
                print "Received event: %s" % event
                self.receiveEvent( event )

    def sendEvent( self, event ):
        """ Send an event object to the client """
        print "Sending event: %s" % event
        # Clear the context to avoid RangeError #2006 from AS3 client
        self.encoder.context.clear()
        # Encode the object
        self.encoder.writeObject( event )
        # Get the object from the output stream and write to the socket
        self.transport.write( self.ostream.getvalue() )
        # Clear the output stream
        self.ostream.truncate()

    def receiveEvent( self, event ):
        """ Receive an event """
        self.session.fireEvent( event )


