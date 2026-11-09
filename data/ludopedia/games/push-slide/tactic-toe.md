---
title: Tactic Toe
slug: tactic-toe
aka: [tactic toe by bens]
family: push-slide
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: null
platforms: [web, PICO-8]
links:
  - {kind: itch, url: "https://bennyboybuggy.itch.io/tactic-toe", best: true, note: "грати в браузері; «блок рухається туди, куди його відштовхують сусіди»; 100+ рівнів, 30 окремих наборів правил, генератор, редактор, мишка C/X"}
  - {kind: play, url: "https://html-classic.itch.zone/html/14193728/index.html", note: "сам PICO-8-картридж (puzzle.js); код Lua розпакований з _cartdat — джерело правил цього файла"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tactic+toe+pico-8+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, piece-move-patterns, inertia-slide, impassable-cells, legal-move-highlight, selection-highlight, undo-unlimited, restart-level, level-select, sequential-levels, level-bank, tutorial-window, in-game-editor, editor-palette, editor-playtest, state-string, save-game, level-solver, difficulty-rating, +adjacency-repel-move, +goal-cover-any, +per-level-ruleset, +n-moves-away-check, +depth-filtered-generator, +type-cycle-per-move, +mirror-move, +trail-spawn]
proposes: ["+cond:pushed_off(a, dir)", "+feature:n-moves-check", "+feature:depth-filtered-generator", "+card:adjacency-repel-move", "+card:per-level-ruleset"]
author: opus
date: 2026-11-09
---

# Tactic Toe — блок їде лише туди, куди його «відштовхують» сусіди: накрий блоками всі цілі на полі 6×6

## Суть
Курсорний пазл на PICO-8 від двох Бенів (bennyboybuggy). На полі 6×6 стоять блоки і цілі; гравець обирає блок і переставляє його на сусідню клітину, але **лише в напрямку «від» іншого блока**: сусід позаду (чи пара сусідів по боках позаду) «відштовхує» його. Ізольований блок не рухається зовсім — щоб посунути один блок, спершу треба підвести до нього інший. Типи блоків змінюють, *як* застосовується відштовхування: звичайний робить крок, ракета ковзає до упору, кінь стрибає буквою «Г», камінь не рухається, але відштовхує. Пізні паки — 30 рівнів, у кожному з яких перекручене одне правило (дзеркало, ліміт ходів, «перемога, коли ніхто не може рухатись», спецблок Orwell з власною здатністю).

## Поле і час
- Квадратне поле 6×6 (у коді `inbounds`: 1..6), клітина 16×16 px; ліва колонка екрана — кнопки рівня.
- Шари: цілі (маркери, не блокують і не відштовхують) + блоки (займають клітину, відштовхують усі, зокрема камені).
- Хід = одне переміщення одного блока; поза вводом світ стоїть (`time: turn`), випадковості нема — крім режиму нескінченного генератора.
- Сусідство 8-кутне: діагональні сусіди теж відштовхують, і рух можливий у 8 напрямків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ціль | zone | 1+ на рівні | клітина-мета; перемога, коли на кожній цілі стоїть будь-який блок |
| Звичайний блок (regular) | piece | — | крок на 1 у кожен «відштовхнутий» напрямок (до 8) |
| Ракета (rocket) | piece | — | ті самі напрямки, але ковзає до краю поля або до блока; на полі малюються стрілки-сліди |
| Кінь (knight) | piece | дальність курсора 2 | з кожного легального напрямку — стрибок «Г»: діагональ (dx,dy) → (x+dx, y+2dy) і (x+2dx, y+dy); пряма → 2 вперед і 1 вбік у кожен бік |
| Камінь (stone) | static | — | не вибирається й не рухається; як сусід — відштовхує інших |
| Orwell | piece | лише пак «orwell.» | спецблок; у кожному рівні паку — своє правило (дублюється, не рухається, ходить лише діагоналлю, стрибає на 2…) |
| Курсор | — | клітина | рамка під мишею/стрілками; на вибраному блоці — підсвітка, на легальних цілях — точки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, block)` → ЯКЩО `custom: «блок — не камінь»` → ТО `set_state(block, selected)`, `custom: «показати точки на всіх легальних клітинах»`; клік по каменю → `block`.
- Звичайний: КОЛИ `input(click, dot)` → ЯКЩО `custom: «для напрямку d є сусід у клітині −d; або (d прямий) обидва діагональні сусіди позаду; або (d діагональний) обидва прямі сусіди позаду»` and `free(target)` and `custom: «ціль у межах 6×6»` → ТО `move(block, d)`.
- Ракета: та сама умова напрямку → ТО `slide(rocket, d)` до краю або до блока.
- Кінь: ЯКЩО `custom: «d — легальний напрямок звичайного ходу»` and `free(l_cell)` → ТО `move(knight, l_cell)` (L-клітини з таблиці вище; дублікати відкидаються).
- Цілі не блокують: блок може стати на ціль; маркер цілі не відштовхує.
- КОЛИ `custom: «на кожній цілі стоїть блок будь-якого типу»` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(x)` → ТО `undo(1)` (стек усіх ходів рівня).
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `input(check)` («??») → ТО `custom: «перебір усіх ходів на глибину 3 (зріз після 40 гілок) → напис "close!" або "not close"»`.
- Нескінченний режим: КОЛИ `level_start` → ТО `spawn_at(goal, random)` ×1–3, `spawn_at(block, random)` ×6–7 (камінь/звичайний/ракета/кінь) → ЯКЩО `custom: «розвʼязок є на глибині ≤5, але нема на ≤3, і нема накладань»` → прийняти; інакше генерувати знову.
- Експериментальний пак (15 правил, підказка — кнопкою «rules»): key — ЯКЩО `custom: «на першій цілі стоїть саме блок-ключ»` → ТО `win`; least — ЯКЩО `counter(moves, >, 5)` → ТО `custom: «перемога не зараховується»`; lose — КОЛИ `no_moves(all)` → ТО `win`; evolve — КОЛИ `turn_end` → ТО `transform(each_block, next_type)` по колу камінь → звичайний → ракета → кінь → камінь; mirror — КОЛИ `custom: «блок зробив хід»` → ТО `move(mirror_block, x → 7−x)`, якщо дзеркальна клітина вільна; press — `custom: «цілі — плити: перемога, коли накрито ≥2 рази»` (?); stack — `custom: «блоки можуть ділити клітину»`; undo_odnu — `custom: «undo скасовує найперший хід, а не останній»`.
- Пак «orwell.» (15 правил для блока Orwell): chain — КОЛИ `custom: «будь-який блок зробив хід»` → ТО `spawn_at(orwell, old_cell)`; meta — `custom: «Orwell може стати на будь-яку вільну клітину»`; undo — `custom: «Orwell ходить на будь-яку клітину з історії ходів»`; bishop — `custom: «лише діагональні напрямки»`; dead — Orwell → `block`; eye — `custom: «ціль Orwell — точкове відображення інших блоків відносно нього»`.
- Перемога: усі цілі накриті. · Поразка: нема (глухий кут — undo/restart). · Рахунок: нема; прогрес — розвʼязані рівні паку.

## Керування і ввід
- Мишка: C = клік (вибрати блок / клітину / кнопку), X = правий клік (undo; на екрані перемоги — «level select»). Сторінка itch: «Mouse Controls (C=Click, X=Right Click)».
- Стрілки рухають курсор по клітинах і по лівій колонці кнопок; вибраний блок обмежує курсор радіусом 1 (кінь — 2).
- Підказка внизу: «c to select, x to undo»; у редакторі — «c to choose, x to place».

## Вікна, меню, HUD
- `splash-screen`: поле заповнюється випадковими блоками й розсипається; клік → титул.
- `main-menu` (титул «tactic toe», ver 1.0, «by bens»): карусель `< play / make / ???? / dele / info >`; галочка біля кожного пройденого паку, окремий значок за всі 8.
- `custom-window` вибору паку: карусель піксельних логотипів 60×60 з лічильником «n/15» і галочкою; пак 1 — правила («press c»).
- `tutorial-window` («rules»): «to win: get block on goal · to move: push off blocks · this block can move … then it can't».
- `level-select` («sel»): рівні паку, старт з першого нерозвʼязаного.
- `game-screen`: поле 6×6, угорі «N. назва рівня», ліворуч кнопки exit / ?? / restart, унизу текст-підказка; HUD — `selection-highlight`, `legal-move-highlight` (точки), стрілки ракети.
- `end-screen`: рамка «continue / level select / retry»; останній рівень паку → святковий екран з кольоровим фоном і частинками.
- `editor-window` («make»): палітра goal / stone / regular / rocket / knight / delete, «play level».
- «????» — нескінченний режим: «generating level (30 sec)».
- `confirm-dialog` («dele»): «hold c to delete save file» зі смугою утримання.
- `about-window` («info»): «thank you for playing!», тестувальники, подяки.
- Переходи: splash → main-menu → пак → (rules | level-select) → game-screen → end-screen → наступний / level-select / retry.

## Фічі поза полем
- `puzzle-bank` паками: base (15), rocket (15), knight (15), more (15), experimental (15), orwell. (15), «no.» (5) і «leftovers» з рівнем тестувальника — разом понад 100.
- `undo` без ліміту + `restart-level`; `hint` у вигляді перевірки «чи до перемоги ≤3 ходи».
- `mode-endless` з генератором, що відсіює рівні за глибиною розвʼязку (4–5 ходів).
- `level-editor` зі збереженням у cartdata; рівень — рядок трійок «x y тип» (`share-code` через dev-константи `custom` / `mycode`).
- `autosave` прогресу паків (cartdata `bens_tactic_toe`), видалення сейва утриманням.

## Варіації й родичі
- [singleton-traffic](singleton-traffic.md) — рух залежить від сусідів поперек осі; [newtons-crates](newtons-crates.md) — поштовх передається через ряд; [sokochess](sokochess.md) і [unlock-the-king](unlock-the-king.md) — шахові патерни ходу в штовхальному пазлі; [atomix](atomix.md) і [ricochet-robots](ricochet-robots.md) — ковзання до упору, як у ракети.
- Осі варіацій:
  - **хто рухає блок**: аватар штовхає (Sokoban) / сусіди «відштовхують» (Tactic Toe) / один ввід рухає всіх (Singleton Traffic);
  - **відстань**: крок / до упору (ракета) / стрибок «Г» (кінь) / будь-куди (Orwell meta);
  - **сусідство**: 4 / 8 / пари бокових сусідів як «віртуальний» сусід позаду;
  - **правило рівня**: одне для всієї гри / окреме для кожного рівня (паки experimental і orwell).

## Цікавинки для курсу
- Генерація легальних ходів «відштовхуванням» з 8 сусідами і правилом пар — 📎 (три гілки умови, легко помилитись знаком).
- Три типи блоків як стратегії над одним списком напрямків (крок / ковзання / «Г») — 🥉.
- Кнопка «чи ≤3 ходи до перемоги»: DFS з обмеженням глибини й кількості гілок — 🥉.
- Генератор рівнів з фільтром «розвʼязний за 4–5, але не за 3» — 🥈 (генерація + солвер як суддя складності).
- Правило на рівень (30 модифікаторів: дзеркало, еволюція типів, перемога без ходів, undo навпаки) — 🥈: вимагає архітектури з хуками до ходу/після ходу/перевірки перемоги.
- Рівень як рядок трійок «x y тип» + редактор зі збереженням — 📎.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ мишка й стрілки; `piece-move-patterns` ↔ кінь і типи блоків; `inertia-slide` ↔ ракета; `impassable-cells` ↔ камінь; `legal-move-highlight` + `selection-highlight` ↔ точки й рамка; `undo-unlimited` + `restart-level`; `level-select` + `sequential-levels` + `level-bank` ↔ паки з прогресом; `tutorial-window` ↔ rules; `in-game-editor` + `editor-palette` + `editor-playtest`; `state-string` ↔ рядок рівня; `save-game` ↔ cartdata; `level-solver` ↔ перевірка «3 moves away»; `difficulty-rating` ↔ фільтр генератора за глибиною.
- **Нема** → пропозиції карток:
  - `+adjacency-repel-move` «Рух лише від сусіда: блок без сусідів нерухомий» · entities/legality · 📎.
  - `+goal-cover-any` «Цілі накрити будь-якими блоками» · game-logic/win · 🌱 (на відміну від `all-on-targets`, ящиків може бути більше за цілі).
  - `+per-level-ruleset` «Окреме правило для кожного рівня» · game-logic · 🥈 · слот {hooks: before_move, after_move, win_check}.
  - `+n-moves-away-check` «Підказка "чи за N ходів"» · levels/solvability · 🥉 · слот {depth}.
  - `+depth-filtered-generator` «Генератор із солвером-суддею» · levels/generation · 🥈 · слоти {min_depth, max_depth}.
  - `+type-cycle-per-move`, `+mirror-move`, `+trail-spawn` — модифікатори з паків experimental/orwell, кожен 📎.

## Пропозиції до словників
- `+cond:pushed_off(a, dir)` — у A є «відштовхувач» для напрямку dir (сусід позаду або пара бокових сусідів позаду).
- `+feature:n-moves-check` — кнопка «до розвʼязку ≤N ходів?» замість конкретної підказки.
- `+feature:depth-filtered-generator` — нескінченний режим, де солвер відсіює занадто легкі/важкі рівні.
- `+card:adjacency-repel-move`, `+card:per-level-ruleset` — механіки, яких у каталозі нема.

## Джерела
- ⭐ [itch: Tactic Toe](https://bennyboybuggy.itch.io/tactic-toe) — опис («a block pusher where the adjacency of a block changes where it can move»), 100+ рівнів / 30 наборів правил, генератор, редактор, сейв, мишка C/X, PICO-8, автори Ben and Ben.
- [Картридж puzzle.js](https://html-classic.itch.zone/html/14193728/index.html) — розпакований Lua-код: `reg` / `rocket` / `knight` (правила руху), `won` (цілі), `future` (перевірка глибини), `free` (генератор), назви паків і тексти підказок правил.
- YouTube: пошук «tactic toe pico-8 gameplay».

## Непевне
- (?) Рік випуску: на сторінці itch дати нема; мітка «No generative AI was used» і номер завантаження натякають на 2025 (?).
- (?) Правило press («every step counts») прочитане з коду поверхово: схоже, перемога — коли цілі накривались ≥2 рази за історію ходів.
- (?) Решту 20+ модифікаторів (palette, crane, match, double, cube, portal, glue, bubble, wrap, quarter, toggle, shy…) описано лише підказками з гри, без перевірки коду.
- (?) Чи відкриваються рівні паку по одному, чи всі одразу (`sel` стартує з першого нерозвʼязаного).
