---
title: Petal Crash
slug: petal-crash
aka: ["Petal Crash 2", "Petal Crash Online"]
family: falling-match
also: [push-slide]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2020
platforms: [Windows, macOS, Linux, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1211110/Petal_Crash/", best: true, note: "суть правил, режими, 7 персонажів, Petal Crash Online з rollback, редактор"}
  - {kind: official, url: "http://www.petalcrash.com/about", note: "правила: ковзання до упору, вибух при збігу, сміття не штовхається; Time/Turn Trial, Versus, Puzzle 5×5 на персонажа, Story, mini board, turbo, коди пазлів"}
  - {kind: other, url: "https://moegamer.net/all-games/petal-crash/", note: "огляд: курсор, ударні хвилі в 4 боки, спавнери з лічильником, fast-forward, tug-of-war з 3 серцями, сміття"}
  - {kind: other, url: "https://www.gamingonlinux.com/2020/10/petal-crash-is-an-absolutely-beautiful-block-smashing-match-puzzler-out-now/page=1/", note: "огляд: вибух відштовхує прикріплені блоки, шкала атаки, 3 серця"}
  - {kind: steam, url: "https://store.steampowered.com/app/2697670/Petal_Crash_2/", note: "сиквел, Early Access з 29.09.2026: score attack, versus, 8 персонажів, редактор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Petal+Crash+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [inertia-slide, chain-reaction, spawner-entity, spawn-schedule, garbage-attack, simultaneous-versus, ai-opponent, online-multiplayer, move-limit, time-out, event-points, score-records, level-bank, puzzle-select, in-game-editor, state-string, character-select, mode-select, game-settings, field-size-picker, tutorial-window, keyboard-controls, +cursor-push, +collide-match-burst, +shockwave-knockback, +spawn-fast-forward, +garbage-adjacent-clear, +garbage-offset, +tug-of-war-meter, +shrinking-meter, +direction-restricted-moves, +adaptive-difficulty]
proposes: ["+effect:knockback", "+effect:offset_garbage", "+trigger:meter_full", "+ui:tug-meter", "+ui:hearts", "+card:collide-match-burst", "+card:shockwave-knockback", "+card:tug-of-war-meter", "+card:garbage-adjacent-clear"]
author: opus
date: 2026-11-09
---

# Petal Crash — штовхни блок курсором: він ковзає до упору, удар об свій колір вибухає й розкидає сусідів

## Суть
Екшн-головоломка Friend & Fairy у дусі аркад Neo Geo, але з механікою з push-slide: замість свапу чи падіння гравець наводить курсор на блок і штовхає його в одному з чотирьох напрямків — блок ковзає, доки не вдариться у стіну чи інший блок. Якщо вдарився в блок свого кольору — обидва (разом з однокольоровими, що до них прилягають) вибухають, а **ударна хвиля** відкидає сусідні блоки в чотири боки; ті ковзають і можуть самі вдаритись у свій колір — ланцюг. Нові блоки дають кольорові спавнери; у versus ланцюги засипають суперника сміттям, а перемогу вирішує шкала «перетягування каната».

## Поле і час
- Квадратна сітка зверху; стандартний розмір — (?); є «mini board» для новачків.
- Логіка поля покрокова: стан змінюється від поштовху і його наслідків; спавнери наповнюються **кожен хід** (moegamer). Над цим — годинник режиму: Time Trial (кілька хвилин), Versus/Story — одночасна гра двох у real-time; Turn Trial — без поспіху, ліміт ходів.
- Versus: два окремі поля поруч, спільна шкала tug-of-war унизу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | клітина | обирає блок; поштовх у 4 напрямки (3 схеми керування) |
| Кольоровий блок (пелюстка) | tile | колір | штовхнутий — ковзає до упору; удар об свій колір → вибух; ударна хвиля відкидає його |
| Спавнер | spawner | колір, лічильник | щохід наповнюється; повний → породжує блок свого кольору; блок поверх спавнера відкладає спавн, але не скасовує |
| Сміттєвий блок | hazard | — | приходить від суперника; не штовхається; знищується лише вибухом поруч |
| Стіна / край поля | static | — | зупиняє ковзання |
| Шкала tug-of-war | zone | маркер, довжина; 3 серця на гравця | маркер їде до того, хто пропустив Crash; дійшов до краю → мінус серце; шкала коротшає з часом; 0 сердець → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(cursor_dir)` → ТО `move(cursor, dir)`.
- КОЛИ `input(push, dir)` → ЯКЩО `occupied(cursor_cell, block)` і `not same(block, garbage, kind)` → ТО `slide(block, dir)` — до стіни або іншого блока.
- КОЛИ `input(push, dir)` → ЯКЩО `custom: «пазл забороняє цей напрям»` → ТО `block`.
- КОЛИ `blocked(block)` → ЯКЩО `same(block, hit_block, color)` → ТО `clear(group)` — обидва блоки й усі однокольорові, ортогонально прилеглі до них; `score(n)`.
- КОЛИ `blocked(block)` → ЯКЩО `not same(block, hit_block, color)` → ТО `custom: «блок зупиняється поруч»`.
- КОЛИ `after(clear)` → ТО `custom: «knockback — кожен блок, що прилягав до вибуху, відкидається від нього в одному з 4 напрямків»`, далі `slide(block, away)` (?).
- КОЛИ `after(clear)` → ЯКЩО `chain(n)` → ТО `combo(+1)`, `score(bonus)` — відкинутий блок, що вдарився у свій колір, продовжує ланцюг.
- КОЛИ `turn_end(player)` → ТО `counter(spawner_meter, +1)` для всіх спавнерів.
- КОЛИ `counter(spawner_meter, ==, full)` → ЯКЩО `free(spawner_cell)` → ТО `spawn_at(block, spawner_cell)` свого кольору; ЯКЩО `occupied(spawner_cell, block)` → ТО спавн відкладено.
- КОЛИ `input(fast_forward)` → ТО `spawn_at(block, all_spawners)` негайно.
- Versus: КОЛИ `after(clear)` → ТО `custom: «маркер шкали зсувається до суперника»`; КОЛИ `reach(marker, end)` → ТО `lives(-1)` для того, на чиєму боці край, `custom: «шкала скидається»`.
- Versus: КОЛИ `timer(every)` → ТО `shrink(meter, both_ends)`; КОЛИ `custom: «влучний удар»` → ТО `grow(meter, full)`.
- Versus: КОЛИ `after(clear)` → ЯКЩО `chain(>=, 2)` → ТО `send_garbage(n)` — більше ланцюгів підряд, більше сміття; КОЛИ `custom: «сміття летить до тебе»` → ЯКЩО `after(clear)` → ТО `custom: «offset — гасиш або повертаєш сміття»`.
- КОЛИ `adjacent(garbage, clear)` → ТО `disappear(garbage)`; інакше сміття не прибрати.
- КОЛИ `counter(hearts, ==, 0)` → ТО `lose`; суперник — `win`.
- Time Trial: КОЛИ `timer(==, 0)` → ТО `game_over`, рекорд для поєднання налаштувань; Turn Trial: КОЛИ `counter(moves, ==, limit)` → ТО `game_over`.
- Puzzle: КОЛИ `custom: «досягнуто мети пазла (очистити все / частину)»` → ТО `win`; КОЛИ `counter(moves, ==, limit)` → ТО `lose`, `restart`.
- Story: КОЛИ `win` → ТО `custom: «складність CPU +1»`; КОЛИ `lose` → ТО `custom: «складність CPU −1»`.
- Перемога: versus — суперник без сердець; соло — рекорд; пазл — мета за ліміт ходів · Поразка: 0 сердець / ходи скінчились · Рахунок: Crash-і й ланцюги (точних сум джерела не дають).

## Керування і ввід
- Курсор — хрестовина/стрілки; поштовх — одна з **трьох схем керування** (moegamer; деталі — (?)): напр., кнопка + напрям.
- Кнопка fast-forward — усі спавнери спрацьовують негайно (коли поле збідніло).
- Versus — локально (спліт-скрін) або через Petal Crash Online (Windows/Linux, лобі й rollback-неткод).

## Вікна, меню, HUD
- `main-menu` = `mode-select`: Story · Solo Play (Time Trial / Turn Trial) · Puzzle · Versus (CPU / людина) · Online (окремий клієнт).
- `character-select`: 7 персонажів — Lilibri, Strelitz, Penny & Deony, Ore Kid, Daize, Yosoti, Rosalia.
- `match-setup` / `settings-window`: налаштування кожного режиму — mini board, turbo, ліміти часу й ходів, правила versus.
- `puzzle-select`: у кожного персонажа сітка 5×5 пазлів — легкі в центрі, складні до країв.
- `editor-window`: Puzzle Editor; пазл ділиться **кодом** (PC); на Switch — без обміну (NWR через moegamer).
- `game-screen`: поле, курсор, спавнери з лічильниками; versus — два поля й `custom: «tug-of-war meter»` унизу, серця, сміття, що летить; соло — `score`, `timer-countdown` або `move-counter`.
- `tutorial-window` — неінтерактивне навчання.
- `dialogue-window` — сюжетні сцени Story (?); `end-screen` — підсумок раунду / рекорд.
- `lobby-window` — Petal Crash Online.
- Переходи: main-menu → character-select → (Story) dialogue → game-screen → end-screen → наступний суперник; Puzzle → puzzle-select → game-screen.

## Фічі поза полем
- `mode-time-attack` (Time Trial), `mode-puzzle` (ліміт ходів, деякі пазли обмежують напрямки), `mode-versus` + `online-multiplayer` (rollback), Story з адаптивною складністю.
- `custom-rules` / `custom-difficulty`: mini board, turbo, ліміти часу/ходів; рекорди окремо для кожного поєднання (`leaderboard-local`).
- `level-editor` + `share-code` (коди пазлів).
- `puzzle-bank` 5×5 на персонажа; `achievements` (Steam); `tutorial`.
- Немає endless-режиму й онлайн-рекордів (Switch).

## Варіації й родичі
- **Petal Crash 2** (Early Access з 29.09.2026): «кидати блоки по полю й складати вибухи кольору», «спрощені механіки»; зараз score attack і versus, 8 персонажів, редактор пазлів; обіцяно повний Puzzle, ремастер Story, run-based пригоду, онлайн з rollback.
- Родичі: Puzznic і Tetromino Slide (штовхання/ковзання + збіг), Pengo і Ice Climber (ковзання блока до упору), Kickle Cubicle, Puyo Puyo (versus зі сміттям і offset), Yoshi's Cookie (курсор над полем).
- **Осі варіацій**: як рухається плитка (свайп / падіння / **поштовх до упору**) · що дає збіг (зникнення / **вибух + відкидання сусідів**) · звідки нові плитки (згори / **спавнери на полі з лічильником**) · versus-умова (стек до верху / **tug-of-war із серцями**).

## Цікавинки для курсу
- Поштовх курсором → ковзання до упору → перевірка кольору при ударі — 📎.
- Ударна хвиля: усі сусіди вибуху відкидаються від нього і ковзають, ланцюги з порядком обробки одночасних рухів — 🥈 (детермінізм каскаду).
- Спавнер з лічильником на хід, якого блокує зайнята клітина, + fast-forward — 📎.
- Сміття, яке не штовхається і зникає лише від вибуху поруч, + offset — 🥉.
- Tug-of-war зі шкалою, що коротшає з часом, і 3 серцями — 🥉.
- Сітка пазлів 5×5 «легкі в центрі» як вікно прогресії — 🌱.
- Коди пазлів (серіалізація поля в рядок) — 📎 (картка `state-string`).

## Мапа на каталог
- Є: `inertia-slide` (ковзання до упору) · `chain-reaction` · `spawner-entity` + `spawn-schedule` (спавнери на лічильнику) · `garbage-attack` · `simultaneous-versus` · `ai-opponent` · `online-multiplayer` · `move-limit` (Turn Trial, Puzzle) · `time-out` (Time Trial) · `event-points` · `score-records` · `level-bank` + `puzzle-select` (5×5 на персонажа) · `in-game-editor` + `state-string` (коди) · `character-select` · `mode-select` · `game-settings` + `field-size-picker` (mini board, turbo) · `tutorial-window` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+cursor-push` «Курсор штовхає обраний блок у напрямку» · interface/input · 🌱.
  - `+collide-match-burst` «Удар ковзного блока об свій колір → вибух групи» · entities/interact · 📎.
  - `+shockwave-knockback` «Вибух відкидає сусідів у 4 боки» · entities/combat · 🥉 · слот {dist: 1|slide}.
  - `+spawn-fast-forward` «Кнопка: усі спавнери негайно» · interface/input · 🌱.
  - `+garbage-adjacent-clear` «Сміття зникає лише від зачистки поруч» · game-logic/opponent · 📎.
  - `+garbage-offset` (вже є з Tetris) — ланцюги гасять або повертають сміття.
  - `+tug-of-war-meter` «Спільна шкала: маркер до того, хто відстає» · game-logic/opponent · 🥉.
  - `+shrinking-meter` «Шкала коротшає з часом раунду» · game-logic/opponent · 🌱.
  - `+direction-restricted-moves` «Пазл дозволяє лише деякі напрямки» · levels/rules · 🌱.
  - `+adaptive-difficulty` «Перемога підвищує, поразка знижує складність» · progression · 📎.

## Пропозиції до словників
- `+effect:knockback` — відкинути сутність від джерела удару (тут — сусіди вибуху); уже ×11 🔥 у пропозиціях.
- `+effect:offset_garbage` — власний ланцюг гасить або повертає сміття, що летить (×2: Puyo, Tetris).
- `+trigger:meter_full` — лічильник спавнера / шкала атаки заповнились (×2: Tetris Effect, Tetrisphere).
- `+ui:tug-meter` — спільна шкала tug-of-war з маркером; `+ui:hearts` — серця раунду.
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Petal Crash](https://store.steampowered.com/app/1211110/Petal_Crash/) — ядро («штовхни блок у будь-якому напрямку, він іде до стіни чи блока; удар об свій колір — вибух, сусіди летять»), режими, 7 персонажів, Petal Crash Online з rollback, Friend & Fairy / GalaxyTrail, 12.10.2020.
- [petalcrash.com/about](http://www.petalcrash.com/about) — сміття не штовхається й зникає лише від зачистки поруч; Time/Turn Trial; Puzzle 5×5 на персонажа; Story з адаптивною складністю; mini board, turbo; редактор з кодами.
- [moegamer: Petal Crash](https://moegamer.net/all-games/petal-crash/) — курсор, 3 схеми керування, ударна хвиля в 4 боки, спавнери з лічильником на хід, fast-forward, tug-of-war (3 серця, шкала коротшає), offset сміття, пазли з обмеженими напрямками.
- [GamingOnLinux](https://www.gamingonlinux.com/2020/10/petal-crash-is-an-absolutely-beautiful-block-smashing-match-puzzler-out-now/page=1/) — вибух «відштовхує прикріплені блоки», шкала атаки, 3 серця.
- [Steam: Petal Crash 2](https://store.steampowered.com/app/2697670/Petal_Crash_2/) — Early Access, режими й плани.
- YouTube: пошук «Petal Crash gameplay».

## Непевне
- (?) Як далеко летять відкинуті блоки: на 1 клітину чи ковзають до упору (огляди кажуть лише «відштовхує», «блоки штовхають одне одного»).
- (?) Розмір стандартного поля і mini board, кількість кольорів, тривалість Time Trial, числа очок і сміття.
- (?) Чи спавнери зʼявляються випадково (поставлено `random: runtime`) і чи «щохід» означає хід гравця і в real-time versus.
- (?) Три схеми керування — назви й відмінності.
- (?) Наявність Switch-версії взято з огляду NWR (через moegamer); Steam — Windows/macOS/Linux.
- (?) Dialogue-вікна Story, екрани підсумку — з опису режимів, не з скріншотів.
