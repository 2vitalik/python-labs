---
title: Castle Panic
slug: castle-panic
aka: [Паніка в замку]
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: coop
  info: full
  random: runtime
  goal: survive
year: 2009
platforms: [board]
links:
  - {kind: other, url: "https://c.tabletopia.com/games/castle-panic/rules/cp-rulesweb/en", best: true, note: "офіційний рулбук (PDF): кільця, фази ходу, усі Castle-карти й Monster-токени, стіни/вежі, валун, боси, Overlord, соло"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Castle_Panic", note: "6 дуг × 4 кільця, 3 кольори, 6 фаз ходу, доповнення й спінофи"}
  - {kind: other, url: "https://www.ultraboardgames.com/castle-panic/game-rules.php", note: "правила коротко: компоненти, розмір руки, обміни, HP монстрів, Master Slayer"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=castle+panic+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hp-damage, enemy-waves, spawn-points, enemy-reached-base, status-effects, explode-area, chain-reaction, event-points, score-records, difficulty-levels, game-screen, end-screen, help-window, +deck-draw, +hand-limit, +card-trade, +ring-sector-board, +color-ring-match, +rotate-token-hp, +wall-rebuild, +wall-fortify, +rolling-boulder, +monster-event-tokens, +overlord-mode, +mvp-scoring, +local-coop]
proposes: ["+role:card", "+role:base", "+role:event", "+effect:draw", "+effect:discard", "+effect:trade", "+effect:rebuild", "+effect:knockback", "+cond:ring_color_match", "+ui:monster-pile", "+window:trade-window", "+feature:mode-overlord", "+axis:field=polar"]
author: opus
date: 2026-11-09
---

# Castle Panic — кооперативний tower defense на круглому полі: кільця × кольорові дуги, карта бʼє лише «свою» клітину

## Суть
Від 1 до 6 гравців разом захищають замок у центрі круглої дошки. Монстри зʼявляються в лісі на краю й щоходу підходять на кільце ближче; гравці грають карти з руки, і кожна карта бʼє лише в **своєму кільці та своєму кольорі** (Лучник синій — лише синє кільце лучників). Через це ядро — обмін картами й планування, хто чим прикриє яку дугу. Перемога — пережити всі 49 токенів; поразка — втратити всі 6 веж.

## Поле і час
- Поле — полярна сітка: 6 пронумерованих дуг (1–6) × кільця Ліс → Лучник → Лицар → Мечник → Замок; кожна пара дуг має колір (червоний, зелений, синій).
- Між кільцем Мечника і Замку — 6 ліній стін; у кільці Замку — 6 веж.
- Монстр займає клітину «дуга × кільце»; рух — до центру (кільце ближче), у Замку — по колу за годинниковою.
- Хід гравця — 6 фаз; монстри рухаються після кожного ходу гравця (по колу гравців).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кільце Лісу | zone | 6 дуг з номерами | точка спавну; тут монстрів бити не можна (крім валуна) |
| Кільця Лучника / Лицаря / Мечника | zone | колір дуги | карта влучає лише в своє кільце свого кольору |
| Кільце Замку | zone | 6 клітин | тут монстр бʼє вежі; дістати можуть лише окремі карти |
| Стіна | gate | 6, знищувана | монстр, що йде з кільця Мечника, бʼє стіну: стіна зникає, монстр −1 HP |
| Fortify token | gate | 2 | на стіні: поглинає один удар замість стіни |
| Вежа | static (`+role:base`) | 6, не відбудовується | монстр, що входить у її клітину, руйнує її й отримує 1 шкоди |
| Гоблін / Орк / Троль | enemy | HP 1 / 2 / 3 | крок до центру щоходу; HP — поворотом токена |
| Бос: Goblin King | boss | HP (?) | зʼявляється + витягнути ще 3 токени |
| Бос: Orc Warlord | boss | HP (?) | монстри його кольору кроком ближче (у Замку — за годинниковою) |
| Бос: Troll Mage | boss | HP (?) | усі монстри на дошці кроком ближче |
| Бос: Healer | boss | HP (?) | усі монстри на дошці лікують 1 HP |
| Валун / Giant Boulder | hazard | — | котиться через дугу, знищує всіх монстрів у ній, зупиняється на першій стіні/вежі/fortify і руйнує її |
| Монстр-ефект | hazard (`+role:event`) | — | не стає на поле: Plague!, усі скидають 1, +3/+4 токени, рух за/проти годинникової, рух кольору на 1 |
| Tar token | mark | 1 | монстр під смолою не рухається цей хід |
| Castle-карта | pickup (`+role:card`) | клас × колір | Archer/Knight/Swordsman (колір або «Any Color»), Hero (колір, будь-яке з трьох кілець), Barbarian, Brick, Mortar, Nice Shot, Missing, Drive Him Back!, Tar, Fortify Wall, Scavenge, Draw 2 |
| Колода / рука | zone | 49 карт; рука 6 / 5 / 4 за кількістю гравців | добір до повної руки на старті ходу |
| Трофей | resource | очки 1/2/3/4 | хто добив монстра, бере токен собі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(draw)` → ТО `custom: «добрати карти до розміру руки (колода скінчилась — перетасувати скид)»`.
- КОЛИ `input(discard_draw)` → ЯКЩО `first_time` → ТО `custom: «скинути 1, добрати 1»` (соло — 2).
- КОЛИ `input(trade, card, player)` → ЯКЩО `counter(trades, <, 1)` (6 гравців — 2) → ТО `swap(a, b)` — лише обмін, не подарунок.
- КОЛИ `input(play, hit_card, monster)` → ЯКЩО `custom: «кільце й колір монстра = кільце й колір карти»` and `not cell(monster, forest)` → ТО `damage(1)`, `rotate(monster, next_lower_hp)`.
- КОЛИ `input(play, hero, monster)` → ЯКЩО `custom: «колір карти, кільце Лучника/Лицаря/Мечника»` → ТО `damage(1)`.
- КОЛИ `input(play, nice_shot + hit_card, monster)` → ТО `custom: «монстра вбито одразу»`.
- КОЛИ `input(play, barbarian, monster)` → ЯКЩО `not cell(monster, forest)` → ТО `custom: «вбити будь-якого монстра, включно з кільцем Замку»`.
- КОЛИ `input(play, drive_him_back, monster)` → ТО `move(monster, forest)` у тій самій дузі.
- КОЛИ `input(play, tar, monster)` → ТО `set_state(monster, tarred, 1)`: не рухається ні у фазі руху, ні від нових токенів.
- КОЛИ `input(play, brick + mortar, wall_slot)` → ЯКЩО `free(wall_slot)` → ТО `custom: «відбудувати стіну»`.
- КОЛИ `input(play, fortify_wall, wall)` → ТО `set_state(wall, fortified)`.
- КОЛИ `input(play, missing)` → ТО `custom: «у фазі 6 цього ходу не тягнути монстрів»`; `scavenge` → `custom: «взяти будь-яку карту зі скиду»`; `draw_2` → `custom: «+2 карти понад ліміт руки»`.
- КОЛИ `hp_zero(monster)` → ТО `give(player, trophy)` тому, хто добив; убиті іншими способами — у скид.
- КОЛИ `phase_start(move_monsters)` → ТО `move(monster, inward)` для всіх поза Замком; у Замку — `move(monster, clockwise)`.
- КОЛИ `custom: «монстр з кільця Мечника йде на стіну»` → ЯКЩО `state(wall, fortified)` → ТО `clear_state(wall, fortified)`, `damage(monster, 1)`, монстр лишається; інакше → ТО `disappear(wall)`, `damage(monster, 1)`; вижив — лишається в кільці Мечника до наступного руху.
- КОЛИ `custom: «монстр іде з кільця Мечника, стіни нема»` → ТО `move(monster, castle)` без шкоди.
- КОЛИ `enter(monster, tower_cell)` → ТО `disappear(tower)`, `damage(monster, 1)`; вижив — стоїть на місці вежі й далі йде по колу.
- КОЛИ `phase_start(new_monsters)` → ТО `custom: «витягнути 2 токени»`; монстр — `spawn_at(monster, forest[d6])`; ефект — `custom: «виконати й скинути»`.
- КОЛИ `custom: «токен Giant Boulder»` → ТО `custom: «d6 → дуга»`, `custom: «знищити всіх монстрів у дузі (і в Лісі)»`, `custom: «котиться до першої стіни/вежі/fortify, руйнує її і стає; нема — далі через Замок у протилежну дугу»`.
- КОЛИ `custom: «токен Plague! Archers/Knights/Swordsmen»` → ТО `custom: «усі скидають карти цього класу»`.
- КОЛИ `custom: «токен Monsters Move Clockwise / Counter-Clockwise / Move 1 (колір)»` → ТО `move(monsters, dir)` у межах кільця або кроком до центру для кольору.
- КОЛИ `custom: «Healer»` → ТО `heal(all_monsters, 1)`; `Troll Mage` → `move(all_monsters, inward)`; `Goblin King` → `custom: «+3 токени»`.
- КОЛИ `all_gone(towers)` → ТО `lose`.
- КОЛИ `custom: «усі 49 токенів зіграно»` and `all_gone(monsters)` → ТО `win`; `counter(trophy_points)` → `custom: «Master Slayer — найбільше очок (бос 4, троль 3, орк 2, гоблін 1), нічия — більше вбитих»`.
- Перемога: пережити всі 49 токенів і вбити всіх монстрів · Поразка: зруйновано всі 6 веж · Рахунок: Master Slayer за трофеями (лише при перемозі).

## Керування і ввід
- Настільна: гравці по черзі; карти лежать відкрито (кооператив — таємниць нема), обговорення ходів вільне.
- (цифрова версія) Клік по карті → підсвічуються клітини, куди вона влучає (кільце × колір) → клік по монстру; drag карти на іншого гравця = пропозиція обміну; кнопка «кінець ходу» запускає рух монстрів і витяг токенів.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup` (кількість гравців 1–6, варіант: стандарт / Co-op / Overlord / Less Panic) → `game-screen`.
- (цифрова версія) `game-screen`: кругла дошка, `pocket` (рука активного гравця), руки інших, `+ui:monster-pile` (лишилось з 49), лічильник веж, `legal-move-highlight` для вибраної карти, `turn-indicator` з поточною фазою (6 фаз), `log-window` (який токен витягли).
- (цифрова версія) `+window:trade-window` — вибір карти для обміну; `end-screen` — перемога/поразка, таблиця Master Slayer; `help-window` — довідка по токенах (на дошці в кутах надруковано пам'ятки).

## Фічі поза полем
- Соло: рука 6, «скинути й добрати» — 2 карти.
- `+feature:mode-overlord` — один гравець керує монстрами: замість фаз 5–6 обирає, які токени грати (до 2, можна 0), місце — кидком кубика.
- Co-op варіант (без Master Slayer (?)); «Less Panic» — полегшення (напр., Hero бʼє і в кільці Замку).
- Доповнення: The Wizard's Tower (2011: чарівники, вогонь, боси), The Dark Titan (2015: Агранок), Engines of War (2016: облогові машини, балісти, інженер).

## Варіації й родичі
- Спінофи: Munchkin Panic, Star Trek Panic, Dead Panic, My First Castle Panic; Castle Panic Big Box.
- У сімʼї: [rampart](rampart.md) (замок і стіни, відбудова), [plants-vs-zombies](plants-vs-zombies.md) (вороги по смугах до бази), [isle-of-arrows](isle-of-arrows.md) (настільна логіка TD з плитками).
- **Осі варіацій**: поле — смуги / кільця × сектори · влучання — дальність вежі / відповідність клітини типу карти · ворожий хід — детермінований крок / подієві токени · суперник — колода / живий Overlord · перемога — пережити все / пережити N хвиль.

## Цікавинки для курсу
- Полярне поле «кільце × дуга» і рух до центру, у центрі — по колу — 🌱.
- Влучання за двома ключами (кільце і колір) з картами-джокерами (Any Color, Hero) — 📎.
- HP як поворот токена: стан монстра = його орієнтація — 🌱.
- Валун: «промінь» через дугу до першої перешкоди, з переходом на протилежну дугу — 📎.
- Стіна з fortify і відбудовою з двох карт (Brick + Mortar) — 🌱.
- Мішок подієвих токенів (монстри й ефекти в одній купі) — 📎.
- Overlord: AI/гравець, що вибирає з витягнутого — 🥉.

## Мапа на каталог
- Є: `hp-damage` ↔ HP 1–3 · `enemy-waves` ↔ 2 токени щоходу · `spawn-points` ↔ дуги 1–6 у Лісі · `enemy-reached-base` ↔ вежі · `status-effects` ↔ смола · `explode-area` ↔ валун на дугу · `chain-reaction` ↔ Goblin King тягне ще 3 · `event-points` + `score-records` ↔ Master Slayer · `difficulty-levels` ↔ Less Panic · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+ring-sector-board` «Полярне поле кільце × сектор» · fields/topology · 📎.
  - `+color-ring-match` «Карта діє лише на клітину свого типу й кольору» · entities/legality · 🌱.
  - `+rotate-token-hp` «HP як орієнтація токена» · entities/state · 🌱.
  - `+rolling-boulder` «Обʼєкт котиться до першої перешкоди й руйнує її» · entities/move · 📎.
  - `+monster-event-tokens` «Мішок: вороги й події разом» · game-logic/waves · 📎.
  - `+card-trade` «Обмін картами між гравцями з лімітом» · game-logic/economy · 🌱.
  - `+hand-limit` «Рука до N за кількістю гравців» · game-logic/setup · 🌱.
  - `+overlord-mode` «Один гравець за ворогів» · game-logic/opponent · 🥉.
  - `+mvp-scoring` «Кооп-перемога + особистий найкращий» · game-logic/score · 🌱.

## Пропозиції до словників
- `+role:card` · `+role:base` · `+role:event` — токен-подія з мішка ворогів, що не стає на поле.
- `+effect:draw` · `+effect:discard` · `+effect:trade` · `+effect:rebuild` (відновити знищену сутність на її місці) · `+effect:knockback` (відкинути на старт смуги).
- `+cond:ring_color_match` — клітина цілі відповідає кільцю й кольору карти.
- `+ui:monster-pile` (рука — наявний `pocket`).
- `+window:trade-window`.
- `+feature:mode-overlord`.
- `+axis:field=polar` — кільця × сектори.

## Джерела
- ⭐ [Castle Panic: офіційні правила (Tabletopia, PDF)](https://c.tabletopia.com/games/castle-panic/rules/cp-rulesweb/en) — кільця й дуги, 6 фаз, руки за кількістю гравців, усі Castle-карти, стіни й fortify, вежі в Замку, валуни, Plague, боси, Overlord, соло, Less Panic.
- [Wikipedia: Castle Panic](https://en.wikipedia.org/wiki/Castle_Panic) — 6 дуг × 4 кільця, 3 кольори, фази, доповнення, спінофи.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/castle-panic/game-rules.php) — компоненти (49 карт, 49 токенів, 6 стін, 6 веж), обміни, HP 1/2/3, Master Slayer.
- [YouTube: пошук](https://www.youtube.com/results?search_query=castle+panic+how+to+play) — як грати.

## Непевне
- (?) HP босів і точний склад колоди (скільки карт кожного типу) — у витягнутому тексті рулбука не знайшов.
- (?) Звичайний валун (Boulder) відрізняється від Giant Boulder — сценарії в рулбуку є, але різницю не розібрав.
- (?) Правила Co-op-варіанта (чи скасовується лише Master Slayer).
- (?) Офіційної цифрової версії не перевіряв (є на Tabletopia як симулятор) — вікна вище — гіпотеза.
