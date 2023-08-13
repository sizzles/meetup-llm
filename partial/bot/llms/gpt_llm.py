from .base_llm import BaseLLM, LLMResponse
from typing import Union
from enum import Enum
import openai
import logging


class Model(Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"

    def __str__(self) -> str:
        return self.value


class GPTLLM(BaseLLM):
    def __init__(self, model: Model, api_key: Union[str, None]):
        BaseLLM.__init__(self)
        self.model = model
        self.api_key = api_key

    def set_model(self, model: Model):
        self.model = model

    def get_response(self, prompt: str) -> LLMResponse:
        """TODO: We need to:
         
          1) send a message to the OpenAI api (think about what happens if the api key is not set - would this be useful perhaps?)
          2) extract the 'text' we are interested in from the response
          3) calcualte the cost of the request
          4) concat the response to include original prompt + repsonse from OpenAI
          5) return an LLMResponse object containing the correct data"""
        
        response = ""
        concat_response = ""
        cost =0
        return LLMResponse(
            response=response, concat_response=concat_response, cost=cost
        )

    def _calc_cost(self, model: Model, total_tokens, prompt_tokens, completion_tokens):
        """TODO: Use this method with the correct args to calculate the cost in $ for the request/response from OpenAI."""
        if model == Model.GPT35:
            cost = total_tokens * 0.002 / 1000
        elif model == Model.GPT4:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
        else:
            raise Exception(f"Cost calc not supported for model type: {str(model)}")
        return cost
