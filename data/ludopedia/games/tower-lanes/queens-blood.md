---
title: Queen's Blood
slug: queens-blood
aka: []
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: score
year: 2024
platforms: [PS5, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Queen's_Blood", best: true, note: "3 ряди-смуги, ранг-пішаки визначають місце, сила йде в рахунок ряду, переможець ряду забирає його суму; натхнення Gwent, Marvel Snap, Splatoon"}
  - {kind: other, url: "https://apptrigger.com/posts/final-fantasy-7-rebirth-how-to-play-queen-s-blood-01hr51xm11ew", note: "стартові пішаки в крайніх колонках, патерн карти (біле/жовте/червоне), захоплення перефарбовує пішаків, переможений у ряду — 0"}
  - {kind: other, url: "https://gamerguides.com/final-fantasy-vii-rebirth/guide/minigames/queens-blood/queens-blood-tutorial-final-fantasy-vii-rebirth", note: "поле 3×5, колода ≤ 15, ліва/права сторони, кінець — коли обидва не можуть ставити"}
  - {kind: other, url: "https://digitaltrends.com/?p=3526461", note: "жовті клітинки — пішаки, червоні — посилення/ослаблення, рівність у ряду — нікому, прев'ю ефекту при наведенні, муліган"}
  - {kind: other, url: "https://thenerdstash.com/complete-queens-blood-guide-for-final-fantasy-7-rebirth/", note: "рука 5, одна перездача, 6 колод, ранги Blood Squire → Blood Champion"}
  - {kind: other, url: "https://powerpyx.com/?p=233155", note: "15 клітинок, 7–10 карт за матч, приклади здібностей (Ifrit, Archdragon)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Queen%27s+Blood+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cursor-place, legal-move-highlight, pocket, ai-opponent, no-moves-left, event-points, end-screen, tutorial-window, +lane-grid, +deck-draw, +deck-builder, +card-collection, +mulligan-redraw, +rank-cost-pawns, +stamp-pattern-placement, +pawn-stack-cap, +territory-capture, +row-power-sum, +row-winner-takes-sum, +enhance-enfeeble, +destroy-at-zero-power, +conditional-card-abilities, +effect-preview, +win-card-reward, +opponent-ladder, +tournament-bracket]
proposes: ["+effect:draw_card", "+effect:add_pawn", "+trigger:power_zero", "+cond:pawns_ge_rank", "+role:card", "+role:pawn", "+ui:row-power", "+ui:card-pattern-grid", "+ui:effect-preview", "+window:deck-builder", "+window:opponent-list", "+window:tournament-bracket", "+card:rank-cost-pawns", "+card:stamp-pattern-placement", "+card:row-winner-takes-sum"]
author: opus
date: 2026-11-09
---

# Queen's Blood — картярка з FF VII Rebirth: поле 3×5, пішаки-«територія» визначають, куди ставити карту, а ряд забирає той, у кого більша сума

## Суть
Міні-гра у Final Fantasy VII Rebirth: два гравці з колодами по 15 карт ставлять карти на поле **3 ряди × 5 клітинок**, починаючи з власної крайньої колонки. Карта має **ранг 1–3** — стільки своїх пішаків має бути на клітинці, щоб її туди поставити — і **патерн** на сітці 5×5 навколо себе: жовті клітинки додають або перефарбовують пішаків (розширення території), червоні — посилюють чи ослаблюють карти. Наприкінці кожен ряд дістається тому, в кого більша сума сили, — і **вся сума ряду** йде йому в рахунок; переможений у ряду отримує 0. Розробники називали натхненням Gwent, баланс Marvel Snap і захоплення території зі Splatoon.

## Поле і час
- Поле 3×5 (15 клітинок); гравець — ліворуч (свої пішаки в лівій колонці), суперник — праворуч (у правій).
- Клітинка: порожня · з пішаками одного кольору (1–3) · з картою (карта займає клітинку назавжди, якщо її не знищено).
- Ряд — смуга підрахунку; ліворуч і праворуч від ряду — суми сили гравців.
- Хід почерговий, одна карта за хід; партія триває, доки обидва можуть ставити (на практиці 7–10 карт на гравця).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта | piece (`+role:card`) | ранг 1–3, сила (power), патерн 5×5, здібність | ставиться на свою клітинку з пішаками ≥ рангу; сила додається до ряду |
| Пішак | mark (`+role:pawn`) | колір (свій/чужий), 1–3 на клітинці | право ставити карту; кількість — максимальний ранг для клітинки |
| Жовта клітинка патерну | zone | відносно карти | +1 пішак (порожня/своя) або перефарбування чужих пішаків |
| Червона клітинка патерну | zone | суцільна / контурна | ціль здібності: посилення (enhance) або ослаблення (enfeeble) карти там, своєї чи чужої |
| Ряд ×3 | zone (`+role:lane`) | сума сили кожного гравця | наприкінці: більша сума забирає весь ряд |
| Колода · рука | zone | колода 15, рука на старті 5 | одна перездача на старті |
| Суперник | — | ранг на мапі | NPC у містах; перемога дає його карту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «колода 15, кожен бере 5»`, `choose(карти для перездачі)` один раз; `spawn_at(pawn, own_edge_column)` по 1 у кожному ряду.
- КОЛИ `turn_start(side)` → ТО `custom: «draw_card ×1»` (?).
- КОЛИ `input(place, card, cell)` → ЯКЩО `turn_of(side)` and `occupied(cell, own_pawn)` and `counter(pawns[cell], >=, rank)` and `not occupied(cell, card)` → ТО `place(player, card)`, `counter(row_power[side], +power)`; інакше `block`.
- КОЛИ `spawned(card)` → ЯКЩО `free(yellow_cell)` → ТО `spawn(pawn, yellow_cell)` свого кольору.
- КОЛИ `spawned(card)` → ЯКЩО `occupied(yellow_cell, own_pawn)` and `counter(pawns, <, 3)` → ТО `counter(pawns[yellow_cell], +1)`.
- КОЛИ `spawned(card)` → ЯКЩО `occupied(yellow_cell, enemy_pawn)` → ТО `set_side(pawns, player)` — кількість та сама (3 червоні → 3 сині).
- КОЛИ `spawned(card)` → ЯКЩО `occupied(red_cell, card)` and `custom: «здібність — enhance»` → ТО `counter(power[target], +n)`.
- КОЛИ `spawned(card)` → ЯКЩО `occupied(red_cell, card)` and `custom: «здібність — enfeeble»` → ТО `counter(power[target], -n)`.
- КОЛИ `counter(power[card], <=, 0)` → ТО `disappear(card)` (?).
- КОЛИ `custom: «умова здібності (напр. за кожну посилену карту)»` → ТО `counter(power[card], +n)` — Dio +1, Ifrit +2 за кожну посилену.
- КОЛИ `spawned(archdragon)` → ЯКЩО `occupied(right_cell, enemy_card)` → ТО `disappear(enemy_card)`.
- КОЛИ `no_moves(side)` → ТО `pass_turn` (?).
- КОЛИ `no_moves(both)` → ТО `game_over`, підрахунок.
- КОЛИ `game_over` → ТО `custom: «для кожного ряду: більша сума → score(+row_total) переможцю ряду; меншій стороні — 0; рівно — нікому»`.
- КОЛИ `custom: «рядки підраховано»` → ЯКЩО `custom: «твій загальний рахунок більший»` → ТО `win`, `give(player, opponent_card)`; менший — `lose`; рівний — `draw` (?).
- Перемога: більша сума очок за виграні ряди · Поразка: менша · Рахунок: сума рядів, де ти мав більшу силу.

## Керування і ввід
- Геймпад/миша: вибір карти з руки → курсор по клітинках; доступні клітинки підсвічені.
- Наведення карти на клітинку показує прев'ю: де зʼявляться пішаки, кого посилить/ослабить, як зміняться суми рядів.
- Перездача на старті: позначити карти й замінити.
- Пас / пропуск ходу — див. «Непевне».

## Вікна, меню, HUD
- Мапа світу FF VII Rebirth: суперники в містах із номером рангу (`+window:opponent-list`) → діалог виклику.
- `+window:deck-builder` — до 6 колод по 15 карт; колекція карт (купують у крамницях, в обміні GP у Gold Saucer, виграють у суперників).
- `game-screen`: поле 3×5 з пішаками двох кольорів, `+ui:row-power` (суми кожного ряду з обох боків), рука (`pocket`), карта крупно з `+ui:card-pattern-grid`, `+ui:effect-preview`, `legal-move-highlight`.
- `tutorial-window` — навчальна партія з першим суперником.
- `end-screen` — підсумок рядів, переможець, карта-нагорода, підвищення рангу.
- `+window:tournament-bracket` — турнір Queen's Blood у сюжеті.

## Фічі поза полем
- `rank-tiers`: Blood Squire → Blood Knight → … → Blood Champion; перемоги над суперниками піднімають ранг і відкривають сильніших.
- `unlockables`: карта за кожного переможеного суперника, паки й карти в крамницях.
- Колоди-пресети (до 6), без онлайну; планується «перероблена» версія у FF VII Revelation (2027).

## Варіації й родичі
- Родичі в корпусі: [gwent](gwent.md) (ряди-суми, рядок забирає більший), [marvel-snap](marvel-snap.md) (3 локації, більшість), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md), [inscryption](inscryption.md); з настільних — [tiny-towns](../board-digital/tiny-towns.md) (патерни на сітці).
- Поза корпусом: Triple Triad (FF VIII) і Tetra Master (FF IX) — попередні картярки серії; Splatoon (фарбування території).
- **Осі варіацій**: місце для карти — будь-де / лише своя територія з рангом · ріст території — сусідство / штамп-патерн карти · рахунок — сума всіх / більшість рядів / переможець ряду бере суму ряду · рівність у ряду — нікому / обом.

## Цікавинки для курсу
- Штамп-патерн 5×5 навколо карти: накласти маску на поле з обрізанням країв — 📎.
- Ранг-ціна як кількість пішаків на клітинці (1–3), захоплення перефарбовує зі збереженням кількості — 🥉.
- «Переможець ряду забирає всю суму ряду, переможений — 0» — 🌱, але змушує рахувати, де вигідно поступитися.
- Enhance/enfeeble з мітками «посилена» і здібності «за кожну посилену» — 📎.
- Прев'ю наслідків ходу при наведенні (симуляція ходу без застосування) — 🥉.
- AI-суперник з колодою і пресетом рангу — 🥈.

## Мапа на каталог
- Є: `cursor-place` ↔ карта на клітинку · `legal-move-highlight` · `pocket` ↔ рука · `ai-opponent` · `no-moves-left` ↔ кінець партії · `event-points` ↔ сума рядів · `end-screen`, `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+mulligan-redraw`, `+territory-capture`, `+row-power-sum` — уже в корпусі.
  - `+rank-cost-pawns` «Ціна карти — кількість своїх пішаків на клітинці» · entities/legality · 🥉.
  - `+stamp-pattern-placement` «Карта ставить пішаків за маскою навколо себе» · entities/legality · 📎.
  - `+pawn-stack-cap` «До 3 пішаків на клітинці» · 🌱.
  - `+row-winner-takes-sum` «Переможець ряду бере його суму, інший — 0» · game-logic/score · 🌱.
  - `+enhance-enfeeble` «±сила картам у зоні дії» · entities/state · 📎; `+destroy-at-zero-power` · 🌱; `+conditional-card-abilities` · 🥉.
  - `+effect-preview` «Прев'ю ходу при наведенні» · interface/hud · 🥉.
  - `+win-card-reward` «Перемога дає карту суперника» · 🌱; `+opponent-ladder` · 🌱; `+tournament-bracket` · 📎.

## Пропозиції до словників
- `+effect:draw_card` — взяти карту (повтор).
- `+effect:add_pawn` — +1 пішак свого кольору на клітинку (до 3).
- `+trigger:power_zero` — сила карти дійшла до 0.
- `+cond:pawns_ge_rank` — на клітинці своїх пішаків ≥ рангу карти.
- `+role:card`, `+role:lane` — повтори; `+role:pawn` — маркер права на клітинку з кількістю.
- `+ui:row-power` — повтор з Gwent; `+ui:card-pattern-grid` — мініатюра патерну на карті; `+ui:effect-preview`.
- `+window:deck-builder` — повтор; `+window:opponent-list`; `+window:tournament-bracket`.
- `+card:rank-cost-pawns`, `+card:stamp-pattern-placement`, `+card:row-winner-takes-sum`.

## Джерела
- ⭐ [Wikipedia: Queen's Blood](https://en.wikipedia.org/wiki/Queen%27s_Blood) — три ряди, ранг-пішаки визначають місце, сила йде в ряд, переможець ряду додає його суму; натхнення, рецензії, продовження у FF VII Revelation.
- [AppTrigger: How to play](https://apptrigger.com/posts/final-fantasy-7-rebirth-how-to-play-queen-s-blood-01hr51xm11ew) — стартові колонки, патерн (біле/жовте/суцільне й контурне червоне), захоплення перефарбовує, переможений у ряду — 0.
- [GamerGuides: Tutorial](https://gamerguides.com/final-fantasy-vii-rebirth/guide/minigames/queens-blood/queens-blood-tutorial-final-fantasy-vii-rebirth) — 3×5, колода 15, ліва/права сторони, кінець, коли обидва не можуть ставити.
- [Digital Trends](https://digitaltrends.com/?p=3526461) — жовті й червоні клітинки, рівність у ряду — нікому, перездача, прев'ю.
- [The Nerd Stash](https://thenerdstash.com/complete-queens-blood-guide-for-final-fantasy-7-rebirth/) — рука 5, одна перездача, 6 колод, ранги.
- [PowerPyx](https://powerpyx.com/?p=233155) — 15 клітинок, 7–10 карт за матч, Ifrit, Archdragon.
- [GameSFuze](https://gamesfuze.com/guides/final-fantasy-7-rebirth-queens-blood-card-game-guide/) — колода 15, рука 5, карта суперника за перемогу.
- [GGRecon](https://www.ggrecon.com/guides/final-fantasy-7-rebirth-queens-blood-how-to-play/) — 5×3, очки ряду зараховуються лише тому, хто його виграв.
- YouTube: пошук «Queen's Blood gameplay».

## Непевне
- (?) Добір карти на початку кожного ходу і пас: у відкритих джерелах прямо не описано.
- (?) Знищення карти при силі 0 і доля пішаків під нею.
- (?) Мета: Wikipedia/GamerGuides/AppTrigger/GGRecon — загальна сума виграних рядів; TheNerdStash — «2 з 3 рядів»; прийнято суму (GameSFuze прямо каже, що виграти один ряд мало, якщо два інших переважають).
- (?) Перездача — кількість карт (одна чи кілька): Digital Trends — «одну», TheNerdStash — «скинуті карти».
- (?) Нічия за загальним рахунком.
- (?) PC-версія FF VII Rebirth — з памʼяті; Wikipedia про платформи мовчить.
- (?) Як жовта клітинка діє на клітинку з картою.
