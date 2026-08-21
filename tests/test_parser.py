from intent_parser.llm import FakeLLM
from intent_parser.models import Action, IntentType
from intent_parser.parser import parse_intent

VALID_JSON = (
    '{"intent_type": "device_control", "device": "switch 1", '
    '"room": "Main Room", "action": "off", "confidence": 0.94}'
)

INVALID_ANSWER = '{"Sure, here is your answer:"}'

INVALID_VALUE_CONFIDENCE = (
    '{"intent_type": "device_control", "device": "switch 1", '
    '"room": "Main Room", "action": "off", "confidence": 1.56}'
)

INVALID_MISSING_VALUES = '{"device": "switch 1"}'


def test_parses_valid_response():
    intent = parse_intent("turn off switch 1", FakeLLM(VALID_JSON))
    assert intent is not None
    assert intent.intent_type == IntentType.DEVICE_CONTROL
    assert intent.device == "switch 1"
    assert intent.room == "main_room"
    assert intent.action == Action.OFF
    assert intent.confidence == 0.94


def test_invalid_answer():
    intent = parse_intent("turn off switch 2", FakeLLM(INVALID_ANSWER))
    assert intent == None


def test_invalid_value_confidence():
    intent = parse_intent("turn off switch 3", FakeLLM(INVALID_VALUE_CONFIDENCE))
    assert intent == None


def test_missing_values():
    intent = parse_intent("turn off switch 3", FakeLLM(INVALID_MISSING_VALUES))
    assert intent == None


def test_prompt_contains_user_text():
    fake = FakeLLM(VALID_JSON)
    parse_intent("turn off lights", fake)
    assert "turn off lights" in fake.calls[0]
