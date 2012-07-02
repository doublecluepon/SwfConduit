package swfconduit.test {

	import flash.events.EventDispatcher;
	import swfconduit.ISocket;
	import swfconduit.Event;

	/**
	 * This is a mock socket that implements SwfConduit's socket interface, allowing
	 * for testing without a server.
	 *
	 * Instead of sending events over a socket, this object captures them and adds them
	 * to an internal array which can be examined and then cleared for the next event.
	 *
	 * To test events being sent from the server, use recieveEvent(), which will send
	 * the given event through the normal dispatch cycle.
	 */
	public class MockSocket extends EventDispatcher implements swfconduit.ISocket {
		
		/**
		 * The host we were asked to connect to
		 */
		public var host:String;

		/**
		 * The port we were asked to connect to
		 */
		public var port:int;

		/**
		 * The events that were written to us
		 */
		private var writtenEvents:Array;

		/**
		 * Create a new mock socket
		 */
		public function MockSocket() {

		}

		/**
		 * Update our host/port. Does not actually connect to anything.
		 */
		public function connect( host:String, port:int ):void {
			this.host = host;
			this.port = port;
		}

		/**
		 * Add an event to the list of events we've captured.
		 * @param event The event intended to be sent to the server
		 */
		public function writeEvent( event:swfconduit.Event ):void {
			writtenEvents.push( event );
		}

		/**
		 * Clear all the events that were written to prepare for the next test.
		 */
		public function clearWrittenEvents():void {
			writtenEvents = new Array();
		}

		/**
		 * Get all the events that were written to the socket since the last clearWrittenEvents()
		 */
		public function getWrittenEvents():Array {
			return writtenEvents;
		}

		/**
		 * Pretend an event was recieved, dispatching through the normal event
		 * listener cycle
		 */
		public function recieveEvent(event:swfconduit.Event):void {
			dispatchEvent( event );
		}

	}
}
