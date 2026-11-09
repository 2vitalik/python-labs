---
title: Starquake
slug: starquake
aka: [BLOB]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: collect
year: 1985
platforms: [ZX Spectrum]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Starquake_(video_game)", best: true, note: "BLOB, 512 екранів, 9 частин ядра, FIFO-інвентар на 4, ховер-платформи й доки, тимчасові платформи, телепорти з кодами, піраміди обміну, очки, рандомізація предметів"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-info/s/Starquake.txt", note: "інструкція: клавіші, лазер і мости як ресурси, ховер-пади, вакуумні труби, 16 слів-кодів телепортів, ключ і картка доступу, слабка підлога, вороги"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/4873/ZX-Spectrum/Starquake", note: "картка ZX: автор Stephen Crow, Bubble Bus 1985, flip-screen, відгуки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Starquake+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, item-pickup, inventory-items, inventory-limit, key-and-door, teleport, projectile-shot, touch-death, hp-damage, player-death, timed-despawn, destructible-blocks, carrier-platform, event-points, score-records, time-out, game-pause, controls-remap, status-panel, game-screen, keyboard-controls, +flip-screen-rooms, +place-bridge, +fifo-inventory, +teleport-code-word, +trade-exchange, +vehicle-dock, +random-setup, +weak-floor-smash, +lowest-stat-refill]
proposes: ["+cond:inventory_full", "+trigger:landed", "+window:teleport-code-entry", "+card:fifo-inventory", "+card:teleport-code-word", "+card:trade-exchange", "+card:vehicle-dock", "+card:weak-floor-smash", "+card:lowest-stat-refill"]
author: opus
date: 2026-11-09
---

# Starquake — BLOB обшукує 512 екранів планети, будує тимчасові мости й телепортується за словами-кодами, щоб зібрати 9 частин ядра

## Суть
Flip-screen платформер-пригода: BLOB має зібрати й донести до ядра планети **9 частин**, поки воно не вибухнуло. Набір потрібних частин і розкладка предметів **випадкові для кожної гри**, а мапа й телепорти — сталі. BLOB несе до 4 предметів у черзі FIFO (першим узяв — першим віддаси), будує під собою мости, що швидко розсипаються, літає на ховер-падах (які сідають лише в доках) і міняє предмети в пірамідах Хеопса. Ядро — логістика: що нести, у якому порядку, якою дорогою.

## Поле і час
- Мапа — 512 екранів, повʼязаних краями (flip-screen), плюс телепорти-будки й вакуумні труби; кожен екран — тайлова сцена збоку.
- Видно поточний екран; мапи в грі нема.
- Real-time; гравітація; ліміт часу на ремонт ядра (Wikipedia).
- Випадковість лише на старті гри: розміщення обʼєктів і які з них потрібні ядру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| BLOB | player | енергія, лазер, запас мостів, життя, 4 слоти | бігає, падає, стріляє лазером, кладе міст під себе, бере/кладе предмет |
| Міст (bridge) | terrain | короткий час | кладеться під BLOB, швидко розсипається |
| Ховер-пад | platform | — | BLOB стає й злітає вгору; у польоті не може брати/класти предмети; зійти — лише в доку |
| Док | static | — | місце посадки й висадки з ховер-пада |
| Вакуумна труба / ліфт | terrain | напрям угору | засмоктує BLOB на вищий рівень; на ховер-паді не можна |
| Телепорт-будка | static | слово-код | перенесення до будки з введеним кодом (16 кодів; QUAKE — до ядра) |
| Ядро | static | 9 гнізд | показує потрібні предмети; приймає їх по одному |
| Частина ядра | pickup | тип | потрібна ядру (який саме набір — випадково) |
| Ключ | pickup | — | відчиняє деякі двері; місце випадкове |
| Картка доступу | pickup | — | замінює номерний чип для дверей безпеки; дає торгувати в піраміді |
| Двері / двері безпеки | gate | номер чипа | відчиняються ключем / чипом / карткою |
| Піраміда Хеопса | container | — | з карткою: віддай предмет — отримай корисніший (часто частину ядра) |
| Пакети енергії, лазера, мостів | pickup | — | поповнюють свій ресурс |
| Циліндр (re-equip) | pickup | — | поповнює найнижчий з ресурсів; на останньому житті ще й +1 життя |
| Джойстик | pickup | — | +1 життя |
| Слабка підлога | terrain | — | ламається, якщо BLOB падає на неї з висоти |
| Таємний прохід | terrain | — | вузький, лише для BLOB; скорочує шлях |
| Літаючі істоти | enemy | 80–320 очок | дотик забирає енергію; знищуються лазером |
| Міни | enemy | — | рухаються як істоти; дотик — смерть |
| Дзиґи (spinning tops) | enemy | — | дотик — миттєва смерть |
| Шипи, енергетичні поля | hazard | — | дотик — смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(blob, dir)`.
- КОЛИ `tick` → ЯКЩО `not supported(blob)` → ТО `fall(blob)`.
- КОЛИ `input(down)` → ЯКЩО `counter(bridges, >, 0)` і `free(cell_below)` → ТО `place(blob, bridge)`, `counter(bridges, -1)`; КОЛИ `timer(bridge_life)` → ТО `disappear(bridge)`.
- КОЛИ `input(up)` → ЯКЩО `occupied(here, item)` і `custom: «є вільний слот із 4»` → ТО `pickup`; ЯКЩО слоти повні → `custom: «найстаріший предмет кладеться на місце нового»` (FIFO).
- КОЛИ `input(fire)` → ЯКЩО `counter(laser, >, 0)` → ТО `spawn(laser_shot)`, `counter(laser, -1)`; КОЛИ `contact(laser_shot, creature)` → ТО `disappear_b`, `score(80..320)`.
- КОЛИ `contact(blob, creature)` → ТО `hp(blob, -n)`; КОЛИ `contact(blob, mine|top|spikes|field)` → ТО `lives(-1)`; КОЛИ `hp_zero(blob)` → ТО `lives(-1)`.
- КОЛИ `enter(blob, hover_pad)` + `input(up)` → ТО `attach(blob, hover_pad)` — політ; ЯКЩО `state(blob, flying)` → `input(up)` біля предмета — `block`.
- КОЛИ `enter(blob, dock)` → ЯКЩО `state(blob, flying)` → ТО `custom: «можна зійти з пада»`; поза доком — не можна.
- КОЛИ `enter(blob, tube)` → ЯКЩО `not state(blob, flying)` → ТО `move(blob, up_level)`.
- КОЛИ `enter(blob, teleport)` → ТО `window(teleport-code)`; КОЛИ `input(code_word)` → ТО `teleport(blob, booth[code])`.
- КОЛИ `contact(blob, door)` → ЯКЩО `has(blob, key)` або `has(blob, chip[n])` або `has(blob, access_card)` → ТО `custom: «двері відчиняються»`; інакше `block`.
- КОЛИ `enter(blob, pyramid)` → ЯКЩО `has(blob, access_card)` → ТО `custom: «обмін: віддати предмет, отримати інший»`.
- КОЛИ `enter(blob, core)` → ЯКЩО `has(blob, needed_piece)` → ТО `take(blob, piece)`, `counter(core, +1)`, `score(10000)`.
- КОЛИ `custom: «BLOB у новому екрані вперше»` → ТО `score(250)`.
- КОЛИ `contact(blob, energy|laser|bridge_pack)` → ТО `custom: «поповнити свій ресурс»`; КОЛИ `contact(blob, cylinder)` → ТО `custom: «поповнити найнижчий ресурс»`; ЯКЩО `counter(lives, =, 1)` → ТО `lives(+1)`.
- КОЛИ `contact(blob, joystick)` → ТО `lives(+1)`.
- КОЛИ `custom: «BLOB впав з висоти на слабку підлогу»` → ТО `set_cell(floor, empty)`.
- КОЛИ `counter(core, =, 9)` → ТО `win`; КОЛИ `timer(limit)` → ТО `custom: «ядро вибухає»`, `game_over`; КОЛИ `counter(lives, =, 0)` → ТО `game_over`.
- Перемога: 9 частин в ядрі. Поразка: життя скінчились або вийшов час. Рахунок: істоти + частини ядра + нові екрани.

## Керування і ввід
- O / P — ліво/право; Q — вгору / взяти предмет; A — вниз / покласти міст; M — лазер.
- Клавіші перевизначаються; Kempston, Interface 2, Cursor.
- BREAK/SPACE — пауза; A+S+D+F+G разом — перервати гру.
- Ввід слова-коду в телепорті з клавіатури (?).

## Вікна, меню, HUD
- `main-menu` (?): старт, вибір керування, перевизначення клавіш.
- `game-screen`: екран + HUD — енергія, лазер, запас мостів, життя, 4 слоти інвентарю, рахунок (?).
- `custom-window` «телепорт»: ввід слова-коду призначення.
- `custom-window` «ядро»: показує потрібні частини (?).
- `end-screen` — рахунок / рекорд (?).

## Фічі поза полем
- Рандомізація стартового розкладу предметів і набору потрібних частин — `random-setup`.
- Читерський POKE на безкінечні життя (Your Sinclair) випадково прибирав таємні проходи.
- Збереження нема.

## Варіації й родичі
- Родичі «відкритий світ з flip-screen екранів»: [jet-set-willy](jet-set-willy.md), [montezumas-revenge](montezumas-revenge.md), [treasure-island-dizzy](treasure-island-dizzy.md) (інвентар і логістика).
- Тимчасові платформи: [solomons-key](solomons-key.md) (блок назавжди), [toki-tori](toki-tori.md) (міст-ресурс).
- Пізніше: Quakestar (ZX Spectrum Next) — натхнений Starquake.
- Осі: **інвентар** (1 предмет / N з вибором / FIFO-черга); **транспорт** (ходьба / пад з доками / ліфти / телепорти з кодами); **рандомізація** (нема / розклад предметів при сталій мапі).

## Цікавинки для курсу
- FIFO-інвентар на 4: порядок підбору = порядок віддачі — 🌱 (deque).
- Телепорти з адресою-словом: таблиця «код → будка» — 🌱.
- Ховер-пад, з якого можна зійти лише в доці (стан «у транспорті» з обмеженнями дій) — 📎.
- Тимчасовий міст як витратний ресурс — 📎.
- Рандомізація набору потрібних предметів при сталій мапі (гра щоразу інша) — 🥉 (гарантувати прохідність).
- Пакет, що поповнює найнижчий ресурс — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `item-pickup` · `inventory-items` · `inventory-limit` (4) · `key-and-door` · `teleport` · `projectile-shot` (лазер) · `touch-death` · `hp-damage` (енергія) · `player-death` · `timed-despawn` (мости) · `destructible-blocks` (слабка підлога) · `carrier-platform` (ховер-пад, труби) · `event-points` · `score-records` · `time-out` · `game-pause` · `controls-remap` · `status-panel` · `game-screen` · `keyboard-controls`.
- Уже в корпусі з `+`: `+flip-screen-rooms` · `+place-bridge` · `+random-setup`.
- **Нема** → пропозиції карток:
  - `+fifo-inventory` «Інвентар-черга FIFO» · entities/state · 🌱.
  - `+teleport-code-word` «Телепорт за словом-адресою» · entities/interact · 🌱.
  - `+trade-exchange` «Обмінник: предмет → інший предмет» · game-logic/economy · 📎.
  - `+vehicle-dock` «Транспорт: сісти/зійти лише в доці, обмеження дій» · entities/move · 📎.
  - `+weak-floor-smash` «Підлога ламається від падіння з висоти» · entities/interact · 🌱.
  - `+lowest-stat-refill` «Бонус поповнює найнижчий ресурс» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:inventory_full` — усі слоти зайняті (FIFO-витіснення).
- `+trigger:landed` — приземлення після падіння з висоти (слабка підлога).
- `+window:teleport-code-entry` — ввід адреси телепорту.
- `+card:fifo-inventory`, `+card:teleport-code-word`, `+card:trade-exchange`, `+card:vehicle-dock`, `+card:weak-floor-smash`, `+card:lowest-stat-refill` — див. вище.

## Джерела
- ⭐ [Wikipedia: Starquake](https://en.wikipedia.org/wiki/Starquake_(video_game)) — BLOB, ядро, FIFO-інвентар, ховер-пади, мости, ліфти, телепорти, піраміди, предмети, вороги, очки, 512 екранів, рандомізація.
- [Інструкція (Spectrum Computing)](https://spectrumcomputing.co.uk/pub/sinclair/games-info/s/Starquake.txt) — клавіші, ресурси, телепорт-слова, двері, слабка підлога, вороги.
- [Spectrum Computing: картка](https://spectrumcomputing.co.uk/entry/4873/ZX-Spectrum/Starquake) — автор, рік, жанр, керування.

## Непевне
- (?) Тривалість ліміту часу, стартова кількість життів і ресурсів — у джерелах нема.
- (?) Порти на інші платформи (C64, CPC, BBC, Atari ST, MSX…) — з памʼяті, не перевірено; у шапці лише ZX.
- (?) Як саме витісняє FIFO при повному інвентарі (кладе найстаріший чи відмова).
- (?) Wikipedia: тимчасовими платформами можна проходити «пастки-двері», падаючи на них, — механізм незрозумілий.
- (?) Склад HUD і вигляд вікна вводу коду.
- (?) Чи дають життя за очки, чи лише предметами.
