from typing import Any, override

from openai import OpenAI

from .base import BaseLLM
from ..utils.types import InputData, OutputData

class OpenAILLM(BaseLLM):
    def __init__(self, model_cfgs: dict[str, Any], inference_cfgs: dict[str, Any]) -> None:
        super().__init__(model_cfgs, inference_cfgs)
        self.model_name = model_cfgs.get("model_name", "deepseek-chat")
        base_url = model_cfgs.get("base_url", "https://api.deepseek.com")
        api_key = model_cfgs.get("api_key", "")
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    @override
    def generate(self, input_data: InputData) -> OutputData:
        messages = input_data.messages
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **self.inference_cfgs,
        )
        raw_response = response.choices[0].message.content
        if "<search_query>" in raw_response and "</search_query>" in raw_response:
            search_query = raw_response.split("<search_query>")[1].split("</search_query>")[0].strip()
            return OutputData(
                response="",
                input=input_data,
                is_tool_calling=True,
                search_query=search_query,
                meta_data={},
            )
        return OutputData(
            response=raw_response,
            input=input_data,
            is_tool_calling=False,
            search_query=None,
            meta_data={},
        )
