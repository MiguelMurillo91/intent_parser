import os

import pytest

from intent_parser.anthropic_client import AnthropicClient
from intent_parser.models import Action, IntentType
from intent_parser.parser import parse_intent


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="no ANTHROPIC_API_KEY set",
)
def test_real_api_parses_a_command():
    intent = parse_intent("turn off the lights in the main room", AnthropicClient())
    assert intent is not None
    assert intent.intent_type == IntentType.DEVICE_CONTROL
    assert intent.action == Action.OFF
    assert intent.room == "main_room"
