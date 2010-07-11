
from dcserver.session import Session

class Server(object):
    cfg             = {}
    sessions        = []
    session         = Session

    def __init__( self, cfg ):
        self.cfg        = cfg

    def openSession( self, protocol ):
        """ Open a user session """
        session = self.session( self, protocol )
        self.sessions.append( session )
        session.open()
        return session

    def closeSession( self, session ):
        """ Close a user session """
        # Remove session from sessions
        pass

    def fireEvent( self, event, session ):
        """ Fire the event """
        event.fire( self, session )

    def sendEvent( self, event ):
        print "sending event %s" % event
        self.protocol.sendEvent( event )
