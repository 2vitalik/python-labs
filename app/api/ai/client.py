"""The one call to the Claude API (T291 §14): the stable start cached, the answer as JSON by the schema, no streaming.
A failure comes back as AskError with a line for the student; its `usage` is kept — a refusal is paid for too."""
import json
import logging
from functools import cache

import anthropic

from core.config import settings

FALLBACK = ("claude-sonnet-5-5", "claude-opus-5-5")  # the server retries a classifier's refusal on another model; Haiku has none
TOKENS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
logger = logging.getLogger(__name__)


class AskError(Exception):
    def __init__(self, message: str, usage: dict | None = None):
        super().__init__(message)
        self.message, self.usage = message, usage or {}


@cache
def client(key: str) -> anthropic.AsyncAnthropic:
    return anthropic.AsyncAnthropic(api_key=key)


def request(model: str, system: str, user: str, schema: dict) -> dict:
    """The named arguments of messages.create — the smoke checks the SDK takes each of them."""
    kw = {"model": model, "max_tokens": 16000, "messages": [{"role": "user", "content": user}],
          "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
          "output_config": {"effort": settings.ai_effort, "format": {"type": "json_schema", "schema": schema}}}
    return kw | ({"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"} if model in FALLBACK else {})


async def ask(model: str, system: str, user: str, schema: dict) -> tuple[dict, dict]:
    """(the answer, usage with the model that answered)."""
    kw, api = request(model, system, user, schema), client(settings.anthropic_api_key)
    try:
        r = await (api.beta.messages.create(**kw) if "betas" in kw else api.messages.create(**kw))
    except anthropic.RateLimitError:
        raise AskError("ШІ-помічник зараз перевантажений — спробуй за хвилину")
    except (anthropic.AuthenticationError, anthropic.PermissionDeniedError) as e:
        logger.error("anthropic key: %s", e)
        raise AskError("Ключ API Anthropic не прийнято — напиши викладачеві")
    except anthropic.APIStatusError as e:
        logger.error("anthropic %s: %s", e.status_code, e)
        raise AskError("API Anthropic не відповів — спробуй пізніше")
    except anthropic.APIConnectionError as e:
        logger.error("anthropic connection: %s", e)
        raise AskError("Нема звʼязку з API Anthropic — спробуй пізніше")
    usage = {"model": r.model} | {k: getattr(r.usage, k, 0) or 0 for k in TOKENS}
    if r.stop_reason == "refusal":
        raise AskError("Модель відмовилась розбирати цей текст — спробуй сформулювати інакше", usage)
    if r.stop_reason == "max_tokens":
        raise AskError("Текст завеликий для одного розбору — розбий на частини", usage)
    try:
        return json.loads(next(b.text for b in r.content if b.type == "text")), usage
    except (StopIteration, json.JSONDecodeError):
        raise AskError("Модель відповіла не за формою — спробуй ще раз", usage)
