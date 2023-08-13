import requests
import json
import logging
import os
from queue import Queue
import concurrent.futures


class WhatsAppService:
    def __init__(self) -> None:
        """Handles sending messages to WhatsApp, using a queue mechanism.
        TODO: Implement a queueing mechanism with a thread monitoring it constantly."""
        self.whatsapp_bearer_token = os.getenv("WHATSAPP_BEARER_TOKEN")
        self.whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_ID")
        self.simulator_mode = os.getenv("SIMULATOR_MODE")
        self.end_marker = os.getenv("END_MARKER")

        pass

    def send_message(self, to, message):
        """API most other objects will use to send a message."""
        self.outgoing_msg_q.put((to, message))

    def outgoing_worker_task(self):
        """TODO: Setup the blocking loop that will constantly listen for new messages to send and then post them to WhatsAPP API."""
        pass

    def _post_message(self, to, message):
        """TODO: Internal API for using the requests library to make the needed POST to the WhatsAPP URL endpoint.
        Finish implementation.
        Hint use the requests library to make a post request"""
        body = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": str(to),
            "type": "text",
            "text": {"body": str(message)},
        }

        headers = {
            "Authorization": self.whatsapp_bearer_token,
            "Content-Type": "application/json",
        }
        

        pass
