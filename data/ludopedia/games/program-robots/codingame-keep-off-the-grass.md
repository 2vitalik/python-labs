---
title: "CodinGame: Keep Off the Grass (Fall Challenge 2022)"
slug: codingame-keep-off-the-grass
aka: [Keep Off The Grass, Fall Challenge 2022, KOTG]
family: program-robots
also: [build-sim, tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: territory
year: 2022
platforms: [web, local CLI]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/FallChallenge2022-KeepOffTheGrass/main/config/statement_en.html.tpl", best: true, note: "повна умова: клітини зі scrap, переробники, роботи, фази ходу, протокол MOVE/BUILD/SPAWN, 50 мс, 200 ходів"}
  - {kind: official, url: "https://github.com/CodinGame/FallChallenge2022-KeepOffTheGrass", note: "рушій-суддя (Java, pom.xml), конфіг ліг, Boss.py, стартові боти спільноти"}
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/keep-off-the-grass", note: "арена CodinGame (сторінка на JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+keep+off+the+grass", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, round-currency, spawn-points, coverage-area, piece-capture, chase-bfs, move-timer, replay, leaderboard, hover-highlight, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +auto-pathfind-command, +stack-units-in-cell, +one-for-one-annihilation, +territory-by-presence, +shrinking-field, +cell-depletion, +harvester-adjacent, +build-cancels-move, +stalemate-end, +league-boss-promotion, +local-referee, +symmetric-map-generation]
proposes: ["+trigger:timeout(bot)", "+trigger:depleted(cell)", "+cond:can_build(cell)", "+cond:in_range_of(cell, recycler)", "+effect:annihilate(a, b, n)", "+effect:eliminate(bot)", "+effect:intent(a, action)", "+ui:debug-message", "+feature:bot-upload", "+feature:league-promotion"]
author: opus
date: 2026-11-09
---

# CodinGame: Keep Off the Grass — роботи фарбують клітини, переробники зʼїдають поле під ногами, перемагає більша територія

## Суть
Осінній конкурс CodinGame 2022 на двох ботів. Кожна клітина має запас **scrap**; переробник (recycler) щоходу знімає по 1 scrap зі своєї та 4 сусідніх клітин і дає за це матерію, а клітина з нулем стає **травою** — непрохідною, і все на ній гине. Матерію витрачають на нових роботів і нові переробники; роботи стоять купами, анігілюють ворожих 1:1 і фарбують клітину, на якій лишились. Головна напруга — економіка проти території: переробник годує, але знищує поле, за яке йде гра.

## Поле і час
- Квадратна сітка; ліга 1: ширина 12–15, висота 6–7; вища ліга: 12–24 × 6–12; (0,0) — лівий верхній кут, y вниз.
- Клітина: `scrapAmount` (0 = трава), `owner` (1 — ти, 0 — суперник, −1 — нейтральна/трава), кількість роботів, чи є переробник.
- Хід = обидва боти відповідають за 50 мс (перший — 1000 мс); дії застосовуються одночасно за фазами.
- Повна інформація; карта — випадкова при старті (симетрична (?)).
- Поле **зменшується**: трава розростається з-під переробників.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | piece | власник; купа N у клітині | рух на сусідню або далеку клітину автошляхом; анігіляція 1:1 з ворожими; фарбує клітину |
| Переробник (recycler) | spawner | власник, 10 матерії | щохід −1 scrap собі й 4 сусідам (не траві); +1 матерії власнику за клітину; зникає, коли під ним 0 |
| Клітина з scrap | terrain | scrapAmount, owner | прохідна; власник змінюється лише, коли на ній у кінці ходу стоять роботи |
| Трава | static | scrapAmount = 0 | непрохідна; поява трави знищує роботів і переробник на ній |
| Матерія | resource | myMatter, oppMatter | +10 щоходу + переробка; витрата 10 за робота чи переробник |
| Територія гравця | zone | кількість клітин | мета гри; тут можна будувати й спавнити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «суддя шле myMatter oppMatter і width×height рядків по 7 чисел: scrap owner units recycler canBuild canSpawn inRangeOfRecycler»`.
- КОЛИ `phase_start(build)` → ЯКЩО `custom: «canBuild = 1: своя, порожня, без роботів»` and `has(player, matter ≥ 10)` → ТО `spawn_at(recycler, cell)`, `currency(−10)`.
- КОЛИ `phase_start(build)` → ЯКЩО `custom: «MOVE або SPAWN цілить у клітину, де будується переробник»` → ТО `block` — навіть якщо це наказ суперника чи пізніший у виводі.
- КОЛИ `exec(SPAWN n x y)` → ЯКЩО `cell(x y, own)` and `has(player, matter)` → ТО `spawn_at(robot × n, cell)`, `currency(−10·n)`; робот не може в цей хід ще й іти.
- КОЛИ `exec(MOVE n fx fy tx ty)` → ТО `move(n robots, step)` за `custom: «найкоротший шлях, з перевагою ближчих до центру; недосяжна — до найближчої досяжної»`; одночасно зі SPAWN.
- КОЛИ `phase_start(combat)` → ЯКЩО `occupied(cell, both_sides)` → ТО `custom: «min(a, b) роботів кожної сторони знищуються 1:1»`.
- КОЛИ `phase_start(mark)` → ЯКЩО `occupied(cell, robots_of_side)` → ТО `set_side(cell, side)`; без роботів власник не змінюється.
- КОЛИ `phase_start(recycle)` → ТО кожен переробник: `counter(scrap, −1)` своєї та 4 сусідніх не-трав'яних клітин; власнику `currency(+1)` за клітину; клітина переробляється не більше разу за хід, навіть під кількома переробниками; спільна клітина двох гравців дає +1 обом.
- КОЛИ `counter(scrap, ==, 0)` клітини → ТО `set_cell(cell, grass)`, `disappear_a` для роботів і переробника на ній.
- КОЛИ `turn_end` → ТО `currency(+10)` кожному.
- КОЛИ `custom: «бот не відповів за 50 мс або нерозпізнана команда»` → ТО `lose`.
- КОЛИ `counter(tiles_of_side, ==, 0)` → ТО `game_over`; КОЛИ `custom: «20 ходів жодна клітина не змінила scrap чи owner»` → ТО `game_over`; КОЛИ `counter(turn, ==, 200)` → ТО `game_over`.
- Перемога: більше клітин наприкінці · Поразка: таймаут, погана команда, 0 клітин · Рахунок: кількість своїх клітин.

## Керування і ввід
- Ініціалізація: `width height`.
- Вивід — кілька дій в одному рядку через `;`: `MOVE amount fromX fromY toX toY` · `BUILD x y` · `SPAWN amount x y` · `WAIT` · `MESSAGE text` (текст на HUD свого боку).
- Наказ — купі роботів з клітини, а не окремому роботу; далека ціль — автошлях.
- Поля `canBuild`, `canSpawn`, `inRangeOfRecycler` — підказки судді, щоб бот не рахував легальність сам.

## Вікна, меню, HUD
- `arena-ide` і `league-ladder` — рамка в [bot-arenas](bot-arenas.md).
- `replay-viewer`: поле з кольорами власників, цифрами роботів і scrap; наведення на клітину → `tooltip` з її історією; шестерня — налаштування відображення; Space — play/pause, стрілки — по кадру (`frame-scrubber`).
- HUD: матерія й кількість клітин кожного, номер ходу, `debug-message` з MESSAGE.

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion` (бос Wood → більші карти).
- `local-referee`: відкритий рушій на GitHub (Java), `starterAIs/` спільноти.
- `replay` з історією клітини; `seed-input` для повтору матчу (?).

## Варіації й родичі
- Арени ботів з територією й економікою: Halite I (сила/виробництво клітин) — у [bot-arenas](bot-arenas.md); [lux-ai](lux-ai.md) (місто без палива гине); [screeps](screeps.md).
- Механіка «поле зʼїдається» — Xonix навпаки, Tron (слід-стіна).
- Осі варіацій: **економіка** (фіксований дохід / переробка поля / обидва); **знищення поля** (ніколи / від свого видобутку / за часом); **бій** (1:1 анігіляція / сила / HP); **одиниця наказу** (робот / купа в клітині); **захоплення** (присутність у кінці ходу / шлях / оточення).

## Цікавинки для курсу
- Симулятор ходу за 7 фазами з одночасним застосуванням і правилом «BUILD скасовує MOVE/SPAWN» — 🥉.
- Переробник: зона 1+4 клітин, «не більше разу за хід», спільні клітини, трава вбиває — 📎.
- Бот «Вороного»: поділ поля на ближчі до себе/суперника клітини й фронт, куди слати роботів — 🥈.
- Оцінка переробника: скільки матерії дасть до виснаження проти скількох клітин відрізає й знищить — 🥈.
- Автошлях з tie-break «ближче до центру» та «найближча досяжна, якщо ціль недосяжна» — 🥉.
- Повний бот з балансом економіки, фронту й ізоляції острівців — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (трава) · `round-currency` (матерія) · `spawn-points` (спавн на своїй клітині) · `coverage-area` (зона переробника) · `piece-capture` (анігіляція) · `chase-bfs` (автошлях) · `move-timer` · `replay` · `leaderboard` · `hover-highlight` (історія клітини).
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee`, `+symmetric-map-generation` — з [bot-arenas](bot-arenas.md); `+auto-pathfind-command` — з [codingame-hypersonic](codingame-hypersonic.md).
  - `+stack-units-in-cell` «Купа своїх юнітів у клітині як число» · entities/state · 📎.
  - `+one-for-one-annihilation` «Ворожі юніти в клітині знищуються 1:1» · entities/combat · 🌱.
  - `+territory-by-presence` «Клітина стає твоєю, коли ти на ній у кінці ходу» · game-logic/win · 🌱.
  - `+shrinking-field` «Поле зменшується в ході гри» · levels · 📎.
  - `+cell-depletion` «Клітина має запас, вичерпалась — змінює тип» · entities/state · 📎.
  - `+harvester-adjacent` «Будівля видобуває з себе й сусідів» · game-logic/economy · 📎.
  - `+build-cancels-move` «Пріоритет дій у фазах: будівництво скасовує рух у клітину» · game-logic · 📎.
  - `+stalemate-end` «Кінець, коли N ходів нічого не змінюється» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:timeout(bot)` — підтвердження; `+trigger:depleted(cell)` — запас клітини вичерпано.
- `+cond:can_build(cell)` — клітина легальна для будівлі (своя, порожня); `+cond:in_range_of(cell, recycler)` — клітина в зоні дії будівлі.
- `+effect:annihilate(a, b, n)` — взаємне знищення n на n; `+effect:eliminate(bot)`, `+effect:intent(a, action)` — підтвердження.
- `+ui:debug-message` — текст бота на HUD.
- `+feature:bot-upload`, `+feature:league-promotion` — підтвердження.

## Джерела
- ⭐ [statement_en.html.tpl](https://raw.githubusercontent.com/CodinGame/FallChallenge2022-KeepOffTheGrass/main/config/statement_en.html.tpl) — повна умова: розміри ліг, трава, переробник (10 матерії, 1+4 клітини, раз за хід), роботи, 7 фаз, протокол, 50/1000 мс, 200 ходів, 20 ходів без змін.
- [GitHub: FallChallenge2022-KeepOffTheGrass](https://github.com/CodinGame/FallChallenge2022-KeepOffTheGrass) — рушій (`src/`, `pom.xml`), `config/` з Boss.py і умовами EN/FR, `starterAIs/`.
- [CodinGame: Keep Off the Grass](https://www.codingame.com/multiplayer/bot-programming/keep-off-the-grass) — арена; сторінка віддає «Loading…».

## Непевне
- (?) Стартова матерія й стартові роботи, правило нічиєї — в умові не названо.
- (?) Ціна SPAWN за робота — 10 матерії, виведено з «a new robot costs 10»; явно за одиницю не сказано.
- (?) Симетричність генерації карти — з памʼяті.
- (?) Чи можна прочитати seed у реплеї — не перевірено.
