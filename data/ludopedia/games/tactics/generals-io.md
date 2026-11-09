---
title: generals.io
slug: generals-io
aka: [Generals, generals]
family: tactics
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: setup
  goal: state
year: 2016
platforms: [web]
links:
  - {kind: other, url: "https://arxiv.org/html/2507.06825v2", best: true, note: "Generals.io як RL-середовище: тайли, ріст армій, хід «усі крім 1 / половина», бій відніманням, туман 8 сусідів, пів-ходи по 500 мс"}
  - {kind: play, url: "https://generals.io/", note: "грати в браузері"}
  - {kind: official, url: "https://wiki.generals.io/1v1guide", note: "офіційна вікі: раунд 25 ходів, 1 армія на клітині, розміри мап 1v1/FFA, відстань між генералами"}
  - {kind: official, url: "https://generals.io/versions", note: "історія версій: клавіші, міста 40–50 і реген до 50, тайли, модифікатори, режими, реплеї, редактор"}
  - {kind: other, url: "https://raw.githubusercontent.com/strakam/generals-bots/master/README.md", note: "generals-bots: захоплення генерала, командні правила, формат дії"}
  - {kind: other, url: "https://tildes.net/~games/1uw3/generals_io_a_simple_yet_very_cool_online_real_time_strategy_game", note: "обговорення гравців: «real-time Risk», міста, генерал віддає всю територію"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=generals.io+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [impassable-cells, fog-of-war, online-multiplayer, keyboard-controls, cell-click, selection-highlight, wrap-edges, move-timer, rule-variants, match-setup, lobby-window, replay, replay-window, rating-system, in-game-editor, editor-draw-tools, game-screen, end-screen, +territory-capture, +capture-income, +king-capture-win, +simultaneous-turns, +army-split-move, +army-subtract-combat, +periodic-land-growth, +move-queue, +team-shared-vision, +fair-spawn-generation, +afk-surrender]
proposes: ["+effect:transfer_territory", "+ui:live-ranking", "+ui:move-queue-arrows", "+feature:replay-edit-mode", "+card:army-split-move"]
author: opus
date: 2026-11-09
---

# generals.io — real-time «Risk на клітинах»: розводь армії від генерала й міст, захопи чужого генерала в тумані

## Суть
Браузерна онлайн-стратегія на квадратній сітці: кожна клітина має власника і число армії. Генерал (столиця) і захоплені міста щоходу додають по армії, а раз на 25 ходів кожна своя клітина отримує ще по одній — тож гра — це гонка експансії й концентрації сил. Хід — перенести армію з однієї своєї клітини в сусідню: «усі, крім однієї» або «половину»; у чужій клітині армії віднімаються. Хто захопить генерала суперника, отримує всю його територію; виграє останній, хто лишився.

## Поле і час
- Сітка H×W: 1v1 — 20–30 клітин у ширину/висоту, FFA — 30–40; близько 20 % клітин — гори; генерали щонайменше за 15 кроків один від одного (1v1), у FFA — 9.
- Шари: тип клітини (рівнина, гора, генерал, місто; в нових мапах — болото, пустеля, тунель, фортеця, вартова вежа, обсерваторія) + власник + число армії.
- Час: хід = 2 пів-ходи по 500 мс (онлайн), усі гравці ходять **одночасно**; «раунд» = 25 ходів. Партія обмежена 25 000 с; є ігрова швидкість, у кастомних — Chess Clock і «необмежена швидкість».
- Туман: видно свої клітини і 8 сусідів кожної; решта прихована. Гори й міста в тумані позначені як перешкода (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Генерал (корона) | spawner | власник, армія | +1 армія щоходу; захоплений — стає містом нового власника, гравець вибуває |
| Місто (castle) | spawner | нейтральне 40–50 армії | нейтральне з <50 само відновлюється до 50; захоплене — +1 армія щоходу власнику |
| Гора | static | — | непрохідна |
| Рівнина | terrain | власник, армія | своя клітина тримає ≥1 армію; +1 кожні 25 ходів |
| Армія на клітині | piece | число, власник | переходить у сусідню клітину цілком (−1) або наполовину |
| Болото | terrain | — | у custom-мапах з 2017; ефект (?) |
| Пустеля, тунель, фортеця | terrain | тунель: ліміт пропуску армії; фортеця: «сила» замість блокування | нові тайли 2023+; деталі (?) |
| Вартова вежа / обсерваторія | terrain | — | розширюють огляд (переробка зору 30.0.0); радіус (?) |
| Союзник (командні режими) | ally | — | спільний зір; вхід на його клітину обʼєднує армії |
| Суперник | enemy | — | людина онлайн (або бот через API) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` (пів-ходу) → ТО `custom: «з черги кожного гравця виконується по одному ходу, одночасно»`.
- КОЛИ `input(select, cell)` + `input(dir)` → ЯКЩО `custom: «клітина своя і армії > 1»` і `not cell(target, mountain)` → ТО `custom: «перенести всі армії, крім однієї, у сусідню клітину»`.
- КОЛИ `input(dir)` → ЯКЩО `state(player, half_mode)` (Z) → ТО `custom: «перенести половину армії»`.
- КОЛИ `custom: «армія входить у свою клітину»` → ТО `counter(army[target], +moved)`.
- КОЛИ `custom: «армія входить у нейтральну або ворожу клітину»` → ЯКЩО `custom: «moved > defenders»` → ТО `set_side(target, player)`, `set_value(army[target], moved - defenders)`; інакше `counter(army[target], -moved)`; при рівності клітина лишається попередньому власнику.
- КОЛИ `timer(1 turn)` → ТО `counter(army[general], +1)`, `counter(army[owned_city], +1)`.
- КОЛИ `timer(25 turns)` → ТО `counter(army[each_owned_cell], +1)`.
- КОЛИ `timer(?)` → ЯКЩО `custom: «місто нейтральне і армії < 50»` → ТО `counter(army[city], +1)` до 50.
- КОЛИ `custom: «армія захопила клітину генерала»` → ТО `set_side(victim_cells, capturer)`, `custom: «армії на переданих клітинах ділиться навпіл з округленням угору»`, `transform(general, city)`, `lose` для жертви.
- КОЛИ `custom: «два генерали захоплено в той самий пів-хід»` → ТО `custom: «обмін землею й генералами»` (версія 31.1.0).
- КОЛИ `tick` → ТО `reveal(owned_cells + adjacent8)`, `hide(rest)`; у команді зір спільний.
- КОЛИ `custom: «армія входить на клітину союзника»` → ТО `custom: «армії обʼєднуються»`, `set_side(target, mover)`.
- КОЛИ `custom: «лишився один гравець (або одна команда)»` → ТО `win`; команда програє, коли впали всі її генерали.
- КОЛИ `input(surrender)` → ТО `custom: «земля пульсує і стає сірою (нейтральною)»`, `lose`.
- КОЛИ `idle(n)` → ЯКЩО `custom: «1v1, після 35-го ходу»` → ТО `custom: «AFK-капітуляція»`; у командах земля AFK-гравця переходить союзникам.
- КОЛИ `counter(time, >=, 25000 s)` → ТО `game_over`.
- Модифікатор Torus: КОЛИ `edge(army)` → ТО `wrap(army)`.
- Перемога: захопити генералів усіх суперників · Поразка: втрата свого генерала / капітуляція / AFK · Рахунок: у партії нема; рейтинг — зірки ладдера, у FFA враховуються місця.

## Керування і ввід
- Клік по своїй клітині — вибір; WASD / стрілки / IJKL — поставити хід у напрямку в **чергу**, виділення йде слідом (ланцюг ходів наперед).
- Z — перемкнути 50 %; E — скасувати останній хід у черзі; Q — очистити чергу; Пробіл — зняти виділення; H — вибрати генерала без центрування мапи.
- T — чат команди, Tab — команда/усі; правий клік або F+клік — пінг; Esc — капітуляція (модальне вікно).
- Вибрати можна навіть чужу клітину, якщо вона вже в черзі ходів (30.6.6). Бот-API: дія = [pass, рядок, стовпець, напрям, split].

## Вікна, меню, HUD
- `main-menu`: FFA (до 8 гравців), 1v1, 2v2 (через «парті»), Big Team, Custom game; чат головного меню.
- `lobby-window`: черга / кастомна кімната; `match-setup` — команди, швидкість, мапа, модифікатори (Leapfrog, City-State, Misty Veal, Crystal Clear, Silent War, Torus, Fading Smog, Slippery, Chess Clock), повзунки чесності міст і спавнів.
- `game-screen`: сітка з числами армій і кольорами власників; HUD — `+ui:live-ranking` (земля й армія кожного гравця), лічильник ходу (`turn-counter`), `+ui:move-queue-arrows` (стрілки черги ходів), `fog-overlay`, `chat-box`, `selection-highlight`.
- `confirm-dialog` — капітуляція; `end-screen` — перемога/поразка, далі — реплей.
- `replay-window`: перемотка по 25 ходів, «Step by Round», режим редагування (ставити ходи за будь-кого й дивитись альтернативи), spoiler-free з точки зору гравця.
- `editor-window` — редактор мап (лівий drag — лінія тайлів, правий — гумка, превʼю мапи при наведенні); `leaderboard` — ладдер із сезонами; Generals TV — реплеї топ-гравців.

## Фічі поза полем
- `online-multiplayer` з матчмейкінгом, `rank-tiers`/зірки, сезони, розпад зірок після 48 год неактивності; provisional-гравці (<10 ігор).
- `custom-rules`: модифікатори; `turn-timer` (Chess Clock); `mode-versus`, команди будь-якого складу в кастомних іграх.
- `level-editor` + `user-levels-browser`: кастомні мапи спільноти (1x-мапи, Plots, Fantasy).
- `replay` з редагуванням, `spectator` (Generals TV), `chat` з історією 10 хв, записується в реплей.
- Бот-API для власних ботів; дослідницькі середовища (generals-bots) з тим самим набором правил.

## Варіації й родичі
- Режими: 1v1 · FFA · 2v2 · Big Team · Custom (з модифікаторами й кастомними мапами). Torus — мапа-тор.
- Родичі: Risk (захоплення територій армією), [polytopia](polytopia.md) і [civilization](civilization.md) (міста як джерело росту), [diplomacy](diplomacy.md) (одночасні ходи), [advance-wars](advance-wars.md) (міста як ресурс).
- **Осі варіацій**: ріст армії — лише столиця / міста / уся земля раз на N ходів · хід — уся армія / половина / довільне число · бій — віднімання / кидки (Risk) · видимість — уся мапа / туман з радіусом 1 / вежі.

## Цікавинки для курсу
- Модель «клітина = (власник, число)» + ріст за таймером (генерал, міста, уся земля раз на 25) — 🌱.
- Хід «усі крім 1 / половина» з відніманням армій і правилом рівності — 📎.
- Захоплення генерала: передати всю землю з половиною армій, генерал → місто — 📎.
- Черга ходів наперед із undo останнього і очищенням — 📎.
- Туман «свої клітини + 8 сусідів» з окремою маскою «перешкода в тумані» — 🥉.
- Одночасні ходи кількох гравців у пів-хід і детермінований порядок розвʼязання конфліктів — 🥈.
- Генерація мапи з чесними спавнами (мінімальна відстань BFS, місто в радіусі 6) — 🥇.
- Бот для generals.io (жадібна експансія → пошук генерала в тумані) — 👑.

## Мапа на каталог
- Є: `impassable-cells` ↔ гори; `fog-of-war` ↔ огляд 8 сусідів; `online-multiplayer`; `keyboard-controls` ↔ WASD/стрілки/Z/E/Q; `cell-click` ↔ вибір клітини; `selection-highlight`; `wrap-edges` ↔ Torus; `move-timer` ↔ Chess Clock; `rule-variants` ↔ модифікатори; `match-setup`, `lobby-window`; `replay`, `replay-window`; `rating-system` ↔ зірки ладдера; `in-game-editor`, `editor-draw-tools` ↔ редактор мап; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+territory-capture`, `+capture-income`, `+king-capture-win`, `+simultaneous-turns` — уже в корпусі.
  - `+army-split-move` «Перенести всю армію (−1) або половину» · entities/move · 📎 · слот {modes: all-but-one|half}.
  - `+army-subtract-combat` «Бій як віднімання чисел, рівність — за власником» · entities/combat · 🌱.
  - `+periodic-land-growth` «+1 на кожну свою клітину раз на N ходів» · entities/state · 🌱 · слот {every: 25}.
  - `+move-queue` «Черга ходів наперед з undo/очищенням» · interface/input · 📎.
  - `+team-shared-vision` «Спільний туман команди» · interface/render · 📎.
  - `+fair-spawn-generation` «Генерація з мінімальною відстанню спавнів і ресурсом поруч» · levels/generation · 🥇.
  - `+afk-surrender` «Автокапітуляція за бездіяльність» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+effect:transfer_territory` — передати всі клітини переможеного захоплювачу з перерахунком армії (тут — навпіл).
- `+ui:live-ranking` — живий рейтинг гравців (земля/армія) у партії (уже пропоновано в корпусі).
- `+ui:move-queue-arrows` — стрілки запланованих ходів на полі.
- `+feature:replay-edit-mode` — у реплеї поставити інші ходи й дивитись альтернативну гілку.
- `+card:army-split-move` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [arXiv 2507.06825: Generals.io як середовище](https://arxiv.org/html/2507.06825v2) — повний опис правил: тайли, ріст +1 генерал/місто, +1 на клітину раз на 25 ходів, ходи «усі крім 1 / половина», бій відніманням, туман з 8 сусідами, пів-ходи 500 мс, генерація мап.
- [generals.io](https://generals.io/) — сама гра в браузері.
- [Офіційна вікі: 1v1 guide](https://wiki.generals.io/1v1guide) — раунд 25 ходів, 1 армія на клітину, розміри мап, відстань генералів, пів-ходи.
- [Version history](https://generals.io/versions) — клавіші (WASD, Q, E, Z, H, T, Esc), міста 40–50 і реген до 50, тайли (болото, пустеля, тунель, фортеця, вежі), модифікатори, режими, реплеї, редактор, AFK.
- [generals-bots README](https://raw.githubusercontent.com/strakam/generals-bots/master/README.md) — захоплення генерала (земля переходить, армії навпіл, генерал → місто), командні правила, спільний зір.
- [Tildes: обговорення](https://tildes.net/~games/1uw3/generals_io_a_simple_yet_very_cool_online_real_time_strategy_game) — «real-time Risk», ціна захоплення міста, туман і розвідка.
- YouTube: пошук «generals.io gameplay».

## Непевне
- (?) Як працюють болота (з памʼяті — віднімають армію щоходу, не перевірено), пустелі, тунелі, фортеці, вежі й обсерваторії — в опрацьованих джерелах лише назви.
- (?) Як часто нейтральне місто відновлює армію до 50 (раз на хід чи раз на раунд).
- (?) Чи гори й міста в тумані показані як одна «перешкода»: README ботів має маску `structures_in_fog`, але сам інтерфейс не перевірено.
- (?) Порядок розвʼязання одночасних ходів у межових випадках — arXiv-стаття прямо каже, що опускає його.
- (?) Розбіжність у статті: «split=0 — усі армії» в описі дій проти «усі, крім однієї» в описі гри; за грою — лишається 1.
