---
title: "CodinGame: Cellularena (Winter Challenge 2024)"
slug: codingame-cellularena
aka: [Cellularena, Winter Challenge 2024, CodinGame Winter Challenge 2024]
family: program-robots
also: [build-sim]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: territory
year: 2024
platforms: [web]
links:
  - {kind: other, url: "https://github.com/CodinGame/WinterChallenge2024-Cellularena", best: true, note: "відкритий рушій (Java) і повна умова config/statement_en.html.tpl з усіма лігами, порядком фаз і протоколом"}
  - {kind: other, url: "https://gist.github.com/CGjupoulton/9b15eca86001975297e6a1290a301dd1", note: "стартовий бот на Python з умови (є також JS, Java, TypeScript)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+cellularena+winter+challenge+2024", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 75
mechanics: [command-program, impassable-cells, item-pickup, round-currency, orientation-state, spawn-points, reachability-check, ai-opponent, move-timer, replay, leaderboard, hover-highlight, message-log, death-animation, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +auto-pathfind-command, +league-boss-promotion, +local-referee, +symmetric-map-generation, +territory-by-presence, +grow-from-parent, +cascade-death-subtree, +contested-cell-becomes-wall, +facing-harvester, +multi-resource-cost, +spore-ray-spawn, +facing-zone-of-control, +tiebreak-by-stock]
proposes: ["+trigger:timeout(bot)", "+effect:grow_from(parent, cell, type)", "+effect:kill_subtree(a)", "+cond:contested(cell)", "+cond:can_afford(cost)", "+cond:clear_ray(a, cell)", "+role:organ", "+window:replay-viewer", "+window:arena-ide", "+window:league-ladder", "+ui:debug-message", "+ui:resource-counters", "+feature:bot-upload", "+feature:league-promotion", "+feature:local-referee"]
author: opus
date: 2026-11-09
---

# CodinGame: Cellularena — бот вирощує організм з органів за білки A–D: збирачі доять джерела, щупальця відрізають ворожі гілки, спори засновують нові корені

## Суть
Конкурс ботів CodinGame (Winter Challenge 2024, 2 гравці). Бот щоходу читає зі stdin усі сутності поля й друкує по команді на кожен свій організм: `GROW` (виростити орган із наявного), `SPORE` (вистрілити новий корінь) або `WAIT`. Організм — дерево органів (ROOT → BASIC/HARVESTER/TENTACLE/SPORER), кожен займає клітину й коштує набір білків A–D; білки дають поглинання джерела ростом на нього (+3) і HARVESTER, що дивиться на джерело (+1 щоходу). Перемагає той, чиї органи займають більше клітин; смерть органа вбиває все піддерево, удар у ROOT — увесь організм. Рамка арен (протокол, ліги, реплеї) — у [bot-arenas](bot-arenas.md).

## Поле і час
- Квадратна сітка, 4-сусідство; `16 ≤ width ≤ 24`, `8 ≤ height ≤ 12` (умова); генератор бере `h` ∈ [8, 12] і `w = 2h`.
- Симетрія: з імовірністю 3/4 центральна (поворот на 180°), інакше дзеркальна ліво-право (`ySym = rnd || rnd` у `GridMaker`). Стіни (до 50 % клітин) і джерела білків (до 25 %, мінімум 8 пар, типи A→B→C→D по колу) ставляться парами.
- Острови вільних клітин зшиваються: генератор знімає стіни-«мости», доки все вільне не стане однією компонентою.
- Старт: ROOT гравця — у випадковій клітині за ≤ 3 від лівого верхнього кута, суперника — у симетричній; обидва дивляться на північ. Початковий запас кожного білка — випадково 3–10, однаковий для обох.
- Тік = хід: обидва боти відповідають одночасно; ≤ 50 мс на хід, ≤ 1000 мс на перший; не більше 100 ходів.
- Порядок ходу: (1) GROW і SPORE → (2) стіни від зіткнень → (3) збір білків → (4) атаки щупалець → (5) перевірка кінця гри.
- Повна інформація: видно всі органи з напрямками й батьками, усі джерела, запаси обох гравців.
- Вудові ліги (рівні 1–4) — фіксовані навчальні сценарії: лише BASIC і 10 A · + HARVESTER (ще 1 C і 1 D) · + TENTACLE (по 50 A/B/C, без джерел) · + SPORER (джерело далеко від старту).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| ROOT (корінь) | piece | A1 B1 C1 D1; без батька | центр організму; створюється лише спорою; його смерть убиває весь організм |
| BASIC | piece | A1 | просто займає клітину (рахунок) |
| HARVESTER (збирач) | piece | C1 D1; напрям N/E/S/W | наприкінці ходу дає +1 білка того джерела, на яке дивиться |
| TENTACLE (щупальце) | piece | B1 C1; напрям | після збору вбиває ворожий орган у клітині перед собою; суперник не може рости в цю клітину |
| SPORER (спороносець) | piece | B1 D1; напрям | `SPORE` за A1 B1 C1 D1: новий ROOT у будь-якій вільній клітині по прямій перед собою, якщо шлях чистий |
| Джерело білка A / B / C / D | resource | тип | ріст на нього → +3 білка й джерело зникає; HARVESTER поруч доїть по +1 |
| Стіна | static | — | непрохідна для росту й спор |
| Стіна зіткнення | static | — | зʼявляється, коли ≥ 2 рости/спори цілять в одну клітину в одному ході |
| Запас білків A–D | supply | 4 лічильники на гравця | витрачається на органи; при нічиїй — тай-брейк |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «суддя шле entityCount рядків x y type owner organId organDir organParentId organRootId, запаси обох гравців і requiredActionsCount»`.
- КОЛИ `exec(GROW id x y type dir)` → ЯКЩО `custom: «запас ≥ вартості type»` and `free(target)` and `in_range(organ_id, target, 1)` → ТО `spawn_at(organ(type, dir), target)`, `counter(proteins, −cost)`; новий орган отримує батька `id` і корінь його організму.
- КОЛИ `exec(GROW …)` → ЯКЩО `not in_range(organ_id, target, 1)` and `path_exists(organ_id, target)` → ТО `custom: «A* через свої органи й вільні клітини; орган виростає з останньої своєї клітини шляху на перший вільний крок»`; немає шляху — помилка в журналі, дія пропадає.
- КОЛИ `exec(GROW id x y ROOT)` → ТО `block` — корінь не росте, лише спора.
- КОЛИ `exec(SPORE id x y)` → ЯКЩО `state(id, SPORER)` and `custom: «ціль строго в напрямку погляду SPORER, усі клітини між ними без стін і органів»` and `custom: «є A1 B1 C1 D1»` → ТО `spawn_at(ROOT, target)` — новий незалежний організм.
- КОЛИ `exec(GROW|SPORE …)` → ЯКЩО `custom: «ціль — стіна чи орган, перед ціллю ворожий TENTACLE, чужий id, мало білків або цей організм уже діяв у ході»` → ТО `block`, `message(error)` у журнал; бот не вибуває.
- КОЛИ `custom: «два й більше ростів чи спор цілять в одну клітину в одному ході (навіть свої)»` → ТО `set_cell(target, wall)`; білки за всі ці дії вже сплачено.
- КОЛИ `enter(organ, protein_source)` → ТО `pickup`, `counter(protein_type, +3)`, `disappear_b`.
- КОЛИ `phase_start(harvest)` → ЯКЩО `occupied(front_cell(harvester), protein_source)` → ТО `counter(protein_type, +1)`; кілька збирачів одного гравця на одне джерело дають усе одно +1; обидва гравці можуть доїти одне джерело.
- КОЛИ `phase_start(attacks)` → ЯКЩО `occupied(front_cell(tentacle), enemy_organ)` → ТО `disappear_b`; усі атаки одночасні — два щупальця «лоб у лоб» гинуть обидва.
- КОЛИ `died(organ)` → ТО `trigger(rule)`: `custom: «гинуть усі нащадки за organParentId, рекурсивно»`; смерть ROOT стирає весь організм.
- КОЛИ `exec(WAIT)` → ТО `custom: «організм пропускає хід»`; WAIT обовʼязковий для кожного організму, що не діє (рядків рівно requiredActionsCount).
- КОЛИ `exec(cmd text)` → ТО `message(text)` над організмом у реплеї (до 48 символів).
- КОЛИ `custom: «рядок команди не розпізнано або бот не відповів вчасно»` → ТО `lose` (гравець дискваліфікований).
- КОЛИ `all_gone(organs_of_player)` → ТО `game_over`.
- КОЛИ `custom: «жоден гравець не може більше рости (нема білків на жоден орган і жоден збирач не доїть) або застряг той, хто позаду»` → ТО `game_over`.
- КОЛИ `custom: «усі клітини — органи або стіни»` → ТО `game_over`.
- КОЛИ `counter(turn, >=, 100)` → ТО `game_over`.
- КОЛИ `game_over` → ТО `score(count(organs))`; рівно → `custom: «тай-брейк — сума білків у запасі»`.
- Перемога: більше клітин під органами · Поразка: таймаут, нерозпізнана команда, загибель усіх органів · Рахунок: кількість органів (тай-брейк — запас білків).

## Керування і ввід
- Ініціалізація: `width height`.
- Щоходу: `entityCount`, рядки сутностей (тип — `WALL`, `ROOT`, `BASIC`, `HARVESTER`, `TENTACLE`, `SPORER`, `A`–`D`; `owner` 1 / 0 / −1), `myA myB myC myD`, `oppA oppB oppC oppD`, `requiredActionsCount`.
- Вивід: `requiredActionsCount` рядків — `GROW id x y type [dir]`, `SPORE id x y` або `WAIT`; хвіст рядка — текст-повідомлення.
- Організми ходять одночасно; належність органа — за `organRootId`, дерево — за `organParentId`.
- Тестування — IDE CodinGame (вибір суперника, перегляд матчу); Submit → матчі в лізі.

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова з розкриттям «правила вищих ліг», редактор коду, консоль, Play testing / Submit.
- `replay-viewer`: поле зі спрайтами органів за напрямком, анімації росту, поглинання, збору, атаки, польоту спори, смерті й появи стіни; наведення на клітину → `tooltip` з даними органа; шестерня — опції відображення; Space — пауза, стрілки — по кадру.
- HUD реплею: для кожного гравця аватар, нік, `score` (кількість органів) і 4 лічильники білків A–D.
- Журнал ходу (`message-log`): помилки на кшталт «cannot grow in front of tentacle», підказки автошляху, звідки скільки білків отримано.
- `end-screen`: рейтинг; при нічиїй — «N (and M proteins)».
- `league-ladder`: 4 вудові ліги з босом, далі повні правила.

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion`: у нижчих лігах Submit грає лише з босом — перемога best-of-five відкриває наступну лігу і нові органи.
- `replay` будь-якого матчу; `local-referee`: рушій відкритий (Maven, Java), параметр гри `SHOW_WALL_POINTS` показує «сайд-квест» — очки за стіни від зіткнень власних ростів.
- Стартові боти від організаторів на JS, Java, Python, TypeScript.
- Нема undo, паузи гри чи налаштувань поля — лише сид матчу.

## Варіації й родичі
- [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md) — територія й ресурс клітин; [codingame-hypersonic](codingame-hypersonic.md) — бомби; [bot-arenas](bot-arenas.md) — Tron, Ants, Halite; [lux-ai](lux-ai.md) — економіка юнітів.
- Ріст-територія як у [game-of-life](../build-sim/game-of-life.md) чи «амебі» Boulder Dash, але з явними батьками й ціною.
- Осі варіацій: **ріст** (лише до сусіда / автошлях до цілі / спора по променю) · **економіка** (один ресурс / кілька типів з таблицею цін) · **атака** (контакт / орган-зброя з напрямком) · **смерть** (одна клітина / все піддерево) · **зіткнення** (обидва програють / стіна / пріоритет).

## Цікавинки для курсу
- Симулятор ходу з фазами й одночасними діями: дві дії в одну клітину → стіна — 🥉 (порядок фаз важливіший за код).
- Дерево органів: батьки, корені, каскадне видалення піддерева — 📎.
- `GROW` з автошляхом: A* лише крізь свої клітини і вибір «останній свій вузол → перший вільний крок» — 🥉.
- Економіка 4 білків: коли ставити збирача, скільки ходів окупається, що купувати — 🥈.
- Спора: промінь до першої перешкоди, вибір найкращої клітини для нового кореня — 🥉.
- Генератор симетричної мапи зі зшиванням островів (BFS-компоненти) — 🥉.
- Бот з пошуком на кілька ходів (beam search / Вороного за територією) проти боса — 🥇.

## Мапа на каталог
- Є: `command-program` (бот = програма) · `impassable-cells` · `item-pickup` (поглинання джерела) · `round-currency` (білки: здобуття й витрати) · `orientation-state` (напрям органа визначає збір і атаку) · `spawn-points` (симетричний старт) · `reachability-check` (зшивання островів) · `ai-opponent` (бос ліги) · `move-timer` (50 мс) · `replay` · `leaderboard` · `hover-highlight` · `message-log` · `death-animation`.
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee`, `+symmetric-map-generation`, `+auto-pathfind-command`, `+territory-by-presence` — з [bot-arenas](bot-arenas.md) і [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md), тут підтвердження.
  - `+grow-from-parent` «Нова сутність виростає з наявної в сусідню клітину, памʼятає батька» · entities/spawn · 📎.
  - `+cascade-death-subtree` «Смерть вузла вбиває все піддерево» · entities/state · 📎.
  - `+contested-cell-becomes-wall` «Одночасні дії в одну клітину → стіна» · game-logic/opponent · 📎.
  - `+facing-harvester` «Збирач доїть клітину, на яку дивиться, раз на хід» · game-logic/economy · 🌱.
  - `+multi-resource-cost` «Таблиця цін у кількох ресурсах» · game-logic/economy · 🌱.
  - `+spore-ray-spawn` «Спавн у вільну клітину на промені погляду» · entities/spawn · 📎.
  - `+facing-zone-of-control` «Клітина перед органом закрита для ворога» · entities/combat · 🌱.
  - `+tiebreak-by-stock` «Нічия за рахунком → більший запас ресурсу» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:timeout(bot)` — підтвердження (bot-arenas, Hypersonic, Battlesnake).
- `+effect:grow_from(parent, cell, type)` — виростити сутність-нащадка з посиланням на батька (ріст органів; є і в Snake-подібних «рости від голови»).
- `+effect:kill_subtree(a)` — каскадне знищення нащадків.
- `+cond:contested(cell)` — у клітину в цьому ході цілить ≥ 2 дій (Cellularena, Exotec, Battlesnake «голова в голову»).
- `+cond:can_afford(cost)` — запас покриває ціну в кількох ресурсах.
- `+cond:clear_ray(a, cell)` — між A і клітиною по прямій нема перешкод (спора; відрізняється від `line_of_sight` ціллю-клітиною).
- `+role:organ` — частина тіла-дерева гравця (зараз `piece`).
- `+window:replay-viewer`, `+window:arena-ide`, `+window:league-ladder` — підтвердження.
- `+ui:debug-message` — текст бота над організмом; `+ui:resource-counters` — ряд лічильників кількох ресурсів гравця.
- `+feature:bot-upload`, `+feature:league-promotion`, `+feature:local-referee` — підтвердження.

## Джерела
- ⭐ [CodinGame/WinterChallenge2024-Cellularena](https://github.com/CodinGame/WinterChallenge2024-Cellularena) — `config/statement_en.html.tpl` (усі ліги, вартості, порядок фаз, протокол, обмеження), `Game.java` (зіткнення, збір, атаки, каскад, кінець гри, тай-брейк), `GridMaker.java` (розмір, симетрія, острови, старт), `OrganType.java` (ціни).
- [Стартовий бот Python](https://gist.github.com/CGjupoulton/9b15eca86001975297e6a1290a301dd1) — посилання з умови.

## Непевне
- (?) Назви ліг понад вудові (Bronze, Silver, Gold, Legend) — за звичаєм CodinGame; у коді лише «рівень ≤ 4 — навчальний».
- (?) Точні дати конкурсу (грудень 2024) — репозиторій їх не каже; рік — з назви.
- (?) Чи тай-брейк за запасом білків остаточний, якщо й запаси рівні, — код тоді дає нічию.
- (?) Чи зіткнення двох власних організмів в одній клітині чимось карається, крім втрати білків і «очок сайд-квесту» (видно лише з параметром `SHOW_WALL_POINTS`).
