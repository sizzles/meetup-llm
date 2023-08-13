from typing import Union
from typing import Union, Dict
from pathlib import Path


class Prompt:
    def __init__(self, template: str):
        self.template = template

    @staticmethod
    def build_from(template_source: Union[str, "Path"]) -> "Prompt":
        """TODO: Creates a prompt from either a file or text directly."""
        pass

    def to_str(self, input_vars: Union[Dict[str, str], None] = None) -> str:
        """TODO: Converts to a string and substitutes in the variables enclosed with {} for values in input_vars."""
        pass
        
    def concat(self, next_prompt: Union["Prompt", str]) -> "Prompt":
        """TODO: Joins together base templates of two prompts and returns a new Prompt object."""
        pass