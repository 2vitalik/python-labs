---
title: Dr. Mario (Доктор Маріо)
slug: dr-mario
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: collect
year: 1990
platforms: [NES, Game Boy, arcade (VS. System), SNES, N64, Wii, Wii U, 3DS, mobile]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Dr._Mario_(game)", best: true, note: "Super Mario Wiki — пляшка 8×16, віруси за рівнем, швидкості, таблиця очок, versus, музика"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dr._Mario", note: "правила коротко, версії й сиквели"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dr+mario+nes+gameplay", note: "пошук; геймплей NES"}
stage: v1
coverage: 75
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, collect-all, destroy-all-enemies, sequential-levels, difficulty-levels, progress-acceleration, event-points, combo-multiplier, score-records, game-pause, background-music, music-toggle, end-screen, +line-match-clear, +chain-reaction, +split-on-clear, +next-queue, +garbage-attack, +virus-board-generation]
proposes: ["+trigger:locked", "+trigger:settled", "+effect:split", "+effect:send_garbage", "+window:difficulty-select", "+ui:virus-counter", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# Dr. Mario — кидай двоколірні капсули, щоб 4 в ряд знищили віруси свого кольору

## Суть
У пляшці 8×16 розкидано віруси трьох кольорів; гравець керує падаючою капсулою з двох половинок (кожна свого кольору). Лінія з 4+ однакових кольорів (половинки й віруси) по горизонталі чи вертикалі зникає; половинки без опори падають і можуть утворити нові лінії. Мета рівня — знищити всі віруси, поразка — забити горлечко пляшки. На відміну від Tetris/Puyo, поле має **заздалегідь задану ціль** (віруси), і зникнення розриває капсулу на незалежні половинки.

## Поле і час
- Пляшка 8 стовпців × 16 рядів, вузьке горлечко зверху по центру (спавн капсули). Game Boy-версія — менше поле.
- Real-time: капсула падає з темпом швидкості (Low/Med/Hi), швидкість зростає після певної кількості кинутих капсул (сигнал — пʼятинотний дзвоник).
- Шари: віруси (нерухомі, частина стартового стану) + осілі половинки (кожна памʼятає, чи вона ще зʼєднана з парою) + активна капсула. Після зникнення — фаза каскаду, як у Puyo.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Капсула (мегавітамін) | player | 2 половинки, кольори з {R, Y, B}, горизонт./вертик. | зсув, поворот на 90° в обидва боки, прискорене падіння; приземлення → фіксується як дві зʼєднані половинки |
| Половинка капсули (зʼєднана) | tile | колір, звʼязок з парою | падає разом з парою, лише якщо пара не має опори |
| Половинка (одинока) | tile | колір | після зникнення пари падає окремо, доки є порожнеча під нею |
| Вірус (Fever/червоний, Weird/жовтий, Chill/синій) | tile | колір | нерухомий, не падає; зникає в лінії ≥4 свого кольору; лічильник рівня |
| Сміттєва половинка (versus) | hazard | колір як у рядів, що їх зчистив суперник | падає згори в певні стовпці, поводиться як одинока половинка |
| Горлечко | static | 2 центральні клітини верху | зайняте осілими → поразка |
| Next-капсула | spawner | 1 | Маріо тримає й кидає наступну |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(virus, random_cells)` к-сть `4 × level + 4` (рівень 0 → 4, рівень 20 → 84; далі 84), кольори випадкові; верхні ряди лишаються вільними.
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(capsule, down)` з темпом швидкості; інакше `custom: «lock — капсула стає двома зʼєднаними половинками»`.
- КОЛИ `input(shift)` → ЯКЩО `free(target)` → ТО `move(capsule, dir)`; КОЛИ `input(rotate_a|rotate_b)` → ЯКЩО `free(new_cells)` → ТО `rotate(capsule, ±90)` (кольори міняються місцями при повних обертах).
- КОЛИ `input(down)` → ТО прискорене падіння.
- КОЛИ `locked(capsule)` → ЯКЩО `pattern(line(4+, same_color))` по горизонталі або вертикалі (половинки + віруси) → ТО `clear(line)`; кілька ліній одночасно — разом.
- КОЛИ `after(clear)` → ТО `custom: «split — партнер зниклої половинки стає одиноким»`, `fall(unsupported)`: одинока половинка падає сама; зʼєднана пара — лише якщо обидві без опори.
- КОЛИ `after(fall)` → ЯКЩО `pattern(line(4+))` → ТО `clear`, `combo(+1)` і повтор до стабілізації.
- Рахунок: лише за віруси; за кожен наступний вірус, знищений одним ходом, ціна подвоюється: Low 100, 200, 400, 800, 1600, 3200 (6+); Med ×2 (200…6400), Hi ×3 (300…9600). Половинки й падіння очок не дають.
- КОЛИ `counter(capsules_dropped, ==, n)` → ТО `speed(fall, +1)`, `sound(chime)`.
- КОЛИ `all_gone(virus)` → ТО `win` рівня, `next_level` (+1 рівень, більше вірусів).
- КОЛИ `locked(capsule)` → ЯКЩО `occupied(neck_cells)` → ТО `lose` (Game Over).
- Versus: КОЛИ `after(clear)` → ЯКЩО `lines_cleared ≥ 2` за хід → ТО `custom: «send_garbage — N одиноких половинок кольорів зчищених ліній; 2 шт. — через 4 стовпці, 3 — через 2»`; КОЛИ `all_gone(own_virus)` або суперник `lose` → `win` раунду; матч — до 3 перемог.

## Керування і ввід
- NES: ←/→ — зсув (утримання — автоповтор), A — поворот за годинниковою, B — проти, ↓ — прискорене падіння, Start — пауза. Hard drop у класиці нема.
- Versus: двоє гравців одночасно, кожен своя пляшка.

## Вікна, меню, HUD
- `splash-screen` — титул з Маріо, `main-menu`: 1 Player / 2 Player.
- `custom: «level/speed/music select»` (`difficulty-select`): Virus Level 0–20 (повзунок), Speed Low/Med/Hi, Music Type Fever/Chill/Off — один екран-налаштування перед грою.
- `game-screen`: пляшка в центрі; Маріо праворуч тримає наступну капсулу (`next-piece-preview`); ліворуч `hi-score` (TOP) і `score`; праворуч `level-number`, `custom: «speed»`, `remaining-counter` (Virus); лупа з трьома анімованими вірусами, що зникають, коли їхній колір вибито.
- `end-screen`: «Stage Clear» з переходом на наступний рівень; Game Over з поверненням до вибору.
- 2P: дві пляшки, лічильник перемог (корони) кожного; `pause-menu` — просто «Pause».
- Переходи: splash → main-menu → settings (level/speed/music) → game-screen → (clear) → game-screen наступного рівня; (game over) → вибір.

## Фічі поза полем
- `custom-difficulty`: стартовий рівень (к-сть вірусів) + швидкість окремо; `music-toggle` з вибором треку.
- `hi-score` між рівнями однієї сесії; `levels-sequential` — нескінченно після 20 (84 віруси).
- `mode-versus` / `local-multiplayer` (2P), пізніше — Flash/Marathon/онлайн (Dr. Mario 64, Online Rx, Dr. Luigi з L-капсулами).
- `pause`.

## Варіації й родичі
- Dr. Mario 64 (story, 4 гравці) · Dr. Mario Online Rx · Dr. Luigi (2013 — L-подібні подвійні капсули) · Miracle Cure (предмети-«ліки») · Dr. Mario World (мобільна, вірусів знизу, ходи).
- Родичі: Puyo Puyo (група, а не лінія; кожна кулька окремо), Columns (3 у лінію з діагоналями), Tetris (без цілей на полі).
- **Осі варіацій**: ціль поля (нема / віруси / квота) · фігура (1×2 / L / 2×2) · звʼязок половинок після зникнення (розрив / нема) · умова (4 у лінію / група) · сміття (одинокі половинки / ряди).

## Цікавинки для курсу
- Генерація стартового поля з N вірусів без готових ліній — 📎 (перегенерація або перевірка 3 в ряд при розстановці).
- Капсула з двох половинок, що «розривається» при зникненні однієї — 🥉 (звʼязок пар як стан клітини).
- Каскад з двома видами падіння (пара разом / одинока окремо) — 🥉.
- Подвоєння очок за вірус у межах одного ходу × швидкість — 🌱.
- Versus зі сміттям-половинками кольорів зчищених ліній — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (капсула 1×2) · `keyboard-controls` · `collect-all` / `destroy-all-enemies` (усі віруси) · `sequential-levels` · `difficulty-levels` (рівень + швидкість) · `progress-acceleration` · `event-points` · `combo-multiplier` · `score-records` · `game-pause` · `background-music` + `music-toggle` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+line-match-clear` «Зникнення лінії з N однакових» · entities/legality · 📎 · слоти {n: 3|4|5, dirs: 2|4}.
  - `+chain-reaction` «Ланцюгова реакція збігів» · game-logic/score · 🥉 (спільна з Puyo).
  - `+split-on-clear` «Розрив звʼязаної фігури» · entities/state · 🥉.
  - `+next-queue` · interface/hud · 🌱 (спільна).
  - `+garbage-attack` · game-logic/opponent · 🥉 (спільна).
  - `+virus-board-generation` «Стартове поле з цілей без готових збігів» · levels/generation · 📎 · слот {count}.

## Пропозиції до словників
- `+trigger:locked`, `+trigger:settled` — як у Tetris/Puyo.
- `+effect:split` — розірвати звʼязок пари (половинка стає незалежною); `+effect:send_garbage`.
- `+window:difficulty-select` — ⏳ підтверджую (рівень вірусів + швидкість + музика на одному екрані).
- `+ui:virus-counter` — радше `remaining-counter` (⏳), окреме слово не потрібне, якщо куратор погодить.
- `+axis:gravity` — `cascade` з парами (половинки зʼєднані до розриву).

## Джерела
- ⭐ [Super Mario Wiki: Dr. Mario (game)](https://www.mariowiki.com/Dr._Mario_(game)) — пляшка 8×16, віруси 4×level+4, Low/Med/Hi, таблиця очок, garbage у versus, Fever/Chill/Off, умова Game Over.
- [Wikipedia: Dr. Mario](https://en.wikipedia.org/wiki/Dr._Mario) — правила коротко, 1990 NES/Game Boy, versus до 3 перемог, сиквели.
- YouTube: пошук «dr mario nes gameplay».

## Непевне
- (?) Через скільки капсул зростає швидкість (10?) — джерело не дає числа.
- (?) Обмеження висоти розстановки вірусів за рівнем — не перевірено.
- (?) Чи таблиця очок кумулятивна (1-й вірус 100, 2-й 200 → разом 300) — сформульовано як подвоєння за кожен наступний вірус, з памʼяті.
- (?) Лупа з анімованими вірусами і розташування HUD — з памʼяті про NES.
