# T357 · Сайт ods цілком — звіт

`2026-11-19` · ⚙️ задача · контракт — [plan.md](plan.md)

## Стан (оновлюється на кожній чистій точці)

`2026-11-19`, перша хвиля в роботі — нічого з коду ще не закомічено.

| Що | Хто | Де результат | Стан |
|:--|:--|:--|:--|
| Пари 02.10, 16.10, 30.10: транскрипт, конспект, звіт | Opus × 3 | `sites/ods/transcripts/<дата>/` (поза git) | зводяться; чернетки днів уже є на стенді (`bin/lesson -t t357 collect`) |
| Сторінки лаб і розмітка | Opus «лаби» | `sites/ods/vue/src/{pages/Lab*Page, pages/OldLabsPage, components/LabNav}.vue`, `rich.js`, `rich.css`, `richMd.js`; нотатка `.dev/.drafts/T357/labs.md` | пишеться |
| Сторінки лекцій і пошук | Opus «лекції» | `pages/{LecturesPage, LecturePage}.vue`, `lectures.js`, `components/LectureFind.vue`; нотатка `.dev/.drafts/T357/lectures.md` | пишеться |
| Імпорт через API, `GUIDE_STAFF`, `POST /api/me/as` | Opus «імпорт» | `sites/ods/api/{routes/content.py, content_disk.py, tests/smoke_content.py}`, `bin/content`, ядро; готові до перенесення `main.py`, `db.py`, `site.env`, `routes/media.py`, `content_io.py` — у скретчі `…/scratchpad/backend/handover/`; нотатка `.dev/.drafts/T357/backend.md` | пишеться |
| Око «Очима студента» в меню | Opus «око» | `core/ui/{api.js, user.js, components/NavUser.vue}`; нотатка `.dev/.drafts/T357/eye.md` | пишеться |

## Що далі (порядок для того, хто продовжує)

1. Дочекатись рядка від сесії T354 з хешем її коміту (вона комітить `LabPartPage`, `LabParts`, `LabFiles`, `labPages.js`, `routes/lab_pages.py`, `models/lab_page.py`, `content_io.py`); до того її файли, `main.py` і `db.py` не чіпати.
2. Інтеграція (після п. 1): перенести `handover/` бекенда; у `router.js` — маршрути з нотаток `labs.md` і `lectures.md` (`LabsPage`, `LabPage`, `OldLabsPage` з `access: 'admin'`, `LecturesPage`, `LecturePage`); у `main.js` — `useMd(richMd)`; прибрати з маршрутів `DocPage`, `DocsPage`, `LabPartPage`, `LabParts` (стануть зайвими — видалити разом з імпортами).
3. Стенд: `bash .dev/.drafts/T357/stand/tree.sh` (копія `HEAD` + файли з `mine.txt`) → `up.sh` → імпорт контенту в базу стенда (`ODS_DATA` — справжня тека даних, лише локально) → перевірка сторінок у headless Chrome (`cdp.mjs`): `/labs`, `/labs/3`, `/labs/3/case1`, `/labs/about/start`, `/labs/old`, `/lectures`, `/lectures/7`, `/lessons`, око в меню — адміном і тестовим студентом, світла й темна теми, телефон.
4. Пари: `LESSONS_DIR=sites/ods/transcripts LESSONS_COURSE=ods ~/.venvs/python-labs/bin/python bin/lesson -t t357 push <дата>` на стенд → погляд → те саме в дев-базу `ods` (ціль для неї ще треба завести: `AGENT_TOKENS` у `.env` сайту — рішення Vitalik-а) → публікація лише за його словом.
5. Смоуки ods і ядра, збірка фронту; коміти по одному на рішення; README вузла, CHANGELOG, STATUS, Q-тікет із виборами, C-тікет «чого бракує сайту», сторінка-звіт.

## Домовленості із сусідами

- T354 («Формочка для завантаження лабораторних ОДС»): її — «Моя лаба», «Результати», перевірка, ноутбук, `labs_*.py`, `routes/labs.py`, `lab_io.py`, `labCols.js`, `bin/nbrun`; спільні `router.js`, `api.js`, `site.js`, `main.py`, `db.py` — точково.
- T355 («Третя лабораторна: перевірка і сайт»): тексти й `pages.json` у `sites/ods/data/labs/site/`; розмітка — plan.md §4; порядок сторінок лаби — за `order`.
- Ліміт Fable (слово Vitalik-а 2026-11-19, лишилось 8 %): усе, що можна, — субагентам Opus; обом сесіям передано.
