---
title: "Minesweeper у вимірах: 4D Minesweeper, Tilesweeper, Timesweeper"
slug: minesweeper-dimensions
aka: [4D Minesweeper, Tilesweeper, Timesweeper]
family: hidden-deduction
also: [pencil-logic]
klass: cursor
axes:
  field: graph
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2018
platforms: [PC (Steam), macOS, Linux, web (itch.io)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/787980/", best: true, note: "4D Minesweeper: до 80 сусідів, підсвітка сусідів, delta-режим, сферичні виміри (труби, тори), 1D–4D, 80+ пазлів без вгадування"}
  - {kind: steam, url: "https://store.steampowered.com/app/867180/", note: "Tilesweeper: тема Castle, Classic 9×9/16×16/30×16 і Arcade з нестандартними формами"}
  - {kind: itch, url: "https://marissaangell.itch.io/timesweeper", note: "Timesweeper: міни рухаються, поле — шари часових кроків, Q/E перемикають крок; Thinky Puzzle Jam 3"}
  - {kind: other, url: "https://steamcommunity.com/app/787980/guides/", note: "посібники спільноти 4D Minesweeper (самі посібники не відкрились — 429)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=4D+Minesweeper+gameplay", note: "пошук; 4D Minesweeper"}
stage: v1
coverage: 65
mechanics: [neighbor-count-clue, flood-reveal, flag-cycle, cell-click, hover-highlight, remaining-counter, no-guess-generation, mines-after-first-click, wrap-edges, level-bank, save-autosave, field-size-picker, difficulty-levels, +n-dimensional-neighborhood, +slice-view, +delta-clue-mode, +per-axis-wrap, +starting-move-button, +shaped-board, +time-layer-board, +moving-mines-deduction, +timeline-scrub]
proposes: ["+axis:field=nd", "+axis:field=timeline", "+cond:adjacent_count_nd", "+ui:neighbor-highlight", "+ui:timeline-scrubber", "+feature:delta-mode", "+card:time-layer-board"]
author: opus
date: 2026-11-09
---

# Minesweeper у вимірах — та сама підказка «скільки мін поруч», але сусідство розтягнуто на 4 виміри або на сусідні моменти часу

## Суть
База — [minesweeper](minesweeper.md): відкрий усі безпечні клітини, число = кількість мін серед сусідів. Тут три ігри, що міняють **граф сусідства**, а не правила. **4D Minesweeper** (Julian Schlüntz, 2018) — поле в чотирьох вимірах, у клітини до 80 сусідів, показане на 2D-екрані, з delta-режимом підказок і вимірами, що замикаються в кільце. **Timesweeper** (Marissa Angell, 2023, джем) — міни **рухаються**: поле — стос часових кроків, міна між кроками зсувається на сусідню клітину, і нуль на одному кроці щось каже про сусідні кроки. **Tilesweeper** (IEVO, 2018) — класика в 3D-темі з полями нестандартної форми; механічно найближча до бази. Інші варіанти правил — у [14-minesweeper-variants](14-minesweeper-variants.md), нескінченне поле — у [minesweeper-infinite](minesweeper-infinite.md), сфера — у [globesweeper](globesweeper.md).

### Що змінено
| Гра | Поле | Сусіди клітини | Нове |
|---|---|---|---|
| Minesweeper | 2D прямокутник | ≤ 8 | — |
| 4D Minesweeper | 1D–4D, кожен вимір — відрізок або кільце | ≤ 80 (3⁴ − 1) | delta-режим, підсвітка сусідів, пазли без вгадування, кнопка «стартовий хід» |
| Timesweeper | 2D × часові кроки | сусіди в межах свого кроку; міна зсувається між кроками | перемотка Q/E, «нуль» обмежує сусідні кроки |
| Tilesweeper | 2D, Arcade — довільна форма | ≤ 8 | тема й форма поля |

## Поле і час
- **4D:** поле `a×b×c×d` (кожен розмір задається; 1D/2D/3D — частковий випадок), завжди показане у 2D (як саме — зрізами (?)). Будь-який вимір можна зробити «сферичним» — кінці зʼєднуються, тож виходять труби, тори й інші форми; сусідство тоді через край (`wrap-edges` на кожну вісь).
- **Timesweeper:** рівень — кілька часових кроків одного 2D-поля; між кроками кожна міна переходить у сусідню клітину (діагональ теж) або (у принципі) стоїть. Q/E — показати попередній/наступний крок. Пазли розвʼязні й за припущення, що міни можуть стояти.
- **Tilesweeper:** Classic — стандартні 9×9, 16×16, 30×16; Arcade — поля нестандартних форм і розмірів.
- Усі — без часу на ходи (`time: static`); таймер, якщо є, — лише рекорд (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | mark | — | відкривається кліком |
| Відкрита клітина з числом | mark | 0…80 (4D) | число мін серед сусідів; delta-режим — мін, що лишились невідмічені |
| Міна | hazard | — | відкрити = програш |
| Рухома міна (Timesweeper) | hazard | позиція на кожному кроці | між кроками зсувається в одну з 8 сусідніх клітин (або лишається) |
| Прапорець | mark | — | позначка гравця |
| Вимір-кільце (4D) | zone | відкритий / замкнений | замкнений додає сусідів через край |
| Часовий крок (Timesweeper) | zone | номер | окреме 2D-поле зі своїми мінами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(reveal, cell)` → ЯКЩО `occupied(cell, mine)` → ТО `lose`; інакше `reveal(cell)`, `set_value(cell, adjacent_count(cell, mine))`.
- 4D: `custom: «сусіди = усі клітини, що відрізняються на ≤1 по кожній з 4 осей, крім самої клітини (до 80)»`; ЯКЩО `custom: «вісь замкнена»` → ТО `wrap` по цій осі.
- КОЛИ `input(hover, cell)` (4D) → ТО `custom: «підсвітити всіх сусідів клітини в усіх зрізах»` (`+ui:neighbor-highlight`).
- КОЛИ `custom: «delta-режим»` → ТО `custom: «число = сусідні міни − сусідні прапорці»` (`+feature:delta-mode`).
- КОЛИ `input(start_move)` (4D) → ТО `reveal(safe_cell)` — кнопка дає безпечний старт.
- КОЛИ `reveal(cell)` → ЯКЩО `adjacent_count(cell, mine, ==, 0)` → ТО `custom: «каскад»` (`flood-reveal`) — для 4D і Tilesweeper (?).
- КОЛИ `input(flag, cell)` → ТО `mark(cell, flag)`; `remaining-counter` −1.
- Timesweeper: КОЛИ `input(timeline, ±1)` → ТО `custom: «показати сусідній часовий крок»`.
- Timesweeper: КОЛИ `custom: «перехід між кроками t → t+1»` → ТО `move(mine, neighbor8|stay)`.
- Timesweeper: ЯКЩО `adjacent_count(cell@t, mine, ==, 0)` → ТО `custom: «на кроках t±1 у самій клітині міни бути не може»` — бо міна приходить лише з сусідньої клітини.
- Timesweeper: `custom: «кількість мін, що лишились, — головна підказка деяких рівнів»`.
- КОЛИ `custom: «усі безпечні клітини відкрито»` → ТО `win` (Timesweeper — на всіх часових кроках).
- 4D: генерація `no-guess-generation` для 80+ готових пазлів; поле зберігається при виході (`save-autosave`).

## Керування і ввід
- **4D:** клік — відкрити, правий клік — прапорець (?); наведення — підсвітка сусідів; кнопка «стартовий хід».
- **Timesweeper:** ЛКМ — відкрити, ПКМ — прапорець, Ctrl — перемкнути підсвітку (показує клітини, куди могла піти міна), Q/E — крок часу; кнопка рестарту рівня (v1.1).
- **Tilesweeper:** як класика (?).

## Вікна, меню, HUD
- **4D:** `game-screen` — 2D-подача 4D-поля, `remaining-counter`; `field-size-picker` — розміри й замкненість кожного виміру; `puzzle-select` — 80+ пазлів.
- **Timesweeper:** `game-screen` з `+ui:timeline-scrubber` (номер кроку, Q/E), перемикач підсвітки; `level-select` (?); прогрес не зберігається.
- **Tilesweeper:** `main-menu` → `theme-select` (поки одна тема Castle) → `mode-select` (Classic / Arcade) → `game-screen`.

## Фічі поза полем
- 4D: `level-bank` (80+ пазлів без вгадування), `save-autosave`, Steam Cloud; `custom-difficulty` — розміри й кількість вимірів.
- Timesweeper: прототип для Thinky Puzzle Jam 3; задумані, але вирізані петлі часу, розгалужені лінії часу й «паралельні всесвіти».
- Tilesweeper: теми як DLC (заявлено).

## Варіації й родичі
- У корпусі: `minesweeper` (база), `14-minesweeper-variants` (правила-модифікатори), `globesweeper` (сфера — інша топологія), `minesweeper-infinite`, `minesweeper-genius`, `hexcells` (інша сітка).
- **Осі варіацій «граф сусідства»:** розмірність (1D…4D); межі по кожній осі (відрізок / кільце); час як вісь (статичні міни / міни, що рухаються між кроками); форма поля (прямокутник / довільна маска).

## Цікавинки для курсу
- N-вимірне поле і сусідство через `itertools.product([-1,0,1], repeat=n)` — 🌱 у коді, 📎 з рендером зрізами.
- Замикання будь-якої осі (тор у 4D) — 🌱.
- Delta-режим: число мінус прапорці — 🌱.
- Рендер 4D-поля на 2D-екрані сіткою зрізів з підсвіткою сусідів у всіх зрізах — 🥉.
- Міни, що рухаються між часовими кроками, і дедукція через кроки — 🥈 (генератор і перевірка розвʼязності складні).
- Генерація без вгадування для 80-сусідства — 🥇.

## Мапа на каталог
- Є: `neighbor-count-clue` · `flood-reveal` · `flag-cycle` · `cell-click` · `hover-highlight` · `remaining-counter` · `no-guess-generation` · `mines-after-first-click` (≈ кнопка стартового ходу) · `wrap-edges` · `level-bank` · `save-autosave` · `field-size-picker`.
- **Нема** → пропозиції карток:
  - `+n-dimensional-neighborhood` «Сусідство в N вимірах» · game-logic/constraints · 📎.
  - `+slice-view` «Багатовимірне поле як сітка 2D-зрізів» · interface/render · 🥉.
  - `+delta-clue-mode` «Підказка мінус поставлені позначки» · game-logic/constraints · 🌱.
  - `+per-axis-wrap` «Кожна вісь — відрізок або кільце» · entities/move · 🌱 (дитина `wrap-edges`).
  - `+starting-move-button` «Кнопка безпечного старту» · game-logic/difficulty · 🌱.
  - `+shaped-board` «Поле довільної форми-маски» · levels/format · 🌱.
  - `+time-layer-board` «Поле як стос часових кроків» · levels/format · 🥈.
  - `+moving-mines-deduction` «Приховані сутності рухаються між кроками» · game-logic/constraints · 🥈.
  - `+timeline-scrub` «Перемикання часового кроку» · interface/input · 🌱.

## Пропозиції до словників
- `+axis:field=nd` — N-вимірна сітка (ширше за `3d`); `+axis:field=timeline` — поле × час як вісь (Timesweeper, 5D Chess).
- `+cond:adjacent_count_nd` — лічильник сусідів у N вимірах (або параметр `adjacent_count(..., dims=n)`).
- `+ui:neighbor-highlight` — підсвітка всіх сусідів клітини (критично, коли сусіди не поруч на екрані).
- `+ui:timeline-scrubber` — перемикач/повзунок часового кроку (повтор з Frozen Synapse).
- `+feature:delta-mode` — альтернативна подача підказок.
- `+card:time-layer-board` — див. вище.

## Джерела
- ⭐ [Steam: 4D Minesweeper](https://store.steampowered.com/app/787980/) — 80 сусідів, підсвітка, delta-режим, сферичні виміри, 1D–4D у 2D-подачі, 80+ пазлів без вгадування, стартовий хід, автозбереження.
- [Steam: Tilesweeper](https://store.steampowered.com/app/867180/) — тема Castle, Classic і Arcade.
- [itch.io: Timesweeper](https://marissaangell.itch.io/timesweeper) — керування, рух мін, правило нуля через кроки (відповіді авторки в коментарях), джем.
- [Steam: посібники 4D Minesweeper](https://steamcommunity.com/app/787980/guides/) — список; самі посібники не відкрились.
- YouTube: пошук «4D Minesweeper gameplay».

## Непевне
- (?) Як саме 4D-поле розкладено на екрані (велика сітка з малих 2D-зрізів — найімовірніше, але не підтверджено) і чи є навігація/прокрутка зрізів.
- (?) Чи є в 4D каскад нулів і безпечний перший клік поза кнопкою «стартовий хід».
- (?) Tilesweeper: «аркадний режим на час» із черги не підтверджено — Steam описує Arcade лише як нестандартні форми; теги Physics/Destruction натякають на фізичне руйнування плиток.
- (?) Timesweeper: чи зсуваються міни на кожному кроці обовʼязково; чи відкриття на одному кроці щось відкриває на інших; чи є каскад нулів.
- (?) `field: graph` — компромісно для N-вимірного й часового сусідства.
