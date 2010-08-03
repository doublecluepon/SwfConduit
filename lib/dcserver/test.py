
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

"""

dcserver.test -- A test server

This server tests the event handling of DCServer. It also serves as a 
reference for your own plugins

"""

import pyamf
import dcserver.server
import dcserver.session
from dcserver.event import Event
from twisted.internet.defer import Deferred
from twisted.internet.task import LoopingCall

class Session(dcserver.session.Session):
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


class Server(dcserver.server.Server):
    session     = Session

class TickEvent( Event ):
    def fire( self, server, session ):
        print "Fired TickEvent"

class HelloEvent( Event ):
    def fire( self, server, session ):
        print "Fired HelloEvent"
        session.sendEvent( TickEvent() )

# Register events for this server
pyamf.register_class( TickEvent, "dcserver.test.TickEvent" )
pyamf.register_class( HelloEvent, "dcserver.test.HelloEvent" )

