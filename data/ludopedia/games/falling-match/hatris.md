---
title: Hatris
slug: hatris
aka: [ハットリス, Хетріс]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 1990
platforms: [arcade, NES, Famicom, Game Boy, PC Engine, PC-9801, Sharp Wizard, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hatris", best: true, note: "Пажитнов і Похилько, BPS; 5 однакових капелюхів зникають; платформи й дати"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ハットリス", note: "детальні правила: 6 стовпців, пари, 6 типів, FIRE, SALE, версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hatris+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, line-match-clear, keyboard-controls, next-queue, event-points, combo-multiplier, progress-acceleration, score-records, sequential-levels, round-currency, shop-window, simultaneous-versus, garbage-attack, mode-select, difficulty-levels, game-pause, end-screen, +falling-pair-swap, +shape-stack-height, +column-burn, +sale-meter-shop, +helper-summon, +column-swap, +match-size-setting]
proposes: ["+effect:burn", "+cond:stack_run", "+ui:sale-letters", "+feature:match-size-setting", "+card:shape-stack-height", "+card:sale-meter-shop", "+card:column-burn"]
author: opus
date: 2026-11-09
---

# Hatris — пари капелюхів падають на голови покупців; п'ять однакових капелюхів у стосі зникають

## Суть
Друга гра Олексія Пажитнова (з Володимиром Похилько) після Tetris. Згори падають **пари** капелюхів; гравець рухає пару вліво-вправо й міняє два капелюхи місцями. Капелюхи стають стосами в шести стовпцях (на головах покупців), і коли в стосі зібралося **п'ять однакових поспіль**, вони зникають («сет»). Шість типів капелюхів мають різну висоту й форму: одні вкладаються один в одного майже без втрати висоти, інші стоять «башнею», тож порядок важить. Гра закінчується, коли стос дістає верху.

## Поле і час
- 6 стовпців завширшки, до 35 рядків заввишки (аркада); низ кожного стовпця — голова покупця (аркада, NES) або підлога (Famicom).
- Real-time: пара падає з постійною швидкістю, «вниз» прискорює; Famicom додав hard drop і затримку фіксації на стосі.
- Наступна пара видима (?) (`info: partial`); типи — випадкові (`random: runtime`).
- Висота стосу рахується не в клітинах, а в сумі висот капелюхів з урахуванням вкладання (`+card:shape-stack-height`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Циліндр (top hat, чорний) | tile | висота, ширина основи/верху | падає в парі; стос 5 однакових зникає |
| Мʼякий капелюх (зелений, загнуті поля) | tile | висота, форма | те саме |
| Шолом (синій, без полів) | tile | висота, форма | те саме; у Famicom замінено |
| Сомбреро (широке) | tile | висота, форма | те саме; у Famicom замінено |
| Корона | tile | висота, форма | те саме; не горить у FIRE |
| Ковпак (гострий) | tile | висота, форма | те саме |
| Пара капелюхів | player | 2 капелюхи поруч | рух ←/→, обмін місцями (A), прискорення ↓ |
| Стовпець (голова) | zone | стос | тримає капелюхи; верх поля → кінець гри |
| Червоне полумʼя (FIRE) | pickup | — | спалює в стовпці всі капелюхи одного типу (аркада) |
| Синє полумʼя (FIRE) | pickup | — | спалює весь стовпець; двічі по покупцю — лисина (аркада) |
| Шкала SALE | resource | 4 літери | кожен сет запалює частину; повна (15 сетів) → магазин |
| Помічники Pajitnov / Vladimir (NES) | ally | купуються за cash | один скидає нижній ряд капелюхів, інший міняє два стовпці |
| Cash (NES) | resource | очки | валюта на виклик помічників |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `fall(pair)` на крок; КОЛИ `input(down)` → ТО `speed(pair, +n)`.
- КОЛИ `input(left|right)` → ЯКЩО `free(cell)` → ТО `move(pair, dir)`; інакше `block`.
- КОЛИ `input(A)` → ТО `swap(hat_left, hat_right)`.
- КОЛИ `contact(hat, stack_top)` → ТО `custom: «капелюх лягає на стос; приріст висоти залежить від пари форм (вкладання)»`; кожен з пари падає у свій стовпець окремо.
- КОЛИ `after(land)` → ЯКЩО `pattern(match(type, 5))` поспіль зверху стосу → ТО `clear(set)`, `score(base × level_factor)` (множник до ×10).
- КОЛИ `after(clear)` → ЯКЩО `chain(2)` (два сети поспіль) → ТО `multiplier(2)` для другого.
- КОЛИ `pattern(match(type, 6+))` → ТО `score(+bonus)` (Game Boy: очки за 5 + 1000).
- КОЛИ `contact(red_fire, stack)` → ТО `custom: «burn — згорають усі капелюхи одного типу в стовпці (крім корон)»`; `score` зменшено, якщо згоріло ≤ 3.
- КОЛИ `contact(blue_fire, stack)` → ТО `custom: «burn — згорає весь стовпець (крім корон)»`, `score` зменшено.
- КОЛИ `counter(sets, ==, 15)` → ТО `window(shop-window)` SALE: гравець обирає тип і `clear(all of type)`; той тип «SOLD OUT» до наступного порогу; аркада — з лімітом часу.
- КОЛИ `input(skip sale)` → ТО `score(+bonus)`, `custom: «магазин відкладено на потім»`.
- КОЛИ `input(B)` → ЯКЩО `has(player, helper)` → ТО `custom: «нижній ряд скинуто»` або `swap(column_a, column_b)` (NES).
- КОЛИ `reach(stack, top)` → ТО `game_over`.
- КОЛИ `counter(sets, >=, quota)` → ТО `next_level` (Famicom: 25 сетів, Game Boy: 20; аркада — без стадій).
- Перемога: нема (аркада, нескінченно) або 10 стадій (Famicom/NES). Поразка: стос дістав верху. Рахунок: тип × рівень, подвоєння за серію, бонуси 6+, SALE; лічильник до 999 999.

## Керування і ввід
- Хрестовина ←/→ — рух пари; ↓ — прискорення; A — обмін капелюхів у парі; B — виклик помічника (NES).
- Famicom: hard drop.
- Пауза — Start (?).

## Вікна, меню, HUD
- `game-screen`: 6 стовпців з головами покупців, падаюча пара, наступна пара (`next-piece-preview`) (?), `score`, `hi-score`, лічильник сетів, літери SALE (`+ui:sale-letters`), рівень (`level-number`).
- `shop-window` SALE: вибір типу капелюха для розпродажу, таймер (аркада).
- `custom-window`: налаштування старту — кількість капелюхів, високошвидкісний режим (Famicom/NES).
- `mode-select`: Game Boy — versus по лінк-кабелю; мобільні — endless і 2-хвилинна атака на час.
- `end-screen`: кінець гри, кількість сетів і очки → таблиця рекордів (`leaderboard`).
- `attract-demo`: аркадний demo (?).
- Переходи: title → налаштування → game-screen ↔ shop-window → end-screen → leaderboard.

## Фічі поза полем
- `difficulty-presets`: стартова кількість капелюхів, швидкий режим (Famicom/NES).
- `levels-sequential`: 10 стадій (Famicom/NES).
- `local-multiplayer` versus (Game Boy) — сети дають запас вогню, двійний сет додає стоку (?) для атаки.
- Мобільна версія: `mode-endless`, `mode-time-attack` (2 хв), `theme-select` (капелюхи → черепахи, відра, конуси), налаштування розміру сету 3/4/5 (`+feature:match-size-setting`).
- `leaderboard-local`: сети й очки.

## Варіації й родичі
- **Tetris** (`tetris.md`) — той самий автор; там лінії, тут стовпці-стоси.
- **Columns** (`columns.md`), **Dr. Mario** (`dr-mario.md`), **Puyo Puyo** (`puyo-puyo.md`) — падаючі пари/трійки з кольоровим збігом.
- **Baku Baku Animal** (`baku-baku-animal.md`) — пари, але «їжа ↔ тварина».
- **Klax** (`klax.md`) — стос плиток, 1990.
- **Осі варіацій**: що збігається (колір / тип з формою) · де (лінія / стос у стовпці / група) · висота елемента (1 клітина / залежить від форми) · розмір сету (3 / 4 / 5) · допомога (вогонь / магазин / помічник).

## Цікавинки для курсу
- Стос капелюхів, де приріст висоти залежить від пари форм (таблиця «що на чому») — 📎.
- Падаюча пара з окремим падінням кожного капелюха в свій стовпець — 🌱.
- 5 однакових поспіль на верху стосу → зникнення + серія ×2 — 🌱.
- Шкала SALE: 15 сетів → вибір типу й очищення всіх таких з «SOLD OUT» — 📎.
- Червоний / синій вогонь з винятком для корон — 🌱.
- Помічники за валюту (скинути ряд, обміняти стовпці) — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `line-match-clear` (тут — 5 у стосі) · `keyboard-controls` · `next-queue` · `event-points` · `combo-multiplier` (×2 за серію) · `progress-acceleration` · `score-records` · `sequential-levels` · `round-currency` + `shop-window` (SALE, cash) · `simultaneous-versus` + `garbage-attack` (Game Boy (?)) · `mode-select` · `difficulty-levels` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+falling-pair-swap` «Падаюча пара з обміном елементів» · entities/move · 🌱 (Hatris, Columns-подібні).
  - `+shape-stack-height` «Висота стосу залежить від форм елементів» · entities/legality · 📎.
  - `+column-burn` «Бонус спалює тип/стовпець» · entities/interact · 🌱.
  - `+sale-meter-shop` «Шкала сетів відкриває разове очищення типу» · game-logic/economy · 📎.
  - `+helper-summon` «Помічник за валюту виконує одну дію над полем» · game-logic/economy · 📎.
  - `+column-swap` «Обміняти два стовпці» · entities/move · 🌱.
  - `+match-size-setting` «Налаштування розміру збігу 3/4/5» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+effect:burn` — знищити сутності в стовпці за фільтром типу (FIRE у Hatris; споріднено з `clear`).
- `+cond:stack_run` — верхні N у стосі однакові (Hatris, Hexa Sort, Water Sort).
- `+ui:sale-letters` — літерна шкала прогресу до бонусу (SALE; Bubble Bobble EXTEND).
- `+feature:match-size-setting` — гравець задає розмір сету.
- `+card:shape-stack-height` · `+card:sale-meter-shop` · `+card:column-burn` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Hatris](https://en.wikipedia.org/wiki/Hatris) — Пажитнов і Похилько (ParaGraph), Bullet-Proof Software, Video System; аркада 04.1990; 5 однакових капелюхів зникають, різні типи стосуються по-різному; платформи й дати.
- [Wikipedia (ja): ハットリス](https://ja.wikipedia.org/wiki/ハットリス) — 6×35, пари, A — обмін, 6 типів, FIRE, SALE (15 сетів), множник рівня ×10, подвоєння за серію, версії Famicom/NES/Game Boy/мобільна.
- YouTube: пошук «hatris gameplay».

## Непевне
- (?) Чи показується наступна пара.
- (?) Як саме працює versus на Game Boy (стік вогню як атака) — переказ ja-статті неповний.
- (?) Конкретні висоти й правила вкладання кожної пари типів — статті не дають чисел.
- (?) Кожен капелюх пари падає окремо (як Puyo), якщо стовпці різної висоти — логічно, але явно не сказано.
- StrategyWiki і MobyGames віддали 403.
