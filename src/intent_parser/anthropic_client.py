from anthropic import Anthropic

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 512


class AnthropicClient:
    """Real LLM client. Sends prompts to Anthropic's API."""

    def __init__(self, model: str = MODEL) -> None:
        self._client = Anthropic()
        self._model = model

    def complete(self, prompt: str) -> str:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        for block in message.content:
            if block.type == "text":
                return block.text
        return ""
