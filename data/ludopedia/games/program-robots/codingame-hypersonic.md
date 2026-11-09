---
title: "CodinGame: Hypersonic"
slug: codingame-hypersonic
aka: [Hypersonic, HyperSonic]
family: program-robots
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: score
year: 2016
platforms: [web]
links:
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/hypersonic", best: true, note: "арена CodinGame (сторінка на JS, автоматично не читається): «знищити якнайбільше ящиків і вижити»"}
  - {kind: other, url: "https://forum.codingame.com/t/hypersonic-feedback-strategy/2067", note: "розбори топ-гравців: 4 гравці, ліги, одночасні дії, 100 мс, DFS/MCTS/A*/Вороного"}
  - {kind: other, url: "https://forum.codingame.com/t/hypersonic-puzzle-discussion/2193", note: "обговорення: ліги Wood → Bronze → Gold"}
  - {kind: other, url: "https://github.com/paulannekov/codingame-hypersonic", note: "бот на Dart: формат вводу, таймер 8, клітини . X 0-2, типи сутностей 0/1/2"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman", note: "прообраз"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+hypersonic", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, bomb-fuse, blast-wave, chain-detonation, destructible-blocks, in-round-upgrades, item-pickup, event-points, chase-bfs, realtime-ai, move-timer, replay, leaderboard, level-from-txt, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +auto-pathfind-command, +item-in-box, +blast-stops-at-first, +league-boss-promotion, +local-referee]
proposes: ["+trigger:timeout(bot)", "+cond:bombs_left(a)", "+effect:place_bomb(range)", "+effect:eliminate(bot)", "+ui:debug-message", "+feature:bot-upload", "+feature:league-promotion"]
author: opus
date: 2026-11-09
---

# CodinGame: Hypersonic — Bomberman для ботів: бомби з запалом, ящики з бонусами, ланцюгові вибухи, усі ходять одночасно

## Суть
Конкурс CodinGame (вересень–жовтень 2016): гравець пише бота, що щоходу читає з stdin сітку й список сутностей і друкує одну команду — йти до клітини або поставити бомбу й іти. Бомба вибухає через кілька ходів хрестом, руйнує ящики (за кожен — очко), з ящиків випадають бонуси (+радіус, +бомба), бомби в полі вибуху детонують ланцюгом. Матч 2–4 ботів; виграє той, хто зруйнував найбільше ящиків і не загинув. Загальна рамка арен (протокол, ліги, реплеї) — у [bot-arenas](bot-arenas.md); тут — правила поля й тіку.

## Поле і час
- Квадратна сітка; розмір приходить у першому рядку (`width height myId`); типово 13×11 (?).
- Клітини: `.` підлога, `X` стіна (нерушима), `0` ящик порожній, `1`/`2` ящик з бонусом певного типу.
- Тік = хід: усі боти відповідають, дії застосовуються **одночасно**; ліміт ~100 мс на хід (форум; пропонували 50 мс).
- Повна інформація: видно всі бомби з таймерами й радіусами, усі бонуси; вміст ящика видно за цифрою (?).
- Старти — у кутах (?); карта генерується симетрично (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бот-гравець (entityType 0) | player | owner, x, y, param1 = бомб у запасі, param2 = радіус | крок 1 на хід у 4 напрямки; ставить бомбу на свою клітину |
| Бомба (entityType 1) | object | owner, x, y, param1 = ходів до вибуху, param2 = радіус | таймер −1 щоходу; на 0 — вибух хрестом; непрохідна (?) |
| Бонус (entityType 2) | pickup | x, y, param1 = тип (1 = +радіус, 2 = +бомба) | підбирається входом у клітину; гине у вибуху |
| Ящик `0` / `1` / `2` | object | що всередині | руйнується вибухом, лишає бонус за цифрою |
| Стіна `X` | static | — | непрохідна, зупиняє вибух |
| Полумʼя вибуху | hazard | один тік | убиває гравця в клітині |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «суддя шле сітку рядками й список сутностей entityType owner x y param1 param2»`.
- КОЛИ `exec(MOVE x y)` → ТО `move(player, step)` за `custom: «найкоротший шлях до (x, y); недосяжна — стоїть (?)»`.
- КОЛИ `exec(BOMB x y)` → ЯКЩО `has(player, bomb)` and `not occupied(cell, bomb)` → ТО `spawn_at(bomb, player_cell)` з таймером 8 і радіусом гравця, потім `move` до (x, y).
- КОЛИ `timer(every)` (кожен хід) → ТО у кожної бомби `counter(fuse, −1)`.
- КОЛИ `counter(fuse, ==, 0)` → ТО `explode(cross(range − 1))` — промінь у 4 боки до `range − 1` клітин (код бота: `for i in 1..range−1`).
- КОЛИ `custom: «промінь вибуху дійшов до стіни, ящика, бонусу чи іншої бомби»` → ТО промінь зупиняється на цій клітині: стіна — без змін; ящик — `disappear_b` і `score(+1)` власнику бомби; бонус — `disappear_b`; бомба — `trigger(rule)` ланцюгова детонація в тому ж ході.
- КОЛИ `destroyed(box)` → ЯКЩО `custom: «цифра ящика > 0»` → ТО `spawn_at(item, box_cell)` — бонус зʼявляється після вибуху, тому той самий вибух його не знищує (?).
- КОЛИ `contact(player, flame)` → ТО `lose` для цього бота (вибуває, місце за часом смерті (?)).
- КОЛИ `contact(player, item)` → ТО `pickup`: тип 1 → `counter(range, +1)`, тип 2 → `counter(max_bombs, +1)`.
- КОЛИ `custom: «бомба гравця вибухнула»` → ТО `counter(bombs_left, +1)` — бомба повертається в запас (за форумом, з затримкою на хід (?)).
- КОЛИ `custom: «бот не відповів вчасно або нерозпізнана команда»` → ТО `lose`.
- КОЛИ `custom: «ліміт ходів»` або `counter(alive, <=, 1)` → ТО `game_over` (?); переможець — більше зруйнованих ящиків серед тих, хто вижив (?).
- Перемога: найбільше ящиків, вижити довше за суперників · Поразка: смерть у полумʼї, таймаут · Рахунок: +1 за ящик бомбою бота.

## Керування і ввід
- Ініціалізація: `width height myId`.
- Щоходу: `height` рядків сітки → `entities` → рядки `entityType owner x y param1 param2`.
- Вивід: `MOVE x y` або `BOMB x y` (+ необовʼязковий текст-повідомлення після координат, видно в реплеї (?)).
- Бот не керує кроком напряму: ціль-клітина, шлях будує суддя — тому стратегія вирішує «куди», а не «як».
- Тестування — IDE CodinGame з вибором суперників-ботів; Submit → матчі в лізі.

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова, редактор коду, вибір мови, консоль stderr, Play testing / Submit.
- `replay-viewer`: поле по кадрах, бомби з лічильниками, радіуси, накази й повідомлення ботів; `frame-scrubber`.
- `league-ladder`: Wood 3…1 → Bronze → Silver → Gold → Legend; «бос» ліги.
- HUD реплею: портрети 2–4 гравців з рахунком ящиків, бомб і радіусом (?).

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion` (обійти боса).
- `replay` будь-якого матчу; ліги відкривають правила поступово (у нижчих лігах — простіші правила (?)).
- Нема undo/pause — лише покроковий реплей.

## Варіації й родичі
- Bomberman (Hudson Soft) — живий прообраз; у корпусі арени ботів — [bot-arenas](bot-arenas.md) (Tron, Ants, Halite).
- CodinGame «Legends of Code & Magic», «Code a la Mode» — інші конкурси того ж формату; [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md) — територія.
- Осі варіацій: **ціль** (ящики / вбивства / виживання); **бонуси** (з ящика / випадково); **поширення вибуху** (до першої перешкоди / крізь ящики); **команда руху** (напрямок / ціль-клітина з автошляхом); **кількість гравців** (1v1 / FFA 4).

## Цікавинки для курсу
- Симулятор бомб: таймери, хрест до першої перешкоди, ланцюгова детонація в межах одного ходу — 🥉.
- «Небезпечні клітини»: карта часу вибуху кожної клітини з урахуванням ланцюгів → BFS-втеча з поправкою на час — 🥈.
- Бот, що обирає клітину для бомби за кількістю ящиків у хресті й наявністю шляху втечі — 🥈.
- Пошук на кілька ходів уперед (DFS з поглибленням / MCTS) з моделлю суперників як «фантомних бомб» — 🥇.
- Локальний суддя на 4 боти з одночасним застосуванням ходів і реплеєм — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `bomb-fuse` (таймер 8, ліміт бомб) · `blast-wave` (хрест на N) · `chain-detonation` · `destructible-blocks` (ящики з дропом) · `in-round-upgrades` (радіус, бомби — саме так описана картка) · `item-pickup` · `event-points` (+1 за ящик) · `chase-bfs` (автошлях і втеча) · `realtime-ai` · `move-timer` · `replay` · `leaderboard` · `level-from-txt` (сітка рядками).
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee` — з [bot-arenas](bot-arenas.md), тут підтвердження.
  - `+auto-pathfind-command` «Команда — ціль-клітина, шлях будує рушій» · entities/move · 📎 (є і в Keep Off the Grass).
  - `+item-in-box` «Вміст ящика видно/задано типом клітини» · entities/spawn · 🌱.
  - `+blast-stops-at-first` «Вибух зупиняється на першій перешкоді, руйнуючи її» · entities/combat · 📎 (слот blast-wave).

## Пропозиції до словників
- `+trigger:timeout(bot)` — вже просили з bot-arenas; тут друге підтвердження.
- `+cond:bombs_left(a)` — у гравця є вільна бомба (окремо від `has`, бо бомби повертаються).
- `+effect:place_bomb(range)` — поставити бомбу з параметрами власника; `+effect:eliminate(bot)` — друге підтвердження.
- `+ui:debug-message` — текст бота поруч з аватаром у реплеї.
- `+feature:bot-upload`, `+feature:league-promotion` — підтвердження.

## Джерела
- ⭐ [CodinGame: Hypersonic](https://www.codingame.com/multiplayer/bot-programming/hypersonic) — арена; умова рендериться JS, автоматично не прочитана; опис «destroy as many boxes as possible without dying» — зі сніпета пошуку.
- [Forum: Feedback & Strategy](https://forum.codingame.com/t/hypersonic-feedback-strategy/2067) — 4 гравці, ліги з босами, одночасні дії, 100 мс, повернення бомби, стратегії.
- [Forum: Puzzle Discussion](https://forum.codingame.com/t/hypersonic-puzzle-discussion/2193) — ліги, сутності «bombs, items, players, boxes».
- [paulannekov/codingame-hypersonic](https://github.com/paulannekov/codingame-hypersonic) — Dart-бот: `countdown = 8`, `range = 3`, сітка `. X 0 1 2`, сутності 0/1/2, `MOVE`/`BOMB x y`, «fire doesn't go behind the box».
- [Wikipedia: Bomberman](https://en.wikipedia.org/wiki/Bomberman) — прообраз.

## Непевне
- (?) Розмір 13×11, старти в кутах, симетрична генерація — з памʼяті; бот читає розмір з вводу.
- (?) Значення бонусів (1 = радіус, 2 = бомба) — код підтверджує лише, що тип 2 дає +бомбу.
- (?) Порядок фаз ходу (вибухи → підбір → рух → нові бомби), коли саме зʼявляється бонус із ящика й коли повертається бомба — форум каже, що правила були неясні.
- (?) Чи бомба непрохідна для гравців; чи полумʼя вбиває в нижчих лігах.
- (?) Ліміт ходів, умова кінця (усі ящики знищено + N ходів) і правило ранжування загиблих — не бачив у джерелі; форум лише каже, що гра тягнулась 100+ ходів після останнього ящика.
- (?) Перший хід з довшим лімітом — як у інших аренах CodinGame, не перевірено.
