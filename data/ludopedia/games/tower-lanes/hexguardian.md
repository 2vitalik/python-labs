---
title: Hexguardian
slug: hexguardian
aka: []
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: hex
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2024
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2381740/Hexguardian/", best: true, note: "офіційний опис: плитки за вбитих ворогів, замкнена петля гасить портал, вежі/загони/закляття, чудеса, висота дає дальність, погода й стихійні реакції, благословення за босів, режими"}
  - {kind: other, url: "https://rogueliker.com/hexguardian-review/", note: "огляд: щодня фаза будівництва і фаза оборони, замок у центрі, плитка зʼєднується лише з відповідними сусідами, вибір 1 з 3, roguelike-режим"}
  - {kind: other, url: "https://gameluster.com/hexguardian-review-modular-satisfaction/", note: "огляд: камінь з ворогів, дороги й ріки, закриття петлі окремо для піхоти й човнів, раннє завершення за бонус, казарми з радіусом, талант-локи"}
  - {kind: other, url: "https://fingerguns.net/reviews/2024/05/02/hexguardian-review-pc-the-sixth-tower-sense/", note: "огляд: гроші й поклоніння, слоти будівель за ландшафтом, 5 типів мап × easy/hard/crazy, трофеї → дерево талантів"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2381740&count=60&maxlength=4000&enddate=1717200000", note: "патчноути (JSON): +200 % зірок за всі закриті портали, боси на день 7/10, нескінченні рівні, Conduct і Toxical Explosion, талант-лок за кожні 15 талантів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hexguardian+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, enemy-reached-base, spawn-points, round-currency, drop-on-death, hp-damage, status-effects, projectile-shot, explode-area, melee-vs-ranged, speed-per-type, spawner-entity, respawn, in-round-upgrades, level-unlock, difficulty-levels, leaderboard, game-pause, +hex-grid-render, +tile-draw-place, +tile-connectors, +path-by-tiles, +loop-detection, +loop-closes-spawner, +height-range-bonus, +weather-modifiers, +element-reaction, +wall-ignoring-enemy, +target-priority, +rally-point, +hero-in-td, +economy-buildings-income, +adjacency-bonus, +choose-upgrade, +talent-tree, +boss-fight, +fast-forward, +weekly-challenge]
proposes: ["+trigger:tile_placed", "+trigger:status_combo", "+cond:edges_match", "+cond:on_terrain", "+role:tower", "+role:building", "+role:base", "+role:unit", "+ui:range-circle", "+ui:wave-origin-marker", "+window:choice-window", "+window:talent-tree", "+feature:talent-lock", "+feature:mode-weekly", "+card:loop-closes-spawner", "+card:height-range-bonus", "+axis:session"]
author: opus
date: 2026-11-09
---

# Hexguardian — tower defense, де мапу добудовуєш сам гекс-плитками: замкни петлю дороги чи ріки — і портал згасне

## Суть
Посередині мапи стоїть замок, до нього ведуть дороги й ріки, а з їхніх відкритих кінців лізуть вороги. Вбиті вороги дають камінь, за який гравець **прибудовує нові гекс-плитки** (як у Carcassonne): плитка мусить збігтися краями з сусідами, подовжує шлях, відкриває слоти будівель чи скриню — або **замикає петлю**, і тоді портал на цьому шляху гасне. Решта — класичний TD у реальному часі: вежі, казарми з загонами, закляття, економічні будівлі, чудеса, погода й стихійні реакції; між забігами — дерево талантів.

## Поле і час
- Поле — гекс-сітка, що росте від замку в центрі; мапа стоїть на краю урвища, ріки стікають за край світу.
- Кожна плитка має на шести краях дорогу, ріку, обидва чи нічого; ставиться лише поруч із наявною сушею і з відповідністю країв.
- Шари плитки: ландшафт (рівнина, нагірʼя, оаза, лава) + дорога/ріка + слоти будівель + вміст (скриня, камінні брили).
- Нагірні мапи мають висоту: вежа на височині стріляє далі.
- Час — дні: фаза будівництва (поставити плитку, вежу, будівлю) і фаза оборони, коли хвилі йдуть одним або кількома шляхами; звідки й хто прийде — показано наперед. Є пауза й прискорення.
- Рівні нескінченні: після дня 20 вороги різко сильнішають; межу днів підняли з 99 до 150.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Замок | static (`+role:base`) | у центрі мапи | усі дороги й ріки ведуть до нього; падіння — кінець забігу; біля нього моляться за благословення |
| Гекс-плитка | tile | краї: дорога / ріка / обидва / порожньо; вміст | ставиться за камінь поруч із сушею; краї мусять збігатися |
| Дорога | terrain | — | шлях піхоти від порталу до замку |
| Ріка | terrain | — | шлях човнів; герой її не перетинає |
| Портал | spawner | на відкритому шляху | породжує хвилі; гасне, коли петлю шляху замкнено |
| Нагірʼя | terrain | висота | вежа на ньому має більшу дальність |
| Слот будівлі | zone | тип ландшафту | вежі й будівлі — лише тут; слотів мало |
| Скриня | pickup | золото | зʼявляється на покладеній плитці |
| Камінна брила | terrain | — | підсилює сусідню каменярню |
| Лава (Lava Land) | hazard | — | вогняна шкода ворогам поруч; виверження прискорюються з кожною новою плиткою |
| Вежі: стрілецька, бомбова/гармата, вогняна, крижана, водяна, громова, світла, темна, стихійна | static (`+role:tower`) | дальність, шкода, темп, апгрейди | стріляє по ворогах у радіусі; пріоритет цілі в три шари |
| Вежа колод (Rolling Log) | static (`+role:tower`) | розмір колоди | колода після влучання котиться дорогою до порталу |
| Вежа сюрикенів | static (`+role:tower`) | — | бʼє всіх у радіусі; апгрейд — сюрикени діляться й наводяться |
| Казарма / стрільбище | spawner | радіус дії, точка збору | випускає загін; полеглі відроджуються за час |
| Загони: мечники, лучники, кінні лучники, маги, жерці, піромант, катапульта, гармата | ally (`+role:unit`) | HP, атака, час відродження | ближні зупиняють ворога на дорозі; дальні бʼють здалеку; маги накладають стани; жерці лікують |
| Герой з Вівтаря (Lyra, Ragnar, Isolde, Kael) | ally | 1 на гру; базове вміння + 3 вивчені | ходить будь-куди, крім як через ріки; атака росте щодня |
| Будинок, рибальська хата, ринок, вітряк | static (`+role:building`) | дохід | монети/золото |
| Обсерваторія | static (`+role:building`) | дохід | зірки |
| Каменярня | static (`+role:building`) | дохід × сусідні брили | камінь на нові плитки |
| Будівлі поклоніння | static (`+role:building`) | дохід | очки поклоніння на благословення |
| Чудо: Stonehenge, Oracle, Taj Mahal, Mausoleum | static (`+role:building`) | велика будівля | Stonehenge — шанс каменю за смерть ворога поруч; Oracle — блискавка навколо за кожне благословення |
| Піхота (звичайна, броньована, зі щитом) | enemy | гурт | іде дорогою щільною групою |
| Човни: галера, вітрильник | enemy | швидкі, розкидані | пливуть рікою |
| Дирижабль | enemy | летить | іде до замку, ігноруючи дороги |
| Бос (каракка тощо) | boss | лють | приходить у визначений день; за смерть — монети, благословення |
| Закляття | object | шкода / сповільнення | гравець кидає в ціль |
| Погода: дощ, піщана буря | zone | — | дощ взаємодіє зі стихійними вежами й закляттями; буря шкодить усім, союзникам — наполовину |
| Монети · камінь · поклоніння · зірки · трофеї | resource | — | будівлі · плитки · благословення · бонус забігу · таланти між забігами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `died(enemy)` → ЯКЩО `prob(p)` → ТО `counter(stone, +1)`.
- КОЛИ `input(place_tile, cell)` → ЯКЩО `custom: «клітина межує з сушею»` and `custom: «краї збігаються з сусідами: дорога до дороги, ріка до ріки»` and `counter(stone, >=, cost)` → ТО `place(player, tile)`, `counter(stone, -cost)`; інакше `block`.
- КОЛИ `custom: «покладено плитку зі скринею»` → ТО `currency(+gold)`.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля дороги замикає шлях порталу»` → ТО `set_state(portal, closed)` — піхота звідти більше не йде.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля ріки»` → ТО `set_state(portal, closed)` для човнів; летючі не залежать від шляхів.
- КОЛИ `custom: «закрито всі портали»` → ТО `custom: «забіг завершується достроково»`, `custom: «+200 % бонусу зірок»`, `win`.
- КОЛИ `phase_start(defense)` → ТО `spawn_at(wave, portal)`: піхота — на дорогу, човни — на ріку, дирижаблі — `custom: «прямо до замку»`.
- КОЛИ `tick` → ТО `move(enemy, path_to_castle)`.
- КОЛИ `input(build, slot)` → ЯКЩО `custom: «ландшафт слота дозволяє будівлю»` and `counter(gold, >=, cost)` → ТО `place(player, building)`, `currency(-cost)`.
- КОЛИ `in_range(tower, enemy, range)` → ЯКЩО `custom: «перезарядка минула»` → ТО `damage(enemy, atk)`; ціль — за пріоритетом.
- КОЛИ `spawned(tower)` → ЯКЩО `custom: «слот на нагірʼї»` → ТО `custom: «+дальність»`.
- КОЛИ `custom: «колода влучила»` → ТО `custom: «котиться дорогою до порталу, бʼючи всіх на шляху»`.
- КОЛИ `timer(revive)` → ЯКЩО `count(squad, <, max)` → ТО `respawn(unit, barracks)`.
- КОЛИ `contact(melee_unit, enemy)` → ТО `block` (ворог зупиняється), обидва `damage`.
- КОЛИ `input(rally, barracks, cell)` → ЯКЩО `custom: «клітина в радіусі казарми»` → ТО `move(squad, cell)`.
- КОЛИ `input(move, hero, cell)` → ЯКЩО `custom: «шлях не перетинає ріку»` → ТО `move(hero, cell)`.
- КОЛИ `input(cast, spell, target)` → ТО `damage(area, n)` або `speed(enemies, -n)`.
- КОЛИ `custom: «на ворога діють дві стихії»` → ТО `custom: «стихійна реакція»`: Conduct — `stun(enemies, n)` ланцюгом на кілька цілей; Toxical Explosion — `explode(area, n)`; Burning — `set_state(enemy, burning)`.
- КОЛИ `custom: «ворог у стані burning отримує шкоду»` → ТО `damage(enemy, extra)`.
- КОЛИ `custom: «громова шкода по летючому»` → ТО `damage(enemy, ×2)`.
- КОЛИ `custom: «піщана буря»` → ТО `damage(all, n)`; союзникам — половина.
- КОЛИ `phase_start(day)` → ТО `currency(+income)` від будинків і хат; `counter(stone, +n)` від каменярні, ЯКЩО `adjacent_count(quarry, stone_block, >=, 1)` — більше.
- КОЛИ `died(enemy)` → ЯКЩО `in_range(stonehenge, enemy, r)` and `prob(p)` → ТО `counter(stone, +1)`.
- КОЛИ `custom: «покладено нову плитку на Lava Land»` → ТО `custom: «тектонічний рух прискорює всі виверження»`; КОЛИ `in_range(lava, enemy, r)` → ТО `damage(enemy, fire)`.
- КОЛИ `phase_start(day)` → ТО `choose(3: вежа | будівля | закляття | бонус)`.
- КОЛИ `schedule(day 7; Hard — day 10)` → ТО `spawn_at(boss, portal)`; КОЛИ `died(boss)` → ТО `currency(+coins)`, `choose(blessing)`.
- КОЛИ `input(pray, castle)` → ЯКЩО `counter(worship, >=, cost)` → ТО `choose(blessing)` — тимчасовий баф золота, дальності, шкоди чи закляття.
- КОЛИ `custom: «отримано благословення»` → ЯКЩО `count(oracle, >=, 1)` → ТО `damage(enemies_near_oracle, n)`.
- КОЛИ `counter(day, >, 20)` → ТО `custom: «HP і броня ворогів ростуть швидше»`.
- КОЛИ `reach(enemy, castle)` → ТО `custom: «замок падає»` (?), `lose`.
- КОЛИ `game_over` → ТО `custom: «трофеї за кожен прожитий день»`.
- Перемога: закрити всі портали (дострокове завершення) або протриматись якомога довше · Поразка: замок упав · Рахунок: прожиті дні, зірки, трофеї.

## Керування і ввід
- Миша: вибрати плитку, навести на вільну клітину біля суші, підтвердити; вибрати слот і будівлю з меню; кинути закляття в точку.
- Казарма: перетягнути точку збору в межах радіусу; героя — ведеш кліком по мапі.
- Пріоритет цілі вежі — три шари (напр., стрілецька першою бʼє летючих).
- Пауза, прискорення спокійних відрізків, вибір карти на початку дня; перепризначення клавіш.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Standard, Weekly Challenge, Roguelike Challenge; `level-select` — біоми (5 типів мап, серед них Rainforest, Rocky, Lava Land) зі складністю easy / hard / crazy, далі Inferno.
- `game-screen`: гекс-мапа в ізометрії, `coins`, лічильники каменю, поклоніння й зірок, `+ui:wave-origin-marker` (звідки йде хвиля), `wave-counter` (день), меню будівель, `ability-buttons` закляття, `+ui:range-circle`, `speed-slider` / `fast-forward`, `pause-button`.
- `+window:choice-window` — 1 з 3 на початку дня; `+window:talent-tree` — велике дерево талантів між забігами з лок-слотами.
- `leaderboard` — тижнева таблиця Weekly Challenge; `end-screen` — прожиті дні й трофеї; `settings-window` — клавіші.

## Фічі поза полем
- `meta-progression`: трофеї за прожиті дні → дерево талантів (вежі, загони, будівлі, закляття, пасиви, чудеса); скидання дерева повертає 80 %.
- `+feature:talent-lock` — кожні 15 відкритих талантів дають лок, що прибирає талант з пулу вибору в забігу.
- `level-unlock`: пройдені мапи відкривають нові мапи й складності; roguelike-режим відкривається після hard на скелястій мапі.
- `+feature:mode-weekly` — тижневий виклик з обмеженими ресурсами, обраними перками, загонами й одним благословенням; `leaderboard-online`.
- `autosave` з резервною копією сейвів, `achievements`, `remap-controls`, 10 мов.

## Варіації й родичі
- Оновлення: Lava Land (виверження, тектоніка), Heroes (Вівтар і 4 героя), нові вежі (колоди, сюрикени), каменярня й камінь як ціна плитки.
- Родичі в корпусі: [isle-of-arrows](isle-of-arrows.md) (плитки-острови з дорогою, TD покроково), [rogue-tower](rogue-tower.md) (шлях росте сам), [thronefall](thronefall.md) (день/ніч, економічні будівлі), [emberward](emberward.md); поза сімʼєю — [carcassonne](../board-digital/carcassonne.md) (збіг країв, замкнена дорога) і [dorfromantik](../build-sim/dorfromantik.md) (гекс-плитки з ріками).
- **Осі варіацій**: хто будує шлях — дизайнер / гравець плитками / лабіринт з веж · закрити спавн — неможливо / замкнути петлю · висота — нема / дальність / шкода.

## Цікавинки для курсу
- Замкнена петля гасить портал: граф доріг на гекс-сітці, пошук відкритих кінців і циклів — 🥉.
- Збіг шести країв плитки з сусідами (дорога/ріка/обидва) — 📎.
- Окремі графи для піхоти (дороги), човнів (ріки) і летючих (прямо) — 🥉.
- Висота клітини дає вежі дальність — 🌱.
- Стихійні реакції: два стани на цілі → третій ефект (ланцюговий стан, вибух) — 🥉.
- Казарма з радіусом і точкою збору, ближні загони блокують дорогу — 🥉.
- Вибір 1 з 3 щодня + лок талантів, що прибирає варіант з пулу — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ вежі в слотах · `tower-range` · `enemy-waves`, `spawn-points` ↔ портали · `enemy-reached-base` ↔ замок · `round-currency` ↔ монети/камінь · `drop-on-death` ↔ камінь з ворога · `hp-damage` · `status-effects` ↔ burning, stun · `projectile-shot` · `explode-area` ↔ Toxical Explosion · `melee-vs-ranged` ↔ загони · `speed-per-type` ↔ піхота/човни/летючі · `spawner-entity` ↔ казарма · `respawn` ↔ відродження загону · `in-round-upgrades` · `level-unlock` · `difficulty-levels` · `leaderboard` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+tile-draw-place`, `+path-by-tiles`, `+hex-grid-render`, `+tile-connectors`, `+loop-detection`, `+wall-ignoring-enemy`, `+target-priority`, `+hero-in-td`, `+economy-buildings-income`, `+adjacency-bonus`, `+choose-upgrade`, `+talent-tree`, `+boss-fight`, `+fast-forward`, `+weather-modifiers` — уже в корпусі.
  - `+loop-closes-spawner` «Замкнена петля шляху гасить спавн» · game-logic/waves · 🥉.
  - `+height-range-bonus` «Висота клітини збільшує дальність вежі» · entities/combat · 🌱.
  - `+element-reaction` «Два стани на цілі дають третій ефект» · entities/state · 🥉.
  - `+rally-point` «Точка збору загону в радіусі будівлі» · entities/move · 📎.
  - `+weekly-challenge` «Тижневий виклик з однаковими умовами й таблицею» · levels/bank · 📎.

## Пропозиції до словників
- `+trigger:tile_placed` — гравець поклав плитку (Hexguardian, Isle of Arrows, Carcassonne).
- `+trigger:status_combo` — на цілі зійшлись два стани/стихії (реакції).
- `+cond:edges_match` — краї плитки збігаються з сусідніми (дорога до дороги).
- `+cond:on_terrain` — сутність стоїть на клітині типу (нагірʼя → дальність); зараз — `custom`.
- `+role:tower` · `+role:building` · `+role:base` · `+role:unit` — повтори з корпусу.
- `+ui:range-circle` — повтор; `+ui:wave-origin-marker` — позначка, з якого порталу й ким піде хвиля.
- `+window:choice-window` — повтор; `+window:talent-tree` — дерево талантів між забігами.
- `+feature:talent-lock` — прибрати варіант з пулу випадкових виборів; `+feature:mode-weekly` — тижневий виклик.
- `+card:loop-closes-spawner`, `+card:height-range-bonus`; `+axis:session` — `run` / `endless`.

## Джерела
- ⭐ [Steam: Hexguardian](https://store.steampowered.com/app/2381740/Hexguardian/) — офіційний опис: плитки за ворогів, петля гасить портал, вежі, загони, закляття, суша/море/повітря, чудеса й ринки, висота, погода й реакції, благословення за босів, режими й дерево талантів; Split Second Games / Yogscast Games, 2 травня 2024.
- [Rogueliker: огляд](https://rogueliker.com/hexguardian-review/) — фаза будівництва й оборони, замок у центрі, плитка зʼєднується лише з певними сусідами, скрині, вибір 1 з 3, швидкість і пауза, roguelike-режим після hard.
- [Gameluster: огляд](https://gameluster.com/hexguardian-review-modular-satisfaction/) — камінь з кілів, дороги/ріки, петля по типу ворога, раннє завершення за бонус, поведінка піхоти/човнів/летючих, казарми з радіусом, талант-локи.
- [Finger Guns: огляд](https://fingerguns.net/reviews/2024/05/02/hexguardian-review-pc-the-sixth-tower-sense/) — урвище й ріки за край, обмежені слоти за ландшафтом, гроші й поклоніння, 5 мап × easy/hard/crazy, трофеї.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2381740&count=60&maxlength=4000&enddate=1717200000) — патчі v0.54–v1.21 і оновлення Lava Land та Heroes.
- YouTube: пошук «Hexguardian gameplay».

## Непевне
- (?) Чи можна обертати плитку перед установкою і чи гравець обирає з кількох плиток — джерела не кажуть.
- (?) Чи має замок HP, чи падає від першого ворога — «втратити замок = кінець спроби», без чисел.
- (?) Де саме стоять портали (на кожному відкритому кінці шляху чи фіксовано) — з описів «закрий петлю → портал згасне».
- (?) Звʼязок зірок і трофеїв: зірки — бонус забігу, трофеї — валюта талантів; як одне переходить в інше, не перевірено.
- (?) Survival як окремий режим чи синонім нескінченного Standard — на Steam описано обидва.
- (?) Повний список стихійних реакцій і точна роль дощу.
- (?) Назва складності Inferno відносно easy/hard/crazy.
