---
title: HyperRogue
slug: hyperrogue
family: roguelike
also: [chess-abstract]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: ai
  info: full
  random: both
  goal: collect
year: 2011
platforms: [PC (Windows, macOS, Linux), Android, iOS, web (WebGL-демо), OpenPandora]
links:
  - {kind: official, url: "https://roguetemple.com/z/hyper/", best: true, note: "офіційний сайт Zeno Rogue: правила одним абзацом, галерея земель, моделі геометрії, завантаження"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/HyperRogue", note: "тайлінг, 72 землі, «шах», історія"}
  - {kind: fandom, url: "https://hyperrogue.miraheze.org/wiki/Main_Page", note: "офіційна вікі: землі, орби, монстри, скарби"}
  - {kind: other, url: "https://roguetemple.com/z/hyper/gallery.php", note: "галерея земель з короткими правилами кожної"}
  - {kind: play, url: "https://roguetemple.com/z/hyper/online.php", note: "WebGL-демо в браузері"}
  - {kind: other, url: "https://github.com/zenorogue/hyperrogue/", note: "сирці (GPL-2.0)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=hyperrogue", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hyperrogue+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, touch-death, piece-capture, no-move-into-check, chase-greedy, speed-per-type, multi-cell-size, item-pickup, inventory-duration, temporary-modes, infinite-field, level-unlock, progress-acceleration, cell-transform, impassable-cells, player-death, score-records, save-progress, cell-click, legal-move-highlight, game-screen, settings-window, help-window, +hyperbolic-grid, +great-wall-lands, +treasure-raises-danger, +orb-charges, +heat-diffusion, +mirror-mimics, +delayed-shadow, +raise-undead, +collapsing-floor, +color-restricted-move, +key-far-away, +geometry-switch, +projection-model, +permadeath]
proposes: ["+trigger:illegal_move", "+cond:temperature", "+cond:cell_color", "+effect:melt", "+effect:mimic_move", "+effect:raise", "+effect:collapse", "+effect:paint", "+role:land", "+window:quest-status", "+window:geometry-select", "+window:model-select", "+ui:treasure-row", "+ui:orb-charges", "+ui:compass-beacon", "+feature:mode-pure-tactics", "+feature:orb-strategy", "+feature:geometry-switch", "+axis:field=hyperbolic", "+axis:session=run"]
author: opus
date: 2026-11-02
---

# HyperRogue — роглайк на гіперболічній площині: клітин у кожному кільці експоненційно більше, тож назад дороги нема

## Суть
Гравець ходить по нескінченній мозаїці з семикутників і шестикутників на гіперболічній площині (показ — диск Пуанкаре), збирає скарби в десятках «земель» і уникає монстрів. Бій шаховий: монстр і гравець гинуть від одного удару, а хід, після якого гравця можна вбити, **заборонений** — як хід під шах. Кожен зібраний у землі скарб робить землю небезпечнішою; 10 скарбів відкривають орб землі й нові землі. Головний урок — геометрія: відійти легко, а повернутися в ту саму клітину майже неможливо (на відстані 100 — порядку тисяч клітин).

## Поле і час
- Поле — **граф**: зрізаний порядку-7 трикутний тайлінг (семикутники в оточенні шестикутників); у семикутника 7 сусідів, у шестикутника 6. Кількість клітин на відстані n росте експоненційно, а не лінійно.
- Камера завжди в центрі диска Пуанкаре; далекі клітини стискаються до краю. Альтернативні моделі: Клейн, смуга, «гіперболічний килим» (Hypersian Rug), конформні.
- Світ **нескінченний і генерується на льоту**: «Великі стіни» (гіперболічні прямі) ділять площину на землі; за стіною — інша земля, перехресні точки — хаби Crossroads.
- Покроково: хід = рух у сусідню клітину / атака сусідньої / чекання. Монстри ходять після гравця; деякі — через хід (Lesser Demon, повільні) або двічі.
- Інформація повна в межах диска: монстри детерміновані й видимі; невідоме — лише те, що ще не згенероване.
- Режими геометрії: евклідова, сферична, еліптична, «семикутний» режим (ще сильніша гіперболічність), 3D-геометрії Терстона — щоб порівняти, що змінюється.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 1 удар = смерть | рух у 6/7 сусідів; вхід у клітину монстра = вбити |
| Велика стіна | static | пряма | межа земель; генерує нову землю за собою |
| Скарб землі | pickup | вид на землю | +1 до лічильника землі; більше скарбів → більше монстрів |
| Орб | pickup | заряди | дає силу на N ходів, −1 заряд щохід |
| Yeti | enemy | — | жадібна погоня (Icy Land) |
| Ice Wolf | enemy | — | іде лише в теплішу клітину — «нюхає» тепло |
| Крижана стіна | static | температура | тане, коли температура > 0 °C |
| Багаття (Bonfire) | switch | — | запалити → гріє сусідні клітини, відволікає вовків |
| Sandworm | enemy | багатоклітинний | повільний, важко вбити (Desert) |
| Ivy (плющ) | enemy | багатоклітинний | росте з кореня, бʼє гілками (Jungle) |
| Жива стіна | static | — | росте, коли біля неї вбито Cave Troll (Living Cave) |
| Клітина кольору / слиз | terrain / enemy | колір | ходити лише по одному кольору; вбитий слиз фарбує сусідів (Alchemist Lab) |
| Магічне дзеркало / хмара міражу | object | — | розбити → 3 (6) мімік-двійників гравця (Hall of Mirrors) |
| Мімік | ally | — | повторює хід гравця дзеркально (вперед/назад так само, ліво↔право) |
| Могила свіжа / стара | static | — | стіна; некромант на свіжій → зомбі + привид (Graveyard) |
| Zombie / Ghost | enemy | привид ефірний | зомбі — базова погоня; привид проходить крізь стіни |
| Necromancer | enemy | — | біля свіжої могили піднімає нежить |
| Shadow | enemy | невразливий | повторює шлях гравця з затримкою 15 ходів |
| Підлога, що падає | terrain | — | обвалюється, щойно гравець зійшов (Land of Eternal Motion) |
| Міна (Minefield) | hazard | прихована | як у сапері: числа сусідніх мін |
| Ворота / перемикач / люк | gate / switch / hazard | — | лабіринт Палацу |
| Lesser / Greater Demon | enemy | повільні | Greater не вбивається звичайним ударом; кожен 10-й Lesser перетворює Greater на Lesser (Hell) |
| Озеро сірки | hazard | — | зіштовхнутий туди монстр тоне |
| Орб Йендора | pickup | ключ за 100 клітин | перемога; ключ треба принести до орба |
| Ключ | pickup | — | відкриває свій Орб Йендора |
| Друзі (голем, мімік) | ally | — | бʼються на боці гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move to neighbor)` → ЯКЩО `occupied(cell, monster)` and `custom: «вразливий до звичайного удару»` → ТО `disappear_b`, `counter(kills, +1)`.
- КОЛИ `input(move|wait)` → ЯКЩО `custom: «після ходу гравець опиниться під атакою»` → ТО `block`, `message(«you would be killed»)` — заборона ходу під шах (`+trigger:illegal_move`).
- КОЛИ `no_moves(player)` → ТО `lose` (?).
- КОЛИ `turn_end(player)` → ТО монстри: `chase-greedy` до гравця; ЯКЩО `adjacent(monster, player)` → ТО `lose` (неможливо через правило шаху, крім пасток/особливих).
- КОЛИ `contact(player, treasure)` → ТО `pickup`, `counter(treasure[land], +1)`, `score(+1)`.
- КОЛИ `counter(treasure[land], >=, 10)` → ТО `unlock(orb of land)` у землі й хабах; `unlock(lands)` за правилами; КОЛИ `>= 25` → орб скрізь.
- КОЛИ `spawned(monster)` → `custom: «частота спавну в землі росте з кількістю скарбів цієї землі»` — фарм неможливий.
- КОЛИ `counter(kills, >=, 100)` → ТО `unlock(Graveyard)`.
- КОЛИ `contact(player, orb)` → ТО `custom: «+N зарядів орба»`; КОЛИ `turn_end` → ТО `counter(orb, -1)` для кожного орба.
- Орби (приклади): Flash — `custom: «при атаці/незаконному ході знищити все в радіусі 2»`; Speed — монстри ходять раз на 2 ходи; Shielding — імунітет до атак; Teleport — `teleport(target)`; Winter — лишає крижані стіни; Fire — вогняний слід; Aether — крізь стіни й прірви; Life — `spawn(golem ally)`.
- КОЛИ `tick` (Icy Land) → ТО `custom: «температура дифундує дискретним рівнянням тепла; гравець гріє сусідів»`; ЯКЩО `temperature(cell) > 0` → ТО `set_cell(ice_wall → floor)` (`+effect:melt`).
- КОЛИ `turn_start(ice_wolf)` → ЯКЩО `custom: «сусідня клітина тепліша»` → ТО `move(wolf, warmer)`; інакше стоїть.
- КОЛИ `destroyed(mirror)` → ТО `spawn(3 mimics)`; КОЛИ `input(move dir)` → ТО `mimic_move(mimics, mirror(dir))`.
- КОЛИ `adjacent(necromancer, fresh_grave)` → ТО `spawn(zombie)`, `spawn(ghost)`, `set_cell(ancient_grave)`.
- КОЛИ `turn_end` (Graveyard) → ТО `move(shadow, player_pos[t−15])`.
- КОЛИ `leave(player, cell)` (Eternal Motion) → ТО `set_cell(chasm)`.
- КОЛИ `input(move)` (Alchemist Lab) → ЯКЩО `not same(cell, player_cell, color)` → ТО `block`; КОЛИ `died(slime)` → ТО `paint(neighbors, slime_color)`.
- КОЛИ `contact(player, yendor_orb)` → ЯКЩО `has(player, key)` → ТО `win`; інакше `custom: «вмикається маяк-стрілка до ключа за 100 клітин»`; назад до орба стрілки нема.
- КОЛИ `counter(10 of each of 9 treasures)` → ТО `unlock(Hell)`; Hyperstone Quest — по 10 скарбів кожної землі.
- Перемога: Орб Йендора (або квести Hyperstone, Принц(еса), Граль). Поразка: один удар; гра без кінця інакше. Рахунок: сума скарбів ($), убивства, час; найкращі — у таблиці.

## Керування і ввід
- Миша: клік по сусідній клітині — хід/атака; наведення — опис клітини/монстра. Клавіатура: numpad / vi-клавіші відображаються на найближчий напрямок (7 сусідів не лягають рівно на 8 клавіш) (?).
- `.` / `s` — чекати хід (?); незаконні ходи просто не виконуються (повідомлення чому).
- Активні орби (Teleport…) — клік по цільовій клітині, коли орб заряджений.
- Shmup-режим: real-time, вільний рух, підтримка двох гравців на одному екрані.

## Вікна, меню, HUD
- `game-screen`: диск Пуанкаре з гравцем у центрі; по краях — `+ui:treasure-row` (іконки скарбів з лічильниками), `+ui:orb-charges` (активні орби з залишком), `score` ($), kills, повідомлення внизу.
- `+window:quest-status` (Esc): зібране по землях, що відкриває наступне, прогрес квестів Hyperstone/Yendor, статистика ходів і часу.
- `main-menu` / налаштування (`settings-window`): графіка, модель проєкції (`+window:model-select`), геометрія і тайлінг (`+window:geometry-select`), режими (Pure Tactics, Orb Strategy, Yendor Challenge, shmup, евклідовий), мова.
- `help-window` — опис землі/монстра/орба під курсором.
- `end-screen` — «You are killed» з причиною + quest status → нова гра.
- `leaderboard` — локальні рекорди по режимах; `achievements-window` (Steam).
- Переходи: старт → game-screen (Crossroads/Icy Land); Esc → quest-status → назад; меню → геометрія/модель → перезапуск світу.

## Фічі поза полем
- `permadeath`: одна партія = один забіг; рекорди й досягнення між партіями.
- Режими: Pure Tactics Mode (одна земля, тактика), Orb Strategy Mode (орби в інвентарі, вживати будь-коли), Yendor Challenge (сценарії), shmup (real-time, 2 гравці), Casual (?).
- `custom-rules` на рівні геометрії: евклідова/сферична/еліптична/«семикутна»/3D, фактори-простори, — **те саме правило гри на іншій топології**.
- `theme-select` у сенсі моделей проєкції (Пуанкаре, Клейн, смуга, Rug); VR (з 12.0).
- `localization` (кілька мов), сирці відкриті.

## Варіації й родичі
- Свої: shmup-режим, RogueViz (візуалізації на тому самому рушії); у ширшому колі — Hyperbolica (CodeParade, інший автор) (?).
- Родичі за ідеєю: Hoplite і Into the Breach (детерміновані вороги, «шахова» тактика), шахи (заборона ходу під шах), Minesweeper (Minefield), Sokoban (штовхання в деяких землях).
- Осі варіацій: **геометрія поля** (евклідова / сферична / гіперболічна) · **граф сусідства** (6 / 7 / змішаний) · **проєкція** (Пуанкаре / Клейн / смуга) · **смерть** (від одного удару / HP) · **легальність** (будь-який хід / заборона ходу під атаку) · **складність** (час / кількість скарбів у землі).

## Цікавинки для курсу
- Гіперболічна сітка як граф: генерація сусідів на льоту, координати через шляхи від центру — 👑 (дослідницький рівень геометрії і структур даних).
- Заборона ходу «під шах» для аватара: перевірка, чи хтось із монстрів дістане клітину після їхнього ходу — 🥇 (картка `no-move-into-check` є).
- Дифузія температури + танення стін + вовк, що йде на тепло — 🥈 (клітинне рівняння тепла з ігровим наслідком).
- Дзеркальні міміки: ввід → дзеркальне перетворення напрямку для кожного двійника — 🥉.
- Тінь, що повторює шлях гравця із затримкою 15 ходів — 📎 (черга позицій).
- «Скарби підвищують небезпеку»: спавн як функція локального лічильника — 🌱.
- Ключ за 100 клітин від орба: навігація без зворотної стрілки — 🥈 (найкращий урок про експоненційний ріст).

## Мапа на каталог
- Є: `move-by-input` · `touch-death` · `piece-capture` (вхід у клітину = вбити) · `no-move-into-check` · `chase-greedy` · `speed-per-type` · `multi-cell-size` (Ivy, Sandworm) · `item-pickup` · `inventory-duration` + `temporary-modes` (орби) · `infinite-field` · `level-unlock` (землі) · `progress-acceleration` (скарби → спавн) · `cell-transform` (танення, обвал, фарбування) · `impassable-cells` · `player-death` · `score-records` · `save-progress` · `cell-click` · `legal-move-highlight` · `game-screen` · `settings-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+hyperbolic-grid` «Гіперболічна сітка {7,3} як граф» · levels/generation · 👑.
  - `+great-wall-lands` «Землі за прямими-стінами, генерація на льоту» · levels/generation · 🥇.
  - `+treasure-raises-danger` «Спавн росте з кількістю зібраного в зоні» · game-logic/waves · 🌱 · слот {rate}.
  - `+orb-charges` «Сила із зарядами, що тануть щохід» · entities/state · 📎 · слоти {charges, decay}.
  - `+heat-diffusion` «Температура клітин і рівняння тепла» · entities/interact · 🥈.
  - `+mirror-mimics` «Двійники повторюють хід дзеркально» · entities/move · 🥉.
  - `+delayed-shadow` «Тінь іде слідом із затримкою N ходів» · entities/move · 📎 · слот {delay}.
  - `+raise-undead` «Ворог біля могили породжує інших» · entities/spawn · 📎.
  - `+collapsing-floor` «Підлога обвалюється за спиною» · entities/interact · 🌱.
  - `+color-restricted-move` «Рух лише по клітинах свого кольору» · entities/legality · 📎.
  - `+key-far-away` «Ключ далеко від цілі без стрілки назад» · levels/generation · 🥉.
  - `+geometry-switch` «Та сама гра на іншій топології поля» · interface/settings · 👑.
  - `+projection-model` «Модель проєкції поля (Пуанкаре, Клейн)» · interface/render · 🥇.
  - `+permadeath` (з Rogue).

## Пропозиції до словників
- `+trigger:illegal_move` — гравець спробував заборонений хід (Orb of Flash спрацьовує саме на нього).
- `+cond:temperature` — температура клітини порівняно з порогом; `+cond:cell_color` — колір клітини (Alchemist Lab).
- `+effect:melt` — стіна стає підлогою за температурою; `+effect:mimic_move` — інша сутність повторює ввід з перетворенням напрямку; `+effect:raise` — некромант піднімає нежить; `+effect:collapse` — клітина стає прірвою; `+effect:paint` (є як ⏳, тут уживання).
- `+role:land` — зона нескінченного світу зі своїми правилами (ширша за `zone`: має свої сутності, скарб, орб).
- `+window:quest-status` — екран прогресу квестів і розблокувань; `+window:geometry-select`; `+window:model-select`.
- `+ui:treasure-row` — ряд іконок скарбів з лічильниками; `+ui:orb-charges` — орби з зарядами; `+ui:compass-beacon` — стрілка до ключа.
- `+feature:mode-pure-tactics`, `+feature:orb-strategy`, `+feature:geometry-switch`.
- `+axis:field=hyperbolic` — граф не передає головного: експоненційний ріст кілець; `+axis:session=run`.

## Джерела
- ⭐ [HyperRogue — офіційний сайт](https://roguetemple.com/z/hyper/) — правила («шах», один удар), землі, скарби → монстри, 10/25 скарбів, режими й геометрії.
- [Wikipedia: HyperRogue](https://en.wikipedia.org/wiki/HyperRogue) — тайлінг {7,3} зрізаний, 72 землі, Великі стіни, багатоклітинні монстри.
- [HyperRogue Wiki](https://hyperrogue.miraheze.org/wiki/Main_Page) — [Orbs](https://hyperrogue.miraheze.org/wiki/Orbs), [Icy Land](https://hyperrogue.miraheze.org/wiki/Icy_Land), [Graveyard](https://hyperrogue.miraheze.org/wiki/Graveyard), [Hall of Mirrors](https://hyperrogue.miraheze.org/wiki/Hall_of_Mirrors), [Hell](https://hyperrogue.miraheze.org/wiki/Hell), [Orb of Yendor](https://hyperrogue.miraheze.org/wiki/Orb_of_Yendor).
- [Gallery of Lands](https://roguetemple.com/z/hyper/gallery.php) — коротко правила кожної землі.
- [WebGL-демо](https://roguetemple.com/z/hyper/online.php) — грати в браузері.
- YouTube: пошук «hyperrogue gameplay».

## Непевне
- (?) Поразка при відсутності легальних ходів — з памʼяті; вікі говорить лише про блокування ходів під атаку.
- (?) Клавіші (numpad/vi на 7 напрямків, `.`/`s` чекати, Esc → quest status) і склад HUD — з памʼяті.
- (?) Casual-режим (згадка в Hell: «40 lands») — деталі не читались.
- (?) Мінне поле: чи числа рахують усіх сусідів клітини (6/7) — з памʼяті за аналогією з сапером.
- (?) Steam-сторінку прямо не бачив — дано пошук.
