---
title: Aquarium (Акваріум)
slug: aquarium
aka: [Акваріум, Аквариум, puzzle-aquarium]
family: pencil-logic
also: [dig-gravity]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [paper, web, mobile]
links:
  - {kind: play, url: "https://puzz.link/rules.html?aquarium", best: true, note: "puzz.link: правила й плеєр з автоперевіркою (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/aquarium.js", note: "текст правил EN/JP, тест-дошки з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/aquarium.js", note: "реалізація: ввід, checklist, перевірка рівня по басейну / по області, прапорець aquarium_regions"}
  - {kind: official, url: "https://www.puzzle-aquarium.com/", note: "сайт жанру: 6×6/10×10/15×15 Easy–Hard, daily/weekly/monthly, Hall of Fame, «Auto flood water and air»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=aquarium+logic+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, dot-mark, line-sum-clue, gravity-fall, difficulty-levels, daily-puzzle, score-records, level-bank, in-game-editor, import-open-formats, undo-redo, rule-variants, +irregular-regions, +water-level-check, +auto-flood-fill, +clue-done-mark]
proposes: ["+cond:water_level", "+effect:flood_to_level", "+feature:auto-flood", "+card:water-level-check", "+card:auto-flood-fill"]
author: opus
date: 2026-11-09
---

# Aquarium — налий воду в резервуари так, щоб рівень у кожному був горизонтальним, а числа по краю зійшлися

## Суть
Сітка, вид збоку, розбита жирними лініями на «акваріуми». Гравець зафарбовує клітинки водою: числа зверху й збоку кажуть, скільки водяних клітинок у кожному стовпці й рядку. Вода підкоряється фізиці — під кожною водяною клітинкою або дно/межа, або вода, а в одному тілі води поверхня на одній висоті (навіть у U-подібних резервуарах). Ядро — **гравітація й сполучені посудини як статичне обмеження**: рішення в акваріумі одновимірне (висота рівня), а числа рядків/стовпців звʼязують акваріуми між собою.

## Поле і час
- Прямокутна сітка, вид збоку: верх і низ різні (вода тече вниз), ліво/право симетричні.
- Шари: межі акваріумів (дані) · підказки поза полем — над стовпцями й біля рядків (дані) · стан клітинки гравця: невідомо / вода / повітря (крапка).
- На puzzle-aquarium.com розміри 6×6, 10×10, 15×15, складність Easy / Normal / Hard.
- Час статичний; хід = зафарбувати клітинку (або на сайті — налити до рівня одним кліком).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | unknown / water / air (dot) | вода — зафарбована; крапка «повітря» лише нотатка, на перевірку не впливає |
| Акваріум | zone | клітинки між межами | резервуар; на сайті — одна висота води на всю ширину |
| Межа | static | ребро між клітинками | тримає воду знизу (дно) і з боків |
| Підказка стовпця / рядка | static | n ≤ висоти / ширини | скільки водяних клітинок у ряду; можна позначити «виконано» (сіріє) |
| Тіло води (басейн) | zone | звʼязна компонента води | одна поверхня: усі клітинки тіла не вище за верхню лінію, а порожніх під нею нема |
| Поверхня (рівень) | zone | висота | горизонтальна лінія; над нею в цьому тілі — повітря, під нею — вода |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `paint(cell, water)`; повтор → `unmark(cell)`.
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (повітря); `input(right_click×2, clue)` на підказці → `custom: «позначити підказку виконаною»` (тест-дошка puzz.link) (?).
- КОЛИ `input(click, cell)` → ЯКЩО `mode(auto_flood)` → ТО `custom: «залити воду до цього рівня по всьому акваріуму, вище — повітря»` (puzzle-aquarium.com, опція «Auto flood water and air»).
- КОЛИ `constraint_broken(support)` → ЯКЩО `not supported(water)` — під водяною клітинкою нема ні межі, ні води → ТО конфлікт `csNoSupport`.
- КОЛИ `constraint_broken(level)` → ЯКЩО `custom: «у тілі води є порожня клітинка на висоті рівня або нижче»` (`+cond:water_level`) → ТО конфлікт `csNoLevel` (дефолт puzz.link: рівень по звʼязному басейну).
- КОЛИ `constraint_broken(level)` → ЯКЩО `mode(regions)` and `custom: «в акваріумі порожня клітинка на висоті найвищої води або нижче»` → ТО конфлікт `bkNoLevel` (прапорець `aquarium_regions`, правило сайту puzzle-aquarium).
- КОЛИ `constraint_broken(count)` → ЯКЩО `custom: «води в рядку/стовпці ≠ підказці»` → ТО конфлікт `exShadeNe`.
- КОЛИ `constraint_broken(empty)` → ЯКЩО `count(water, ==, 0)` → ТО конфлікт `brNoShade` (порожнє поле не розвʼязок).
- КОЛИ `all_constraints_met` → ТО `win`, `timer(stop)` (сайт: Done → Hall of Fame).
- Дедукція «рівень = одне число на акваріум»: розвʼязок акваріуму — вибір висоти; підказка рядка рахує ширини акваріумів, залитих до цього рядка.
- Дедукція «U-подібний»: дві гілки, сполучені внизу, мають однаковий рівень — заливаються разом.
- Дедукція «∩-подібний» (дві ноги без зʼєднання водою): у дефолті puzz.link ноги — різні басейни з різними рівнями, у режимі областей — один рівень (?).
- Перемога: числа рядків і стовпців збігаються, вода має опору, рівні горизонтальні. Поразки й рахунку нема (на сайті — час у рейтингу).

## Керування і ввід
- puzz.link: ліва кнопка — вода, права — крапка-повітря, drag — той самий стан по ряду; клік по підказці поза полем — «виконано».
- puzzle-aquarium.com: клік по клітинці, опція «Auto flood water and air» (один клік ставить рівень), Start Over, Done, New Puzzle.
- Редактор puzz.link: drag — межі акваріумів, клік по позаполевій клітинці + цифра — підказка.

## Вікна, меню, HUD
- `game-screen`: сітка з жирними межами, числа над стовпцями й ліворуч від рядків, синя вода, `conflict-highlight`, `+ui:clue-greyed` для виконаних підказок.
- puzzle-aquarium.com: панель Done · Start Over · Print · Share · New Puzzle; `timer-elapsed` (можна сховати / «особистий»); `settings-window` з перемикачами: Hide game controls, Sticky toolbar, Auto submit, Show checkpoints, Show board coordinates, Auto flood water and air, Highlight last change, Show counters, Count remaining, Night mode, Thicker block borders.
- `mode-select` / `difficulty-select`: розмір × складність, Daily / Weekly / Monthly.
- `leaderboard` — Hall of Fame.
- puzz.link: як у [puzz-link](puzz-link.md) (Check, Undo/Redo, Trial, URL).
- Переходи: вибір розміру → game-screen → Done → результат / Hall of Fame.

## Фічі поза полем
- `difficulty-presets` (6×6…15×15 × Easy/Normal/Hard), `mode-daily` + weekly/monthly, `leaderboard-online` (Hall of Fame).
- `+feature:auto-flood` — допомога вводу: рівень одним кліком.
- `auto-check`: puzz.link за кнопкою з кодом помилки; сайт — опція «Highlight errors», «Auto submit».
- `share-code`: сайт — «Progress Permalink» і «Progress Screenshot»; puzz.link — URL пазла.
- Сайт: друк (Print), нічний режим, координати, лічильники «скільки лишилось».
- Мобільні застосунки PuzzleGym (App Store, Google Play).

## Варіації й родичі
- Правило рівня: по звʼязному тілу води (puzz.link дефолт) / по всьому акваріуму (puzzle-aquarium.com, прапорець `aquarium_regions`).
- Родичі «статична гравітація»: [Dosun-Fuwari](dosun-fuwari.md) (ядра падають, кульки спливають), [Sto-Stone](sto-stone.md) (блоки падають у пазлі); з аркад — `dig-gravity`, рідини в falling sand.
- Числа поза полем як у [Nonogram](nonogram.md) і Tents, але тут лише кількість, без серій.
- **Осі варіацій**: де рівень однаковий (тіло води / резервуар) · що тримає воду (дно і межі / ще й чорні клітинки (?)) · підказки (рядки+стовпці / лише частина / в акваріумі).

## Цікавинки для курсу
- Перевірка опори: під водою межа або вода — 🌱.
- Рівень у звʼязному тілі води: BFS по воді, знайти найвищий рядок, перевірити, що всі клітинки резервуару, досяжні з тіла, нижче рівня залиті — 📎.
- «Налити до рівня» одним кліком: заливка резервуару з урахуванням сполучених посудин (U-форма) — 🥉.
- Розвʼязувач: кожен акваріум = вибір висоти; числа рядків/стовпців = лінійні обмеження → перебір з відсіканням — 🥉.
- Генератор: випадкові області + випадкові рівні → підказки → перевірка єдиності — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` · `cell-click`, `dot-mark` · `line-sum-clue` ↔ кількість води в ряду · `gravity-fall` ↔ вода мусить «впасти» на опору · `difficulty-levels`, `daily-puzzle`, `score-records` (Hall of Fame), `level-bank` · `in-game-editor`, `import-open-formats` (puzz.link) · `undo-redo` · `rule-variants` ↔ `aquarium_regions`.
- Перевикористано: `+irregular-regions`, `+clue-done-mark` (з інших файлів сімʼї).
- **Нема** → пропозиції карток:
  - `+water-level-check` «Сполучені посудини: один рівень у тілі рідини» · game-logic/constraints · 📎 · слот {scope: pool|region}.
  - `+auto-flood-fill` «Налити до рівня одним кліком» · interface/input · 🥉.

## Пропозиції до словників
- `+cond:water_level` — у тілі рідини/резервуарі нема порожньої клітинки на рівні поверхні або нижче.
- `+effect:flood_to_level` — залити область до висоти, вище — позначити повітрям.
- `+feature:auto-flood` — допоміжна заливка рівнем.
- `+card:water-level-check`, `+card:auto-flood-fill` — див. мапу.

## Джерела
- ⭐ [puzz.link: Aquarium](https://puzz.link/rules.html?aquarium) — плеєр і правила (рендериться JS; текст узяв з pzpr-samples).
- [pzpr-samples/aquarium.js](https://puzz.link/js/pzpr-samples/aquarium.js) — правила EN/JP: вид збоку, числа = кількість води в ряду, опора знизу, одна поверхня «(including in U-shaped areas)»; коди `brNoShade`, `csNoSupport`, `exShadeNe`, `csNoLevel`, `bkNoLevel`.
- [src/variety/aquarium.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/aquarium.js) — ввід (shade / unshade / completion), підказки в `excell`, checklist, перевірка по басейну й по області.
- [puzzle-aquarium.com](https://www.puzzle-aquarium.com/) — правила сайту, розміри й складність, daily/weekly/monthly, налаштування, Hall of Fame, PuzzleGym.
- YouTube: пошук «aquarium logic puzzle».

## Непевне
- (?) Автор і рік жанру — не знайшов.
- (?) Чи `checkSupports` вимагає опору лише знизу, чи також збоку (переказ коду від WebFetch згадав «left, right, or below»; текст правил — лише «below»).
- (?) Поведінка ∩-подібного акваріуму в обох режимах — виведено з правил, на прикладі не перевіряв.
- (?) Яка дія кнопок миші в puzz.link (ліва — вода, права — крапка) — з тест-послідовностей `mouse,left` / `mouse,right`, не з тексту.
- (?) `random: setup` — для сайту (генеровані пазли); на puzz.link пазли авторські.
