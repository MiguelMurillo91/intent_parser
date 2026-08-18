from enum import StrEnum
from pydantic import BaseModel, Field, field_validator
from intent_parser.intent import normalize_room


class IntentType(StrEnum):
    DEVICE_CONTROL = "device_control"
    QUERY = "query"
    UNKNOWN = "unknown"


class Action(StrEnum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"


class Intent(BaseModel):
    intent_type: IntentType
    device: str
    room: str
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("room")
    @classmethod
    def _normalize_room(cls, value: str) -> str:
        return normalize_room(value)
