---
title: Sword of Fargoal
slug: sword-of-fargoal
aka: [Fargoal, "Sword of Fargoal Legends", Меч Фарґоала]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1982
platforms: [VIC-20, C64, iOS (2009)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sword_of_Fargoal", best: true, note: "темні рівні, що світлішають, храм ховає від ворогів, авто-бій, злодії, відлік після меча, сходи породжують монстрів"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Sword_of_Fargoal", note: "C64-Wiki: меч на 15–20 рівні, ~30 хв, пороги досвіду 200/400/800, вміст скринь, заклинання й клавіші"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Sword_of_Fargoal", note: "RogueBasin: 2000 секунд на повернення, меч можна вкрасти дорогою"}
  - {kind: other, url: "https://www.mocagh.org/epyx/fargoal-refcard.pdf", note: "картка Epyx (C64): легенда символів, клавіші, маяки, panic button, мандрівні монстри"}
  - {kind: official, url: "https://www.fargoal.com/fargoal/features/", note: "ремейк 2009: типи рівнів, 30+ монстрів, тач-керування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sword+of+Fargoal+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, dungeon-generation, stairs-levels, fog-of-war, hp-damage, unit-xp-skills, inventory-items, item-pickup, round-currency, thief, chase-player, spawn-points, teleport-random-exit, temporary-modes, time-out, player-death, permadeath, score-records, drop-on-death, +remembered-map, +auto-battle, +sneak-attack, +sanctuary-cell, +altar-sacrifice, +escape-countdown, +hidden-trap-square, +gold-capacity, +beacon-anchor, +panic-button, +level-regenerate-on-return, +wandering-monster, +enemy-picks-up-items]
proposes: ["+trigger:sneak_attack", "+cond:gold_capacity(op, n)", "+effect:sacrifice(gold)", "+effect:regenerate_level", "+role:sanctuary", "+ui:spell-charges", "+feature:panic-button", "+card:escape-countdown", "+card:sanctuary-cell", "+card:beacon-anchor"]
author: opus
date: 2026-11-09
---

# Sword of Fargoal — спустись у темряву по меч, а потім тікай нагору, поки йде відлік

## Суть
Воїн спускається випадково згенерованими рівнями підземелля, щоб знайти Меч Фаргоала (лежить десь між 15-м і 20-м рівнем) і винести його на поверхню. Кожен рівень спершу цілком темний і світлішає лише там, де воїн пройшов; бій автоматичний — гравець вирішує лише, коли нападати й коли тікати. Щойно меч у руках, починається відлік: не встиг вийти — меч втрачено назавжди. На кожному рівні є храм, де воїна не видно монстрам і куди він жертвує золото за досвід.

## Поле і час
- Вид згори, клітинний лабіринт рівня; рух у 8 напрямках (джойстик).
- Рівні генеруються випадково; після виходу з рівня й повернення планування **нове** (рівень не зберігається).
- Видимість: рівень темний, пройдені клітини лишаються відкритими (мапа «малюється» ходою); заклинання Light розширює огляд до кінця рівня.
- Real-time: воїн рухається вільно, монстри — рідкими кроками з інтервалами. Довго стояти на рівні небезпечно: зі сходів вище й нижче приходять мандрівні монстри.
- Відлік після здобуття меча — 2000 секунд (RogueBasin; C64-Wiki каже «близько 30 хвилин»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Воїн | player | HP, рівень досвіду, золото (спершу до 100), предмети, заряди заклинань | рух 8 напрямків; бій сам собою при контакті |
| Стіна | static | — | непрохідна |
| Невідкрита клітина | zone | темна / відкрита | відкривається, коли воїн поруч; відкрита лишається на мапі рівня |
| Сірий квадрат | container | скарб або пастка (приховано) | що це — видно, лише коли ступиш |
| Скриня | container | предмет / золото / пастка | відкривається при вході; монстр може підібрати її, наступивши |
| Мішок золота | pickup | сума | +золото до ліміту; монстр підбирає, наступивши |
| Храм | zone | один на рівень | жертва золота → досвід; монстри не бачать і не атакують; HP відновлюються вдвічі швидше |
| Сходи вгору / вниз | static | напрям | перехід на сусідній рівень; звідси приходять мандрівні монстри |
| Яма-пастка | hazard | — | падіння й шкода; Drift запобігає |
| Вибух | hazard | — | шкода |
| Обвал стелі | hazard | — | шкода; вчасний Teleport рятує |
| Маяк | object | один на рівень | у клітині маяка воїн невидимий; телепорти рівня ведуть до нього |
| Монстр-істота | enemy | сила | ходить рідкими кроками, наближається до воїна |
| Гуманоїд | enemy | сильніший за істот | небезпечніший; частина краде |
| Злодій | enemy | — | краде золото; убитий — золото повертається |
| Меч Фаргоала | pickup | рівень 15–20 | запускає відлік; може бути вкрадений |
| Зілля зцілення | pickup | — | +HP |
| Магічний мішок | pickup | — | більший ліміт золота |
| Мапа | pickup | — | відкриває мапу рівня |
| Зачарована зброя | pickup | — | сильніший удар |
| Амулет зцілення / світла (рідкісні) | pickup | — | постійна регенерація / постійне світло |
| Свиток заклинання | pickup | Shield, Regeneration, Teleport, Invisibility, Light, Drift | + заряд відповідного заклинання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir8)` → ЯКЩО `free(cell)` → ТО `move(warrior, dir)`; стіна → `block`.
- КОЛИ `tick` → ТО `reveal(cells around warrior)`; відкрите лишається видимим до кінця рівня.
- КОЛИ `timer(monster_step)` → ТО `custom: «монстр робить крок до воїна»` (кроки рідкі, не щотіку).
- КОЛИ `contact(warrior, monster)` → ТО `custom: «автоматичний бій: обидва бʼють без участі гравця»`, `damage(n)` обом.
- КОЛИ `input(dir8)` під час бою → ЯКЩО `not custom: «монстр напав першим, до кроку воїна»` → ТО `custom: «втеча з бою»`; інакше `block` (`+trigger:sneak_attack`).
- КОЛИ `died(monster)` → ТО `counter(xp, +n)`; інколи `spawn(item)` на місці.
- КОЛИ `counter(xp, >=, 200 × 2^k)` → ТО `custom: «рівень +1: сильніший удар, більше HP»` (200 → 1-й, 400, 800…).
- КОЛИ `enter(warrior, grey_square)` → ТО `reveal(cell)`; ЯКЩО `cell(here, chest)` → ТО `pickup`; ЯКЩО `cell(here, trap)` → правила пасток.
- КОЛИ `enter(warrior, pit_trap)` → ЯКЩО `state(warrior, drift)` → ТО `clear_state(warrior, drift)`; інакше `fall(warrior)`, `damage(n)`.
- КОЛИ `enter(warrior, ceiling_trap)` → ЯКЩО `custom: «вчасно вжито Teleport»` → ТО `teleport(warrior, random)`; інакше `damage(n)`.
- КОЛИ `enter(warrior, explosion_trap)` → ТО `damage(n)`.
- КОЛИ `contact(warrior, gold)` → ЯКЩО `custom: «золото < ліміту»` → ТО `pickup`, `currency(+n)`; інакше `block` для решти суми.
- КОЛИ `picked(warrior, magic_sack)` → ТО `custom: «ліміт золота зростає»`.
- КОЛИ `contact(monster, gold|chest)` → ТО `disappear(gold|chest)`, `custom: «монстр несе знахідку»`.
- КОЛИ `contact(thief, warrior)` → ТО `take(warrior, gold)`; КОЛИ `died(thief)` → ТО `give(warrior, stolen gold)`.
- КОЛИ `enter(warrior, temple)` → ТО `currency(−all)`, `counter(xp, +n)` за пожертву, `set_state(warrior, unseen)`.
- КОЛИ `tick` → ЯКЩО `cell(here, temple)` → ТО `heal(warrior, ×2 regen)`; монстри — `block` для атаки.
- КОЛИ `input(S)` → ЯКЩО `has(warrior, shield)` → ТО `set_state(warrior, shield, next fight)` — у наступному бою шкоди нема.
- КОЛИ `input(R)` → ЯКЩО `has(warrior, regeneration)` → ТО `set_state(warrior, regen)`.
- КОЛИ `input(I)` → ЯКЩО `has(warrior, invisibility)` → ТО `set_state(warrior, invisible)` — монстри не йдуть прямо до воїна.
- КОЛИ `input(L)` → ЯКЩО `has(warrior, light)` → ТО `set_state(warrior, light)`; `input(O)` — вмикає/вимикає; КОЛИ `level_start` → ТО `clear_state(warrior, light)`.
- КОЛИ `input(T)` → ЯКЩО `custom: «на рівні поставлено маяк»` → ТО `teleport(warrior, beacon)`; інакше `teleport(warrior, random cell)`, `custom: «часто губиться мапа рівня»`.
- КОЛИ `input(H)` → ЯКЩО `has(warrior, potion)` → ТО `heal(warrior, n)`, `take(warrior, potion)`.
- КОЛИ `input(+)` → ЯКЩО `has(warrior, beacon)` → ТО `place(warrior, beacon)`.
- КОЛИ `input(fire)` → ЯКЩО `occupied(here, beacon)` → ТО `teleport(warrior, temple)` без витрати телепорту.
- КОЛИ `input(fire held)` → ТО `custom: «panic: автоматично вжити корисне — зілля, Teleport, Drift»`.
- КОЛИ `input(fire|C)` → ЯКЩО `cell(here, stairs|pit)` → ТО `custom: «на рівень вище / нижче»`, `custom: «рівень генерується наново»`.
- КОЛИ `custom: «воїн довго лишається на рівні»` → ТО `spawn_at(monster, stairs)` — мандрівні монстри приходять згори й знизу.
- КОЛИ `picked(warrior, sword)` → ТО `timer(start, 2000 s)`.
- КОЛИ `custom: «меч украдено дорогою нагору»` → ТО `take(warrior, sword)`; ЯКЩО `timer(>, 0)` → ТО `custom: «спускатись знову на рівень меча»`.
- КОЛИ `counter(sword_timer, ==, 0)` → ЯКЩО `has(warrior, sword)` → ТО `custom: «меч втрачено назавжди»`, `lose`.
- КОЛИ `reach(warrior, surface)` → ЯКЩО `has(warrior, sword)` → ТО `win`.
- КОЛИ `hp_zero(warrior)` → ТО `lose`, `game_over` — смерть остаточна, гра з початку.
- Перемога: меч на поверхні до кінця відліку. Поразка: смерть або сплив час із мечем. Рахунок: таблиця рекордів (формула не відома).

## Керування і ввід
- Джойстик — рух у 8 напрямках; кнопка — підйом/спуск по сходах і ямах, пас на порожній клітині (?), активація Drift; утримана кнопка — **panic button**.
- Клавіші (C64): H — зілля, S / R / T / I / L — заклинання, O — світло вкл/викл, + — поставити маяк, B — закопати золото, C — сходи, P — пас, Q — вийти.
- Ремейк 2009: тач — торкнутись місця, і герой іде туди.

## Вікна, меню, HUD
- `splash-screen` — титул (?).
- `game-screen`: мапа рівня згори з відкритими клітинами; `status-panel` — HP, золото, досвід, рівень підземелля, заряди заклинань (`+ui:spell-charges`) (?); `timer-countdown` після меча (?).
- Легенда символів (на картці Epyx): воїн, золото, сірий квадрат (скарб/пастка), монстри, храм, сходи вгору/вниз.
- `end-screen` — смерть / перемога; `leaderboard` — рекорди (?).
- Переходи: титул → гра → (смерть / вихід із мечем) → рекорди → титул.

## Фічі поза полем
- `permadeath`: одна спроба, після смерті — нова гра.
- `leaderboard-local` — рекорди (на C64-Wiki є таблиця рахунків гравців).
- Ремейк iOS (2009, «Legends» 2011+): понад 20 рівнів, близько 107 рівнів і варіацій генеруються на старті гри, три типи рівнів, лабіринт рівня меча, крипти з wraiths і скелетами, сховища з артефактами.

## Варіації й родичі
- Оригінал VIC-20 (1982) → C64 (Epyx, 1983) додав маяки й «panic button» → ремейк iOS (2009) з 30+ типами монстрів (ogres, trolls, wyverns з отрутою, Shadow Dragons, ельфи з луками, rogues, assassins).
- Попередник автора — Gammaquest II: мапа відкривається шматками й лишається світлою позаду героя.
- Родичі: [rogue](rogue.md) (покрокова класика, видимість кімнатами), [hack](hack.md), [larn](larn.md) (теж дедлайн забігу, але на всю гру), [dungeons-of-daggorath](dungeons-of-daggorath.md) (real-time підземелля того ж часу), [beneath-apple-manor](beneath-apple-manor.md), [castle-of-the-winds](castle-of-the-winds.md).
- Осі варіацій: **бій** (авто з вибором «бити/тікати» / покроковий / дія) · **таймер** (нема / на весь забіг / лише на втечу після мети) · **рівень** (зберігається / генерується при кожному вході) · **безпечна зона** (нема / храм на рівні / маяк, який ставиш сам).

## Цікавинки для курсу
- Відлік «на втечу» після ключової події: гра змінює мету й напрям руху — 🌱.
- Храм-сховок: клітина, у якій ворог тебе не бачить і не атакує, + подвоєна регенерація — 🌱.
- Монстри підбирають золото й скрині, злодій повертає вкрадене, коли вбитий — предмет у «кишені» ворога — 📎.
- Маяк як точка-якір для всіх телепортів рівня + безкоштовний телепорт до храму — 📎.
- Panic button: одна кнопка сама обирає найкорисніший предмет у кризі — 📎 (пріоритети предметів).
- Рівень генерується наново при кожному вході (на відміну від Rogue/NetHack, де рівні памʼятаються) — 🥉 разом із генератором.

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `fog-of-war` (темрява, відкриття ходою) · `hp-damage` · `unit-xp-skills` (рівні досвіду) · `inventory-items` / `item-pickup` · `round-currency` (золото) · `thief` · `chase-player` · `spawn-points` (сходи) · `teleport-random-exit` (Teleport без маяка) · `temporary-modes` (Shield, Invisibility, Light) · `time-out` (відлік із мечем) · `player-death` · `permadeath` · `score-records` · `drop-on-death`.
- Вже пропоновані: `+remembered-map` (як у Rogue) · `+auto-battle` · `+sneak-attack` · `+altar-sacrifice` · `+wandering-monster`.
- **Нема** → пропозиції карток:
  - `+escape-countdown` «Після ключової дії — таймер на втечу» · game-logic/lose · 🌱.
  - `+sanctuary-cell` «Клітина, де ворог не бачить і не атакує» · entities/interact · 🌱.
  - `+hidden-trap-square` «Сірий квадрат: скарб чи пастка — видно, лише ступивши» · entities/interact · 🌱.
  - `+gold-capacity` «Ліміт золота, що зростає від мішків» · entities/state · 🌱.
  - `+beacon-anchor` «Поставлений маяк — ціль усіх телепортів рівня» · entities/interact · 📎.
  - `+panic-button` «Одна кнопка вживає найкорисніший предмет» · interface/input · 📎.
  - `+level-regenerate-on-return` «Рівень генерується знову при кожному вході» · levels/generation · 🥉.
  - `+enemy-picks-up-items` «Ворог підбирає предмети з підлоги» · entities/move · 📎.

## Пропозиції до словників
- `+trigger:sneak_attack` — монстр почав бій раніше, ніж воїн зробив крок (втеча заборонена).
- `+cond:gold_capacity(op, n)` — скільки золота ще влазить.
- `+effect:sacrifice(gold)` — віддати золото в храмі/на вівтарі за досвід (як у Telengard).
- `+effect:regenerate_level` — згенерувати рівень наново при вході.
- `+role:sanctuary` — клітина-сховок від ворогів (храм, маяк).
- `+ui:spell-charges` — лічильники зарядів кожного заклинання.
- `+feature:panic-button` — автоматичний вибір рятівного предмета.
- `+card:escape-countdown` · `+card:sanctuary-cell` · `+card:beacon-anchor`.

## Джерела
- ⭐ [Wikipedia: Sword of Fargoal](https://en.wikipedia.org/wiki/Sword_of_Fargoal) — темні рівні, що світлішають, сходи вгору/вниз, нове планування після повернення, храм на кожному рівні (жертва золота → досвід, невидимість), авто-бій, втеча крім «підкраденої атаки», монстри ходять рідкими кроками, сходи породжують мандрівних, скрині з пастками (вибух, обвал, яма), магічні мішки, ліміт 100 золота, злодії, відлік після меча, permadeath.
- [C64-Wiki: Sword of Fargoal](https://www.c64-wiki.com/wiki/Sword_of_Fargoal) — меч між 15-м і 20-м рівнем, ~30 хв на вихід, пороги досвіду 200/400/800, храм (монстри не атакують, регенерація ×2), повний вміст скринь, заклинання з клавішами, кнопка-panic, фінал із Gedwyn.
- [RogueBasin: Sword of Fargoal](https://www.roguebasin.com/index.php/Sword_of_Fargoal) — 2000 секунд на повернення, меч крадуть дорогою, Teleport проти обвалу, Drift проти ями.
- [Картка Epyx для C64](https://www.mocagh.org/epyx/fargoal-refcard.pdf) — легенда символів, 8 напрямків, H/I/R/T/S/L/O/+/B/C/P/Q, маяки, мандрівні монстри зі сходів вище й нижче.
- [fargoal.com: Features](https://www.fargoal.com/fargoal/features/) — ремейк 2009: 20+ рівнів, ~107 рівнів і варіацій, 3 типи рівнів, 30+ монстрів, тач-рух.

## Непевне
- (?) Що саме робить «пас» (P / кнопка на порожній клітині) — «Pass over next square»: постояти хід чи переступити клітину.
- (?) Навіщо закопувати золото (B) — сховати від злодіїв чи понад ліміт; джерела не пояснюють.
- (?) Яма-пастка скидає на рівень нижче чи лише ранить: C64-Wiki каже «падаєш і травмуєшся», картка — що кнопкою можна лізти «вгору чи вниз» біля ям.
- (?) Скільки досвіду дає золото в храмі — джерела без формули.
- (?) Кількість рівнів оригіналу (рядок черги й ремейк кажуть «20+»; C64-Wiki — лише «меч на 15–20 рівні»).
- (?) Склад HUD (які лічильники на екрані) і формула рахунку — не бачив.
- (?) Хто може вкрасти меч (злодій-гуманоїд?) — RogueBasin каже лише «може бути вкрадений».
