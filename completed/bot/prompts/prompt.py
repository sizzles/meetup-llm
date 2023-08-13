from typing import Union
from typing import Union, Dict
from pathlib import Path


class Prompt:
    def __init__(self, template: str):
        self.template = template

    @staticmethod
    def build_from(template_source: Union[str, "Path"]) -> "Prompt":
        """Creates a prompt from either a file or text directly."""
        if isinstance(template_source, str):
            return Prompt(template_source)

        elif isinstance(template_source, Path):
            # Eagerly load the file
            with template_source.open("r") as file:
                return Prompt(file.read())
        else:
            raise TypeError(
                f"Unsupported source template type: {str(type(template_source))}"
            )

    def to_str(self, input_vars: Union[Dict[str, str], None] = None) -> str:
        """Converts to a string and substitutes in the variables enclosed with {} for values in input_vars."""
        if input_vars is None:
            return self.template
        elif isinstance(input_vars, Dict):
            return self.template.format(**input_vars)
        else:
            raise TypeError(f"Unsupported input var type: {str(type(input_vars))}")

    def concat(self, next_prompt: Union["Prompt", str]) -> "Prompt":
        """Joins together base templates of two prompts and returns a new Prompt object."""
        if isinstance(next_prompt, Prompt):
            next_prompt = next_prompt.to_str(None)
        elif isinstance(next_prompt, str):
            pass
        else:
            raise TypeError(f"Unsupported next prompt type: {str(type(next_prompt))}")

        new_template = f"{self.template}{next_prompt}"
        return Prompt.build_from(new_template)
