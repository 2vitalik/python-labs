---
title: Ahoist Cratey
slug: ahoist-cratey
aka: []
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://thinkycollective.itch.io/ahoist-cratey", best: true, note: "грати в браузері; «exquisite corpse» 25 учасників Thinky Puzzle Games Discord (30.08.2020–27.01.2021); керування Z/R/Esc"}
  - {kind: other, url: "https://html-classic.itch.zone/html/3267134/index.html", note: "HTML5-збірка з itch: повний сирець PuzzleScript — девлог внесків, список багів, правила, 24 рівні з історією"}
  - {kind: other, url: "https://github.com/pancelor/PuzzleScript/tree/level-select", note: "форк PuzzleScript з меню вибору рівня (Esc), на якому зроблено гру"}
  - {kind: other, url: "https://www.bontegames.com/2021/01/ahoist-cratey-browser.html", note: "Bart Bonte (29.01.2021); коментарі гравців: стрибок на 1, підйом на нерухомий ящик, ліфти, стос із піратів"}
  - {kind: other, url: "https://thinkycollective.itch.io/indiana-hat-and-the-temple-of-puzz", note: "гра-напарниця Thinky Collective"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ahoist+Cratey+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-by-input, keyboard-controls, push-object, gravity-fall, impassable-cells, all-on-targets, sequential-levels, level-select, undo-unlimited, restart-level, level-from-txt, sound-effects, event-effects, +step-climb-1, +climb-if-stuck, +jump-fixed-height, +simultaneous-movement, +stack-climb, +vertical-lifter, +floating-block]
proposes: ["+effect:climb", "+effect:lift", "+trigger:landed", "+axis:gravity", "+card:climb-if-stuck", "+card:floating-block", "+card:vertical-lifter"]
author: opus
date: 2026-11-19
---

# Ahoist Cratey — пірати-сокобанщики з гравітацією: штовхни ящик, залізь на застряглий, підніми вантаж ліфтом на тросі

## Суть
Колективна PuzzleScript-гра Thinky Collective: 25 учасників Discord-сервера Thinky Puzzle Games по черзі додавали рівень, механіку чи шліфування («exquisite corpse», третій раунд формату). Вид збоку з гравітацією: пірат ходить ліворуч-праворуч, штовхає ящики, лізе на сходинку висотою 1 і їздить ліфтами-клітками на тросах, піднімаючи над головою ящики. У частині рівнів кілька піратів, і всі ходять **одним вводом одночасно**; перемога — коли на кожному виході стоїть пірат.

Назва — гра слів «Ahoy, matey» / hoist / crate; поверх пазлів — піратська історія сліпого скарбника Bluebeard.

## Поле і час
- Квадратна сітка, вид збоку; 24 рівні — невеликі кімнати від 7×8 до 18×11 і 13×18 клітин, обнесені стінами.
- Шари: фон (вихід, трос) → тіла (пірати, ящики, стіни, шестерні) → клітки ліфтів окремим шаром (пірат може стояти в клітці).
- Покроково: хід = натискання; падіння й підйом добігають тіками по 0,1 с (`again`), ввід у цей час не приймається.
- Падіння — по 1 клітині за тік до опори; опора — стіна, ящик, інший пірат, клітка ліфта.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синій пірат (Bluebeard) | player | — | ходить, штовхає, лізе на сходинку 1, «стрибає» на 1, їздить ліфтом |
| Коричневий і червоний пірати | player | є не в усіх рівнях | ті самі дії тим самим вводом одночасно; на них можна стати |
| Помаранчевий ящик | object | — | штовхається по одному; падає; застряглий — сходинка для підйому |
| Рожевий ящик | object | «плаваючий» | штовхається, але гравітації не має — висить у повітрі |
| Стіна / палуба | static | — | непрохідна; сходинка, якщо над нею вільно |
| Клітка ліфта | platform | висить на тросі | їде вгору-вниз разом із піратом усередині; підлога для тих, хто падає; ящик у клітку не заштовхнути |
| Трос | static | довжина | декор: від шестерні до клітки; росте й коротшає з рухом ліфта |
| Шестерня (у фоні / у стіні) | static | — | точка підвісу; крутиться, коли ліфт їде; стопор для ліфта |
| Вихід | static | один або кілька на рівні | на кожному має стояти пірат; ящик збоку в нього не заштовхнути |
| Скарб | pickup | лише у фіналі | дотик — звук скарбу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next_cell)` → ТО `move(pirate, dir)` — **для всіх** піратів на полі, кожен перевіряє свою клітину сам.
- КОЛИ `contact(pirate, crate)` збоку → ЯКЩО `free(cell_behind)` і `not cell(cell_behind, exit)` і `not occupied(cell_behind, elevator)` → ТО `push`, `sound(push)` — лише один ящик, ряд ящиків не штовхається.
- КОЛИ `contact(pirate, wall|crate)` збоку → ЯКЩО `custom: «перешкода не зрушить: стіна або застряглий ящик»` і `free(above_obstacle)` і `free(above_pirate)` → ТО `custom: «підйом: крок угору, наступного тіку — крок уперед на перешкоду»`, `sound(climb)`; ящик, що лежить на сходинці, при цьому штовхається.
- Ящик «застряг» у бік руху, якщо там стіна, клітка ліфта, інший нерухомий ящик, щось застрягле або пірат, за яким стіна, — `custom`-ланцюг, що перераховується щоходу.
- КОЛИ `input(up)` → ЯКЩО `not occupied(pirate_cell, elevator)` і `free(above)` → ТО `move(pirate, up)`, `sound(jump)` — стрибок на місці: наступні тіки гравітація повертає пірата вниз.
- КОЛИ `after(move)` → ЯКЩО `not supported(a)` → ТО `fall(a)` по 1 клітині за тік — для піратів і помаранчевих ящиків; рожеві ящики не падають.
- КОЛИ `custom: «тіло приземлилось»` → ТО `sound(thud)`, `animate(squish)`, `animate(smoke)`.
- КОЛИ `custom: «одне тіло падає в клітину, куди інше заходить збоку»` → ТО бічний рух має пріоритет, падіння чекає.
- КОЛИ `input(up|down)` → ЯКЩО `occupied(pirate_cell, elevator)` → ТО `move(pirate, dir)`, `move(elevator, dir)`, `sound(elevator)` — клітка їде з піратом, трос подовжується чи вкорочується, шестерня крутиться.
- КОЛИ `contact(pirate_in_elevator, crate)` згори → ТО `push` угору — ящик їде над головою (підйом вантажу).
- КОЛИ `blocked(elevator)` (стіна, шестерня, ящик або вихід) → ТО `custom: «клітка відкочується на місце»`, `sound(blocked)`; решта піратів цього ходу рухається.
- КОЛИ `custom: «пірат у клітці рухається вертикально у вихід»` → ТО `block`.
- КОЛИ `all_on(exit, pirate)` — на кожному виході стоїть пірат → ТО `win`, `next_level`.
- КОЛИ `contact(pirate, treasure)` → ТО `sound(treasure)` (фінальний рівень історії).
- КОЛИ `input(Z)` → ТО `undo(1)`.
- КОЛИ `input(R)` → ТО `restart`.
- КОЛИ `input(Esc)` → ТО `window(level-select)`.
- Перемога: усі виходи зайняті піратами (зайвий пірат може лишитись деінде). · Поразка: нема — глухий кут лікується undo/R. · Рахунку нема.

## Керування і ввід
- ←/→ (або A/D) — крок, поштовх або підйом залежно від того, що попереду.
- ↑/↓ — у клітці ліфта: їхати; поза ліфтом ↑ — стрибок на 1 клітину з поверненням.
- Z — undo, R — рестарт рівня, Esc — меню вибору рівня; кнопки дії нема (`noaction`).
- Усі пірати отримують той самий ввід; перемикання між ними нема.

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript («start game» / «continue»), звук старту.
- `level-select` — меню вибору рівня форку pancelor (Esc), 24 точки вибору.
- `dialogue-window` — текстові вставки піратської історії перед рівнями (Bluebeard, капітан Clement «the inclement», розвʼязка-сюрприз у фіналі).
- `game-screen` — кімната без HUD.
- Переходи: титул → повідомлення → рівень → (усі виходи зайняті) → повідомлення → наступний рівень; Esc → `level-select` → рівень.

## Фічі поза полем
- `levels-sequential` (24 рівні, останній — фінал історії зі скарбом) + `level-select`.
- `undo` ∞, `restart-level`.
- Звуки: поштовх, підйом, стрибок, приземлення (окремо для ящика), ліфт угору / вниз / упор, скарб, undo, рестарт.
- Анімація приземлення: «сплющення» піратів і клубки диму обабіч.
- Колективна розробка видна в коді: девлог 25 внесків (#0–#24), список «відомих багів-фіч», коментарі гравців-розробників із розвʼязками й перестановками рівнів.

## Варіації й родичі
- Формат Thinky Collective «exquisite corpse»: гра-напарниця Indiana Hat and the Temple of Puzz; наступний раунд — [conveyor-confusion](../push-slide/conveyor-confusion.md).
- Родичі: [block-dude](block-dude.md) (сходинка 1, без стрибка), [catrap](catrap.md) (кілька персонажів, гравітація, ящики), [boxboy](boxboy.md), [fire-n-ice](fire-n-ice.md), [sokoban](../push-slide/sokoban.md).
- Осі варіацій:
  - **гравітація за типом**: падає все / помаранчеві падають, рожеві висять (тут);
  - **як піднятися**: сходинка 1 / стрибок / ліфт на тросі / стати на іншого пірата — тут усі чотири;
  - **кілька аватарів**: один / перемикання клавішею (Catrap) / усі одним вводом одночасно (тут);
  - **поштовх чи підйом**: один і той самий ввід «вбік» штовхає ящик, якщо той зрушить, і лізе на нього, якщо застряг.

## Цікавинки для курсу
- Покрокова гравітація тіками після ходу (PuzzleScript `again`) — 📎.
- «Штовхни, а якщо застряг — залізь»: обчислення застряглості ланцюгом (стіна, ящик, пірат за ним) — 🥉.
- Ліфт на тросі: їде з піратом усередині, піднімає ящик над головою, відкочується при упорі, трос перемальовується — 🥉.
- Кілька піратів одним вводом + «кожен вихід зайнятий»: незалежні зіткнення в одному ході — 🥉.
- Пріоритет бокового руху над падінням за спірну клітину — 📎.
- Гравітація за типом (рожеві ящики висять) — 🌱.
- BFS-розвʼязувач рівня (пірати, ящики, висоти ліфтів) — 🥇.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls` ↔ стрілки/WASD; `push-object` ↔ ящик; `gravity-fall` ↔ падіння піратів і помаранчевих ящиків; `impassable-cells` ↔ стіни; `all-on-targets` ↔ кожен вихід зайнятий піратом; `sequential-levels` + `level-select` ↔ 24 рівні й Esc; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-рівні; `sound-effects` + `event-effects` ↔ звуки, «сплющення» й дим.
- **Нема** → пропозиції карток:
  - `+step-climb-1` (є з Block Dude, Fire 'n Ice) — підйом на перешкоду висотою 1.
  - `+climb-if-stuck` «Штовхнути, а якщо не зрушить — залізти» · entities/legality · 🥉.
  - `+jump-fixed-height` (є) · слот {height: 1} — стрибок на місці.
  - `+simultaneous-movement` (є) — усі аватари одним вводом.
  - `+stack-climb` (є) — пірат стає на пірата.
  - `+vertical-lifter` (є з Infinifactory) — тут клітка на тросі, керована зсередини, що піднімає вантаж над собою.
  - `+floating-block` «Блок без гравітації серед падаючих» · entities/move · 🌱.

## Пропозиції до словників
- `+effect:climb` — піднятися на перешкоду висотою 1 (є з Block Dude, Bonfire Peaks).
- `+effect:lift` — ліфт піднімає пасажира й вантаж над ним.
- `+trigger:landed` — тіло приземлилось після падіння (звук, анімація).
- `+axis:gravity` = `per-type`: пірати й помаранчеві ящики падають, рожеві — ні.
- `+card:climb-if-stuck`, `+card:floating-block`, `+card:vertical-lifter` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `after`, `blocked`, `cell`, `supported`, `animate`, `platform`.

## Джерела
- ⭐ [itch.io: Ahoist Cratey](https://thinkycollective.itch.io/ahoist-cratey) — гра в браузері, формат, 25 учасників, дати, керування, лінк на форк.
- [HTML5-збірка з itch](https://html-classic.itch.zone/html/3267134/index.html) — сирець PuzzleScript: девлог (#0 jackk — падіння й підйом, #3 Marcos D — ліфти, #13 Toomber — пріоритет бокового руху, #14 TophWells — плаваючі ящики), правила `climbable`/`stuck`/`elevator_trying_to_move`, перемога `all exit on player`, 24 рівні з текстами.
- [GitHub: pancelor/PuzzleScript level-select](https://github.com/pancelor/PuzzleScript/tree/level-select) — форк рушія з меню рівнів.
- [Bart Bonte](https://www.bontegames.com/2021/01/ahoist-cratey-browser.html) — анонс і коментарі гравців.
- YouTube: пошук «Ahoist Cratey puzzlescript».

## Непевне
- (?) Чи стрибок дає щось корисне (підштовхнути ящик угору чи заскочити в клітку ліфта над головою) — випливає з коду, у грі не перевірено.
- (?) Хто з піратів хто (коричневий — капітан Clement?) — здогад із текстів повідомлень.
- (?) Як розвʼязуються зіткнення кількох піратів, що йдуть в одну клітину одного ходу, — стандарт PuzzleScript, не перевірено.
