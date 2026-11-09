---
title: "CodinGame: Exotec (Winter Challenge 2026)"
slug: codingame-exotec
aka: [Exotec, Winter Challenge 2026, CodinGame Winter Challenge 2026, Snakebots]
family: program-robots
also: [maze-arcade, grid-platformer]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: score
year: 2026
platforms: [web]
links:
  - {kind: other, url: "https://github.com/CodinGame/WinterChallenge2026-Exotec", best: true, note: "відкритий рушій (Java) і умова config/statement_en.html.tpl: рух, гравітація, обезголовлення, протокол"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+winter+challenge+2026+exotec", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 80
mechanics: [command-program, move-auto, body-queue, self-collision, no-reverse-turn, gravity-fall, item-pickup, impassable-cells, spawn-points, move-timer, replay, leaderboard, hover-highlight, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +league-boss-promotion, +local-referee, +symmetric-map-generation, +grow-on-eat, +behead-next-segment, +solid-pickup-support, +bodies-are-ground, +fall-off-map-death, +shared-pickup-on-tie, +debug-mark-cells, +league-map-size-skew, +tiebreak-fewer-losses]
proposes: ["+trigger:timeout(bot)", "+cond:contested(cell)", "+effect:behead(a)", "+effect:fall_group(a)", "+ui:debug-marks", "+ui:debug-message", "+window:replay-viewer", "+feature:league-promotion", "+feature:local-referee"]
author: opus
date: 2026-11-09
---

# CodinGame: Exotec — команда змійок-роботів у вигляді збоку: вічний рух, гравітація, їжа-опора, розбита голова передає роль наступному сегменту

## Суть
Конкурс ботів CodinGame (Winter Challenge 2026, «Exotec» — у назві репозиторію, 2 гравці). Кожен гравець веде команду змійок-«снейкботів»; щоходу бот лише повертає їм голови (`id UP|DOWN|LEFT|RIGHT`), а змійки самі повзуть у поточному напрямку. Поле видно збоку: платформи, джерела живлення, і **гравітація** — змійка падає, якщо жоден сегмент не стоїть на твердому, а тверді тут і платформи, і джерела, і інші змійки. Удар головою в стіну чи тіло зносить голову (довжина −1), коротка змійка гине цілком; з'їдене джерело дає +1 сегмент. Виграє той, у кого сумарно більше сегментів. Ядро нагадує [Snakebird](../thinky/snakebird.md), але в реальному змаганні ботів; рамка арен — у [bot-arenas](bot-arenas.md).

## Поле і час
- Квадратна сітка, вид збоку; `15 ≤ width ≤ 45`, `10 ≤ height ≤ 30` (умова). Генератор: висота 10–24, `width = round(1.8·height)`, парна; у бронзі мапи частіше малі, у легенді — великі (степеневий перекіс за лігою).
- Нижній ряд — суцільна платформа; щільність платформ зростає донизу; мапа дзеркальна ліво-право; «повітряні кишені» менше 10 клітин замуровуються; клітини з ≥ 3 сусідами-стінами розкопуються.
- Змійки стартують вертикальними стовпчиками по 3 сегменти над платформою, голова вгорі, напрям «вгору»; на гравця 2–4 змійки (менше на низьких мапах), старти не біля центральної лінії; суперник — дзеркально.
- Джерела живлення — випадкові вільні клітини лівої половини з дзеркалом (≈2,5 %, мінімум 8).
- Тік = хід: команди обох ботів застосовуються одночасно; фази ходу — рух → поїдання → обезголовлення → падіння.
- Межа поля не стіна: змійка може висунутись за край; випадає вниз за поле повністю — знищена.
- ≤ 50 мс на хід, ≤ 1000 мс на перший; не більше 200 ходів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Змійка (снейкбот) | piece | id, тіло — список клітин від голови; напрям | щоходу голова на 1 клітину в напрямку, тіло тягнеться слідом |
| Голова | piece | перший сегмент | визначає рух, їсть, б'ється об перешкоди |
| Сегмент тіла | piece | — | твердий для всіх змійок (на ньому можна стояти, в нього можна врізатись) |
| Платформа `#` | static | — | непрохідна, тверда опора |
| Джерело живлення | pickup | x, y | тверда опора; голова входить → змійка росте, джерело зникає |
| Маркер `MARK` | mark | ≤ 4 за хід | лише для налагодження в реплеї |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «суддя шле кількість і координати джерел, потім кожну змійку: id і тіло "x,y:x,y:…" від голови»`.
- КОЛИ `exec(id DIR)` → ЯКЩО `custom: «DIR не протилежний нинішньому напрямку голови»` → ТО `face(snakebot, DIR)`; інакше `block` і помилка в журналі («cannot move backwards»).
- КОЛИ `exec(id DIR)` → ЯКЩО `custom: «змійка чужа, мертва або вже отримала наказ цього ходу»` → ТО `block`, помилка в журналі.
- КОЛИ `phase_start(move)` → ТО `move(head, facing)`; `custom: «хвіст звільняє клітину, тіло зсувається чергою»`.
- КОЛИ `contact(head, power_source)` → ТО `grow(snakebot, 1)` (хвіст цього ходу не скорочується), `disappear_b`.
- КОЛИ `custom: «кілька голів входять в одне джерело»` → ТО `grow(each, 1)` — джерело зʼїдене кожною.
- КОЛИ `contact(head, platform)` або `contact(head, body)` → ЯКЩО `counter(length, >, 3)` → ТО `custom: «голова знищується, наступний сегмент стає головою»` (`shrink(snakebot, 1)`); інакше `disappear_a` — змійка знищена цілком.
- КОЛИ `custom: «дві голови в одній клітині»` → ТО обидві обезголовлюються за тим самим правилом (кожна голова — «в тілі» іншої).
- КОЛИ `contact(head, own_body)` → ТО те саме обезголовлення (самозіткнення).
- КОЛИ `phase_start(fall)` → ЯКЩО `not supported(snakebot)` → ТО `fall(snakebot)` на 1 клітину, повтор до опори; опора — платформа, джерело або змійка, що вже стоїть.
- КОЛИ `edge(snakebot)` → ЯКЩО `custom: «усі сегменти нижче поля»` → ТО `disappear_a`.
- КОЛИ `exec(MARK x y)` → ЯКЩО `counter(marks, <, 4)` → ТО `mark(cell, debug)`; п'ятий — помилка.
- КОЛИ `exec(id DIR text)` → ТО `message(text)` над змійкою (до 48 символів).
- КОЛИ `custom: «рядок не розпізнано або бот не відповів вчасно»` → ТО `lose` (дискваліфікація, рахунок −1).
- КОЛИ `all_gone(snakebots_of_player)` або `all_gone(power_source)` або `counter(turn, >=, 200)` → ТО `game_over`.
- КОЛИ `game_over` → ТО `score(сума сегментів живих змійок)`; рівно → `custom: «мінус втрати: −1 за кожну знесену голову, −довжина за загиблу змійку»`.
- Перемога: більше сегментів · Поразка: таймаут, нерозпізнана команда · Рахунок: сумарна довжина команди.

## Керування і ввід
- Ініціалізація: `myId`, `width`, `height`, `height` рядків з `#` і `.`, `snakebotsPerPlayer`, id своїх змійок, id змійок суперника.
- Щоходу: `powerSourceCount` і пари `x y`, `snakebotCount` і рядки `snakebotId body`.
- Вивід: один рядок, дії через `;`: `id UP|DOWN|LEFT|RIGHT [text]`, `MARK x y`, `WAIT`; приклад `1 LEFT;2 RIGHT;MARK 12 2`.
- Без наказу змійка повзе далі — бот керує лише поворотами; розворот на 180° заборонено.
- Тестування — IDE CodinGame; Submit → матчі в лізі.

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова, редактор, консоль, Play testing / Submit.
- `replay-viewer`: поле збоку зі спрайтами змійок двох кольорів, анімації руху, поїдання, обезголовлення, падіння; маркери `MARK` підсвічують клітини; текст над змійкою; наведення → `tooltip` клітини; шестерня — опції; Space — пауза, стрілки — по кадру.
- `end-screen`: «N points», при нічиїй — «N points (and K losses)».
- Журнал ходу: помилки наказів (≤ 4 показано, далі «…and N more errors»).

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion` (бос ліги; розмір мап росте з лігою).
- `replay`; `local-referee` — відкритий рушій (Maven, Java), у ньому є тестові рівні з BMP-картинок (`level_gravity_test.bmp`, `collision_test.bmp`).
- Без undo, паузи гри, налаштувань.

## Варіації й родичі
- [battlesnake](battlesnake.md) — змійки-боти зверху, «голова в голову» вирішує довжина; [snakebird](../thinky/snakebird.md) — змійки з гравітацією в пазлах; [codingame-cellularena](codingame-cellularena.md) — попередній зимовий челендж.
- Класична Snake (maze-arcade) — без гравітації й без обезголовлення.
- Осі варіацій: **гравітація** (нема / вниз для всього тіла) · **удар** (смерть / −голова / обрізання хвоста) · **опора** (лише платформи / + їжа / + інші змійки) · **їжа** (зникає / кожному, хто дійшов) · **керування** (кожен крок / лише повороти).

## Цікавинки для курсу
- Змійка-черга з ростом і обезголовленням замість смерті — 🌱.
- Гравітація для багатоклітинних тіл: «стоїть, якщо будь-який сегмент на опорі», ітеративне заземлення змійок одна на одній — 🥉.
- Одночасне розвʼязання ходу: рух усіх → поїдання → удари → падіння; спільне поїдання одного джерела — 📎.
- Генератор мапи збоку зі щільністю, що росте донизу, дзеркалом і замуровуванням кишень — 🥉.
- Бот: BFS у фізиці з падінням (стан = тіло змійки) до найближчого джерела з безпечним приземленням — 🥈.
- Пошук на кілька ходів для команди з 4 змійок проти суперника (beam search / MCTS) — 🥇.

## Мапа на каталог
- Є: `command-program` · `move-auto` (вічний рух, ввід лише повертає) · `body-queue` · `self-collision` (слот — обезголовлення) · `no-reverse-turn` · `gravity-fall` · `item-pickup` · `impassable-cells` · `spawn-points` · `move-timer` · `replay` · `leaderboard` · `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee`, `+symmetric-map-generation` — з [bot-arenas](bot-arenas.md), підтвердження.
  - `+grow-on-eat` «Їжа додає сегмент у хвіст» · entities/move · 🌱.
  - `+behead-next-segment` «Удар зносить голову, наступний сегмент стає головою; коротка змійка гине» · entities/move · 📎.
  - `+solid-pickup-support` «Предмет є опорою, доки його не зʼїли» · entities/move · 🌱.
  - `+bodies-are-ground` «Тіла інших сутностей — опора для падіння» · entities/move · 📎.
  - `+fall-off-map-death` «Випасти за нижній край — смерть; за бічні — можна» · entities/move · 🌱.
  - `+shared-pickup-on-tie` «Кілька одночасних претендентів отримують предмет усі» · game-logic/opponent · 🌱.
  - `+debug-mark-cells` «Бот підсвічує клітини в реплеї» · interface/hud · 🌱.
  - `+league-map-size-skew` «Розмір мапи залежить від ліги» · levels/generation · 🌱.
  - `+tiebreak-fewer-losses` «Нічия → менше втрат» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:timeout(bot)` — підтвердження.
- `+cond:contested(cell)` — ≥ 2 сутності претендують на одну клітину в одному ході (друге підтвердження після Cellularena).
- `+effect:behead(a)` — знести голову, наступний сегмент стає головою (інакше `shrink` + `custom`).
- `+effect:fall_group(a)` — падіння багатоклітинного тіла як цілого.
- `+ui:debug-marks` — підсвічені ботом клітини; `+ui:debug-message` — підтвердження.
- `+window:replay-viewer`, `+feature:league-promotion`, `+feature:local-referee` — підтвердження.

## Джерела
- ⭐ [CodinGame/WinterChallenge2026-Exotec](https://github.com/CodinGame/WinterChallenge2026-Exotec) — `config/statement_en.html.tpl` (правила, протокол, обмеження), `Game.java` (фази, обезголовлення ≤ 3 сегментів, падіння, тай-брейк), `CommandManager.java` (заборона розвороту, ≤ 4 MARK, дискваліфікація), `GridMaker.java` (розміри за лігою, дзеркало, старт по 3 сегменти), `Referee.java` (200 ходів).

## Непевне
- (?) Дати конкурсу в 2026 р. — у репозиторії не вказані; рік — з назви. Exotec як спонсор (складські роботи) — здогад з назви, умова цього не каже.
- (?) У коді змійки звуться `Bird`, а джерела — `apples`: схоже на іншу початкову тему; на правила не впливає.
- (?) Чи є вудові ліги: коментар генератора каже «якщо зʼявляться вудові ліги», картинка ліги в умові — шаблонна.
- (?) Падіння кількох змійок одна на одній описано за `doFalls`; у коді є ще функція групового падіння «переплетених» змійок, але ніде не викликається — чи буде в наступних версіях, невідомо.
- (?) Змійка, що випала за поле, у втрати тай-брейку, схоже, не йде (рахуються лише удари) — за кодом, не за умовою.
