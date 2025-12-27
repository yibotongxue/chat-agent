from .base import BaseSearch
from typing import Any

class MockSearch(BaseSearch):
    def __init__(self, search_cfgs: dict[str, Any]) -> None:
        super().__init__(search_cfgs)

    def search(self, query: str) -> list[str]:
        print("MockSearch received query:", query)
        return ["Mocked search result 1 for query: " + query,]