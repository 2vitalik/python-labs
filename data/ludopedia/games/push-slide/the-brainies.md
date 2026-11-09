---
title: The Brainies (Tiny Skweeks)
slug: the-brainies
aka: [Tiny Skweeks, The Tinies, Brainies]
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1991
platforms: [Amiga, Atari ST, Amstrad CPC, MS-DOS, Apple IIGS, Macintosh, SNES]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Brainies", best: true, note: "101 рівень, керуєш лише напрямом, стрілки розвертають і на мить знерухомлюють, предмети допомагають або шкодять, ліміт часу коштує життя, 4 складності, SNES-режим 3D (Mode 7)"}
  - {kind: other, url: "https://gamesdb.launchbox-app.com/games/details/84782-the-brainies", note: "4 кольори брейні, приціл + fire бере/віддає керування, іде до стіни, перешкоди чи іншого брейні"}
  - {kind: other, url: "https://www.homeoftheunderdogs.net/game.php?id=1701", note: "Tiny Skweeks (DOS): кожного на пад свого кольору, курсор + пробіл, рух як у Lemmings до упору"}
  - {kind: other, url: "https://www.vgmuseum.com/images/pics2/brainies.html", note: "SNES: 100 рівнів, пароль, знімок поля з HUD TIME / JOKER / SCORE / LEVEL"}
  - {kind: other, url: "https://almarsguides.com/retro/walkthroughs/snes/games/thebrainies/", note: "паролі SNES — 6 літер з B / G / R / Y кожні 5 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Brainies+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, selection-highlight, inertia-slide, all-on-targets, time-out, player-death, item-pickup, difficulty-levels, sequential-levels, level-password, status-panel, +typed-targets, +stop-on-entity, +direction-arrow-tile]
proposes: ["+card:select-then-send", "+feature:view-toggle", "+ui:joker-counter"]
author: opus
date: 2026-11-09
---

# The Brainies — наведи приціл на брейні, дай напрям — і він іде, доки не вріжеться; загнати всіх на пади свого кольору до кінця часу

## Суть
На полі кілька брейні (мексиканських «стрибучих бобів») чотирьох кольорів і пади тих самих кольорів. Гравець прицілом обирає брейні й задає лише **напрям**: той іде, доки не впреться в стіну, перешкоду чи іншого брейні. Пад сам не зупиняє, тому зупинки будуються з перешкод і з інших брейні — як у Ricochet Robots, але в реальному часі й під таймер. Стрілки на підлозі примусово розвертають брейні й на мить роблять його некерованим, а предмети на полі можуть і допомогти, і зашкодити.

## Поле і час
- Квадратна сітка; на SNES — трав'яні острівці з водою по краях, вигляд під кутом (Mode 7, режим 3D); поле видно цілком.
- Шари: підлога (трава / вода-межа) → пади й стрілки → предмети → брейні → приціл.
- Real-time: брейні крокують клітина за клітиною, кілька можуть рухатись одночасно (?); таймер рівня йде весь час.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Брейні | piece | колір (1 з 4) | отримавши напрям, іде до упору; сам є упором для інших |
| Пад | zone | колір | ціль: на ньому має стояти брейні того ж кольору; не зупиняє |
| Стіна / вода по краю | static | — | зупиняє брейні перед собою |
| Перешкода | static | — | зупиняє брейні |
| Стрілка | terrain | напрям | розвертає брейні у свій бік і на мить знерухомлює |
| Предмет | pickup | вид | підбирається на ходу; допомагає або заважає (?) |
| Приціл | — | позиція | рамка-курсор гравця, не сутність поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire)` → ЯКЩО `occupied(cursor_cell, brainy)` → ТО `set_state(brainy, controlled)` (повторне натискання — `clear_state`).
- КОЛИ `input(dir)` → ЯКЩО `state(brainy, controlled)` → ТО `slide(brainy, dir)` — крок за кроком до упору.
- КОЛИ `blocked(brainy)` (стіна, перешкода, інший брейні) → ТО `custom: «зупиняється перед упором»`.
- КОЛИ `enter(brainy, pad)` → ТО `custom: «іде далі — пад не зупиняє»`.
- КОЛИ `enter(brainy, arrow)` → ТО `face(brainy, arrow_dir)`, `stun(brainy, n)`, далі `slide(brainy, arrow_dir)`.
- КОЛИ `contact(brainy, item)` → ТО `pickup`, `custom: «ефект предмета: допомагає або шкодить»` (?).
- КОЛИ `all_on(brainy, same_color_pad)` → ТО `win`, `score(n)` (?), `next_level`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lives(-1)`, `restart`.
- Перемога: усі брейні на падах свого кольору. · Поразка: вичерпано час → мінус життя; життя скінчились — кінець гри (?). · Рахунок: SCORE у HUD SNES, формула невідома (?).

## Керування і ввід
- Стрілки / джойстик рухають приціл; пробіл / fire над брейні — взяти або віддати керування; далі напрямок — куди йти (DOS: пробіл).
- Два режими вводу по черзі: «наведення прицілу» і «напрям обраному брейні» (`+card:select-then-send`).
- SNES: перемикання на 3D-вигляд (Mode 7).

## Вікна, меню, HUD
- `game-screen` (SNES): угорі TIME (запас часу / життя-обличчя (?)), JOKER, SCORE, LEVEL; поле з прицілом-рамкою.
- `difficulty-select` — 4 рівні складності.
- `level-password` (SNES): 6 кольорових літер B / G / R / Y, видається кожні 5 рівнів.
- `end-screen` — кінець рівня / кінець гри (?).
- Переходи: титул → вибір складності / пароль → рівень → (усі на падах) наступний рівень; час вийшов → той самий рівень мінус життя.

## Фічі поза полем
- `levels-sequential` — 101 рівень (комп'ютери), 100 на SNES.
- `difficulty-presets` — 4 складності; `level-password` замість збереження.
- `+feature:view-toggle` — 2D / 3D (Mode 7) на SNES.
- «Joker» — лічильник у HUD; призначення не підтверджене (?).

## Варіації й родичі
- Назви: The Tinies (комп'ютери), Tiny Skweeks (Європа, приписано до серії Skweek пізно), The Brainies (Північна Америка, SNES від Titus). За FR-вікі — на основі інді-гри Leitmotiv.
- [Ricochet Robots](ricochet-robots.md) — та сама ідея «до упору, інші фігури — упори», але покроково й без таймера.
- [ChuChu Rocket!](../maze-arcade/chuchu-rocket.md) — стрілки на підлозі розвертають мишей (`+direction-arrow-tile`); [Lemmings](../dig-gravity/lemmings.md) — істоти йдуть самі.
- [Ice-sliding puzzles](ice-sliding-puzzles.md), [Atomix](atomix.md) — ковзання до упору як основа.
- Осі варіацій: **хто рухається** (одна фігура / будь-яка з набору) · **час** (покроково / таймер) · **що зупиняє** (стіна / інша фігура / спецклітина) · **ціль** (будь-яка / свого кольору).

## Цікавинки для курсу
- Рух «до упору», де інші фігури — упори, для кількох фігур одночасно — 📎.
- Приціл: обрати фігуру, потім напрям (двофазний ввід) — 🌱.
- Стрілки, що розвертають і знерухомлюють на N тіків — 📎.
- Цілі за кольором + таймер рівня з життями — 🌱.
- Розвʼязувач BFS для покрокової версії (позиції всіх брейні) — 🥈.
- Пароль рівня як код із 6 кольорів — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ приціл і напрям; `selection-highlight` ↔ рамка прицілу; `inertia-slide` ↔ іде до упору; `all-on-targets` ↔ пади; `time-out` + `player-death` ↔ таймер і життя; `item-pickup` ↔ предмети; `difficulty-levels`; `sequential-levels`; `level-password`; `status-panel` ↔ TIME / JOKER / SCORE / LEVEL.
- **Нема** → пропозиції карток:
  - `+typed-targets` (уже пропонована) — пад свого кольору.
  - `+stop-on-entity` (уже пропонована, Inertia) — інший брейні як упор.
  - `+direction-arrow-tile` (уже пропонована, ChuChu Rocket!) — стрілка розвертає.
  - `+select-then-send` «Обрати фігуру курсором, потім дати напрям» · interface/input · 🌱.

## Пропозиції до словників
- `+card:select-then-send` — двофазний ввід: вибір фігури прицілом, потім напрям.
- `+feature:view-toggle` — перемикання 2D / 3D-вигляду без зміни логіки (SNES Mode 7).
- `+ui:joker-counter` — лічильник «джокерів» у HUD (призначення — у «Непевне»).

## Джерела
- ⭐ [Wikipedia: The Brainies](https://en.wikipedia.org/wiki/The_Brainies) — правила, стрілки, предмети, таймер і життя, 4 складності, 101 рівень, 3D на SNES, автори, назви.
- [LaunchBox Games DB](https://gamesdb.launchbox-app.com/games/details/84782-the-brainies) — 4 кольори, приціл + fire, рух до упору.
- [Home of the Underdogs](https://www.homeoftheunderdogs.net/game.php?id=1701) — мета «кожного на пад свого кольору», керування пробілом.
- [VGMuseum](https://www.vgmuseum.com/images/pics2/brainies.html) — SNES: 100 рівнів, пароль, знімок поля й HUD; «перешкоди й інші брейні — щоб спрямувати кожного на пад».
- [Almar's Guides](https://almarsguides.com/retro/walkthroughs/snes/games/thebrainies/) — паролі з 6 кольорових літер.
- [Wikipedia FR: Skweek](https://fr.wikipedia.org/wiki/Tiny_Skweeks) — Tiny Skweeks як частина серії, основа — Leitmotiv.

## Непевне
- (?) Список предметів і їхні ефекти, призначення JOKER — джерела кажуть лише «допомагають або шкодять».
- (?) Чи можна зупинити брейні посеред руху (повторний fire) і чи рухаються кілька брейні одночасно.
- (?) Що означають три обличчя під TIME у HUD SNES (запас часу чи життя), формула SCORE.
- (?) Рік: Wikipedia — 1991 (комп'ютери), DOS-база — 1992; SNES — 1994 (VGMuseum) / 1996 (Wikipedia).
- (?) Almar's Guides також пише, що брейні «зникають групами по 4» — суперечить усім іншим джерелам, не враховано.
