from intent_parser.llm import FakeLLM


def test_fake_returns_canned_response():
    fake = FakeLLM("canned answer")
    assert fake.complete("test prompt") == "canned answer"


def test_fake_llm_call_list():
    fake = FakeLLM("canned answer")
    fake.complete("prompt_1")
    fake.complete("prompt_2")
    assert len(fake.calls) == 2
    assert fake.calls[0] == "prompt_1"
    assert fake.calls[1] == "prompt_2"
