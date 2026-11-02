---
title: Kuromasu (Kurodoko, Range) + Cave (Bag)
slug: kuromasu
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1991
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kuromasu", best: true, note: "правила, Nikoli №34 (червень 1991), назви, техніки, NP-повнота (Kölker 2012)"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/kurodoko/", note: "Nikoli: правила Kurodoko, Sample → Progressing → Solution"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/range.html", note: "Tatham Range: правила, миша/клавіатура, Shift+стрілки, преференс кнопок"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html", note: "Range у браузері (WebAssembly)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kurodoko.js", note: "puzz.link: правила Kurodoko, 4 коди помилок"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/cave.js", note: "puzz.link: правила Cave (Bag), коди cuDivide / csConnOut / nmSumViewNe"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/Kurodoko", note: "WPC-вікі: автор Tea.M., варіант Open Space"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/Cave", note: "WPC-вікі: Cave, автор Gesaku, Full Cave, Twilight Cave"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kurodoko+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, reachability-check, level-solver, unique-puzzle-generation, field-size-picker, game-settings, level-bank, import-open-formats, in-game-editor, +undo-redo, +seed-share, +solve-into-undo, +cell-shade-toggle, +dot-mark, +input-scheme-toggle, +no-adjacent-check, +global-connectivity, +ray-cast-light, +visibility-count-clue, +edge-connectivity]
proposes: ["+cond:view_count", "+cond:connected_to_edge", "+card:visibility-count-clue", "+card:edge-connectivity", "+card:drag-dot-trail"]
author: opus
date: 2026-11-02
---

# Kuromasu — число каже, скільки білих клітинок видно з нього в чотири боки

## Суть
Гравець зафарбовує клітинки так, щоб чорні не торкалися сторонами, а білі лишились однією звʼязною областю. Числа — білі клітинки-«очі»: число = скільки білих клітинок видно з неї по рядку й стовпцю (включно з собою), доки погляд не впреться в чорну клітинку або край поля. **Cave** (Bag) — сестринський жанр з тією самою підказкою видимості: біла «печера» звʼязна, а кожна чорна мусить зʼєднуватись із краєм поля (чорні не торкаються — правила нема). Незвичне: **підказка-видимість** — сімейство, де число міряє промені до перешкоди (Light Up освітлює, Skyscrapers рахує видимі вежі ззовні, тут рахуються білі клітинки зсередини).

## Поле і час
- Прямокутна сітка; клітинки: число (завжди біле) · порожня.
- Промені — 4 ортогональні напрямки від числа; зупиняються на чорній або на краю. Сусідство ортогональне для заборони дотику чорних і звʼязності білих.
- Cave: «зовні поля» — віртуальна чорна рамка; кожна чорна група торкається краю; білі утворюють одну область без «дірок».
- Шари: числа (незмінні) · стан клітинки: невідомо / зафарбовано / крапка.
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Число | static | N | не фарбується; видимих білих у 4 променях + 1 (сама) = N |
| Промінь видимості | zone | напрям, довжина | клітинки від числа до першої чорної / краю |
| Клітинка | mark | стан unknown / shaded / dot | клік змінює стан |
| Зафарбована (Kuromasu) | mark | — | не сусідить сторонами з іншою чорною; обриває промені |
| Зафарбована (Cave) | mark | — | обриває промені; її група торкається краю поля |
| Крапка | mark | — | позначка гравця «не чорна» |
| Біла область / печера | zone | кількість компонент | усі білі — одна 4-звʼязна компонента |
| Край поля (Cave) | static | — | «якір» для чорних груп |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; ліва повторно → `mark(cell, dot)` → `unmark(cell)` (Tatham: кнопки циклюють filled → dotted → empty у протилежних напрямках).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)`; права повторно → `mark(cell, shaded)` → `unmark(cell)`.
- КОЛИ `input(shift+arrow)` → ТО `move(cursor, dir)`, `mark(passed_cell, dot)` (Tatham: крапки на кожній пройденій клітинці).
- КОЛИ `constraint_broken(view_count)` — ЯКЩО `not view_count(clue) == N` → ТО число підсвічене (puzz.link `nmSumViewNe`, спільний з Cave).
- КОЛИ `constraint_broken(no_adjacent_shaded)` — ЯКЩО `adjacent_count(shaded, shaded, >, 0)` → ТО конфлікт (`csAdjacent`; лише Kuromasu).
- КОЛИ `constraint_broken(white_connected)` — ЯКЩО `not connected(white)` → ТО конфлікт (`cuDivideRB` у Kuromasu, `cuDivide` у Cave).
- КОЛИ `constraint_broken(shaded_to_edge)` — ЯКЩО `not connected_to_edge(shaded_group)` → ТО конфлікт (`csConnOut`; лише Cave).
- КОЛИ `constraint_broken(board_not_empty)` — нічого не зафарбовано → ТО конфлікт (`brNoShade`).
- КОЛИ `all_constraints_met` → ТО `win`, `flash` (Tatham).
- Обчислення `view_count`: від числа йти в кожен з 4 напрямків, доки клітинка біла (у ході гри: не чорна) і в межах поля; сума довжин + 1.
- Дедукції (Wikipedia): число = максимум, який воно може побачити, → усі клітинки рядка й стовпця до перешкод білі (крапки); «2» поруч з іншим числом → решта його сусідів і клітинка за сусіднім числом чорні; дві білі з однією клітинкою між ними, і задіяна «2» → середня чорна; верхня межа (видно до наявних чорних) і нижня межа (видно гарантовано білих) звужуються з двох боків.
- Cave-дедукції: чорна в куті «печери» мусить мати шлях до краю; біла, оточена чорними з трьох боків біля краю, — тупик печери.
- Перемога (Kuromasu): усі числа виконані, чорні не торкаються, білі звʼязні. Перемога (Cave): числа виконані, білі звʼязні, усі чорні зʼєднані з краєм. Поразки й рахунку нема.

## Керування і ввід
- Tatham Range: ліва — чорна, права — крапка, повтор циклює стани в протилежних напрямках; стрілки — курсор; Return = ліва; Space = права; Shift+стрілки — крапки по шляху.
- Tatham Preferences: перепризначити, яка кнопка миші що робить (`+input-scheme-toggle`).
- Спільні дії Tatham: N — нова гра, U/Ctrl+Z — undo, R/Ctrl+R — redo, Solve, Restart.
- puzz.link: ліва — фарба, права — крапка, drag протягує (?); edit mode — числа з клавіатури, у Cave — і «-» (?) (тести `cave.js` вводять тире й числа).

## Вікна, меню, HUD
- `game-screen`: сітка з числами + `conflict-highlight` (число з невірною видимістю, сусідні чорні, розрізана біла область) + `cursor` (клавіатура).
- Tatham: меню Game (New, Restart, Undo, Redo, Solve, Enter game ID, Enter random seed, Download/Upload save file, Preferences) · меню Type (пресети розміру + Custom…).
- `custom-window` → `+window:params-dialog`: Width, Height (Tatham Custom…).
- `+window:game-id-dialog`: ввести/показати ID чи seed.
- `settings-window` (Preferences): призначення кнопок миші.
- `help-window`: Full instructions (Tatham), правила Nikoli.
- puzz.link: Check, Undo, Redo, Clear answer; `editor-window` — edit mode.
- Переходи: Type → params-dialog → генерація → game-screen; розвʼязано → спалах → New game.

## Фічі поза полем
- `auto-check` (Tatham — миттєве підсвічування; puzz.link — за кнопкою з кодом).
- `undo` ∞ і `redo`; Solve в історії undo (Tatham).
- `seed-input` / `share-code` (game ID, seed), `save-slots` через файл.
- `custom-difficulty`: розмір поля; генератор з унікальним розвʼязком (Jonas Kölker для Tatham).
- `level-editor` + `share-code` (puzz.link URL / pzprv3).
- `puzzle-bank` / `daily-puzzle`: щоденна версія на Kurodoko.com, вебгра 0hn0.com (згадані у Wikipedia).

## Варіації й родичі
- **Cave / Bag** (Nikoli, «Gesaku», 1996): без заборони дотику чорних, але чорні тримаються за край; Nikoli вважає його петельним жанром (межа печери — петля).
- **Full Cave** (Matej Uher, WPC 2016) — біла звʼязна фігура, решта чорна, числа бачать до чорних; чи лишається умова «чорні до краю» — не ясно (?); **Twilight Cave** (Gabi Penn-Karras, WPC 2019) — число в чорній = розмір її чорної групи.
- **Open Space** (WPC 2015) — Kurodoko, де чорні не торкаються й діагонально.
- **0h n0** — мобільна гра на ту саму підказку видимості (сині/червоні крапки) з власними правилами (?).
- Сімейство «підказка-видимість»: **Light Up** (лампа освітлює промені до стіни; число на стіні — сусідні лампи) · **Skyscrapers** (число ззовні = скільки веж видно, вища ховає нижчі) · **Kuromasu** (число всередині = скільки білих видно до чорної) · **Cave** (те саме + інша глобальна умова).
- Родичі за глобальними умовами: Hitori, Heyawake, Yajilin (чорні не торкаються + білі звʼязні).
- **Осі варіацій**: звідки дивимось (зсередини / ззовні поля) · що зупиняє погляд (чорна / стіна / вища вежа) · що рахуємо (клітинки / вежі / освітлення) · глобальна умова чорних (не торкаються / тримаються за край / нема).

## Цікавинки для курсу
- Підрахунок видимості 4 променями до перешкоди — 🌱 (`+ray-cast-light`, слот dirs: 4).
- Заборона сусідства чорних + звʼязність білих — 🌱 + 📎 (той самий модуль, що в Hitori/Heyawake).
- Cave: «кожна чорна група торкається краю» — 📎 (flood fill від рамки або віртуальна вершина «зовні»).
- Інтервальна дедукція: для кожного числа мінімум/максимум видимості в кожному напрямку — 🥉, класична техніка розвʼязувача.
- Схема кнопок, що циклюють стани в протилежних напрямках, + Shift-стрілки для серії крапок — 📎.
- Розвʼязувач (інтервали + точки розрізу білих) — 🥇; генератор з унікальним розвʼязком (Kölker 2012: NP-повнота) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` ↔ Tatham · `reachability-check` ↔ звʼязність білих, чорні до краю · `level-solver`, `unique-puzzle-generation` · `field-size-picker`, `game-settings` ↔ Custom… / Preferences · `level-bank` · `import-open-formats` · `in-game-editor`.
- Перевикористано: `+undo-redo`, `+seed-share`, `+solve-into-undo`, `+cell-shade-toggle`, `+dot-mark`, `+input-scheme-toggle` (Hitori), `+no-adjacent-check`, `+global-connectivity` (Tatham Range), `+ray-cast-light` (Light Up).
- **Нема** → пропозиції карток:
  - `+visibility-count-clue` «Число = скільки клітинок видно до перешкоди» · game-logic/constraints · 🌱 · слот {from: inside|outside, stop: shaded|wall|taller, counts: cells|towers}.
  - `+edge-connectivity` «Кожна група стану зʼєднана з краєм поля» · game-logic/constraints · 📎 — Cave; родич `+global-connectivity` з віртуальною вершиною «зовні».
  - `+drag-dot-trail` «Модифікатор + стрілки ставить мітки на шляху курсора» · interface/input · 🌱 — Tatham Range.

## Пропозиції до словників
- `+cond:view_count` — кількість клітинок, видимих з клітинки в 4 напрямках до перешкоди (включно з собою).
- `+cond:connected_to_edge` — група клітинок має шлях до краю поля.
- `+card:visibility-count-clue`, `+card:edge-connectivity`, `+card:drag-dot-trail` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Kuromasu](https://en.wikipedia.org/wiki/Kuromasu) — правила, №34 (червень 1991), назви (Kurodoko, «Where is Black Cells»), техніки, NP-повнота.
- [Nikoli: Kurodoko](https://www.nikoli.co.jp/en/puzzles/kurodoko/) — офіційні правила, приклад.
- [Tatham: Range](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/range.html) — правила, керування, параметри, Preferences; автор порту Jonas Kölker.
- [Range у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/range.html) — меню Game/Type, New/Restart/Undo/Redo/Solve.
- [puzz.link kurodoko.js](https://puzz.link/js/pzpr-samples/kurodoko.js) — правила, vol. 34, коди `brNoShade`, `csAdjacent`, `cuDivideRB`, `nmSumViewNe`.
- [puzz.link cave.js](https://puzz.link/js/pzpr-samples/cave.js) — правила Cave, історія «Bag», коди `cuDivide`, `csConnOut`, `nmSumViewNe`, тести вводу.
- [WPC unofficial wiki: Kurodoko](https://wpcunofficial.miraheze.org/wiki/Kurodoko) — автор Tea.M., Open Space, 8 появ на WPC.
- [WPC unofficial wiki: Cave](https://wpcunofficial.miraheze.org/wiki/Cave) — автор Gesaku, Full Cave, Twilight Cave, раунди WPC.
- YouTube: пошук «kurodoko puzzle how to solve».

## Непевне
- (?) Перша публікація Cave: puzz.link — vol. 58 («Bag»), WPC-вікі — vol. 60 (1996).
- (?) Назву «Corral» для Cave/Bag у джерелах не бачив (WebSearch вичерпано) — у шапці не вжито.
- (?) Правила Full Cave — переказ WPC-вікі, деталі не перевірені.
- (?) Правила 0h n0 і зміст Kurodoko.com — лише згадка у Wikipedia, сайти не відкривав.
- (?) Дії мишею в puzz.link — тестів play-вводу нема.
