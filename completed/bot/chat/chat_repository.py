import os
from .chat import Chat
from typing import Union


class ChatRepository:
    def __init__(self, data_folder: str) -> None:
        """Base repository - adding a layer over local file system, working with jsons."""
        self.data_folder = data_folder
        self.chat_file = "chat.json"

    def _get_chat_path(self, wa_id):
        return os.path.join(self.data_folder, wa_id, self.chat_file)

    def exists(self, wa_id: str) -> bool:
        chat_file = self._get_chat_path(wa_id)
        return os.path.exists(chat_file)

    def load_chat(self, wa_id) -> Union[Chat, None]:
        if not self.exists(wa_id):
            # Can't load what we don't have
            return None

        chat_file = self._get_chat_path(wa_id)
        with open(chat_file, "r") as f:
            chat = Chat.from_json(f.read())
        return chat

    def save_chat(self, chat: Chat):
        chat_folder = os.path.join(self.data_folder, chat.wa_id)

        os.makedirs(chat_folder, exist_ok=True)
        chat_file = os.path.join(chat_folder, self.chat_file)

        with open(chat_file, "w") as f:
            f.write(chat.to_json())
