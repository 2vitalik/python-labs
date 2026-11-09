---
title: Bone Cruncher
slug: bone-cruncher
aka: [Bonecruncher]
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1987
platforms: [BBC Micro, Acorn Electron, C64, Amiga]
links:
  - {kind: other, url: "https://acorn.huininga.nl/pub/mirrors/8bs.com/elecgame/bonecruncher.htm", best: true, note: "інструкція оригіналу (Electron/BBC): усі обʼєкти, клавіші, паролі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bone_Cruncher", note: "огляд: Superior Software, Glooks, монстри, Fozzy, вулкан"}
  - {kind: wiki, url: "https://c64-wiki.com/wiki/BoneCruncher", note: "C64: очки за дії, «вітер», паролі 22 секцій, функціональні клавіші"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bone+Cruncher+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, dig-terrain, push-object, gravity-fall, wall-follower, touch-death, environment-death, player-death, item-pickup, inventory-limit, key-and-door, spawner-entity, event-points, sequential-levels, level-password, restart-level, game-pause, status-panel, goal-counter, +snap-action, +shifting-gravity, +trap-to-convert, +craft-at-station, +ally-guard, +self-destruct]
proposes: ["+effect:set_gravity", "+cond:surrounded", "+axis:gravity-shifting", "+ui:wind-meter", "+feature:self-destruct", "+card:shifting-gravity", "+card:trap-to-convert", "+card:craft-at-station", "+card:ally-guard"]
author: opus
date: 2026-11-09
---

# Bone Cruncher — Boulder Dash навпаки: «камені» живі й повзуть за запахом мила

## Суть
Дракон Боно збирає скелети в замку, варить з них мило в казані й відносить його морським монстрам, що купаються біля виходів. Від [Boulder Dash](boulder-dash.md) лишились копання землі й штовхання, але **«камені» тут — живі Glooks**: вид згори, падіння вниз нема, натомість Glooks повзуть у бік «аромату мила», і цей напрям змінюється після кожної доставки. Кожна доставка перекроює лабіринт, тому порядок доставок — головна задача. Вороги стають ресурсом: монстр, затиснутий Glook-ами, перетворюється на скелет.

## Поле і час
- Замок із 22 камер; камера — прямокутна сітка, вид згори (не збоку, як у BD).
- Один шар: у клітині один елемент; у Glooks є стан «рухається / стоїть».
- Real-time. «Гравітація» одна на всю камеру й має напрям: Glooks зсуваються в нього, доки не вперлись. Напрям задає вхід на сходи (BBC/Electron); на C64 — «вітер» з лічильником до наступної зміни.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боно | player | життя; несе ≤9 скелетів, ≤9 мила, ≤9 ключів | рух 4 напрямки; копає землю; штовхає один Glook; дія + напрямок — без кроку |
| Земля | terrain | — | Боно викопує; у ній бувають замуровані монстри |
| Цвіль (C64) | terrain | — | прибирається дією без кроку |
| Стіна | static | — | непрохідна |
| Glook | object | напрям = напрям аромату; рухається / стоїть | повзе в напрямку аромату до упору; один штовхається, ряд — непрохідний; небезпечний лише в русі |
| Скелет | pickup | 10 очок (C64) | збирається; 5 = одне мило; павуки їдять |
| Казан | switch | — | дотик збоку: 5 скелетів → 1 мило |
| Сходи до моря (купальня монстра) | gate | 5 на камеру | доставка мила; змінює напрям аромату |
| Монстр (goblin) | enemy | — | дотик — смерть; затиснутий Glook-ами → скелет; у пастці-люку зникає без скелета |
| Павук | enemy | невбивний | тримається **лівого** краю; їсть скелети; укус смертельний |
| Fozzy | ally | енергія, 3 життя | тримається **правого** краю; стримує монстрів і павуків; імунний до павуків; оглушений — штовхни; застряг або енергія 0 → гине |
| Пастка-люк | hazard | — | ковтає монстрів і самого Боно |
| Ключ | pickup | 10 очок (C64) | відкриває двері |
| Двері | gate | — | прохід лише з ключем |
| Вулкан | spawner | прихований, 1 на камеру | крок на певну клітину відкриває його; вивергає Glooks |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth|empty)` → ТО `move(bono, dir)`; земля → `set_cell(empty)`.
- КОЛИ `input(action+dir)` → ТО `custom: «копнути землю / зсунути Glook у сусідній клітині, не рухаючись»`.
- КОЛИ `contact(bono, glook)` → ЯКЩО `free(cell_behind)` and `state(glook, still)` → ТО `push`; ЯКЩО за ним ще Glook → `block`.
- КОЛИ `tick` → ЯКЩО `free(cell in aroma_dir)` → ТО `move(glook, aroma_dir)`, `set_state(glook, moving)`; інакше `clear_state(glook, moving)`.
- КОЛИ `contact(moving glook, bono)` → ТО `lose`, `lives(-1)`.
- КОЛИ `blocked(monster)` → ЯКЩО `custom: «surrounded: затиснутий Glook-ами, жодного ходу»` → ТО `transform(skeleton)`.
- КОЛИ `enter(monster, trapdoor)` → ТО `disappear_a` (скелета нема); КОЛИ `enter(bono, trapdoor)` → ТО `lose`.
- КОЛИ `contact(monster|spider, bono)` → ТО `lose`, `lives(-1)`.
- КОЛИ `tick` → ТО `custom: «павук — тримається лівої стіни; Fozzy — правої»`.
- КОЛИ `contact(spider, skeleton)` → ТО `disappear_b`.
- КОЛИ `contact(fozzy, monster|spider)` → ТО `block` для ворога; `custom: «енергія Fozzy спадає»`.
- КОЛИ `counter(fozzy_energy, ==, 0)` або `blocked(fozzy)` надовго → ТО `custom: «Fozzy гине, −1 його життя»`.
- КОЛИ `contact(bono, skeleton|key)` → ЯКЩО `custom: «нести < 9»` → ТО `pickup`, `score(10)`.
- КОЛИ `contact(bono, cauldron)` → ЯКЩО `has(bono, skeleton, 5)` → ТО `take(skeleton, 5)`, `give(soap)`, `score(100)`.
- КОЛИ `enter(bono, stairs)` → ЯКЩО `has(bono, soap)` → ТО `take(soap)`, `counter(soap_sold, +1)`, `score(1000)`, `custom: «set_gravity: аромат тепер тягне Glooks у напрямку, яким Боно зайшов на сходи»`.
- КОЛИ `timer(wind)` (C64) → ТО `custom: «вітер міняє напрям аромату»`.
- КОЛИ `contact(bono, door)` → ЯКЩО `has(bono, key)` → ТО `take(key)`, `set_cell(empty)`; інакше `block`.
- КОЛИ `enter(bono, volcano_spot)` → ТО `reveal(volcano)`; КОЛИ `tick` → `spawn_at(glook, near volcano)`.
- КОЛИ `counter(soap_sold, ==, 5)` → ТО `win`, `message(password)`, `next_level`.
- КОЛИ `input(suicide)` → ТО `lives(-1)`, `restart` — вихід із безвихідної позиції.
- Перемога: 5 милин доставлено в камері. Поразка: дотик монстра/павука, Glook у русі, люк; 0 життів → `game_over`.
- Рахунок (C64): цвіль 1 · скелет 10 · ключ 10 · мило зварено 100 · мило продано 1000.

## Керування і ввід
- BBC/Electron: Z/X — ліво/право, `*`/`?` — вгору/вниз; RETURN — дія (з напрямком — без кроку); P — пароль на старті; ESCAPE — самогубство; SHIFT+R — рестарт; COPY/S — пауза, DELETE/Q — зняти.
- C64: джойстик 4 напрямки; fire + короткий рух — прибрати цвіль без кроку; F1 — пароль, F3 — рестарт гри, F5 — убити Боно, якщо застряг.
- Боно, що довго стоїть, колупається в носі — idle-анімація.

## Вікна, меню, HUD
- `main-menu`: старт кнопкою fire / клавішею; P / F1 → `level-password`.
- `game-screen`: камера; статус-рядок — `lives`, `score`, скелети/мило/ключі на руках (`inventory-bar`), енергія Fozzy (`energy-bar`); C64 — `custom` «вітромір»: напрям і відлік до зміни.
- `level-password`: введення пароля камери (22 слова).
- `pause-menu`: пауза з клавіатури.
- `custom-window`: пароль після камери; особливе повідомлення, якщо гру пройдено без паролів.
- `end-screen`: game over → титул; рекорди на C64 не зберігаються.

## Фічі поза полем
- `levels-sequential`: 22 камери; пароль після кожної → `level-password` як чекпоінт.
- `restart-level` і самогубство (−1 життя), `pause`.
- Fozzy — союзник з власним лічильником життів і енергії: гравець має його берегти.

## Варіації й родичі
- Батьки: [Boulder Dash](boulder-dash.md) (копання, штовхання, падіння) і [Repton](repton.md) (BBC-лінія, вид збоку).
- Сиквелів нема (?). Порт на Amiga (1988).
- **Осі варіацій**: напрям «гравітації» — «завжди вниз (BD) / per-type (XOR) / один на камеру, змінюється дією гравця (Bone Cruncher) / перемикачами (Crystal Mines II)»; падаючий обʼєкт — «неживий / живий з метою»; ворог — «лише загроза / ресурс після знешкодження».

## Цікавинки для курсу
- Глобальний напрям гравітації, що змінюється подією гравця, і повторне «осідання» всіх Glooks — 🥉: та сама фізика падіння, але по 4 напрямках і з порядком скану під напрямок.
- Монстр, затиснутий з усіх боків, → скелет — 📎: перевірка «нема вільних сусідів».
- Казан-рецепт (5 скелетів → мило) і ліміт 9 на руках — 🌱.
- Павук і Fozzy — «тримайся лівої / правої стіни» — 📎 кожен, 🥉 з взаємодією «союзник блокує ворога».
- Прихований вулкан-генератор, що відкривається кроком — 📎.

## Мапа на каталог
- Є: `move-4dir` · `dig-terrain` · `push-object` (один Glook) · `gravity-fall` ↔ Glooks у напрямку аромату · `wall-follower` ↔ павук і Fozzy · `touch-death` · `environment-death` (Glook у русі, люк) · `player-death` · `item-pickup` · `inventory-limit` (9 кожного) · `key-and-door` · `spawner-entity` ↔ вулкан · `event-points` · `sequential-levels` · `level-password` · `restart-level` · `game-pause` · `status-panel` + `goal-counter`.
- **Нема** → пропозиції карток:
  - `+shifting-gravity` «Гравітація змінює напрям» · entities/move · 🥉 · слот {by: player-event|timer|switch} — Bone Cruncher, Crystal Mines II.
  - `+trap-to-convert` «Замуруй ворога → ресурс» · entities/interact · 📎 — нема ходу → сутність перетворюється.
  - `+craft-at-station` «Переробка в станції» · entities/state · 🌱 · слот {recipe} — N предметів → один інший.
  - `+ally-guard` «Союзник-охоронець з енергією» · entities/move · 🥉 — блокує ворогів, сам може застрягти.
  - `+snap-action` (з BD) · `+self-destruct` «Самознищення, коли застряг» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:set_gravity(dir)` — змінити напрям падіння для всіх (аромат Bone Cruncher, перемикачі Crystal Mines II).
- `+cond:surrounded(a)` — усі 4 сусіди зайняті (монстр у пастці з Glooks).
- `+axis:gravity-shifting` — значення осі `gravity`: напрям змінюється під час рівня.
- `+ui:wind-meter` — напрям «вітру» і відлік до зміни (C64).
- `+feature:self-destruct` — убити свого героя за −1 життя, коли застряг (ESC/F5).

## Джерела
- ⭐ [8bs: Bonecruncher (Electron)](https://acorn.huininga.nl/pub/mirrors/8bs.com/elecgame/bonecruncher.htm) — інструкція: павук ліворуч / Fozzy праворуч, вхід на сходи задає напрям Glooks, клавіші, ліміт 9, паролі.
- [C64-Wiki: BoneCruncher](https://c64-wiki.com/wiki/BoneCruncher) — 25 скелетів на секцію, вітромір, очки, F1/F3/F5, паролі 22 секцій.
- [Wikipedia](https://en.wikipedia.org/wiki/Bone_Cruncher) — огляд, вид згори, вулкан, платформи.

## Непевне
- (?) Чи Glooks рухаються весь час до упору, чи лише одразу після зміни аромату — джерела кажуть «рухаються до монстра, що купається».
- (?) «Вітер» з таймером — лише C64; у BBC/Electron напрям задає вхід на сходи; як саме поєднано на Amiga — невідомо.
- (?) Скільки життів у Боно на старті; чи є ліміт часу — не знайшов.
- (?) Як вороги-монстри рухаються (погоня / блукання) — не описано; `random: none` поставлено умовно.
- (?) Цвіль — лише в C64-описі; у BBC її нема в інструкції.
