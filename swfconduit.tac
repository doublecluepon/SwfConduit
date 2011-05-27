
import os, sys, types

# Add current bin and lib directories
current_dir  = os.getcwd()
sys.path.append( current_dir )
sys.path.append( os.path.normpath( os.path.join( current_dir, "lib" ) ) )

from swfconduit.loader import Loader

loader  = Loader()
loader.load_from_config( os.path.join( current_dir, "server.ini" ) )
application = loader.get_application()

# Create an http server for stuff
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.application.internet import TCPServer
from twisted.web.static import File
from storyteller.web import FileManager
http_root = Resource()
http_root.putChild( "file", FileManager( loader.servers[0] ) )
http_server = TCPServer( 8080, Site( http_root ) )
http_server.setServiceParent( application )

