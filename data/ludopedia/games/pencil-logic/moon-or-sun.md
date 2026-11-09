---
title: Moon or Sun (月か太陽)
slug: moon-or-sun
aka: [Moonsun, 月か太陽, Tsuki ka Taiyō, Місяць або Сонце]
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
year: null
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/moon_or_sun/", best: true, note: "Nikoli: правила EN з картинками «Sample / Progressing / Solution»"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Moonsun/index.htm", note: "Janko: правила DE/EN, 200 пазлів грати в браузері"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/moonsun.js", note: "puzz.link/pzpr: правила EN/JP, Nikoli vol. 154, тести вводу, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти кодів помилок (bkMSPassedGt2.moonsun…)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=moon+or+sun+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, single-loop-check, path-drawing, path-cut, edge-marking, conflict-highlight, in-game-editor, import-open-formats, level-bank, undo-redo, +irregular-regions, +region-visit-once, +alternating-region-type, +input-scheme-toggle]
proposes: ["+cond:visits(loop, region, n)", "+cond:alternates", "+cond:crosses", "+trigger:pattern(loop_branch)", "+card:region-visit-once", "+card:alternating-region-type"]
author: opus
date: 2026-11-09
---

# Moon or Sun — петля заходить у кожну кімнату рівно раз і бере там або всі місяці, або всі сонця, чергуючи їх

## Суть
Поле поділене товстими лініями на кімнати; у клітинках стоять символи місяця й сонця. Гравець малює одну замкнену петлю через центри клітинок, яка відвідує кожну кімнату рівно один раз. У кожній кімнаті петля проходить через усі місяці й жодного сонця або навпаки, а «місячні» й «сонячні» кімнати вздовж петлі чергуються. Незвичне: обмеження накладене не на клітинку, а на послідовність кімнат уздовж шляху.

## Поле і час
- Прямокутна сітка; кімнати — області з товстими межами (Nikoli: прямокутники; puzz.link: довільні області).
- Клітинки: порожня · місяць · сонце.
- Шари: кімнати й символи (незмінні) · петля гравця (сегменти) · допоміжні мітки.
- Час статичний; хід = додати/стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | межі | петля входить і виходить рівно раз; тип кімнати = місячна або сонячна |
| Місяць | static | — | у місячній кімнаті петля мусить пройти через усі місяці; у сонячній — обійти |
| Сонце | static | — | дзеркально до місяця |
| Порожня клітинка | terrain | — | петля може пройти або ні |
| Петля | mark | сегменти | одна, замкнена; без перетинів і розгалужень; клітинку не відвідує двічі |
| Допоміжна мітка | mark | — | хрестик / позначка гравця (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, cells)` → ТО `custom: «додати сегменти петлі між сусідніми центрами»`; drag назад — стерти.
- КОЛИ `pattern(loop_branch)` → ТО `set_state(cell, error)` (pzpr `lnBranch`).
- КОЛИ `constraint_broken(crossing)` → ЯКЩО `custom: «петля перетинає себе»` (`+cond:crosses`) → ТО `set_state(cell, error)` (`lnCross`).
- КОЛИ `constraint_broken(room_twice)` → ЯКЩО `custom: «петля заходить у кімнату вдруге»` (`+cond:visits(loop, region, n)`) → ТО `set_state(room, error)` (`bkPassTwice`: «A line passes a room twice or more»).
- КОЛИ `constraint_broken(room_skipped)` → ЯКЩО `custom: «петля не заходить у кімнату»` → ТО `set_state(room, error)` (`bkNoLine`).
- КОЛИ `constraint_broken(both_marks)` → ЯКЩО `custom: «у кімнаті пройдено і місяць, і сонце»` → ТО `set_state(room, error)` (`bkBothMarksPassed`).
- КОЛИ `constraint_broken(no_marks)` → ЯКЩО `custom: «у кімнаті не пройдено жодного символу»` → ТО `set_state(room, error)` (`bkNoMarksPassed`).
- КОЛИ `constraint_broken(not_all)` → ЯКЩО `state(room, moon)` and `custom: «не всі місяці кімнати на петлі»` → ТО `set_state(room, error)` (`bkNotAllMSPassed`); для сонць — `bkNotAllMUPassed`.
- КОЛИ `constraint_broken(alternation)` → ЯКЩО `same(room, next_room, type)` → ТО `set_state(room, error)` (`bkMSPassedGt2` / `bkMUPassedGt2`: «passes the marks of the moon for two rooms in a row»).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «у клітинці 1 сегмент»` → ТО `set_state(cell, error)` (`lnDeadEnd`).
- КОЛИ `constraint_broken(loops)` → ЯКЩО `not single_loop` → ТО `set_state(board, error)` (`lnPlLoop`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «парність»: тип чергується вздовж замкненої петлі, тож кімнат парна кількість, а сусідні по петлі кімнати — різного типу; дві кімнати, які петля мусить пройти поспіль, отримують протилежні типи.
- Дедукція «вибір типу»: якщо в кімнаті символи одного виду неможливо всі зібрати одним заходом (розкидані, заблоковані), кімната — іншого типу.
- Перемога: одна петля, кожна кімната — рівно один захід, усі символи обраного типу пройдено, протилежного — ні, типи чергуються. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: ліва кнопка + drag малює петлю; клік по клітинці ставить допоміжні мітки — тест показує, що клік по символу (`mouse,left, 1,1`) змінює стан усіх символів кімнати (?).
- puzz.link: налаштування `use` (`setconfig,use,1`) — схема кнопок миші (ліва/права окремо чи одна кнопка) (?).
- puzz.link edit: повторний клік по клітинці (`leftx2`) перебирає місяць / сонце / порожньо; межі кімнат малюються drag-ом (?).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами кімнат, символи місяця й сонця, петля, `conflict-highlight` для кімнати чи клітинки з помилкою.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window` (схема вводу).
- `help-window` — правила (Nikoli з трьома картинками; puzz.link; Janko).
- `puzzle-select` — 200 пазлів Janko.
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko; генератора не бачив (?).

## Варіації й родичі
- У сімʼї: [Country Road](country-road.md) (кожна область — рівно один захід петлі), [Masyu](masyu.md) (два види кружків як правила петлі), [Heyawake](heyawake.md) (кімнати), [Nagareru Loop](nagareru-loop.md), [puzz.link](puzz-link.md).
- pzpr ділить з Moon or Sun коди помилок жанру Dotchi Loop 2 («white and black pearls in the same region») — близький родич (?).
- **Осі варіацій**: що вимагає кімната (усі символи одного виду / кількість / жоден) · чергування (так / ні / за шаблоном) · скільки разів у кімнату (рівно 1 / ≥1) · форма кімнат (прямокутники / довільні).

## Цікавинки для курсу
- Розбиття петлі на послідовність заходів у кімнати (обхід циклу з мапою клітинка → кімната) — 📎.
- Перевірка «рівно один захід» через підрахунок перетинів межі кімнати (рівно 2 сегменти на межі) — 🌱.
- Перевірка «усі символи одного виду, жодного іншого» в кожній кімнаті — 🌱.
- Перевірка чергування по циклу (і висновок про парність кількості кімнат) — 📎.
- Повний валідатор з кодами pzpr — 🥉; розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints`, `single-loop-check` · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід петлі · `conflict-highlight` · `in-game-editor`, `import-open-formats` (puzz.link) · `level-bank` (Janko) · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+irregular-regions` — повтор: поле поділене на довільні області.
  - `+region-visit-once` — повтор з Country Road: петля заходить у кожну область рівно раз.
  - `+alternating-region-type` «Тип області чергується вздовж шляху» · game-logic/constraints · 📎 · слот {types: 2|n}.
  - `+input-scheme-toggle` — повтор: схема кнопок миші в налаштуваннях.

## Пропозиції до словників
- `+cond:visits(loop, region, n)` — повтор з Country Road: скільки разів лінія заходить в область.
- `+cond:alternates` — властивість чергується вздовж послідовності (кімнат шляху, ходів).
- `+cond:crosses` — лінія перетинає себе (повтор з Masyu/Icebarn).
- `+trigger:pattern(loop_branch)` — повтор.
- `+card:region-visit-once`, `+card:alternating-region-type` — див. мапу.

## Джерела
- ⭐ [Nikoli: Moon or Sun](https://www.nikoli.co.jp/en/puzzles/moon_or_sun/) — правила: «The loop goes through each room only one time», «all of the moon cells or all of the sun cells», чергування; кімнати — прямокутники; картинки Sample / Progressing / Solution.
- [Janko: Moonsun](https://www.janko.at/Raetsel/Moonsun/index.htm) — правила DE/EN, назви Moonsun / 月か太陽, 200 пазлів; винахідник невідомий.
- [puzz.link moonsun.js](https://puzz.link/js/pzpr-samples/moonsun.js) — правила EN/JP («All regions must have at least one moon or sun that is used»), Nikoli vol. 154, коди `lnBranch`, `lnCross`, `bkPassTwice`, `bkBothMarksPassed`, `bkMSPassedGt2`, `bkMUPassedGt2`, `bkNotAllMUPassed`, `bkNotAllMSPassed`, `bkNoLine`, `bkNoMarksPassed`, `lnDeadEnd`, `lnPlLoop`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- YouTube: пошук «moon or sun nikoli puzzle».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 154; рік не перевірено (`year: null`).
- (?) Що саме робить клік по символу в play-режимі puzz.link (тест змінює стан усіх трьох клітинок кімнати) — схоже на допоміжне «викреслити тип», не перевірено.
- (?) Сенс `setconfig,use` — за аналогією з іншими жанрами pzpr.
- (?) Звʼязок із Dotchi Loop 2 — лише за спільними ключами помилок у failcode.en.json.
