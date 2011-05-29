package swfconduit.chat {

	import swfconduit.Event;

	/**
	 * A chat message. We send them out when we speak, and we recieve them
	 * when other people speak.
	 */
	public class ChatEvent extends swfconduit.Event {
		
		/**
		 * The person who sent the event
		 */
		public var nickname:String;

		/**
		 * The message being sent/recieved
		 */
		public var text:String;

		/**
		 * Create a new chat message with the given text. You can then pass this
		 * object directly to Socket.sendEvent
		 */
		public function ChatEvent( nickname:String="", text:String="" ) {
			this.nickname = nickname;
			this.text = text;
		}
	}
}
