# ---------- Stage 1: build ----------
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Dependencies first — this layer is cached unless pyproject/uv.lock change
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Now the source, which changes often
COPY src/ src/
RUN uv sync --frozen --no-dev


# ---------- Stage 2: runtime ----------
FROM python:3.14-slim AS runtime

RUN useradd --create-home --uid 1000 app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"

USER app

EXPOSE 8000

CMD ["uvicorn", "intent_parser.api:app", "--host", "0.0.0.0", "--port", "8000"]