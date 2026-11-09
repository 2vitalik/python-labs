---
title: GIPF
slug: gipf
aka: [Гіпф, ГІПФ]
family: chess-abstract
also: [push-slide]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1996
platforms: [board, web]
links:
  - {kind: other, url: "https://www.gipf.com/gipf/rules/rules.html", best: true, note: "офіційні правила (турнірна версія): вштовхування з точки, ряди з 4, продовження ряду, GIPF-фішки, кінець гри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/GIPF_(game)", note: "37 точок, 24 точки входу, базова / стандартна / турнірна гра, кілька рядів одночасно, potentials"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/GIPF_project", note: "серія Kris Burm: GIPF — хаб, potentials з інших ігор"}
  - {kind: play, url: "https://www.boardspace.net/english/about_gipf.html", note: "BoardSpace: усі три офіційні версії, робот для новачків"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=GIPF", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=GIPF+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [push-object, piece-capture, line-match-clear, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, selection-highlight, last-move-highlight, pocket, move-notation, replay, online-multiplayer, game-screen, main-menu, end-screen, help-window, settings-window, mode-select, state-as-data, unit-tests, +hex-grid-render, +edge-insert-push, +line-win, +row-extension-clear, +reserve-recycle, +reserve-empty-lose, +stacked-power-piece, +rule-variants, +add-on-pieces]
proposes: ["+effect:insert_push", "+effect:return_to_reserve", "+trigger:reserve_empty", "+cond:line_full", "+ui:entry-dots", "+ui:row-choice-highlight", "+window:row-choice", "+feature:handicap", "+card:edge-insert-push", "+card:row-extension-clear", "+card:reserve-recycle", "+card:stacked-power-piece"]
author: opus
date: 2026-11-09
---

# GIPF — вштовхуй фішку з краю гексагона: чотири своїх у ряд знімаються разом із «хвостом»

## Суть
Двоє по черзі вводять фішку зі свого запасу: ставлять її на точку за краєм поля і вштовхують усередину вздовж лінії, зсуваючи все, що стоїть на ній. Коли 4 фішки одного кольору стають у ряд, ряд знімається разом з усіма фішками, що безперервно його продовжують: свої повертаються в запас, чужі — взяті назавжди. Мета — щоб у суперника скінчились фішки для ходу (або, у стандартній грі, — щоб у нього не лишилось GIPF-фішок на полі). Перша і «хаб» гра GIPF Project Kris Burm.

## Поле і час
- Гексагон зі стороною 4 = 37 точок на трикутній сітці (`field: hex`, точки перетину ліній, а не клітини). Навколо — 24 точки входу (dots): фішка на точці входу ще не в грі.
- Кожна лінія сітки має два кінці на точках входу — вштовхувати можна з будь-якого кінця.
- По 18 фішок у кожного (білі/чорні); GIPF-фішка — дві звичайні, поставлені одна на одну, рахується як одна фішка на полі.
- Покроково, хід = одне введення; знімання рядів — не хід, а наслідок ходу (свого чи чужого). Партія ~30 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка | piece | сторона white/black | лежить у запасі або на точці; сама не ходить, лише зсувається вштовхуванням |
| GIPF-фішка | piece | 2 фішки в стосі; сторона | у стандартній грі: може лишитись на полі, коли її ряд знімається; її втрата всіх — поразка |
| Запас | supply | 18 на старті (у турнірі) | звідси береться фішка на кожен хід; порожній = поразка |
| Точка поля (spot) | terrain | 37 | може бути порожньою або зайнятою однією фішкою |
| Точка входу (dot) | zone | 24 | місце, куди ставиш фішку перед вштовхуванням; не рахується в ряди |
| Лінія | zone | 3 напрямки × паралелі | вздовж неї відбувається вштовхування і рахуються ряди |
| Взяті фішки | zone | — | чужі фішки з виграного ряду; з гри вибули |
| Potential | piece | TAMSK / ZÈRTZ / DVONN / YINSH / PÜNCT | додаткові фішки з особливою дією (варіант) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «запас порожній»` (`+trigger:reserve_empty`) → ТО `lose`.
- КОЛИ `input(enter, dot, dir)` → ЯКЩО `free(next_spot)` → ТО `place(piece, next_spot)`; `end_turn`.
- КОЛИ `input(enter, dot, dir)` → ЯКЩО `occupied(next_spot, piece)` і `custom: «на лінії попереду є хоч одна порожня точка»` → ТО `custom: «нова фішка займає точку, ряд до першої порожньої зсувається на 1»` (`+effect:insert_push`); фішки за порожньою точкою не рухаються.
- КОЛИ `input(enter, dot, dir)` → ЯКЩО `custom: «лінія зайнята до протилежного краю»` (`+cond:line_full`) → ТО `block` (з поля фішку ніколи не виштовхують).
- КОЛИ `input(move, piece)` (фішка, що вже на полі) → ТО `block`: окремо вона не ходить.
- КОЛИ `pattern(line(4))` (4 фішки одного кольору підряд, точки входу не рахуються) → ТО `custom: «зняти ряд і всі фішки, що безперервно його продовжують, будь-якого кольору»` (`clear(line)`).
- КОЛИ `after(clear)` → ЯКЩО `same(piece, row_owner, side)` → ТО `custom: «повернути в запас власника»` (`+effect:return_to_reserve`); інакше `take(opponent, piece)` — взята.
- КОЛИ `pattern(line(4))` ×2 → ЯКЩО `custom: «ряди не мають спільної фішки»` → ТО обидва `clear(line)`; інакше `choose(row)` — знімається лише один.
- КОЛИ `pattern(line(4))` в обох → ЯКЩО `turn_of(side)` → ТО першим знімає той, хто зробив хід.
- КОЛИ `pattern(line(4))` кольору суперника після вашого ходу → ТО знімає він, до свого наступного ходу; знімання — не окремий хід.
- Стандартна гра: КОЛИ `pattern(line(4))` → ЯКЩО `occupied(cell, gipf_piece)` → ТО `choose(keep|remove)` для кожної GIPF-фішки; своя знята GIPF-фішка повертається в запас як 2 звичайні.
- Стандартна гра: КОЛИ `after(clear)` → ЯКЩО `count(own_gipf_piece, ==, 0)` → ТО `lose` (поразка без жодної GIPF-фішки на полі).
- Турнірна гра: КОЛИ `turn_start(side)` → ЯКЩО `first_time` → ТО `place(gipf_piece, ...)` обовʼязково; далі GIPF-фішки дозволені, доки гравець не ввів першу звичайну.
- КОЛИ `no_moves(side)` → ТО `lose` (?) — нічиєї нема: хто першим не може ввести фішку, той програв, навіть якщо суперник програв би наступним ходом.
- Перемога: суперник без запасу (усі версії) або без GIPF-фішок на полі (стандарт/турнір) · Поразка: дзеркально · Рахунок: нема, лише стан.

## Керування і ввід
- Настільна: поставити фішку на точку входу (dot) і посунути її на першу точку поля, штовхаючи лінію.
- (цифрова версія) Клік по точці входу → підсвітка 1–2 можливих напрямків вштовхування → клік по напрямку або drag фішки всередину; заблоковані (повні) лінії не підсвічуються.
- Після ходу — вибір ряду кліком, якщо ряди перетинаються, і вибір «лишити / зняти» для кожної GIPF-фішки в ряду.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати → `mode-select` (базова / стандартна / турнірна) → `match-setup` (людина/робот, годинник).
- `game-screen`: гекс-поле з точками входу (`entry-dots`), `turn-indicator`, `reserve-counter` (лишок запасу кожного), `captured-pieces`, `row-choice-highlight` (ряди, що знімаються), `last-move-highlight`, `move-list`, `player-clock`.
- `row-choice` — модал/режим вибору ряду й долі GIPF-фішок.
- `end-screen`: хто лишився без запасу / без GIPF-фішок.
- `help-window`: правила з діаграмами рядів-продовжень.
- Переходи: main-menu → mode-select → game-screen ⇄ row-choice → end-screen.

## Фічі поза полем
- `online-multiplayer` і `ai-opponent-levels` — BoardSpace (усі три версії, робот «для новачків»), BoiteAJeux.
- `custom-rules`: базова гра +1–3 фішки в запас, `handicap` — слабшому до 3 додаткових.
- Запис партії (`move-notation`) і `replay` — на BoardSpace (?).

## Варіації й родичі
- Три офіційні версії: **базова** (без GIPF-фішок, по 3 фішки на полі на старті, 12 у запасі) · **стандартна** (по 3 GIPF-фішки на старті, 12 у запасі) · **турнірна** (порожнє поле, перший хід — GIPF-фішка, далі скільки хочеш, доки не введеш звичайну).
- Potentials — додаткові фішки з силою інших ігор серії: TAMSK (зайвий хід), ZÈRTZ (перестрибнути сусідню), DVONN (стати на чужу фішку й перефарбувати її), YINSH (рух прямою через порожні), PÜNCT (стати на чужий potential чи GIPF-фішку). MATRX GIPF обʼєднує всі.
- Родичі всередині серії (GIPF Project, Kris Burm): [zertz](zertz.md) (поле зникає), [dvonn](dvonn.md) (стоси), [yinsh](yinsh.md) (кільця і ряди з 5 — ближча кузина GIPF), PÜNCT, TZAAR, LYNGK.
- Інші родичі: [abalone](abalone.md) (штовхання ряду на гексі, але виштовхування — взяття, тут — заборонено), [line-games](line-games.md) (k-в-ряд), конвеєрний зсув ряду в Sixteen/Loopover (`row-conveyor`).
- Осі варіацій: **вштовхування** (до порожньої точки / до краю з викиданням) · **що знімає ряд** (лише ряд / ряд + продовження) · **доля своїх** (у запас / вибувають) · **ціль** (запас суперника / GIPF-фішки).

## Цікавинки для курсу
- Вштовхування з краю: знайти лінію за точкою входу, зсунути відрізок до першої порожньої, заборона повної лінії — 📎.
- Гекс-поле з 37 точками + 24 точки входу як «рамка»: координати й напрямки ліній — 🥉.
- Пошук рядів з 4 і їх продовжень у 3 напрямках, перетини, черговість гравців — 🥉.
- Рециклінг: свої фішки повертаються в запас, чужі — вибувають; запас як ресурс і таймер партії — 🌱.
- GIPF-фішка як стос із двох з правом «лишитись на полі» + перехід стандарт → турнір — 📎.
- AI minimax: оцінка «запас + GIPF-фішки + контроль центру»; ходів лише ~42 (24 точки × 1–2 напрямки) — 🥇.

## Мапа на каталог
- Є: `push-object` ↔ вштовхування ряду · `piece-capture` ↔ взяття чужих у ряду · `line-match-clear` ↔ ряд з 4 знімається · `pocket` ↔ запас і взяті поза полем · `hot-seat`, `turn-enforcement`, `move-timer`, `online-multiplayer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `selection-highlight`, `last-move-highlight` · `move-notation`, `replay`, `state-as-data`, `unit-tests` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`, `mode-select`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. hex.md) — гекс-поле точок.
  - `+edge-insert-push` «Вштовхування з краю» · entities/move · 📎 · слоти {overflow: block|eject}.
  - `+row-extension-clear` «Ряд знімається з продовженнями» · entities/interact · 📎 · слоти {n: 4} — дитина `line-match-clear`.
  - `+reserve-recycle` «Свої зняті — назад у запас» · game-logic/score · 🌱.
  - `+reserve-empty-lose` «Скінчився запас — поразка» · game-logic/lose · 🌱.
  - `+stacked-power-piece` «Подвійна фішка з особливою силою» · entities/state · 📎.
  - `+line-win` (див. line-games.md), `+rule-variants` (див. lichess-variants.md), `+add-on-pieces` «Додаткові фішки-potentials» · 🥉.

## Пропозиції до словників
- `+effect:insert_push` — нова сутність входить з краю і зсуває відрізок лінії до першої порожньої клітини (GIPF; Labyrinth — з викиданням).
- `+effect:return_to_reserve` — сутність з поля повертається в запас власника (GIPF, ряди YINSH).
- `+trigger:reserve_empty` — запас гравця порожній (GIPF, Tak).
- `+cond:line_full` — лінія від точки входу до протилежного краю зайнята повністю.
- `+ui:entry-dots` — точки входу навколо поля з підсвіткою можливих вштовхувань.
- `+ui:row-choice-highlight` — підсвітка рядів, що знімаються, з вибором при перетині.
- `+window:row-choice` — вибір ряду й долі GIPF-фішок після ходу.
- `+feature:handicap` — слабшому додаткові фішки.
- `+card:edge-insert-push`, `+card:row-extension-clear`, `+card:reserve-recycle`, `+card:stacked-power-piece` — див. «Мапа на каталог».

## Джерела
- ⭐ [gipf.com: правила GIPF](https://www.gipf.com/gipf/rules/rules.html) — офіційні правила турнірної версії: 24 точки входу, 37 точок, 18 фішок, вштовхування, ряд з 4 + продовження, перетини, кінець гри, «нічиєї нема».
- [Wikipedia: GIPF](https://en.wikipedia.org/wiki/GIPF_(game)) — базова/стандартна/турнірна, кілька рядів, potentials, Spiel des Jahres recommended 1998, видавці.
- [Wikipedia: GIPF project](https://en.wikipedia.org/wiki/GIPF_project) — склад серії і сила кожного potential.
- [BoardSpace: GIPF](https://www.boardspace.net/english/about_gipf.html) — онлайн, три версії, робот.

## Непевне
- (?) Рік: інфобокс Wikipedia — 1996, категорія — 1997.
- (?) Стартова розстановка базової гри (де саме стоять 3 фішки кожного) — бачив лише текст «3 на полі, 12 у запасі», без діаграми.
- (?) Що буває, коли запас є, але всі лінії повні (ходу нема) — офіційна сторінка не пояснює; ймовірно, поразка як «нема чим ходити».
- (?) Функції цифрових версій (нотація, replay, рівні робота) — не перевірено; офіційної цифрової версії Wikipedia не згадує.
- (?) Детальні правила potentials (коли можна вводити, як взаємодіють) — лише одним рядком на кожен.
