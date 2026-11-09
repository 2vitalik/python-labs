---
title: Jungler
slug: jungler
aka: [ジャングラー]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1981
platforms: [arcade, Tomy Tutor, Arcadia 2001, Gakken tabletop, PS4, Switch]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%82%B8%E3%83%A3%E3%83%B3%E3%82%B0%E3%83%A9%E3%83%BC", best: true, note: "JA: будова змійки (голова/тіло/хвіст), довжини 8 і 9, бій головами, постріл у хвіст, блокади, очки, запас довжини"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jungler", note: "EN: кольори ворогів за довжиною, полуниці, прискорення коротших, порти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=jungler+konami+arcade+gameplay", note: "пошук; аркада"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-auto, body-queue, no-reverse-turn, projectile-shot, impassable-cells, speed-per-type, spawn-random-cell, item-pickup, destroy-all-enemies, event-points, extra-life-threshold, player-death, sequential-levels, progress-acceleration, realtime-ai, +length-duel, +shoot-off-segment, +length-color-cue, +shorter-is-faster, +body-stock, +stuck-self-destruct, +ghost-body]
proposes: ["+cond:compare", "+feature:length-stock"]
author: opus
date: 2026-11-09
---

# Jungler — змійка проти трьох ворожих змійок: довжина вирішує, хто кого зʼїсть при зіткненні головами

## Суть
Гравець — біла змійка в синьому лабіринті, вороги — три такі самі змійки. Постріл у хвіст відрізає сегмент, а зіткнення головами виграє довша (або рівна) змійка: колір ворога весь час показує, довший він за тебе (червоний), рівний (жовтий) чи коротший (зелений). Коротші змійки рухаються швидше — тож обрізаний ворог стає верткішим. На відміну від `snake.md`, довжина тут — бойовий стат, а не рахунок, і тіло не має зіткнень.

## Поле і час
- Клітинний лабіринт на один екран, видно все; рух по коридорах 4 напрямками.
- Real-time; швидкість кожної змійки залежить від її довжини (коротша — швидша); після 8-го етапу цикл повторюється з вищою загальною швидкістю.
- 8 етапів-лабіринтів; етап закривається, коли знищено всіх трьох ворогів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець-змійка | player | голова 1 + тіло 0–7 + хвіст 0–1; старт — 8, максимум 9 | рух 4 напрямки, **можна** розвернутись на 180°; стріляє |
| Ворог червоний | enemy | довший за гравця; старт 9 | зіткнення головами → гравець втрачає життя |
| Ворог жовтий | enemy | рівний гравцю | зіткнення головами → ворог переможений (EN: нешкідливий) |
| Ворог зелений | enemy | коротший | зіткнення головами → гравець його зʼїдає |
| Голова | object | — | єдина частина, що бʼється в дуелі |
| Тіло (сегменти) | object | — | **без зіткнень**: крізь нього проходять |
| Хвіст | object | — | ціль для пострілів: влучання → −1 сегмент |
| Постріл (гравця / ворога) | projectile | — | летить коридором; вороги теж стріляють |
| Полуниця | pickup | 500 очок | зʼявляється у випадковому місці; +1 сегмент гравцю |
| Блокада | static | — | гравцю непрохідна; ворог, що вперся, застрягає і за час самознищується |
| Стіна лабіринту | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(snake, facing)`; `speed(snake, ~1/length)` — коротші швидші.
- КОЛИ `input(dir, player)` → ТО `face(player, dir)` (розворот дозволено); ворог: ЯКЩО `custom: «dir протилежний»` → ТО `block`.
- КОЛИ `input(fire, player)` → ТО `spawn(shot, facing)`.
- КОЛИ `contact(shot, enemy_tail)` → ТО `grow(enemy, -1)`, `score(60)`.
- КОЛИ `contact(shot, enemy_head)` → ЯКЩО `custom: «у ворога лише голова»` → ТО `disappear(enemy)`, `score(500)`.
- КОЛИ `contact(enemy_shot, player_tail)` → ТО `grow(player, -1)`.
- КОЛИ `contact(enemy_shot, player_head)` → ЯКЩО `custom: «у гравця лише голова»` → ТО `lives(-1)`.
- КОЛИ `contact(shot, body)` → ТО `custom: «нічого — тіло без зіткнень»`.
- КОЛИ `contact(player_head, enemy_head)` → ЯКЩО `custom: «довжина гравця ≥ довжини ворога»` → ТО `disappear(enemy)`, `score(80 × enemy_length)`; інакше `lives(-1)`.
- КОЛИ `custom: «довжина будь-якої змійки змінилась»` → ТО `custom: «колір ворога перераховується: червоний > гравця, жовтий =, зелений <»`.
- КОЛИ `rng(p)` → ТО `spawn_at(strawberry, random_free_cell)`; КОЛИ `contact(player, strawberry)` → ТО `score(500)`, ЯКЩО `counter(length, <, 9)` → ТО `grow(player, +1)`.
- КОЛИ `contact(enemy, blockade)` → ТО `set_state(enemy, stuck)`; КОЛИ `contact(shot|player, stuck_enemy)` → ТО `disappear(enemy)`, `score(300)`; КОЛИ `timer(stuck_time)` → ТО `disappear(enemy)` без очок.
- КОЛИ `contact(player, blockade)` → ТО `block`.
- КОЛИ `all_gone(enemy)` → ТО `next_level`; ЯКЩО `counter(length, ==, 9)` → ТО `counter(stock, +1)`, наступний етап з довжиною 8.
- КОЛИ `counter(stock, ==, 8)` → ТО `lives(+1)`; КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)`.
- КОЛИ `died(player)` → ЯКЩО `counter(lives, ==, 0) and counter(stock, ==, 0)` → ТО `game_over`; ЯКЩО `counter(stock, >, 0)` → ТО `respawn(player, start)` з довжиною із запасу.
- Перемога: нема (цикл 8 етапів). Поразка: життя і запас вичерпано. Рахунок: тарани (80 × довжина), хвости, голови, застряглі, полуниці.

## Керування і ввід
- 4-позиційна рукоятка + одна кнопка пострілу.
- Змійка, судячи з жанру, рухається безперервно, рукоятка змінює напрям (?).

## Вікна, меню, HUD
- `attract-demo` — аркадний атракт (?).
- `game-screen`: лабіринт, `score`, `hi-score`, `lives`, запас довжини (?), `level-number` (?).
- Переходи: атракт → монета → етап → (усі вороги) наступний → … → життя 0 → атракт.

## Фічі поза полем
- `hotseat` — 2 гравці по черзі (?).
- Arcade Archives (Hamster, 2024): `speed-control`, `operator-settings` (?).
- `+feature:length-stock` — накопичувана «запасна довжина», що переходить у життя.

## Варіації й родичі
- Відмінності від `snake.md`: довжина обмежена (≤ 9) і є бойовим статом; тіло без зіткнень; зростання — лише полуниця; постріл зрізає хвіст; гравець може розвертатися, вороги — ні; коротша = швидша.
- Родичі: `centipede.md` (сегментований ворог, що втрачає частини від пострілів), `snake.md`, `blockade.md` / `tron-light-cycles.md` (змійки-суперники), `snake-rattle-n-roll.md` (довжина як ресурс).
- **Осі варіацій:** тіло (смертельне / прохідне); дуель (довший виграє / хто перший / ніхто); постріл (нема / зрізає хвіст / вбиває); зростання (за їжу / за перемогу / обмежене).

## Цікавинки для курсу
- Бій головами за порівнянням довжин — 🌱: одна умова, багато тактики.
- Колір ворога як живий індикатор «сильніший / рівний / слабший» відносно гравця — 🌱.
- Постріл у хвіст відрізає сегмент; ворог коротшає і прискорюється — 📎.
- Швидкість як функція довжини (тік через раз для довгих) — 📎.
- Блокада, на якій ворог застрягає, а гравець — ні (різна прохідність за типом) — 🌱.
- Запас довжини між етапами → життя — 🌱.
- AI змійки без розвороту в лабіринті — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` · `body-queue` · `no-reverse-turn` (лише вороги) · `projectile-shot` · `impassable-cells` (блокада — для гравця) · `speed-per-type` · `spawn-random-cell` (полуниця) · `item-pickup` · `destroy-all-enemies` · `event-points` · `extra-life-threshold` · `player-death` · `sequential-levels` · `progress-acceleration` · `realtime-ai`.
- **Нема** → пропозиції карток:
  - `+length-duel` «Зіткнення головами: виграє довший» · entities/combat · 🌱.
  - `+shoot-off-segment` «Постріл зрізає сегмент тіла» · entities/combat · 📎.
  - `+length-color-cue` «Колір ворога = порівняння з гравцем» · interface/render · 🌱.
  - `+shorter-is-faster` «Швидкість залежить від довжини» · entities/state · 📎.
  - `+body-stock` «Запас довжини між рівнями» · levels/progression · 🌱.
  - `+stuck-self-destruct` «Ворог застряг і самознищився» · entities/death · 🌱.
  - `+ghost-body` «Тіло без зіткнень» · entities/move · 🌱 (варіант `self-collision` «ігнорувати»).

## Пропозиції до словників
- `+cond:compare` — порівняння властивості двох сутностей (`compare(a, b, length, >=)`); `same` покриває лише рівність.
- `+feature:length-stock` — запас «довжини», що конвертується в життя.

## Джерела
- ⭐ [Wikipedia JA: ジャングラー](https://ja.wikipedia.org/wiki/%E3%82%B8%E3%83%A3%E3%83%B3%E3%82%B0%E3%83%A9%E3%83%BC) — будова змійки, довжини, розворот, дуель, постріли у хвіст, блокади, очки, запас, 8 етапів.
- [Wikipedia: Jungler](https://en.wikipedia.org/wiki/Jungler) — кольори ворогів, полуниці, прискорення, порти.
- YouTube: пошук «jungler konami arcade gameplay».

## Непевне
- (?) Жовтий ворог: JA — таран його перемагає, EN — зіткнення нешкідливе.
- (?) Чи рух безперервний (як у Snake), чи змійка стоїть без вводу.
- (?) Як саме формула швидкості залежить від довжини; поріг часу самознищення на блокаді; пороги додаткових життів; стартові життя.
- (?) Чи зʼїдений зелений ворог дає гравцю сегменти.
- (?) Режим на двох і DIP — не перевірено.
- WebSearch-ліміт вичерпано; StrategyWiki 403.
