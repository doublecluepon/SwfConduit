
from datetime import datetime

class Event( ):
    timestamp   = None
    payload     = { }

    def __init__( self ):
        self.timestamp  = datetime.now()
        pass

    # Tried this for AS3 readObject problem. May need in future
    #def __readamf__( self, input ):
    #    self.timestamp = input.readObject()
    #    self.payload   = input.readObject()
    #
    #def __writeamf__( self, output ):
    #    output.writeObject( self.timestamp )
    #    output.writeObject( self.payload )

