---
title: Puzzle Pirates — Alchemistry (Алхімія)
slug: puzzle-pirates-alchemistry
aka: [Alchemistry, Y!PP Alchemistry]
family: connect-rotate
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2004
platforms: [PC, Mac, Linux]
links:
  - {kind: fandom, url: "https://yppedia.puzzlepirates.com/Alchemistry", best: true, note: "YPPedia: керування, змішування, пляшки й зірки, спецфігури, рахунок, назви комбо, історія (лічильник 75 ходів до 2010)"}
  - {kind: official, url: "https://yppedia.puzzlepirates.com/Official:Alchemistry", note: "офіційна довідка: мета, керування, кольори, великі пляшки, три спецфігури, принципи рахунку"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Pirates", note: "контекст: MMO з пазлами замість дій, Three Rings, 2003, Java, Steam і free-to-play з 2011"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=cz8HE1hpJEs", note: "відео з YPPedia («Decent video, no sound») — не переглядав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Puzzle+Pirates+Alchemistry", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tile-rotate, pipe-connectors, cell-click, keyboard-controls, controls-remap, highlights, event-points, combo-multiplier, spawn-random-cell, move-limit, game-screen, end-screen, settings-window, achievements-window, leaderboard, score-records, +color-mixing-flow, +layered-bottle, +commit-button, +crossing-pipe, +wildcard-carryover, +broken-slot-clog, +combo-name-ladder]
proposes: ["+effect:flow", "+effect:mix", "+effect:pour", "+ui:fill-button", "+ui:quality-stars", "+window:duty-report", "+card:color-mixing-flow", "+card:layered-bottle", "+card:crossing-pipe", "+card:wildcard-carryover"]
author: opus
date: 2026-11-09
---

# Puzzle Pirates — Alchemistry — крути труби, щоб фарби з колб згори дотекли й змішалися дорогою до пляшок із потрібною етикеткою

## Суть
Ремісничий пазл аптекаря в MMO Puzzle Pirates: годину праці в крамниці відпрацьовуєш, розвʼязуючи дошку (витягнуто лише сітковий шар; світ, кораблі й економіка гри — поза файлом). Зверху — колби з первинними фарбами, внизу на конвеєрі — пляшки з етикетками; гравець крутить плитки-труби, щоб провести кольори до пляшок, і тисне FILL. Два первинні кольори, що зустрілися в трубі, змішуються у вторинний; три — у бурий мул, що розбиває пляшку. Механіка запозичена з [Rocket Mania](rocket-mania.md), але без таймера: тиск дає лише конвеєр, де розбита пляшка засмічує слот до кінця сесії.

## Поле і час
- Квадратна сітка плиток-труб (на скріншоті YPPedia ≈ 8 стовпців × 10 рядків (?)); над нею ряд колб, під нею конвеєр із пляшками й ряд слотів для заповнених.
- Хід = поворот однієї плитки; FILL — окремий «коміт», після якого дошка оновлюється. Час на рахунок не впливає.
- До 9 березня 2010 був лічильник: 75 ходів, після яких цінніші пляшки розбивались; тепер — без обмеження.
- Сесія закінчується, коли всі слоти під конвеєром заповнені.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Колба | source | колір: жовтий / червоний / синій (на скріншоті — по дві, жовті ліворуч, червоні в центрі, сині праворуч) | дає фарбу в трубу під собою |
| Колба ртуті | source | джокер | зʼявляється на наступній дошці після спецфігури Q; наливає будь-який нижній колір |
| Труба: пряма, кут, Т, хрест | conduit | порти, орієнтація | крутиться; проводить фарбу між портами; суміжні гілки зливаються |
| Труба-перехрестя | conduit | два незалежні канали | два потоки проходять крізь клітину, не змішуючись; цінна для багатоколірних заливок |
| Пляшка | sink | етикетка з 1+ кольорів знизу вгору | приймає лише нижній незаповнений колір; повна — переїжджає в слот із 0–3 зірками |
| Розбита пляшка | static | — | лишається на конвеєрі й засмічує місце до кінця сесії |
| Слот під конвеєром | zone | кількість | заповнена пляшка займає слот; усі зайняті — кінець |
| Монета (бонус) | pickup | на плитці | фарба крізь неї — трохи більше очок за заливку |
| Стрілка (multi-fill) | pickup | на плитці | заливає поспіль усі шари цього кольору в пляшці, якщо він нижній |
| Q (quicksilver) | pickup | на плитці | кожен колір крізь неї → колба ртуті на наступній дошці |
| Бурий мул | hazard | 3 первинні | розбиває будь-яку пляшку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click_left, tile)` → ТО `rotate(tile, -90)`; КОЛИ `input(click_right, tile)` → ТО `rotate(tile, 90)`; колесо — обидва боки.
- КОЛИ `after(rotate)` → ЯКЩО `path_exists(bulb, tile)` → ТО `custom: «труба зафарбовується кольором потоку»` (потік видно до FILL).
- КОЛИ `custom: «у вузлі зустрілись два первинні потоки»` → ТО `custom: «змішати: жовтий + синій = зелений, червоний + жовтий = помаранчевий, синій + червоний = фіолетовий»`.
- КОЛИ `custom: «зустрілись усі три первинні»` → ТО `transform(flow, brown)`.
- КОЛИ `input(fill)` → ЯКЩО `path_exists(bulb, bottle)` хоча б для однієї пляшки → ТО `custom: «налити в усі звʼязані пляшки одночасно»`; без такого шляху кнопки FILL нема.
- КОЛИ `input(fill)` → ЯКЩО `same(flow, bottle_bottom_label, color)` → ТО `custom: «заповнити нижній шар»`; інакше `transform(bottle, broken)`.
- КОЛИ `input(fill)` → ЯКЩО `state(flow, brown)` → ТО `transform(bottle, broken)`, `score(-small)`.
- КОЛИ `custom: «усі шари пляшки заповнено»` → ТО `move(bottle, slot)`, `set_value(bottle, stars 0..3)`.
- КОЛИ `after(fill)` → ТО `disappear(painted_tiles)`, `spawn(random_tile)` на звільнені місця (як саме — (?)).
- КОЛИ `after(fill)` → ЯКЩО `custom: «заливка дала багато очок»` → ТО `spawn(special_tile)` з більшою ймовірністю.
- КОЛИ `custom: «фарба пройшла через монету»` → ТО `score(+bonus)`.
- КОЛИ `custom: «фарба пройшла через стрілку»` → ЯКЩО `custom: «колір — нижній шар пляшки»` → ТО `custom: «заповнити всі поспіль шари цього кольору»`.
- КОЛИ `custom: «фарба пройшла через Q»` → ТО `custom: «на наступній дошці колба цього кольору стає ртуттю»` (вторинний колір → дві колби).
- КОЛИ `input(fill)` → ЯКЩО `state(flow, quicksilver)` → ТО `custom: «заповнити будь-який нижній колір»`; у рахунку ртуть — один колір.
- Рахунок заливки: КОЛИ `input(fill)` → ТО `score(+bottle_value)`; кілька пляшок одного кольору — зростаючий бонус; різні кольори — зростаючий `multiplier`; вторинні цінніші за первинні, «далекий» вторинний (з крайніх колб) — трохи більше; багатошарова пляшка — середнє шарів з невеликим бонусом за шар.
- КОЛИ `counter(bottles_in_fill, >=, 2)` → ТО `message(…)`: 2 Double Bottle! · 3 Triple Bottle! · 4 Quadruple Bottle! · 5 Five Bottles! · 6 Bingo! · 7 Donkey! · 8 Vegas! · 9 Potent Potions! · 10 Witch Doctor! · 11+ Voodoo!
- КОЛИ `counter(colors_in_fill, >=, 2)` → ТО `message(…)`: 2 Double Double! · 3 Toil & Trouble! · 4 Fire Burn! · 5 Cauldron Bubble! · 6 Wicked! · 7 Transmutation! (лише з ртуттю).
- КОЛИ `count(empty_slot, ==, 0)` → ТО `game_over`, `window(end-screen)` (duty report з оцінкою).
- КОЛИ `custom: «усі пляшки розбито»` → ТО `message(Booched Brew)`, оцінка «booched».
- Перемога: заповнити всі слоти (оцінка від booched до incredible за середніми зірками) · Поразка: формально нема, лише погана оцінка · Рахунок: за заповнені пляшки.

## Керування і ввід
- Миша: вказати плитку; ЛКМ — проти годинникової, ПКМ — за годинниковою, колесо — обидва боки.
- Клавіатура: стрілки — вибір плитки, S — проти, D — за годинниковою, пробіл — FILL; призначення змінюються на екрані налаштувань.
- Клік по пляшці на конвеєрі — показати її «сяйво» (скільки вона вартуватиме).

## Вікна, меню, HUD
- `custom-window` (світ MMO): станція в аптеці — «Work at the Shoppe» (є робота) або «Practice Crafting» (тренування).
- `game-screen`: заголовок «Alchemistry», ряд колб, сітка труб, конвеєр із пляшками, кнопка FILL, ряд слотів зі зірками, зображення щура, лічильник у правому нижньому куті (?).
- HUD: кольоровий потік у трубах до заливки (`highlights`), `popup-text` з назвами комбо, сяйво пляшок (`quality-stars`).
- `end-screen` — duty report: оцінка сесії (booched … incredible); при 14+ шарах за одну заливку звіт не зʼявляється — Escape кілька разів (баг).
- `settings-window` — призначення клавіш; `achievements-window` — трофеї (Incredible Alchemist, Ultimate Alchemist, #1 Alchemist…); `leaderboard` — рейтинги алхіміків по океанах.
- Переходи: станція → game-screen → (слоти заповнено) duty report → світ.

## Фічі поза полем
- `mode-practice` — Practice Crafting без роботи; робоча сесія = 2 години праці над товаром з черги аптеки.
- `rank-tiers` — рейтинг навички за результатами; трофеї; «Ultimate list» по океанах (`leaderboard-online`).
- `remap-controls`; гра безкоштовна раз на тиждень (?) — так у YPPedia, залежить від підписки.

## Варіації й родичі
- [Rocket Mania](rocket-mania.md) — прямий предок: обертання плиток-ґнотів, згоряння шляху й поповнення; тут замість вогню — фарби з мішанням і пляшки зі стосом шарів.
- Корпус: [Pipe Mania](pipe-mania.md) (потік по трубах), [Chromatron](chromatron.md) (змішування кольорів променів), [Infinity Loop](infinity-loop.md) (лише звʼязність), [Alchemy (PopCap)](../falling-match/alchemy-popcap.md) — лише схожа назва, механіка інша (руни на сітці).
- Осі варіацій: **що тече** — вогонь (Rocket Mania) / рідина з мішанням (Alchemistry) / промінь (Chromatron) · **тиск** — таймер / ліміт ходів (до 2010) / лише ціна помилки · **приймач** — один колір / стос шарів знизу вгору.

## Цікавинки для курсу
- Колір як бітова маска первинних (Ж=1, Ч=2, С=4): змішування = OR, три біти = бурий — 🌱.
- Потік від кожної колби через граф труб (BFS по портах) з обчисленням кольору в кожній трубі — 🥉.
- Труба-перехрестя: дві незалежні мережі в одній клітині — 📎.
- Пляшка-стек шарів: приймає лише нижній, помилка — розбиття й засмічений слот — 📎.
- Рахунок з бонусом за кількість пляшок, множником за кількість кольорів і назвами комбо — 📎.
- Ртуть-джокер, що переходить на наступну дошку; спецфігури частіше після хорошої заливки — 📎.
- Видалення використаних труб і генерація нових (порада гравців: «підчищати» нудні кути, щоб зʼявились перехрестя) — 🥉.

## Мапа на каталог
- Є: `tile-rotate` ↔ поворот труби; `pipe-connectors` ↔ порти; `cell-click`, `keyboard-controls`, `controls-remap`; `highlights` ↔ кольоровий потік; `event-points` ↔ вартість пляшок; `combo-multiplier` ↔ множник за кольори; `spawn-random-cell` ↔ нові труби (?); `move-limit` ↔ 75 ходів до 2010; `game-screen`, `end-screen`, `settings-window`, `achievements-window`, `leaderboard`, `score-records`.
- **Нема** → пропозиції карток:
  - `+color-mixing-flow` «Змішування кольорів потоку у вузлах мережі» · entities/interact · 🥉 · слот {mix: OR|table}.
  - `+layered-bottle` «Приймач-стек шарів: лише нижній» · game-logic/win · 📎.
  - `+commit-button` «Кнопка-коміт (FILL): дія застосовується лише за запитом» · interface/input · 🌱.
  - `+crossing-pipe` «Перехрестя: два незалежні канали в клітині» · entities/interact · 📎.
  - `+wildcard-carryover` «Джокер переходить на наступну дошку» · entities/items · 📎.
  - `+broken-slot-clog` «Помилка засмічує слот до кінця» · game-logic/lose · 🌱.
  - `+combo-name-ladder` «Назви комбо за розміром» · interface/hud · 🌱.

## Пропозиції до словників
- `+effect:flow` — потік іде мережею від джерела (підтвердження, ×9 у корпусі).
- `+effect:mix` — два потоки дають третій колір (підтвердження: Chromatron та ін.).
- `+effect:pour` — налити в приймач (підтвердження, ×2).
- `+ui:fill-button` — кнопка застосування накопиченої дії; `+ui:quality-stars` — 0–3 зірки / сяйво якості на обʼєкті.
- `+window:duty-report` — підсумок сесії з оцінкою-словом (booched … incredible).
- `+card:color-mixing-flow`, `+card:layered-bottle`, `+card:crossing-pipe`, `+card:wildcard-carryover`.

## Джерела
- ⭐ [YPPedia: Alchemistry](https://yppedia.puzzlepirates.com/Alchemistry) — керування, змішування, бурий, великі пляшки й зірки, три спецфігури (ртуть і з вторинними), рахунок, порада «підчищати» дошку, назви комбо, booched, баг 14+ шарів, історія: введено 2004-10-21, лічильник 75 ходів знято 2010-03-09; зображення дошки.
- [YPPedia: Official:Alchemistry](https://yppedia.puzzlepirates.com/Official:Alchemistry) — офіційна довідка: мета, клавіші S / D / пробіл, змішування, правило нижнього кольору, спецфігури частіше після високої заливки, принципи рахунку (WebFetch віддає порожньо — читано curl).
- [Wikipedia: Puzzle Pirates](https://en.wikipedia.org/wiki/Puzzle_Pirates) — Three Rings, 2003, Java, Steam / free-to-play з 2011; про Alchemistry не пише.

## Непевне
- (?) Розмір сітки й кількість колб — лише зі скріншоту; чи змінюються з рівнем гравця — не перевірено.
- (?) Як саме зʼявляються нові труби після заливки (падають згори, як у Rocket Mania, чи на місці) — джерела лише кажуть, що зафарбовані труби звільняють місце.
- (?) Набір типів труб (пряма, кут, Т, хрест, перехрестя) — з порад гравців і скріншоту; можливі інші.
- (?) Лічильник «43» у кутку скріншоту — ходи (до 2010) чи щось інше.
- (?) Чи змішуються два однакові первинні потоки (наприклад, з двох жовтих колб) як один колір — очевидно так, але явно не сказано.
