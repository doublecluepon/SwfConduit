package swfconduit {

	import flash.net.Socket;
	import flash.net.registerClassAlias;
	import flash.events.Event;
	import flash.events.ProgressEvent;
	import flash.utils.ByteArray;
	import swfconduit.Event;
	import swfconduit.ErrorMessage;
	import swfconduit.ISocket;

	/**
	 * This class handles events to and from the SwfConduit server. Though this
	 * is a regular flash Socket, you should only send SwfConduit events using the
	 * writeEvent() method, and you should only receive events by adding event 
	 * listeners for your event types.
	 *
	 * <p>You should listen for the close and error events yourself.</p>
	 *
	 * @see swfconduit.Event
	 * @see http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/net/Socket.html flash.net.Socket
	 * @see http://github.com/doublecluepon/SwfConduit/wiki/A-simple-chat-server Tutorial: A simple chat server
	 *
	 * @example Using Events
	 *
	 * <p>This example shows how to use Events with the Socket.</p>
	 *
	 * <listing version="3.0">
<!-- NOTE: Leave the spaces, they create empty lines -->
// Our Event class
package {
	import swfconduit.Event;
	public class MyEvent extends swfconduit.Event {
		public function MyEvent() { }
	}
}
 
// Register our event class
import flash.net.registerClassAlias;
registerClassAlias("myproject.MyEvent",MyEvent);
 
// Create a socket and send an event
import swfconduit.Socket;
var socket:swfconduit.Socket = new swfconduit.Socket("localhost",8000);
socket.writeEvent(new MyEvent());
 
// Listen for the event from the server
function handleMyEvent(event:MyEvent):void {
	trace("Got MyEvent!");
}
socket.addEventListener("MyEvent", handleMyEvent);

</listing>
	 * @example Extending the SwfConduit Socket
	 *
	 * <p>Extending the Socket can simplify creating and reusing connections. Here we
	 * extend the Socket to create a custom "Session" class that handles all the socket
	 * events.</p>
	 *
	 * <listing version="3.0">
package {
	import flash.events.&#42;;
	import flash.errors.&#42;;
	import swfconduit.Socket;
	
	public class Session extends swfconduit.Socket {
		
		public function Session(host:String="localhost", port:int=8000) {
			super();
			addEventListener(Event.CLOSE, closeHandler);
			addEventListener(Event.CONNECT, connectHandler);
			addEventListener(IOErrorEvent.IO_ERROR, ioErrorHandler);
			addEventListener(SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler);
			connect(host, port);
		}
		
		private function closeHandler(e:Event):void {
			trace("Socket closed");
		}
		
		private function connectHandler(e:Event):void {
			trace("Socket connected");
		}
		
		private function ioErrorHandler(e:IOErrorEvent):void {
			trace("IO Error: " + e);
		}
		
		private function securityErrorHandler(e:SecurityErrorEvent):void {
			trace("Security Error: " + e);
		}
	}
}
</listing>
	 *
	 */
	public class Socket extends flash.net.Socket implements swfconduit.ISocket {
		
		/**
		 * Buffer of socket data, in case a complete event isn't sent in a
		 * single socket data event
		 */
		public var buffer:ByteArray = new ByteArray();

		/**
		 * The default error handler, run if no other handler of an ErrorEvent 
		 * message calls preventDefault() on the message.
		 */
		public var defaultErrorHandler:Function = function (...args):void { };

		/**
		 * Create a new SwfConduit Socket.
		 * @param host The host to connect to
		 * @param port The port to connect to
		 * @see connect
		 */
		public function Socket(host:String=null, port:uint=0) {
			registerClassAlias( 'swfconduit.event.ErrorEvent', ErrorMessage );
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

				if ( reply is swfconduit.Event ) {
					dispatchEvent(reply);	
					if ( reply is ErrorMessage && !reply.isDefaultPrevented() ) {
						defaultErrorHandler( reply );
					}
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

		/**
		 * Set a default error handler
		 */
		public function setDefaultErrorHandler( handler:Function ):void {
			this.defaultErrorHandler = handler;
		}
	}
}
