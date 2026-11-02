---
title: Lode Runner
slug: lode-runner
family: grid-platformer
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 1983
platforms: [Apple II, Atari 8-bit, C64, VIC-20, PC, NES, arcade (Irem 1984), PC Engine, Steam (Legacy 2017)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner", best: true, note: "правила копання, вартові, золото, редактор, усі версії"}
  - {kind: play, url: "https://archive.org/details/arcade_ldrun", note: "Internet Arcade — аркадна версія Irem у браузері"}
  - {kind: other, url: "https://mocagh.org/broderbund/masksun-loderunner-loderunner-manual.pdf", note: "мануал Championship Lode Runner (правила як в оригіналі): клавіші, Ctrl-команди, очки, рекорди"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=lode+runner", note: "пошук; Lode Runner Legacy"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lode+runner+apple+ii+gameplay", note: "пошук; геймплей оригіналу"}
stage: v2
coverage: 75
mechanics: [move-4dir, gravity-fall, collect-all, reach-exit, touch-death, environment-death, player-death, chase-player, respawn, spawn-random-cell, cell-transform, timed-despawn, impassable-cells, event-points, score-records, sequential-levels, level-select, game-pause, status-panel, in-game-editor, editor-palette, editor-playtest, +dig-hole, +hole-refill, +ladder-climb, +hang-bar, +trapdoor-fake-floor, +reveal-exit-ladder, +enemy-carries-item, +stand-on-enemy]
proposes: ["+effect:dig", "+effect:restore_cell", "+trigger:all_collected", "+cond:supported", "+effect:reveal_cells", "+role:ladder", "+feature:level-editor", "+card:dig-hole"]
author: opus
date: 2026-11-02
---

# Lode Runner — збери все золото, копаючи ями ліворуч і праворуч, щоб у них падали вартові

## Суть
Бігун на одному екрані з цегли, драбин і перекладин збирає всі злитки, тікаючи від вартових. Стрибати не можна — лише бігати, лазити, висіти на перекладині й **копати яму в цеглі зліва або справа знизу**. Яма за кілька секунд заростає: вартовий у ній застрягає, а якщо не встиг вилізти — гине й зʼявляється знову вгорі. Коли золото зібране, проявляються приховані драбини до верхнього краю — вихід. 150 рівнів і вбудований редактор («Game Generator»).

## Поле і час
- Один нескролений екран-сітка (оригінал ≈ 28×16 клітин (?)); аркада Irem — менша сітка 24×15; NES — скрол.
- Гравітація клітинна: сутність без опори (цегла, драбина, перекладина, голова вартового) падає на клітину вниз щотік; падіння з будь-якої висоти безпечне.
- Real-time з фіксованим тіком; швидкість гри налаштовується клавішами під час гри.
- Клітина має тип (порожньо, цегла, бетон, драбина, перекладина, пастка, прихована драбина) + стан цегли (ціла / викопана з таймером).
- Інформація часткова: пастки (фальш-цегла) виглядають як цегла, приховані драбини невидимі до кінця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун | player | 5 життів на старті, +1 за рівень | біг, лазіння, висіння, падіння, копання ліворуч/праворуч униз; стрибати й вилазити з ями не може |
| Цегла | terrain | ціла / яма (таймер) | копається; через N тіків заростає |
| Бетон (bedrock) | static | — | не копається, непрохідний |
| Драбина | terrain | — | рух угору/вниз; опора |
| Перекладина (bar) | terrain | — | рух уздовж «руками»; вниз — зістрибнути |
| Пастка (trapdoor) | terrain | виглядає як цегла | не тримає: усі провалюються крізь неї |
| Прихована драбина | terrain | прихована | зʼявляється, коли зібрано все золото |
| Золото | pickup | — | збирає бігун; вартовий може підняти й нести |
| Вартовий | enemy | несе ≤ 1 злитка (злиток у нього невидимий) | переслідує; дотик — смерть бігуна; падає в ями, вилазить, якщо яма не заросла |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` і (`cell(here, ladder)` для вгору) → ТО `move(runner, dir)`; на перекладині — лише ліво/право, вниз = відпустити.
- КОЛИ `tick` → ЯКЩО `not supported(a)` (опора: цегла, бетон, драбина, перекладина, голова вартового) → ТО `fall(a)` на 1 (для бігуна і вартових).
- КОЛИ `input(dig_left|dig_right)` → ЯКЩО `cell(below_side, brick)` і `free(side)` → ТО `set_cell(below_side, hole)`, `custom: «таймер заростання»`. Під себе копати не можна.
- КОЛИ `timer(refill)` для ями → ТО `set_cell(hole, brick)`; ЯКЩО `occupied(hole, runner)` → `lose`; ЯКЩО `occupied(hole, guard)` → `disappear_b`, `score(n)`, `respawn(guard, near_top)`.
- КОЛИ `enter(guard, hole)` → ТО `set_state(guard, trapped)`; ЯКЩО `has(guard, gold)` → ТО `custom: «кидає злиток на клітину над ямою»`; через кілька тіків `custom: «вилазить угору»`, якщо яма ще не заросла.
- КОЛИ `contact(runner, guard)` → ЯКЩО `custom: «бігун зверху на голові вартового»` → ТО вартовий — опора, можна пройти по головах застряглих (рух униз з голови — смерть); інакше `lose`.
- КОЛИ `contact(guard, gold)` → ЯКЩО `not has(guard, gold)` → ТО `pickup` (злиток стає невидимим); `custom: «пізніше випадково кидає»` (?).
- КОЛИ `contact(runner, gold)` → ТО `pickup`, `score(250)` (?), `counter(gold_left, -1)`.
- КОЛИ `input(ctrl_a)` → ТО `lives(-1)`, `restart` — вихід із безвиході (вартовий зі злитком застряг у глухому куті).
- КОЛИ `counter(gold_left, ==, 0)` → ТО `reveal(hidden_ladders)`.
- КОЛИ `reach(runner, top_edge)` → ЯКЩО `counter(gold_left, ==, 0)` → ТО `win`, `lives(+1)`, `next_level`.
- КОЛИ `enter(a, trapdoor)` → ТО `fall(a)` — пастка не опора.
- Копання з драбини чи перекладини: копаєш, спускаєшся на ряд, копаєш знову — «шахта» вниз; кілька шарів цегли вимагають широкого проходу.
- Вартові: `chase-player` з простим евристичним вибором (не найкоротший шлях: на драбинах «відштовхуються»).
- Поразка: дотик вартового або яма заросла над бігуном → життя −1, рівень з початку; 0 життів → кінець. Рахунок: золото, застряглий вартовий, загиблий вартовий, рівень (Championship: 500 / 100 / 100 / 2000; оригінал — 250 / 75 / 75 / 1500 (?)).

## Керування і ввід
- Apple II: клавіатура (I/J/K/L — рух, U/O — копати ліворуч/праворуч) або джойстик (кнопка 0 — копати ліворуч, 1 — праворуч).
- Ctrl-команди (Apple): Ctrl-A — здатися при безвиході, Ctrl-R — завершити гру, Ctrl-S — звук, Ctrl-J/K — джойстик/клавіатура, Ctrl-X/Y — інверсія осей, окремі клавіші — повільніше/швидше; Esc — заморозити гру.
- Режим редактора: курсор по сітці + клавіша типу клітини (0–9) (?).

## Вікна, меню, HUD
- `splash-screen` / атракт: демо проходження рівнів.
- `main-menu` (Apple II): Play · Edit (Game Generator) · вибір стартового рівня (?).
- `game-screen` — поле + рядок унизу: `score`, `lives` («MEN»), `level-number`.
- `editor-window` (Game Generator): та сама сітка + курсор; палітра типів клітин; збереження рівня на диск, тест-гра.
- `leaderboard` — таблиця рекордів після game over, ім'я до 8 символів; Return показує її, Ctrl-C у демо — стирає.
- Переходи: splash → game-screen; game-screen → (вихід угору) наступний рівень; (смерть) той самий рівень; меню → editor-window → (play) game-screen з рівнем.

## Фічі поза полем
- `level-editor` — один із перших користувацьких редакторів у грі; рівні зберігаються на диск, `level-sharing` через дискети.
- `levels-sequential` 150 рівнів + вибір стартового рівня (`level-select`) (?).
- `speed-control` (швидкість гри), `sound-toggle`, `pause` (Esc), `remap-controls` (джойстик/клавіатура, інверсія осей, обмін кнопок копання).
- Legacy (2017): режими, кооператив, редактор з публікацією.

## Варіації й родичі
- Championship Lode Runner (1984, 50 складних рівнів, збереження гри Ctrl-S), Irem-аркада (1984, 24 рівні на 24×15, висіння на кінці драбини, розумніші вартові), NES/Famicom (Hudson, 50 рівнів, скрол, фрукти й овочі за очки), Lode Runner's Rescue (1985, 3-D перспектива), Lode Runner: The Legend Returns (1994, нові інструменти — бомби, газ (?)), Lode Runner 2 / 3-D (ізометрія і 3D).
- Родичі: Hard Hat Mack, Space Panic (копати ями ворогам), Dig Dug (копання), Boulder Dash (клітинна фізика), Mr. Robot.
- Осі: **де копати** (лише вбік-вниз / під себе / будь-куди); **що стається з ямою** (заростає за таймером / назавжди); **що роблять вороги з предметами** (ігнорують / несуть / кидають у ямі).

## Цікавинки для курсу
- Копання вбік-вниз + таймер заростання з перевіркою «хто всередині» — 🥉: тимчасова зміна клітини з наслідком.
- Клітинна гравітація з видами опор (цегла, драбина, перекладина, голова ворога) — 🥉.
- Вартовий з інвентарем на 1 злиток, що кидає його в ямі — 📎.
- Приховані драбини, що проявляються після «все зібрано» — 🌱.
- Пастка-фальшпідлога — 🌱.
- Game Generator: редактор сітки з тест-грою і збереженням у файл — 🥈 (`in-game-editor` + `editor-playtest`).
- AI вартових по драбинах/перекладинах (граф руху з гравітацією) — 🥇, якщо BFS по такому графу.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `collect-all` · `reach-exit` · `touch-death` · `environment-death` (яма заросла) · `player-death` · `chase-player` · `respawn` (вартовий угорі) · `spawn-random-cell` · `timed-despawn` (яма) · `cell-transform` · `impassable-cells` (бетон) · `event-points` · `sequential-levels` · `level-select` · `in-game-editor` · `editor-palette` · `editor-playtest` · `game-pause` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+dig-hole` «Копання ями вбік-вниз» · entities/interact · 🥉 · слот {sides: left|right|down}.
  - `+hole-refill` «Яма заростає за таймером» · entities/interact · 📎 · слот {delay}.
  - `+ladder-climb` «Драбини» · entities/move · 📎.
  - `+hang-bar` «Перекладина: висіти й рухатись» · entities/move · 📎.
  - `+trapdoor-fake-floor` «Фальшпідлога» · entities/legality · 🌱.
  - `+reveal-exit-ladder` «Вихід проявляється після збору» · game-logic/win · 🌱.
  - `+enemy-carries-item` «Ворог несе предмет» · entities/interact · 📎.
  - `+stand-on-enemy` «Ворог як опора» · entities/move · 📎.

## Пропозиції до словників
- `+effect:dig(cell, side)` — прибрати цеглу збоку внизу (тимчасово).
- `+effect:restore_cell(cell, after)` — повернути тип клітини через N тіків.
- `+trigger:all_collected(kind)` — зібрано все золото (окремо від `all_gone`: частину несуть вороги).
- `+cond:supported(a)` — під сутністю опора (цегла/драбина/перекладина/інша сутність).
- `+effect:reveal_cells(kind)` — проявити приховані клітини типу.
- `+role:ladder` — або `terrain` з прапорцем «можна лізти»; варто вирішити один раз для всіх платформерів.
- `+feature:level-editor` ↔ вже є в `features.md` — тут лише позначка, що редактор зберігає на диск і є в меню гри.
- `+card:dig-hole` — див. вище.

## Джерела
- ⭐ [Wikipedia: Lode Runner](https://en.wikipedia.org/wiki/Lode_Runner) — копання лише вбік, заростання ям, вартові з золотом і респавном угорі, опора на голові, редактор, 150 рівнів, усі версії.
- [Internet Arcade: Lode Runner](https://archive.org/details/arcade_ldrun) — аркада Irem у браузері; підтвердження драбини після золота.
- [Мануал Championship Lode Runner](https://mocagh.org/broderbund/masksun-loderunner-loderunner-manual.pdf) — «правила як у Lode Runner»: 5 життів, драбина після золота, невидимий злиток у вартового, клавіші IJKL/U/O, Ctrl-команди, очки Championship, рекорди.
- Steam: пошук «lode runner» — Lode Runner Legacy.
- YouTube: пошук «lode runner apple ii gameplay».

## Непевне
- (?) Розмір поля оригіналу 28×16 — з памʼяті.
- (?) Очки оригіналу 1983 (золото 250, вартовий 75 + 75, рівень 1500) — лише з пошукового підсумку про мануал Broderbund (PDF не відкрився); перевірені числа — з Championship (500/100/100/2000).
- (?) Клавіші й Ctrl-команди перевірені за мануалом Championship; що в оригіналі 1983 вони ті самі — припущення (мануал каже «rules are the same»).
- (?) Чи вартові кидають злиток випадково поза ямами — описи розходяться.
- (?) Вибір стартового рівня в оригіналі; інструменти Legend Returns (Wikipedia: лише «enhanced graphics and tools»).
