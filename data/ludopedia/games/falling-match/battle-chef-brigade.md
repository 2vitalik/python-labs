---
title: Battle Chef Brigade
slug: battle-chef-brigade
aka: [Battle Chef Brigade Deluxe, BCB]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2017
platforms: [PC, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Chef_Brigade", best: true, note: "двофазний бій: полювання-брейлер → кухня; інгредієнти → самоцвіти смаку у 4×4, однакові зливаються в вищий ранг, судді, таймер"}
  - {kind: steam, url: "https://store.steampowered.com/app/452570/", note: "режими: кампанія, Daily Cook-Off, Restaurant Rush, Break the Dishes, Survival, Free Play, локальний мультиплеєр"}
  - {kind: official, url: "http://www.battlechefbrigade.com/", note: "сайт гри: персонажі й стихії, лінки на магазини"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1212005853", note: "Loadout Item Guide: увесь посуд (Match 2/3/4, печі), соуси, кістки, отрута, крихкі, експертизи"}
  - {kind: other, url: "https://gameluster.com/battle-chef-brigade-review-pc/", note: "огляд: три в ряд/стовпець → рівень вище, 3 рівні, червоний/зелений/синій = вогонь/земля/вода"}
  - {kind: other, url: "https://www.magicgameworld.com/battle-chef-brigade-cooking-match-guide/", note: "гайд матчів: смаки суддів, правило «нічия за більшістю», тема-інгредієнт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battle+chef+brigade+cooking+gameplay", note: "пошук; геймплей кухні"}
stage: v1
coverage: 45
mechanics: [tile-merge, line-match-clear, combo-multiplier, time-out, ai-opponent, inventory-limit, inventory-items, shop-between-levels, event-points, daily-puzzle, leaderboard, mode-select, achievements-window, simultaneous-versus, game-screen, end-screen, +star-up-merge, +tier-ladder, +wildcard-tile, +recolor-power, +cookware-match-rule, +timed-auto-promote, +fragile-tile-moves, +preference-scoring, +multi-board-placement, +equip-loadout]
proposes: ["+cond:majority(kind, among)", "+window:loadout-select", "+card:cookware-match-rule", "+card:timed-auto-promote", "+card:fragile-tile-moves", "+card:preference-scoring"]
author: opus
date: 2026-11-09
---

# Battle Chef Brigade — інгредієнти стають самоцвітами смаку на сковороді 4×4; три однакові зливаються в рівень вище

## Суть
Гра з двох шарів: бічний брейлер-полювання (Mina чи Thrash бʼє монстрів і збирає частини в сумку) і **кухня**, де кожен інгредієнт кладеться в посудину й розпадається на самоцвіти смаку — вогонь (червоні), вода (сині), земля (зелені). Три однакові самоцвіти в ряд або стовпець зливаються в один самоцвіт **наступного рівня** (1 → 2 → 3); що більше самоцвітів 3-го рівня потрібного смаку, то вища оцінка суддів. Описано лише сітковий шар; бій — контекст, звідки приходять фігури-інгредієнти.

## Поле і час
- Кожна посудина — окрема сітка 4×4 (Wikipedia, Game Informer); CGM пише про «12 клітин» — (?). Одночасно до трьох страв (за кількістю суддів), кожна у своїй посудині.
- Real-time: спільний годинник раунду — і для полювання, і для кухні; з трьома суддями матч близько 10 хв (GamesBeat).
- Суперник-кухар готує паралельно; судді оцінюють обох після подачі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Самоцвіт смаку | tile | колір (вогонь / вода / земля), рівень 1–3 | три однакові (колір + рівень) у лінію → один рівнем вище |
| Райдужний самоцвіт | tile | — | підходить як будь-який колір (wildcard) |
| Кістка | object | — | займає клітину, не дає смаку; рахується як інгредієнт |
| Отрута («поганий» самоцвіт) | hazard | — | псує страву / сусідні самоцвіти (?); знімається дошкою або піччю очищення |
| Крихкий самоцвіт | tile | ходів до руйнування | руйнується після ходу(ів), якщо не захищений |
| Інгредієнт | object | набір самоцвітів (напр. 2 червоні + 0–1 кістка), форма | кладеться в посудину й стає самоцвітами |
| Тема-інгредієнт | object | частини | обовʼязковий у кожній страві матчу |
| Соус | pickup | колір / Promote | перефарбовує самоцвіт (рівень лишається) або підвищує рівень |
| Посудина | zone | правило збігу, авто-ефект | сковороди: Dull / Combo — збіг 3; Stoic's — збіг 4 і подвійне підвищення; Ethereal Fire/Water/Earth — збіг 2 лише свого кольору |
| Піч / повільноварка | zone | швидкість | з часом: Slow Cooker підвищує рівень, Purifying — очищає погані, Hearty — лагодить крихкі, Crystallizer — клонує, Orcish Fire — швидко підвищує лише вогонь |
| Обробна дошка | zone | — | прибирає самоцвіти (і отруту) |
| Суддя | neutral | улюблений смак або пара смаків | оцінює страву |
| Кухар-суперник | enemy | — | подає свої страви тим самим суддям |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, ingredient, cookware)` → ЯКЩО `free(cells)` (?) → ТО `place(player, gems)`, `counter(moves, +1)`; самоцвіти можна обертати перед розміщенням, «як у Puyo Puyo» (Wikipedia).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(gems, color_and_level)` → ТО `merge(gems → gem_level+1)` (рівень 1 ×3 → 2, рівень 2 ×3 → 3).
- КОЛИ `pattern(line(n))` → ЯКЩО `custom: «n = правилу посудини: 2 (Ethereal, лише її колір) / 3 (Dull, Combo) / 4 (Stoic's)»` → ТО `merge(...)`; Stoic's → `set_value(gem, level+2)`.
- КОЛИ `settled` → ЯКЩО `state(gem, rainbow)` → ТО `custom: «рахується будь-яким кольором у збігу»`.
- КОЛИ `after(merge)` → ЯКЩО `timer(<, combo_window)` → ТО `counter(combo, +1)`; Combo Pan → `score(+n)` за комбо; Focus Charm подовжує вікно.
- КОЛИ `input(apply, sauce, gem)` → ТО `transform(gem, sauce_color)` (рівень зберігається); Promote-соус → `set_value(gem, level+1)`.
- КОЛИ `timer(every)` → ЯКЩО `occupied(slow_cooker, gem)` → ТО `set_value(gem, level+1)`; Orcish Fire Oven — те саме швидше й лише для вогню.
- КОЛИ `timer(every)` → ЯКЩО `occupied(purifying_oven, bad_gem)` → ТО `transform(bad_gem, taste_gem)`.
- КОЛИ `timer(every)` → ЯКЩО `occupied(crystallizer, gem)` → ТО `clone(gem)`.
- КОЛИ `input(cut, gem)` → ЯКЩО `occupied(cutting_board, gem)` → ТО `disappear(gem)`.
- КОЛИ `after(place)` → ЯКЩО `state(gem, fragile)` і `custom: «вичерпано ходи крихкого»` → ТО `disappear(gem)`; Wart's Spatula дає +1 хід, Hearty Oven лагодить.
- КОЛИ `input(serve, dish, judge)` → ЯКЩО `has(dish, theme_ingredient)` → ТО `score(n)` за самоцвіти рівня 3; ЯКЩО `custom: «улюблений смак судді — більшість серед самоцвітів рівня 3 (для пари — обидва нарівні найбільші)»` → ТО `score(+bonus)`.
- КОЛИ `counter(round_clock, ==, 0)` → ТО `custom: «раунд закінчено, неподане не рахується»` (?); ЯКЩО `custom: «сума очок суддів ≥ суперника»` → ТО `win`, інакше `lose`.
- КОЛИ `picked(player, ingredient)` → ЯКЩО `custom: «сумка повна»` → ТО `block` (шар полювання; слоти сумки — з предметів).
- Перемога: більше очок за суперника · Поразка: менше · Рахунок: рівні самоцвітів, відповідність смаку суддів, тема-інгредієнт, бонуси експертиз (Feast — 25+ інгредієнтів, Flavor — по одному 3-му рівню кожного кольору, Focus — комбо ×5 тощо).

## Керування і ввід
- Геймпад / клавіатура: вибір інгредієнта з сумки, позиції й повороту в посудині; соуси й дошка — окремі дії (?).
- Брейлер-шар: рух, стрибок, атаки, магія стихії персонажа (Mina — вітер, Thrash — вогонь, берсерк).

## Вікна, меню, HUD
- `main-menu` → кампанія (розділи, матчі, завдання між ними) · `mode-select`: Daily Cook-Off · Restaurant Rush · Break the Dishes · Survival · Free Play · Local Multiplayer · Art Gallery.
- `+window:loadout-select` — вибір посуду, інгредієнтів, експертиз і бойових предметів перед матчем.
- `shop-window` — купівля спорядження за гроші з кампанії.
- `game-screen`: арена полювання + кухня з посудинами, `timer-countdown`, панель суддів з улюбленими смаками (`objective-text`), оцінка страви, що росте під час готування (Game Informer).
- `end-screen` — оцінки суддів, рахунок обох кухарів; `leaderboard` (Daily, Survival); `achievements-window` (Steam).

## Фічі поза полем
- Кампанія за Mina (і розділ за Thrash), завдання між матчами: без таймера «максимум смаку з заданих інгредієнтів», «якомога більше страв», полювання.
- `daily-puzzle` (Daily Cook-Off з онлайн-таблицею), `mode-endless`-подібний Survival, `mode-sandbox` (Free Play), `local-multiplayer` з власними правилами, `unlockables` (галерея), `cloud-save`.

## Варіації й родичі
- Deluxe-оновлення: Ziggy (кухар-некромант) у локальному мультиплеєрі, Survival, Free Play, галерея.
- Родичі в корпусі: [triple-town](triple-town.md) (три однакові → рівень вище), [threes](threes.md) і [2048](2048.md) (злиття рангів), [puzzle-quest](puzzle-quest.md) (match-3 як частина іншої гри), [puyo-puyo](puyo-puyo.md) (поворот фігури перед скиданням).
- **Осі варіацій**: розмір збігу (2 / 3 / 4 — задає посуд) · що дає збіг (зникнення / **злиття в рівень вище**) · мета (очки / **смак-більшість для конкретного судді**) · пасивні клітини (нема / **печі, що з часом підвищують, клонують, очищують**).

## Цікавинки для курсу
- Злиття трійки в самоцвіт наступного рівня з драбиною 1→2→3 — 🌱.
- Правило збігу як параметр посудини (2 / 3 / 4, фільтр кольору) — 📎 (стратегія-обʼєкт).
- Оцінювання за суддями: більшість смаку серед самоцвітів рівня 3, нічия для пари смаків, обовʼязковий інгредієнт — 📎.
- Кілька дошок паралельно з авто-ефектами за таймером (повільноварка, клонувальник) — 🥉.
- Крихкі самоцвіти з лічильником ходів — 🌱.

## Мапа на каталог
- Є: `tile-merge` ↔ злиття трійки; `line-match-clear` ↔ три в ряд/стовпець; `combo-multiplier` ↔ комбо-вікно; `time-out` ↔ годинник раунду; `ai-opponent` ↔ кухар-суперник; `inventory-limit` ↔ слоти сумки; `inventory-items` ↔ предмети спорядження; `shop-between-levels`; `event-points`; `daily-puzzle` ↔ Daily Cook-Off; `leaderboard`; `mode-select`; `achievements-window`; `simultaneous-versus` ↔ локальний мультиплеєр; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+cookware-match-rule` «Правило збігу задає контейнер: розмір 2/3/4, фільтр кольору, сила підвищення» · entities/legality · 📎.
  - `+timed-auto-promote` «Контейнер з часом підвищує / клонує / очищує плитки» · entities/state · 🌱.
  - `+fragile-tile-moves` «Крихка плитка руйнується через N ходів» · entities/state · 🌱.
  - `+preference-scoring` «Оцінка за перевагами суддів: більшість потрібного виду + обовʼязковий інгредієнт» · game-logic/score · 📎.
  - Повтор чужих: `+star-up-merge`, `+tier-ladder`, `+wildcard-tile`, `+recolor-power` (соус), `+multi-board-placement`, `+equip-loadout`.

## Пропозиції до словників
- `+cond:majority(kind, among)` — вид має найбільшу кількість серед заданих (смак судді серед самоцвітів рівня 3; пара — нічия на першому місці).
- `+window:loadout-select` — вибір спорядження перед матчем (уже пропоноване корпусом).
- `+card:cookware-match-rule`, `+card:timed-auto-promote`, `+card:fragile-tile-moves`, `+card:preference-scoring` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Battle Chef Brigade](https://en.wikipedia.org/wiki/Battle_Chef_Brigade) — дві фази, 4×4, самоцвіти смаку, злиття в ранг, обертання «як у Puyo», таймер, обовʼязковий інгредієнт, судді.
- [Steam: Battle Chef Brigade Deluxe](https://store.steampowered.com/app/452570/) — режими, Ziggy, таблиці, досягнення.
- [Steam guide: Loadout Item Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1212005853) — увесь посуд з правилами збігу, печі, соуси, кістки, отрута, райдужні, крихкі, експертизи й бонуси.
- [GameLuster review](https://gameluster.com/battle-chef-brigade-review-pc/) — три по горизонталі/вертикалі → рівень вище, три рівні, кольори = стихії, посуд Match 2 і авто-підвищення.
- [Magic Game World: cooking match guide](https://www.magicgameworld.com/battle-chef-brigade-cooking-match-guide/) — смаки суддів по матчах, правило «пара смаків нарівні найбільші», тема-інгредієнт, Stoic's Pan.
- [Game Informer review](https://gameinformer.com/games/battle_chef_brigade/b/switch/archive/2017/11/20/battle-chef-brigade-review.aspx) — «маленька сітка 4×4», крихкі й отруйні, Match 2-сковорода, повільноварка, оцінка росте під час готування.
- [CGM review](https://www.cgmagonline.com/reviews/battle-chef-brigade-switch-review-cooking-storm/) — рівні 1→2→3, обробна дошка проти отрути, піч працює, поки готуєш інше.
- [GamesBeat review](https://gamesbeat.com/battle-chef-brigade-review-who-knew-monsters-could-be-so-delicious/) — до трьох суддів, ~10 хв матч.

## Непевне
- (?) Як саме інгредієнт входить у посудину: падає згори з гравітацією чи кладеться на вибрані клітини; де зʼявляється злитий самоцвіт.
- (?) 4×4 чи 12 доступних клітин (CGM); що буває, коли посудина повна.
- (?) Що саме робить отрута на полі (псує сусідні? знижує оцінку?) і скільки ходів живе крихкий самоцвіт.
- (?) Пошуковий сніпет приписував опису Deluxe «обертовий квадрат 2×2 на дошці match-3» (стиль Thrash?) — у відкритих сторінках не підтверджено.
- (?) Точна формула очок суддів і чи можна подати страву без тема-інгредієнта (зі штрафом).
