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
        """TODO: How can we check if a user already exists?"""
        pass

    def load_chat(self, wa_id) -> Union[Chat, None]:
        """TODO: We want to read the chat json file from disk for this user."""
        pass
        
    def save_chat(self, chat: Chat):
        """TODO: We want to save the chat json file to disk. WA_ID is contained in the chat object."""
        pass