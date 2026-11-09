---
title: Crystal Castles
slug: crystal-castles
aka: [Кришталеві замки, Bentley Bear]
family: maze-arcade
also: []
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: collect
year: 1983
platforms: [arcade, Atari 2600, Atari 8-bit, Atari ST, ZX Spectrum, C64]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crystal_Castles_(video_game)", best: true, note: "Bentley Bear, трекбол + стрибок, вороги, капелюх, мед, варпи, фінал"}
  - {kind: other, url: "https://www.arcade-history.com/game/549/", note: "очки (500/1000/2000), бонус останнього самоцвіта, бонус часу, три варпи, 10 рівнів / 37 замків, фінальні титули"}
  - {kind: other, url: "https://arcade-museum.com/Videogame/crystal-castles", note: "KLOV: трекбол, Jump, рівень кінчається, коли самоцвіти зникли; лінки на операторський мануал"}
  - {kind: other, url: "https://www.arcade-museum.com/manuals-videogames/C/crystalsp.pdf", note: "операторський мануал (PDF, 47 с.) — побачений на KLOV, не відкривав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crystal+castles+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 60
mechanics: [collect-all, item-pickup, touch-death, player-death, chase-bfs, random-walk, temporary-modes, carrier-platform, event-points, time-bonus, extra-life-threshold, sequential-levels, score-records, attract-demo, +isometric-maze, +jump-stun-enemy, +rival-collector, +vulnerable-while-eating, +hidden-passages, +secret-warp, +guard-swarm, +last-item-bonus, +ending-rank, +trackball-input]
proposes: ["+trigger:jump_over", "+effect:warp_level", "+cond:eating", "+role:rival", "+feature:trackball", "+feature:secret-warp", "+window:ending-rank"]
author: opus
date: 2026-11-09
---

# Crystal Castles — ведмідь Бентлі трекболом збирає самоцвіти ізометричних замків раніше за ворогів-їдців, стрибаючи через дерева і ховаючись у тунелях

## Суть
Pac-Man у тривимірному замку: Бентлі Беар бігає доріжками ізометричного (тримерного) замку, збираючи самоцвіти, і замок пройдено, коли самоцвітів не лишилось — хоч зібрав їх він, хоч вороги. Gem Eaters теж їдять самоцвіти і вразливі лише під час їжі; дерева шукають найкоротший шлях до Бентлі й глушаться стрибком через них. Ліфти, сходи, рампи й тунелі за стінами дають кілька висот, а капелюх відьми — тимчасову невразливість. Одна з небагатьох аркад зі справжнім фіналом.

## Поле і час
- Замок — ізометричний лабіринт з доріжок на кількох висотах (`field: iso`); сходи, рампи, ліфти й тунелі сполучають рівні; частина проходів і рамп схована за стінами (`info: partial`).
- Рух вздовж доріжок (4 напрямки на ізосітці (?)) + стрибок на місці; падіння з краю немає (?).
- Real-time. Рівень = 4 замки (хвилі); 4-й — з відьмою Бертільдою. Аркада: 10 рівнів / 37 замків (останній рівень — 1 замок); Wikipedia — «16 полів, по 4 хвилі».
- Наприкінці 10-го рівня — фінальний екран з титулом за кількістю життів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бентлі Беар | player | життя | біг доріжками, стрибок; збирає самоцвіти |
| Самоцвіт | pickup | — | очки; рівень кінчається, коли всі зникли |
| Gem Eater | enemy | їсть / не їсть | повзе до самоцвітів і зʼїдає їх; під час їжі вразливий (500 / 1000), інакше дотик — смерть |
| Злюще дерево (Nasty Tree) | enemy | — | шукає найкоротший шлях до Бентлі; стрибок через нього — дерево зменшується й тимчасово вимкнене |
| Кришталева куля | enemy | — | котиться доріжками; уникати |
| Скелет · привид | enemy | — | уникати; частина ворогів рухається випадково, частина женеться |
| Рій бджіл | enemy | ≈ кожні 5 с | вилітає охороняти горщик меду |
| Горщик меду | pickup | 1000 | очки; після нього бджоли рідшають |
| Чарівний капелюх | pickup | 2000, тимчасовий | невразливість + можна вбити Бертільду |
| Бертільда (відьма) | boss | — | у 4-му замку рівня; вбити лише в капелюсі |
| Ліфт | terrain | — | схожий на драбину з лінією, що бігає вгору-вниз; везе між висотами |
| Тунель / схований прохід | terrain | за стіною | Бентлі проходить крізь стіну, скорочуючи шлях |
| Сходи · рампа | terrain | — | перехід між висотами; деякі рампи сховані |
| Точка варпу | zone | секретна | стрибок тут → перенос на вищий рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(path_ahead)` → ТО `move(bentley, dir)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок на місці / вперед — проскакує над ворогом»`.
- КОЛИ `contact(bentley, gem)` → ТО `pickup`, `score(gem_value)`.
- КОЛИ `contact(gem_eater, gem)` → ТО `disappear_b`, `set_state(gem_eater, eating, short)`.
- КОЛИ `contact(bentley, gem_eater)` → ЯКЩО `state(gem_eater, eating)` → ТО `disappear_b`, `score(500|1000)`; інакше `lose`.
- КОЛИ `custom: «Бентлі перестрибнув через дерево»` (`+trigger:jump_over`) → ТО `shrink(tree)`, `stun(tree, n)`.
- КОЛИ `tick` → ТО дерево: `custom: «крок найкоротшим шляхом до Бентлі»` (`chase-bfs`); інші вороги — `chase-player` або `move(a, rng_dir)`.
- КОЛИ `contact(bentley, enemy)` → ЯКЩО `not state(bentley, hat)` → ТО `lose`.
- КОЛИ `contact(bentley, hat)` → ТО `pickup`, `score(2000)`, `set_state(bentley, hat, duration)`.
- КОЛИ `contact(bentley, enemy)` → ЯКЩО `state(bentley, hat)` → ТО `disappear_b`, `score(n)` (Бертільда — бонус).
- КОЛИ `contact(bentley, honey_pot)` → ТО `pickup`, `score(1000)`, `custom: «бджоли зʼявляються рідше»`.
- КОЛИ `timer(≈5s)` → ЯКЩО `occupied(maze, honey_pot)` → ТО `spawn_at(bee_swarm, honey_pot)`.
- КОЛИ `enter(bentley, elevator)` → ТО `carry` — ліфт піднімає/опускає Бентлі на іншу висоту.
- КОЛИ `enter(bentley, tunnel)` → ТО `hide(bentley)` (за стіною) і вихід з іншого боку.
- КОЛИ `all_gone(gem)` → ЯКЩО `custom: «останній самоцвіт узяв Бентлі»` → ТО `score(1000 + ((level×4 − 1) − (4 − board)) × 100)`; `next_level` (наступний замок).
- КОЛИ `input(jump)` → ЯКЩО `occupied(warp_spot, bentley)` → ТО `custom: «перенос на наступний непарний рівень»` (`+effect:warp_level`), іноді з життями.
- КОЛИ `timer(4s)` → ТО `counter(time_bonus, −1000)` від 200 000; КОЛИ `died(bentley)` → ТО `counter(time_bonus, −1000)` щонайменше.
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)` (?).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- КОЛИ `level_end` → ЯКЩО `level(op, ==, 10)` → ТО `win`, `message(«YOU WIN YOU MUST BE» + титул за життями)`, `score(time_bonus)`.
- Перемога: пройти 10-й рівень. Поразка: скінчились життя. Рахунок: самоцвіти, вороги, мед, капелюх, бонус останнього самоцвіта, бонус часу.

## Керування і ввід
- Трекбол — рух (швидкість обертання = швидкість бігу (?)); одна кнопка Jump.
- Стрибок на секретних точках — варп; стрибок через дерево — оглушення.
- 2 гравці по черзі; панель симетрична для лівші й правші.

## Вікна, меню, HUD
- `attract-demo` — демо-замок.
- `game-screen` — замок; `score` (P1/P2), `hi-score`, `lives`, номер рівня / хвилі (?).
- Початок рівня — екран з номером рівня і, на першому, вибором старту з вищого рівня (?).
- `end-screen` фіналу — «I GIVE UP : YOU WIN YOU MUST BE …» з титулом: 1 життя — AMAZINGLY GOOD … 6 — A VIDEO WIZ; далі бонус часу і анімація прямокутників.
- `leaderboard` — рекорди з ініціалами (?).
- Переходи: атракт → (монета) → замок 1 → … → 4-й замок рівня (відьма) → наступний рівень → … → фінал / GAME OVER.

## Фічі поза полем
- `secret-warp` — три сховані варпи: стрибок у певному місці переносить на рівень 3 / 5 / 7 (з чотирма життями); «чит» відомий як пасхалка.
- `levels-sequential` + справжній кінець гри з `ending-rank` (титул за життями).
- `operator-settings` — 5 DIP-налаштувань (зміст не бачив).
- `hotseat` 2 гравці по черзі.

## Варіації й родичі
- Порти: Atari 2600 (спрощений), Atari 8-bit, ST, ZX Spectrum, C64 тощо — з джойстиком замість трекбола.
- Родичі в корпусі: Pac-Man (збір усього, вороги-переслідувачі), Q*bert (ізометрична сітка), Amidar, Lady Bug, Centipede (той самий трекбол Atari), Marble Madness (ізометрія + трекбол).
- **Осі варіацій:** суперник-збирач (нема / їсть твої цілі й кінчає рівень) · вразливість ворога (ніколи / лише під час дії / під бонусом) · висоти поля (одна / кілька зі ліфтами й тунелями) · видимість (уся / частина за стінами) · кінець (нескінченно / фінал з рангом).

## Цікавинки для курсу
- Ізометричний рендер клітинного лабіринту з кількома висотами — 🥈 (порядок малювання + переходи між висотами).
- Ворог-конкурент, що збирає ті самі самоцвіти, і рівень кінчається будь-як — 📎.
- Вразливість ворога лише в стані «їсть» — 🌱.
- Дерево з BFS-погонею, оглушене стрибком через нього — 🥉 (BFS по ізографу + стан).
- Тунелі за стінами: гравця не видно — 📎 (сортування глибини + прихований рух).
- Секретні варпи стрибком у точці — 🌱.
- Фінал з титулом за кількістю життів + бонус часу, що тане — 🌱.

## Мапа на каталог
- Є: `collect-all` · `item-pickup` · `touch-death` · `player-death` · `chase-bfs` (дерева) · `random-walk` · `temporary-modes` (капелюх) · `carrier-platform` (ліфт) · `event-points` · `time-bonus` · `extra-life-threshold` (?) · `sequential-levels` · `score-records` · `attract-demo`.
- **Нема** → пропозиції карток:
  - `+isometric-maze` «Лабіринт в ізометрії з висотами» · interface/render · 🥈.
  - `+jump-stun-enemy` «Перестрибнути ворога — оглушити» · entities/combat · 📎.
  - `+rival-collector` «Ворог збирає ті самі цілі» · entities/interact · 📎 — Gem Eaters.
  - `+vulnerable-while-eating` «Ворог вразливий лише в стані дії» · entities/state · 🌱.
  - `+hidden-passages` «Проходи й рампи за стінами» · entities/legality · 📎.
  - `+secret-warp` «Сховані точки перескоку рівнів» · levels/progression · 🌱.
  - `+guard-swarm` «Рій охороняє бонус, спавн за таймером» · entities/spawn · 📎.
  - `+last-item-bonus` «Бонус за останній предмет рівня» · game-logic/score · 🌱.
  - `+ending-rank` «Фінальний титул за результатом» · interface/menus · 🌱.
  - `+trackball-input` «Трекбол як ввід руху» · interface/input · 📎.

## Пропозиції до словників
- `+trigger:jump_over` — аватар перестрибнув сутність (Crystal Castles, Frogger-подібні).
- `+effect:warp_level` — перескочити на рівень N.
- `+cond:eating` — ворог у фазі дії, коли вразливий (окремий від загального `state` для читабельності; куратору вирішити).
- `+role:rival` — ворог-конкурент за ресурс, не лише мисливець.
- `+feature:trackball`, `+feature:secret-warp` — трекбол і сховані варпи.
- `+window:ending-rank` — фінальний екран з титулом.

## Джерела
- ⭐ [Wikipedia: Crystal Castles](https://en.wikipedia.org/wiki/Crystal_Castles_(video_game)) — Бентлі, трекбол і стрибок, тримерна проєкція, Gem Eaters вразливі під час їжі, дерева шукають найкоротший шлях і глушаться стрибком, Бертільда в 4-й хвилі, капелюх, мед, варпи, фінальне повідомлення.
- [arcade-history: Crystal Castles](https://www.arcade-history.com/game/549/) — 500/1000 за Gem Eater, мед 1000, капелюх 2000, формула останнього самоцвіта, бонус часу 200 000 − 1000/4 с, три варпи, 10 рівнів / 37 замків, титули фіналу, бджоли ≈ 5 с.
- [KLOV: Crystal Castles](https://arcade-museum.com/Videogame/crystal-castles) — трекбол, рівень кінчається, хоч хто забрав самоцвіти, кулі/скелети/привиди, лінки на мануали.
- YouTube: пошук «crystal castles arcade gameplay».

## Непевне
- (?) Структура рівнів: Wikipedia «16 полів × 4 хвилі» проти arcade-history «10 рівнів, 37 замків».
- (?) Старт 5 життів і бонусне життя кожні 20 000 — з пошукового фрагмента.
- (?) Рівні 9+: капелюх перетворюється на кришталеву кулю, якщо до нього не встигнути — з пошукового фрагмента (StrategyWiki, 403).
- (?) Очки за самоцвіт; поведінка кришталевих куль, скелетів, привидів; чи кулі теж збирають самоцвіти.
- (?) Чи можна впасти з краю доріжки; як саме трекбол перекладається на ізонапрямки.
