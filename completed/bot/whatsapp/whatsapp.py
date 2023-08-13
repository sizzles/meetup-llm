import requests
import json
import logging
import os
from queue import Queue
import concurrent.futures


class WhatsAppService:
    def __init__(self) -> None:
        """Handles sending messages to WhatsApp, using a queue mechanism."""
        self.whatsapp_bearer_token = os.getenv("WHATSAPP_BEARER_TOKEN")
        self.whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_ID")
        self.simulator_mode = os.getenv("SIMULATOR_MODE")
        self.end_marker = os.getenv("END_MARKER")

        self.outgoing_msg_q = Queue()
        outgoing_workers = 1
        outgoing_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=outgoing_workers, thread_name_prefix="outgoing"
        )
        for _ in range(outgoing_workers):
            outgoing_executor.submit(self.outgoing_worker_task)
        logging.info("Created Outgoing Queue Processors")

    def _get_whatsapp_url(self):
        if self.simulator_mode == "True":
            url = "http://localhost:6000/incoming"
        else:
            url = f"https://graph.facebook.com/v16.0/{self.whatsapp_phone_id}/messages"
        return url

    def send_message(self, to, message):
        """API most other objects will use to send a message."""
        self.outgoing_msg_q.put((to, message))

    def outgoing_worker_task(self):
        """Setup the blocking loop that will constantly listen for new messages to send."""
        while True:
            try:
                wa_id, msg = self.outgoing_msg_q.get()

                if wa_id == self.end_marker:
                    break

                # send this to user
                self._post_message(wa_id, msg)

            except Exception as e:
                logging.exception(f"Error sending outgoing message to : {str(wa_id)}")
                logging.exception(e)
            finally:
                self.outgoing_msg_q.task_done()

    def _post_message(self, to, message):
        """Internal API for using the requests library to make the needed POST to the WhatsAPP URL endpoint."""
        body = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": str(to),
            "type": "text",
            "text": {"body": str(message)},
        }

        msg = requests.post(
            url=self._get_whatsapp_url(),
            headers={
                "Authorization": self.whatsapp_bearer_token,
                "Content-Type": "application/json",
            },
            data=json.dumps(body),
        )

        logging.info(msg.status_code)
        logging.info(msg.content)

        return msg.status_code
