---
title: Klax
slug: klax
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1990
platforms: [arcade, Amiga, Atari ST, C64, ZX Spectrum, MS-DOS, NES, Genesis, Game Boy, Lynx, PlayStation, GameCube]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Klax_(video_game)", best: true, note: "конвеєр, лопатка на 5, колодязь 5×5, Klax по 3 у будь-якому напрямку, 100 хвиль, drop meter, вибір хвилі"}
  - {kind: other, url: "https://www.arcade-museum.com/game_detail.php?game_id=8266", note: "Killer List of Videogames — аркадна плата, флаєри"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/0002707", note: "порт ZX Spectrum, інструкція"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Klax", note: "пошук; Klax у збірках Atari/Midway"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=klax+arcade+gameplay", note: "пошук; аркадний геймплей"}
stage: v1
coverage: 70
mechanics: [row-conveyor, inventory-limit, keyboard-controls, gravity-fall, collect-quota, event-points, combo-multiplier, time-bonus, progress-acceleration, sequential-levels, level-select, score-records, game-pause, end-screen, +line-match-clear, +chain-reaction, +conveyor-catch, +lifo-hand, +miss-meter, +wave-goal, +warp-choice, +flip-back]
proposes: ["+trigger:edge", "+trigger:pattern", "+trigger:counter", "+effect:catch", "+effect:place", "+effect:flip_back", "+cond:free", "+role:supply", "+ui:drop-meter", "+ui:objective-text", "+window:wave-select", "+axis:control"]
author: opus
date: 2026-11-02
---

# Klax — лови плитки з конвеєра лопаткою й скидай у колодязь 5×5, складаючи трійки в ряд, стовпець і діагональ

## Суть
Кольорові плитки перекочуються по похилому конвеєру до гравця; він рухає лопатку (paddle) під кінцем конвеєра, ловить їх у стопку до 5 штук і скидає верхню у колодязь 5×5. Три однакові в ряд — горизонтально, вертикально чи по діагоналі — це **Klax**: плитки зникають, верхні осідають і можуть скласти новий Klax. Ядро — **два буфери з різною дисципліною**: стопка на лопатці (LIFO, ліміт 5) і колодязь (обмежений, з гравітацією), плюс тиск часу конвеєра. Кожна хвиля має свою ціль («N Klax», «N діагоналей», «N очок», «витримати N плиток»).

## Поле і час
- Три зони, по 5 смуг/стовпців: **конвеєр** (5 доріжок, плитки рухаються до гравця, перекидаючись) → **лопатка** (одна з 5 позицій, стопка до 5) → **колодязь** 5 стовпців × 5 рядів.
- Камера фіксована, вид у перспективі (конвеєр іде «вглиб»); колодязь — звичайна квадратна сітка.
- Real-time: плитки зʼявляються в дальньому кінці випадкових доріжок і рухаються з темпом хвилі; ввід — будь-коли. Колодязь сам по собі статичний, змінюється лише скиданням і зчищенням.
- 100 хвиль = 20 груп по 5; темп і різноманіття кольорів ростуть із хвилею (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лопатка (paddle) | player | позиція 1–5, стопка ≤ 5 | рух ліворуч/праворуч; ловить плитку, що дійшла до краю конвеєра в її смузі |
| Плитка на конвеєрі | object | колір, смуга, позиція | рухається до гравця; не спіймана → падає в прірву (drop) |
| Плитка в стопці | object | колір | лише верхню можна скинути чи підкинути назад |
| Плитка в колодязі | tile | колір | падає до опори; бере участь у Klax 3+ у 8 напрямках |
| Миготлива плитка (wild) | tile | — | (?) підходить до будь-якого кольору в Klax |
| Колодязь (bin) | zone | 5×5 | повний стовпець не приймає плитку; повний увесь — поразка |
| Drop meter | zone | дозволено N промахів | +1 за кожну втрачену плитку; заповнений → поразка |
| Генератор плиток | spawner | темп хвилі, палітра | породжує плитки на випадкових доріжках конвеєра |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(spawn_rate)` → ТО `spawn_at(tile, far_end(random_lane))`.
- КОЛИ `tick` → ТО `move(tile, toward_player)`; `input(down)` → `speed(tiles, ×k)` (прискорити конвеєр).
- КОЛИ `reach(tile, conveyor_end)` → ЯКЩО `facing(paddle, lane) and count(paddle_stack, <, 5)` → ТО `custom: «catch — плитка лягає на верх стопки»`; інакше `custom: «drop — плитка падає в прірву»`, `counter(drops, +1)`.
- КОЛИ `input(up)` → ЯКЩО `count(paddle_stack, >, 0)` → ТО `custom: «flip_back — верхня плитка підкидається назад угору конвеєром»` (виграш часу).
- КОЛИ `input(button)` → ЯКЩО `free(top_of(bin_column[paddle_pos]))` → ТО `place(top_tile, bin_column)`, `fall(tile)` до опори; інакше `block`.
- КОЛИ `pattern(line(3+, same_color))` у колодязі (горизонталь, вертикаль, будь-яка діагональ) → ТО `clear(line)`, `score(klax_type)`, `counter(klax, +1)`, `counter(goal, +1)` за типом.
- КОЛИ одна плитка замикає кілька ліній → ТО всі зникають, `score(multi_klax_bonus)`; лінія з 4 чи 5 — окремий бонус.
- КОЛИ `after(clear)` → ТО `fall(tiles_above)`; ЯКЩО `pattern(line(3+))` → ТО `clear`, `combo(+1)`, бонус за «падаючий» Klax (каскад).
- КОЛИ `counter(goal, ≥, wave_target)` → ТО `custom: «wave_cleared»`, `score(bonus × tiles_on_conveyor_and_paddle)`, `score(bonus × empty_bin_cells)`, `next_level`.
- КОЛИ `counter(drops, ==, max_drops)` → ТО `lose`.
- КОЛИ `count(bin_empty_cells, ==, 0)` → ТО `lose` (колодязь повний).
- КОЛИ `level_start` хвиль 1, 6, 11 … (кожні 5) → ТО `counter(drops, =0)`, `window(wave-select)`: одна з трьох наступних хвиль; дальша — більше очок і більше дозволених промахів.
- Типи цілей хвилі: N Klax будь-яких · N діагоналей · N горизонталей (?) · N очок · спіймати/пережити N плиток.
- Перемога: пройдено 100 хвиль. Поразка: drop meter або повний колодязь. Рахунок: Klax за типом (діагональ — найдорожча (?)) + мульти-Klax + довжина + каскад + бонуси кінця хвилі + бонус «варпу».

## Керування і ввід
- Аркада: джойстик ←/→ — лопатка між 5 позиціями; ↑ — підкинути верхню плитку назад; ↓ — прискорити конвеєр; кнопка — скинути верхню плитку в колодязь під лопаткою.
- Курсор-лопатка — «рука», що несе буфер: не аватар на полі, а дискретна позиція над стовпцями колодязя.
- Дві ортогональні дії з одним буфером: «взяти» відбувається саме (ловля), «покласти» — свідомо (кнопка).

## Вікна, меню, HUD
- `attract-demo` з гаслом «It's the 90's. Time for Klax.» (?) і таблицею рекордів.
- `window(wave-select)` — `custom: «вибір хвилі»`: три номери хвиль (напр. 1 / 6 / 11) з бонусом очок і кількістю промахів; таймер вибору (?).
- `game-screen`: конвеєр у перспективі, лопатка зі стопкою, колодязь 5×5; `score`, `wave-counter`, `objective-text` (ціль хвилі на старті, «Klax To Go»), `custom: «drop-meter»` (лампочки дозволених промахів), `remaining-counter` до цілі.
- `popup-text` «KLAX!», «DIAGONAL» та бонуси на місці лінії (?).
- Міжхвильовий `end-screen`: бонуси за плитки на конвеєрі/лопатці й порожні клітини.
- `end-screen` Game Over → `leaderboard` (ініціали).
- Переходи: attract → (монета) wave-select → game-screen → (ціль) бонус → game-screen наступної хвилі; кожні 5 хвиль — знову wave-select; drop meter / повний колодязь → game over → leaderboard.

## Фічі поза полем
- `levels-sequential` 100 хвиль із `custom: «warp»` — вибір стартової хвилі кожні 5 (ризик ↔ бонус), аналог `level-select` без збереження.
- `leaderboard-local` (аркада), `continue` за монету (?).
- `operator-settings` — DIP-налаштування складності/життів на аркаді (?).
- Домашні порти — `pause`, `difficulty-presets` (?); жодного undo/hint.

## Варіації й родичі
- Порти 1990–1992 на десятки платформ (Tengen NES, Lynx, Genesis, Spectrum …), Klax у збірках Midway Arcade Treasures / Atari; Klax-рівень у Lego Dimensions.
- Родичі: Columns (той самий збіг 3+ у 8 напрямках, але фігура падає в стакан), Tetris (прямий конкурент ери), Puzznic, Magical Drop (теж «рука» над стовпцями, але бере з поля).
- **Осі варіацій**: звідки плитки (падають фігурою / приїжджають конвеєром / піднімаються знизу) · буфер (нема / 1 hold / стопка LIFO ≤ 5) · напрямки збігу (4 / 8) · ціль (виживання / квота типу лінії / очки) · штраф (стеля / лічильник промахів).

## Цікавинки для курсу
- Лопатка-стопка LIFO з лімітом 5 і ловлею на краю конвеєра — 📎 (стек + колізія «плитка дійшла до краю»).
- Пошук ліній 3+ у 8 напрямках у колодязі 5×5 з розрізненням типу (гориз./верт./діаг.) — 🌱.
- Каскад після зчищення з бонусом «падаючого Klax» — 🥉 (спільний із Columns/Bejeweled).
- Ціль хвилі як параметр (тип лінії + кількість) з лічильником «лишилось» — 📎.
- Drop meter + повний колодязь — дві незалежні умови поразки — 🌱.
- Вибір хвилі кожні 5 з бонусом за ризик — 🌱 (гарне вікно).
- Конвеєр у перспективі (5 доріжок, плитки перекидаються) у GUI — 🥈 за рендер, 📎 у консолі.

## Мапа на каталог
- Є: `row-conveyor` (конвеєр доріжок) · `inventory-limit` (стопка ≤ 5) · `keyboard-controls` · `gravity-fall` (осідання в колодязі) · `collect-quota` (ціль хвилі) · `event-points` · `combo-multiplier` (мульти-Klax, каскад) · `time-bonus` (бонус за плитки, що лишились) · `progress-acceleration` · `sequential-levels` · `level-select` (warp) · `score-records` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+line-match-clear` «Лінія 3+ одного кольору зникає» · entities/legality · 📎 · слот {directions: 4|8} — тут 8 (спільна з Dr. Mario/Lines 98).
  - `+chain-reaction` · game-logic/score · 🥉 (спільна).
  - `+conveyor-catch` «Ловля плиток з конвеєра» · entities/interact · 📎 — кінець доріжки + позиція лопатки.
  - `+lifo-hand` «Рука-стопка LIFO з лімітом» · entities/state · 📎 · слот {capacity: 5} (родич `inventory-limit`, Magical Drop `held-stack`).
  - `+miss-meter` «Лічильник промахів до поразки» · game-logic/lose · 🌱 · слот {max}.
  - `+wave-goal` «Ціль хвилі з типом і квотою» · game-logic/win · 📎 · слоти {kind: klax|diagonal|points|tiles, n}.
  - `+warp-choice` «Вибір стартової хвилі з бонусом» · levels/progression · 🌱.
  - `+flip-back` «Повернути обʼєкт назад у потік» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:edge` — ⏳ підтверджую: плитка дійшла до кінця конвеєра (точка ловлі/промаху).
- `+trigger:pattern` — ⏳ підтверджую: `line(3, any_dir)`.
- `+trigger:counter` — ⏳ підтверджую: drops = max, ціль хвилі виконана.
- `+effect:catch` — сутність переходить із потоку в буфер гравця (відмінне від `pickup`: обʼєкт лишається плиткою і піде на поле).
- `+effect:place` — 🔥 підтверджую: скинути з руки в стовпець.
- `+effect:flip_back` — повернути обʼєкт із буфера назад у потік.
- `+cond:free` — 🔥 підтверджую: стовпець колодязя не повний.
- `+role:supply` — 🔥 підтверджую: стопка на лопатці як запас поза полем.
- `+ui:drop-meter` — індикатор дозволених промахів (родич `lives`, але не життя).
- `+ui:objective-text` — ⏳ підтверджую: ціль хвилі словами.
- `+window:wave-select` — вибір з трьох хвиль із бонусом (родич `level-select`, але в процесі гри).
- `+axis:control` — тут `indirect`-подібне: гравець не рухає плитку, а лише «руку» над стовпцями.

## Джерела
- ⭐ [Wikipedia: Klax](https://en.wikipedia.org/wiki/Klax_(video_game)) — конвеєр, лопатка на 5, колодязь 25 = 5×5, Klax 3 у будь-якому напрямку, бонуси, 100 хвиль × 20 груп, drop meter, вибір хвилі, умови кінця, платформи.
- [Killer List of Videogames: Klax](https://www.arcade-museum.com/game_detail.php?game_id=8266) — аркадна версія.
- [Spectrum Computing: Klax](https://spectrumcomputing.co.uk/entry/0002707) — порт ZX Spectrum.
- [Wikipedia: Tile-matching video game](https://en.wikipedia.org/wiki/Tile-matching_video_game) — місце Klax/Columns у другому поколінні (контекст).
- YouTube: пошук «klax arcade gameplay».

## Непевне
- (?) Конкретні очки за типи Klax (вертикаль < горизонталь < діагональ) — з памʼяті; Wikipedia лише каже, що є бонуси.
- (?) Миготлива плитка-джокер у пізніх хвилях — з памʼяті, не перевірено.
- (?) Гасло атракт-режиму, напис «Klax To Go», `popup-text`, таймер вибору хвилі, continue за монету, DIP-налаштування — з памʼяті.
- (?) Мультиплеєр: Wikipedia в інфобоксі має «multiplayer», але не пояснює (почергово чи два колодязі) — `opponent: none` поставлено як основний режим.
- (?) Чи можна підкинуту плитку спіймати знову — логічно так (вона знову котиться донизу), але джерело не підтверджує.
- HG101 і StrategyWiki під час дослідження були недоступні (переїзд сервера / 403); WebSearch вичерпано.
