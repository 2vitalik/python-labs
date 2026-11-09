---
title: Poker Smash
slug: poker-smash
aka: []
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: score
year: 2008
platforms: [Xbox 360 (XBLA), iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Poker_Smash", best: true, note: "детальні правила: руки, керування, режими, мультиплеєр на фішках, сміття від дилера"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Attack", note: "прообраз: swap-стек, що росте знизу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=poker+smash+xbox+live+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [keyboard-controls, gravity-fall, chain-reaction, combo-multiplier, event-points, progress-acceleration, time-out, garbage-attack, simultaneous-versus, online-multiplayer, rating-system, leaderboard, score-records, game-pause, end-screen, mode-select, theme-select, satisfy-constraints, level-bank, +rising-stack, +manual-row-add, +swap-cursor, +poker-hand-match, +shape-bonus, +challenge-hand, +slow-time-meter, +bomb-single-clear, +chip-stack-hp, +rotating-dealer, +garbage-adjacent-clear, +unlock-shop]
proposes: ["+cond:poker_hand", "+effect:raise_stack", "+effect:convert_garbage", "+ui:chip-stacks", "+ui:challenge-hand", "+feature:unlock-bank", "+card:poker-hand-match", "+card:chip-stack-hp", "+card:rotating-dealer", "+card:challenge-hand"]
author: opus
date: 2026-11-09
---

# Poker Smash — стек Panel de Pon, де збіг — це покерна рука з карт 10…A

## Суть
Стек карт (10, J, Q, K, A різних мастей) у **п'яти стовпцях** невпинно піднімається знизу. Гравець курсором переставляє сусідні карти по горизонталі (як у Tetris Attack / Panel de Pon) і складає в ряд або стовпець 3+ карти, що утворюють **покерну комбінацію**: сет, каре, фул-хаус, стрит, флеш (до 9 карт), роял-флеш. Рука зникає, карти над нею падають — можливі ланцюги. Очки — «фішки»; у мультиплеєрі фішки — це життя, а кожна рука списує їх із суперників.

## Поле і час
- **5 стовпців**; висота поля в джерелі не названа (?). Нові карти входять ряд за рядом знизу, стек піднімається з поступовим прискоренням (Action).
- Real-time; гравець може прискорити підйом (лівий тригер) або **сповільнити час** (правий тригер) за рахунок енергії, що повільно відновлюється.
- Поразка в Action — стек досяг верху поля.
- Мультиплеєр: до 5 полів (локальний split-screen або Xbox Live).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | клітина + вибрана карта/порожнеча | ходить по полю; переносить вибране вліво/вправо, обмін із сусідом |
| Карта | tile | ранг (10, J, Q, K, A), масть | бере участь у руці в ряду/стовпці; падає в порожнечу |
| Порожня клітина | terrain | — | її теж можна «вибрати» й посунути (обмін із картою) |
| Бомба | pickup | запас обмежений, поповнюється з грою | ставиться на одну карту й прибирає її |
| Рядок сміття | hazard | ширина ряду | надходить від дилера; рука, що торкається, перетворює його на нові карти |
| Новий ряд знизу | spawner | темп росте | виштовхує стек угору |
| Верх поля | static | межа | стек тут → кінець гри (Action) |
| Банк фішок | resource | рахунок | соло — очки й валюта розблокувань; мультиплеєр — «HP» гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move_cursor)` → ТО `move(cursor, dir)`.
- КОЛИ `input(slide_left|slide_right)` → ТО `swap(selected, neighbour)` — карта ↔ карта або карта ↔ порожнеча.
- КОЛИ `after(swap)` → ЯКЩО `free(cell_below)` → ТО `fall(card)`.
- КОЛИ `pattern(line(3+))` → ЯКЩО `custom: «poker_hand — карти лінії утворюють сет / каре / фул-хаус / стрит / флеш / роял-флеш»` → ТО `clear(cells)`, `score(hand_value)` — простіша рука дає менше фішок, складніша — більше.
- КОЛИ `pattern(line)` → ЯКЩО `custom: «флеш — однакова масть, до 9 карт у лінії»` → ТО `clear(cells)`, `score(flush_value)`.
- КОЛИ кілька рук утворено одночасно → ТО `custom: «shape bonus — бонус за форму з кількох рук»`.
- КОЛИ `after(clear)` → ТО `fall(cards_above)`; КОЛИ нова рука складається з падаючих карт → ЯКЩО `chain(n)` → ТО `multiplier(×k)` — множник росте з ланцюгом.
- КОЛИ `input(bomb)` → ЯКЩО `has(player, bomb)` → ТО `clear(card)`, `take(player, bomb)`.
- КОЛИ `custom: «бомби поповнюються з перебігом гри»` → ТО `give(player, bomb)`.
- КОЛИ `tick` → ТО `custom: «raise_stack — стек угору, новий ряд знизу»`; швидкість росте (Action).
- КОЛИ `input(raise)` (лівий тригер) → ТО `custom: «raise_stack — швидкий підйом»`.
- КОЛИ `input(slow)` (правий тригер) → ЯКЩО `counter(energy, >, 0)` → ТО `speed(stack, ×k<1)`, `counter(energy, -n)`; без вводу `counter(energy, +n)` повільно.
- КОЛИ `custom: «Challenge Hand — гра називає руку»` → ЯКЩО рука складена `timer(<, limit)` → ТО `score(bonus)`; бонус росте з перебігом гри.
- КОЛИ `reach(stack, top)` → ЯКЩО `mode(action)` → ТО `game_over`.
- КОЛИ `timer(3 min)` вичерпано → ЯКЩО `mode(timed)` → ТО `game_over` (рахунок — фішки).
- КОЛИ `all_gone(card)` → ЯКЩО `mode(puzzle)` → ТО `win`; у Puzzle стек не росте, ходи й час не обмежені.
- Мультиплеєр: КОЛИ `pattern(hand)` → ТО `custom: «вартість руки порівну списується з фішок суперників і переходить гравцю»`.
- Мультиплеєр: КОЛИ `counter(chips, ≤, 0)` → ТО `lose` (вибув); останній із фішками — `win`.
- Мультиплеєр: КОЛИ `turn_start(dealer)` → ТО роль дилера переходить по черзі; ЯКЩО `chain(3|5|7…)` у дилера → ТО `send_garbage(row)` суперникам.
- КОЛИ `pattern(hand)` → ЯКЩО `adjacent(hand, garbage)` → ТО `custom: «convert_garbage — рядок сміття стає новими картами»`.
- Перемога: Puzzle — прибрати всі карти; мультиплеєр — забрати всі фішки · Поразка: стек дійшов верху / фішки скінчились · Рахунок: фішки за руки, shape bonus, множник ланцюга, challenge hands.

## Керування і ввід
- Ліва стіка / D-pad — курсор; права стіка ←/→ — перенести вибрану карту **або порожнечу** на сусідню клітину (обмін).
- Кнопка — поставити бомбу на карту під курсором.
- Лівий тригер — прискорити підйом; правий — сповільнити час (енергія).
- iOS-версія — дотик/перетягування (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Action · Timed · Puzzle · Practice · Multiplayer (локальний / Xbox Live: Ranked, Unranked).
- `game-screen`: поле 5 стовпців, курсор, `score` (фішки), множник/ланцюг `popup-text`, `+ui:energy-bar` уповільнення, запас бомб, `+ui:challenge-hand` (поточна вимога з таймером), `danger-line`.
- Мультиплеєр-екран: до 5 полів, `+ui:chip-stacks` (фішки кожного), позначка дилера.
- `puzzle-select` — пазли (+15 у DLC Puzzle Pack).
- `shop-window`/банк: фішки витрачаються на теми, картинки й розвʼязки пазлів.
- `leaderboard` (Xbox Live: найкращі очки, найдовші ланцюги, TrueSkill-ранг) · `end-screen`.
- Переходи: main-menu → mode-select → game-screen → end-screen → leaderboard / знову.

## Фічі поза полем
- Режими: `mode-classic` (Action), `mode-time-attack` (Timed, 3 хв), `mode-puzzle`, `mode-practice` (рахунок і статистика не зберігаються), `mode-versus`.
- `online-multiplayer` до 5 гравців: Ranked з Microsoft TrueSkill і Unranked; `local-multiplayer` split-screen.
- `unlockables`: банк фішок → теми, картинки, розвʼязки пазлів (`+feature:unlock-bank`).
- `theme-select`: 10 музичних тем (David Sease, Stretch Arm Strong), DLC Environment Pack (2 оточення Action).
- `leaderboard-online` · `stats`.

## Варіації й родичі
- Прообраз — Tetris Attack / [panel-de-pon](panel-de-pon.md) (Puzzle League): swap-курсор, стек знизу, ручний підйом, ланцюги, сміття, що перетворюється на нові плитки.
- Відмінність: збіг — **не однаковість**, а **комбінація** (ранги + масті), тож одна лінія може бути «рукою» за двома правилами.
- Родичі за ідеєю «збіг за правилом, а не кольором»: [puzzle-quest](puzzle-quest.md) (збіг → ресурс), [money-puzzle-exchanger](money-puzzle-exchanger.md) (збіг за таблицею).
- **Осі варіацій**: предикат збігу (той самий колір / числова послідовність / набір) · мультиплеєр-ресурс (сміття / спільні фішки-HP) · роль у ході (рівні гравці / дилер по черзі) · керування часом (лише прискорити / і сповільнити за енергію).

## Цікавинки для курсу
- Предикат «покерна рука» для лінії 3–9 карт (сет, каре, фул-хаус, стрит, флеш, роял) — 🥉: класифікатор комбінацій на сітці.
- Обмін з порожнечею — swap-курсор, що «везе» карту в дірку — 📎.
- Фішки як спільне HP: кожна рука порівну списує з усіх суперників — 📎.
- Дилер по черзі + сміття лише на непарних ланцюгах — 🥉 (стан матчу, черга ролей).
- Уповільнення часу за енергію, що відновлюється — 🌱.
- Challenge Hand: випадкова вимога з таймером і зростаючим бонусом — 📎.
- Бомба на одну карту з обмеженим запасом, що поповнюється — 🌱.

## Мапа на каталог
- Є: `keyboard-controls` · `gravity-fall` · `chain-reaction` · `combo-multiplier` · `event-points` · `progress-acceleration` · `time-out` (Timed) · `garbage-attack` · `simultaneous-versus` · `online-multiplayer` · `rating-system` (TrueSkill) · `leaderboard` · `score-records` · `game-pause` · `end-screen` · `mode-select` · `theme-select` · `satisfy-constraints` (Puzzle) · `level-bank` (пазли).
- **Нема** → пропозиції карток:
  - `+rising-stack` · `+manual-row-add` · `+swap-cursor` · `+garbage-adjacent-clear` — ⏳ підтверджую (Panel de Pon).
  - `+poker-hand-match` «Лінія карт зникає, якщо утворює покерну комбінацію» · entities/interact · 🥉 · слоти {hands: [set, quads, full, straight, flush, royal], min: 3}.
  - `+shape-bonus` «Бонус за кілька збігів одним ходом» · game-logic/score · 🌱.
  - `+challenge-hand` «Випадкова ціль-збіг на час» · game-logic/score · 📎.
  - `+slow-time-meter` «Сповільнення за енергію, що відновлюється» · game-logic/difficulty · 🌱.
  - `+bomb-single-clear` «Лімітована бомба на одну плитку» · entities/interact · 🌱.
  - `+chip-stack-hp` «Очки = життя; збіг списує їх із суперників» · game-logic/opponent · 📎.
  - `+rotating-dealer` «Роль дилера по черзі: лише він шле сміття» · game-logic/opponent · 🥉.
  - `+unlock-shop` «Банк очок → розблокування тем і розвʼязків» · game-logic/economy · 📎.

## Пропозиції до словників
- `+cond:poker_hand` — лінія карт утворює покерну комбінацію (Poker Smash; карткові match-гри).
- `+effect:raise_stack` · `+effect:convert_garbage` — ⏳ підтверджую (Panel de Pon).
- `+ui:chip-stacks` — фішки кожного гравця як HP у мультиплеєрі.
- `+ui:challenge-hand` — поточна вимога-ціль із таймером.
- `+feature:unlock-bank` — очки як валюта розблокувань (теми, картинки, розвʼязки).
- `+card:poker-hand-match` · `+card:chip-stack-hp` · `+card:rotating-dealer` · `+card:challenge-hand`.

## Джерела
- ⭐ [Wikipedia: Poker Smash](https://en.wikipedia.org/wiki/Poker_Smash) — 5 стовпців, руки, керування (бомби, тригери, енергія), очки, режими, мультиплеєр на фішках, дилер і сміття, DLC, TrueSkill.
- [Wikipedia: Tetris Attack](https://en.wikipedia.org/wiki/Tetris_Attack) — прообраз механіки.
- YouTube: пошук «poker smash xbox live arcade gameplay».

## Непевне
- (?) Висота поля й темп підйому — не названо.
- (?) Чи рахується **пара** / дві пари / стрит з 3–4 карт — у джерелі перелік лише: сет, каре, фул-хаус, стрит, флеш, роял-флеш; мінімум — 3 карти в лінії.
- (?) Чи стоять карти тільки 10–A (5 рангів) у всіх режимах — так у Вікіпедії.
- (?) Точні вартості рук у фішках і формула shape bonus.
- (?) Як часто поповнюються бомби; що буде з невдалим Challenge Hand.
- (?) Умова поразки в Puzzle (ходи й час не обмежені).
- (?) Керування в iOS-версії.
