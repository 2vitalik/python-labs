---
title: Chuzzle
slug: chuzzle
aka: [Chuzzle Deluxe]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 2005
platforms: [Windows, Mac OS X, Java ME, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chuzzle", best: true, note: "6×6, 8 кольорів, зсув ряду/стовпця з загортанням, Fat/Super/Lock, колба, режими Classic/Speed/Zen/Mind Bender/BeChuzzed"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Chuzzle", note: "пошук; Chuzzle Deluxe"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chuzzle+deluxe+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [row-conveyor, wrap-edges, drag-drop-piece, swipe-gestures, line-match-clear, gravity-fall, spawn-random-cell, chain-reaction, explode-area, multi-cell-size, no-moves-left, event-points, sequential-levels, level-unlock, mode-select, difficulty-levels, goal-counter, puzzle-select, +row-col-slide-wrap, +lock-overlay, +fill-meter-level, +paid-hint, +reshuffle-charges, +idle-lock-timer, +pattern-goal, +level-end-bonus]
proposes: ["+effect:slide_line", "+effect:reshuffle", "+ui:fill-flask", "+card:row-col-slide-wrap", "+card:fill-meter-level", "+card:paid-hint", "+card:reshuffle-charges", "+card:idle-lock-timer", "+card:pattern-goal"]
author: opus
date: 2026-11-09
---

# Chuzzle — match-3, де хід не обмін, а зсув цілого рядка чи стовпця з загортанням через край

## Суть
Поле 6×6 пухнастих «чазлів» восьми кольорів. Хід — **перетягнути цілий рядок або стовпець**: він зсувається, а те, що вийшло за край, заходить з протилежного боку (тор по одній лінії). Три й більше однакових поруч лопаються, нові падають згори, можливі каскади. Прогрес рівня — **колба**: очі лопнутих чазлів летять у неї, повна колба = наступний рівень. Тиск створюють **замки**: чазл під замком блокує свій рядок і стовпець від зсуву.

## Поле і час
- Квадрат 6×6, 8 кольорів (Wikipedia).
- Кожен рядок і стовпець — кільце: зсув на k позицій циклічно переставляє 6 клітин.
- Classic / Zen / Mind Bender — покроково (хід = зсув); Speed — з таймером замків, що росте, коли гравець нічого не лопає.
- Після лопання — гравітація вниз і поповнення згори; каскади.
- Fat Chuzzle займає 2×2.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чазл | tile | колір (8) | рухається разом зі своїм рядком/стовпцем; 3+ однакових поруч → лопається; падає |
| Fat Chuzzle | tile | 2×2, колір | зʼявляється, коли відкривається порожнє місце 2×2; збіг з ним — додаткові очки |
| Super Chuzzle | tile | колір | створюється збігом 5 одного кольору; вибухає й чистить 3×3 |
| Замок (Lock) | gate | — | чіпляється до чазла; блокує зсув його рядка й стовпця; збіг цього чазла з двома іншими знищує замок |
| Trinket Chuzzle (Zen) | tile | частина веселки | замість переходу рівня; 5 штук складають веселку → charm |
| Колба (flask) | zone | рівень наповнення | очі лопнутих летять у неї; наповнена «до шийки» → кінець рівня |
| Scramble | resource | кількість | перемішує поле, коли нема ходів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag row|col, k)` → ЯКЩО `not occupied(line, lock)` → ТО `shift(line, dir)`, `wrap(chuzzles)`; інакше `block`.
- КОЛИ `after(shift)` → ЯКЩО `not custom: «склався збіг 3+»` → ТО `custom: «лінія повертається назад»` (?).
- КОЛИ `pattern(group(3+))` → ЯКЩО `same(cells, color)` and `connected(cells)` → ТО `clear(group)`, `score(n)`, `counter(flask, +n)`.
- КОЛИ `pattern(group(5, color))` → ТО `spawn_at(super_chuzzle)`; КОЛИ `destroyed(super_chuzzle)` → ТО `explode(3×3)`.
- КОЛИ `pattern(group(6+))` → ТО `counter(flask, +більше)` («значно швидше»).
- КОЛИ `after(clear)` → ТО `fall(chuzzles)`, `spawn_at(random_chuzzle, top)`; КОЛИ знову `pattern` → `clear`, `combo(+1)` — кілька лопань за хід дають більше очок.
- КОЛИ `settled` → ЯКЩО `custom: «порожнє місце 2×2»` → ТО `spawn_at(fat_chuzzle)`.
- КОЛИ `after(clear)` → ЯКЩО `occupied(group, lock)` → ТО `disappear(lock)`.
- КОЛИ `counter(flask, ==, full)` → ЯКЩО `mode(zen)` → ТО `spawn_at(trinket)`; інакше `score(1000 × level)` (Casual) / `score(2000 × level)` (Expert), ≤ 10 000, `next_level`.
- КОЛИ `counter(score, ≥, +300 000)` → ЯКЩО `mode(classic)` → ТО `give(scramble)`.
- КОЛИ `settled` → ЯКЩО `no_moves(player)` and `has(player, scramble)` → ТО `custom: «reshuffle»`, `take(scramble)`; без scramble → `game_over` (Classic).
- КОЛИ `tick` → ЯКЩО `mode(speed)` and `custom: «нічого не лопнуто»` → ТО `counter(lock_timer, +1)`; лопання → `counter(lock_timer, −n)`; КОЛИ `counter(lock_timer, ==, full)` → ТО `spawn_at(lock, random)`.
- КОЛИ `input(hint)` → ТО `custom: «показати хід»`, `score(−n)`, `counter(flask, −n)`.
- Mind Bender: КОЛИ `custom: «поле збіглось із заданим візерунком»` → ТО `win` (пазл); 3 з 5 пазлів рівня → `unlock(next_level)`.
- Перемога: нема (Classic — на рахунок) · Поразка: нема ходів і scramble · Рахунок: очки за лопання, каскади, Fat Chuzzle, бонус рівня.

## Керування і ввід
- Миша / тач: схопити чазл і тягнути вздовж рядка або стовпця — рухається вся лінія, з загортанням через край; відпустити — хід.
- Кнопка Hint (коштує очок і прогресу колби).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Classic · Speed · Zen · Mind Bender (+ секретний BeChuzzed).
- `difficulty-select` — Casual / Expert (?) (Wikipedia згадує бонус рівня для обох).
- `game-screen`: поле 6×6, `custom: «fill-flask»` (колба з очима поруч із полем = `progress-bar`), `score`, `level-number`, `hint-button`, запас scramble; у Speed — шкала таймера замка.
- `puzzle-select` — Mind Bender: 20 рівнів по 5 пазлів, позначки пройдених.
- `end-screen` — кінець гри (нема ходів).

## Фічі поза полем
- `mode-classic` · `mode-time-attack`-подібний Speed (таймер замків) · `mode-zen` (нескінченний, без замків; колба → трінкети й charm-и) · `mode-puzzle` (Mind Bender) · секретний BeChuzzed (без замків і колби, прогрес не зберігається).
- `levels-sequential` + `level-unlock` (Mind Bender) · `hint` за плату · `difficulty-presets` (Casual / Expert).
- `collectibles` — charm-и за зібрані веселки в Zen (?) — призначення в джерелі не розкрите.

## Варіації й родичі
- Відрізняється від `bejeweled` / `shariki` ходом: не обмін двох, а **циклічний зсув лінії** (родич Sixteen/«Loopy» і `2048` зі зсувом усього поля).
- Родичі в корпусі: `candy-crush` (замок-накладка), `money-puzzle-exchanger`, `hexic` (обертання трійки замість обміну).
- **Осі варіацій**: хід (обмін / зсув лінії з загортанням / зсув без загортання / обертання) · що блокує (замок на плитці / замок на всій лінії) · прогрес рівня (очки / колба-квота / візерунок).

## Цікавинки для курсу
- Циклічний зсув рядка/стовпця й перевірка збігу після нього — 🌱 (одна операція над списком).
- Замок, що блокує цілий рядок і стовпець — 📎 (легальність ходу від стану іншої плитки).
- Fat Chuzzle 2×2: багатоклітинна плитка в полі, де рухаються лінії — 🥈 (що буде, коли зсув «розрізає» 2×2).
- Колба-квота замість очок як прогрес рівня + бонус рівня з капом — 🌱.
- Speed: таймер бездіяльності породжує замки — 📎.
- Mind Bender: зсувами скласти заданий візерунок — 🥉 (пазл-режим, перевірка стану).

## Мапа на каталог
- Є: `row-conveyor` (уся смуга зсувається разом) · `wrap-edges` · `drag-drop-piece` / `swipe-gestures` · `line-match-clear` · `gravity-fall` · `spawn-random-cell` · `chain-reaction` · `explode-area` (Super, 3×3) · `multi-cell-size` (Fat 2×2) · `no-moves-left` · `event-points` · `sequential-levels` · `level-unlock` · `mode-select` · `difficulty-levels` · `goal-counter` (колба) · `puzzle-select`.
- **Нема** → пропозиції карток:
  - `+row-col-slide-wrap` «Хід — зсув рядка/стовпця з загортанням» · entities/move · 🌱.
  - `+lock-overlay` (з Candy Crush) — тут замок блокує цілу лінію.
  - `+fill-meter-level` «Рівень = наповнити шкалу прибраними плитками» · game-logic/win · 🌱.
  - `+paid-hint` «Підказка коштує очок/прогресу» · game-logic/score · 🌱.
  - `+reshuffle-charges` «Обмежені перемішування, поповнюються за очки» · game-logic/lose · 🌱.
  - `+idle-lock-timer` «Бездіяльність накопичує таймер блокера» · entities/spawn · 📎.
  - `+pattern-goal` «Скласти заданий візерунок на полі» · game-logic/win · 📎.
  - `+level-end-bonus` «Бонус рівня = множник × номер, з капом» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:slide_line` — циклічний зсув однієї лінії на k клітин (не `shift` усього поля 2048 і не `slide` однієї сутності).
- `+effect:reshuffle` — перемішати плитки поля (Bejeweled, Candy Crush, Chuzzle — підтверджую).
- `+ui:fill-flask` — шкала-колба, що наповнюється прибраними плитками (родич `progress-bar`, але з анімацією «очі летять»).
- `+card:row-col-slide-wrap` · `+card:fill-meter-level` · `+card:paid-hint` · `+card:reshuffle-charges` · `+card:idle-lock-timer` · `+card:pattern-goal` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Chuzzle](https://en.wikipedia.org/wiki/Chuzzle) — 6×6, 8 кольорів, зсув з загортанням, лопання 3+, каскади, Fat/Super/Lock, колба, бонус рівня Casual/Expert з капом 10 000, Hint за плату, scramble за 300 000, усі 5 режимів.

## Непевне
- (?) Чи повертається лінія назад, якщо зсув не дав збігу (у Wikipedia не сказано).
- (?) «Connecting three or more» — лише лінія 3+ чи будь-яка звʼязна група (L, T); у правилах записано групу як ширше прочитання.
- (?) Як зсув поводиться з Fat Chuzzle 2×2 (блокує чи рухає обидві лінії).
- (?) Назви складностей (Casual/Expert) як окремий вибір у меню; Prize closet / реакції на «тицяння» з памʼяті, у джерелі нема.
