package swfconduit {

	import flash.events.Event;
	import flash.utils.getQualifiedClassName;

	/**
	 * The Event is a message between server and client. Every message between
	 * server and client is handled by an Event class. The Event object 
	 * encapsulates the objects being transferred.
	 *
	 * You should subclass this for your own events. Make sure to use
	 * flash.net.registerClassAlias() to register your classes.
	 *
	 * @see swfconduit.Socket
	 */
	public class Event extends flash.events.Event {

		/**
		 * The date/time the event was sent
		 */
		public var timestamp:Date;
		
		/**
		 * Create an event. 
		 *
		 * NOTE: For events being received by the client, you must provide default
		 * values for all arguments to the constructor.
		 */
		public function Event() {
			// Determine the type from the class
			var type:String = getQualifiedClassName(this);
			var index:int = type.indexOf(":");
			type = type.slice(index+2);

			super(type,true,true);
		}
	}
}
