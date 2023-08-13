from .prompt import Prompt
from pathlib import Path
import os


class PromptService:
    def __init__(self, prompt_directory: str) -> None:
        """Designed to help centralise logic for loading key prompts.
        If the solution size increased, you could make this more generic."""
        self.prompt_directory = prompt_directory

    def get_continuation_prompt(self) -> Prompt:
        """For continuing an existing conversation with a customer."""
        return Prompt.build_from("%MSG%{input_message}%MSG%")

    def get_initial_prompt(self) -> Prompt:
        """Prompt when we received a message from a customer for the first time."""
        prompt_path = Path(os.getcwd(), self.prompt_directory, "initial_prompt.txt")
        print(prompt_path)
        return Prompt.build_from(prompt_path)

    def get_order_prompt(self) -> Prompt:
        """Prompt to pass to the order LLM - to extract relevant order details and determine if new order is required yet.
        TODO: 
        Follow the examples above to load the 'order_prompt.txt' file."""
        pass

    def get_cus_response_prompt(self) -> Prompt:
        """Prompt to extract the exact text that should be returned to a customer.
        TODO: 
        Follow the examples above to load the 'cus_response_prompt.txt' file."""
        pass
