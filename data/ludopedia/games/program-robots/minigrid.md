---
title: MiniGrid (з BabyAI)
slug: minigrid
aka: [Minigrid, gym-minigrid, BabyAI, Farama Minigrid]
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: both
  goal: state
year: 2018
platforms: [Python, Gymnasium]
links:
  - {kind: official, url: "https://minigrid.farama.org/", best: true, note: "документація Farama: списки середовищ Minigrid / BabyAI / WFC, обгортки, API"}
  - {kind: other, url: "https://github.com/Farama-Foundation/Minigrid", note: "код: minigrid_env.py (step, reward), core/world_object.py (обʼєкти), envs/babyai/core/verifier.py (місії)"}
  - {kind: other, url: "https://github.com/mila-iqia/babyai", note: "оригінальний BabyAI (Mila), звідки взято мовні рівні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=minigrid+babyai+reinforcement+learning", note: "пошук; агенти в DoorKey, BabyAI"}
stage: v1
coverage: 70
mechanics: [command-program, move-4dir, orientation-state, facing-icon, impassable-cells, key-and-door, item-pickup, inventory-limit, environment-death, touch-death, reach-exit, random-walk, fog-of-war, dungeon-generation, maze-generation, reachability-check, seed-share, difficulty-levels, rule-variants, keyboard-controls, console-render, gui-render, logic-render-split, state-as-data, game-loop, objective-text, +agent-program-interface, +percept-vector, +egocentric-view, +occlusion-by-walls, +text-mission, +mission-verifier, +reward-decay-by-steps, +step-limit-truncation, +box-reveals-content, +wfc-level-generation, +observation-wrappers]
proposes: ["+trigger:step_done", "+trigger:truncated(max_steps)", "+effect:toggle(a)", "+effect:reward(r)", "+cond:can_overlap(cell)", "+cond:matches_mission(a)", "+ui:mission-text", "+ui:view-highlight", "+feature:agent-api", "+feature:observation-wrappers", "+feature:env-registry", "+axis:observation"]
author: opus
date: 2026-11-09
---

# MiniGrid — сітковий світ для навчання агентів на Python: трикутник-агент бачить 7×7 перед собою, носить один предмет, відмикає двері ключем свого кольору й виконує текстові місії BabyAI

## Суть
Бібліотека простих сіткових середовищ для навчання з підкріпленням (раніше `gym-minigrid`, зараз Farama Foundation, API Gymnasium). «Гравець» — програма-агент: на кожному кроці отримує спостереження (картинку 7×7 перед собою, напрям і **текст місії**) і повертає одну з 7 дій; середовище повертає винагороду. Набір: десятки середовищ Minigrid (DoorKey, FourRooms, LavaCrossing, Dynamic Obstacles, Memory, KeyCorridor, ObstructedMaze…) і понад сотню рівнів BabyAI з синтетичною англійською мовою: «put the red ball next to the blue key», «open the door on your left, then go to a box». Суть для курсу — чиста модель «стан → дія → нагорода» на сітці з дверима, ключами, ящиками й лавою.

## Поле і час
- Квадратна сітка з периметром стін; розмір задається параметром середовища (5×5…16×16 і більше; BabyAI — кімнати `room_size`, сітки кімнат з дверима).
- Агент стоїть у клітині й дивиться в один з 4 напрямків (0 → праворуч, 1 → вниз, 2 → ліворуч, 3 → вгору).
- Тік = крок: одна дія агента; динамічні перешкоди ходять у тому ж кроці.
- Часткове спостереження: квадрат `agent_view_size` (типово 7, непарний ≥ 3) перед агентом, повернутий так, що агент «дивиться вгору»; стіни й зачинені двері затуляють, що за ними (`see_through_walls=False`). Повний огляд — обгортка `FullyObsWrapper`.
- Генерація: кожен `reset(seed)` будує рівень заново (розстановка, кольори, місія); те саме зерно — той самий рівень.
- Ліміт `max_steps` (базово 100; у BabyAI — кількість навігацій × `room_size²` × кімнат); вичерпано — епізод обрізається (`truncated`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | player | позиція, напрям 0–3, `carrying` (≤ 1 предмет) | повертає, йде вперед, бере/кладе/вмикає клітину перед собою |
| Стіна | static | колір | непрохідна, непрозора |
| Підлога (floor) | terrain | колір | прохідна (зафарбована клітина) |
| Двері | gate | колір; open / closed / locked | відчинені — прохідні й прозорі; зачинені — `toggle` відчиняє; замкнені — лише з ключем того ж кольору |
| Ключ | pickup | колір | береться в руку; відмикає двері свого кольору, лишається в руці |
| Куля (ball) | object | колір | береться й кладеться; у Dynamic Obstacles — рухома перешкода |
| Ящик (box) | container | колір, вміст | береться; `toggle` — ящик зникає, на його місці вміст (або порожньо) |
| Ціль (goal) | static | зелена | агент входить → успіх |
| Лава | hazard | — | агент входить → кінець епізоду з нулем |
| Рухома перешкода | enemy | куля | щокроку стрибає у випадкову вільну клітину свого 3×3; зіткнення → −1 і кінець |

Кольори: red, green, blue, purple, yellow, grey. Кодування клітини в спостереженні — трійка `(OBJECT_IDX, COLOR_IDX, STATE)`: unseen 0, empty 1, wall 2, floor 3, door 4, key 5, ball 6, box 7, goal 8, lava 9, agent 10; стани дверей open 0 / closed 1 / locked 2.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left)` / `input(right)` → ТО `face(agent, dir ∓ 90°)`.
- КОЛИ `input(forward)` → ЯКЩО `free(front_cell)` or `custom: «клітина перекривна: підлога, ціль, лава, відчинені двері»` → ТО `move(agent, facing)`; інакше `block` (крок усе одно витрачено).
- КОЛИ `enter(agent, goal)` → ТО `win`, `custom: «нагорода 1 − 0.9 · step_count / max_steps»`.
- КОЛИ `enter(agent, lava)` → ТО `lose` (нагорода 0).
- КОЛИ `input(pickup)` → ЯКЩО `occupied(front_cell, key|ball|box)` and `not has(agent, item)` → ТО `pickup` — клітина спорожніє.
- КОЛИ `input(drop)` → ЯКЩО `free(front_cell)` and `has(agent, item)` → ТО `place(agent, item)` у клітину попереду.
- КОЛИ `input(toggle)` → ЯКЩО `state(door, locked)` and `has(agent, key)` and `same(key, door, color)` → ТО `set_state(door, open)`; без відповідного ключа — нічого.
- КОЛИ `input(toggle)` → ЯКЩО `state(door, closed)` or `state(door, open)` → ТО `set_state(door, flip)`.
- КОЛИ `input(toggle)` → ЯКЩО `occupied(front_cell, box)` → ТО `transform(box, contents)`.
- КОЛИ `input(done)` → ТО нічого в Minigrid; у BabyAI з `BABYAI_DONE_ACTIONS` — `win`, лише якщо попередній крок виконав місію, інакше `lose`.
- КОЛИ `tick` → ТО `reveal(view_7x7)`, `custom: «спостереження {image, direction, mission}; тіні від стін і зачинених дверей»`.
- КОЛИ `counter(step_count, >=, max_steps)` → ТО `custom: «truncated — обрізання з нагородою 0»`.
- Dynamic Obstacles: КОЛИ `tick` → ТО `move(obstacle, rng)` у межах 3×3; КОЛИ `input(forward)` → ЯКЩО `occupied(front_cell, obstacle|wall)` → ТО `lose`, `custom: «нагорода −1»`.
- Fetch: КОЛИ `picked(agent, object)` → ЯКЩО `same(object, mission, color_and_type)` → ТО `win`; інакше `lose`.
- PutNear / BabyAI PutNext: КОЛИ `custom: «агент поклав обʼєкт»` → ЯКЩО `in_range(moved_object, target_object, 1)` → ТО `win`.
- BabyAI GoTo: КОЛИ `tick` → ЯКЩО `custom: «обʼєкт з опису місії — у клітині попереду»` → ТО `win`.
- BabyAI Open: КОЛИ `input(toggle)` → ЯКЩО `custom: «відчинено двері з опису»` → ТО `win`; у strict-рівнях відчинено інші двері → `lose`.
- BabyAI послідовності: `custom: «A, then B» — B зараховується лише після A; «A after you B» — навпаки; «A and B» — обидва в будь-якому порядку`; порушення порядку → `lose`.
- Memory: КОЛИ `enter(agent, end_of_hallway)` → ЯКЩО `same(object_there, object_in_start_room, type)` → ТО `win`; інакше `lose` (дія pickup тут = toggle).
- KeyCorridor / ObstructedMaze: КОЛИ `picked(agent, target_ball)` → ТО `win`; ключі сховані в ящиках, двері затулені кулями.
- Перемога: виконати місію · Поразка: лава, рухома перешкода, неправильний предмет/порядок · Рахунок: нагорода `1 − 0.9 · кроки / max_steps` (швидше — більше), інакше 0.

## Керування і ввід
- Для агента: `Discrete(7)` — 0 left, 1 right, 2 forward, 3 pickup, 4 drop, 5 toggle, 6 done; API `env = gym.make("MiniGrid-DoorKey-8x8-v0")`, `obs, info = env.reset(seed=…)`, `obs, reward, terminated, truncated, info = env.step(action)`.
- Для людини (`manual_control.py`): ← / → — поворот, ↑ — вперед, Space — toggle, PageUp або Tab — pickup, PageDown або Left Shift — drop, Enter — done, Backspace — новий епізод, Esc — вихід.
- Діє лише на клітину **попереду**: усі взаємодії «через ніс», а не наступанням.

## Вікна, меню, HUD
- `game-screen` (render_mode `human`, вікно pygame «minigrid»): уся сітка, агент-трикутник за напрямком, підсвічена зона огляду агента (`view-highlight`), під полем — текст місії (`mission-text`).
- Режим `rgb_array` — кадр для запису; `agent_pov=True` — рендер лише того, що бачить агент.
- Текстовий вигляд `pprint_grid` / `str(env)`: двосимвольні клітини (`W` стіна, `D` двері, `L` замкнені, `K` ключ, `A` куля, `B` ящик, `G` ціль, `V` лава + літера кольору; агент `>>`, `VV`, `<<`, `^^`).
- Меню нема: вибір середовища — рядком id в коді чи аргументом `--env-id`.

## Фічі поза полем
- Реєстр середовищ Gymnasium: `MiniGrid-*` і `BabyAI-*` з розмірами в назві (`DoorKey-5x5`…`16x16`, `KeyCorridorS3R1`…`S6R3`, `LavaCrossingS9N1`…`S11N5`) — `difficulty-levels` і основа для curriculum.
- Обгортки спостережень і дій: `FullyObs`, `ImgObs`, `RGBImgObs`, `RGBImgPartialObs`, `OneHotPartialObs`, `SymbolicObs`, `FlatObs`, `ViewSize`, `DirectionObs`, `DictObservationSpace`; `StochasticAction` (випадкова дія з імовірністю), `NoDeath`, `ActionBonus` і `PositionBonus` (бонуси за новизну), `ReseedWrapper` (фіксовані зерна).
- WFC-середовища: рівні, згенеровані wave function collapse за шаблонами (лабіринти, підземелля, кімнати).
- `seed` для відтворення; бенчмарк швидкості `benchmark.py`; `manual_control.py` для гри руками.

## Варіації й родичі
- [wumpus-world](wumpus-world.md) — класичний «агент + сприйняття» на сітці; [gymnasium-toy-text](gymnasium-toy-text.md) — найпростіші табличні світи; [karel](karel.md) — програма замість політики.
- Miniworld — те саме в 3D від тих самих авторів; BabyAI — мовні рівні від Mila, тепер усередині Minigrid.
- [chips-challenge](../maze-arcade/chips-challenge.md) — ключі-двері-ящики як аркада для людини.
- Осі варіацій: **спостереження** (егоцентричне вікно / повна мапа / символьне / пікселі) · **місія** (фіксована / текстова з композицією «then / after / and») · **дії** (поворот + вперед / 4 напрямки) · **випадковість** (лише генерація / рухомі перешкоди / стохастична дія) · **нагорода** (рідкісна за ціль / бонуси за новизну).

## Цікавинки для курсу
- Своє середовище з `reset()/step()` і стіною-дверима-ключем у кілька класів (`WorldObj.can_overlap / can_pickup / toggle`) — 📎.
- Егоцентричне вікно 7×7 з поворотом і тінями від стін — 🥉.
- Текстова місія: граматика BabyAI (GoTo / Open / Pickup / PutNext + «then / after / and») і верифікатор, що стежить за подіями — 🥈.
- Бот-планувальник для DoorKey / KeyCorridor: BFS з підцілями «ключ → двері → ціль», ящик як схованка ключа — 🥉.
- Табличний Q-learning на `MiniGrid-Empty-5x5` з графіком навчання — 🥈.
- Генерація кімнат із замкненими дверима, де ключ гарантовано досяжний (перевірка досяжності на графі кімнат) — 🥈.
- Генерація рівнів WFC за зразком — 🥇.

## Мапа на каталог
- Є: `command-program` (агент — програма) · `move-4dir` · `orientation-state` · `facing-icon` (трикутник) · `impassable-cells` · `key-and-door` (колір до кольору, ключ не витрачається) · `item-pickup` · `inventory-limit` (рука на 1 предмет) · `environment-death` (лава) · `touch-death` (рухома перешкода) · `reach-exit` · `random-walk` · `fog-of-war` (вікно огляду) · `dungeon-generation`, `maze-generation` · `reachability-check` · `seed-share` · `difficulty-levels` · `rule-variants` (параметри конструктора) · `keyboard-controls` · `console-render` / `gui-render` / `logic-render-split` · `state-as-data` · `game-loop` · `objective-text`.
- **Нема** → пропозиції карток:
  - `+agent-program-interface`, `+percept-vector` — з [wumpus-world](wumpus-world.md), підтвердження.
  - `+egocentric-view` «Огляд у системі координат агента, повернутий за напрямком» · interface/render · 🥉.
  - `+occlusion-by-walls` «Непрозорі клітини затуляють, що за ними» · interface/render · 🥉.
  - `+text-mission` «Мета рівня — згенерований текст» · levels/generation · 📎.
  - `+mission-verifier` «Перевірка складеної місії за подіями (then / after / and)» · game-logic/goals · 🥈.
  - `+reward-decay-by-steps` «Нагорода за успіх тим менша, чим довше йшов» · game-logic/score · 🌱.
  - `+step-limit-truncation` «Епізод обрізається після N кроків» · game-logic/goals · 🌱.
  - `+box-reveals-content` «Відкритий контейнер замінюється вмістом» · entities/interact · 🌱.
  - `+wfc-level-generation` «Рівень з wave function collapse за зразком» · levels/generation · 🥇.
  - `+observation-wrappers` «Один світ — кілька форм спостереження» · code/architecture · 🥉.

## Пропозиції до словників
- `+trigger:step_done` — крок середовища завершено (з wumpus-world, підтвердження).
- `+trigger:truncated(max_steps)` — вичерпано ліміт кроків без перемоги й поразки.
- `+effect:toggle(a)` — «увімкнути» клітину попереду: двері, ящик, перемикач (одна дія з різним ефектом за типом).
- `+effect:reward(r)` — нагорода агентові (не очки гравця: може бути дробовою й залежати від кроків).
- `+cond:can_overlap(cell)` — у клітину можна стати, хоч вона й не порожня (ціль, лава, відчинені двері).
- `+cond:matches_mission(a)` — сутність відповідає опису з тексту місії.
- `+ui:mission-text` — рядок місії під полем; `+ui:view-highlight` — підсвічена зона огляду агента.
- `+feature:agent-api` — підтвердження; `+feature:observation-wrappers`; `+feature:env-registry` — середовища за рядковим id з параметрами в назві.
- `+axis:observation` — `full / egocentric / symbolic / pixels`.

## Джерела
- ⭐ [minigrid.farama.org](https://minigrid.farama.org/) — опис, списки середовищ (23 Minigrid, ~39 BabyAI, ~24 WFC), обгортки, приклад API.
- [Farama-Foundation/Minigrid](https://github.com/Farama-Foundation/Minigrid) — `minigrid_env.py` (крок, нагорода, огляд, рендер, `pprint_grid`), `core/actions.py`, `core/world_object.py`, `core/constants.py`, `envs/*.py` (докстрінги середовищ і місій), `envs/babyai/core/verifier.py`, `manual_control.py`, `wrappers.py`, `README.md` (історія: gym-minigrid, Mila, NeurIPS 2023).
- [mila-iqia/babyai](https://github.com/mila-iqia/babyai) — першоджерело мовних рівнів (посилання з README).

## Непевне
- (?) Рік 2018 — з цитування BabyAI (`chevalier2018babyai`) у README; точна дата першого `gym-minigrid` не перевірена.
- (?) `max_steps` конкретних середовищ (DoorKey, FourRooms тощо) не переписано — кожне задає своє.
- (?) RedBlueDoors: чи відчинення синіх дверей першими — поразка, — з докстрінга лише «відчинити червоні, потім сині».
- (?) Кількість середовищ на сайті (23 / ~39 / ~24) — з підсумку сторінки, не перелічено поштучно.
