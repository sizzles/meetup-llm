from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
from threading import Lock


@dataclass
class CachedMessage:
    received_at: datetime
    message: str


class MsgCache:
    def __init__(self) -> None:
        """Holds incoming WhatsApp messages in memory. Messages are quickly inserted so a response can be quickly returned to WhatsApp."""
        self.incoming_msg_cache = defaultdict(list)
        self.cache_lock = Lock()

    def append(self, wa_id, message):
        now = datetime.utcnow()
        cached_msg = CachedMessage(received_at=now, message=message)

        with self.cache_lock:
            self.incoming_msg_cache[wa_id].append(cached_msg)

    def get_cached_msgs(self, wa_id):
        with self.cache_lock:
            messages = self.incoming_msg_cache[wa_id]

            if len(messages) == 0:
                return None, None

            last_received = messages[-1].received_at
            messages = list(
                map(
                    lambda m: m.message.get("text").get("body"),
                    self.incoming_msg_cache[wa_id],
                )
            )
            input_message = str.join("\n", messages)

        return input_message, last_received
