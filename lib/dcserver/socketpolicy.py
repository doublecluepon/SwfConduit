
# Copyright (c) 2010 Double Cluepon Software
# Licensed for use under the GPL version 2.0 or later

"""

dcserver.socketpolicy -- Handle requests for the Socket Policy file

This Twisted application handles all requests for the Socket Policy file.

Copy/pasted from PyAMF library

TODO: Autogenerate the policy based on the configuration file

"""

import os
import twisted.application.internet
import twisted.internet.protocol

policy_file = os.path.normpath( os.path.join( __file__, "..", "..", "..", "etc", "socket-policy.xml" ) )
policy_port = 843

class SocketPolicyProtocol(twisted.internet.protocol.Protocol):
    """
    Serves strict policy file for Flash Player >= 9,0,124.

    @see: U{http://adobe.com/go/strict_policy_files}
    """
    def connectionMade(self):
        self.buffer = ''

    def dataReceived(self, data):
        self.buffer += data

        if self.buffer.startswith('<policy-file-request/>'):
            self.transport.write(self.factory.getPolicyFile(self))
            self.transport.loseConnection()


class SocketPolicyFactory(twisted.internet.protocol.Factory):
    protocol = SocketPolicyProtocol

    def __init__(self, policy_file):
        """
        @param policy_file: Path to the policy file definition
        """
        self.policy_file = policy_file

    def getPolicyFile(self, protocol):
        return open(self.policy_file, 'rt').read()

def add_service( service_parent ):
    factory = SocketPolicyFactory( policy_file )
    twisted.application.internet.TCPServer( policy_port, factory ).setServiceParent( service_parent )

