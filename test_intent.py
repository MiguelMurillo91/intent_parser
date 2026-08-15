from intent import normalize_room


def test_nomalizes_spaced_and_case():
    assert normalize_room("  Living Room  ") == "livingroom"
    assert normalize_room("KITCHEN") == "kitchen"
    assert normalize_room("  Bedroom  ") == "bedroom"
    assert normalize_room("Dining Room") == "dining_room"
