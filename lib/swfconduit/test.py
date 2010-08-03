
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

"""

swfconduit.test -- A test server

This server tests the event handling of swfconduit. It also serves as a 
reference for your own plugins

"""

import pyamf
import swfconduit.server
import swfconduit.session
from swfconduit.event import Event
from twisted.internet.defer import Deferred
from twisted.internet.task import LoopingCall

class Session(swfconduit.session.Session):
    def open(self):
        """ Initialize periodic events """
        self.ticker = LoopingCall( self.tick )
        self.ticker.start(10)

    def tick(self):
        event = HelloEvent()
        print "TICK! %s" % event.timestamp
        self.sendEvent( event )

    def close(self):
        self.ticker.stop()
        super(Session, self).close()


class Server(swfconduit.server.Server):
    session     = Session

class TickEvent( Event ):
    def fire( self, server, session ):
        print "Fired TickEvent"

class HelloEvent( Event ):
    def fire( self, server, session ):
        print "Fired HelloEvent"
        session.sendEvent( TickEvent() )

# Register events for this server
pyamf.register_class( TickEvent, "swfconduit.test.TickEvent" )
pyamf.register_class( HelloEvent, "swfconduit.test.HelloEvent" )

