from dataclasses import dataclass
from typing import Union, Optional
import json
import re


@dataclass
class Chat:
    """Domain object for 'chat' """
    wa_id: str
    chat_message: str = ""
    cost: Union[float, int] = 0
    has_ended: bool = False

    def to_json(self) -> str:
        return json.dumps(
            {
                "wa_id": self.wa_id,
                "chat_message": self.chat_message,
                "cost": self.cost,
                "has_ended": self.has_ended,
            }
        )

    def should_end(self) -> bool:
        """If our chat contains more than 1 %END tag - end the chat."""
        return len(re.findall(re.escape("%END%"), self.chat_message)) == 2

    @staticmethod
    def from_json(str) -> "Chat":
        j = json.loads(str)
        return Chat(
            wa_id=j["wa_id"],
            chat_message=j["chat_message"],
            cost=j["cost"],
            has_ended=j["has_ended"],
        )

    def is_valid(self) -> (bool, Optional[str]):
        if self.has_ended:
            return (
                False,
                "Thanks for your enquiry - sorry we couldn't help you today.",
            )
        if self.cost > 0.2:
            return (
                False,
                "We are a little busy right now - someone will get back to you shortly.",
            )

        return (True, None)
