---
title: Pipe Mania (Pipe Dream)
slug: pipe-mania
family: connect-rotate
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1989
platforms: [Amiga, Atari ST, DOS, Windows, NES, Game Boy, C64, ZX Spectrum, arcade, PS2, DS, PSP]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pipe_Mania", best: true, note: "правила, спецтруби, рахунок, бонус-раунд, версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pipe+Mania+gameplay", note: "пошук; геймплей Amiga/DOS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pipe+Dream+Windows+Entertainment+Pack", note: "пошук; Windows-версія"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Pipe+Mania", note: "пошук; ремейк 2008"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BioShock", note: "Pipe Mania як міні-гра злому"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, event-points, progress-acceleration, sequential-levels, score-records, game-pause, game-screen, end-screen, main-menu, +piece-queue, +flow-propagation, +replace-with-penalty, +pipe-connectors, +one-way-cell, +wrap-edges, +min-length-goal, +crossing-bonus, +reservoir-delay, +sliding-bonus-round, +level-password]
proposes: ["+role:source", "+role:sink", "+role:conduit", "+trigger:flow_enter", "+trigger:flow_blocked", "+cond:ports_match", "+effect:advance_flow", "+ui:flow-countdown", "+ui:distance-counter", "+window:bonus-round", "+card:piece-queue", "+card:flow-propagation", "+card:replace-with-penalty"]
author: opus
date: 2026-11-02
---

# Pipe Mania — будуй трубопровід з черги випадкових труб, поки за тобою біжить «флуз»

## Суть
Гравець бере трубу з черги (не обирає і не крутить її) і кладе в будь-яку порожню клітину, прокладаючи шлях від джерела. За таймером із джерела починає текти рідина — «флуз» — і йде трубами клітина за клітиною; щойно вона дійде до відкритого кінця чи краю, рівень закінчено. Треба, щоб флуз пройшов не менше N труб. Ядро — гонка «будівельник проти фронту потоку» з випадковою чергою: план постійно ламає наступна труба, а невдалу трубу можна замінити лише зі штрафом.

## Поле і час
- Квадратна сітка (оригінал Amiga/DOS — близько 10×7 (?)); одне джерело зі стартовим напрямком. На полі лише один шар — труби, перешкоди, спецклітини.
- Real-time: відлік до старту потоку (скорочується з рівнем), далі флуз заповнює кожну трубу за фіксований час; з рівнями потік швидшає, а мінімальна довжина росте.
- У пізніх рівнях — отвори на краях: протилежні краї звʼязані, потік виходить з одного боку й заходить з другого (тор).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джерело (start) | source (custom) | напрям виходу | після відліку випускає флуз в один бік |
| Флуз | object | швидкість, позиція фронту | тече трубами; на кожному стику переходить у сусідню клітину, якщо порти збігаються |
| Пряма труба ─ / │ | object | 2 порти | пропускає вздовж осі |
| Коліно ×4 (┌ ┐ └ ┘) | object | 2 порти | повертає потік на 90° |
| Хрест ┼ | object | 4 порти, 2 незалежні канали | потік іде прямо; можна пройти двічі (горизонталь + вертикаль) → бонус |
| Диспенсер (черга) | container | 5 труб видно | кладеш нижню, зверху падає нова випадкова |
| Порожня клітина | static | — | сюди можна покласти трубу |
| Перешкода | static | — | не можна будувати |
| Заздалегідь покладена труба | static | — | не замінюється; бонус, якщо флуз пройде через неї |
| Резервуар | object | час заповнення | флуз затримується на кілька секунд — додатковий час |
| Одностороння труба | object | напрям | пропускає потік лише в один бік |
| Кінцева труба (end piece) | sink (custom) | — | флуз має закінчитися в ній, інакше програш навіть з довжиною |
| Отвір на краю | terrain | пара протилежних країв | переносить потік на протилежний край |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `cell(cell, empty)` → ТО `spawn_at(queue.bottom, cell)`, `custom: «черга зсувається, зверху нова випадкова труба»`.
- КОЛИ `input(click, cell)` → ЯКЩО `occupied(cell, pipe) and not state(pipe, filled) and not cell(cell, preplaced)` → ТО `transform(queue.bottom)`, `score(-n)`, `custom: «коротка затримка перед наступним кладінням»`.
- КОЛИ `timer(countdown)` → ТО `custom: «флуз виходить із джерела»`.
- КОЛИ `timer(flow_step)` → ЯКЩО `ports_match(front_cell, next_cell)` → ТО `advance_flow`, `set_state(next_cell, filled)`, `score(+n)`, `counter(distance, -1)`.
- КОЛИ `timer(flow_step)` → ЯКЩО `not ports_match(front_cell, next_cell)` або `edge(front)` без отвору → ТО `custom: «флуз витікає — рівень закінчено»`.
- КОЛИ `flow_enter(cross)` → ЯКЩО `state(cross, filled_other_axis)` → ТО `score(+bonus)`; 5 перетинів за рівень → великий бонус.
- КОЛИ `flow_enter(reservoir)` → ТО `custom: «потік стоїть, доки резервуар не заповниться»`, `score(+bonus)`.
- КОЛИ `flow_enter(one_way)` → ЯКЩО `not moving(flow, allowed_dir)` → ТО `custom: «вхід заборонено = витік»`.
- КОЛИ `edge(front)` → ЯКЩО `cell(edge, opening)` → ТО `wrap(front)`.
- КОЛИ `level_end` → ЯКЩО `counter(distance, <=, 0) and (not has_end_piece or flow_in(end_piece))` → ТО `score(-unused_pipes)`, `next_level`; інакше `game_over`.
- КОЛИ `level_end` → ТО `score(+bonus × (filled - min_length))` за кожну трубу понад мінімум.
- КОЛИ `counter(level, %4, 0)` → ТО `window(bonus-round)`: поле-«пʼятнашки» з однією діркою, зсуваєш труби, рахунок за довжину шляху; наприкінці — пароль.
- Перемога рівня: довжина ≥ мінімуму (+ кінцева труба, якщо є). Поразка: флуз витік раніше за мінімум — кінець гри (життів нема).
- Рахунок: + за кожну заповнену трубу, − за заміну, − за невикористані труби на полі, бонуси за хрест, резервуар, заздалегідь покладену трубу, довжину понад мінімум.

## Керування і ввід
- Миша/курсор (консолі — хрестовина) і одна кнопка: клік по порожній клітині — покласти; по своїй незаповненій трубі — замінити.
- Повертати чи обирати трубу не можна — лише місце; це й робить чергу головним обмеженням.
- Кнопка прискорення потоку («fast flow»), коли трубопровід готовий, — щоб не чекати й отримати бонус часу (?).

## Вікна, меню, HUD
- `main-menu` (оригінал): старт, кількість гравців (?), пароль.
- `game-screen`: поле, ліворуч диспенсер — `next-piece-preview` на 5 труб, `score`, `level-number`, `distance-counter` (скільки труб ще потрібно), `flow-countdown` (шкала до старту потоку), `cursor`.
- `level-password` — ввести пароль із бонус-раунду, щоб почати з потрібного рівня.
- `custom-window` бонус-раунд (кожні 4 рівні): поле-«пʼятнашки» з трубами.
- `end-screen`: підрахунок рівня (труби, бонуси, штраф за невикористані); `game over`.
- `leaderboard` — таблиця рекордів з імʼям.
- Переходи: main-menu → game-screen → (довжина ок) end-screen рівня → game-screen наступного; кожен 4-й → бонус-раунд → пароль; витік → game over → leaderboard.

## Фічі поза полем
- `levels-sequential` з наростанням: швидший потік, коротший відлік, довший мінімум, нові спецтруби.
- `level-password` після бонус-раунду замість збереження.
- `leaderboard-local`; `pause`.
- Двоє гравців на одному полі (Amiga/DOS) (?).
- Аркадна версія (Video System, 1990) — інша схема: зʼєднати джерело і злив випадковими трубами.

## Варіації й родичі
- Pipe Dream (Lucasfilm, США) — та сама гра; Windows-версія в Microsoft Entertainment Pack.
- Pipe Mania (2008, ремейк), Pipe Dreams 3D (2000), міні-гра злому в BioShock (2007), клони Wallpipe, Oilcap, MacPipes.
- Осі варіацій: **труба з черги / вільний вибір / обертання наявної** (Pipe Mania ↔ Infinity Loop) · **потік за таймером / потік лише в кінці** · **мета — довжина / зʼєднати джерело і злив** (аркада, BioShock) · **заміна дозволена зі штрафом / заборонена**.

## Цікавинки для курсу
- Труба як бітмаска портів (N/E/S/W) і перевірка стику двох клітин — 🌱; основа всієї сімʼї.
- Фронт потоку, що просувається по трубах за таймером (хрест — два незалежні канали, резервуар — затримка) — 🥉.
- Черга з 5 випадкових фігур + заміна зі штрафом і затримкою — 📎.
- Тор через отвори на краях — 📎.
- Бонус-раунд «пʼятнашки з трубами» і пошук найдовшого шляху — 🥈 (пошук найдовшого шляху в графі труб від джерела).
- Підрахунок рівня з усіма бонусами й штрафами як окремий екран — 🌱.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `event-points` (за трубу, хрест, резервуар) · `progress-acceleration` (швидший потік) · `sequential-levels` · `score-records` · `game-pause` · `game-screen` · `end-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+piece-queue` «Черга наступних фігур» · entities/spawn · 📎 · слоти {visible: 5, random: uniform} — Pipe Mania, Tetris-подібні.
  - `+flow-propagation` «Фронт потоку по зʼєднаннях» · game-logic · 🥉 · слоти {step_time, start_delay}.
  - `+replace-with-penalty` «Заміна фігури зі штрафом» · entities/legality · 🌱 · слоти {penalty, delay}.
  - `+pipe-connectors` «Плитка-зʼєднувач з портами» · entities/state · 🌱 — бітмаска сторін, спільна для сімʼї.
  - `+one-way-cell` «Одностороння клітина» · entities/legality · 🌱.
  - `+wrap-edges` «Обгортання країв (тор)» · entities/move · 📎.
  - `+min-length-goal` «Мінімальна довжина шляху» · game-logic/win · 🌱 · слот {min_length}.
  - `+crossing-bonus` «Бонус за подвійний прохід хреста» · game-logic/score · 🌱.
  - `+reservoir-delay` «Клітина-затримка потоку» · entities/interact · 🌱.
  - `+sliding-bonus-round` «Бонус-раунд-пʼятнашки» · levels · 🥈.
  - `+level-password` «Вхід на рівень за паролем» · interface/menus · 🌱.

## Пропозиції до словників
- `+role:source` — джерело потоку/променя (старт труб, лазер); `+role:sink` — приймач (кінцева труба, злив, рецептор); `+role:conduit` — клітина, що проводить потік (труба, дзеркало), не `object`, бо сенс — у портах.
- `+trigger:flow_enter(cell)` — фронт потоку зайшов у клітину; `+trigger:flow_blocked` — фронту нема куди йти (витік).
- `+cond:ports_match(a, b)` — порти двох сусідніх клітин стикуються.
- `+effect:advance_flow` — просунути фронт потоку на клітину.
- `+ui:flow-countdown` — шкала до старту потоку; `+ui:distance-counter` — скільки ще труб до мети.
- `+window:bonus-round` — окремий міні-рівень з іншими правилами між звичайними.
- `+card:piece-queue`, `+card:flow-propagation`, `+card:replace-with-penalty` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Pipe Mania](https://en.wikipedia.org/wiki/Pipe_Mania) — повний опис: диспенсер на 5, заміна зі штрафом, резервуари, односторонні й кінцеві труби, отвори на краях, рахунок, бонус-раунд із паролем, версії.
- [Wikipedia: BioShock](https://en.wikipedia.org/wiki/BioShock) — Pipe Mania як міні-гра злому.
- YouTube: пошук «Pipe Mania gameplay» і «Pipe Dream Windows Entertainment Pack».
- Steam: пошук «Pipe Mania» (ремейк 2008).

## Непевне
- (?) Розмір поля 10×7 і точні очки (за трубу, штраф за заміну/невикористані) — з памʼяті, у Wikipedia чисел нема; різняться між портами.
- (?) Кнопка прискорення потоку («fast flow») — є в Windows/консольних версіях за памʼяттю, Wikipedia її не згадує.
- (?) Режим на двох гравців в Amiga/DOS — не перевірено.
- (?) Набір односторонніх труб і кінцевої труби — в яких саме портах зʼявляються; Wikipedia каже лише «пізні рівні».
