---
title: Vindinium
slug: vindinium
aka: [Віндиніум, vindinium.org]
family: program-robots
also: [roguelike, maze-arcade]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: score
year: 2014
platforms: [web, local server]
links:
  - {kind: official, url: "https://github.com/ornicar/vindinium", best: true, note: "сервер гри (Scala/Play, MongoDB): правила, API, генератор карт, рушій; домен vindinium.org втрачено — лише локальний запуск"}
  - {kind: other, url: "https://raw.githubusercontent.com/ornicar/vindinium/master/app/views/documentation.scala.html", note: "сторінка правил: легенда карти, хід героя, шахти й гобліни, таверна, бійки, спрага, смерть, кінець, Elo"}
  - {kind: other, url: "https://raw.githubusercontent.com/ornicar/vindinium/master/app/views/starters.scala.html", note: "технічна документація: HTTP-архітектура, режими training/arena, JSON стану, таймаут 1 с, стартові пакети ~28 мов"}
  - {kind: other, url: "https://raw.githubusercontent.com/ornicar/vindinium/master/app/Arbiter.scala", note: "розвʼязання ходу: крок, шахта, таверна, бійки, респавн із телефрагом, видобуток"}
  - {kind: other, url: "https://raw.githubusercontent.com/ornicar/vindinium/master/app/Config.scala", note: "параметри карти: розмір 10–28, стіни 10–41 %, шахти 3–9 %; 300×4 ходів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=vindinium+bot", note: "пошук; реплеї ботів"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, hp-damage, respawn, spawn-points, ai-random, online-multiplayer, rating-system, leaderboard, replay, replay-window, profile-stats, move-timer, turn-enforcement, level-from-txt, reachability-check, state-as-data, game-loop, +http-json-bot, +training-vs-arena, +mine-capture-guardian, +income-per-owned-cell, +tavern-heal-for-gold, +adjacent-auto-attack, +spawn-telefrag, +hp-floor-drain, +mirror-symmetric-map, +crashed-bot-stays, +starter-packs]
proposes: ["+trigger:timeout(bot)", "+cond:owner(a, side)", "+effect:income(per_owned)", "+feature:bot-api-modes", "+feature:starter-packs", "+window:bot-register", "+window:live-tv", "+ui:gold-score-bar"]
author: opus
date: 2026-11-09
---

# Vindinium — чотири боти-герої по HTTP ріжуть гоблінів за золоті шахти, а виграє той, хто за 300 ходів назбирав найбільше золота

## Суть
AI-змагання від автора lichess (ornicar) і vjousse: гравець пише бота будь-якою мовою, бот на кожен хід отримує JSON зі станом і шле HTTP-запит з одним наказом (Stay/North/South/East/West). Чотири герої на симетричній карті захоплюють шахти (бій з гобліном коштує HP), отримують золото з кожної своєї шахти щоходу, лікуються пивом у тавернах за золото й бʼють сусідніх героїв. Убитий герой відроджується на старті з усім золотом, але без шахт — їх забирає вбивця. Ядро — економіка «ризикни HP → отримай дохід» плюс прості, але повні правила для пошуку шляху й оцінки позиції.

## Поле і час
- Квадратне поле `size × size`, клітина кодується **двома символами**: `##` ліс (непрохідний), `  ` порожньо, `@1`…`@4` герої, `[]` таверна, `$-` нейтральна шахта, `$1`…`$4` шахта героя N. Стан поля — один рядок `tiles` довжини size²·2 (рядок карти — `% size`).
- Генератор: чверть карти з відсотком стін/шахт, потім дзеркалення по X і Y → симетрія 4-го порядку; завжди 4 таверни й 4 герої; старт героя перевіряється flood-fill-ом (досяжні дзеркальні старти), шахти без доступу стають лісом. Арена: розмір 10–28 (парний), стіни 10–41 %, шахти 3–9 % (Config.scala). Тренування — 6 готових карт m1–m6 або випадкова.
- Час `programmed`: ходи **по черзі** (turn % 4), один наказ на хід; партія — 300 ходів кожного героя (у JSON `turn`/`maxTurns` рахують накази: 1200). На відповідь — 1 с.
- Інформація повна: кожен бот бачить усю карту, HP, золото, шахти й позиції всіх героїв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (бот) | player | HP 100 max, gold ≥ 0, spawnPos, crashed | наказ Stay/N/S/E/W; кінець ходу — бійка, видобуток, спрага |
| Герой суперника | enemy | те саме | ходить у свою чергу; сусідній — атакує |
| Ліс `##` | static | — | непрохідний; край поля — теж |
| Шахта `$-` / `$N` | resource | власник: нейтральна або герой N | вхід = бій із гобліном (−20 HP); вижив — шахта твоя, +1 золото/хід |
| Гоблін | enemy | охоронець шахти | не рухається; після захоплення «охороняє» шахту для нового власника |
| Таверна `[]` | static | ціна 2 золота | вхід = пиво: −2 золота, +50 HP (до 100); герой лишається на місці |
| Точка старту | zone | одна на героя, дзеркальні | респавн; хто стоїть на ній у момент респавну — гине |
| Випадковий бот | ally | лише в training | 3 суперники, що ходять навмання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(hero)` → ТО `custom: «сервер відповідає боту JSON: game (turn, maxTurns, heroes, board.tiles, finished), hero, token, viewUrl, playUrl»`.
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(hero, dir)`; `input(Stay)` — герой стоїть.
- КОЛИ `input(dir)` → ЯКЩО `cell(cell_ahead, wood)` або `edge(hero)` або `occupied(cell_ahead, hero)` → ТО `block` (у героя бійка — пізніше, у кінці ходу).
- КОЛИ `contact(hero, mine)` → ЯКЩО `not state(mine, owned_by_hero)` → ТО `block`, `damage(hero, 20)`; ЯКЩО `counter(hp, >, 0)` → ТО `set_side(mine, hero)`.
- КОЛИ `contact(hero, mine)` → ЯКЩО `state(mine, owned_by_hero)` → ТО `block` (нічого не стається).
- КОЛИ `hp_zero(hero)` після бою з гобліном → ТО `set_side(all_mines_of(hero), neutral)`, `respawn(hero, spawnPos)`.
- КОЛИ `contact(hero, tavern)` → ЯКЩО `counter(gold, >=, 2)` → ТО `block`, `currency(-2)`, `heal(hero, 50)` (стеля 100); золота нема — просто `block`.
- КОЛИ `turn_end(hero)` → ЯКЩО `adjacent_count(hero, enemy_hero, >=, 1)` → ТО `damage(each_adjacent_enemy, 20)`; атакер не втрачає HP; діагональ не рахується.
- КОЛИ `hp_zero(defender)` у бійці → ТО `set_side(all_mines_of(defender), attacker)`, `respawn(defender, spawnPos)`.
- КОЛИ `custom: «герой респавниться»` → ЯКЩО `occupied(spawnPos, enemy_hero)` → ТО `custom: «той гине (телефраг), його шахти переходять до відродженого, а він сам респавниться за тим самим правилом»`.
- КОЛИ `custom: «герой або ціль щойно відродились у цей хід»` → ТО `custom: «бійки з ними пропускаються»`.
- КОЛИ `turn_end(hero)` → ТО `currency(+mines_owned)` (дохід за кожну свою шахту); потім `damage(hero, 1)` (спрага), `custom: «HP не падає нижче 1»`.
- КОЛИ `custom: «герой відроджується»` → ТО `heal(hero, 100)`, `custom: «золото зберігається, шахт нуль»`.
- КОЛИ `custom: «нема наказу за 1 с»` → ТО `set_state(hero, crashed)` до кінця гри: стоїть, але зберігає золото й шахти й може виграти.
- КОЛИ `custom: «усі 4 боти crashed»` (у training — будь-який) → ТО `game_over`.
- КОЛИ `counter(turn, ==, maxTurns)` → ТО `game_over`; найбільше золота → `win`; рівність лідерів → `draw` («no winner»).
- КОЛИ `game_over` → ЯКЩО `mode(arena)` → ТО `custom: «Elo попарно між усіма 4 (K = 16), +1 бонус з шансом 1/10»`; `mode(training)` — без рейтингу.
- КОЛИ `game_start` → ТО `custom: «генерувати чверть карти, віддзеркалити ×4, поставити 4 таверни так, щоб не відрізати шахти; до 100 спроб»`.
- Перемога: найбільше золота після 300 ходів · Поразка: менше золота · Рахунок: золото = Σ(шахти × ходи володіння) − 2 × пиво.

## Керування і ввід
- Людина не керує героєм: бот — HTTP-клієнт. Реєстрація: імʼя → секретний `key` (не відновлюється).
- Тренування: `POST /api/training` з `key`, необовʼязкові `turns` (за замовч. 300) і `map` (m1–m6) → JSON стану; хід — `POST playUrl` з `key` і `dir`.
- Арена: `POST /api/arena` з `key`; сервер чекає 4 ботів, гра рейтингова.
- Коди відповіді: 200 — ок; 4xx — помилка (чужий хід, гра скінчилась, запізно); 500 — сервер.
- Глядач: `viewUrl` у браузері — реплей/живий перегляд; можна запускати кілька копій свого бота.

## Вікна, меню, HUD
- `main-menu` (головна): девіз, «TV» — живі ігри, список останніх ігор (імена, Finished / In progress), `leaderboard` (імʼя + Elo).
- `help-window` «Documentation» — правила з легендою карти; `custom-window` «Starters» — технічна документація API й стартові пакети.
- `bot-register` (custom): форма «Create a bot» → показ ключа.
- `profile-window` бота (`/ai/<id>`): Elo, ігри, «зараз грає»; `leaderboard` топ ботів (`/ai`).
- `game-screen` / `replay-window` (`/<gameId>`): анімована карта (герої, шахти з кольором власника, таверни, кров, сліди), `gold-score-bar` (custom: частки золота 4 героїв), `stat-panel` героїв (HP, золото, шахти, Elo), `turn-counter`, панель відтворення (`pause-button`, `speed-slider`, перемотування — custom), позначка Live.
- `live-tv` (custom): потік поточної гри на арені (`/tv`).
- Переходи: головна → Documentation / Starters / Register; головна → TV або гра зі списку → replay-window.

## Фічі поза полем
- Два режими API: `training` (3 випадкові боти, без рейтингу, свої ходи й карта) і `arena` (Elo).
- `rating-system` Elo, `leaderboard-online`, профіль бота, `replay` кожної гри за `viewUrl`.
- `starter-packs`: ~28 мов (Python, Java, Haskell, Rust, Prolog, OCaml…) — бот, що ходить навмання, з готовим HTTP/JSON.
- Сервер відкритий (Scala, Play, MongoDB): `sbt run` → localhost:9000 для приватних турнірів; IRC і сабреддит спільноти.

## Варіації й родичі
- Корпус: [bot-arenas](bot-arenas.md) (AI Challenge Ants, Halite, Battlecode, CodinGame), [battlesnake](battlesnake.md) (HTTP-вебхук, `move` на хід), [kaggle-kore-fleets](kaggle-kore-fleets.md) і [lux-ai](lux-ai.md) (економіка ресурсів), [screeps](screeps.md) (постійний світ), [ai-challenge-ants](ai-challenge-ants.md).
- Осі варіацій: **протокол** (HTTP-pull на хід / вебхук-push / stdin-stdout); **черговість** (по черзі — Vindinium / одночасно — Battlesnake, Ants); **смерть** (відродження зі збереженням золота / вибування); **економіка** (володіння клітинами-джерелами / збір і доставка); **симетрія карти** (дзеркальна ×4 — справедливість для 4 сторін).

## Цікавинки для курсу
- Захоплення шахти ціною HP + дохід щоходу + перехід шахт до вбивці — 🥉 (власник клітини як стан, `set_side`).
- Генератор симетричної карти: чверть → дзеркала, flood-fill перевірка досяжності, таверни без відрізання шахт — 🥇.
- Порядок фаз кінця ходу (бійка → видобуток → спрага з підлогою 1 HP) і телефраг при респавні з ланцюгом — 🥈.
- HTTP/JSON-протокол бота + таймаут 1 с + «crashed» бот, що лишається на полі — 🥈 (клієнт-сервер у лабі).
- Простий бот: BFS до найближчої чужої шахти / таверни з евристикою HP — 🥉; minimax/MCTS для 4 гравців — 👑.
- Elo попарно для гри 4 гравців — 📎.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (ліс) · `hp-damage` · `respawn` · `spawn-points` · `ai-random` (тренувальні боти) · `online-multiplayer` · `rating-system` (Elo) · `leaderboard` · `replay` / `replay-window` · `profile-stats` · `move-timer` (1 с на хід) · `turn-enforcement` («Not your turn to move») · `level-from-txt` (карти рядком по 2 символи) · `reachability-check` (генератор) · `state-as-data` (JSON стану) · `game-loop`.
- **Нема** → пропозиції карток:
  - `+http-json-bot` «Бот як HTTP-клієнт: стан JSON → наказ» · game-logic/opponent · 🥈.
  - `+training-vs-arena` «Тренування без рейтингу проти випадкових ботів і рейтингова арена» · game-logic/opponent · 🥉.
  - `+mine-capture-guardian` «Захоплення клітини-шахти ціною HP» · entities/interact · 🥉.
  - `+income-per-owned-cell` «Дохід щоходу за кожну свою клітину» · game-logic/economy · 📎.
  - `+tavern-heal-for-gold` «Лікування за валюту на клітині» · entities/interact · 🌱.
  - `+adjacent-auto-attack` «Автоатака сусіда в кінці ходу» · entities/combat · 📎.
  - `+spawn-telefrag` «Респавн вбиває того, хто стоїть на точці» · entities/death · 📎.
  - `+hp-floor-drain` «Втрата HP щоходу з підлогою 1» · entities/state · 🌱.
  - `+mirror-symmetric-map` «Карта з дзеркальною симетрією для N сторін» · levels/generation · 🥈.
  - `+crashed-bot-stays` «Бот, що не відповів, стоїть до кінця» · game-logic/opponent · 🌱; `+starter-packs` · support/docs · 📎.

## Пропозиції до словників
- `+trigger:timeout(bot)` — бот не надіслав наказ за ліміт часу (Vindinium 1 с, Battlesnake, AI Challenge).
- `+cond:owner(a, side)` — власник клітини/обʼєкта (шахта героя N, нейтральна); зараз лише через `state`.
- `+effect:income(per_owned)` — дохід, пропорційний кількості своїх клітин (шахти, території).
- `+feature:bot-api-modes` — окремі точки API для тренування і рейтингової арени; `+feature:starter-packs` — стартові клієнти багатьма мовами.
- `+window:bot-register` — реєстрація бота з видачею секретного ключа; `+window:live-tv` — потік поточної рейтингової гри.
- `+ui:gold-score-bar` — смуга часток рахунку всіх гравців.

## Джерела
- ⭐ [GitHub ornicar/vindinium](https://github.com/ornicar/vindinium) — сервер, README (домен втрачено, локальна установка), створено січень 2014.
- [documentation.scala.html](https://raw.githubusercontent.com/ornicar/vindinium/master/app/views/documentation.scala.html) — повні правила й легенда карти.
- [starters.scala.html](https://raw.githubusercontent.com/ornicar/vindinium/master/app/views/starters.scala.html) — API, режими, JSON, таймаут, коди відповіді, стартові пакети.
- [Arbiter.scala](https://raw.githubusercontent.com/ornicar/vindinium/master/app/Arbiter.scala) + Hero.scala, Game.scala, Generator.scala, Config.scala, system/Elo.scala, system/Client.scala — константи (100 HP, −20, +50/2 золота, −1), телефраг, порядок ходу, генерація, Elo K = 16, випадкові боти training.
- YouTube: пошук «vindinium bot».

## Непевне
- (?) Ліміт 1 с — з документації; у коді таймаут береться з конфігурації `vindinium.ai-timeout`, значення в репо не дивився.
- (?) Розмір карт m1–m6 і чи training без `map` бере ту саму випадкову генерацію, що й арена.
- (?) Вигляд сторінки реплею (панелі, кнопки) — з назв компонентів клієнта (GoldScoreBar, HeroStats, PlayControls, TurnCount, Live), сам інтерфейс не бачив.
- (?) Скільки часу сайт працював (2014 — до втрати домену).
