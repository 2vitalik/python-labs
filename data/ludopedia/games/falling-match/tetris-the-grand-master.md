---
title: Tetris The Grand Master (TGM)
slug: tetris-the-grand-master
aka: [TGM, TGM1, "Tetris: The Grand Master", テトリス ザ・グランドマスター]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1998
platforms: [arcade]
links:
  - {kind: fandom, url: "https://tetris.wiki/Tetris_The_Grand_Master", best: true, note: "TetrisWiki: поле, лічильник рівня, таблиця гравітації до 20G, ARE/DAS/lock delay, формула очок і комбо, грейди 9…S9, умови GM, секретний грейд, приховані режими з кодами"}
  - {kind: fandom, url: "https://tetris.wiki/Arika_Rotation_System", note: "ARS: спавн плоскою стороною вгору, кік праворуч/ліворуч, I не кікає, правило центрального стовпчика"}
  - {kind: fandom, url: "https://tetris.wiki/TGM_randomizer", note: "історія з 4 фігур, ZZZZ на старті, 4 спроби, перша не S/Z/O; TGM2 — 6 спроб, TGM3 — мішок 35"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris:_The_Grand_Master", note: "серія: TGM2 Master/T.A. Death, TGM3 Shirase/Sakura, TGM4"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetris+the+grand+master+GM+20G+gameplay", note: "пошук; проходження до GM"}
stage: v1
coverage: 70
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, event-points, combo-multiplier, score-records, cheat-codes, attract-demo, game-screen, end-screen, splash-screen, +line-clear, +next-queue, +ghost-piece, +lock-delay, +srs-wall-kicks, +history-randomizer, +level-counter-gate, +grade-rank, +time-split-check, +initial-rotation]
proposes: ["+trigger:landed", "+cond:pattern_holes", "+effect:set_grade", "+card:history-randomizer", "+card:level-counter-gate", "+card:grade-rank", "+card:time-split-check", "+card:initial-rotation", "+feature:title-codes", "+ui:grade-display"]
author: opus
date: 2026-11-09
---

# Tetris The Grand Master — аркадний Tetris на швидкість: 20G, ARS, рівні 0–999 і грейд аж до Grand Master

## Суть
Та сама механіка рядів, що й у [Tetris](tetris.md), але інша філософія: мета — не рахунок до топ-ауту, а дійти до рівня 999 і отримати **грейд** (9 → 1 → S1…S9 → GM) за очками й контрольними часами. Гравітація росте нерівно й з рівня 500 стає 20G: фігура зʼявляється одразу на дні, і гра — це лише зсуви й повороти під час lock delay. Обертання ARS з простими кіками, IRS (поворот при появі), рандомайзер з історією замість мішка. Нема hold і hard drop, 1 next.

## Поле і час
- Колодязь 10 × 20 видимих + 1 буферний ряд (21-й); клітини, залочені вище, видаляються.
- Real-time, тік = кадр; гравітація = Internal Gravity / 256 рядів за кадр. Рівень 0 — 4/256; 251 — 1G; 300 — 2G; 400 — 5G; потім **спад** (420 — 4G, 450 — 3G), і з 500 — 20G (5120/256). На 200 гравітація падає знову до 4/256.
- Сталий хендлінг на всю гру: ARE 30 кадрів, DAS 16, lock delay 30, затримка зчищення 41 кадр.
- Шари: стек + активна фігура + TLS-тінь (лише до рівня 100) + 1 next.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура | player | тип I/O/T/S/Z/J/L, стан повороту, lock-таймер 30 кадрів | падає за гравітацією рівня; лочиться після lock delay або soft drop на землі |
| I | object | 4×1 | **ніколи не кікає** |
| T · J · L | object | 3×2, плоска довга сторона вгору при спавні | з 3-широких станів не кікають «від центрального стовпчика» |
| S · Z · O | object | — | кік праворуч, потім ліворуч; S/Z/O ніколи не перша фігура гри |
| Клітина стеку | tile | колір фігури (схема Sega) | зникає з повним рядом; клітина в 21-му ряду лишається прихованою |
| Next | spawner | 1 фігура | з рандомайзера історії |
| Рандомайзер | spawner | історія 4 фігур (старт ZZZZ), 4 спроби | тягне фігуру, якої нема в історії; після 4 невдач — бере останню спробу |
| TLS-тінь | — (ui `ghost-piece`) | лише рівні 0–100 | показує, куди впаде фігура |
| Грейд | — (ui) | 9 … 1, S1 … S9, GM | визначається очками; GM — очками й часом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(piece)` → ЯКЩО `not counter(level_mod_100, ==, 99) and not counter(level, ==, 998)` → ТО `counter(level, +1)` — рівень росте за кожну нову фігуру, але на x99 і 998 «стоїть», доки не зчистиш ряд.
- КОЛИ `spawned(piece)` → ЯКЩО `custom: «затиснуто кнопку повороту»` → ТО `rotate(piece, 90)` (IRS — фігура зʼявляється вже повернутою).
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `game_over` з поточним грейдом.
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)` × G рівня; при 20G — одразу до опори.
- КОЛИ `input(rotate_cw|rotate_ccw)` → ТО `rotate(piece, ±90)`; якщо зайнято → `custom: «kick — спершу на 1 праворуч, потім на 1 ліворуч; I не кікає; T/J/L не кікають, коли заважає клітина центрального стовпчика»`; жоден → `block`.
- КОЛИ `input(shift_left|shift_right)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`; утримання — автоповтор після DAS 16 кадрів (DAS можна заряджати під час ARE).
- КОЛИ `custom: «фігура на опорі»` → ТО `timer(start, 30)`; КОЛИ `timer(lock, ==, 0)` → ТО `custom: «lock»`; рух униз (падіння на нижчий ряд) перезапускає lock delay (step reset (?)).
- КОЛИ `input(soft_drop)` → ТО `move(piece, down)` прискорено, `counter(soft, +1)` за кожен кадр утримання; на опорі — миттєвий lock (+1 до soft).
- КОЛИ `locked(piece)` → ЯКЩО `pattern(row_full)` → ТО `clear(rows)`, `drop_rows`, `counter(level, +lines)`.
- Комбо: КОЛИ `locked(piece)` → ЯКЩО `count(cleared_lines, >, 0)` → ТО `counter(combo, combo + 2×lines − 2)`; інакше `counter(combo, =1)`.
- Очки: `score((⌈(level + lines) / 4⌉ + soft) × lines × combo × bravo)`; bravo = 4, якщо поле стало порожнім, інакше 1. Soft drop дає очки лише разом зі зчищенням.
- Грейд: КОЛИ `counter(score, >=, поріг)` → ТО `custom: «set_grade»`: 9 — 0 · 8 — 400 · 7 — 800 · 6 — 1400 · 5 — 2000 · 4 — 3500 · 3 — 5500 · 2 — 8000 · 1 — 12 000 · S1 — 16 000 · S2 — 22 000 · S3 — 30 000 · S4 — 40 000 · S5 — 52 000 · S6 — 66 000 · S7 — 82 000 · S8 — 100 000 · S9 — 120 000.
- КОЛИ `counter(level, >=, 300)` → ЯКЩО `counter(score, >=, 12000) and timer(<, 04:15:00)` → ТО `set_state(player, gm_track)`; інакше `clear_state(player, gm_track)`.
- КОЛИ `counter(level, >=, 500)` → ЯКЩО `state(player, gm_track) and counter(score, >=, 40000) and timer(<, 07:30:00)` → ТО `set_state(player, gm_track)`; інакше `clear_state`.
- КОЛИ `counter(level, >=, 999)` → ТО `game_over`; ЯКЩО `state(player, gm_track) and counter(score, >=, 126000) and timer(<, 13:30:00)` → ТО `custom: «set_grade GM»`.
- Секретний грейд: КОЛИ `game_over` (топ-аут) → ЯКЩО `custom: «дірки в стеку складають візерунок „>“»` → ТО `custom: «secret grade — від 9 за першу дірку до GM за 19 рядів»` (повідомлення лише від грейду 5).
- Поразка/кінець: топ-аут до 999 дає поточний грейд і його «mastering time» · Рахунок: очки → грейд, час → GM.

## Керування і ввід
- Аркадний джойстик: ←/→ — зсув, ↓ — soft drop / ручний lock, ↑ — нічого (hard drop нема); кнопки A і C — поворот проти годинникової, B — за годинниковою (?).
- IRS: затиснутий поворот під час ARE застосовується до появи наступної фігури.
- Коди на титульному екрані — послідовності напрямків і кнопок (див. «Фічі»).

## Вікна, меню, HUD
- `splash-screen` / `attract-demo` — аркадний титул і демонстрація.
- `game-screen`: колодязь 10×20, `next-piece-preview` (1), `custom: «grade-display»` поточного грейду і очки до наступного (?), `level-number` у форматі «поточний / сотня-межа» (?), `timer-elapsed`, `score`, `ghost-piece` до рівня 100.
- `end-screen`: грейд, mastering time; `leaderboard` — таблиця рекордів автомата (ігри з кодами не записуються).
- Переходи: titles → (кредит) game-screen → (999 або топ-аут) end-screen → leaderboard → titles.

## Фічі поза полем
- `custom: «title-codes»` (`cheat-codes`): 20G Mode `DDDDDDDDCBA` · Big Mode `LLLLDCBA` (фігури подвійного розміру ≈ поле 5×10) · Rev Mode `DUUDCBA` (фігури спавняться внизу й летять угору) · Mono Mode `RRRUCBA` (усі одного кольору) · TLS Mode `ABCCBAACB` (тінь усю гру) · Uki Mode (дитячий голос замість звуку зчищення); коди комбінуються.
- `leaderboard-local` на автоматі; `custom: «grade-rank»` як прогресія майстерності; `operator-settings` (?).

## Варіації й родичі
- TGM2 / TAP (2000): Master (жорсткіші умови M/GM, після M — кредити з **невидимими** фігурами після локу), Normal, Versus з предметами, кооп на двох; TGM2+ — TGM+ (сміття росте знизу) і T.A. Death (старт з 20G, усе прискорюється).
- TGM3 Terror-Instinct (2005): Easy, Sakura (пазли), Master, Shirase (ще швидше, сміття, рівні понад 999); World/Classic правила; мішок 35 фігур; floor kicks (I — раз, T — двічі). TGM Ace (2005, Xbox 360), TGM4 Absolute Eye (2025).
- Родичі: [Tetris](tetris.md) (Guideline: SRS, 7-bag, hold, hard drop, T-spin), Sega Tetris (1988 — джерело повороту й кольорів).
- **Осі варіацій**: крива гравітації (плавна / зі спадами / одразу 20G) · хендлінг (сталий / прискорюється — T.A. Death) · рандомайзер (історія 4 × 4 спроби / × 6 / мішок 35) · кік (нема / 2 тести / floor kick) · мета (рахунок / рівень 999 + грейд / час) · видимість (тінь до 100 / завжди / невидимі фігури в кредитах).

## Цікавинки для курсу
- Лічильник рівня, що росте за спавн і зупиняється на x99 до зчищення — 🌱.
- Рандомайзер з історією 4 і обмеженою кількістю спроб, перша фігура не S/Z/O — 🌱.
- ARS-кік (праворуч, потім ліворуч) і правило центрального стовпчика для T/J/L — 📎.
- 20G: фігура спавниться на дні, гра — лише зсуви під lock delay (DAS, ARE як параметри) — 📎.
- Формула очок з комбо і bravo + таблиця грейдів — 📎.
- Контрольні точки GM (рівень 300/500/999 × очки × час) — 🥉 (стан «ще на треку GM»).
- Секретний грейд за візерунком дірок «>» — 🥉; невидимі фігури в кредитах (TGM2) — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` · `keyboard-controls` · `progress-acceleration` (крива G) · `event-points` (формула) · `combo-multiplier` · `score-records` · `cheat-codes` (коди режимів) · `attract-demo` · `game-screen` · `end-screen` · `splash-screen`.
- Уже запропоновані Tetris-ом: `+line-clear`, `+next-queue`, `+ghost-piece` (тут — лише до рівня 100), `+lock-delay`, `+srs-wall-kicks` (слот table: ars).
- **Нема** → пропозиції карток:
  - `+history-randomizer` «Рандомайзер з історією» · levels/generation · 🌱 · слоти {history: 4, tries: 4|6, first_not: [S, Z, O]}.
  - `+level-counter-gate` «Рівень росте за дії, але стоїть на межі до умови» · game-logic/waves · 🌱.
  - `+grade-rank` «Грейд за порогами очок» · game-logic/score · 🌱 · слот {table}.
  - `+time-split-check` «Контрольні точки часу для вищої нагороди» · game-logic/score · 🥉.
  - `+initial-rotation` «IRS — поворот, затиснутий до появи» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:landed` — фігура торкнулась опори (старт lock delay; уже просив Tetris).
- `+cond:pattern_holes` — дірки в стеку утворюють заданий візерунок (секретний грейд TGM).
- `+effect:set_grade` — присвоїти гравцеві ранг/грейд за таблицею.
- `+feature:title-codes` — режими, що вмикаються кодом на титульному екрані, і не пишуться в рекорди.
- `+ui:grade-display` — поточний грейд і поріг до наступного.
- Вжито вже наявні `locked`, `spawned`, `counter`, `timer`, `drop_rows`, `ghost-piece`, `cheat-codes`.

## Джерела
- ⭐ [TetrisWiki: Tetris The Grand Master](https://tetris.wiki/Tetris_The_Grand_Master) — поле 10×20+1, лічильник рівня, таблиця Internal Gravity, ARE/DAS/lock/line clear, формули очок і комбо, грейди, GM, секретний грейд, коди режимів.
- [TetrisWiki: Arika Rotation System](https://tetris.wiki/Arika_Rotation_System) — кік праворуч→ліворуч, I без кіків, центральний стовпчик, floor kicks TGM3.
- [TetrisWiki: TGM randomizer](https://tetris.wiki/TGM_randomizer) — історія 4, ZZZZ, 4 спроби, перша не S/Z/O; TGM2 6 спроб; TGM3 мішок 35.
- [Wikipedia: Tetris: The Grand Master](https://en.wikipedia.org/wiki/Tetris:_The_Grand_Master) — серія, TGM2 невидимі кредити, T.A. Death, TGM3 режими, TGM4.

## Непевне
- (?) Розкладка кнопок A/B/C → напрям повороту — з памʼяті.
- (?) Lock delay скидається лише при спуску на нижчий ряд (step reset) — TetrisWiki лише каже «lock delay 30 кадрів».
- (?) Що робить рандомайзер після 4 невдалих спроб (бере останню) — сторінка це не цитувала прямо.
- (?) Вигляд HUD (поріг наступного грейду, формат рівня «x/100») і наявність кредитів у TGM1 — не звірено.
- (?) Uki Mode код `ABABABABABABABABB` — у джерелі є, але не перевірено на автоматі; `operator-settings` для TGM — з памʼяті.
