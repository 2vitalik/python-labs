---
title: "Captain Toad: Treasure Tracker"
slug: captain-toad-treasure-tracker
aka: [Captain Toad, "Susume! Kinopio Taichō", Treasure Tracker]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 2014
platforms: [Wii U, Switch, 3DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Captain_Toad:_Treasure_Tracker", best: true, note: "діорами без стрибка, обертання камери, тач і гіроскоп, 2 HP, епізоди, Pixel Toad, порти, кооп, DLC"}
  - {kind: fandom, url: "https://www.mariowiki.com/Captain_Toad:_Treasure_Tracker", note: "керування й камера, предмети, 3 самоцвіти на рівень, бонус-ціль, обʼєкти й вороги, 79 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Captain+Toad+Treasure+Tracker+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, ladder-climb, item-pickup, key-and-door, teleport-pair, button-toggle, carrier-platform, timed-despawn, destructible-blocks, projectile-shot, temporary-modes, touch-death, environment-death, player-death, respawn, enemy-patrol, chase-player, collect-all, reach-exit, extra-life-threshold, level-select, sequential-levels, world-map, time-bonus, game-screen, end-screen, pause-menu, player-camera, mode-indicator, +no-jump-avatar, +rotate-view-to-solve, +touch-move-platform, +freeze-when-watched, +bonus-objective, +hidden-object-hunt, +mirror-clone, +assist-after-deaths, +coop-pointer]
proposes: ["+trigger:watched_by(a, b)", "+effect:rotate_camera(deg)", "+effect:pluck(cell)", "+feature:assist-after-deaths", "+feature:bonus-objective", "+card:no-jump-avatar", "+card:rotate-view-to-solve", "+card:freeze-when-watched", "+card:touch-move-platform", "+axis:control=world-touch"]
author: opus
date: 2026-11-09
---

# Captain Toad: Treasure Tracker — герой, що не вміє стрибати, обходить кубічні діорами, а камеру гравець крутить, щоб побачити шлях

## Суть
79 маленьких рівнів-«мініуніверсумів»: кубічна діорама, яку видно цілком і яку можна обертати й наближати. Toad (пізніше й Toadette) не стрибає через важкий рюкзак — лише ходить, біжить, лізе драбинами, висмикує ріпу й кидає її. Пазл — знайти маршрут до Power Star: прихований за кутом прохід, платформа, яку рухаєш дотиком, перемикачі, що перебудовують рівень. Додаткові цілі — 3 Super Gems і бонус-завдання на рівень.

## Поле і час
- Рівень — тривимірна блокова діорама (сітка кубів з пандусами, драбинами, трубами); камера орбітальна навколо діорами.
- Камера: обертання стиком/гіроскопом, крок L/R — 45°, ZL — за спину героя, X — наблизити/віддалити; без камери частину проходів не видно.
- Real-time, гравітація (падіння з уступу), але без стрибка; таймера рівня нема, є опційний цільовий час.
- Інформація часткова лише через кут огляду — схованки за стінами, під блоками, у грядках.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Captain Toad / Toadette | player | Small / Super; життя | ходить, біжить, драбини, висмикує й кидає; не стрибає |
| Грядка (Pluck Patch) | container | вміст | висмикнути: ріпа, монети, бонус |
| Ріпа (Turnip) | projectile | — | кидок по дузі, вбиває ворогів |
| Велетенська ріпа | projectile | — | лише проти боса Wingo |
| Монета / стос монет | pickup | 1 / 5 | 100 монет = +1 життя |
| Золотий гриб | pickup | — | дає монети |
| 1-Up гриб | pickup | +1 життя | — |
| Super Mushroom | pickup | — | Small → Super (переживає удар); у Super — 10 монет |
| Подвійна вишня | pickup | — | клон, що повторює рухи гравця |
| Гриб невразливості | pickup | на рівень | невразливість до кінця рівня |
| Super Pickax | pickup | тимчасово | вбиває будь-якого ворога, ламає цеглу |
| Ключ / Key Coin | pickup | 5 монет-ключів | ключ — Key Door; 5 Key Coin розблоковують Warp Box |
| Super Gem | pickup | 3 на рівень | для 100 % |
| Power Star | static | 1 на рівень | ціль рівня |
| Assist Pluck Patch | container | після 5 смертей у рівні | дає гриб невразливості |
| Donut Block | terrain | — | повільно падає під вагою |
| Brick / Rock Block | object | міцність | ламаються (кирка, ріпа) |
| P Panel | switch | група | усі натиснуті одночасно → Super Gem |
| P Switch / Pull Switch | switch | — | змінює розкладку рівня / піднімає шматок ґрунту |
| Spinwheel | switch | — | повертає частину рівня або весь рівень |
| Seesaw / Multi-Vator | terrain | вага / кількість | нахил за положенням / рушає, коли стоїть N персонажів |
| Touchstone | terrain | — | рухається від дотику до екрана |
| Turning Floor / Flip Panel / Dash Panel | terrain | — | крутить / тимчасовий шлях / ривок |
| Turnip Cannon / Mine Cart | object | — | стріляє ріпою; вагонетка по рейках з видом від першої особи й стрільбою ріпою |
| Warp Pipe / Clear Pipe / Warp Box | static | пара | переносять у іншу частину рівня |
| Shy Guy (червоний) | enemy | маршрут | ходить шляхом; помітивши — переслідує |
| Shy Guy (блакитний) | enemy | — | стоїть, повертається на 90° кожні кілька секунд; помітивши — переслідує |
| Goomba / Goomba Tower | enemy | висота | біжить на гравця |
| Boo / Big Boo | enemy | — | летить до гравця; завмирає, коли на нього дивляться |
| Peepa | enemy | маршрут | рухається за схемою, перекриває шлях |
| Piranha Plant / Creeper / Sprout | enemy | — | кусає / довге стебло / плює бомби й ховається |
| Stumper | neutral | невразливий | на ньому можна стояти й переїхати |
| Mud Trooper | enemy | — | помітивши — повільно переслідує; ліхтар тимчасово вимикає |
| Лава, отрута | hazard | — | миттєва втрата життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(toad, dir)`; з уступу — `fall(toad)`; стрибка нема — `custom: «піднятись можна лише драбиною, ліфтом, трубою»`.
- КОЛИ `input(camera)` → ТО `custom: «обертання камери навколо діорами на 45° / вільно»` — поле не змінюється, змінюється видимість.
- КОЛИ `input(pluck)` → ЯКЩО `occupied(here, pluck_patch)` → ТО `spawn(content)`; ріпа — в руки.
- КОЛИ `input(throw)` → ЯКЩО `has(toad, turnip)` → ТО `spawn(turnip)`; КОЛИ `contact(turnip, enemy)` → ТО `disappear_both`.
- КОЛИ `input(touch, cell)` → ЯКЩО `occupied(cell, touchstone)` → ТО `move(touchstone, dir)`.
- КОЛИ `input(lamp)` → ТО `stun(mud_trooper, n)` і `custom: «у темних рівнях Shy Guy біжать на світло»`.
- КОЛИ `line_of_sight(shy_guy, toad)` → ТО `custom: «ворог переходить у погоню»`.
- КОЛИ `custom: «камера/гравець дивиться на Boo»` → ТО `freeze(boo)`; інакше `move(boo, toward toad)`.
- КОЛИ `contact(enemy|hazard, toad)` → ЯКЩО `state(toad, super)` → ТО `transform(toad, small)`; ЯКЩО `state(toad, small)` → ТО `lives(-1)`, `restart`.
- КОЛИ `enter(toad, lava|poison)` → ТО `lives(-1)`.
- КОЛИ `contact(toad, double_cherry)` → ТО `clone(toad)` — клон дублює ввід.
- КОЛИ `contact(toad, pickax)` → ТО `set_state(toad, pickax, dur)`; у стані — `custom: «удар знищує ворога / цеглу»`.
- КОЛИ `custom: «усі P Panel групи натиснуті одночасно»` → ТО `spawn(super_gem)`.
- КОЛИ `count(chars_on_multivator, >=, n)` → ТО `move(multivator, dir)`.
- КОЛИ `contact(toad, key)` → ТО `pickup`; КОЛИ `contact(toad, key_door)` → ЯКЩО `has(toad, key)` → ТО `disappear_b`.
- КОЛИ `counter(key_coins, =, 5)` → ТО `transform(warp_box_locked, warp_box)`.
- КОЛИ `counter(coins, =, 100)` → ТО `lives(+1)`.
- КОЛИ `counter(deaths_in_level, =, 5)` → ТО `spawn(assist_pluck_patch)`.
- КОЛИ `contact(toad, power_star)` → ТО `win`, `next_level`.
- Перемога: Power Star. Поразка: 0 життів → кінець гри. Рахунок нема; фіксуються найбільше монет і час, 3 самоцвіти й бонус-ціль — для 100 %.

## Керування і ввід
- Стік — рух; кнопки — біг, висмикнути/кинути, ліхтар, зум; правий стік / хрестовина / нахил — камера; L/R — крок 45°, ZL — за спину.
- Wii U: дотик до екрана GamePad рухає платформи й оглушує ворогів, подув у мікрофон рухає деякі платформи, гіроскоп — приціл у вагонетці.
- Switch: у док-режимі — курсор з гіроскопом замість дотику; кооп — 2-й гравець курсором допомагає й кидає ріпу або керує другим Toad.
- 3DS: стилус + два екрани, стерео-3D.

## Вікна, меню, HUD
- `main-menu` → `level-select`: книга епізодів, сторінка = рівень з позначками 3 самоцвітів, бонус-цілі й рекордів (?).
- `game-screen`: діорама + HUD: `lives`, монети, зібрані самоцвіти (?), стан Small/Super.
- `pause-menu` (?) · `end-screen`: Power Star, підсумок самоцвітів і бонус-цілі.
- `custom-window`: «Хованки» з Pixel Toad — знайти піксельного Toad у рівні (з amiibo — за 10 с в оригіналі).
- Переходи: книга → рівень → зірка → книга; після 1-го проходження відкривається бонус-ціль рівня.

## Фічі поза полем
- Прогресія: 3 епізоди за складністю (18 / 18 / 28 рівнів) + бонус-епізод; рівні відкриваються послідовно, частина — за кількістю самоцвітів (?).
- Бонус-ціль після першого проходження («без шкоди», «зібрати 70 монет»), опційний цільовий час.
- Допомога: після 5 смертей у рівні — грядка з невразливістю.
- amiibo: Pixel Toad, бонусні рівні Odyssey; DLC 2019 — 18 рівнів у 5 курсах; кооп на Switch.

## Варіації й родичі
- Міні-рівні Captain Toad у Super Mario 3D World — першоджерело.
- [Kula World](kula-world.md) — обертання світу навколо героя; [Pushmo](pushmo.md) — діорама як пазл; [Super Mario Maker](super-mario-maker.md) — та сама вселена.
- Осі: **вертикаль** (стрибок / лише драбини й ліфти); **хто керує камерою** (гравець — частина пазла / фіксована); **ввід у світ** (лише аватар / ще й дотик до обʼєктів).

## Цікавинки для курсу
- Аватар без стрибка: рух вгору — лише через драбини, ліфти, труби; BFS по 3D-сітці — 🥉.
- Обертання камери навколо діорами з кроком 45° як частина пошуку шляху — 🥈.
- Boo завмирає, коли на нього дивишся (умова від напряму камери/героя) — 📎.
- Вороги з конусом огляду: помітив → погоня — 🥉.
- Подвійна вишня: клон повторює ввід гравця — 📎.
- Плита-ліфт, що рушає, коли на ній N персонажів — 🌱.
- Допомога після 5 смертей у рівні (assist-грядка) — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `ladder-climb` · `item-pickup` · `key-and-door` · `teleport-pair` (труби) · `button-toggle` (P Switch, Pull Switch) · `carrier-platform` (Turning Floor, ліфти) · `timed-despawn` (Donut Block) · `destructible-blocks` · `projectile-shot` (ріпа) · `temporary-modes` (кирка, невразливість) · `touch-death` · `environment-death` · `player-death` · `respawn` · `enemy-patrol` · `chase-player` · `collect-all` (самоцвіти) · `reach-exit` (зірка) · `extra-life-threshold` (100 монет) · `level-select` · `sequential-levels` · `world-map` (книга) · `time-bonus` (цільовий час) · `game-screen` · `end-screen` · `pause-menu` · `player-camera` · `mode-indicator`.
- **Нема** → пропозиції карток:
  - `+no-jump-avatar` «Аватар без стрибка: вертикаль лише через обʼєкти» · entities/move · 🌱.
  - `+rotate-view-to-solve` «Обертання камери відкриває приховані проходи» · interface/render · 🥈.
  - `+touch-move-platform` «Рух обʼєкта поля прямим дотиком гравця» · interface/input · 📎.
  - `+freeze-when-watched` «Ворог завмирає, коли на нього дивляться» · entities/move · 📎.
  - `+bonus-objective` «Додаткова ціль рівня після першого проходження» · game-logic/win · 🌱.
  - `+hidden-object-hunt` «Знайти схований обʼєкт у рівні за час» · game-logic/win · 🌱.
  - `+mirror-clone` «Клон повторює рухи гравця» · entities/move · 📎.
  - `+assist-after-deaths` «Допомога після N смертей» · game-logic/difficulty · 🌱.
  - `+coop-pointer` «Другий гравець — курсор-помічник» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+trigger:watched_by(a, b)` — A у полі зору B / камери (Boo).
- `+effect:rotate_camera(deg)` — повернути камеру навколо поля без зміни стану.
- `+effect:pluck(cell)` — висмикнути вміст клітини-грядки в руки.
- `+feature:assist-after-deaths`, `+feature:bonus-objective` — див. вище.
- `+axis:control=world-touch` — гравець торкається обʼєктів поля напряму, крім керування аватаром.
- `+card:no-jump-avatar`, `+card:rotate-view-to-solve`, `+card:freeze-when-watched`, `+card:touch-move-platform` — див. вище.

## Джерела
- ⭐ [Wikipedia: Captain Toad: Treasure Tracker](https://en.wikipedia.org/wiki/Captain_Toad:_Treasure_Tracker) — без стрибка, камера, тач/мікрофон/гіроскоп, 2 HP, епізоди, Pixel Toad, порти, кооп, DLC.
- [Super Mario Wiki](https://www.mariowiki.com/Captain_Toad:_Treasure_Tracker) — керування й камера, повний список предметів, обʼєктів і ворогів, 3 самоцвіти, бонус-ціль, цільовий час, 79 рівнів, assist-грядка.
- YouTube: пошук «Captain Toad Treasure Tracker gameplay».

## Непевне
- (?) HUD і меню-книга — з памʼяті; як саме відкриваються бонус-рівні.
- (?) «Конус огляду» Shy Guy — форма й дальність не вказані.
- (?) Boo завмирає від погляду героя чи камери — у Mario-серії від героя; у діорамі — неперевірено.
- (?) Чи смерть повертає до початку рівня чи до чекпойнта — Wikipedia: «рестарт рівня».
