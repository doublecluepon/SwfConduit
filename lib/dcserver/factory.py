
"""

dcserver.factory -- The Twisted Factory for DCServer

A very thin persistence layer to keep track of the Server object

"""

import twisted.internet.protocol
import dcserver.protocol

class Factory( twisted.internet.protocol.Factory ):
    protocol    = dcserver.protocol.Protocol

    def __init__( self, server ):
        self.server = server
