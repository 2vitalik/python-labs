---
title: PANIK
slug: panik
aka: [Panik]
family: thinky
also: [chess-abstract]
klass: figure
axes:
  field: iso
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2749610/PANIK/", best: true, note: "опис, теги (Grid-Based Movement, Isometric, Chess), 170+ рівнів, 9 світів, 15 панікерів; реліз 29.09.2025"}
  - {kind: other, url: "https://steamcommunity.com/app/2749610/reviews/?browsefilter=toprated", note: "відгуки: король, ходи лише поруч із ним, ліміт ходів кожного, цілі, структура глав"}
  - {kind: itch, url: "https://chumasgames.itch.io/panik", note: "демо (Windows): 35 рівнів, доступність, девлоги 2023–2025"}
  - {kind: itch, url: "https://chumasgames.itch.io/panik-jamversion", note: "джем-версія (Spain Game Devs Jam III): лідери й не-лідери, поразка — усі в паніці або скінчились ходи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=PANIK+ChumasGames+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, selection-highlight, legal-move-highlight, hover-highlight, piece-move-patterns, move-limit, teleport, destructible-blocks, level-unlock, tutorial-window, undo-redo, save-autosave, achievements-window, +leader-adjacency-move, +panic-state, +per-unit-move-budget, +occupy-all-goals, +clone-unit, +flying-unit, +open-level-pool]
proposes: ["+role:leader", "+ui:unit-move-badge", "+feature:open-level-pool", "+axis:actors", "+card:leader-adjacency-move", "+card:per-unit-move-budget"]
author: opus
date: 2026-11-09
---

# PANIK — переляканих панікерів веде король: хто стоїть поруч із ним, заспокоюється й може зробити свій хід до цілі

## Суть
Покрокова пазл-гра ChumasGames (Xavi Morales) на ізометричній сітці. Панікери налякані й самі не рухаються: ходити може лише той, хто стоїть поруч із **королем** (персонаж у короні); король ходить завжди. У кожного персонажа — свій патерн ходу, своя здібність і **власний ліміт ходів**. Мета — зайняти панікерами всі цільові клітини. Нові панікери вводяться парами по главах: літають, телепортуються, розмножуються, руйнують клітини поля.

## Поле і час
- Квадратна сітка клітин, показана ізометрично; цільові клітини позначено.
- Хід = клік по персонажу й клік по клітині; світ покроковий, без таймерів («Playable without Timed Input»).
- Частина клітин може зникати (здібність «руйнує простір рівня»); розміри полів — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король (корона) | piece | ліміт ходів | ходить завжди; сусідні панікери стають спокійними й можуть ходити |
| Панікер | piece | патерн ходу, ліміт ходів, стан PANIK / спокій | вибирається й ходить лише поруч із королем; у паніці — не клікається |
| Панікер-виняток | piece | — | один вид ходить без короля (за відгуком «all but one»), який саме — (?) |
| Літун | piece | — | «can fly» — переліт (через що саме — (?)) |
| Телепортер | piece | — | «teleport» — переносить себе (куди — (?)) |
| Розмножувач | piece | — | «multiply» — створює копії |
| Руйнівник | piece | — | «destroy the level space» — прибирає клітини поля |
| Фокусник, робот, ніндзя | piece | — | названі в описі Steam; здібності не описано (?) |
| Цільова клітина | zone | — | кожна має бути зайнята панікером |
| Клітина поля | terrain | — | по ній ходять; може бути зруйнована |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, paniker)` → ЯКЩО `not state(paniker, panik)` → ТО `custom: «вибрати й підсвітити клітини, куди може піти»`.
- КОЛИ `input(click, paniker)` → ЯКЩО `state(paniker, panik)` → ТО `block`.
- КОЛИ `input(click, cell)` → ЯКЩО `legal(moveset_of_paniker)` і `counter(moves_left, >, 0)` → ТО `move(paniker, cell)`, `counter(moves_left, -1)`.
- КОЛИ `turn_end(player)` → ЯКЩО `adjacent_count(paniker, king, =, 0)` і `custom: «не виняток»` → ТО `set_state(paniker, panik)`; інакше `clear_state(paniker, panik)`.
- КОЛИ `input(click, king)` → ЯКЩО `counter(moves_left, >, 0)` → ТО `custom: «король вибирається завжди»`.
- КОЛИ `input(click, cell)` → ЯКЩО `state(selected, teleporter)` → ТО `teleport(paniker, cell)` (?).
- КОЛИ `input(click, cell)` → ЯКЩО `state(selected, multiplier)` → ТО `clone(paniker)` (?).
- КОЛИ `input(click, cell)` → ЯКЩО `state(selected, destroyer)` → ТО `set_cell(cell, void)` (?).
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «на кожній цільовій клітині стоїть панікер»` → ТО `win`, `next_level`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «усі в паніці»` або `counter(moves_left_all, =, 0)` → ТО `lose` (так у джем-версії).
- КОЛИ `input(undo)` → ТО `undo(1)`; після рестарту історія undo порожня.
- Перемога: зайняті всі цілі. · Поразка: вичерпано ходи / усі в паніці (джем-версія). · Рахунку нема.

## Керування і ввід
- Миша: клік по спокійному персонажу → підсвітка досяжних клітин → клік по клітині. Наведення показує «бульбашку» з рештою ходів персонажа; є опція «показувати завжди».
- Джем-версія: лівий клік — вибір клітини, R — рестарт.
- Клавіатура — лише в меню вибору рівнів (за відгуком); Steam заявляє повну підтримку геймпада (?).

## Вікна, меню, HUD
- `game-screen`: ізометричне поле, цілі, персонажі; HUD — `+ui:unit-move-badge` (бульбашка з ходами над персонажем), `legal-move-highlight` після вибору.
- `chapter-select` (?): 8–9 глав-світів; кожна відкривається, коли розвʼязано досить рівнів попередньої.
- `level-select` у главі: туторіальні рівні нових панікерів, далі пул відкритих рівнів.
- `settings-window`: показ лічильників ходів; у демо — палітра для дальтоніків, контраст, субтитри.
- `achievements-window` (Steam), секрети.

## Фічі поза полем
- `+feature:open-level-pool` — після туторіалів відкрито 5 з 13 рівнів глави в будь-якому порядку; кожен розвʼязаний відкриває ще один; досить розвʼязаних — нова глава. Так можна «пропускати» важкі рівні.
- `tutorial` — по рівню-навчанню на кожного нового панікера (двоє на главу); остання глава поєднує всіх.
- `undo` (не через рестарт), `autosave`; рестарт — за одним відгуком, лише вийти й зайти в рівень.
- `colorblind-palette`, `high-contrast`, субтитри; `localization` EN / ES / CA; `achievements`.

## Варіації й родичі
- Джем-версія (Spain Game Devs Jam III) → веб-версія (2023) → демо (2025, 35 рівнів) → повна гра (29.09.2025).
- Родичі: шахові патерни ходу ([Chess with Different Armies](../chess-abstract/chess-with-different-armies.md)), покрокові пазли з лімітом ходів ([Hitman GO](../push-slide/hitman-go.md), [Helltaker](../push-slide/helltaker.md)).
- **Осі варіацій:** хто може ходити (усі / лише поруч із лідером / ланцюжком від лідера) · ліміт ходів (спільний / на кожного) · мета (дійти до виходу / зайняти всі цілі).

## Цікавинки для курсу
- Стан «паніка» за сусідством із королем, перерахунок після кожного ходу — 🌱.
- Окремий лічильник ходів на кожну фігуру + бульбашка на hover — 🌱.
- Фігури з різними патернами ходу й підсвіткою досяжних клітин — 📎.
- Розмноження й руйнування клітин як ходи (зміна складу фігур і поля) — 📎.
- Розвʼязувач BFS: стан = позиції + ходи кожного + поле; ліміти ходів тримають простір малим — 🥉.
- Пул відкритих рівнів («5 з 13, кожен відкриває ще один») — 🌱.

## Мапа на каталог
- Є: `cell-click`, `selection-highlight`, `legal-move-highlight`, `hover-highlight` ↔ вибір і підказки; `piece-move-patterns` ↔ свої мувсети; `move-limit` ↔ ходи кожного; `teleport`; `destructible-blocks` ↔ руйнування клітин; `level-unlock`, `tutorial-window`, `undo-redo`, `save-autosave`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+leader-adjacency-move` «Фігура ходить лише поруч із лідером» · entities/legality · 🌱 · слоти {range: adjacent|chain, exceptions}.
  - `+panic-state` «Стан, що блокує вибір фігури» · entities/state · 🌱.
  - `+per-unit-move-budget` «Ліміт ходів у кожної фігури» · entities/legality · 🌱.
  - `+occupy-all-goals` «Кожна ціль зайнята будь-якою фігурою» · game-logic/win · 🌱.
  - `+clone-unit`, `+flying-unit` — здібності · entities · 📎.
  - `+open-level-pool` — див. «Фічі поза полем».

## Пропозиції до словників
- `+role:leader` — фігура, що дає право ходу іншим (повтор).
- `+ui:unit-move-badge` — бульбашка над фігурою з рештою її ходів.
- `+feature:open-level-pool` — N відкритих рівнів, кожен розвʼязаний відкриває наступний.
- `+axis:actors` — `party` (повтор): кілька підконтрольних фігур.
- `+card:leader-adjacency-move`, `+card:per-unit-move-budget` — див. вище.

## Джерела
- ⭐ [Steam: PANIK](https://store.steampowered.com/app/2749610/PANIK/) — «The panikers are scared and can't move!», 170+ рівнів, 9 світів, «15 panikers… (Or maybe it's 16?)», корона / фокусник / робот / ніндзя, теги, нагороди (фіналіст Spain Game Devs Jam III, Best Puzzle Game Guadalindie 2024), мови.
- [Steam-відгуки](https://steamcommunity.com/app/2749610/reviews/?browsefilter=toprated) — король «can always move and makes others move… if standing next to them», «all but one», ліміт ходів і бульбашка, «fly, teleport, multiply, destroy the level space», цілі, 5 з 13 рівнів, undo не після рестарту, лише миша.
- [itch: демо](https://chumasgames.itch.io/panik) — 35 рівнів, доступність, дати девлогів, рівень «Chess 2» у коментарі.
- [itch: джем-версія](https://chumasgames.itch.io/panik-jamversion) — лідери / не-лідери, «can't move if they are not close to a leader», поразка, лівий клік, R.

## Непевне
- (?) Чи «поруч із королем» передається ланцюжком (відгук каже «connected»), чи лише пряме сусідство (інший відгук — «next to»); і чи сусідство 4- чи 8-клітинне.
- (?) Конкретні патерни ходу й здібності 14–16 панікерів, їхні імена — не знайдено.
- (?) Кількість рівнів/світів розходиться: Steam — 170+ / 9, демо-сторінка — 100+ / 8, відгуки — 150–210.
- (?) Undo і рестарт: один відгук (ES) каже, що нема ні undo, ні reset, інший — undo є; можливо, різні версії.
- (?) `also: chess-abstract` — за тегом Steam «Chess» і рівнем «Chess 2»; чи є справжні шахові фігури — не перевірено.
