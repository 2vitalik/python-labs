---
title: Blockout (Block Out)
slug: blockout
aka: [Block Out, BlockOut II, 3D Tetris]
family: falling-match
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1989
platforms: [MS-DOS, Amiga, Atari ST, C64, Apple IIGS, Mac OS, arcade, Mega Drive, Atari Lynx, PC-98]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blockout", best: true, note: "3D-стакан згори, полікуби, поворот трьома кнопками по трьох осях, грань-шар зникає, раунди Mega Drive, бонус-етап, versus"}
  - {kind: official, url: "http://www.blockout.net/blockout2/", note: "BlockOut II — відкритий ремейк (GPL), онлайн-рекорди з повторами"}
  - {kind: other, url: "http://www.blockout.net/blockout2/scoretable.php?set=0&width=5&height=5&depth=12", note: "таблиці очок BlockOut II: набори FLAT/BASIC/EXTENDED, стакан 3–7 × 3–7 × 6–18, рівні 0–10, бонус за порожній стакан"}
  - {kind: fandom, url: "https://www.harddrop.com/wiki/Blockout", note: "HardDrop: стакан 5×5×12, без hold, налаштовуваний"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=blockout+1989+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, event-points, time-out, score-records, leaderboard, difficulty-levels, field-size-picker, game-settings, replay, simultaneous-versus, garbage-attack, +3d-polycube-rotation, +layer-clear-3d, +depth-gauge, +drop-height-bonus, +empty-pit-bonus, +piece-set-select]
proposes: ["+effect:rotate3d", "+cond:fits3d", "+ui:depth-gauge", "+ui:pit-wireframe", "+feature:pit-size", "+feature:piece-set", "+feature:online-replay-scores", "+card:3d-polycube-rotation"]
author: opus
date: 2026-11-09
---

# Blockout — тетріс у справжньому 3D-стакані: полікуби, поворот по трьох осях, зникає повний шар

## Суть
Дивишся згори в прямокутний 3D-«колодязь» (pit); полікуб (фігура з кубиків) повільно опускається вглиб, гравець зсуває його по двох горизонтальних осях і **обертає навколо будь-якої з трьох осей**. Фігура фіксується, щойно торкнулась дна чи кубика. Повністю заповнений **горизонтальний шар** («грань», face) зникає, верхні кубики опускаються. Головна складність — просторове мислення: дно видно крізь стек, глибину кодує колір шару. Решта — як [Tetris](tetris.md), перенесений на одну вимірність вище.

## Поле і час
- Стакан W × D × H: на ПК налаштовується від 3×3×6 до 7×7×18 (195 розмірів); типово 5×5×12. Разом із наборами фігур і швидкістю — 585 конфігурацій.
- Камера фіксована, вид згори в перспективі (каркас стінок); фігура малюється каркасом, стек — заповненими кубиками; колір кубика залежить від глибини шару (?).
- Real-time: фігура опускається на шар за тік рівня; швидкість росте з рівнем.
- Mega Drive: розміри стакана змінюються від раунду до раунду; кожен 5-й раунд — бонус-етап 2×2 на 30 с.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активний полікуб | player | форма (1–5 кубиків), орієнтація в 3D | опускається; ввід зсуває по X/Y, обертає по X/Y/Z; торкнувся опори — фіксується |
| Кубик стеку | tile | глибина (колір шару) | нерухомий; зникає з повним шаром |
| Шар (face) | zone | W×D клітин | повний → зникає, усе вище опускається на 1 |
| Набір FLAT | spawner | плоскі полікуби (≈ тетроміно + дрібні) | однокубові по висоті — «2D-тетріс у 3D» |
| Набір BASIC | spawner | 7 фігур куба Сома | плоскі й обʼємні фігури |
| Набір EXTENDED | spawner | 41 фігура: 1 моно-, 1 ди-, 2 три-, 8 тетра-, 29 пентакубів | усі полікуби до 5 |
| Кубики суперника (versus) | hazard | 1 рівень | твоя грань піднімає стек суперника на 1 рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(level_speed)` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)` (на шар углиб).
- КОЛИ `input(move_x|move_y)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)` у площині шару.
- КОЛИ `input(rotate_x|rotate_y|rotate_z)` → ЯКЩО `custom: «fits3d — повернута фігура в межах стакана й не перетинає кубиків»` → ТО `custom: «rotate3d — поворот на 90° навколо осі»`; інакше `block`.
- КОЛИ `input(drop)` → ТО `move(piece, lowest_free)`, `custom: «lock»`; очки за фігуру більші, якщо скинуто з високої позиції.
- КОЛИ `custom: «будь-яка клітина фігури торкнулась дна або кубика»` → ТО `custom: «lock — кубики фігури → стек»` (без lock delay (?)).
- КОЛИ `pattern(custom: «шар W×D повний»)` → ТО `clear(layer)`, `drop_rows` (усе вище на 1 шар униз).
- Рахунок: `score(+n)` за кожну фігуру (за таблицею рівня, більше при скиданні) і за грані; кілька граней однією фігурою — значно більше; таблиці BlockOut II — рівні 0–10.
- КОЛИ `after(clear)` → ЯКЩО `count(stack_cubes, ==, 0)` → ТО `score(block_out_bonus)` (BlockOut II: «flush» = бонус 2 лінії).
- КОЛИ `counter(faces, ≥, n)` → ТО `counter(level, +1)`, `speed(piece, ×k)` (ПК) · Mega Drive: `next_level` (раунд із новим стаканом і фігурами).
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose` (стек дійшов до верху стакана).
- Бонус-етап (Mega Drive): `timer(30 s)`, стакан 2×2; КОЛИ `timer(stage, ==, 0)` або переповнення → ТО `next_level` без поразки.
- Versus (Mega Drive): КОЛИ `after(clear)` у гравця → ТО `custom: «стек суперника піднімається на 1 рівень»`; раунд виграє той, хто першим набрав норму граней або «втопив» суперника; переможець серії продовжує соло.

## Керування і ввід
- ПК: клавіші-стрілки — зсув по двох осях; три пари клавіш (Q/W/E та A/S/D (?)) — поворот навколо X/Y/Z; пробіл — скидання.
- Mega Drive: хрестовина — зсув, три кнопки A/B/C — поворот по трьох осях, окрема дія — швидке скидання.
- Ментальна частина вводу: зсув «вгору/вниз» на екрані = глибина площини, не висота.

## Вікна, меню, HUD
- `main-menu`: Play · Setup · High scores · три рекомендовані пресети: Flat Fun (FLAT), 3D Mania (BASIC), Out of Control (EXTENDED).
- `settings-window` (Setup): ширина й глибина стакана (3–7), висота (6–18), набір фігур, стартова швидкість/рівень (0–10).
- `game-screen`: каркас стакана згори; `custom: «шкала глибини»` збоку з кольорами шарів, що показує висоту стеку; `score`, кубиків/граней, `level-number`, фігура-каркас.
- `end-screen` → `leaderboard` (окремий для кожної конфігурації (?)); BlockOut II — онлайн-таблиця з повторами (`replay-window`).
- Mega Drive: `custom: «екран раунду»` з нормою граней; `match-setup` для versus.

## Фічі поза полем
- `custom-rules` — 585 конфігурацій (стакан × набір × швидкість); `difficulty-presets` — 3 рекомендовані.
- `leaderboard-local`; BlockOut II — `leaderboard-online` з завантаженням повторів і виявленням підробних рахунків, статистика.
- Mega Drive: раунди з нормою граней, бонус-етап, `mode-versus` (`local-multiplayer`).
- BlockOut II — відкритий код (GPL), Windows/Linux, «майже ідентична» кінематика оригіналу.

## Варіації й родичі
- [tetris.md](tetris.md) — 2D-предок; набір FLAT робить з Blockout «тетріс на кількох площинах».
- [welltris.md](welltris.md) — Пажитнов відповів 2D-фігурами в 3D-колодязі (Wikipedia: натхнення Blockout).
- 3D Tetris (Virtual Boy), Tetrisphere — інші спроби «тетріс у 3D»; див. [tetrisphere.md](tetrisphere.md).
- **Осі варіацій**: фігури (полікуби 1–5 / Сома / плоскі) · обертання (2 осі / 3 осі) · очистка (повний шар / повний ряд у площині) · розмір стакана (фіксований / налаштовуваний / за раундом) · versus (без / підйом стеку).

## Цікавинки для курсу
- 3D-поле як масив `[z][y][x]` + очистка повного шару — 📎.
- Поворот полікуба на 90° навколо трьох осей з перевіркою колізій — 🥉 (матриці поворотів, нормалізація координат).
- Генерація всіх полікубів до 5 (41 вільна фігура) з відкиданням поворотних дублів — 🥇.
- Проєкція 3D-стакана на 2D-екран (вид згори, глибина кольором) — 🥈 у консолі, 🥉 у GUI.
- Конфігурація партії «стакан × набір × швидкість» з окремими рекордами — 🌱.

## Мапа на каталог
- Є: `gravity-fall`, `multi-cell-size`, `keyboard-controls`, `progress-acceleration`, `event-points`, `time-out` (бонус-етап 30 с), `score-records`, `leaderboard`, `difficulty-levels`, `field-size-picker` (стакан), `game-settings`, `replay` (BlockOut II), `simultaneous-versus` + `garbage-attack` (Mega Drive versus).
- **Нема** → пропозиції карток:
  - `+3d-polycube-rotation` «Поворот полікуба по трьох осях» · entities/legality · 🥉 · слот {axes: 3}.
  - `+layer-clear-3d` «Повний шар 3D-поля зникає» · entities/interact · 📎.
  - `+depth-gauge` «Шкала глибини кольорами» · interface/hud · 🌱.
  - `+drop-height-bonus` «Очки за висоту скидання» · game-logic/score · 🌱.
  - `+empty-pit-bonus` «Бонус за порожнє поле» · game-logic/score · 🌱.
  - `+piece-set-select` «Вибір набору фігур» · interface/settings · 🌱.

## Пропозиції до словників
- `+effect:rotate3d` — поворот обʼємної фігури на 90° навколо X/Y/Z (наявний `rotate` — лише в площині).
- `+cond:fits3d` — фігура в межах 3D-стакана й не перетинає кубиків (тривимірний `fits`).
- `+ui:depth-gauge` — колонка кольорів шарів і висоти стеку; `+ui:pit-wireframe` — каркас стінок для читання глибини.
- `+feature:pit-size` — розмір 3D-поля як налаштування; `+feature:piece-set` — набір фігур як налаштування; `+feature:online-replay-scores` — рекорд приймається разом із повтором (антиобман).
- `+card:3d-polycube-rotation` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Blockout](https://en.wikipedia.org/wiki/Blockout) — вид згори в 3D-стакан, полікуби, три кнопки повороту, фіксація від дотику, грань зникає, бонус «Block Out», раунди й бонус-етап 2×2/30 с, versus, розробники, платформи, BlockOut II.
- [BlockOut II](http://www.blockout.net/blockout2/) — ремейк з тією самою кінематикою, онлайн-рекорди з повторами, GPL.
- [BlockOut II: Scoring](http://www.blockout.net/blockout2/scoretable.php?set=0&width=5&height=5&depth=12) — набори FLAT/BASIC/EXTENDED, стакан 3–7 × 6–18, рівні 0–10, очки за фігуру більші при скиданні з висоти, порожній стакан = бонус 2 лінії.
- [HardDrop: Blockout](https://www.harddrop.com/wiki/Blockout) — стакан 5×5×12, без hold, налаштування.

## Непевне
- (?) Набір FLAT: «усі поліоміно до 4, крім прямої» (JammaPlay) vs «8 фігур, як тетроміно + L-трикуб і прямі 1–3» (Segaretro) — з результатів пошуку, сторінки не відкрито.
- (?) Пресети: 3D Mania — 3×3×10; Out of Control — 5×5×10 — з результатів пошуку; Flat Fun — 5×5×12.
- (?) Колір кубика за глибиною шару і шкала глибини — з памʼяті.
- (?) Розкладка ПК-клавіш для поворотів (Q/W/E, A/S/D) — з памʼяті.
- (?) Lock без затримки на ПК — Wikipedia описує Mega Drive; рекорди окремо за конфігурацією — з памʼяті.
- (?) Формула очок не опублікована — лише таблиці BlockOut II.
