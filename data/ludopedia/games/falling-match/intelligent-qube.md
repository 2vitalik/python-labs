---
title: "I.Q.: Intelligent Qube (Kurushi)"
slug: intelligent-qube
aka: [Kurushi, "I.Q インテリジェントキューブ", I.Q., "Kurushi Final: Mental Blocks", "I.Q. Final", "I.Q. Remix+", "I.Q. Mania"]
family: falling-match
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: score
year: 1997
platforms: [PlayStation, PS2 (Remix+), PSP (Mania), mobile (i-mode, EZweb), PS Classic, PS Plus Classics]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/I.Q.:_Intelligent_Qube", best: true, note: "EN: стадія, типи кубів, штрафи, block scale, perfect, бонуси за кількість перекочувань, очки, I.Q., режими Final"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/I.Q_インテリジェントキューブ", note: "JA: механіка мітки (синя → червона), зелена мітка 3×3 переходить у наступну задачу, «Again!», par-кроки, рейтинги PERFECT/GREAT/EXCELLENT, 9 стадій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Intelligent+Qube+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, explode-area, environment-death, player-death, event-points, score-records, sequential-levels, level-select, game-over-continue, character-select, in-game-editor, hot-seat, move-counter, remaining-counter, mode-select, +mark-then-trigger, +rolling-wave, +forbidden-tile-penalty, +shrinking-stage, +perfect-bonus, +par-count-bonus, +final-rating, +carry-over-mark, +unlockable-characters]
proposes: ["+effect:capture", "+trigger:crushed", "+ui:block-scale", "+ui:iq-rating", "+card:mark-then-trigger", "+card:rolling-wave", "+card:forbidden-tile-penalty", "+card:shrinking-stage"]
author: opus
date: 2026-11-09
---

# I.Q.: Intelligent Qube — ряди кубів котяться на тебе: познач клітину, захопи сірий, пропусти чорний

## Суть
Людина-аватар бігає по прямокутній платформі з клітин; з дальнього краю на неї хвилями котяться ряди кубів, перекочуючись на одну клітину за такт. Гравець ставить **мітку** на клітину під собою і, коли куб опиниться на ній, «спрацьовує» мітку — куб провалюється (захоплено). Сірі куби треба захопити, зелені при захопленні лишають мітку-бомбу на 3×3, а чорні захоплювати не можна — їх треба пропустити за край. Помилки (захоплені чорні, пропущені сірі) **вкорочують платформу** на ряд; коли під гравцем не лишається підлоги — кінець гри.

## Поле і час
- Платформа — прямокутна сітка (ширина 4 на першій стадії, 7 на фінальній); на старті рівня 23–30 рядів, з них піднімаються 12–16 (EN-вікі). Задній край — звідки приходять куби, передній — куди вони падають.
- Real-time з дискретним тактом котіння: куби хвилі перекочуються одночасно на одну клітину (`roll` через ребро); гравець бігає вільніше за такт (?).
- Хвиля (задача, 問題) — набір рядів кубів; 1–4 набори йдуть разом; після знищення набору піднімаються наступні — 4 «підйоми» на рівень (EN) / 4 раунди по 3 задачі (JA, оригінал).
- Оригінал — 9 стадій; пізніші довші й ширші; останню звуть FINAL.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (Eliot; відкривні — Cynthia/Cherry, пес Spike — швидші) | player | швидкість бігу | біг 4 напрямки по платформі; ставить / спрацьовує мітку під собою |
| Сірий куб (normal) | object | колір як у стадії | котиться до переднього краю; має бути захоплений; 100 очок |
| Зелений куб (advantage) | object | — | захоплений → лишає зелену мітку на своїй клітині |
| Чорний куб (forbidden) | hazard | — | треба пропустити за край; захоплений → мінус ряд, 0 очок, perfect неможливий |
| Синя мітка | mark | одна на полі | ставиться під гравцем; повторна постановка стирає попередню |
| Червона мітка | mark | — | слід спрацьованої мітки; рахується окремо від синьої — можна одразу ставити нову |
| Зелена мітка | mark | зона 3×3 | детонується окремою кнопкою: захоплює всі куби в 3×3; невикористана переходить у наступну задачу |
| Ряд платформи | terrain | — | підлога; втрачений ряд обвалюється з переднього краю |
| Block scale (шкала) | zone | ліміт = ширина − 1 (EN) / ширина (JA) | рахує пропущені сірі й зелені куби; переповнення → мінус ряд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ТО `roll(all_cubes_of_wave, toward_front)` — усі куби хвилі перекочуються на одну клітину.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; клітина з кубом — `block` (?).
- КОЛИ `input(mark)` → ЯКЩО `not occupied(blue_mark)` → ТО `mark(cell_under_player, blue)`; ЯКЩО синя мітка вже є → ТО `unmark(old)`, `mark(cell_under_player, blue)`.
- КОЛИ `input(mark)` → ЯКЩО `occupied(blue_mark_cell, cube)` → ТО `custom: «capture — куб провалюється в мітку»`, `mark(cell, red)`; сірий — `score(100)`.
- КОЛИ `custom: «захоплено зелений куб»` → ТО `mark(cell, green)`; КОЛИ `input(advantage)` → ТО `explode(square3x3, captured)` навколо зеленої мітки — кожен куб у зоні вдвічі дорожчий (200).
- КОЛИ `custom: «захоплено чорний куб»` → ТО `shrink(stage, 1)` (мінус ряд), `score(0)`, `clear_state(wave, perfect_possible)`.
- КОЛИ `edge(cube)` (куб скотився з переднього краю) → ЯКЩО `not same(cube, forbidden, kind)` → ТО `counter(block_scale, +1)`.
- КОЛИ `counter(block_scale, >, limit)` → ТО `shrink(stage, 1)`, `counter(block_scale, reset)`.
- КОЛИ `contact(cube, player)` (куб накотився на гравця) → ТО `stun(player, n)`, `custom: «решта кубів хвилі прискорено скочується; усі, включно з чорними, — у block scale»`, `message(Again!)`, повтор тієї ж задачі (крім останньої хвилі рівня).
- КОЛИ `all_gone(cube)` у хвилі → ЯКЩО `custom: «жодного чорного не захоплено, усі сірі й зелені захоплено»` → ТО `message(Perfect!)`, `score(bonus)`, `grow(stage, 1)` (ряд додається в кінець).
- КОЛИ `all_gone(cube)` у хвилі → ТО `custom: «порівняти кількість перекочувань від першого до останнього захоплення з par»`: рівно par / більше / менше — різні бонуси (оригінал EN: 5000 / 1000 / 10000; Final: 10000 / 2000 / 15000).
- КОЛИ `level_end` → ТО `score(rows_left × 1000)`.
- КОЛИ `custom: «під гравцем обвалився ряд»` або `edge(player)` (зіштовхнуто кубами за край) → ТО `lose` → `window(game-over-continue)`.
- КОЛИ `game_over` → ТО `custom: «I.Q. 0–999 як частка набраних очок»`, `window(end-screen)`.
- Перемога: пройти фінальну стадію · Поразка: впасти з платформи (обвал під ногами або виштовхнули) · Рахунок: 100 за куб, ×2 у зоні зеленої мітки, бонуси perfect і par, 1000 за ряд, що лишився; без continue — I.Q. ≥ 350, добра гра ≈ 1 млн очок.

## Керування і ввід
- Хрестовина — біг; кнопка мітки — поставити синю / спрацювати; окрема кнопка — детонувати зелену мітку. Конкретні кнопки PS1 у джерелах не названо (?).
- Прискорення котіння утриманням кнопки — (?): JA згадує «перемотку» лише як автоматичне скочування після розчавлення.
- Режим 2P — гравці по черзі (hot-seat), не одночасно.

## Вікна, меню, HUD
- `splash-screen` з диктором (Nakata Joji; у Final — Peter Barakan).
- `main-menu` → `mode-select`: гра · Original Mode (після першого проходження; редактор задач без підрахунку I.Q.) · 2P. У Kurushi Final: Kurushi Final · Tektonics · 100 Attack · Survival · Create.
- `character-select` — Eliot за замовчуванням, відкривні швидші персонажі.
- `game-screen`: 3D-перспектива платформи за спиною гравця; HUD — `score`, `custom: «block scale»` (сіра шкала пропущених кубів з поділками-лімітом), `custom: «лічильник перекочувань / par»` (`move-counter`, `par-moves`), номер стадії/хвилі, `popup-text` («Perfect!», «Again!», «Brilliant / Great / True Genius»).
- `end-screen` стадії: бонус за ряди, що лишились; фінальний екран з I.Q.
- `game-over-continue` — «продовжити?»; у Final — `level-select` будь-якої стадії до найдальшої пройденої (макс. 8-а).
- `editor-window` — Original Mode / Create.
- `pause-menu` (?).
- Переходи: splash → mode-select → character-select → game-screen (стадія) → end-screen стадії → наступна → … → фінальний I.Q.; падіння → game-over-continue.

## Фічі поза полем
- `levels-sequential` (9 стадій) + `continue`; у Final — `level-select` до найдальшої пройденої.
- `unlockables`: персонажі за кількаразове проходження; Original Mode після першого; Tektonics — за I.Q. ≥ 500 або 20+ хв Survival.
- `level-editor` (Original Mode / Create; у Create рахуються перекочування).
- `mode-endless` (Survival), `mode-puzzle` (100 Attack — 100 окремих задач на обмежену кількість перекочувань), Tektonics — одна велетенська задача на 20 хвиль.
- `difficulty-presets`-подібні швидкості 0–4 (повне проходження ≈ 2 год на 0, ≈ 75 хв на 4).
- `hotseat` для 2P.

## Варіації й родичі
- **I.Q. Final / Kurushi Final: Mental Blocks** (1998/1999) — 3 раунди на стадію, нові бонуси (GREAT/EXCELLENT), персонаж Abel, режими Tektonics / 100 Attack / Survival / Create, вибір стадії після game over.
- **I.Q. Remix+** (PS2, 2000) — додано програш за довге стояння на краю. **I.Q. Mania** (PSP, 2006) — задачі всіх трьох ігор.
- Родичі: Devil Dice (перекочування кубів аватаром — тут куби котяться самі), Bombliss / Bomberman (зона вибуху), Tetris (поле, що «вкорочується» помилками — навпаки до росту стека), Frogger (рухомі ряди проти аватара).
- **Осі варіацій**: хто рухає плитки (гравець / **хвиля сама**) · як прибирати (збіг / **мітка-пастка з відкладеним спрацюванням**) · штраф (стек росте / **поле коротшає**) · заборонені плитки (нема / **чорні — не чіпати**).

## Цікавинки для курсу
- Мітка-пастка: поставити → чекати, поки куб накотиться → спрацювати; одна активна мітка + окремий «слід» — 📎.
- Хвиля кубів, що синхронно перекочується, + розчавлення аватара — 🥉.
- Зелена мітка на 3×3 з перенесенням між задачами — 📎 (картка `explode-area` є).
- Поле, що коротшає від штрафів і росте за perfect: стан гри = довжина платформи — 🥉.
- Block scale: лічильник із порогом, що залежить від ширини стадії — 🌱.
- Par за кількістю перекочувань від першого до останнього захоплення: оптимізатор «коли ставити мітки» (пошук по часу) — 🥇.
- Фінальний «I.Q.» як нормований рейтинг замість очок — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` · `explode-area` (зелена мітка 3×3) · `environment-death` / `player-death` (впасти з платформи) · `event-points` · `score-records` · `sequential-levels` · `level-select` (Final) · `game-over-continue` · `character-select` · `in-game-editor` · `hot-seat` · `move-counter` · `remaining-counter` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+mark-then-trigger` «Мітка на клітині, спрацювання окремою дією» · entities/interact · 📎 · слот {max_marks: 1}.
  - `+rolling-wave` «Хвиля обʼєктів синхронно котиться на гравця» · entities/move · 🥉.
  - `+forbidden-tile-penalty` «Заборонена плитка: прибрати — штраф» · game-logic/score · 🌱.
  - `+shrinking-stage` «Поле коротшає від помилок і росте за бездоганність» · levels/state · 🥉.
  - `+perfect-bonus` «Бонус за бездоганну хвилю» · game-logic/score · 🌱.
  - `+par-count-bonus` «Бонус за точне / краще за par число тактів» · game-logic/score · 📎.
  - `+final-rating` «Підсумковий рейтинг (I.Q.) з очок» · game-logic/score · 🌱.
  - `+carry-over-mark` «Невикористаний бонус переходить у наступну задачу» · entities/state · 🌱.
  - `+unlockable-characters` · progression · 🌱.

## Пропозиції до словників
- `+effect:capture` — прибрати обʼєкт у клітині-пастці (куб провалюється в мітку); вже пропонована ×7 (шахи — інший зміст, куратору звести).
- `+trigger:crushed` — обʼєкт накотився/навалився на аватара (I.Q., Tetris Plus — стеля); відрізняється від `contact`, бо наслідок — ефект на аватара, а не взаємодія.
- `+ui:block-scale` — шкала пропущених плиток з поділкою-лімітом; `+ui:iq-rating` — підсумковий рейтинг.
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia EN: I.Q.: Intelligent Qube](https://en.wikipedia.org/wiki/I.Q.:_Intelligent_Qube) — стадія (23–30 рядів, 12–16 піднімаються, ширина 4…7), типи кубів, штрафи, block scale (ширина − 1), розчавлення, perfect + ряд, par-бонуси оригіналу і Final, 100/200 очок, 1000 за ряд, I.Q. 0–999, персонажі, Original Mode, режими Final, дати.
- [Wikipedia JA: I.Q インテリジェントキューブ](https://ja.wikipedia.org/wiki/I.Q_インテリジェントキューブ) — мітка синя → червона, повторна постановка стирає попередню, зелена мітка переходить у наступну задачу, «Again!», block meter, game over (обвал / виштовхнули / Remix+ — стояння на краю), par-кроки, 9 стадій × 4 раунди × 3 задачі, серія.
- YouTube: пошук «Intelligent Qube gameplay».

## Непевне
- (?) Ліміт block scale: EN — «ширина − 1» (3 на першій, 6 на фінальній), JA — «кожна ширина стадії пропущених кубів» — розходяться.
- (?) Рейтинги par: EN для оригіналу — рівно par 5000 «Brilliant», більше 1000 «Great», менше 10000 «True Genius»; JA — PERFECT/GREAT/EXCELLENT з іншими сумами; назви й суми залежать від версії.
- (?) EN: «чорний куб можна позначити без захоплення, якщо він у зоні зеленої мітки» — механіка не зрозуміла (чи 3×3 захоплює чорні).
- (?) Чи може гравець пройти крізь куб / стояти на ньому, кнопки керування, прискорення котіння кнопкою, швидкість бігу відносно такту.
- (?) Чи задачі в межах стадії фіксовані (дизайнені з par), чи випадкові з пулу — `random: none` поставлено за наявністю par на кожну задачу.
