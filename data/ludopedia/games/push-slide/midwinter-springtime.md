---
title: Midwinter Springtime
slug: midwinter-springtime
aka: ["Весна посеред зими"]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [web]
links:
  - {kind: itch, url: "https://pap4qlxxlevb.itch.io/midwinter-springtime", best: true, note: "грати в браузері (PuzzleScript); керування WASD/Z/R/Esc, посилання на сирець, коментарі гравців"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=3e73c82343df51a600786e75745ccf6b", note: "сирець у редакторі PuzzleScript (посилання автора зі сторінки itch)"}
  - {kind: other, url: "https://api.github.com/gists/3e73c82343df51a600786e75745ccf6b", note: "той самий сирець як gist JSON: обʼєкти, шари, правила, рівень 19×15"}
  - {kind: other, url: "https://confoundingcalendar.itch.io/", note: "Confounding Calendar 2025 — адвент-календар пазлів, для якого зроблено гру"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Midwinter+Springtime+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, orientation-state, inertia-slide, environment-death, death-animation, reach-exit, undo-unlimited, restart-level, level-from-txt, sound-effects, +push-chain, +spring-launch, +fly-over-pits]
proposes: ["+effect:launch", "+card:spring-launch", "+card:fly-over-pits"]
author: opus
date: 2026-11-19
---

# Midwinter Springtime — стисни пружину об стіну, стань на неї й злети над ямами до загубленого подарунка

## Суть
Однорівнева PuzzleScript-головоломка для адвент-календаря Confounding Calendar 2025: герой загубив подарунок у «пружинному підземеллі» й має до нього дійти. Ящиків тут нема — штовхаються **пружини** двох орієнтацій, пружні вздовж своєї осі й жорсткі поперек. Пружину, притиснуту вздовж осі до стіни, можна **стиснути** й стати на неї; крок геть від стіни — і вона **катапультує** героя до найближчої перешкоди, над ямами. Так само стиснута пружина викидає іншу пружину, якою її притиснули.

## Поле і час
- Квадратна сітка, один рівень 19 × 15 у рамці стін: кілька кімнат, перегороджених рядами ям; 9 пружин (6 вертикальних, 3 горизонтальні); подарунок у кімнаті, до якої пішки не дійти — лише перелетіти яму. Камери нема, увесь екран видно.
- Шари клітини (collision layers): фон → позначка «тут не падати» → ціль або яма → анімація падіння → тверді (гравець, стіна, пружини) → стиснута пружина → маркери польоту → декоративні обводки стін.
- Хід = крок гравця; після нього каскад `again` (інтервал 0,03 с) докручує політ по одній клітині за кадр, доки той не зупиниться. Без вводу нічого не рухається.
- Стіни мають колір тла сторінки, темні обводки малюються пізніми правилами там, де стіна межує з підлогою (`run_rules_on_level_start`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | стан: стоїть / летить | рух 4 напрямки; штовхає пружини; стискає пружину й стає на неї; падає в яму |
| Горизонтальна пружина | object | вісь ↔ | штовхається як ящик; рух ← або → у нерухому опору стискає її; для руху ↑↓ сама є жорсткою опорою |
| Вертикальна пружина | object | вісь ↕ | те саме вздовж ↕; для руху ↔ — жорстка опора |
| Стиснута пружина | object | бік опори (4) | лежить у клітині разом із тим, хто її стиснув; хто рушить геть від опори — летить; порожня — розпрямляється |
| Стіна | static | — | непрохідна; опора для стискання; зупиняє політ |
| Яма | hazard | — | гравець чи пружина, що стали на неї не в польоті, падають і зникають; яма лишається відкритою |
| Подарунок | static | — | ціль: на ньому має стояти гравець, і ніхто не летить |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; у стіну — `block` зі звуком «не можна».
- КОЛИ `contact(player, spring)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(player, dir)`.
- КОЛИ `contact(spring, spring)` (рухома пружина впирається в іншу) → ЯКЩО `not cell(cell_behind_second, wall)` → ТО `push` — ланцюг будь-якої довжини; за останньою стіна — стоїть увесь ланцюг.
- КОЛИ `contact(player, spring_h)` при русі ← або → → ЯКЩО `occupied(cell_behind, wall|spring_v)` і `not moving(anvil, dir)` → ТО `set_state(spring_h, compressed)`, `move(player, dir)` — гравець стає на стиснуту пружину; для вертикальної пружини те саме вгору/вниз з опорою «стіна або горизонтальна пружина».
- КОЛИ `contact(spring_v, spring_h)` (поперечна пружина тисне вздовж осі іншої) → ЯКЩО `occupied(cell_behind, wall|spring_v)` → ТО `set_state(spring_h, compressed)`, `move(spring_v, dir)` — пружина-«вершник» займає клітину стиснутої (і навпаки для пари ↕).
- КОЛИ `input(dir)` → ЯКЩО `state(spring_under_player, compressed)` і `custom: «dir — геть від опори»` → ТО `set_state(player, flying)`, `slide(player, dir)`, `sound(fling)`.
- КОЛИ `turn_end` → ЯКЩО `occupied(compressed_cell, spring)` і `not occupied(release_cell, player)` → ТО `set_state(spring, flying)`, `slide(spring, release_dir)` — гравець, що стоїть упритул з боку виходу, утримує «вершника».
- КОЛИ `leave(player|spring, compressed_cell)` → ТО `clear_state(spring, compressed)`, `sound(spring)` — пружина розпрямляється на своєму місці; крок убік від осі — звичайний крок без польоту.
- КОЛИ `blocked(flyer)` (попереду стіна чи пружина; для пружини — ще й гравець) → ТО `clear_state(flyer, flying)`, `sound(hit_wall)` — летун стоїть перед перешкодою, нічого не штовхаючи.
- КОЛИ `enter(flyer, pit)` → ЯКЩО `state(flyer, flying)` → ТО нічого: у польоті яма не діє.
- КОЛИ `enter(player|spring, pit)` → ЯКЩО `not state(flying)` → ТО `fall`, `disappear`, `sound(fall)` — пішки, поштовхом або там, де закінчився політ; яма не засипається.
- КОЛИ `enter(player, gift)` → ЯКЩО `not state(player, flying)` → ТО `win` (умови сирцю «All Target on player» і «no roll»).
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: гравець стоїть на подарунку після польоту. · Поразка: формально нема — гравець зник у ямі, далі лише undo або рестарт. · Рахунок: нема.

## Керування і ввід
- WASD / стрілки — крок, поштовх, стискання пружини або зліт (якщо стоїш на стиснутій пружині й ідеш геть від опори).
- Z — undo, R — рестарт, Esc — меню (сторінка itch і повідомлення в грі «[ Z to undo, R to restart ]»).
- Поворотів, мишки чи окремої кнопки «стрибок» нема: зліт — це звичайний крок у потрібний бік.

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript (назва, автор, старт гри).
- `custom-window` — повідомлення-заставки: перед рівнем «Nuts... I dropped my gift inside the spring dungeon...» і підказка клавіш; після — «Yippee! My gift is safe and sound!», «...», «Why did I build a spring dungeon down here again...?».
- `game-screen` — один екран підземелля без HUD: лічильників, таймера й рівнів нема.
- `pause-menu` — Esc: меню рушія PuzzleScript (?).
- Переходи: титул → повідомлення → рівень → (подарунок) фінальні повідомлення → титул.

## Фічі поза полем
- `undo` (∞) і `restart-level` — стандарт PuzzleScript.
- Звук на кожну подію: крок у стіну, рух пружини, стискання, розпрямлення, кидок, удар об стіну, падіння.
- Один рівень — нема вибору рівнів, підказок, редактора; сирець відкритий (автор дає посилання в редактор).

## Варіації й родичі
- Осі варіацій «пружина як обʼєкт Sokoban»:
  - **що стискає**: гравець (і стає зверху) / поперечна пружина / ланцюг;
  - **кого кидає**: гравця / пружину, що лежить на стиснутій;
  - **як летить**: до упору (як `inertia-slide` у [Pengo](pengo.md) чи [ковзанні по льоду](ice-sliding-puzzles.md)) і над ямами; яма діє лише в точці зупинки.
- Родичі: [Sokoban](sokoban.md) (штовхання), [Kwirk](kwirk.md) (ями, але там засипаються), [Tomb of the Mask](tomb-of-the-mask.md) (рух до упору як основа).

## Цікавинки для курсу
- Пружина з віссю: пружна вздовж, жорстка поперек — одна сутність, два стани (звичайна / стиснута) — 📎.
- Катапульта: рух до упору з окремим станом польоту, у якому ями не діють, і перевірка ями лише в точці зупинки — 🥉.
- Пружина-«вершник» вилітає наступним кадром, якщо з боку виходу нема гравця, — 📎.
- Ланцюгове штовхання з умовою «за останнім не стіна» — 🌱.
- Розвʼязувач для одного великого екрана (BFS по станах: гравець, 9 пружин зі станом, які пружини «зʼїли» ями) — 🥇.
- Порт PuzzleScript-правил на Python (шари, `late`, каскад `again`) як вправа «правила як дані» — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ пружини як ящики; `impassable-cells` ↔ стіни; `orientation-state` ↔ горизонтальна / вертикальна пружина; `inertia-slide` ↔ політ до упору; `environment-death` ↔ ями; `death-animation` ↔ три кадри падіння; `reach-exit` ↔ подарунок; `undo-unlimited` + `restart-level`; `level-from-txt` ↔ рівень текстом у сирці; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+push-chain` (є в корпусі) — ланцюг пружин з умовою «за останнім не стіна».
  - `+spring-launch` «Пружина-катапульта: стиснути об опору, зійти геть — і полетіти до упору» · entities/interact · 🥉 · слоти {axis: h|v, rider: player|object}.
  - `+fly-over-pits` «У польоті яма не діє; падіння — лише там, де зупинився» · entities/move · 📎.

## Пропозиції до словників
- `+effect:launch` — запустити сутність у політ до упору від пружини; у реченнях записано як `set_state(flying)` + `slide`.
- `+card:spring-launch`, `+card:fly-over-pits` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch: Midwinter Springtime](https://pap4qlxxlevb.itch.io/midwinter-springtime) — опис «spring-springing block-pushing puzzle» на один екран, Confounding Calendar 2025, керування, посилання на сирець, коментарі (подарунок у «spring dungeon», шарування трюків).
- [Сирець у редакторі PuzzleScript](https://www.puzzlescript.net/editor.html?hack=3e73c82343df51a600786e75745ccf6b) і [gist JSON](https://api.github.com/gists/3e73c82343df51a600786e75745ccf6b) — усі обʼєкти й шари, правила стискання, відскоку, польоту, ям і ланцюга, умови перемоги `All Target on player` + `no roll`, рівень і повідомлення.
- [Confounding Calendar](https://confoundingcalendar.itch.io/) — джем-календар, для якого зроблено гру.
- YouTube: пошук «Midwinter Springtime puzzlescript».

## Непевне
- (?) Точна дата: гра з Confounding Calendar 2025 (грудень 2025); на сторінці itch дати нема, лише вік коментарів.
- (?) Меню й Esc — стандартні екрани рушія PuzzleScript, у сирці не описані; чи є сенсорне керування — сторінка мовчить.
- (?) У сирці є фальшива стіна й табличка (`fakewall`, `sign1`), але на рівні їх нема — автор пише, що код зібрано з частин старих проєктів.
