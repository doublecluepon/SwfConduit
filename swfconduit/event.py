#-----------------------------------------------------------------------------
# Copyright (c) 2010 Double Cluepon Software
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

"""
The Event is the basic message passed to and from the server. Inherit from the
Event class to create custom Events.::

    class MyEvent( swfconduit.event.Event ):
        myproperty  = "default"
        def fire( self, server, session ):
            # Do stuff here

To use the event, register it with pyamf, giving the Class and the
name of a class in the AS3 code::

    import pyamf
    pyamf.register_class( MyEvent, "mypackage.events.MyEvent" )

Now the MyEvent class will be created on the client as an instance of a 
mypackage.events.MyEvent object, and any incoming AS3 Events of type 
"mypackage.events.MyEvent" will be created as MyEvent objects.

The corresponding AS3 object should then look like this::

    package mypackage.events {
        import swfconduit.Event;
        class MyEvent extends swfconduit.Event {
            // Only public members will be passed
            public var myproperty   = "default";
            public function MyEvent( ) { }
        }
    }

All events' properties need to be defined in both server and client.
otherwise the client will warn about missing properties.

"""
from datetime import datetime
from random import getrandbits
import traceback

class Event( object ):
    id = 0
    timestamp = None

    def __init__( self ):
        self.id         = getrandbits(29) # Size of an AMF3 integer field
        self.timestamp  = datetime.now()
        pass

    def fire( self, server, session ):
        """ Perform the event's task """
        pass

    # Tried this for AS3 readObject problem. May need in future
    #def __readamf__( self, input ):
    #    self.timestamp = input.readObject()
    #    self.payload   = input.readObject()
    #
    #def __writeamf__( self, output ):
    #    output.writeObject( self.timestamp )
    #    output.writeObject( self.payload )

    def reply( self, cls, *args ):
        """ Create a reply with the given class. Will set the reply's id field appropriately """
        reply = cls(*args)
        reply.id = self.id
        return reply

class ErrorEvent( Event ):
    e = None
    traceback = ""

    def __init__( self, e ):
        self.e = e
        self.traceback = traceback.format_exc()

    def fire( self, server, session ):
        # Can't raise here, we already ARE an error
        print "Whachotalkingboutwillis?" + self.__repr__()
