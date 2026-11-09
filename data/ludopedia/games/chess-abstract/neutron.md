---
title: Neutron (Нейтрон)
slug: neutron
aka: [Нейтрон]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 1978
platforms: [board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Neutron_(game)", best: true, note: "правила: 5×5, по 5 фішок, нейтрон у центрі, хід = нейтрон + своя фішка, ковзання до упору, три способи перемоги"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Neutron", note: "Ludii: формалізовані правила, виняток першого ходу, «не може завершити хід — програв»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Neutron+board+game+Kraus+gameplay", note: "пошук; партії"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, move-8dir, inertia-slide, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, level-solver, cell-click, drag-drop-piece, legal-move-highlight, selection-highlight, last-move-highlight, mode-indicator, game-screen, main-menu, end-screen, help-window, settings-window, field-size-picker, undo-step, state-as-data, +shared-neutral-piece, +two-phase-turn, +first-turn-exception]
proposes: ["+role:shared-piece", "+card:shared-neutral-piece", "+card:two-phase-turn", "+card:first-turn-exception"]
author: opus
date: 2026-11-09
---

# Neutron — кожен хід спершу штовхаєш спільний «нейтрон», потім свою фішку; усе ковзає до упору

## Суть
Двоє гравців, по 5 фішок на своєму домашньому ряду, у центрі — одна нічия фішка, нейтрон. Хід складається з двох фаз: спершу пересунути нейтрон, потім одну свою фішку; усе рухається лише по прямій (8 напрямків) і **обовʼязково до упору**. Мета — щоб нейтрон опинився на твоєму домашньому ряду, хоч би хто його туди привів, або щоб суперник не мав куди рушити нейтрон. Ядро — примусовий хід спільною фігурою: іноді будь-який рух нейтрона веде його до суперника (зугцванг).

## Поле і час
- Дошка 5×5, один шар, на клітині ≤1 фішка. Взяття нема — кількість фішок незмінна всю гру.
- Домашній ряд кожного — його край дошки (перший ряд білих, протилежний — чорних); він же ціль для нейтрона.
- Покроково, двоє, повна інформація. Хід = 2 фази: `neutron` → `soldier`; виняток — найперший хід партії лише з фазою `soldier`.
- Рух фігури = ковзання по одному з 8 напрямків через порожні клітини до краю або до першої фішки (як ферзь, але без права зупинитись раніше).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка гравця (soldier) | piece | сторона; ×5 у кожного | ковзає до упору в одному з 8 напрямків; не бʼє |
| Нейтрон | piece | без власника; ×1; старт — центр | рухається так само; його рухають обидва гравці, кожен у свою першу фазу ходу |
| Домашній ряд | zone | край дошки, по одному на сторону | нейтрон тут → перемога власника ряду |
| Порожня клітина | static | — | через неї можна ковзати |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «5 фішок кожного на домашньому ряду, нейтрон у центрі»`.
- КОЛИ `turn_start(side)` → ЯКЩО `first_time` (перший хід партії) → ТО `custom: «фаза нейтрона пропускається»` — лише `phase_start(soldier)`.
- КОЛИ `phase_start(neutron)` → ЯКЩО `turn_of(side)` → ТО гравець обирає напрям: `input(dir, neutron)`.
- КОЛИ `input(dir, piece)` → ЯКЩО `free(next_in_dir)` → ТО `slide(piece, dir)` — до краю або до першої фішки; інакше `block` (у цей бік не можна).
- КОЛИ `input(stop, piece)` до упору → ТО `block`: `custom: «зупинитись раніше, ніж до упору, не можна»`.
- КОЛИ `contact(piece, any_piece)` під час ковзання → ТО `custom: «зупинка на клітині перед фішкою»`; взяття нема.
- КОЛИ `after(slide(neutron))` → ТО `phase_start(soldier)`: `input(dir, own_soldier)` → `slide(own_soldier, dir)` → `end_turn`.
- КОЛИ `reach(neutron, home_row(A))` → ТО `win` гравця A — незалежно від того, хто рушив нейтрон (довести нейтрон на ряд суперника = програти).
- КОЛИ `phase_start(neutron)` → ЯКЩО `no_moves(neutron)` → ТО `lose(side)` — той, хто мав його рушити (нейтрон затиснуто з усіх 8 боків).
- КОЛИ `phase_start(soldier)` → ЯКЩО `no_moves(side)` → ТО `lose(side)` — за Ludii «не може завершити хід».
- Перемога: нейтрон на своєму ряду (своїм або чужим ходом) · суперник не може рушити нейтрон · суперник не може завершити хід. Нічиєї в правилах нема. Рахунок: партія 1 / 0.

## Керування і ввід
- Настільна: фішки рухають руками; нейтрон зазвичай іншого кольору.
- (цифрова версія) Фаза нейтрона: нейтрон підсвічено, клік по ньому → до 8 клітин-кінцевих точок (`legal-move-highlight` лише в точках упору); клік по точці — ковзання. Фаза фішки — те саме для своїх.
- Ввід «звідки → куди», де «куди» однозначно визначене напрямком; drag-n-drop по прямій з підсвіткою точки упору.
- Індикатор фази (`mode-indicator`): «Хід нейтрона» / «Хід фішки».

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє за одним пристроєм · Правила · Налаштування.
- `settings-window` / `match-setup`: хто ходить першим, рівень AI, розмір поля для варіантів.
- `game-screen`: дошка 5×5 з підсвіченими домашніми рядами; `turn-indicator` + індикатор фази; `selection-highlight`; `legal-move-highlight` (точки упору); `last-move-highlight` (дві траєкторії останнього ходу); `undo-button` проти AI.
- `end-screen`: «нейтрон на ряду білих — білі перемогли» / «нейтрон затиснуто»; Реванш.
- `help-window`: дві фази ходу, ковзання до упору, автогол.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen.

## Фічі поза полем
- `ai-opponent-levels` (minimax на 5×5 — мале дерево); `hint` (показати, куди нейтрон іде «безпечно»).
- `undo` проти AI; `replay` партії; `custom-rules` — розмір дошки й варіанти (Zillions of Games містить Neutron і кілька варіантів).

## Варіації й родичі
- Wikipedia згадує 15 варіантів (інші розміри дошки тощо) без опису.
- Ковзання до упору: Ricochet Robots, Inertia (сімʼя `push-slide`); фігура-ферзь з повною довжиною — `amazons.md` (там можна зупинитись будь-де).
- Обмеження ходу через спільний обʼєкт: `kamisado.md` (колір клітини диктує, якою фігурою ходить суперник), Quoridor (`quoridor.md`) — перегони з перешкодами.
- Перегони до свого/чужого краю — `breakthrough-loa.md`.
- **Осі варіацій**: спільна фігура (нема / одна нейтральна / кілька) · довжина руху (1 крок / будь-яка / лише до упору) · хто виграє від нейтрона на ряду (власник ряду / той, хто рушив) · перший хід (повний / без нейтрона).

## Цікавинки для курсу
- Генератор ходів «ковзання до упору» у 8 напрямків — 🌱 (один цикл на напрям).
- Двофазний хід як скінченний автомат `neutron → soldier → end_turn` з винятком першого ходу — 📎.
- Перевірка перемоги після **кожної** фази, включно з автоголом, — 🌱.
- Minimax / alpha-beta з оцінкою «куди може дійти нейтрон» — 🥉.
- Повний розвʼязок 5×5 ретроградним аналізом (база позицій, хто виграє) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух як ферзь · `move-8dir` · `inertia-slide` ↔ лише до упору · `no-moves-left` ↔ затиснутий нейтрон · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax`, `level-solver` ↔ розвʼязання 5×5 · `cell-click`, `drag-drop-piece`, `legal-move-highlight`, `selection-highlight`, `last-move-highlight`, `mode-indicator` ↔ фаза ходу · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`, `field-size-picker` · `undo-step` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+shared-neutral-piece` «Спільна нейтральна фігура» · entities/legality · 🌱 — фігура без власника, яку рухають обидва; перемога залежить від того, де вона.
  - `+two-phase-turn` «Хід із кількох обовʼязкових фаз» · game-logic/opponent · 📎 · слоти {phases} — Neutron, Amazons (хід + стріла).
  - `+first-turn-exception` «Обмежений перший хід» · game-logic/opponent · 🌱 — компенсація переваги першого ходу (Neutron, Hex-swap, Konane-відкриття).

## Пропозиції до словників
- `+role:shared-piece` — фігура без сторони, яку рухають обидва гравці (нейтрон); не `neutral`, бо власної поведінки не має.
- `+card:shared-neutral-piece` · `+card:two-phase-turn` · `+card:first-turn-exception` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Neutron (game)](https://en.wikipedia.org/wiki/Neutron_(game)) — Robert A. Kraus, Games & Puzzles 1978; 5×5, 5+5 фішок, нейтрон у центрі; рух по прямій до упору, без взяття; хід = нейтрон, потім своя фішка; перший хід — лише фішка; три способи перемоги; Zillions of Games; 15 варіантів.
- [Ludii: Neutron](https://ludii.games/details.php?keyword=Neutron) — формалізація: перший гравець не рухає нейтрон у першому ході; перемога — нейтрон на своєму першому ряду або суперник не може завершити хід.
- YouTube: пошук «Neutron board game Kraus gameplay».

## Непевне
- (?) Хто ходить першим (білі/чорні) — джерела не кажуть.
- (?) Чи поразка «не можу рушити свою фішку після нейтрона» — офіційне правило; Wikipedia каже лише про затиснутий нейтрон, Ludii — ширше «не може завершити хід».
- (?) Твердження, що перший гравець виграє при ідеальній грі, — у Wikipedia з позначкою [citation needed].
- (?) Склад 15 варіантів і які з них у Zillions — не бачив.
