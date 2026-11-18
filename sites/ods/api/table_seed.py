"""The site's own views of /table (T352): ODS has no repositories — a lab is a card, an answer line and the teacher's points.
The teacher edits the views afterwards: this is only where they start."""
from core import views_seed
from core.config import settings

# «Усе»: the answers and the points of every lab — a lab's state says little here till the site reads it off the answer line
LABS = ",".join(f"lab{n}.ok,lab{n}.points" for n in range(1, settings.labs + 1))
views_seed.ALL_COLS = f"fio,seen,bot,tg,{LABS},fields:"
views_seed.START_COLS = "fio,seen,last,bot,tg,polls:start"
views_seed.START_ABOUT = "Лійка реєстрації: хто зайшов на сайт і привʼязав бота."
VARIANT = "lab.vid,lab.ok,lab.tries,lab.checked,lab.nb,lab.points,lab.pnote"  # sites/ods/vue/src/labCols.js
MARKS = "lab.asked,lab.ext,lab.met,lab.note,fields:lab,polls:lab"
views_seed.LAB_COLS |= {0: f"lab,{VARIANT},{MARKS}"}
views_seed.LAB_ABOUT |= {0: "Лаба: картка кожного студента, рядок відповідей і спроби, ноутбук, бали; подовження й відповіді опитувань."}
