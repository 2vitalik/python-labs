---
title: Megapanel (メガパネル)
slug: megapanel
aka: [メガパネル, Mega Panel]
family: falling-match
also: [push-slide]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [Mega Drive, Mega Drive Mini 2]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/メガパネル", best: true, note: "поле 11×6, 3+ по вертикалі/горизонталі, без ланцюгів, підйом знизу, режими Exercise/Pin-Up/Vs, предмети атаки й захисту"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Megapanel", note: "одна порожня клітина, плитки зсуваються в неї; 3 життя; бомби Pin-Up"}
  - {kind: other, url: "https://gaminghell.co.uk/Megapanel.html", note: "огляд: чорна клітина, керування D-pad/A/C, NEXT, цілі Exercise, зелені блоки Pin-Up, налаштування"}
  - {kind: other, url: "https://retroxp.beehiiv.com/p/it-s-new-to-me-megapanel", note: "огляд: лише одна дірка, нерівні стовпці, цілі раундів"}
  - {kind: other, url: "https://segadoes.com/?p=4709", note: "огляд: бомба падає під центр зчищеної трійки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=megapanel+mega+drive+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [line-match-clear, impassable-cells, progress-acceleration, sequential-levels, level-select, extra-life-threshold, player-death, event-points, garbage-attack, simultaneous-versus, objective-text, goal-counter, game-settings, theme-select, +slide-into-gap, +rising-stack, +manual-row-add, +picture-reveal, +multi-hit-block, +defense-item, +round-goals, +no-chain-bonus]
proposes: ["+effect:raise_stack", "+card:round-goals", "+card:defense-item", "+feature:navigator-mute"]
author: opus
date: 2026-11-09
---

# Megapanel — «пʼятнашки» в стеку, що росте знизу: одна чорна клітина, і три однакові в лінію зникають

## Суть
Поле 6×11 заповнене кольоровими панелями, серед них рівно **одна чорна (порожня) клітина**; D-pad зсуває сусідню панель у неї, тож рухається саме «дірка», як у «пʼятнашках». Мета — не впорядкувати панелі, а скласти 3+ одного кольору в рядок чи стовпець: вони зникають. Тим часом знизу періодично вʼїжджає новий ряд, і стек торкнувся верху — промах. Гравітації під час руху й вільного курсора нема, тож панель, до якої дірка не дістає, «застрягає» — у цьому вся головоломка.

## Поле і час
- Сітка 6 стовпців × 11 рядів + додатковий нижній ряд для панелей, що наступають (рядок NEXT).
- Одна чорна клітина завжди присутня; рух можливий лише між нею й сусідньою панеллю. Високий самотній стовпець можна зсувати лише вгору-вниз, убік — ні (поруч нема панелей).
- Real-time: ряди знизу підіймаються з фіксованим інтервалом; перед підйомом блимає напис NEXT. Швидкість росте з рівнем, а перед кінцем рівня темп нових рядів різко зростає.
- Pin-Up: праворуч друге поле — «яма» з блоками, що ховають картинку; ліве поле керує бомбами для правого.
- Versus: два поля поруч, одночасна гра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чорна клітина (дірка) | player | позиція | міняється місцями з сусідньою панеллю за напрямком D-pad; завжди одна |
| Панель | tile | колір (усі однієї квадратної форми) | зсувається лише в дірку; 3+ одного кольору в рядок/стовпець → зникає |
| Ряд NEXT | spawner | 6 панелей | підіймається знизу за таймером або за кнопкою A |
| Бомба (Pin-Up) | projectile | стовпець | падає в праве поле в стовпці центральної панелі зчищеної лінії; руйнує блок картинки |
| Блок картинки (Pin-Up) | tile | 1 удар | зникає від бомби, відкриваючи частину картинки |
| Зелений блок (Pin-Up) | tile | 2 удари | потрібна ще одна бомба |
| Предмет атаки (Vs) | tile | — | зʼявляється після кожних 20+ зчищених; зчищений у трійці → незнищенні блоки супернику |
| Предмет захисту (Vs) | tile | — | зчищений у трійці → прибирає всі незнищенні блоки зі свого поля |
| Незнищенний блок (Vs) | object | — | не збігається й не зникає від трійок; прибирає лише предмет захисту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `occupied(neighbour_of_gap(dir), panel)` → ТО `swap(gap, panel)` (панель переходить у дірку, дірка — на її місце); інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «за діркою в цьому напрямку край поля або порожнеча над стеком»` → ТО `block`.
- КОЛИ `pattern(line(3+, same_color))` → ЯКЩО `custom: «лише рядок або стовпець; діагональ не рахується»` → ТО `clear(cells)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `custom: «клітини зчищеної лінії прибираються зі стеку; як заповнюються — див. Непевне»`.
- КОЛИ `pattern(line(3+))` → ЯКЩО `chain(n)` → ТО `custom: «ланцюг не дає бонусу: концепції ланцюга нема»` (випадковий збіг лише ламає план).
- КОЛИ `timer(interval)` → ТО `message(NEXT)`, потім `custom: «raise_stack — стек на ряд угору, ряд NEXT стає активним»`, `spawn_at(next_row, bottom)`.
- КОЛИ `input(A)` → ТО `custom: «raise_stack — підняти ряди вручну»`.
- КОЛИ `level_start` → ТО `speed(rise, +)`; КОЛИ `custom: «рівень близький до завершення»` → ТО `speed(rise, ×k)`.
- КОЛИ `reach(stack, top)` → ЯКЩО `mode(exercise)` → ТО `game_over` (континʼю нема).
- КОЛИ `reach(stack, top)` → ЯКЩО `mode(pin_up)` → ТО `lives(-1)`, `restart`; КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Exercise: КОЛИ `all_constraints_met` (умова раунду справа на екрані: кількість збігів, збіги певного кольору по 4–5, ціль очок) → ТО `win`, `next_level`; 30 раундів.
- Pin-Up: КОЛИ `pattern(line(3))` → ТО `spawn_at(bomb, column_of_center_panel)` у правому полі.
- Pin-Up: КОЛИ `pattern(line(4+))` (одним зчищенням) → ТО `spawn_at(bomb, each_cleared_panel)` — по бомбі на панель; вертикальна лінія кидає кілька бомб в один стовпець, горизонтальна — по всьому ряду.
- Pin-Up: КОЛИ `contact(bomb, picture_block)` → ТО `damage(1)`; КОЛИ `hp_zero(picture_block)` → ТО `disappear`, `reveal(cell)` (зелений блок потребує двох бомб).
- Pin-Up: КОЛИ `all_gone(picture_block)` → ТО `win`, `next_level`; 30 раундів.
- Pin-Up: КОЛИ `counter(score, ≥, threshold)` → ТО `lives(+1)`.
- Versus: КОЛИ `counter(cleared, ≥, 20)` → ТО `spawn(item_panel)` (атака або захист).
- Versus: КОЛИ `pattern(line(3, includes attack_item))` → ТО `send_garbage(unbreakable)`.
- Versus: КОЛИ `pattern(line(3, includes defense_item))` → ТО `disappear(all_unbreakable_own)`.
- Versus: КОЛИ `pattern(line(4+))` → ТО `send_garbage(unbreakable)`.
- Versus: КОЛИ `reach(stack, top)` → ТО `lose` раунду; матч — до 2 перемог із 3.

## Керування і ввід
- D-pad — зсунути сусідню з діркою панель у дірку (тобто «перемістити дірку»); утримання й діагоналей — (?).
- A — підняти ряди вручну (раніше за таймер).
- C — вимкнути коментарі навігаторки в раунді Pin-Up (у мануалі не описано).
- Решта кнопок, за оглядом, нічого не роблять у грі; пауза на Start — (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` / `mode-select`: 1P Exercise · 1P Pin-Up · 2P Versus · налаштування.
- `level-select` — Exercise: вибір одного з 4 стартових раундів.
- `match-setup` — Versus: предмети атаки/захисту вмикаються окремо для кожного гравця перед матчем.
- `settings-window` — сепія та режим «монохромного зору» (без нього символи панелей важко розрізнити).
- `game-screen` (Exercise): поле 6×11 з рядком NEXT, справа `objective-text` (умова раунду) і `goal-counter`, `score`, `level-number`; персонаж-навігатор з `hint-text` японською.
- `game-screen` (Pin-Up): ліве поле + права яма з картинкою, `lives`, `score`.
- `game-screen` (Versus): `opponent-boards` — два поля поруч, рахунок раундів (?).
- `end-screen` / game over; паролів і континʼю нема.
- Переходи: main-menu → mode → (level-select / match-setup) → game-screen → наступний раунд / game over → main-menu.

## Фічі поза полем
- Режими: `mode-puzzle`-подібний Exercise (раунди з цілями), Pin-Up (відкрити картинку), `mode-versus` (2P, best of 3).
- `levels-sequential` (30 + 30 раундів), старт з одного з 4 раундів у Exercise.
- Життя: 3 у Pin-Up, додаткові — за пороги очок.
- `theme-select`-подібні сепія та монохром; `custom-rules` — вмикання предметів у Versus.
- Перевидання: вбудована гра Mega Drive Mini 2 (2022).

## Варіації й родичі
- Первісно лише Японія (Namco, 1990); перше власне Mega Drive-видання Namco. Інших портів, крім Mega Drive Mini 2, нема.
- Родичі в корпусі: `panel-de-pon` (стек росте знизу, але курсор-обмін 2×1 і гравітація), `sliding-tile-permutation` («пʼятнашки» — тут без мети впорядкування), `chuzzle` і `yoshis-cookie` (зсув цілого ряду замість однієї дірки), `puzzle-scape` (стек знизу).
- **Осі варіацій**:
  - чим рухати плитки: одна дірка (Megapanel) / курсор-обмін (Panel de Pon) / зсув ряду з загортанням (Chuzzle) / вільний drag;
  - що після зчищення: осідання стовпця / дірки лишаються / нові панелі згори;
  - ланцюги: нема бонусу (Megapanel) / chain-множник (Panel de Pon, Puyo);
  - мета раунду: виживання / задана ціль (кольори, довжини) / відкрити картинку другим полем.

## Цікавинки для курсу
- Одна дірка в стеку: хід = обмін дірки з сусідом, блок у край і в «повітря» над стеком — 📎 (простий автомат, але треба тримати позицію дірки).
- Пошук ходів: BFS по позиціях дірки до найближчого можливого збігу (підказка або AI) — 🥈 (стан = усе поле, але глибина мала).
- Pin-Up: зчищення в лівому полі керує бомбами в правому, з правилом «4+ → бомба на кожну панель» і блоками на 2 удари — 🥉.
- Цілі раунду як дані (N збігів, колір×довжина, очки) з перевіркою після кожного зчищення — 📎.
- Versus-предмети атаки/захисту з порогом «кожні 20 зчищених» і незнищенне сміття — 🥉.
- Підйом стеку за таймером із попередженням NEXT і ручним прискоренням — 🌱.

## Мапа на каталог
- Є: `line-match-clear` ↔ 3+ у рядок/стовпець; `impassable-cells` ↔ край і порожнеча над стеком; `progress-acceleration` ↔ швидкість підйому з рівнем; `sequential-levels` + `level-select` ↔ 30 раундів, вибір старту; `extra-life-threshold` ↔ життя за очки; `player-death` ↔ 3 життя Pin-Up; `event-points`; `garbage-attack` + `simultaneous-versus` ↔ Versus; `objective-text` + `goal-counter` ↔ умова раунду; `game-settings` + `theme-select` ↔ сепія/монохром.
- **Нема** → пропозиції карток:
  - `+slide-into-gap` (спільна з «пʼятнашками», Forbidden Desert) — панель у дірку, дірка одна.
  - `+rising-stack` (спільна з Panel de Pon) і `+manual-row-add` (кнопка A).
  - `+picture-reveal` (спільна з Pictobits, Gals Panic) — тут друге поле, яке руйнують бомби з першого.
  - `+multi-hit-block` (спільна з Crystal Mines II) — зелений блок на 2 бомби.
  - `+defense-item` «Предмет захисту знімає все сміття зі свого поля» · game-logic/opponent · 🌱 — пара до атаки.
  - `+round-goals` «Ціль раунду як набір умов (N збігів, колір, довжина, очки)» · game-logic/win · 📎.
  - `+no-chain-bonus` «Ланцюг без нагороди» · game-logic/score · 🌱 — вісь «ланцюги» в нуль.

## Пропозиції до словників
- `+effect:raise_stack` — стек на ряд угору з новим рядом знизу (повтор з Panel de Pon).
- `+card:round-goals` — умови раунду як дані (Megapanel Exercise; родич `collect-quota`).
- `+card:defense-item` — предмет, що прибирає сміття зі свого поля.
- `+feature:navigator-mute` — вимкнути коментатора-підказника в раунді.

## Джерела
- ⭐ [Wikipedia JA: メガパネル](https://ja.wikipedia.org/wiki/メガパネル) — поле 11×6, «15-пазл», 3+ по вертикалі/горизонталі, діагональ і ланцюги не рахуються, підйом знизу, Exercise (умови праворуч, 30 раундів), Pin-Up (бомба на зчищення, 4+ → по бомбі на блок, 30 раундів), Vs (best of 3, предмети після 20+ зчищених), Mega Drive Mini 2.
- [Wikipedia EN: Megapanel](https://en.wikipedia.org/wiki/Megapanel) — одна порожня клітина, ряд знизу, 3 життя, Pin Up.
- [Gaming Hell: Megapanel](https://gaminghell.co.uk/Megapanel.html) — 6×11 + ряд NEXT, одна чорна клітина, «без гравітації й вільного курсора», D-pad/A/C, 4 стартові раунди, зелені блоки, перемикання предметів Vs, сепія/монохром.
- [RetroXP: It's new to me — Megapanel](https://retroxp.beehiiv.com/p/it-s-new-to-me-megapanel) — одна дірка, нерівні стовпці після зчищень, цілі Exercise, 3 спроби в Pin-Up, C вимикає навігаторку.
- [Sega Does: Megapanel](https://segadoes.com/?p=4709) — бомба падає під центральною панеллю трійки; картинку руйнують лише бомби.
- YouTube: пошук «megapanel mega drive gameplay».

## Непевне
- (?) Що відбувається з клітинами після зчищення: огляди кажуть «одна чорна клітина завжди» і «без гравітації», але й про нерівні стовпці та «випадкові ланцюги» — найімовірніше, стовпець над зчищеним осідає, а дірка лишається одна; прямого опису нема.
- (?) Напрям D-pad: «вгору» — панель знизу йде в дірку, чи дірка йде вгору — не перевірено.
- (?) Кількість кольорів панелей, таблиця очок, інтервал підйому — не знайдено.
- (?) EN-вікі: у Versus «три й більше рядів» кидають блоки супернику; JA і Gaming Hell — 4–5 панелей одним зчищенням і предмет атаки. Беру JA.
- (?) Чи є Versus проти CPU — джерела згадують лише 2P.
