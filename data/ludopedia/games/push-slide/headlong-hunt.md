---
title: Headlong Hunt
slug: headlong-hunt
aka: [Headlong, Headlong Hunt (PuzzleScript Version)]
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
year: 2023
platforms: [PC, Mac, Linux, web]
links:
  - {kind: play, url: "https://toombler.itch.io/headlong-hunt", best: true, note: "безкоштовна PuzzleScript-версія 2021 у браузері: 37 рівнів, керування, level select"}
  - {kind: steam, url: "https://store.steampowered.com/app/2323660/Headlong_Hunt/", note: "комерційна версія 2023: 100+ пазлів, оверворлд, undo крізь рестарт, ремап"}
  - {kind: itch, url: "https://toombler.itch.io/headlong", note: "та сама комерційна версія, Win/Mac/Linux, devlog з патчами"}
  - {kind: other, url: "https://api.github.com/gists/6df4e6ea8d2c69842f4caf382e9e2bd5", note: "сирці PuzzleScript-версії: зір, втеча, кущі, кристали, вода, пастка"}
  - {kind: play, url: "https://dario-zubovic.github.io/PuzzleScript/play.html?p=6df4e6ea8d2c69842f4caf382e9e2bd5", note: "той самий скрипт у форку PuzzleScript (мобільний вхід)"}
  - {kind: other, url: "https://steamcommunity.com/app/2323660/reviews/?browsefilter=toprated&l=english", note: "відгуки: механіки комерційної версії (кущі, лід, темні блоки, мости)"}
  - {kind: other, url: "https://roomescapeartist.com/2023/12/17/headlong-hunt-review/", note: "огляд: сітка-пастка, undo, оверворлд, без підказок"}
  - {kind: youtube, url: "https://youtube.com/playlist?list=PLgX5yD9FMWbdyeJOK1vta6NltZSRBnLSG", note: "проходження PuzzleScript-версії (Joseph Mansfield), лінк зі сторінки itch"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Headlong+Hunt+gameplay", note: "пошук; геймплей комерційної версії"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, controls-remap, push-object, impassable-cells, inertia-slide, floor-types, cell-transform, stop-cell, undo-unlimited, restart-level, level-select, world-map, level-from-txt, movement-animation, +flee-player, +cover-cell, +herd-into-trap, +trample-on-leave, +undo-through-restart, +light-count-melt]
proposes: ["+effect:flee", "+effect:stop", "+cond:hidden", "+feature:undo-through-restart", "+feature:undo-hold-repeat", "+feature:unlock-all-levels", "+card:flee-player", "+card:cover-cell", "+card:herd-into-trap", "+card:trample-on-leave"]
author: opus
date: 2026-11-09
---

# Headlong Hunt — загнати полохливу істоту в сітку-пастку: вона тікає по прямій, щойно тебе побачить

## Суть
Покрокова головоломка з видом згори: біолог на крижаних островах має зловити швидку полохливу тваринку. Ловити напряму не можна — істота **бачить уздовж рядка й стовпця на будь-яку відстань** і, побачивши гравця, **мчить від нього по прямій до першої перешкоди**. Гравець керує нею непрямо: стає з потрібного боку, ховається в кущах, ставить кристали-перешкоди, щоб ковзання закінчилось точно на клітині з сіткою. Гра виросла з безкоштовної PuzzleScript-версії (2021, 37 рівнів); комерційна (2023, Unity) має приблизно втричі більше пазлів і кілька нових механік.

## Поле і час
- Квадратна сітка: острови з льоду серед води; краї острова — вода, вихід за межу екрана теж можливий (для істоти).
- Шари (PuzzleScript): фон-лід → вода → записки → ціль-пастка → знищений кущ → тверді обʼєкти (гравець, скеля, кристал, істота — одна клітина на одного) → кущ (окремий шар: у кущі можна стояти).
- Хід = крок гравця; після нього світ досчитується: перевірка зору, і якщо істота налякана — вона рухається клітинка за клітинкою (`again`) до упору. Без вводу нічого не відбувається.
- Камера статична, рівень видно цілком; випадковість лише косметична (вигляд кущів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біолог | player | — | рух 4 напрямки; штовхає один кристал; у воду не заходить; ховається в кущі |
| Істота | neutral | — | бачить по 4 прямих без меж; побачивши гравця — ковзає від нього до упору; стоїть, доки не бачить |
| Сітка-пастка | zone | — | ціль: істота, що зупинилась тут, спіймана |
| Скеля | static | — | непрохідна; закриває огляд; зупиняє істоту |
| Кристал (камінь) | object | — | штовхається на 1; закриває огляд; зупиняє істоту; у воді тоне (PuzzleScript) |
| Вода | terrain | — | непрохідна для гравця; істота пробігає по ній і навіть зупиняється на ній |
| Кущ | terrain | цілий / витоптаний | хто стоїть у кущі — невидимий і не лякається; закриває огляд; зупиняє ковзну істоту; витоптується, коли з нього вийшли |
| Витоптаний кущ | terrain | — | звичайна підлога |
| Записка | pickup | номер 1–12 | на дотик показує текст-лор (у ньому — натяки на правила) |
| Крижаний блок (комерційна) | object | — | штовхається (?); тане, коли засвічено досить темних блоків |
| Темний блок (комерційна) | switch | світиться / ні | засвічується під час погоні; після N засвічених лід тане (?) |
| Трава (комерційна) | terrain | — | укриття; істота крізь неї не проходить (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, water)` або `cell(next_cell, rock)` або `occupied(next_cell, creature)` → ТО `block`.
- КОЛИ `contact(player, crystal)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(player, dir)`; інакше `block` (два кристали підряд не рушать).
- КОЛИ `enter(crystal, water)` → ТО `disappear_a` (PuzzleScript: камінь тоне з анімацією); у комерційній версії штовхнутий у воду предмет може стати переходом — `set_cell(water, floor)` (?).
- КОЛИ `line_of_sight(creature, player)` → ЯКЩО `not state(player, in_bush)` і `not state(creature, in_bush)` і `free(cell_beyond_creature)` → ТО `slide(creature, away_from_player)` (`custom: «тікати»`); відстань не важлива.
- Огляд перекривають скеля, кристал і кущ: ЯКЩО `custom: «між ними є непрозора клітина»` → ТО `block` (істота не лякається).
- КОЛИ `blocked(creature)` → ТО `custom: «стоп, анімація удару об скелю чи кристал»`, `sound(bump)`.
- КОЛИ `enter(creature, bush)` → ТО `custom: «ковзання зупиняється в кущі»`, `set_state(creature, in_bush)`.
- КОЛИ `enter(player, bush)` → ТО `set_state(player, in_bush)` — гравця не видно, можна підкрастися впритул.
- КОЛИ `leave(player, bush)` → ЯКЩО `custom: «у кущі нікого й нічого не лишилось»` → ТО `set_cell(bush, trampled)` (кущ — одноразове укриття).
- КОЛИ `adjacent(player, creature)` → ЯКЩО `state(creature, in_bush)` і `not state(player, in_bush)` і `free(cell_beyond_creature)` → ТО `set_cell(bush, trampled)` — кущ істоти знищено, вона знову видима й тікає.
- КОЛИ `input(dir)` → ЯКЩО `state(player, in_bush)` і `occupied(next_cell, creature)` → ТО `push` (копняк із куща: істота зсувається на 1).
- КОЛИ `edge(creature)` → ТО `disappear_a` — істота втекла за край; рівень не пройти, лише undo/рестарт.
- КОЛИ `enter(creature, trap)` → ЯКЩО `custom: «ковзання закінчилось на цій клітині»` → ТО `win`, `next_level` (пробіг над пасткою — не рахується; гравцю на час анімації рух заблоковано).
- КОЛИ `enter(player, note)` → ТО `message(lore)`, `disappear_b`.
- КОЛИ `custom: «погоня засвічує темний блок»` → ТО `set_state(dark_block, lit)`; КОЛИ `counter(lit_blocks, >=, n)` → ТО `disappear(ice_block)` (лід тане; комерційна, деталі (?)).
- КОЛИ `input(undo)` → ТО `undo(1)` (комерційна: можна відкотити й рестарт) · КОЛИ `input(restart)` → ТО `restart`.
- Перемога: істота нерухома на клітині пастки. · Поразка: формальної нема; істота за краєм — глухий кут. · Рахунок: нема (без таймера, ліміту ходів і оцінок).

## Керування і ввід
- Стрілки / WASD — крок або поштовх; кнопки дії немає (`noaction` у PuzzleScript).
- Z — undo, R — рестарт, Esc — до вибору рівня/меню, M — без звуку (PuzzleScript-версія).
- Комерційна: клавіатура й геймпад (Xbox/PlayStation), повне перепризначення, утримання undo прискорюється.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript (назва, автор, «почати / продовжити»).
- `level-select` — вибір будь-якого з 37 рівнів (PuzzleScript, рекомендовано по порядку).
- `map-window` — комерційна: суцільна мапа-оверворлд з двома основними шляхами й необовʼязковими островами.
- `game-screen` — острів; HUD мінімальний: `level-number` угорі ліворуч (з патча 1.0.2).
- `custom-window` — текст записок-лору (12 записок у PuzzleScript; у комерційній — окремі нотатки).
- `pause-menu` — комерційна: номер версії показано лише на паузі; `settings-window` — звук (вимкнення у фоні), ремап, розблокувати всі рівні, сітка вмк/вимк (?).
- Переходи: титул → вибір рівня / мапа → рівень → (спіймано) анімація сітки → мапа.

## Фічі поза полем
- `undo` (∞) і `+undo-through-restart` (комерційна; PuzzleScript — штатний Z/R); `+undo-hold-repeat`.
- `restart-level`, `level-select`, `world-map` з гілками й необовʼязковими островами.
- `remap-controls`, `gamepad-support`; налаштування «розблокувати всі рівні» (`+unlock-all-levels`) замість підказок — підказок нема.
- `cloud-save` (Steam Cloud); сейви itch і Steam в одній теці.
- Демо: 14 перших рівнів.

## Варіації й родичі
- PuzzleScript-версія (2021, «In pursuit of purple», 37 островів) → комерційна Headlong Hunt (2023): ~3× пазлів, лід і темні блоки, трава, мости, оверворлд, нова графіка.
- Осі варіацій:
  - **як NPC реагує на гравця**: женеться (`rodents-revenge`, Theseus) / **тікає по прямій до упору** (Headlong Hunt) / тікає на 1–2 кроки з пріоритетом поворотів (`paquerette-down-the-bunburrows`);
  - **що бачить NPC**: 4 прямі без меж (тут) / радіус / сусідні клітини;
  - **як ховатись**: нема / кущ як одноразове укриття / стіни-перешкоди огляду;
  - **ціль**: дійти самому (`sokoban`) / **доставити чужу сутність** у клітину ковзанням (тут, `ice-sliding-puzzles`, `ricochet-robots`).
- Родичі: `ice-sliding-puzzles` (ковзання до упору), `ricochet-robots` (робот ковзає до перешкоди, ставиш блокери), `paquerette-down-the-bunburrows`, `pengo`, `sokoban`.

## Цікавинки для курсу
- Втеча по лінії зору: перевірка 4 променів до непрозорої клітини + ковзання до упору — 📎 (два відомі алгоритми разом).
- Кущ: стан «прихований» для обох сторін, витоптування при виході, копняк із куща — 📎.
- Ціль «нерухомо на клітині», а не «пройшов через» — 🌱, але гарний урок про стан наприкінці ходу.
- PuzzleScript-трюк: ковзання як `again`-цикл по одній клітині з анімацією — 🌱.
- Лічильник засвічених блоків, що розтоплює лід — 🥉 (глобальний стан + перетворення клітин).
- Розвʼязувач: BFS по станах (гравець, істота, кристали, витоптані кущі) і пошук «на два кроки наперед» — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `controls-remap` ↔ керування; `push-object` ↔ кристали; `impassable-cells` ↔ скелі, вода; `inertia-slide` ↔ ковзання істоти; `floor-types` ↔ лід / вода / кущ; `cell-transform` ↔ кущ → витоптаний; `stop-cell` ↔ кущ зупиняє ковзання; `undo-unlimited` + `restart-level`; `level-select` + `world-map`; `level-from-txt` ↔ ASCII-рівні PuzzleScript; `movement-animation` ↔ анімація ковзання й удару.
- **Нема** → пропозиції карток:
  - `+flee-player` (вже Paquerette) · слот {range: ∞, stop: obstacle} — тут без меж дальності й до упору.
  - `+cover-cell` «Укриття: хто в клітині, того не видно» · entities/state · 📎.
  - `+herd-into-trap` «Загнати NPC у клітину-пастку» · game-logic/win · 🌱.
  - `+trample-on-leave` «Клітина руйнується, коли з неї зійшли» · entities/interact · 🌱.
  - `+undo-through-restart` «Undo відкочує й рестарт» · game-logic/history · 🌱.
  - `+light-count-melt` «Лічильник засвічених блоків знімає перешкоди» · entities/state · 🥉 (?).

## Пропозиції до словників
- `+effect:flee` — тікати від джерела (тут — ковзання до упору; повтор Paquerette, Gladiabots).
- `+effect:stop` — зупинити рух сутності, що ковзає (кущ, пастка); `block` описує відмову ходу, а не зупинку посеред ковзання.
- `+cond:hidden` — сутність невидима для огляду іншої (у кущі); ширше за `state`, бо діє на `line_of_sight`.
- `+feature:undo-through-restart` — рестарт теж відкочується.
- `+feature:undo-hold-repeat` — утримання undo повторює й прискорює.
- `+feature:unlock-all-levels` — налаштування, що відкриває всі рівні (альтернатива підказкам і `skip-level`).
- `+card:flee-player`, `+card:cover-cell`, `+card:herd-into-trap`, `+card:trample-on-leave` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch: Headlong Hunt (PuzzleScript Version)](https://toombler.itch.io/headlong-hunt) — 37 рівнів, керування Z/R/WASD/Esc/M, level select, лінки на плейлисти.
- [GitHub Gist API: сирці](https://api.github.com/gists/6df4e6ea8d2c69842f4caf382e9e2bd5) — правила зору (`Opaque = StoneCrate or Wall or Bush`), втеча `again`, кущ і копняк, тонучий кристал, вихід за край, перемога «stationary Spirit Target», 12 записок.
- [Steam](https://store.steampowered.com/app/2323660/Headlong_Hunt/) — опис, 100+ пазлів, оверворлд, undo through reset, ремап, контролер.
- [itch: Headlong Hunt](https://toombler.itch.io/headlong) + devlog — дата релізу, демо 14 рівнів, патчі (трава, тонення, номер рівня), «~3× пазлів і кілька нових механік».
- [Steam: відгуки](https://steamcommunity.com/app/2323660/reviews/?browsefilter=toprated&l=english) — «flees when it sees you», «always escapes in a straight line», вода, кущі одноразові, лід, темні блоки, undo з рестарту, без таймера й оцінок.
- [Room Escape Artist: review](https://roomescapeartist.com/2023/12/17/headlong-hunt-review/) — сітка-пастка, undo, налаштування розблокування, без підказок, 100+ рівнів.
- Скріншоти Steam (переглянуто): острови льоду, скелі, кристали, лід у воді, кущі, сітка над клітиною з силуетом істоти.

## Непевне
- (?) Комерційні механіки описано з відгуків і скріншотів: що саме засвічує темні блоки, скільки треба, чи штовхається крижаний блок і чи предмет у воді завжди стає мостом.
- (?) Трава: «укриття» (відгук) і «істота інколи проходила крізь траву» (патч 1.0.2) — роль трави точно не перевірено.
- (?) «Trapping the creature while sinking» (патч 1.0.5) — хто тоне і коли, невідомо.
- (?) Лічильник «113 рівнів» — з одного відгуку; Steam каже «100+».
- (?) Чи є в комерційній версії записки-лор як у PuzzleScript — згадка «lore note» у патчі 1.0.5, деталі не бачив.
