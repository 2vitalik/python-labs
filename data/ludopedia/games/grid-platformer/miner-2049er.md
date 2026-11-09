---
title: Miner 2049er
slug: miner-2049er
aka: ["Miner 2049er: Starring Bounty Bob"]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1982
platforms: [Atari 8-bit, Atari 5200, Atari 2600, ColecoVision, TI-99/4A, Apple II, IBM PC, C64, Game Boy, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Miner_2049er", best: true, note: "суть: пройти всю підлогу шахти; мутанти, предмети, транспортери, гармата, гірки; порти й кількість рівнів"}
  - {kind: other, url: "https://ia803209.us.archive.org/24/items/Miner_2049er_1983_Big_Five_Software/Miner_2049er_1983_Big_Five_Software_text.pdf", note: "мануал Atari 5200: 10 станцій з мутантами й предметами, транспортери, ліфт, гармата, очки, зони 1–255, екрани"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Miner 2049er.txt", note: "мануал ColecoVision: 11 рівнів, очки, пороги життів, гідравлічний насос, штампи"}
  - {kind: other, url: "https://www.atarimagazines.com/cva/v1n2/miner.php", note: "Creative Computing 1983: гірки, транспортери, пульверизатори, гармата, зони складності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Miner+2049er+Atari+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, ladder-climb, gravity-fall, visited-trail, touch-death, environment-death, player-death, temporary-modes, item-pickup, event-points, time-out, time-bonus, extra-life-threshold, teleport, teleport-cooldown, carrier-platform, one-way-cell, difficulty-levels, score-records, leaderboard, attract-demo, splash-screen, game-pause, hot-seat, sequential-levels, status-panel, game-screen, +claim-all-floor, +fall-damage-by-height, +numbered-transporter, +controllable-lift, +cannon-charge-height, +timed-crusher, +slide-chute]
proposes: ["+trigger:landed", "+effect:control_transfer(a, b)", "+effect:launch(a, height)", "+window:stage-intro", "+window:name-entry", "+ui:charge-meter", "+card:claim-all-floor", "+card:controllable-lift", "+card:cannon-charge-height", "+card:numbered-transporter"]
author: opus
date: 2026-11-09
---

# Miner 2049er — шериф Bounty Bob ходить кожною секцією каркаса шахти, щоб «застовпити» її, поки не скінчився таймер

## Суть
Платформер-«фарбувальник»: кожна секція каркаса, по якій пройшов Bounty Bob, стає суцільною; станцію пройдено, коли застовплено **всі** секції. Мутанти смертельні при дотику, але загублені речі шахтарів на кілька секунд роблять їх «їстівними». Кожна з 10 станцій додає свій механізм: гірки, транспортери на вибраний поверх, керований ліфт, пульверизатори, гармату на тротилі. Таймер станції — і загроза, і бонус.

## Поле і час
- Один екран на станцію, вигляд збоку: горизонтальні балки каркаса з секціями, драбини, механізми.
- Секція каркаса: незастовплена / застовплена (суцільна).
- Real-time; «Miner Timer» угорі відлічує час станції; залишок → очки.
- Гравітація: з краю Bob падає; падіння понад сталу безпечну висоту вбиває.
- Складність — «зона» 1–255 (Atari 5200): швидкість мутантів і тривалість їхньої вразливості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Bounty Bob | player | життя (3 / 5 за версією) | ходить, лазить драбинами, стрибає в напрямку джойстика |
| Секція каркаса | terrain | застовплена / ні | стає суцільною, коли Bob по ній пройшов; +5 очок |
| Драбина | terrain | ціла / зламана | вертикальний рух; по зламаній не можна лізти |
| Гірка (slide) | terrain | — | наступив на вузьку точку старту — Bob зʼїжджає донизу, назад не можна |
| Мутант | enemy | смертельний / їстівний | ходить по каркасу; дотик смертельний, у стані «їстівний» — гине від Боба |
| Загублена річ (свічка, свердло, мартіні…) | pickup | 100–1100 очок | взяти → очки + усі мутанти тимчасово їстівні |
| «BF» | pickup | великі очки | рідкісний приз (станція 7) |
| Радіоактивні відходи | hazard | — | падіння в бак — смерть |
| Рухома частина (лілійка) | platform | — | везе Боба, що на ній стоїть |
| Транспортер | static | заряджений / перезарядка | двері з номерами поверхів 1–4; після використання червоний, доки не зарядиться |
| Ліфт (станція 8) | platform | — | гравець бере керування ліфтом і рухає його джойстиком |
| Пульверизатор (станція 9) | hazard | цикл | періодично бʼє; пройти — вгадавши паузу |
| Тротил (станція 10) | pickup | 10 т за каністру | заряджає гармату |
| Гармата (станція 10) | static | заряд у тоннах | Bob падає в неї, цілиться й вилітає на поверх = заряд/10 т |
| Miner Timer | static | секунди | спадає; блимає й пищить, коли мало; 0 — смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; вгору/вниз — лише ЯКЩО `cell(here, ladder)` і `not state(ladder, broken)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок у напрямку джойстика на фіксовану відстань»`.
- КОЛИ `enter(player, framework_section)` → ЯКЩО `not state(section, claimed)` → ТО `paint(section, claimed)`, `score(5)`.
- КОЛИ `custom: «усі секції каркаса застовплено»` → ТО `score(timer)`, `win` станції, `next_level`.
- КОЛИ `timer(every)` → ТО `counter(miner_timer, -1)`; КОЛИ `counter(miner_timer, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `contact(player, possession)` → ТО `pickup`, `score(n)`, `set_state(all mutants, edible, duration)`.
- КОЛИ `contact(player, mutant)` → ЯКЩО `state(mutant, edible)` → ТО `disappear_b`, `score(80..90)`; інакше `lives(-1)`.
- КОЛИ `state_off(mutant, edible)` → ТО мутант знову смертельний (перед тим блимає).
- КОЛИ `custom: «Bob приземлився після падіння»` → ЯКЩО `custom: «висота > безпечної»` → ТО `lives(-1)`.
- КОЛИ `enter(player, slide_start)` → ТО `custom: «зʼїхати гіркою до низу»` — шлях лише вниз.
- КОЛИ `enter(player, radioactive_waste)` → ТО `lives(-1)`.
- КОЛИ `contact(player, moving_piece)` → ЯКЩО `custom: «стоїть зверху»` → ТО `carry(moving_piece, player)`.
- КОЛИ `input(level_n)` → ЯКЩО `occupied(transporter, player)` і `state(transporter, charged)` і `custom: «n ≠ поточний поверх»` → ТО `teleport(player, level_n)`, `set_state(transporter, recharging)`.
- КОЛИ `input(lift_on)` → ЯКЩО `occupied(lift, player)` → ТО `custom: «джойстик керує ліфтом, а не Бобом»`; КОЛИ `input(cancel)` → ТО керування назад Бобові.
- КОЛИ `timer(cycle)` → ТО `set_state(pulverizer, down)`; КОЛИ `contact(player, pulverizer)` → ЯКЩО `state(pulverizer, down)` → ТО `lives(-1)`.
- КОЛИ `contact(player, tnt)` → ТО `counter(tnt_load, +10)`, `score(n)`.
- КОЛИ `input(fire)` → ЯКЩО `occupied(cannon, player)` → ТО `custom: «Боба вистрілює на поверх = заряд / 10 т»`; ЯКЩО `custom: «перевантаження»` → ТО `lives(-1)`.
- КОЛИ `counter(score, >=, 10000)` → ТО `lives(+1)`.
- Перемога: застовпити всі станції. Поразка: 0 життів (дотик мутанта, падіння, відходи, таймер). Рахунок: секції, речі, мутанти, тротил, залишок таймера.

## Керування і ввід
- Джойстик: ліво/право — хід; вгору/вниз — драбина; кнопка + напрямок — стрибок (зі стрибком можна злетіти з уступу).
- Клавіатура/кейпад: `1`–`4` — поверх для транспортера; окрема клавіша — увімкнути/вимкнути керування ліфтом; кнопка в гарматі — постріл, джойстик — приціл.
- Перед грою: `0`–`9` — вибір зони складності, перемикач 1/2 гравці; PAUSE; RESET — на титул.
- ColecoVision: `#` — пауза й вимкнення часу, `0` — рестарт, `*` — звук.

## Вікна, меню, HUD
- `splash-screen` — титул: Bob «відкриває» назву гри, грає тема.
- `leaderboard` — топ-10 рекордів з іменами (не зберігається після вимкнення).
- `+window:stage-intro` («Alert mode») — яка станція далі і яка зона складності.
- `game-screen`: каркас, механізми + HUD: `score` обох гравців, кружечки запасних життів (`lives`), Miner Timer (`timer-countdown`), на станції 10 — заряд тротилу (`+ui:charge-meter`).
- `+window:name-entry` — введення ініціалів у рекорди (~2 хв, літери «прокручуються» джойстиком).
- `attract-demo` — по колу титул, рекорди й зразок гри на станції 1.
- `pause-menu` — заморожування гри клавішею PAUSE.
- Переходи: титул ↔ рекорди ↔ демо; START → `stage-intro` → гра → (станцію застовплено) наступний `stage-intro` → (0 життів) `name-entry` або титул.

## Фічі поза полем
- `difficulty-presets`: зони 1–255 (вища зона — швидші мутанти, коротша вразливість, більше очок).
- `hotseat`: 2 гравці по черзі.
- `leaderboard-local`: топ-10 до вимкнення консолі.
- `pause`; `levels-sequential`: 10 станцій (Atari), 11 (ColecoVision), 8 (TI), 3 (Atari 2600).

## Варіації й родичі
- Сиквели: Miner 2049er II (1984, Apple II), Bounty Bob Strikes Back! (1985) — 25 станцій, нові механізми; скасований Scraper Caper.
- Родичі в корпусі: [space-panic](space-panic.md), [lode-runner](lode-runner.md), [kings-valley](kings-valley.md); фарбування підлоги кроками — як у Q*bert / Kula World ([kula-world](kula-world.md)).
- Осі: **що є метою** (пройти всю підлогу / зібрати предмети / дійти до виходу); **механізм станції** (одна «фішка» на екран — гірка, транспортер, ліфт, гармата); **покарання за падіння** (смерть понад висоту / оглушення / нема).

## Цікавинки для курсу
- Застовпити всі секції підлоги: слід пройдених клітин + перевірка «усі» — 🌱.
- Тимчасова вразливість ворогів після підбору предмета (як енерджайзер Pac-Man) — 📎.
- Смерть від падіння понад безпечну висоту: лічильник висоти польоту — 📎.
- Транспортер на вибраний поверх із перезарядкою — 📎.
- Керований ліфт: ввід перемикається з аватара на механізм і назад — 🥉.
- Гармата: заряд у «тоннах» визначає висоту польоту, перевантаження вбиває — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `ladder-climb` · `gravity-fall` · `visited-trail` (застовплені секції) · `touch-death` · `environment-death` (відходи, пульверизатор) · `player-death` · `temporary-modes` (мутанти їстівні) · `item-pickup` · `event-points` · `time-out` · `time-bonus` · `extra-life-threshold` · `teleport` · `teleport-cooldown` · `carrier-platform` · `one-way-cell` (гірка) · `difficulty-levels` · `score-records` · `leaderboard` · `attract-demo` · `splash-screen` · `game-pause` · `hot-seat` · `sequential-levels` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+claim-all-floor` «Пройти кожну секцію підлоги, щоб завершити рівень» · game-logic/win · 🌱.
  - `+controllable-lift` «Ввід переходить з аватара на механізм» · entities/move · 🥉.
  - `+cannon-charge-height` «Заряд визначає висоту польоту, перевантаження — смерть» · entities/move · 📎 · слот {units per floor, max}.
  - `+numbered-transporter` «Телепорт на поверх за номером клавіші, з перезарядкою» · entities/interact · 📎.
  - `+fall-damage-by-height`, `+timed-crusher`, `+slide-chute` — див. правила.

## Пропозиції до словників
- `+trigger:landed` — приземлення після падіння (з висотою) (Miner 2049er, Space Panic, BurgerTime).
- `+effect:control_transfer(a, b)` — ввід гравця переходить до іншої сутності (ліфт; керування механізмом).
- `+effect:launch(a, height)` — підкинути сутність на висоту (гармата).
- `+window:stage-intro` — екран-анонс станції/рівня перед грою.
- `+window:name-entry` — введення ініціалів для рекорду.
- `+ui:charge-meter` — індикатор накопиченого заряду (тонн TNT).
- `+card:claim-all-floor`, `+card:controllable-lift`, `+card:cannon-charge-height`, `+card:numbered-transporter` — див. вище.

## Джерела
- ⭐ [Wikipedia: Miner 2049er](https://en.wikipedia.org/wiki/Miner_2049er) — мета (пройти всю підлогу), мутанти й речі, транспортери, гармата, гірки, 5 життів, 10 рівнів, порти.
- [Мануал Atari 5200 (archive.org)](https://ia803209.us.archive.org/24/items/Miner_2049er_1983_Big_Five_Software/Miner_2049er_1983_Big_Five_Software_text.pdf) — 10 станцій з кількістю мутантів і речей, транспортери 1–4 з перезарядкою, ліфт, гармата 10 т/поверх, очки (5 / 80–90 / 100–1100), життя на 10 000, зони 1–255, екрани.
- [Мануал ColecoVision](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Miner 2049er.txt) — 11 рівнів, штампи, гідравлічний насос, лілійки, тротил 150 очок, життя на 10/30/50 тис.
- [Creative Computing, 1983](https://www.atarimagazines.com/cva/v1n2/miner.php) — гірки з вузькою точкою старту, пульверизатори, зламані драбини, світні («отруйні») предмети, зони.

## Непевне
- (?) Стартова кількість життів: Wikipedia — 5, Creative Computing — 3; різниться за версіями.
- (?) Безпечна висота падіння в клітинах — у джерелах лише «завжди однакова».
- (?) Чи можна вбити мутанта стрибком згори (Creative Computing — так; мануал — ні).
- (?) Поріг перевантаження гармати на Atari (ColecoVision: понад 3 т за раз — смерть).
- (?) Поведінка мутантів: патруль балкою чи переслідування.
- (?) Чи можна застовпити секції під гіркою, не зʼїхавши нею (мануал радить перевіряти їх першими).
