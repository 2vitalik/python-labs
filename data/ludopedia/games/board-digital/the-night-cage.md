---
title: The Night Cage
slug: the-night-cage
aka: [Night Cage, Нічна клітка]
family: board-digital
also: [maze-arcade]
klass: figure
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: both
  goal: state
year: 2021
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/the-night-cage/rulebook", best: true, note: "повні правила: склад 80 тайлів, тор 6×6, світло радіусом 1, обвал і ями, ключі, ворота, Wax Eater, Lights Out, Nerve, Final Flickers"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Night_Cage", note: "огляд правил, автори, видавець, Kickstarter 2020, доповнення Shrieking Hollow 2024"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Night+Cage+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [wrap-edges, pipe-connectors, tile-rotate, coverage-area, fog-of-war, key-and-door, line-of-sight-attack, chain-reaction, difficulty-levels, remaining-counter, game-screen, end-screen, help-window, match-setup, +light-source, +vanish-when-unlit, +reveal-on-light, +crumbling-floor, +pit-fall-relocate, +shared-field-coop, +all-must-exit, +key-pass-adjacent, +draw-stack-timer, +spendable-nerve, +status-blind-relight, +connect-on-place]
proposes: ["+cond:lit", "+effect:discard", "+effect:fall_through", "+trigger:deck_empty", "+trigger:attacked", "+ui:light-overlay", "+ui:status-card", "+card:vanish-when-unlit", "+card:pit-fall-relocate"]
author: opus
date: 2026-11-09
---

# The Night Cage — кооп у темряві: лабіринт існує лише в радіусі свічок, вийшов зі світла — тайл падає в ніщо

## Суть
Вʼязні з однією свічкою кожен блукають підземеллям, якого нема: поле — порожній тор 6×6, а тайли-проходи тягнуться зі стопки лише туди, куди падає світло (сусідні клітини, зʼєднані проходом). Щойно тайл перестає бути освітленим — його скидають, тож лабіринт народжується й зникає довкола гравців. Треба знайти ключі (по одному на вʼязня) і всім разом стати на одні ворота, поки стопка тайлів (таймер гри) не скінчилась. Заважають обвальні тайли, ями й монстри Wax Eater, що гасять свічку.

## Поле і час
- Двобічне поле; сторона 6×6 — для будь-якої кількості гравців. Поле — **тор** в обидва напрямки: вихід за край → протилежний край; монстри атакують теж крізь край.
- Клітина або порожня (темрява), або з тайлом-проходом. Свічка вʼязня освітлює орто-сусідні клітини, куди веде прохід з його тайла (радіус 1, без діагоналей).
- Новий тайл ставлять по одному й повертають так, щоб прохід зʼєднався з тайлом, від якого світять; стіна, що закриває прохід, лишається, доки освітлена.
- Хід — по черзі за годинниковою стрілкою; один вʼязень за хід. Стопка тайлів (Draw Stack) — і генератор поля, і таймер: коли вона порожня — фаза Final Flickers.
- Інформація прихована: тайли лежать закритими (зворот — яма), що буде в темряві — невідомо; випадковість — тасування й добір.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вʼязень | player | статус Lit / Lights Out; Nerve 0–2; ≤1 ключ | Stay або Move на 1 по проходу; світить радіусом 1 |
| Стартовий тайл | terrain | 4 шт., обвальний | ставиться на першому ході в будь-яку вільну клітину |
| Прямий прохід | terrain | 10 шт., обвальний | 2 протилежні виходи |
| T-прохід | terrain | 30 шт. | 3 виходи |
| Хрестовий прохід | terrain | 12 шт. | 4 виходи |
| Ключовий тайл | terrain | 7 шт. (у грі 6), обвальний | при появі — на ньому жетон ключа |
| Жетон ключа | pickup | 1 на вʼязня | взяти — вільна дія при вході; передати сусіду — вільна дія |
| Ворота | gate | 4 шт. | єдиний тайл, де можуть стояти кілька вʼязнів; мета гри |
| Wax Eater | enemy | 12 шт. | атакує по прямих неперервних проходах у 4 напрямки, крізь край тора |
| Яма | hazard | зворот кожного тайла | вхід → падіння; лишається, доки освітлена |
| Порожня клітина | static | — | темрява; зупиняє атаки монстрів |
| Тримач тайлів (Draw Stack) | supply | 80 тайлів; зверху 2×N проходів | джерело тайлів і таймер; порожній → Final Flickers |
| Жетон Nerve | resource | 12 шт.; старт 1, макс. 2 | витрата: ще хід, Stay у темряві, Block, Charge, Sustain |
| Картка статусу | mark | Lit / Lights Out | перевертається при влучанні монстра |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «2 ключові тайли — у коробку (лишається 6 ключів і 12 монстрів); 2×N випадкових проходів — закритими на верх стопки»`; соло — 4 вʼязні під керуванням одного гравця, удвох — по 2, утрьох — господар веде 4-го.
- КОЛИ `turn_start(prisoner)` → ЯКЩО `first_time` → ТО `place(prisoner, start_tile)` у будь-яку вільну клітину, `custom: «на кожен відкритий вихід — тягнути й поставити тайл»`.
- Stay. КОЛИ `input(stay)` → ЯКЩО `not state(prisoner, lights_out)` → ТО `counter(nerve, +1)` (макс. 2), `custom: «скинути верхній тайл стопки відкритим»` (`+effect:discard`); Stay не будить монстрів.
- КОЛИ `after(stay_discard)` → ЯКЩО `custom: «скинутий тайл — монстр»` → ТО `custom: «поставити його замість тайла, зʼєднаного з вʼязнем»`.
- Move. КОЛИ `input(move, dir)` → ЯКЩО `custom: «прохід зʼєднує обидва тайли»` і (`not occupied(cell, prisoner)` або `cell(target, gate)`) → ТО `move(prisoner, dir)`; за краєм — `wrap(prisoner)`.
- Світло. КОЛИ `after(move)` → ТО для кожного відкритого виходу з нової клітини ЯКЩО `free(cell)` і `custom: «клітину ще не освітлює інший вʼязень»` (`+cond:lit`) → ТО `place(stack_top, cell)`, `rotate(tile, connect_to_source)`.
- Темрява. КОЛИ `after(illuminate)` → ТО `custom: «скинути кожен тайл, якого не освітлює жодна свічка»` (`+effect:discard`).
- Обвал. КОЛИ `turn_start(prisoner)` → ЯКЩО `custom: «вʼязень з минулого ходу стоїть на обвальному тайлі (старт, прямий, ключовий)»` → ТО `custom: «наприкінці цього ходу тайл перевертається ямою: Move — уникнув, Stay — падіння»`, `transform(tile, pit)`.
- КОЛИ `enter(prisoner, pit)` → ТО `custom: «падіння: фішка поза полем у рядку або стовпці ями»` (`+effect:fall_through`), `end_turn`.
- КОЛИ `turn_start(prisoner)` → ЯКЩО `state(prisoner, fallen)` → ТО `choose(вільна неосвітлена клітина того рядка чи стовпця)`, `place(stack_top, cell)`, `move(prisoner, cell)`; ЯКЩО `custom: «стопка порожня»` → ТО `lose` («впав навіки»).
- Ключ. КОЛИ `spawned(key_tile)` → ТО `spawn(key_token)` на ньому. КОЛИ `enter(prisoner, key_tile)` → ЯКЩО `not has(prisoner, key)` → ТО `pickup(key)`.
- КОЛИ `input(pass_key)` → ЯКЩО `adjacent(prisoner, other)` → ТО `give(other, key)` — вільна дія.
- КОЛИ `destroyed(key_tile)` → ЯКЩО `custom: «ключ ще на тайлі»` → ТО `disappear(key)` — ключ втрачено назавжди.
- Монстр. КОЛИ `line_of_sight(wax_eater, prisoner)` → ЯКЩО `custom: «вʼязень щойно рухався в лінії монстра, упав на нього або монстра зачепила атака іншого»` → ТО `custom: «атака по 4 прямих неперервних проходах, крізь край тора; порожні клітини й ями зупиняють»`.
- КОЛИ `custom: «вʼязня влучила атака»` (`+trigger:attacked`) → ТО `custom: «скинути 3 верхні тайли стопки»`, `set_state(prisoner, lights_out)`; за кожен монстр окремо.
- КОЛИ `custom: «атака дійшла до іншого монстра»` → ТО `custom: «той теж атакує»` — ланцюгова реакція.
- КОЛИ `enter(prisoner, wax_eater)` падінням → ТО `custom: «атака монстра»`, `transform(wax_eater, pit)`.
- Lights Out. ЯКЩО `state(prisoner, lights_out)` → ТО `custom: «бачить лише свій тайл; тайли, які він освітлював, скидаються, якщо не світить інший»`; Stay заборонено без Nerve; при русі наосліп — `custom: «тягнути 1 тайл для нової клітини, скинути покинутий»`.
- КОЛИ `adjacent(prisoner, lit_prisoner)` (зʼєднані проходом) → ЯКЩО `state(prisoner, lights_out)` → ТО `clear_state(prisoner, lights_out)`; поточний гравець тягне тайли для нових освітлених клітин.
- Nerve. КОЛИ `input(spend_nerve, x)` → ЯКЩО `counter(nerve, >=, 1)` → ТО `counter(nerve, −1)` і: Move Again — `extra_move` (скільки завгодно разів); Stay у Lights Out — без приросту Nerve; Block — скинути 2 тайли замість 3; Charge — `custom: «свідомо зайти на монстра: його атака, Lights Out, монстр → яма»`; Sustain — пропустити зняття тайла у Final Flickers.
- Final Flickers. КОЛИ `custom: «стопка порожня»` (`+trigger:deck_empty`) → ТО `set_state(game, final_flickers)`: нових тайлів нема.
- КОЛИ `turn_end(prisoner)` → ЯКЩО `state(game, final_flickers)` і `not custom: «Sustain»` → ТО `custom: «прибрати ще один тайл будь-де, навіть монстра»`; додаткові Move з Nerve — до цього зняття.
- Перемога: КОЛИ `all_on(prisoner, same_gate)` → ЯКЩО `has(each_prisoner, key)` → ТО `win`.
- Поразка: КОЛИ `custom: «втрачено всі 4 ворота»` або `custom: «ключів лишилось менше, ніж вʼязнів»` або `custom: «темрява розʼєднала вʼязнів назавжди»` → ТО `lose`; падіння без тайла для приземлення → `lose`.
- Складність: важче — прибрати 1 ключ або 1 ворота (або обидва); легше — додати 1–2 ключі.

## Керування і ввід
- Настільна: обрати Stay чи Move, тягнути тайли з тримача й повертати їх під зʼєднання, скидати неосвітлені, витрачати жетони Nerve, передавати ключ.
- Кооператив: усі обговорюють план; хід переходить за годинниковою стрілкою; соло — гравець по черзі веде 4 вʼязнів.
- (цифрова версія) Клік по сусідньому зʼєднаному тайлу — Move, кнопка Stay; новий тайл зʼявляється з вибором повороту (лише повороти, що зʼєднують прохід); кнопки Nerve-дій і «Передати ключ».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Гра · Соло · Правила.
- `match-setup`: 1–4 гравці (розподіл 4 вʼязнів), складність (кількість ключів і воріт).
- `game-screen`: тор 6×6 з позначками переходу через край; темрява довкола; `light-overlay` радіусів свічок; `threat-range` ліній монстрів; HUD — `remaining-counter` тайлів у стопці, `status-card` кожного вʼязня (Lit / Lights Out, Nerve, ключ), резерв ключів, `turn-indicator`.
- `help-window`: памʼятка Stay / Move / Nerve / Final Flickers.
- `end-screen`: «втекли» або причина поразки (ворота втрачено, ключів бракує, впав навіки).
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `mode-coop` — уся гра кооперативна; соло з чотирма вʼязнями.
- `difficulty-presets` через кількість ключів і воріт.
- Доповнення Shrieking Hollow (2024) — лише назва.

## Варіації й родичі
- **Осі варіацій**: існування поля (постійне / лише в світлі — тут) · радіус світла (1 орто / Lights Out — лише своя клітина / повторне запалення від сусіда) · таймер (стопка тайлів + Final Flickers) · монстр (атака по прямих проходах, ланцюг, Charge) · підлога (обвал через хід, яма з перенесенням у рядку/стовпці).
- Родичі: Forbidden Desert (`forbidden-desert.md`, кооп і колода-таймер), Labyrinth (`labyrinth.md`, тайли-проходи), Magic Maze (`magic-maze.md`, кооп і всі на виходах разом), Carcassonne (`carcassonne.md`, зʼєднання країв тайла), Pac-Man (тор).

## Цікавинки для курсу
- Поле існує лише в радіусі світла: тайл генерується при вході у світло й знищується при виході — «лабіринт на ходу» — 🥈.
- Поворот нового тайла під зʼєднання з джерелом світла: порти тайла й вибір допустимих поворотів — 📎.
- Тор 6×6, атаки й рух крізь край — 🌱.
- Монстр з атакою по прямих проходах + ланцюг монстрів — 🥉.
- Обвальні тайли й падіння з вибором місця приземлення в рядку/стовпці — 📎.
- Стопка як таймер, потім Final Flickers: щохід −1 тайл — 🌱.
- Кооп-перемога «усі з ключами на одних воротах» + перевірка недосяжності (поразка, коли ключів/воріт забракло) — 📎.
- Соло-бот або порадник: Монте-Карло по невідомій стопці — 🥇.

## Мапа на каталог
- Є: `wrap-edges` ↔ тор · `pipe-connectors` / `tile-rotate` ↔ проходи й поворот · `coverage-area` ↔ радіус свічки · `fog-of-war` ↔ видно лише в світлі · `key-and-door` ↔ ключ → ворота · `line-of-sight-attack` ↔ Wax Eater · `chain-reaction` ↔ ланцюг монстрів · `difficulty-levels` · `remaining-counter` ↔ стопка · `game-screen`, `end-screen`, `help-window`, `match-setup`.
- **Нема** → пропозиції карток:
  - `+vanish-when-unlit` «Тайли існують лише в радіусі світла» · entities/state · 🥈 · слоти {radius: 1, diagonal: false}.
  - `+reveal-on-light` / `+connect-on-place` «Тайл тягнеться при освітленні й повертається під зʼєднання» · entities/spawn · 📎.
  - `+pit-fall-relocate` «Падіння в яму: поза полем, приземлення в рядку/стовпці» · entities/interact · 📎.
  - `+draw-stack-timer` «Стопка тайлів як таймер + фаза добивання» · game-logic/lose · 🌱.
  - `+spendable-nerve` «Жетони на одноразові підсилення дій» · game-logic/economy · 🌱 · слоти {max: 2}.
  - `+status-blind-relight` «Сліпота до контакту з союзником» · entities/state · 📎.
  - `+key-pass-adjacent` «Передати предмет сусіду — вільна дія» · entities/interact · 🌱.
  - `+light-source`, `+crumbling-floor`, `+shared-field-coop`, `+all-must-exit` — уже пропоновані корпусом.

## Пропозиції до словників
- `+cond:lit(cell)` — клітину освітлює хоча б одна свічка (радіус 1 по проходах).
- `+effect:discard(tiles)` — тайл у скид (неосвітлений, верх стопки при Stay, 3 при влучанні).
- `+effect:fall_through(a)` — фішка падає крізь поле й повертається з краю рядка/стовпця (`fall` у словнику — падіння вниз до опори).
- `+trigger:deck_empty(stack)` — стопка вичерпалась (Final Flickers); `+trigger:attacked(a)` — сутність влучила атака (без HP).
- `+ui:light-overlay` — підсвітка освітлених клітин навколо свічок; `+ui:status-card` — картка стану гравця (Lit/Lights Out, жетони, ключ).
- `+card:vanish-when-unlit` · `+card:pit-fall-relocate` — див. «Мапа на каталог».

## Джерела
- ⭐ [RulesPal: The Night Cage rulebook](https://rulespal.com/the-night-cage/rulebook) — склад (80 тайлів: 4 старт, 7 ключ, 4 ворота, 12 Wax Eater, 10 прямих, 30 T, 12 хрестових; 12 Nerve), тор 6×6, світло, обвал і ями, падіння, ключі, монстри, Lights Out, Nerve-дії, Final Flickers, перемога й поразки, складність, розподіл вʼязнів.
- [Wikipedia: The Night Cage](https://en.wikipedia.org/wiki/The_Night_Cage) — огляд правил, автори (Christopher Ryan Chan, Chris McMahon, Rosswell Saunders), видавець, Kickstarter 2020, роздріб 2021, Shrieking Hollow 2024.
- YouTube: пошук «The Night Cage how to play».

## Непевне
- (?) Склад з RulesPal у сумі дає 79 тайлів, а не 80 — різниця не пояснена.
- (?) Кількість гравців: Wikipedia — 1–5, RulesPal — 1–4 (4 фішки вʼязнів); у шапці не вказую.
- (?) Точний момент перетворення обвального тайла на яму («наступного ходу після кроку на нього») — переказ, перевірити за оригінальною книжкою.
- (?) Фраза «перший вʼязень, що рухається чи падає, може уникнути атаки» — сенс неясний, не вніс як правило.
- (?) Друга сторона поля — для чого (доповнення / інший розмір) — у джерелі не сказано.
- (?) `also: [maze-arcade]` — моє тлумачення (лабіринт і монстри), не з джерел.
