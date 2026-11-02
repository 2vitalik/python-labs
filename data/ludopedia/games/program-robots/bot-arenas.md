---
title: Арени ботів на сітці (CodinGame, AI Challenge Ants, Halite, Battlecode)
slug: bot-arenas
family: program-robots
also: [chess-abstract, tactics, maze-arcade]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: hidden
  random: setup
  goal: score
year: 2011
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/aichallenge/aichallenge", best: true, note: "AI Challenge 2011 «Ants»: рушій, playgame.py, візуалізатор, генератор карт — готова локальна арена"}
  - {kind: other, url: "https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/playgame.py", note: "параметри за замовчуванням: 1000 ходів, loadtime 3000 мс, turntime 1000 мс, радіуси"}
  - {kind: other, url: "https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/ants.py", note: "фази ходу, режими бою, протокол w/f/h/a/d → o row col dir"}
  - {kind: official, url: "https://github.com/HaliteChallenge/Halite", note: "Halite I (2016, Two Sigma): рушій, стартові набори, візуалізатор"}
  - {kind: other, url: "https://raw.githubusercontent.com/HaliteChallenge/Halite/master/website/rules_game.php", note: "правила Halite I: сила, виробництво, злиття, overkill, 10·√(W·H) ходів"}
  - {kind: official, url: "https://github.com/HaliteChallenge/Halite-II", note: "Halite II (2017) — неперервний простір, не сітка"}
  - {kind: official, url: "https://github.com/HaliteChallenge/Halite-III", note: "Halite III (2018) — знову квадратна сітка, збір halite кораблями"}
  - {kind: official, url: "https://battlecode.org/", note: "MIT Battlecode — щорічна RTS автономних роботів"}
  - {kind: official, url: "https://github.com/battlecode/battlecode25", note: "рушій (Java), клієнт-реплеєр, специфікації, приклади ботів"}
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/tron-battle", note: "CodinGame Tron Battle (сторінка на JS)"}
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/tic-tac-toe", note: "CodinGame Tic-Tac-Toe → Ultimate у вищих лігах"}
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/ocean-of-code", note: "CodinGame Ocean of Code"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe", note: "правила Ultimate TTT; MCTS проти minimax"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tron_(video_game)", note: "Light Cycles — прообраз Tron Battle"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+bot+programming+tron+battle", note: "пошук; розбори ботів"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, realtime-ai, ai-minimax, ai-greedy, chase-bfs, move-timer, replay, leaderboard, level-from-txt, maze-generation, hp-damage, piece-capture, spawn-points, collect-quota, +command-program, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +trail-wall, +torus-wrap, +fog-of-war-vision, +focus-battle-resolution, +strength-production-territory, +overkill-damage, +merge-same-owner, +nested-board-constraint, +enemy-tracking-from-orders, +sonar-sector-query, +bytecode-limit, +shared-memory-comm, +league-boss-promotion, +rating-trueskill, +local-referee, +cutoff-rules, +swarm-same-program, +symmetric-map-generation]
proposes: ["+trigger:exec(cmd)", "+trigger:turn_start(side)", "+trigger:timeout(bot)", "+trigger:phase_start", "+cond:in_range", "+cond:count_in_radius(a, kind, r2)", "+cond:visible(cell)", "+effect:intent(a, action)", "+effect:eliminate(bot)", "+effect:raze(hill)", "+effect:merge", "+effect:reveal", "+effect:wrap", "+role:spawner", "+role:resource", "+role:zone", "+window:replay-viewer", "+window:arena-ide", "+window:league-ladder", "+ui:debug-overlay", "+ui:frame-scrubber", "+feature:bot-upload", "+feature:local-referee", "+feature:league-promotion", "+axis:control", "+axis:actors", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Арени ботів — програма грає замість тебе: читає стан текстом, відповідає ходом за мілісекунди

## Суть
Окремий жанр змагань: гравець пише **бота** — програму, що щоходу отримує стан гри текстом у stdin і відповідає наказами в stdout, з жорстким лімітом часу; потім боти грають тисячі матчів між собою, а рейтинг (TrueSkill/Elo) визначає місце. Поле майже завжди клітинне: світлові цикли Tron, вкладені хрестики-нулики, мурахи на торі (Google AI Challenge Ants), клітини з силою й виробництвом (Halite I), підводний човен з торпедами (Ocean of Code), RTS автономних роботів з лімітом байткоду (Battlecode). Для курсу це найближчий до лабораторних формат: рушій-суддя + два студентські боти + реплей.

## Поле і час
- Квадратна сітка; часто **тор** (Ants, Halite I: вихід за край → протилежний край), часто **симетрична генерація** карти, щоб старт був чесним.
- Хід = обмін повідомленнями: суддя шле стан → боти думають (ліміт часу) → накази всіх застосовуються **одночасно** (Ants, Halite, Tron на 2–4) або по черзі (UTTT, Ocean of Code).
- Інформація: повна (Tron, UTTT, Halite I) або прихована — туман у радіусі огляду (Ants), невідома позиція ворога (Ocean of Code), видимість у радіусі робота (Battlecode).
- Сесія — матч; поза матчем — ліга/рейтинг.

### Арени — по рядку
| Арена | Рік | Поле і правила | Протокол (на хід) | Ліміт часу | Кінець і рейтинг |
|---|---|---|---|---|---|
| CodinGame **Tron Battle** | 2013 (?) | сітка 30×20 (?), 2–4 гравці; цикл щохід рухається на 1, слід стає стіною; врізався — вибув, слід зникає | in: `N P`, далі N рядків `X0 Y0 X1 Y1` (старт і голова) (?); out: `UP/DOWN/LEFT/RIGHT` | ~100 мс (?) | останній живий; ліги Wood→Legend |
| CodinGame **Ultimate Tic-Tac-Toe** | 2016 (?) | 9 малих полів 3×3; позиція твого ходу в малому полі = поле, де ходить суперник; закрите поле → вільний вибір | in: останній хід суперника `row col` + список легальних ходів; out: `row col` | ~100 мс, перший хід ~1000 мс (?) | виграти велике поле; нижчі ліги — звичайні хрестики-нулики (?) |
| CodinGame **Ocean of Code** | 2020 | 15×15 з островами (?), 2 підводні човни, 6 HP (?); не можна повертатись у свої клітини, SURFACE скидає слід (−1 HP, видає сектор); TORPEDO (радіус 4), SONAR (сектор 1–9), SILENCE (стрибок), MINE/TRIGGER (?) | in: свої дані + **текст наказів суперника** (напрямок руху, сектор сплиття); out: накази через `|` | ~50 мс (?) | 0 HP; суть — вивести позицію ворога з його наказів |
| Google AI Challenge **Ants** | 2011 | тор; мурахи 4 напрями; їжа поруч (spawnradius²=1) → у мурашник → нова мураха; спірну їжу знищено; бій «focus» в attackradius²=5; огляд viewradius²=77; знищити чужий мурашник: +2 собі, −1 власнику | на старті параметри (`loadtime`, `turntime`, `rows`, `cols`, `turns`, радіуси) → `ready`/`go`; щохід `turn N`, рядки `w`/`f`/`h`/`a`/`d row col [owner]` → `go`; out: `o row col n|e|s|w` + `go` | loadtime 3000 мс, turntime 1000 мс у playgame.py (на сервері менше (?)) | 1000 ходів або cutoff (85 % популяції в одного 150 ходів; гниє їжа); рейтинг TrueSkill (?) |
| **Halite I** (Two Sigma) | 2016 | тор; клітина = власник, сила 0–255, виробництво; STILL → сила += виробництво; рух лишає клітину зі силою 0; свої в одній клітині зливаються (cap 255); бій: кожна фігура віднімає свою силу в **кожного** сусіднього/спільного ворога (overkill) | стан карти щохід (власники RLE + сили) (?); out: накази для своїх клітин | ініціалізація 15 с, хід 1 с; прострочив → вибув, клітини стають нейтральними | один живий або 10·√(W·H) ходів; рівні — за територією |
| **Halite II** | 2017 | неперервний простір (кораблі, планети) — **не сітка**, лише для повноти | — | — | — |
| **Halite III** | 2018 | сітка; кораблі збирають halite з клітин і везуть на верф/док; зіткнення знищує обидва (?) | стан + накази кораблям (?) | (?) | найбільше halite наприкінці (?) |
| **Battlecode** (MIT) | щороку (з 2000-х (?)) | RTS на сітці (розмір і юніти змінюються щороку); кожен робот — окремий екземпляр коду; спілкування через спільний масив/прапорці (?) | API в Java/Python замість тексту | **ліміт байткоду** на робота за хід (?) | знищити базу/виконати ціль року; турнір-сітка, Sprint і фінал у Kresge |

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бот (програма гравця) | player | процес, ліміт часу/памʼяті | щохід читає стан, друкує накази; таймаут → вибуває |
| Суддя (referee) | — (рушій) | правила, seed карти | приймає накази, застосовує, рахує, пише реплей |
| Світловий цикл (Tron) | figure | голова, напрям | рух на 1 щохід, лишає стіну-слід |
| Стіна-слід | static | власник | непрохідна; зникає разом з загиблим гравцем |
| Мураха (Ants) | figure | власник | рух на 1; гине в бою або при зіткненні своїх у клітині |
| Мурашник (hill) | spawner | власник, знесений? | породжує мурах із зібраної їжі; ворожа мураха на ньому → знесено |
| Їжа | resource | — | спавниться симетрично; збирається, якщо поруч мураха лише одного гравця |
| Вода | static | — | непрохідна |
| Клітина Halite I | zone | власник, сила, виробництво | росте, коли стоїть; бʼється з сусідами-ворогами |
| Мале поле UTTT | zone | стан: відкрите / вигране / нічия | визначає, де ходить суперник |
| Підводний човен (OoC) | figure | HP, заряди торпеди/сонара/тиші/міни | рухається, не перетинаючи свій слід |
| Острів (OoC) | static | — | непрохідний |
| Робот Battlecode | figure | тип, HP, cooldown, байткод | автономний; бачить радіус; спільна памʼять команди (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «суддя шле кожному боту його видимий стан текстом»`.
- КОЛИ `timeout(bot)` (не відповів за turntime) → ТО `eliminate(bot)`; Halite I: клітини стають частиною карти.
- КОЛИ `phase_start(apply)` → ТО накази всіх ботів виконуються одночасно (`intent`); недопустимий наказ (чужа мураха, дубль, у воду) — ігнорується.
- **Tron**: КОЛИ `exec(dir)` → ЯКЩО `free(next)` → ТО `move(head)`, `set_cell(prev, trail)`; інакше `lose` для бота, `custom: «його слід зникає»`.
- **UTTT**: КОЛИ `input(cell)` → ЯКЩО `legal(cell)` → ТО `mark(cell, side)`; наступне поле суперника = позиція `cell` у малому полі; КОЛИ `pattern(line(3))` у малому полі → ТО `set_side(subboard, side)`; лінія з малих полів → `win`.
- **Ants** — фази ходу: накази (зіткнення своїх → обидві гинуть) → бій → знесення мурашників → спавн з їжі → збір їжі → спавн нової їжі.
- **Ants бій «focus»**: КОЛИ `phase_start(attack)` → ЯКЩО `custom: «у мурахи A ворогів у радіусі ≥ ніж у найслабшого з цих ворогів»` → ТО `disappear_a` (усі такі гинуть одночасно) (?).
- **Ants**: КОЛИ `count_in_radius(food, ants_of_one_player, 1)` → ТО `pickup` → мурашник `spawn`; кілька гравців поруч → `disappear_b`. КОЛИ `contact(enemy_ant, hill)` → ТО `raze(hill)`, `score(+2)` собі, `score(−1)` власнику.
- **Ants cutoff**: КОЛИ `custom: «один бот має ≥85 % популяції 150 ходів»` або їжа гниє → ТО `game_over`.
- **Halite I**: КОЛИ `exec(STILL)` → ТО `counter(strength, +production)`; КОЛИ `exec(dir)` → ТО `move`, лишена клітина = власник із силою 0; кілька своїх в одній клітині → `merge` (сума, cap 255); КОЛИ `phase_start(combat)` → ТО кожна фігура `damage(own_strength)` кожному ворогу в своїй і 4 сусідніх клітинах; сила ≤ 0 → `disappear_a` (нульові, що не бились, виживають).
- **Ocean of Code**: КОЛИ `exec(MOVE dir)` → ЯКЩО `not visited(next)` and `free(next)` → ТО `move`, `counter(charge, +1)`; КОЛИ `exec(SURFACE)` → ТО `hp(−1)`, `reveal(sector)`, `custom: «скинути слід»`; КОЛИ `exec(TORPEDO x y)` → ЯКЩО `in_range(4)` → ТО `damage(2)` у клітині, `damage(1)` навколо (?); КОЛИ `exec(SONAR s)` → ТО `feedback(Y|N)` (?).
- **Battlecode**: КОЛИ `custom: «робот вичерпав байткод»` → ТО `end_turn` для нього (решта коду — наступного ходу) (?).
- Перемога: останній живий (Tron, Halite, OoC) · найбільше очок/території до ліміту ходів (Ants, Halite) · лінія полів (UTTT). Рейтинг — за серією матчів, не за одним.

## Керування і ввід
- Ввід — **програма** в одній з десятків мов (CodinGame), стартові набори (Ants, Halite), Java/Python (Battlecode).
- Протокол — рядки тексту: «ініціалізація один раз → цикл: стан → накази». Дебаг — у stderr (видно в реплеї, не судді).
- Локально: `playgame.py [options] -m map "bot1 cmd" "bot2 cmd"` (Ants); `./gradlew headless` (Battlecode); environment-бінарник (Halite).
- Онлайн: IDE в браузері → «Play» проти вибраних суперників → «Submit» в арену (CodinGame).

## Вікна, меню, HUD
- `arena-ide` (CodinGame): умова з протоколом, редактор коду, вибір мови, консоль stderr, кнопки Play testing / Submit.
- `replay-viewer`: поле по кадрах, `frame-scrubber`, швидкість, накази й stderr кожного бота на кадрі; візуалізатори Ants/Halite/Battlecode — окремі HTML/клієнт-програми.
- `league-ladder`: ліги Wood 3…1 → Bronze → Silver → Gold → Legend, «бос» ліги; таблиця рейтингу, графік позиції (?).
- `leaderboard` + `profile-window` (Ants, Halite: рейтинг, історія матчів, мова бота).
- `match-setup` — вибір суперників/кількості гравців/seed для тестового матчу.
- HUD реплея: `debug-overlay` (Battlecode: лінії/точки з коду бота), лічильники очок/сил/HP, номер ходу.
- Переходи: умова → IDE → тест-матч → реплей → Submit → ліга → нова ліга з новими правилами (CodinGame відкриває механіки поступово).

## Фічі поза полем
- `bot-upload` + автоматичні матчі сервера, `leaderboard-online` з TrueSkill/Elo (?), `league-promotion` (обійти боса ліги).
- `replay` будь-якого матчу, `seed-input` для повторення, `local-referee` (рушій відкритий: Ants, Halite, Battlecode, Screeps).
- Генератор карт (симетричних) і власні карти для тестів (`level-from-txt`: формат карти Ants — рядки символів).
- Обмеження чесності: ліміт часу/памʼяті, пісочниця компіляції, однакові стартові умови.
- Нема undo/pause у сенсі гравця — є покроковий реплей.

## Варіації й родичі
- Інші CodinGame-арени з черги: Hypersonic (Bomberman ботів), Spring Challenge 2020 (Pac-Man загони, туман), Spring 2021 (гекс-ліс, тінь), Keep Off the Grass (поле зʼїдається), The Great Escape (Quoridor на 3–4).
- AI Challenge до Ants: Tron (2010 (?)), Planet Wars (2010 (?)) — граф планет, не сітка.
- Screeps (персистентний світ замість матчу), Russian AI Cup, RoboCode (неперервний танк), Kaggle Halite (2020 (?)).
- Осі варіацій: **черговість** (одночасно / по черзі); **інформація** (повна / туман / виведення з наказів суперника); **топологія** (прямокутник / тор / вкладені поля); **бюджет** (мс на хід / байткод / CPU-відро); **кількість гравців** (1v1 / FFA 2–6); **одиниця керування** (одна голова / рій мурах / клітини-території).

## Цікавинки для курсу
- Локальна арена: суддя запускає два студентські боти як підпроцеси, текстовий протокол через stdin/stdout, ліміт часу, реплей у JSON — 🥇.
- Tron на двох з ботом «заливкою простору» (flood fill / Вороного) — 🥈; переможець проти випадкового — 🥉.
- Ultimate Tic-Tac-Toe з правилом «куди ходити далі» + бот minimax/MCTS — 🥇.
- Halite-подібні клітини: сила, виробництво, злиття, overkill-бій сусідів, територія — 🥈.
- Мурахи на торі з туманом і боєм «focus» — 🥇 (рахунок ворогів у радіусі, одночасна смерть).
- Ocean of Code: відслідковування можливих позицій ворога за його наказами (множина кандидатів) — 🥇.
- Ліги з «босом» для підвищення і рейтинг TrueSkill/Elo серед ботів групи — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (вода, острови, слід) · `realtime-ai` (Tron-змійка — саме так описана картка) · `ai-minimax` (UTTT) · `ai-greedy` (базові боти) · `chase-bfs` (пошук шляху мурах) · `move-timer` (ліміт часу ходу) · `replay` · `leaderboard` · `level-from-txt` (карти Ants) · `maze-generation`/генерація карт · `hp-damage` (OoC) · `piece-capture` · `spawn-points` (мурашники) · `collect-quota` (Halite III).
- **Нема** → пропозиції карток:
  - `+text-io-protocol` «Бот спілкується з суддею рядками stdin/stdout» · code/architecture · 🥈.
  - `+turn-time-limit` «Ліміт часу на хід з вибуванням» · game-logic/opponent · 📎 (сусід `move-timer`).
  - `+simultaneous-hidden-orders` (з RoboRally) — накази всіх застосовуються разом.
  - `+trail-wall` «Слід стає стіною» · entities/move · 📎 (сусід `body-queue`).
  - `+torus-wrap` (з The Farmer) — поле-тор.
  - `+fog-of-war-vision` «Туман з радіусом огляду юнітів» · interface/render · 🥉.
  - `+focus-battle-resolution` «Бій за кількістю ворогів у радіусі» · entities/combat · 🥈.
  - `+strength-production-territory` «Клітини з силою й виробництвом» · game-logic/economy · 🥈.
  - `+overkill-damage` «Шкода всім сусідам одночасно» · entities/combat · 🥉.
  - `+merge-same-owner` «Свої в одній клітині зливаються» · entities/interact · 📎.
  - `+nested-board-constraint` «Хід визначає поле суперника» · entities/legality · 🥉.
  - `+enemy-tracking-from-orders` «Виведення позиції ворога з його наказів» · game-logic/opponent · 🥇.
  - `+sonar-sector-query` «Запит так/ні про сектор» · entities/interact · 📎.
  - `+bytecode-limit` «Бюджет інструкцій на хід» · game-logic · 🥈.
  - `+shared-memory-comm` «Спільна памʼять/масив команди» · game-logic · 🥉.
  - `+league-boss-promotion` «Ліги з босом-ботом» · interface/results · 🥉.
  - `+rating-trueskill` «Рейтинг за серією матчів» · interface/results · 🥈.
  - `+local-referee` «Суддя-рушій з запуском ботів» · code/architecture · 🥇.
  - `+cutoff-rules` «Достроковий кінець за домінуванням» · game-logic · 📎.
  - `+swarm-same-program` (з 7 Billion Humans) — один код на всіх мурах.
  - `+symmetric-map-generation` «Симетрична карта для чесного старту» · levels/generation · 🥉.

## Пропозиції до словників
- `+trigger:exec(cmd)` (сімʼя) · `+trigger:turn_start(side)` ⏳ · `+trigger:timeout(bot)` — бот не встиг · `+trigger:phase_start` 🔥 (рух → бій → спавн).
- `+cond:in_range` ⏳ · `+cond:count_in_radius(a, kind, r2)` — кількість у радіусі (квадрат відстані на торі); `+cond:visible(cell)` — клітина в огляді бота.
- `+effect:intent(a, action)` — наказ із відкладеним застосуванням (як у Screeps); `+effect:eliminate(bot)`; `+effect:raze(hill)`; `+effect:merge` ⏳; `+effect:reveal` ⏳ (сплиття OoC); `+effect:wrap` ⏳.
- `+role:spawner` ⏳ (мурашник) · `+role:resource` 🔥 (їжа, halite) · `+role:zone` 🔥 (клітина-територія, мале поле UTTT).
- `+window:replay-viewer` (= ⏳ `replay-window`, тут головне вікно жанру) · `+window:arena-ide` · `+window:league-ladder`.
- `+ui:debug-overlay` — малювання з коду бота поверх реплею · `+ui:frame-scrubber` — повзунок кадрів.
- `+feature:bot-upload` · `+feature:local-referee` · `+feature:league-promotion`.
- `+axis:control` — `programmed`; `+axis:actors` — `single` (Tron) / `swarm` (Ants, Halite); `+axis:turn-structure` 🔥 — `simultaneous` (Ants, Halite, Tron) vs `sequential` (UTTT, OoC).

## Джерела
- ⭐ [GitHub: aichallenge/aichallenge](https://github.com/aichallenge/aichallenge) — повний набір Ants 2011: рушій, playgame.py, карти, генератор, візуалізатор, менеджер турніру.
- [playgame.py](https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/playgame.py) — параметри: 1000 ходів, 3000/1000 мс, radius² 77/5/1, режим бою focus.
- [ants.py](https://raw.githubusercontent.com/aichallenge/aichallenge/epsilon/ants/ants.py) — фази ходу, режими бою, протокол, cutoff, +2/−1 за мурашник.
- [Halite I rules](https://raw.githubusercontent.com/HaliteChallenge/Halite/master/website/rules_game.php) — повні правила й ліміти часу; [Halite I repo](https://github.com/HaliteChallenge/Halite).
- [Halite II](https://github.com/HaliteChallenge/Halite-II) — неперервний простір; [Halite III](https://github.com/HaliteChallenge/Halite-III) — сітка, збір halite.
- [Battlecode](https://battlecode.org/) — MIT, щорічно; [battlecode25](https://github.com/battlecode/battlecode25) — рушій, клієнт, специфікації.
- CodinGame: [Tron Battle](https://www.codingame.com/multiplayer/bot-programming/tron-battle) · [Tic-Tac-Toe/Ultimate](https://www.codingame.com/multiplayer/bot-programming/tic-tac-toe) · [Ocean of Code](https://www.codingame.com/multiplayer/bot-programming/ocean-of-code) — сторінки рендеряться JS, умову автоматично не прочитав.
- [Wikipedia: Ultimate tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) · [Wikipedia: Tron (video game)](https://en.wikipedia.org/wiki/Tron_(video_game)).
- YouTube: пошук «codingame bot programming tron battle».

## Непевне
- (?) Усі деталі CodinGame (розмір 30×20, формат вводу Tron, ліміти 100/1000/50 мс, правила й числа Ocean of Code, ліги з босами) — з памʼяті: сторінки віддають лише «Loading…», WebSearch вичерпано.
- (?) Точне формулювання бою «focus» в Ants — з памʼяті; код підтверджує лише назву режиму й порядок фаз.
- (?) Ліміти часу Ants на офіційному сервері могли бути меншими за дефолти playgame.py; TrueSkill як рейтинг AI Challenge — з памʼяті.
- (?) Правила Halite III (зіткнення, верф/док, ціна руху) і формат стану Halite I — README цього не містить.
- (?) Battlecode: рік початку, ліміт байткоду, спільний масив/прапорці — змінюються щороку; не перевірено.
- Halite II у таблиці лише для повноти: поле неперервне, у корпус як клітинну гру не годиться.
