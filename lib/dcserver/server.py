
"""

dcserver.server -- The Server instance

A Server handles the overall persistence and events. It connects to databases,
manages Sessions, caches data, handles world persistence, and does the final
firing of Events.

Your Server subclass should add any necessary properties like DB connections.

"""

from dcserver.session import Session

class Server(object):
    cfg             = {}
    sessions        = {}
    session         = Session

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
