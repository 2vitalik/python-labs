---
title: Trainyard
slug: trainyard
family: connect-rotate
also: [program-robots, thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2010
platforms: [iOS, Android]
links:
  - {kind: official, url: "https://trainyard.ca/", best: true, note: "сайт гри: 100 + 50 бонусних пазлів, Express, обмін розвʼязками, редактор"}
  - {kind: official, url: "https://trainyard.ca/solutions", note: "усі пазли по містах із найкращим track count"}
  - {kind: official, url: "https://trainyard.ca/solutions/faq", note: "track count «20+7», унікальність розвʼязку, редактор, Express"}
  - {kind: other, url: "https://www.pocketgamer.com/trainyard/review/", note: "огляд: малювання колій, змішування, злиття, перемикання, швидкість, гумка"}
  - {kind: other, url: "http://www.148apps.com/reviews/trainyard/", note: "огляд 17.06.2010: перемикання, фарбування, сайт розвʼязків"}
  - {kind: other, url: "https://toucharcade.com/games/trainyard", note: "картка гри (з черги; 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Trainyard+Matt+Rix+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, swipe-gestures, game-screen, end-screen, level-select, level-unlock, level-bank, in-game-editor, level-exchange, completion-detection, game-pause, help-window, +path-drawing, +run-simulation, +track-budget, +color-mixing, +train-merge, +train-split, +paint-cell, +junction-toggle, +crash-on-mismatch, +speed-control, +erase-mode, +solution-sharing, +undo-redo]
proposes: ["+role:source", "+role:sink", "+role:conduit", "+trigger:input(drag)", "+trigger:exec(tick)", "+trigger:program_end", "+cond:same", "+cond:simultaneous", "+effect:extend_path", "+effect:mix", "+effect:merge", "+effect:split", "+effect:paint", "+effect:crash", "+effect:toggle_junction", "+ui:run-button", "+ui:speed-slider", "+ui:eraser-toggle", "+ui:train-queue", "+feature:colorblind-palette", "+feature:solution-sharing", "+axis:control=drag-path", "+card:color-mixing", "+card:train-merge", "+card:junction-toggle"]
author: opus
date: 2026-11-02
---

# Trainyard — намалюй колії, щоб поїзди доїхали до станцій свого кольору; кольори змішуються при зустрічі

## Суть
На сітці 7×7 (?) стоять станції-джерела, що випускають поїзди певних кольорів, і станції-цілі, що чекають поїзди певних кольорів. Гравець пальцем малює колії, натискає «Start» — і поїзди їдуть одночасно, по тіку. Ядро — **кольорова арифметика й таймінг**: два поїзди, що вʼїхали в одну клітину одночасно, зливаються в один і змішують кольори (червоний + синій = фіолетовий), фарбувальні клітини перефарбовують, роздільники розщеплюють поїзд на два. Помилка кольору чи виїзд у нікуди — аварія.

## Поле і час
- Квадратна сітка (7×7, ?); клітини: порожні (місце під колію), камені, станції, фарбувальники, роздільники.
- У клітині — **до двох колій** (пряма/поворот між будь-якими двома боками); дві колії = стрілка (junction) з активною і неактивною гілкою.
- Дві фази: **план** (статичне малювання) → **симуляція** (тіки; швидкість регулюється слайдером). Симуляцію можна зупинити, виправити колії, запустити знову.
- Поїзди рухаються синхронно, по клітині за тік; станція-джерело випускає по одному поїзду через інтервал.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Станція-джерело (outlet) | source (custom) | бік виходу; черга кольорів | після Start випускає поїзди по одному в заданому порядку |
| Станція-ціль (goal) | sink (custom) | список потрібних кольорів; відкриті боки | приймає поїзд потрібного кольору (знімає його зі списку); інший колір → аварія |
| Поїзд | object | колір: 3 основні, 3 змішані, коричневий | їде коліями; колір змінюється злиттям/фарбуванням |
| Колія | conduit (custom) | пара боків клітини | малюється гравцем; веде поїзд з одного боку на інший |
| Стрілка (2 колії в клітині) | switch | активна гілка | після проїзду поїзда активна гілка перемикається (?) |
| Камінь | static | — | на ньому не можна класти колію |
| Фарбувальник (painter) | terrain | колір; фіксований прямий проїзд | поїзд, що проїхав, набуває кольору фарбувальника |
| Роздільник (splitter) | terrain | бік входу | поїзд ділиться на два, що виїжджають ліворуч і праворуч; змішаний колір → дві складові (?) |
| Перехрестя | conduit (custom) | 2 прямі колії навхрест | поїзди проїжджають, не зʼєднуючись; одночасний проїзд змішує кольори (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cell_a→cell_b)` → ЯКЩО `free(cell)` and `not occupied(cell, rock|station)` → ТО `extend_path` (колія між боками входу й виходу пальця).
- КОЛИ `input(drag)` у клітині з колією → ТО `custom: «друга колія; клітина стає стрілкою»`; повторне проведення → зайві шматки ізолюються.
- КОЛИ `input(tap, junction)` → ТО `toggle_junction` (яка гілка активна на старті, ?).
- КОЛИ `input(erase, cell)` → ТО `set_cell(empty)`; `input(clear_all)` → прибрати всі колії.
- КОЛИ `input(start)` → ТО `custom: «фаза симуляції»`, джерела починають випускати поїзди.
- КОЛИ `exec(tick)` → ТО кожен поїзд `move(a, next_cell_by_track)`.
- КОЛИ `exec(tick)` → ЯКЩО `not custom: «є колія з боку входу»` (порожня клітина, камінь, край, обрив) → ТО `crash` — `lose`, симуляція зупиняється.
- КОЛИ `contact(train, junction)` → ТО поїзд їде активною гілкою; `after` → `toggle_junction` (?).
- КОЛИ `contact(train_a, train_b)` в одній клітині ЯКЩО `simultaneous` and `custom: «виїжджають одним боком»` → ТО `merge(a, b → c)`, колір c = `mix(a, b)`.
- КОЛИ `contact(train_a, train_b)` ЯКЩО зустрічні / навхрест одночасно → ТО `mix` кольорів обох, поїзди їдуть далі (?).
- КОЛИ `enter(train, painter)` → ТО `paint(train, painter.color)`.
- КОЛИ `enter(train, splitter)` → ТО `split(train)` → два поїзди ліворуч і праворуч від напрямку; основний колір → дві копії, змішаний → складові (?).
- КОЛИ `contact(train, goal)` → ЯКЩО `same(train, goal.next_needed, color)` → ТО `disappear_a`, `counter(goal_left, -1)`; інакше `crash`.
- Змішування: червоний+синій = фіолетовий · червоний+жовтий = помаранчевий · синій+жовтий = зелений · однакові → той самий колір · несумісне (напр. змішаний + інший) → коричневий (?).
- КОЛИ `all_constraints_met` (усі цілі отримали всі поїзди, жоден не розбився) → ТО `win`, `window(end-screen)`, `unlock(next)`.
- Перемога: усі цілі задоволені · Поразка: аварія (рестарт симуляції, колії лишаються) · Рахунок: у грі — зірки за пазл (?), на сайті — track count «N+M» (клітин з колією + з них подвійних; менше = краще).

## Керування і ввід
- Тач-drag: провести пальцем через клітини — колії кладуться за траєкторією (вхід/вихід пальця визначає форму).
- Тап по клітині-стрілці — змінити активну гілку (?); режим гумки — провести, щоб стерти; кнопка «стерти все».
- Кнопка Start/Stop; слайдер швидкості симуляції (змінювати можна на ходу, щоб побачити, де ламається).
- Помилки не карають: після аварії повернення до плану з намальованими коліями.

## Вікна, меню, HUD
- `main-menu`: Play → `map-window` (провінції/міста Канади — Abbotsford, Brampton … — як групи пазлів) → `puzzle-select` міста; Bonus; Editor; Settings.
- `game-screen`: поле, `run-button` (Start/Stop), `speed-slider`, `eraser-toggle`, кнопка «стерти все», `train-queue` — кольори, що лишились у джерелах/цілях (значки на станціях).
- `end-screen`: «Puzzle complete», перехід до наступного, кнопка поділитися розвʼязком (?).
- `help-window` / туторіал: короткі пояснення кожного нового елемента в перших ~40 рівнях.
- `editor-window` (пізні версії, не в Express): розставити станції, камені, фарбувальники, роздільники; опублікувати на сайт.
- `settings-window`: звук, режим для дальтоніків.
- Переходи: main-menu → map-window → puzzle-select → game-screen ⇄ (Start/аварія) → end-screen → наступний пазл.

## Фічі поза полем
- `puzzle-bank`: 100 основних + 50 бонусних пазлів; `level-unlock` по містах (?).
- `level-editor` + `user-levels-browser` + `level-sharing` (User-Made / Featured Puzzles на trainyard.ca).
- `solution-sharing`: розвʼязок завантажується на сайт; рейтинг за track count, унікальність — «не розвʼязано точно так само раніше».
- `speed-control`, `undo` (?), `colorblind-palette` (є за trainyard.ca і Pocket Gamer).
- Trainyard Express — безкоштовна версія з власним набором пазлів, без редактора.

## Варіації й родичі
- Родичі: Railbound (план колій → симуляція), Cosmic Express (одна колія, пасажири), Mini Metro, Pipe Mania (потік замість поїздів), SpaceChem/Opus Magnum (синхронні маніпулятори).
- Осі варіацій: **що несе колір: поїзд / пасажир / потік** · **зустріч двох: аварія / злиття / змішування** · **клітина: одна колія / дві зі стрілкою** · **оцінка: розвʼязано / мінімум колій** · **керування стрілкою: авто-перемикання / вручну**.

## Цікавинки для курсу
- Модель кольорів як множин основних (`{R}`, `{R,B}` …) — змішування = обʼєднання, коричневий = «більше двох» — 🌱; роздільник = розклад множини (?) — 📎.
- Синхронна симуляція: усі поїзди роблять крок разом, потім розвʼязуються зустрічі (злиття / змішування / аварія) — 🥉; коректне виявлення «зустрілись на ребрі між клітинами» — 🥈.
- Стрілка, що перемикається після кожного поїзда: клітина зі станом і двома гілками — 📎.
- Малювання колії drag-ом: з пари «звідки зайшов / куди вийшов палець» вивести тип колії — 📎.
- Track count «N+M» як метрика розвʼязку + перевірка унікальності розвʼязку (нормалізація стану поля) — 🥉.
- Редактор пазлів + обмін через файл/код — 🥈.

## Мапа на каталог
- Є: `cell-click` · `swipe-gestures` (drag колій) · `game-screen` · `end-screen` · `level-select` · `level-unlock` · `level-bank` · `in-game-editor` · `level-exchange` · `completion-detection` · `game-pause` (Stop) · `help-window`.
- **Нема** → пропозиції карток:
  - `+path-drawing` «Малювання шляху drag-ом» · interface/input · 📎 — з Flow Free; тут слот {per_cell: 2}.
  - `+run-simulation` «План → запуск симуляції» · game-logic · 🥉 — з Cosmic Express/Railbound.
  - `+track-budget` — з Railbound; тут не ліміт, а метрика якості (track count).
  - `+color-mixing` «Змішування кольорів при зустрічі» · entities/interact · 📎 · слот {rules: rgb|ryb, overflow: brown}.
  - `+train-merge` «Злиття двох рухомих в один» · entities/interact · 📎.
  - `+train-split` «Розщеплення на два» · entities/interact · 📎.
  - `+paint-cell` «Клітина-фарбувальник» · entities/interact · 🌱 (родич `cell-transform`, але змінює властивість, не тип).
  - `+junction-toggle` «Стрілка, що перемикається після проїзду» · entities/state · 📎.
  - `+crash-on-mismatch` «Аварія при невідповідності/обриві» · game-logic/lose · 🌱.
  - `+speed-control` «Слайдер швидкості симуляції» · interface/hud · 🌱.
  - `+erase-mode` «Режим гумки / стерти все» · interface/input · 🌱.
  - `+solution-sharing` «Публікація розвʼязку й рейтинг за ресурсом» · support/sites · 🥈.
  - `+undo-redo` «Undo ходів гравця» · game-logic · 📎.

## Пропозиції до словників
- `+role:source` / `+role:sink` / `+role:conduit` — джерело, станція-ціль, колія (підтвердження ×3).
- `+trigger:input(drag)`, `+trigger:exec(tick)` ⏳, `+trigger:program_end` ⏳ — симуляція скінчилась (усі поїзди доїхали або аварія).
- `+cond:simultaneous` — дві сутності входять у клітину в той самий тік (ключ до злиття).
- `+effect:extend_path` (з Flow Free); `+effect:mix(a, b)` — колір = змішування; `+effect:merge` ⏳ (тут для рухомих); `+effect:split(a)` — один → два; `+effect:paint(a, color)` ⏳ (`paint` для сутності, не клітини); `+effect:crash` ⏳ (×корпус: аварія програми); `+effect:toggle_junction` — перемкнути гілку.
- `+ui:run-button`, `+ui:speed-slider` (є `speed-slider` ⏳ — підтвердження), `+ui:eraser-toggle`, `+ui:train-queue` (значки кольорів на станціях).
- `+feature:colorblind-palette` ⏳ підтверджується; `+feature:solution-sharing` — розвʼязки на сайті з рейтингом.
- `+axis:control=drag-path` — ⏳ значення осі `control` підтверджується.

## Джерела
- ⭐ [trainyard.ca](https://trainyard.ca/) — опис гри, 100 + 50 бонусних, Android/iOS, Express, режим для дальтоніків, обмін розвʼязками.
- [Пазли й розвʼязки](https://trainyard.ca/solutions) — список пазлів по містах (Abbotsford … Niagara Falls), найкращий track count.
- [FAQ розвʼязків](https://trainyard.ca/solutions/faq) — track count «20+7» (клітини з колією + подвійні), унікальність, редактор, Express без редактора.
- [Pocket Gamer review](https://www.pocketgamer.com/trainyard/review/) — злиття синій+жовтий=зелений, перехрестя без аварії, перемикання і пріоритет, швидкість, гумка, 150 рівнів.
- [148Apps review](http://www.148apps.com/reviews/trainyard/) — 17.06.2010, ~40 туторіальних рівнів, перефарбування, сайт розвʼязків.
- YouTube: пошук «Trainyard Matt Rix gameplay».

## Непевне
- (?) Розмір поля 7×7 — з памʼяті; джерела не кажуть.
- (?) Точні правила роздільника (змішаний колір → складові, основний → дві копії) і змішування при зустрічі навхрест/лоб у лоб — з памʼяті; огляди кажуть лише «merge» і «cross without crashing».
- (?) Автоперемикання стрілки після кожного проїзду і тап для зміни гілки — з памʼяті; огляди згадують «junction changes» і «train priority».
- (?) Коричневий для несумісних сумішей, зірки за пазл, undo — не звірено.
- (?) Пошук (WebSearch) вичерпаний; Wikipedia-статті про гру нема (редирект на «Classification yard»); fandom віддає 402, TouchArcade/Gamezebo — 403.
