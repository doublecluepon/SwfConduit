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

swfconduit.event -- Base class for SwfConduit events

The Event is the basic message passed to and from the server. You should
subclass this for your own Events.

    class MyEvent( swfconduit.event.Event ):
        myproperty  = "default"
        def fire( self, server, session ):
            # Do my task here

To use your event, you must register it with pyamf, giving the Class and the
name of a class in the AS3 code:

    import pyamf
    pyamf.register_class( MyEvent, "mypackage.events.MyEvent" )

Now your MyEvent class will be created on the client as an instance of a 
mypackage.events.MyEvent object, and any incoming AS3 Events of type 
"mypackage.events.MyEvent" will be created as MyEvent objects.

Your AS3 object should then look like this:

    package mypackage.events {
        import swfconduit.event;
        class MyEvent extends swfconduit.event.Event {
            // Only public members will be passed
            public var myproperty   = "default";
            public function fire( ) {

            }
        }
    }

All events' properties need to be defined in both SwfConduit and your AS3 code, 
even if only one of those has defined a fire() method.

"""
from datetime import datetime

class Event( object ):
    timestamp   = None

    def __init__( self ):
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

class ErrorEvent( Event ):
    e = None

    def __init__( self, e ):
        self.e = e

    def fire( self, server, session ):
        # Can't raise here, we already ARE an error
        print "Whachotalkingboutwillis?" + self.__repr__()
