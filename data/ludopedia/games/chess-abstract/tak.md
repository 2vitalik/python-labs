---
title: Tak (Так)
slug: tak
aka: [Tak — A Beautiful Game, Так]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2016
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tak_(game)", best: true, note: "розміри дощок і запаси, перший хід чужим каменем, стоси, стіна і капстоун, дорога, плоска перемога, комі, історія (Rothfuss, Ernest)"}
  - {kind: official, url: "https://ustak.org/play-beautiful-game-tak/", note: "US Tak Association: повні правила руху стосу, ліміт перенесення, сплющування стіни"}
  - {kind: other, url: "https://ustak.org/portable-tak-notation/", note: "PTN — нотація партій (сторінку не відкривав)"}
  - {kind: play, url: "https://playtak.com", note: "онлайн-сервер; статистика переваги першого ходу (згадано у Wikipedia; не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tak+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, move-4dir, cell-click, drag-drop-piece, selection-highlight, legal-move-highlight, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, connectivity-check, reachability-check, completion-detection, field-size-picker, move-notation, replay, online-multiplayer, rating-system, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +place-stone, +connect-sides-win, +stack-control, +stack-spread-move, +carry-limit, +standing-stone, +capstone-flatten, +first-move-opponent-piece, +flat-count-win, +komi]
proposes: ["+cond:top_side", "+cond:carry_limit", "+effect:pick_up_stack", "+effect:drop_trail", "+effect:flatten", "+trigger:reserve_empty", "+ui:stack-view", "+ui:reserve-counter", "+ui:road-highlight", "+card:stack-spread-move", "+card:capstone-flatten", "+card:first-move-opponent-piece", "+card:flat-count-win"]
author: opus
date: 2026-11-09
---

# Tak — стоси каменів і дорога між краями: ставиш плоский, стоячий чи капстоун і «розсипаєш» стос по рядку

## Суть
Двоє на квадратній дошці 3×3…8×8 будують **дорогу** зі своїх каменів між протилежними краями. Хід — або поставити камінь із запасу (плоско, стоячи-«стіною» або капстоун), або взяти верх свого стосу і рознести його по прямій, лишаючи на кожній клітині хоча б один камінь. Стос належить власнику **верхнього** каменя, тож рухом можна «накрити» чужі камені. Немає взяття — є перекриття; запасний фініш — більше плоских каменів зверху, коли дошка повна або в когось скінчився запас.

## Поле і час
- Квадратна дошка N×N, N від 3 до 8 (найчастіше 5×5 і 6×6); на старті порожня.
- Запас на гравця (камені / капстоуни): 3×3 — 10/0 · 4×4 — 15/0 · 5×5 — 21/1 · 6×6 — 30/1 · 7×7 — 40/2 · 8×8 — 50/2.
- Шари: клітина містить **стос** будь-якої висоти; важливі верхній камінь (власник, тип) і порядок решти.
- Суміжність лише ортогональна (і для руху, і для дороги).
- Покроково, пасувати не можна; турніри — з годинником. Перший гравець — білі; на 5×5 перевага першого ходу ≈55 %, на 6×6 ≈52 % (дані playtak за Wikipedia).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плоский камінь (flat) | piece | сторона; лежить | рахується в дорогу; на нього можна класти/переносити інші |
| Стоячий камінь (wall) | piece | сторона; стоїть | не рахується в дорогу; на нього не можна ставити нічого, крім капстоуна, що сплющує |
| Капстоун | piece | 0–2 на гравця | рахується в дорогу; на нього нічого не ставиться; сам (останнім кроком) сплющує стіну на плоский |
| Стос | container | висота ∞; контроль — за верхнім каменем | рухається власником верху; розкладається по рядку |
| Запас (reserve) | supply | лічильник каменів і капстоунів | джерело ходу «поставити»; вичерпався — кінець гри |
| Клітина | zone | порожня / стос | ставити можна лише на порожню |
| Край дошки | zone | 4 краї, пари протилежних | дорога зʼєднує пару протилежних |
| Дорога | zone | ланцюг своїх flat/cap-верхів | перемога, якщо торкається двох протилежних країв |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `first_time` (перший хід кожного) → ТО `place(opponent_flat, cell)` — ставиш **чужий** плоский камінь на будь-яку порожню клітину.
- КОЛИ `input(place, kind, cell)` → ЯКЩО `free(cell)` і `has(reserve, kind)` → ТО `place(kind, cell)` (kind = flat / wall / capstone); `end_turn`.
- КОЛИ `input(pick, cell, k)` → ЯКЩО `custom: «верхній камінь стосу — мій»` (`+cond:top_side`) і `custom: «k ≤ N і k ≤ висоти»` (`+cond:carry_limit`) → ТО `custom: «зняти k верхніх, зберігши порядок»` (`+effect:pick_up_stack`).
- КОЛИ `input(move, dir)` → ТО `custom: «рух прямою, на кожну наступну клітину лишити ≥1 камінь знизу взятих»` (`+effect:drop_trail`); стартову клітину можна лишити порожньою; поворот і діагональ — `block`.
- КОЛИ `input(move, dir)` → ЯКЩО `occupied(next, wall)` або `occupied(next, capstone)` → ТО `block` (через стіну й капстоун не переступити).
- КОЛИ `input(move, dir)` → ЯКЩО `occupied(next, wall)` і `custom: «останнім кроком на неї падає сам капстоун»` → ТО `transform(wall, flat)` (`+effect:flatten`), капстоун стає зверху.
- КОЛИ `after(move)` → ТО `custom: «стос контролює власник нового верху»` — перекриті камені суперника «в полоні», доки їх не відкриють.
- КОЛИ `after(place|move)` → ЯКЩО `path_exists(edge_a, edge_b)` через свої flat/cap-верхи, ортогонально → ТО `win` (дорога).
- КОЛИ `after(move)` → ЯКЩО дороги склались в обох → ТО `win` тому, хто ходив («Dragon clause»).
- КОЛИ `custom: «дошка заповнена або гравець поставив останній камінь із запасу»` (`+trigger:reserve_empty`) → ЯКЩО дороги нема → ТО `custom: «порахувати плоскі верхи кожного»`; більше — `win`, рівно — `draw`.
- Комі (турніри USTA): `counter(flats, +2)` другому гравцю у плоскому підрахунку.
- Пас — `block`: хід обовʼязковий.
- Перемога: дорога або більше плоских верхів · Поразка: навпаки · Рахунок: у турнірах — очки за розмір перемоги (?).

## Керування і ввід
- Настільна: кладеш камінь плоско чи на ребро; береш у руку верхні k каменів стосу й розкладаєш знизу по одному-кілька.
- (цифрова версія) Клік по порожній клітині → вибір типу (flat / wall / cap, перемикач або повторний клік); клік по своєму стосу → вибір k (кількість у руці) → клацання по сусідніх клітинах у напрямку руху, кожне клацання кладе 1 камінь (повторне — ще один).
- Підсвітка дозволених клітин продовження; скасувати незавершене перенесення; drag стосу з розгортанням.
- Нотація PTN для запису партій (розміщення типом, рух з кількістю і розкладом).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Онлайн · Проти AI · З другом · Задачі (?) · Правила → `help-window` · Налаштування.
- `match-setup`: розмір дошки (3–8), комі, годинник, колір.
- `game-screen`: дошка; стоси як вежі з видимим порядком (`stack-view`, спливна підказка з повним складом); `reserve-counter` — лишилось каменів і капстоунів у кожного; `turn-indicator`; `player-clock`; `move-list` (PTN); `last-move-highlight`; `road-highlight` — підсвітка переможної дороги.
- `end-screen`: перемога дорогою / плоска перемога / нічия; рахунок плоских.
- `replay-window` — перегляд партії за PTN.
- Переходи: main-menu → match-setup → game-screen → end-screen → replay-window / реванш.

## Фічі поза полем
- `online-multiplayer`, `rating` (playtak), `turn-timer`.
- `ai-opponent-levels`; `custom-rules` — розмір дошки, комі.
- `export-import` партій у PTN; `replay`.
- `komi` — компенсація другому гравцю, як у го.

## Варіації й родичі
- Розміри 3×3 … 8×8 — по суті різні ігри (на 3×3 і 4×4 нема капстоуна).
- Комі 0 / 2 / дробові варіанти (?); турнірні правила USTA.
- Походить із вигаданої гри з роману Патріка Ротфусса «The Wise Man's Fear» (2011); дизайн — James Ernest з Ротфуссом (2014), Kickstarter Cheapass Games (2016), реліз 2017.
- Родичі: Hex (дорога між краями), го (комі, контроль поля), lasca (стоси зі «полоненими» знизу), Focus/Domination (?), checkers-variants.
- **Осі варіацій**: стос (нема / контроль верхом / ліміт висоти) · рух стосу (цілим / розкладом слідом) · типи каменів (лише плоский / стіна / капстоун) · мета (дорога / підрахунок верхів / обидва).

## Цікавинки для курсу
- Клітина як стос (список), контроль за верхом, порядок при перенесенні — 🌱.
- Хід «підняти k і розкласти слідом»: генерація всіх розкладів (композиції k) з упором у стіни/капстоуни — 🥉.
- Капстоун сплющує стіну лише останнім кроком і лише сам — 📎 (тонкий випадок легальності).
- Перевірка дороги BFS між протилежними краями, з урахуванням стін і чужих верхів — 📎; «Dragon clause» — 🌱.
- Плоска перемога: два тригери кінця (повна дошка / порожній запас) + підрахунок з комі — 🌱.
- AI: великий фактор розгалуження через розклади стосів; minimax з оцінкою «довжина дороги» — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns`, `move-4dir` ↔ рух лише ортогонально · `cell-click`, `drag-drop-piece`, `selection-highlight`, `legal-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `connectivity-check`, `reachability-check` ↔ дорога · `completion-detection` ↔ дошка повна · `field-size-picker` · `move-notation` ↔ PTN · `replay`, `online-multiplayer`, `rating-system` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+stack-control` «Стос, яким керує верхній» · entities/stacks · 📎 (див. lasca: `+piece-stack-capture`).
  - `+stack-spread-move` «Рознести стос слідом по прямій» · movement · 🥉 · слоти {carry_limit, min_drop: 1}.
  - `+carry-limit` «Ліміт перенесення = розмір дошки» — слот попередньої.
  - `+standing-stone` «Камінь-стіна: блокує, але не рахується» · entities · 🌱.
  - `+capstone-flatten` «Особлива фігура сплющує стіну» · entities/interaction · 📎.
  - `+first-move-opponent-piece` «Перший хід — чужим каменем» · game-logic/balance · 🌱.
  - `+flat-count-win` «Запасна перемога підрахунком верхів» · scoring · 🌱.
  - `+connect-sides-win`, `+place-stone` (див. hex.md), `+komi` (див. go.md).

## Пропозиції до словників
- `+cond:top_side` — стос контролює сторона верхнього елемента (lasca, Tak).
- `+cond:carry_limit` — кількість взятих ≤ ліміту.
- `+effect:pick_up_stack` — зняти k верхніх зі стосу в «руку».
- `+effect:drop_trail` — розкласти «руку» слідом по прямій, ≥1 на клітину.
- `+effect:flatten` — стіна → плоский під капстоуном (окремий випадок `transform`, але з умовою «останній крок, сам»).
- `+trigger:reserve_empty` — гравець витратив весь запас (кінець гри).
- `+ui:stack-view` — склад стосу; `+ui:reserve-counter` — лишок запасу кожного; `+ui:road-highlight` — підсвітка переможного шляху.
- `+card:stack-spread-move`, `+card:capstone-flatten`, `+card:first-move-opponent-piece`, `+card:flat-count-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Tak (game)](https://en.wikipedia.org/wiki/Tak_(game)) — таблиця запасів за розмірами, перший хід чужим каменем, три типи каменів, рух стосу, ліміт, дорога, Dragon clause, плоска перемога, комі +2, терміни Tak/Tinuë/Gaelet, статистика playtak, історія.
- [US Tak Association: Play Tak](https://ustak.org/play-beautiful-game-tak/) — правила руху: порядок, пряма лінія, ≥1 на клітину, не перестрибнути стіну/капстоун, сплющування, кінець гри.
- [PTN](https://ustak.org/portable-tak-notation/) — нотація (лише лінк у навігації, не відкривав).
- [playtak.com](https://playtak.com) — онлайн-сервер (згаданий у статті, не відкривав).

## Непевне
- (?) Сторінка USTA не дає 3×3 (10/0) — це лише з Wikipedia.
- (?) Типове комі «2» — для турнірів USTA; на сайтах буває 0–2 і половинне (не перевірено).
- (?) Очки за розмір перемоги (кількість лишку запасу) — бачив лише в загальних описах, у відкритих джерелах не підтверджено.
- (?) Набір вікон цифрової версії (задачі, AI-рівні) — типовий, playtak не відкривав.
