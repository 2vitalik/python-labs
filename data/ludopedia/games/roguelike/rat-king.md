---
title: Rat King (torcado)
slug: rat-king
aka: [ratking]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: score
year: 2025
platforms: [web (HTML5), PC (Windows, Linux)]
links:
  - {kind: itch, url: "https://torcado.itch.io/rat-king", best: true, note: "грати в браузері; «a broughlike about a rat and a rat», керування: стрілки/WASD/свайп, предмети 1–5"}
  - {kind: other, url: "https://torcado.itch.io/rat-king/comments?after=0", note: "відповіді розробника: щури на окремих дошках, дошка стоїть, коли щур не діяв, удар у стіну — не дія; привиди ходять від дій іншого щура"}
  - {kind: other, url: "https://torcado.itch.io/rat-king/devlog/987710/rat-king-11", note: "Rat King 1.1 (16.07.2025): серця в магазині, рідкісні вороги, прихована корона, ціни предметів, портали, таблиця рекордів"}
  - {kind: other, url: "https://itch.io/games/tag-broughlike", note: "тег broughlike на itch.io"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rat+King+torcado+broughlike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [move-4dir, keyboard-controls, swipe-gestures, inventory-items, item-pickup, round-currency, shop-catalog, spawn-points, drop-on-death, stairs-levels, sequential-levels, dungeon-generation, player-death, leaderboard, +twin-boards, +bump-no-action, +cross-board-ghost, +rising-item-cost]
proposes: ["+trigger:acted(a)", "+cond:board_of(a, b)", "+effect:pass_board(a, b)", "+ui:twin-board-view", "+axis:actors=twin", "+card:twin-boards"]
author: opus
date: 2026-11-09
---

# Rat King — broughlike на двох дошках: один щур і ще один щур, кожен у своєму підземеллі, а хід дошки — лише коли її щур справді діяв

## Суть
Гравець веде **двох щурів одночасно**, кожен — на окремій дошці-підземеллі. Дошка робить хід (вороги діють) лише тоді, коли її щур виконав дію — крок або предмет; **удар у стіну дією не вважається**, тож упором у стіну можна «притримати» одну дошку, поки друга рухається. Між дошками є зв'язок через привидів: вони ходять від дій **іншого** щура і їх можна перегнати на сусідню дошку. Решта — класичний broughlike: вороги з порталів, монети, магазини, предмети 1–5, серця, поверхи й таблиця рекордів.

## Поле і час
- Дві квадратні дошки-кімнати поруч, по щуру на кожній; поверхи з кімнатами, магазинні кімнати й «спільна кімната» (common room).
- Покроково: дошка змінюється лише від дії свого щура; без дії — стоїть (розробник: вороги не «чекають», просто нема ходу).
- Генерація рівнів процедурна (?); портали підкидають ворогів під час гри.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Щур ×2 | player | серця (спільні?), предмети | крок 4 напрямки на своїй дошці |
| Ворог (звичайний, рідкісні варіанти) | enemy | — | атакує щура своєї дошки; сильнішає з поверхами |
| Привид | enemy | — | ходить, коли діє *інший* щур; атака по привиду — дія |
| Портал (зокрема «привидний») | spawner | — | породжує ворогів; після 5-го порталу вороги без луту |
| Монета / діамант | resource | — | валюта магазину |
| Серце | pickup | — | життя; продається в магазині |
| Предмет (лікування, парирування, секундомір, будування стіни, мапа, щит) | pickup | ціна використання | слот 1–5; деякі — миттєві |
| Корона | pickup | — | прихований предмет, не продається |
| Крамар і «нора крамаря» | neutral | — | магазин; у нору можна сховати одного щура, щоб вести лише другого |
| Полумʼя | hazard | — | (?) шкодить; на ньому портали не з'являються |
| Сходи | static | — | вихід на наступний поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `custom: «наказ отримують обидва щури»` (?); для кожного щура ЯКЩО `free(cell)` → ТО `move(rat, dir)`.
- КОЛИ `blocked(rat)` → ТО `custom: «щур не діяв — його дошка не ходить»`.
- КОЛИ `custom: «щур діяв (крок, предмет, атака)»` → ТО `custom: «вороги його дошки роблять хід»`, `custom: «привиди на іншій дошці роблять хід»`.
- КОЛИ `input(item_1..5)` → ЯКЩО `has(rat, item)` → ТО `use(rat, item)`, `currency(−cost)` (?); ціна росте після 10-го використання в кімнаті й 50-го на поверсі.
- КОЛИ `input(stopwatch)` → ТО `custom: «час на дошці заморожено»` (?) · КОЛИ `input(parry)` → ТО `set_state(rat, parry)` (?) · КОЛИ `input(wall)` → ТО `set_cell(cell, wall)`.
- КОЛИ `custom: «вороги атакують»` → ЯКЩО `not state(rat, parry|shield)` → ТО `damage(rat, n)` (?).
- КОЛИ `custom: «щур у пастці без виходу»` → ТО `lives(−1)`.
- КОЛИ `timer(every)` або `spawned(portal)` → ТО `spawn_at(enemy, portal)` (?).
- КОЛИ `died(enemy)` → ЯКЩО `counter(portals, <=, 5)` → ТО `spawn_at(pickup, cell)`.
- КОЛИ `enter(rat, stairs)` → ТО `custom: «щур чекає на сходах; обидва — наступний поверх»` (?).
- КОЛИ `custom: «серця скінчились»` → ТО `game_over`; рахунок і поверх — у таблицю рекордів.

## Керування і ввід
- Стрілки / WASD / свайп — крок; клавіші 1–5 або тап — предмети.
- Підтримка геймпада (згадано мертву зону контролера).

## Вікна, меню, HUD
- `game-screen`: дві дошки поруч, серця, монети, `inventory-bar` (слоти 1–5).
- `shop-window` — магазинна кімната з крамарем (у світі гри).
- `leaderboard` — сортування за поверхом або рахунком.
- `main-menu` (?), `end-screen` (?).

## Фічі поза полем
- `leaderboard-online` (за поверхом / за рахунком).
- `touch-controls`, `gamepad-support`.
- Захист від фарму рахунку (зростання цін, вороги без луту після 5-го порталу).

## Варіації й родичі
- Broughlike-школа: [868-HACK](868-hack.md), [Mosaic](mosaic-broughlike.md), [Magpie](magpie-broughlike.md); той самий автор — Manymancer, Critter Switcher (itch).
- Подвійне керування одним вводом — родич [Twinfold](twinfold.md) (один свайп рухає все поле) і пазлів «один ввід — кілька аватарів» (thinky).
- Осі варіацій: **скільки дошок** (одна / дві паралельні) · **коли дошка ходить** (кожен ввід / лише при реальній дії свого аватара) · **зв'язок дошок** (нема / привиди, що реагують на інший аватар).

## Цікавинки для курсу
- Дві дошки, один ввід, «удар у стіну — не дія» як спосіб розсинхронізувати — 📎.
- Привид, що ходить від дій іншого аватара й переходить між дошками (зміна парності ходів) — 🥉.
- Ціна предмета, що росте після N використань у кімнаті/поверсі (анти-фарм) — 🌱.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`, `swipe-gestures`; `inventory-items`, `item-pickup`; `round-currency` + `shop-catalog` ↔ монети й крамар; `spawn-points` ↔ портали; `drop-on-death` ↔ лут ворогів; `stairs-levels`, `sequential-levels`, `dungeon-generation`; `player-death`; `leaderboard`.
- **Нема** → пропозиції карток:
  - `+twin-boards` «Два аватари на двох окремих дошках одним вводом» · entities/move · 📎.
  - `+bump-no-action` «Упор у стіну не витрачає хід» · entities/legality · 🌱.
  - `+cross-board-ghost` «Ворог, що ходить від дій іншого аватара» · entities/move · 🥉.
  - `+rising-item-cost` «Ціна використання росте з кількістю використань» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:acted(a)` — аватар реально виконав дію (не упор у стіну).
- `+cond:board_of(a, b)` — сутність на тій самій дошці, що й аватар.
- `+effect:pass_board(a, b)` — перевести сутність на іншу дошку.
- `+ui:twin-board-view` — дві дошки поруч.
- `+axis:actors=twin` — два одночасні аватари одним вводом.
- `+card:twin-boards`.

## Джерела
- ⭐ [itch: Rat King](https://torcado.itch.io/rat-king) — опис, керування, теги broughlike / traditional-roguelike, платформи.
- [itch: коментарі](https://torcado.itch.io/rat-king/comments?after=0) — відповіді torcado про дошки, дії й привидів; гравці про предмети, монети, серця, нору крамаря.
- [itch: devlog Rat King 1.1](https://torcado.itch.io/rat-king/devlog/987710/rat-king-11) — серця, рідкісні вороги, корона, ціни предметів, портали, рекорди.
- [itch: тег broughlike](https://itch.io/games/tag-broughlike).

## Непевне
- (?) Чи один ввід рухає обох щурів одночасно — випливає з відповідей розробника («дошка стоїть, коли щур не діяв»; «удар у стіну — не дія») і огляду Thinky (сніпет пошуку: «рішення з огляду на обидва оточення одночасно»), прямо не сказано.
- (?) Як атакують щури й вороги (удар упритул?), що роблять щит, парирування, секундомір; спільні чи окремі серця.
- (?) Процедурність рівнів і темп порталів; полум'я як пастка.
- (?) Рік: devlog 1.1 — липень 2025; дату першого релізу не бачив.
- Сторінка Thinky Games (джерело черги) агентам недоступна (403).
