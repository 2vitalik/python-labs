---
title: Liquidum
slug: liquidum
aka: [Liquidum Lite]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2024
platforms: [PC (Windows, macOS, Linux), iOS, Android, web (Liquidum Lite)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2716690/Liquidum/", best: true, note: "6 секцій, 70+ рівнів, приховані підказки, човни, діагоналі, daily з таблицями, Explorer, редактор + Workshop; трейлер"}
  - {kind: official, url: "https://github.com/MarvellousSoft/liquidum", note: "відкритий код (GPL-3.0, Godot 4): правила води, човнів, діагоналей і підказок у GridImpl.gd; тексти навчання в localizations.csv"}
  - {kind: other, url: "https://raw.githubusercontent.com/MarvellousSoft/liquidum/main/lite-web/src/i18n/locales/en.json", note: "Liquidum Lite: правила коротко, пензлі й клавіші, теми днів тижня"}
  - {kind: play, url: "https://marvelloussoft.github.io/liquidum/", note: "Liquidum Lite — веб-версія з щоденним пазлом"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2716690&count=20&maxlength=3000", note: "Steam News: палітри, Weekly marathon, Paint mode, cellhints (DLC Secrets of the Deep), «maybe boat», флери, iOS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Liquidum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [satisfy-constraints, completion-detection, markup-validity, line-sum-clue, neighbor-count-clue, cell-click, dot-mark, hover-highlight, conflict-highlight, undo-redo, restart-level, daily-puzzle, leaderboard, streak-stats, share-result, in-game-editor, level-exchange, unique-puzzle-generation, level-solver, difficulty-levels, rule-variants, level-select, level-unlock, theme-select, +water-level-check, +auto-flood-fill, +half-cell-triangles, +boat-on-water, +contiguity-clue, +basin-histogram-clue, +mistake-counter, +allow-mistakes-toggle, +auto-cross-line, +liar-clue, +snake-constraint, +knight-exclusion, +weekday-themes, +weekly-marathon, +paint-overlay]
proposes: ["+cond:water_level", "+effect:flood_to_level", "+cond:contiguous", "+ui:basin-panel", "+window:flair-picker", "+feature:allow-mistakes", "+card:boat-on-water", "+card:basin-histogram-clue", "+card:snake-constraint", "+card:weekday-themes"]
author: opus
date: 2026-11-19
---

# Liquidum — налий воду в акваріуми за підказками ліній: рівень спільний, човни пливуть, діагональні стінки ділять клітину навпіл

## Суть
Пазл-гібрид паперового Aquarium і нонограми від бразильської Marvellous Soft. Товсті стінки ділять поле на акваріуми; гравець позначає воду, а числа на краях кажуть, скільки води в кожному рядку й стовпці. Вода підкоряється гравітації: в акваріумі рівень спільний і вода не висить над порожнечею, тож клік по клітині заливає весь акваріум до рівня цього рядка.

Кампанія по одному додає діагональні стінки (половинка клітини = 0,5 води), човни над водою, приховані «?», серійність {N}/-N-, гістограму акваріумів і числа в клітинах (cellhints). Кожен рівень має єдиний розвʼязок, а хибний хід гра за замовчуванням відхиляє й рахує як помилку.

## Поле і час
- Квадратна сітка; клітина або ціла, або розрізана діагональною стінкою на два трикутники (`IncDiag` / `DecDiag` у коді), і кожна половинка має свій вміст.
- Стінки лежать на ребрах клітин і на діагоналях; блок `#` — непрохідна клітина. **Акваріум** — звʼязна множина половинок, не розділених стінками.
- Вміст половинки: порожньо · вода · X («no water») · човен (лише на цілій клітині) · нотатка «нема човна / може бути човен».
- Підказки: на смугах біля країв — вода на лінії (кількість, {N}, -N-, «?»), підказки човнів; окремо — загальна вода, загальні човни й панель «Aquariums Expected».
- Статичний пазл: таймер іде лише для статистики й таблиць рекордів, показ вмикається в налаштуваннях.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | terrain | ціла / діагональна (2 половинки) | вміщує воду: ціла = 1, половинка = 0,5 |
| Стінка | static | ребро або діагональ | ділить поле на акваріуми; вода крізь неї не тече |
| Блок `#` | static | — | непрохідна клітина; cellhint усередині блока не рахує себе |
| Акваріум | zone | обʼєм води | половинки без стінок між ними; рівень води спільний |
| Вода | mark | 1 або 0,5 | ставиться пензлем і розтікається вбік і вниз до рівня кліку |
| X («no water») | mark | — | необовʼязкова позначка «тут води нема»; поширюється вгору й убік |
| Човен | mark | — | лише на цілій клітині без стінки знизу, не в нижньому ряду; під ним має бути вода, сам він не вода |
| «Нема човна» / «?човен» | mark | — | нотатка гравця, на перевірку не впливає |
| Підказка лінії | static | N · {N} · -N- · ? | вода в рядку чи стовпці: кількість, одна серія, кілька серій, невідомо |
| Підказка човнів лінії | static | N | кількість човнів у рядку чи стовпці |
| Підказка акваріумів | static | список «обʼєм → кількість» | скільки басейнів кожного обʼєму на полі |
| Cellhint (число в клітині) | static | N · {N} · -N- | вода в квадраті 3×3 навколо; {N} / -N- — одна чи кілька плям |
| Загальні лічильники | static | вода, човни | сума на все поле |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(water, c)` → ЯКЩО `custom: «у розвʼязку в c є вода»` → ТО `fill(c)`: вода розтікається по акваріуму вбік і вниз, але не вище рядка c (`+effect:flood_to_level`).
- КОЛИ `input(water, c)` → ЯКЩО `custom: «у розвʼязку в c води нема»` and `not mode(allow_mistakes)` → ТО `block`, `counter(mistakes, +1)`, `animate(error)`, `sound(error)`.
- КОЛИ `input(water, c)` → ЯКЩО `mode(allow_mistakes)` → ТО `fill(c)` навіть хибно; лічильник помилок прихований, але в таблиці рекордів помилка йде.
- КОЛИ `input(eraser, c)` → ЯКЩО `occupied(c, water)` → ТО `unmark(c)` і `custom: «зникає вода цього рядка й вище в звʼязній частині акваріуму, а човни над нею знімаються»`; вода нижче лишається.
- КОЛИ `input(nowater, c)` → ТО `mark(c, x)`; з автопоширенням — `custom: «X розходиться вгору й убік по акваріуму»` (над X води бути не може).
- КОЛИ `input(boat, c)` → ЯКЩО `custom: «c ціла, без стінки знизу, не в нижньому ряду»` and `cell(below(c), water)` → ТО `mark(c, boat)`; якщо під c ще нема води — гра спершу робить `fill(below(c))`.
- КОЛИ `input(noboat, c)` → ТО `mark(c, maybe_boat)` (лише нотатка).
- Рівень води: ЯКЩО `custom: «в акваріумі вода не стоїть над порожньою половинкою й має один рівень у сполучених частинах»` (`+cond:water_level`).
- Підказка N: КОЛИ `counter(water_in_line, ==, N)` → ТО `set_state(hint, satisfied)`, `animate(wave_from_cell)`, `sound(complete)`; КОЛИ `counter(water_in_line, >, N)` → ТО `set_state(hint, wrong)`; менше — звичайний стан, навіть коли лінію закрито X.
- Половинки: кожен залитий трикутник дає `counter(water_in_line, +0.5)`.
- {N}: ЯКЩО `custom: «вода лінії — одна суцільна серія»` (`+cond:contiguous`); -N-: ЯКЩО `custom: «щонайменше дві серії з порожнечею між ними»`.
- КОЛИ `counter(water_in_line, ==, N)` → ЯКЩО `custom: «форма серій не та, що в {N} / -N-»` → ТО `set_state(hint, wrong)`.
- «?»: перевірки нема (прості «?» можна ховати в налаштуваннях); форма {?} / -?- без числа перевіряється лише за серійністю (?).
- Човни лінії: ЯКЩО `count(boat_in_line, ==, N)`; загальні підказки: `count(water, ==, W)`, `count(boat, ==, B)`.
- Акваріуми: ЯКЩО `custom: «кількість басейнів кожного обʼєму = списку панелі»` — статус лише «виконано / ще ні», без «wrong».
- Cellhint N у клітині c: ЯКЩО `adjacent_count(c, water, ==, N)` — квадрат 3×3, сама c теж, якщо вона не блок; {N} / -N- — `connected(water_in_3x3)` чи ні.
- КОЛИ `input(left_click, hint)` → ЯКЩО `state(hint, satisfied)` → ТО `mark(empty_cells_of_line, x)`.
- КОЛИ `input(right_click, hint)` → ТО `set_state(hint, faded)`.
- КОЛИ `custom: «вся вода й усі човни збігаються з розвʼязком»` → ТО `win`, `timer(stop)`, `window(end-screen)`; X ставити не обовʼязково.
- Режими Pandora («рівні з випадковими правилами») і острів Pandora's Passage додають правило поверх звичайних:
  - Sudoku — `unique(row)`, `unique(col)`, `unique(box3x3)` для кількості води 1–9;
  - Liar — `custom: «кожна числова підказка рівно на 1 більша чи менша за правду»`; Impostor — `custom: «рівно одна числова підказка бреше»`;
  - Snake — `custom: «уся вода — одна змійка, що не торкається себе сторонами»`;
  - Knight — `custom: «дві води на відстані ходу коня заборонені»`; Quad — `custom: «у кожному квадраті 2×2 є вода»`;
  - Symbols — `same(hint_a, hint_b, value)` для однакових символів, різні символи — різні значення; Pool — `region_size(water_group(c), N)` для cellhint; Mirrors — `custom: «вода й човни дзеркальні по горизонталі»`.
- Перемога: розвʼязок збігається. · Поразка: нема. · Рахунок: час і помилки (найкращий час, найменше помилок, серії перемог, таблиці daily і weekly).

## Керування і ввід
- Пензлі: вода, X («no water»), човен, «нема човна»; ЛКМ — поточний пензель, ПКМ — другорядний (X / «нема човна») або гумка, СКМ і коліщатко — зміна пензля, протяжка — кілька клітин (опція «Fill with drag»).
- Paint mode (з v1.2.0): кнопка-пензлик біля вибору пензлів — вільне малювання кольорами поверх поля, на перевірку не впливає.
- Клік по виконаній підказці — X у решту клітин лінії; ПКМ по підказці — притемнити її.
- Клавіатура (у Lite): W / X / B / N — пензлі, 1–4 і Tab — вибір; мобільні — тап, довгий тап, протяжка, тап по підказці підсвічує лінію.
- Undo / Redo, Restart з підтвердженням, Back — вихід зі збереженням; «Invert mouse buttons» у налаштуваннях.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Dive (кампанія) · Daily Level · Weekly marathon · Explorer mode · Create · Workshop levels · Extra islands · Profile · Settings · Credits · Exit.
- `level-select` (хаб секцій): 6 секцій кампанії, рівні відкриваються поступово; на рівні — «Completed», найкращий час, найменше помилок.
- `difficulty-select` (Explorer): Easy · Medium (з {N}/-N-) · Hard (діагоналі й човни) · Expert (будь-які правила кампанії) · Insane (після всієї кампанії); Endless — «Continue / New level»; кнопки Snake і Pandora's Box («Play more levels to unlock»).
- `game-screen`: поле з підказками на смугах (`line-clue`), `remaining-counter` води й човнів, `mistake-counter` «Mistakes:», `timer-elapsed` (опційно), `+ui:basin-panel` «Aquariums Expected», вибір пензля (`tool-palette`), `undo-button`, `redo-button`, `restart-button`, кнопка навчання, Share.
- `tutorial-window`: текст правила рівня під полем (кампанія й острови).
- `end-screen`: час і помилки; Continue · Play again («New … level» у Explorer) · Share; у марафоні — «Continue marathon (N left)» / «Finish marathon».
- `leaderboard`: daily і weekly, спільні для всіх платформ; кнопка-око ховає таблицю.
- `editor-window` (Create): стінки, діагоналі, блоки, підказки, перевірка єдиності «YES / NO / UNIQUE_TOO_HARD»; публікація в Workshop.
- `profile-window`: профілі; `+window:flair-picker` — значок-флер біля імені в таблицях.
- `settings-window`: Sound · Display · Gameplay · Controls — Allow mistakes, Show timer, Skip animations, Fill with drag, Invert mouse buttons, Dark mode, 4 палітри, товсті стінки, ховати прості «?», cellhints «total / remaining», розблокувати всі рівні.
- `confirm-dialog`: скинути рівень (у daily і weekly — «It will not reset the timer or mistakes»).
- `credits-window` — після останнього рівня кампанії («Thank you for playing»).
- Переходи: main-menu → level-select → game-screen → end-screen → наступний рівень / назад; Daily Level → game-screen → leaderboard; останній рівень → credits-window.

## Фічі поза полем
- `mode-daily` з темою дня тижня (так у Lite): пн — без особливих правил, вт — човни з прихованими підказками, ср — діагоналі без «?», чт — приховані підказки води й човни, пт — усі правила, сб — видно лише одну підказку рядка, нд — діагоналі й багато підказок акваріумів.
- `mode-marathon` — Weekly marathon: 10 рівнів поспіль, з паузою; `mode-endless` — Explorer: генерація з вибором складності й нескінченна серія.
- `level-editor` + `level-sharing` через Steam Workshop; механіки DLC у редакторі й Workshop-рівнях — безкоштовно.
- Острови-доповнення: Small & Tricky, Mirrors, Femme Fatale (DLC), Cryptic Caves (безкоштовний пак зі своїм генератором), Enigma Ebb (DLC Secrets of the Deep — cellhints), Reef Riddles, Marine Mysteries, Olympian Odyssey, Pandora's Passage (Snake).
- `streaks` (поточна й найкраща серія), `stats` (найкращий час, найменше помилок), `leaderboard-online`, `share-result` (текст у буфер), `achievements` (100 перемог на Insane — найважче).
- Щомісячні челенджі: ≥15 daily за місяць — флер; інший колір флера — ≥15 daily з ≤2 помилками.
- `undo`, `redo`, `restart-level`, `skip-animation`, `colorblind-palette`-подібні палітри, `high-contrast` (товсті стінки, більший текст підказок).
- Збереження в Steam Cloud; на мобільних — реклама після рівнів поза секціями 1–3.

## Варіації й родичі
- Паперовий предок — [aquarium.md](aquarium.md): та сама вода за рівнем і лічильники ліній; Liquidum додає діагоналі, човни, {N}/-N-, гістограму акваріумів і cellhints.
- {N}/-N- — з Hexcells (`hidden-deduction/hexcells.md`); половинки клітин — як у [shakashaka.md](shakashaka.md) і [slant.md](slant.md); cellhint 3×3 — сапер; Liar — [usowan.md](usowan.md); Knight і Sudoku — [sudoku-variants.md](sudoku-variants.md).
- Liquidum Lite — полегшена веб-версія з щоденним пазлом (окремий TypeScript-рушій у тому самому репозиторії).
- **Осі варіацій**: вміст клітини — ціла / 2 половинки · рідина — без фізики (нонограма) / рівень в акваріумі · обʼєкти над рідиною — нема / човни · підказка лінії — кількість / + серійність / «?» · глобальна підказка — сума / гістограма басейнів · правило-модифікатор — нема / Liar / Snake / Knight / Quad / Sudoku / Mirrors.

## Цікавинки для курсу
- Акваріум як граф половинок без стінок і «вода не вище рівня кліку» (DFS із мінімальним рядком) — 📎.
- Діагональна стінка ділить клітину на два трикутники з різними сусідами й вагою 0,5 у сумах ліній — 🥉.
- Човен: ставиться лише над водою, сам не вода, рахується окремою підказкою — 🌱.
- Гістограма акваріумів (скільки басейнів кожного обʼєму): компоненти звʼязності й підрахунок обʼємів — 📎.
- Перевірка ходу проти збереженого розвʼязку: відмова й лічильник помилок, а з «Allow mistakes» — пропустити, але рахувати — 🌱.
- Правила-модифікатори Pandora як підключувані перевірки (Liar ±1, Snake, Knight, Quad, Sudoku, Mirrors) — 🥉 за набір.
- Генератор Explorer: розвʼязувач стратегіями визначає єдиність і складність, рівні Easy…Insane — за набором дозволених правил — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection`; `markup-validity` ↔ статус «wrong»; `line-sum-clue` ↔ вода й човни на лінії; `neighbor-count-clue` ↔ cellhints 3×3; `cell-click`; `dot-mark` ↔ «?човен»; `hover-highlight` ↔ підсвітка рядка й стовпця; `conflict-highlight` ↔ «⚠ Over»; `undo-redo`, `restart-level`; `daily-puzzle`, `leaderboard`, `streak-stats`, `share-result`; `in-game-editor`, `level-exchange` ↔ Workshop; `unique-puzzle-generation`, `level-solver` ↔ перевірка єдиності; `difficulty-levels` ↔ Explorer; `rule-variants` ↔ Pandora; `level-select`, `level-unlock`; `theme-select` ↔ палітри й темний режим.
- **Нема** → пропозиції карток:
  - `+water-level-check`, `+auto-flood-fill` (повтор: aquarium).
  - `+half-cell-triangles` (повтор: shakashaka) «Діагональна стінка ділить клітину на два трикутники» · entities/state · 📎.
  - `+boat-on-water` «Обʼєкт стоїть лише над рідиною й рахується окремо» · game-logic/constraints · 🌱.
  - `+contiguity-clue` (повтор: hexcells) «{N} / -N-: одна серія чи кілька» · game-logic/constraints · 📎.
  - `+basin-histogram-clue` «Підказка: скільки басейнів кожного обʼєму» · game-logic/constraints · 📎.
  - `+mistake-counter` (повтор: hexcells) · `+allow-mistakes-toggle` «Відхиляти хибний хід чи пропускати й рахувати» · game-logic/lose · 🌱.
  - `+auto-cross-line` (повтор: nonogram) — клік по виконаній підказці ставить X.
  - `+liar-clue` (повтор) · `+snake-constraint` «Позначене — одна змійка без дотиків до себе» · game-logic/constraints · 📎 · `+knight-exclusion` «Дві позначки не на відстані ходу коня» · game-logic/constraints · 🌱.
  - `+weekday-themes` «Щоденний пазл з темою за днем тижня» · levels/bank · 🌱 · `+weekly-marathon` «10 рівнів поспіль раз на тиждень» · levels/bank · 🌱.
  - `+paint-overlay` «Вільне малювання поверх поля без впливу на перевірку» · interface/input · 🌱.

## Пропозиції до словників
- `+cond:water_level` — рівень води в акваріумі спільний, під водою нема порожнечі (повтор із aquarium).
- `+effect:flood_to_level` — залити акваріум до рівня кліку (повтор із aquarium).
- `+cond:contiguous` — позначене в лінії чи області — одна серія (повтор із hexcells).
- `+ui:basin-panel` — панель «Aquariums Expected» зі списком «обʼєм → кількість».
- `+window:flair-picker` — вибір значка-флера біля імені в таблицях.
- `+feature:allow-mistakes` — дозволити хибні ходи («як на папері»), не змінюючи підрахунку помилок.
- `+card:boat-on-water`, `+card:basin-histogram-clue`, `+card:snake-constraint`, `+card:weekday-themes` — див. мапу.

## Джерела
- ⭐ [Steam: Liquidum](https://store.steampowered.com/app/2716690/Liquidum/) — 6 секцій, 70+ рівнів, приховані підказки, човни, діагоналі, daily з таблицями, Explorer, редактор і Workshop; трейлер.
- [GitHub MarvellousSoft/liquidum](https://github.com/MarvellousSoft/liquidum) — відкритий код: `project/game/level/grid/GridImpl.gd` (розтікання й зняття води, X, човни, перевірка проти розвʼязку, статуси підказок, Pandora-правила), `Level.gd`, `GridView.gd`, `project/localization/localizations.csv` (тексти навчання й меню), `project/database/extra_levels/*/config.ini` (острови й DLC).
- [Liquidum Lite: en.json](https://raw.githubusercontent.com/MarvellousSoft/liquidum/main/lite-web/src/i18n/locales/en.json) — правила коротко, пензлі й клавіші, теми днів тижня.
- [Liquidum Lite](https://marvelloussoft.github.io/liquidum/) — веб-версія «Daily Logic Puzzles» (сторінка на JS, текст не читається).
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2716690&count=20&maxlength=3000) — v1.0.13–v1.3.4: палітри, товсті стінки, Weekly marathon, Paint mode, cellhints у DLC Secrets of the Deep, «maybe boat», флери, iOS.
- YouTube: пошук «Liquidum gameplay».

## Непевне
- (?) Що саме стоїть на правій і нижній смугах підказок (човни лінії чи допоміжні «лишилось») — у коді чотири смуги й лічильники човнів на лінії, вигляду не бачив.
- (?) Порядок, у якому кампанія вводить діагоналі, човни, «?», {N}/-N- і підказки акваріумів, — узято з туторіалів Lite; у Steam-кампанії може відрізнятись.
- (?) Які острови платні: у конфігах DLC-ідентифікатори стоять у кількох, Steam показує два DLC (Femme Fatale, Secrets of the Deep).
- (?) Теми днів тижня — з Lite-версії; Steam-сторінка каже лише «themed levels each weekday».
- (?) Розміри полів — чисел не бачив.
- (?) Symbols, Pool, Impostor є в текстах правил; у коді взаємодія Pool з Liar позначена «not implemented», а форма {?} / -?- без числа — моє прочитання коду.
