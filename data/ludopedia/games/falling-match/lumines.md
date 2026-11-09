---
title: Lumines (Люмінес)
slug: lumines
aka: ["Lumines: Puzzle Fusion", Lumines Remastered, Lumines Live!, Lumines II, Lumines Supernova, Lumines Arise, ルミネス]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: rhythm
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2004
platforms: [PSP, PS2, PC, Xbox 360, PS3, iOS, Android, PS Vita, Switch, PS4, Xbox One, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lumines:_Puzzle_Fusion", best: true, note: "правила оригіналу: 2×2 двоколірні фігури, поле 16×10, time line, special block, скіни й темп, режими Challenge/Single Skin/Time Attack/Puzzle/Versus"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lumines", note: "серія: Lumines II (Mission, Skin Edit, Sequencer), Live!, Supernova (DigDown), Electronic Symphony, Arise (Burst)"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ルミネス", note: "скін = BGM + звуки + блоки + фон; 40 скінів в оригіналі"}
  - {kind: other, url: "https://diplograph.net/2018-09/luminesremasterednotes", note: "фан-нотатки: 40 очок за квадрат, 4× за 4+ квадрати за прохід, combo до 16× у Remastered, правила chain block у різних версіях"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Lumines", note: "пошук; Lumines Remastered, Lumines Arise"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lumines+puzzle+fusion+psp+gameplay", note: "пошук; геймплей PSP"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, keyboard-controls, next-queue, event-points, combo-multiplier, score-records, time-out, game-pause, end-screen, mode-select, theme-select, avatar-picker, background-music, sound-effects, ai-opponent, level-bank, +sweep-line-clear, +square-group-match, +split-on-landing, +rhythm-sync-tempo, +flood-same-color, +board-state-bonus, +versus-boundary-tug, +skin-unlock-progression, +skin-playlist]
proposes: ["+role:sweeper", "+effect:mark_group", "+effect:flood_clear", "+effect:shift_boundary", "+ui:sweep-counter", "+feature:skin-playlist", "+feature:music-sequencer"]
author: opus
date: 2026-11-09
---

# Lumines — 2×2 двоколірні фігури, одноколірні квадрати стирає лінія, що біжить у такт музиці

## Суть
Зверху падає фігура 2×2 з блоків двох кольорів (світлий/темний); її обертають і кладуть, складаючи **одноколірні квадрати 2×2** і більші прямокутники. Квадрат не зникає одразу: його стирає **time line** — вертикальна лінія, що безперервно біжить полем зліва направо з темпом поточного треку. Головна думка — відкладене зчищення: між утворенням квадрата і його зникненням є час, за який можна доліпити ще квадрати й зібрати більший прохід. Скін (фон + музика + блоки + темп лінії) змінюється по ходу гри, тож змінюється і ритм.

## Поле і час
- Поле 16 стовпців × 10 рядів (Wikipedia); фігура спавниться по центру зверху.
- Шари: стек блоків + активна фігура 2×2 + time line (окремий шар поверх поля) + черга наступних фігур.
- Два годинники: **падіння фігури** (свій темп) і **time line** (темп = BPM треку скіна). Лінія не зупиняється, коли гравець думає.
- Лягання: якщо одна половина фігури впирається, друга відривається й падає далі окремо (фігура «розколюється»).
- Повний прохід лінії від лівого краю до правого — одиниця рахунку: очки нараховуються за кількість квадратів, стертих за прохід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура 2×2 | player | 4 блоки, кожен світлий/темний | падає; ліво/право; обертання на 90°; швидке падіння; лягає → 4 окремі блоки |
| Блок | tile | колір (2 на скін) | лежить у стеку; без опори падає |
| Квадрат (позначена група) | zone | ≥2×2 одного кольору | утворюється одразу при доторку; підсвічується; чекає на time line |
| Special block (самоцвіт / хрестик) | tile | колір | у складі квадрата стирає всі сусідні блоки свого кольору (заливкою) |
| Time line | custom: «sweeper» | позиція x, темп = BPM | рухається зліва направо, на правому краї повертається ліворуч; стирає позначені квадрати |
| Лічильник проходу | — | n квадратів | показується на лінії; скидається на кожному новому проході |
| Черга next | spawner | 3 фігури (Remastered) | джерело наступних фігур |
| Межа поля (Versus) | zone | позиція межі | поле поділене навпіл; зчищення зсуває межу в бік суперника |
| Скін | — | фон, блоки, трек, звуки, темп | змінюється за рівнем у Challenge; задає швидкість лінії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose` (стек дійшов до верху).
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; інакше `custom: «lock — фігура стає 4 блоками стеку»`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`.
- КОЛИ `input(rotate_cw|rotate_ccw)` → ТО `rotate(piece, ±90)` (форма 2×2 лишається, міняється розкладка кольорів).
- КОЛИ `input(drop)` → ТО `fall(piece)` до опори.
- КОЛИ `locked(piece)` → ЯКЩО `not supported(block)` → ТО `fall(block)` окремо (розкол фігури).
- КОЛИ `settled` → ЯКЩО `pattern(group(2×2, same_color))` → ТО `custom: «mark_group — блоки групи позначені квадратом, ще не зникли»`; суміжні квадрати одного кольору зливаються в прямокутник (2×3 = 2 квадрати зі спільним стовпцем).
- КОЛИ `tick` → ТО `move(time_line, right)` з темпом `custom: «BPM поточного скіна»`.
- КОЛИ `contact(time_line, marked_group)` → ЯКЩО `custom: «група утворилась до того, як лінія зайшла на неї»` → ТО `clear(group)`, `counter(sweep_squares, +n)`.
- КОЛИ `contact(time_line, marked_group)` → ЯКЩО `custom: «квадрат утворився посеред лінії»` → ТО `clear(intersected_part)` без очок.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)` — каскад; нові квадрати можуть утворитись і потрапити в той самий прохід.
- КОЛИ `pattern(group(2×2, same_color))` → ЯКЩО `custom: «у групі є special block»` → ТО `custom: «flood_clear — позначити всі блоки цього кольору, звʼязні з групою»`.
- КОЛИ `reach(time_line, right_edge)` → ТО `score(40 × sweep_squares)`, `wrap(time_line)`.
- КОЛИ `reach(time_line, right_edge)` → ЯКЩО `count(sweep_squares, ≥, 4)` → ТО `multiplier(×4)` (оригінальний бонус).
- КОЛИ `reach(time_line, right_edge)` → ЯКЩО `count(sweep_squares, ≥, 4)` і попередній прохід теж ≥4 → ТО `combo(+1)` (Live!/Remastered; в оригіналі нема); інакше `reset_combo`.
- КОЛИ `reach(time_line, right_edge)` → ЯКЩО `count(colors_on_field, ==, 1)` → ТО `score(+bonus)` («одноколірне поле»).
- КОЛИ `reach(time_line, right_edge)` → ЯКЩО `all_gone(blocks)` → ТО `score(+bonus)` (all clear).
- КОЛИ `counter(squares_cleared, ≥, level_quota)` → ТО `counter(level, +1)`; ЯКЩО `custom: «кінець блоку рівнів скіна»` → ТО `custom: «наступний скін — інші кольори, музика й темп лінії»`.
- Time Attack: КОЛИ `timer(==0)` → ТО `game_over`, підсумок стертих блоків.
- Versus: КОЛИ `reach(time_line, edge)` → ЯКЩО `counter(sweep_squares, >, 0)` → ТО `custom: «shift_boundary — межа полів зсувається в бік суперника»`; той, чиє поле переповнилось, програє.
- Puzzle: КОЛИ `all_constraints_met` → ТО `win` (квадрати склали задану картинку).
- Mission (Lumines II): КОЛИ `counter(goal, ≥, n)` → ЯКЩО `count(moves, ≤, limit)` → ТО `win`.
- Поразка: блоки дійшли до верху. Рахунок: квадрати за прохід × бонуси; макс. 999 999 (оригінал).

## Керування і ввід
- PSP: d-pad ←/→ — зсув, ↓ — швидке падіння, дві кнопки — обертання в різні боки (?), Start — пауза.
- Touch Fusion (iOS): фігуру тягнуть і обертають пальцем; клавіш нема.
- Ввід не впливає на time line: гравець лише кладе фігури; керування темпом — тільки через вибір скіна (Single Skin / Skin Edit).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` з `mode-select`: Challenge · Single Skin · Time Attack · Puzzle · Vs CPU · Vs 2P (?) · Options.
- `skin-select` — вибір відкритого скіна (Single Skin; Skin Edit — порядок скінів).
- `custom-window` «Avatar» — вибір аватара, що показується поруч із полем (?); у Puzzle аватари відкриваються за 100 пазлів.
- `game-screen`: поле, time line з лічильником квадратів проходу, `next-piece-preview` (3 фігури), `score`, `hi-score`, `level-number`, `timer-elapsed`, назва скіна; Time Attack — `timer-countdown`.
- `pause-menu`: продовжити / вийти (?).
- `end-screen` Game Over → `leaderboard` (рекорди за режимами).
- Versus: два аватари й спільне поле з рухомою межею.
- Переходи: main-menu → вибір режиму/скіна → game-screen → (стек до верху / час вийшов) end-screen → leaderboard.

## Фічі поза полем
- Режими: `mode-endless` (Challenge — скіни по колу зі зростанням складності), `mode-time-attack`, `mode-puzzle` (картинки з квадратів), `mode-versus` (CPU і бездротово), Mission (Lumines II), DigDown (Supernova: прокопати дві вертикальні лінії за час).
- `unlockables`: скіни відкриваються проходженням; `theme-select` — Single Skin.
- `custom: «skin-playlist»` — Skin Edit (Lumines II, Live!): власний порядок відкритих скінів.
- `custom: «music-sequencer»` — Lumines II/Supernova: секвенсор зі звуків гри.
- `leaderboard-local`, `achievements` (Live!), `online-multiplayer` (Live!).

## Варіації й родичі
- Puzzle Fusion (PSP, 2004) → Lumines Plus (PS2) → Lumines II (Mission, Skin Edit, Sequencer) → Lumines Live! (XBLA, онлайн) → Supernova (PS3, DigDown) → Touch Fusion (iOS) → Electronic Symphony (Vita, World Block, Shuffle-блок) → Puzzle & Music (mobile) → Remastered (2018) → Arise (2025, Burst: заповнити шкалу й «заморозити» квадрати в один великий).
- Родичі: Tetris (падаюча фігура), Columns/Puyo (колір як критерій), Meteos (той самий автор Mizuguchi-Q Entertainment, теж «музичні» скіни (?)), Tetris Effect (скіни + музика, що реагує на гру).
- **Осі варіацій**: момент зчищення (одразу / лінія-розгортка / за кнопкою) · форма збігу (лінія 3+ / квадрат 2×2 / звʼязна група 4+) · джерело темпу (рівень / BPM треку) · спецблок (нема / заливка кольору / shuffle) · кількість кольорів (2 / більше).

## Цікавинки для курсу
- Time line як сутність-розгортка: зчищення відкладене до проходу лінії, лічильник за прохід — 📎 (стан «позначено» між утворенням і зникненням).
- Пошук одноколірних квадратів 2×2 з перекриттям (прямокутник 2×3 = 2 квадрати) — 🌱.
- Розкол фігури 2×2 при доторку однією половиною — 🌱.
- Квадрат, що утворився посеред лінії: часткове стирання без очок — 📎 (порядок обробки стовпців).
- Special block: заливка звʼязних блоків кольору (BFS) — 📎.
- Темп лінії = BPM треку, синхронізація логіки з музикою — 🥉.
- Versus з рухомою межею на спільному полі — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (фігура 2×2) · `piece-rotate-flip` · `keyboard-controls` · `next-queue` · `event-points` · `combo-multiplier` (серія проходів) · `score-records` · `time-out` (Time Attack) · `game-pause` · `end-screen` · `mode-select` · `theme-select` (скіни) · `avatar-picker` · `background-music` · `sound-effects` · `ai-opponent` (Vs CPU) · `level-bank` (Puzzle, Mission).
- **Нема** → пропозиції карток:
  - `+sweep-line-clear` «Лінія-розгортка стирає позначене» · entities/interact · 📎.
  - `+square-group-match` «Одноколірний квадрат 2×2 з перекриттям» · entities/interact · 🌱.
  - `+split-on-landing` «Фігура розколюється, коли частина вперлась» · entities/move · 🌱 (Puyo-пара теж).
  - `+rhythm-sync-tempo` «Темп логіки від BPM треку» · game-logic/waves · 🥉.
  - `+flood-same-color` «Спецплитка стирає звʼязну область свого кольору» · entities/interact · 📎.
  - `+board-state-bonus` «Бонус за стан поля: один колір / порожньо» · game-logic/score · 🌱.
  - `+versus-boundary-tug` «Спільне поле з межею, що зсувається» · game-logic/opponent · 🥈.
  - `+skin-unlock-progression` «Скіни відкриваються проходженням» · levels/progression · 🌱.
  - `+skin-playlist` «Власний порядок скінів» · interface/settings · 🌱.

## Пропозиції до словників
- `+role:sweeper` — сутність-розгортка, що проходить полем і застосовує ефект до клітин (time line Lumines; родич — скан-лінія).
- `+effect:mark_group` — позначити групу як «до зчищення» без негайного `clear` (Lumines; Panel de Pon — затримка перед зникненням).
- `+effect:flood_clear` — стерти звʼязну область того самого кольору від клітини (special block).
- `+effect:shift_boundary` — зсунути межу між зонами гравців (Lumines Versus).
- `+ui:sweep-counter` — лічильник подій поточного проходу/циклу на самій лінії.
- `+feature:skin-playlist` — порядок тем/скінів задає гравець.
- `+feature:music-sequencer` — вбудований секвенсор зі звуків гри.

## Джерела
- ⭐ [Wikipedia: Lumines: Puzzle Fusion](https://en.wikipedia.org/wiki/Lumines:_Puzzle_Fusion) — поле 16×10, 2×2 двоколірні фігури, розкол, time line, частковий квадрат без очок, special block, бонуси одного кольору й all clear, скіни й темп, режими, макс. 999 999.
- [Wikipedia: Lumines (серія)](https://en.wikipedia.org/wiki/Lumines) — сиквели: Mission, Skin Edit, Sequencer, DigDown, Burst; chain block у пізніх версіях.
- [ja.wikipedia: ルミネス](https://ja.wikipedia.org/wiki/ルミネス) — скін = BGM + SE + блоки + фон; 40 скінів в оригіналі, 100+ у Lumines II.
- [diplograph: Lumines Remastered notes](https://diplograph.net/2018-09/luminesremasterednotes) — 40 очок за квадрат, 4× за 4+ квадрати, combo у Live!/Remastered, chain block, 3 фігури в черзі.
- YouTube: пошук «lumines puzzle fusion psp gameplay».

## Непевне
- (?) Ширина поля: Wikipedia — 16×10, фан-нотатки — «20 блоків завширшки»; можливо, різні версії.
- (?) Точний момент стирання: лінія стирає групу стовпець за стовпцем чи цілу групу, коли пройшла її правий край.
- (?) Величини бонусів «один колір» і all clear (для Live! згадують 1 000 і 10 000) — для оригіналу не перевірено.
- (?) Квота квадратів на рівень і кількість рівнів на скін у Challenge.
- (?) Розкладка кнопок PSP, кількість кнопок обертання.
- (?) Аватари: лише косметика чи щось змінюють у Versus; повний список пунктів головного меню.
- (?) Різниця special block між версіями: «у складі квадрата» (оригінал, Live!) vs «доторкнувся до свого кольору» (Remastered).
