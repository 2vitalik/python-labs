---
title: Magical Tetris Challenge
slug: magical-tetris-challenge
aka: []
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1998
platforms: [arcade, N64, PlayStation, Game Boy Color]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Magical_Tetris_Challenge", best: true, note: "магічні фігури до 5×5 і контратака, Pentris, Magic Meter, Updown, режими GBC (Signal, Towering, Target, Quest), лазер висоти суперника"}
  - {kind: other, url: "https://tetris.wiki/Magical_Tetris_Challenge", note: "TetrisWiki: 10×18, 2 next, без hold, hard drop, спільна черга, контратака → квадрати до 5×5, своя система кіків у рамці 5×5, Signal/Harmony на GBC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magical+Tetris+Challenge+N64+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, next-queue, garbage-attack, simultaneous-versus, ai-opponent, event-points, character-select, difficulty-levels, mode-select, +line-clear, +ghost-piece, +hard-drop, +garbage-offset, +giant-piece-attack, +attack-piece-growth, +meter-board-wipe, +all-clear-bonus, +shared-next-queue, +signal-row-match, +rising-rows, +clear-all-goal, +sync-clear-coop, +bbox-kick-rules, +story-chapters]
proposes: ["+ui:magic-meter", "+ui:opponent-height-bar", "+effect:offset_garbage", "+card:giant-piece-attack", "+card:attack-piece-growth", "+card:meter-board-wipe", "+card:shared-next-queue", "+card:signal-row-match", "+card:sync-clear-coop", "+card:bbox-kick-rules"]
author: opus
date: 2026-11-09
---

# Magical Tetris Challenge — versus-Tetris, де атака — не сміттєві ряди, а гігантські фігури супернику, а контратака роздуває їх до 5×5

## Суть
Tetris від Capcom з персонажами Disney (Міккі, Мінні, Дональд, Гуфі). У головному режимі **Magical Tetris** зчищення рядів не додає супернику сміття знизу, а **підкладає в його чергу «магічні» фігури** — пентаміно й більші; якщо він зчищає ряди, поки ці фігури ще в черзі, частину з них він гасить і відсилає назад уже як **квадратні блоки**, які при кожній новій контратаці ростуть аж до 5×5. Поруч із полем — **Magic Meter**: заповнений рядами й комбо, він ущільнює стек і стирає все вище своєї лінії. Версія для Game Boy Color додає режими-пазли, найцікавіший — **Signal Tetris** з фарбуванням «підлоги» під колодязем.

## Поле і час
- Колодязь 10×18; next — 2 фігури (аркада, N64, PS1), 1 (GBC); hold нема; є hard drop і ghost; допоміжна сітка стовпців.
- Фігура входить у колодязь згори по одному ряду; поразка — нова фігура при вході перекриває стек.
- Real-time; versus — два колодязі поруч; на GBC видно лише свій колодязь, а висоту стеку суперника — блимаючим «лазером» ліворуч.
- Обидва гравці беруть фігури зі **спільної** черги, з якої поповнюються їхні власні черги next.
- Своя система поворотів: кожна фігура в рамці 5×5; при колізії рахується сума зсувів точок зіткнення від центру рамки (X, Y) і за шістьма правилами обирається **один** кік; не вдався — поворот скасовано.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | player | 7 форм | падає, зсувається, повертається з кіком у рамці 5×5, hard drop |
| Магічна фігура | player | пентаміно (зокрема пряма з 5 — дає Pentris) та більші | приходить у чергу від суперника як атака; керується як звичайна |
| Квадратний блок | player | 2×2 … 5×5 | контратака: погашена магічна фігура повертається квадратом; кожна наступна контратака збільшує квадрат, максимум 5×5 |
| Клітина стеку | tile | — | зникає з повним рядом |
| Сміттєвий ряд (Updown) | hazard | повний ряд з однією діркою в заданому стовпці | піднімається знизу; можна відіслати назад контратакою |
| Лінія Magic Meter | zone | висота; старт — 4-й ряд, мінімум 2 | заповнений метр стирає все вище лінії |
| Заданий стовпець | zone | — | «випадає» при спрацюванні Magic Meter |
| Ряд-зразок і сигнальний ряд (Signal, GBC) | mark | кольори червоний / синій (+ жовтий на Expert) | під колодязем; збіг кольорів → додаткові ряди зникають |
| Ключ-блок (Towering, GBC) | static | у нижньому ряду | зчистити його ряд — перемога |
| Доміно-фігура (Towering, GBC) | player | 1×2 | поки на екрані, A/B скидає з неї одиночні блоки; на локу зникає |
| Мішені (Target, GBC) | object | жолуді / блискавки / полумʼя | зчистити всі заданою послідовністю фігур |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose`.
- КОЛИ `custom: «гравець бере наступну фігуру»` → ТО `custom: «його черга next поповнюється зі спільної черги обох гравців»`.
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`.
- КОЛИ `input(rotate)` → ТО `rotate(piece, ±90)`; ЯКЩО `not free(new_cells)` → ТО `custom: «kick — X, Y = сума зсувів точок зіткнення від центру рамки 5×5; Y=0, X=−3 → 2 вправо; Y=0, X=+3 → 2 вліво; Y=+3, X=0 → 2 вгору; |Y|=|X| → убік за напрямом повороту; |Y|>|X| → 1 вниз/вгору; інакше 1 убік»`; одна спроба, не вдалась — `block` (на GBC правило |Y|=|X| пропущено).
- КОЛИ `input(hard_drop)` → ТО `move(piece, ghost_pos)`, `custom: «lock»`.
- КОЛИ `locked(piece)` → ЯКЩО `pattern(row_full)` → ТО `clear(rows)`, `drop_rows`; 5 рядів прямою пентаміно — Pentris.
- **Magical**: КОЛИ `after(clear)` → ЯКЩО `mode(magical)` і `custom: «у моїй черзі нема магічних фігур суперника»` → ТО `custom: «send_garbage — магічні фігури в чергу суперника»`.
- **Magical**: КОЛИ `after(clear)` → ЯКЩО `custom: «у моїй черзі є магічні фігури суперника»` → ТО `custom: «offset — частину з них погашено»`, `transform(countered, square_block)`, `custom: «квадрати летять назад у чергу суперника»`.
- **Magical**: КОЛИ `custom: «квадратний блок знову погашено контратакою»` → ТО `grow(square_block, +1)`, максимум 5×5.
- **Updown**: КОЛИ `after(clear)` → ЯКЩО `mode(updown)` → ТО `send_garbage(rows)` — повні ряди з діркою в заданому стовпці, знизу; вхідні ряди можна відіслати назад контратакою.
- **Magic Meter**: КОЛИ `after(clear)` → ТО `counter(magic, +n)` за ряди й комбо.
- КОЛИ `counter(magic, ≥, meter_line)` → ТО `collapse` (усі блоки падають, заповнюючи порожнини), `clear(predetermined_column)`, `clear(cells_above_meter_line)`, `counter(magic, =, 0)`.
- КОЛИ `custom: «спрацював метр»` → ЯКЩО `difficulty(higher)` → ТО `custom: «лінія метра піднімається на 2 ряди»` (важче заповнити, менше стирає).
- КОЛИ `after(clear)` → ЯКЩО `count(stack_cells, ==, 0)` → ТО `custom: «All Clear — лінія метра −2 ряди, не нижче 2»`.
- Рахунок: КОЛИ `after(clear)` → ТО `score(n)` — за кількість комбо й контратак, а не лише за ряди.
- **Signal (GBC)**: КОЛИ `after(clear)` → ТО `paint(signal_row, colors)` — колір кожної клітини сигнального ряду змінюється за стовпцями блоків, що заповнили зчищені ряди; ЯКЩО `same(signal_cell, sample_cell, color)` для m стовпців → ТО `clear(bottom m rows)`.
- **Towering (GBC)**: КОЛИ `timer(every)` → ТО `spawn_at(garbage_row, bottom)`; КОЛИ `custom: «зчищено ряд із ключ-блоком»` → ТО `win`.
- **Towering (GBC)**: КОЛИ `input(A|B)` → ЯКЩО `state(piece, domino)` → ТО `spawn_at(single_block, below_domino)`; КОЛИ `locked(domino)` → ТО `disappear(domino)`.
- **Target (GBC)**: задана послідовність фігур; КОЛИ `all_gone(target)` → ТО `win`.
- **Harmony (GBC, кооп)**: КОЛИ `pattern(row_full)` в одного гравця → ЯКЩО `custom: «інший теж склав повний ряд»` → ТО `clear(rows)`; інакше ряд чекає.
- **Versus GBC**: КОЛИ `custom: «лазер висоти суперника дійшов до верху»` → ТО `custom: «суперник програв»`.
- Перемога: суперник перекрив спавн (versus/story) · Поразка: власний top out · Рахунок: комбо й контратаки.

## Керування і ввід
- Хрестовина: зсув, soft drop; кнопки — поворот у дві сторони; hard drop; hold немає.
- Towering (GBC): A або B, поки на екрані доміно, — скинути одиночний блок.
- Versus: двоє гравців одночасно (аркада / консоль), або проти AI у Story / Endless.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story · Versus · Endless · Classic (консолі); на GBC — Quest, Magical, Updown, Signal, Towering, Target, Harmony.
- `character-select`: Mickey · Minnie · Donald · Goofy (на GBC — + Pete, відкривається Quest-ом).
- `difficulty-select`: Classic — три складності; Signal — Easy / Normal / Expert.
- `game-screen`: колодязь 10×18 з сіткою стовпців і `ghost-piece`, `next-piece-preview` (2 / 1), поруч — шкала `+ui:magic-meter` з лінією; другий колодязь суперника; рахунок. GBC: `+ui:opponent-height-bar` (лазер ліворуч); Signal — ряд-зразок і сигнальний ряд під полем; Towering — шкала прогресу ліворуч.
- `map-window` (GBC Quest): ралі — монети в NPC і будівель, кожна виграється матчем Tetris, фініш — на станції ралі раніше за суперників.
- `puzzle-select` (Target): понад сто пазлів за складністю.
- `dialogue-window` — сюжетні сцени Story між боями.
- `end-screen` — перемога / поразка, рахунок.
- Переходи: main-menu → mode-select → character-select → game-screen → end-screen → наступний суперник (Story).

## Фічі поза полем
- Story — у кожного персонажа свій шлях; фінальні суперники — Ласка і Великий Злий Вовк, потім Піт (`+story-chapters`).
- `mode-versus` (2 гравці), `ai-opponent-levels` (складність Story), `mode-marathon` (Classic, 3 складності), `mode-coop` (Harmony, GBC), `mode-puzzle` (Target, 100+), `unlockables` (Pete — Quest пройдено 4 рази; нові режими — після Quest).

## Варіації й родичі
- GBC-версія — суттєво інша гра: лише своє поле, власні режими, Magic Meter лише в частині варіантів.
- **Осі «форма атаки у versus»**: сміттєві ряди знизу (Tetris Guideline, тут Updown) / зайві фігури в черзі суперника (Magical) / блоки, що ростуть з кожною контратакою (тут, до 5×5) / краплі зверху (Puyo `puyo-puyo`, Dr. Mario `dr-mario`).
- **Осі «запобіжник стеку»**: нема (Tetris) / Magic Meter стирає верх (тут) / Zone (Tetris Effect `tetris-effect`).
- Родичі: Tetris (`tetris`), Tetris Worlds (`tetris-worlds`), Puyo Puyo Tetris (`puyo-puyo-tetris`), Super Puzzle Fighter II Turbo (`super-puzzle-fighter-ii-turbo`) — теж Capcom-versus.

## Цікавинки для курсу
- Атака фігурами в черзі суперника + гасіння контратакою з перетворенням на квадрат, що росте до 5×5 — 🥈 (дві черги, стан «чия фігура», ріст розміру).
- Спільна черга, з якої наповнюються дві власні черги next, — 📎 (чесний рандом для обох).
- Magic Meter: ущільнення стеку (кожна клітина падає), «випадіння» стовпця, стирання вище лінії, рух лінії від складності й All Clear — 🥉.
- Кік-система «сума зсувів точок зіткнення в рамці 5×5 → одне правило» — 🥈 (геометрія, порівняння з SRS).
- Signal Tetris: фарбування сигнального ряду кольорами блоків зчищених рядів і бонусні ряди за збіг зі зразком — 🥉.
- Harmony: зчищення лише синхронно в обох гравців — 📎.

## Мапа на каталог
- Є: `gravity-fall`, `multi-cell-size` (пентаміно, квадрати до 5×5), `keyboard-controls`, `next-queue`; `garbage-attack` ↔ Updown і магічні фігури; `simultaneous-versus`; `ai-opponent`; `event-points`; `character-select`; `difficulty-levels`; `mode-select`.
- Уже пропоновані: `+line-clear`, `+ghost-piece`, `+hard-drop`, `+garbage-offset` (тут гасіння магічних фігур), `+all-clear-bonus` (тут знижує лінію метра), `+rising-rows` (Towering), `+clear-all-goal` (мішені Target), `+story-chapters`.
- **Нема** → пропозиції карток:
  - `+giant-piece-attack` «Атака — зайві великі фігури в черзі суперника» · game-logic/opponent · 🥉 · слот {pieces: pentomino..5×5}.
  - `+attack-piece-growth` «Контратакований блок росте» · game-logic/opponent · 📎 · слот {max: 5×5}.
  - `+meter-board-wipe` «Метр заповнено → ущільнення і стирання вище лінії» · game-logic/score · 🥉 · слоти {start_line: 4, min: 2, rise: 2}.
  - `+shared-next-queue` «Спільна черга фігур для двох гравців» · game-logic/opponent · 📎.
  - `+signal-row-match` «Сигнальний ряд під полем зі зразком» · game-logic/score · 🥉 · слот {colors: 2|3}.
  - `+sync-clear-coop` «Ряд зникає лише разом із рядом партнера» · game-logic/opponent · 📎.
  - `+bbox-kick-rules` «Кік за сумою зсувів у рамці» · entities/legality · 🥈 — альтернатива `+srs-wall-kicks`.

## Пропозиції до словників
- `+ui:magic-meter` — шкала-лінія збоку поля, заповнення якої стирає верх стеку.
- `+ui:opponent-height-bar` — висота стеку суперника індикатором замість його поля (GBC).
- `+effect:offset_garbage` — погасити вхідну атаку своєю (вже пропонована `tetris`; тут — з перетворенням на квадрат).
- `+card:giant-piece-attack`, `+card:attack-piece-growth`, `+card:meter-board-wipe`, `+card:shared-next-queue`, `+card:signal-row-match`, `+card:sync-clear-coop`, `+card:bbox-kick-rules`.

## Джерела
- ⭐ [Wikipedia: Magical Tetris Challenge](https://en.wikipedia.org/wiki/Magical_Tetris_Challenge) — магічні фігури (пентаміно → до 5×5), контратака, Pentris, Magic Meter (4-й ряд, ущільнення, стовпець, +2 від складності, All Clear −2 до мінімуму 2), спавн по ряду, сітка й ghost, рахунок за комбо й контратаки, режими GBC, лазер висоти.
- [TetrisWiki: Magical Tetris Challenge](https://tetris.wiki/Magical_Tetris_Challenge) — 10×18, next 2/1, без hold, hard drop, спільна черга, квадрати до 5×5, Updown, Classic з 3 складностями, Signal (ряд-зразок і сигнальний), Towering, Target, Harmony, повний алгоритм кіків.
- YouTube: пошук «Magical Tetris Challenge N64 gameplay».

## Непевне
- (?) Скільки й яких магічних фігур надсилається за 1/2/3/4 ряди і скільки гасить контратака — не знайдено.
- (?) Signal Tetris: обидва джерела формулюють правило фарбування нечітко (Wikipedia сама просить звірити з первинним джерелом); точна відповідність «стовпець блока → клітина сигнального ряду» — (?).
- (?) Endless: Wikipedia — «класичний Tetris без магічних фігур», TetrisWiki — «Magical Tetris можна грати в story, versus або endless»; Classic як окремий режим — лише в TetrisWiki.
- (?) Програш у Target при вичерпанні послідовності та механіка Harmony «ряд чекає» — з короткого опису.
- (?) Як вибирається «заданий стовпець» Magic Meter.
- (?) Розкладка кнопок для кожної платформи не перевірена.
