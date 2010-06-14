
import sys
import twisted.internet.protocol
import dcserver.protocol

class Factory( twisted.internet.protocol.Factory ):
    protocol    = dcserver.protocol.Protocol

    def __init__( self, server ):
        self.server = server
