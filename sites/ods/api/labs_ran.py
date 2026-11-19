"""How a notebook was run, read off the file (T354 §3): execution counts and the moments Colab or Jupyter stamped."""
from datetime import datetime, timezone
from itertools import pairwise

import labs_out


def ran(nb: dict) -> dict | None:
    """{count, of, ordered, fresh, errors}: fresh — counts 1…k in a row over every cell («перезапустити й виконати все»);
    marimo's .py carries no outputs — None."""
    if nb["kind"] == "marimo":
        return None
    code = [c for c in nb["cells"] if c["kind"] == "code" and c["source"].strip()]
    counts = [c["count"] for c in code if c["count"] is not None]
    return {"count": len(counts), "of": len(code), "ordered": all(a < b for a, b in pairwise(counts)),
            "fresh": counts == list(range(1, len(code) + 1)), "errors": sum(bool(labs_out.error(c["outputs"])) for c in code)}


def moment(meta: dict) -> datetime | None:
    """Colab's executionInfo.timestamp (ms) or Jupyter's start of execution; whose account it was is not kept."""
    info, run = meta.get("executionInfo"), meta.get("execution")
    try:
        if isinstance(info, dict) and isinstance(ts := info.get("timestamp"), (int, float)):
            return datetime.fromtimestamp(ts / 1000, timezone.utc)
        at = datetime.fromisoformat(run["iopub.execute_input"])
        return at if at.tzinfo else at.replace(tzinfo=timezone.utc)
    except (KeyError, TypeError, ValueError, OverflowError, OSError):
        return None


def times(cells: list[dict]) -> dict | None:
    """{first, last} — the first and the last cell run."""
    at = sorted(t for c in cells if (t := moment(c["meta"])))
    return {"first": at[0].isoformat(), "last": at[-1].isoformat()} if at else None
