package swfconduit {

	import flash.net.Socket;
	import flash.events.Event;
	import flash.events.ProgressEvent;
	import flash.utils.ByteArray;
	import swfconduit.Event;

	/**
	 * This class handles events to and from the SwfConduit server. Though this
	 * is a regular flash Socket, you should only send SwfConduit events using the
	 * sendEvent() method, and you should only receive events by adding event 
	 * listeners for your event types.
	 *
	 * You should listen for the close and error events yourself.
	 *
	 * @see swfconduit.Event
	 */
	public class Socket extends flash.net.Socket {
		
		/**
		 * Buffer of socket data, in case a complete event isn't sent in a
		 * single socket data event
		 */
		public var buffer:ByteArray = new ByteArray();

		/**
		 * Create a new SwfConduit Socket.
		 * @param host The host to connect to
		 * @param port The port to connect to
		 * @see connect
		 */
		public function Socket(host:String=null, port:uint=0) {
			super(host, port);
			addEventListener(ProgressEvent.SOCKET_DATA,handleSocketData);
		}

		/**
		 * Read data from the socket to get and dispatch events
		 */
		public function handleSocketData(event:ProgressEvent):void {
			var startingPosition:int = buffer.position;
			readBytes(buffer,buffer.length);
			buffer.position=startingPosition;
			
			while (buffer.bytesAvailable > 0) {
				try {
					var currentPosition:int = buffer.position;
					var reply:* = buffer.readObject();
				}
				catch (e:*) {
					buffer.position = currentPosition;
					var tempBuff:ByteArray = new ByteArray();		
					buffer.readBytes(tempBuff,0);
					tempBuff.position = 0;
					buffer = tempBuff;
					return; // Don't clear it out!
				}

				if ( typeof reply == "object" ) {
					dispatchEvent(reply);	
				}
				else {
					trace( "SwfConduit recieved invalid event: " + reply );
				}
			}
			buffer = new ByteArray(); // We completed successfully, clear it out
		}

		/**
		 * Write an event to the server.
		 * @param event The event to send
		 */
		public function writeEvent(event:swfconduit.Event):void {			
			writeObject(event);
			flush();
		}
	}
}
