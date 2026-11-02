---
title: Blood Bowl
slug: blood-bowl
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 1986
platforms: [board, PC (2009, 2015, 2023), Xbox, PlayStation, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blood_Bowl", best: true, note: "правила коротко: 11 на полі, стати MA/ST/AG/AV/PA, дії Move/Block/Blitz/Pass/Hand-off/Foul, turnover, перекиди, навички, редакції"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blood_Bowl_(2009_video_game)", note: "Cyanide 2009: покроковий і real-time режими, LRB 5.0, кар'єра, онлайн-турніри"}
  - {kind: official, url: "https://www.games-workshop.com/en-GB/searchResults?Ntt=blood+bowl", note: "пошук; настільна гра Games Workshop"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=blood+bowl", note: "пошук на BGG"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=blood+bowl"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=blood+bowl+3+gameplay", note: "пошук; геймплей цифрової версії"}
stage: v1
coverage: 70
mechanics: [hp-damage, push-object, hot-seat, ai-opponent, turn-enforcement, move-timer, event-points, save-progress, replay, game-screen, help-window, legal-move-highlight, hover-highlight, +zone-of-control, +turnover, +dice-pool-choice, +risk-reroll, +ball-scatter, +armor-injury-roll, +go-for-it, +pilot-xp-skills, +deployment-phase, +turn-limit-score, +status-effects, +roster-league]
proposes: ["+trigger:fail", "+trigger:reach", "+trigger:turn_end", "+cond:roll", "+cond:adjacent_count", "+cond:has", "+effect:dice", "+effect:end_turn", "+effect:set_status", "+effect:push", "+effect:scatter", "+role:piece", "+role:object", "+role:zone", "+ui:roll-target", "+ui:block-dice", "+ui:reroll-counter", "+ui:message-log", "+window:deployment", "+window:team-roster", "+window:kickoff-event", "+window:reroll-prompt", "+feature:roster-carryover", "+axis:session"]
author: opus
date: 2026-11-02
---

# Blood Bowl — фентезі-регбі на сітці 26×15: кожен ризик — кидок кубика, і будь-який провал закінчує твій хід

## Суть
Дві команди фентезі-рас (люди, орки, гноми, ельфи, скавени…) по 11 гравців намагаються занести мʼяч у залікову зону суперника. Хід команди — серія дій її гравців, і кожна ризикована дія (ухилення з зони захоплення, підбирання мʼяча, пас, блок) — кидок кубика; **провал = turnover**, хід одразу переходить суперникові. Ядро — порядок дій: спершу безпечне, потім ризиковане, з обмеженим запасом перекидів. Блок — кидок спеціальних кубиків, де кількість кубиків і хто обирає результат залежать від сили з підтримкою.

## Поле і час
- Поле 26×15 квадратів (у настолці — 15 у ширину, 26 у довжину): по краях — залікові зони, центральна лінія (лінія сутички), бічні «wide zones» по 4 клітини (?).
- Матч — 2 тайми по 8 ходів кожної команди (16 ходів на тайм); ходи команд чергуються. Перед кожним розіграшем — розстановка й удар (kick-off).
- Клітина — до одного гравця; гравець стоїть, лежить (prone) або оглушений (stunned, лицем донизу); мʼяч — окремий обʼєкт на клітині або в руках.
- У настолці історично був ліміт 4 хвилини на хід; у цифрових версіях — налаштовуваний таймер ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Lineman, Blitzer, Thrower, Catcher, Big Guy…) | piece | MA, ST, AG, PA, AV, навички | одна дія за хід команди; має зону захоплення, якщо стоїть |
| Лежачий гравець (prone) | piece | — | без зони захоплення; встає за 3 MA |
| Оглушений (stunned) | piece | — | наступного свого ходу лише перевертається в prone |
| Мʼяч | object | — | лежить / у руках; падає з розльотом на сусідню клітину |
| Зона захоплення (tackle zone) | zone | 8 сусідніх клітин стоячого гравця | вихід з неї — кидок Dodge; штраф до кидків у ній |
| Залікова зона | zone | рядок клітин біля краю | гравець з мʼячем у ній = тачдаун |
| Лінія сутички, wide zones | zone | — | обмеження розстановки (≥3 на лінії, ≤2 у кожній бічній) |
| Аут (за краєм поля) | hazard | — | виштовхнутого бʼють глядачі (кидок травми); мʼяч повертають натовпом |
| Тренерські перекиди (team re-rolls) | resource | 0–8 на матч | перекинути будь-який провал, не більше одного за хід |
| Суддя | neutral | — | вилучає за фол, якщо на кубиках дубль |
| Дагаут (резерв, KO, травмовані) | zone | — | вибулі; KO повертаються на 4+ перед розіграшем |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(team)` → ТО кожен гравець може один раз діяти: Move, Block (скільки завгодно); Blitz, Pass, Hand-off, Foul — по одному на хід команди.
- КОЛИ `input(move, p, cell)` → ЯКЩО `custom: «кроків ≤ MA»` → ТО `move`; понад MA — до 2 «Go For It»/Rush: `roll(d6) ≥ 2`, інакше `fail`.
- КОЛИ `leave(p, tackle_zone(enemy))` → ТО Dodge: `roll(d6) ≥ AG − custom: «модифікатори: −1 за кожну ворожу зону на клітині призначення»`; провал → `set_status(p, prone)`, armor roll, `fail`.
- КОЛИ `enter(p, ball_cell)` → ТО Pick up: `roll(d6) ≥ AG` з −1 за кожну ворожу зону; провал → `scatter(ball)`, `fail`.
- КОЛИ `input(block, a, d)` → ЯКЩО `adjacent(a, d)` and `state(a, standing)` → ТО `custom: «ST з асистами (+1 за кожного вільного союзника поруч із ціллю)»`: рівні — 1 кубик; сильніший — 2 кубики, обирає атакувальник; вдвічі сильніший — 3; слабший — 2/3, обирає захисник.
- Грані кубика блоку: **Attacker Down** (атакувальник падає → `fail`) · **Both Down** (обидва падають; навичка Block рятує) · **Push Back** ×2 (`push(d)` на клітину позаду, атакувальник може піти слідом) · **Defender Stumbles** (падає, якщо нема навички Dodge, інакше push) · **Defender Down** (push і падає).
- КОЛИ `push(d)` → ЯКЩО `edge(d)` → ТО `custom: «натовп: кидок травми без броні»`, `disappear`; ЯКЩО `occupied(cell_behind)` → ТО ланцюгове штовхання.
- КОЛИ `set_status(p, prone)` від падіння → ТО Armour roll `2d6`: ЯКЩО `custom: «результат > AV (BB2020: ≥ AV)»` → Injury roll `2d6`: 2–7 stunned · 8–9 KO (у дагаут) · 10+ casualty (кидок таблиці травм: пропуск матчу, зниження статів, смерть).
- КОЛИ `input(pass, p, target_cell)` → ТО дальність лінійкою (Quick / Short / Long / Long Bomb), кидок точності; неточний — мʼяч розлітається; гравець суперника на траєкторії може перехопити; ловець — Catch roll; ніхто не зловив → `fail`.
- КОЛИ `input(hand_off, p, q)` → ЯКЩО `adjacent(p, q)` → ТО Catch roll q; провал → мʼяч розлітається, `fail`.
- КОЛИ `input(foul, p, prone_enemy)` → ТО Armour roll з асистами; ЯКЩО `custom: «дубль на кубиках»` → ТО суддя вилучає p.
- Блиц: рух + один блок по дорозі (блок коштує 1 клітину руху).
- КОЛИ `fail` (свій гравець упав, мʼяч не зловлено чи впав, вилучення за фол, Attacker Down…) → ТО `end_turn(team)` — **turnover**.
- КОЛИ `fail` → ЯКЩО `has(team, reroll)` and `custom: «у цей хід ще не перекидали»` → ТО `choose(перекинути)`; навички (Dodge, Sure Hands, Catch, Pass, Sure Feet) дають власний перекид свого кидка.
- КОЛИ `scatter(ball)` → ТО `custom: «d8 напрямок, 1 клітина»`; якщо там гравець — він ловить (Catch roll) або мʼяч летить далі.
- КОЛИ `reach(p_with_ball, opponent_endzone)` і p стоїть → ТО `score(+1 touchdown)`, `end_turn`, нова розстановка й kick-off від того, хто забив.
- Kick-off: мʼяч летить на обрану клітину з відхиленням `d8 × d6`; подія з таблиці `2d6` (Blitz, Perfect Defence, Riot, Brilliant Coaching, Changing Weather, Pitch Invasion…).
- Перемога: більше тачдаунів після 2 таймів (у турнірах — овертайм). Рахунок: тачдауни; у лізі — SPP гравцям: TD 3, casualty 2, completion 1, interception 2, MVP 4 (?).

## Керування і ввід
- Настолка: тренер називає гравця і дію, рухає мініатюру, кидає кубики; «фішка ходу» на треку відмічає ходи.
- Цифрові: клік по гравцю → меню дій (Move, Block, Blitz, Pass, Hand-off, Foul) → клітини руху з іконками ризику (кістка Dodge з цільовим числом, GFI) → підтвердження шляху; блок — вибір цілі з показом «2 кубики червоні/білі» (хто обирає).
- Після кидка блоку — клік по грані, яку обираєш; після провалу — діалог «Використати перекид?»; після push — вибір клітини й «follow up?».
- Кінець ходу — кнопка; таймер ходу онлайн; режим real-time у BB 2009 (одночасні накази) (?).

## Вікна, меню, HUD
- `main-menu`: Campaign, Single Match/Friendly, Online (ліги, змагання), Team Management, Tutorial, Settings.
- `team-roster` — склад команди: стати, навички, SPP, травми, вартість (TV), скарбниця, найм/звільнення, Star Players.
- `deployment` — розстановка 11 гравців з перевіркою правил (лінія ≥3, бічні ≤2).
- `kickoff-event` — показ події таблиці удару.
- `game-screen`: поле 26×15 зі стадіоном; табло — рахунок, тайм, `turn-counter` обох команд, `reroll-counter`; `roll-target` іконки на клітинах шляху; `block-dice` — грані після кидка; `message-log` — журнал кожного кидка з цільовим числом і результатом; панель гравця (MA/ST/AG/PA/AV, навички); `legal-move-highlight`; `tooltip` з % успіху (BB2/BB3).
- `reroll-prompt` — підтвердження перекиду; `confirm-dialog` ризикованої дії.
- `end-screen` — підсумок матчу: тачдауни, травми, MVP, SPP, гроші, підвищення рівнів (`upgrade-window` вибору навички).
- `replay-window`, `help-window` (правила й навички), `settings-window`.

## Фічі поза полем
- Ліга (`roster-carryover`): команда між матчами накопичує SPP і навички гравців, травми й смерті перманентні, скарбниця для найму; Team Value і «inducements» для слабшої команди.
- `hotseat` (настолка й цифрові), `online-multiplayer`, `ai-opponent`, `turn-timer`, `replay`.
- `tutorial`, `codex` (навички, раси), кампанія (BB3), кастомізація команди (логотип, кольори).
- Редакції правил як `custom-rules`: 1986, 1988, 3-тя (1994: turnover і 16 ходів), LRB 4–6, BB2016, BB2020, 2025.

## Варіації й родичі
- Blood Bowl: Team Manager (карткова), Dungeonbowl (поле-підземелля з телепортами), Blood Bowl Sevens (7 гравців, менше поле), Death Zone.
- Цифрові родичі: Frozen Synapse (одночасні ходи), Mutant Football League; FUMBBL і Rebbl — онлайн-ліги за правилами LRB.
- Осі варіацій:
  - **кінець ходу**: коли всі сходили (XCOM) / дії вичерпано / **перший провал** (Blood Bowl);
  - **ZOC**: зупиняє (Wesnoth) / вихід через кидок (Blood Bowl);
  - **бій**: ймовірність одного числа / пул кубиків із вибором грані (Blood Bowl) / формула (Polytopia);
  - **мета**: знищити / доставити обʼєкт у зону (Blood Bowl — гра з мʼячем на сітці).

## Цікавинки для курсу
- Turnover: будь-який провал закінчує хід — проста подія, що робить порядок дій головним рішенням — 🌱.
- Блок: кількість кубиків із ST і асистів + хто обирає грань — 📎 (підрахунок асистів по сусідах).
- Зони захоплення з кидком на вихід і штрафом за кожну ворожу зону на клітині призначення — 📎.
- Ймовірність успіху всього плану (ланцюг кидків з перекидами) як підказка в UI — 🥉.
- Розліт мʼяча (d8 напрямок) і ланцюг ловів/відскоків — 📎.
- Штовхання з ланцюгом і виштовхуванням за край у натовп — 📎 (є `push-object`).
- Ліга: травми, SPP і навички між матчами — 🥈 (персистентний ростер).

## Мапа на каталог
- Є: `hp-damage` (опосередковано — броня/травма) · `push-object` ↔ Push Back · `hot-seat` · `ai-opponent` · `turn-enforcement` · `move-timer` ↔ таймер ходу · `event-points` ↔ SPP · `save-progress` ↔ ліга · `replay` · `legal-move-highlight` + `hover-highlight` · `game-screen`/`main-menu`/`end-screen`/`help-window`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` (з Wesnoth) — тут слот {effect: roll_to_leave}.
  - `+turnover` «Провал завершує хід» · game-logic/opponent · 🌱.
  - `+dice-pool-choice` «Пул кубиків із вибором грані» · entities/combat · 📎 · слот {dice: 1–3, chooser}.
  - `+risk-reroll` «Перекид невдачі із запасу» · game-logic/difficulty · 📎 · слот {per_turn: 1, pool}.
  - `+ball-scatter` «Розліт обʼєкта» · entities/move · 📎 · слот {dir: d8, dist}.
  - `+armor-injury-roll` «Броня → травма двома кидками» · entities/combat · 📎.
  - `+go-for-it` «Ризикований додатковий крок» · entities/move · 🌱 · слот {extra: 2, fail_on: 1}.
  - `+pilot-xp-skills` (з Into the Breach) — SPP і навички.
  - `+deployment-phase` (з FFT) — розстановка з обмеженнями.
  - `+turn-limit-score` (з Polytopia) — 2×8 ходів, рахунок.
  - `+status-effects` (з Wesnoth) — prone, stunned, KO.
  - `+roster-league` «Ліга з персистентним ростером» · levels/progression · 🥈 · слот {injuries, spp, treasury}.

## Пропозиції до словників
- `+trigger:fail(roll)` — провал кидка як подія (turnover, перекид); `+trigger:reach` ⏳ — тачдаун; `+trigger:turn_end` ⏳.
- `+cond:roll(op, n)` — результат кидка проти цільового числа; `+cond:adjacent_count` ⏳ — асисти й штрафи зон; `+cond:has` ⏳ — навичка/перекид.
- `+effect:dice(n, sides)` — кинути кубики (не плутати з `+effect:roll` = скочування); `+effect:end_turn` ⏳; `+effect:set_status` (з Into the Breach) — prone/stunned/KO; `+effect:push` ✅; `+effect:scatter(a, dir_dice, dist)` — випадкове зміщення обʼєкта.
- `+role:object` ✅ — мʼяч; `+role:zone` ⏳ — залікова зона, зона захоплення.
- `+ui:roll-target` — цільове число / % на клітині шляху; `+ui:block-dice` — грані й хто обирає; `+ui:reroll-counter`; `+ui:message-log` ⏳ — журнал кидків.
- `+window:deployment` (≈ `+window:formation` з FFT); `+window:team-roster`; `+window:kickoff-event`; `+window:reroll-prompt`.
- `+feature:roster-carryover` (з Wesnoth) — ліга.
- `+axis:session` = `match` (+ `league`).

## Джерела
- ⭐ [Wikipedia: Blood Bowl](https://en.wikipedia.org/wiki/Blood_Bowl) — стати, дії й обмеження «одна на хід», turnover, перекиди, навички, редакції 1986–2025, цифрові ігри.
- [Wikipedia: Blood Bowl (2009 video game)](https://en.wikipedia.org/wiki/Blood_Bowl_(2009_video_game)) — Cyanide, LRB 5.0, покроковий і real-time режими, кар'єра, онлайн-турніри, платформи.
- [Games Workshop: пошук «blood bowl»](https://www.games-workshop.com/en-GB/searchResults?Ntt=blood+bowl) — настільна гра й правила.
- [BGG: пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=blood+bowl) — сторінки редакцій.
- YouTube: пошук «blood bowl 3 gameplay».

## Непевне
- (?) Детальні числа (Dodge через AG у BB2020 vs таблиця AG у LRB, GFI 2+, броня «> AV» vs «≥ AV», травми 2–7/8–9/10+, SPP) — з памʼяті: WebSearch вичерпано, офіційні правила агенту недоступні.
- (?) Розмір wide zone (4 клітини) і точні межі розстановки.
- (?) Ліміт перекидів «один за хід» — правило редакцій від 3-ї; деталі навичок різняться між редакціями.
- (?) Real-time режим у BB 2009 — за Wikipedia є RTS-режим, але механіка не описана.
- (?) Наявність % успіху плану в UI BB2/BB3 — за памʼяттю.
