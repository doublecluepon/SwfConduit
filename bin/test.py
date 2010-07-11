
# Shamelessly ripped from The PyAMF Project.

"""
Python client for socket example.

@since: 0.5
"""

import os, sys, types, time

# Add current bin and lib directories
current_dir  = os.getcwd()
sys.path.append( current_dir )
sys.path.append( os.path.normpath( os.path.join( current_dir, "..", "lib" ) ) )

import socket
import pyamf
from dcserver.event import Event
from dcserver.test import TickEvent, HelloEvent

appPort = 7000
host    = '127.0.0.1'

pyamf.register_class( TickEvent, "dcserver.test.TickEvent" )
pyamf.register_class( HelloEvent, "dcserver.test.HelloEvent" )

class AmfSocketClient(object):
    encoding    = pyamf.AMF3

    def __init__(self):
        self.encoder    = pyamf.get_encoder( self.encoding )
        self.stream     = self.encoder.stream
        self.sock       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.decoder    = pyamf.get_decoder( self.encoding )
        self.istream    = self.decoder.stream

    def connect(self, host, port):
        print "Connecting to socket server on %s:%d" % (host, port)
        try:
            self.sock.connect((host, port))
            print "Connected to server.\n"
            event   = HelloEvent()
            self.encoder.writeObject( event )
            value   = self.stream.getvalue()
            self.sock.send( value )
            self.stream.consume()

        except socket.error, e:
            raise Exception("Can't connect: %s" % e[1])

    def start(self):
        msg = ''

        # Create an object to send
        event       = TickEvent()
        self.encoder.writeObject( event )
        value = self.stream.getvalue()

        try:
            self.sock.send( value )
        except socket.error, e:
            raise Exception("Can't connect: %s" % e[1])

        self.stream.consume()

        # read from server
        print "Reading..."
        amf = self.sock.recv(100)

        if amf == '':
            print "Connection closed."

        self.istream.append( amf )
        got_events = []
        while ( not self.istream.at_eof() ):
            event = self.decoder.readElement()
            got_events.append( event )
        print "Recieved %s objects!" % len( got_events )
        for event in got_events:
            print "Event: %s; Time: %s" % ( event, event.timestamp )

        self.istream.consume()
        time.sleep(1)
        return self.start()

    def stop(self):
        print "send request: stop"


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-p", "--port", default=appPort,
        dest="port", help="port number [default: %default]")
    parser.add_option("--host", default=host,
        dest="host", help="host address [default: %default]")
    (options, args) = parser.parse_args()

    host = options.host
    port = int(options.port)

    client = AmfSocketClient()
    client.connect(host, port)

    try:
        client.start()
    except KeyboardInterrupt:
        client.stop()   
