from typing import Protocol


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str: ...


class FakeLLM:
    """A stand in LLM for tests. Always returnt the response you gave it"""

    def __init__(self, response: str) -> None:
        self._response = response
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self._response


def _check(client: LLMClient) -> str:
    return client.complete("hi")


_check(FakeLLM("ok"))