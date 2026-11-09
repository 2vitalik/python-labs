---
title: Kine
slug: kine
aka: []
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [PC, Xbox One, PS4, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/824570/Kine/", best: true, note: "Steam (2020): 120+ пазлів, три роботи-інструменти, демо"}
  - {kind: other, url: "https://www.videogamer.com/reviews/kine-review", note: "огляд: рухи Quat/Roo/Euler, мета — аркуш нот, undo, платформи, дата 2019"}
  - {kind: other, url: "https://gametyrant.com/news/kine-review-puzzling-instruments-that-make-your-head-spin", note: "огляд: орієнтація змінює рухи, взаємодія інструментів, undo по кроку і ресет"}
  - {kind: other, url: "https://www.geekyhobbies.com/?p=20381", note: "огляд: перекочування «як кубик», колізії виступів, ~22 стадії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kine+gwen+frey+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, multi-cell-size, orientation-state, party-switch, impassable-cells, reach-exit, undo-redo, undo-step, restart-level, sequential-levels, level-unlock, level-select, movement-animation, background-music, height-levels, +roll-block, +extend-retract-body, +rotate-view-to-solve, +lift-other-avatar, +shape-shifting-body, +optional-side-levels]
proposes: ["+effect:extend(a, part, n)", "+effect:retract(a, part)", "+cond:part_clear(a, part, dir)", "+cond:orientation(a, o)", "+trigger:collected(a, goal)", "+role:multi-body", "+card:extend-retract-body", "+card:lift-other-avatar", "+axis:actors=party"]
author: opus
date: 2026-11-09
---

# Kine — три роботи-інструменти перекочуються 3D-сіткою, як кубики, і висувають частини тіла, щоб дістатись до нот

## Суть
Гравець по черзі керує трьома механічними музикантами: барабаном Quat, акордеоном Roo і тромбоном Euler. Кожен робить крок, **перекочуючись на сусідню клітину, як кубик** (міняється верхня грань), а ще має власний механізм: Quat висуває штангу з тарілкою, Roo розтягує міх, Euler рухає дві куліси незалежно. Що саме робить механізм, залежить від **орієнтації тіла** — те саме висування підносить, відштовхує або тримає над перешкодою. Мета — довести інструмент до цільової клітини з аркушем нот; пізні рівні потребують співпраці двох-трьох роботів.

## Поле і час
- 3D-сітка з ящиків, стільців, шаф, що виринають і складаються; камера обертається, гравець обирає зручний кут; часом перспектива повертається на 90°.
- Покрокова: кожна дія (перекочування, висування, втягування) — один хід; нема таймерів і ворогів.
- Колізії: виступи тіла не проходять крізь підлогу й перешкоди — такий хід заборонено.
- Гравітація (?): висування дає піднятись або перетнути проліт — отже, без опори тіло падає (не перевірено).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Quat (барабан) | player | орієнтація, штанга з тарілкою з одного боку | перекочується в 4 боки; ковзає вздовж штанги — відштовхується вгору або вбік залежно від орієнтації |
| Roo (акордеон) | player | 2 стани: стиснута / розтягнута; кінцівки | міх розтягується на кілька клітин: штовхає себе, підносить у повітря, підсовує чи підіймає інших; на боці — підноситься над прольотом |
| Euler (тромбон) | player | Г-подібне тіло, 2 куліси | кожна куліса висувається незалежно; відштовхує від барʼєру або тримає над перешкодою; перекочується, якщо куліси нікуди не впираються |
| Блок / меблі (ящик, стілець, шафа) | static | висота | опора й перешкода; частина виринає/складається (?) |
| Аркуш нот (ціль) | static | — | інструмент дістався → рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` і `custom: «виступи тіла не впираються після повороту»` → ТО `roll(active, dir)`; інакше `block`.
- КОЛИ `input(extend)` → ЯКЩО `custom: «простір для виступу вільний»` → ТО `custom: «механізм висувається; тіло зсувається від опори»` (пропозиція `extend`).
- КОЛИ `input(extend)` → ЯКЩО `facing(active, down)` → ТО `move(active, up)` — підносить себе.
- КОЛИ `input(extend)` → ЯКЩО `facing(active, side)` і `blocked(active)` → ТО `move(active, away)` — відштовхується від стіни.
- КОЛИ `input(extend, roo)` → ЯКЩО `occupied(cell_ahead, instrument)` → ТО `push(instrument)` або `custom: «підняти інший інструмент»`.
- КОЛИ `input(retract)` → ТО `custom: «механізм втягується»` (пропозиція `retract`).
- КОЛИ `input(slide, euler, slide_n)` → ТО `custom: «одна куліса висувається / втягується незалежно від другої»`.
- КОЛИ `input(switch)` → ТО `custom: «активний інструмент змінюється»` (`party-switch`).
- КОЛИ `tick` → ЯКЩО `not supported(active)` → ТО `fall(active)` (?).
- КОЛИ `reach(instrument, sheet_music)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`; КОЛИ `input(reset)` → ТО `restart`.
- Перемога: інструмент на цілі · Поразки нема — лише глухий кут → undo/ресет · Рахунку нема.

## Керування і ввід
- Геймпад/клавіатура: напрям — перекотитись; окремі кнопки — висунути/втягнути механізм (у Euler — кожну кулісу); перемкнути інструмент; обертати камеру (?).
- Undo по одному кроку (утомливо на довгих спробах) і повний ресет рівня.

## Вікна, меню, HUD
- `main-menu` → `level-select` у вигляді «композицій» з «частинами» (movements); побічні історії окремо.
- `game-screen`: діорама, мінімальний HUD — активний інструмент (?).
- `pause-menu`: продовжити, ресет, вихід (?).
- `settings-window`: мова (8 мов), звук.
- `end-screen` / перехід до наступної частини.

## Фічі поза полем
- 120+ пазлів (Steam), організовані в композиції й частини; рівень відкриває наступний; частина рівнів має кілька пазлів, неповне проходження не зараховується.
- Необовʼязкові побічні історії, не потрібні для основного сюжету.
- `undo` по кроку, `restart-level`; Steam-досягнення, cloud-save; демо.
- Саундтрек як частина подачі (нагороди за музику).

## Варіації й родичі
- Родичі: Bloxorz (перекочування багатоклітинного блоку), Stephen's Sausage Roll (орієнтація як стан), Snakebird (тіло з кількох клітин з гравітацією), The Lost Vikings (герої з різними вміннями).
- Осі: **форма тіла** (кубик / паралелепіпед / Г-подібне / змінна довжина) · **власний механізм** (штанга / міх / дві куліси) · **співпраця** (один / двоє / троє на рівні).

## Цікавинки для курсу
- Перекочування тіла з виступами: поворот набору клітин навколо ребра + перевірка колізій — 🥈.
- Механізм змінної довжини (висування відштовхує тіло від опори) — 🥉.
- Орієнтація визначає ефект тієї самої дії — 🥉 (таблиця «орієнтація × дія»).
- Кілька аватарів з різними фізиками на одному полі, один підіймає іншого — 🥈.
- Розвʼязувач для рівня з трьома тілами — 🥇 (великий простір станів).

## Мапа на каталог
- Є: `move-4dir` · `multi-cell-size` ↔ тіла з кількох клітин · `orientation-state` ↔ верхня грань · `party-switch` ↔ три інструменти · `height-levels` ↔ 3D-висоти · `impassable-cells` · `reach-exit` ↔ аркуш нот · `undo-redo` + `undo-step` · `restart-level` · `level-unlock` · `level-select`.
- **Нема** → пропозиції карток:
  - `+roll-block` (як у Bloxorz) · `+rotate-view-to-solve` (як у Captain Toad).
  - `+extend-retract-body` «Тіло висуває частину і відштовхується» · entities/move · 🥉.
  - `+lift-other-avatar` «Аватар підіймає/штовхає іншого аватара» · entities/interact · 🥉.
  - `+shape-shifting-body` «Тіло змінює форму між станами» · entities/state · 🥉.
  - `+optional-side-levels` «Необовʼязкові побічні рівні» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:extend(a, part, n)` — висунути частину тіла на N клітин.
- `+effect:retract(a, part)` — втягнути частину.
- `+cond:part_clear(a, part, dir)` — для частини тіла є вільне місце.
- `+cond:orientation(a, o)` — тіло в орієнтації (ширше за `facing`: яка грань угорі).
- `+trigger:collected(a, goal)` — інструмент забрав ціль (можна лишити `reach`).
- `+role:multi-body` — аватар з кількох рухомих частин.
- `+axis:actors=party` — підтвердження осі (три аватари по черзі).
- `+card:extend-retract-body` · `+card:lift-other-avatar` — див. вище.

## Джерела
- ⭐ [Steam: Kine](https://store.steampowered.com/app/824570/Kine/) — 120+ пазлів, три жовті роботи, мови, демо, Chump Squad; Steam-реліз 19.10.2020.
- [VideoGamer: огляд](https://www.videogamer.com/reviews/kine-review) — рухи трьох інструментів, ціль — аркуш нот, undo, меблі сітки, платформи, дата 18.10.2019.
- [Game Tyrant: огляд](https://gametyrant.com/news/kine-review-puzzling-instruments-that-make-your-head-spin) — орієнтація змінює дію, Roo підіймає інших, undo по кроку і ресет, композиції й частини.
- [Geeky Hobbies: огляд](https://www.geekyhobbies.com/?p=20381) — крок як перекочування кубика, колізії виступів, ~22 стадії по 5–10 рівнів, побічні історії.
- YouTube: пошук «kine gwen frey gameplay».

## Непевне
- (?) Гравітація: чи тіло падає без опори і чи можна «впасти з рівня» — огляди прямо не кажуть.
- (?) Кількість пазлів: Steam — 120+, Geeky Hobbies — ~100 (22 стадії × 5–10).
- (?) Точне керування (кнопки висування, обертання камери) і HUD.
- (?) Рік: перший реліз 18.10.2019 (за VideoGamer; Epic/консолі), Steam — 2020; Wikipedia-статті нема (404).
- (?) Чи меблі, що «виринають і складаються», — механіка поля чи анімація переходу.
