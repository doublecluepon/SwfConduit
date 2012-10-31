package swfconduit {
	import flash.events.IEventDispatcher;
	/**
	 * This is an interface for Swfconduit sockets.
	 * 
	 * By implementing this interface, you can make mock sockets for testing.
	 *
	 * @see swfconduit.Socket
	 */
	public interface ISocket extends IEventDispatcher {
		/**
		 * Write an event to the socket, sending the event to the server.
		 * @param event The event to send
		 */
		function writeEvent( event:swfconduit.Event ):void;
		/**
		 * Connect to a server.
		 * @param host The host name or IP address to connect to
		 * @param port The port to connect to
		 */
		function connect( host:String, port:int ):void;
		/**
		 * Set the default error handler that will be run on ErrorMessage
		 * messages, unless preventDefault() is called on the message
		 */
		function setDefaultErrorHandler( handler:Function ):void;
		/**
		 * Close the socket
		 */
		function close():void;
	}
}
