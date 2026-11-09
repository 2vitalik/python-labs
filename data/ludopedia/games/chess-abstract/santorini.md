---
title: Santorini (Санторіні)
slug: santorini
aka: [Санторіні]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: layers
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: race
year: 2004
platforms: [board, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Santorini_(game)", best: true, note: "поле 5×5, хід = рух + будівля, обмеження підйому, купол, перемога на 3-му рівні, сили богів, історія Hamilton → Roxley"}
  - {kind: other, url: "https://www.ultraboardgames.com/santorini/game-rules.php", note: "повні правила: розстановка, рух на 8 сусідів, обовʼязкова будівля, поразка без ходу, прості боги з точними ефектами, 3–4 гравці"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=santorini", note: "пошук BGG (не відкривав)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=santorini", note: "пошук цифрових версій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Santorini+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [height-levels, move-8dir, piece-move-patterns, cell-click, selection-highlight, legal-move-highlight, reachable-highlight, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, character-select, placement-screen, rule-variants, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +move-then-build, +climb-limit, +dome-cap, +reach-height-win, +god-powers, +god-draft, +team-play]
proposes: ["+cond:height_diff", "+effect:build", "+effect:dome", "+trigger:moved_up", "+role:modifier", "+ui:height-view", "+ui:power-card", "+window:god-draft", "+feature:god-powers", "+card:move-then-build", "+card:climb-limit", "+card:god-powers"]
author: opus
date: 2026-11-09
---

# Santorini — два будівельники на острові 5×5: крок, потім поверх; хто перший зійде на 3-й рівень, той виграв

## Суть
Кожен гравець має двох робітників на полі 5×5. Хід завжди з двох обовʼязкових частин: **перемістити** одного робітника на сусідню клітину, потім **збудувати** поверх на клітині поруч із ним. Підійматись можна лише на 1 рівень за хід, спускатись — на скільки завгодно. Перемога — зійти своїм робітником на 3-й рівень; купол на 3-му рівні назавжди закриває клітину, тому основна тактика — «добудувати купол» перед ворогом. Версія Roxley додає **сили богів**: кожен гравець ламає одне правило по-своєму.

## Поле і час
- Сітка 5×5, суміжність 8-напрямна (з діагоналями).
- Кожна клітина має висоту 0–3 і, можливо, купол: 0 → блок 1 → блок 2 → блок 3 → купол (`field: layers`).
- Купол — кінець клітини: на неї не ходять і не будують.
- Покроково; хід = move → build (обидва обовʼязкові). Без випадковості, крім роздачі богів (`random: setup`).
- Гравців 2 (основний режим), 3 (лише з богами, вибування), 4 (команди 2×2 зі спільними робітниками).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робітник | piece | 2 на гравця; стоїть на клітині з висотою | рух на 1 з 8 сусідів: вгору ≤1 рівень, вниз — будь-скільки; клітина без робітника й купола |
| Блок рівня 1 / 2 / 3 | object | рівень = поверх | ставиться на клітину відповідної висоти; підіймає її |
| Купол | static | лише на 3-му рівні (без сил богів) | клітина назавжди закрита для руху й будівлі; «повна вежа» = 3 блоки + купол |
| Клітина | terrain | висота 0–3, купол так/ні | визначає, куди можна зійти |
| Карта бога | modifier | одна на гравця | змінює одне правило руху/будівлі/перемоги |
| Запас блоків | supply | окремо для кожного рівня | спільний; кількість обмежена (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «стартовий гравець ставить 2 робітники на будь-які клітини, потім інші»` → `place(worker, cell)` ×2.
- КОЛИ `input(select, worker)` → ЯКЩО `turn_of(side)` → ТО обраний робітник мусить і рухатись, і будувати цим ходом.
- КОЛИ `input(move, worker, to)` → ЯКЩО `custom: «to — один з 8 сусідів»` і `free(to)` (нема робітника й купола) і `custom: «висота(to) − висота(from) ≤ 1»` (`+cond:height_diff`) → ТО `move(worker, to)`; інакше `block`.
- КОЛИ `after(move)` → ЯКЩО `custom: «робітник піднявся з 2-го на 3-й рівень своїм ходом»` → ТО `win`.
- КОЛИ `input(build, cell)` → ЯКЩО `adjacent(worker, cell)` і `free(cell)` → ТО `set_cell(cell, level+1)` (`+effect:build`); ЯКЩО рівень уже 3 → `set_cell(cell, dome)` (`+effect:dome`).
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «жоден робітник не може зробити хід, а за ним будівлю»` (`no_moves(side)`) → ТО `lose`.
- Робітник, якого перемістила сила суперника (Apollo, Minotaur), «не рухався» — потрапивши так на 3-й рівень, не виграє.
- Боги, вибір: КОЛИ `game_start` → ТО `custom: «Challenger бере стільки карт богів, скільки гравців»`; інші `choose(god)` за годинниковою, Challenger — останню.
- Apollo: КОЛИ `input(move, worker, to)` → ЯКЩО `occupied(to, enemy_worker)` → ТО `swap(worker, enemy_worker)`.
- Artemis: КОЛИ `after(move)` → ТО `custom: «можна рухатись ще раз, не на стартову клітину»`.
- Athena: КОЛИ `after(move)` → ЯКЩО `custom: «робітник Athena піднявся»` (`+trigger:moved_up`) → ТО `set_state(opponents, no_climb, 1)` — наступного ходу суперники не підіймаються.
- Atlas: КОЛИ `input(build, cell)` → ТО `custom: «купол на будь-якому рівні»`.
- Demeter: КОЛИ `after(build)` → ТО `custom: «ще одна будівля, не на ту саму клітину»`.
- Hephaestus: КОЛИ `after(build)` → ТО `custom: «ще один блок (не купол) на ту саму клітину»`.
- Hermes: КОЛИ `input(move)` → ЯКЩО обидва робітники не змінюють висоту → ТО `custom: «кожен рухається будь-скільки разів по одному рівню, потім будівля»`.
- Minotaur: КОЛИ `input(move, worker, to)` → ЯКЩО `occupied(to, enemy_worker)` і `free(cell_behind)` → ТО `push(enemy_worker)`, `move(worker, to)`.
- Pan: КОЛИ `after(move)` → ЯКЩО `custom: «спустився на 2+ рівні»` → ТО `win`.
- Prometheus: КОЛИ `input(build)` до руху → ЯКЩО робітник потім не підіймається → ТО будівля і до, і після руху.
- 3 гравці: КОЛИ `custom: «гравець програв»` → ТО `disappear(його робітники)`; останній — `win`. 4 гравці: команди спільно виграють/програють.
- Перемога: зійти на 3-й рівень (або сила бога) · Поразка: нема ходу з будівлею · Рахунок: —.

## Керування і ввід
- Настільна: тривимірне поле на «скелі»-підставці; блоки трьох розмірів і куполи — фізичні.
- (цифрова версія) Клік по своєму робітнику → підсвітка дозволених клітин руху (з урахуванням висоти) → клік → підсвітка клітин будівлі навколо → клік (тип поверху визначається автоматично; для Atlas — вибір «блок / купол»).
- Сили «ще раз»: кнопка «Пропустити» для необовʼязкових частин (Artemis, Demeter).
- Обертання камери навколо поля; вид згори з цифрами висот.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати (AI / локально / онлайн (?)) · Правила → `help-window` · Налаштування → `settings-window`.
- `match-setup`: кількість гравців, з богами / без, лише прості боги.
- `god-draft` (`character-select`): Challenger обирає карти, гравці по черзі беруть.
- `placement-screen`: розставлення 2 робітників.
- `game-screen`: 3D/ізо-поле, `height-view` (цифри рівнів), `power-card` бога кожного гравця з текстом сили, `turn-indicator` з фазою «рух» / «будова», `legal-move-highlight`, `undo-button` у межах ходу.
- `end-screen`: переможець і причина (3-й рівень / суперник заблокований / сила бога).
- Переходи: main-menu → match-setup → god-draft → placement-screen → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: базова гра / прості боги (позначені квіткою гібіскуса) / складні боги; герої (Golden Fleece); `+feature:god-powers`.
- `hotseat`, `ai-opponent-levels`, `mode-coop` — командна гра 2×2.
- `rules-page` з картками богів; `codex` — каталог богів із прикладами.

## Варіації й родичі
- Дизайн Gordon Hamilton (1985 задумано, 2004 — біле деревʼяне видання), Roxley 2016 Kickstarter, роздріб 2017; друге видання з ребалансом — 2025.
- Розширення: Golden Fleece (2017), Riddle of the Sphinx (2025); спін-офи: Santorini: New York (2020), Pantheon Edition (2025).
- Родичі: hive, onitama (малі абстракти без випадковості), go (блокування простору), `height-levels`-ігри (Tak за висотою стосу).
- **Осі варіацій**: обмеження підйому (≤1 / нема) · будівля (обовʼязкова після руху / до і після / двічі) · мета (висота 3 / спуск на 2 / блок суперника) · асиметрія (нема / сила на гравця) · гравці (1×1 / FFA з вибуванням / команди).

## Цікавинки для курсу
- Поле висот і перевірка «підйом ≤1, спуск будь-який» — 🌱.
- Двофазний хід з одним обраним робітником (move → build) як маленький автомат станів — 📎.
- Сили богів як модифікатори правил (хуки «до руху / після руху / до будови / перевірка перемоги») — 🥈: класична вправа на архітектуру правил, ідеально лягає на «Мою гру».
- Купол як незворотне закриття клітини і тактика «захисного купола» — 🌱.
- AI minimax з оцінкою «висота робітників + доступні підйоми» на 5×5 — 🥉.
- 3D-рендер веж або ізо-поле з цифрами висот — 🥉.

## Мапа на каталог
- Є: `height-levels` ↔ рівні 0–3 · `move-8dir` · `piece-move-patterns` · `cell-click`, `selection-highlight`, `legal-move-highlight`, `reachable-highlight` · `no-moves-left` ↔ нема ходу = поразка · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `character-select` ↔ вибір бога · `placement-screen` ↔ розстановка робітників · `rule-variants` ↔ з богами / без · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+move-then-build` «Хід = рух + будівля тією самою фігурою» · game-logic/turns · 📎.
  - `+climb-limit` «Підйом не більше ніж на N рівнів» · movement · 🌱 · слоти {up: 1, down: ∞}.
  - `+dome-cap` «Клітина закривається назавжди» · field · 🌱.
  - `+reach-height-win` «Перемога — стати на висоту» · goals · 🌱.
  - `+god-powers` «Асиметричні сили, що ламають одне правило» · game-logic/rules · 🥈 · слоти {hooks: before_move, after_move, build, win_check}.
  - `+god-draft` «Драфт сил: Challenger обирає, інші беруть» · setup · 📎.
  - `+team-play` «Команди зі спільними фігурами» · players · 📎.

## Пропозиції до словників
- `+cond:height_diff(from, to, op, n)` — різниця висот клітин (підйом ≤1, Pan: спуск ≥2).
- `+effect:build` — підняти клітину на рівень (зараз `set_cell(cell, level+1)`); `+effect:dome` — закрити клітину назавжди.
- `+trigger:moved_up` — сутність піднялась цим ходом (Athena).
- `+role:modifier` — сутність поза полем, що змінює правила для власника (карта бога; також карти правил у інших іграх).
- `+ui:height-view` — висоти клітин цифрами/кольором; `+ui:power-card` — картка сили гравця на екрані.
- `+window:god-draft` — драфт асиметричних сил (вужче за `character-select`: обирає один, беруть по черзі).
- `+feature:god-powers` — режим з асиметричними силами.
- `+card:move-then-build`, `+card:climb-limit`, `+card:god-powers` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Santorini (game)](https://en.wikipedia.org/wiki/Santorini_(game)) — поле 5×5, два робітники, рух + будівля, обмеження підйому, купол, перемога, сили богів (без переліку), історія, розширення, друге видання.
- [UltraBoardGames: Santorini rules](https://www.ultraboardgames.com/santorini/game-rules.php) — розстановка, 8 сусідів, обовʼязкові рух і будівля, поразка без ходу, драфт богів, 10 простих богів з ефектами, «Forced Worker не рухався», правила на 3 і 4 гравці.
- Steam / BGG / YouTube — пошукові сторінки.

## Непевне
- (?) Кількість блоків кожного рівня й куполів у коробці — не підтверджено жодним відкритим джерелом.
- (?) Скільки всього карт богів (прості + складні) — не бачив.
- (?) Цифрові версії (офіційний застосунок Roxley, онлайн-режим) — не відкривав; вікна — типова «цифрова версія».
- (?) Рік: 2004 — перше видання Hamilton; масова версія Roxley — 2016/2017.
