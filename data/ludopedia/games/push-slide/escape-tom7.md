---
title: Escape (Tom 7)
slug: escape-tom7
aka: [Escape, Escape by Tom Murphy VII]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2004
platforms: [Windows, macOS, Linux]
links:
  - {kind: other, url: "http://escape.spacebar.org/win32/escape.txt", best: true, note: "офіційна документація: повний список плиток, лазери, панелі й bizarro-світ, роботи, бомби, керування, редактор, вивантаження"}
  - {kind: official, url: "http://escape.spacebar.org/", note: "сайт гри, завантаження, браузер рівнів, коментарі"}
  - {kind: other, url: "http://escape.spacebar.org/win32/changelog", note: "changelog з 2004: undo (2005), бомби (2005), redo (2006), bizarro (2006)"}
  - {kind: other, url: "http://escape.spacebar.org/levels.shtml", note: "веб-браузер рівнів спільноти з рейтингами style/difficulty"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Escape+Tom+7+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, push-object, inertia-slide, impassable-cells, fill-hole, destructible-blocks, beam-tracing, line-of-sight-attack, button-toggle, teleport-one-way, chase-greedy, explode-area, chain-detonation, environment-death, touch-death, collect-all, reach-exit, interaction-table, undo-redo, redo, restart-level, in-game-editor, editor-palette, editor-playtest, level-exchange, level-rating, level-bank, replay, state-as-data, +two-layer-field, +signal-wires, +sphere-cradle, +axis-locked-block, +one-push-block, +trap-stages, +collect-to-wake, +robot-turn-order, +solution-upload, +moderated-collections]
proposes: ["+trigger:signal_rise", "+effect:pulse", "+effect:switch_layer", "+effect:toggle_cell", "+cond:on_axis", "+role:robot", "+feature:upload-requires-solution", "+feature:moderated-collections", "+feature:speedrun-solutions", "+window:upload-dialog", "+card:two-layer-field", "+card:signal-wires", "+card:sphere-cradle", "+card:robot-turn-order"]
author: opus
date: 2026-11-09
---

# Escape (Tom 7) — дійди до виходу крізь лазери, дроти, панелі й прихований bizarro-світ, без жодних рефлексів

## Суть
Покрокова кімнатна головоломка в лінії Adventures of Lolo / Chip's Challenge: аватар ходить по клітинах і має стати на вихід, не опинившись під променем лазера. Ядро — **десятки типів плиток** із власною поведінкою: блоки, що штовхаються по-різному (ковзають, лише вздовж осі, стають нерухомими після одного поштовху), кулі-«колиска Ньютона», дроти з електрикою, кольорові підлоги, що перемикаються імпульсами, роботи й бомби. Найнезвичніше — **bizarro-світ**: кожне поле має прихований другий шар, і панелі міняють плитки між шарами. Реакція не потрібна взагалі: усе вирішується після ходу.

## Поле і час
- Квадратна сітка довільного розміру; рівень може бути більшим за екран (автори радять тримати все видимим).
- Два шари: видимий світ і **bizarro-світ** (прихований двійник тієї ж сітки); у редакторі перемикаються клавішею Y. Гравець, роботи й бомби в обміні шарів не беруть участі.
- Хід = один крок гравця (або поштовх без кроку); потім за порядком ходять роботи (за номером), останніми — бомби; обмін шарів панелями — в кінці ходу. Лазери й вихід перевіряються лише після ходу (рівень може стартувати з гравцем під лазером або на виході).
- Анімація не впливає на результат: «нічого не можна обігнати».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок 4 напрямки; штовхає; гине від лазера, вибуху, робота на своїй клітині |
| Підлога | terrain | — | прохідна |
| Rough | terrain | — | гравець ходить, блок сюди не заштовхнути |
| Червоний блок | object | — | зсувається на 1 від поштовху |
| Сірий блок | object | — | як червоний + засипає дірку |
| Синій блок | static | — | нерухомий; декоративні stop/стрілки — те саме |
| Зелений блок | object | — | після одного поштовху стає синім |
| Золотий блок | object | — | ковзає до упору; гравець лишається на місці |
| Кулі (синя/червона/зелена/звичайна) | object | колір | як золото; поштовх суцільного ряду куль запускає крайню («колиска Ньютона») |
| Сталь / кольорова сталь | object | колір | ряд сталі зсувається разом; кольорова вмикає панель свого кольору |
| Блоки LR / UD | object | вісь | рухаються лише вздовж своєї осі; на панелі не заштовхуються |
| Блоки 0 / 1 | static | — | натиск міняє всі LR ↔ UD |
| Broken | static | — | поштовх руйнує його в підлогу, гравець стоїть |
| Дірка | terrain | — | непрохідна, доки сірий блок не засипле |
| Trap2 → Trap1 | terrain | стадія 2/1 | зійшов з Trap2 → Trap1; зійшов з Trap1 → дірка |
| Вихід | static | — | стати на нього живим = перемога |
| Sleeping door | gate | — | синій блок, доки не зібрано всі серця |
| Heart framer | pickup | — | зібрати всі → прокидаються двері й сплячі роботи; до того блокують лазер і роботів |
| Лазер | hazard | напрям | убиває гравця на прямій лінії без перешкод |
| Black | static | — | непрохідний, лазер пропускає |
| Електрична підлога | hazard | — | гравця не пускає; блок, заштовхнутий сюди, знищується |
| Кнопка ON / OFF | switch | — | ON вимикає всю електрику (→ підлога) і стає інертною OFF |
| Транспортер | static | ціль | ступив — переніс у фіксовану клітину |
| Дроти NS/NE/NW/SE/SW/WE, хрест NSWE | object | конектори | несуть імпульс; штовхаються як червоні; тиснуть панелі |
| Кнопка (button) | switch | — | шле імпульс у всі приєднані дроти |
| Лампи B/R/G | switch | колір | кожен імпульс перемикає підлоги свого кольору; 2 імпульси = 0, 3 = 1 |
| Кольорова підлога up/down | gate | колір, стан | down — прохідна як rough; up — суцільна стіна |
| Панель (сіра) | switch | ціль | край події «наїхав / зʼїхав» міняє цільову клітину між шарами |
| Кольорова панель B/R/G | switch | колір | спрацьовує лише від кулі або сталі свого кольору |
| Remote panel | switch | ціль | спрацьовує від імпульсу, передає його далі; не штовхається |
| Транспондер | object | пара | передає електрику «по повітрю» іншому транспондеру; промінь блокують ті ж плитки, що й лазер, і сам гравець |
| Broken / sleeping bot | object | — | стоїть, штовхається як блок |
| Hugbot | enemy | номер | крок до гравця, з перевагою горизонталі |
| Dalek | enemy | номер | рухається як hugbot; заходить в електрику; зіткнення з роботом — злиття |
| Бомба | object | запал 0–10 | поштовх запалює; щохід −1; на 0 — вибух |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, red_block)` → ЯКЩО `free(cell_behind)` and not `cell(cell_behind, rough)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `enter(grey_block, hole)` → ТО `disappear_a`, `set_cell(hole, floor)`.
- КОЛИ `after(push)` → ЯКЩО `state(block, green)` → ТО `transform(blue_block)`.
- КОЛИ `contact(player, gold_block)` → ЯКЩО `free(cell_behind)` → ТО `slide(gold_block, dir)` (гравець не рухається).
- КОЛИ `contact(player, sphere)` → ЯКЩО `custom: «за кулею суцільний ряд куль»` → ТО `slide(last_sphere, dir)`; решта ряду лишається.
- КОЛИ `contact(player, steel)` → ЯКЩО `custom: «за рядом сталі є вільна клітина»` → ТО `push` (увесь ряд).
- КОЛИ `contact(player, lr_block)` → ЯКЩО `custom: «напрям поштовху вздовж осі блока»` and `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `contact(player, zero_one_block)` → ТО `transform(lr_blocks → ud, ud_blocks → lr)`.
- КОЛИ `contact(player, broken)` → ТО `set_cell(broken, floor)`.
- КОЛИ `leave(player, trap2)` → ТО `set_cell(trap2, trap1)`; КОЛИ `leave(player, trap1)` → ТО `set_cell(trap1, hole)`.
- КОЛИ `enter(block, electric)` → ТО `disappear_a`; гравець в електрику — `block`.
- КОЛИ `enter(player, on_button)` → ТО `set_cell(all_electric, floor)`, `transform(off_button)`.
- КОЛИ `enter(player, transporter)` → ТО `teleport`.
- КОЛИ `contact(player, button)` → ТО `custom: «імпульс у всі зʼєднані дроти»`.
- КОЛИ `custom: «імпульс дійшов до лампи кольору c»` → ТО `custom: «перемкнути всі підлоги кольору c up ↔ down»`.
- КОЛИ `enter(obj, panel)` або `leave(obj, panel)` → ТО `custom: «обміняти цільову клітину з bizarro-шаром»` (наприкінці ходу).
- КОЛИ `enter(colored_sphere|colored_steel, panel_same_color)` → ЯКЩО `same(obj, panel, color)` → ТО `custom: «обмін шарів»`.
- КОЛИ `custom: «імпульс дійшов до remote panel»` → ТО `custom: «обмін шарів, імпульс іде далі»`.
- КОЛИ `picked(player, heart)` → ЯКЩО `count(heart, =, 0)` → ТО `transform(sleeping_door → exit)`, `transform(sleeping_bot → bot)`.
- КОЛИ `turn_end(player)` → ТО `custom: «кожен робот за номером робить крок до гравця»` (hugbot / dalek).
- КОЛИ `contact(dalek, electric)` → ТО `disappear_a`; КОЛИ `contact(dalek, robot)` → ТО `custom: «злиття в broken bot»`.
- КОЛИ `contact(player, bomb)` → ТО `push`, `set_state(bomb, lit)`, `counter(fuse, n)`.
- КОЛИ `turn_end` → ЯКЩО `state(bomb, lit)` → ТО `counter(fuse, -1)`.
- КОЛИ `counter(fuse, =, 0)` → ТО `explode(adjacent, floor)`: роботи поруч знищені, сусідні бомби детонують, багато плиток → підлога.
- КОЛИ `turn_end` → ЯКЩО `line_of_sight(laser, player)` → ТО `lose`.
- КОЛИ `turn_end` → ЯКЩО `occupied(player_cell, robot)` або `custom: «гравець на/поруч з вибухом»` → ТО `lose`.
- КОЛИ `turn_end` → ЯКЩО `cell(player_cell, exit)` → ТО `win`.
- Перемога: стати на вихід живим (після перевірки лазерів). · Поразка: лазер, вибух, робот у клітині гравця. · Рахунок: нема; є довжина розвʼязку (найкоротший вивантажується як рекорд).

## Керування і ввід
- Стрілки — крок/поштовх; Enter — рестарт рівня; Esc — головне меню; U — undo (з 2005), redo — окремо (з 2006).
- Головне меню цифрами: 1 — грати, 2 — редактор, 3 — оновити гру, 4 — оновити колекції рівнів, T — наступний туторіал, R — зареєструвати гравця.
- Екран рівнів: Ctrl+R — оцінити, Ctrl+C — коментар, Ctrl+U — вивантажити рівень/розвʼязок; Ctrl+M — розвʼязки рівня.
- Редактор: ЛКМ — малювати плиткою, ПКМ — рамка виділення, СКМ — піпетка, P — тест, Y — bizarro-шар, [ ] — зум, Ctrl+стрілки — зсув виділення, Shift+стрілки — розмноження патерну.

## Вікна, меню, HUD
- `main-menu`: Load/Play → `level-select`; Edit → `editor-window`; Upgrade; Update levels; Tutorial; Register.
- `level-select` (load screen): колекції (Official / Triage / Quarantine), ✓ біля розвʼязаних, рейтинги; дії rate/comment/upload.
- `game-screen`: рівень (назва, автор), поле; HUD мінімальний (?).
- `solutions-window` (Ctrl+M): збережені розвʼязки, вибір для вивантаження, позначка speedrun.
- `editor-window`: палітра плиток (другий ряд), перемикач шарів, тест.
- `custom-window`: реєстрація гравця; діалог оцінки (style/difficulty) після проходження з пропозицією вивантажити розвʼязок.
- `end-screen` (?): рівень пройдено → оцінка.
- Переходи: main-menu → level-select → game-screen → (вихід) оцінка/upload → level-select.

## Фічі поза полем
- `level-editor` з тестом і bizarro-шаром; `level-sharing` автоматично через сервер (GPL-ліцензія на завантажене).
- `user-levels-browser` у грі й на сайті; колекції Official / Triage (усе нове) / Quarantine — модерація.
- `level-rating` (style, difficulty) лише для зареєстрованих; коментарі видно на сайті.
- Сервер гарантує, що кожен рівень розвʼязний: вивантажити можна лише рівень, який сам розвʼязав.
- Розвʼязки зберігаються у файлі гравця; найкоротший/перший вивантажується, `replay` розвʼязку; позначка speedrun.
- `undo` / `redo`, `restart-level`; `tutorial`-рівні; автооновлення гри.

## Варіації й родичі
- Родичі: [adventures-of-lolo](adventures-of-lolo.md) (серця відкривають вихід, ворог-«погляд»), Chip's Challenge (каталог плиток), [sokoban](sokoban.md); з thinky — DROD (покрокові роботи-переслідувачі).
- Осі варіацій:
  - **як рухається блок від поштовху**: на 1 (червоний) / до упору (золото) / передача імпульсу ряду (кулі) / ряд цілком (сталь) / лише вздовж осі (LR/UD) / один раз (зелений);
  - **як передається сигнал**: дотик кнопки → дроти → лампа (поле перемикається) / по повітрю (транспондер) / через remote panel;
  - **скільки шарів у поля**: один / два з обміном клітин (bizarro);
  - **панель спрацьовує**: на фронті «наїхав/зʼїхав» (Escape) / поки щось стоїть (типова кнопка Chip's).

## Цікавинки для курсу
- Таблиця взаємодій «що робить поштовх у кожну з ~40 плиток» як дані, не if-и — 🥈 (масштаб і пріоритети).
- Кулі «колиска Ньютона»: знайти кінець суцільного ряду і запустити крайню ковзати — 📎.
- Дроти з конекторами + лампи з парністю імпульсів (2 = 0) — обхід графа провідників — 🥉.
- Bizarro-шар: два масиви плиток, панель міняє клітину між ними на фронті події, обмін наприкінці ходу — 🥉.
- Порядок фаз ходу: гравець → роботи за номером → бомби → обмін шарів → перевірка лазерів і виходу — 🥉.
- Вивантаження рівня лише з власним розвʼязком + перевірка розвʼязку сервером реплеєм — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ червоні/сірі/дроти; `inertia-slide` ↔ золото й кулі; `fill-hole` ↔ сірий блок у дірці; `destructible-blocks` ↔ broken; `beam-tracing` + `line-of-sight-attack` ↔ лазер; `button-toggle` ↔ ON/OFF, кнопки й лампи; `teleport-one-way` ↔ транспортер; `chase-greedy` ↔ hugbot/dalek; `explode-area` + `chain-detonation` ↔ бомби; `environment-death`, `touch-death`; `collect-all` ↔ серця; `reach-exit`; `interaction-table`; `undo-redo` + `redo` + `restart-level`; `in-game-editor` + `editor-palette` + `editor-playtest`; `level-exchange` + `level-bank` + `level-rating` ↔ сервер рівнів; `replay` + `state-as-data` ↔ розвʼязки.
- **Нема** → пропозиції карток:
  - `+two-layer-field` «Поле з прихованим двійником, панелі міняють клітини між шарами» · entities/state · 🥉.
  - `+signal-wires` «Дроти-плитки несуть імпульс від кнопки до ламп, перемикання за парністю» · entities/interact · 🥉.
  - `+sphere-cradle` «Поштовх ряду куль запускає крайню» · entities/move · 📎.
  - `+axis-locked-block` «Блок рухається лише вздовж своєї осі» · entities/legality · 🌱.
  - `+one-push-block` «Після поштовху блок фіксується» · entities/state · 🌱.
  - `+trap-stages` (вже пропонована) — підлога руйнується після N сходів.
  - `+collect-to-wake` «Зібрав усі — прокидаються двері й вороги» · game-logic/win · 🌱.
  - `+robot-turn-order` «Вороги ходять у фіксованому порядку після гравця» · entities/move · 📎.
  - `+solution-upload` «Розвʼязок як доказ розвʼязності при вивантаженні» · levels/solvability · 🥈.
  - `+moderated-collections` «Official / Triage / Quarantine» · levels/bank · 📎.

## Пропозиції до словників
- `+trigger:signal_rise` — імпульс дійшов до лампи / remote panel (уже пропонований у схемотехнічних іграх).
- `+effect:pulse` — пустити імпульс по графу дротів від кнопки.
- `+effect:switch_layer` — обміняти клітину між видимим і bizarro-шаром.
- `+effect:toggle_cell` — перемкнути стан клітини up ↔ down (кольорові підлоги).
- `+cond:on_axis` — напрям поштовху збігається з віссю блока (LR/UD).
- `+role:robot` — ворог, що ходить у порядку номерів після гравця (відрізняти від real-time `enemy`) (?).
- `+feature:upload-requires-solution` — рівень приймається сервером лише з розвʼязком автора.
- `+feature:moderated-collections` — колекції рівнів за статусом модерації.
- `+feature:speedrun-solutions` — вивантаження найкоротшого розвʼязку як рекорду.
- `+window:upload-dialog` — оцінка + пропозиція вивантажити після проходження.
- `+card:two-layer-field`, `+card:signal-wires`, `+card:sphere-cradle`, `+card:robot-turn-order`.

## Джерела
- ⭐ [escape.txt — документація Beta 3 (2010)](http://escape.spacebar.org/win32/escape.txt) — правила, усі плитки, bizarro, роботи, бомби, керування, редактор, колекції, рейтинги, розвʼязки.
- [Офіційний сайт](http://escape.spacebar.org/) — платформи (Windows/macOS/Linux), автооновлення, браузер рівнів, коментарі.
- [Changelog](http://escape.spacebar.org/win32/changelog) — дати undo, redo, бомб, bizarro, рейтингів.
- [Браузер рівнів](http://escape.spacebar.org/levels.shtml) — мініатюри, автори, топи за style/difficulty.
- YouTube: пошук «Escape Tom 7 puzzle gameplay».

## Непевне
- (?) Рік: copyright 1996–2010, changelog починається 13.05.2004; перший публічний реліз (2003?) не перевірено — у шапці 2004.
- (?) Hugbot: «штовхає гравця замість обіймів» — документ сформульовано неоднозначно; чи hugbot убиває — не зрозуміло.
- (?) Dalek: «walking into the player kills» — переказ; чи гине гравець, чи dalek, — перевірити в грі.
- (?) Зона вибуху бомби — «adjacent»: 4 чи 8 сусідів не сказано.
- (?) Точна поведінка транспондерів і remote panel у ланцюгах; вміст HUD ігрового екрана; чи є окремий end-screen.
- (?) Чи кольорова сталь може стояти на звичайній (сірій) панелі.
