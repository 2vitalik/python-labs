---
title: "Snake Rattle 'n' Roll"
slug: snake-rattle-n-roll
aka: [Snake Rattle n Roll, SRnR]
family: maze-arcade
also: [grid-platformer]
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: coop
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [NES, Mega Drive]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snake_Rattle_%27n%27_Roll", best: true, note: "Rare, 11 ізометричних рівнів, ваги з дзвоником, предмети, кришки-люки, хижі акули у воді"}
  - {kind: other, url: "https://stoneagegamer.com/blog/why-i-love-snake-rattle-n-roll/", note: "види Nibbley Pibbley, вороги, предмети, кришки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=snake+rattle+n+roll+nes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, body-queue, height-levels, gravity-fall, environment-death, item-pickup, spawner-entity, temporary-modes, inventory-duration, hidden-under-block, player-death, time-out, sequential-levels, simultaneous-versus, event-points, +weigh-exit, +tongue-attack, +stomp-attack, +own-color-food-bonus, +zone-stay-punisher, +control-reverse-pickup, +level-warp]
proposes: ["+effect:jump", "+card:weigh-exit", "+card:tongue-attack", "+card:stomp-attack", "+card:own-color-food-bonus", "+card:zone-stay-punisher", "+card:control-reverse-pickup", "+card:level-warp", "+trigger:zone_stay"]
author: opus
date: 2026-11-09
---

# Snake Rattle 'n' Roll — змійка в ізометрії: їж, щоб важити, і стрибни на ваги біля виходу

## Суть
Гравець веде змійку (Rattle; другий гравець — Roll) ізометричним рівнем з уступами, водою й водоспадами. Змійка росте, ковтаючи Nibbley Pibbleys — круглих істот, що бігають, літають і стрибають; язиком вона ловить їжу й бʼє ворогів, а стрибком розчавлює їх. Мета рівня — не очки, а **маса**: досить довгий хвіст починає блимати, змійка стрибає на ваги, дзвоник відкриває двері виходу. Відмінність від `snake`: тут хвіст — це «гаманець», а не пастка; смерть — від висоти, води, таймера й ворогів, а не від власного тіла.

## Поле і час
- Ізометричне 3D-поле з висотами: уступи, плато, ями, вода, водоспади; падіння з великої висоти вбиває.
- NES — 11 рівнів, Mega Drive — 12-й рівень (астероїд).
- Real-time, кожен рівень має таймер; рух не автоматичний (змійка стоїть, коли не тиснеш — на відміну від `snake`) (?).
- Двоє гравців — одночасно на одному полі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Змійка (Rattle / Roll) | player | довжина-сегменти, життя | рух по ізометрії, стрибок, язик; тіло тягнеться за головою |
| Nibbley Pibbley | pickup | колір, вид | їжа; живі: Pib-bal котиться, Pibble-bat літає, Pibble-splat стрибає й лишає калюжі, Pibble-jogger бігає, Pibble-Boing — пружина |
| Жовтий Pibbley | pickup | — | дає найбільший приріст |
| Pibbley свого кольору | pickup | колір = колір змійки | росте швидше, ніж від чужого |
| Диспенсер | spawner | — | випадково викидає Pibbleys, а також бомби |
| Бомба з диспенсера | hazard | — | шкодить змійці |
| Кришка-люк | container | — | відкривається язиком; під нею Pibbleys, предмет, життя, вхід у бонус-рівень або ворог |
| Ваги з дзвоником | switch | поріг маси | стрибок важкої змійки → дзвін → двері відкриті |
| Двері виходу | gate | закриті/відкриті | вихід з рівня після дзвоника |
| Bigfoot | enemy | — | гігантська ступня стрибає й розчавлює |
| Стрибаюча шина | enemy | — | перший ворог; стрибає (?) |
| Сидіння унітаза | enemy | — | клацає кришкою на змійку |
| Jaws (акула) | enemy | — | нападає, якщо змійка задовго у воді |
| Гострі обʼєкти | hazard | — | дотик — мінус життя |
| Падаючі обʼєкти (ковадла) | hazard | — | розчавлення згори — мінус життя |
| Вода | terrain | — | можна плавати, але з таймером акули |
| Водоспад | terrain | — | підйом лише з предметом «риб'ячий хвіст» |
| Предмети | pickup | тривалість | заводна ручка (швидкість), невидимість (діамант), довший язик, +життя, +continue, +час, «риб'ячий хвіст», реверс керування (шкідливий) |
| Прихований варп | static | — | переносить на кілька рівнів уперед |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(snake, dir)`; тіло — `custom: «сегменти повторюють шлях голови»`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок угору/вперед»` (`+effect:jump`).
- КОЛИ `input(tongue)` → ЯКЩО `in_range(snake, pibbley, tongue_len)` → ТО `pickup`, `grow(snake, n)`.
- КОЛИ `picked(snake, pibbley)` → ЯКЩО `same(snake, pibbley, color)` → ТО `grow(snake, more)`; ЯКЩО `custom: «жовтий»` → ТО `grow(snake, max)`.
- КОЛИ `counter(length, >=, quota)` → ТО `set_state(snake, tail_flashing)` — можна виходити.
- КОЛИ `contact(snake, scale)` після стрибка → ЯКЩО `state(snake, tail_flashing)` → ТО `custom: «дзвоник»`, `set_cell(door, open)`.
- КОЛИ `enter(snake, door)` → ЯКЩО `state(door, open)` → ТО `next_level`.
- КОЛИ `contact(snake, enemy)` → ТО `custom: «мінус один сегмент»`; КОЛИ `counter(length, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `contact(snake, enemy)` згори, у стрибку → ТО `disappear_b`, `score(more)`; язиком — `disappear_b`, `score(less)`.
- КОЛИ `contact(snake, spikes)` → ТО `lives(-1)`; КОЛИ `contact(falling_object, snake)` → ТО `lives(-1)`.
- КОЛИ `custom: «падіння з великої висоти»` → ТО `lives(-1)`.
- КОЛИ `custom: «змійка у воді понад N тіків»` (`+trigger:zone_stay`) → ТО `spawn(shark)`; КОЛИ `contact(shark, snake)` → ТО `lives(-1)`.
- КОЛИ `timer(level)` вичерпано → ТО `lives(-1)`.
- КОЛИ `rng(p)` біля диспенсера → ТО `spawn_at(pibbley | bomb, dispenser)`.
- КОЛИ `input(tongue)` → ЯКЩО `cell(here, lid)` → ТО `reveal(lid)`: Pibbleys / предмет / життя / бонус-вхід / ворог.
- КОЛИ `picked(snake, crank)` → ТО `speed(snake, +k)`; `picked(diamond)` → `set_state(snake, invisible, t)`; `picked(tongue_ext)` → `custom: «довший язик»`; `picked(reverse)` → `invert_controls(t)`.
- КОЛИ `picked(snake, fishtail)` → ТО `custom: «може підійматися водоспадами»`.
- КОЛИ `enter(snake, warp)` → ТО `custom: «стрибок на кілька рівнів уперед»`.
- КОЛИ `counter(lives, ==, 0)` → ЯКЩО `has(player, continue)` → ТО `custom: «продовжити з того ж місця»`; інакше `game_over`.
- Перемога: пройти всі рівні · Поразка: життя й continues вичерпано · Рахунок: вороги (стрибком дорожче), їжа (?).

## Керування і ввід
- D-pad: рух у 8 напрямках по ізометрії; одна кнопка — стрибок, друга (B) — язик.
- Двоє гравців одночасно: другий керує Roll.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: 1 або 2 гравці.
- `game-screen`: ізометричне поле; HUD — `lives`, `score`, `timer-countdown`, довжина/маса змійки (?).
- `game-over-continue`: використати continue.
- Бонус-рівні за кришками — окремі поля (`custom-window`) (?).
- Переходи: main-menu → game-screen → (дзвоник і двері) наступний рівень; (життя 0) → game-over-continue / end-screen.

## Фічі поза полем
- `levels-sequential` з прихованими варпами (`skip-level` за знахідку).
- `continue` — кілька продовжень з того самого місця.
- `local-multiplayer` — двоє одночасно (кооп/змагання за їжу (?)).
- Збережень і паролів нема (?).

## Варіації й родичі
- Snake (див. `snake`) — та сама «їж → рости», але там довжина — ризик (власне тіло), а тут — квота для виходу.
- Sneaky Snakes (Game Boy, 1991) — продовження (?).
- Snake Pass (2017) — змійка без сітки з фізикою тіла: обвиватися навколо обʼєктів, хват, стрибків нема; межа корпусу — окремий файл не пишеться.
- Marble Madness, Q*bert (див. `qbert`) — ізометрія з падінням за край.
- **Осі варіацій:**
  - роль довжини: ризик (Snake) / ресурс-ключ (тут) / маса для буста (Slither.io);
  - поле: площина / ізометрія з висотою / вільна 3D-фізика (Snake Pass);
  - як їсти: в'їхати головою / язиком на відстані;
  - смерть: від тіла / від висоти, води, таймера, ворогів.

## Цікавинки для курсу
- Вихід, що відкривається масою (довжина ≥ квоти + стрибок на ваги) — 🌱: квота як двері.
- Сегменти як HP: удар ворога відкушує сегмент, 0 сегментів — смерть — 📎.
- Їжа зі своєю поведінкою (котиться, літає, стрибає, тікає) — 🥉: їжа сама — набір ворогів-втікачів.
- Таймер перебування в зоні (вода → акула) — 📎: лічильник, що скидається при виході.
- Ізометричне поле з висотами й смертю від падіння — 🥈: рендер і порядок малювання.
- Кришки-люки з випадковим вмістом — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `body-queue` · `height-levels` + `gravity-fall` · `environment-death` (вода, падіння, гострі) · `item-pickup` · `spawner-entity` (диспенсер) · `temporary-modes` + `inventory-duration` (невидимість, швидкість) · `hidden-under-block` (кришки) · `player-death` · `time-out` · `sequential-levels` · `simultaneous-versus` (двоє одночасно) · `event-points`.
- **Нема** → пропозиції карток:
  - `+weigh-exit` «Вихід відкривається масою/довжиною» · game-logic/win · 🌱 · слот {quota}.
  - `+tongue-attack` «Язик: удар/збір на відстані» · entities/combat · 📎 · слот {range}.
  - `+stomp-attack` «Стрибок на ворога знищує його» · entities/combat · 📎.
  - `+own-color-food-bonus` «Їжа свого кольору дає більше» · game-logic/score · 🌱.
  - `+zone-stay-punisher` «Задовго в зоні → карач» · game-logic/lose · 📎 · слот {ticks}.
  - `+control-reverse-pickup` «Шкідливий предмет перевертає керування» · entities/state · 🌱.
  - `+level-warp` «Прихований варп через кілька рівнів» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:jump` — стрибок аватара (висота/дальність); у корпусі вже є `jump(height)` у King's Valley — підтверджую.
- `+trigger:zone_stay` — сутність перебуває в зоні/клітині типу N тіків поспіль (вода → акула).
- `+card:weigh-exit`, `+card:tongue-attack`, `+card:stomp-attack`, `+card:own-color-food-bonus`, `+card:zone-stay-punisher`, `+card:control-reverse-pickup`, `+card:level-warp`.

## Джерела
- ⭐ [Wikipedia: Snake Rattle 'n' Roll](https://en.wikipedia.org/wiki/Snake_Rattle_%27n%27_Roll) — Rare 1990, 11 рівнів (+1 на Mega Drive), язик, ріст від свого кольору і жовтих, ваги з дзвоником, блимання хвоста, диспенсери з бомбами, сегменти й життя, акули, таймер, предмети, кришки, варпи, continues.
- [Stone Age Gamer: Why I love Snake Rattle 'n' Roll](https://stoneagegamer.com/blog/why-i-love-snake-rattle-n-roll/) — види Pibbleys, Bigfoot, шина, акула, унітази, ручка-швидкість, риб'ячий хвіст, реверс.
- YouTube: пошук «snake rattle n roll nes gameplay».

## Непевне
- (?) Тривалість таймера, поріг маси, кількість життів і continues — не знайдено.
- (?) Чи змійка стоїть без вводу, чи рухається постійно — з памʼяті.
- (?) Як взаємодіють двоє гравців (спільна їжа, шкода один одному), чи рахуються очки — не знайдено.
- (?) Бонус-рівні за кришками — лише згадка «bonus level entrances», правила не описані.
- (?) Sneaky Snakes як продовження — з назви пошукового результату.
