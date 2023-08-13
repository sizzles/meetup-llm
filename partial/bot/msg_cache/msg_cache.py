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
        """TODO: Add a CachedMessage to the cache for the wa_id specified.
        Think about how to make sure it is thread safe? Hint think about cache lock.
        Think about fields in cached message.
        Hint - for received_at consider timezones and issues that coudl bring"""
        pass
    

    def get_cached_msgs(self, wa_id):
        """TODO: 
        1) Get the list of cached messages for the given wa_id
        2) Concat them all into a string 
        3) Return the input message and the time received of the most recent message
        Think about how to make sure it is thread safe? Hint think about cache lock.
        Hint the messages are in the format m.message.get('text').get('body')
        Hint using [-1] will address the item at the end of a list
        """
        pass
 