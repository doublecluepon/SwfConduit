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

