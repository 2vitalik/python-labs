---
title: Wolfenstein 3D
slug: wolfenstein-3d
aka: [Wolf3D, Вольфенштайн 3D]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1992
platforms: [PC (DOS), Mac, SNES, Jaguar, 3DO, GBA, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wolfenstein_3D", best: true, note: "сітка стін і дверей, рейкастинг, предмети, життя, ліфт, бонуси кінця рівня"}
  - {kind: official, url: "https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_DEF.H", note: "вихідний код id: MAPSIZE 64, MAXDOORS 64, типи дверей, тайли ліфта/pushwall/ambush"}
  - {kind: official, url: "https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_ACT1.C", note: "код: двері (замки, автозакриття, зони) і pushwall"}
  - {kind: official, url: "https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_AGENT.C", note: "код: предмети, очки, кнопка Use, ліфт"}
  - {kind: other, url: "https://lodev.org/cgtutor/raycasting.html", note: "туторіал: рейкаст по сітці DDA, перпендикулярна відстань, тінь сторін"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wolfenstein+3d+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, orientation-state, impassable-cells, key-and-door, hp-damage, item-pickup, inventory, projectile-shot, line-of-sight-attack, melee-vs-ranged, chase-player, enemy-patrol, reach-exit, sequential-levels, event-points, extra-life-threshold, player-death, difficulty-levels, save-game, end-screen, status-panel, gui-render, player-camera, time-bonus, +grid-raycast, +sliding-door, +auto-close-door, +secret-pushwall, +use-key-front-tile, +sound-areas, +ambush-flag, +blocking-decor, +level-ratios, +par-time, +secret-exit, +restart-with-pistol]
proposes: ["+trigger:use(tile)", "+trigger:noise(area)", "+cond:connected(area_a, area_b)", "+effect:open_door", "+effect:push_wall(dir, n)", "+effect:alert(a)", "+ui:face-health", "+window:level-stats", "+window:episode-select", "+axis:view=first-person"]
author: opus
date: 2026-11-09
---

# Wolfenstein 3D — клітинна мапа 64×64, яку рейкаст показує «від першої особи»: двері-слайди, таємні стіни-штовханці й ліфт на виході

## Суть
Гравець (B.J. Blazkowicz) іде поверхом-бункером, стріляє в охорону й шукає ліфт на наступний поверх. Під 3D-виглядом лежить **плоска сітка тайлів**: кожна клітина — або стіна однакової висоти, або двері, або підлога з предметами. Рендер — **рейкаст по сітці**: на кожен стовпчик екрана один промінь іде клітинами (DDA) до першої стіни. Цей файл описує саме клітинний шар; бій і предмети — коротко.

## Поле і час
- Мапа до **64×64** тайлів (`MAPSIZE 64`), два шари: стіни/двері/зони підлоги і шар обʼєктів (старт гравця, вороги, предмети, маркери pushwall).
- Стіна = повна клітина з текстурою; висота стін однакова, сходів і поверхів у межах рівня нема.
- Двері стоять **у клітині** посередині й відʼїжджають убік; до 64 дверей на мапу. Тайли підлоги мають **номер зони** (`AREATILE 107` + 37 зон): двері зʼєднують зони.
- Рух гравця і ворогів — неперервний (координати з дробовою частиною, `TILEGLOBAL = 1<<16`), повороти плавні; сітка обмежує лише колізії й рендер. Тому `field: square` — за мапою, а не за кроком.
- Real-time; видно лише те, що в полі зору (`info: hidden`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | здоровʼя 0–100 %, патрони ≤ 99, життя ≤ 9, ключі | рух/поворот, стрільба, кнопка Use на клітину попереду |
| Стіна | static | текстура | непрохідна, зупиняє промінь |
| Pushwall (таємна стіна) | object | маркер у шарі обʼєктів | по Use зсувається вглиб, відкриваючи схованку |
| Двері звичайні | gate | стан open/opening/closing/closed | відкриваються Use, самі зачиняються через час |
| Двері замкнені (lock1–lock4) | gate | потрібний ключ | без ключа — звук «не можна» |
| Двері ліфта | gate | — | ведуть у кабіну ліфта |
| Перемикач ліфта | switch | `ELEVATORTILE 21` | Use збоку (схід/захід) → кінець рівня; альтернативна клітина → таємний рівень |
| Ключ (золотий, срібний) | pickup | — | відкриває замкнені двері свого типу |
| Скарб (хрест, чаша, біблія, корона) | pickup | 100 / 500 / 1000 / 5000 очок | +очки, +1 до лічильника скарбів |
| Аптечка / їжа / собача їжа | pickup | +25 / +10 / +4 HP | не береться при 100 % |
| Кров (gibs) | pickup | +1 HP | лише при HP ≤ 10 |
| Обойма / підібрана обойма | pickup | +8 / +4 патрони | не береться при 99 |
| Кулемет, кулемет Гатлінга | pickup | зброя | відкриває кращу зброю |
| One-up (синя сфера) | pickup | +99 HP, +25 патронів, +1 життя | рахується як скарб |
| Декор блокуючий (бочка, стіл, колона, лампа…) | static | `block` | займає клітину, не проходиться |
| Декор прохідний (калюжа, люстра, кістки) | static | — | лише картинка |
| Охоронець, офіцер, SS, пес, мутант | enemy | HP, зброя | патруль або стоїть; чує постріли, бачить гравця, біжить і стріляє (пес кусає) |
| Ворог у засідці (ambush) | enemy | `AMBUSHTILE 106` | не реагує на звук, лише на погляд (?) |
| Бос | boss | — | кінець епізоду (робот-костюм з чотирма кулеметами та ін.) |

## Правила (КОЛИ → ЯКЩО → ТО)
Клітинний шар:
- КОЛИ `input(move)` → ЯКЩО `free(cell)` → ТО `move(player, to)`; стіна, закриті двері, блокуючий декор → `block`.
- КОЛИ `input(use)` → ЯКЩО `cell(front, door)` `and not has(player, key)` для замкнених → ТО `sound(«no way»)`; інакше `custom: «двері відʼїжджають / зачиняються»` (`+effect:open_door`).
- КОЛИ `timer(300 tics)` (двері відчинені) → ЯКЩО `not occupied(door_cell, any)` → ТО `custom: «двері зачиняються»`; якщо щось зайшло під час закривання → двері знову відчиняються.
- КОЛИ `custom: «двері почали відчинятись»` → ТО `custom: «зони по обидва боки зʼєднані»` (`+cond:connected`); КОЛИ двері повністю зачинились → `custom: «зʼєднання знято»`.
- КОЛИ `input(use)` → ЯКЩО `cell(front, pushwall)` `and free(cell_behind)` `and not state(pushwall, moving)` → ТО `custom: «стіна повзе від гравця на 2 клітини»` (`+effect:push_wall`), `counter(secrets, +1)`, `sound(pushwall)`; зайнято → `sound(«no way»)`. Одночасно рухається лише одна.
- КОЛИ `input(use)` → ЯКЩО `cell(front, elevator_switch)` `and facing(player, east|west)` → ТО `next_level`; ЯКЩО `cell(under_player, alt_elevator)` → ТО `custom: «таємний рівень»`.
- Рендер: КОЛИ `tick` → ТО `custom: «для кожного стовпчика екрана промінь іде клітинами (DDA) до першої стіни; висота стовпчика ∝ 1 / перпендикулярна відстань»`.

Бій і предмети:
- КОЛИ `contact(player, pickup)` → ЯКЩО `not custom: «показник на максимумі»` → ТО `pickup`, `score(n)` / `heal(player, n)` / `counter(ammo, +n)`.
- КОЛИ `input(fire)` → ЯКЩО `has(player, ammo)` → ТО `custom: «hitscan-постріл обраною зброєю»`, `counter(ammo, -1)`; без патронів — лише ніж.
- КОЛИ `custom: «постріл гравця»` → ТО `custom: «вороги в зʼєднаних зонах чують і прокидаються»` (`+trigger:noise`, `+effect:alert`).
- КОЛИ `line_of_sight(enemy, player)` → ТО `custom: «ворог помічає, біжить і стріляє»`.
- КОЛИ `custom: «влучання ворога»` → ТО `damage(n)`; ЯКЩО `difficulty(baby)` → шкода ÷ 4.
- КОЛИ `hp_zero(player)` → ТО `lives(-1)`, `restart` (рівень заново з ножем, пістолетом і 8 патронами).
- КОЛИ `counter(score, >=, next_extra)` → ТО `lives(+1)`.
- КОЛИ `level_end` → ТО `window(level-stats)`: % вбитих, % таємниць, % скарбів, час проти par; бонус за 100 % і за час.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: дійти до ліфта (останній рівень епізоду — вбити боса). Поразка: життя скінчились. Рахунок: вороги, скарби, бонуси кінця рівня.

## Керування і ввід
- Стрілки — вперед/назад, поворот; Alt + стрілка — крок убік (strafe) (?); Shift — біг (?).
- Ctrl — вогонь; пробіл — Use (двері, pushwall, перемикач ліфта) на клітину попереду (?).
- 1–4 — вибір зброї з наявних (ніж, пістолет, кулемет, Гатлінг).
- Підтримка миші й джойстика (?).

## Вікна, меню, HUD
- `main-menu`: New Game → `episode-select` (6 епізодів) → `difficulty-select` (4 рівні); Sound; Control; Load Game; Save Game; Change View; Read This!; View Scores; Back to Demo; Quit (?).
- `game-screen` — 3D-вид + статус-панель: `level-number` (Floor), `score`, `lives`, обличчя B.J. (стан здоровʼя), `hp-bar` (%), ammo, ключі, картинка зброї.
- `custom-window` — статистика рівня (`+window:level-stats`): ratios, час, par, бонуси.
- `leaderboard` — View Scores; `save-slots` — Load/Save; `attract-demo` — Back to Demo.
- `end-screen` — кінець епізоду: трилітерний код з рахунком і часом (для скасованого конкурсу).
- Переходи: меню → епізод → складність → поверх → (ліфт) статистика → наступний поверх → … → бос → кінець епізоду.

## Фічі поза полем
- `difficulty-presets` — 4 складності (`gd_baby`…`gd_hard`): шкода гравцю й набір ворогів (?).
- `save-slots` — збереження будь-де (у DOS); у багатьох портах — лише між рівнями.
- `levels-sequential` — 6 епізодів × 10 поверхів, останній — бос; таємний рівень через альтернативний ліфт.
- `collectibles` — таємниці й скарби з відсотком на екрані статистики.
- Код рекорду в кінці епізоду; Change View — розмір вʼюпорта.

## Варіації й родичі
- [3D Monster Maze](3d-monster-maze.md) — теж лабіринт від першої особи, але **крок на клітину й поворот на 90°**, без дверей і стрільби; Wolf3D рухається неперервно, сітка лишається тільки під стінами.
- [Maze War](maze-war.md) — лабіринт-сітка від першої особи з дискретними кроками й поворотами, мультиплеєр; у Wolf3D — AI-вороги, двері й таємниці.
- Spear of Destiny (1992) і місії — той самий рушій; DOOM (1993) — висоти й непрямі стіни, вже не сітка.
- Catacomb 3-D (1991) — попередник id на схожому рушії.
- **Осі варіацій:** крок (клітина / неперервний); двері (нема / слайд у клітині / замкнені ключем); таємниці (нема / pushwall / фальшиві стіни); вихід (клітина / перемикач з орієнтацією).

## Цікавинки для курсу
- Рейкаст по сітці DDA: 2D-мапа → псевдо-3D, перпендикулярна відстань проти «риб'ячого ока» — 🥈 (математика й рендер, але класичний туторіал).
- Двері в клітині зі станами open/opening/closing/closed і автозакриттям, що не зачиняє на гравцеві — 📎.
- Pushwall: одна стіна за раз, перевірка вільної клітини позаду, лічильник таємниць — 🌱.
- Зони підлоги, зʼєднані відчиненими дверима, — звук іде лише по зʼєднаних зонах — 🥉 (union/flood по графу зон).
- Use на клітину попереду: одна кнопка, поведінка за типом тайла — 🌱.
- Статистика рівня: % вбитих / таємниць / скарбів і par-час — 🌱.
- Мапа з двох шарів (стіни + обʼєкти) у txt/масиві 64×64 — 📎.

## Мапа на каталог
- Є: `move-by-input` · `orientation-state` · `impassable-cells` · `key-and-door` · `hp-damage` · `item-pickup` · `inventory` · `projectile-shot` (умовно, постріли hitscan) · `line-of-sight-attack` · `melee-vs-ranged` (ніж/пес) · `chase-player` · `enemy-patrol` · `reach-exit` · `sequential-levels` · `event-points` · `extra-life-threshold` · `player-death` · `difficulty-levels` · `save-game` · `end-screen` · `status-panel` · `gui-render` · `player-camera` · `time-bonus` (par).
- **Нема** → пропозиції карток:
  - `+grid-raycast` «Псевдо-3D рейкаст по сітці (DDA)» · interface/render · 🥈 · слоти {fov, textures}.
  - `+sliding-door` «Двері в клітині, що відʼїжджають» · entities/state · 📎.
  - `+auto-close-door` «Автозакриття дверей, якщо проріз вільний» · entities/state · 🌱 · слот {ticks}.
  - `+secret-pushwall` «Таємна стіна, що зсувається на N клітин» · entities/interaction · 🌱 · слот {n}.
  - `+use-key-front-tile` «Кнопка Use діє на клітину попереду» · interface/input · 🌱.
  - `+sound-areas` «Зони, зʼєднані відчиненими дверима, для звуку» · entities/ai · 🥉.
  - `+ambush-flag` «Ворог реагує лише на погляд» · entities/ai · 🌱.
  - `+blocking-decor` «Декор займає клітину / не займає» · entities/collision · 🌱.
  - `+level-ratios` «% вбитих / таємниць / скарбів наприкінці» · game-logic/score · 🌱.
  - `+par-time` «Еталонний час рівня з бонусом» · game-logic/score · 🌱.
  - `+secret-exit` «Альтернативний вихід на таємний рівень» · levels/progression · 🌱.
  - `+restart-with-pistol` «Смерть → рівень заново з базовим спорядженням» · game-logic/death · 🌱.

## Пропозиції до словників
- `+trigger:use(tile)` — гравець натиснув Use на клітину попереду (Wolf3D, DOOM, Grimrock-кнопки).
- `+trigger:noise(area)` — у зоні пролунав шум (постріл); `+effect:alert(a)` — ворог переходить у бойовий режим.
- `+cond:connected(area_a, area_b)` — зони зʼєднані відчиненими дверима (вужче за ⏳ `connected` множини — може лягти в нього).
- `+effect:open_door` — відчинити двері зі станом (open/closing); `+effect:push_wall(dir, n)` — зсунути стіну-таємницю.
- `+ui:face-health` — портрет героя, що показує здоровʼя (Wolf3D, DOOM).
- `+window:level-stats` — екран статистики рівня (ratios, час, par); `+window:episode-select` — вибір епізоду.
- `+axis:view=first-person` — уже пропоновано в DM / 3D Monster Maze; тут підтвердження.

## Джерела
- ⭐ [Wikipedia: Wolfenstein 3D](https://en.wikipedia.org/wiki/Wolfenstein_3D) — сітка стін і дверей рівної висоти, рейкастинг, спрайти з 8 кутів, зброя, предмети, 4 життя на епізод, рестарт з ножем/пістолетом/8 патронами, ліфт, бонуси кінця рівня, 6 епізодів × 10 рівнів, збереження.
- [id Software, WL_DEF.H](https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_DEF.H) — `MAPSIZE 64`, `MAXDOORS 64`, `MAXACTORS 150`, `MAXSTATS 400`, типи дверей `dr_normal/dr_lock1–4/dr_elevator`, `PUSHABLETILE 98`, `ELEVATORTILE 21`, `AMBUSHTILE 106`, `AREATILE 107`/37 зон, 4 складності.
- [id Software, WL_ACT1.C](https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_ACT1.C) — PushWall (одна за раз, вільна клітина позаду, лічильник таємниць), двері (замок за бітом ключа, `OPENTICS 300`, не зачиняються на сутності), зʼєднання зон, блокуючий декор.
- [id Software, WL_AGENT.C](https://raw.githubusercontent.com/id-Software/wolf3d/master/WOLFSRC/WL_AGENT.C) — значення предметів, ліміти 100/99/9, Use і ліфт (лише зі сходу/заходу), альтернативний ліфт, шкода ÷ 4 на baby.
- [Lode's raycasting tutorial](https://lodev.org/cgtutor/raycasting.html) — DDA по сітці, перпендикулярна відстань, тінь y-сторін; обмеження рушія Wolf3D.
- YouTube: пошук «wolfenstein 3d gameplay».

## Непевне
- (?) Pushwall: коментар у коді каже «два тайли», а арифметика `pwallstate > 256` з кроком 128 може давати три; у файлі — 2.
- (?) Ambush: «реагує лише на погляд» — з памʼяті; у коді видно лише константу тайла.
- (?) Розкладка клавіш і пункти головного меню — з памʼяті.
- (?) Поріг додаткового життя (`EXTRAPOINTS` у відкритому фрагменті не визначено; з памʼяті 40 000).
- (?) `OPENTICS 300`: коментар — «3 секунди», реальний час залежить від частоти тіків (70 Гц → ~4 с).
- (?) Що змінює складність, крім шкоди на baby (кількість ворогів на мапі — з памʼяті).
- (?) Чи зʼєднання зон впливає і на «бачення» ворогів — коментар у коді каже так, у відкритому файлі не видно.
