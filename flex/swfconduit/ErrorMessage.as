package swfconduit {
    import swfconduit.Event;
	/**
	 * The ErrorMessage class contains an error from the server.
	 */
    public class ErrorMessage extends swfconduit.Event {
		/**
		 * The error from the server
		 */
        public var e:*;
		/**
		 * The traceback from the server, for debugging purposes
		 */
		public var traceback:String;
    }
}
