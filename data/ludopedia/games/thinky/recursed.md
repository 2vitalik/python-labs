---
title: Recursed
slug: recursed
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: graph
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/497780/Recursed/", best: true, note: "трейлер + опис: скрині-кімнати, ключі, ящики, кристал, копіювання й знищення кімнат; 60+ рівнів, без смерті"}
  - {kind: other, url: "https://www.grospixels.com/site/recursed.php", note: "Grospixels (FR): найповніший розбір — керування, усі світи й механіки (вода, стійкі предмети, aqua mortua, глеки-спогади, ооблеки, казани), парадокси"}
  - {kind: other, url: "https://simbabbad.blogspot.com/2022/04/recursed-steam-portponky.html", note: "блог (FR): кімната як тимчасова копія моделі скрині, Knot/Loop/Attic, парадокс → бонус-рівень"}
  - {kind: play, url: "https://portponky.itch.io/recursed", note: "itch.io: та сама гра без Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Recursed+Portponky+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, keyboard-controls, gravity-fall, key-and-door, item-pickup, impassable-cells, floor-types, reach-exit, sequential-levels, level-unlock, save-progress, player-camera, teleport, +recursive-boxes, +enter-box, +room-reset-on-enter, +persistent-object, +throw-object, +carry-object, +flood-container, +float-block, +state-snapshot-jar, +mimic-pickup, +parallel-worlds, +paradox-bonus, +hint-item, +world-map]
proposes: ["+trigger:input", "+trigger:paradox", "+trigger:leave", "+cond:has", "+cond:state", "+cond:cell", "+effect:enter", "+effect:exit", "+effect:carry", "+effect:throw", "+effect:reset_room", "+effect:snapshot", "+effect:restore", "+effect:transform", "+effect:set_state", "+effect:flood", "+effect:message", "+role:container", "+role:terrain", "+window:map-window", "+feature:world-map", "+axis:field-nested", "+axis:session"]
author: opus
date: 2026-11-02
---

# Recursed — платформер, де скриня — це вхід у кімнату, кімнату можна винести назовні, а скриню — внести саму в себе

## Суть
Героїня бігає й стрибає по плоских кімнатах-сітках, носить і кидає предмети (ключі, блоки, скрині) і має дістати фіолетовий кристал рівня. Дверей між кімнатами нема: стрибнувши в **скриню**, потрапляєш у кімнату, яку вона містить; вихід — фіолетовий «димок» усередині. Кожен вхід створює свіжу копію кімнати за моделлю скрині, а вихід її знищує — тому предмети в скринях «нескінченні», а принесене всередину губиться. Скрині можна носити між кімнатами, перебудовуючи ієрархію вкладення; стійкі (зелені) предмети пам'ятають стан, і тоді скриня може опинитися всередині самої себе — **парадокс**, що кидає гравця в бонус-рівень.

## Поле і час
- Кожна кімната — невелика 2D-сітка «збоку» з гравітацією (стіни, платформи, ґрати, рідина). Камера показує поточну кімнату; фон змінюється з глибиною вкладення (цикл із 4 візерунків).
- Простір — **стек вкладення**: існують лише кімнати, що містять гравця (як матрьошка); вихід знищує внутрішню. Модель скрині може посилатися на кімнату-предка або на стартову кімнату — тоді вкладення нескінченне («Loop»).
- Real-time платформер (біг, стрибок, кидок), але без ворогів, смерті й таймера — фактично покроковий пазл у реальному часі.
- Ні випадковості, повна інформація.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Героїня | player | стрибок 3 клітини (з вантажем — 2) | біг, стрибок, взяти/поставити/кинути предмет (по одному), плавання |
| Кристал | pickup | — | мета рівня |
| Скриня | container | модель кімнати | стрибок у скриню → вхід у її кімнату; носиться, кидається, копіюється, знищується |
| Димок виходу (фіолетовий) | static | — | вихід із кімнати в батьківську (до скрині); точка появи при вході; кімната без димка — стартова |
| Ключ | pickup | будь-який до будь-яких ґрат | відкриває ґрати й витрачається |
| Ґрати | gate | — | зникають від ключа |
| Блок | object | — | носиться/кидається; підставка для стрибка |
| Стійкий предмет / скриня (зелений) | object / container | стан і позиція зберігаються | не скидається з кімнатою; не копіюється; у собі самій зникає з кімнати |
| Вода | terrain | — | у ній плавають; скриня у воді заливає свою кімнату |
| Пемза (білий блок) | object | — | плаває, рівень води відкриває/закриває проходи |
| Aqua mortua (червона рідина) | terrain | — | як вода + знімає стійкість з зелених предметів |
| Тріщина (зелений димок із зірками) | static | разова | дія без вантажу → стан кімнати записується в глек |
| Глек-спогад | container | записаний стан кімнати | стрибок у глек → повернення в той момент; вихід через димок розбиває глек |
| Оублек (зелений жетон) | object | — | коли героїня бере предмет, усі оублеки кімнати стають таким самим предметом |
| Казан | container | колір світу | переносить у паралельний світ (свій ланцюг вкладення); носиться, кидається, копіюється |
| Кільце | pickup | аудіоповідомлення | кинуте об стіну — грає підказку |
| Червоний вентилятор | terrain | — | у бонус-рівнях дме вгору, несе предмети |
| Липка стіна | static | — | у The Last Tapestry (?) поведінку не перевірено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(jump)` → ТО стрибок на 3 клітини; ЯКЩО `has(player, item)` → на 2.
- КОЛИ `input(action)` біля предмета → ЯКЩО руки вільні → ТО `carry(player, item)`; з вантажем — `custom: «поставити»` або `throw(item)`: летить по прямій до стіни, потім `fall`.
- КОЛИ `contact(player, chest)` стрибком у неї → ТО `enter(player, chest)`: `reset_room(model(chest))` — створюється свіжа копія кімнати, героїня зʼявляється біля димка, вантаж у руках переходить із нею.
- КОЛИ `input(action)` на димку → ТО `exit(player)`: героїня зʼявляється біля скрині в батьківській кімнаті, внутрішня кімната знищується разом із нестійкими предметами, залишеними в ній.
- КОЛИ предмет винесено зі скрині → ТО при наступному вході він знову є в кімнаті: скриня з предметом = «роздавач» копій.
- КОЛИ `contact(player, grate)` → ЯКЩО `has(player, key)` → ТО `disappear_b`, ключ витрачається; інакше `block`.
- КОЛИ стійкий предмет змінює стан/позицію → ТО `set_state(chest_model, rewritten)` — модель скрині запамʼятовує його.
- КОЛИ стійку скриню поміщено в її ж кімнату → ТО вона зникає з кімнати (`custom: «скриня в собі»`).
- КОЛИ стійку скриню вилучено з її місця в ланцюгу вкладення так, що кімнату-предка не відтворити → ТО `paradox` → `custom: «перехід у бонус-рівень (діамант/рубін)»`.
- КОЛИ `enter(chest, water|aqua_mortua)` → ТО `flood(room(chest))`.
- КОЛИ `enter(green_item, aqua_mortua)` → ТО `clear_state(item, persistent)`.
- КОЛИ `input(action)` на тріщині без вантажу → ТО `snapshot(room)` у глек, героїня виходить з глеком у руках; стрибок у глек → `restore(snapshot)`; вихід через димок → глек `disappear`.
- КОЛИ `input(action)` бере предмет X → ТО для всіх оублеків кімнати `transform(oublek → X)` (без стійкості).
- КОЛИ `contact(player, cauldron)` → ТО `teleport` у світ казана: перший раз — у початкову кімнату світу, далі — до останнього використаного казана.
- КОЛИ `contact(player, crystal)` → ТО `win`, повернення до вибору рівня.
- Смерті, ворогів і поразки нема; глухий кут → вийти з кімнати / рестарт рівня.

## Керування і ввід
- Дві кнопки + напрямки: стрибок і дія (взяти / поставити / кинути / вийти через димок / записати в глек).
- Багаторазові натискання стрибка — плавання у воді.
- Рестарт рівня; undo — не перевірено (?).

## Вікна, меню, HUD
- `main-menu` — продовжити, налаштування, вихід (?).
- `map-window` / `level-select` — світи (Woodland, Sewer, Dungeon, Ruins, Temple, The Void, плюс The Oobleck Conundrum, The Last Tapestry) і рівні в них (?).
- `game-screen` — поточна кімната, фон за глибиною вкладення; HUD мінімальний (?).
- `settings-window` — мова (9), звук, керування (?).
- Переходи: вибір рівня → кімната → (скриня) вкладена кімната → (димок) назад → (кристал) вибір рівня; парадокс → бонус-рівень → назад.

## Фічі поза полем
- `levels-sequential` у світах: Woodland 12 · Sewer 8 · Dungeon 10 · Ruins 10 · Temple 12 · The Void 6 + безкоштовні розширення The Oobleck Conundrum 16 (після Sewer) і The Last Tapestry 20 (після Ruins); 20 парадокс-бонусів (діаманти/рубіни) — `collectibles`, прихована кінцівка.
- `achievements`, `cloud-save`, trading cards (Steam); `localization` (9 мов).
- Редактора нема (Steam про нього мовчить).

## Варіації й родичі
- Patrick's Parabox ([patricks-parabox.md](patricks-parabox.md)) — ящики теж містять рівні, але: у Parabox вкладена сітка **одна й жива** (вміст рухається з ящиком і зберігається), а в Recursed кімната — **модель**, що створюється заново при кожному вході й знищується при виході; у Parabox самовкладення — легальна механіка (∞/ε), у Recursed — парадокс, що викидає з рівня; Parabox — покроковий Sokoban, Recursed — платформер з перенесенням і кидком.
- Braid (порівняння в рецензіях: незвичне ядро, доведене до логічного кінця), Sokosoko.
- **Осі варіацій:** вкладене поле — живе (Parabox) / модель-шаблон із ресетом (Recursed); самовкладення — механіка / парадокс; предмети — копіюються / стійкі; хто переходить між рівнями вкладення — гравець з вантажем / ящик з усім вмістом.

## Цікавинки для курсу
- Кімната як шаблон: вхід = deepcopy моделі, вихід = знищення копії — 🥈 (копія vs посилання в Python на живому прикладі).
- Стек вкладення кімнат замість карти — 🥈 (стек кадрів як ігрове поле; вихід = pop).
- Стійкі предмети, що переписують модель скрині, і виявлення парадоксу (скриня в собі, неможливо відтворити предка) — 🥇.
- Глек-спогад: знімок стану кімнати і відновлення — 🥉 (серіалізація стану, як undo-point у грі).
- Оублеки: «усі X стають тим, що ти взяв» — 📎.
- Скриня у воді заливає свою кімнату — 📎 (властивість контейнера впливає на вміст).
- Казани: кілька паралельних стеків-світів і телепорт «до останнього використаного» — 🥈.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `gravity-fall`; `key-and-door` ↔ ключ і ґрати; `item-pickup` ↔ кристал, предмети; `impassable-cells`; `floor-types` ↔ вода, aqua mortua, вентилятори; `reach-exit` ↔ кристал як фініш; `sequential-levels` + `level-unlock` + `save-progress`; `player-camera`; `teleport` (казани) — наближено.
- **Нема** → пропозиції карток:
  - `+recursive-boxes` «Ящик містить сітку-рівень» · entities/state · 🥇 (з Parabox).
  - `+enter-box` «Вхід у контейнер / вихід назовні» · entities/move · 🥈 (з Parabox).
  - `+room-reset-on-enter` «Кімната — модель, вхід створює свіжу копію» · entities/state · 🥈 — дитина `recursive-boxes`.
  - `+persistent-object` «Предмет, що зберігає стан між ресетами» · entities/state · 🥈.
  - `+carry-object` «Нести предмет у руках» · entities/state · 🥉 (родич `+carry-stack` з Bonfire Peaks).
  - `+throw-object` «Кинути предмет по прямій до стіни» · entities/move · 📎.
  - `+flood-container` «Контейнер у рідині заливає свій вміст» · entities/interact · 📎.
  - `+float-block` «Блок, що плаває на рівні рідини» · entities/move · 📎.
  - `+state-snapshot-jar` «Знімок стану як предмет» · entities/state · 🥉.
  - `+mimic-pickup` «Мімік-жетони стають взятим предметом» · entities/interact · 📎.
  - `+parallel-worlds` «Кілька паралельних полів, перехід між ними» · levels/format · 🥈.
  - `+paradox-bonus` «Парадокс веде в секретний рівень» · levels/progression · 🥉.
  - `+hint-item` «Предмет-підказка (аудіо при кидку)» · interface/hud · 🌱.
  - `+world-map` · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:input`; `+trigger:paradox` — неможливо відтворити ланцюг вкладення (з Parabox, друга гра); `+trigger:leave` — вихід з кімнати.
- `+cond:has` (ключ, вантаж), `+cond:state` (стійкий), `+cond:cell` (у рідині).
- `+effect:enter` / `+effect:exit` — зміна рівня вкладення (з Parabox); `+effect:carry`, `+effect:throw`; `+effect:reset_room` — відтворити кімнату з моделі; `+effect:snapshot` / `+effect:restore` — запис і повернення стану; `+effect:transform` (оублек); `+effect:set_state` / `clear_state` (стійкість); `+effect:flood`; `+effect:message` (кільце).
- `+role:container` (скриня, глек, казан — третя гра з центральною роллю), `+role:terrain`.
- `+window:map-window`, `+feature:world-map`.
- `+axis:field-nested` — тут стек вкладення з моделями-шаблонами (друга гра після Parabox, варто прийняти).
- `+axis:session` — `level`.

## Джерела
- ⭐ [Steam: Recursed](https://store.steampowered.com/app/497780/Recursed/) — трейлер, опис механік (скрині, копіювання/знищення кімнат), 60+ рівнів, сотні кімнат, без смерті й ворогів, 30 вересня 2016, Portponky / Shambles Software.
- [Grospixels](https://www.grospixels.com/site/recursed.php) — керування (висота стрибка, кидок по прямій), усі світи з кількістю рівнів, усі механіки розширень, парадокс-бонуси.
- [Blog simbabbad](https://simbabbad.blogspot.com/2022/04/recursed-steam-portponky.html) — модель кімнати, рівні Knot/Loop/Attic, стійкі скрині, парадокс.
- [itch.io](https://portponky.itch.io/recursed) — DRM-free версія (Windows, Linux).
- [YouTube: пошук «Recursed Portponky gameplay»](https://www.youtube.com/results?search_query=Recursed+Portponky+gameplay).

## Непевне
- (?) Undo в грі — не знайдено в джерелах; ймовірно лише рестарт і ресет кімнати виходом.
- (?) Вигляд меню й вибору рівнів (світи як хаб чи список).
- (?) Чи блокується вхід у скриню, якщо героїня несе цю саму скриню (точне формулювання «carry a chest out of itself»).
- (?) Точна умова парадоксу для звичайних (не стійких) скринь — джерела описують лише стійкі.
- (?) Липкі стіни в The Last Tapestry — лише згадка.
- (?) Розмір кімнат-сіток і чи рух героїні строго клітинний (платформер, позиція може бути неклітинною).
