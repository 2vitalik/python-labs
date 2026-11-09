---
title: Arofuro (アローフロー, Arrow Flow)
slug: arofuro
aka: [アローフロー, Arrow Flow, Arrowflow, Pfeilfluss, Потік стрілок]
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
year: 2008
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Arofuro/index.htm", best: true, note: "Janko: правила DE/EN/JP, Naoki Inaba 2008, приклад з розвʼязком, галерея, розміри 6×6–8×8"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Naoki/Arofuro.htm", note: "розділ Inaba у Janko: アローフロー, дата 2008-07-06, 4 пазли, споріднений Roma"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Arofuro/001.a.htm", note: "applet Janko, пазл 6×6; у даних — e/w/n/s, x, числа"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Arofuro/Bedienung.htm", note: "керування: меню стрілок, ? «будь-яка стрілка», ✕, протягування-копіювання, клавіші як на numpad"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/roma.js", note: "pzprjs: arrowflow ділить код із Roma — ввід, перевірки, «дорога» до цілі"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/test/script/arrowflow.js", note: "тест pzprjs: коди nmAdjacent, arCountLt, arCountGt, stopHalfway"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=arrow+flow+arofuro+puzzle", note: "пошук"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, conflict-highlight, path-preview, level-bank, level-rating, puzzle-select, help-window, in-game-editor, seed-share, save-game, undo-redo, replay, +no-adjacent-check, +arrow-flow-count, +aux-direction-marks, +drag-copy-value, +hint-reveal, +cell-coloring]
proposes: ["+cond:flows_to(cell, kind)", "+cond:upstream_count(cell, n)", "+card:arrow-flow-count", "+card:aux-direction-marks", "+card:drag-copy-value", "+ui:solved-frame", "+ui:value-popup-menu", "+window:puzzle-info"]
author: opus
date: 2026-11-09
---

# Arofuro (Arrow Flow) — постав у кожну білу клітинку стрілку; число каже, скільки стрілок зрештою стікається в нього

## Суть
На сітці — числа в кружечках, чорні клітинки й білі клітинки. У кожну білу клітинку гравець ставить стрілку в один із 4 напрямків; стрілка показує на сусідню клітинку, і, йдучи за стрілками, з будь-якої білої клітинки треба потрапити в якесь число. Число дорівнює кількості всіх стрілок, що ведуть у нього прямо або ланцюжком; дві однаково спрямовані стрілки не можуть бути ортогональними сусідами. Незвичне: поле стає **лісом потоків** — кожне число є коренем дерева, а підказка задає розмір цього дерева.

## Поле і час
- Прямокутна сітка; у Janko — 6×6, 7×7, 8×8; приклад правил і пазл №1 — 6×6.
- Клітинки: число в кружечку (ціль) · чорна (поза грою) · біла (отримує стрілку).
- Стрілка показує на сусідню клітинку в своєму напрямку (на прикладі ланцюг ↓ → ↓ ← приводить у ⑤).
- Шари: числа й чорні (незмінні) · стрілки гравця · допоміжні позначки напрямків, ✕, «?».
- Час статичний; хід = поставити / змінити / стерти стрілку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Число (ціль) | sink | n у кружечку; у puzz.link буває «?» | n = кількість стрілок, чий ланцюг закінчується тут |
| Чорна клітинка | static | — | без стрілки; ланцюг у неї не може зайти |
| Стрілка | conduit | N / S / E / W | показує на сусіда; разом утворюють ланцюги |
| Басейн числа | zone | клітинки, що стікають у число | розмір = число; дерево без циклів |
| Позначка «?» | mark | «тут якась стрілка» (Janko) | лише для гравця |
| Допоміжна позначка напрямку | mark | біт на кожен із 4 напрямків (puzz.link) | лише для гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cell, dir)` → ТО `set_value(cell, arrow(dir))` (puzz.link, play).
- КОЛИ `input(key_1|2|3|4 або shift+arrow, cell)` → ТО `set_value(cell, ↑|→|↓|←)`; `6` або пробіл → `unmark(cell)`; `ctrl+arrow` → `mark(cell, aux dir)` — перемикач біта (puzz.link, roma.js).
- КОЛИ `input(left_click, cell)` → ТО `window(+value-popup-menu)` → стрілка / ? / ✕ / порожньо (Janko).
- КОЛИ `input(left_drag, cells)` або `shift+arrow` → ТО `custom: «скопіювати значення в клітинки по дорозі»` (Janko).
- КОЛИ `input(key_8|2|4|6 або w|x|a|d, cell)` → ТО `set_value(cell, ↑|↓|←|→)` — розкладка numpad; `,` → ✕; `.`, `?`, `o` → «?»; `–`, `/`, ⌫, Entf — стерти (Janko).
- Сусіди: КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(same_direction_arrows)` → ТО конфлікт «Equal arrows are adjacent» (nmAdjacent).
- Мало: КОЛИ `constraint_broken(count)` → ЯКЩО `custom: «у басейні менше стрілок, ніж число»` (`+cond:upstream_count`) → ТО «A number does not have enough arrows pointing towards it» (arCountLt).
- Забагато: КОЛИ `constraint_broken(count)` → ЯКЩО `custom: «у басейні більше стрілок, ніж число»` (`+cond:upstream_count`) → ТО «A number has too many arrows pointing towards it» (arCountGt).
- Кінець ланцюга: КОЛИ `constraint_broken(flow)` → ЯКЩО `not custom: «ланцюг від клітинки закінчується в числі»` (`+cond:flows_to`) → ТО «A cell cannot reach a goal» (stopHalfway) — ланцюг пішов у чорну, за край або в цикл.
- КОЛИ `input(click, cell)` у режимі info-road → ТО `custom: «підсвітити "дорогу" ланцюга»` (puzz.link, dispRoad).
- КОЛИ `all_constraints_met` → ТО `win` (Janko — `custom: «зелена рамка»`).
- Janko: F6 — помилки червоним; F3 — режим підказки; F4 — розвʼязок з логічним шляхом; Ctrl+Z / Pos1 → `undo(1)` / `undo(all)`.
- Дедукція «сума»: кожна біла клітинка стікає рівно в одне число, тож сума всіх чисел = кількість білих клітинок (наслідок правил; приклад: 1+2+4+6+3+5+5 = 26 = 36 − 3 чорні − 7 чисел).
- Дедукція «сходинки»: сусідні в ланцюгу стрілки — ортогональні сусіди, тож не однакові й не протилежні (інакше цикл); ланцюг повертає на 90° на кожному кроці (наслідок правил; приклад ↓ → ↓ ←).
- Дедукція «без циклів»: цикл не досягає числа, тож басейн — дерево з коренем у числі (наслідок правил).
- Дедукція «одиниця»: у число 1 входить рівно одна стрілка, і в неї саму не входить жодна (наслідок правил).
- Перемога: стрілка в кожній білій, однакові не поруч, усі ланцюги в числах, розміри басейнів = числа · Поразка: — · Рахунок: —.

## Керування і ввід
- puzz.link, play: протягування з клітинки задає стрілку; режими вводу play — diraux, arrow, clear, info-road; edit — number, clear, empty (чорна), info-road.
- puzz.link, клавіатура: 1–4 або Shift+стрілки — стрілка; 6 / пробіл — стерти; Ctrl+стрілки — допоміжні позначки напрямку.
- Janko applet: лівий клік / тап — меню (стрілки, ?, ✕, порожньо); правий клік / утримання — позначки й кольори; протягування — копіювання; Enter / Space / Ins — гортати ✕ → стрілки → ? → порожньо.
- Папір: PDF на сайті Naoki Inaba (за посиланням Janko).

## Вікна, меню, HUD
- `game-screen`: сітка, кружечки з числами, чорні клітинки, стрілки, `conflict-highlight` (Janko F6, перевірка puzz.link), `path-preview` ↔ режим «дорога» puzz.link, `+ui:solved-frame`, `+ui:value-popup-menu` (Janko).
- puzz.link: перемикач play / edit і панель режимів вводу.
- `puzzle-select` — Janko: індекс за датою / розміром / складністю + розділ Naoki (4 пазли).
- `help-window` — правила DE/EN/JP, Bedienungsanleitung, галерея прикладів.
- `+window:puzzle-info` (F1, Janko).

## Фічі поза полем
- `auto-check` (Janko F6, puzz.link), автовизнання розвʼязку.
- `undo` / `redo`; збереження стану Ctrl+S / Ctrl+L (Janko).
- `hint` (F3), `show-solution` (F4) з логічним шляхом (Janko).
- `puzzle-bank` Janko — рейтинг 1–8 лише за часом; пазли з відтворюваним шляхом — кольором.
- `level-editor` + `share-code` — puzz.link (зразок URL-даних `4/4/1g0.j5h0i2`); у редакторі число 0 = чорна клітинка.

## Варіації й родичі
- Автор — Naoki Inaba, 6 липня 2008, сайт «Puzzle Laboratorium»; Janko знає лише назви Arrow Flow / Pfeilfluss.
- **Roma** (ろーま) — споріднений жанр: puzz.link реалізує обидва в одному модулі; у Roma стрілки в кімнатах без повторів і всі ведуть до цілі (коди «An area has duplicate arrows», «A cell cannot reach a goal»).
- Cross+A (Ілля Морозов, Сергій Кутасов) підтримує жанр (за Janko).
- Родичі в корпусі: [Guide Arrow](guide-arrow.md) (стрілки й дерево білих до зірки), [Signpost](signpost.md) (стрілка в кожній клітинці), [Nurikabe](nurikabe.md) і [Fillomino](fillomino.md) (розмір області = число), [Zeiger](zeiger.md) (стрілки з підрахунком).
- **Осі варіацій**: що рахує число (увесь басейн / лише прямих сусідів) · заборона (однакові поруч / повтор у кімнаті) · напрямки (4 / 8) · ціль (число / коло без числа).

## Цікавинки для курсу
- Перевірка: з кожної білої клітинки йти за стрілками з детекцією циклу (кольори відвідування) — 📎.
- Обернений граф стрілок і BFS від числа = розмір басейну — 📎.
- Підсвітка «дороги» ланцюга за кліком — 🌱.
- Розвʼязувач: 4 значення на клітинку + заборона однакових сусідів + «сходинки» + розміри дерев + backtracking — 🥇.
- Генератор: випадковий ліс «сходинкових» дерев навколо цілей → числа = розміри → перевірка єдиності — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `conflict-highlight` · `path-preview` ↔ «дорога» ланцюга · `level-bank`, `level-rating`, `puzzle-select`, `help-window` · `in-game-editor`, `seed-share` ↔ URL puzz.link · `save-game`, `undo-redo`, `replay` ↔ логічний шлях F4.
- Перевикористано: `+no-adjacent-check` (слот: однаковий напрямок), `+hint-reveal`, `+cell-coloring`.
- **Нема** → пропозиції карток:
  - `+arrow-flow-count` «Число = розмір басейну стрілок, що стікаються в клітинку» · game-logic/constraints · 📎 · слот {dirs: 4|8, step: adjacent|ray}.
  - `+aux-direction-marks` «Допоміжні позначки напрямків у клітинці (біт на напрямок)» · interface/input · 🌱 — puzz.link.
  - `+drag-copy-value` «Протягування копіює значення в клітинки по дорозі» · interface/input · 🌱 — Janko.

## Пропозиції до словників
- `+cond:flows_to(cell, kind)` — ланцюг стрілок від клітинки закінчується в сутності виду.
- `+cond:upstream_count(cell, n)` — кількість клітинок, чиї ланцюги закінчуються тут, = n.
- `+card:arrow-flow-count`, `+card:aux-direction-marks`, `+card:drag-copy-value` — див. мапу.
- `+ui:solved-frame`, `+ui:value-popup-menu`, `+window:puzzle-info` — повтори Janko-applet-а.

## Джерела
- ⭐ [Janko: Arofuro](https://www.janko.at/Raetsel/Arofuro/index.htm) — правила DE/EN/JP (JP: кожен ланцюг закінчується в числі), Inaba 2008, розміри, рейтинг, посилання на Cross+A.
- [Janko: Naoki Inaba — Arofuro](https://www.janko.at/Raetsel/Naoki/Arofuro.htm) — アローフロー, 2008-07-06, 4 пазли, Roma.
- [Janko: Arofuro №1](https://www.janko.at/Raetsel/Arofuro/001.a.htm) — дані applet-а (Otto Janko, 6×6).
- [Janko: Bedienung](https://www.janko.at/Raetsel/Arofuro/Bedienung.htm) — меню, копіювання, розкладка клавіш.
- [pzprjs: roma.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/roma.js) — режими вводу, клавіші, перевірки checkAdjacentDiffNumber / checkGoalGt / checkGoalLt / checkBalls.
- [pzprjs test: arrowflow.js](https://raw.githubusercontent.com/robx/pzprjs/master/test/script/arrowflow.js) — коди помилок; тексти — у pzprjs failcode.en.json.
- YouTube: пошук «arrow flow arofuro puzzle».

## Непевне
- (?) Скільки пазлів у Janko: таблиці індексу за розмірами порожні; бачив №1 (Otto Janko) і 4 пазли Inaba у розділі Naoki.
- (?) Режим info-road puzz.link: що саме підсвічує (ланцюг від клітинки чи басейн числа) — з коду, на сторінці не перевіряв.
- (?) Ціль «?» без числа (puzz.link `qnum = -2`) — бачив лише в коді; чи бувають такі в опублікованих пазлах, не знаю.
- (?) Сайт Inaba (inabapuzzle.com) не відкрився (помилка сертифіката) — оригінальні правила й PDF не бачив.
