
import os, sys, types

# Add correct lib directory
current_dir  = os.getcwd()
sys.path.append( os.path.normpath( os.path.join( current_dir, "..", ".." ) ) )

# Create our event class
from swfconduit.event import Event
class ChatEvent( Event ):
    # The nickname of the user sending the event
    nickname = ""
    # The message
    text = ""

    def fire( self, server, session ):
        # We recieved a chat event, send it to every other person
        print "CHAT {}> {}".format(self.nickname, self.text)
        for session_id in server.sessions:
            s = server.sessions[session_id]
            if (s is not session):
                s.sendEvent( self )

# Register our ChatEvent class. the first argument is the same as the
# registerClassAlias string in the client
import pyamf
pyamf.register_class( ChatEvent, "swfconduit.chat.ChatEvent" )

# Create the SwfConduit server
from swfconduit.loader import Loader
from swfconduit.server import Server
loader = Loader()
server = Server({ "proto" : "tcp", "port" : 8000 })
loader.servers.append( server );
application = loader.get_application()

