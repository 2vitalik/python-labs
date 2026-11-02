---
title: Supaplex
slug: supaplex
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
year: 1991
platforms: [Amiga, MS-DOS, Windows (Megaplex/clones), web]
links:
  - {kind: fandom, url: "https://elmerproductions.com/sp/cast.html", best: true, note: "«Cast»: кожен елемент з властивостями (destructible/edible/movable) і правилами гравітації"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Supaplex", note: "історія, 111 рівнів, пропуск 3 рівнів, SpeedFix"}
  - {kind: play, url: "https://www.megaplex.website/docs/exit", note: "Megaplex Online: гра в браузері + база знань елементів, редактор, демо"}
  - {kind: fandom, url: "https://elmerproductions.com/sp/tricks.html", note: "трюки й баги двіжка (обʼєкти між клітинами)"}
  - {kind: wiki, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/Supaplex.html", note: "огляд у bd-fans"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=supaplex+1991+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, gravity-fall, push-object, collect-quota, reach-exit, touch-death, environment-death, impassable-cells, chain-detonation, inventory-items, item-pickup, sequential-levels, player-camera, status-panel, goal-counter, replay, level-select, +dig-terrain, +roll-off-rounded, +explode-3x3, +wall-follower, +snap-action, +one-way-port, +gravity-toggle, +remote-detonation]
proposes: ["+trigger:enter", "+trigger:timer", "+cond:state", "+cond:facing", "+effect:fall", "+effect:roll", "+effect:explode", "+effect:set_state", "+role:terrain", "+role:gate", "+role:switch", "+role:hazard", "+card:timed-bomb-drop", "+card:lethal-state-cell", "+card:skip-level", "+feature:skip-level", "+window:hall-of-fame"]
author: opus
date: 2026-11-02
---

# Supaplex — Boulder Dash усередині мікросхеми: інфотрони, порти, дискети-бомби

## Суть
Мерфі «їсть» друковану плату, збирає квоту інфотронів і йде до виходу. База — фізика Boulder Dash (зонки-камені падають і скочуються, вороги тримаються стіни, вибухи 3×3), до якої додано **порти** (однобічні проходи лише для Мерфі), **гравітацію, що вмикається на рівні** (тоді падає й сам Мерфі), і три види **дискет-вибухівки** (падає й вибухає / підривається терміналом / носиш і кладеш). Таймера нема — рівні стають чистими логічними пазлами на вибухах і порядку дій.

## Поле і час
- Рівень — сітка 60×24, рамка з «hardware», камера скролить за Мерфі; внизу панель.
- Real-time, але **не повністю клітинний**: обʼєкти під час руху стоять між клітинами, що дає відомі баги-трюки.
- Гравітація — властивість рівня (вимк/увімк), її не видно; деякі однобічні порти її перемикають.
- Таймера рівня нема; смерть → рівень заново (життів нема).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мерфі | player | — | 4 напрямки; їсть базу/інфотрони/червоні диски; штовхає; snap пробілом; при гравітації падає |
| Base (плата) | terrain | їстівна | зникає, коли Мерфі проходить; інші обʼєкти крізь неї не проходять |
| Bug | hazard | активний/неактивний (іскра) | виглядає як base; зʼїсти в активний момент → смерть |
| Інфотрон | pickup | падає, круглий | падає і скочується з інфотронів/зонків/RAM; збирається проходом або snap |
| Зонк | object | падає, круглий | камінь: падає, скочується; штовхається лише вбік, по одному |
| Exit | gate | квота інфотронів | працює лише після квоти; може бути кілька; вибух його знищує |
| Snik-snak (ножиці) | enemy | — | ліворуч → прямо → праворуч; гине від падіння/вибуху → вибух 3×3 |
| Electron | enemy | — | як snik-snak; вибух 3×3 перетворює клітини (крім hardware) на інфотрони |
| Порт однобічний | gate | напрям; може перемикати гравітацію | Мерфі проходить лише з широкого боку на вузький |
| Порт двобічний / чотирибічний | gate | осі | двобічний — обидва напрямки; чотирибічний — прямо по обох осях, без повороту всередині; вороги не проходять |
| Оранжева дискета | object | — | падає (не скочується); вдарившись після падіння → вибух 3×3; штовхається вбік |
| Жовта дискета | object | — | не падає; штовхається в будь-який бік; вибухає від термінала, сусіднього вибуху чи інфотрона згори |
| Червона дискета | pickup | лічильник у інвентарі | Мерфі підбирає; кладе (пробіл) → вибух через кілька тіків |
| Термінал | switch | — | Мерфі входить → вибухають **усі** жовті дискети рівня |
| RAM-чип | static | круглий; руйнується | стіна, з якої скочуються зонки/інфотрони; вибух руйнує |
| Hardware | static | невразлива | стіна-рамка; не кругла; вибух не бере, електрон не перетворює |
| Вибух | hazard | 3×3 | смертельний; лишає порожнечу або інфотрони (від електрона й усього ланцюга від нього) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, empty|base|infotron|red_disk)` → ТО `move(murphy, dir)`; base → `set_cell(empty)`; інфотрон → `pickup`, `counter(infotrons_left, -1)`; червоний диск → `give(murphy, red_disk)`.
- КОЛИ `input(space+dir)` → ТО `custom: «snap: зʼїсти/взяти сусіднє, не рухаючись»`.
- КОЛИ `contact(murphy, zonk)` горизонтально → ЯКЩО `free(cell_behind)` → ТО `push`; вертикально — `block`.
- КОЛИ `contact(murphy, yellow_disk)` → ЯКЩО `free(cell_behind)` → ТО `push` (будь-який напрямок); оранжевий — лише вбік.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(zonk|infotron|orange_disk)`; ЯКЩО `state(level, gravity_on)` → ТО також `fall(murphy)`.
- КОЛИ `tick` → ЯКЩО `cell(below, zonk|infotron|ram)` and `free(side)` and `free(side_below)` → ТО `roll(zonk|infotron, side)`; з hardware не скочуються.
- КОЛИ `contact(falling zonk|infotron, murphy)` → ТО `lose`; КОЛИ `contact(falling zonk|infotron, snik_snak|electron)` → ТО `explode(3×3)`.
- КОЛИ `contact(falling orange_disk, any)` → ТО `explode(3×3, empty)`.
- КОЛИ `contact(falling infotron, yellow_disk)` → ТО `explode(3×3)`; зонк на жовтій — нічого.
- КОЛИ `contact(murphy, terminal)` → ТО `custom: «explode усі yellow_disk рівня»` (`remote-detonation`).
- КОЛИ `input(hold space)` → ЯКЩО `has(murphy, red_disk)` → ТО `spawn(red_disk_armed)`, `take(murphy, red_disk)`; КОЛИ `timer(delay)` → ТО `explode(3×3)`.
- КОЛИ `explode(cells)` → ТО усе, крім hardware, знищується; ЯКЩО джерело — electron (або ланцюг від нього) → ТО `set_cell(infotron)`; інакше `set_cell(empty)`. Вибухові обʼєкти в зоні підриваються (`chain-detonation`).
- КОЛИ `contact(murphy, port)` → ЯКЩО `custom: «вхід з дозволеного боку»` and `free(cell_after_port)` → ТО `move(murphy, 2)`; ЯКЩО порт гравітаційний → ТО `set_state(level, gravity, flip)`.
- КОЛИ `contact(snik_snak|electron, port)` → ТО `block`.
- КОЛИ `tick` → ТО `custom: «snik-snak/electron: ліворуч вільно → поворот ліворуч; прямо вільно → крок; інакше поворот праворуч»`.
- КОЛИ `contact(snik_snak|electron, murphy)` → ТО `lose`, `explode(3×3)`.
- КОЛИ `rng(p)` → ТО `set_state(bug, active, short)`; КОЛИ `contact(murphy, bug)` → ЯКЩО `state(bug, active)` → ТО `lose`; інакше як base.
- КОЛИ `contact(murphy, exit)` → ЯКЩО `counter(infotrons_left, <=, 0)` → ТО `win`, `next_level`; інакше нічого.
- Перемога: квота інфотронів + вихід. Поразка: ворог, вибух, падаючий обʼєкт, рухомий обʼєкт «в лоб» → рестарт рівня. Знищені всі виходи → рівень нерозвʼязний.

## Керування і ввід
- Стрілки — рух; пробіл + стрілка — snap (дія без руху); утримати пробіл — покласти червону дискету.
- Right Shift — показати кількість червоних дискет; Esc — здатись і рестарт рівня; пауза (?).
- Варіанти: джойстик; у Megaplex — швидкість гри Z/X, покадрово N, сегменти-збереження S/L.

## Вікна, меню, HUD
- `main-menu`: список гравців (новий/видалити/пропустити рівень) · список рівнів зі статусом (пройдено/пропущено) · рейтинг гравців · Hall of Fame рівня (найкращий час) · демо · керування/звук · титри.
- `game-screen`: поле зі скролом; нижня панель — імʼя гравця, номер і назва рівня, `remaining-counter` інфотронів, `timer-elapsed`.
- `custom-window` «Hard luck» (Megaplex): рестарт / пропустити / завантажити сегмент.
- `replay-window`: демо-записи проходжень.
- Переходи: меню → рівень → (вихід) → меню з наступним рівнем; смерть → рестарт рівня.

## Фічі поза полем
- `levels-sequential`: 111 рівнів строго по порядку; `level-unlock`: до 3 рівнів можна пропустити (скіп «у борг»).
- Кілька профілів гравців з прогресом і часом проходження (`save-slots`, `stats`).
- `replay`: демо-файли проходжень (ранні — вшиті у гру; фанатські демо як «доказ» розвʼязку).
- `level-editor` / `level-sharing`: фанатські редактори й набори рівнів (Megaplex, sple.me).
- SpeedFix — патч, що прибрав залежність швидкості від процесора й додав опції.

## Варіації й родичі
- Батько — Boulder Dash; Emerald Mine (схожі динаміт і кислота); Rocks'n'Diamonds відтворює Supaplex-елементи; Megaplex/Megaplex Online — фанатське продовження з новими елементами (Zonker, Anti-zonk, Plasma, Negaton, Green Disk).
- **Осі варіацій**: вибухівка — «падає й рветься від удару / підриваєш дистанційно / носиш і кладеш з таймером»; прохід — «звичайна клітина / однобічний порт / порт з перемиканням гравітації»; гравітація — «лише для обʼєктів / і для аватара».

## Цікавинки для курсу
- Порти: прохід лише з певного боку + «перестрибування» через клітину — 📎.
- Гравітація як перемикач рівня (і для гравця) — 🥉: та сама логіка падіння на аватар, лазити можна лише «з'їдаючи» base.
- Три дискети — три способи детонації (удар, дистанційний сигнал, таймер) на одному вибуху 3×3 — 🥉.
- Electron: вибух, що перетворює клітини на ресурс, і «зараження» ланцюга — 📎 поверх вибуху.
- Bug — клітина, смертельна лише в активному стані за випадковим таймером — 🌱.
- Пропуск до 3 рівнів як мʼякий замок прогресії — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `push-object` · `collect-quota` ↔ інфотрони · `reach-exit` · `touch-death` · `environment-death` · `impassable-cells` (hardware, порти для ворогів) · `chain-detonation` · `inventory-items` + `item-pickup` ↔ червоні дискети · `sequential-levels` · `level-select` · `replay` ↔ демо · `player-camera` · `status-panel` · `goal-counter`.
- **Нема** → пропозиції карток:
  - `+one-way-port` «Однобічний прохід» · entities/legality · 📎 · слот {dirs} — прохідний лише з напрямку, лише для типу.
  - `+gravity-toggle` «Перемикач гравітації» · entities/move · 🥉 — гравітація для аватара вмикається клітиною.
  - `+remote-detonation` «Дистанційний підрив» · entities/combat · 📎 — термінал → усі жовті дискети.
  - `+timed-bomb-drop` «Покласти бомбу з таймером» · entities/combat · 📎 · слот {delay} — червона дискета (родич Bomberman).
  - `+lethal-state-cell` «Клітина, смертельна в стані» · entities/death · 🌱 · слот {period}.
  - `+skip-level` «Пропуск рівня з лімітом» · levels/progression · 🌱 · слот {max_skips}.
  - Повтори з Boulder Dash: `+dig-terrain`, `+roll-off-rounded`, `+explode-3x3` (слот into: empty|infotron), `+wall-follower`, `+snap-action`.

## Пропозиції до словників
- `+trigger:enter` ⏳ (base, порт), `+trigger:timer` ✅ уже є — для червоної дискети як таймера після події пропоную `timer(after, n)`.
- `+cond:state` ⏳ (гравітація рівня, активний bug), `+cond:facing` ⏳ (з якого боку вхід у порт).
- `+effect:fall` ⏳, `+effect:roll`, `+effect:explode(area, into)`, `+effect:set_state` ⏳ (гравітація рівня).
- `+role:terrain` (base), `+role:gate` (порти, exit), `+role:switch` (термінал), `+role:hazard` (bug, вибух) — усі ⏳.
- `+feature:skip-level` — пропустити рівень, лишивши «борг» (ліміт 3).
- `+window:hall-of-fame` — найкращі часи на конкретному рівні (не загальна `leaderboard`).

## Джерела
- ⭐ [Elmer Productions — Supaplex cast](https://elmerproductions.com/sp/cast.html) — усі елементи з правилами: падіння/скочування, порти, три дискети, вибухи електрона, гравітація.
- [Wikipedia](https://en.wikipedia.org/wiki/Supaplex) — 111 рівнів, пропуск 3, не повністю клітинний рух, SpeedFix.
- [Megaplex Online](https://www.megaplex.website/docs/exit) — гра в браузері, база знань елементів, керування (snap, червона дискета), демо, редактор.
- [Elmer Productions — tricks](https://elmerproductions.com/sp/tricks.html) — трюки й баги двіжка.
- [bd-fans: Supaplex](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/Supaplex.html) — огляд у спільноті Boulder Dash.

## Непевне
- (?) Розмір рівня 60×24 — з памʼяті; джерела, які читав, розміру не дають.
- (?) Склад головного меню (рейтинг, Hall of Fame, статистика, демо) і нижньої панелі (лічильник інфотронів, час) — з памʼяті про DOS-версію; перевірено лише HUD Megaplex.
- (?) Затримка вибуху червоної дискети в тіках і пауза в оригіналі — не знайшов.
- (?) Чи може оранжева дискета вибухнути від штовхання/сусіднього вибуху — джерела кажуть лише про удар після падіння.
- Вікі каже, що жовту дискету можна штовхати в будь-який бік, але «не тягнути»; cast — «по одній» — суперечності нема, але деталі руху вгору при гравітації не перевірив.
