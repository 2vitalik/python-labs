---
title: "Pac-Man: сиквели 1983–2021"
slug: pac-man-sequels
aka: [Jr. Pac-Man, Pac-Mania, Pac-Man Vs., Pac-Man 99, パックマニア]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: collect
year: 1983
platforms: [arcade, Atari 2600, Amiga, Genesis, GameCube, GBA, Nintendo DS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_Vs.", best: true, note: "асиметричний мультиплеєр: Пекмен на GBA бачить усе, привиди на TV — лише окіл; хто впіймав — стає Пекменом"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jr._Pac-Man", note: "лабіринт удвічі ширший за екран, без тунелів, іграшки роблять «товсті» точки і підривають енерджайзер"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Mania", note: "похилий вид зі скролом, стрибок над привидами, Funky і Spunky стрибають теж, червоні й зелені енерджайзери"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_99", note: "99 гравців, Jammer-Пекмени суперникам, сплячі привиди-потяги, вибір цілі атак"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+vs+gamecube+gameplay", note: "пошук; Pac-Man Vs."}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac-man+99+gameplay", note: "пошук; Pac-Man 99"}
stage: v1
coverage: 60
mechanics: [move-auto, collect-all, touch-death, temporary-modes, player-camera, wrap-edges, fog-of-war, event-points, sequential-levels, progress-acceleration, garbage-attack, simultaneous-versus, online-multiplayer, hot-seat, match-setup, mode-select, ai-opponent, realtime-ai, +scrolling-maze, +bonus-upgrades-dots, +bonus-destroys-powerup, +jump-over-enemy, +jump-decay-timer, +enemy-jump-classes, +colored-power-pellets, +asymmetric-roles, +catcher-swaps-role, +limited-vision-radius, +neutral-ghost-tagging, +jammer-attack, +sleeping-ghost-train, +attack-target-strategy, +powerup-choice-while-powered]
proposes: ["+trigger:jump", "+cond:airborne", "+effect:swap_role(a, b)", "+effect:tag(a, side)", "+ui:vision-circle", "+ui:target-strategy", "+window:split-device", "+axis:asymmetry", "+card:asymmetric-roles", "+card:jammer-attack"]
author: opus
date: 2026-11-09
---

# Pac-Man: сиквели 1983–2021 — чотири способи змінити Pac-Man: ширший лабіринт, стрибок, привиди-люди з обмеженим оглядом, 99 суперників з «сміттям»

## Суть
Усі чотири гри стоять на правилах [pac-man](pac-man.md) (точки, енерджайзер, привиди, будиночок) і [ms-pac-man](ms-pac-man.md) (мандрівний бонус). Кожна змінює одну вісь. **Jr. Pac-Man** (1983) — лабіринт удвічі ширший за екран, без тунелів, а бонус-іграшка псує поле. **Pac-Mania** (1987) — похилий 3D-вид і **стрибок** над привидами, на який деякі привиди відповідають своїм. **Pac-Man Vs.** (2003) — привидами керують люди, і бачать вони лише окіл, а Пекмен — усе. **Pac-Man 99** (2021) — battle royale: зʼїдений привид летить суперникові «джамером». PvP на спільному полі — у [pac-man-battle-royale](pac-man-battle-royale.md), 64 лабіринти з воротами — у [pac-man-spinoffs](pac-man-spinoffs.md), нескінченний лабіринт — у [pac-man-256](pac-man-256.md).

### Що змінено
| Гра | Поле | Нове в ядрі | Суперник |
|---|---|---|---|
| Jr. Pac-Man | 7 лабіринтів удвічі ширших за екран, горизонтальний скрол, тунелів нема | іграшка перетворює точки на «товсті», потім підриває енерджайзер | 4 привиди (Tim замість Clyde) |
| Pac-Mania | 4 світи, похилий вид, скрол в обидва боки | стрибок; червоні (×2 очок) і зелені (швидкість) енерджайзери | 5 привидів + Funky і Spunky, що стрибають |
| Pac-Man Vs. | 6 лабіринтів | асиметрія: Пекмен бачить усе, привиди — коло огляду | 1–3 гравці-привиди, ролі міняються |
| Pac-Man 99 | свій лабіринт у кожного (?) | джамери, сплячі привиди, вибір цілі | 98 онлайн-суперників |

## Поле і час
- **Jr.:** лабіринт «удвічі ширший за монітор», камера скролить по горизонталі за гравцем; жодного тунелю-тору; 5 лабіринтів мають 6 енерджайзерів, 2 — по 4.
- **Pac-Mania:** похилий (не ізометричний) вид, скрол по обох осях; у деяких планах лівий і правий краї зʼєднані. Світи: Block Town, Pac-Man's Park, Sandbox Land, Jungly Steps — по кілька раундів, потім цикл. Висота — лише для стрибка: логіка лабіринту лишається плоскою.
- **Vs.:** гравець-Пекмен дивиться на екран GBA з усім лабіринтом; привиди — на TV, де видно лише коло навколо кожного привида.
- **99:** свій лабіринт по центру, мініатюри суперників ліворуч і праворуч. Зʼїдений бонус разом зі сплячими привидами генерує новий лабіринт (?).
- Усі — real-time.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен / Jr. Pac-Man | player | — | як у `pac-man.md`; у Pac-Mania може стрибати |
| Іграшка (Jr.: триколісний велосипед, змій, кульки…) | pickup | 1 на раунд | стартує над будиночком, мандрує; точки під нею → «товсті»; згодом іде до енерджайзера і вибухає разом з ним |
| «Товста» точка (Jr.) | pickup | дорожча | сповільнює їдця сильніше; при смерті зникає або повертається у звичайну |
| Tim (Jr.) | enemy | — | замість Clyde |
| Funky (зелений), Spunky (сірий) (Pac-Mania) | enemy | пізні раунди | стрибають; над Funky Пекмен ледь перестрибує, над Spunky — ні |
| Sue (фіолетовий, Pac-Mania) | enemy | — | п'ятий привид від старту |
| Червоний енерджайзер (Pac-Mania) | pickup | — | очки за синіх привидів ×2, доки не втрачено життя |
| Зелений енерджайзер (Pac-Mania) | pickup | — | тимчасово пришвидшує Пекмена |
| Привид-гравець (Vs.) | enemy | коло огляду | людина керує; ловить Пекмена — забирає очки й роль |
| Сірий CPU-привид (Vs.) | neutral | — | при <4 гравцях; не шкодить, доки гравець-привид його не «позначить» своїм кольором |
| Фрукт (Vs.) | pickup | під будиночком | їдять і Пекмен, і привиди; привидам розширює огляд |
| Сплячий привид (99) | neutral | — | Пекмен, проходячи, збирає його в «потяг» за привидом-ватажком |
| Jammer-Пекмен (99) | enemy | звичайний / червоний | прилітає в лабіринт цілі: звичайний сповільнює, червоний вибиває |

## Правила (КОЛИ → ЯКЩО → ТО)
Jr. Pac-Man:
- КОЛИ `tick` → ТО `custom: «камера тримає гравця, лабіринт скролиться по горизонталі»`; КОЛИ `edge(pac)` → ТО `block` — тору нема.
- КОЛИ `level_start` → ТО `spawn_at(toy, above_house)`; КОЛИ `contact(toy, dot)` → ТО `transform(dot → fat_dot)`.
- КОЛИ `contact(pac, fat_dot)` → ТО `pickup`, `score(n)`, `speed(pac, −)` — сильніше, ніж на звичайній.
- КОЛИ `timer(toy)` → ТО `custom: «іграшка йде до одного з лишених енерджайзерів»`; КОЛИ `contact(toy, energizer)` → ТО `disappear_both`.
- КОЛИ `contact(pac, toy)` → ТО `pickup`, `score(n)`.
- КОЛИ `died(pac)` → ТО `custom: «товсті точки зникають або стають звичайними — залежно від кількості лишених точок»`.
Pac-Mania:
- КОЛИ `input(jump)` → ТО `set_state(pac, airborne, t)` (`+trigger:jump`); КОЛИ `contact(pac, ghost)` → ЯКЩО `state(pac, airborne)` and `not state(ghost, airborne)` → ТО `custom: «проліт над привидом»`; інакше `lives(-1)`.
- КОЛИ `input(jump)` поряд з Funky/Spunky → ТО `custom: «привид стрибає у відповідь»`: над Funky — ледь вдається, над Spunky — ні.
- КОЛИ `timer(stage)` → ЯКЩО `custom: «раунд затягнуто»` → ТО `custom: «висота стрибка поступово спадає до нуля»`.
- КОЛИ `contact(pac, red_pellet)` → ТО `multiplier(×2)` для синіх привидів; КОЛИ `died(pac)` → ТО `reset_combo`.
- КОЛИ `contact(pac, green_pellet)` → ТО `speed(pac, +, t)`.
- КОЛИ `counter(dots_eaten, ==, n)` → ТО `spawn_at(bonus, center)` — бонусом може бути й червоний/зелений енерджайзер.
- КОЛИ `custom: «пройдено всі світи задану кількість разів»` → ТО `game_over`; режими 11 / 25 раундів / нескінченний.
Pac-Man Vs.:
- КОЛИ `tick` → ТО `custom: «привид-гравець бачить лише клітини в радіусі r»`; Пекмен бачить усе (`+ui:vision-circle`).
- КОЛИ `contact(ghost_player, pac)` → ТО `score(ghost_player, n)`, `custom: «упіймав → наступний раунд він Пекмен»` (`+effect:swap_role`), `custom: «забирає 1600 у Пекмена»`.
- КОЛИ `all_gone(dot)` → ТО `score(pac_player, 1600)`, `custom: «лишається Пекменом»`.
- КОЛИ `contact(ghost_player, cpu_ghost)` → ТО `custom: «CPU-привид отримує колір гравця й тепер ловить на його рахунок»` (`+effect:tag`).
- КОЛИ `contact(pac, energizer)` → ТО `set_state(ghosts, frightened, t)`, `speed(ghosts, −)`; КОЛИ `contact(pac, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `custom: «Пекмен забирає очки привида»`, `respawn(ghost, house)`.
- КОЛИ `contact(ghost_player, fruit)` → ТО `score(n)`, `custom: «тимчасово ширше коло огляду»`.
- КОЛИ `counter(score, >=, target)` (7 000 / 10 000 / 15 000) → ТО `win` для цього гравця.
Pac-Man 99:
- КОЛИ `contact(pac, sleeping_ghost)` → ТО `custom: «приєднується до потяга за привидом»`; під енерджайзером зʼїсти весь потяг — серія.
- КОЛИ `contact(pac, ghost)` → ЯКЩО `state(ghost, frightened)` → ТО `send_garbage(target, jammer)`.
- КОЛИ `contact(jammer, pac)` → ТО `speed(pac, −)`; ЯКЩО `custom: «червоний джамер»` → ТО `lose`.
- КОЛИ `contact(pac, energizer)` → ТО `custom: «звичайні джамери зникають, червоні завмирають»`; КОЛИ `contact(pac, fruit)` → ТО `disappear_b` (червоні джамери).
- КОЛИ `contact(pac, ghost)` → ЯКЩО `not state(ghost, frightened)` → ТО `lose` — вибування.
- КОЛИ `custom: «лишився один гравець»` → ТО `win`.

## Керування і ввід
- **Jr.:** джойстик як в оригіналі.
- **Pac-Mania:** джойстик + кнопка стрибка (?) — джерело кнопок не описує.
- **Vs.:** Пекмен — GBA через кабель-лінк до GameCube; привиди — 1–3 геймпади GameCube; один телевізор, але різна інформація на двох екранах (`+window:split-device`).
- **99:** геймпад Switch; окремо — перемикач стратегії цілі атак (`+ui:target-strategy`): той, хто майже вибув / ті, хто атакує мене / лідер за KO / випадково; вибір посилення, що діє під енерджайзером (швидше / сильніше).

## Вікна, меню, HUD
- **Jr.:** `game-screen` зі скролом; `+window:intermission` — сценки Jr. Pac-Man і Yum-Yum (донька Blinky).
- **Pac-Mania:** `level-select` — старт з будь-якого з перших трьох світів; `game-screen`; `mode-select` 11/25/∞ (?) — можливо, це операторське налаштування.
- **Vs.:** `match-setup` — ціль очок 7 000 / 10 000 / 15 000, вибір лабіринту з 6; TV `game-screen` з колами огляду; GBA `game-screen` з повним лабіринтом; коментатор (голос Маріо) оголошує енерджайзери й фрукти.
- **99:** `main-menu` → `mode-select` (онлайн; з DLC — офлайн, приватні матчі, score attack) → `lobby-window` → `game-screen` (свій лабіринт, мініатюри суперників, перемикач цілі, місце) → `end-screen`; `theme-select` — теми з ігор Namco (Galaga, Dig Dug…).

## Фічі поза полем
- Jr.: `levels-sequential` по 7 лабіринтах.
- Pac-Mania: бонус очок за перший раунд у Pac-Man's Park і Sandbox Land; режими 11 / 25 / ∞ раундів.
- Vs.: `local-multiplayer` на двох пристроях; пізніші версії — DS Download Play (Namco Museum DS, 2007), мобільна через Bluetooth, Switch (Namco Museum, 2017).
- 99: `online-multiplayer` на 99; платні DLC (режими, теми); закрито 8 жовтня 2023 — офлайн-режими лишились у власників DLC.

## Варіації й родичі
- У корпусі: `pac-man` (база), `ms-pac-man` (мандрівний бонус → у Jr. він ще й псує поле), `pac-man-battle-royale` (PvP на одному полі), `pac-man-spinoffs` (Pac & Pal, Baby, Mega Tunnel Battle), `pac-man-256` (нескінченний лабіринт), `pac-man-championship-edition`, `super-pac-man`.
- Pac-Man 99 — та сама схема, що Tetris 99: власне поле + атаки «сміттям» на обраного суперника.
- **Осі варіацій:** камера (весь лабіринт / скрол / похилий вид); ухилення (лише маневр / стрибок / стрибок проти стрибунів); хто привиди (AI / люди з обмеженим оглядом); як суперники шкодять одне одному (спільне поле / сміття в чуже поле / ворота між полями).

## Цікавинки для курсу
- Скрол лабіринту ширшого за екран — `player-camera` на клітинному полі — 🌱.
- Бонус, що перетворює клітини на шляху і руйнує ціль, — 📎 (агент з таймером намірів).
- Стрибок з «висотою», яку перевіряє зіткнення, і вороги-стрибуни, що його нейтралізують, — 📎.
- Асиметрична інформація: двоє бачать одне поле по-різному (коло огляду для привидів) — 🥈 (два рендери одного стану).
- «Хто впіймав — той Пекмен»: роль переходить переможцеві раунду — 📎.
- Джамери + вибір стратегії цілі — 🥈 (атаки між полями, черга сміття, вибір отримувача).
- Сплячі привиди-потяг: збір сутностей у ланцюжок за ватажком — 📎.

## Мапа на каталог
- Є: `move-auto` · `collect-all` · `touch-death` · `temporary-modes` · `player-camera` (Jr., Pac-Mania) · `wrap-edges` (Pac-Mania; у Jr. навмисно нема) · `fog-of-war` (Vs., для привидів) · `garbage-attack` + `simultaneous-versus` (99) · `online-multiplayer` · `hot-seat` (Vs.: кілька людей за одним TV) · `match-setup` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+scrolling-maze` «Лабіринт ширший за екран» · interface/render · 🌱 (дитина `player-camera`).
  - `+bonus-upgrades-dots` «Бонус змінює клітини на своєму шляху» · entities/interact · 📎.
  - `+bonus-destroys-powerup` «Бонус знищує посилення, якщо не встигнути» · entities/interact · 📎.
  - `+jump-over-enemy` «Стрибок над ворогом» · entities/move · 📎 · слот {duration}.
  - `+jump-decay-timer` «Стрибок слабшає, якщо затягнути рівень» · game-logic/difficulty · 🌱.
  - `+enemy-jump-classes` «Вороги, що стрибають у відповідь» · entities/move · 📎.
  - `+colored-power-pellets` «Різні посилення: ×2 очок / швидкість» · entities/state · 🌱.
  - `+asymmetric-roles` «Один гравець проти кількох з різними правилами» · game-logic/opponent · 🥈.
  - `+catcher-swaps-role` «Хто впіймав — міняється роллю» · game-logic/opponent · 📎.
  - `+limited-vision-radius` «Гравець бачить лише коло навколо своєї сутності» · interface/render · 📎 (дитина `fog-of-war`).
  - `+neutral-ghost-tagging` «Нейтральна сутність переходить на бік того, хто торкнувся» · entities/interact · 📎.
  - `+jammer-attack` «Ворог-джамер у поле суперника» · game-logic/opponent · 🥈 (дитина `garbage-attack`).
  - `+sleeping-ghost-train` «Сутності збираються в ланцюжок» · entities/move · 📎.
  - `+attack-target-strategy` «Стратегія вибору цілі атак» · game-logic/opponent · 📎.
  - `+powerup-choice-while-powered` «Обране посилення діє лише під енерджайзером» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:jump` — сутність відірвалась від поля (стрибок як подія); `+cond:airborne` — у повітрі (чи можна замінити `state(a, airborne)` — питання куратору).
- `+effect:swap_role(a, b)` — гравці міняються ролями (Vs.).
- `+effect:tag(a, side)` — нейтральна сутність переходить на бік (близько до ⏳ `set_side`, але без захоплення).
- `+ui:vision-circle` — коло видимості навколо сутності; `+ui:target-strategy` — перемикач цілі атак.
- `+window:split-device` — ті самі дані на двох пристроях з різною видимістю.
- `+axis:asymmetry` — сторони грають за різними правилами/інформацією (Vs., Dead by Daylight, Scotland Yard).
- `+card:asymmetric-roles`, `+card:jammer-attack` — див. вище.

## Джерела
- ⭐ [Wikipedia: Pac-Man Vs.](https://en.wikipedia.org/wiki/Pac-Man_Vs.) — GBA + TV, обмежений огляд, фрукт розширює огляд, CPU-привиди і «позначення», 1600 очок, цілі 7 000/10 000/15 000, 6 лабіринтів.
- [Wikipedia: Jr. Pac-Man](https://en.wikipedia.org/wiki/Jr._Pac-Man) — ширина «удвічі за монітор», 7 лабіринтів, 6/4 енерджайзери, нема тунелів, іграшки й товсті точки, Yum-Yum.
- [Wikipedia: Pac-Mania](https://en.wikipedia.org/wiki/Pac-Mania) — похилий вид, 4 світи, стрибок і його згасання, Funky/Spunky, червоні й зелені енерджайзери, режими 11/25/∞.
- [Wikipedia: Pac-Man 99](https://en.wikipedia.org/wiki/Pac-Man_99) — 99 гравців, джамери звичайні й червоні, сплячі привиди, стратегії цілі, DLC, закриття 2023.
- YouTube: пошуки «pac-man vs gamecube gameplay», «pac-man 99 gameplay».

## Непевне
- (?) Pac-Man 99: Wikipedia прямо не каже, що в кожного свій лабіринт (лише мініатюри суперників збоку); механізм «новий лабіринт від бонуса й сплячих привидів» описано неясно.
- (?) Pac-Mania: кнопка стрибка, кількість раундів на світ, чи 11/25/∞ — вибір гравця чи DIP-налаштування.
- (?) Pac-Man Vs.: радіус огляду, кількість точок до появи фрукта, загальна кількість гравців (1 Пекмен + 1–3 привиди ⇒ 2–4).
- (?) Jr.: очки за товсті точки й іграшки, таймер іграшки, кількість життів.
- (?) Пріоритет осі `opponent`: файл зводить чотири гри; `online` — за Pac-Man 99, решта — `ai` / `hotseat`.
