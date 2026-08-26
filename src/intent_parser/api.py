from functools import lru_cache
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from intent_parser.anthropic_client import AnthropicClient
from intent_parser.llm import LLMClient
from intent_parser.models import Intent
from intent_parser.parser import parse_intent

load_dotenv()

app = FastAPI(title="intent-parser")


@lru_cache
def get_llm_client() -> LLMClient:
    """Build the real LLM client once and reuse it."""
    return AnthropicClient()


class ParseRequest(BaseModel):
    """The JSON body a client must send to /parse."""

    text: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
def parse(
    request: ParseRequest,
    client: Annotated[LLMClient, Depends(get_llm_client)],
) -> Intent | None:
    return parse_intent(request.text, client)
