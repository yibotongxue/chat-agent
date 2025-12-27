from abc import ABC, abstractmethod
from typing import Any

class BaseSearch(ABC):
    def __init__(self, search_cfgs: dict[str, Any]) -> None:
        self.search_cfgs = search_cfgs

    @abstractmethod
    def search(self, query: str) -> list[str]:
        pass
