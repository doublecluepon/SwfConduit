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

swfconduit.socketpolicy -- Handle requests for the Socket Policy file

This Twisted application handles all requests for the Socket Policy file.

Copy/pasted from PyAMF library

TODO: Autogenerate the policy based on the configuration file

"""

import os
import twisted.application.internet
import twisted.internet.protocol

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

def add_service( service_parent, policy_file ):
    factory = SocketPolicyFactory( policy_file )
    twisted.application.internet.TCPServer( policy_port, factory ).setServiceParent( service_parent )

