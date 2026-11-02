---
title: Light Up (Akari, Бідзюцукан)
slug: light-up
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
year: 2001
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Light_Up_(puzzle)", best: true, note: "правила, назви Akari/Bijutsukan, техніки, NP-повнота й класи Akari-n"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/akari/", note: "Nikoli: 4 правила, рік 2001, Sample → Progressing → Solution"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html", note: "Tatham Light Up: правила, ввід, параметри Custom, преференс міток"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html", note: "Light Up у браузері (WebAssembly)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/lightup.js", note: "puzz.link: правила, тести вводу use=1/2, коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=akari+light+up+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, import-open-formats, impassable-cells, +undo-redo, +seed-share, +dot-mark, +solve-into-undo, +input-scheme-toggle, +ray-cast-light, +neighbor-count-clue, +guarded-marks, +symmetry-generation]
proposes: ["+effect:illuminate", "+cond:lit", "+trigger:pattern(unlit_cell)", "+window:params-dialog", "+feature:symmetry-option", "+card:ray-cast-light", "+card:neighbor-count-clue", "+card:guarded-marks"]
author: opus
date: 2026-11-02
---

# Light Up (Akari) — розстав лампи, щоб освітити всю залу й жодна лампа не бачила іншу

## Суть
Сітка з білих і чорних клітинок (стін); частина стін має число 0–4. Гравець ставить лампи в білі клітинки; лампа світить по своєму рядку й стовпцю до стіни або краю. Треба освітити кожну білу клітинку так, щоб жодна лампа не освітлювала іншу, а кожна стіна з числом мала рівно стільки ламп ортогонально поруч. Незвичне: обмеження задає **промінь** (видимість по лінії), а не сусідство — те саме обчислення, що «ворог бачить гравця» в аркадах. Японська назва 美術館 — «художній музей» (лампи-охоронці освітлюють залу).

## Поле і час
- Прямокутна сітка; типи клітинок: біла (порожня), чорна без числа, чорна з числом 0–4.
- Промінь — 4 напрямки до першої чорної або рамки; діагоналі не світять і не рахуються для чисел.
- Шари клітинки: тип (незмінний) · стан гравця: порожньо / лампа / мітка «тут не лампа» · похідне: освітлена чи ні.
- Час статичний; хід = поставити/зняти лампу чи мітку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | mark | стан empty / bulb / no-bulb mark; lit | приймає лампу чи мітку; у розвʼязку — освітлена |
| Лампа | mark | — | освітлює себе й промені в 4 напрямках до стіни; не може бути освітлена іншою лампою |
| Мітка «не лампа» (крапка) | mark | — | позначка гравця; Tatham: на ній не можна поставити лампу |
| Чорна стіна | static | — | непрохідна для променя; без вимог |
| Чорна стіна з числом | static | N 0–4 | рівно N ламп у 4 ортогональних сусідах |
| Промінь (освітлена смуга) | zone | рядок/стовпець між стінами | похідна область; підсвічується жовтим |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `cell(x, white)` and `not state(cell, marked)` → ТО `mark(cell, bulb)`; повтор → `unmark(cell)`.
- КОЛИ `input(right_click, cell)` → ЯКЩО `cell(x, white)` → ТО `mark(cell, no_bulb)`; повтор → `unmark(cell)` (Tatham: мітку не ставлять на освітлену клітинку (?)).
- КОЛИ `after(mark(bulb))` → ТО `custom: «освітити рядок і стовпець до першої стіни»` (`+effect:illuminate`).
- КОЛИ `line_of_sight(bulb, bulb)` → ТО `constraint_broken(bulbs_see_each_other)`, обидві лампи червоні (Tatham; puzz.link `akariDup`).
- КОЛИ `constraint_broken(wall_count)` — ЯКЩО `not adjacent_count(wall, bulb, ==, N)` → ТО число червоне (Tatham — коли ламп забагато або сусіди вже вичерпані (?); puzz.link `nmAkariNe`).
- КОЛИ `constraint_broken(all_lit)` — ЯКЩО є біла клітинка без світла → ТО конфлікт при перевірці (puzz.link `ceDark`).
- КОЛИ `all_constraints_met` → ТО `win`; Tatham: розвʼязано, коли всі білі жовті й нема червоних ламп.
- Дедукції (Wikipedia): почати з 4 або з числа, обмеженого стінами; клітинка, яку може освітити лише одна кандидатка, → там лампа; навколо 0 і діагонально до 3 → мітки; пари «3 через клітинку», «1 по діагоналі до 2» — шаблони.
- Перемога: усе освітлено, лампи не бачать одна одну, числа виконані. Поразки й рахунку нема.

## Керування і ввід
- Tatham: ліва кнопка — лампа вкл/викл; права — мітка вкл/викл; лампа не стає на мітку.
- puzz.link: `use=1` — ліва лампа, права крапка; `use=2` — ліва циклює порожньо → лампа → крапка, права — назад; drag правою протягує крапки.
- Клавіатура: курсор стрілками + клавіші дій (Tatham, загальні) (?).
- Спільні дії Tatham: N, U/Ctrl+Z, R/Ctrl+R, Restart, Solve.

## Вікна, меню, HUD
- `game-screen`: сітка, лампи-кружечки, освітлені клітинки жовті, `conflict-highlight` (червоні лампи й числа), `dot-mark` (мітки).
- Tatham: Game (New, Restart, Undo, Redo, Solve, Enter game ID, Enter random seed, Download/Upload save file, Preferences) · Type (пресети + Custom…).
- `+window:params-dialog` (Custom…): Width, Height, %age of black squares, Symmetry, Difficulty (Easy — без перебору; Hard — ймовірно з вгадуванням).
- `settings-window` (Preferences): чи малювати мітки «not a light» на освітлених клітинках.
- `+window:game-id-dialog` — ID / seed пазла.
- `help-window` — правила (Nikoli, Tatham doc).
- Переходи: Type → Custom → params-dialog → генерація → game-screen; розвʼязання → спалах → New game.

## Фічі поза полем
- `auto-check` миттєвий (Tatham: червоне) або за кнопкою (puzz.link — код першої помилки).
- `undo`/`redo` ∞; `auto-solve` у історії undo; `seed-input`, `share-code`, збереження у файл.
- `custom-difficulty`: розмір, відсоток стін (генератор може додати більше), симетрія стін, складність.
- `level-editor` + `share-code` (puzz.link edit mode).
- `puzzle-bank`: три книги Nikoli Akari станом на 2011; сайти щоденних пазлів.

## Варіації й родичі
- **Akari-n** (Wikipedia): стіни мають лише одне значення n + стіни без числа; Akari-1/2/3 — NP-повні, Akari-4 і без чисел — у P, Akari-0 — невідомо.
- Родичі: Minesweeper (число = кількість обʼєктів довкола), задача художньої галереї (art gallery problem) — охоронці бачать залу; лазерні пазли (`connect-rotate`) — той самий промінь до перешкоди.
- **Осі варіацій**: напрямки променя (4 / 8) · що зупиняє промінь (стіна / лампа / нічого) · чи можуть лампи бачити одна одну · що рахує число (сусіди / освітлені клітинки).

## Цікавинки для курсу
- Промінь до стіни в 4 напрямках і перерахунок освітлення після кожного ходу — 🌱/📎 (інкрементно — 📎).
- «Лампи не бачать одна одну» як `line_of_sight` між однотипними — 🌱; той самий код, що зір ворога.
- Число на стіні = кількість ламп поруч — 🌱 (`adjacent_count`, як у Сапері).
- Мітка, що блокує лампу (guarded input), — 🌱 приклад валідації вводу.
- Генератор із параметрами % стін і симетрії + перевірка унікальності — 👑; лише симетрична розстановка стін — 📎.
- Розвʼязувач правилами «4 → лампи», «0 → мітки», «єдиний кандидат на освітлення» — 🥇.

## Мапа на каталог
- Є: `markup-validity` ↔ червоні лампи/числа · `completion-detection`, `satisfy-constraints` · `cell-click` · `keyboard-controls` · `impassable-cells` ↔ стіни для променя · `unique-puzzle-generation`, `level-solver`, `difficulty-levels`, `field-size-picker`, `game-settings` ↔ Custom · `import-open-formats` ↔ puzz.link URL.
- Перевикористано: `+undo-redo`, `+seed-share`, `+dot-mark`, `+solve-into-undo`, `+input-scheme-toggle` (з Hitori).
- **Нема** → пропозиції карток:
  - `+ray-cast-light` «Промінь до перешкоди» · game-logic/constraints · 📎 · слот {dirs: 4|8} — освітлення Akari, лазери, зір.
  - `+neighbor-count-clue` «Число = кількість обʼєктів у сусідах» · game-logic/constraints · 🌱 · слот {adjacency: 4|8} — Akari (4), Minesweeper (8).
  - `+guarded-marks` «Мітка забороняє хід у клітинку» · interface/input · 🌱.
  - `+symmetry-generation` «Симетрія розстановки при генерації» · levels/generation · 📎 · слот {symmetry}.

## Пропозиції до словників
- `+effect:illuminate` — позначити клітинки по променю до перешкоди як освітлені.
- `+cond:lit` — клітинка освітлена (у будь-якої лампи є `line_of_sight`).
- `+trigger:pattern(unlit_cell)` — лишилась неосвітлена біла клітинка.
- `+window:params-dialog` — форма Custom (повтор із Tatham-збірки, для правила трьох).
- `+feature:symmetry-option` — параметр симетрії в генераторі.
- `+card:ray-cast-light`, `+card:neighbor-count-clue`, `+card:guarded-marks` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Light Up](https://en.wikipedia.org/wiki/Light_Up_(puzzle)) — правила, назви, техніки, NP-повнота (Circuit-SAT), Akari-n.
- [Nikoli: Akari](https://www.nikoli.co.jp/en/puzzles/akari/) — правила й ілюстрації; Nikoli датує жанр 2001 роком.
- [Tatham: Light Up](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html) — ввід, червоні помилки, параметри Custom, преференс міток.
- [Light Up у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html) — меню й кнопки.
- [Tatham: common actions](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — спільні клавіші, Solve в undo.
- [puzz.link lightup.js](https://puzz.link/js/pzpr-samples/lightup.js) — «first appeared in Puzzle Communication Nikoli vol. 95», тести вводу, коди `nmAkariNe`, `akariDup`, `ceDark`.
- YouTube: пошук «akari light up puzzle how to solve».

## Непевне
- (?) Чи Tatham забороняє мітку на освітленій клітинці, чи лише не малює її (преференс) — переказ документації неоднозначний.
- (?) Коли саме Tatham фарбує число червоним (лише перебір чи й неможливість добрати).
- (?) Пресети Type і варіанти Symmetry Tatham — сторінка не перелічує; клавіатурні дії Light Up в доці не описані.
- (?) Рік: Nikoli — 2001, puzz.link — Nikoli vol. 95; точний місяць не перевірено.
