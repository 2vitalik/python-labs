---
title: Ice-sliding puzzles (Inertia і жанр «ковзай до упору»)
slug: ice-sliding-puzzles
family: push-slide
also: [pencil-logic]
klass: avatar
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: collect
year: 2005
platforms: [PC, web, mobile, GB/GBA (Pokémon-лід)]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/inertia.html", best: true, note: "довідка Inertia: кулька, стіни, стопи, самоцвіти, міни, 8 напрямків, Solve зі стрілкою, undo після смерті"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html", note: "грати в браузері"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/", note: "Simon Tatham's Portable Puzzle Collection"}
  - {kind: other, url: "https://raw.githubusercontent.com/ghewgill/puzzles/master/inertia.c", note: "код (дзеркало): генератор (стіни/стопи/міни по 1/5), самоцвіти лише на «петлях» зі старту, солвер як TSP-вставка"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії: undo/redo, Solve, game ID"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ice+sliding+puzzle+game", note: "пошук; жанр льодових пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Simon+Tatham+Inertia+puzzle", note: "пошук; Inertia"}
stage: v1
coverage: 80
mechanics: [inertia-slide, move-8dir, move-4dir, keyboard-controls, cell-click, impassable-cells, item-pickup, collect-all, touch-death, reach-exit, reachability-check, level-solver, unsolvable-states, game-settings, field-size-picker, goal-counter, completion-detection, property-tests, save-game, +undo-redo, +undo-after-death, +solve-into-undo, +seed-share, +state-string, +hint-move, +stop-on-entity, +stop-cell, +diagonal-gap-pass, +loop-gem-generation, +stop-graph]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:blocked", "+trigger:all_gone", "+cond:cell", "+effect:slide", "+effect:counter", "+effect:message", "+role:terrain", "+role:hazard", "+ui:remaining-counter", "+ui:death-counter", "+ui:hint-marker", "+window:hints-window", "+feature:undo", "+feature:show-solution", "+feature:seed-input", "+axis:stop-rule"]
author: opus
date: 2026-11-02
---

# Ice-sliding puzzles — ковзай до упору, збери все, не вріжся в міну

## Суть
Жанр головоломок, де аватар **не може зупинитися з власної волі**: обраний напрямок означає ковзання, доки щось не зупинить — стіна, спецклітина-стоп чи інша сутність. Тому позиції, де можна стояти, — лише «точки упору», і рівень перетворюється на граф переходів між ними. Еталон — **Inertia** з колекції Simon Tatham: кулька у 8 напрямках, самоцвіти збираються на льоту, міни вбивають, стопи — безпечні зупинки; генератор гарантує, що кожен самоцвіт досяжний. Файл описує Inertia повно, а жанрові родичі — посиланнями на вже описані ігри.

## Поле і час
- Квадратна сітка W×H (Tatham — налаштовується, пресети 10×8 тощо (?)); межа поля діє як стіна.
- Один шар клітин: порожньо / стіна / стоп / міна / самоцвіт; поверх — кулька. Поле видно цілком.
- Хід = одне ковзання (будь-якої довжини); світ без вводу не змінюється (`static`). Inertia рухається у **8 напрямках**, більшість інших льодових пазлів — у 4.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кулька | player | позиція | ковзає в обраному з 8 напрямків, доки не зупиниться |
| Стіна | static | — | зупиняє кульку перед собою; діагональна щілина між двома стінами пропускає діагональний рух |
| Стоп | terrain | — | кулька, що в'їхала, зупиняється на ній за будь-якого напрямку |
| Самоцвіт | pickup | — | збирається на льоту, не зупиняє |
| Міна | hazard | — | в'їзд — смерть (навіть якщо останній самоцвіт уже зібрано в цьому ж ході) |
| Порожня клітина | terrain | — | лід: кулька ковзає далі |
| Стартова клітина | terrain | — | позначена; поводиться як стоп (?) |
| Лід Pokémon / підлога ToTM | terrain | — | див. родичів: аватар ковзає до стіни, ціль — вихід (не збирання) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir8)` → ТО `slide(ball, dir)` клітина за клітиною; хід, що одразу впирається в стіну, — `block` (не зараховується) (?).
- Під час ковзання, на кожній клітині: КОЛИ `enter(ball, gem)` → ТО `pickup`, `counter(gems_left, -1)`, рух триває.
- КОЛИ `enter(ball, stop)` → ТО `custom: «зупинка»` — кулька лишається на стопі.
- КОЛИ `blocked(ball)` (наступна клітина — стіна або край) → ТО зупинка перед нею.
- КОЛИ `custom: «діагональний рух між двома стінами, що торкаються кутами»` → ТО прохід дозволено (кулька не зупиняється).
- КОЛИ `enter(ball, mine)` → ТО `lose`, `counter(deaths, +1)`; якщо цим ходом зібрано останній самоцвіт — все одно поразка.
- КОЛИ `all_gone(gem)` (і кулька вижила) → ТО `win`; статус-рядок «COMPLETED!».
- Undo після смерті: повертає позицію перед фатальним ходом, гра триває; лічильник смертей зберігається (redo того самого ходу смертей не додає).
- Solve: КОЛИ `input(solve)` → ТО `custom: «обчислити маршрут, що збирає всі самоцвіти й повертається в поточну точку»`; на кульці зʼявляється стрілка першого напрямку; Space — зробити хід за стрілкою; після ходу не за стрілкою стрілки показуються, лише якщо пазл ще розвʼязний.
- Генерація: стіни, стопи й міни — приблизно по 1/5 клітин, один старт; самоцвіти (~1/5 від кількості клітин) ставляться лише на клітини, які можна «зібрати на петлі зі старту назад у старт»; сітку відкидають, якщо найбільша BFS-відстань від клітини до найближчого кандидата завелика. Отже, кожен самоцвіт досяжний із поверненням — розвʼязність гарантована (поки гравець не вбився).
- Солвер Tatham: граф «звідки куди можна доїхати» (вершини — точки зупинки), потім тур, що бере всі самоцвіти, — родич задачі комівояжера, тому шукається «не надто поганий» тур: жадібна вставка найдешевшої петлі до найближчого самоцвіту + прибирання зайвих відрізків.
- Перемога: усі самоцвіти зібрано. · Поразка: міна (відкатна через undo). · Рахунок: нема; статус — самоцвітів лишилось і кількість смертей.

## Керування і ввід
- Цифровий блок (8 напрямків) або клік по полю — рух «у загальному напрямку кліку».
- Space — хід за стрілкою-підказкою після Solve.
- Спільне Tatham: N — нова гра, U/Ctrl+Z — undo, R/Ctrl+R — redo, Restart, Solve, Specific/Random Seed.

## Вікна, меню, HUD
- `game-screen`: поле; статус-рядок — `remaining-counter` самоцвітів (замінюється на «COMPLETED!») і `death-counter`; `hint-marker` — стрілка на кульці після Solve.
- `settings-window` (Type → Custom…): Width, Height; пресети розмірів у меню Type.
- `custom-window` «Specific / Random Seed» — ID пазла; save/load у файл.
- `help-window`, `about-window`; окремого `end-screen` нема (флеш + статус).
- Переходи: Game → New → game-screen; Solve → стрілки на game-screen (без зміни стану — на відміну від інших пазлів Tatham (?)).

## Фічі поза полем
- `undo` ∞ / `redo` через усю сесію, зокрема **undo після смерті** з лічильником смертей (`+undo-after-death`).
- `show-solution` у вигляді покрокової стрілки, що перераховується після відхилення від маршруту.
- `seed-display` / `seed-input` / `share-code` — game ID; `custom-difficulty` — розмір поля.
- Генерація з гарантією досяжності кожного самоцвіту (`property-tests`: «генератор завжди видає розвʼязне»).

## Варіації й родичі
- [Pokémon-лід і кімнати-пазли RPG](rpg-dungeon-puzzle-rooms.md) — аватар ковзає до стіни в 4 напрямках, мета — вийти до виходу; тріснутий лід і валуни як доповнення.
- [Tomb of the Mask](tomb-of-the-mask.md) — те саме ковзання до упору, але real-time з шипами, ворогами й приливом знизу.
- [Ricochet Robots](ricochet-robots.md), [Atomix](atomix.md) — ковзають фігури, а не аватар; зупиняють стіни й інші фігури.
- [Klotski + Lunar Lockout](klotski.md) — Lunar Lockout: зупиняє **лише** інша фігура, стін нема.
- [Pengo](pengo.md) — ковзає штовхнутий блок, а не гравець.
- [Chip's Challenge](../maze-arcade/chips-challenge.md) — лід з кутами-поворотами як один із типів підлоги.
- Осі варіацій:
  - **що зупиняє**: стіна · стіна + сутність · спецклітина-стоп · нічого, крім сутностей (Lunar Lockout) — `+axis:stop-rule`;
  - **напрямки**: 4 / 8 (Inertia) / з поворотом на кутах (Chip's);
  - **ціль**: вихід (Pokémon) · зібрати всі (Inertia) · цільова клітина для фігури (Ricochet) · вижити (ToTM);
  - **небезпека**: нема · міни (Inertia) · вороги й шипи (ToTM);
  - **час**: покроково · real-time.

## Цікавинки для курсу
- Ковзання до упору з перевіркою стіни/стопу/міни на кожній клітині — 🌱.
- Діагональний рух і правило проходу крізь кутову щілину — 📎.
- Undo після смерті з лічильником смертей (смерть як подія в історії, а не кінець гри) — 📎.
- Граф точок зупинки + BFS «найкоротший шлях до виходу» (Pokémon-лід) — 🥉.
- Генератор Inertia: самоцвіти лише на клітинах, що лежать на петлі зі старту, + відкидання сіток з далекими кандидатами — 🥈.
- Солвер «зібрати все» як наближений TSP на графі зупинок (жадібна вставка + чистка) — 🥇; підказка-стрілка, що перераховується після відхилення — 🥉.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання; `move-8dir` (Inertia) / `move-4dir` (Pokémon) ↔ напрямки; `keyboard-controls` + `cell-click` ↔ ввід; `impassable-cells` ↔ стіни; `item-pickup` + `collect-all` + `goal-counter` ↔ самоцвіти; `touch-death` ↔ міни; `reach-exit` ↔ варіант Pokémon; `reachability-check` + `level-solver` + `unsolvable-states` ↔ генератор і Solve («стрілки лише якщо ще розвʼязно»); `game-settings` + `field-size-picker` ↔ Custom; `completion-detection` ↔ «COMPLETED!»; `property-tests` ↔ гарантія розвʼязності; `save-game` ↔ save/load.
- **Нема** → пропозиції карток:
  - `+stop-cell` «Клітина-гальмо» · entities/interact · 🌱 — зупиняє ковзання з будь-якого напрямку.
  - `+diagonal-gap-pass` «Діагональний прохід між кутами стін» · entities/legality · 📎.
  - `+loop-gem-generation` «Цілі лише на досяжних петлях зі старту» · levels/generation · 🥈 — гарантія розвʼязності без повного солвера.
  - `+stop-graph` «Граф точок зупинки» · levels/solvability · 🥉 — основа солвера будь-якої льодової гри.
  - Повтор корпусу: `+undo-redo`, `+undo-after-death`, `+solve-into-undo`, `+seed-share`, `+state-string`, `+hint-move` (стрілка), `+stop-on-entity` (родичі).

## Пропозиції до словників
- `+trigger:input`, `+trigger:enter` (стоп, міна, самоцвіт на льоту), `+trigger:blocked`, `+trigger:all_gone` (самоцвіти).
- `+cond:cell` — тип наступної клітини (стіна / стоп / міна).
- `+effect:slide`, `+effect:counter` (самоцвіти, смерті), `+effect:message` («COMPLETED!»).
- `+role:terrain` (стоп, лід), `+role:hazard` (міна).
- `+ui:remaining-counter`, `+ui:death-counter` — смерті як метрика поряд з undo, `+ui:hint-marker` (стрілка на кульці).
- `+window:hints-window` — тут вбудовано в game-screen; `+feature:undo`, `+feature:show-solution`, `+feature:seed-input`.
- `+axis:stop-rule` — що зупиняє ковзання (спільна вісь з klotski.md).

## Джерела
- ⭐ [Tatham: Inertia (довідка)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/inertia.html) — повні правила, 8 напрямків, діагональна щілина, стопи, міни після останнього самоцвіту, Solve зі стрілкою, undo після смерті з лічильником.
- [Inertia у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html).
- [Код inertia.c (дзеркало ghewgill/puzzles)](https://raw.githubusercontent.com/ghewgill/puzzles/master/inertia.c) — генератор (частки 1/5, POSSGEM на петлях, BFS-відсів), солвер як TSP-вставка, статус-рядок.
- [Tatham: спільні дії](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — undo/redo на всю сесію, Solve як крок історії, game ID.
- [Simon Tatham's Portable Puzzle Collection](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/) — «Collect all the gems without running into any of the mines».
- YouTube: пошуки «ice sliding puzzle game», «Simon Tatham Inertia puzzle».

## Непевне
- (?) Рік появи Inertia в колекції (2005) — з памʼяті; пошук вичерпано.
- (?) Чи старт поводиться як стоп і чи хід «у стіну впритул» зараховується.
- (?) Чи Solve в Inertia лише показує стрілки, не змінюючи стану (за довідкою — так), на відміну від `+solve-into-undo` інших пазлів Tatham.
- (?) Пресети розмірів (10×8, 15×12, 20×16) — з памʼяті.
