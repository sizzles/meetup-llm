from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class LLMResponse:
    response: str
    concat_response: str
    cost: Union[float, int]


class BaseLLM(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def get_response(self, prompt: str) -> LLMResponse:
        ...
