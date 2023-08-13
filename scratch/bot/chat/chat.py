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
        """TODO: Implement converting this object to a json string"""
        pass

    @staticmethod
    def from_json(str) -> "Chat":
        """Create and return a new Chat object from a json string"""

    def is_valid(self) -> (bool, Optional[str]):
        """Apply validation rules to check if this chat is still valid.
        For example check if it has ended or cost has overrun."""
