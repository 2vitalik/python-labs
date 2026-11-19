---
title: Bombuzal
slug: bombuzal
aka: [Ka-Blooey, Bomb Uzal]
family: thinky
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1988
platforms: [Amiga, Atari ST, C64, MS-DOS, SNES (Ka-Blooey), Switch (Nintendo Classics), Steam (DOS)]
links:
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Bombuzal", best: true, note: "C64-Wiki: усі бомби, плитки, дроїди, вороги, керування, вид 2D / 3D, паролі кожні 8 рівнів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bombuzal", note: "один крок на втечу після підпалу, розміри бомб і зони реакції (велика — 13 клітин), рейки, Sinister і Dexter, версії"}
  - {kind: other, url: "https://www.c64-wiki.de/wiki/Bombuzal", note: "німецька C64-Wiki: ті самі правила, «безпечне поле» після останнього вибуху, +1 життя за рівень"}
  - {kind: steam, url: "https://store.steampowered.com/app/1084010/Bombuzal/", note: "DOS-версія (2019): вид згори або ізометрія, hotseat на двох"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bombuzal+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, chain-detonation, blast-wave, explode-area, floor-types, inertia-slide, teleport, button-toggle, push-object, party-switch, wall-follower, touch-death, environment-death, player-death, time-out, time-bonus, status-panel, remaining-counter, level-password, sequential-levels, map-window, hot-seat, sound-effects, +step-off-fuse, +destructible-floor, +crumbling-floor, +spinner-tile, +view-2d-3d-toggle, +linked-detonation, +variable-bomb, +blast-stopper, +blast-proof-floor, +rail-only-move, +survive-final-blast, +move-slows-timer, +extra-life-per-level]
proposes: ["+trigger:blast_reached", "+cond:in_blast_zone", "+effect:smother", "+effect:detonate_all", "+feature:view-toggle", "+feature:level-password", "+card:step-off-fuse", "+card:linked-detonation", "+card:move-slows-timer"]
author: opus
date: 2026-11-19
---

# Bombuzal — підпали бомбу, зійди на одну клітину й переживи ланцюгову реакцію, що зʼїдає підлогу

## Суть
Бомбузал ходить островом із плиток у порожнечі, де розкладено бомби й міни; щоб пройти рівень, треба знищити **всі** до кінця таймера й лишитися на цілій плитці. Підпалити бомбу можна, лише ставши на неї, а вибухає вона, щойно з неї зійти, — тож без смерті запалюється тільки найменша, решту підривають ланцюгом. Вибухи знищують плитки, тому кожен підрив змінює поле втечі; головоломку ускладнюють лід, плитки, що зникають після проходу, клепані плитки, телепорти й двоє ворогів-обхідників.

## Поле і час
- Квадратна сітка плиток, що висить у порожнечі; знищена вибухом плитка стає проваллям (?). Пробіл показує огляд-мапу всього рівня, таймер при цьому йде (C64-Wiki).
- Вид — 2D згори або 3D-ізометрія, обирається на титулі; логіка та сама.
- Real-time: таймер рівня, вороги ходять самі; порада C64-Wiki — поки Бомбузал рухається, час спливає повільніше.
- 130 рівнів; пароль — після кожних 8.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бомбузал | player | життя (+1 за рівень) | крок у 4 напрямки; підпалює бомбу, на якій стоїть; бере й кладе бомбу лише на пазовій плитці |
| Мала бомба | object | реакція — хрест 1 | вибух знищує лише свою плитку й підриває бомби / міни на 4 сусідніх клітинах |
| Середня бомба | object | радіус на 1 більший | без смерті — лише ланцюгом |
| Велика бомба | object | 13 клітин | знищує 13 плиток; зона реакції — ще на клітину далі в 4 напрямках і між ними по діагоналі; лише ланцюгом |
| Змінна бомба | object | мала → середня → велика по колу | розмір фіксується в мить першого натискання вогню |
| A-бомби | object | звʼязані | вибух однієї підриває всі A-бомби рівня |
| Міна | hazard | — | став — вибух плитки й смерть; знищується лише ланцюгом; рахується в «лишилось» |
| Звичайна плитка | terrain | — | вибух знищує → провалля |
| Клепана плитка | terrain | — | вибух не знищує |
| Лід | terrain | — | Бомбузал ковзає до першої неледяної плитки |
| Розчинна плитка | terrain | — | зникає, щойно з неї зійти |
| Пазова плитка (рейка) | terrain | — | бомбу на ній можна штовхати вздовж паза, брати й класти |
| Силове поле | terrain | — | вибух, що дійшов сюди, гасне |
| Перемикач | switch | → повʼязана плитка | вмикає / вимикає ще одну плитку |
| Спінер | terrain | — | штовхає Бомбузала у випадковий бік |
| Телепорт | terrain | ціль не показана | переносить; під час перенесення вибухи не шкодять |
| Dexter | enemy | — | обходить плитки за годинниковою стрілкою (завжди праворуч, де можна); не переслідує; дотик — смерть |
| Sinister | enemy | — | те саме проти годинникової (завжди ліворуч) |
| Дроїд Bubble | ally | — | «можна активувати, далі — керувати»; гине лише від підпаленої бомби / міни |
| Дроїд Squeak | ally | — | теж керований після активації; гине від дотику до бомби / міни |
| Порожнеча | hazard | — | за краєм і на місці знищених плиток; хто опинився над нею — падає |

## Правила (КОЛИ → ЯКЩО → ТО)
Підпал і вибух:
- КОЛИ `input(fire_hold)` → ЯКЩО `occupied(cell_under, bomb)` → ТО `set_state(bomb, lit)` після відліку утримання.
- КОЛИ `leave(player, lit_bomb)` → ТО `explode(own_cell, void)` — на втечу є рівно один крок (Wikipedia).
- КОЛИ `custom: «вибух накрив клітину»` → ЯКЩО `cell(x, normal)` → ТО `set_cell(x, void)`; клепана лишається; на силовому полі — `custom: «вибух гасне»`.
- КОЛИ `destroyed(bomb)` → ЯКЩО `in_range(bomb, other, reaction_zone)` → ТО `custom: «підірвати сусідню бомбу чи міну»` — ланцюг.
- КОЛИ `destroyed(a_bomb)` → ТО `custom: «підірвати всі A-бомби рівня»`.
- КОЛИ `input(fire)` → ЯКЩО `occupied(cell_under, variable_bomb)` → ТО `set_value(variable_bomb, current_size)` — далі розмір не змінюється.
- КОЛИ `custom: «вибух накрив Бомбузала»` → ЯКЩО `not state(player, teleporting)` → ТО `lives(-1)`.
- КОЛИ `destroyed(tile_under_player)` → ТО `fall(player)`, `lives(-1)`.

Плитки:
- КОЛИ `enter(player, ice)` → ТО `slide(player, dir)` до першої неледяної плитки.
- КОЛИ `leave(player, dissolving)` → ТО `set_cell(dissolving, void)`.
- КОЛИ `enter(player, switch)` → ТО `set_cell(linked_tile, on_off)`.
- КОЛИ `enter(player, spinner)` → ТО `move(player, rng_dir)`.
- КОЛИ `enter(player, teleport)` → ТО `teleport(player, target)`, `set_state(player, teleporting)` — недосяжний для вибухів.
- КОЛИ `contact(player, bomb)` → ЯКЩО `cell(bomb_cell, slot)` and `free(next_in_slot)` → ТО `push` уздовж паза.
- КОЛИ `input(fire_short)` → ЯКЩО `cell(cell_under, slot)` and `occupied(cell_under, bomb)` → ТО `pickup(player, bomb)`.
- КОЛИ `input(fire_short)` → ЯКЩО `has(player, bomb)` and `cell(cell_under, slot)` → ТО `place(player, bomb)`.

Вороги, час, мета:
- КОЛИ `tick` → ТО `move(dexter, dir)`, `custom: «Dexter завжди повертає праворуч, де можна; Sinister — ліворуч»`.
- КОЛИ `contact(player, dexter|sinister)` → ТО `lives(-1)`.
- КОЛИ `enter(player, mine)` → ТО `explode(own_cell, void)`, `lives(-1)`.
- КОЛИ `tick` → ЯКЩО `moving(player, any)` → ТО `custom: «таймер спадає повільніше»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lives(-1)` (?).
- КОЛИ `all_gone(bomb)` і `all_gone(mine)` → ЯКЩО `custom: «Бомбузал живий і стоїть на цілій плитці поза вибухами»` → ТО `win`, `lives(+1)`, `next_level`.
- КОЛИ `game_over` → ТО `message(password)` — код останнього рубежу кратного 8 рівнів.
- Перемога: знищено всі бомби й міни, Бомбузал на безпечній плитці. · Поразка: вибух, міна, ворог, падіння, (?) час → −1 життя; без життів — кінець гри з паролем. · Рахунок: очки й бонус за час (формула — (?)).

## Керування і ввід
- Джойстик: 4 напрямки — крок; вогонь утримати на бомбі — підпал після відліку; коротко — взяти / покласти бомбу (лише на пазовій плитці).
- Пробіл — огляд рівня (таймер іде); C= — вийти (C64).
- Титул: вогонь — старт; вгору — 2D, вниз — 3D; ліворуч — заново, праворуч — продовжити; C= — ввести пароль.
- Дроїди: «можна активувати, далі — керувати» (C64-Wiki); як саме перемикатися — (?).

## Вікна, меню, HUD
- `main-menu` (титул): вибір 2D / 3D, restart / continue, вхід у `level-password` (C=).
- `level-password`: 4-літерне слово (BOMB — 1-й рівень, SINK — 128-й).
- `game-screen`: поле + рядок стану — `score`, `lives`, бонус часу, `level-number`, `remaining-counter` бомб і мін.
- `map-window` (пробіл): огляд усього рівня, таймер не зупиняється.
- `end-screen`: кінець гри з паролем; мовні семпли «get ready», «happy birthday».
- Переходи: main-menu → (вогонь) game-screen → (усі бомби, безпечно) наступний рівень → … → (життя скінчились) end-screen → main-menu; main-menu → (C=) level-password → game-screen потрібного рівня.

## Фічі поза полем
- `levels-sequential` 130 рівнів; `level-password` після кожних 8; +1 життя за кожен пройдений рівень.
- Перемикач виду 2D згори / 3D-ізометрія — той самий стан, інший рендер (як у Kwirk).
- `hotseat` на двох (Steam-сторінка DOS-версії); C64-Wiki знає лише одного гравця.
- Звук: титульна музика, ефекти, мовні семпли.
- Undo, редактора, збережень, крім паролів, — нема (?).

## Варіації й родичі
- Ka-Blooey (SNES; JP 1990, NA 1992) — порт; Charlie Blast's Territory (N64) — наступник із видом згори чи ізометрією. Автори — Antony Crowther і David Bishop (Image Works).
- У корпусі: `games/maze-arcade/bomberman.md` (бомби кладе сам гравець і вони вибухають за таймером — протилежний підхід), `games/push-slide/blast-one-standing.md` (вибух звʼязної групи), `games/dig-gravity/boulder-dash.md` (ланцюгові вибухи), `games/maze-arcade/chips-challenge.md` (бомба-плитка).
- **Осі варіацій:** хто кладе бомби — рівень (Bombuzal) / гравець (Bomberman); запал — «зійти з бомби» / N тіків / дистанційно; форма — своя клітина / хрест / ромб; знищення ≠ реакція (Bombuzal) / одна зона; що руйнує вибух — підлогу (Bombuzal) / стіни (Bomberman); звʼязок бомб — сусідство / група A-бомб.

## Цікавинки для курсу
- Ланцюгова реакція з окремими зонами знищення й реакції (мала знищує 1 клітину, а підриває хрест) — 🥉.
- Вибух, що знищує підлогу: поле після кожного підриву інше, а герой має лишитися на цілій плитці — 📎.
- Запал «вибух, щойно зійшов» замість таймера — 🌱.
- A-бомби: група підривається цілком, незалежно від відстані — 📎.
- Змінна бомба (цикл розмірів, фіксація в мить дії) — 🌱.
- Обхідники Dexter і Sinister (права й ліва рука) на острові, що руйнується — 📎.
- Розвʼязувач порядку підривів (пошук у просторі станів поля) — 🥇.
- Вид 2D ↔ ізометрія одним перемикачем над тим самим станом — 🥉.

## Мапа на каталог
- Є: `move-4dir` ↔ крок; `chain-detonation` ↔ бомба підриває сусідні; `blast-wave` ↔ реакція малої — хрест 1; `explode-area` ↔ велика — 13 клітин (слот shape: ромб); `floor-types` ↔ лід, розчинна, клепана, пазова, силове поле, спінер, телепорт; `inertia-slide` ↔ лід; `teleport` ↔ телепорт із прихованою ціллю; `button-toggle` ↔ перемикач плитки; `push-object` ↔ бомба вздовж паза; `party-switch` ↔ керовані дроїди (?); `wall-follower` ↔ Dexter / Sinister; `touch-death` ↔ ворог і міна; `environment-death` ↔ вибух, падіння; `player-death` ↔ життя; `time-out` + `time-bonus` ↔ таймер і бонус; `status-panel` + `remaining-counter` ↔ рядок стану; `level-password` + `sequential-levels` ↔ коди кожні 8 зі 130; `map-window` ↔ огляд пробілом; `hot-seat` ↔ двоє в DOS-версії; `sound-effects` ↔ мовні семпли.
- **Нема** → пропозиції карток:
  - `+step-off-fuse` «Бомба вибухає, щойно з неї зійшов» · entities/combat · 🌱.
  - `+destructible-floor` «Вибух перетворює підлогу на провалля» · entities/interact · 📎.
  - `+crumbling-floor` (уже в корпусі) — розчинна плитка.
  - `+spinner-tile` (уже в корпусі) — тут не повертає, а штовхає у випадковий бік.
  - `+linked-detonation` «Група звʼязаних бомб вибухає разом» · entities/combat · 📎.
  - `+variable-bomb` «Бомба циклічно міняє розмір» · entities/state · 🌱.
  - `+blast-stopper` «Клітина гасить вибух» · entities/combat · 🌱.
  - `+blast-proof-floor` «Плитка, яку вибух не знищує» · entities/combat · 🌱.
  - `+rail-only-move` «Обʼєкт рухається лише пазом / рейкою» · entities/legality · 📎.
  - `+survive-final-blast` «Після останнього вибуху треба стояти на цілому» · game-logic/win · 🌱.
  - `+move-slows-timer` «Поки рухаєшся, таймер іде повільніше» · game-logic/score · 🌱.
  - `+extra-life-per-level` «+1 життя за пройдений рівень» · game-logic/score · 🌱.
  - `+view-2d-3d-toggle` (уже в корпусі) — перемикач виду.

## Пропозиції до словників
- `+trigger:blast_reached(cell)` — вибух накрив клітину (знищення, гасіння, детонація сусідів).
- `+cond:in_blast_zone(a)` — сутність у зоні поточного чи майбутнього вибуху (безпечна плитка).
- `+effect:smother` — вибух гасне на клітині (силове поле).
- `+effect:detonate_all(kind)` — підірвати всі сутності виду (A-бомби).
- `+feature:view-toggle` — 2D ↔ 3D-ізометрія без зміни логіки (уже пропонував Kwirk).
- `+feature:level-password` — прогресія паролями (уже пропонував Chip's Challenge).
- `+card:step-off-fuse`, `+card:linked-detonation`, `+card:move-slows-timer` — механік нема в каталозі.

## Джерела
- ⭐ [C64-Wiki: Bombuzal](https://www.c64-wiki.com/wiki/Bombuzal) — мета й «безпечне поле», усі плитки (клепана, лід, розчинна, пазова, силове поле, перемикач, спінер, телепорт), бомби (мала, середня, велика, змінна, A-бомби, міни), дроїди Bubble і Squeak, Dexter і Sinister, керування, 2D / 3D, паролі.
- [Wikipedia: Bombuzal](https://en.wikipedia.org/wiki/Bombuzal) — «only able to take one step away», лише мала безпечна, мала знищує свою клітину й зачіпає хрест, велика — 13 клітин і зона на клітину далі, рейки, «contact with either is fatal», версії, Ka-Blooey і Charlie Blast's Territory.
- [C64-Wiki DE](https://www.c64-wiki.de/wiki/Bombuzal) — «Nach der letzten Detonation muss sich Bombuzal auf einem sicheren Feld befinden», +1 життя за рівень.
- [Steam: Bombuzal](https://store.steampowered.com/app/1084010/Bombuzal/) — DOS-перевидання, вид згори чи ізометрія, hotseat на двох.
- YouTube: [пошук «Bombuzal gameplay»](https://www.youtube.com/results?search_query=Bombuzal+gameplay).

## Непевне
- (?) Точна форма середньої бомби (знищення й реакція): C64-Wiki каже лише «радіус на 1 більший»; ромб із 13 клітин — це велика (Wikipedia).
- (?) Чи можна підпалити середню / велику напряму: Wikipedia — можна, але загинеш; C64-Wiki — «лише в комбінації».
- (?) Навіщо дроїди Bubble і Squeak і як їх активувати (ймовірно, підпалити бомбу замість героя) — не перевірено.
- (?) Що стається, коли таймер добіг нуля; тривалість таймера, формула очок і бонусу.
- (?) Що на місці знищеної плитки провалля, у яке падають, — з памʼяті: джерела кажуть лише «destroyed by an explosion» і що після останнього вибуху треба стояти на безпечному полі. Чи може Бомбузал сам зійти в порожнечу, чи такий крок заблоковано, — теж невідомо.
- (?) Hotseat — лише в DOS / Steam чи в усіх версіях; як чергуються гравці.
- (?) Порядок вибору напрямку Dexter / Sinister на розвилці — у джерелах лише «завжди праворуч / ліворуч» і «за / проти годинникової».
