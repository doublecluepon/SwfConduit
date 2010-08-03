
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

"""

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
        print "Opening session"
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
