---
title: Homescapes / Gardenscapes / Royal Match (мета-шар ремонту)
slug: match3-meta-renovation
aka: [Homescapes, Gardenscapes, "Gardenscapes: New Acres", Royal Match, match-3 + renovation meta]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2016
platforms: [iOS, Android, Facebook, Windows, macOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Royal_Match", best: true, note: "ліміт ходів, 5 життів, pre-game і in-game бустери, режими, Teams, відновлення замку"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Homescapes", note: "зірка за рівень → задачі to-do, вибір декору, бустери Rocket/Bomb/Paper Plane/Rainbow Ball, перешкоди, сюжет, ASA і реклама pin-pull"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gardenscapes", note: "New Acres 2016: зірки за задачі, вибір прикрас, pin-pull мініігри; оригінал 2009 — hidden object"}
  - {kind: official, url: "https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/6-creating-and-using-the-power-ups", note: "Royal Match Help Center: як створюються Rocket/Propeller/TNT/Light Ball"}
  - {kind: official, url: "https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/7-power-up-combinations", note: "таблиця комбінацій двох power-up"}
  - {kind: official, url: "https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/15-what-are-tasks-and-how-do-i-complete-them/", note: "задачі зони, зірки, Area Chest"}
  - {kind: official, url: "https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/5-lives/", note: "5 життів (8 з Royal Pass), 1 за 30 хв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=royal+match+gameplay+area+tasks", note: "пошук; геймплей і ремонт"}
stage: v1
coverage: 60
mechanics: [swipe-gestures, cell-click, gravity-fall, spawn-random-cell, chain-reaction, explode-area, chain-detonation, move-limit, collect-quota, goal-counter, sequential-levels, level-unlock, world-map, inventory-items, round-currency, shop-window, save-progress, online-multiplayer, end-screen, +match-3-swap, +special-tiles, +special-combos, +tap-activate-special, +seeking-special, +stars-for-tasks, +task-list-meta, +decor-variant-choice, +area-chest, +story-chapters, +stamina-energy, +pre-level-boosters, +team-lives-request, +minigame-interlude]
proposes: ["+effect:fly_to", "+cond:most_common", "+window:home-screen", "+window:task-list", "+window:decor-choice", "+window:chest-reward", "+feature:renovation-meta", "+feature:teams", "+card:stars-for-tasks", "+card:task-list-meta", "+card:decor-variant-choice", "+card:area-chest", "+card:tap-activate-special", "+card:seeking-special", "+card:minigame-interlude"]
author: opus
date: 2026-11-09
---

# Homescapes / Gardenscapes / Royal Match — рівень match-3 дає зірку, зірки витрачаються на задачі ремонту дому, сад чи замок

## Суть
Ядро поля — match-3 обміном сусідів з цілями й лімітом ходів, як у `candy-crush` (тут не повторюється). Новизна — **мета-шар ремонту**: кожен пройдений рівень дає **зірку** (Royal Match: рівно одну), зірки — валюта для **задач** у списку to-do поточної зони (поставити сходи, відновити статую, вибрати шпалери). Виконані всі задачі зони → **скриня зони** з монетами й бустерами → відкривається нова зона. Сюжет (дворецький Austin у Playrix, король Robert у Dream Games) подається через задачі, а гравець бачить, як порожня кімната стає вмебльованою — прогрес, видимий поза полем. Royal Match додає до поля ще й **спецплитки, що активуються дотиком** без збігу, та Propeller, що сам летить до цілі.

## Поле і час
- Поле match-3 довільної форми з шарами клітин і перешкодами; хід = обмін двох сусідів (або дотик до спецплитки в Royal Match).
- Покроково: хід → каскад до стабілізації → перевірка цілей → ходи −1.
- Два «простори»: **поле рівня** і **сцена зони** (кімната, сад, частина замку) з точками-задачами. Між ними — вікно рівня й вікно задач.
- Реальний час є лише в мета-шарі: відновлення життів (1 за 30 хв у Royal Match), події з дедлайнами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайна плитка | tile | колір | як у Candy Crush: обмін зі збігом, 3+ → зникає, падає |
| Rocket (Royal Match / Homescapes) | tile | напрям | RM: з 4 в лінію; чистить рядок або стовпець за своїм напрямом |
| Propeller (RM) | tile | — | з квадрата 2×2; злітає, чистить сусідні клітини, летить до однієї випадкової цілі й знищує її |
| TNT (RM) / Bomb (Homescapes) | tile | радіус 2 | RM: з L/T з 5; чистить усе в радіусі 2 клітин |
| Light Ball (RM) / Rainbow Ball (Homescapes) | tile | — | RM: з 5 в лінію; прибирає всі плитки одного кольору |
| Paper Plane (Homescapes) | tile | — | прибирає випадкові віддалені плитки |
| Перешкоди (вази, Royal Eggs у RM; вафлі, килим, коробки, фрукти в желе в Homescapes) | hazard | шари | знімаються сусідніми збігами/вибухами; частина — ціль рівня |
| Зірка | resource | 1 за рівень | валюта мета-шару |
| Монети | resource | — | купують життя, бустери, «продовження»; у Homescapes — ще й кастомізацію дому |
| Життя | resource | 5 (8 з Royal Pass), +1 / 30 хв | −1 за програний рівень |
| Задача (task) | static | ціна в зірках | виконана → у сцені зʼявляється обʼєкт / ремонт; іноді вибір варіанта декору |
| Зона (area) | zone | список задач | усі задачі виконано → скриня + кнопка «New Area» |
| Скриня зони (Area Chest) | container | монети, бустери, картки | відкривається за завершену зону |
| Персонажі сюжету | neutral | — | Austin, батьки, король Robert; листи з бонусами (Homescapes) |
| Бустери in-game (RM: Royal Hammer, Arrows, Cannons, Jester's Hat; Homescapes: Hammer) | supply | запас | застосовуються поза ходом на клітину/лінію |

## Правила (КОЛИ → ЯКЩО → ТО)
Поле (лише відмінності від Candy Crush):
- КОЛИ `input(swap a, b)` → ЯКЩО `adjacent(a, b)` → ТО `swap(a, b)`; без збігу — повернення (як у Candy Crush).
- КОЛИ `pattern(line(4))` → ТО `spawn_at(rocket)`; `pattern(square 2×2)` → `spawn_at(propeller)`; `pattern(L|T, 5)` → `spawn_at(tnt)`; `pattern(line(5))` → `spawn_at(light_ball)` (Royal Match).
- КОЛИ `input(tap special)` → ЯКЩО `occupied(cell, special)` → ТО `custom: «activate — спецплитка спрацьовує без збігу»`, `counter(moves, −1)` (RM: «tap or swap any power-up»).
- КОЛИ `custom: «спрацював rocket»` → ТО `clear(row|col за напрямом)`; tnt → `explode(radius 2)`; light_ball → `custom: «clear_color»`.
- КОЛИ `custom: «спрацював propeller»` → ТО `clear(neighbours)`, `custom: «fly_to — летить до випадкового елемента й знищує його»`.
Комбінації двох спецплиток (обмін двох спец — RM Help Center):
- rocket + rocket → `clear(row and col)` · rocket + tnt → `clear(3 rows + 3 cols)` · tnt + tnt → `explode(radius 4)`.
- propeller + propeller → `spawn(propeller ×3)`, кожен знищує 3 випадкові елементи · propeller + rocket|tnt → `custom: «propeller несе rocket/tnt до випадкової клітини»`.
- light_ball + rocket|tnt|propeller → ЯКЩО `custom: «most_common(color)»` → ТО `transform(всі плитки цього кольору → цей power-up)`, далі спрацьовують.
- light_ball + light_ball → `clear(all)` і `custom: «layer_down — по одному шару з кожного елемента»`.
Рівень:
- КОЛИ `counter(goals, ==, done)` → ТО `win`, `give(star, 1)`, `currency(+coins)` (?).
- КОЛИ `counter(moves, ==, 0)` → ЯКЩО `not custom: «цілі виконано»` → ТО `window(out-of-moves-offer)` (?); відмова → `lose`, `lives(−1)`.
- КОЛИ `counter(lives, <, max)` → ТО `timer(30 хв)` → `lives(+1)` (RM: max 5, з Royal Pass 8).
Мета-шар ремонту:
- КОЛИ `input(task)` → ЯКЩО `has(player, stars ≥ cost)` → ТО `take(stars, cost)`, `custom: «build — обʼєкт зʼявляється в сцені»`, `custom: «story — наступна репліка/глава»`.
- КОЛИ `input(task)` → ЯКЩО `custom: «задача з вибором декору»` → ТО `choose(variants)` (Gardenscapes, Homescapes).
- КОЛИ `counter(area_tasks, ==, all)` → ТО `give(area_chest)`: монети, бустери, картки; `unlock(new_area)` через кнопку «New Area».
- КОЛИ `custom: «рівень кратний N»` → ТО `custom: «мінігра pin-pull замість рівня»` (Gardenscapes/Homescapes; «кожні 20 рівнів» — слова розробника).
- Перемога: нема фінальної — нескінченні рівні й зони (RM 12 400+ рівнів, листопад 2025) · Поразка рівня: ходи 0 без цілей · Рахунок: зірки (1 за рівень) і прогрес зон, а не очки.

## Керування і ввід
- Тач / миша: свайп плитки на сусідню; дотик до спецплитки (RM) — активація.
- Pre-game бустери (RM: Rockets, TNT, Light Balls) — галочки у вікні рівня; in-game бустери — вибрати іконку, потім клітину/лінію.
- Мета-шар: дотик по задачі у списку → анімація ремонту → іноді вибір із варіантів декору.

## Вікна, меню, HUD
- `custom: «home-screen»` — сцена зони (кімната / сад / замок) з кнопками: рівень «Play/Level N», список задач, магазин, команди, події, «New Area».
- `custom: «task-list»` — to-do зони: задача, ціна в зірках, кнопка виконати; лічильник зірок.
- `custom: «decor-choice»` — 2–3 варіанти обʼєкта для вибору (?).
- `custom: «level-intro»` — номер рівня, цілі, pre-game бустери, Play.
- `game-screen`: поле, `move-counter`, `goal-counter` (іконки цілей), панель in-game бустерів.
- `end-screen` — перемога (+1 зірка) / поразка (−1 життя, retry); `custom: «out-of-moves-offer»` (?).
- `custom: «chest-reward»` — відкриття скрині зони.
- `shop-window` (монети, набори, Royal Pass) · `lobby-window`-подібне вікно команд (Teams: чат, запит життів) · `leaderboard` подій (King's Cup, Royal League, Team Battle).
- `dialogue-window` — репліки персонажів між задачами; листи з бонусами (Homescapes).
- `settings-window` — звук, акаунт (?).
- Переходи: home-screen → level-intro → game-screen → end-screen → home-screen (+зірка) → task-list → анімація в сцені → (зону завершено) chest-reward → нова зона.

## Фічі поза полем
- `custom: «renovation-meta»` — зірки → задачі → зони; сюжетні глави відкриваються з рівнем (Homescapes).
- `levels-sequential` · `level-unlock`; нові рівні що ~2 тижні (RM).
- `custom: «lives-regen»` (див. candy-crush) · `shop-window` + монети · Royal Pass (сезонний пропуск: 8 життів).
- `custom: «teams»` — альянси: запит життів, командні події (RM Teams, Team Battle).
- `mode-*`-події: Tournament, Challenge, Quest (RM); Flying High, Cake o'clock, щоденний бонус (Homescapes).
- `custom-skins`-подібна кастомізація дому (Homescapes: шпалери, меблі — «100 000+ дизайнів»).
- Офлайн-гра можлива (RM).

## Варіації й родичі
- Ядро — `candy-crush` (2012); мета «будуй дім/місто за зірки» — Playrix (Gardenscapes: New Acres 2016 → Homescapes 2017 → Township-подібні), Dream Games (Royal Match 2020/2021, Royal Kingdom), Peak (`toon-blast` — зірки йдуть у скрині, а не в ремонт).
- Оригінальний Gardenscapes (2009) і Mansion Makeover — hidden-object, не match-3.
- **Осі варіацій**: що дає рівень (очки / 1–3 зірки / рівно 1 зірка) · куди йдуть зірки (скриня / задача ремонту / будівля міста) · вибір у мета-шарі (нема / варіант декору) · сюжет (нема / глави через задачі) · соціальне (друзі / команди).

## Цікавинки для курсу
- Мета-шар «зірка за рівень → задачі зони → скриня → нова зона» як дані (JSON зон і задач) — 🥉.
- Вибір варіанта декору й збереження вибору між сесіями — 📎.
- Спецплитка, що активується дотиком без збігу (витрачає хід) — 🌱.
- Propeller: пошук цілі (випадкова / пріоритетна — ціль рівня) і політ над полем — 📎.
- Комбо light ball + X: перетворити всі плитки найчастішого кольору на спецплитку і підірвати ланцюгом — 🥉.
- Життя, що відновлюються за реальним часом, + бонус-Pass, що збільшує максимум — 📎.
- Мініігра іншого жанру (pin-pull) кожні N рівнів — 🥈 (друга механіка в тій самій оболонці).

## Мапа на каталог
- Є: `swipe-gestures` · `cell-click` · `gravity-fall` · `spawn-random-cell` · `chain-reaction` · `explode-area` (TNT) · `chain-detonation` · `move-limit` · `collect-quota` (цілі рівня) · `goal-counter` · `sequential-levels` · `level-unlock` · `world-map` (зони як вузли прогресу) · `inventory-items` (бустери) · `round-currency` (монети — найближча) · `shop-window` · `save-progress` · `online-multiplayer` (команди, події) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` · `+special-tiles` · `+special-combos` · `+stamina-energy` · `+pre-level-boosters` — як у Candy Crush.
  - `+tap-activate-special` «Спецплитка спрацьовує дотиком, без збігу» · entities/interact · 🌱.
  - `+seeking-special` «Спецплитка сама летить до цілі» · entities/move · 📎 · слот {target: random|goal}.
  - `+stars-for-tasks` «Зірки за рівні — валюта задач мета-шару» · game-logic/economy · 📎.
  - `+task-list-meta` «Список задач зони зі скринею за завершення» · levels/progression · 🥉.
  - `+decor-variant-choice` «Вибір варіанта декору в задачі» · levels/progression · 📎.
  - `+area-chest` «Скриня за завершену зону» · game-logic/economy · 🌱.
  - `+story-chapters` «Сюжетні глави відкриваються прогресом» · levels/progression · 📎.
  - `+team-lives-request` «Запит життів у команди» · game-logic/opponent · 🥈 (сервер).
  - `+minigame-interlude` «Мінігра іншого жанру кожні N рівнів» · levels/progression · 🥈.

## Пропозиції до словників
- `+effect:fly_to` — сутність летить над полем до обраної цілі й діє там (Propeller, рибка Candy Crush).
- `+cond:most_common` — колір/тип, якого найбільше на полі (комбо light ball + X).
- `+window:home-screen` — сцена мета-шару з точками задач (не `map-window`: це одна кімната, а не мапа рівнів).
- `+window:task-list` — список задач зони з цінами в зірках.
- `+window:decor-choice` — вибір одного з варіантів обʼєкта.
- `+window:chest-reward` — відкриття скрині з нагородами (Royal Match, Toon Blast).
- `+feature:renovation-meta` — мета-прогрес «ремонт за зірки» між рівнями.
- `+feature:teams` — постійні команди гравців з чатом і обміном життями (родич `chat`, `online-multiplayer`).
- `+card:*` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Royal Match](https://en.wikipedia.org/wiki/Royal_Match) — ліміт ходів, 5 життів, 12 400+ рівнів, pre-game і in-game бустери, Tournament/Challenge/Quest, Teams, відновлення замку, офлайн.
- [Wikipedia: Homescapes](https://en.wikipedia.org/wiki/Homescapes) — зірка за рівень, to-do задачі, вибір декору, бустери, перешкоди, монети, сюжет, листи, події, ASA і pin-pull.
- [Wikipedia: Gardenscapes](https://en.wikipedia.org/wiki/Gardenscapes) — New Acres: зірки за задачі, вибір прикрас, pin-pull «кожні 20 рівнів»; оригінал 2009.
- Royal Match Help Center: [power-ups](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/6-creating-and-using-the-power-ups) · [комбінації](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/7-power-up-combinations) · [задачі й зони](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/15-what-are-tasks-and-how-do-i-complete-them/) · [життя](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/5-lives/) · [зірки](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/16-how-can-i-get-stars-1721127793/) · [нова зона](https://dreamgames.helpshift.com/hc/az/3-royal-match/faq/17-how-can-i-unlock-a-new-area/).

## Непевне
- (?) Скільки зірок коштує задача й скільки задач у зоні; монети за перемогу.
- (?) Вікно «+5 ходів за монети» перед поразкою — є в жанрі, у відкритих джерелах для цих ігор не підтверджено.
- (?) Скільки варіантів декору дають на вибір (зазвичай 3 — з памʼяті).
- (?) Чи дотик до спецплитки в RM витрачає хід — Help Center пише лише «tap or swap to activate».
- (?) Створення спецплиток у Homescapes/Gardenscapes (за якими фігурами) — Wikipedia перелічує лише ефекти; «Hammer знищує випадкову плитку» — так у Wikipedia, ймовірно — обрану (?).
- (?) King's Nightmare, Super Light Ball, Royal Pass — деталі не перевірено.
