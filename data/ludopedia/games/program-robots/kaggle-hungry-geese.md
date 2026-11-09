---
title: Kaggle Hungry Geese
slug: kaggle-hungry-geese
aka: [Hungry Geese, hungry_geese, Голодні гуси]
family: program-robots
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: both
  goal: survive
year: 2021
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/hungry_geese", best: true, note: "тека середовища: код правил, json-конфіг, візуалізатор (HTML GitHub не відкрився — 504; сирі файли нижче)"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/hungry_geese/hungry_geese.py", note: "інтерпретатор кроку: розворот, їжа, самозіткнення, голод, гістограма зіткнень, нагорода; GreedyAgent; ASCII-рендер"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/hungry_geese/hungry_geese.json", note: "11×7, hunger_rate 40, min_food 2, max_length 99, 200 кроків, 1 с на хід + 60 с запасу"}
  - {kind: other, url: "https://www.kaggle.com/competitions/hungry-geese", note: "сторінка змагання (рендериться JS; прочитано лише заголовок)"}
  - {kind: other, url: "https://speakerdeck.com/hoxomaxwell/kaggle-hungry-geese", note: "слайди рішення 3-го місця (серпень 2021), бачив у результатах пошуку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaggle+hungry+geese", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 75
mechanics: [move-4dir, body-queue, self-collision, wrap-edges, hunger-clock, spawn-random-cell, touch-death, ai-greedy, ai-random, replay, leaderboard, console-render, state-as-data, game-loop, +simultaneous-hidden-orders, +turn-time-limit, +time-bank, +local-referee, +collect-then-apply-eliminations, +head-to-head-both-die, +reverse-move-kills, +food-min-count, +length-cap, +survival-time-reward]
proposes: ["+trigger:timeout(bot)", "+effect:eliminate(bot)", "+cond:reverse_of(dir, last_dir)", "+effect:trim_tail(a, n)", "+window:replay-viewer"]
author: opus
date: 2026-11-09
---

# Kaggle Hungry Geese — змійка для чотирьох ботів на торі 11×7: кожні 40 ходів голод відкушує хвіст, розворот і лоб у лоб убивають

## Суть
Kaggle-симуляція 2021 року: Python-функція `agent(obs, config)` щокроку повертає один із чотирьох напрямків для своєї гуски. Гуски — це змійки на маленькому торі: їжа подовжує, а **голод** раз на 40 кроків забирає по сегменту, тож стояти на місці довжиною не вийде. Розворот на 180°, врізання в себе, у чуже тіло чи лоб у лоб — смерть. Нагорода кодує **час виживання**, а за рівного часу — довжину, тож мета — пережити суперників, а не наїстися. Рамку Kaggle-арен (сабміт, рейтинг, реплеї) див. у [kaggle-kore-fleets](kaggle-kore-fleets.md).

## Поле і час
- Квадратне поле `columns × rows` = 11 × 7 за замовчуванням (мінімум 3 × 3) — **тор**: вихід за край → протилежний бік.
- Клітина кодується одним числом `row · columns + column`; гуска — список таких позицій, голова — перша.
- Старт: голова кожної гуски у випадковій різній клітині, довжина 1; їжа — у випадкових вільних клітинах.
- Крок: усі агенти відповідають одночасно → рушій по черзі індексів рухає кожну гуску (розворот, їжа, самозіткнення, ліміт довжини, голод) → потім **разом** перевіряє зіткнення голів з усіма сегментами → доповнює їжу до мінімуму.
- Епізод — до 200 кроків (`episodeSteps`); `actTimeout` 1 с на хід, `remainingOverageTime` 60 с запасу на перевищення.
- Інформація повна: видно всіх гусей і всю їжу; випадковість — у старті й появі їжі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гуска (голова + тіло) | player | індекс агента, список позицій, остання дія | щокроку голова на 1 клітину; тіло — черга, хвіст знімається, якщо не їла |
| Сегмент тіла | static | належить гусці | непрохідний для всіх голів (смерть при вході), зникає з хвоста |
| Їжа | pickup | позиція | гуска, що зайшла головою, росте на 1 |
| Голод | — (таймер) | `hunger_rate` = 40 | на кожному 40-му кроці кожна гуска втрачає сегмент хвоста |
| Ліміт довжини | — | `max_length` = 99 | довша гуска обрізається з хвоста |
| Вбудовані агенти | enemy | `random`, `greedy` | суперники для тестів (див. «Керування») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «агент отримує obs: geese (списки позицій), food, index, step, remainingOverageTime»`.
- КОЛИ `input(NORTH|EAST|SOUTH|WEST)` → ЯКЩО `custom: «дія протилежна дії попереднього кроку»` → ТО `disappear(goose)`, `lose` для агента (статус DONE).
- КОЛИ `input(dir)` → ТО `move(head, dir)`, `wrap(head)` — нова голова за модулем `rows`/`columns`.
- КОЛИ `enter(head, food)` → ТО `disappear(food)`, `grow(goose, 1)` — хвіст цього кроку не знімається; інакше `custom: «знімається один сегмент хвоста»`.
- КОЛИ `contact(head, own_body)` → ТО `disappear(goose)`, `lose` (перевіряється одразу при русі цієї гуски).
- КОЛИ `counter(length, >=, 99)` → ТО `custom: «знімати хвіст, доки довжина < max_length, і лише тоді додати голову»`.
- КОЛИ `timer(40)` (крок ділиться на `hunger_rate`) → ТО `grow(goose, −1)` для кожної живої гуски.
- КОЛИ `counter(length, ==, 0)` (після голоду) → ТО `disappear(goose)`, `lose`.
- КОЛИ `phase_start(collisions)` → ЯКЩО `custom: «клітину голови займає ще хоч один сегмент будь-якої гуски»` → ТО `disappear(goose)`, `lose` — зіткнення **лоб у лоб** вбиває обох, врізання в чуже тіло — нападника.
- КОЛИ `custom: «агент у статусі ERROR, INVALID або TIMEOUT»` → ТО `disappear(goose)`.
- КОЛИ `phase_start(food)` → ЯКЩО `count(food, <, 2)` → ТО `spawn_at(food, «випадкова клітина без гусей і їжі»)`, доки їжі не стане `min_food`.
- КОЛИ `turn_end` → ЯКЩО `state(agent, ACTIVE)` → ТО `custom: «reward = (кроків + 1) · (max_length + 1) + довжина»` — гуска, що загинула цього кроку, нагороди за нього не отримує.
- КОЛИ `counter(active_geese, ==, 1)` → ТО `custom: «останню гуску переведено в DONE»`, `game_over`.
- КОЛИ `counter(step, ==, 200)` → ТО `game_over`.
- Перемога: найбільша остання нагорода — хто прожив довше, а серед рівних — довший · Поразка: розворот, самозіткнення, чуже тіло, лоб у лоб, голодна смерть, помилка або таймаут · Рахунок: `кроки·100 + довжина`.

## Керування і ввід
- Агент — функція Python `agent(obs, config)` → рядок `"NORTH"`, `"EAST"`, `"SOUTH"` або `"WEST"` (за замовчуванням NORTH).
- Хелпери середовища: `Action` з `opposite()` і `to_row_col()`, `row_col(position, columns)`, `translate(position, direction, columns, rows)` (з обгортанням), `adjacent_positions(...)`, класи `Observation` і `Configuration`.
- Вбудовані суперники: `"random"` і `"greedy"` — `GreedyAgent` не розвертається, уникає клітин тіл і клітин поруч із чужими головами, серед решти бере хід, що найбільше скорочує мангеттенську відстань до їжі; без безпечних ходів — випадковий.
- Локально — `kaggle_environments.make("hungry_geese")`, `env.run([...])`, рендер у ноутбуці.

## Вікна, меню, HUD
- `replay-viewer` — HTML-візуалізатор середовища (`visualizer/default/dist/index.html` або `hungry_geese.js`): поле, гуски кольорами, їжа, номер кроку (?).
- Текстовий рендер — сітка з `+---`/`|`, `F` — їжа, цифра — індекс гуски на кожному її сегменті.
- `leaderboard` Kaggle і сторінка сабмішнів з епізодами (?).

## Фічі поза полем
- `bot-upload` (Kaggle submission), автоматичні матчі, `leaderboard-online` з рейтингом.
- `local-referee`: відкрите середовище `kaggle-environments`, конфіг змінюється (розмір, `hunger_rate`, `min_food`, `max_length`), до 8 слотів агентів у json.
- `time-bank`: 1 с на хід + 60 с запасу (`remainingOverageTime`).
- Нема undo/pause — лише покроковий реплей.

## Варіації й родичі
- [battlesnake](battlesnake.md) — та сама ідея змійок-ботів, але лоб у лоб виграє **довша**, голод — лічильник здоровʼя 100, є зони-шкідники; тут — голод за календарем і смерть обох.
- Класика: [snake](../maze-arcade/snake.md), [nibbler](../maze-arcade/nibbler.md); арени з «тілом-стіною» — Tron у [bot-arenas](bot-arenas.md), [tron-light-cycles](../maze-arcade/tron-light-cycles.md).
- Інші Kaggle-симуляції корпусу: [kaggle-kore-fleets](kaggle-kore-fleets.md), [lux-ai](lux-ai.md), [kaggle-crawl](kaggle-crawl.md).
- Осі варіацій: **голод** (за календарем / лічильник здоровʼя / нема); **лоб у лоб** (обидва гинуть / довший виграє); **розворот** (смерть / заборонено / ігнор); **нагорода** (виживання / довжина / їжа); **поле** (тор / стіни).

## Цікавинки для курсу
- Рушій кроку з чергою-тілом, тором, голодом і доповненням їжі — 🌱.
- Зіткнення через гістограму позицій після руху всіх (лоб у лоб = обидва) — 📎: учить «спершу всі рухаються, потім рахуємо».
- `GreedyAgent`: фільтр небезпечних клітин (тіла, сусіди чужих голів, розворот) + жадібна відстань до їжі — 📎.
- Flood fill «скільки клітин мені лишиться» як оцінка ходу — 🥉.
- Пошук на кілька кроків з одночасними ходами 4 гравців (paranoid / MCTS) — 🥇.
- Навчання з підкріпленням або імітацією на реплеях — 👑.

## Мапа на каталог
- Є: `move-4dir` · `body-queue` (тіло-черга) · `self-collision` (смерть) · `wrap-edges` (тор) · `hunger-clock` (раз на 40 кроків −1 сегмент) · `spawn-random-cell` (їжа) · `touch-death` (чуже тіло) · `ai-greedy`, `ai-random` (вбудовані агенти) · `replay` · `leaderboard` · `console-render` (ASCII-рендер) · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+simultaneous-hidden-orders`, `+turn-time-limit`, `+local-referee` — з [bot-arenas](bot-arenas.md); `+time-bank` — з [kaggle-kore-fleets](kaggle-kore-fleets.md); `+collect-then-apply-eliminations` — з [battlesnake](battlesnake.md).
  - `+head-to-head-both-die` «Лоб у лоб гинуть обидва» · entities/move · 🌱 (пара до `+head-to-head-length-wins`).
  - `+reverse-move-kills` «Розворот на 180° — смерть, а не заборона» · entities/legality · 🌱.
  - `+food-min-count` «Їжа доповнюється до мінімуму на полі» · entities/spawn · 🌱.
  - `+length-cap` «Довжина тіла обмежена, надлишок відрізається» · entities/state · 🌱.
  - `+survival-time-reward` «Нагорода = час виживання, довжина — тай-брейк» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:timeout(bot)` · `+effect:eliminate(bot)` · `+window:replay-viewer` — підтвердження з арен.
- `+cond:reverse_of(dir, last_dir)` — дія протилежна попередній (Hungry Geese, Snake, Battlesnake).
- `+effect:trim_tail(a, n)` — зняти N сегментів з хвоста (голод, ліміт довжини, Battlesnake-шкода).

## Джерела
- ⭐ [kaggle-environments/envs/hungry_geese](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/hungry_geese) — тека середовища (HTML-сторінка GitHub дала 504, читав сирі файли).
- [hungry_geese.py](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/hungry_geese/hungry_geese.py) — порядок кроку, гістограма зіткнень, голод `len(steps) % hunger_rate == 0`, нагорода, `GreedyAgent`, хелпери, ASCII-рендер.
- [hungry_geese.json](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/hungry_geese/hungry_geese.json) — конфіг, схеми спостереження й дії.
- [Kaggle: Hungry Geese](https://www.kaggle.com/competitions/hungry-geese) — сторінка змагання (лише заголовок).
- [Speaker Deck: Kaggle Hungry Geese](https://speakerdeck.com/hoxomaxwell/kaggle-hungry-geese) — розбір 3-го місця (з результатів пошуку: серпень 2021, «4 гуски на полі 7×11»).

## Непевне
- (?) Точні дати змагання (2021 — за слайдами серпня 2021 і arXiv-статтею вересня 2021 у результатах пошуку), кількість гусей у рейтингових матчах — 4 за чергою й пошуком, у json слотів до 8.
- (?) Як саме ранжується матч на Kaggle (за останньою нагородою — так у коді; чи рахуються нічиї рівних нагород — не бачив).
- (?) Перший крок: розворот перевіряється відносно поточної дії, тож на кроці 1 він неможливий — за переказом коду.
- (?) Гуска, що загинула раніше в циклі (розворот/самозіткнення), уже знята з поля й не блокує інших у перевірці зіткнень — висновок із порядку коду.
- (?) Вигляд HTML-візуалізатора й HUD — не відкривав.
