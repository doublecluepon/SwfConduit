package swfconduit {
	/**
	 * This is an interface for Swfconduit sockets.
	 * 
	 * By implementing this interface, you can make mock sockets for testing.
	 *
	 * @see swfconduit.Socket
	 */
	public interface ISocket {
		/**
		 * Write an event to the socket, sending the event to the server.
		 * @param event The event to send
		 */
		function writeEvent( event:swfconduit.Event ):void;
		/**
		 * Add a listener for an event from the server.
		 * @param name The name of the event to listen for, the same as the class name (without package)
		 * @param callback The function to call when the event comes in. The function will get the event as an argument
		 */
		function addEventListener( name:String, callback:Function ):void;
		/**
		 * Remove an event listeners. Takes the exact arguments as addEventListener()
		 * @param name The name of the event we were listening for
		 * @param callback The function we gave to addEventListener()
		 */
		function removeEventListener( name:String, callback:Function ):void;
		/**
		 * Connect to a server.
		 * @param host The host name or IP address to connect to
		 * @param port The port to connect to
		 */
		function connect( host:String, port:int ):void;
	}
}
