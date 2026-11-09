---
title: Zoo Keeper
slug: zoo-keeper
aka: [Zooo, Zoo Puzzle, Zookeeper DX Touch Edition, ZooKeeper]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2003
platforms: [web, GBA, PS2, Nintendo DS, arcade, iOS, Android, 3DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zoo_Keeper_(2003_video_game)", best: true, note: "правила: свап із поверненням, квоти по тваринах, ходи під час каскаду, бінокль, Special Panel, режими Tokoton/Quest/Time Attack"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=zoo+keeper+ds+gameplay", note: "пошук; геймплей DS"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Zoo+Keeper", note: "пошук Steam; ПК-версій може не бути"}
stage: v1
coverage: 70
mechanics: [cell-click, drag-drop-piece, gravity-fall, spawn-random-cell, line-match-clear, chain-reaction, collect-quota, goal-counter, time-out, progress-acceleration, no-moves-left, event-points, combo-multiplier, score-records, mode-select, difficulty-levels, hot-seat, online-multiplayer, end-screen, +match-3-swap, +cascade-refill, +active-chaining, +per-type-quota, +shuffle-keeps-clock, +hint-move, +color-cycling-wildcard, +curator-challenges]
proposes: ["+effect:reshuffle", "+effect:revert_swap", "+effect:clear_color", "+cond:cycling(tile)", "+ui:quota-strip", "+ui:favorite-animal", "+feature:mode-tokoton", "+feature:curator-quests"]
author: opus
date: 2026-11-09
---

# Zoo Keeper — match-3 з квотами по кожній тварині й таймером, де можна свапати, поки падає каскад

## Суть
Поле заповнене плитками-тваринами; гравець міняє місцями дві сусідні, і лінія з 3+ однакових «ловиться». Ціль рівня — не очки, а **квота кожного виду**: під кожною іконкою тварини лічильник, і рівень закінчується, коли виконано всі. Час іде постійно, з рівнем квота росте, а час на неї — меншає. Особливість, якої нема в Bejeweled: можна робити наступний свап, поки попередній ще осідає — гра тримає кілька каскадів одночасно.

## Поле і час
- Квадратна сітка плиток-тварин, повна завжди (зникле поповнюється згори).
- Real-time: таймер рівня тече безперервно, навіть під час перемішування дошки.
- Каскади не блокують ввід: свап можна зробити посеред падіння, і нові лінії з'являються в різних частинах поля паралельно.
- DS: нижній екран — поле (дотик), верхній — улюблена тварина та інформація.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-тварина | tile | вид | свапається з сусідом; 3+ в ряд/стовпець → зникає й зараховується в квоту виду |
| Квота виду | zone | вид, ціль, зібрано | лічильник під іконкою; виконано всі → рівень закінчено |
| Таймер рівня | — | час | спадає; нуль до виконання квот → кінець гри |
| Бінокль | pickup | к-сть | показує хід, якого гравець не знайшов |
| Special Panel | tile | вид змінюється по колу | дотик зупиняє на одній тварині й знімає з поля всі плитки цього виду |
| Улюблена тварина (DS) | — | вид | ловля цього виду дає додаткові очки |
| Куратор (Quest) | neutral | завдання | ставить челендж стадії: «зловити 20 левів», «30 ланцюгів», «заповнити таймер» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap(a, b))` → ЯКЩО `adjacent(a, b)` → ТО `swap(a, b)`.
- КОЛИ `after(swap)` → ЯКЩО `not pattern(line(3+))` → ТО `custom: «revert_swap — плитки вертаються на місця»`.
- КОЛИ `pattern(match(animal, 3+))` → ТО `clear(line)`, `counter(quota[animal], +n)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `fall(tiles_above)`, `spawn_at(random_animal, top)`.
- КОЛИ `settled` → ЯКЩО `pattern(line(3+))` → ТО `clear`, `combo(+1)` — ланцюг.
- КОЛИ `input(swap)` → ЯКЩО `custom: «попередній каскад ще триває»` → ТО `swap(a, b)` — ввід не блокується (паралельні каскади).
- КОЛИ `custom: «на полі нема жодного ходу»` → ТО `custom: «reshuffle — поле скидається»`; таймер не зупиняється.
- КОЛИ `input(binoculars)` → ЯКЩО `has(player, binoculars)` → ТО `custom: «підсвітити доступний хід»`, `take(player, binoculars)`.
- КОЛИ `input(special_panel)` → ТО `custom: «зупинити цикл на поточній тварині»`, `custom: «clear_color — прибрати всі плитки цього виду»`.
- КОЛИ `pattern(line(3, special_panel))` → ТО `score(1000000)`, `message(«Revolution»)`.
- КОЛИ `counter(quota[all], >=, target)` → ТО `next_level`, `custom: «квота росте, час на неї меншає»`.
- КОЛИ `timer(<=, 0)` → ЯКЩО `not custom: «усі квоти виконано»` → ТО `game_over`.
- КОЛИ `pattern(match(favorite, 3+))` → ЯКЩО `mode(ds)` → ТО `score(+bonus)`.
- Tokoton: КОЛИ `counter(quota[animal], >=, 100)` → ТО `custom: «поле очищається, очки за плитку ростуть; скидається лише лічильник цього виду»`, `counter(level, +1)`.
- Quest: КОЛИ `custom: «челендж куратора виконано»` → ТО `next_level` (10 стадій); нагорода — випадкова.
- Time Attack: КОЛИ `timer(<=, 0)` (6 хв) → ТО `game_over`, рахунок — очки; квоти нижчі.
- Перемога: нескінченно (до вичерпання часу) у Zoo Keeper/Tokoton; 10 стадій у Quest. Поразка: таймер = 0. Рахунок: очки з бонусами за ланцюги.

## Керування і ввід
- GBA/PS2: курсор хрестовиною + кнопка вибору двох плиток.
- DS/мобільні: дотик або протягування стилусом/пальцем від плитки до сусіда.
- Кнопка/іконка бінокля — одноразова підказка.
- Мультиплеєр: два гравці на одному екрані (не-DS версії), бій двох DS по бездротовому зв'язку.

## Вікна, меню, HUD
- `main-menu`: Zoo Keeper · Tokoton · Quest · Time Attack · (Super Hard — після розблокування) · Versus · Options · Records.
- `mode-select`, `difficulty-select` (easy/medium/hard — більше очок за плитку на важчих).
- `game-screen`: поле; `custom: «quota-strip»` — ряд іконок тварин з лічильником під кожною; `timer-countdown` смугою; `score`, `level-number`, лічильник біноклів; `popup-text` за ланцюги.
- DS верхній екран: `custom: «favorite-animal»` + статистика.
- `end-screen` (Game Over з очками) → `leaderboard` (high-score таблиця кожного режиму).
- Quest: `dialogue-window` куратора з челенджем стадії.

## Фічі поза полем
- `mode-classic` (Zoo Keeper), `mode-time-attack` (6 хв), `custom: «mode-tokoton»`, `custom: «curator-quests»` (10 стадій з челенджами), `mode-versus`.
- `unlockables`: Super Hard Mode — після першого місця в таблиці рекордів кожного іншого режиму.
- `difficulty-presets` (easy/medium/hard), `leaderboard-local` по режимах.
- `hint` — бінокль як ресурс, а не необмежена кнопка.

## Варіації й родичі
- Родичі в корпусі: [bejeweled](bejeweled.md) (той самий свап, але без квот і з блокуванням вводу на каскаді), [candy-crush](candy-crush.md) (цілі «зібрати N штук» на рівні — нащадок квот), [puzzle-quest](puzzle-quest.md), [panel-de-pon](panel-de-pon.md) (ходи під час падіння теж дозволені), [shariki](shariki.md).
- Версії: браузерна (2003) → GBA → PS2 → DS (дотик, улюблена тварина, бій двох DS) → iOS/Android «Zookeeper DX Touch Edition» → 3DS; Zookeeper Battle (мобільна PvP) (?).
- **Осі варіацій**: мета рівня (очки / квота кожного виду / одного виду) · ввід під час каскаду (блок / паралельно) · підказка (кнопка / ресурс-бінокль) · час (тече завжди / зупиняється на перемішуванні) · спецплитка (вибух / цикл кольору → очистити вид).

## Цікавинки для курсу
- Квота по кожному виду з лічильниками й прогресією «квота ↑, час ↓» — 🌱.
- Паралельні каскади: ввід не блокується, кілька незалежних осідань одночасно — 🥈 (анімації як черга подій по стовпцях).
- Відкат свапу без збігу з анімацією «туди-назад» — 🌱.
- Детекція «нема ходів» + перемішування під тикаючим таймером — 📎.
- Special Panel: плитка циклить вид, дотик фіксує й чистить усі цього виду — 📎.
- Квест-челенджі з випадковою ціллю (лічильник довільної події) — 📎.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` (DS) · `gravity-fall` · `spawn-random-cell` · `line-match-clear` · `chain-reaction` · `collect-quota` · `goal-counter` (лічильники під тваринами) · `time-out` · `progress-acceleration` · `no-moves-left` (тут — не програш, а перемішування) · `event-points` · `combo-multiplier` · `score-records` · `mode-select` · `difficulty-levels` · `hot-seat` (два гравці на одному екрані; найближча) · `online-multiplayer` (бездротова DS; найближча) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` (спільна з Bejeweled) · entities/interact · 📎.
  - `+cascade-refill` (спільна з Bejeweled/PQ) · entities/spawn · 📎.
  - `+active-chaining` «Ввід під час каскаду» · entities/legality · 🥈 (спільна з PPT Fusion).
  - `+per-type-quota` «Квота окремо для кожного типу плитки» · game-logic/win · 🌱 · слоти {start, step}.
  - `+shuffle-keeps-clock` «Перемішування не зупиняє таймер» · game-logic/legality · 🌱.
  - `+hint-move` (спільна з Bejeweled; тут — витратний ресурс) · interface/hud · 📎.
  - `+color-cycling-wildcard` «Плитка циклить вид, дотик фіксує» · entities/interact · 📎.
  - `+curator-challenges` «Стадія з випадковим челенджем-лічильником» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:reshuffle` — перемішати/скинути поле (повтор із Bejeweled, PQ).
- `+effect:revert_swap` — повернути свап без збігу (повтор із Bejeweled).
- `+effect:clear_color` — прибрати всі плитки виду (повтор із Bejeweled).
- `+cond:cycling(tile)` — плитка в стані циклу значень (Special Panel).
- `+ui:quota-strip` — ряд іконок типів із лічильниками квот.
- `+ui:favorite-animal` — «улюблений» тип з бонусом очок.
- `+feature:mode-tokoton` — режим «квота одного виду, решта не скидається».
- `+feature:curator-quests` — стадії з челенджами від NPC.

## Джерела
- ⭐ [Wikipedia: Zoo Keeper (2003 video game)](https://en.wikipedia.org/wiki/Zoo_Keeper_(2003_video_game)) — свап з поверненням, ланцюги, ходи під час каскаду, перемішування з таймером, квоти (старт 3, ростуть), бінокль, Special Panel, Revolution (1 000 000), режими Tokoton (100), Quest (10 стадій), Time Attack (6 хв), Super Hard, DS-фічі, релізи й назви.
- YouTube: пошук «zoo keeper ds gameplay».

## Непевне
- (?) Розмір поля (8×8?) і кількість видів тварин (8?) — Wikipedia не дає.
- (?) Чи таймер поповнюється за ловлю (смуга-шкала) чи лише спадає; скільки біноклів видають і за що.
- (?) Пункти головного меню й кнопки GBA/PS2 — з пам'яті.
- (?) Zookeeper Battle — окрема мобільна гра, не перевірено.
- (?) Чи рахуються в квоту тварини, зловлені в ланцюгу/від Special Panel (логічно — так).
