"""The site's own views (T315 §7): «Усе», «Старт», «Лаба N» live in the base as etalons, their version 1 is the factory one.
The teacher edits and archives them like any other; one deleted for good does not come back."""
from pymongo.errors import DuplicateKeyError

from core.config import settings
from core.models.pref import get_pref, set_pref
from core.models.view import View, ViewVersion

GONE = "table.seeds_gone"
# the columns of «Усе» and «Старт»; `{labs}` — the state of every lab. A site whose row differs puts its own here
ALL_COLS = "fio,seen,bot,tg,gh,repo,commits,{labs},fields:"
START_COLS = "reg,fio,seen,last,bot,tg,gh,repo,commits,lastc,polls:start"
START_ABOUT = "Лійка реєстрації: хто зайшов на сайт, привʼязав бота, дав GitHub і запушив перший коміт."
# the columns and the «для чого» of a lab's view; a site adds its own by the lab's number, 0 — any other lab
LAB_COLS = {0: "reg,lab,lab.review,lab.required,lab.kind,lab.before,lab.after,lab.last,lab.asked,lab.ext,lab.met,lab.note,fields:lab,polls:lab"}
LAB_ABOUT = {0: "Дедлайн лаби: стан кожного студента, звіт агента, подовження й відповіді опитувань."}
# the verdict of a deadline (T340): who made it, who did not, and the borderline ones by their case
DUE_COLS = "lab.answer,lab.case,lab.late,lab.says,lab.flags,lab.met,lab.note,lab.due,lab.asked,lab.ext,lab.review,lab.before,lab.after,lab.last,reg,tg"
DUE_ABOUT = ("Вклався чи ні: чіткі «так», чіткі «ні» й пограничні — групами за випадком. Сайт зводить звіт агента, коміти, подовження "
             "й опитування; останнє слово — колонка ✍.")
DUE_PINNED = 2  # the deadlines on the tabs from the start; the rest wait in the library


def course_labs() -> list[int]:
    return list(range(1, settings.labs + 1))


def seeds(labs: list[int]) -> list[dict]:
    each = ",".join(f"lab{n}" for n in labs)
    return [{"slug": "all", "title": "Усе", "emoji": "📋", "about": "Усі студенти й стан кожної лаби — з цього зручно починати свій вид.",
             "query": {"cols": ALL_COLS.format(labs=each), "group": "group"}},
            {"slug": "start", "title": "Старт", "emoji": "🚀", "about": START_ABOUT,
             "query": {"cols": START_COLS, "group": "group"}},
            *({"slug": f"lab{n}", "title": f"Лаба {n}", "emoji": "📅", "about": LAB_ABOUT.get(n, LAB_ABOUT[0]),
               "query": {"lab": str(n), "cols": LAB_COLS.get(n, LAB_COLS[0]), "group": "group"}} for n in labs),
            *({"slug": f"due{n}", "title": f"Дедлайн {n}", "emoji": "🏁", "about": DUE_ABOUT, "folder": "Дедлайни", "pinned": n <= DUE_PINNED,
               "query": {"lab": str(n), "cols": DUE_COLS, "group": "lab.answer,lab.case"}} for n in labs)]


async def ensure_seeds():
    """The missing ones made, first in order: a view that is there, archived too, stays as the teacher left it."""
    skip = {*await View.get_pymongo_collection().distinct("slug"), *await get_pref(GONE, [])}
    for i, s in enumerate(seeds(course_labs())):
        if s["slug"] in skip:
            continue
        try:
            v = await View(**s, etalon=True, version=1, order=-100 + i).insert()
        except DuplicateKeyError:  # a parallel request made it first
            continue
        await ViewVersion(view=v.slug, n=1, title=v.title, emoji=v.emoji, query=v.query, at=v.created_at).insert()


async def forget_seed(slug: str):
    """A site's view deleted for good: ensure_seeds() does not make it again."""
    gone = await get_pref(GONE, [])
    if slug in {s["slug"] for s in seeds(course_labs())} and slug not in gone:
        await set_pref(GONE, [*gone, slug])
