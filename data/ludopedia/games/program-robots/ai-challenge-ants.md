---
title: Google AI Challenge — Ants
slug: ai-challenge-ants
aka: [Ants, AI Challenge 2011, aichallenge Ants, Мурахи AI Challenge]
family: program-robots
also: [tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: hidden
  random: both
  goal: score
year: 2011
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/aichallenge/aichallenge", best: true, note: "увесь набір Ants: рушій ants.py, playgame.py, карти, генератор, візуалізатор; сайт-специфікація розділами (Turns and Phases, Scoring, Cutoff, Battle…)"}
  - {kind: other, url: "https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/ants.py", note: "рушій: фази ходу, 4 режими бою, збір їжі, спавн, знесення мурашників, очки, cutoff-и, протокол стану"}
  - {kind: other, url: "https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/playgame.py", note: "параметри за замовчуванням і запуск ботів, реплей і HTML-візуалізатор"}
  - {kind: other, url: "https://github.com/aichallenge/aichallenge/tree/epsilon/ants", note: "тека гри: maps, mapgen, visualizer, submission_test, starter-скрипти play_one_game"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/AI_Challenge", note: "лише рядок: конкурс Університету Ватерлоо 2009–2011"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ai+challenge+ants+2011+replay", note: "пошук; реплеї матчів"}
stage: v1
coverage: 75
mechanics: [command-program, move-4dir, wrap-edges, impassable-cells, fog-of-war, spawner-entity, spawn-points, item-pickup, collect-quota, piece-capture, chase-bfs, ai-greedy, realtime-ai, move-timer, replay, replay-window, level-from-txt, maze-generation, map-validation, rating-system, leaderboard, state-as-data, fixture-level-tests, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +focus-battle-resolution, +swarm-same-program, +local-referee, +cutoff-rules, +symmetric-map-generation, +collision-kills-all, +contested-food-destroyed, +rank-stabilized-cutoff]
proposes: ["+trigger:timeout(bot)", "+effect:eliminate(bot)", "+effect:raze(hill)", "+cond:count_in_radius(a, kind, r2)", "+cond:visible(cell)", "+cond:owners_in_radius(cell, r2, n)", "+card:focus-battle-resolution", "+card:collision-kills-all", "+card:contested-food-destroyed", "+card:rank-stabilized-cutoff", "+ui:vision-overlay"]
author: opus
date: 2026-11-09
---

# AI Challenge Ants — бот керує роєм мурах на торі в тумані: збирає їжу на нових мурах і зносить чужі мурашники

## Суть
Конкурс програмування 2011 року (AI Challenge, Університет Ватерлоо): гравець пише **бота**, що щоходу читає зі stdin видиму частину поля й відповідає наказами кожній своїй мурасі. На тороїдальній карті з водою 2–N ботів одночасно рухають мурах, збирають їжу (кожна → нова мураха з мурашника) і намагаються стати мурахою на чужий мурашник — це знесення дає очки. Бій не має HP: мураха гине, якщо поруч ворогів не менше, ніж у найслабшого з її ворогів («focus»). Огляд арен узагалі — у [bot-arenas.md](bot-arenas.md); тут — точні правила рушія `ants.py`.

## Поле і час
- Прямокутна сітка, згорнута в **тор**: усі відстані й огляд рахуються з обгортанням (на кожній осі — коротша з прямої і «через край» різниць).
- Клітини: суша, вода (непрохідна), їжа, мурашник, мураха. Карта — текстовий файл; генератор робить карти симетричними для чесного старту.
- Відстані — **квадрат евклідової**: огляд `viewradius2 = 77`, атака `attackradius2 = 5`, збір їжі `spawnradius2 = 1` (тобто лише 4 сусіди) — дефолти playgame.py.
- Хід: усі боти отримують стан → думають (`turntime` 1000 мс, перший `loadtime` 3000 мс) → накази всіх застосовуються **одночасно**; гра до 1000 ходів або cutoff.
- Фази ходу (finish_turn): накази → бій → знесення мурашників → спавн мурах → збір їжі → спавн нової їжі → очки → огляд → перевірка cutoff.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мураха | piece | власник, позиція | крок на 1 у n/e/s/w або стоїть; гине в бою чи при зіткненні в клітині |
| Мурашник (hill) | spawner | власник, last_touched, знесений? | породжує ≤1 мураху за хід із запасу їжі; чужа мураха на ньому → знесено |
| Запас вулика (hive food) | resource | лічильник на гравця | +1 за зібрану їжу; −1 за кожну нову мураху |
| Їжа | resource | — | спавниться за сценарієм; збирається, якщо поруч мурахи лише одного гравця |
| Вода | static | — | непрохідна; накази в неї відкидаються |
| Суша | terrain | — | звичайна клітина; лише на ній спавниться їжа |
| Туман | zone | на гравця | клітини поза оглядом власних мурах; воду, раз побачену, бот уже знає |
| Бот | player | програма, час на хід | читає стан, видає накази; таймаут / падіння — вибуває (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(bot)` → ТО `custom: «бот отримує рядки w/f/h/a/d row col [owner] для всього видимого + своїх загиблих мурах; власники перенумеровані з точки зору бота»`.
- КОЛИ `input(o row col dir)` → ЯКЩО `custom: «невідома дія, не n/e/s/w, дубль наказу тій самій мурасі, у клітині не своя мураха або вихід за межі»` → ТО `custom: «наказ невалідний, мураха стоїть»`.
- КОЛИ `input(o row col dir)` → ЯКЩО `cell(target, water)` або `cell(target, food)` → ТО `block` («move blocked»: на їжу не ступають, її збирають із сусідньої клітини).
- КОЛИ `phase_start(orders)` → ЯКЩО `custom: «у клітині після ходу більше однієї мурахи (будь-чиї, включно з тією, що стояла)»` → ТО `disappear` усіх них.
- КОЛИ `phase_start(attack)` → ЯКЩО `custom: «кількість ворогів мурахи A в attackradius2 ≥ мінімуму тієї ж кількості серед цих ворогів»` → ТО `disappear_a`; усі смерті одночасні (режим `focus`, дефолт).
- Інші режими бою (опція `attack`): `support` — гине, якщо ворогів поруч більше, ніж своїх; `damage` — кожна мураха ділить 1 шкоду між ворогами, ≥1 шкоди — смерть; `closest` — групи ворогів у взаємному радіусі від найближчих, група з >1 мурахи знімається.
- КОЛИ `enter(enemy_ant, hill)` → ЯКЩО `not state(hill, razed)` → ТО `custom: «мурашник знесено»` (+effect:raze), `score(+2)` тому, хто зніс, `score(-1)` власнику; своя мураха на своєму мурашнику лише оновлює `last_touched`.
- КОЛИ `phase_start(spawn)` → ЯКЩО `counter(hive_food, >, 0)` і `free(hill)` → ТО `spawn_at(ant, hill)`, `counter(hive_food, -1)`; мурашники обходяться від найдавніше торканого (нічия — випадково), ≤1 мураха на мурашник за хід.
- КОЛИ `phase_start(gather)` → ЯКЩО `custom: «в spawnradius2 від їжі мурахи рівно одного гравця»` → ТО `disappear_b`, `counter(hive_food, +1)`; кількох гравців → їжа знищується; нікого — лишається.
- КОЛИ `tick` → ТО `custom: «накопичувач їжі += food_rate × players / food_turn; ціла частина спавниться на суші (симетрично або секціями)»`.
- Старт: `score = кількість власних мурашників`; їжа на старті — `land_area // food_start`, плюс `food_visible` біля кожного старту.
- КОЛИ `custom: «лишився один гравець з мурахами/мурашниками»` → ТО `game_over` («lone survivor»), бонус `+2` за кожен незнесений чужий мурашник.
- КОЛИ `custom: «одна група (бот або «вся їжа на полі») має ≥ 85 % популяції (мурахи + запас + їжа)»` 150 ходів поспіль → ТО `game_over` («food not being gathered» / «ants not razing hills»); знесення мурашника скидає лічильник.
- КОЛИ `custom: «жоден живий гравець з мурашниками вже не змінить рангу навіть найкращим (+2 за кожен чужий мурашник) проти найгіршого (−1 за кожен свій) сценарію»` → ТО `game_over` («rank stabilized»).
- КОЛИ `counter(turn, =, 1000)` → ТО `game_over`.
- КОЛИ `timeout(bot)` (поза рушієм, ?) → ТО `custom: «гравця вимкнено: накази не приймаються, штраф за мурашники знімається; мурахи лишаються на полі, але не рахуються живими»`.
- Перемога: найбільше очок (місце в матчі). · Поразка: усі мурашники знесено / вибув. · Рахунок: мурашники ×(+2 за чужий, −1 за свій втрачений) + бонус survivor-у; рейтинг — за серією матчів (?).

## Керування і ввід
- Ввід — програма будь-якою мовою: стартові набори (starter packages) з класом стану; протокол — текстові рядки в stdin/stdout.
- Старт: рушій шле параметри (`loadtime`, `turntime`, `rows`, `cols`, `turns`, радіуси, `player_seed`) → `ready`; бот відповідає `go`.
- Хід: `turn N` + рядки стану → `go`; бот виводить `o row col n|e|s|w` на кожну мураху й `go`. Кінець — `end` і фінальні очки.
- Локально: `playgame.py [опції] --map_file <карта> "bot1 cmd" "bot2 cmd" …` — кількість ботів = кількість гравців карти (`--fill` повторює останнього); `--strict` (суворі накази), `--capture_errors`, `--serial`, `-R` реплей, `--nolaunch` / `--html`.

## Вікна, меню, HUD
- `replay-window` (візуалізатор): поле по ходах з туманом обраного гравця, графіки популяції й очок, швидкість, крок; HTML `replay.{id}.html` відкривається після гри.
- `leaderboard` + `profile-window` на сайті: рейтинг, матчі бота, мова (?).
- `custom-window` завантаження бота (zip) і статус компіляції; `help-window` — специфікація розділами (Turns and Phases, Scoring, Cutoff Rules, Food Harvesting, Ant Spawning, Food Spawning, Battle Resolution, Hill Razing, Bot Input/Output, Map Format, Replay Format).
- Переходи: сайт → завантажити бота → матчі на сервері → реплеї; локально: playgame → візуалізатор.

## Фічі поза полем
- `local-referee` — рушій і playgame відкриті, `test_bot`-скрипти й `submission_test` для перевірки бота перед здачею.
- `replay` (JSON `.replay`, стрім `.stream`), `seed-input` (`player_seed`, `engine_seed`).
- `level-from-txt` + генератор карт (`mapgen`), набір офіційних карт.
- `custom-rules` — опції `attack`, `food`, радіуси, `turns`, `cutoff_*`, `kill_points`, `scenario`.
- Серверний турнір із рейтингом за серією матчів (TrueSkill (?)).

## Варіації й родичі
- [bot-arenas.md](bot-arenas.md) — жанр арен ботів: CodinGame, Halite, Battlecode; Ants там одним рядком таблиці.
- [codingame-great-escape.md](codingame-great-escape.md) — той самий протокол «стан → наказ за мс», але один аватар і стінки замість рою.
- [lux-ai.md](lux-ai.md), [screeps.md](screeps.md) — рій юнітів, ресурси й база; [7-billion-humans.md](7-billion-humans.md) — одна програма на всіх.
- AI Challenge до Ants: Tron (2010), Planet Wars (2010) — граф планет (?).
- **Осі варіацій:**
  - бій: focus / support / damage / closest — одна опція рушія, чотири різні тактики;
  - їжа: симетрична / секціями / випадкова; спірна знищується;
  - кінець: ліміт ходів / lone survivor / домінування 85 % / стабілізований ранг;
  - зіткнення своїх: усі гинуть (Ants) / одна лишається (інші арени);
  - інформація: туман у радіусі / повна.

## Цікавинки для курсу
- Тор з евклідовою відстанню «через край» і огляд radius² з обгортанням — 📎.
- Focus-бій: для кожної мурахи — кількість ворогів у радіусі, смерть порівнянням з мінімумом серед ворогів, усі смерті одночасно — 🥇 (легко зробити порядкозалежним і зламати).
- Одночасне застосування наказів: «у клітині >1 мурахи → усі гинуть», накази на їжу/воду блокуються — 🥉.
- Спавн з мурашника, найдавніше торканого, ≤1 за хід; збір їжі лише без конкурентів — 📎.
- Cutoff-и: 85 % популяції 150 ходів, rank stabilized (найкращий/найгірший сценарій очок) — 🥈.
- Суддя + два студентські боти через stdin/stdout з лімітом часу і реплеєм — 🥈: готова лабораторна «турнір ботів».
- Бот: BFS від їжі/ворожих мурашників по тору, розподіл цілей між мурахами, бій групами — 🥇.

## Мапа на каталог
- Є: `command-program` ↔ бот; `move-4dir`; `wrap-edges` ↔ тор; `impassable-cells` ↔ вода; `fog-of-war` ↔ огляд radius²; `spawner-entity` + `spawn-points` ↔ мурашники; `item-pickup` + `collect-quota` ↔ їжа → мурахи; `piece-capture` ↔ бій без HP; `chase-bfs` + `ai-greedy` + `realtime-ai` ↔ стратегії ботів; `move-timer` ↔ turntime; `replay` + `replay-window` ↔ візуалізатор; `level-from-txt` + `maze-generation` + `map-validation` ↔ карти; `rating-system` + `leaderboard`; `state-as-data` ↔ протокол; `fixture-level-tests` ↔ test_bot.
- **Нема** → пропозиції карток (частину вже просив `bot-arenas.md`):
  - `+focus-battle-resolution`, `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+swarm-same-program`, `+local-referee`, `+cutoff-rules`, `+symmetric-map-generation` — уже запропоновані.
  - `+collision-kills-all` «Кілька юнітів в одній клітині — гинуть усі» · entities/death · 📎.
  - `+contested-food-destroyed` «Спірний ресурс знищується» · game-logic/economy · 🌱.
  - `+rank-stabilized-cutoff` «Кінець, коли ранг уже не зміниться» · game-logic/win · 🥈.

## Пропозиції до словників
- `+trigger:timeout(bot)`, `+effect:eliminate(bot)`, `+effect:raze(hill)`, `+cond:count_in_radius(a, kind, r2)`, `+cond:visible(cell)` — уже просив `bot-arenas.md`; тут ще одна гра (правило трьох).
- `+cond:owners_in_radius(cell, r2, n)` — скільки різних власників мають юнітів у радіусі (збір їжі: рівно 1).
- `+card:focus-battle-resolution`, `+card:collision-kills-all`, `+card:contested-food-destroyed`, `+card:rank-stabilized-cutoff` — див. «Мапу на каталог».
- `+ui:vision-overlay` — у реплеї перемикання туману «очима гравця N».

## Джерела
- ⭐ [GitHub: aichallenge/aichallenge](https://github.com/aichallenge/aichallenge) — увесь проєкт: рушій, playgame, карти, генератор, візуалізатор, сайт; розділи специфікації в `website/specification.php` (текст підставляється з окремих md, у фетчі порожній).
- [ants.py](https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/ants.py) — focus (`min_enemy_weakness <= weakness`), support/damage/closest, зіткнення «всі гинуть», накази на їжу/воду блокуються, збір лише без конкурентів, спавн за last_touched, +2/−1, старт = кількість мурашників, бонус lone survivor, cutoff 85 %/150, rank stabilized, огляд з обгортанням, формат w/f/h/a/d.
- [playgame.py](https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/playgame.py) — дефолти: 1000 ходів, 3000/1000 мс, 77/5/1, attack focus, food symmetric, food_rate (5,11), food_turn (19,37), food_start (75,175), food_visible (3,5), kill_points 2; запуск ботів, `--fill`, `--strict`, реплей/HTML.
- [GitHub: ants/](https://github.com/aichallenge/aichallenge/tree/epsilon/ants) — склад теки гри.
- [Wikipedia: AI Challenge](https://en.wikipedia.org/wiki/AI_Challenge) — лише «Ватерлоо, 2009–2011».
- YouTube: пошук «ai challenge ants 2011 replay».

## Непевне
- (?) Що саме робить рушій при таймауті/падінні бота — в ants.py лише `kill_player`; логіка детекту — в іншому модулі (engine), не читав.
- (?) Ліміти часу й параметри на офіційному сервері могли відрізнятися від дефолтів playgame.py; рейтинг TrueSkill — з памʼяті.
- (?) Протокол старту (`ready`/`go`, `player_seed`) і `end` — з памʼяті й з `bot-arenas.md`; ants.py підтверджує формат рядків стану.
- (?) Спавн їжі: ants.py має дефолт `sections`, playgame.py — `symmetric`; що було на сервері — не перевірено.
- (?) Опис сайту-специфікації (сторінка aichallenge.org в архіві) не відкрився — web.archive.org недоступний для фетчу.
