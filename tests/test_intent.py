import pytest

from intent_parser.intent import normalize_room


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Living Room  ", "living_room"),
        ("KITCHEN", "kitchen"),
        ("  Bedroom  ", "bedroom"),
        ("Dining Room", "dining_room"),
    ],
)
def test_nomalizes_spaced_and_case(raw: str, expected: str) -> None:
    assert normalize_room(raw) == expected
