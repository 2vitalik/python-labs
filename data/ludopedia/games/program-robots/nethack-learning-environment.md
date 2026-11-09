---
title: NetHack Learning Environment (NLE, MiniHack)
slug: nethack-learning-environment
aka: [NLE, MiniHack, NetHack Challenge, nle, minihack]
family: program-robots
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: score
year: 2020
platforms: [Linux, macOS, Python (gym / Gymnasium), Docker]
links:
  - {kind: official, url: "https://github.com/facebookresearch/nle", best: true, note: "README: що таке NLE, встановлення, gym.make, nle-play, агент TorchBeast, датасет NLD; проєкт переїхав на github.com/heiner/nle"}
  - {kind: official, url: "https://github.com/heiner/nle", note: "нове місце NLE (з README)"}
  - {kind: other, url: "https://raw.githubusercontent.com/facebookresearch/nle/main/nle/env/tasks.py", note: "завдання й нагороди: Score, Staircase, Pet, Oracle, Gold, Eat, Scout, Challenge; штраф за «застиглі» кроки"}
  - {kind: other, url: "https://arxiv.org/abs/2006.13760", note: "стаття NeurIPS 2020 (анотація)"}
  - {kind: official, url: "https://github.com/facebookresearch/minihack", note: "MiniHack: пісочниця рівнів на des-файлах поверх NLE; переїхав на github.com/samvelyan/minihack"}
  - {kind: other, url: "https://minihack.readthedocs.io/en/latest/envs/index.html", note: "каталог середовищ MiniHack: навігація, навички, перенесені MiniGrid/Boxoban/Sokoban"}
  - {kind: other, url: "https://minihack.readthedocs.io/en/latest/getting-started/des_files.html", note: "формат des-файлів: MAP, REGION, MONSTER, OBJECT, TRAP, IF[50%], кубики, SHUFFLE"}
  - {kind: play, url: "https://minihack-editor.github.io", note: "редактор рівнів MiniHack у браузері (з README)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rog-O-Matic", note: "предок: експертна система 1981, що грала Rogue з ASCII-екрана"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=oYSNXTkeCtw", note: "інтервʼю W&B з авторами NLE (лінк з README)"}
stage: v1
coverage: 60
mechanics: [move-8dir, fog-of-war, dungeon-generation, maze-generation, stairs-levels, item-identification, hunger-clock, permadeath, inventory, inventory-items, key-and-door, push-object, environment-death, touch-death, level-from-txt, seed-share, keyboard-controls, console-render, gui-render, replay, ai-random, state-as-data, game-loop, +agent-program-interface, +step-limit-truncation, +egocentric-view, +observation-wrappers, +action-subset, +auto-skip-prompts, +reward-from-score-delta, +frozen-step-penalty, +no-progress-abort, +level-description-dsl, +reward-event-manager, +ttyrec-recording, +offline-dataset]
proposes: ["+trigger:step_done", "+trigger:truncated(max_steps)", "+effect:reward(r)", "+feature:agent-api", "+feature:observation-wrappers", "+feature:env-registry", "+axis:observation", "+trigger:prompt_shown(kind)", "+feature:level-dsl"]
author: opus
date: 2026-11-09
---

# NetHack Learning Environment — NetHack як gym-середовище: Python-агент щокроку обирає клавішу, а MiniHack дає збирати власні міні-рівні з des-файлів

## Суть
NLE (Facebook AI Research, NeurIPS 2020) — форк NetHack 3.6.6 з Python-інтерфейсом gym: `env.step(action)` натискає одну клавішу, повертає спостереження (карта гліфів 21×79, рядок статусу, повідомлення, інвантар, увесь термінал 24×80) і нагороду за обране **завдання**. Сама гра — у [nethack](../roguelike/nethack.md); тут описано шар «агент ↔ гра»: простір дій, спостереження, нагороди, кінець епізоду. MiniHack (NeurIPS 2021) — пісочниця поверх NLE: рівень пишеться des-файлом або `LevelGenerator`, нагорода — `RewardManager`, і з одного рушія виходять лабіринти, ріки з валунами, лава, вовкулаки й порти MiniGrid та Boxoban. Ідейний предок — Rog-O-Matic (1981), експертна система, що вигравала Rogue, читаючи ASCII-екран.

## Поле і час
- Карта NetHack — 21 × 79 клітин, кожна — гліф (0…5991: монстр, предмет, рельєф, улюбленець); поруч символ, колір і спецпрапорці; плюс термінал 24 × 80 з рядком повідомлень і статусом.
- Рух у 8 напрямках; кроки рушія = натиснуті клавіші, а **ігровий час** іде не завжди (меню, `--More--`, питання не забирають ходу).
- Підземелля процедурне: кожен `reset()` генерує нове; туман — бачиш лише освітлене й запамʼятоване.
- Епізод обривається на 5000 кроках (`max_episode_steps`, статус ABORTED), на смерті (DEATH) або на успіху завдання (TASK_SUCCESSFUL).
- MiniHack: малі мапи з `MAP … ENDMAP` у центрі екрана; опційно egocentric-обрізка 9 × 9 навколо агента (`*_crop`) і піксельне спостереження (16 × 16 × 3 на клітину).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент `@` | player | `blstats` (25 чисел: координати, HP, рівень, голод, золото, час…), інвантар до 55 слотів | керується індексом дії; помирає назавжди |
| Монстри | enemy | гліф, назва | власна поведінка NetHack; в MiniHack ставляться des-файлом |
| Улюбленець | ally | гліф `pet` | ходить слідом, бʼється; потрібен для StaircasePet |
| Оракул | neutral | гліф «Oracle» | ціль завдання NetHackOracle (стати поруч) |
| Сходи вниз `>` | static | — | ціль Staircase і типова ціль MiniHack |
| Предмети | pickup | клас, буква в інвантарі, невідома назва | їсти, вдягати, тримати, читати, пити, зап з жезла |
| Золото `$` | pickup | кількість | нагорода в NetHackGold (автопідбір) |
| Двері | gate | відчинені / зачинені / замкнені | відчинити `OPEN`, вибити `KICK`, ключем |
| Валун | object | — | штовхається; у MiniHack-River засипає воду |
| Вода, лава | hazard | — | смерть або загроза; Lava Crossing вимагає левітації/заморозки (?) |
| Пастки, фонтан, раковина, вівтар | terrain | тип | ставляться `LevelGenerator` (`add_trap`, `add_sink`, `add_fountain`, `add_altar`) |

## Правила (КОЛИ → ЯКЩО → ТО)
Шар середовища NLE:
- КОЛИ `input(i)` → ТО `custom: «i → ASCII-код клавіші зі списку actions → крок рушія NetHack»`; для завдань — 23 дії (`MORE`, 8 напрямків, 8 «далеких» напрямків, `<`, `>`, `.`, `KICK`, `EAT`, `SEARCH`).
- КОЛИ `custom: «гра показала --More--, меню або y/n-питання»` → ЯКЩО `not mode(allow_all_modes)` → ТО `custom: «середовище саме тисне пробіл / ESC, крім дозволених питань»`.
- КОЛИ `turn_end` → ТО `score(Δ)` — у NetHackScore нагорода = зміна внутрішнього рахунку гри.
- КОЛИ `turn_end` → ЯКЩО `custom: «ігровий час не зрушив (застиглий крок)»` → ТО `score(−0.01)` (режим штрафу `constant`; є `exp`, `square`, `linear`, `always`).
- КОЛИ `enter(agent, stair_down)` → ТО `win` (NetHackStaircase: +1, кінець епізоду).
- КОЛИ `enter(agent, stair_down)` → ЯКЩО `adjacent_count(agent, pet, >=, 1)` → ТО `win` (NetHackStaircasePet).
- КОЛИ `adjacent(agent, oracle)` → ТО `win` (NetHackOracle).
- КОЛИ `picked(agent, gold)` → ТО `score(+Δgold)` (NetHackGold; автопідбір лише `$`).
- КОЛИ `custom: «рівень ситості зріс (їжа)»` → ТО `score(+Δ)` (NetHackEat); КОЛИ `custom: «на карті відкрились нові клітини»` → ТО `score(+нові клітини)` (NetHackScout).
- КОЛИ `died(agent)` → ТО `game_over` (DEATH).
- КОЛИ `counter(steps, >=, 5000)` → ТО `custom: «гра примусово завершується, статус ABORTED»`.
- NetHackChallenge: КОЛИ `counter(steps, >=, 1 000 000)` або `custom: «ігровий час не змінювався 10 000 кроків»` → ТО ABORTED; повна клавіатура, `--More--` не пропускається, персонаж випадковий, зміна seed заборонена.

Шар MiniHack:
- КОЛИ `level_start` → ТО `custom: «des-файл компілюється в рівень: MAP, REGION, MONSTER, OBJECT, TRAP, DOOR, STAIR; IF[50%], кубики NdM, SHUFFLE, rndcoord — випадковість на кожен reset»`.
- КОЛИ `enter(agent, stair_down)` (типова ціль) → ТО `win`, `score(+1)` (`reward_win`); смерть — `score(0)` (`reward_lose`), `penalty_step` −0.01.
- КОЛИ `custom: «спрацювала подія RewardManager: eat / wield / wear / amulet / kill / message / positional / coordinate / location»` → ТО `score(+reward)`; ЯКЩО `custom: «усі події з terminal_required виконано»` → ТО `win`.
- КОЛИ `contact(agent, boulder)` → ЯКЩО `cell(front, water)` → ТО `push(boulder)`, `disappear(boulder)`, `set_cell(front, floor)` (MiniHack-River) (?).
- Перемога: виконати завдання (сходи, оракул, події) або, у Challenge, «вознестися» з Амулетом · Поразка: смерть, ABORTED · Рахунок: зміна внутрішнього рахунку NetHack або сума нагород завдання.

## Керування і ввід
- Програмно: `env = gym.make("NetHackScore-v0")` / `gym.make("MiniHack-River-v0")`, `env.reset()`, `env.step(i)`, `env.render()`; параметри `observation_keys`, `actions`, `max_episode_steps`, `character` (типово `mon-hum-neu-mal`), `savedir`, `save_ttyrec_every`.
- Повний простір — 98 дій NLE (16 напрямків + 82 команди), MiniHack-навички — 75; навігаційні — 8 напрямків + `OPEN`, `KICK`, `SEARCH` (за бажанням `EAT`). Частина команд «авторегресивні»: `PUTON` → предмет → рука.
- Людина: `nle-play` / `python -m nle.scripts.play` (термінал), `mh-play`, `mh-guiplay` (GUI), `--mode random` — випадковий агент.
- Базові агенти: TorchBeast (`nle.agent`, `minihack.agent.polybeast`), RLlib (`algo=dqn`), обгортка мови `nle-language-wrapper` (текст ↔ дії).

## Вікна, меню, HUD
- `game-screen` = термінал NetHack 24 × 80: рядок повідомлень, карта, два рядки статусу (`blstats`); в обрізаних спостереженнях — вікно 9 × 9 навколо агента.
- Внутрішні вікна гри (інвантар, меню, питання, `--More--`) — частина спостереження; NLE їх або пропускає, або віддає агенту.
- `editor-window`: MiniHack Level Editor у браузері — drag-and-drop клітин, експорт des-файлу.
- `replay-window`: ttyrec-записи епізодів; датасети NLD (`nld-aa`, `nld-nao`) завантажуються як `TtyrecDataset`.
- Графік навчання `nle.scripts.plot` — ASCII-крива середньої нагороди.

## Фічі поза полем
- `agent-api`: стандартний gym/Gymnasium-цикл, реєстр середовищ (`register(id=…)`), власні класи `MiniHackNavigation` / `MiniHackSkill`.
- `observation-wrappers`: вибір ключів спостереження (`glyphs`, `chars`, `colors`, `specials`, `screen_descriptions`, `pixel`, `blstats`, `message`, `inv_*`, `tty_*`, `*_crop`).
- `level-dsl`: des-файли з випадковістю + `LevelGenerator` (`add_object`, `add_monster`, `add_trap`, `add_door`, `add_boulder`, `fill_terrain`, `add_mazewalk`, `set_start_pos`, `add_goal_pos`) + `RewardManager` (`add_eat_event`, `add_kill_event`, `add_location_event`, `add_custom_reward_fn`).
- `seed-input` (крім Challenge), `ttyrec`-запис, Docker-образи, `offline-dataset` NLD для навчання з демонстрацій.

## Варіації й родичі
- Гра всередині — [nethack](../roguelike/nethack.md); предок за ідеєю «бот читає ASCII-екран роглайка» — Rog-O-Matic (1981, CMU), що за три тижні 1983 мав медіану вищу за 15 найкращих гравців CMU і знаходив Амулет (Wikipedia).
- Інші gym-сітки корпусу: [minigrid](minigrid.md) (MiniHack переносить її завдання), [gymnasium-toy-text](gymnasium-toy-text.md), [wumpus-world](wumpus-world.md); Boxoban у MiniHack — [sokoban](../push-slide/sokoban.md).
- Пов'язані середовища з README: gym_nethack, rogueinabox, rogue-gym, CoinRun, MineRL, Procgen, Obstacle Tower.
- Осі варіацій: **простір дій** (8 напрямків / 23 / 75 / 98 клавіш); **спостереження** (гліфи / символи / пікселі / текст / обрізка); **нагорода** (рахунок / подія / золото / дослідження); **рівні** (повна гра / des-файл / генератор).

## Цікавинки для курсу
- Обгортка «гра → середовище»: `reset/step/render`, словник спостережень, статус кінця епізоду — 📎.
- Парсер міні-des-файлу (`MAP`, `MONSTER`, `OBJECT`, `IF[50%]`) у власну клітинну гру — 🥉.
- `RewardManager`: події з нагородою й прапорцем «обовʼязкова для кінця» — 📎.
- Штраф «застиглих» кроків і обрив «без прогресу» як захист від зациклення агента — 🌱.
- Бот на правилах для MiniHack-Room/Corridor: BFS по видимій карті, пошук прихованих дверей `SEARCH` — 🥈.
- Rog-O-Matic-подібна експертна система, що читає 24 × 80 і грає справжній роглайк — 👑.

## Мапа на каталог
- Є: `move-8dir` · `fog-of-war` · `dungeon-generation` · `maze-generation` (`MAZEWALK`, MazeWalk) · `stairs-levels` · `item-identification` · `hunger-clock` · `permadeath` · `inventory`, `inventory-items` · `key-and-door` (KeyRoom, замкнені двері) · `push-object` (валуни River) · `environment-death` (лава, вода) · `touch-death` · `level-from-txt` (`MAP … ENDMAP`) · `seed-share` · `keyboard-controls` (`nle-play`) · `console-render` · `gui-render` (`mh-guiplay`, пікселі) · `replay` (ttyrec) · `ai-random` (`--mode random`) · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+agent-program-interface`, `+step-limit-truncation`, `+egocentric-view`, `+observation-wrappers` — з [minigrid](minigrid.md).
  - `+action-subset` «Обрізаний набір дій під завдання (8 напрямків + 3 команди)» · code/architecture · 🌱.
  - `+auto-skip-prompts` «Середовище саме проходить меню й --More--» · code/architecture · 📎.
  - `+reward-from-score-delta` «Нагорода = приріст внутрішнього рахунку гри» · game-logic/score · 🌱.
  - `+frozen-step-penalty` «Штраф за кроки, що не рухають ігровий час» · game-logic/score · 🌱.
  - `+no-progress-abort` «Обрив епізоду, якщо N кроків нема прогресу» · game-logic/lose · 🌱.
  - `+level-description-dsl` «Рівень описується мовою з випадковістю (des-файл)» · levels/format · 🥈.
  - `+reward-event-manager` «Нагороди як список подій з прапорцем обовʼязковості» · game-logic/score · 📎.
  - `+ttyrec-recording` «Запис терміналу епізоду для повтору» · interface/results · 📎.
  - `+offline-dataset` «Датасет записаних ігор для навчання агентів» · code/architecture · 🥉.

## Пропозиції до словників
- `+trigger:step_done` · `+trigger:truncated(max_steps)` · `+effect:reward(r)` · `+feature:agent-api` · `+feature:observation-wrappers` · `+feature:env-registry` · `+axis:observation` — підтвердження з minigrid / gymnasium-toy-text.
- `+trigger:prompt_shown(kind)` — гра показала меню / питання / `--More--` (рішення: віддати агенту чи пропустити).
- `+feature:level-dsl` — мова опису рівнів з випадковістю (des-файли NetHack/MiniHack).

## Джерела
- ⭐ [facebookresearch/nle](https://github.com/facebookresearch/nle) — README (сирий файл): база NetHack 3.6.6, NeurIPS 2020, `gym.make`, `nle-play`, TorchBeast, NLD, переїзд на heiner/nle.
- [nle/env/tasks.py](https://raw.githubusercontent.com/facebookresearch/nle/main/nle/env/tasks.py) і `nle/env/base.py` — завдання, нагороди, `TASK_ACTIONS`, 5000 кроків, `StepStatus`, Challenge (1e6 кроків, 10 000 без прогресу).
- [arXiv 2006.13760](https://arxiv.org/abs/2006.13760) — анотація статті NLE.
- [facebookresearch/minihack](https://github.com/facebookresearch/minihack) — README, `docs/getting-started` (інтерфейс, нагороди, спостереження, 75/98 дій), `level_generator.py`, `reward_manager.py`.
- [MiniHack: середовища](https://minihack.readthedocs.io/en/latest/envs/index.html) і [des-файли](https://minihack.readthedocs.io/en/latest/getting-started/des_files.html) — каталог завдань і синтаксис.
- [Wikipedia: Rog-O-Matic](https://en.wikipedia.org/wiki/Rog-O-Matic) — 1981, CMU, «belligerent expert system», тест 1983.

## Непевне
- (?) Механіка MiniHack-River (валун у воді стає сушею) і Lava Crossing (левітація/заморозка) — каталог каже лише «переправа штовханням валунів» і «перетин лави»; деталі — з памʼяті про NetHack.
- (?) Результати NeurIPS 2021 NetHack Challenge (символьні боти випередили нейромережі) — з памʼяті, сторінки не відкривав; у коді є лише клас `NetHackChallenge`.
- (?) Кількість гліфів 5991 і розміри спостережень — з документації MiniHack (NetHack 3.6.6); у новіших версіях NLE (heiner/nle) могли змінитись.
- (?) Швидкість середовища (кроків за секунду) — не бачив у відкритих джерелах.
