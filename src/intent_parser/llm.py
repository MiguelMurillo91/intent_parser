from typing import Protocol


class LLMClient(Protocol):
    """Anything that can turn a prompt into a text response."""

    def complete(self, prompt: str) -> str: ...


class FakeLLM:
    """A stand in LLM for tests. Always returnt the response you gave it"""

    def __init__(self, response: str) -> None:
        self._response = response
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self._response
