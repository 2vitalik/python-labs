---
title: The Miner Was Replaced
slug: the-miner-was-replaced
aka: [TMWR, The Farmer Was Replaced — Underground DLC]
family: program-robots
also: [dig-gravity, hidden-deduction]
klass: avatar
axes:
  field: 3d
  time: programmed
  opponent: none
  info: hidden
  random: setup
  goal: collect
year: 2026
platforms: [PC (Windows, macOS), iOS, Android]
links:
  - {kind: other, url: "https://github.com/ChristopheCVB/TheFarmerWasReplacedDocs", best: true, note: "витяг внутрішньоігрової документації, зокрема Underground/DLC: гайди Mining, Coal, Iron, Quartz, Mushroom, Dynamite, Pyramids, Treasure Map, довідник функцій dig / push / jump / hover / prospect_*"}
  - {kind: other, url: "https://raw.githubusercontent.com/ChristopheCVB/TheFarmerWasReplacedDocs/HEAD/guides/unlocks/dynamite.md", note: "гайд «Dynamite»: сапер на шарі сажі, measure() 0–8, перший удар завжди пустий, нагорода n²"}
  - {kind: other, url: "https://raw.githubusercontent.com/ChristopheCVB/TheFarmerWasReplacedDocs/HEAD/guides/unlocks/mining.md", note: "гайд «Mining»: dig(), твердість, обвали за стабільністю"}
  - {kind: steam, url: "https://store.steampowered.com/app/4521700/The_Miner_Was_Replaced/", note: "DLC: 8 нових підземних ресурсів, руїни без пошкоджень, сортування грибів, сапер; 9 скриншотів з кодом"}
  - {kind: other, url: "https://www.metaroot.ch/press-kit/the-miner-was-replaced", note: "прес-кіт: дата 02.11.2026, Windows/Mac, Unity"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847920302248386", note: "реліз DLC: нова гілка дерева, рис на глині, мобільна версія з DLC, патч документації"}
  - {kind: other, url: "https://github.com/Semy0nBu/the-farmer-was-replaced", note: "скрипти гравця для DLC: coal, iron, quartz, mushrooms, dynamite, pyramids, treasure_maps, rice, bamboo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Miner+Was+Replaced+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, wrap-edges, dig-terrain, height-levels, gravity-fall, push-object, fill-hole, neighbor-count-clue, chain-detonation, explode-area, inventory-items, round-currency, in-round-upgrades, collect-quota, leaderboard, code-editor-window, step-execution, sensor-predicates, user-procedures, +real-language-code, +tech-tree-unlock-language, +voxel-column-world, +hardness-dig-time, +stability-cave-in, +ore-veins, +prospect-direction, +prospect-distance-trilateration, +stack-match-harvest, +minesweeper-layer, +structure-restoration, +path-string-follow, +hover-height, +jump-to-feature, +tick-cost-model, +multi-drone-spawn, +simulation-leaderboard-run]
proposes: ["+effect:dig", "+effect:cave_in(cells)", "+effect:hover(h)", "+effect:jump(feature)", "+effect:prospect(ore)", "+cond:hardness(cell, op, n)", "+cond:stability(cell, op, n)", "+cond:height_diff", "+trigger:stratum_cleared", "+window:research-tree", "+axis:field=voxel-columns"]
author: opus
date: 2026-11-09
---

# The Miner Was Replaced — DLC до The Farmer Was Replaced: дрон копає вглиб тривимірного світу, а ти пишеш код для обвалів, жил, сапера й пірамід

## Суть
Платне доповнення (02.11.2026) до `the-farmer-was-replaced`: та сама Python-подібна мова й тех-дерево, але ферма стає верхом **воксельного куба** — дрон отримує бур і `dig()` знімає блок під собою. Нові задачі — алгоритмічні: обвали за стабільністю ґрунту (копай так, щоб не втратити руду), пласти вугілля й вертикальні жили заліза, пошук кварцу за евклідовою відстанню (трилатерація), грибні колонії, які треба **зіштовхувати** однаковими в стоси, **сапер** на шарі сажі під динамітом, відновлення ерозованих пірамід піском, карта скарбів як рядок напрямків. Гра — окрема вітка дерева розблокувань і окремі лідерборди.

## Поле і час
- Поле — квадрат n×n з базової гри (розширюється Expand), тепер з глибиною: кожна клітина — **колонка блоків**; `get_pos_z()` = 0 на поверхні й зменшується з кожним `dig()`. Рух `move` — по горизонталі над верхом колонок, через край — на протилежний бік (тор, як у базовій грі (?)).
- Шари згори вниз (за гайдами): поверхня (Grassland/Soil) → Dirt з тонкими горизонтальними пластами вугілля → тонкий пласт Clay (рис) → Rock з жилами заліза → нижня частина Rock і тверда Dirt (кварц, скамʼянілі гарбузи 3×3×3 / 5×5×5); окремо трапляються пласти Mushroom, Dynamite + Soot, Basalt + Treasure_Map, Perlite/Loam, піщані піраміди на вапняку; Bedrock (?) — дно.
- Висота дрона над верхнім блоком — `hover(h)`, 0–18, за замовчуванням 1; `dig`, `harvest`, `plant` повертають висоту 1.
- Час `programmed`: тіки базової гри (дія 200 тіків, сенсор 1 тік); `dig()` триває `hardness / drill strength` секунд і **не** прискорюється апгрейдами швидкості чи Power.
- Видимість: світ видно ззовні, але руду в товщі не видно — дрон дізнається тип ґрунту під собою й у 4 сусідах через `get_ground_type(dir)`, а далекі жили — через `prospect_*`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дрон з буром | player | x, y, z, hover, капелюх (Mining Hat, Explosive Drill) | виконує код; `dig`, `push`, `place`, `hover`, `jump`; з Megafarm — кілька дронів |
| Dirt / Rock / Limestone / Grassland | terrain | твердість, стабільність | копається в предмет Block; твердість росте з глибиною |
| Clay | terrain | товщина пласта | на ньому `plant(Entities.Rice)`; не руйнується сусіднім копанням |
| Rice_Terrace → Dry_Rice_Terrace | terrain | — | після посадки рису; дозрілий рис висушує террасу, далі — копати до свіжої глини |
| Coal | resource | 1-блоковий горизонтальний пласт, звʼязки й по діагоналі | дає вугілля лише при прямому копанні |
| Iron | resource | жила, лише ортогонально звʼязна, йде й по вертикалі | шукається `prospect_iron()` |
| Quartz | resource | вертикальні голчасті жили | шукається `prospect_quartz()` (евклідова відстань) |
| Mushroom (6 типів, `measure()` 0–5) | object | тип | штовхається `push(dir)`; два однакові один на одному → автозбір |
| Dynamite (живий / пустий) | hazard | live / dud | копання в живий — вибух обох пластів; пустий — трохи динаміту |
| Soot | mark | `measure()` 0–8 | рахує живі заряди у 8 сусідах на шарі вище; після розвʼязання — `None` |
| Sand | object | — | осипається без опори: лише на вапняку або на 3×3 піску |
| Pyramid (Sand на Limestone) | zone | непарна сторона 5×5 … | відновлена → зникає, у центрі виростає великий соняшник з Power |
| Basalt | mark | `measure()` → (x, y) | вказує, де під ним Treasure_Map |
| Treasure_Map | mark | `measure()` → рядок N/E/S/W/D | шлях до скарбу |
| Treasure_Path / Treasure_Goal | terrain | — | зійдеш зі шляху — шлях зламано; на цілі зʼявляється скриня |
| Underground_Treasure | pickup | золото ∝ довжині шляху | `harvest()` |
| Petrified_Pumpkin | resource | блок 3×3×3 / 5×5×5 | копається в гарбузи |
| Perlite / Loam | terrain | — | ×2 урожай: Perlite — кактуси, бамбук, кущі, дерева; Loam — морква, соняшники; садити без `till()` |
| Бамбук | resource | росте 1 блок/с; плід кожні кілька блоків | плід зупиняє ріст — зірвати `hover` + `move`; урожай = n² зрізаних секцій |
| Block_Red / Green / Blue | static | — | декоративні блоки для `place` (Colorful Blocks) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(dig())` → ТО `custom: «блок під дроном знято за hardness / drill_strength с»`, `give(drone, item)`, дрон опускається: `counter(z, −1)`.
- КОЛИ `after(dig)` → ТО `custom: «4 сусідні блоки руйнуються завжди (крім Clay, Iron, Quartz і спецблоків)»` — без ресурсу.
- КОЛИ `after(dig)` → ЯКЩО `custom: «сусід нижчий на ≥ stability + 1»` → ТО `custom: «блок обвалюється разом з усім над ним, без ресурсу»` (каскад).
- КОЛИ `exec(get_hardness(dir))` / `exec(get_stability(dir))` / `exec(get_ground_type(dir))` → ТО `custom: «1 тік, повертає значення під дроном або в сусіді»`.
- КОЛИ `exec(prospect_iron())` → ЯКЩО `has(drone, coal)` → ТО `take(drone, coal)`, повертає напрям кроку до найближчої руди (відстань = кроки + копання); інакше `None`.
- КОЛИ `exec(prospect_quartz())` → ЯКЩО `has(drone, iron)` → ТО `take(drone, iron)`, повертає евклідову 3D-відстань до найближчого кварцу; інакше `None`.
- КОЛИ `exec(push(dir))` → ЯКЩО `cell(under, mushroom)` і `free(target)` і `custom: «не вгору»` → ТО `push(mushroom)`, 200 тіків; інакше 1 тік і False.
- КОЛИ `after(push)` → ЯКЩО `custom: «під блоком порожньо»` → ТО `fall(mushroom)`.
- КОЛИ `custom: «гриб ліг на гриб того ж типу»` → ЯКЩО `same(a, b, type)` → ТО `custom: «обидва блоки збираються автоматично»`, `give(drone, mushroom)`.
- КОЛИ `exec(place(ground))` → ЯКЩО `custom: «блок без спецфункції (Dirt, Rock, Sand…)»` → ТО `place(drone, block)` під дроном; інакше False.
- КОЛИ `exec(place(Sand))` → ЯКЩО `not supported(sand)` (не на вапняку й не на 3×3 піску) → ТО `fall(sand)` / обвал.
- КОЛИ `custom: «піраміда відновлена: квадрат вапняку непарної сторони, над ним шари n×n, n−2, … , 1×1»` → ТО `disappear(pyramid)`, `spawn_at(big_sunflower, center)`; `harvest` → Power (більша піраміда — більше).
- КОЛИ `exec(dig())` на Dynamite → ЯКЩО `first_time` → ТО `custom: «завжди пустий»`.
- КОЛИ `exec(dig())` на Dynamite → ЯКЩО `state(block, live)` → ТО `explode(area)` — обидва пласти (динаміт і сажа) зникають; інакше `give(drone, dynamite)` і відкривається Soot з числом.
- КОЛИ `exec(measure())` на Soot → ТО `custom: «кількість живих зарядів у 8 сусідах (0–8)»` — `adjacent_count(cell, live, =, n)`.
- КОЛИ `all_gone(dud)` → ТО `custom: «динамітний пласт зникає»`, `give(drone, dynamite × (повністю відкриті живі)²)`; `measure()` на сажі → `None`.
- КОЛИ `exec(use_item(Dynamite))` → ТО `explode(area)` під дроном; з капелюхом Explosive Drill `dig()` витрачає динаміт і **збирає** все в радіусі вибуху.
- КОЛИ `exec(measure())` на Basalt → ТО повертає (x, y) карти; на Treasure_Map → `custom: «рядок шляху N/E/S/W/D»`.
- КОЛИ `leave(drone, treasure_path)` → ЯКЩО `not cell(dest, treasure_path)` → ТО `custom: «шлях зламано, скарб втрачено»`.
- КОЛИ `reach(drone, treasure_goal)` → ЯКЩО `custom: «не сходив зі шляху»` → ТО `spawn_at(underground_treasure, goal)`; `harvest` → золото ∝ довжині шляху.
- КОЛИ `exec(plant(Rice))` → ЯКЩО `cell(under, clay)` → ТО `set_cell(under, rice_terrace)`; КОЛИ рис дозрів → ТО `set_cell(under, dry_rice_terrace)`.
- КОЛИ `exec(jump(Unlocks.X))` → ЯКЩО `first_time` (у цьому запуску) → ТО `teleport(drone, «≤ 3 блоки над ресурсом X»)`, 200 тіків; повторно — помилка, `crash`.
- КОЛИ `exec(clear())` → ТО `custom: «повернення на поверхню, світ відновлено й перегенеровано»`, дрон у (0, 0).
- КОЛИ `exec(hover(h))` → ЯКЩО `custom: «0 ≤ h ≤ 18 і не вниз у тверде»` → ТО `custom: «дрон висить на висоті h»`; `move` на висоті плоду бамбука зриває плід.
- Мета: ресурси на розблокування підземної гілки й апгрейди бура (Drill, Ore Boost…); лідерборди — `leaderboard_run(...)` з фіксованим стартом і умовою успіху (напр. `num_items(Items.Quartz) >= 20000`), мінімум 2 години симуляції.

## Керування і ввід
- Ввід — текст коду у вікнах-редакторах базової гри (Python-підмножина: функції, списки, словники, множини, кортежі, `import`); ▶ / ⏸ / ■ і покрокове виконання; `print` / `quick_print`.
- Нові функції DLC: `dig`, `push`, `can_push`, `place`, `hover`, `get_hover`, `jump`, `get_pos_z`, `get_hardness`, `get_stability`, `prospect_iron`, `prospect_quartz`; `get_ground_type` і `measure` приймають напрям.
- Наведення миші на блок — тултіп з назвою, стабільністю й твердістю; Alt — панорама / зум крізь вікна; на мобільних — власна клавіатура для коду.

## Вікна, меню, HUD
- `game-screen`: воксельний куб світу (камера обертається навколо (?)), плаваючі вікна коду (`code-editor` з підсвіткою рядка), `inventory-bar` угорі (сіно, динаміт, дерево, морква, рис, гарбузи, скарби, бамбук, гриби, блоки, вугілля, залізо, кварц…), кнопки «+», «i», «⌃» праворуч угорі.
- `+window:research-tree` — дерево розблокувань з підземною гілкою: Mining (7/8 рівнів), Coal, Iron, Quartz, Mushroom, Dynamite, Pyramid, Rice, Bamboo, `jump()`, `get_hardness()`, Red_Block…; вузли з рівнем «n / m».
- `help-window` / `codex-window` — документація з інтерактивними прикладами коду (з патчем DLC), кнопкою Back, пошуком і поясненням, яке дослідження відкриває сторінку.
- `leaderboard` — підземні категорії: Fastest Underground Reset, Ores, Treasure Map, Rice, Bamboo, Dynamite, Mushrooms, Pyramids і *_Single (один дрон, 8×8).
- Тултіп предмета: зібрано за останню хвилину й найкращий показник за хвилину.

## Фічі поза полем
- `tech-tree`: нова вітка (початок — Mining за 20 моркв, апгрейди бура за Block, Rice, Coal, Bamboo, Iron, Quartz, Mushroom).
- `leaderboard-online` через `leaderboard_run(leaderboard, filename, speedup)` — симуляція з фіксованими умовами, середнє за ≥ 2 години симульованого часу; категорія «найшвидший підземний ресет».
- `simulate()` для тестів, Megafarm (кілька дронів; скарб шукає лише той дрон, що розкопав карту).
- `achievements`, `cloud-save`; мобільна версія TFWR (Android / iOS) містить DLC.
- Нові капелюхи (Mining Hat, Explosive Drill та ін.) — `unlockables`.

## Варіації й родичі
- Базова гра: `the-farmer-was-replaced` (той самий рушій, мова, дрон, тіки) — тут описано лише підземний шар; цей DLC у базовому файлі не згаданий.
- Родичі з `dig-gravity`: `boulder-dash`, `dig-dug`, `mr-driller` (копання і обвали), `motherload`, `dome-keeper`; з `hidden-deduction`: `minesweeper` (тут — сапер, який розвʼязує програма).
- Осі варіацій: **як шукати руду** (навмання / напрям до найближчої / відстань і трилатерація); **що руйнує копання** (лише ціль / сусідів / каскад за стабільністю); **хто розвʼязує пазл** (людина / програма).

## Цікавинки для курсу
- Обвал за стабільністю: каскадна перевірка різниці висот сусідніх колонок — 🥈.
- Сапер, який розвʼязує програма: читання чисел сажі, вивід безпечних клітин, нагорода n² — 🥇.
- Пошук кварцу за евклідовою відстанню з ціною за кожен запит (бінарний пошук / трилатерація) — 👑.
- Грибне сортування штовханням: два однакові один на одному → збір; дірки засипати `place` — 🥈.
- Відновлення піраміди піском з правилом опори «вапняк або 3×3» — 🥉.
- Карта скарбу як рядок `NNEDS…` і заборона сходити зі шляху — 📎.
- Звʼязність жил (вугілля — 8-сусідство, залізо — 4-сусідство) і flood fill для видобутку — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `wrap-edges` · `dig-terrain` · `height-levels` · `gravity-fall` (пісок, гриби) · `push-object` (гриби) · `fill-hole` (`place` у дірку) · `neighbor-count-clue` (сажа) · `chain-detonation` / `explode-area` (динаміт) · `inventory-items` · `round-currency` · `in-round-upgrades` · `collect-quota` · `leaderboard` · `code-editor-window` · `step-execution` · `sensor-predicates` · `user-procedures`.
- **Нема** → пропозиції карток:
  - `+voxel-column-world` «Сітка колонок з глибиною z» · entities/legality · 🥈.
  - `+hardness-dig-time` «Час копання = твердість / сила бура» · entities/state · 📎.
  - `+stability-cave-in` «Каскадний обвал за різницею висот» · entities/interact · 🥈.
  - `+ore-veins` «Жили й пласти з різною звʼязністю» · levels/generation · 🥉.
  - `+prospect-direction` «Сенсор: напрям до найближчого ресурсу за ціну» · game-logic/program · 📎.
  - `+prospect-distance-trilateration` «Сенсор відстані, пошук перетином сфер» · game-logic/program · 👑.
  - `+stack-match-harvest` «Два однакові блоки один на одному збираються» · entities/legality · 📎.
  - `+minesweeper-layer` «Шар-сапер: числа під шаром зарядів» · game-logic/constraints · 🥈.
  - `+structure-restoration` «Відновити ерозовану споруду до шаблону» · game-logic/win · 🥉.
  - `+path-string-follow` «Пройти шлях за рядком напрямків, не сходячи» · game-logic/win · 📎.
  - `+hover-height` «Висота польоту над колонкою» · entities/move · 🌱.
  - `+jump-to-feature` «Один стрибок за запуск до потрібного ресурсу» · game-logic/program · 🌱.
  - `+tech-tree-unlock-language`, `+tick-cost-model`, `+multi-drone-spawn`, `+real-language-code` — спільні з базовою грою.
  - `+simulation-leaderboard-run` «Рекорд = симуляція з фіксованим стартом, середнє за 2 години» · interface/results · 🥈.

## Пропозиції до словників
- `+effect:dig` — зняти блок під собою (є й в інших файлах корпусу).
- `+effect:cave_in(cells)` — обвал колонок без отримання ресурсу.
- `+effect:hover(h)` — змінити висоту польоту.
- `+effect:jump(feature)` — стрибнути до найближчого ресурсу типу.
- `+effect:prospect(ore)` — сенсор за ціну ресурсу (напрям або відстань).
- `+cond:hardness(cell, op, n)` / `+cond:stability(cell, op, n)` — властивості блоку.
- `+cond:height_diff` — різниця висот сусідніх колонок (обвал, піраміда).
- `+trigger:stratum_cleared` — пласт розвʼязано / зник (динаміт, піраміда).
- `+window:research-tree` — дерево розблокувань з рівнями вузлів (як у базовій грі).
- `+axis:field=voxel-columns` — квадратна сітка колонок з глибиною (між `square` і `3d`).

## Джерела
- ⭐ [TheFarmerWasReplacedDocs (GitHub)](https://github.com/ChristopheCVB/TheFarmerWasReplacedDocs) — витяг документації гри з DLC: гайди [Mining](https://raw.githubusercontent.com/ChristopheCVB/TheFarmerWasReplacedDocs/HEAD/guides/unlocks/mining.md), [Dynamite](https://raw.githubusercontent.com/ChristopheCVB/TheFarmerWasReplacedDocs/HEAD/guides/unlocks/dynamite.md), Coal, Iron, Prospecting, Quartz, Mushroom, Pyramids, Treasure Map, Rice, Bamboo, Petrified Pumpkins, Perlite and Loam, Explosive Drill, Underground Leaderboard; довідник `dig`, `push`, `can_push`, `place`, `hover`, `jump`, `get_pos_z`, `get_hardness`, `get_stability`, `prospect_iron`, `prospect_quartz`.
- [Steam: The Miner Was Replaced](https://store.steampowered.com/app/4521700/The_Miner_Was_Replaced/) — опис DLC, дата, платформи; скриншоти з кодом (піраміди, flood fill руди, сортування грибів, сапер на сажі, руїни, дерево розблокувань).
- [Прес-кіт Metaroot](https://www.metaroot.ch/press-kit/the-miner-was-replaced) — дата, Unity, Windows/Mac, команда.
- [Новина про реліз DLC](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847920302248386) — нова гілка дерева, рис на глині, мобільна версія, патч документації.
- [Semy0nBu/the-farmer-was-replaced](https://github.com/Semy0nBu/the-farmer-was-replaced) — назви DLC-скриптів гравця (лише перелік файлів).
- YouTube: пошук «The Miner Was Replaced gameplay».

## Непевне
- (?) Чи рух під землею лишається тором, як `move` на поверхні; як дрон переходить між колонками різної висоти (обмеження на перепад?).
- (?) Точний порядок і глибина пластів Mushroom, Dynamite/Soot, Basalt, Sand/Limestone і Bedrock.
- (?) Скільки всього грибних типів і чи мета — зібрати все в стоси чи довільні пари (гайд: «0–5», «два однакові один на одному»).
- (?) Радіус вибуху динаміту / Explosive Drill і «енергія вибуху» (+30 % з апгрейдом) — числа не знайдено.
- (?) Документація — неофіційний витяг з файлів гри (репозиторій користувача); зміст сторінок — дослівний текст гри, але повноту не перевірено.
- (?) 8 нових ресурсів за Steam — ймовірно Block, Coal, Iron, Quartz, Mushroom, Dynamite, Rice, Bamboo (за списком апгрейдів Mining).
