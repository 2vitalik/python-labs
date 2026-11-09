---
title: "Gymnasium Toy Text: FrozenLake, Taxi, CliffWalking"
slug: gymnasium-toy-text
aka: [FrozenLake, FrozenLake-v1, Frozen Lake, Taxi, Taxi-v4, CliffWalking, CliffWalking-v1, Cliff Walking, OpenAI Gym toy text]
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: state
year: 2016
platforms: [Python, Gymnasium]
links:
  - {kind: official, url: "https://gymnasium.farama.org/environments/toy_text/frozen_lake/", best: true, note: "FrozenLake: мапи, дії, слизький лід, нагороди, параметри"}
  - {kind: official, url: "https://gymnasium.farama.org/environments/toy_text/taxi/", note: "Taxi: мапа 5×5, 500 станів, нагороди, is_rainy, fickle_passenger, action_mask"}
  - {kind: official, url: "https://gymnasium.farama.org/environments/toy_text/cliff_walking/", note: "CliffWalking: 4×12, обрив −100, is_slippery"}
  - {kind: other, url: "https://raw.githubusercontent.com/Farama-Foundation/Gymnasium/main/gymnasium/envs/toy_text/frozen_lake.py", note: "код: таблиця переходів P, generate_random_map; поруч taxi.py, cliffwalking.py"}
  - {kind: other, url: "http://www.incompleteideas.net/book/RLbook2020.pdf", note: "Sutton & Barto, приклад 6.6 Cliff Walking"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=frozenlake+taxi+q-learning+gymnasium", note: "пошук; Q-learning на toy text"}
stage: v1
coverage: 80
mechanics: [command-program, move-4dir, impassable-cells, environment-death, reach-exit, item-pickup, event-points, floor-types, respawn, maze-generation, reachability-check, seed-share, rule-variants, level-from-txt, console-render, gui-render, logic-render-split, state-as-data, game-loop, +agent-program-interface, +slippery-move, +transition-table, +state-index-encoding, +reward-per-step, +thin-walls, +action-mask, +step-limit-truncation, +fall-resets-to-start, +passenger-delivery]
proposes: ["+trigger:step_done", "+trigger:truncated(max_steps)", "+effect:reward(r)", "+effect:slip(a, dir)", "+cond:wall_between(a, dir)", "+feature:agent-api", "+feature:transition-model", "+feature:action-mask", "+axis:observation"]
author: opus
date: 2026-11-09
---

# Gymnasium Toy Text — три крихітні сіткові світи для першого навчання агента: слизьке озеро з ополонками, таксі з пасажиром і стежка над обривом

## Суть
Група «Toy Text» бібліотеки Gymnasium (спадкоємиця OpenAI Gym): найпростіші середовища з дискретним станом — одне ціле число — і текстовим рендером. Агент-програма щокроку обирає дію з 4–6 і отримує нагороду; середовище відкриває **таблицю переходів** `P[s][a] = [(p, s′, r, done)]`, тож їх розвʼязують і навчанням (Q-learning), і плануванням (value iteration). Цей файл — огляд трьох сіткових світів: **FrozenLake** (слизький лід: хід у задуманий бік лише з імовірністю 1/3), **Taxi** (забрати й довезти пасажира крізь тонкі стіни) і **CliffWalking** (обрив, що відкидає на старт з −100). Четвертий член групи, Blackjack, не сітковий — тут не описаний.

## Поле і час
- Усі три — квадратна сітка з 4-сусідством, повністю видима (стан = позиція + прапорці), без руху інших сутностей. Тік = крок агента.
- Вихід за край поля неможливий: позиція обрізається, агент стоїть.
- Рендер: `ansi` (текст) і `rgb_array` / `human` (піксель-арт, у FrozenLake 4 кадри/с).

### FrozenLake
- Мапа з рядків `S F H G`: 4×4 (`SFFF / FHFH / FFFH / HFFG`) або 8×8 (`map_name`); власна — `desc=[…]`; випадкова — `generate_random_map(size, p=0.8)` з перевіркою, що шлях S→G існує.
- Стан `row · ncols + col` (4×4 — 16 станів); старт 0, ціль — правий нижній кут.
- Обрізання епізоду: 100 кроків (4×4), 200 (8×8).

### Taxi
- Мапа 5×5 з **тонкими стінами між клітинами** (`|` у тексті) і 4 стоянками R (0,0), G (0,4), Y (4,0), B (4,3).
- Стан `((taxi_row · 5 + taxi_col) · 5 + passenger_location) · 4 + destination` — 500 станів; пасажир 0–3 на стоянці або 4 — у таксі.
- Старт — рівномірно з 300 станів, де пасажир не в таксі й не на місці призначення; обрізання 200 кроків.

### CliffWalking
- Сітка 4×12, старт [3, 0], ціль [3, 11], обрив [3, 1…10] — уся нижня смуга між ними (Sutton & Barto, приклад 6.6).
- Стан `row · 12 + col`, `Discrete(48)`, досяжних 37; без ліміту кроків (v1 ніколи не обрізається).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент (ельф / таксі / пішохід) | player | стан-число | крок у 4 напрямки (Taxi — ще 2 дії) |
| Старт `S` | static | — | клітина старту; у Cliff — точка повернення |
| Лід `F` (FrozenLake) | terrain | `is_slippery`, `success_rate` | крок у задуманий бік з імовірністю `success_rate` (1/3), інакше в один з перпендикулярних порівну |
| Ополонка `H` (FrozenLake) | hazard | — | ступив → кінець епізоду, нагорода 0 |
| Ціль `G` | static | — | ступив → кінець, нагорода 1 (FrozenLake) |
| Обрив (CliffWalking) | hazard | — | ступив → −100 і назад на старт, епізод триває |
| Тонка стіна (Taxi) | static | між двома клітинами | блокує рух схід-захід через ребро |
| Стоянка R / G / Y / B (Taxi) | zone | колір | місце посадки й висадки |
| Пасажир (Taxi) | pickup | місце 0–4, призначення 0–3 | сідає дією pickup на своїй стоянці; висаджується дією dropoff |

## Правила (КОЛИ → ЯКЩО → ТО)
- Спільне: КОЛИ `input(action)` → ТО `custom: «вибір наступного стану з P[s][a] за ймовірностями»`; КОЛИ `tick` → ТО `custom: «крок повертає (obs, reward, terminated, truncated, info)»`.
- Спільне: КОЛИ `input(move)` → ЯКЩО `custom: «наступна клітина поза полем»` → ТО `block` (агент на місці, крок витрачено).

### FrozenLake
- КОЛИ `input(dir)` → ЯКЩО `state(lake, slippery)` → ТО `custom: «з імовірністю success_rate — move(agent, dir), інакше move(agent, dir ± 90°) порівну»`; інакше `move(agent, dir)`.
- КОЛИ `enter(agent, hole)` → ТО `lose`, `custom: «нагорода reward_schedule[1] = 0»`.
- КОЛИ `enter(agent, goal)` → ТО `win`, `custom: «нагорода reward_schedule[0] = 1»`.
- КОЛИ `enter(agent, frozen)` → ТО `custom: «нагорода reward_schedule[2] = 0»`.
- КОЛИ `counter(steps, >=, 100|200)` → ТО `custom: «truncated (обгортка TimeLimit)»`.

### Taxi
- КОЛИ `input(south|north)` → ТО `move(taxi, dir)` (горизонтальних стін на мапі нема).
- КОЛИ `input(east|west)` → ЯКЩО `custom: «між клітинами нема стіни»` → ТО `move(taxi, dir)`; інакше `block`.
- КОЛИ `input(pickup)` → ЯКЩО `custom: «пасажир на стоянці, де стоїть таксі»` → ТО `pickup`; інакше `score(−10)`.
- КОЛИ `input(dropoff)` → ЯКЩО `has(taxi, passenger)` and `custom: «таксі на стоянці призначення»` → ТО `score(+20)`, `win`.
- КОЛИ `input(dropoff)` → ЯКЩО `has(taxi, passenger)` and `custom: «таксі на іншій стоянці»` → ТО `place(taxi, passenger)` на цю стоянку (крок −1, епізод триває).
- КОЛИ `input(dropoff)` → ЯКЩО `custom: «пасажира нема в таксі або таксі не на стоянці»` → ТО `score(−10)`.
- КОЛИ `tick` → ЯКЩО `custom: «не було +20 чи −10»` → ТО `score(−1)` — навіть за крок у стіну.
- `is_rainy=True`: КОЛИ `input(move)` → ТО `custom: «з імовірністю rainy_probability (0.8) — задуманий бік, інакше по (1 − p)/2 у бічні»`; pickup/dropoff детерміновані.
- `fickle_passenger=True`: КОЛИ `custom: «таксі з пасажиром уперше відʼїхало на клітину від стоянки посадки»` → ЯКЩО `prob(0.3)` → ТО `custom: «пасажир міняє призначення (раз за епізод)»`.

### CliffWalking
- КОЛИ `input(dir)` → ЯКЩО `state(cliff, slippery)` → ТО `custom: «по 1/3: dir, dir − 90°, dir + 90°»`; інакше `move(agent, dir)`.
- КОЛИ `enter(agent, cliff)` → ТО `score(−100)`, `respawn(agent, start)` — без кінця епізоду.
- КОЛИ `tick` → ЯКЩО `custom: «крок не в обрив»` → ТО `score(−1)`.
- КОЛИ `enter(agent, goal)` → ТО `win`.
- Перемога: дійти до G / довезти пасажира · Поразка: ополонка (FrozenLake), обрізання за кроками · Рахунок: сума нагород епізоду (FrozenLake — 0 або 1; Taxi — +20 мінус кроки й штрафи; Cliff — мінус кроки й обриви).

## Керування і ввід
- Програмно: `env = gym.make("FrozenLake-v1", map_name="8x8", is_slippery=True)`, `obs, info = env.reset(seed=…)`, `env.step(a)`; таблиця `env.unwrapped.P` — для планування.
- Дії FrozenLake: 0 ← · 1 ↓ · 2 → · 3 ↑. CliffWalking: 0 ↑ · 1 → · 2 ↓ · 3 ←. Taxi: 0 південь · 1 північ · 2 схід · 3 захід · 4 pickup · 5 dropoff.
- `info`: `prob` / `p` — імовірність переходу; у Taxi ще `action_mask` — які дії змінять стан (`env.action_space.sample(info["action_mask"])`).
- Людського керування в комплекті нема — лише код агента.

## Вікна, меню, HUD
- `game-screen` у `human`: піксель-арт — лід з ополонками й ельфом, місто з таксі, стоянками й будинком призначення, стежка з обривом.
- `ansi`: текстова мапа з підсвіченою позицією; у Taxi — рамка `+---------+` і літери стоянок.
- Меню, налаштувань і HUD нема: усе — параметри `gym.make`.

## Фічі поза полем
- Параметри як конструктор варіантів: `desc`, `map_name`, `is_slippery`, `success_rate`, `reward_schedule` (FrozenLake); `is_rainy`, `rainy_probability`, `fickle_passenger`, `fickle_probability` (Taxi); `is_slippery` (Cliff).
- Відтворюваність через `seed`; генератор випадкових озер з гарантованим шляхом.
- Версії середовищ з історією змін (Taxi v0–v4, FrozenLake v0–v1, CliffWalking v0–v1).

## Варіації й родичі
- [minigrid](minigrid.md) — багатші сіткові світи з частковим оглядом і текстовими місіями; [wumpus-world](wumpus-world.md) — агент із сенсорами в печері.
- Gridworld і Cliff Walking з підручника Sutton & Barto; Taxi — з роботи Dietterich 2000 (ієрархічне RL, MAXQ).
- [chips-challenge](../maze-arcade/chips-challenge.md) — лід як ковзання для людини (тут — стохастичний ковзь).
- Осі варіацій: **стохастичність** (детерміновано / слизько 1/3 / дощ 0.8 / примхливий пасажир) · **нагорода** (рідкісна в цілі / −1 за крок / штраф за обрив) · **кінець при помилці** (ополонка — кінець / обрив — на старт) · **стіни** (клітини / тонкі між клітинами).

## Цікавинки для курсу
- Своє «озеро» з `reset/step` і текстовим рендером за 50 рядків — 🌱.
- Слизький рух: розподіл «1/3 прямо, по 1/3 убік» як таблиця переходів — 📎.
- Taxi: кодування стану в одне число й назад (`encode/decode`) — 📎.
- Тонкі стіни між клітинами в мапі з символів `|` і `:` — 📎.
- Value iteration за таблицею `P` і порівняння з Q-learning — 🥈.
- Генератор випадкового озера з перевіркою досяжності (DFS) — 🥉.
- SARSA проти Q-learning на CliffWalking: «безпечна» і «ризикована» стежки — 🥇.

## Мапа на каталог
- Є: `command-program` (агент — програма) · `move-4dir` · `impassable-cells` (тонкі стіни Taxi) · `environment-death` (ополонка) · `reach-exit` · `item-pickup` (пасажир) · `event-points` (+20, −10, −1, −100) · `floor-types` (лід / ополонка / обрив) · `respawn` (обрив → старт) · `maze-generation` (випадкове озеро) · `reachability-check` (гарантований шлях) · `seed-share` · `rule-variants` · `level-from-txt` (мапа з рядків) · `console-render` / `gui-render` / `logic-render-split` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+agent-program-interface` — з [wumpus-world](wumpus-world.md), підтвердження.
  - `+slippery-move` «Хід у задуманий бік з імовірністю p, інакше вбік» · entities/move · 📎.
  - `+transition-table` «Модель світу як таблиця P[s][a]» · code/architecture · 🥉.
  - `+state-index-encoding` «Стан гри — одне ціле число (mixed radix)» · code/architecture · 📎.
  - `+reward-per-step` «Кожен крок −1, щоб квапити» · game-logic/score · 🌱.
  - `+thin-walls` «Стіни на ребрах між клітинами» · entities/legality · 📎.
  - `+action-mask` «Маска дій, що змінять стан» · interface/hud · 🌱.
  - `+step-limit-truncation` — з [minigrid](minigrid.md), підтвердження.
  - `+fall-resets-to-start` «Пастка повертає на старт зі штрафом, без кінця гри» · entities/interact · 🌱.
  - `+passenger-delivery` «Забрати сутність в одній зоні й висадити в іншій» · game-logic/goals · 📎.

## Пропозиції до словників
- `+trigger:step_done`, `+trigger:truncated(max_steps)`, `+effect:reward(r)` — підтвердження з minigrid / wumpus-world.
- `+effect:slip(a, dir)` — стохастичне зміщення вбік від задуманого.
- `+cond:wall_between(a, dir)` — тонка стіна на ребрі клітини в напрямку руху.
- `+feature:agent-api` — підтвердження; `+feature:transition-model` — середовище віддає повну модель переходів; `+feature:action-mask`.
- `+axis:observation` — тут `state-index` (одне число) — підтвердження з minigrid.

## Джерела
- ⭐ [FrozenLake — Gymnasium](https://gymnasium.farama.org/environments/toy_text/frozen_lake/) — мапи 4×4 і 8×8, дії, `success_rate`, `reward_schedule`, обрізання 100/200.
- [Taxi — Gymnasium](https://gymnasium.farama.org/environments/toy_text/taxi/) — мапа, 500 станів, 300 стартів, нагороди +20/−10/−1, `is_rainy`, `fickle_passenger`, `action_mask`, історія версій.
- [CliffWalking — Gymnasium](https://gymnasium.farama.org/environments/toy_text/cliff_walking/) — 4×12, обрив, −100, приклад 6.6.
- [frozen_lake.py](https://raw.githubusercontent.com/Farama-Foundation/Gymnasium/main/gymnasium/envs/toy_text/frozen_lake.py) і сусідні `taxi.py`, `cliffwalking.py` — таблиці переходів, висадка на чужій стоянці без кінця епізоду, слизький Cliff «по 1/3», `generate_random_map`.
- [Sutton & Barto, RL: An Introduction (2020)](http://www.incompleteideas.net/book/RLbook2020.pdf) — першоджерело Cliff Walking.

## Непевне
- (?) Рік 2016 — вихід OpenAI Gym; чи FrozenLake і Taxi були в першому релізі, а CliffWalking додано пізніше, — не перевірено.
- (?) Коли зʼявився параметр `success_rate` — не перевірено; `reward_schedule` — з Gymnasium v1.3 (історія версій сторінки).
- (?) Обрізання 100/200 для FrozenLake і 200 для Taxi — з реєстрації `TimeLimit`; у власних мапах ліміт задає користувач.
