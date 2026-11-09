---
title: Sleeper Cells
slug: sleeper-cells
aka: []
family: build-sim
also: [thinky]
klass: puzzle
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: territory
year: 2024
platforms: [web]
links:
  - {kind: itch, url: "https://thesquaregroot.itch.io/sleeper-cells", best: true, note: "правила: зараження, синій через 3 раунди, ≥2 ворожі сусіди перефарбовують, камінь-ножиці-папір, ліміт заражень, стінки; Space/Backspace"}
  - {kind: other, url: "https://itch.io/jam/godot-wild-jam-67/rate/2574690", note: "сторінка Godot Wild Jam #67: опис автора, місця, коментарі (слайдер швидкості, ≥15 рівнів, туторіал)"}
  - {kind: other, url: "https://itch.io/jam/godot-wild-jam-67", note: "джем 8–17 березня 2024, тема Parasite"}
  - {kind: other, url: "https://itch.io/games/tag-cellular-automata", note: "тег itch — родинні ігри-автомати"}
stage: v1
coverage: 60
mechanics: [cell-click, keyboard-controls, controls-remap, move-limit, collect-quota, restart-level, sequential-levels, tutorial-window, background-music, sound-effects, game-loop, +cellular-automaton-rule, +run-simulation, +step-run-speed, +rps-majority-convert, +delayed-infection, +place-block]
proposes: ["+card:rps-majority-convert", "+card:delayed-infection", "+cond:beats(a, b)"]
author: opus
date: 2026-11-09
---

# Sleeper Cells — пазл-автомат «камінь-ножиці-папір»: заражай клітини паразитом і стався стінками, щоб синіх стало досить

## Суть
Джем-прототип на тему «Паразит» (Godot Wild Jam #67): на сітці ростуть і змагаються за місце червоні й зелені клітини, а сині паразити самі рости не вміють. Гравець до запуску обирає, які червоні/зелені клітини **заразити** (вони стануть синіми через 3 раунди), а на частині рівнів ставить **стінки**, що спрямовують ріст. Далі автомат працює сам: клітину, оточену ≥ 2 «сильнішими» сусідами, перефарбовує за циклом камінь-ножиці-папір. Мета — набрати на рівні задану кількість синіх.

## Поле і час
- Квадратна сітка («Gridlock» — рух лише по сітці); розмір поля — (?).
- Шари: клітина поля (порожня / стінка) + жива клітина одного з трьох кольорів + стан «заражена, відлік раундів».
- Два режими: планування (статика: кліки по клітинах і кнопках) → симуляція раунд за раундом (`time: programmed`); темп — слайдер швидкості.
- Гра детермінована: та сама розстановка дає той самий результат (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червона клітина (без прикрас) | tile | колір | росте сама; бʼє зелену; програє синій |
| Зелена клітина (з вусами) | tile | колір | росте сама; бʼє синю; програє червоній |
| Синя клітина-паразит (зі злими бровами) | tile | колір | сама не росте; бʼє червону; програє зеленій |
| Заражена клітина | tile | лічильник 3 раунди | червона/зелена, яку обрав гравець; через 3 раунди стає синьою |
| Стінка | static | — | ставить гравець (на деяких рівнях); клітини крізь неї не ростуть |
| Порожня клітинка | terrain | — | місце для росту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` у плануванні → ЯКЩО `cell(cell, red|green)` and `counter(infections_left, >, 0)` → ТО `set_state(cell, infected, 3)`, `counter(infections_left, -1)`; інакше `block`.
- КОЛИ `input(click, empty_cell)` → ЯКЩО `mode(walls_allowed)` and `counter(walls_left, >, 0)` → ТО `place(player, wall)` (?).
- КОЛИ `input(backspace)` → ТО `custom: «стерти всі введені дії рівня»`.
- КОЛИ `input(space)` → ТО `custom: «запустити симуляцію / скинути рівень до планування»`.
- КОЛИ `tick` (раунд) → ЯКЩО `cell(x, red|green)` → ТО `custom: «росте в сусідні вільні клітинки»` (?) — сині не ростуть.
- КОЛИ `state_off(cell, infected)` (минуло 3 раунди) → ТО `transform(cell, blue)`.
- КОЛИ `tick` → ЯКЩО `adjacent_count(x, beater, >=, 2)` and `custom: «beater бʼє колір x за циклом»` → ТО `transform(x, beater)`.
- Цикл переваги: червоний > зелений > синій > червоний (`+cond:beats`).
- КОЛИ `enter(cell_growth, wall)` → ТО `block`.
- КОЛИ `settled` або `custom: «симуляція закінчилась»` (?) → ЯКЩО `count(blue, >=, target)` → ТО `win`, `next_level`; інакше — Space, переставити й запустити знову.
- Поразки нема; рахунок — кількість синіх проти цілі рівня.

## Керування і ввід
- Ліва кнопка миші — кнопки й клітинки сітки (зараження, стінки).
- Space — старт/скидання рівня; Backspace — стерти всі дії; обидві клавіші перепризначаються в налаштуваннях.
- Слайдер швидкості симуляції; кроку й паузи нема (гравці крутили слайдер до нуля, щоб іти по циклу).

## Вікна, меню, HUD
- `game-screen`: сітка з клітинами-«очима», лічильник заражень (`remaining-counter`), ціль синіх (`objective-text`), `speed-slider`, кнопки дій.
- `tutorial-window` — навчання, додане через складність правил.
- `settings-window` — перепризначення клавіш.
- `end-screen` (?) — анімація очей при проходженні рівня.
- `level-select` — (?).

## Фічі поза полем
- `levels-sequential`: ≥ 15 рівнів із наростанням складності; підказка до рівня 15 — на сторінці гри.
- `restart-level` (Space), `remap-controls`, `tutorial`, фонова музика.
- Нема undo, step-mode, редактора.

## Варіації й родичі
- Родичі в корпусі: [cyclic-cellular-automaton](cyclic-cellular-automaton.md) (циклічна перевага кольорів, поріг сусідів), [game-of-life](game-of-life.md), [cell-machine](cell-machine.md) (розставити до старту, далі автомат), [schelling-segregation](schelling-segregation.md), [brians-brain-seeds](brians-brain-seeds.md); у hidden-deduction — [rock-paper-sweeper](../hidden-deduction/rock-paper-sweeper.md).
- Осі варіацій:
  - **перехід кольору**: наступний по колу за порогом (CCA) / більшість сусідів (виборчі моделі) / RPS + поріг ≥ 2 (Sleeper Cells);
  - **вплив гравця**: лише старт (Life) / обмежені «ходи»-зараження й стінки (Sleeper Cells) / вільне малювання;
  - **затримка**: миттєво / через N раундів (зараження).

## Цікавинки для курсу
- Синхронний автомат з трьома кольорами й циклом переваги за порогом сусідів — 📎.
- Зараження з відкладеним переходом (лічильник раундів у клітині) — 🌱.
- Пазл «обмежений бюджет дій до запуску»: перебір розстановок зараження/стінок, щоб досягти цілі (BFS/перебір + симуляція) — 🥇.
- Детекція нескінченного циклу (гравці ловили вічну боротьбу зелених і синіх) — 🥉.
- Слайдер швидкості з тим самим кроком симуляції — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ зараження й стінки; `keyboard-controls` + `controls-remap` ↔ Space/Backspace; `move-limit` ↔ ліміт заражень; `collect-quota` ↔ ціль синіх; `restart-level` ↔ Space; `sequential-levels` ↔ рівні; `tutorial-window` ↔ навчання; `background-music` + `sound-effects` ↔ «Rain Drops» і звуки; `game-loop` ↔ раунди.
- **Нема** → пропозиції карток:
  - `+rps-majority-convert` «Клітина переходить до кольору, що її бʼє, при ≥ N таких сусідах» · entities/state · 📎 · слоти {threshold: 2, cycle: 3}.
  - `+delayed-infection` «Позначена клітина змінює тип через N тіків» · entities/state · 🌱.
  - `+place-block`, `+run-simulation`, `+cellular-automaton-rule`, `+step-run-speed` — уже в корпусі.

## Пропозиції до словників
- `+card:rps-majority-convert` — циклічна перевага з порогом.
- `+card:delayed-infection` — відкладене перетворення.
- `+cond:beats(a, b)` — A сильніший за B за циклом/таблицею (камінь-ножиці-папір, стихії).

## Джерела
- ⭐ [itch.io: Sleeper Cells](https://thesquaregroot.itch.io/sleeper-cells) — правила (ріст, паразити, зараження → синій через 3 раунди, ≥ 2 ворожі сусіди, RPS-ієрархія), ліміт заражень, стінки, ціль синіх, керування, автори й асети, джем і вайлдкарди.
- [Godot Wild Jam #67: сторінка оцінювання](https://itch.io/jam/godot-wild-jam-67/rate/2574690) — опис «cellular automata inspired puzzle game with rock-paper-scissors mechanics», місця, коментарі (слайдер швидкості, ≥ 15 рівнів, туторіал, вічний цикл).
- [Godot Wild Jam #67](https://itch.io/jam/godot-wild-jam-67) — дати джему (березень 2024).

## Непевне
- (?) Як саме ростуть червоні й зелені (у вільні сусідні клітинки 4- чи 8-сусідства, за який час) — на сторінці лише «grow and compete».
- (?) Сусідство для правила «≥ 2 ворожі»: 4 чи 8.
- (?) Розмір сітки, кількість рівнів (≥ 15), чи стінки обмежені лічильником, коли закінчується симуляція й рахується ціль.
- (?) Порядок оновлення (синхронний чи послідовний) і детермінованість.
