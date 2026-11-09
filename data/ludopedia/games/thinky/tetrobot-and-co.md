---
title: Tetrobot and Co.
slug: tetrobot-and-co
aka: [Tetrobot and Co, Tetrobot & Co.]
family: thinky
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2013
platforms: [PC, Mac, Linux, iOS, Android, Wii U, Xbox One]
links:
  - {kind: other, url: "https://jayisgames.com/review/tetrobot-and-co.php", best: true, note: "рецензія: промінь, що всмоктує блоки, політ виплюнутого блока, пісок → скло лазером, дерево горить, метал заряджається, пудинг-липучка, труби, move-by-move undo, 3 сейви"}
  - {kind: steam, url: "https://store.steampowered.com/app/235980/Tetrobot_and_Co/", note: "Psychobot ковтає й випльовує блоки матерії; труби, лазери, вентилятори, хімія слизу; 50+ рівнів, memory blocks, Workshop"}
  - {kind: official, url: "https://www.swingswingsubmarine.com/tetrobot-and-co", note: "сторінка студії, автори, магазини"}
  - {kind: itch, url: "https://swingswingsubmarine.itch.io/tetrobot-and-co", note: "опис, Workshop, сиквел Blocks That Matter, порти iOS/Android"}
  - {kind: other, url: "https://www.gog.com/fr/game/tetrobot_and_co", note: "GOG: point-and-click по сітці, 3 золоті memory blocks на рівень, бонус-блоки; відгуки про пісок, газ, метал, TNT"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blocks_That_Matter", note: "приквел: Tetrobot збирає блоки, бʼючи їх знизу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tetrobot+and+Co+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, inventory, item-pickup, projectile-shot, gravity-fall, stick-together, cell-transform, destructible-blocks, beam-tracing, button-toggle, reach-exit, undo-redo, undo-step, save-multi-slot, level-select, achievements-window, controls-remap, background-music, +absorb-shoot, +material-physics, +material-reaction, +conduct-charge, +sticky-side, +pipe-travel, +cannon-launch, +optional-collectibles]
proposes: ["+trigger:beam_hit", "+cond:material", "+effect:absorb", "+effect:ignite", "+effect:stick_side", "+role:material-block", "+card:absorb-shoot", "+card:material-physics"]
author: opus
date: 2026-11-09
---

# Tetrobot and Co. — крихітний робот всмоктує блоки матерії й вистрілює їх, щоб полагодити механізм

## Суть
Пазл з видом збоку від Swing Swing Submarine (сиквел Blocks That Matter). Гравець веде Psychobot-а, мікроскопічного ремонтного робота, крізь нутрощі роботів-Тетроботів. Головна дія — промінь: він **всмоктує** блок матерії в «шлунок», а потім Psy **випльовує** його в інший бік. Кожен матеріал має свою фізику й реакції (пісок, дерево, метал, пудинг-слиз, газ, TNT), а механізми рівня (лазери, труби, вентилятори, електробарʼєри) реагують на матеріали. Мета — дійти до виходу; три золоті memory blocks на рівень — необовʼязкове ускладнення.

## Поле і час
- Квадратна сітка у вертикальному розрізі, рівень — кілька кімнат механізму (?).
- Ввід point-and-click по клітинах; гра чекає дій гравця — по суті покрокова, хоча анімації йдуть безперервно (?).
- Шари: тло-механізм, блоки матеріалів, пристрої (лазери, труби, вентилятори, гармати, бар'єри).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Psychobot | player | шлунок (запас блоків) | переміщується по клітинах за кліком; стріляє променем уперед/назад |
| Блок матерії | object | матеріал | всмоктується променем; виплюнутий летить, доки не прилипне до схожого матеріалу або не вдариться й не впаде |
| Пісок | object | sand | від лазера стає склом (JIG); падає (?) |
| Дерево | object | wood | горить від жару; лишає «обгоріле дерево» (GOG-відгуки) |
| Метал | object | metal | пролетівши крізь електробарʼєр, заряджається й вмикає пристрої |
| Пудинг / слиз | object | sticky | пудингова стіна; блок, у який влучила пудингова істота, стає липким з одного боку; хімію слизу можна змінювати |
| Газ, TNT | object | — | згадуються у відгуках; поведінка — (?) |
| Крихкий блок | object | — | розсипається з клацанням (?) від удару |
| Пудингова істота | neutral | — | ходить туди-сюди, натискає перемикачі, робить блоки липкими |
| Лазер | hazard | промінь | діє на матеріали (пісок → скло, нагрів дерева (?)) |
| Електробарʼєр | gate | дуга струму | заряджає метал, що пролітає |
| Труба | conduit | сегменти | переносить Psy в інше місце; часом треба добудувати сегменти |
| Вентилятор | terrain | напрям | дме блоки/робота (?) |
| Гармата + водяна стіна | terrain | — | вистрілює Psy крізь воду з кімнати в кімнату |
| Перемикач / пристрій | switch | — | вмикається зарядженим металом або натиском |
| Memory block (золотий) | pickup | 3 на рівень | необовʼязковий збір; відкриває секрети |
| Бонус-блок | pickup | — | допомагає дійти до виходу (GOG-відгук) (?) |
| Вихід / робот, що лагодиться | zone | — | мета рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `path_exists(psy, cell)` → ТО `move(psy, to)` (?).
- КОЛИ `input(beam, dir)` → ЯКЩО `custom: «перший блок на лінії променя всмоктуваний»` → ТО `pickup(psy, block)`.
- КОЛИ `input(shoot, dir)` → ЯКЩО `has(psy, block)` → ТО `throw(block, dir)`, `take(psy, block)`.
- КОЛИ `custom: «летючий блок торкнувся блока схожого матеріалу»` → ТО `attach(block, other)` (прилипає, зупиняється).
- КОЛИ `blocked(block)` → ЯКЩО `not same(block, obstacle, material)` → ТО `fall(block)`.
- КОЛИ `contact(laser, sand)` → ТО `transform(sand, glass)`.
- КОЛИ `contact(heat, wood)` → ТО `transform(wood, burnt_wood)` / `custom: «дерево горить»` (?).
- КОЛИ `contact(metal, electro_barrier)` → ТО `set_state(metal, charged)`; КОЛИ `contact(charged_metal, device)` → ТО `custom: «пристрій вмикається»`.
- КОЛИ `contact(pudding_creature, block)` → ТО `set_state(block, sticky_side)`.
- КОЛИ `contact(pudding_creature, switch)` → ТО `custom: «перемикач спрацьовує»`; істота ходить туди-сюди.
- КОЛИ `enter(psy, pipe)` → ЯКЩО `custom: «труба цілісна»` → ТО `teleport(psy, pipe_end)`.
- КОЛИ `enter(psy, cannon)` → ТО `custom: «Psy вистрілено крізь водяну стіну в сусідню кімнату»`.
- КОЛИ `contact(psy, crumbling_block)` → ТО `disappear(crumbling_block)` (?).
- КОЛИ `contact(psy, memory_block)` → ТО `pickup`, `counter(memory, +1)`.
- КОЛИ `reach(psy, exit)` → ТО `win`, `next_level`.
- Перемога: дійти до виходу · Поразка: нема, лише глухий кут → undo/рестарт (?) · Рахунок: memory blocks (до 3 на рівень).

## Керування і ввід
- Point-and-click по клітинах: клік — куди йти; дії променя/пострілу — вперед або назад (ліворуч/праворуч на екрані).
- Тач на iOS/Android: на маленькому екрані вибір ходу «через раз» (JIG); є підтримка геймпада Xbox 360, перепризначення (?).
- Undo — покроково.

## Вікна, меню, HUD
- `main-menu` → `save-slots` (3 файли збереження).
- `level-select` / мапа восьми Тетроботів, які треба полагодити (?).
- `game-screen`: кімната механізму, Psy, шлунок з блоками (`inventory-bar`) (?), лічильник memory blocks (?).
- `achievements-window` (Steam); `settings-window` — (?).
- Переходи: меню → слот → вибір робота/рівня → рівень → вихід → наступний.

## Фічі поза полем
- `levels-sequential`: 50+ рівнів (Steam; JIG про мобільну — 43 рівні, 8 роботів), секрети за memory blocks.
- `undo` покроковий; `save-slots` ×3; Steam Cloud, досягнення.
- Steam Workshop — створення й поширення своїх пазлів (`level-editor`, `level-sharing`) (?: на сторінці «available soon»).
- `localization` 7 мов; оригінальна музика (Morusque).

## Варіації й родичі
- Blocks That Matter (2011) — приквел-платформер: Tetrobot вибиває блоки знизу й складає з них тетраміно.
- Осі варіацій **поглинання і пострілу**: що бере промінь — перший блок / будь-який / лише свій матеріал; де зупиняється постріл — до упору / прилипає до схожого / падає; запас — 1 / кілька / необмежено.
- Родичі: Toki Tori (інструменти), Fire 'n Ice (матеріали й вогонь), Noita і falling-sand (матеріали з реакціями), Portal (дієслово-інструмент).

## Цікавинки для курсу
- Промінь, що забирає перший блок на лінії, і постріл до упору — 📎.
- Таблиця матеріалів × реакцій (лазер × пісок, жар × дерево, барʼєр × метал) — 🥉: дані, а не if-и.
- Прилипання до схожого матеріалу при польоті — 🥉.
- Заряд металу, що вмикає пристрої — 📎.
- Труби як телепорт, що працює лише при цілісному ланцюгу сегментів — 🥉 (перевірка звʼязності).
- Undo для системи з реакціями матеріалів (повний знімок стану) — 🥉.

## Мапа на каталог
- Є: `cell-click` ↔ point-and-click; `inventory` ↔ шлунок; `item-pickup` ↔ memory blocks; `projectile-shot` ↔ виплюнутий блок; `gravity-fall` ↔ блок падає після удару; `stick-together` ↔ прилипання до схожого; `cell-transform` ↔ пісок → скло; `destructible-blocks` ↔ крихкі блоки; `beam-tracing` ↔ лазери; `button-toggle` ↔ пристрої й перемикачі (?); `reach-exit`; `undo-redo`, `undo-step`; `save-multi-slot`; `level-select`; `achievements-window`; `controls-remap`; `background-music`.
- **Нема** → пропозиції карток:
  - `+absorb-shoot` «Всмоктати обʼєкт променем і вистрілити ним» · entities/interact · 🥉.
  - `+material-physics` «Матеріали з різною фізикою польоту й падіння» · entities/state · 🥉.
  - `+material-reaction` «Реакції матеріал × пристрій (лазер, вогонь, струм)» · entities/interact · 🥉.
  - `+conduct-charge` «Метал заряджається й вмикає пристрої» · entities/interact · 📎.
  - `+sticky-side` «Липка грань блока» · entities/state · 📎.
  - `+pipe-travel` «Труби-переходи, які треба добудувати» · entities/interact · 🥉.
  - `+cannon-launch` «Гармата вистрілює аватара в іншу кімнату» · entities/move · 📎.
  - `+optional-collectibles` «Необовʼязкові 3 предмети на рівень» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit` — промінь/лазер влучив у сутність (пісок → скло, всмоктування).
- `+cond:material` — матеріал сутності (sand, wood, metal…) як умова реакції.
- `+effect:absorb` — забрати сутність з відстані в запас (відрізняється від ✅ `pickup` дальністю й чергою).
- `+effect:ignite` — підпалити (горіння з поширенням) (?).
- `+effect:stick_side` — зробити липкою одну грань.
- `+role:material-block` — блок з матеріалом, що визначає фізику й реакції.
- `+card:absorb-shoot`, `+card:material-physics` — як вище.

## Джерела
- ⭐ [Jay is Games: review](https://jayisgames.com/review/tetrobot-and-co.php) — промінь уперед/назад, поведінка виплюнутого блока, водяні стіни й гармати, крихкі блоки, електробарʼєри й метал, пудинг, пісок → скло, дерево й жар, труби, undo, 3 сейви, 43 рівні / 8 роботів (мобільна).
- [Steam](https://store.steampowered.com/app/235980/Tetrobot_and_Co/) — ковтати й випльовувати блоки, труби/лазери/вентилятори, хімія слизу, memory blocks, 50+ рівнів, Workshop.
- [GOG](https://www.gog.com/fr/game/tetrobot_and_co) — point-and-click по сітці, 3 memory blocks на рівень, бонус-блоки, відгуки про пісок/газ/метал/TNT.
- [itch.io](https://swingswingsubmarine.itch.io/tetrobot-and-co) · [сайт студії](https://www.swingswingsubmarine.com/tetrobot-and-co) · [Wikipedia: Blocks That Matter](https://en.wikipedia.org/wiki/Blocks_That_Matter).
- YouTube: пошук «Tetrobot and Co gameplay».

## Непевне
- (?) Статті Wikipedia про гру нема (лінк черги віддає 404); повного переліку матеріалів не знайдено — газ, TNT, крига (?) лише з відгуків або з памʼяті.
- (?) Чи Psy підкоряється гравітації (літає чи ходить), як саме рухається за кліком; скільки блоків вміщує шлунок.
- (?) Які блоки падають (усі після удару чи лише пісок), що робить вентилятор, як змінюється «хімія слизу».
- (?) Чи є поразка (знищення Psy лазером/вибухом) або лише глухий кут.
- (?) Workshop і вбудований редактор — на Steam «available soon», чи зʼявився — не перевірено.
