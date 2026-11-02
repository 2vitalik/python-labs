---
title: SpellTower
slug: spelltower
family: word-number
also: [falling-match]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 2011
platforms: [iOS, macOS, Android, web, Puzzmo]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SpellTower", best: true, note: "режими Tower/Puzzle/Rush/Battle, 5+ літер чистять сусідів, X/Q/J — ряд, порожні плитки, SpellTower+, Puzzmo"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zach_Gage", note: "автор; походження з ідеї Asher Vollmer «Tetris + Boggle» (Puzzlejuice)"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Wordtris", note: "родич 1991: літери падають у колодязь Tetris"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spelltower+plus+gameplay", note: "пошук; геймплей SpellTower+"}
  - {kind: official, url: "https://www.spelltower.com/", note: "офіційний сайт (сертифікат протермінований — не прочитано)"}
stage: v1
coverage: 70
mechanics: [swipe-gestures, cell-click, gravity-fall, event-points, score-records, leaderboard, no-moves-left, time-out, progress-acceleration, spawn-random-cell, completion-detection, daily-puzzle, profile-stats, end-screen, game-screen, help-window, settings-window, theme-select, background-music, save-progress, hot-seat, +word-validation, +path-trace-word, +word-length-scoring, +long-word-blast, +row-clear-letter, +rising-rows, +min-length-tile, +garbage-send]
proposes: ["+trigger:input", "+trigger:after", "+trigger:timer", "+cond:in_dictionary", "+cond:path_adjacent8", "+cond:length", "+effect:clear", "+effect:fall", "+effect:spawn_at", "+effect:score", "+role:tile", "+ui:word-preview", "+ui:danger-line", "+window:mode-select", "+window:word-lookup", "+feature:mode-zen", "+feature:mode-versus", "+axis:control"]
author: opus
date: 2026-11-02
---

# SpellTower — Boggle у вежі з гравітацією: проведи слово по сусідніх літерах, вони зникають, решта падає

## Суть
Поле — стовпці літерних плиток із гравітацією. Гравець веде пальцем шлях по сусідніх (з діагоналями) плитках, складаючи слово; плитки зникають, а ті, що над ними, падають. Довгі слова (5+) зносять ще й сусідні плитки, рідкісні літери — цілий ряд. Ядро — Boggle, де кожне слово змінює поле, плюс тиск Tetris у режимах, де знизу/зверху прибувають нові ряди (гра виросла з ідеї Asher Vollmer «Tetris + Boggle»).

## Поле і час
- Прямокутна сітка стовпців (≈8 завширшки (?)), плитки лежать стовпцями й падають униз на звільнені місця.
- Шари: плитки-літери + спеціальні плитки (порожні/чорні, рідкісні літери, плитки з мінімальною довжиною (?)).
- Час: покроковий у Tower і Puzzle (хід = слово); real-time у Rush (ряди додаються кожні кілька секунд).
- Режим Tower — висока вежа зі 150 плиток, видно частину; Puzzle/Rush — поле фіксованої висоти, що заповнюється.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість (рідкісна = дорожча) | бере участь у слові; зникає; падає на порожнє |
| Рідкісна літера (X, Q, J …) | tile | — | використана в слові → зникає весь її ряд |
| Порожня (чорна) плитка | object | без літери | не може бути в слові; зникає лише від «вибуху» 5+-слова поруч |
| Плитка з мінімумом (?) | tile | число N | слово через неї мусить мати ≥ N літер (?) |
| Шлях-слово | mark | послідовність клітин | кожна наступна — 8-сусід попередньої, без повторів |
| Новий ряд | spawner | випадкові літери | Puzzle: після кожного слова; Rush: за таймером |
| Верх поля | static | лінія переповнення | стовпець вище → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(trace path)` → ЯКЩО `path_adjacent8(path)` і `not repeated(cell)` → ТО `custom: «слово показується над полем під час ведення»`.
- КОЛИ `input(release)` → ЯКЩО `length(word) >= 3` і `in_dictionary(word)` → ТО `clear(path)`, `score(sum(letter_values) × length)`; інакше `block` (шлях скасовано).
- КОЛИ `after(clear)` → ЯКЩО `length(word) >= 5` → ТО `clear(neighbours(path))` — усі плитки, суміжні зі шляхом, включно з порожніми (без очок за них (?)).
- КОЛИ `after(clear)` → ЯКЩО слово містить рідкісну літеру (X/Q/J) → ТО `clear(row of that tile)`.
- КОЛИ `after(clear)` → ТО `fall(tiles above)` — стовпці осідають.
- КОЛИ `input(word)` → ЯКЩО `mode(puzzle)` → ТО `spawn_at(new row, bottom)` — поле піднімається на ряд.
- КОЛИ `timer(every few s)` → ЯКЩО `mode(rush)` → ТО `spawn_at(new row, bottom)`; темп прискорюється з часом (?).
- КОЛИ `reach(column, top)` → ТО `lose` (Puzzle/Rush).
- КОЛИ `no_moves` (у вежі не складається жодне слово) → ТО `game_over` (Tower).
- Порожні плитки — «сміття», яке не можна прибрати словом напряму: змушує складати довгі слова поруч.
- Мінімальна довжина слова — 3 (?); Q може бути плиткою «Qu» (?).
- Перемога: нема (рекорд) · Поразка: переповнення / нема слів · Рахунок: Σ вартостей літер × довжина слова (довгі слова зростають квадратично).

## Керування і ввід
- Тач: провести пальцем по плитках (`swipe-gestures`), відпустити — подати слово; можна тапати плитки по одній (?).
- Мишка на macOS — drag шляху.
- Battle: двоє на сусідніх пристроях по Bluetooth (iOS) / Wi-Fi (Android), кожен на своєму полі.

## Вікна, меню, HUD
- `game-screen`: поле, поточне слово й його вартість (`word-preview`), рахунок, `danger-line` у Puzzle/Rush (?).
- `mode-select`: Tower · Puzzle · Rush · (SpellTower+) додаткові режими, у т. ч. Debate для двох (?).
- `end-screen`: рахунок, найкраще слово (?), рекорди.
- `word-lookup`: визначення слова (iOS — словник Merriam-Webster з 2017; Android-версія 2013 не мала lookup).
- `settings-window`, `help-window`; у SpellTower+ — джазовий саундтрек.
- Переходи: `mode-select` → `game-screen` → `end-screen` → назад / заново.

## Фічі поза полем
- Режими: `mode-classic` (Tower), `mode-puzzle`-подібний Puzzle, `mode-time-attack` (Rush), `mode-versus` (Battle, з 2012), Extreme/Zen-подібні у SpellTower+ (?).
- Мультиплеєр: локальний Bluetooth/Wi-Fi; слова відправляють плитки на поле суперника (`+garbage-send`).
- `leaderboard-online` (Game Center; Scoreloop на Android), `stats`.
- `daily-puzzle`: з 2023 — щоденна гра на Puzzmo.
- Локалізації: французька й нідерландська версії (окремі словники).

## Варіації й родичі
- Boggle (шлях по сусідах, без гравітації), Wordtris (1991: літерні плитки падають у колодязь, слова чистяться), Puzzlejuice (Asher Vollmer: Tetris + Boggle), Bookworm (поле літер з падінням і вогняними плитками), Letterpress (поле літер як територія).
- SpellTower Minutes (2017, Flash) — бліц-режими; SpellTower+ (2020) — перебудова з нуля разом із Jack Schlesinger.
- **Осі варіацій:** звідки тиск (нічого — вежа / ряд за слово / ряд за таймером / сміття від суперника) · напрямок гравітації (вниз / знизу-вгору) · «бонус довжини» (вибух сусідів / знищення ряду / множник) · шлях (8-сусіди / 4-сусіди / будь-які літери).

## Цікавинки для курсу
- Перевірка шляху: 8-суміжність + без повторів + словник — 🌱.
- Гравітація стовпців після видалення довільного набору клітин — 📎 (картка `gravity-fall`).
- «Вибух» сусідів для 5+ і знищення ряду рідкісною літерою як каскад ефектів — 📎.
- Rush: нові ряди за таймером із прискоренням і лінія переповнення — 🥉.
- Пошук усіх слів на полі (DFS з trie) для детекції «нема ходів» і підказки — 🥇.
- Battle: сміття на поле суперника — 🥈 (стан двох полів + мережа/hotseat).

## Мапа на каталог
- Є: `swipe-gestures` ↔ ведення шляху · `cell-click` · `gravity-fall` · `event-points` ↔ вартість літер · `score-records` · `leaderboard` · `no-moves-left` ↔ кінець Tower · `time-out`-подібне переповнення в Rush · `progress-acceleration` ↔ темп рядів · `spawn-random-cell` ↔ нові ряди · `daily-puzzle` (Puzzmo) · `profile-stats` · `save-progress` · `hot-seat`/мультиплеєр · `end-screen` · `game-screen` · `help-window` · `settings-window` · `theme-select` · `background-music`.
- **Нема** → пропозиції карток:
  - `+word-validation` — див. wordle.md; `+path-trace-word` — див. nyt-connections.md (шлях по 8-сусідах).
  - `+word-length-scoring` «Рахунок слова: Σ вартостей × довжина» · game-logic/score · 🌱 · слоти {formula}.
  - `+long-word-blast` «Довге слово знищує сусідні клітини» · entities/interact · 📎 · слоти {min_len: 5}.
  - `+row-clear-letter` «Рідкісна літера чистить ряд» · entities/interact · 🌱 · слоти {letters}.
  - `+rising-rows` «Нові ряди знизу (за хід / за таймером)» · entities/spawn · 📎 · слоти {trigger: move|timer, interval}.
  - `+min-length-tile` «Плитка, що вимагає довгого слова» · game-logic/constraints · 🌱 (?).
  - `+garbage-send` «Твої дії надсилають сміття супернику» · game-logic/opponent · 🥈.

## Пропозиції до словників
- `+trigger:input`, `+trigger:after` (⏳) — каскад «очистити → вибух → падіння», `+trigger:timer` (Rush).
- `+cond:in_dictionary`; `+cond:path_adjacent8` — шлях по 8-сусідах без повторів; `+cond:length` — довжина слова ≥ N.
- `+effect:clear`, `+effect:fall`, `+effect:spawn_at` (⏳), `+effect:score`.
- `+role:tile`.
- `+ui:word-preview` — слово й очки під час ведення; `+ui:danger-line` (⏳).
- `+window:mode-select` (⏳), `+window:word-lookup` (див. scrabble.md).
- `+feature:mode-zen`, `+feature:mode-versus` (⏳).
- `+axis:control` — `swipe`-шлях як окремий тип вводу.

## Джерела
- ⭐ [Wikipedia: SpellTower](https://en.wikipedia.org/wiki/SpellTower) — режими, правила знищення (5+ → сусіди, X/Q/J → ряд, порожні плитки), версії, Puzzmo, рецепція.
- [Wikipedia: Zach Gage](https://en.wikipedia.org/wiki/Zach_Gage) — історія Puzzlejuice/«Tetris + Boggle».
- [Wikipedia: Wordtris](https://en.wikipedia.org/wiki/Wordtris) — родич з падінням літер.
- [spelltower.com](https://www.spelltower.com/) — офіційний сайт (не прочитано: сертифікат).
- YouTube: пошук «spelltower plus gameplay».

## Непевне
- (?) Формула очок «Σ літер × довжина» — з брифу/памʼяті, Wikipedia рахунок не описує.
- (?) Ширина поля (~8), плитки з числом-мінімумом довжини, Qu-плитка, чи Z теж чистить ряд (вікі називає X, Q, J).
- (?) Склад режимів SpellTower+ (Extreme Puzzle, Zen, Debate) — вікі каже лише «нові режими»; бриф називає Debate двогравцевим.
- (?) SpellTower+ — Wikipedia датує 2020 (бриф — 2022).
- (?) Чи дають очки плитки, знесені «вибухом» 5+-слова.
