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
        # If api key is none or empty - just return a blank response (testing)
        if not self.api_key:
            return LLMResponse("", "", 0)

        openai.organization = ""
        openai.api_key = self.api_key

        logging.info("Sending Chat Completion Request to Open AI")

        completion = openai.ChatCompletion.create(
            model=str(self.model), messages=[{"role": "user", "content": prompt}]
        )

        logging.info("Received Chat Completion Request from Open AI")

        response = completion.choices[0].message.content
        concat_response = f"{prompt}\n{response}"

        total_tokens = completion.usage.total_tokens
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        cost = self._calc_cost(
            self.model, total_tokens, prompt_tokens, completion_tokens
        )

        return LLMResponse(
            response=response, concat_response=concat_response, cost=cost
        )

    def _calc_cost(self, model: Model, total_tokens, prompt_tokens, completion_tokens):
        if model == Model.GPT35:
            cost = total_tokens * 0.002 / 1000
        elif model == Model.GPT4:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
        else:
            raise Exception(f"Cost calc not supported for model type: {str(model)}")
        return cost
