from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from intent_parser.anthropic_client import AnthropicClient
from intent_parser.parser import parse_intent
from intent_parser.models import Intent

load_dotenv()

app = FastAPI(title="intent-parser")


class ParseRequest(BaseModel):
    """The JSON body a client must send to /parse"""

    text: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse")
def parse(request: ParseRequest) -> Intent | None:
    return parse_intent(request.text, AnthropicClient())
