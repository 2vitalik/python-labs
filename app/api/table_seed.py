"""The site's own views of /table (T315 §10): what each lab's deadline asks for — the columns of «Лаба N» when it is first made.
Deadline 1 — registered everywhere and a minimal lab; deadline 2 — the lab's minimum and the game described on the site;
from lab 3 on — the game's table filled, and a demo video for labs 3 and 4 (T318). The teacher edits the views afterwards:
this is only where they start."""
from core import views_seed

MARKS = "lab.before,lab.last,lab.asked,lab.ext,lab.met,lab.note,fields:lab,polls:lab"
GAME = "gname,gfill,gents,gwins,grules"
views_seed.LAB_COLS |= {
    1: f"reg,seen,bot,gh,repo,lab,lab.review,lab.required,lab.kind,{MARKS}",
    2: f"lab,lab.review,lab.required,lab.kind,gname,gfill,{MARKS}",
    3: f"lab,lab.review,lab.required,demo3,{GAME},claims,{MARKS}",
    4: f"lab,lab.review,lab.required,demo4,{GAME},claims,{MARKS}",
    0: f"lab,lab.review,lab.required,{GAME},claims,{MARKS}",
}
views_seed.LAB_ABOUT |= {
    1: "Дедлайн 1: зареєструватись усюди — сайт, бот, GitHub — і здати мінімальну версію лаби.",
    2: "Дедлайн 2: мінімум завдань лаби й гра на сайті, описана хоча б мінімально.",
    3: "Дедлайн 3: код з ООП, таблиця гри заповнена хоча б частково, демо-відео — обовʼязково.",
    4: "Дедлайн 4: код, заповнена таблиця гри, демо-відео.",
    0: "Дедлайн лаби: код і заповнена таблиця гри.",
}
