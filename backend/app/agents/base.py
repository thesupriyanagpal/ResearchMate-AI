from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the agent's logic.
        :param query: The user's input or task description.
        :param context: Additional context (e.g., file paths, history).
        :return: A dictionary containing the result.
        """
        pass
