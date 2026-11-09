---
title: Montezuma's Revenge
slug: montezumas-revenge
aka: [Montezuma's Revenge featuring Panama Joe, Panama Joe, Помста Монтесуми]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: score
year: 1984
platforms: [Atari 2600, Atari 5200, Atari 8-bit, ColecoVision, C64, Apple II, ZX Spectrum, MS-DOS, Master System]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Montezuma%27s_Revenge_(video_game)", best: true, note: "піраміда з 99 кімнат на 9 поверхів, темні кімнати, інвентар, скарбниця, 9 рівнів складності"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%205200/Montezumas%20Revenge.TXT", note: "мануал Atari 5200: усі пастки, вороги, предмети, очки, життя"}
  - {kind: other, url: "https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Montezumas%20Revenge.txt", note: "мануал ColecoVision"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Montezuma%27s+Revenge+1984+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [gravity-fall, ladder-climb, key-and-door, inventory, inventory-items, inventory-limit, inventory-duration, temporary-modes, enemy-patrol, touch-death, environment-death, player-death, periodic-sink, carrier-platform, item-pickup, event-points, extra-life-threshold, difficulty-levels, sequential-levels, status-panel, game-screen, fog-of-war, +fall-height-kill, +flicker-barrier, +dark-room-light-item, +flip-screen-rooms, +colored-key-doors, +treasure-bonus-room]
proposes: ["+trigger:landed", "+cond:inventory_full", "+card:flicker-barrier", "+card:dark-room-light-item", "+card:flip-screen-rooms", "+card:colored-key-doors", "+card:treasure-bonus-room"]
author: opus
date: 2026-11-09
---

# Montezuma's Revenge — Панама Джо спускається підземною пірамідою з 99 кімнат: ключі кольорів, мерехтливі лазери, темрява і скарбниця внизу

## Суть
Флікскрін-платформер-лабіринт: піраміда з кімнат-екранів, звʼязаних дверима, драбинами й жердинами, і її треба пройти до скарбниці в центрі нижнього поверху. Ключі трьох кольорів відкривають двері свого кольору, меч убиває деяких ворогів, амулет на кілька секунд робить усіх нешкідливими, факел освітлює темні кімнати. Інвентар має 5 слотів — що брати і куди нести, і є головоломкою маршруту. Падіння з висоти вбиває, тож вертикальна навігація (драбини, ланцюги, жердини) — ядро руху.

## Поле і час
- Мапа — сітка кімнат: 9 поверхів + вхідна кімната зверху, 99 кімнат; кожна кімната — один нескролений екран, вигляд збоку.
- Перехід у сусідню кімнату — вихід за край екрана (flip-screen); жердина веде на поверх нижче.
- Real-time. Лазерні ворота й зникаюча підлога мерехтять з періодом; вороги рухаються своїм маршрутом.
- Видимість: нижні поверхи мають темні кімнати — без факела видно лише героя й предмети (?), на рівні 9 темно все.
- Рівні 1–9: той самий план, але міняються стіни/драбини, більше й швидших ворогів, менше факелів; рівень 1 — лише ліва половина піраміди, 2 — права, з 3 — уся.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Панама Джо | player | 6 життів | ходить, стрибає на місці / в напрямку руху, лазить драбинами й ланцюгами, зʼїжджає жердиною |
| Підлога | terrain | — | опора |
| Стіна | static | — | блокує |
| Драбина | terrain | — | лише вгору/вниз; на неї й з неї не можна стрибнути |
| Ланцюг / мотузка | terrain | — | застрибнути й лізти вгору/вниз |
| Жердина | terrain | — | застрибнути → зʼїхати на поверх нижче; промах — падіння |
| Конвеєр | terrain | напрямок | за ходом пришвидшує, проти — сповільнює; падіння з нього — смерть |
| Зникаюча підлога | terrain | період | блимає; у фазі «нема» — падіння |
| Вогняна яма | hazard | — | смерть при дотику |
| Лазерні ворота | hazard | період | вмикаються/вимикаються; пройти лише у фазі «вимк» |
| Двері червоні / сині / сірі | gate | колір | відкриваються ключем свого кольору (+300) |
| Ключ | pickup | колір, 50 очок | лягає в інвентар, витрачається на двері |
| Меч | pickup | 50 очок | у інвентарі; при дотику знищує череп або павука, витрачається (?) |
| Факел | pickup | 3000 очок | освітлює темні кімнати до кінця рівня |
| Амулет (у формі молотка) | pickup | 100 очок | вороги сірі й нешкідливі кілька секунд |
| Коштовність | pickup | 1000 очок | не потребує слота, але не береться, коли інвентар повний |
| Череп стрибучий | enemy | 2000 за знищення | підстрибує на місці — пройти під ним |
| Череп котючий | enemy | 2000 | котиться підлогою — перестрибнути |
| Змія | enemy | — | нерухома; меч не бере — лише перестрибнути |
| Павук | enemy | 3000 | ходить, лазить драбинами; меч знищує |
| Скарбниця | zone | таймер | ланцюги з коштовностями; час вийде — далі наступний рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(joe, dir)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` або `cell(here, chain)` → ТО `move(joe, up|down)`.
- КОЛИ `input(jump)` → ЯКЩО `not cell(here, ladder)` → ТО `custom: «стрибок на місці або в напрямку руху»`.
- КОЛИ `tick` → ЯКЩО `not custom: «є опора»` → ТО `fall(joe)`.
- КОЛИ `custom: «приземлився з висоти понад поріг»` → ТО `lives(-1)` (`+trigger:landed`).
- КОЛИ `contact(joe, pole)` → ТО `move(joe, floor_below)` — зʼїхати на поверх нижче.
- КОЛИ `edge(joe)` → ТО `custom: «перехід у сусідню кімнату з того боку»`.
- КОЛИ `tick` → ЯКЩО `cell(under, conveyor)` → ТО `speed(joe, ±n)` за/проти ходу.
- КОЛИ `timer(every)` → ТО `custom: «лазерні ворота і зникаюча підлога перемикають фазу»`.
- КОЛИ `contact(joe, laser)` → ЯКЩО `state(laser, on)` → ТО `lives(-1)`.
- КОЛИ `enter(joe, fire_pit)` → ТО `lives(-1)`.
- КОЛИ `contact(joe, item)` → ЯКЩО `custom: «у інвентарі < 5 предметів»` → ТО `pickup`, `score(n)`; інакше `block` (`+cond:inventory_full`).
- КОЛИ `contact(joe, door)` → ЯКЩО `has(joe, key_same_color)` → ТО `take(joe, key)`, `disappear_b`, `score(300)`; інакше `block`.
- КОЛИ `contact(joe, skull|spider)` → ЯКЩО `has(joe, sword)` → ТО `take(joe, sword)`, `disappear_b`, `score(2000|3000)`.
- КОЛИ `contact(joe, enemy)` → ЯКЩО `not has(joe, sword)` і `not state(enemies, harmless)` → ТО `lives(-1)`; ворог зникає (на рівнях 1–4).
- КОЛИ `contact(joe, snake)` → ТО `lives(-1)` — меч не допомагає.
- КОЛИ `picked(joe, amulet)` → ТО `set_state(enemies, harmless, few_seconds)`.
- КОЛИ `picked(joe, torch)` → ТО `custom: «темні кімнати видно до кінця рівня»`.
- КОЛИ `enter(joe, treasure_room)` → ТО `timer(start)`; КОЛИ `contact(joe, jewel)` → ТО `score(1000)`.
- КОЛИ `custom: «у скарбниці час вийшов або Джо став на жердину»` → ТО `next_level`.
- КОЛИ `counter(score, >=, 10000·k)` → ТО `lives(+1)` (з рівня 4 — кожні 20 000).
- Перемога: нема (9 рівнів і далі цикл (?)). Поразка: 0 життів. Рахунок: предмети, вороги, двері, коштовності.

## Керування і ввід
- Джойстик: ліво/право — хід; вгору/вниз — драбини й ланцюги; діагональ полегшує зійти з драбини.
- Кнопка — стрибок: стоячи — на місці, у русі — у напрямку.
- Перед грою (Atari 5200): клавіші 1/2/3 — стартовий рівень; START — нова гра.

## Вікна, меню, HUD
- `difficulty-select` — вибір стартового рівня 1–3 (кнопками консолі).
- `game-screen`: кімната + HUD: вікно інвентарю (`inventory-bar`, до 5 предметів), `lives` (капелюхи), `level-number`, `score`.
- Темна кімната — поле без тайлів (`fog-overlay`), доки нема факела.
- `custom-window`: скарбниця з таймером.
- `end-screen` — game over; на рівні 1 FIRE продовжує з того самого місця з 6 життями й нулем очок.

## Фічі поза полем
- `difficulty-presets`: 9 рівнів; 1–3 обирають на старті, 4–9 — лише через проходження.
- `continue`: на рівні 1 після game over — продовження з місця смерті.
- Збережень і паролів нема.

## Варіації й родичі
- Порти відрізняються кольорами ключів і розкладом (?); ремейк Montezuma's Return (1998, 3D) (?).
- Родичі в корпусі: [prince-of-persia](prince-of-persia.md) (пастки на клітинах, смерть від падіння), [kings-valley](kings-valley.md), [manic-miner](manic-miner.md), [spelunker](spelunker.md) (печера-мапа, ключі й двері).
- Нащадки: «метроїдванії» з мапою кімнат; відома як важкий бенчмарк для RL (розріджена нагорода).
- Осі: **предмет-ефект** (ключ/меч витрачаються, факел — до кінця рівня, амулет — на час); **хто смертельний** (меч бере черепи й павуків, не змій); **інвентар** (5 слотів, коштовності без слота).

## Цікавинки для курсу
- Двері кольорів + ключі в інвентарі з лімітом 5 — 📎 (планування маршруту).
- Мерехтливі лазери й підлога за таймером — 🌱.
- Флікскрін-мапа кімнат 9×N зі станом кожної кімнати — 🥉.
- Темні кімнати й факел, що діє до кінця рівня — 📎.
- Різні вороги — різна відповідь (пройти під / перестрибнути / мечем) — 🌱.
- Скарбниця: бонус-кімната з таймером, вихід на жердину — 🌱.
- Рівні складності як модифікації однієї мапи (стіни/драбини/вороги) — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `ladder-climb` · `key-and-door` · `inventory`, `inventory-items`, `inventory-limit` (5), `inventory-duration` (факел, амулет) · `temporary-modes` (амулет) · `enemy-patrol` · `touch-death`, `environment-death`, `player-death` · `periodic-sink` (зникаюча підлога) · `carrier-platform` (конвеєр) · `item-pickup` · `event-points` · `extra-life-threshold` · `difficulty-levels`, `sequential-levels` · `status-panel`, `game-screen` · `fog-of-war` (темні кімнати — найближче).
- **Нема** → пропозиції карток:
  - `+fall-height-kill` — як у Space Panic, тут для гравця.
  - `+flicker-barrier` «Барʼєр, що вмикається/вимикається за таймером» · entities/interact · 🌱 · слот {on, off}.
  - `+dark-room-light-item` «Темна кімната, видима лише з предметом-світлом» · interface/render · 📎.
  - `+flip-screen-rooms` «Мапа з кімнат-екранів, перехід за краєм» · levels/progression · 🥉.
  - `+colored-key-doors` «Кілька кольорів ключів і дверей» · entities/interact · 🌱 (нащадок `key-and-door`).
  - `+treasure-bonus-room` «Бонус-кімната з таймером у кінці рівня» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:landed(a, height)` — приземлення після падіння на N клітин (Montezuma, Manic Miner, Spelunker).
- `+cond:inventory_full(a)` — інвентар заповнено, предмет не береться (Montezuma, роглайки).
- `+card:flicker-barrier`, `+card:dark-room-light-item`, `+card:flip-screen-rooms`, `+card:colored-key-doors`, `+card:treasure-bonus-room` — див. вище.

## Джерела
- ⭐ [Wikipedia: Montezuma's Revenge](https://en.wikipedia.org/wiki/Montezuma%27s_Revenge_(video_game)) — 99 кімнат, 9 поверхів, темні кімнати, інвентар, скарбниця, рівні 1–9 (половини піраміди, вороги з рівня 5 не зникають).
- [Мануал Atari 5200](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Atari%205200/Montezumas%20Revenge.TXT) — керування, лазери, конвеєр, зникаюча підлога, двері 3 кольорів, жердини, ланцюги, вороги, предмети й очки, інвентар 5, 6 життів, бонусні життя.
- [Мануал ColecoVision](https://discmaster.textfiles.com/view/1886/1000gamemanuals.iso/Colecovision/Montezumas%20Revenge.txt) — меч 50 очок, черепи й павуки, факел.

## Непевне
- (?) Кольори дверей у різних портах (мануал 5200: червоні, сині, сірі).
- (?) Чи меч витрачається після одного ворога; тривалість амулету в секундах.
- (?) Що саме видно в темній кімнаті без факела.
- (?) Що після рівня 9 — повтор рівня 9 чи кінець.
- (?) Поріг висоти падіння в клітинах.
