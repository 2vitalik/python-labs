---
title: Terminal (Correlation One)
slug: terminal-correlation-one
aka: [Terminal, C1 Terminal, C1Games Terminal]
family: program-robots
also: [tower-lanes]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: none
  goal: score
year: 2018
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/correlation-one/C1GamesStarterKit", best: true, note: "стартовий набір: python-algo, gamelib, engine.jar, game-configs.json, скрипти локальних матчів"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/game-configs.json", note: "характеристики юнітів, ресурси, розпад бітів, ліміти часу"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/game_state.py", note: "де можна ставити, SP/MP, project_future_MP, find_path_to_edge"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/game_map.py", note: "ромб 28×28, чотири краї по 14 клітин, евклідова дальність + getHitRadius"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/navigation.py", note: "BFS до краю, «ідеальна» клітина для самознищення, зигзаг-тайбрейк"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/algocore.py", note: "протокол stdin/stdout: конфіг, turnInfo 0/1/2, два рядки відповіді"}
  - {kind: other, url: "https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/algo_strategy.py", note: "стартова стратегія: турелі, перехоплювачі, лінія демолішерів, реакція на прориви"}
  - {kind: official, url: "https://terminal.c1games.com/rules", note: "сторінка правил (рендериться JS; автоматично прочитав лише опис)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=terminal+c1games+algo+gameplay", note: "пошук"}
stage: v1
coverage: 65
mechanics: [tower-placement, tower-range, hp-damage, explode-area, chase-bfs, enemy-reached-base, round-currency, replay, leaderboard, state-as-data, game-loop, ai-greedy, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +local-referee, +diamond-board, +edge-deploy-only, +own-half-placement, +decaying-currency, +income-ramp, +structure-upgrade, +removal-refund, +mobile-stacking, +path-to-opposite-edge, +zigzag-tiebreak, +self-destruct-if-stuck, +breach-damage-player, +action-frames-feed]
proposes: ["+cond:in_zone(a, zone)", "+effect:decay(a, n)", "+effect:upgrade(a)", "+effect:refund(a, pct)", "+trigger:timeout(bot)", "+window:playground", "+window:replay-viewer", "+feature:bot-upload"]
author: opus
date: 2026-11-09
---

# Terminal — tower defense, де обидві сторони — алгоритми: ставиш стіни й турелі за ядра, кидаєш юніти за біти, що тануть щораунду

## Суть
Змагальна гра Correlation One для програмістів: дві програми («алго») щораунду одночасно будують укріплення на своїй половині ромбоподібного поля й випускають мобільні юніти з власних країв. Юніти самі йдуть найкоротшим шляхом до протилежного краю, бʼються з турелями й юнітами суперника, а кожен, хто дійшов, знімає з суперника 1 HP. Укріплення стоять до руйнування, а «мобільна» валюта тане на чверть щораунду — накопичувати для потужної атаки дорого. Хто перший обнулив HP суперника або мав більше HP наприкінці — виграв.

## Поле і час
- Сітка 28×28, обрізана до **ромба**: рядок y < 14 має клітини x ∈ [13 − y, 14 + y], нижня половина — симетрично; верх і низ по 2 клітини, середина — 28.
- Чотири краї-діагоналі по 14 клітин: `BOTTOM_LEFT`, `BOTTOM_RIGHT` (свої), `TOP_LEFT`, `TOP_RIGHT` (суперника). Юніт з нижнього лівого краю йде до верхнього правого і навпаки.
- Своя територія — y < 14; суперник бачить поле віддзеркаленим так само (кожен «знизу»).
- Раунд: **фаза розгортання** (обидва алго одночасно шлють build і deploy) → **фаза дії** — послідовність кадрів, у яких юніти рухаються й стріляють, доки рух не завершиться; кадри транслюються алго (`on_action_frame`).
- Дальність — евклідова: ціль у радіусі `range + getHitRadius` (0.01).
- Інформація повна (видно всі структури й ресурси суперника), але накази обох приховані до виконання.

## Сутності
| Сутність | Роль | Параметри (config стартового набору) | Поведінка |
|---|---|---|---|
| Стіна (Wall; у config — Filter `FF`) | static | 1 SP, HP 75 → 150 після апгрейду | блокує шлях, поглинає вогонь |
| Підтримка (Support; Encryptor `EF`) | static | 7 SP, HP 30; у config — `generatesResource1: 1`, апгрейд `generatesResource2: 2` | у config — дає ресурс (?); у gamelib є поля щита `shieldPerUnit`, `shieldRange`, `shieldBonusPerY` |
| Турель (Turret; Destructor `DF`) | tower | 2 SP, HP 90, шкода юнітам 5, дальність 2.5 → апгрейд +4 SP: дальність 3.5, шкода 15 | стріляє лише по мобільних |
| Скаут (Scout; Ping `PI`) | piece | 1 MP, HP 15, швидкість 1, шкода 2/2, дальність 3.5 | швидкий, бʼє і юнітів, і структури |
| Демолішер (Demolisher; EMP `EI`) | piece | 3 MP, HP 5, швидкість 0.5, шкода 6/6, дальність 4.5 | далекобійний руйнівник структур |
| Перехоплювач (Interceptor; Scrambler `SI`) | piece | 1 MP, HP 40, швидкість 0.25, шкода юнітам 20 | повільний мисливець на юніти, структур не бʼє |
| Remove (`RM`) | — | повернення 75 %, 1 хід | дія: позначити свою структуру на зняття |
| Upgrade (`UP`) | — | ціна апгрейда | дія: замінити характеристики структури |
| Гравець | player | HP 40, SP 40, MP 5 на старті | втрачає HP за кожен прорив |
| Край (edge) | zone | 14 клітин | свої — місця спавну мобільних; чужі — ціль |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «рушій шле алго JSON-конфіг гри (юніти, ресурси, ліміти)»`.
- КОЛИ `turn_start` → ТО `custom: «стан turnInfo[0] = 0; алго друкує 2 рядки: список build, потім список deploy»`.
- КОЛИ `input(spawn structure, cell)` → ЯКЩО `custom: «клітина в ромбі й на своїй половині, y < 14»` and `free(cell)` and `has(player, SP ≥ ціна)` → ТО `place(player, structure)`, `currency(−ціна SP)`.
- КОЛИ `input(spawn mobile, cell, n)` → ЯКЩО `custom: «клітина на своєму нижньому краю»` and `not occupied(cell, structure)` and `has(player, MP ≥ n·ціна)` → ТО `place(player, mobile ×n)`; мобільні можуть стояти купою в одній клітині.
- КОЛИ `input(remove, cell)` → ЯКЩО `occupied(cell, own_structure)` → ТО `custom: «через 1 хід структура зникає, повертається 75 % ціни»`.
- КОЛИ `input(upgrade, cell)` → ЯКЩО `occupied(cell, own_structure)` and `has(player, SP ≥ ціна апгрейда)` → ТО `set_state(structure, upgraded)` — характеристики замінюються, поточне HP лишається.
- КОЛИ `phase_start(action)` → ТО `custom: «кожен мобільний юніт отримує шлях BFS до протилежного краю»`.
- КОЛИ `tick` (кадр) → ЯКЩО `custom: «минуло 1/speed кадрів з останнього кроку»` → ТО `move(unit, next_on_path)`.
- КОЛИ `custom: «рівних за довжиною сусідів кілька»` → ТО `custom: «після горизонтального кроку — вертикальний і навпаки; за однакового — до цільового краю»` (зигзаг).
- КОЛИ `destroyed(structure)` → ТО `custom: «шляхи всіх юнітів перераховуються»`.
- КОЛИ `custom: «до краю шляху нема»` → ТО `custom: «юніт іде до найглибшої досяжної клітини в бік цілі»`.
- КОЛИ `tick` → ЯКЩО `in_range(unit, enemy, range)` → ТО `damage(enemy, dmg)`: турель і перехоплювач — лише по мобільних, скаут і демолішер — і по структурах.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`.
- КОЛИ `reach(mobile, enemy_edge)` → ТО `damage(enemy_player, 1)`, `disappear(mobile)`; `custom: «подія breach у кадрі»`; config: `coresForPlayerDamage 1` — +1 SP атакувальнику (?).
- КОЛИ `blocked(mobile)` (дійшов до «ідеальної» клітини, далі не можна) → ЯКЩО `counter(steps, >=, 5)` → ТО `explode(radius 1.5, n = selfDestructDamage, —)` (скаут 15, демолішер 5, перехоплювач 40); менше 5 кроків — просто зникає.
- КОЛИ `turn_end` → ТО `currency(SP +5)`; `custom: «MP ×(1 − 0.25), потім + 5 + ⌊хід / 10⌋, максимум 150»`.
- КОЛИ `custom: «алго не відповів за waitTimeBotMax (35 с)»` → ТО `custom: «поразка або пропуск ходу (?)»`.
- КОЛИ `hp_zero(player)` → ТО `lose` для нього, `win` для суперника.
- КОЛИ `custom: «ліміт раундів вичерпано»` → ТО `game_over`: більше HP → `win` (?).
- Перемога: HP суперника = 0 або більше HP наприкінці · Поразка: власне HP = 0 · Рахунок: HP гравців, далі рейтинг.

## Керування і ввід
- Ввід — програма-алго (Python-стартер `python-algo/algo_strategy.py`; є інші мови в спільноті); завантажується на сайт тека мови, не весь набір.
- Протокол: рядок конфігу (містить `replaySave`) → `on_game_start(config)`; рядки з `turnInfo`: `0` — хід (`on_turn`), `1` — кадр фази дії (`on_action_frame`), `2` — кінець гри.
- `gamelib`: `attempt_spawn`, `attempt_remove`, `attempt_upgrade`, `can_spawn`, `get_resource`, `project_future_MP`, `find_path_to_edge`, `get_attackers`, `submit_turn` (обовʼязково наприкінці, інакше алго «висне»).
- Локально: `engine.jar` (Java 10+), скрипти `scripts/test_algo_[OS]`; ручна гра — Playground на сайті.

## Вікна, меню, HUD
- `playground` — ручна гра на тому самому полі (ставиш юніти мишею) для перевірки ідей.
- `replay-viewer` — матчі по кадрах; події breach, damage, death, spawn (?).
- `leaderboard` і сторінка змагань (сезони, призи, вакансії); статистика платформи: ~70 000 гравців, 13 млн матчів.
- HUD (?): HP обох гравців, SP і MP, номер раунду, кадр фази дії.
- Переходи: завантажити алго → матчі з рейтинговими суперниками → реплеї → нова версія.

## Фічі поза полем
- `bot-upload` (тека алго), автоматичні рейтингові матчі, `leaderboard-online`, турніри з призами.
- `local-referee`: `engine.jar` + `game-configs.json` — повний локальний матч, реплей у файл (`replaySave`).
- Сезонні зміни правил (назви юнітів і баланс змінювались: Filter → Wall, Ping → Scout тощо).
- Ліміти: `waitTimeBotMax` 35 000 мс, `waitTimeBotSoft` 5 000 мс, старт гри 3 000 мс.

## Варіації й родичі
- Сітковий TD з лабіринтом із веж — [desktop-tower-defense](../tower-lanes/desktop-tower-defense.md), [fieldrunners](../tower-lanes/fieldrunners.md), [mazing-td-modern](../tower-lanes/mazing-td-modern.md); дуель «вежі + юніти суперника» — [legion-td](../tower-lanes/legion-td.md).
- Арени ботів сімʼї: [bot-arenas](bot-arenas.md), [lux-ai](lux-ai.md), [codingame-great-escape](codingame-great-escape.md) (стіни, що подовжують шлях суперника).
- Осі варіацій: **економіка** (стабільний дохід структур / валюта, що тане, з рампою); **шлях** (BFS з перерахунком / фіксовані доріжки); **застряг** (самознищення / стоїть); **апгрейд** (заміна характеристик / рівні); **черговість** (одночасне розгортання / по черзі).

## Цікавинки для курсу
- Симулятор Terminal: ромб, свої краї, розгортання, кадри руху за швидкістю, стрілянина в радіусі — 🥈.
- Шлях до протилежного краю BFS з перерахунком після руйнування і зигзаг-тайбрейком — 🥉.
- Самознищення застряглого юніта лише після 5 кроків — 📎.
- Економіка «MP ×0.75 + рампа» і `project_future_MP` для планування атаки через N раундів — 📎.
- Бот, що симулює фазу дії для кількох варіантів розгортання й обирає найкращий — 🥇.
- Реакція на прориви: ставити турель над клітиною, де пробили, — 🌱.

## Мапа на каталог
- Є: `tower-placement` · `tower-range` · `hp-damage` · `explode-area` (самознищення радіусом 1.5) · `chase-bfs` (шлях до краю) · `enemy-reached-base` (прорив) · `round-currency` (SP/MP) · `replay` · `leaderboard` · `state-as-data` · `game-loop` · `ai-greedy` (стартова стратегія).
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+local-referee` — з [bot-arenas](bot-arenas.md).
  - `+diamond-board` «Поле-ромб у квадратних координатах» · levels/format · 🌱.
  - `+edge-deploy-only` «Мобільні — лише з клітин свого краю» · entities/legality · 🌱.
  - `+own-half-placement` «Будувати лише на своїй половині» · entities/legality · 🌱.
  - `+decaying-currency` «Валюта тане на % щораунду» · game-logic/economy · 🌱.
  - `+income-ramp` «Дохід росте кожні N раундів» · game-logic/economy · 🌱.
  - `+structure-upgrade` «Апгрейд замінює характеристики структури» · game-logic/economy · 📎.
  - `+removal-refund` «Зняти структуру з частковим поверненням» · game-logic/economy · 🌱.
  - `+mobile-stacking` «Кілька мобільних юнітів в одній клітині» · entities/legality · 🌱.
  - `+path-to-opposite-edge` «Юніт іде до протилежного краю, а не до точки» · entities/move · 📎.
  - `+zigzag-tiebreak` «Рівні шляхи: чергувати горизонталь і вертикаль» · entities/move · 🌱.
  - `+self-destruct-if-stuck` «Застряг після N кроків — вибух» · entities/combat · 📎.
  - `+breach-damage-player` «Юніт на чужому краю знімає HP гравця» · game-logic/win · 🌱.
  - `+action-frames-feed` «Бот отримує кожен кадр симуляції» · code/architecture · 📎.

## Пропозиції до словників
- `+cond:in_zone(a, zone)` — своя половина, свій край (спільне з robot-rumble).
- `+effect:decay(a, n)` — MP тане на 25 % (спільне з battlesnake).
- `+effect:upgrade(a)` — структура отримує набір апгрейд-характеристик.
- `+effect:refund(a, pct)` — зняти й повернути частину ціни.
- `+trigger:timeout(bot)` — підтвердження.
- `+window:playground` — ручна пісочниця на полі змагання ботів.
- `+window:replay-viewer` · `+feature:bot-upload` — підтвердження.

## Джерела
- ⭐ [C1GamesStarterKit](https://github.com/correlation-one/C1GamesStarterKit) — README, склад набору, запуск локальних матчів, Playground.
- [game-configs.json](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/game-configs.json) — усі числа юнітів, ресурсів і таймінгів.
- [game_state.py](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/game_state.py) — правила розміщення, SP/MP, формула MP.
- [game_map.py](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/game_map.py) — ромб, краї, дальність; [navigation.py](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/navigation.py) — пошук шляху, зигзаг, «ідеальна» клітина.
- [algocore.py](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/gamelib/algocore.py) — протокол; [algo_strategy.py](https://raw.githubusercontent.com/correlation-one/C1GamesStarterKit/master/python-algo/algo_strategy.py) — стартова стратегія й breach-події.
- [terminal.c1games.com/rules](https://terminal.c1games.com/rules) — лише опис і статистика (повні правила рендеряться JS).

## Непевне
- (?) `game-configs.json` у репо — зі старого сезону (назви Filter/Encryptor/Destructor/Ping/EMP/Scrambler), а gamelib уже вживає Wall/Support/Turret/Scout/Demolisher/Interceptor; живий сезон може мати інший баланс (напр., Support як щит для юнітів, а не дохід).
- (?) Пріоритет вибору цілі турелями й юнітами (найближча / найслабша / найглибше) — з памʼяті, у gamelib не знайшов.
- (?) Ліміт раундів, тайбрейк і наслідок таймауту — не бачив у відкритих файлах.
- (?) Рік старту (2018) і значення `coresForPlayerDamage`/`metalForBreach` (бонус SP за прорив) — не перевірено.
- (?) Повернення при знятті: 75 % — з config; чи залежить від HP структури — невідомо.
