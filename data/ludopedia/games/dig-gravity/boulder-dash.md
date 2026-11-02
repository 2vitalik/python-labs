---
title: Boulder Dash
slug: boulder-dash
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1984
platforms: [Atari 8-bit, C64, ZX Spectrum, Amstrad CPC, BBC Micro, arcade, NES]
links:
  - {kind: fandom, url: "https://boulder-dash.nl/chars.php?lang=en", best: true, note: "фан-сайт: усі елементи BD1 з поведінкою, коротко й з картинками"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Boulder_Dash_(video_game)", note: "історія, порти, сиквели, Construction Kit"}
  - {kind: wiki, url: "https://www.c64-wiki.com/wiki/Boulder_Dash", note: "печери A–P, інтермісії, 5 рівнів складності, життя"}
  - {kind: official, url: "https://boulder-dash.com/history/", note: "офіційний сайт бренду, історія"}
  - {kind: wiki, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/Files/FanStuff/Programming/BDCFF_Objects_Specifications.doc", note: "BDCFF: технічна специфікація кожного обʼєкта (алгоритми, ймовірності)"}
  - {kind: wiki, url: "https://elmerproductions.com/sp/peterb/BDCFF/objects/0005.html", note: "BDCFF онлайн: розширювана стіна"}
  - {kind: wiki, url: "https://boulder-dash.nl/forum/viewtopic.php?p=2639", note: "форум: як працює проникність слизу"}
  - {kind: play, url: "https://jakesgordon.com/games/boulderdash/play/help/", note: "JS-клон з відкритим кодом і довідкою"}
  - {kind: play, url: "https://archive.org/search?query=boulder+dash", note: "пошук; C64/Atari-версії в браузері (Internet Archive)"}
  - {kind: wiki, url: "https://elmerproductions.com/sp/peterb/BDCFF/objects/index.html", note: "BDCFF онлайн: сторінки обʼєктів (камінь, Рокфорд, світлячок, метелик, амеба)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=boulder+dash+1984+c64+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 75
mechanics: [move-4dir, gravity-fall, push-object, collect-quota, reach-exit, time-out, time-bonus, touch-death, environment-death, player-death, cell-transform, chain-detonation, impassable-cells, event-points, sequential-levels, difficulty-levels, player-camera, status-panel, goal-counter, +dig-terrain, +roll-off-rounded, +explode-3x3, +blob-growth, +wall-follower, +snap-action]
proposes: ["+trigger:enter", "+cond:state", "+cond:free", "+cond:rounded", "+effect:fall", "+effect:roll", "+effect:explode", "+effect:spread", "+effect:set_cell", "+role:terrain", "+role:hazard", "+card:scan-order", "+card:expanding-wall", "+card:permeable-cell", "+axis:session"]
author: opus
date: 2026-11-02
---

# Boulder Dash — копай землю, збирай алмази, не потрап під камінь

## Суть
Рокфорд копає тунелі в землі печери, збирає квоту алмазів і встигає до виходу, поки йде таймер. Ядро — **клітинна фізика**: камені й алмази падають у порожнечу й скочуються з «круглих» обʼєктів, вороги ходять уздовж країв порожнечі, вибухи 3×3 перетворюють клітини. Кожен елемент має кілька рядків правил, а цікаве народжується з їх зіткнення: метелик під каменем → 9 алмазів, амеба в коробці → алмази, магічна стіна → камінь стає алмазом.

## Поле і час
- Печера — прямокутна сітка (C64: 40×22 = 880 клітин, з рамкою зі сталі), видно частину, камера скролить за Рокфордом. Інтермісії — маленькі печери на один екран.
- Один шар: у клітині рівно один елемент (порожнеча, земля, стіна, камінь, ворог…). «Стан» живе в самому елементі: камінь падає/стоїть, світлячок дивиться в напрямку.
- Real-time, але дискретний: тік = **скан печери** від лівого верхнього кута рядками вниз; кожен елемент обробляється раз на тік (зсунутий униз/праворуч позначається «вже оброблено»); на C64 хід Рокфорда обробляється всередині скану. Рокфорд і падаючий камінь проходять по клітині за тік (?).
- Таймер печери в секундах (зворотний відлік); на початку Рокфорд зʼявляється з мигаючого входу (inbox).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рокфорд | player | 3 життя, +1 кожні 500 очок | рух 4 напрямки (діагональ → горизонталь); копає землю; штовхає камінь; дія «на місці» з кнопкою |
| Порожнеча | terrain | — | сюди падають камені; уздовж її країв ходять вороги |
| Земля (dirt) | terrain | — | Рокфорд проходить → порожнеча; амеба росте в неї; вороги не входять |
| Камінь (boulder) | object | falling: так/ні; круглий | падає в порожнечу; скочується з круглого; падаючий на «вибухове» → вибух |
| Алмаз | pickup | круглий; ціна в очках | фізика як у каменя; збирається навіть у падінні; падаючий алмаз теж вбиває |
| Цегляна стіна | static | круглa; руйнується вибухом | непрохідна; камені скочуються |
| Сталева (титанова) стіна | static | не кругла; невразлива | рамка печери; вибух її не бере |
| Магічна стіна | switch | стан dormant → on → expired; час роботи | падаючий камінь крізь неї → алмаз, алмаз → камінь, на 2 клітини нижче |
| Розширювана стіна | static | не кругла | щотіку росте ліворуч/праворуч у порожнечу |
| Слиз (BD2+) | terrain | проникність (байт) | випадково пропускає камінь/алмаз крізь себе вниз |
| Світлячок (firefly) | enemy | напрямок (старт — ліворуч) | пріоритет: поворот ліворуч → прямо → поворот праворуч на місці; за годинниковою вздовж краю порожнечі; вибух у порожнечу |
| Метелик (butterfly) | enemy | напрямок | дзеркально: праворуч → прямо → ліворуч; проти годинникової; вибух у 9 алмазів |
| Амеба | hazard | розмір ≤ 200; швидкість росту | росте у порожнечу/землю; ≥200 → усе каміння; не може рости → усе алмази |
| Вибух | hazard | 3×3, кілька тіків | знищує все, крім сталі; лишає порожнечу або алмази |
| Вихід (outbox) | gate | квота | зʼявляється/відкривається, коли зібрано квоту; вхід → кінець печери |
| Вхід (inbox) | spawner | — | мигає на старті, породжує Рокфорда |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, dirt|empty)` → ТО `move(rockford, dir)`; земля → `set_cell(empty)`.
- КОЛИ `input(fire+dir)` → ТО `custom: «snap: зібрати алмаз / прибрати землю в сусідній клітині, не рухаючись»`.
- КОЛИ `contact(rockford, boulder)` по горизонталі → ЯКЩО `free(cell_behind)` and `state(boulder, still)` and `prob(1/8)` (кожен тік спроби) → ТО `push`; інакше `block`. Вертикально камені не штовхаються.
- КОЛИ `contact(rockford, diamond)` → ТО `pickup`, `counter(diamonds, +1)`, `score(diamond_value)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(boulder|diamond)` (`set_state(falling)`).
- КОЛИ `tick` → ЯКЩО `state(a, falling)` and `cell(below, rounded)` and `state(below, still)` → ТО `roll(a, left)` якщо вільні клітина ліворуч і ліворуч-знизу; інакше `roll(a, right)` за тим самим правилом; інакше `clear_state(a, falling)`.
- КОЛИ `contact(falling boulder|diamond, rockford|firefly|butterfly)` → ТО `explode(3×3, into)`, камінь поглинається вибухом.
- КОЛИ `contact(falling boulder, magic_wall)` → ТО `set_state(magic_wall, on)`; ЯКЩО `state(magic_wall, on)` and `free(2 below)` → ТО `transform(diamond)` на 2 клітини нижче; інакше `disappear_a`. Алмаз дзеркально → камінь. ЯКЩО `state(expired)` → ТО `disappear_a`.
- КОЛИ `timer(milling_time)` після активації → ТО `set_state(magic_wall, expired)`.
- КОЛИ `tick` → ТО `custom: «світлячок: ліворуч вільно → поворот ліворуч і крок; прямо вільно → крок; інакше поворот праворуч на місці»`; метелик — дзеркально.
- КОЛИ `adjacent(firefly|butterfly, rockford|amoeba)` → ТО `explode(3×3, into: empty|diamonds)` до свого руху (перевірка всіх 4 сусідів щотік) — вибухає лише ворог, Рокфорд гине, бо потрапив у зону.
- КОЛИ `explode` → ТО всі клітини 3×3, крім сталі, → `set_cell(explosion)` → `set_cell(empty|diamond)`; Рокфорд і вороги в зоні знищуються; чи ворог у зоні дає власний вибух (`chain-detonation`) — (?).
- КОЛИ `tick` → ЯКЩО `prob(4/128)` (після slow_growth_time — `prob(4/16)`) → ТО `spread(amoeba, rng_dir)` у порожнечу або землю.
- КОЛИ `counter(amoeba_cells, >=, 200)` (підрахунок минулого тіку; 200 = 22.7 % з 880) → ТО усі клітини амеби `transform(boulder)`.
- КОЛИ `custom: «амеба не змогла вирости за минулий тік»` → ТО усі клітини амеби `transform(diamond)`.
- КОЛИ `tick` → ТО `spread(expanding_wall, left|right)` у порожнечу; нові шматки ростуть з наступного тіку.
- КОЛИ `contact(falling boulder|diamond, slime)` → ЯКЩО `custom: «rnd AND permeability == 0»` and `free(below slime)` → ТО `move` крізь слиз; інакше лежить на ньому.
- КОЛИ `counter(diamonds, >=, quota)` → ТО `set_state(outbox, open)`, `flash`, ціна алмаза → `extra_value`.
- КОЛИ `contact(rockford, outbox)` → ЯКЩО `state(outbox, open)` → ТО `win`, `score(time_left)`, `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`, `lives(-1)`, `restart`.
- Перемога (печера): квота алмазів + вихід до кінця часу. Поразка: падаючий камінь/алмаз, вибух, дотик ворога, кінець часу → −1 життя; 0 життів → `game_over`.
- Рахунок: алмаз = ціна печери (після квоти — «додаткова» ціна), залишок часу → очки на виході; кожні 500 очок — +1 життя.

## Керування і ввід
- Джойстик/стрілки: 4 напрямки; одночасно дві осі → перемагає горизонталь.
- Fire + напрямок: дія на сусідній клітині без руху («snap»: підхопити алмаз, прибрати землю), щоб не підставитись під камінь.
- Меню (C64): вибір кількості гравців (F3), стартової печери (A/E/I/M — джойстик ліво/право) і рівня складності 1–5 (вперед/назад); дві особи грають по черзі.
- C64 у грі: Run/Stop — перезапустити печеру, пробіл — пауза.

## Вікна, меню, HUD
- `splash-screen`: титульний екран з музикою, прокрутка імен.
- `main-menu`: гравці 1/2 · печера A/E/I/M · рівень 1–5 → старт `game-screen` (`difficulty-select` і `level-select` вбудовані у меню).
- `custom-window` «картка печери»: «Player 1, N men, Cave X» перед стартом.
- `game-screen`: поле зі скролом; верхній рядок HUD — квота алмазів і їх ціна (`objective-text`, `remaining-counter`), зібрано, `timer-countdown`, `score`; при відкритті виходу — спалах екрана.
- `end-screen`: «Game over» → повернення на титул з рекордом (`hi-score`).
- Переходи: титул → печера → (інтермісія після кожної 4-ї) → наступна печера; смерть → та сама печера знову.

## Фічі поза полем
- `levels-sequential`: 16 печер A–P + 4 інтермісії (бонусні логічні мініпечери).
- `difficulty-presets`: 5 рівнів для кожної печери (ті самі мапи, інші параметри).
- `level-select`: старт лише з кожної 4-ї печери (A, E, I, M) — квазі-чекпоінти.
- `hotseat`: два гравці по черзі.
- `pause` (пробіл) і `restart-level` (Run/Stop) на C64.
- `level-editor`: Boulder Dash Construction Kit (1986) — редактор печер, 12 печер і 3 інтермісії в комплекті; таймери амеби й магічної стіни — параметри печери (BDCFF).
- Рекорди: після кожної печери показано рахунок і hi-score.

## Варіації й родичі
- Сиквели: Boulder Dash II (1985), Boulder Dash 3 (1986), Construction Kit (1986), Super Boulder Dash (1986, збірка), NES-версія (1990; мапа світу (?)), Rockford (аркада 1988), Boulder Dash Part 2 (аркада 1990), Boulder Dash-XL (2011), Boulder Dash 40th Anniversary (2025). Аркадні порти: Exidy Max-A-Flex (1984, гроші за 30 с гри), Data East DECO Cassette (1985, урізана сітка).
- Клони й нащадки: Emerald Mine (кислота, динаміт, 2 гравці), Supaplex (порти, дискети), Repton (паралельна BBC-лінія), Rocks'n'Diamonds (обʼєднаний двіжок), GDash (точний емулятор із редактором), Diamond Caves.
- **Осі варіацій**: падіння — «лише вниз / скочування з круглого / per-type напрямок (XOR)»; вибух — «у порожнечу / в алмази / в інфотрони»; ріст — «амеба (випадково, з порогом) / розширювана стіна (детерміновано по осі) / грибок Repton (без перетворення)»; скан — «зверху-зліва / подвійний буфер» (дає різні каскади).
- Формат BDCFF — спільний текстовий опис печер і обʼєктів для фанатських двіжків.

## Цікавинки для курсу
- Падіння + скочування з круглих обʼєктів з порядком скану зверху вниз — 🥉: кілька умов, але треба вирішити, як не обробити камінь двічі за тік.
- Вороги «тримай стіну ліворуч/праворуч» з пріоритетом поворотів — 📎 на одного, 🥉 за пару з вибухом при сусідстві.
- Вибух 3×3 з типом результату (порожнеча/алмази) і ланцюгом через інших ворогів — 🥉.
- Амеба: ймовірнісний ріст, два фінали (поріг розміру → каміння, задушення → алмази) — 🥈: глобальна умова на групу клітин.
- Магічна стіна з таймером станів і «прольотом» на 2 клітини — 🥉.
- Детермінований vs ймовірнісний двіжок (штовхання 1/8, слиз за маскою rnd) і відтворюваність за seed — 🥇, якщо з реплеєм.

## Мапа на каталог
- Є: `move-4dir` ↔ Рокфорд · `gravity-fall` ↔ камені/алмази · `push-object` ↔ штовхання каменя · `collect-quota` ↔ квота алмазів → вихід · `reach-exit` · `time-out` + `time-bonus` · `touch-death` (вороги, амеба) · `environment-death` (камінь згори, вибух) · `player-death` (3 життя) · `cell-transform` ↔ магічна стіна · `chain-detonation` ↔ вибух підриває ворогів у зоні · `impassable-cells` (стіни) · `event-points` · `sequential-levels` · `difficulty-levels` · `player-camera` · `status-panel` + `goal-counter`.
- **Нема** → пропозиції карток:
  - `+dig-terrain` «Копання землі» · entities/interact · 🌱 — земля стає порожнечею, коли через неї пройти; для ворогів — стіна.
  - `+roll-off-rounded` «Скочування з круглих» · entities/move · 🥉 · слот {priority: left|right} — дитина `gravity-fall`.
  - `+explode-3x3` «Вибух 3×3 з результатом» · entities/combat · 🥉 · слот {into: empty|item} — поряд із `blast-wave`.
  - `+blob-growth` «Амеба: ріст і перетворення групи» · entities/spawn · 🥈 · слоти {max, slow_time} — ріст у випадковий бік, фінал за станом усієї групи.
  - `+wall-follower` «Ворог тримається стіни» · entities/move · 🥉 · слот {side: left|right} — повтор пропозиції з Chip's Challenge.
  - `+snap-action` «Дія без руху» · interface/input · 🌱 — модифікатор кнопки: взаємодія з сусідньою клітиною на місці.
  - `+scan-order` «Порядок обробки клітин за тік» · code/architecture · 🥉 — прапорець «оброблено» проти подвійного руху.
  - `+expanding-wall` «Стіна, що росте» · entities/spawn · 📎 · слот {axis: h|v|both}.
  - `+permeable-cell` «Проникна клітина» · entities/interact · 📎 · слот {chance} — слиз пропускає падаюче з ймовірністю.

## Пропозиції до словників
- `+trigger:enter` — Рокфорд входить у землю/вихід (клітина-тип, не сутність); ⏳ уже є, рахую на правило трьох.
- `+cond:state` (камінь падає/стоїть, магічна стіна on/expired) і `+cond:free` (порожнеча під/збоку) — ⏳, підтвердження вжитку.
- `+cond:rounded` — клітина «кругла» (з неї скочується падаюче): камінь, алмаз, цегла так; сталь, магічна стіна ні.
- `+effect:fall` ⏳ · `+effect:roll(a, dir)` — скотитись убік-униз з круглої опори (не те саме, що `slide`).
- `+effect:explode(area, into)` — вибух області з результатом (порожнеча / алмази); зараз нема окремого слова.
- `+effect:spread(a, dir)` — сутність займає сусідню клітину, лишаючись на місці (амеба, розширювана стіна, грибок).
- `+effect:set_cell` ⏳ (земля → порожнеча), `+role:terrain` ⏳ (земля, порожнеча, слиз), `+role:hazard` ⏳ (амеба, вибух).
- `+axis:session` — тут `level` із «точками входу» (A/E/I/M у меню); ⏳ кандидат осі, рахую на правило трьох.

## Джерела
- ⭐ [boulder-dash.nl — characters](https://boulder-dash.nl/chars.php?lang=en) — усі елементи BD1 і їх поведінка (амеба ≤200, метелик → 9 алмазів, світлячок за годинниковою, метелик проти).
- [BDCFF Objects Specifications](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/Files/FanStuff/Programming/BDCFF_Objects_Specifications.doc) — алгоритми: скочування (спершу ліворуч), пріоритети поворотів ворогів, амеба 4/128 → 4/16, штовхання 1/8, snap кнопкою, milling time.
- [BDCFF онлайн: обʼєкти](https://elmerproductions.com/sp/peterb/BDCFF/objects/index.html) — окремі сторінки: камінь (0000), Рокфорд (0006), світлячок (0008), метелик (0009), амеба (000A).
- [BDCFF Object 0005: Expanding wall](https://elmerproductions.com/sp/peterb/BDCFF/objects/0005.html) — ріст ліворуч/праворуч, не кругла.
- [Форум boulder-dash.nl: slime permeability](https://boulder-dash.nl/forum/viewtopic.php?p=2639) — формула `rnd AND permeability == 0`.
- [C64-Wiki: Boulder Dash](https://www.c64-wiki.com/wiki/Boulder_Dash) — 3 життя, +1 за 500 очок, 5 рівнів, печери A/E/I/M у меню, інтермісії після D/H/L/P, пауза й рестарт.
- [Wikipedia](https://en.wikipedia.org/wiki/Boulder_Dash_(video_game)) — версії, сиквели, Construction Kit, аркадні порти.
- [Jake Gordon: JS Boulder Dash](https://jakesgordon.com/games/boulderdash/play/help/) — грається в браузері, відкритий код для курсу.
- [Internet Archive: пошук](https://archive.org/search?query=boulder+dash) — оригінальні версії в браузері (стара сторінка c64.krissz.hu віддає 404).

## Непевне
- (?) Видиме вікно ~20×12 — з памʼяті про C64; 40×22 виводиться з BDCFF (200 = 22.7 % від 880 клітин).
- (?) Чи світлячок/метелик, що потрапив у чужий вибух, вибухає сам (ланцюг) — у перевірених сторінках не сказано; тег `chain-detonation` тримається на цьому.
- (?) Рокфорд і падаючий камінь — однакова швидкість (клітина за тік) — з памʼяті.
- (?) Ціна алмаза до/після квоти («extra diamond value») і нарахування залишку часу на виході — відоме з фанатських описів, у перевірених джерелах лише «bonus points».
- (?) Точний порядок скану (рядками зверху-зліва) у джерелах прямо не сказано; BDCFF згадує лише «Rockford already scanned this frame».
- (?) Слиз — з BD2/Construction Kit, не з BD1; джерело не називає гру, де він зʼявився.
- (?) Тривалість роботи магічної стіни («milling time») і slow-growth амеби — параметри печери, чисел не знайшов; на C64 BD1 відома «дивна» поведінка таймера магічної стіни.
