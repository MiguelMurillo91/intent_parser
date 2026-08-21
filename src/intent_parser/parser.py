import json

from pydantic import ValidationError

from intent_parser.llm import LLMClient
from intent_parser.models import Intent

PROMPT_TEMPLATE = """Extract the smart-home intent from the user's message.
Respond with ONLY a JSON object. No markdown, no explanation, no code fences.

Keys:
  intent_type: one of device_control, query, unknown
  device: the device name
  room: the room name
  action: one of on, off, toggle
  confidence: a number between 0 and 1

Message: {text}"""


def parse_intent(text: str, client: LLMClient) -> Intent | None:
    """Ask the LLM to extract an intent. Returns None if the response is unusable."""
    prompt = PROMPT_TEMPLATE.format(text=text)
    raw = client.complete(prompt)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None

    try:
        return Intent.model_validate(data)
    except ValidationError:
        return None
