---
title: Globesweeper
slug: globesweeper
aka: [«Сапер на глобусі»]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: graph
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2019
platforms: [PC (Windows, macOS, Linux / Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/982220/", best: true, note: "опис: гекс/квадрат/трикутник на сфері, 6/8/12 сусідів, 5 розмірів (92–20 480 клітин), 4 складності, гарантовано розвʼязний режим, 120 таблиць, 14 тем"}
  - {kind: steam, url: "https://store.steampowered.com/app/1121530/", note: "Globesweeper: Hex Puzzler (2019) — порожнисті глобуси, 8 нових типів підказок, 92 рівні без вгадувань"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Globesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, neighbor-count-clue, no-guess-generation, difficulty-levels, field-size-picker, game-settings, completion-detection, leaderboard, profile-stats, achievements-window, theme-select, save-progress, game-screen, end-screen, +flood-reveal, +spherical-grid, +corner-neighborhood, +camera-orbit, +achievement-unlocks-theme]
proposes: ["+axis:field=sphere", "+ui:globe-rotate", "+effect:flood_reveal", "+card:spherical-grid", "+card:corner-neighborhood", "+card:camera-orbit", "+card:achievement-unlocks-theme"]
author: opus
date: 2026-11-09
---

# Globesweeper — сапер на поверхні кулі: поле без країв із гексів, квадратів або трикутників

## Суть
Класичний Minesweeper, перенесений на сферу: гравець обертає глобус і відкриває клітини, число показує кількість мін, що торкаються клітини. Країв і кутів нема — кожна клітина має повний набір сусідів, тож зникають «легкі» кутові дедукції площини. Три сітки (гекс, квадрат, трикутник) дають 6, 8 або 12 сусідів — та сама логіка з різною «густиною» підказки. Відкрив міну — вибухає весь глобус.

## Поле і час
- Поле — поверхня сфери, розбита на клітини одного з трьох типів; сусіди — клітини, що мають спільний кут: 6 (гекс), 8 (квадрат), 12 (трикутник).
- 5 розмірів глобуса: від крихітного гексового на 92 клітини до трикутного на 20 480.
- Топологія — граф без межі; камера обертає кулю, видно лише передню півсферу.
- Час статичний: нічого не відбувається без кліку; таймер (?) — міра результату для таблиць.
- Геометрія (виведено, не з джерела): 92 = 10·9 + 2 — грань поліедра Голдберга, де неминуче є 12 пʼятикутників з 5 сусідами; 20 480 = 20·4⁵ — ікосфера після 5 поділів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | форма: hex / square / triangle | приймає відкриття або прапорець |
| Число | mark | n = міни серед сусідів по куту | підказка; 0 → каскад відкриття (?) |
| Міна | hazard | — | відкриття → вибух глобуса, програш |
| Прапорець | mark | — | позначка міни, захищає від кліку (?) |
| Глобус | zone | розмір 1–5, тип сітки | обертається камерою; тема-скін (Земля, Місяць, Марс, самоцвіти) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `explode(globe)`, `lose`.
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` зі значенням `adjacent_count(c, mine)`; сусідство — спільний кут (6 / 8 / 12).
- КОЛИ `after(reveal(c))` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `custom: «відкрити всіх сусідів рекурсивно (flood reveal)»` (?).
- КОЛИ `input(flag, c)` → ЯКЩО `cell(c, closed)` → ТО `mark(c, flag)`.
- КОЛИ `level_start` → ЯКЩО `mode(guaranteed_solvable)` → ТО `custom: «генерувати розкладку, розвʼязну без вгадувань»`.
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `win`, `custom: «час у таблицю для (сітка, розмір, складність)»`.
- КОЛИ `custom: «виконано досягнення»` → ТО `unlock(theme)`.
- Перемога: усі безпечні клітини відкриті. · Поразка: відкрита міна. · Рахунок: час (?) у 120 таблицях лідерів.

## Керування і ввід
- Миша: клік — відкрити, інша кнопка — прапорець (?); перетягування — обертання глобуса, колесо — зум (?).
- Акорд по числу — не згадано в описі (?).

## Вікна, меню, HUD
- `main-menu` (?): вибір сітки (hex / classic / triangle), розміру (5), складності (4), режиму (traditional / guaranteed solvable).
- `game-screen`: глобус у центрі, обертання; `remaining-counter` і `timer-elapsed` (?).
- `end-screen`: вибух глобуса або перемога з часом.
- `leaderboard`: 120 глобальних таблиць (комбінації сітка × розмір × складність × режим, 3·5·4·2 = 120 — збіг виведено).
- `skin-select`: 14 тем, що відкриваються досягненнями.
- `stats-window` (Steam Stats), `achievements-window`.

## Фічі поза полем
- `difficulty-presets` (4) × розміри (5) × сітки (3).
- `no-guess` — режим «guaranteed solvable».
- `achievements` → `unlockables` (теми глобуса), `leaderboard-online`, `stats`, `cloud-save`.

## Варіації й родичі
- [minesweeper](minesweeper.md) — площинний оригінал (8 сусідів, межа поля); [hexcells](hexcells.md) і [tametsi](tametsi.md) — гекси/графи з ручними задачами; [14-minesweeper-variants](14-minesweeper-variants.md) — модифікатори підказок.
- Globesweeper: Hex Puzzler (2019) — порожнисті глобуси з дірками, 8 нових підказок (Cluster — скільки реактивних клітин звʼязано з числом; Area — у ширшій зоні; Group — кількість окремих груп), 92 рівні без вгадувань.
- Осі варіацій: **топологія** — площина / тор (Tatham) / сфера / порожниста сфера; **сітка** — квадрат / гекс / трикутник; **сусідство** — по ребру / по куту; **генерація** — випадкова / no-guess / ручна.

## Цікавинки для курсу
- Сітка на сфері як граф сусідства (поліедр Голдберга або ікосфера) — 🥈: побудова клітин і списків сусідів, 12 «дефектних» вершин.
- Сусідство «по куту» для трьох сіток (6 / 8 / 12) як параметр одного двіжка сапера — 📎.
- Обертання глобуса й вибір клітини променем з камери — 🥈 (3D-рендер) або 📎 (проєкція на 2D-карту).
- Generator «guaranteed solvable» на довільному графі — 🥇.
- Теми як нагорода за досягнення — 🌱.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` ↔ число по кутових сусідах · `no-guess-generation` ↔ guaranteed solvable · `difficulty-levels` + `field-size-picker` + `game-settings` ↔ складність/розмір/сітка · `completion-detection` · `leaderboard` ↔ 120 таблиць · `profile-stats` ↔ Steam Stats · `achievements-window` · `theme-select` ↔ 14 тем · `save-progress` ↔ Steam Cloud · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+spherical-grid` «Сітка на поверхні сфери» · levels/generation · 🥈 · слоти {cell: hex|square|triangle, size}.
  - `+corner-neighborhood` «Сусідство по куту для довільної сітки» · game-logic/constraints · 📎.
  - `+camera-orbit` «Обертання 3D-поля камерою» · interface/render · 🥈.
  - `+achievement-unlocks-theme` «Досягнення відкривають скіни» · interface/settings · 🌱.
  - `+flood-reveal` — повтор пропозиції з [minesweeper](minesweeper.md).

## Пропозиції до словників
- `+axis:field=sphere` — поле на сфері: граф без межі з геометрією (ширше за `graph`, вужче за `3d`).
- `+ui:globe-rotate` — контрол обертання/зуму 3D-поля.
- `+effect:flood_reveal` — рекурсивне відкриття (повтор з minesweeper, для правила трьох).

## Джерела
- ⭐ [Steam: Globesweeper](https://store.steampowered.com/app/982220/) — сітки й кількість сусідів, 5 розмірів (92–20 480), 4 складності, traditional / guaranteed solvable, 120 таблиць, 14 тем за досягнення, Incandescent Games, 12.02.2019.
- [Steam: Globesweeper: Hex Puzzler](https://store.steampowered.com/app/1121530/) — порожнисті глобуси, Cluster / Area / Group, 92 рівні, «never have to guess».
- YouTube: пошук «Globesweeper gameplay».

## Непевне
- (?) Каскад нулів, прапорці, акорд, таймер і безпечний перший клік — опис Steam їх не згадує (прапорці — лише в цитаті з відгуку).
- (?) Керування мишею (обертання, зум) — не перевірено.
- (?) Чи гексова сфера має 12 пʼятикутників, а трикутна — вершини з 5 трикутниками (тоді в частини клітин сусідів менше за 12) — геометричний висновок, не з джерела.
- (?) Розкладка 120 таблиць як 3×5×4×2 — арифметичний збіг, не підтверджено.
