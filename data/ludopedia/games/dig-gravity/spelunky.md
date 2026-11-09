---
title: Spelunky
slug: spelunky
aka: [Spelunky Classic, Spelunky HD]
family: dig-gravity
also: [grid-platformer, roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2008
platforms: [PC (freeware 2008), Xbox 360 (HD, 2012), PC, PS3, Vita, PS4]
links:
  - {kind: other, url: "https://tinysubversions.com/spelunkyGen/", best: true, note: "інтерактивний розбір генерації: сітка 4×4 кімнат, типи 0–3, шлях-розвʼязок, зміїні ями"}
  - {kind: other, url: "https://tinysubversions.com/spelunkyGen2/", note: "частина 2: шаблони кімнат 10×8, імовірнісні тайли, блоки-перешкоди 5×3, дзеркалення"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spelunky", note: "огляд: бомби й мотузки, руйнований рельєф, крамниці, permadeath, 4 зони"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spelunky+gameplay", note: "пошук; геймплей"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Spelunky", note: "пошук Steam (HD, Spelunky 2)"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, ladder-climb, destructible-blocks, explode-area, bomb-fuse, push-object, hp-damage, touch-death, environment-death, player-death, permadeath, item-pickup, inventory-items, round-currency, shop-catalog, thief, timeout-punisher, reach-exit, sequential-levels, dungeon-generation, weighted-spawn, reachability-check, player-camera, status-panel, in-game-editor, +room-template-grid, +solution-path-gen, +probabilistic-tile, +obstacle-chunk, +rope-throw, +fall-damage, +throw-item, +mirror-room, +shopkeeper-aggro, +idol-trap]
proposes: ["+trigger:land", "+effect:rope", "+ui:bombs-counter", "+ui:ropes-counter", "+card:room-template-grid", "+card:solution-path-gen", "+card:probabilistic-tile", "+card:obstacle-chunk", "+card:rope-throw", "+card:shopkeeper-aggro", "+card:idol-trap"]
author: opus
date: 2026-11-09
---

# Spelunky — процедурна печера з тайлів, яку бомби й мотузки перебудовують під себе

## Суть
Спелеолог спускається рівнями печери до виходу, збирає золото й рятує дамсел, уникаючи пасток і ворогів. Ядро для корпусу — **клітинний шар**: кожен рівень зібраний генератором із шаблонів кімнат, рельєф руйнований, а обмежені бомби (дірка в стіні/підлозі) і мотузки (вертикальний шлях угору) дозволяють прокласти свій маршрут замість задуманого. Смерть остаточна, тож кожен вибух — витрата дефіцитного ресурсу.

## Поле і час
- Рівень = **сітка 4×4 кімнат**, кожна кімната — **10×8 тайлів**; довкола — незруйновна рамка.
- Види тайлів: порожнеча, твердий блок (руйнується бомбою), драбина, платформа на вершині драбини, штовхальний блок, шипи, пастки; незруйновні межі.
- Шлях-розвʼязок від стартової кімнати у верхньому ряду до виходу в нижньому гарантований типами кімнат; решта кімнат — тип 0 без гарантій виходів.
- 4 зони по кілька рівнів з наростанням складності; глибше — дорожчі скарби. Real-time; камера слідує, видно частину рівня (`info: partial`), бувають темні рівні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Спелеолог | player | серця (HP), бомби, мотузки, золото | біг, стрибок, лазіння драбиною/мотузкою, батіг, кидок предмета |
| Твердий тайл (земля, камінь) | terrain | руйнується | опора; бомба → порожнеча |
| Незруйновна рамка | static | — | межа рівня |
| Драбина / платформа | terrain | — | лазіння; на платформу можна стати знизу |
| Штовхальний блок | object | — | штовхається, падає без опори |
| Шипи | hazard | — | падіння на них → смерть |
| Пастка-стріла | hazard | — | стріляє, коли щось на лінії |
| Бомба | projectile | запал (?) | кидається, відскакує, вибухає, руйнує тайли в радіусі |
| Мотузка | object | — | кидається вгору, розвертається вниз; по ній лазять |
| Золото / самоцвіти | pickup | ціна; глибше дорожче | +очки й гроші |
| Ящик (crate) | container | — | відкрити → випадковий предмет |
| Предмети (кирка, рукавички, пружинні черевики, джетпак, рушниця…) | pickup | — | змінюють правила руху/руйнування; кирка копає тайли |
| Дамсела | neutral | — | донести до виходу → +HP |
| Продавець (shopkeeper) | neutral | — | продає; крадіжка/напад → ворог із рушницею |
| Ідол | pickup | — | взяти → пастка (котиться валун) (?) |
| Вівтар Калі | switch | — | жертва → нагорода; знищити → кара |
| Вороги (змії, павуки, кажани…) | enemy | HP | патрулі/стрибки/пікірування; дотик — шкода |
| Привид | enemy | — | зʼявляється, коли час рівня ~2:30; проходить крізь стіни |
| Вихід (двері) | static | — | наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «шлях-розвʼязок: старт у верхньому ряду, щокроку rng 1–5: 1–2 ліворуч, 3–4 праворуч, 5 вниз; край → вниз і розворот»`.
- КОЛИ `custom: «шлях іде вниз»` → ТО `set_value(room, type2)`; наступна кімната — тип 2 або 3; спроба вниз з нижнього ряду → `spawn_at(exit, room)`.
- КОЛИ `custom: «кімната поза шляхом»` → ТО `set_value(room, type0)`; 3–4 кімнати 0 у стовпчик → `prob(p)` → зміїна яма.
- КОЛИ `custom: «заповнення кімнати»` → ТО `custom: «вибір шаблону 10×8 з 8–16 для типу; тайл "4" — 25 % штовхального блока, "7" — 33 % шипів, "2" — 50 % блок/порожнеча; "5"/"6" — блок-перешкода 5×3 земний/повітряний»`; `prob(0.5)` → `custom: «дзеркалити кімнату»`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)` (гравець, блоки, предмети, тіла).
- КОЛИ `custom: «приземлення»` → ЯКЩО `custom: «висота падіння велика»` (?) → ТО `damage(player, 1)`, `stun(player, n)`; на шипи → `lose`.
- КОЛИ `input(bomb)` → ЯКЩО `counter(bombs, >, 0)` → ТО `counter(bombs, -1)`, `spawn(bomb)` кинутою або покладеною.
- КОЛИ `timer(fuse)` → ТО `explode(circle, r, into: empty)`: тверді тайли в радіусі → порожнеча; рамка й незруйновні — `block`; сутності — `damage`.
- КОЛИ `after(explode)` → ЯКЩО `not supported(push_block|item)` → ТО `fall(a)`.
- КОЛИ `input(rope)` → ЯКЩО `counter(ropes, >, 0)` → ТО `counter(ropes, -1)`, `custom: «мотузка злітає вгору до стелі й звисає вниз — нова вертикаль для лазіння»`.
- КОЛИ `input(up)` → ЯКЩО `cell(here, ladder|rope)` → ТО `move(player, up)`.
- КОЛИ `contact(player, push_block)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `input(whip)` → ЯКЩО `in_range(player, enemy, 1)` → ТО `damage(enemy, 1)`; стрибок на ворога зверху — теж `damage`.
- КОЛИ `input(throw)` → ТО `throw(held_item)`; КОЛИ `contact(thrown, enemy)` → ТО `damage(enemy, 1)`.
- КОЛИ `line_of_sight(arrow_trap, a)` → ТО `spawn(arrow)`; КОЛИ `contact(arrow, a)` → ТО `damage(a, n)`.
- КОЛИ `contact(enemy, player)` → ТО `damage(player, 1)`; КОЛИ `hp_zero(player)` → ТО `lose`, `game_over`, `custom: «наступний забіг з першого рівня»`.
- КОЛИ `contact(player, gold)` → ТО `pickup`, `currency(+value)`, `score(+value)`.
- КОЛИ `input(open)` → ЯКЩО `occupied(here, crate)` → ТО `spawn(random item)`.
- КОЛИ `reach(player, exit)` → ЯКЩО `has(player, damsel)` → ТО `heal(player, 1)`; ТО `next_level`.
- КОЛИ `input(buy)` → ЯКЩО `counter(gold, >=, price)` → ТО `currency(-price)`, `give(player, item)`.
- КОЛИ `custom: «винесено товар без оплати / удар по продавцю / вибух у крамниці»` → ТО `set_state(shopkeeper, angry)`; продавці на всіх наступних рівнях ворожі.
- КОЛИ `picked(player, idol)` → ТО `custom: «спрацьовує пастка: котиться валун»` (?).
- КОЛИ `counter(level_time, >=, 2:30)` → ТО `spawn_at(ghost, edge)`; попередження на 2:00; КОЛИ `contact(ghost, player)` → ТО `lose`.
- КОЛИ `destroyed(altar)` → ТО `custom: «кара Калі; третій вівтар — темрява й привид»`.
- Перемога: пройти всі зони (і фінал). Поразка: HP 0 або миттєва пастка. Рахунок: золото за забіг.

## Керування і ввід
- Стрілки — рух і лазіння; стрибок; батіг/дія; біг (утримання); кнопки «бомба» і «мотузка»; вниз + дія — підняти/покласти; кидок того, що в руках.
- Вниз біля краю — висіти на ребрі; «бомба вниз» — покласти під себе.
- Класика (2008) — клавіатура/геймпад; HD — геймпад, локальний кооп/дезматч до 4.

## Вікна, меню, HUD
- `main-menu` (класика — «печера-хаб» з дверима режимів, ?).
- `game-screen`: печера; HUD — `hp-bar` (серця), `bombs-counter`, `ropes-counter`, `coins` (гроші), `timer-elapsed` рівня, предмети в руках/на поясі.
- `end-screen` між рівнями: зібране золото, час рівня й забігу, вороги (?).
- `end-screen` смерті: підсумок забігу, рекорд.
- `editor-window` — вбудований редактор рівнів у класиці.
- `pause-menu`, `settings-window`.
- Переходи: вихід → підсумок рівня → наступний рівень; смерть → підсумок → хаб.

## Фічі поза полем
- `permadeath` / `mode-hardcore` за замовчуванням; ярлики Tunnel Man (відкриття старту з пізніших зон, ?).
- `level-editor` (класика), `local-multiplayer` (HD: кооп і дезматч до 4).
- Секрети: артефакти (капала, хеджет), що дають надприродні здібності; хеджет вимикає привида.
- `leaderboard-online` і daily (HD, ?).

## Варіації й родичі
- Spelunky HD (2012), Spelunky 2 (2020) — розвиток тих самих систем (рідини в 2).
- У сімʼї: Noita — руйнування до рівня пікселя з фізикою матеріалів; Dig Dug / Mr. Driller — копання як ядро; SteamWorld Dig — копання + драбини.
- Родичі: Lode Runner (руйнування тайлу як інструмент, grid-platformer), La-Mulana.
- **Осі варіацій**: генерація — «повністю шум / шаблони кімнат на гарантованому шляху (Spelunky) / BSP-кімнати й коридори (Rogue)»; руйнування — «обмеженими бомбами / необмеженим копанням (кирка) / пікселями (Noita)»; виправлення маршруту — «мотузка / драбина / телепорт».

## Цікавинки для курсу
- Генерація шляху-розвʼязку в сітці 4×4 з типами кімнат 0–3 — 🥉 (декілька рядків коду, гарантована прохідність).
- Шаблони кімнат з імовірнісними тайлами й блоками-перешкодами 5×3, дзеркалення — 🥈.
- Бомба руйнує тайли в радіусі, крім незруйновних, з осіданням незакріпленого — 📎.
- Мотузка як «тимчасова драбина» за ресурс — 🌱.
- Привид-таймер проти зволікання (картка `timeout-punisher`) — 🌱.
- Продавець, що стає ворогом на всі наступні рівні (глобальний стан забігу) — 📎.
- Перевірка, що бомби/мотузки не обовʼязкові для проходу (BFS по тайлах) — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `ladder-climb` ↔ драбини, мотузки · `destructible-blocks` · `explode-area` + `bomb-fuse` · `push-object` · `hp-damage` · `touch-death` · `environment-death` ↔ шипи, пастки · `player-death` · `permadeath` · `item-pickup` · `inventory-items` · `round-currency` + `shop-catalog` · `thief` (тут гравець — злодій, наслідок — агресія) · `timeout-punisher` ↔ привид · `reach-exit` · `sequential-levels` · `dungeon-generation` · `weighted-spawn` ↔ імовірнісні тайли · `reachability-check` ↔ гарантований шлях · `player-camera` · `status-panel` · `in-game-editor`.
- **Нема** → пропозиції карток:
  - `+room-template-grid` «Рівень із сітки кімнат-шаблонів» · levels/generation · 🥈 · слоти {grid, room_size, templates}.
  - `+solution-path-gen` «Генерація гарантованого шляху кімнатами» · levels/generation · 🥉.
  - `+probabilistic-tile` «Тайл шаблону з імовірністю» · levels/generation · 🌱.
  - `+obstacle-chunk` «Підшаблон-перешкода 5×3 у кімнаті» · levels/generation · 📎.
  - `+mirror-room` «Випадкове дзеркалення кімнати» · levels/generation · 🌱.
  - `+rope-throw` «Мотузка за ресурс як нова вертикаль» · entities/move · 📎.
  - `+fall-damage` (повтор з Motherload, SteamWorld Dig) · `+throw-item` «Кинути предмет з рук» · entities/combat · 📎.
  - `+shopkeeper-aggro` «Нейтрал стає ворогом на весь забіг» · entities/state · 📎.
  - `+idol-trap` «Взяти скарб — спрацьовує пастка» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:land` — приземлення після падіння (повтор: SteamWorld Dig, Motherload).
- `+effect:rope` — створити тимчасову вертикаль для лазіння.
- `+ui:bombs-counter`, `+ui:ropes-counter` — лічильники витратних інструментів зміни рельєфу.

## Джерела
- ⭐ [Spelunky Generator Lessons, ч. 1](https://tinysubversions.com/spelunkyGen/) — сітка 4×4, типи кімнат 0–3, правило rng 1–5, вихід, зміїні ями.
- [Spelunky Generator Lessons, ч. 2](https://tinysubversions.com/spelunkyGen2/) — шаблони 10×8, коди тайлів, 25/33/50 %, блоки 5×3, дзеркалення.
- [Wikipedia: Spelunky](https://en.wikipedia.org/wiki/Spelunky) — механіки, крамниці й крадіжка, permadeath, 4 зони, артефакти, дамсели, редактор, HD-кооп.
- YouTube: пошук «Spelunky gameplay».

## Непевне
- (?) Стартові 4 серця / 4 бомби / 4 мотузки, тривалість запалу й радіус вибуху — з памʼяті; вікі (fandom) віддає 402.
- (?) Привид на 2:30 з попередженням на 2:00 — з пошукових сніпетів fandom, сторінку не відкрито.
- (?) Пастка ідола (валун) і поведінка вівтаря Калі — з памʼяті та сніпетів.
- (?) Шкода від падіння (1 серце, оглушення) і висота порогу.
- (?) Назви зон (Шахти, Джунглі, Крижані печери, Храм) — у Wikipedia не названі.
- (?) Вікна (хаб-меню, екран підсумку) і daily — з памʼяті, переважно HD.
- (?) Сімʼя: за `families.md` гра межує з `grid-platformer`/`roguelike`; тут описано клітинний шар (генерація, руйнування).
