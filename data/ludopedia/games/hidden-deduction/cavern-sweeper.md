---
title: Cavern Sweeper
slug: cavern-sweeper
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2022
platforms: [web (HTML5)]
links:
  - {kind: itch, url: "https://hempuli.itch.io/cavern-sweeper", best: true, note: "грати в браузері; керування, «прочитай Бестіарій»; коментарі про слизів, змій, привидів, драконів"}
  - {kind: other, url: "https://hempuli.itch.io/cavern-sweeper/devlog", note: "девлог 15–18.11.2022: змії, мітки цифрами, режим All Hazards, HARD, лічильник перемог"}
  - {kind: other, url: "https://hempuli.itch.io/cavern-sweeper/devlog/452279/version-16", note: "v1.6: змії, мітки цифровими клавішами, до 8 типів небезпек"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cavern+Sweeper+Hempuli", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [cell-click, flood-reveal, hp-damage, difficulty-levels, mode-select, codex-window, remaining-counter, dot-mark, streak-stats, game-screen, +typed-hazard-footprints, +moving-hidden-hazard, +numbered-monster-marks, +hazard-mix-mode]
proposes: ["+effect:mark_kind", "+cond:in_footprint", "+feature:hazard-mix", "+card:typed-hazard-footprints", "+card:moving-hidden-hazard", "+card:hazard-mix-mode"]
author: opus
date: 2026-11-09
---

# Cavern Sweeper — сапер, де замість мін монстри різних видів, і кожен вид по-своєму змінює числа довкола

## Суть
Hempuli-варіант сапера: у печері сховані монстри, а не міни, і «монстри — як міни, тільки інакші». Кожен вид має власну зону впливу на числа (не обовʼязково 8 сусідів), тож нуль не гарантує, що сусіди безпечні. Правила видів пояснює вбудований Бестіарій. Помилка забирає здоровʼя, а не одразу програш.

## Поле і час
- Квадратна сітка; розмір і склад монстрів залежать від складності (?).
- Статичний пазл: хід = клік; таймер лише міряє час.
- Число на клітині — сумарний «вплив» монстрів, у чию зону вона потрапляє (гравці: «міни змінюють числа довкола», «у монстрів більша зона дії, ніж звик») (?).
- Змії мають «патерн руху» (v1.6b) — імовірно, займають кілька клітин ланцюгом (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | прихований вміст | ЛКМ — відкрити; позначену відкрити не можна |
| Відкрита клітина з числом | mark | n | вплив монстрів, чиї зони її накривають (?) |
| Слиз (slime) | enemy | зона впливу (?) | базовий монстр-«міна» |
| Змія (serpent) | enemy | форма тіла / патерн (?) | зламує «навколо нуля безпечно» |
| Привид (ghost) | enemy | дальня зона (range) | вплив на відстані — нуль поруч не гарантія |
| Дракон (dragon) | enemy | — (?) | у важчих режимах (?) |
| Мітка гравця | mark | вид монстра або «?» | ПКМ / цифрові клавіші; 9 — просто «?» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(reveal, c)` → ЯКЩО `not state(c, marked)` and `not occupied(c, monster)` → ТО `reveal(c)` з числом `custom: «сума впливу монстрів, у чию зону входить c»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `state(c, marked)` → ТО `block` (з v1.5.5d).
- КОЛИ `after(reveal(c))` → ЯКЩО `custom: «число = 0»` → ТО `reveal(neighbors)` (?) — авто-відкриття, яке, за гравцями, «видає» змій і привидів.
- КОЛИ `input(reveal, c)` → ЯКЩО `occupied(c, monster)` → ТО `custom: «втрата здоровʼя»` (`hp(player, -n)` (?)), монстр відкривається з червоною рамкою.
- КОЛИ `hp_zero(player)` → ТО `lose` (?).
- КОЛИ `input(mark, c, kind)` → ТО `mark(c, kind)`; `input(9, c)` → ТО `mark(c, "?")`.
- КОЛИ `custom: «відкрито всі безпечні клітини»` → ТО `win`, `message(victory)`, `counter(wins, +1)`, `counter(streak, +1)`.
- Перемога: очистити печеру (?) · Поразка: здоровʼя вичерпано (?) · Рахунок: час, серія перемог (cookies).

## Керування і ввід
- ЛКМ — відкрити; ПКМ — мітка (по колу видів (?) — гравець скаржиться «шість кліків на привида»).
- Цифрові клавіші — мітка конкретним видом (v1.6); 9 — «?» (v1.6.2).
- Клавіатурні скорочення перестають працювати, якщо клікнути поза грою на сторінці.

## Вікна, меню, HUD
- `game-screen`: поле, таймер, `remaining-counter` монстрів, здоровʼя.
- `codex-window` — Бестіарій: правила кожного виду (обовʼязкове читання за автором).
- `difficulty-select` / `mode-select`: рівні складності (зокрема HARD, «max difficulty») і All Hazards.
- `end-screen` — повідомлення про перемогу (v1.5.6).

## Фічі поза полем
- `difficulty-presets`; режим All Hazards — усі типи небезпек разом (до 8 видів після v1.6).
- `stats`: перемоги й серія перемог через cookies (v1.6.2); налаштування живуть між рестартами, доки не покинеш сторінку.
- Генерація без балансу — автор визнає, що бувають вгадування.

## Варіації й родичі
- Той самий автор: [mamono-mower](mamono-mower.md). Монстри замість мін: [mamono-sweeper](mamono-sweeper.md), [dragonsweeper](dragonsweeper.md), [demoncrawl](demoncrawl.md).
- Інші зони впливу клітин-підказок: [14-minesweeper-variants](14-minesweeper-variants.md), [hexcells](hexcells.md); вороги-міни зі своєю поведінкою — [tacticsweeper](tacticsweeper.md).
- **Осі варіацій**: зона впливу = 8 сусідів / відстань / форма тіла; мітка = прапорець / вид монстра; помилка = програш / мінус здоровʼя.

## Цікавинки для курсу
- Вид монстра як «маска впливу» на числа (параметризований генератор підказок) — 📎.
- Монстр, що займає кілька клітин ланцюгом (змія) — 🥉.
- Мітки за видом з цифрових клавіш — 🌱.
- Режим «усі небезпеки разом» з комбінуванням масок — 📎.
- Вбудований бестіарій як паспорт сутностей — 🌱.

## Мапа на каталог
- Є: `cell-click` · `flood-reveal` · `hp-damage` ↔ здоровʼя · `codex-window` ↔ Бестіарій · `remaining-counter` · `dot-mark` ↔ «?» · `streak-stats` ↔ серія перемог · `difficulty-levels` + `mode-select`.
- **Нема** → пропозиції карток:
  - `+typed-hazard-footprints` «Різні види мін з різною зоною впливу на число» · game-logic/constraints · 📎.
  - `+moving-hidden-hazard` «Прихований монстр-ланцюг/рухомий (змія)» · entities/state · 🥉.
  - `+hazard-mix-mode` «Режим з усіма видами небезпек» · game-logic/difficulty · 🌱.
  - `+numbered-monster-marks` — як у Mamono Sweeper.

## Пропозиції до словників
- `+effect:mark_kind(c, kind)` — мітка видом сутності, не просто прапорцем.
- `+cond:in_footprint(c, monster)` — клітина в зоні впливу монстра (форма залежить від виду).
- `+feature:hazard-mix` — режим, що змішує всі види небезпек.

## Джерела
- ⭐ [itch.io: Cavern Sweeper](https://hempuli.itch.io/cavern-sweeper) — опис, керування, коментарі про види монстрів, здоровʼя, складності.
- [Девлог](https://hempuli.itch.io/cavern-sweeper/devlog) — 1.5.5–1.6.2, листопад 2022.
- [Version 1.6](https://hempuli.itch.io/cavern-sweeper/devlog/452279/version-16) — змії, мітки цифрами, до 8 типів.

## Непевне
- (?) Точні зони впливу кожного виду — у Бестіарії, який поза доступом; опис за коментарями.
- (?) Чи всі види лише додають 1 до числа, чи різні значення.
- (?) Скільки здоровʼя й скільки забирає помилка; що таке «дракон» і в яких режимах.
- (?) Рік: девлоги з 15.11.2022; дата першого релізу не вказана.
- (?) Чи каскад нулів відкриває 8 сусідів, чи лише гарантовано безпечні.
