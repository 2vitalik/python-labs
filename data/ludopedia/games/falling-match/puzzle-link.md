---
title: Puzzle Link (Renketsu Puzzle Tsunagete Pon!)
slug: puzzle-link
aka: [連結パズル つなげてポンッ!, Renketsu Puzzle Tsunagete Pon!, Tsunagete Pon!, Puzzle Link 2, つなげてポンッ!2]
family: falling-match
also: [connect-rotate]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: both
  goal: state
year: 1998
platforms: [Neo Geo Pocket, Neo Geo Pocket Color]
links:
  - {kind: other, url: "https://archive.org/download/neo-geo-pocket-manuals/puzzle_link-english_text.pdf", best: true, note: "англ. мануал NGPC: керування, екран гри, зʼєднувачі, ланцюги, режими Norm/Clear/Battle, undo, continue, name entry, опції"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Link", note: "поле 9×10, тип труби = перший блок, вільні блоки падають угору, скрол, 46 раундів, картки, режими, дати"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Link_2", note: "сиквел: 60 раундів, Endless з power-up, Card mode, ручне просування, скіни мішеней"}
  - {kind: other, url: "https://archive.org/download/neo-geo-pocket-manuals/puzzle_link_2-english_text.pdf", note: "мануал Puzzle Link 2: Power UP, Endless до рівня 9, Card Mode з анте, Auto Off"}
  - {kind: other, url: "http://thegemsbok.com/art-reviews-and-articles/mid-week-mission-puzzle-link-2-yumekobo/", note: "The Gemsbok: три цілі раунду, пауза наступу під час каскаду, ручне просування в PL2"}
  - {kind: other, url: "https://www.retrogamesreview.co.uk/2020/03/puzzle-link-neo-geo-pocket-color-review.html", note: "огляд: 5 раундів на стадію, 91 картка, ланцюги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzle+link+neo+geo+pocket+color+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [projectile-shot, shoot-forward, move-by-input, keyboard-controls, chain-reaction, event-points, progress-acceleration, completion-detection, difficulty-levels, difficulty-select, level-select, level-unlock, sequential-levels, undo-step, time-bonus, sound-warnings, score-records, leaderboard, save-progress, game-pause, game-over-continue, mode-select, attract-demo, garbage-attack, simultaneous-versus, hot-seat, ai-opponent, tutorial-window, theme-select, +typed-connector-shot, +link-separate-groups, +gravity-up, +descending-pattern, +manual-advance, +clear-all-of-type, +card-collection]
proposes: ["+cond:links_groups", "+effect:scroll_field", "+feature:card-collection", "+window:name-entry", "+window:card-file"]
author: opus
date: 2026-11-09
---

# Puzzle Link — знизу стріляєш зʼєднувачами вгору, звʼязуючи розрізнені групи мішеней одного типу; решта мішеней «падає» вгору

## Суть
Мішені кількох типів звисають згори і поле поволі сповзає донизу, до лінії поразки. Гравець — персонаж унизу, що ходить ліворуч-праворуч і **стріляє вгору зʼєднувачами** — одноклітинними відрізками труби; тип зʼєднувача задає перша мішень, у яку він влучив, і далі персонаж стріляє тим самим типом. Щойно зʼєднувачі **поєднали дві (або більше) окремі групи одного типу**, ці групи разом із трубою зникають, а решта мішеней підіймається заповнювати порожнечу над собою — гравітація тут **вгору**, і підняті мішені можуть дати ланцюг. У Normal раунд закінчується, коли після квоти звичайних мішеней зʼєднано дві мішені «c».

## Поле і час
- Сітка 9×10 клітин; мішені тримаються «стелі» (верх поля), порожнеча — знизу; під полем — рядок персонажа і лінія deadline над ним.
- Гравітація вгору: після зникнення мішені піднімаються, доки над ними порожньо (`gravity: up`).
- Real-time: у Normal поле скролиться вниз на один ряд за раз; Hard — швидше. Під час зникнення й каскаду наступ зупиняється, але персонаж рухається (The Gemsbok).
- Clear All — статична розстановка без часу: розвʼязати пазл повністю.
- Battle — два поля на двох консолях через кабель, одночасно.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | стовпець | ходить уздовж низу; стріляє зʼєднувачами вгору; памʼятає активний тип |
| Звичайна мішень | tile | тип (4 типи в PL1) | тримається групою; зникає, коли її групу звʼязано з іншою групою того ж типу |
| Група мішеней | zone | звʼязна множина однотипних | одиниця звʼязування: «окремі ділянки» одного типу |
| Мішень «c» (round clear) | tile | 2 шт. | зʼявляються після квоти звичайних; зʼєднати обидві → раунд пройдено |
| Зʼєднувач | object | тип = тип першої влученої мішені | летить угору по стовпцю, стає в поле; звʼязні зʼєднувачі одного типу утворюють трубу |
| Порожня клітина | static | — | простір для зʼєднувачів і підйому мішеней |
| Deadline | static | лінія над персонажем | мішень перетнула → кінець гри |
| Приціл і напрямна | — (ui `path-preview`) | — | показує стовпець, куди полетить зʼєднувач |
| Шкала картки | — (ui `timer-countdown`) | час | встиг до нуля → картка персонажа |
| Ряд сміття (Battle) | spawner | ряд мішеней | приходить від суперника за ланцюг |
| Power UP (PL2 Endless) | pickup | 3 постріли | зчищення мішені стирає всі мішені її типу на полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(character, dir)` уздовж низу поля.
- КОЛИ `input(fire)` → ЯКЩО `not state(character, typed)` → ТО `spawn_at(connector, above_character)`, `set_value(connector, type_of_lowest_target_in_column)`, `set_state(character, typed)`.
- КОЛИ `input(fire)` → ЯКЩО `state(character, typed)` → ТО `spawn_at(connector, above_character)` того самого типу, навіть під мішенню іншого типу.
- КОЛИ `tick` → ТО `move(connector, up)`; КОЛИ `blocked(connector)` → ТО `custom: «зʼєднувач стає в останню вільну клітину під перешкодою (мішенню чи іншим зʼєднувачем)»` (?).
- КОЛИ `after(connector_placed)` → ЯКЩО `path_exists(group_a, group_b)` через звʼязні зʼєднувачі свого типу, `same(group_a, group_b, type)` → ТО `clear(linked_groups + connectors)`, `score(n)`, `clear_state(character, typed)`.
- Якщо труба торкається трьох груп — зникають усі три: «If you link the middle target last… you can clear all three targets at once».
- КОЛИ `input(erase)` → ТО `clear(connectors)`, `clear_state(character, typed)` — передумав, обираєш інший тип.
- КОЛИ `after(clear)` → ТО `custom: «мішені під порожнечею піднімаються вгору, доки над ними порожньо»` (`fall` з `gravity: up`).
- КОЛИ `settled` → ЯКЩО `custom: «піднята мішень торкнулась мішені свого типу через залишену трубу»` → ТО `clear(groups)`, `combo(+1)`, `score(+bonus)` — ланцюг (?: точна умова).
- КОЛИ `timer(scroll_rate)` → ЯКЩО `mode(normal|battle)` and `not chain(1)` → ТО `custom: «scroll_field — поле на ряд униз, згори новий ряд»`.
- КОЛИ `custom: «мішень за 2 клітини від deadline»` → ТО `sound(warning)`.
- КОЛИ `reach(target, deadline)` (стовпець з 11 мішеней) → ТО `lose`, `window(game-over-continue)`.
- КОЛИ `counter(cleared_basic, ≥, quota)` → ТО `spawn_at(round_clear_target ×2, field)` (?: де саме).
- КОЛИ `custom: «зʼєднано дві мішені c»` → ТО `win`, `next_level`; ЯКЩО `timer(card_gauge, >, 0)` → ТО `give(player, character_card)`.
- Clear All: КОЛИ `all_gone(target)` → ТО `win`; КОЛИ `custom: «решту мішеней уже неможливо зчистити»` → ТО `lose`; очки — що менше ходів, то більше.
- Clear All: КОЛИ `input(option)` після зчищення → ТО `window(confirm-dialog)` «Undo?» → `undo(1)` — стан до попереднього зчищення.
- Battle: КОЛИ `chain(n)` на своєму полі → ТО `send_garbage(target_rows, opponent)`; КОЛИ `counter(wins, ==, 3)` → ТО `win`.
- PL2: КОЛИ `input(down)` → ТО `custom: «scroll_field вручну — +1 ряд мішеней»` (більше мішеней на полі — більше очок за Power UP).
- PL2 Endless: КОЛИ `counter(powerup_gauge, ==, full)` → ТО `give(player, power_up)` (3 постріли); КОЛИ `after(clear)` → ЯКЩО `has(player, power_up)` → ТО `clear(all_targets_of_type)`.
- PL2 Endless: КОЛИ `counter(cleared, ≥, n)` → ТО `custom: «рівень +1 (максимум 9), темп росте»`.
- Перемога: зʼєднати «c» (Normal) / зчистити все (Clear) / 3 раунди (Battle) · Поразка: стовпець перетнув deadline / нема розвʼязку (Clear) · Рахунок: зчищені мішені, бонус ланцюга, мало ходів (Clear).

## Керування і ввід
- Джойстик ←/→ — рух персонажа (у меню — курсор); A — постріл зʼєднувачем, старт, вибір; B — стерти зʼєднувачі, назад у меню; Option — пауза / зняти паузу, меню undo (Clear All).
- Puzzle Link 2: джойстик ↓ — додати ряд мішеней вручну (ризик заради очок і швидшої картки (?)).
- Тактика з мануалу: «Plan ahead!» — спершу підвести трубу під одну групу, потім вистрілити туди, де вона торкнеться кількох груп одразу.

## Вікна, меню, HUD
- `attract-demo` → A показує титульний екран: Start · Opt.
- `mode-select`: Norm · Clear · Battle (PL2: Card Game · Endless · Battle · Clear · Card).
- Normal: `difficulty-select` (Easy · Avg · Hard) + `level-select` стадії з уже пройдених (недоступно на Easy).
- Clear All: Type — Fixed / Random; Round — початковий раунд (лише Fixed).
- `game-screen`: стадія і раунд, шкала картки (`timer-countdown`), очки (`score`), мішені, мішені «c», зʼєднувачі, приціл і напрямна (`path-preview`), deadline (`danger-line`), персонаж; портрет персонажа збоку (Moomy, у PL2 — Ace).
- `pause-menu` (Option); у Clear All — `confirm-dialog` «Undo? Yes».
- `game-over-continue`: «Cont» — Yes продовжує.
- Name entry — ініціали, якщо результат у топ-5.
- Opt: Cards (перегляд здобутих карток з деталями) · Rank (`leaderboard` Normal і Clear) · Reset (стерти збережені дані). PL2 додає Targets (вибір набору мішеней) і Auto Off (вимкнення через 10 хв бездії).
- Battle: підготовка — дві консолі, два картриджі, кабель; обидва на титулі обирають Battle.

## Фічі поза полем
- Normal: `difficulty-presets` (Easy — 5 тренувальних, кампанія з 1-1 на Avg, Hard — швидший спуск); 46 раундів, по 5 на стадію; стадії відкриваються послідовно (`level-unlock`).
- `card-collection`: картка персонажа за раунд, пройдений до кінця шкали; у PL1 картки лише для перегляду (91 за оглядом).
- `undo` на 1 зчищення (Clear All); Clear: фіксовані пазли з рекомендованою кількістю ходів і випадкові майже повні поля.
- Рекорди Normal / Clear з ініціалами (`leaderboard-local`), збереження на картриджі, Reset.
- `local-multiplayer` через кабель (Battle, до 3 перемог).

## Варіації й родичі
- **Puzzle Link 2** (JP 11.1999, EU/NA 2000) — лише відмінності: Normal → Card Game, Clear → All Clear; 60 раундів (5 рівнів по 10 доступні одразу + фінальний рівень з 10 після них); навчання замість вибору складності; шкала картки — смуга «c» замість пісочного годинника; ручне просування ↓; Endless (2–4 типи мішеней, Power UP вкл/викл, рівні до 9); Card Mode — дуель картками проти CPU чи людини: 5 груп (10, J, Q, K, A), потрібно ≥2 картки кожної групи, сильніша картка дає очки, до 6 очок, анте-картка переходить переможцю; скіни мішеней — масті, фігури PL1, істоти з очима.
- Не плутати з puzz.link (`pencil-logic/puzz-link`) — онлайн-редактор паперових пазлів, інша гра.
- Родичі: [quarth.md](quarth.md) (корабель знизу стріляє блоками у фігури, що спускаються), [puzzle-bobble.md](puzzle-bobble.md) (стріляєш угору в стелю, що спускається), [magical-drop.md](magical-drop.md) (витягти знизу й кинути вгору), [shisen-sho.md](shisen-sho.md) (зʼєднати дві однакові плитки шляхом через порожнечу), Flow Free (`connect-rotate`, траса між однаковими).
- **Осі варіацій**: що летить знизу (блок-добудова — Quarth / кулька-колір — Puzzle Bobble / типізований зʼєднувач — Puzzle Link) · коли тип визначено (заздалегідь / першою влученою мішенню) · куди осідають мішені після зникнення (вниз / угору до стелі) · наступ поля (автоматичний / ручний ↓ у PL2).

## Цікавинки для курсу
- Зʼєднувач, тип якого задає перша влучена мішень, і активний тип персонажа до зчищення або стирання — 🌱.
- Звʼязування груп: union-find над мішенями і зʼєднувачами; зчистити всі групи, яких торкається одна труба — 🥉.
- Гравітація вгору (дзеркальний `fall`) з каскадом після підйому — 📎.
- Скрол поля вниз з паузою на час каскаду + deadline і звукове попередження — 📎.
- Clear All: детектор «нерозвʼязно» й undo на одне зчищення — 🥈 (детектор — 🥇, якщо чесний пошук).
- Battle: ряди сміття за ланцюг між двома полями — 🥈.
- Колекція карток за швидкість раунду + міні-гра з анте (PL2) — 📎.

## Мапа на каталог
- Є: `projectile-shot` + `shoot-forward` ↔ зʼєднувач угору · `move-by-input` + `keyboard-controls` ↔ рух персонажа (джойстик) · `chain-reaction` ↔ ланцюг після підйому · `event-points` · `progress-acceleration` (Hard, рівні Endless) · `completion-detection` ↔ Clear All · `difficulty-levels` + `difficulty-select` · `level-select` + `level-unlock` + `sequential-levels` ↔ стадії й раунди · `undo-step` ↔ Undo в Clear · `time-bonus` (найближча: картка за швидкість) · `sound-warnings` ↔ сигнал біля deadline · `score-records` + `leaderboard` ↔ топ-5 з ініціалами · `save-progress` · `game-pause` · `game-over-continue` · `mode-select` · `attract-demo` · `garbage-attack` + `simultaneous-versus` + `hot-seat` (найближча: кабель) ↔ Battle · `ai-opponent` ↔ Card Mode проти CPU · `tutorial-window` (PL2) · `theme-select` (скіни мішеней PL2).
- **Нема** → пропозиції карток:
  - `+typed-connector-shot` «Постріл, що бере тип першої влученої сутності» · entities/combat · 🌱.
  - `+link-separate-groups` «Зʼєднати ≥2 окремі групи одного типу — вони зникають» · entities/interact · 🥉.
  - `+gravity-up` «Осідання вгору, до стелі» · entities/move · 🌱.
  - `+descending-pattern` (повтор Quarth) — поле сповзає вниз рядами.
  - `+manual-advance` «Гравець сам підганяє поле заради очок» · game-logic/waves · 🌱.
  - `+clear-all-of-type` «Power-up стирає всі мішені типу» · entities/interact · 🌱.
  - `+card-collection` (повтор) — колекційні картки за раунди.

## Пропозиції до словників
- `+cond:links_groups` — мережа звʼязних зʼєднувачів торкається ≥N окремих груп свого типу (Puzzle Link; близько до ⏳ `path_exists`, але з підрахунком груп).
- `+effect:scroll_field` (повтор Quarth) — усе поле на ряд униз, згори новий ряд; у PL2 також за вводом.
- `+feature:card-collection` (повтор) — колекція карток персонажів за швидке проходження, галерея й дуель з анте.
- `+window:name-entry` (повтор Miner 2049er) — ввід ініціалів для таблиці рекордів.
- `+window:card-file` — галерея зібраних карток з деталями (родич ⏳ `codex-window`, але для нагород, не правил).

## Джерела
- ⭐ [Мануал Puzzle Link (англ., archive.org)](https://archive.org/download/neo-geo-pocket-manuals/puzzle_link-english_text.pdf) — кнопки, елементи екрана, 4 типи мішеней, постріл «for the target type that the character is under», ланцюги від підйому, Normal / Clear All / Battle, 11 мішеней за deadline, undo, continue, топ-5, Cards / Rank / Reset, підказки.
- [Wikipedia: Puzzle Link](https://en.wikipedia.org/wiki/Puzzle_Link) — 9×10, тип труби від першого блока, скасування труби, підйом вільних блоків, скрол, попередження за 2 клітини, 46 раундів, картки, дати.
- [Wikipedia: Puzzle Link 2](https://en.wikipedia.org/wiki/Puzzle_Link_2) — відмінності сиквела.
- [Мануал Puzzle Link 2 (англ., archive.org)](https://archive.org/download/neo-geo-pocket-manuals/puzzle_link_2-english_text.pdf) — ручне просування ↓, Power UP, Endless, Card Mode, Options.
- [The Gemsbok: Puzzle Link 2](http://thegemsbok.com/art-reviews-and-articles/mid-week-mission-puzzle-link-2-yumekobo/) — пауза наступу під час каскаду, три цілі раунду.
- [Retro Games Review](https://www.retrogamesreview.co.uk/2020/03/puzzle-link-neo-geo-pocket-color-review.html) — 5 раундів на стадію, 91 картка.

## Непевне
- (?) Точна геометрія: зʼєднувач стає в клітину під найнижчим обʼєктом стовпця чи прилипає інакше; звʼязність зʼєднувачів лише по 4 сусідах.
- (?) Чи зникає вся звʼязна група однотипних мішеней, чи лише мішені, яких торкається труба; «sections» у Wikipedia радить перше.
- (?) Точна умова ланцюга після підйому (мануал: «they may touch other targets of the same type»); чи потрібна залишена труба.
- (?) Чи нові ряди Normal випадкові; квота звичайних мішеней до появи «c» і де зʼявляються «c».
- (?) Імʼя керованого персонажа; Moomy — портрет збоку за Wikipedia.
- (?) Як рахуються очки (за мішень, за групу, множник ланцюга) — джерела не кажуть.
