"""The catalog as the model sees it: active cards in the catalog's order — zone, subzone, the card's place in the file.
The same for everyone, so the prompt built from it stays the same byte for byte (the cache)."""
from models.task import Task
from zones import ZONES, kind_of

CLAIMED = ("mechanic", "element", "rule", "level", "field", "game")  # written as claims; the other kinds are picked in the forms


class Source:
    def __init__(self, cards: list[Task]):
        self.cards = cards

    def of(self, *kinds: str) -> list[Task]:
        return [t for t in self.cards if kind_of(t) in kinds]

    def opts(self, kind: str) -> dict[str, Task]:
        """opt → card, the first one wins — as options.catalog() picks."""
        out = {}
        for t in self.of(kind):
            if t.opt:
                out.setdefault(t.opt, t)
        return out

    def values(self, prop: str) -> list[str]:
        """A field property's options: the `prop:value` opts of fieldopt cards."""
        return [o.split(":", 1)[1] for o in self.opts("fieldopt") if o.startswith(prop + ":")]


async def load() -> Source:
    zones = {z: i for i, z in enumerate(ZONES)}
    subs = {(z, s): i for z in ZONES for i, s in enumerate(ZONES[z]["subzones"])}
    cards = await Task.find(Task.status == "active").to_list()
    cards.sort(key=lambda t: (zones.get(t.zone, len(zones)), subs.get((t.zone, t.subzone), 99), t.order, t.slug))
    return Source(cards)
