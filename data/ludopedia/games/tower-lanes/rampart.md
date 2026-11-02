---
title: Rampart
slug: rampart
family: tower-lanes
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 1990
platforms: [arcade, NES, SNES, Genesis, Master System, Game Boy, Lynx, MS-DOS, Amiga, C64, PS3]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rampart_(video_game)", best: true, note: "цикл фаз, замикання територій, гармати за замки, поразка без замку"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/rampart", note: "KLOV: 3 гравці, трекбол, режими річки/гавані, типи кораблів"}
  - {kind: fandom, url: "https://strategywiki.org/wiki/Rampart", note: "StrategyWiki (з черги; при перевірці 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rampart+arcade+1990+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [enemy-waves, projectile-shot, hp-damage, round-currency, time-out, event-points, difficulty-levels, sequential-levels, hot-seat, cell-click, hover-highlight, +enclosure-territory, +polyomino-placement, +phase-cycle, +leading-shot, +tower-placement]
proposes: ["+trigger:phase_start", "+trigger:phase_end", "+cond:enclosed", "+effect:fill", "+effect:rotate", "+effect:set_cell", "+role:castle", "+ui:phase-timer", "+ui:ghost-piece", "+window:castle-select", "+feature:local-versus", "+axis:opponent"]
author: opus
date: 2026-11-02
---

# Rampart — замкни замок стіною з тетроміно, постав гармати, відстріляйся від флоту

## Суть
Три фази по колу: **будівництво** (фігури-поліоміно латають стіну, щоб замкнути хоча б один замок), **розстановка гармат** на замкненій території, **бій** у реальному часі — гармати стріляють по кораблях, кораблі руйнують стіни. Територія — це все, що оточене суцільною стіною; незамкнене втрачається разом із гарматами. Якщо після будівництва жоден замок не замкнений — гра закінчена. Гібрид Tetris і tower defense, з режимом на 2–3 гравців.

## Поле і час
- Квадратна сітка: суходіл з кількома замками (castle), берег і море (одиночна гра) або річки, що ділять поле між гравцями (2 гравці — річка/гавань, 3 — Y-подібна річка).
- Клітина: вода / земля / стіна / замок / гармата (2×2) / уламки-вирви від влучань (?).
- Фази з таймером: будівництво — обмежений час (лічильник секунд), розстановка — до вичерпання гармат або часу, бій — до N потоплених кораблів (1 гравець) або фіксований час (2 гравці).
- Камера статична, видно все поле; снаряди летять відчутний час (треба цілитися з упередженням).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Замок (castle) | static | домашній / звичайний | замкнений → входить у територію, дає гармати |
| Стіна | static | 1 клітина | частина огорожі; влучання руйнує сегмент |
| Фігура стіни | object | форма поліоміно, поворот | кладеться на вільну землю; дозволені нестандартні форми (?) |
| Гармата | tower | 2×2 (?) | ставиться на замкнену територію; стріляє в точку прицілу |
| Ядро гравця | projectile | час польоту | летить по дузі в точку; влучило в корабель — шкода |
| Корабель малий | enemy | 1 влучання | підходить і стріляє по стінах |
| Корабель великий (галеон) | enemy | кілька влучань | міцніший, різні кольори/розміри |
| Десантний корабель | enemy | — | висаджує піхоту на берег (?) |
| Піхотинці (grunts / peons) | enemy | — | ходять до замків, не стріляють по діагоналі; заважають будувати (?) |
| Вирва / уламки (crater) | hazard | кілька раундів (?) | клітина недоступна для будівництва |
| Бонусна клітина | pickup | — | замкнена — очки |
| Ворожий замок (versus) | static | — | ціль пострілів суперника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «вибір домашнього замку; компʼютер обносить його стіною»`.
- КОЛИ `custom: «phase_start(cannons)»` → ТО `give(player, cannons = 1 за кожен замкнений замок + 2 за домашній, якщо є місце)`.
- КОЛИ `input(place, cannon, cell)` → ЯКЩО `custom: «cond enclosed(cell)»` and `free(cells_2x2)` → ТО `spawn(cannon)`; інакше `block`.
- КОЛИ `input(fire, target_cell)` → ЯКЩО `custom: «гармата перезаряджена»` → ТО `spawn(projectile)` з польотом до точки.
- КОЛИ `contact(projectile, ship)` → ТО `damage(1)`; `hp_zero(ship)` → `disappear_a`, `score(+n)`, `counter(sunk, +1)`.
- КОЛИ `contact(ship_shot, wall)` → ТО `set_cell(cell, crater|rubble)` (?) — у стіні діра.
- КОЛИ `counter(sunk, >=, quota)` або `timer(battle_end)` → ТО `custom: «phase_end(battle)»` → фаза будівництва.
- КОЛИ `custom: «phase_start(repair)»` → ТО `timer(start, t)`; кожна наступна фігура — випадкова форма.
- КОЛИ `input(rotate)` → ТО `rotate(piece, 90)`; КОЛИ `input(place)` → ЯКЩО `free(cells_of_piece)` (не вода, не стіна, не гармата, не вирва) → ТО `custom: «клітини фігури стають стіною»`; інакше `block`.
- КОЛИ `custom: «phase_end(repair)»` → ТО `custom: «flood fill від краю/моря: усе, що не досяжне без перетину стіни, — територія»` (`pattern(region_closed)`).
- КОЛИ `custom: «castle не в території»` → ТО `custom: «castle втрачено»`; гармати поза територією `disappear`.
- КОЛИ `count(enclosed_castles, ==, 0)` після будівництва → ТО `lose` (одиночна) / поразка гравця (versus).
- КОЛИ `custom: «grunt у замкненій території»` → ТО `disappear_a`, `score(+n)` (?).
- КОЛИ `custom: «бонусна клітина замкнена»` → ТО `score(+n)`.
- Versus: снаряди летять у стіни суперника; хто втратив усі замки — програв; якщо обидва вижили — вищий рахунок.
- Перемога: пройти 6 рівнів (аркада, 1 гравець) · Поразка: жодного замкненого замку після ремонту · Рахунок: кораблі, бонусні клітини, розчищення поля від піхоти й вирв.

## Керування і ввід
- Аркада: оптичний трекбол + 2 кнопки (fire / rotate); один курсор служить і прицілом, і «рукою» з фігурою.
- Консолі: хрестовина рухає курсор; A — поставити/вогонь, B — поворот.
- Фаза визначає зміст вводу: будівництво — курсор несе фігуру (тінь показує, де ляже); гармати — курсор ставить гармату; бій — курсор = приціл, кнопка — постріл найближчої готової гармати (?).

## Вікна, меню, HUD
- `splash-screen` / attract mode аркади.
- `+window:castle-select` — вибір домашнього замку на старті (і після втрати, якщо є континью (?)).
- `game-screen`: поле, курсор, `+ui:phase-timer` (секунди фази), `score`, лічильник гармат до розстановки, `+ui:ghost-piece` (фігура під курсором), підпис фази «BUILD / PLACE CANNONS / FIRE» (`objective-text`).
- `end-screen` — підсумок раунду: замки, кораблі, бонуси; фінал гри/поразка; у versus — сцена страти командира переможеним (Wikipedia).
- Консольні версії: `main-menu` → кількість гравців, `difficulty-select`, тренувальні рівні (Famicom: 7 training).
- Переходи: splash → castle-select → [cannons → battle → repair]×N → end-screen.

## Фічі поза полем
- `local-multiplayer` до 3 одночасно (аркада), 2 гравці на консолях; `online-multiplayer` у PS3-версії (2007).
- `difficulty-presets` (Famicom: 3 рівні складності), `mode-practice` (тренувальні рівні).
- `levels-sequential`: 6 рівнів одиночної гри.
- `continue` (аркада, кредити) (?).

## Варіації й родичі
- Порти відрізняються картами, кількістю рівнів і правилами для піхоти (NES/SNES/DOS — Bitmasters, Famicom — Konami).
- Родичі: Tetris (фігури), Xonix/Qix (територія = замкнена область), Go (оточення), Castles; сучасні — Emberward (тетроміно як лабіринт), Isle of Arrows (плитки-шляхи).
- **Осі варіацій**: фігура — фіксований набір тетроміно / довільні поліоміно · територія — замкнена стіною / за впливом · фази — по черзі з таймерами / одночасно · суперник — флот AI / інший гравець.

## Цікавинки для курсу
- Перевірка замкненості: flood fill від моря/краю, усе недосяжне — територія; втрата незамкнених замків і гармат — 🥇 (класичний алгоритм як ядро правил).
- Розміщення поліоміно з поворотом на зайнятій сітці (легальність + тінь) — 🥉.
- Цикл фаз зі своїм вводом і таймером: машина станів гри — 🥉.
- Постріл з часом польоту і приціл з упередженням — 🥉 (снаряд летить у точку, а не в ціль).
- Ресурс = кількість замкнених замків: економіка, що виростає з геометрії — 📎.
- Versus на одному полі з річкою: два гравці одночасно з одним вводом кожен — 🥈.

## Мапа на каталог
- Є: `enemy-waves` ↔ флот раунду · `projectile-shot` + `hp-damage` (галеони на кілька влучань) · `round-currency` ↔ гармати за замки · `time-out` ↔ таймер фази · `event-points` · `difficulty-levels` · `sequential-levels` · `hot-seat` (≈ спільний екран, але одночасно) · `cell-click` + `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+enclosure-territory` «Територія = замкнений стіною регіон» · game-logic/win · 🥇 — flood fill, втрата незамкненого.
  - `+polyomino-placement` «Розміщення фігури-поліоміно з поворотом» · entities/legality · 🥉 · слоти {shapes, rotate}.
  - `+phase-cycle` «Цикл фаз гри» · game-logic/waves · 🥉 · слот {phases: list, timer}.
  - `+leading-shot` «Снаряд у точку з часом польоту» · entities/combat · 🥉.
  - `+tower-placement` — див. fieldrunners; тут лише на своїй території.

## Пропозиції до словників
- `+trigger:phase_start` (з TFT), `+trigger:phase_end` — початок/кінець фази циклу.
- `+cond:enclosed` — клітина всередині замкненого стіною регіону.
- `+effect:fill` ⏳, `+effect:rotate` ⏳, `+effect:set_cell` — підтвердження (стіна з фігури, вирва).
- `+role:castle` — ключова будівля: дає ресурс, поки «замкнена»; втрата всіх = поразка.
- `+ui:phase-timer` — таймер поточної фази; `+ui:ghost-piece` — уже ⏳.
- `+window:castle-select` — вибір стартової позиції на мапі.
- `+feature:local-versus` — одночасна гра 2–3 гравців на одному екрані (не hot-seat).
- `+axis:opponent` — значення `versus-local` (одночасно, не по черзі).

## Джерела
- ⭐ [Wikipedia: Rampart](https://en.wikipedia.org/wiki/Rampart_(video_game)) — фази, гармати (1 за замок, 2 за домашній), фігури для ремонту, поразка без замкненого замку, рахунок, порти.
- [KLOV / Arcade Museum](https://www.arcade-museum.com/Videogame/rampart) — до 3 гравців, трекбол, режими річки й гавані, типи кораблів, «peons».
- [StrategyWiki: Rampart](https://strategywiki.org/wiki/Rampart) — з черги пошукового агента; при перевірці 403.
- YouTube: пошук «rampart arcade 1990 gameplay».

## Непевне
- (?) Розмір гармати (2×2) і поля; чи є «великі гармати» в окремих портах.
- (?) Поведінка піхоти: як саме висаджується, що робить із замком, чи гине в замкненій території.
- (?) Скільки раундів тримаються вирви й чи блокують вони будівництво.
- (?) Тривалість фаз у секундах; чи вибирається новий домашній замок після втрати.
- (?) Набір фігур: лише тетроміно чи й нестандартні поліоміно (джерела кажуть «Tetris-like»).
