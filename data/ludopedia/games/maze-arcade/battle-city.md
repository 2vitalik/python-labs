---
title: Battle City (Танчики) і Tank Battalion
slug: battle-city
aka: [Танчики, Tank Battalion, Tank 1990, VS. Battle City, Tank Force]
family: maze-arcade
also: [tower-lanes]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 1985
platforms: [Famicom/NES, arcade (VS. System), Game Boy, Sharp X1, Wii/Wii U VC, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_City", best: true, note: "правила коротко: 20 танків, база, рельєф, бонуси, редактор"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Battle_City", note: "найповніше: типи танків з очками, 4-та/11-та/18-та бонусні, тривалості бонусів, зірки по рівнях"}
  - {kind: wiki, url: "https://uk.wikipedia.org/wiki/Battle_City", note: "UA-стаття: рельєф, бонуси, версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tank_Battalion", note: "аркадний предок 1980: 20 ворогів, база-орел"}
  - {kind: play, url: "https://retrogames.cz/play_014-NES.php", note: "NES-версія в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battle+city+nes+gameplay", note: "пошук; геймплей NES"}
stage: v1
coverage: 75
mechanics: [move-4dir, +facing-icon, projectile-shot, shoot-modes, shoot-forward, shoot-burst, projectile-collision, destructible-blocks, impassable-cells, floor-types, inertia-slide, hp-damage, speed-per-type, random-walk, spawn-points, spawn-schedule, spawn-animation, reinforcements, temporary-modes, item-pickup, respawn, player-death, enemy-reached-base, destroy-all-enemies, goal-counter, remaining-counter, status-panel, event-points, score-records, sequential-levels, progress-acceleration, in-game-editor, editor-palette, editor-window, main-menu, game-screen, end-screen, game-pause, +drop-on-death, +base-defense, +cover-tiles, +shot-through-water, +power-tiers, +screen-bomb, +freeze-enemies, +fortify-base, +local-coop]
proposes: ["+effect:shoot", "+effect:erode", "+role:base", "+role:cover", "+cond:tier", "+window:score-tally", "+card:subtile-destruction", "+card:bonus-carrier", "+card:decoy-ai"]
author: opus
date: 2026-11-09
---

# Battle City — захисти орла: танк проти 20 ворожих танків у лабіринті з цегли, яку розносять постріли

## Суть
Гравець керує танком на полі 13×13 блоків і мусить знищити 20 ворожих танків стадії, поки вони не розстріляли **базу-орла** внизу поля або сам танк. Цегляні стіни руйнуються постріл за пострілом (по чверті блока), сталеві — лише найсильнішим танком; кущі ховають, вода не пускає танки, але пропускає снаряди, лід ковзає. «Блимаючі» вороги лишають випадковий бонус: зірка (апгрейд гармати), граната (знищити всіх), годинник (заморозка), шолом (щит), лопата (сталь навколо бази), танк (+1 життя). Гра — суміш аркадного лабіринту і tower defense: ти водночас нападник і охоронець точки.

## Поле і час
- Поле 13×13 «блоків» (169 клітин), одна стадія = один екран, камера нерухома (NES). Праворуч — сіра бічна панель зі станом.
- Блок рельєфу ділиться на **чверті**: цегла руйнується частинами, тому стіна поступово «прогризається» з боку пострілу (базовий танк знімає чверть, 3-зірковий — половину).
- Real-time: танки й снаряди рухаються щокадру; вороги мають різні швидкості руху і снарядів.
- Згори — точки появи ворогів; знизу по центру — орел у цегляній «підкові», поруч старти гравців (1-й ліворуч, 2-й праворуч).
- Одночасно на полі ≤ 4 ворожих танки (у грі на двох — ≤ 6); решта — у резерві, показаному іконками на панелі.
- 35 стадій; далі вони повторюються з іншим набором ворогів і швидшою появою (кінця нема). Game Boy-версія: поле не влазить у екран — камера і радар.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк гравця 1 (жовтий) | player | життя, рівень зірок 0–3 | рух 4 напрямки, повертається в бік руху, стріляє вперед |
| Танк гравця 2 (зелений) | player | те саме | лише в режимі 2 PLAYERS, одночасно з першим |
| Снаряд | projectile | швидкість за рівнем/типом | летить прямо до перешкоди; знищує цеглу, танк, базу; зустрічний снаряд — обидва зникають |
| Орел (база) | base | 1 влучання | влучання будь-чийого снаряда (навіть свого) → кінець гри |
| Цегла | static | 4 чверті | руйнується частинами від пострілів обох сторін |
| Сталь (бетон) | static | — | непрохідна; руйнується лише снарядом 3-зіркового танка |
| Вода | terrain | — | непрохідна для танків, снаряди пролітають |
| Кущі (ліс) | terrain | — | прохідні; ховають танки й снаряди під собою |
| Лід | terrain | — | танк гравця ковзає ще трохи після відпускання керування |
| Простий танк (Basic) | enemy | 1 влучання · 100 очок | повільний, звичайний снаряд |
| Швидкий (бронетранспортер, Fast) | enemy | 1 влучання · 200 | найшвидший рух |
| Скорострільний (Power) | enemy | 1 влучання · 300 | швидкі снаряди |
| Важкий (Armor) | enemy | 4 влучання · 400 | міняє колір із кожним влучанням |
| Блимаючий танк | enemy (стан) | 4-й, 11-й і 18-й у стадії | влучання → бонус у випадковому місці; важкий блимаючий — бонус уже з першого влучання |
| Точка появи | spawner | кілька вгорі | ворог «проявляється» блиманням-зіркою, потім рушає |
| Зірка | pickup | 500 | +1 рівень гармати (до 3) |
| Граната | pickup | 500 | знищує всіх ворогів на екрані (очок за них не дає) |
| Годинник | pickup | 500 | заморожує всіх ворогів ≈10 с |
| Шолом | pickup | 500 | щит невразливості ≈10 с |
| Лопата | pickup | 500 | стіни навколо орла стають сталлю ≈20 с, потім — відбудована цегла |
| Танк-бонус | pickup | 500 | +1 життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `face(tank, dir)`; ЯКЩО `free(cell_ahead)` → ТО `move(tank, dir)`; інакше `block` (цегла, сталь, вода, інший танк).
- КОЛИ `input(fire)` → ЯКЩО `count(own_shot, <, max_shots)` (0–1 зірка: 1; 2–3 зірки: 2) → ТО `custom: «постріл вперед від гармати»` (`+effect:shoot`).
- КОЛИ `tick` → ТО `move(shot, dir)`; КОЛИ `edge(shot)` → ТО `disappear_a`.
- КОЛИ `contact(shot, brick)` → ТО `disappear_a`, `custom: «знищити 1 або 2 чверті цегли з боку удару»` (`+effect:erode`).
- КОЛИ `contact(shot, steel)` → ЯКЩО `state(shooter, stars=3)` → ТО `set_cell(empty)`; інакше `disappear_a`.
- КОЛИ `contact(shot, water|bush|ice)` → ТО `custom: «пролітає»` (кущі й лід ще й ховають снаряд).
- КОЛИ `contact(shot, shot)` → ТО `disappear_both` (дружній і ворожий снаряди гасять одне одного).
- КОЛИ `contact(player_shot, enemy)` → ТО `damage(1)`; КОЛИ `hp_zero(enemy)` → ТО `disappear_b`, `score(100|200|300|400)`, `explode(enemy)`.
- КОЛИ `contact(player_shot, enemy)` → ЯКЩО `state(enemy, flashing)` → ТО `clear_state(enemy, flashing)`, `spawn_at(bonus, random_cell)`.
- КОЛИ `spawned(flashing_enemy)` → ЯКЩО `count(bonus, >, 0)` → ТО `custom: «попередній бонус зникає»`.
- КОЛИ `contact(enemy_shot, player)` → ЯКЩО `not state(player, shield)` → ТО `lives(-1)`, `respawn(player, start)`, `custom: «зірки скидаються до 0»`, `set_state(player, shield, 3 s)`.
- КОЛИ `contact(any_shot, eagle)` → ТО `transform(eagle → broken_flag)`, `game_over`.
- КОЛИ `enter(player, ice)` → ТО `slide(player, dir)` на короткий відрізок після відпускання.
- КОЛИ `enter(tank, bush)` → ТО `custom: «малюється під кущем — невидимий»`.
- КОЛИ `contact(player, star)` → ТО `pickup`, `score(500)`, `custom: «рівень зірок +1: швидший снаряд → два снаряди → пробиває сталь і пів-цегли»`.
- КОЛИ `contact(player, grenade)` → ТО `pickup`, `score(500)`, `custom: «знищити всіх ворогів на екрані без очок»` — лічильник знищених росте.
- КОЛИ `contact(player, clock)` → ТО `pickup`, `score(500)`, `freeze(enemies, 10 s)`.
- КОЛИ `contact(player, helmet)` → ТО `pickup`, `score(500)`, `set_state(player, shield, 10 s)`.
- КОЛИ `contact(player, shovel)` → ТО `pickup`, `score(500)`, `set_cell(eagle_ring, steel)` на 20 с; КОЛИ `timer(20 s)` → ТО `set_cell(eagle_ring, brick)` (повністю відбудована цегла).
- КОЛИ `contact(player, tank_bonus)` → ТО `pickup`, `score(500)`, `lives(+1)`.
- КОЛИ `timer(spawn_delay)` → ЯКЩО `count(enemies_on_field, <, 4)` (6 у грі на двох) `and counter(reserve, >, 0)` → ТО `spawn_at(enemy, spawn_point)`, `counter(reserve, -1)`.
- КОЛИ `tick` → ТО ворог: `custom: «їде прямо; на розвилці чи впершись — випадковий новий напрям, з тяжінням до бази або гравця»` (?), `custom: «випадково стріляє вперед»`.
- КОЛИ `contact(enemy_shot, brick)` → ТО те саме руйнування, що й від гравця — вороги «прогризають» шлях до бази.
- КОЛИ `contact(player_shot, partner)` (2 гравці) → ТО `custom: «партнер не гине»`; `stun(partner, n)` (?).
- КОЛИ `counter(killed, ==, 20)` → ТО `window(score-tally)`, `next_level`.
- КОЛИ `counter(lives, ==, 0)` (усі гравці) → ТО `game_over`.
- Перемога: стадія — знищено 20 ворогів; гра безкінечна (стадії по колу). Поразка: орел знищений (будь-ким, і власним снарядом теж) або скінчились життя. Рахунок: 100/200/300/400 за танки, 500 за бонус; у грі на двох — +1000 тому, хто знищив більше за стадію (?).

## Керування і ввід
- Хрестовина — рух 4 напрямки (танк одразу повертає корпус, діагоналей нема); A/B — постріл.
- Start — пауза; Select — вибір пункту меню.
- На двох — два геймпади одночасно (кооператив у реальному часі, не hotseat).
- Редактор (Construction): курсор по сітці блоків, кнопка перебирає варіанти блока (цегла/сталь цілими й половинками, вода, кущі, лід, порожньо) (?).

## Вікна, меню, HUD
- `main-menu` — титул «BATTLE CITY», рахунок і рекорд, пункти `1 PLAYER` · `2 PLAYERS` · `CONSTRUCTION`.
- `custom-window` «STAGE N» — сіра заставка з номером стадії перед кожною стадією (?) вибір стадії на старті.
- `game-screen` — поле 13×13; права панель `status-panel`: `remaining-counter` (іконки танків резерву, гаснуть по одному), `lives` «IP/IIP», `level-number` (прапорець + номер стадії) (?).
- `+window:score-tally` — підсумок стадії: по кожному типу ворога кількість × очки, разом, рекорд (`end-screen`-подібне, між стадіями) (?).
- `end-screen` — напис «GAME OVER» на полі, далі таблиця й повернення в меню.
- `editor-window` (Construction) — порожнє поле з орлом і курсором; зібрана мапа грається через `1/2 PLAYER` (?).
- `pause-menu` — блимаючий «PAUSE» поверх поля.
- Переходи: main-menu → STAGE N → game-screen → (20 знищено) score-tally → STAGE N+1 …; game-screen → (орел/життя) GAME OVER → score-tally → main-menu; main-menu → CONSTRUCTION → editor-window → (Start) main-menu.

## Фічі поза полем
- `level-editor` — Construction mode, один із перших вбудованих редакторів у відеоіграх (Wikipedia); збереження на касету — лише у Famicom-версії з Data Recorder (?).
- `levels-sequential` — 35 стадій по колу, на другому колі вороги інші й з'являються швидше (`progress-acceleration`).
- `local-multiplayer` — кооператив на двох одночасно (+ змагальний бонус за більше знищених).
- `pause`, рекорд сесії (`score-records`) без збереження.

## Варіації й родичі
- **Tank Battalion (1980, аркада):** предок — 20 ворогів за раунд, вороги заходять згори, база-орел, руйнівні цегляні стіни; без бонусів і без кооперативу на двох (?).
- **Tank 1990 (піратський хак, 1989–1991)** — нові стадії й бонуси (пістолет = 3 зірки, що ще й зрізає кущі; човен — їхати по воді, при влучанні губиш човен замість життя); на Dendy — «Танчики».
- **Tank Force (Namco, 1991, аркада)** — спрощена аркадна версія; **VS. Battle City** — аркадна на VS. System.
- **Game Boy (1991)** — більше поле, камера і радар.
- Родичі за механіками: Bomberman (руйнівні блоки, бонуси з цегли), Wizard of Wor (стрільба в лабіринті, кооп-змагання), Berzerk (снаряд у лабіринті), Combat (Atari 2600, танкова дуель), Space Invaders (захисні бункери, що руйнуються частинами), tower defense (захист точки).
- **Осі варіацій:** що руйнує снаряд (нічого / цеглу / цеглу частинами / сталь за апгрейдом); що захищати (нічого / базу / ворота); звідки бонуси (з ворога / з цегли / за часом); кооп (нема / одночасний / друг = суперник); рельєф-модифікатори (вода пропускає снаряди, кущі ховають, лід ковзає).

## Цікавинки для курсу
- Снаряд як сутність із власним тіком + зіткнення снарядів між собою — 🥉 (окремий список сутностей, порядок оновлення, анігіляція).
- Цегла з чвертями: руйнування частинами залежно від напрямку удару і сили танка — 🥈 (підклітинна сітка, логіка «з якого боку»).
- Рельєф-матриця «прохідність танка × прохідність снаряда × видимість» (вода, кущі, лід, сталь) — 📎 (таблиця взаємодій як дані).
- Ворожі хвилі: резерв 20, ≤ 4 на полі, точки появи, блимаючі 4/11/18 з бонусом — 🥉 (спавн за розкладом + стан носія бонуса).
- Бонуси з таймером (заморозка, щит, сталь навколо бази з відбудовою цегли після) — 🥉 (тимчасові стани і відновлення клітин).
- Рівні гармати (зірки), що скидаються після смерті — 📎.
- Редактор рівнів Construction із запуском своєї мапи — 🥈 (палітра блоків + серіалізація).
- AI ворога «випадково + тяжіння до бази» і приманка, що відводить гравця від бази, — 🥈, якщо зробити два профілі (blocker/raider).

## Мапа на каталог
- Є: `move-4dir` · `projectile-shot` (снаряд) · `shoot-modes`/`shoot-forward`/`shoot-burst` (два снаряди з 2-ї зірки) · `projectile-collision` · `destructible-blocks` (цегла) · `impassable-cells` (сталь, вода) · `floor-types` (лід, кущі, вода) · `inertia-slide` (лід) · `hp-damage` (важкий танк 4 влучання) · `speed-per-type` · `random-walk` · `spawn-points` · `spawn-schedule` (≤4 на полі) · `spawn-animation` (зірка-поява) · `reinforcements` (+1 за знищеного, доки є резерв) · `temporary-modes` (шолом, годинник) · `item-pickup` · `respawn` · `player-death` · `enemy-reached-base` (влучання в орла) · `destroy-all-enemies` (20) · `goal-counter`/`remaining-counter` (іконки резерву) · `status-panel` · `event-points` · `score-records` · `sequential-levels` · `progress-acceleration` · `in-game-editor`/`editor-palette`/`editor-window` · `main-menu` · `game-screen` · `end-screen` · `game-pause`.
- `+facing-icon` і `+drop-on-death` — картки вже є в `catalog/tasks.yaml` (з тегом battle-city), але ще не в автоген `catalog-cards.md`.
- **Нема** → пропозиції карток:
  - `+base-defense` «Захисти базу» · game-logic/lose · 🌱 — обʼєкт на полі, знищення якого = поразка (ширше за `enemy-reached-base`: база гине і від свого снаряда).
  - `+cover-tiles` «Кущі ховають сутності» · entities/legality · 🌱 · слот {hides: tanks|shots|both}.
  - `+shot-through-water` «Клітина пропускає снаряди, але не танки» · entities/legality · 🌱 — окремі маски прохідності для ходу й пострілу.
  - `+subtile-destruction` «Блок руйнується частинами» · entities/interact · 🥈 · слоти {parts: 4, per_hit: 1|2}.
  - `+power-tiers` «Рівні зброї, що скидаються після смерті» · entities/state · 📎 · слот {tiers: list}.
  - `+screen-bomb` «Бонус знищує всіх ворогів на екрані» · entities/combat · 🌱.
  - `+freeze-enemies` «Бонус заморожує ворогів» · entities/state · 🌱 · слот {duration}.
  - `+fortify-base` «Тимчасове укріплення бази з відбудовою» · entities/interact · 📎 · слот {duration}.
  - `+bonus-carrier` «Ворог-носій бонуса за номером появи» · entities/spawn · 📎 · слот {indices: 4,11,18}.
  - `+decoy-ai` «Ворог-приманка відводить гравця від цілі» · entities/move · 🥈.
  - `+local-coop` «Двоє на одному полі одночасно» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+effect:shoot` — сутність випускає снаряд у напрямку погляду (Battle City, Berzerk, Wizard of Wor); зараз це `spawn(shot, facing)`, але постріл трапляється в корпусі постійно.
- `+effect:erode` — зняти частину клітини (чверть цегли) замість повного `set_cell` (Battle City, бункери Space Invaders).
- `+role:base` — обʼєкт, який гравець захищає; його втрата — поразка (орел; PvZ-будинок, TD-ядро).
- `+role:cover` — тло, що ховає сутності під собою, не впливаючи на рух (кущі).
- `+cond:tier` — рівень апгрейда сутності (зірки 0–3: сталь пробиває лише tier 3); зараз — через `state(a, stars=3)`.
- `+window:score-tally` — підсумок між стадіями з розбивкою очок за типами ворогів.
- `+card:subtile-destruction` — див. «Мапа на каталог».
- `+card:bonus-carrier`, `+card:decoy-ai` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Battle City](https://en.wikipedia.org/wiki/Battle_City) — 35 стадій 13×13, 20 танків, база, рельєф, блимаючі червоні танки з бонусом, редактор, версії.
- [Вікіпедія RU: Battle City](https://ru.wikipedia.org/wiki/Battle_City) — типи ворогів з очками, 4/11/18-й блимаючі, ≤4/6 на полі, тривалості годинника/шолома/лопати, рівні зірок, чверть/половина цегли, Tank 1990.
- [Вікіпедія UA: Battle City](https://uk.wikipedia.org/wiki/Battle_City) — рельєф і бонуси, платформи.
- [Wikipedia: Tank Battalion](https://en.wikipedia.org/wiki/Tank_Battalion) — аркадний предок 1980.
- [RetroGames.cz](https://retrogames.cz/play_014-NES.php) — NES-версія в браузері (у видачі пошуку).
- YouTube: пошук «battle city nes gameplay».
- Пошукові фрагменти StrategyWiki (`strategywiki.org/wiki/Battle_City/Walkthrough`, сайт віддає 403): снаряди гасять одне одного, стандартна стіна — 4 постріли.

## Непевне
- (?) Поведінка вдруге влученого партнера в грі на двох (заморозка на кілька секунд) — з памʼяті, у відкритих джерелах не знайдено.
- (?) +1000 очок тому, хто знищив більше за стадію, — лише з відгуку на MobyGames (у пошуку).
- (?) Точний AI ворогів (частка «до бази» / «до гравця» / випадково) — є лише загальна фраза Wikipedia про приманки.
- (?) Вигляд панелі (IP/IIP, прапорець) і екран підсумку з розбивкою за типами — з памʼяті.
- (?) Точний набір блоків у Construction і чи можна вибрати стадію на заставці «STAGE N».
- (?) Tank Battalion: відсутність бонусів і кооперативу, кількість снарядів — стаття Wikipedia цього не каже.
- (?) Рух танка кроками по пів-блока (вирівнювання до сітки при повороті) — з памʼяті.
