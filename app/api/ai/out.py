"""The proposals being made of one answer (AI-CONTRACT §3): keys, states, what points at what. A proposal names the others
it needs by (kind, title) while the answer is read; finish() turns those into keys once every proposal has one."""
from ai.check import card
from ai.context import Ctx

PREFIX = {"field": "f", "entity": "e", "rule": "r", "window": "w", "level": "l", "claim": "c", "unknown": "u"}


def quote(x: dict) -> str:
    return " ".join(str(x.get("quote", "")).split())[:300]


def text(x: dict, key: str) -> str:
    return " ".join(str(x.get(key, "")).split())


def title(x: dict) -> str:
    return text(x, "title")


class Out:
    def __init__(self, ctx: Ctx):
        self.ctx = ctx
        self.items = {g: [] for g in PREFIX}
        # (kind, title.lower()) → (token, title): the game's entities and windows by id, proposals by a «new:» token
        self.names = {k: v for k, v in ctx.parts.items() if k[0] in ("entity", "window")}
        self.keys: dict[tuple, str] = {}  # (kind, title.lower()) → the proposal's key
        self.failed: set[tuple] = set()  # proposals that did not pass: a rule naming one does not either

    def add(self, group: str, data: dict, quote: str, hint: str = "", needs=(), state: str = "open") -> str:
        n = len(self.items[group]) + 1
        key = "f" if group == "field" else f"{PREFIX[group]}{n}"
        self.items[group].append({"key": key, "group": group, "data": data, "quote": quote, "hint": hint,
                                  "needs": [] if state == "exists" else list(needs), "state": state, "made": ""})
        return key

    def unknown(self, quote: str, why: str, candidates=()) -> None:
        self.add("unknown", {"why": why, "candidates": [c for c in dict.fromkeys(candidates) if c in self.ctx.cards]}, quote)

    def name(self, kind: str, title: str) -> tuple:
        """A proposal the rules and menus may point at; its key comes with add()."""
        ref = (kind, title.lower())
        self.names[ref] = (f"new:{kind}:{title.lower()}", title)
        return ref

    def claims(self, x: dict, where: str, label: str, anchor: tuple | None) -> tuple[list, bool]:
        """The good cards of a proposal; a bad one goes to «не розпізнано» with the proposal's quote. Second: every card is
        claimed on `anchor` (part, rule) already — None when the proposal is new to the game."""
        good = []
        for c in x.get("claims") or []:
            data, why = card(self.ctx, c, where, False)
            if not data:
                self.unknown(quote(x), f"{label}: {why}", [str(c.get("slug", ""))])
            elif data not in good:
                good.append(data)
        old = anchor is not None and all((c["slug"], *anchor) in self.ctx.claimed for c in good)
        return good, old

    def finish(self) -> list[dict]:
        out = [it for g in PREFIX for it in self.items[g]]
        for it in out:
            it["needs"] = list(dict.fromkeys(self.keys[r] for r in it["needs"] if r in self.keys))
        return out
