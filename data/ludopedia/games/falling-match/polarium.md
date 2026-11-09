---
title: Polarium
slug: polarium
aka: [Polarium DS, ポラリウム, Polarium Advance]
family: falling-match
also: [pencil-logic]
klass: hybrid
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2004
platforms: [Nintendo DS, GBA (Polarium Advance, 2005–2006)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Polarium", best: true, note: "правила штриха, нейтральна рамка, Challenge/Puzzle/Versus, очки Chains/Split/Borders, паролі, редактор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Polarium_Advance", note: "GBA: Solid/Hurdle/Multi-плитки, Daily Polarium на 365 пазлів, редактор на 100, Time Attack"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=polarium+ds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [path-drawing, visited-trail, line-match-clear, gravity-fall, chain-reaction, event-points, progress-acceleration, sequential-levels, level-bank, in-game-editor, level-password, level-exchange, daily-puzzle, restart-level, score-records, leaderboard, tutorial-window, mode-select, simultaneous-versus, garbage-attack, +one-stroke-flip, +row-clear-when-solved, +neutral-border-cells, +clear-all-goal, +wildcard-tile, +grade-letter, +rising-stack]
proposes: ["+effect:flip", "+cond:visited", "+card:one-stroke-flip", "+card:neutral-border-cells", "+card:grade-letter", "+ui:drawn-icon"]
author: opus
date: 2026-11-09
---

# Polarium — одним безперервним штрихом перевертай чорні й білі плитки, щоб кожен рядок став одного кольору

## Суть
Поле з чорних і білих плиток; гравець стилусом проводить **один безперервний штрих** по клітинах, і всі пройдені плитки перевертаються (чорна ↔ біла). Рядок, що став повністю чорним або повністю білим, зникає. У Puzzle-режимі задача — зчистити все поле одним штрихом (паперова логіка), у Challenge — плитки підіймаються/падають безперервно, як у Tetris, і треба встигати чистити. Гра — гібрид `puzzle` (статичні одноштрихові задачі) і `cursor` (real-time Challenge).

## Поле і час
- Квадратна сітка чорних/білих плиток, оточена рамкою сірих «нейтральних» клітин: по них можна вести штрих, вони не перевертаються й не впливають на рядки, але дозволяють одним штрихом дістати розʼєднані групи.
- Puzzle: статичне поле, без часу; один штрих — одна спроба.
- Challenge (DS): ряди плиток надходять безперервно, стопка росте на нижньому екрані; програш — стопка дійшла до верху верхнього екрана. 10 рівнів, +1 рівень за кожні 100 рядків.
- Versus: два поля, зчищені рядки зʼявляються в суперника.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | колір black/white | перевертається, коли штрих проходить по ній |
| Нейтральна клітина | terrain | сіра | прохідна для штриха, не перевертається, не входить у рядок |
| Штрих | mark | послідовність клітин | один безперервний шлях; на кінці перевертає всі пройдені плитки |
| Рядок | zone | — | повністю одного кольору → зникає |
| Рожевий ряд (Challenge) | zone | — | кінець рівня: дійшов донизу → екран чиститься, +10 000 очок |
| Solid (GBA) | tile | — | зчищений → плитки над ним падають |
| Hurdle (GBA) | static | — | штрих через неї не проходить |
| Multi (GBA) | tile | wild | рахується і як чорна, і як біла |
| Суперник (Versus) | enemy | своє поле | його зчищені рядки додаються тобі; може перевертати твої плитки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(stroke_start, cell)` → ТО `mark(cell, stroke)`.
- КОЛИ `input(stroke_move, cell)` → ЯКЩО `adjacent(cell, last)` and `custom: «клітина ще не в штриху»` and `not cell(cell, hurdle)` → ТО `mark(cell, stroke)`; інакше `block` (?).
- КОЛИ `input(stroke_end)` → ТО `custom: «flip — кожна плитка штриха чорна ↔ біла»`; нейтральні клітини без змін.
- КОЛИ `after(flip)` → ЯКЩО `pattern(row_full, same_color)` (Multi — як будь-який) → ТО `clear(row)`, `score(n)`.
- КОЛИ `after(clear)` → ЯКЩО `state(row, solid)` → ТО `fall(tiles_above)` (GBA).
- Очки за один штрих: більше рядків разом — більше очок; Chains — багато рядків одним штрихом; Split — два рядки з незчищеними між ними; Borders — рядки різної полярності одним штрихом.
- Puzzle: КОЛИ `input(stroke_end)` → ЯКЩО `all_gone(tiles)` → ТО `win`, `next_level`; інакше `restart` (спроба не вдалась).
- Challenge: КОЛИ `timer(feed_rate)` → ТО `spawn_at(row_group, top)`, `fall(rows)`; КОЛИ `reach(stack, top_of_upper_screen)` → ТО `lose`.
- Challenge: КОЛИ `counter(lines, ≥, 100 × level)` → ТО `custom: «level up»`, `speed(feed, ×k)`; КОЛИ `reach(pink_row, bottom)` → ТО `clear(all)`, `score(10000)`.
- Versus: КОЛИ `clear(rows)` → ТО `send_garbage(opponent, rows)`; power-up → `custom: «перевернути плитки суперника / заблокувати його нейтральну рамку»`.
- Перемога: поле порожнє (Puzzle) / суперник переповнений (Versus). Поразка: стопка до верху (Challenge). Рахунок: очки + рядки → літерна оцінка (A-, …).

## Керування і ввід
- DS: стилус — провести штрих по сусідніх клітинах; відпустити — завершити штрих і перевернути.
- GBA (Advance): D-pad веде курсор, A (або L для однієї руки) — почати й закінчити штрих.
- Штрих — єдина дія; у Puzzle немає «часткових» ходів.

## Вікна, меню, HUD
- `main-menu`: Challenge · Practice · Puzzle · Versus · Lounge (налаштування, туторіали, обмін пазлами бездротово).
- `puzzle-select` — 100 пазлів з позначками розвʼязаних; пройдені всі → `credits-window`.
- `editor-window` — свій пазл; генерує числовий пароль (`level-password`) для обміну.
- `game-screen` (Challenge): два екрани стопки, `score`, `custom: «lines»` (рядки), `level-number`; `popup-text` за Chains/Split/Borders.
- `leaderboard` — рекорди з намальованою гравцем іконкою, очками, рядками й літерною оцінкою.
- `tutorial-window` (у Lounge).
- `end-screen` Challenge: очки, рядки, оцінка.
- `lobby-window`/Download Play — Versus і демо бездротово.

## Фічі поза полем
- `puzzle-bank` 100 пазлів; `level-editor` + `share-code` (числові паролі) + бездротовий обмін пазлами.
- `mode-practice` — будь-який досягнутий рівень Challenge без ліміту часу й штрафу.
- `leaderboard-local` з власною іконкою; літерна оцінка результату.
- Polarium Advance: `daily-puzzle` (Daily Polarium, 365 — по одному на день року), архів розвʼязаних, `level-editor` на 100 пазлів з поступовим відкриттям плиток, `mode-time-attack` (5 важких або 10 легких випадкових), `one-hand-mode` (кнопка L).

## Варіації й родичі
- Polarium Advance (GBA) — без Challenge, нові плитки Solid/Hurdle/Multi, майже вчетверо більше пазлів.
- Родичі: Lights Out (перемикання стану клітин), Tetris (рядок повний → зникає), Flow/одноштрихові задачі (`pencil-logic`), Reversi (полярність), Gunpey (лінія через поле).
- **Осі варіацій**: що робить дія (одна клітина / хрест / **шлях**) · умова зчищення (рядок одного кольору / будь-який) · штрих (з повторами / без самоперетину) · обмеження (один штрих / ліміт штрихів / час).

## Цікавинки для курсу
- Штрих по сусідніх клітинах без повторів + перевертання наприкінці — 📎.
- Нейтральна рамка, що зʼєднує розірвані групи, — 🌱 (поле з неперевертними клітинами).
- Розвʼязувач одноштрихового пазла: пошук простого шляху, після якого всі рядки однокольорові — 🥇 (DFS по шляхах з відсіканням за рядками).
- Генерація пазла з гарантованим розвʼязком (від порожнього поля назад одним штрихом) — 🥈.
- Очки Chains/Split/Borders — класифікація зчищених рядків одного штриха — 📎.
- Числовий пароль як кодування пазла для обміну — 🥉 (серіалізація сітки в число й назад).

## Мапа на каталог
- Є: `path-drawing` (штрих drag-ом) · `visited-trail` (клітини штриха) · `line-match-clear` (рядок одного кольору) · `gravity-fall` · `chain-reaction` (Chains) · `event-points` · `progress-acceleration` · `sequential-levels` · `level-bank` · `in-game-editor` · `level-password` · `level-exchange` · `daily-puzzle` (Advance) · `restart-level` · `score-records` · `leaderboard` · `tutorial-window` · `mode-select` · `simultaneous-versus` · `garbage-attack`.
- **Нема** → пропозиції карток:
  - `+one-stroke-flip` «Один штрих перевертає пройдені клітини» · interface/input · 📎 · слот {revisit: no}.
  - `+neutral-border-cells` «Рамка прохідних неактивних клітин» · world/field · 🌱.
  - `+grade-letter` «Літерна оцінка результату (A-, B…)» · game-logic/score · 🌱.
  - `+row-clear-when-solved` · `+clear-all-goal` · `+wildcard-tile` (Multi) · `+rising-stack` (Challenge) — теги вже є в корпусі.

## Пропозиції до словників
- `+effect:flip` — перевернути двостанову плитку (чорна ↔ біла); пропозиція вже є в корпусі — підтверджую.
- `+cond:visited` — клітина вже в поточному шляху/штриху (підтверджую).
- `+card:one-stroke-flip` · `+card:neutral-border-cells` · `+card:grade-letter` — див. «Мапу».
- `+ui:drawn-icon` — іконка, яку гравець малює сам для таблиці рекордів.

## Джерела
- ⭐ [Wikipedia: Polarium](https://en.wikipedia.org/wiki/Polarium) — штрих, перевертання, нейтральна рамка, Challenge (10 рівнів по 100 рядків, рожевий ряд, +10 000), Practice, Puzzle (100, паролі, редактор), Versus, Lounge, оцінки.
- [Wikipedia: Polarium Advance](https://en.wikipedia.org/wiki/Polarium_Advance) — Solid/Hurdle/Multi, Daily Polarium на 365, редактор на 100, Time Attack, керування D-pad + A/L.
- YouTube: пошук «polarium ds gameplay».

## Непевне
- (?) Заборона проходити штрихом ту саму клітину двічі (самоперетин) — з памʼяті; Wikipedia про це мовчить.
- (?) Чи штрих може йти діагоналлю — вважаю, лише ортогонально.
- (?) Розмір поля (Puzzle і Challenge) — не знайдено.
- (?) Чи рядки в Challenge падають згори вниз, чи стопка росте від низу: Wikipedia — «блоки безперервно падають згори, накопичуються внизу».
- (?) Деталі Versus-power-up-ів; JA Wikipedia не відкрилась (404).
