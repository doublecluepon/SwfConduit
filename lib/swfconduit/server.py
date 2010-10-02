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

swfconduit.server -- The Server instance

A Server handles the overall persistence and events. It connects to databases,
manages Sessions, caches data, handles world persistence, and does the final
firing of Events.

Your Server subclass should add any necessary properties like DB connections.

"""

from swfconduit.session import Session
import twisted.internet.protocol
import swfconduit.protocol


class Server( twisted.internet.protocol.Factory ):
    protocol        = swfconduit.protocol.Protocol
    session         = Session
    cfg             = {}
    sessions        = {}

    def __init__( self, cfg ):
        """ Init a new Server with the given configuration """
        self.cfg        = cfg

    def openSession( self, protocol ):
        """ Open a user session """
        session = self.session( self, protocol )
        self.sessions[ session.id ] = session
        session.open()
        return session

    def closeSession( self, session ):
        """ A session is closing, clean up after it """
        del( self.sessions[ session.id ] )
        pass

    def fireEvent( self, event, session ):
        """ Fire the event """
        event.fire( self, session )

    def sendGlobalEvent( self, event ):
        """ Send an event to all active sessions """
        pass
