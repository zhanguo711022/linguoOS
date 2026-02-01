from typing import Protocol


class Agent(Protocol):
    def name(self) -> str:
        ...
