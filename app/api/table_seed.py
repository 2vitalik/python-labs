"""The site's own views of /table (T315 §10): what each lab's deadline asks for — the columns of «Лаба N» when it is first made.
Deadline 1 — registered everywhere and a minimal lab; deadline 2 — the lab's minimum and the game described on the site;
from lab 3 on — the game's table filled. The teacher edits the views afterwards: this is only where they start."""
from core import views_seed

MARKS = "lab.before,lab.last,lab.asked,lab.ext,lab.met,lab.note,polls:lab,fields:lab"
views_seed.LAB_COLS |= {
    1: f"reg,seen,bot,gh,repo,lab,lab.review,lab.required,lab.kind,{MARKS}",
    2: f"lab,lab.review,lab.required,lab.kind,gname,gfill,{MARKS}",
    0: f"lab,lab.review,lab.required,gname,gfill,gents,gwins,grules,claims,{MARKS}",
}
views_seed.LAB_ABOUT |= {
    1: "Дедлайн 1: зареєструватись усюди — сайт, бот, GitHub — і здати мінімальну версію лаби.",
    2: "Дедлайн 2: мінімум завдань лаби й гра на сайті, описана хоча б мінімально.",
    0: "Дедлайн лаби: код, заповнена таблиця гри, демо.",
}
