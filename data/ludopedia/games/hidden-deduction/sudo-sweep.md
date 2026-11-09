---
title: Sudo Sweep
slug: sudo-sweep
aka: []
family: hidden-deduction
also: [pencil-logic]
klass: puzzle
axes:
  field: layers
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: null
platforms: [web (HTML5)]
links:
  - {kind: itch, url: "https://gamesforcrows.itch.io/sudo-sweep", best: true, note: "грати в браузері; правило «цифра судоку = кількість мін у секторі», коментарі про розміри"}
  - {kind: other, url: "https://github.com/vividfax/sudo-sweep", note: "відкритий код (p5.js): Sudoku.js, Minesweeper.js, sketch.js"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sudo+Sweep+sudoku+minesweeper", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [cell-click, chord-click, flood-reveal, neighbor-count-clue, markup-validity, satisfy-constraints, completion-detection, difficulty-levels, field-size-picker, dot-mark, game-screen, +linked-puzzles, +region-mine-count, +auto-chord, +cycle-digit-click, +elapsed-timer]
proposes: ["+cond:count_in_region", "+effect:cycle_value", "+effect:auto_chord", "+feature:size-cycle-button", "+card:linked-puzzles", "+card:region-mine-count", "+card:auto-chord", "+card:cycle-digit-click"]
author: opus
date: 2026-11-09
---

# Sudo Sweep — два пазли поруч: цифра в клітині судоку каже, скільки мін у відповідному секторі сапера

## Суть
На екрані дві сітки: мале судоку і великий сапер, поділений на сектори — по одному на клітину судоку. Цифра в клітині судоку (у грі показана як 0…N−1) дорівнює кількості мін у відповідному секторі. Судоку майже без даних (лише кілька «нулів»), тож розвʼязати його можна лише через сапер, а сапер — через судоку. Перемога — коли судоку заповнене правильно і всі безпечні клітини сапера відкриті.

## Поле і час
- Два поля одночасно (`field: layers` — логічно звʼязані шари): судоку N×N з блоками w×h і сапер (N·sw)×(N·sh), де sw×sh — розмір сектора.
- П'ять пресетів (кнопка розміру по колу): судоку 4×4 (блоки 2×2) з секторами 2×2; 6×6 (3×2) з секторами 3×2; 6×6 з 3×3; 9×9 (3×3) з 3×3 → сапер 27×27; 9×9 з 4×4 → сапер 36×36.
- Статичний пазл; секундомір стартує з першого кліку і показується в кінці.
- Генерація: повне судоку бектрекінгом → у кожному секторі d−1 мін на випадкових місцях (d — справжня цифра 1…N).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина судоку | mark | значення 0…N−1 або порожньо | клік крутить цифру по колу |
| Дана клітина судоку | mark | завжди «0» | не змінюється; N−1 штук, по одній у стовпці, крім одного |
| Блок судоку | zone | w×h | цифри без повторів |
| Сектор сапера | zone | sw×sh клітин | кількість мін = цифра відповідної клітини судоку |
| Закрита клітина сапера | static | прихований вміст | відкривається лівим кліком |
| Міна | hazard | — | відкриття → вибух, усе поле відкрите, поразка |
| Число сапера | mark | n | мін серед 8 сусідів (через межі секторів) |
| Порожня клітина | mark | 0 сусідів | відкриває сусідів каскадом |
| «?» (прапорець) | mark | — | блокує лівий клік; не рахується в перевірці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left, sudoku_cell)` → ЯКЩО `not custom: «дана клітина»` → ТО `custom: «значення +1 по колу, після максимуму — порожньо»`.
- КОЛИ `input(right, sudoku_cell)` → ТО `custom: «значення −1 по колу»`.
- Судоку: `unique(row)`, `unique(col)`, `unique(block)`; звʼязок полів: `custom: «кількість мін у секторі = значення клітини судоку»`.
- КОЛИ `input(left, c)` → ЯКЩО `occupied(c, mine)` and `not state(c, flagged)` → ТО `reveal(all)`, `lose`.
- КОЛИ `input(left, c)` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `reveal(c)` + каскад по порожніх; інакше `reveal(c)` з числом.
- КОЛИ `input(right, c)` → ЯКЩО `not state(c, revealed)` → ТО `mark(c, ?)` / `unmark(c)`.
- КОЛИ `input(left, c)` → ЯКЩО `custom: «прапорців навколо c = числу c»` → ТО `reveal(8 сусідів без «?»)` — акорд спрацьовує сам після будь-якого лівого кліку; міна серед них → вибух.
- КОЛИ `custom: «судоку = розвʼязок»` and `custom: «усі безпечні клітини сапера відкриті»` → ТО `win`, фон змінюється, показ часу.
- Перемога: обидва пазли розвʼязано. · Поразка: відкрита міна. · Рахунок: час у секундах.
- Першого безпечного кліку нема: міни розкладено до гри, перший клік може влучити.

## Керування і ввід
- Лише миша. Судоку: лівий клік +1, правий −1 (по колу з порожнім). Сапер: лівий — відкрити (і авто-акорд), правий — поставити/зняти «?».
- Кнопки під полем: «новий пазл» і «розмір» (по колу пʼять пресетів).
- Нотаток-кандидатів у судоку нема (гравці просять).

## Вікна, меню, HUD
- `game-screen`: судоку зліва/зверху (?), сапер з товстими межами секторів, дві кнопки; таймер з'являється по завершенні («103.516 seconds»).
- Окремих меню нема; `end-screen` — зміна фону на виграш + час.
- HUD: `timer-elapsed` (в кінці), межі блоків/секторів.

## Фічі поза полем
- `difficulty-presets` — пʼять розмірів кнопкою по колу (`+feature:size-cycle-button`).
- Відкритий код на GitHub (Processing/p5.js); тег itch «color-blind friendly».
- Нема undo, підказок, збереження, рекордів.

## Варіації й родичі
- Сапер з регіонами-лічильниками: [tametsi](tametsi.md) (лічильник кольорової групи), [14-minesweeper-variants](14-minesweeper-variants.md).
- Інші гібриди «сапер + пазл»: [polimines](polimines.md), [lizzi-crossing](lizzi-crossing.md) (нонограма); судоку — `pencil-logic/sudoku.md`.
- Осі варіацій: **звʼязок пазлів** цифра = кількість мін у секторі / сума / позиція; **дані** судоку майже без даних (тримається на сапері) / звичайне судоку; **безпечність** перший клік ризиковий / безпечний / без вгадувань.

## Цікавинки для курсу
- Два поля з відображенням «клітина ↔ сектор» і спільна перевірка перемоги — 🥉.
- Генерація: бектрекінг судоку → розкладка мін за цифрами — 📎.
- Авто-акорд після кожного кліку (`flags == number`) — 🌱.
- Цифра по колу ЛКМ/ПКМ без клавіатури — 🌱.
- Генератор без 50/50: перевіряти спільний солвер двох пазлів — 👑 (автор визнає, що 50/50 лишились).

## Мапа на каталог
- Є: `cell-click` · `chord-click` ↔ авто-акорд · `flood-reveal` · `neighbor-count-clue` · `markup-validity` ↔ судоку · `satisfy-constraints` + `completion-detection` ↔ подвійна перевірка · `difficulty-levels` + `field-size-picker` ↔ пресети · `dot-mark` ↔ «?» · `game-screen`.
- **Нема** → пропозиції карток:
  - `+linked-puzzles` «Два пазли, що розвʼязують один одного» · game-logic/constraints · 🥉.
  - `+region-mine-count` «Регіон із заданою кількістю цілей» · game-logic/constraints · 🌱.
  - `+auto-chord` «Акорд спрацьовує сам після кліку» · interface/input · 🌱.
  - `+cycle-digit-click` «ЛКМ/ПКМ крутять значення клітини по колу» · interface/input · 🌱.
  - `+elapsed-timer` «Секундомір від першого кліку» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:count_in_region(zone, kind, op, n)` — кількість сутностей виду в регіоні/секторі.
- `+effect:cycle_value(cell, ±1)` — значення клітини по колу.
- `+effect:auto_chord` — відкрити сусідів, якщо прапорці збігаються з числом.
- (`timer-elapsed` уже є в ui-elements — лише вжиток.)
- `+feature:size-cycle-button` — одна кнопка перебирає пресети розміру.

## Джерела
- ⭐ [itch.io: Sudo Sweep](https://gamesforcrows.itch.io/sudo-sweep) — «each square in the sudoku corresponds to a sector in the minesweeper», коментарі про 27×27 і 36×36, «?» правим кліком, 50/50; Rianna Suen (Games For Crows), програмування qqwref.
- [GitHub: vividfax/sudo-sweep](https://github.com/vividfax/sudo-sweep) — код: пресети розмірів, d−1 мін на сектор, дані «0», авто-акорд, вибух, перевірка перемоги, таймер.
- YouTube: пошук «Sudo Sweep sudoku minesweeper».

## Непевне
- (?) Рік випуску — на сторінці не вказано.
- (?) Розміщення двох полів на екрані.
- (?) Розміри сапера для пресетів 4×4 і 6×6 (8×8, 18×12, 18×18) — висновок з коду (N·sw × N·sh), не з гри.
- (?) Версія на itch може відрізнятися від коду в репо (гілка master).
