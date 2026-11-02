---
title: Rocks'n'Diamonds
slug: rocks-n-diamonds
family: dig-gravity
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: runtime
  goal: collect
year: 1995
platforms: [Linux, Windows, macOS, MS-DOS, Android]
links:
  - {kind: official, url: "https://www.artsoft.org/rocksndiamonds/manual/reference.html", best: true, note: "Elements Reference: усі стандартні елементи, згруповані за поведінкою, з мітками походження BD/EM/SP/DC2/SB"}
  - {kind: official, url: "https://www.artsoft.org/rocksndiamonds/manual/tutorial.html", note: "Editor Tutorial: редактор, Custom Elements (сторінки змін), Group Elements"}
  - {kind: official, url: "https://www.artsoft.org/rocksndiamonds/manual/manual.html", note: "Program Manual: меню, setup, магнітофон (tapes), team mode, мережа"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rocks%27n%27Diamonds", note: "історія, порти, GPL, 50 000+ рівнів спільноти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rocks%27n%27diamonds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, push-object, collect-quota, all-on-targets, reach-exit, time-out, time-bonus, touch-death, environment-death, player-death, chain-detonation, key-and-door, teleport, cell-transform, interaction-table, impassable-cells, inventory-items, item-pickup, chase-player, row-conveyor, sequential-levels, level-unlock, level-select, score-records, replay, state-as-data, in-game-editor, editor-palette, editor-draw-tools, level-exchange, player-camera, status-panel, +dig-terrain, +roll-off-rounded, +explode-3x3, +wall-follower, +snap-action, +custom-element-rules, +group-element]
proposes: ["+trigger:enter", "+trigger:smashed", "+trigger:timer-delay", "+cond:prop", "+effect:explode", "+effect:change_into_area", "+effect:fall", "+role:custom", "+card:custom-element-rules", "+card:group-element", "+card:element-property-flags", "+card:engine-per-level", "+card:tape-rerecord", "+card:time-gate-wheel", "+card:game-of-life-wall", "+card:wind-drift", "+window:tape-recorder", "+feature:team-mode", "+axis:engine"]
author: opus
date: 2026-11-02
---

# Rocks'n'Diamonds — обʼєднаний двіжок rocks-and-diamonds, де елемент — це запис властивостей

## Суть
Гравець, як у Boulder Dash, копає пісок, збирає самоцвіти, штовхає камені й тікає до виходу, але **один двіжок** відтворює елементи Boulder Dash, Emerald Mine (і Emerald Mine Club), Supaplex, Sokoban, Diamond Caves 2 та DX Boulder Dash. Ключова ідея для курсу: елемент — не клас із кодом, а **набір властивостей** (копається, штовхається, падає, слизький, вибуховий, збирається, смертельний на дотик) плюс до 32 «сторінок змін» у 256 Custom Elements — умова → «перетворитись на». Редактор рівнів, магнітофон-реплей і 50 000+ рівнів спільноти зробили гру архівом жанру.

## Поле і час
- Прямокутна сітка довільного розміру (задається в INFO рівня), камера скролить за гравцем; у team mode — за «фокусним» гравцем.
- Один шар елементів; стан (падає, напрямок руху, CE-лічильник, затримка зміни) живе в клітині.
- **Двіжок обирається на рівень** (INFO-сторінка редактора): RnD-двіжок підтримує всі елементи й «асинхронний» — рух може початися будь-коли; EM-двіжок підтримує лише EM/EMC-елементи і синхронний — тік кожні 8 кадрів при 50 кадр/с. У новіших версіях є й інші (?) (SP, MM).
- Таймер рівня (може бути вимкнений), квота самоцвітів; у Sokoban-рівні замість квоти — усі обʼєкти на полях.

## Сутності
Довідник групує елементи за поведінкою; нижче — групи з представниками (повний перелік — сотні елементів (?), див. Reference).

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Rockford ×4 кольори) | player | до 4; гравітація гравця вимк/увімк | рух 4 напрямки, копає, штовхає, snap, кладе динаміт; падає лише при player gravity |
| Пісок / трава / база (SP) / fake grass | terrain | diggable | гравець проходить → порожньо; snap — прибрати без руху |
| Камінь EM / камінь BD | object | pushable, falling | падає; EM-камінь лише звичайне штовхання, BD — ще й snap-push |
| Самоцвіти: BD-алмаз, смарагд, кольорові, інфотрон — 1; EM-алмаз — 3; перлина — 5; кристал — 8 | pickup | вартість у «смарагдах», falling, slippery | падають, з них скочується; збір → мінус до квоти |
| Горіх (nut) | container | вміст: смарагд | камінь згори розколює → смарагд; вибух знищує вміст |
| Стіни: звичайна, сталь, слизька, BD/EM-варіанти, текстові (TXT) | static | destructible / indestructible, slippery | непрохідні; сталь EM/EMC пропускає «зісковзування» самоцвітів, горіхів ні |
| Невидимі стіна/сталь/пісок + вимикач світла, лінза | static | — | поводяться як видимі, показуються лише при світлі |
| Вихідні двері (кілька стилів) | gate | квота | відкриваються, коли лічильник самоцвітів = 0 |
| Ключі й двері (RnD, EM, сірі EM, DC2) ×4 кольори | gate | колір | EM-двері прохідні наскрізь, стояти в них не можна, клітина за ними має бути вільна |
| Порти SP: однобічні, гравітаційні, двобічні, чотирибічні | static | напрям | гравець проходить, але не стоїть; гравітаційний порт перемикає гравітацію |
| Труби (DX) | static | форма | гравець усередині невидимий і захищений, вихід обирає сам |
| Динаміт, динабомба, бомба EM | object | 3×3; динабомба — хрест 3+3 | бомба вибухає від удару/падіння/вибуху; динаміт кладеться і горить |
| Вороги на дотик: жук, космічний корабель, світлячок, метелик, рослина | enemy | 4 напрямки + random-start | тримаються правої/лівої сторони (жук/корабель); метелик/світлячок як у BD |
| Вороги на зіткнення: Yam-Yam, робот, Pacman та ін. | enemy | вміст при вибуху | Yam-Yam іде прямо до упору, їсть EM-алмази; робот іде до найближчого гравця |
| Колесо робота | switch | час обертання | роботи ігнорують гравців і йдуть до колеса, доки воно крутиться |
| Амеби: звичайна, BD, крапельна | hazard | — | ростуть / кидають краплі; крапля падає, вбиває, приземлившись стає амебою |
| Магічна стіна (BD, EM), сипучий пісок | switch | стиль виходу | EM: смарагд → EM-алмаз → камінь → смарагд; BD-стіна завжди віддає BD-стиль |
| Кислота (EM) | hazard | басейн зі слизькими краями | знищує все, що впало, включно з гравцем (щит не рятує) |
| Time Gate + колеса | gate + switch | 10 с за замовчуванням | ворота відкриті, доки крутиться хоч одне колесо; таймер від останньої активації |
| Конвеєри (DC2) ×4 кольори + перемикачі | terrain + switch | ліво/стоп/право | несуть падаючі обʼєкти; перемикач по колу «ліво–стоп–право–стоп»; камінь теж перемикає |
| Повітряні кулі + пульти вітру (EMC) | object | напрям вітру з INFO | дрейфують за вітром; гравець може штовхати проти вітру |
| Пружина + бампер (EMC) | object | — | штовхнута їде до упору / відбивається; давить роботів |
| Magic Ball (EMC) | spawner | вміст | після вмикання періодично спавнить вміст; усі кулі перемикаються разом |
| Живі стіни: Game of Life, Biomaze | hazard | оновлення кожні 0,5 с | клітинний автомат Конвея (виживання 2–3, народження 3); у Life гравець рахується клітиною |
| Лампи-чекпоінти | switch | — | усі невідвідані треба відвідати до відкриття виходу |
| Sokoban-обʼєкт і поле | object + static | — | чистий Sokoban, якщо інших елементів нема; інакше — звичайний рівень із виходом |
| Custom Element ×256 | custom | CONFIG + до 32 сторінок змін | поводиться як задано властивостями й правилами змін |
| Group Element ×32 | custom | до 16 елементів, choice type | заглушка: при розміщенні/зміні обирає елемент групи (random, loop, linear, pingpong) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cond:prop(target, diggable)` → ТО `move`, `set_cell(empty)`; ЯКЩО `prop(target, walkable)` → `move`; ЯКЩО `prop(target, passable)` (порт, EM-двері) → `custom: «перейти на клітину за ним»`.
- КОЛИ `input(snap+dir)` → ТО `custom: «snap»`: підібрати/прибрати сусіднє без руху; для BD-каменя — snap-push.
- КОЛИ `contact(player, pushable)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(player, collectible)` → ТО `pickup`, `counter(gems_needed, -value)`.
- КОЛИ `tick` → ЯКЩО `prop(a, falling)` and `free(below)` → ТО `fall(a)`.
- КОЛИ `tick` → ЯКЩО `state(a, falling)` and `prop(below, slippery)` → ТО `roll(a, left|right)` у вільний бік.
- КОЛИ `trigger:smashed(a)` (впало згори) → ЯКЩО `a = nut` → ТО `transform(emerald)`; `a = EM diamond` → `disappear_a`; `a = bomb|player|bug…` → `explode`.
- КОЛИ `explode(a)` → ТО `explode(3×3, into: content(a))`; `chain-detonation` для вибухових сусідів; індестрактибл не зачіпає; жук → 1 алмаз + 8 смарагдів.
- КОЛИ `contact(falling gem|rock, magic_wall)` → ТО `transform(next_in_cycle)` під стіною.
- КОЛИ `enter(any, acid)` → ТО `disappear_a` (гравець — `lose`).
- КОЛИ `input(drop)` (утримання) → ЯКЩО `has(player, dynamite)` → ТО `spawn(burning_dynamite)`, `timer(fuse)` → `explode`.
- КОЛИ `contact(player, robot_wheel)` → ТО `set_state(wheel, spinning, t)`; роботи `custom: «ціль = колесо»`; повторне натискання таймер не скидає.
- КОЛИ `contact(player, timegate_wheel)` → ТО `set_state(time_gates, open, 10s)` від останньої активації.
- КОЛИ `contact(player|rock, belt_switch)` → ТО `set_state(belts[color], next_of(left, stop, right, stop))`.
- КОЛИ `timer(0.5s)` → ТО `custom: «Game of Life: клітина з 2–3 сусідами живе, порожня/копана з 3 — народжується»`.
- КОЛИ `counter(gems_needed, ==, 0)` and `all lamps visited` → ТО `set_state(exit, open)`; КОЛИ `contact(player, exit)` → `win`, `score(time_left)`.
- КОЛИ `all_on(sb_object, sb_field)` → ТО `win` (Sokoban-рівень).
- **Custom Element** (сторінка зміни): КОЛИ `timer-delay(CE DELAY [+RANDOM])` | `contact` «TOUCHED BY PLAYER» | `smashed` «SMASHED (FROM ABOVE)» | непрямо «PLAYER TOUCHES» / «TOUCHING» інший елемент (з фільтрами сторони/гравця/сторінки) → ТО `transform(«ELEMENT CHANGES TO»)` або `explode` («EXPLODE INSTEAD OF CHANGE»); розширено — `change_into_area(3×3)` з «REPLACE WHEN» (порожнє / руйнівне), «REPLACE ALL OR NOTHING», «USE RANDOM REPLACE %».
- Перемога: квота + вихід (або Sokoban-умова). Поразка: падіння/вибух/ворог/кислота/час → рівень знову. Рахунок: таблиця очок рівня + залишок часу; рекорди в Hall of Fame.

## Керування і ввід
- Стрілки — рух; Left Ctrl + стрілка — snap; Right Ctrl — drop (динаміт, утримання для EM-динаміту); Space — старт/пауза.
- До 4 гравців на одній машині (окремі пристрої в INPUT DEVICES) або мережа клієнт–сервер (`rocksndiamonds -n`); «ONLY MOVE FOCUSED PLAYER» — один ввід керує кількома гравцями по черзі.
- Магнітофон: F1 — точка збереження, F2 — відновлення; кнопки EJECT/STOP/PAUSE/RECORD/PLAY.

## Вікна, меню, HUD
- `main-menu`: NAME · LEVELSET · HALL OF FAME · LEVEL CREATOR · INFO SCREEN · START GAME · SETUP · QUIT.
- `level-select` (LEVELSET) — дерево наборів рівнів (групи через `levelinfo.conf`), поточний/перший/останній рівень.
- `leaderboard` (HALL OF FAME) — рекорди по рівню.
- `help-window` / `codex-window` (INFO SCREEN) — довідка по елементах, музика, титри.
- `settings-window` (SETUP): GAME & MENU (TEAM-MODE, HANDICAP, SKIP UNSOLVED LEVELS, TIME LIMIT, AUTO RECORD TAPES) · EDITOR · GRAPHICS · SOUND & MUSIC · CUSTOM ARTWORK · INPUT DEVICES · KEY SHORTCUTS · EXIT / SAVE AND EXIT.
- `game-screen`: поле + бічна панель: `remaining-counter` (самоцвітів треба), `inventory-bar` (ключі, динаміт), `score`, `timer-countdown`, `level-number`; під нею — `custom-window` «магнітофон» з лічильником кадрів і станом запису/відтворення.
- `editor-window` (LEVEL CREATOR): палітра елементів (`element-picker`, секції CE/GE), інструменти малювання, сторінки INFO рівня і ELEMENT SETTINGS (INFO · CONFIG 1/2 · CHANGE) для кожного CE.
- `confirm-dialog` — вихід/ESC з підтвердженням.
- Переходи: main-menu → START GAME → game-screen → (рівень пройдено) → наступний / Hall of Fame; LEVEL CREATOR → editor-window → «playtest» → game-screen.

## Фічі поза полем
- `level-editor` з двома рівнями глибини: розставити елементи і **запрограмувати** нові (CE/GE) без коду — головна фіча.
- `replay` як магнітофон: кожна спроба пишеться автоматично; можна відмотати на будь-який кадр і перезаписати далі — `rewind` + ветвлення.
- `level-unlock` (HANDICAP: наступний рівень після розвʼязання) · `levels-sequential` · `leaderboard-local`.
- `local-multiplayer` / `online-multiplayer` (TEAM-MODE до 4; мережа лише на RnD-двіжку).
- `custom-skins` / `mod-support`: власні графіка, звуки, музика (CUSTOM ARTWORK з OVERRIDE).
- `level-sharing`: набори рівнів — теки з `levelinfo.conf`; 50 000+ рівнів спільноти.

## Варіації й родичі
- Предки, чиї елементи імпортовано: Boulder Dash, Emerald Mine (+ Emerald Mine Club), Supaplex, Sokoban, Diamond Caves 2, DX Boulder Dash; двіжок виріс з Mirror Magic II того ж автора.
- Родичі-«енциклопедії»: GDash (точний BD-емулятор), Diamond Caves, Chip's Challenge 2 (теж редактор + різні набори правил).
- **Осі варіацій**: стиль одного елемента (BD- vs EM-камінь: snap-push є/нема; BD- vs EM-магічна стіна: стиль виходу); двіжок синхронний (EM, тік 8 кадрів) vs асинхронний (RnD); елемент вшитий vs CE (дані + правила).

## Цікавинки для курсу
- Елемент як **запис властивостей** (diggable, pushable, falling, slippery, explosive, collectible, deadly) і загальний двіжок, що читає ці прапорці — 🥈: рефакторинг «класи → таблиця даних».
- Custom Element: сторінки змін «тригер → перетворитись / вибухнути / замінити 3×3» з затримкою й випадковістю — 🥇: маленька мова правил, інтерпретатор у двіжку.
- Group Element: заглушка «одне з N» з режимами random/loop/pingpong — 📎.
- Магнітофон з перемотуванням і перезаписом від будь-якого кадру — 🥇: детермінізм + ввід як дані.
- Game of Life як стіна в рівні (автомат тікає раз на 0,5 с, гравець — клітина) — 🥉.
- Два двіжки за перемикачем рівня (синхронний / асинхронний) — 🥇.
- Конвеєри з перемикачем «ліво–стоп–право–стоп» за кольором — 📎.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-quota` (самоцвіти з вагою 1/3/5/8) · `all-on-targets` (Sokoban) · `reach-exit` · `time-out` + `time-bonus` · `touch-death` · `environment-death` (кислота, камінь) · `player-death` · `chain-detonation` (динабомба — хрест 3+3) · `key-and-door` · `teleport` (через CE «Player Triggering Change») · `cell-transform` (магічна стіна, горіх) · `interaction-table` (довідник властивостей) · `impassable-cells` · `inventory-items` (динаміт, ключі) · `item-pickup` · `chase-player` (робот) · `row-conveyor` (конвеєри) · `sequential-levels` + `level-unlock` + `level-select` · `score-records` · `replay` · `state-as-data` · `in-game-editor` + `editor-palette` + `editor-draw-tools` · `level-exchange` · `player-camera` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+custom-element-rules` «Елемент, заданий правилами змін» · entities/interact · 🥇 · слоти {trigger, delay, target, area} — міні-мова поведінки в редакторі.
  - `+group-element` «Група-заглушка з вибором» · levels/editor · 📎 · слот {choice: random|loop|linear|pingpong}.
  - `+element-property-flags` «Поведінка з прапорців властивостей» · code/architecture · 🥈 — дитина `interaction-table`.
  - `+engine-per-level` «Набір правил на рівень» · game-logic · 🥇 — як MS/Lynx у Chip's Challenge.
  - `+tape-rerecord` «Реплей з перемотуванням і перезаписом» · interface/results · 🥇 — дитина `replay`.
  - `+time-gate-wheel` «Ворота, відкриті на час» · entities/interact · 📎 · слот {seconds}.
  - `+game-of-life-wall` «Клітинний автомат у рівні» · entities/spawn · 🥉 · слот {rule: life|biomaze}.
  - `+wind-drift` «Обʼєкти дрейфують за вітром» · entities/move · 📎.
  - `+dig-terrain`, `+roll-off-rounded`, `+explode-3x3`, `+wall-follower`, `+snap-action` — повтор з Boulder Dash.

## Пропозиції до словників
- `+trigger:enter` ⏳ — вхід у кислоту, порт, трубу.
- `+trigger:smashed(a)` — на A впав обʼєкт згори (горіх, бомба, CE «SMASHED»); не те саме, що `contact`.
- `+trigger:timer-delay` — відкладена зміна власної клітини через N (+random) тіків (CE DELAY).
- `+cond:prop(a, flag)` — сутність має прапорець властивості (diggable, slippery, explosive…).
- `+effect:explode(area, into)` — повтор з Boulder Dash; `+effect:change_into_area(3×3, policy)` — заміна області за правилами «всі або нічого / % випадково»; `+effect:fall` ⏳.
- `+role:custom` — сутність, чия роль визначається даними рівня (CE).
- `+window:tape-recorder` — панель магнітофона на ігровому екрані.
- `+feature:team-mode` — до 4 гравців в одному рівні, локально або мережею.
- `+axis:engine` — який набір правил (двіжок) застосовано до рівня.

## Джерела
- ⭐ [Elements Reference](https://www.artsoft.org/rocksndiamonds/manual/reference.html) — групи елементів, властивості, ваги самоцвітів, двіжки RnD/EM, порти, конвеєри, Game of Life, CE/GE коротко.
- [Editor Tutorial](https://www.artsoft.org/rocksndiamonds/manual/tutorial.html) — 256 CE, 32 сторінки змін, «ELEMENT CHANGES TO», розширена ціль 3×3, 32 GE по 16 елементів.
- [Program Manual](https://www.artsoft.org/rocksndiamonds/manual/manual.html) — головне меню, SETUP, клавіші, магнітофон, team mode, мережа.
- [Wikipedia](https://en.wikipedia.org/wiki/Rocks%27n%27Diamonds) — Holger Schemel, 1995, GPL, порти, 50 000+ рівнів.
- YouTube: пошук «rocks'n'diamonds gameplay».

## Непевне
- (?) Загальна кількість стандартних елементів («сотні») — у джерелах числа не знайшов.
- (?) Повний список тригерів CE (pushed, dug, collected, hit by, explosion of, counter…) — у Tutorial бачив лише TOUCHED BY PLAYER, SMASHED, PLAYER TOUCHES, TOUCHING, CE DELAY; решта — з памʼяті.
- (?) Двіжки SP і MM (Mirror Magic) як окремі варіанти вибору в INFO — у прочитаних сторінках прямо названо лише RnD і EM.
- (?) Деталі Yam-Yam (поворот після упору — випадковий?) і швидкість росту амеб — не перевірено.
