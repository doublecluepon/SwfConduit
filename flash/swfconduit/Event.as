package swfconduit {

	public class Event {
		public var timestamp = 0;
		
		public function Event( ) {
			
			
		}
		
		/* Tried this to fix readObject problem. failed. 
		   may need in the future...
		public function readExternal( input:IDataInput ):void {
			this.timestamp  = input.readObject();
			this.payload	= input.readObject();
		}
		
		public function writeExternal( output:IDataOutput ):void {
			output.writeObject( this.timestamp );
			output.writeObject( this.payload );
		}
		*/
	}
}



