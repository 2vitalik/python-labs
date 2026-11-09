---
title: Undead (Haunted Mirror Maze)
slug: undead
aka: [Haunted Mirror Maze, Vampire Mirror Maze, Spukschloss, Будинок з привидами]
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/undead.html", best: true, note: "Tatham Undead: правила видимості, керування, A/C, Preferences, автор жанру й портера"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html", note: "Undead у браузері; меню Game/Type, кнопки"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Spukschloss/index.htm", note: "janko.at Spukschloss: правила, 60 пазлів 4×4…~50 клітинок, David Millar"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=undead+puzzle+tatham+ghosts+vampires+zombies", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, beam-tracing, mirror-reflect, line-sum-clue, cell-click, keyboard-controls, pencil-marks, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, undo-redo, seed-share, import-open-formats, remaining-counter, +visibility-count-clue, +clue-done-mark, +solve-into-undo, +reflection-visibility, +type-quota]
proposes: ["+cond:view_count", "+cond:seen_via(direct|mirror)", "+cond:type_count", "+effect:reflect", "+ui:count-style-toggle", "+ui:clue-done-mark", "+ui:glyph-toggle", "+window:params-dialog", "+card:reflection-visibility", "+card:type-quota"]
author: opus
date: 2026-11-09
---

# Undead — розстав привидів, вампірів і зомбі в лабіринті дзеркал так, щоб з кожного краю було видно рівно стільки монстрів

## Суть
Поле — сітка з діагональними дзеркалами; кожна клітинка без дзеркала містить одного монстра: привида, вампіра або зомбі. Загальна кількість кожного виду дана. Число на краю — скільки монстрів видно, якщо дивитися в поле з цього місця вздовж рядка/стовпця, відбиваючись від дзеркал. Фокус: вампір видно лише напряму (до першого дзеркала), привида — лише у відображенні (після дзеркала), зомбі — завжди; монстр, якого промінь перетнув двічі, рахується двічі.

## Поле і час
- Прямокутна сітка W×H (Tatham, Custom: Width/Height); janko.at — 4×4, 5×5, 6×6 і близько 50 клітинок.
- Дзеркала `/` і `\` — двосторонні, дані умовою; решта клітинок — порожні під монстрів.
- Підказки — у рамці навколо поля, по одній на кожну клітинку краю з кожного боку (?).
- Над полем — лічильники видів (привиди, вампіри, зомбі) з трьома стилями показу.
- Шари: дзеркала й підказки (незмінні) · монстр гравця · pencil marks · сірі підказки.
- Час статичний; хід = поставити/стерти монстра чи кандидата.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дзеркало `/` / `\` | static | орієнтація | відбиває промінь погляду на 90°, з обох боків |
| Порожня клітинка | mark | монстр або кандидати | має отримати рівно одного монстра |
| Привид (G) | mark | — | видно лише у відображенні (після ≥1 дзеркала) |
| Вампір (V) | mark | — | видно лише напряму (до першого дзеркала) |
| Зомбі (Z) | mark | — | видно завжди |
| Кандидат | mark | набір G/V/Z | ігнорується перевіркою |
| Підказка краю | static | число v, вхідна клітинка, напрямок | промінь з краю бачить рівно v монстрів (з повторами) |
| Лічильник виду | static | загальна кількість | всього монстрів виду = число; сіріє, коли виконано |
| Промінь погляду | zone | шлях від краю до краю | послідовність клітинок; ламається на дзеркалах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` + `input(key_G|1)` → ТО `set_value(cell, ghost)`; V|2 → vampire; Z|3 → zombie (Tatham).
- КОЛИ `input(left_click, count_icon)` → ЯКЩО `custom: «є виділена клітинка»` → ТО `set_value(cell, kind)` (Tatham: клік по лічильнику ставить монстра).
- КОЛИ `input(right_click, cell)` + `input(key_monster)` → ЯКЩО `not custom: «у клітинці вже стоїть монстр»` → ТО `mark(cell, candidate kind)`; повтор тієї ж клавіші → `unmark(cell)` для кандидата.
- КОЛИ `input(key_Space)` на клітинці → ТО `unmark(cell)` (стерти монстра або всі кандидати).
- Промінь: КОЛИ `custom: «промінь входить у клітинку з дзеркалом»` → ТО `custom: «напрямок повертає на 90° за орієнтацією дзеркала»` (`+effect:reflect`); інакше йде прямо до виходу з поля.
- Підрахунок: монстр на промені рахується, ЯКЩО `custom: «зомбі; або вампір і дзеркал ще не було; або привид і дзеркало вже було»` (`+cond:seen_via(direct|mirror)`).
- Повтор: ЯКЩО `custom: «промінь проходить ту саму клітинку вдруге»` → ТО `custom: «монстр рахується кожного разу, коли видимий»` (Tatham).
- КОЛИ `constraint_broken(edge_clue)` → ЯКЩО `custom: «видимих на промені ≠ v»` (`+cond:view_count`) → ТО конфлікт (?).
- КОЛИ `constraint_broken(type_total)` → ЯКЩО `custom: «монстрів виду на полі ≠ лічильнику»` (`+cond:type_count`) → ТО конфлікт.
- КОЛИ `custom: «монстрів виду на полі = лічильнику»` → ТО `mark(count, done)` автоматично (лічильник сіріє, Tatham).
- КОЛИ `input(left_click, clue)` → ТО `mark(clue, done)` / `unmark(clue)` — сіра підказка вручну.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «нуль»: промінь з підказкою 0 — до першого дзеркала лише привиди, після — лише вампіри.
- Дедукція «без дзеркал»: промінь, що проходить поле без дзеркал, бачить усіх, крім привидів.
- Дедукція «вичерпаний вид»: коли лічильник виду виконано, вид викреслюється з кандидатів усіх порожніх клітинок.
- Дедукція «максимум»: підказка = кількість клітинок променя (з повторами), що можуть бути видимими, — усі вони видимі: до дзеркала — V/Z, після — G/Z.
- Перемога: усі клітинки заповнені, лічильники видів і всі підказки краю виконано. Поразки й рахунку нема.

## Керування і ввід
- Tatham: клік по порожній клітинці + G/1, V/2, Z/3; або клік по монстру в лічильниках зверху — ставить у виділену клітинку.
- Виправлення: клік + Space або Undo.
- Pencil: правий клік + клавіша монстра — додати/прибрати кандидата; правий клік + Space або лівий клік + клавіша/Space — очистити кандидатів.
- Клавіатура: стрілки — курсор; Return — перемикач «монстр / кандидат».
- Вигляд: A — картинки ⇄ літери; C або правий клік по лічильнику — стиль лічильника: усього / лишилось (відʼємне) / поставлено з усього.
- Підказки: лівий клік — сіра/звичайна.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve, game ID, seed, save file, Preferences.

## Вікна, меню, HUD
- `game-screen`: сітка з дзеркалами, підказки краю, монстри (картинки або літери), `pencil-marks`, курсор, лічильники видів зверху (`remaining-counter` у стилі «лишилось»).
- Tatham: меню Game (Enter game ID…, Enter random seed…, Download save file…, Upload save file…, Preferences…) · Type (пресети + Custom…) · кнопки New game, Restart game, Undo move, Redo move, Solve game.
- `+window:params-dialog` (Custom…): Width, Height, Difficulty.
- `settings-window` (Preferences): літери чи картинки, стиль лічильників — зберігаються між іграми (на відміну від клавіш A і C).
- `help-window` — «Full instructions».
- Переходи: Type → Custom → генерація → game-screen; Solve → розвʼязок.

## Фічі поза полем
- `undo` / `redo`; `auto-solve`; `seed-input`, `share-code`, збереження у файл.
- `custom-difficulty`: ширина, висота, складність.
- Налаштування вигляду: `+ui:glyph-toggle` (картинки/літери), `+ui:count-style-toggle` (три стилі лічильника).
- janko.at — банк 60 пазлів.

## Варіації й родичі
- Автор жанру — David Millar («Haunted Mirror Maze», «Vampire Mirror Maze»; сайт The Griddle); у Tatham — внесок Steffen Bauer.
- Родичі: [Skyscrapers](skyscrapers.md) і [Kuromasu](kuromasu.md) (число = скільки видно), [Light Up](light-up.md) (промені від ламп), [Tatham Collection](tatham-collection.md) (Undead серед інших).
- Поза сімʼєю: лазери й дзеркала `connect-rotate` (Deflektor, Laser Tank, Khet) — там дзеркало повертають, тут воно дане, а невідоме — вміст клітинок.
- **Осі варіацій**: хто видимий як (напряму / у відображенні / завжди) · повторне проходження (рахувати двічі / раз) · дзеркала дані / ставить гравець · загальні кількості дано / ні.

## Цікавинки для курсу
- Трасування променя з краю через дзеркала `/` `\` до виходу — 🌱.
- Підрахунок видимих з правилом «вампір до дзеркала, привид після, повтори рахуються» — 📎.
- Перемикач вигляду (картинки ⇄ літери) і три стилі лічильника як налаштування з persist — 📎.
- Розвʼязувач: кожен промінь — лінійне обмеження «сума видимостей = v» над змінними клітинок → перебір з пропагацією — 🥇.
- Генератор: випадкові дзеркала + випадкова розстановка → підказки → перевірка єдиності — 🥇.

## Мапа на каталог
- Є: `beam-tracing` ↔ промінь погляду · `mirror-reflect` ↔ дзеркала · `line-sum-clue` ↔ підказка краю · `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks` · `remaining-counter` ↔ лічильники видів · `unique-puzzle-generation`, `difficulty-levels`, `level-solver`, `field-size-picker`, `game-settings` · `undo-redo`, `seed-share`, `import-open-formats`.
- Перевикористано: `+visibility-count-clue` (з Kuromasu), `+clue-done-mark` (зі Skyscrapers), `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+reflection-visibility` «Видимість залежить від того, чи був промінь відбитий» · game-logic/constraints · 📎 · слот {visible: direct|mirror|always}.
  - `+type-quota` «Загальна кількість кожного виду на полі» · game-logic/constraints · 🌱 — Undead, Star Battle-подібні квоти.

## Пропозиції до словників
- `+cond:view_count` — скільки видно з точки (повтор з Kuromasu/Skyscrapers).
- `+cond:seen_via(direct|mirror)` — сутність на промені до / після відбиття.
- `+cond:type_count` — кількість сутностей виду на полі = N (уточнення `count` для квоти виду; якщо `count` покриває — зняти).
- `+effect:reflect` — промінь змінює напрямок на дзеркалі (`bounce` — для руху сутності, не променя).
- `+ui:count-style-toggle` — лічильник у стилях усього / лишилось / поставлено з усього.
- `+ui:glyph-toggle` — картинки ⇄ літери для сутностей.
- `+ui:clue-done-mark`, `+window:params-dialog` — повтори.
- `+card:reflection-visibility`, `+card:type-quota` — див. мапу.

## Джерела
- ⭐ [Tatham: Undead](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/undead.html) — правила видимості, повтори, керування, A/C, Preferences, David Millar, Steffen Bauer.
- [Undead у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html) — меню й кнопки.
- [janko.at: Spukschloss](https://www.janko.at/Raetsel/Spukschloss/index.htm) — правила, 60 пазлів за розмірами, назви Haunted / Vampire Mirror Maze.
- YouTube: пошук «undead puzzle tatham».

## Непевне
- (?) Як Tatham підсвічує невиконані підказки краю — сірінням лише лічильників видів описано, підказок — ні.
- (?) Чи є підказка на кожній клітинці краю, чи деякі пропущені.
- (?) Назви рівнів складності Undead — сторінка їх не наводить.
- (?) Рік винаходу David Millar — не знайшов.
- (?) Чи дзеркало може стояти в клітинці на краю і як тоді входить промінь.
