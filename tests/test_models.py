import pytest
from intent_parser.models import Intent, IntentType, Action
from pydantic import ValidationError


def test_intent_model():
    intent = Intent(
        intent_type=IntentType.DEVICE_CONTROL,
        device="switch 1",
        room="main room",
        action=Action.ON,
        confidence=0.6,
    )

    assert intent.intent_type == IntentType.DEVICE_CONTROL
    assert intent.device == "switch 1"
    assert intent.room == "main_room"
    assert intent.action == Action.ON
    assert intent.confidence == 0.6


def test_rejects_confidence_grater_one():
    with pytest.raises(ValidationError,  match="less_than_equal"):
        intent = Intent(
            intent_type=IntentType.DEVICE_CONTROL,
            device="switch 1",
            room="main room",
            action=Action.ON,
            confidence=1.5,
        )

        assert intent.confidence <= 1


def test_rejects_confidence_less_zero():
    with pytest.raises(ValidationError,  match="greater_than_equal"):
        intent = Intent(
            intent_type=IntentType.DEVICE_CONTROL,
            device="switch 1",
            room="main room",
            action=Action.ON,
            confidence=-0.5
        )

        assert intent.confidence <= 1


def test_intent_parser():
    intent = Intent(
        intent_type=IntentType.DEVICE_CONTROL,
        device="switch 1",
        room="main room",
        action=Action.OFF,
        confidence=0.5,
    )

    assert intent.room == "main_room"


def test_rejects_no_valid_action():
    with pytest.raises(ValidationError):
        Intent(
            intent_type=IntentType.DEVICE_CONTROL,
            device="switch 1",
            room="main room",
            action="break",
            confidence=0.5,
        )
