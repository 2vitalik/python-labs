---
title: Pac-Man Capture the Flag (UC Berkeley CS188)
slug: pacman-capture-the-flag
aka: [Pacman Capture the Flag, Pacman CTF, Pacman Conquer the Flag, capture.py, Пакмен: захоплення прапора]
family: program-robots
also: [maze-arcade]
klass: figure
axes:
  field: square
  time: programmed
  opponent: ai
  info: partial
  random: both
  goal: score
year: 2009
platforms: [PC (Python 3), local CLI]
links:
  - {kind: official, url: "https://github.com/aig-upf/pacman-contest", best: true, note: "шаблон контесту на Python 3 з кодом гри (capture.py, baseline_team), README з атрибуцією Berkeley"}
  - {kind: other, url: "https://raw.githubusercontent.com/aig-upf/pacman-contest/main/src/contest/capture.py", note: "уся механіка: половини, перетворення привид↔пакмен, їжа й повернення, капсули 40 ходів, висипання їжі, сонар ±6, зір 5, ліміти часу, 1200 ходів"}
  - {kind: other, url: "https://github.com/ssardina-teaching/pacman-contest", note: "скрипт турнірів RMIT/UniMelb: коло всіх з усіма, 3/1/0 очок, фіксовані й випадкові мапи, HTML-таблиця"}
  - {kind: other, url: "https://rpl.cs.utexas.edu/cs343h_fall2024/ctf.html", note: "UT Austin 2024 — правила прозою (варіант з повною видимістю)"}
  - {kind: other, url: "https://github.com/aig-upf/pacman-agent", note: "шаблон команди: my_team.py, CaptureAgent.choose_action, запуск проти baseline_team"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pacman+capture+the+flag+contest", note: "пошук; реплеї турнірів"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, item-pickup, temporary-modes, respawn, touch-death, drop-on-death, fog-of-war, chase-bfs, ai-greedy, move-timer, level-from-txt, maze-generation, seed-share, keyboard-controls, console-render, gui-render, replay, leaderboard, state-as-data, game-loop, +agent-program-interface, +home-away-role-switch, +carry-and-deposit, +noisy-distance-sensor, +team-shared-vision, +time-warning-forfeit, +round-robin-tournament, +mirrored-halves, +return-quota-win]
proposes: ["+cond:on_home_side(a)", "+effect:deposit(a, items)", "+effect:sense(percepts)", "+effect:scatter(items, area)", "+trigger:timeout(bot)", "+feature:agent-api", "+feature:tournament-runner"]
author: opus
date: 2026-11-09
---

# Pac-Man Capture the Flag — дві команди Python-агентів на одній мапі: удома ти привид-захисник, на чужій половині — пакмен, що несе їжу додому

## Суть
Фінальний проєкт-контест курсу UC Berkeley CS188 (і клонів у RMIT, UniMelb, UPF, UT Austin): мапа-лабіринт ділиться навпіл на червону й синю половини, у кожної команди по два агенти. Агент на своїй половині — **привид**, що зʼїдає ворожих пакменів; перейшовши межу, він стає **пакменом** і збирає ворожу їжу, але очки зараховуються лише коли він **донесе** її назад. Спійманий пакмен висипає ношу на мапу й відроджується на старті; зʼївши ворожу капсулу, команда лякає ворожих привидів на 40 ходів. Супротивники видимі лише поруч, інакше — шумна відстань, тому агенти мусять стежити за ворогом імовірнісно.

## Поле і час
- Мапа-лабіринт з `.lay`-файла (фіксовані `defaultCapture`, `contest05Capture`…) або випадкова `RANDOM<seed>` (генератор лабіринтів); червоні — ліва половина (`x < width // 2`), сині — права.
- Їжа (зазвичай 60 точок, завжди 60 на випадкових мапах) і капсули — на обох половинах; команда їсть лише чужу.
- Чотири агенти ходять **по черзі** (порядок індексів), кожен хід — один крок `North/South/East/West/Stop`.
- Гра триває до 1200 ходів агентів (`-i/--time`) або до перемоги поверненням їжі.
- Видимість: позицію ворога видно, лише якщо він у межах 5 клітин (Мангеттен) від будь-якого агента команди; інакше — сонар: відстань + рівномірний шум із [−6, 6].

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент-привид (удома) | piece | команда, старт, `scared_timer` | патрулює свою половину; доторк до ворожого пакмена — той відроджується |
| Агент-пакмен (у гостях) | piece | `num_carrying`, `num_returned` | їсть ворожу їжу й капсули; перетин межі додому зараховує ношу |
| Їжа (точка) | pickup | половина | пакмен підбирає в ношу |
| Капсула | pickup | половина | лякає всіх ворожих агентів на 40 ходів |
| Наляканий привид | piece | `scared_timer` > 0 | доторк пакмена відправляє **привида** на старт |
| Стіна | static | — | непрохідна |
| Межа половин | zone | `x = width // 2` | перетин змінює роль агента |
| Стартова клітина | static | одна на агента | місце відродження |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(agent)` → ТО `custom: «агент отримує make_observation: стан гри, де далекі вороги приховані, і шумні відстані до всіх агентів»`.
- КОЛИ `input(dir)` → ЯКЩО `legal(dir)` → ТО `move(agent, dir)`; нелегальна дія — `custom: «виняток, агент падає»` → `lose` для команди.
- КОЛИ `enter(agent, enemy_half)` → ТО `set_state(agent, pacman)`; КОЛИ `enter(agent, home_half)` → ТО `set_state(agent, ghost)`.
- КОЛИ `enter(pacman, enemy_food)` → ТО `pickup(pacman, food)` — `num_carrying +1`, очок ще нема.
- КОЛИ `enter(agent, home_half)` → ЯКЩО `has(agent, food)` → ТО `score(+n)` (червоним плюс, синім мінус), `custom: «num_returned += n, num_carrying = 0»`.
- КОЛИ `counter(returned, >=, TOTAL_FOOD/2 − 2)` → ТО `win` команді, `game_over`.
- КОЛИ `enter(pacman, enemy_capsule)` → ТО `disappear(capsule)`, `set_state(enemy_agents, scared, 40)`.
- КОЛИ `contact(pacman, ghost)` (відстань ≤ 0.7) → ЯКЩО `not state(ghost, scared)` → ТО `custom: «їжа з ноші висипається BFS-ом на найближчі вільні клітини половини, звідки її взято»`, `respawn(pacman, start)`.
- КОЛИ `contact(pacman, ghost)` → ЯКЩО `state(ghost, scared)` → ТО `respawn(ghost, start)`, `clear_state(ghost, scared)`.
- КОЛИ `tick` → ЯКЩО `state(agent, scared)` → ТО `counter(scared_timer, −1)`.
- КОЛИ `turn_start(agent)` → ЯКЩО `not in_range(enemy, teammate, 5)` для обох членів команди → ТО `hide(enemy_position)`; завжди `custom: «відстань = Мангеттен + U{−6…6}»`.
- КОЛИ `counter(moves, ==, 1200)` → ТО `game_over`: рахунок > 0 — червоні, < 0 — сині, 0 — `draw`.
- КОЛИ `custom: «хід агента довший за 1 с»` → ТО `custom: «попередження»`; ЯКЩО `custom: «третє попередження або хід > 3 с»` → ТО `lose` команді; на `register_initial_state` — 15 с.
- КОЛИ `custom: «агент кинув виняток»` → ТО `custom: «рахунок ±1 на користь суперника»`, `game_over`.
- Перемога: повернути всю чужу їжу, крім двох точок, або мати більший рахунок на 1200-му ході · Поразка: суперник повернув квоту, таймаути, падіння агента · Рахунок: різниця повернених точок (червоні +, сині −); за вбивство — 0 (`KILL_POINTS = 0`).

## Керування і ввід
- Команда — файл Python з `create_team(first_index, second_index, is_red, …)` і класами-нащадками `CaptureAgent`, що перевизначають `register_initial_state` і `choose_action(game_state)`.
- API стану: `get_legal_actions`, `generate_successor`, `get_agent_state`, `get_agent_position` (None для невидимих), `get_agent_distances` (шумні), `get_distance_prob`, `get_red_food` / `get_blue_food`, `get_capsules`, `get_walls`, `get_score`; у `CaptureAgent` — лабіринтні відстані й історія спостережень (?).
- Запуск: `python capture.py -r baseline_team -b my_team.py`; опції `-l RANDOM23`, `-n` ігор, `-i` ходів, `-q/-Q`, `-t` (текстова графіка), `-z` (масштаб), `--record`, `--replay`, `--setRandomSeed`, `-c` (ловити винятки й тримати ліміти).
- Людина теж може грати: `--keys0…3` робить агента клавіатурним; P1 — `a s d w`, P2 — `l ; , p`.

## Вікна, меню, HUD
- `game-screen` (tkinter): лабіринт з червоною й синьою половинами, їжа, капсули, агенти-привиди й пакмени, рахунок і ходи внизу (?).
- Текстовий режим `-t` — поле символами в консолі; `-q` — без графіки.
- `replay-window`: `--replay <файл>` / `replay.py` програє записану гру з `--delay-step`.
- `leaderboard`: HTML-сторінка турніру (скрипт ssardina) — таблиця команд, перемоги/нічиї/поразки, посилання на реплеї й логи.

## Фічі поза полем
- `agent-api`: шаблон команди, `baseline_team` (OffensiveReflexAgent / DefensiveReflexAgent на ознаках і вагах) як суперник.
- `seed-input` (`--setRandomSeed`, `-f`), випадкові мапи `RANDOM<seed>`.
- `replay` і запис (`--record`, `--record-log`).
- Турнір (`pacman_contest_cluster.py`): кожен з кожним на k мапах — `n(n−1)/2 · k` ігор; 3 очки за перемогу, 1 за нічию, 0 за поразку (збій = поразка); сортування — очки, перемоги, рахунок; запуск на кластері воркерів, поділ на підтурніри `--split`, гра лише проти команд викладачів.

## Варіації й родичі
- Прообраз — [pac-man](../maze-arcade/pac-man.md): ті самі точки, капсули й переляк, але привиди — теж гравці, а «будинок» — пів мапи.
- Варіанти курсів: UT Austin 2024 — повна видимість; деякі роки — пакмен рахує очки одразу при поїданні (?); RMIT/UniMelb — Python 3, контест на кластері.
- Інші арени корпусу: [bot-arenas](bot-arenas.md) (Spring Challenge 2020 — Pac-Man загони з туманом), [ai-challenge-ants](ai-challenge-ants.md) (туман і їжа), [wumpus-world](wumpus-world.md) (агент з частковими сприйняттями).
- Осі варіацій: **очки** (при поверненні / при поїданні); **видимість** (радіус + сонар / повна); **ролі** (за половиною / фіксовані); **смерть пакмена** (висипати ношу / втратити); **хід** (по черзі / одночасно).

## Цікавинки для курсу
- Правила половин: перетворення привид ↔ пакмен, ноша й зарахування на межі — 🌱.
- Висипання ноші BFS-ом на вільні клітини правильної половини — 📎.
- Фільтр частинок / баєсове відстеження ворога за шумною відстанню й видимістю — 🥈.
- Захисник на лабіринтних відстанях (BFS-таблиця всіх пар) з перехопленням пакмена біля межі — 🥉.
- Нападник: A* до їжі з «ціною небезпеки» від привидів і поверненням при ноші ≥ N — 🥈.
- Пошук або навчання (MCTS / Q-learning з ознаками) на дві ролі з координацією в команді — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `item-pickup` (їжа, капсули) · `temporary-modes` (переляк 40 ходів) · `respawn` (на старті) · `touch-death` · `drop-on-death` (ноша висипається) · `fog-of-war` (радіус 5 від команди) · `chase-bfs` (лабіринтні відстані) · `ai-greedy` (baseline-агенти) · `move-timer` (1 с / 3 с) · `level-from-txt` (`.lay`) · `maze-generation` (`RANDOM<seed>`) · `seed-share` · `keyboard-controls` · `console-render` · `gui-render` · `replay` · `leaderboard` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+agent-program-interface` — з [minigrid](minigrid.md) / [wumpus-world](wumpus-world.md).
  - `+home-away-role-switch` «Роль сутності залежить від половини поля» · entities/state · 📎.
  - `+carry-and-deposit` «Підібране рахується лише після доставки на базу» · game-logic/score · 🌱.
  - `+noisy-distance-sensor` «Відстань до прихованого ворога з рівномірним шумом» · interface/render · 📎.
  - `+team-shared-vision` «Видно те, що бачить будь-хто з команди» · interface/render · 🌱.
  - `+time-warning-forfeit` «Попередження за повільний хід, N попереджень = поразка» · game-logic/opponent · 🌱.
  - `+round-robin-tournament` «Коло всіх з усіма на кількох мапах, 3/1/0» · interface/results · 📎.
  - `+mirrored-halves` «Мапа з двох дзеркальних половин-баз» · levels/generation · 🌱.
  - `+return-quota-win` «Перемога — донести всю чужу їжу, крім N» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:on_home_side(a)` — агент на своїй половині (визначає роль).
- `+effect:deposit(a, items)` — здати ношу на базі: перетворити несене на очки.
- `+effect:sense(percepts)` — підтвердження з wumpus-world: агент отримує сприйняття (тут — шумні відстані).
- `+effect:scatter(items, area)` — розкидати предмети на найближчі вільні клітини (висипання ноші).
- `+trigger:timeout(bot)` · `+feature:agent-api` — підтвердження.
- `+feature:tournament-runner` — запуск турніру ботів зі сторінкою результатів.

## Джерела
- ⭐ [aig-upf/pacman-contest](https://github.com/aig-upf/pacman-contest) — Python 3-версія контесту, README з атрибуцією Berkeley (DeNero, Klein).
- [capture.py](https://raw.githubusercontent.com/aig-upf/pacman-contest/main/src/contest/capture.py) — константи (`SIGHT_RANGE = 5`, `SONAR_NOISE_RANGE = 13`, `SCARED_TIME = 40`, `MIN_FOOD = 2`, `KILL_POINTS = 0`), правила руху, поїдання, повернення, смерті, ліміти 15 с / 1 с / 3 с / 2 попередження, опції запуску.
- [ssardina-teaching/pacman-contest](https://github.com/ssardina-teaching/pacman-contest) — README турнірного скрипта (3/1/0, сортування, `--max-steps 1200`, фіксовані й випадкові мапи).
- [UT Austin CS343H 2024: CTF](https://rpl.cs.utexas.edu/cs343h_fall2024/ctf.html) — правила прозою: очки за доставку, капсули, ліміти часу, 1200 ходів, нічия при 0.
- [aig-upf/pacman-agent](https://github.com/aig-upf/pacman-agent) — шаблон команди (README через raw).
- Сторінки Berkeley `inst.eecs.berkeley.edu/~cs188/sp09/projects/contest/contest.html` (і sp12) бачив у пошуку, але вони за логіном.

## Непевне
- (?) Рік: сторінка контесту для весни 2009 є в результатах пошуку; чи був контест раніше — не перевірив.
- (?) Порядок ходів: у коді команди визначаються за стартовою половиною, а агенти ходять за індексами; що індекси чергуються червоний/синій — з памʼяті.
- (?) Деталі `CaptureAgent` (лабіринтні відстані через `distancer`, історія спостережень) — з памʼяті, файл `capture_agents.py` не читав.
- (?) Вигляд HUD tkinter (де рахунок, лічильник ходів) — не бачив.
- (?) У старих версіях Berkeley очки могли нараховуватись при поїданні, а не при поверненні — у коді лишились закоментовані рядки на це.
