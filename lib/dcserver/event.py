
"""

dcserver.event -- Base class for DCServer events

The Event is the basic message passed to and from the server. You should
subclass this for your own Events.

    class MyEvent( dcserver.event.Event ):
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
        import dcserver.event;
        class MyEvent extends dcserver.event.Event {
            // Only public members will be passed
            public var myproperty   = "default";
            public function fire( ) {

            }
        }
    }

All events' properties need to be defined in both DCServer and your AS3 code, 
even if only one of those has defined a fire() method.

"""
from datetime import datetime

class Event( ):
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

