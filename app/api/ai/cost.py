"""What a request cost, from the API's `usage` (T291 §14). $ per million tokens: input, output, cache read; a cache write is
the input ×1.25. Haiku's price is for a prompt up to 100K tokens — ours is far below."""
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50, 0.01),
    "claude-sonnet-5-5": (2, 10, 0.10),
    "claude-opus-5-5": (4, 20, 0.20),
}
WRITE = 1.25
UNKNOWN = PRICES["claude-opus-5-5"]  # a model the table lacks: count it dear, the budget errs on the safe side


def of(usage: dict, model: str) -> float:
    """`usage` — client.ask()'s, with the model that answered (a fallback may); `model` — the one asked."""
    if not usage:
        return 0
    inp, out, read = PRICES.get(usage.get("model")) or PRICES.get(model) or UNKNOWN
    n = lambda k: usage.get(k) or 0  # noqa: E731
    total = n("input_tokens") * inp + n("cache_creation_input_tokens") * inp * WRITE + n("cache_read_input_tokens") * read + n("output_tokens") * out
    return round(total / 1e6, 6)
