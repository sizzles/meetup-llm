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
        """WhatsApp sends different message types eg. text, audio, video - only worry about text for the moment."""
        try:
            entry = whatsapp_body.get("entry")
            try:
                wa_id = entry[0]["changes"][0]["value"]["contacts"][0]["wa_id"]
            except:
                return  # invalid message - dont worry about it

            message = entry[0]["changes"][0]["value"]["messages"][0]

            if len(entry[0]["changes"][0]["value"]["messages"]) > 1:
                raise Exception(f"Only single messages handled at the moment. ")

            if message.get("type") == "text":
                self._route_text_message(wa_id, message)
                logging.info(f"Routing msg for wa_id: {wa_id}")

        except Exception as e:
            print("Error routing message")
            print(e)
            print(whatsapp_body)
