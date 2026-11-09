---
title: Patterna
slug: patterna
aka: []
family: hidden-deduction
also: [pencil-logic]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2016
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/503860/", best: true, note: "опис: граф вузлів, pattern / non-pattern, підказки відстані, звʼязності й кольору; генератор, редактор, 70+ рівнів"}
  - {kind: other, url: "https://steamcommunity.com/app/503860/reviews/?browsefilter=toprated", note: "огляди гравців — найповніший розбір підказок: кільця, {}, -n-, стрілки, кольори, hardcore"}
  - {kind: other, url: "https://steamcommunity.com/app/503860/guides/", note: "гайди розробника: редактор рівнів, Workshop, власні генератори графів"}
  - {kind: other, url: "https://steamcommunity.com/id/lonelyfirewolf/recommended/503860/", note: "огляд (cz): попередження за вгадування, hardcore-режим"}
  - {kind: other, url: "https://thinkygames.com/games/patterna/", note: "картка Thinky Games (403 для WebFetch)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Patterna+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, satisfy-constraints, completion-detection, neighbor-count-clue, connectivity-check, no-guess-generation, level-bank, sequential-levels, tutorial-window, in-game-editor, level-exchange, game-settings, hover-highlight, highlights, remaining-counter, wrong-mark-lose, achievements-window, game-screen, background-music, +graph-adjacency, +clue-radius-rings, +contiguity-clue, +directed-edges, +color-group-count, +guess-detection, +mistake-counter, +tentative-mark, +custom-graph-generator]
proposes: ["+cond:count_within", "+cond:deducible", "+cond:contiguous", "+effect:warn", "+role:edge", "+ui:color-group-counters", "+ui:range-rings", "+feature:guess-warning", "+feature:generator-options", "+card:clue-radius-rings", "+card:directed-edges", "+card:guess-detection", "+card:tentative-mark", "+card:custom-graph-generator"]
author: opus
date: 2026-11-09
---

# Patterna — Hexcells на довільному графі: віднеси кожен вузол до візерунка або ні за підказками відстані, звʼязності й кольору

## Суть
Рівень — мережа вузлів, зʼєднаних ребрами; кожен вузол або належить прихованому візерунку (pattern), або ні. Гравець по одному класифікує закриті вузли; правильна відповідь відкриває нові числа. Ідея Hexcells узагальнена: замість гекс-сусідства — довільний граф, радіус підказки задається кільцями, ребра бувають однонапрямні, а вузли — кольорові групи з власними лічильниками. Гра стежить, чи хід випливав із логіки: за вгадування спершу попереджає, потім рахує помилку.

## Поле і час
- Поле — граф (`field: graph`): вузли довільно розкладені на площині, сусідство = ребро; відстань = кількість ребер.
- Ребра двох видів: звичайні й зі стрілкою (інформація йде лише в один бік).
- Шари: прихований стан вузла (pattern / non-pattern) + відкрите число з модифікаторами (кільця, `{}`, `-n-`, колір) + колір вузла.
- Статичний пазл без таймера; поза полем — загальний лічильник і лічильники кольорів (лівий нижній кут).
- Рівні — ручні (70+ з туторіалом), згенеровані генератором з параметрами або з Workshop.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закритий вузол | static | прихований стан, колір | класифікується гравцем як pattern / non-pattern |
| Вузол pattern | mark | число (необовʼязково) | число = скільки pattern-вузлів зʼєднано з ним ланцюжком (?) |
| Вузол non-pattern з числом | mark | n, радіус 1–3 (кільця) | n = кількість pattern-вузлів у межах радіуса |
| Вузол non-pattern без числа | mark | — | інформації не дає |
| Кільця навколо числа | mark | 1 / 2 / 3 | радіус підказки в ребрах |
| Дужки `{n}` | mark | — | усі pattern у зоні підказки утворюють одну звʼязну групу |
| Тире `-n-` | mark | — | pattern у зоні **не** звʼязні: є хоча б один розрив |
| Звичайне ребро | static | — | сусідство в обидва боки |
| Ребро-стрілка | static | напрям | підказка рахує / звʼязність іде лише за стрілкою |
| Колір вузла | zone | 1 з 4 кольорів | група з окремим лічильником |
| Кольорове число | mark | колір | відкривається на non-pattern; рахує лише вузли свого кольору (?) |
| Загальний лічильник | zone | неозначено / з них pattern | два числа: скільки вузлів ще не класифіковано і скільки серед них pattern |
| Лічильник кольору | zone | ті самі два числа | те саме в межах кольору |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(mark_pattern, n)` → ЯКЩО `custom: «вузол справді pattern»` → ТО `reveal(n)` з числом, `counter(unknown, -1)`, `counter(pattern_left, -1)`.
- КОЛИ `input(mark_non_pattern, n)` → ЯКЩО `custom: «вузол справді non-pattern»` → ТО `reveal(n)` з числом / кольоровим числом / порожньо, `counter(unknown, -1)`.
- КОЛИ `input(mark_*, n)` → ЯКЩО `not custom: «відповідь правильна»` → ТО `counter(mistakes, +1)`, вузол лишається закритим (?).
- КОЛИ `input(mark_*, n)` → ЯКЩО `custom: «стан вузла ще не виводиться з відкритого»` and `first_time` → ТО `message(«це вгадування»)` (попередження); повторно → `counter(mistakes, +1)`.
- Число non-pattern з k кільцями: `custom: «кількість pattern у радіусі k ребер = n»`; одне кільце = прямі сусіди, тобто `adjacent_count(n, pattern, ==, n)`.
- Число на pattern-вузлі: `custom: «довжина/розмір звʼязного ланцюжка pattern, до якого належить вузол»` (?).
- `{n}`: ЯКЩО `connected(pattern у зоні підказки)` — обмеження виконано; `-n-`: ЯКЩО `not connected(…)`.
- Ребро-стрілка: `custom: «підказка і звʼязність не проходять проти стрілки»`.
- Кольорове число: `custom: «кількість pattern свого кольору в зоні»` (?).
- Лічильник кольору: `custom: «у групі кольору лишилось a неозначених, з них b pattern»` — глобальне обмеження на групу.
- КОЛИ `input(highlight, n)` → ТО `custom: «підсвітити всі вузли, на які впливає підказка»` (до 4 підсвіток разом).
- КОЛИ `input(tentative, n)` → ТО `mark(n, pattern?|non-pattern?)` — попередня позначка без перевірки (додано оновленням).
- КОЛИ `counter(unknown, ==, 0)` → ТО `win`, `window(end-screen)`.
- КОЛИ `counter(mistakes, >=, 1)` → ЯКЩО `mode(hardcore)` → ТО `lose` (рівень завершується).
- Перемога: класифіковано всі вузли. · Поразка: лише в hardcore — перша помилка. · Рахунок: помилки (для досягнень і позначки «ідеально» (?)).
- Гарантія дизайну: кожен рівень розвʼязний без вгадувань.

## Керування і ввід
- Мишею: клік по закритому вузлу — дві дії «pattern» / «non-pattern» (яка кнопка яка — (?)).
- Клік по відкритому числу — підсвітка зони впливу; до 4 зон одночасно (огляд гравця).
- Попередня позначка вузла (з оновлення) — нотатка без перевірки.
- Вузли, які ще не можна підтвердити, гравці описують позначкою «???» (?).

## Вікна, меню, HUD
- `game-screen`: граф, числа з кільцями й дужками, стрілки на ребрах, загальний лічильник і до 4 лічильників кольорів (лівий нижній кут).
- `main-menu` → рівні (`puzzle-select` 70+ з туторіалом), генератор, редактор, Workshop (?).
- `tutorial-window` — навчальні рівні, що вводять типи підказок по одному.
- `settings-window` генератора — «багато опцій» перед генерацією (`+feature:generator-options`).
- `editor-window` — редактор рівнів (гайд розробника «Building Levels for Patterna»).
- `end-screen` рівня — помилки (?).
- HUD: `remaining-counter` (неозначені / pattern), `+ui:color-group-counters`, `hover-highlight`/підсвітка зони, `+ui:range-rings` (кільця радіуса на числі), `mistake-counter` (?).
- Переходи: main-menu → puzzle-select | generator → game-screen → end-screen.

## Фічі поза полем
- `puzzle-bank`: 70+ ручних рівнів + туторіал.
- Генератор випадкових рівнів з налаштуваннями; власні генератори графів (гайд «How to create custom graph-generators»).
- `level-editor` + `level-sharing` через Steam Workshop (гайди «Uploading Puzzles to the Workshop»).
- `mode-hardcore`: одна помилка — рівень програно.
- `+feature:guess-warning`: гра визначає, чи хід був виводимим, і карає за вгадування.
- `achievements` (є приховані), `cloud-save`, `stats`; `localization` (EN, DE, RU, zh-Hans, zh-Hant); саундтрек Alex Cottrell (окремо безкоштовно).

## Варіації й родичі
- Прямий предок — [hexcells](hexcells.md): та сама пара «так/ні», `{n}` / `-n-`, підказки радіуса 2 («квітка»).
- Родичі на графах: [tametsi](tametsi.md) (довільні графи, кольорові групи з лічильником), [globesweeper](globesweeper.md) (сфера).
- Класика: [minesweeper](minesweeper.md); гібриди з нонограмою — [polimines](polimines.md), [lizzi-crossing](lizzi-crossing.md).
- Осі варіацій: **сусідство** решітка / гекс / довільний граф / орграф; **радіус** 1 / 2 / 3 ребра; **тип підказки** кількість / кількість+звʼязність / колір / глобальний лічильник групи; **помилка** лічильник / смерть (hardcore) / попередження за вгадування; **джерело рівнів** ручні / генератор / Workshop.

## Цікавинки для курсу
- Поле як граф: список суміжності, відстань BFS, підказка «у радіусі k ребер» — 🥉.
- Орієнтовані ребра: та сама підказка, але BFS лише за стрілками — 📎 (одна зміна в обході, великий вплив на логіку).
- Перевірка `{n}` / `-n-` — звʼязність підмножини вузлів у підграфі — 📎.
- Детектор вгадування: перед прийняттям ходу перевірити, чи стан вузла однозначно виводиться з відкритих підказок (SAT/перебір на межі) — 🥇.
- Генератор з налаштуваннями + перевірка «без вгадувань» солвером — 👑.
- Лічильники кольорових груп як глобальні обмеження — 🌱.

## Мапа на каталог
- Є: `cell-click` · `satisfy-constraints` · `completion-detection` · `neighbor-count-clue` ↔ число з одним кільцем · `connectivity-check` ↔ `{n}` / `-n-` · `no-guess-generation` ↔ генератор · `level-bank` + `sequential-levels` + `tutorial-window` · `in-game-editor` + `level-exchange` ↔ редактор і Workshop · `game-settings` ↔ опції генератора · `hover-highlight` + `highlights` ↔ підсвітка зони · `remaining-counter` · `wrong-mark-lose` ↔ hardcore · `achievements-window` · `game-screen` · `background-music`.
- **Нема** → пропозиції карток:
  - `+graph-adjacency` «Поле-граф: сусідство за ребрами» · field · 🥉.
  - `+clue-radius-rings` «Радіус підказки задається на самій підказці (1–3 кільця)» · game-logic/constraints · 📎 · слот {r}.
  - `+directed-edges` «Однонапрямні ребра: підказка рахує лише за стрілкою» · game-logic/constraints · 📎.
  - `+color-group-count` «Лічильник групи кольору: лишилось / з них цілей» · game-logic/constraints · 🌱 (уже пропонував Tametsi).
  - `+guess-detection` «Попередження/помилка, якщо хід не виводиться логікою» · game-logic/lose · 🥇.
  - `+tentative-mark` «Попередня позначка без перевірки» · interface/input · 🌱.
  - `+custom-graph-generator` «Користувацькі генератори форми графа для рандом-рівнів» · levels/generation · 🥈.
  - `+contiguity-clue`, `+mistake-counter` — як у Hexcells.

## Пропозиції до словників
- `+cond:count_within(cell, kind, r, op, n)` — кількість сутностей виду в радіусі r кроків (ребер); `adjacent_count` — окремий випадок r=1.
- `+cond:deducible(cell)` — стан клітини однозначно виводиться з відкритого (детектор вгадування).
- `+cond:contiguous` — цілі в зоні підказки утворюють одну звʼязну групу (Hexcells `{n}`; тут — у межах радіуса).
- `+effect:warn` — попередження без штрафу (перше вгадування).
- `+role:edge` — ребро графа як сутність з властивістю (напрям).
- `+ui:color-group-counters` · `+ui:range-rings` — кільця радіуса навколо числа.
- `+feature:guess-warning` · `+feature:generator-options` — параметри рандом-генератора перед стартом.

## Джерела
- ⭐ [Steam: Patterna](https://store.steampowered.com/app/503860/) — граф, pattern/non-pattern, «distance, connectivity, and color» підказки, «absolutely no guessing», 70+ рівнів, генератор з опціями, редактор, Workshop; kerntief, 03.10.2016.
- [Steam-огляди (top rated)](https://steamcommunity.com/app/503860/reviews/?browsefilter=toprated) — кільця радіуса, `{}`/`-n-`, стрілки, 4 кольори з лічильниками, підсвітка до 4 зон, попередня позначка, hardcore.
- [Steam-гайди](https://steamcommunity.com/app/503860/guides/) — назви гайдів розробника: редактор, Workshop, власні генератори графів (самі гайди віддали 429).
- [Огляд lonelyfirewolf](https://steamcommunity.com/id/lonelyfirewolf/recommended/503860/) — попередження за вгадування → помилка, hardcore.
- YouTube: пошук «Patterna puzzle gameplay».

## Непевне
- (?) Точний зміст числа на pattern-вузлі («how many pattern nodes are connected in sequence») — розмір групи чи довжина ланцюжка в радіусі.
- (?) Що саме рахує кольорове число на non-pattern-вузлі.
- (?) Які кнопки миші відповідають pattern / non-pattern; чи помилкова відповідь лишає вузол закритим (як у Hexcells).
- (?) Параметри генератора (кількість вузлів, щільність, типи підказок) — «багато опцій», конкретику не бачив; гайди Steam віддали 429.
- (?) Позначка «???» — з огляду гравця, що вона означає в інтерфейсі, не перевірено.
- (?) Чи є `end-screen` з помилками й позначка «ідеально».
