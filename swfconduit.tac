
import os, sys, types

# Add current bin and lib directories
current_dir  = os.getcwd()
sys.path.append( current_dir )

from swfconduit.loader import Loader

loader  = Loader()
loader.load_from_config( os.path.join( current_dir, "swfconduit.ini" ) )
application = loader.get_application()

