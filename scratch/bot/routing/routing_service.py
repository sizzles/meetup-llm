import logging
from queue import Queue
from ..msg_cache import MsgCache


class RoutingService:
    def __init__(self, target_q: Queue, msg_cache: MsgCache):
        """Routing service - interacts with an incoming message queue and message cache to send messages to correct destination."""
        self.target_q = target_q
        self.msg_cache = msg_cache

    def _route_text_message(self, wa_id, message):
        """Add into our message cache, and notify the processing queue a new message has been received."""
        self.msg_cache.append(wa_id, message)
        self.target_q.put(wa_id)

    def route_message(self, whatsapp_body):
        """WhatsApp sends different message types eg. text, audio, video - only worry about text for the moment.
        TODO: extract the relevant wa_id and message from the received request. Look in the logs to see a sample output for what that looks like."""