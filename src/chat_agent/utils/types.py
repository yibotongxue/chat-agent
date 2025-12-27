from typing import Any

from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class InputData(BaseModel):
    messages: list[Message]
    meta_data: dict[str, Any]

class OutputData(BaseModel):
    response: str
    input: InputData
    is_tool_calling: bool
    search_query: str | None
    meta_data: dict[str, Any]
