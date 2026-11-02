---
title: Tetris (Тетрис, Tetris Guideline)
slug: tetris
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
year: 1985
platforms: [Elektronika 60, PC, NES, Game Boy, Switch, PS4, mobile, web]
links:
  - {kind: fandom, url: "https://tetris.wiki/Tetris_Guideline", best: true, note: "TetrisWiki — повний перелік вимог Guideline: поле, спавн, кольори, 7-bag, SRS, hold, ghost, lock down, керування, режими"}
  - {kind: fandom, url: "https://tetris.wiki/Super_Rotation_System", note: "SRS: стани 0/R/2/L, таблиці кіків"}
  - {kind: fandom, url: "https://tetris.wiki/Scoring", note: "таблиця очок Guideline, B2B, комбо, perfect clear"}
  - {kind: fandom, url: "https://tetris.wiki/Garbage", note: "таблиця сміття у versus, offset"}
  - {kind: fandom, url: "https://tetris.wiki/T-Spin", note: "правило трьох кутів, mini vs proper"}
  - {kind: fandom, url: "https://tetris.wiki/Marathon", note: "fixed/variable goal, крива гравітації"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris", note: "історія, Пажитнов, версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_99", note: "battle royale на 99, таргетинг, бейджі"}
  - {kind: play, url: "https://play.tetris.com/", note: "офіційна браузерна версія (tetris.com); боту віддає 403"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Tetris+Effect", note: "пошук; Tetris Effect: Connected"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetris+guideline+sprint+40+lines+gameplay", note: "пошук; геймплей Sprint"}
stage: v2
coverage: 70
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, progress-acceleration, event-points, combo-multiplier, score-records, leaderboard, time-out, game-pause, end-screen, controls-remap, ai-opponent, +srs-wall-kicks, +bag-randomizer, +hold-piece, +next-queue, +ghost-piece, +lock-delay, +hard-drop, +line-clear, +t-spin-detection, +back-to-back, +garbage-attack, +garbage-offset]
proposes: ["+trigger:landed", "+trigger:locked", "+cond:last_move", "+cond:corners_occupied", "+cond:difficult", "+effect:lock", "+effect:kick", "+effect:send_garbage", "+effect:offset_garbage", "+effect:hold_swap", "+feature:handling-settings", "+feature:mode-sprint", "+feature:mode-ultra", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# Tetris — керуй падаючою фігурою з 4 клітин, щоб заповнювати й зчищати повні ряди

## Суть
Тетроміно (одна з 7 фігур із 4 клітин) падає в колодязь 10×20; гравець зсуває й обертає його, доки фігура не «залочиться», після чого повні ряди зникають, а все вище осідає. Ядро — нескінченна черга фігур, що прискорюється, і рішення «куди покласти зараз, щоб не зіпсувати стек». Сучасний **Tetris Guideline** (стандарт The Tetris Company) додає точну інженерію: 7-bag, SRS з кіками, hold, ghost, черга next, lock delay, T-spin, back-to-back, комбо і сміття у versus. Клас `avatar` умовний: керуєш однією сутністю, але щоразу новою.

## Поле і час
- Матриця 10 стовпців × 20 видимих рядів + **буфер 20 рядів зверху** (схований; ряд 21 показують смужкою). Фігури спавняться в рядах 21–22, по центру (з округленням ліворуч), пласкою стороною донизу, і одразу падають.
- Два шари: «стек» (залочені клітини, лише колір, без звʼязку з фігурою) + активна фігура (4 клітини, позиція, стан повороту 0/R/2/L) + ghost (тінь, не взаємодіє).
- Real-time, тік = кадр (60 Гц). Гравітація в G (клітин за кадр): рівень 1 ≈ 1/60 G, рівень 15 ≈ 2.36 G, рівень 19 ≈ 20G (фігура зʼявляється одразу на дні); вище 19 — без єдиного правила. Час падіння на ряд: `(0.8 − (level−1)·0.007)^(level−1)` с (крива Tetris Worlds).
- Хендлінг (рекомендації Guideline при 60 FPS): DAS 10 кадрів (~167 мс затримки автоповтору), ARR 2 кадри, ARE 6 кадрів (пауза між лоченням і спавном).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура | player | тип I/O/T/S/Z/J/L, стан 0/R/2/L, lock-таймер, лічильник ресетів | падає за гравітацією; ввід зсуває/обертає/скидає; лочиться → стає клітинами стеку |
| I (світло-синя) | object | 4×1 | власна таблиця кіків SRS |
| O (жовта) | object | 2×2 | не кікає; поворот візуально нічого не змінює |
| T (пурпурова) | object | 3×2 з «носиком» | єдина, що дає T-spin |
| S (зелена) · Z (червона) | object | 3×2 | спільна таблиця кіків J/L/S/T/Z |
| J (темно-синя) · L (помаранчева) | object | 3×2 | спільна таблиця кіків J/L/S/T/Z |
| Клітина стеку | tile | колір фігури | нерухома; зникає лише з повним рядом; осідає на висоту зчищених рядів під нею (без «вільного падіння») |
| Ghost | — (ui `ghost-piece`) | — | проєкція активної фігури на місце, куди впаде; не блокує |
| Hold-слот | container | 1 фігура, прапорець «вже використано» | обмін з активною раз на фігуру |
| Черга next | spawner | 1–6 видимих фігур | з неї бере спавн; наповнюється 7-bag |
| Мішок 7-bag | spawner | перестановка 7 фігур | роздає по одній; порожній → нова перемішана сімка |
| Сміттєвий ряд (versus) | hazard | сірий, з діркою (розклад дірок — за грою) | виштовхує стек угору знизу; зчищається як звичайний ряд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose` (block out).
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)` з темпом гравітації рівня; інакше `custom: «запустити lock-таймер 0.5 с»`.
- КОЛИ `input(shift_left|shift_right)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`; утримання → автоповтор після DAS кожні ARR кадрів.
- КОЛИ `input(rotate_cw|rotate_ccw)` → ТО `rotate(piece, ±90)` і `custom: «kick — перевірити до 5 зсувів SRS по черзі, взяти перший вільний; жоден → поворот не відбувся»`. Для J/L/S/T/Z, 0→R: `(0,0) (−1,0) (−1,+1) (0,−2) (−1,−2)`; I має власну таблицю; O не кікає. Кожен поворот оборотний.
- КОЛИ `input(soft_drop)` → ТО `move(piece, down)` прискорено (множник — за грою), `score(+1/клітина)`; не лочить.
- КОЛИ `input(hard_drop)` → ТО `move(piece, ghost_pos)`, `score(+2/клітина)`, `custom: «lock — миттєво»`.
- КОЛИ `input(hold)` → ЯКЩО `not state(hold, used)` → ТО `custom: «hold_swap — активна в слот, з слота (або з черги) нова фігура згори»`, `set_state(hold, used)`; знімається при наступному локу.
- Lock down (move reset): КОЛИ `input(move|rotate)` → ЯКЩО `state(piece, on_ground) and counter(resets, <, 15)` → ТО `timer(reset)`, `counter(resets, +1)`; спуск нижче за найнижчий досягнутий ряд обнуляє лічильник. Альтернативи: infinity (без ліміту) і step reset (лише при спуску).
- КОЛИ `timer(lock, ==, 0)` → ТО `custom: «lock — клітини фігури → стек»`, далі перевірка рядів, `spawn_at(next, spawn)` після ARE.
- КОЛИ `after(custom: «lock»)` → ЯКЩО `custom: «last_move == rotate»` і piece == T і `custom: «≥3 з 4 діагональних кутів зайнято»` → ТО `custom: «T-spin: обидва передні кути → proper; один передній + обидва задні → mini; кік зі зсувом (1, 2) підвищує mini до proper»`; стіна/підлога рахуються зайнятими.
- КОЛИ `pattern(row_full)` → ТО `clear(rows)`, `drop_rows` (наївна гравітація: усе вище опускається на кількість зчищених рядів під ним, порожнини лишаються).
- Рахунок (× рівень до зчищення): Single 100 · Double 300 · Triple 500 · Tetris 800 · T-spin без рядів 400 · mini T-spin 100 · mini T-spin Single 200 · mini T-spin Double 400 (де є) · T-spin Single 800 · T-spin Double 1200 · T-spin Triple 1600.
- КОЛИ `after(custom: «lock»)` → ЯКЩО `custom: «difficult clear»` (Tetris або будь-який T-spin з рядами, зокрема mini) і `state(player, b2b)` → ТО `multiplier(×1.5)` (без очок за drop); Single/Double/Triple без спіна знімають B2B; T-spin без рядів — не знімає.
- КОЛИ `after(custom: «lock»)` → ЯКЩО `count(cleared_rows, >, 0)` → ТО `combo(+1)`, `score(50 × combo × level)`; інакше `reset_combo`.
- КОЛИ `after(clear)` → ЯКЩО `count(stack_cells, ==, 0)` → ТО `score(perfect_clear)`: 800/1200/1800/2000 × level за 1/2/3/4 ряди, B2B Tetris PC — 3200 × level (додається до звичайних очок).
- КОЛИ `counter(lines, ≥, goal)` → ТО `counter(level, +1)`, `speed(gravity, curve(level))`. Fixed goal (стандарт з ~2010): 10 рядів на рівень, стеля 15 (150 рядів) або нескінченно; variable goal (застарілий): 5×level «очок цілі».
- Поразка (top out): спавн перекривається зі стеком (block out) · фігура залочилась повністю над видимим полем (lock out) · сміття виштовхнуло клітину вище 20-рядного буфера.
- Versus: КОЛИ `after(custom: «lock»)` → ЯКЩО `count(cleared_rows, >, 0)` → ТО `custom: «send_garbage»`: Single 0 · Double 1 · Triple 2 · Tetris 4 · T-spin Single 2 · T-spin Double 4 · T-spin Triple 6 · mini TSS 0 · mini TSD 1 · perfect clear 10 (+ за тип очистки); B2B: +1 (mini TSS/TSD, TSS), +2 (TSD, Tetris), +3 (TST); комбо — дод. рядки (таблиця залежить від гри).
- КОЛИ `after(custom: «send_garbage»)` → ЯКЩО `count(incoming_queue, >, 0)` → ТО `custom: «offset — спершу гасить чергу вхідного сміття, залишок летить супернику»`.
- КОЛИ `after(custom: «lock»)` → ЯКЩО `count(cleared_rows, ==, 0)` і `count(incoming_queue, >, 0)` → ТО `spawn_at(garbage_rows, bottom)`, стек зсувається вгору.
- Tetris 99: перемога — останній живий з 99; КОЛИ `died(opponent)` через твоє сміття → ТО `custom: «KO → частинка бейджа»`; бейджі `multiplier(attack, до +100%)`.

## Керування і ввід
- Клавіатура (Guideline): ←/→ — зсув (DAS/ARR), ↑ — поворот за годинниковою, Z/Ctrl — проти, ↓ — soft drop, Space — hard drop, C/Shift — hold, Esc/F1 — пауза.
- Геймпад: D-pad вгору — hard drop, вниз — soft drop, ліво/право — зсув; праві/ліві кнопки — поворот CW/CCW, плечові — hold.
- Необовʼязкові: 180°-поворот (у частині ігор), IRS/IHS — затиснутий поворот/hold під час ARE застосовується до наступної фігури.
- Tetris 99: ручний вибір цілі або стратегія автотаргету: випадкові · хто атакує мене · майже мертві (KO) · власники бейджів; розкладка кнопок для цього — див. «Непевне».

## Вікна, меню, HUD
- `splash-screen` — логотип Tetris (обовʼязковий за Guideline), музика «Коробейники».
- `main-menu` → `mode-select`: Marathon · Sprint (40 Lines) · Ultra · Versus/Online · Options; стартовий рівень обирається.
- `game-screen`: матриця 10×20 із ghost; праворуч або згори `next-piece-preview` (к-сть Guideline не фіксує, часто до 6, у стартовій орієнтації); ліворуч `hold-slot` (затемнений, якщо використано); `score`, `level-number`, лічильник рядів, `timer-elapsed` (Sprint) або `timer-countdown` (Ultra); `action-text` назви дії («T-SPIN DOUBLE», «BACK-TO-BACK», «4 COMBO», «PERFECT CLEAR»).
- Versus: `garbage-meter` — стовпчик вхідного сміття біля поля; Tetris 99 — 98 міні-полів суперників довкола (`opponent-boards`), лінії атаки, лічильник KO і бейджів, гравців лишилось (`remaining-counter`).
- `pause-menu`: Продовжити · Рестарт · Вихід (`confirm-dialog`).
- `end-screen`: Game Over / результат (очки, ряди, час, к-сть Tetris/T-spin, PPS у сучасних); `leaderboard` для Marathon/Sprint/Ultra.
- `settings-window`: керування (`controls-remap`), хендлінг DAS/ARR/SDF, ghost вкл/вимк, к-сть next, режим lock (у частині ігор), звук/музика.
- Переходи: splash → main-menu → mode-select → game-screen → (top out / ціль) end-screen → leaderboard / main-menu.

## Фічі поза полем
- Режими: `mode-marathon` (150 рядів або ендлес), `custom: «Sprint»` (40 рядів на час), `custom: «Ultra»` (2–3 хв на очки), `mode-versus`, `online-multiplayer` (Tetris 99 — battle royale), `ai-opponent-levels` (CPU у Puyo Puyo Tetris та ін.), `mode-zen` (Tetris Effect).
- `leaderboard-local` / `leaderboard-online`, `stats` (PPS, APM), `replay` (Tetris Effect, TETR.IO).
- `custom-difficulty` — стартовий рівень; `custom: «handling-settings»` DAS/ARR/SDF — налаштування «відчуття» керування, характерне для сімʼї.
- `pause`; Guideline вимагає Korobeiniki; `music-toggle`, `volume-sliders`.
- Tetris 99: тематичні події Maximus Cup; `xp-level` гравця після матчу (?).

## Варіації й родичі
- Класичний Tetris NES (1989): без hold, ghost, кіків, лише 1 next, нема lock delay, рандомайзер з повтором — «до-Guideline» база; рівень 29 довго вважали непрохідним через швидкість («kill screen»). Hold зʼявився в The New Tetris (1999).
- TGM (Arika, 1998): ARS-поворот + IRS, 20G, історичний рандомайзер (?), грейд 9…S9 за очками, GM — за часом — інша філософія швидкості.
- Puyo Puyo Tetris — дві гри в одній партії; TETR.IO / Jstris — онлайн-клони з налаштовуваним хендлінгом.
- Hatris (1990, капелюхи), Welltris (1990, колодязь із 4 стінками), Blockout (3D), Tetris Effect (Zone (?): зупинка часу, ряди складаються донизу).
- **Осі варіацій**: рандомайзер (чистий random / історичний / 7-bag / 35-bag TGM3 / 63-bag The New Tetris) · поворот (без кіків / ARS / SRS) · lock (миттєвий / step / move reset 15 / infinity) · гравітація після очистки (наївна / «sticky» — кластери падають / «cascade» — кожна клітина падає) · попередній перегляд (0 / 1 / 6) · сміття (нема / дірка в одному стовпці / рандом) · фігури (тетроміно / пентаміно / 3D).

## Цікавинки для курсу
- 7-bag рандомайзер замість `random.choice` — 🌱; гарантія «I не пізніше 12 фігур» як тест — 📎.
- Ghost-фігура: та сама перевірка колізій, що й hard drop — 🌱.
- Hold з блокуванням до локу — 📎 (стан «використано»).
- Lock delay з move reset і лімітом 15 — 🥉 (таймер + лічильник + найнижчий ряд; легко зламати «вічну» фігуру).
- SRS з таблицею кіків як даними — 🥈 (5 тестів × 8 переходів × 2 таблиці, оборотність повороту).
- Детектор T-spin за трьома кутами + mini/proper + B2B/комбо — 🥈 (історія останнього руху, підрахунок кутів, стан серії).
- Versus із сміттям, offset і чергою вхідних рядів (проти AI-бота) — 🥇.

## Мапа на каталог
- Є: `gravity-fall` (падіння фігури) · `multi-cell-size` (фігура з 4 клітин) · `keyboard-controls` + `controls-remap` · `progress-acceleration` (гравітація з рівнем) · `event-points` (таблиця очок) · `combo-multiplier` (комбо, B2B) · `score-records` + `leaderboard` · `time-out` (Ultra) · `game-pause` · `end-screen` · `ai-opponent` (versus CPU).
- **Нема** → пропозиції карток:
  - `+srs-wall-kicks` «Поворот із кіками» · entities/legality · 🥈 · слоти {table: srs|none|ars, tests: 5}.
  - `+bag-randomizer` «Мішковий рандомайзер» · levels/generation · 🌱 · слот {bag_size: 7|14|35}.
  - `+hold-piece` «Відкласти фігуру» · entities/state · 📎.
  - `+next-queue` «Черга наступних» · interface/hud · 🌱 · слот {size: 1..6}.
  - `+ghost-piece` «Тінь падіння» · interface/hud · 🌱.
  - `+lock-delay` «Затримка фіксації» · entities/state · 🥉 · слоти {delay, mode: step|move|infinity, max_resets}.
  - `+hard-drop` «Миттєве скидання» · interface/input · 🌱.
  - `+line-clear` «Зчищення повних рядів з осіданням» · game-logic/score · 📎 · слот {gravity: naive|sticky|cascade}.
  - `+t-spin-detection` «Детектор T-spin» · game-logic/score · 🥈.
  - `+back-to-back` «Серія складних дій» · game-logic/score · 📎.
  - `+garbage-attack` «Сміття супернику» · game-logic/opponent · 🥉 · слот {table}.
  - `+garbage-offset` «Гасіння вхідного сміття» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+trigger:landed` — фігура торкнулась опори (старт lock-таймера); `+trigger:locked` — фігура зафіксована в стеку (точка підрахунку рядів, спінів, сміття).
- `+cond:last_move` — останній успішний ввід був певного типу (поворот → T-spin); `+cond:corners_occupied` — скільки діагональних кутів зайнято.
- `+effect:lock` — перетворити активну фігуру на клітини поля; `+effect:kick` — спроба набору зсувів при повороті; `+effect:send_garbage` — додати ряди в чергу суперника; `+effect:offset_garbage` — гасіння вхідної черги; `+effect:hold_swap` — обмін зі слотом.
- `+cond:difficult` — дія належить до «складних» (Tetris, T-spin з рядами) — основа B2B.
- Вжито вже наявні `garbage-meter`, `opponent-boards`, `action-text`, `ghost-piece`, `hold-slot`, `mode-select` — ще одна гра для правила трьох.
- `+feature:handling-settings` — DAS/ARR/SDF як налаштування; `+feature:mode-sprint` — N рядів на час; `+feature:mode-ultra` — макс. очок за фіксований час.
- `+axis:gravity` — `naive | sticky | cascade` — як осідають клітини після зчищення (Tetris / Tetris sticky / Puyo, Dr. Mario).

## Джерела
- ⭐ [TetrisWiki: Tetris Guideline](https://tetris.wiki/Tetris_Guideline) — поле, спавн, кольори, 7-bag, SRS, hold, next, ghost, lock down, керування, рекомендовані DAS/ARR/ARE, режими.
- [TetrisWiki: SRS](https://tetris.wiki/Super_Rotation_System) — стани й 5 тестів кіків.
- [TetrisWiki: Scoring](https://tetris.wiki/Scoring) — повна таблиця очок, B2B ×1.5, комбо 50×n, perfect clear.
- [TetrisWiki: T-Spin](https://tetris.wiki/T-Spin) — правило трьох кутів, mini/proper, виняток кіка.
- [TetrisWiki: Garbage](https://tetris.wiki/Garbage) — таблиця атаки, B2B-бонус, offset, черга.
- [TetrisWiki: Random Generator](https://tetris.wiki/Random_Generator) — 7-bag, макс. 12 між I, макс. 4 S/Z підряд, варіанти 35-bag/63-bag.
- [TetrisWiki: Marathon](https://tetris.wiki/Marathon) · [Ultra](https://tetris.wiki/Ultra) · [40 lines](https://tetris.wiki/40_lines) — режими, крива гравітації.
- [Wikipedia: Tetris](https://en.wikipedia.org/wiki/Tetris) — історія (1985, Пажитнов, Electronika 60), версії.
- [Wikipedia: Tetris 99](https://en.wikipedia.org/wiki/Tetris_99) — 99 гравців, 4 стратегії таргету, бейджі до +100%.
- [play.tetris.com](https://play.tetris.com/) — офіційна браузерна версія.

## Непевне
- (?) Таблиця сміття за комбо — у різних Guideline-іграх своя; TetrisWiki її не дає.
- (?) Розкладка hold на геймпаді (плечові кнопки) і 180°-поворот — з памʼяті, Guideline їх не фіксує.
- (?) Швидкість soft drop (часто згадують ×20 гравітації) — не звірено.
- (?) Форма сміттєвого ряду (одна дірка в стовпці) — TetrisWiki каже лише «ряди з дірками, розклад за грою».
- (?) TGM: рандомайзер з історією 4 останніх фігур — сторінка TGM лише посилається на окрему статтю.
- (?) Tetris 99: ручний таргет правим стіком, XP-рівень — з памʼяті; Wikipedia підтверджує лише 4 стратегії й бейджі до +100%.
- (?) Tetris Effect Zone — з памʼяті.
- (?) Esc/F1 — пауза в розкладці Guideline — з памʼяті.
