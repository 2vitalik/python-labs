---
title: Deflektor (+ Mindbender)
slug: deflektor
family: connect-rotate
also: [maze-arcade]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1987
platforms: [ZX Spectrum, C64, Amstrad CPC, Atari ST, Amiga, PC-98, X68000]
links:
  - {kind: wiki, url: "https://www.c64-wiki.com/wiki/Deflektor", best: true, note: "C64-Wiki: усі елементи — клітини, міни, гремліни, поляризатори, призми, оптоволокно, перегрів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Deflektor", note: "історія, Costa Panayi, платформи, сиквел Mindbender"}
  - {kind: official, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-info/d/Deflektor.txt", note: "оригінальна інструкція ZX (клавіші, перегрів, енергія)"}
  - {kind: wiki, url: "https://spectrumcomputing.co.uk/reviews/1327", note: "огляди: курсор, поворот дзеркала, бар'єр перед приймачем"}
  - {kind: play, url: "https://www.artsoft.org/mirrormagic/", note: "Mirror Magic — вільна реінкарнація з рівнями Deflektor/Mindbender і редактором"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Deflektor+C64+gameplay", note: "пошук; геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mindbender+Amiga+gameplay", note: "пошук; сиквел"}
stage: v1
coverage: 65
mechanics: [cell-click, keyboard-controls, collect-all, reach-exit, time-out, player-death, environment-death, sequential-levels, score-records, leaderboard, cheat-codes, game-screen, main-menu, status-panel, +beam-tracing, +mirror-reflect, +tile-rotate, +one-way-cell, +random-deflector, +fiber-link, +overheat-meter, +enemy-tamper, +auto-rotate, +barrier-after-quota, +practice-mode]
proposes: ["+role:source", "+role:sink", "+role:conduit", "+trigger:beam_hit", "+trigger:beam_hit_for(n)", "+effect:rotate", "+effect:reflect", "+effect:emit_beam", "+ui:energy-bar", "+ui:overload-meter", "+feature:mode-practice", "+card:beam-tracing", "+card:mirror-reflect", "+card:overheat-meter", "+card:enemy-tamper"]
author: opus
date: 2026-11-02
---

# Deflektor — повертай дзеркала, щоб лазер спалив усі клітини й дійшов до приймача

## Суть
На одноекранному рівні стоїть лазерна гармата, приймач і десятки дзеркал. Гравець курсором крутить дзеркала, і промінь, відбиваючись, має «спалити» всі клітини-цілі; тоді зникає барʼєр, і промінь треба завести в приймач. Тиснуть дві шкали: енергія лазера постійно тане (це таймер), а перегрів росте, якщо промінь вертається в гармату, лежить на міні чи стає задовгим. Гремліни тим часом самі повертають твої дзеркала. Real-time пазл про трасування променя.

## Поле і час
- Один екран-сітка без скролу; кожна клітина — порожня, стіна або пристрій. Промінь — ламана, що перераховується щокадру від гармати.
- Промінь іде не лише ортогонально: дзеркала мають кілька положень, і кут променя кратний кроку повороту дзеркала (?).
- Real-time: енергія спадає щосекунди; перегрів — шкала, що заповнюється під час «поганого» стану й спадає, коли його виправлено; гремліни зʼявляються періодично.
- 60 рівнів (C64), 3 життя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лазерна гармата | source (custom) | напрям | випускає промінь; промінь назад у неї → перегрів |
| Приймач (receiver) | sink (custom) | закритий барʼєром | промінь у ньому після знищення всіх клітин → рівень пройдено |
| Барʼєр | gate | — | закриває приймач; зникає, коли знищено всі клітини |
| Клітина (cell / node, «кулька») | pickup | — | промінь торкнувся → лопає; треба всі |
| Дзеркало | conduit (custom) | кут (кілька положень) | відбиває за кутом; гравець повертає за/проти годинникової |
| Авто-дзеркало | conduit | швидкість | обертається само |
| Відбивна стіна | static | — | відбиває промінь |
| Поглинальна стіна | static | — | промінь зупиняється |
| Міна | hazard | час до вибуху | промінь задовго на ній → вибух, мінус життя; також перегріває |
| Колючки (spikes) | hazard | — | промінь на них → перегрів (інструкція ZX) |
| Поляризатор | conduit | дозволений кут | пропускає промінь лише під певним кутом/напрямом |
| Призма | conduit | — | відхиляє промінь випадково |
| Оптоволокно | conduit | пара кінців | промінь входить в один кінець і виходить з другого; видно лише кінці |
| Гремлін (phantom) | enemy | період появи | сідає на дзеркало й повертає його; знищується курсором з fire |
| Бонус-предмет | pickup | — | зустрічаються на рівнях (?) |
| Курсор | player | — | рухається по клітинах, фіксує дзеркало, крутить, бʼє гремлінів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `emit_beam(laser)`: `custom: «трасувати промінь від гармати: на дзеркалі reflect(angle), на поляризаторі — пропуск лише під дозволеним кутом, на призмі — випадковий напрям, на оптоволокні — teleport до другого кінця, на поглиначі/барʼєрі — стоп»`.
- КОЛИ `beam_hit(cell)` → ТО `disappear_b`, `score(+n)`, `counter(cells_left, -1)`.
- КОЛИ `counter(cells_left, ==, 0)` → ТО `set_cell(barrier, floor)` — приймач відкрито.
- КОЛИ `beam_hit(receiver)` → ЯКЩО `count(cells, ==, 0)` → ТО `win`, `score(+energy_left)` (?), `next_level`.
- КОЛИ `input(fire+left|right, mirror)` → ТО `rotate(mirror, -step|+step)`.
- КОЛИ `timer(every)` → ТО `rotate(auto_mirror, step)`.
- КОЛИ `beam_hit(laser)` or `beam_hit(spikes)` or `beam_hit(mine)` or `custom: «промінь задовгий»` → ТО `counter(overload, +n)` щотік; інакше `counter(overload, -n)`.
- КОЛИ `counter(overload, >=, max)` → ТО `lives(-1)`, `restart`.
- КОЛИ `beam_hit_for(mine, n)` → ТО `custom: «вибух»`, `lives(-1)`.
- КОЛИ `tick` → ТО `counter(energy, -1)`; КОЛИ `counter(energy, low)` → ТО `flash(beam)` (промінь мерехтить); КОЛИ `counter(energy, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `timer(gremlin_period)` → ТО `spawn_at(gremlin, mirror)`; гремлін `rotate(mirror, rng)`.
- КОЛИ `input(fire, gremlin)` → ТО `disappear_b`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`, `window(leaderboard)`.
- Перемога рівня: усі клітини знищені + промінь у приймачі. Поразка: енергія 0, вибух міни, перегрів до максимуму — мінус життя (3 на гру). Рахунок: очки за клітини й рівні; таблиця рекордів (5 літер).

## Керування і ввід
- Курсор по клітинах: QAKL + M (ZX), джойстик (C64/Amiga).
- Затиснути fire над дзеркалом і натискати вліво/вправо — поворот дзеркала (дзеркало «захоплене», курсор не рухається).
- Fire над гремліном — знищити (найлегше, коли він сидить на дзеркалі).
- Немає прямого керування променем — лише дзеркалами: класичне «непряме» керування.

## Вікна, меню, HUD
- `main-menu`: старт, Practice, вибір керування (джойстик/клавіші).
- `game-screen`: поле; панель — `energy-bar` (таймер), `overload-meter` (графік перегріву), `lives`, `score`, `level-number` (?).
- `end-screen`/перехід: рівень пройдено → наступний; життя втрачено → рестарт рівня.
- `leaderboard` — рекорди з імʼям до 5 літер (зберігаються лише у версії REMEMBER на C64).
- Переходи: main-menu → game-screen (рівень 1 або Practice) → … → game over → leaderboard → main-menu.

## Фічі поза полем
- `mode-practice` — рівень як звичайний, але з набагато більшим запасом часу.
- `levels-sequential` (60 рівнів), без паролів і збережень (оглядачі зберігались знімками емулятора).
- `cheat-codes` (C64 REMEMBER): нескінченні життя, без перегріву, без гремлінів, стартовий рівень — готовий список «вимикачів механік».
- Mindbender (1989) — сиквел: ті самі дзеркала й промінь, нові пристрої та редактор рівнів (?); Mirror Magic (Artsoft) — сучасний порт з рівнями обох ігор, редактором, онлайн-рекордами.

## Варіації й родичі
- Mindbender, Mirror Magic; LaserTank (промінь з танка, але покроково); Khet / Laser Chess (дзеркала-фігури проти суперника); мобільні «laser puzzle».
- Осі варіацій: **хто рухає дзеркала: гравець / самі / вороги** · **час: real-time з енергією / покроково** · **промінь: ортогональний / 8 / 16 напрямків** · **мета: знищити цілі / дійти до приймача / обидва послідовно** · **покарання: перегрів за довжину/петлю / нема**.

## Цікавинки для курсу
- Трасування променя по сітці з дзеркалами (таблиця «напрям × кут дзеркала → новий напрям») і захист від нескінченної петлі — 🥉.
- Пристрої-модифікатори променя: поляризатор (фільтр кута), призма (випадковий напрям), оптоволокно (телепорт променя) — 📎 кожен.
- Шкала перегріву, що росте від «поганого» стану й спадає — 📎; разом з енергією-таймером — дві шкали HUD.
- Гремлін, що псує стан поля (повертає дзеркала), і курсор, що його ловить — 🥉.
- Барʼєр, що зникає після квоти цілей — 🌱 (як розетка Chip's Challenge).
- Нецілі кути променя (16 напрямків) і перетин з клітинами — 🥇 (геометрія, а не BFS).

## Мапа на каталог
- Є: `cell-click`/`keyboard-controls` (курсор) · `collect-all` (усі клітини) · `reach-exit` (приймач) · `time-out` (енергія) · `player-death` (3 життя) · `environment-death` (міна, перегрів) · `sequential-levels` · `score-records` · `leaderboard` · `cheat-codes` · `game-screen` · `main-menu` · `status-panel` · `mode-indicator`.
- **Нема** → пропозиції карток:
  - `+beam-tracing` «Трасування променя по сітці» · entities/combat · 🥉 · слоти {directions: 4|8|16, max_length}.
  - `+mirror-reflect` «Дзеркало з кутом» · entities/interact · 📎 · слот {positions: 2|4|8|16}.
  - `+tile-rotate` «Обертання клітини гравцем» · entities/state · 🌱.
  - `+one-way-cell` «Одностороння клітина (поляризатор)» · entities/legality · 🌱.
  - `+random-deflector` «Випадковий відхилювач (призма)» · entities/interact · 🌱.
  - `+fiber-link` «Парні кінці для променя (оптоволокно)» · entities/interact · 📎 (як `teleport-pair`, але для променя).
  - `+overheat-meter` «Шкала перегріву» · game-logic/lose · 📎 · слоти {fill_rate, cool_rate}.
  - `+enemy-tamper` «Ворог псує стан поля» · entities/move · 🥉.
  - `+auto-rotate` «Само-обертна клітина» · entities/move · 🌱 · слот {period}.
  - `+barrier-after-quota` «Барʼєр зникає після квоти» · game-logic/win · 🌱.
  - `+practice-mode` «Режим тренування з більшим часом» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+role:source` / `+role:sink` — гармата / приймач (спільне з Pipe Mania); `+role:conduit` — дзеркало, поляризатор, призма, оптоволокно.
- `+trigger:beam_hit(a)` — промінь торкнувся сутності; `+trigger:beam_hit_for(a, n)` — промінь тримається на сутності N тіків (міна).
- `+effect:rotate` ⏳ (третя гра сімʼї); `+effect:reflect` — змінити напрям променя за кутом; `+effect:emit_beam` — перерахувати промінь від джерела.
- `+ui:energy-bar` (є як ⏳ `energy-bar` — підтвердження), `+ui:overload-meter` — шкала перегріву.
- `+feature:mode-practice` ⏳ підтверджується.

## Джерела
- ⭐ [C64-Wiki: Deflektor](https://www.c64-wiki.com/wiki/Deflektor) — найповніший перелік елементів: гармата, приймач, дзеркала, клітини, міни, гремліни, поляризатори, призми, оптоволокно, стіни; енергія, перегрів, 60 рівнів, чити.
- [Інструкція ZX Spectrum](https://spectrumcomputing.co.uk/pub/sinclair/games-info/d/Deflektor.txt) — клавіші, енергія, графік перегріву (промінь у гармату, на колючки), авто-дзеркала, фантоми, Practice.
- [Wikipedia](https://en.wikipedia.org/wiki/Deflektor) — Costa Panayi / Vortex / Gremlin, 1987, платформи, сиквел.
- [Spectrum Computing: огляди](https://spectrumcomputing.co.uk/reviews/1327) — курсор, поворот, барʼєр перед приймачем, 3 життя.
- [Mirror Magic](https://www.artsoft.org/mirrormagic/) — грати сьогодні; рівні Deflektor і Mindbender, редактор.
- YouTube: пошук «Deflektor C64 gameplay», «Mindbender Amiga gameplay».

## Непевне
- (?) Кількість положень дзеркала і напрямків променя (огляд ZX каже «45°», за памʼяттю промінь іде і під 22.5°) — перевірити в емуляторі.
- (?) «Промінь задовгий» як причина перегріву — лише C64-Wiki; інструкція ZX називає гармату й колючки.
- (?) Колючки (spikes) і міни — можливо, різні назви одного елемента в різних версіях.
- (?) Бонус-предмети на рівнях — Wikipedia згадує «collectible items» без деталей.
- (?) Mindbender: персонаж-маг, нові пристрої й редактор — з памʼяті; Wikipedia деталей не дає.
- (?) Формула очок (за клітини, залишок енергії) — не знайдено.
