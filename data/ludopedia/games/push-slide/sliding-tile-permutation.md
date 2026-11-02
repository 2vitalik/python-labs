---
title: Sliding-tile permutation puzzles (пʼятнашки й родичі)
slug: sliding-tile-permutation
family: push-slide
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 1880
platforms: [wooden, PC, web, mobile, board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/15_puzzle", best: true, note: "правила, історія, інваріант парності, 80 ходів, NP-hard оптимум, евристики A*"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/fifteen.html", note: "Fifteen у браузері (Tatham)"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/fifteen.html", note: "довідка Fifteen: керування, преференс «рухати плитку / дірку», підказка h"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/sixteen.html", note: "Sixteen — зсув ряду/стовпця по колу"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/sixteen.html", note: "довідка Sixteen: shuffle limit, стрілки по краю"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/twiddle.html", note: "Twiddle — обертання блока n×n"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/twiddle.html", note: "довідка Twiddle: розмір блока, орієнтація, «одне число на ряд»"}
  - {kind: play, url: "https://www.loopover.xyz/", note: "Loopover — 2D-«Рубік» на торі зі спідкуб-таймером"}
  - {kind: other, url: "https://github.com/Loopover", note: "Loopover org: BFS/God's number, хешування дошки"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/Sliding_puzzle", note: "огляд жанру, теорія груп для n×m"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/netslide.html", note: "Netslide — зсув рядів як у Sixteen, але збирається мережа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Loopover+speedsolve", note: "пошук; спідсолви Loopover"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rubik%27s+Race+game+how+to+play", note: "пошук; правила Rubik's Race"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, swipe-gestures, drag-drop-piece, completion-detection, unsolvable-states, level-solver, difficulty-levels, field-size-picker, game-settings, movement-animation, score-records, leaderboard, profile-stats, hot-seat, logic-render-split, state-as-data, property-tests, +undo-redo, +wrap-edges, +rotate-2x2, +seed-share, +solve-into-undo, +move-vs-step, +state-string, +slide-into-gap, +shift-line, +parity-check, +scramble-by-moves, +speedsolve-timer, +orientation-goal, +race-to-pattern]
proposes: ["+trigger:input", "+trigger:pattern", "+cond:same", "+effect:swap", "+effect:shift", "+effect:rotate", "+effect:wrap", "+effect:counter", "+effect:timer", "+role:tile", "+ui:move-counter", "+ui:timer-elapsed", "+ui:par-moves", "+ui:target-preview", "+window:stats-window", "+window:mode-select", "+feature:seed-input", "+feature:mode-speedrun", "+feature:custom-difficulty", "+axis:move-kind"]
author: opus
date: 2026-11-02
---

# Sliding-tile permutation — переставити плитки в порядок одним видом ходу

## Суть
Парасолька над «пʼятнашками» та їхніми нащадками: поле — перестановка пронумерованих плиток, гравець має лише **один тип ходу** (зсунути плитку в дірку / зсунути весь ряд по колу / повернути блок 2×2), і мусить повернути поле в упорядкований стан. Гра — жива ілюстрація теорії груп: хід — генератор групи перестановок, половина станів класичних «пʼятнашок» **нерозвʼязна** через парність, і генератор пазла мусить це знати. Різновиди відрізняються саме генератором ходу — тому вони в одному файлі: Fifteen, Sixteen, Twiddle, Loopover, Rubik's Race.

## Поле і час
- Квадратна сітка W×H (класика 4×4; Tatham — будь-який W×H; Loopover — N×N, типово 5×5 (?); Rubik's Race — 5×5 з однією діркою).
- Один шар: кожна клітина — плитка з міткою (число / літера / колір); у Fifteen і Rubik's Race одна клітина — порожня «дірка».
- Топологія ходу різна: Fifteen — звичайна сітка з краями; Sixteen і Loopover — **тор по рядах і стовпцях** (зсунута за край плитка зʼявляється з протилежного боку того самого ряду); Twiddle — без тору, обертаються вікна n×n, що повністю лежать у полі.
- Час: `static` — світ не змінюється без ходу; лічильник ходів. Loopover і Rubik's Race — спідсолв: секундомір від першого ходу (Loopover) або змагання двох гравців на швидкість (Rubik's Race) — але час лише метрика, правила від нього не залежать.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка Fifteen | tile | номер 1..W·H−1 | сусідня з діркою зсувається в неї; клік у рядку/стовпці дірки зсуває кілька разом |
| Дірка Fifteen | terrain | позиція | порожня клітина; хід = обмін дірки з сусідньою плиткою |
| Плитка Sixteen | tile | номер 1..W·H | зсувається лише разом з усім рядом/стовпцем; дірки нема |
| Стрілка краю Sixteen | switch (UI) | ряд/стовпець, напрям | клік → циклічний зсув ряду/стовпця на 1 |
| Плитка Twiddle | tile | номер; опц. орієнтація 0..3 | обертається разом з блоком n×n навколо його центру; опц. орієнтація теж повертається |
| Блок обертання Twiddle | zone | розмір n (2 базово) | вікно n×n; клік ЛКМ — проти год. стрілки, ПКМ — за |
| Плитка Loopover | tile | літера/число й колір рядка (?) | зсувається з рядом/стовпцем по тору; drag на N клітин = N кроків (?) |
| Плитка Rubik's Race | tile | 6 кольорів (?) | як у Fifteen: зсув у дірку; кілька підряд в одному ряду — одним рухом |
| Скремблер Rubik's Race | spawner | 9 кубиків з 6 кольоровими гранями (?) | трусиш → центральний 3×3 зразок для обох гравців |
| Ціль (зразок) | zone | упорядкування / 3×3 патерн | Fifteen/Sixteen/Twiddle/Loopover — рядки по порядку; Rubik's Race — центр 3×3 = зразок |

## Правила (КОЛИ → ЯКЩО → ТО)
- Fifteen: КОЛИ `input(dir)` → ЯКЩО `occupied(cell_next_to_gap_in_dir, tile)` → ТО `swap(tile, gap)`, `counter(moves, +1)`; інакше `block`. Преференс Tatham «Move the gap» інвертує напрям стрілки.
- Fifteen (миша): КОЛИ `input(click(cell))` → ЯКЩО `same(row|col, cell, gap)` → ТО `custom: «зсунути всі плитки між діркою і клітиною; дірка опиняється під курсором»`; Tatham рахує кожну плитку окремо (?), класична метрика «multi-tile» — один хід.
- Sixteen: КОЛИ `input(edge_arrow(line, dir))` → ТО `shift(line, dir)` + `wrap(last_tile)`, `counter(moves, +1)`; ПКМ — у протилежний бік.
- Twiddle: КОЛИ `input(click(centre_of_block))` → ТО `rotate(block_n×n, ±90°)`; ЯКЩО `mode(orientable)` → кожна плитка блока теж `rotate(tile, ±90°)` (і центральна при непарному n).
- Loopover: КОЛИ `input(drag(row|col, k))` → ТО `shift(line, k)` з `wrap`; `counter(moves, +k)` (?); перший хід запускає `timer(start)`.
- Rubik's Race: КОЛИ `input(slide)` → як Fifteen; КОЛИ `pattern(centre3x3 == scrambler)` → ТО `custom: «гравець закриває поле планкою — перемога в раунді»` (?).
- КОЛИ `pattern(all_in_order)` → ТО `win`; Tatham: статус-рядок «COMPLETED! Moves: N», флеш поля; Loopover: `timer(stop)`, запис у статистику.
- Twiddle «One number per row»: ціль — усі «1» у першому ряду, «2» — у другому…; `cond: same(tile, row_label)`.
- Twiddle «Orientation matters»: ціль додатково — усі трикутники вгору (`state(tile, orient=0)`).
- **Парність (Fifteen):** інваріант = парність перестановки 16 клітин (з діркою) XOR парність манхеттенської відстані дірки від правого нижнього кута; кожен хід міняє обидві — тож половина розстановок недосяжна (Johnson & Story, 1879). Знаменита «14-15 переставлені» Сема Лойда нерозвʼязна.
- **Парність (Sixteen / Loopover):** зсув ряду довжини W — цикл довжини W; при непарних W і H кожен хід — парна перестановка, тож досяжні лише парні; якщо хоч один вимір парний — досяжне все. Tatham при W, H непарних примусово робить перестановку парною (міняє дві останні плитки).
- **Парність (Twiddle):** поворот 2×2 — 4-цикл (непарна перестановка), тож обмеження на позиції нема; сумарна орієнтація при n=2 змінюється на ±4 ≡ 0 (mod 4) (?) — Tatham перемішує випадковими ходами від розвʼязку і не перевіряє інваріант, а додає +0/1 хід «щоб уникнути проблем парності».
- Генерація: (а) випадкова перестановка + виправлення парності обміном двох останніх (Fifteen, Sixteen); (б) N випадкових ходів від розвʼязку без взаємно-скасовних пар (Sixteen/Twiddle з `shuffle limit`; Twiddle за замовчуванням `W·H·n²·2` ходів); (в) фізичний скремблер (Rubik's Race).
- Перемога: упорядковано / центр = зразок. · Поразка: нема (Rubik's Race — суперник закінчив першим). · Рахунок: кількість ходів (+ ціль «target N» при shuffle limit), час (Loopover, Rubik's Race).

## Керування і ввід
- Fifteen (Tatham): ЛКМ у рядку/стовпці дірки — зсув кількох плиток; стрілки — зсув сусідньої плитки; `h` — підказка наступного ходу (повторне `h` врешті розвʼязує).
- Sixteen: ЛКМ по стрілці на краю — зсув ряду в напрямку стрілки, ПКМ — навпаки; курсор по краю + Enter; Ctrl/Shift+стрілка — рухати конкретну плитку (з курсором / без); Enter і Space — «залипаючі» Ctrl і Shift.
- Twiddle: клік у точку, де сходяться 4 плитки (2×2) або в центральну плитку (непарне n); ЛКМ — проти год. стрілки, ПКМ — за; клавіатура: стрілки водять рамку, Enter / Space — обертання.
- Loopover: перетягування ряду/стовпця мишею або пальцем (drag = кілька кроків одразу), клавіатурні схеми для спідсолву (?).
- Rubik's Race: фізично великим пальцем зсуваєш плитки; цифрова версія — клік/свайп як у Fifteen.
- Спільні дії Tatham: N — нова, U/Ctrl+Z — undo, R/Ctrl+R — redo, Restart, Solve, Specific/Random Seed (ID гри).

## Вікна, меню, HUD
- `game-screen`: поле; HUD — `move-counter` («Moves: N», «(target N)» при обмеженому перемішуванні; «Moves since auto-solve: N» після Solve), `timer-elapsed` (Loopover), `selection-highlight` (рамка блока Twiddle, курсор по краю Sixteen).
- `settings-window` (Tatham «Type → Custom…»): Width, Height; Sixteen — Shuffle limit; Twiddle — Rotating block size, One number per row, Orientation matters, Shuffle limit. Пресети розмірів у меню Type (`difficulty-select`).
- `custom-window` «Specific…/Random Seed…» (Tatham): ввід/показ ID пазла — відтворення генерації.
- `settings-window` Preferences: напрям стрілок «Move the tile / Move the gap» (Fifteen).
- `stats-window` (Loopover, цифрова версія спідкубу): середні ao5/ao12, найкращий час, історія спроб (?).
- `mode-select` (Loopover): розмір N×N, режими/«івенти» (?) ; `leaderboard` — онлайн-рекорди (?).
- `end-screen`: у Tatham — лише флеш і «COMPLETED!» у статус-рядку, окремого вікна нема.
- `help-window` — довідка Tatham, `about-window`.
- Переходи: Game → New → game-screen; Type → Custom → settings-window → нова гра; Solve → game-screen у розвʼязаному стані (крок історії, можна undo).

## Фічі поза полем
- `undo` ∞ / `redo` (Tatham — через усю сесію, навіть після save/load); `restart-level`.
- `auto-solve` як крок історії (`+solve-into-undo`); Fifteen — покрокова `hint`.
- `seed-display` / `seed-input` / `share-code` — game ID `params:desc`; `save-game` / load у файл.
- `custom-difficulty`: розмір поля, кількість перемішувальних ходів; Twiddle — розмір блока, орієнтація, режим «ряд = одне число».
- Loopover: `mode-speedrun` (секундомір, скрембл), `stats`, `leaderboard-online` (?); спільнота рахувала **God's number** (BFS по всіх станах) для малих розмірів.
- Rubik's Race: `hotseat`-змагання двох, `local-multiplayer` у фізичній версії.

## Варіації й родичі
- **Генератор ходу** (головна вісь): зсув плитки в дірку (Fifteen, Rubik's Race) · циклічний зсув ряду/стовпця (Sixteen, Loopover, Netslide) · обертання блока n×n (Twiddle, Ro (?)) · зсув частини ряду (Rubik's Slide (?)) · блоки різних розмірів (→ [klotski](klotski.md), [rush-hour](rush-hour.md)).
- **Тор**: нема (Fifteen) / по рядах і стовпцях (Sixteen, Loopover) — також Yoshi's Cookie (→ `falling-match`).
- **Що таке «порядок»**: числа по рядах · літери (Loopover) · картинка (фото-пʼятнашки) · орієнтація теж (Twiddle orientable) · групи однакових («одне число на ряд») · шаблон 3×3 у центрі (Rubik's Race) · мережа зʼєднань (Netslide).
- **Метрика ходу**: одна плитка = хід (15-puzzle «single-tile», макс. 80) · ряд будь-якої довжини = хід («multi-tile», макс. 43) · зсув ряду на k = k ходів чи 1 (Loopover) (?).
- **Перемішування**: випадкова перестановка з виправленням парності · N ходів від розвʼязку (шукати зворотний шлях) · фізичний скремблер.
- **Розмір**: 8-puzzle (3×3), 15, 24 (5×5 — ~7.76·10²⁴ станів), довільний W×H.
- Історія: Noyes Chapman (Канастота, NY), виробник Matthias Rice — «Gem Puzzle»; манія в США 1880 р.; Сем Лойд з 1891 р. приписував собі винахід і обіцяв $1000 за нерозвʼязну «14-15».

## Цікавинки для курсу
- Fifteen з кліком «зсунь усі між діркою і курсором» + лічильник — 🌱 (одна функція swap).
- Перевірка розвʼязності за парністю (інверсії + рядок дірки) і генератор, що її гарантує — 📎 (класичне «чому половина нерозвʼязна»).
- Sixteen/Loopover: циклічний зсув ряду + умовна парність (обидва виміри непарні) — 📎; drag ряду мишею з прилипанням до клітин — 🥉.
- Twiddle: обертання вікна n×n з орієнтацією плиток — 🥉 (індексна арифметика + стан орієнтації).
- Перемішування «N ходів від розвʼязку без скасовних пар» + режим «знайди зворотний шлях за N» — 📎.
- Оптимальний розвʼязувач 8-puzzle BFS — 🥉; 15-puzzle IDA* з манхеттенською евристикою (+ linear conflict) — 🥇; God's number Loopover 3×3/4×4 BFS з хешем станів — 🥇.
- Rubik's Race: два поля + скремблер-зразок + гонка (hot-seat на одному екрані або проти AI) — 🥈.

## Мапа на каталог
- Є: `cell-click` ↔ клік-зсув; `keyboard-controls` ↔ стрілки/рамка; `swipe-gestures` + `drag-drop-piece` ↔ drag ряду (Loopover); `completion-detection` ↔ «упорядковано»; `unsolvable-states` ↔ нерозвʼязні 50 % (парність); `level-solver` ↔ Solve/hint; `difficulty-levels` + `field-size-picker` + `game-settings` ↔ Type/Custom; `movement-animation` ↔ анімація зсуву; `score-records` + `leaderboard` + `profile-stats` ↔ час/ходи Loopover; `hot-seat` ↔ Rubik's Race; `state-as-data` ↔ game ID; `property-tests` ↔ «генератор завжди розвʼязний»; `logic-render-split` ↔ мід-енд Tatham.
- **Нема** → пропозиції карток:
  - `+slide-into-gap` «Зсув плитки в дірку» · entities/move · 🌱 · слот {multi: bool} — хід = обмін з порожнечею; multi — увесь відрізок до курсора.
  - `+shift-line` «Циклічний зсув ряду/стовпця» · entities/move · 📎 · слот {wrap: bool} — Sixteen, Loopover (родич `row-conveyor`, але за вводом).
  - `+rotate-2x2` (є в корпусі) — обертання блока, слот {n, orientable}.
  - `+wrap-edges` (є) — тор по рядах/стовпцях.
  - `+parity-check` «Перевірка розвʼязності за парністю» · levels/solvability · 📎 — інверсії + позиція дірки / непарні виміри.
  - `+scramble-by-moves` «Перемішування N ходами від розвʼязку» · levels/generation · 📎 · слот {moves, no_cancel}.
  - `+speedsolve-timer` «Секундомір спідсолву від першого ходу» · interface/hud · 🌱 · слоти {inspection, averages: ao5|ao12}.
  - `+orientation-goal` «Орієнтація плитки як частина цілі» · game-logic/win · 📎 — Twiddle orientable (родич `orientation-state`, але без перекочування).
  - `+race-to-pattern` «Гонка до випадкового зразка» · game-logic/win · 🥉 — Rubik's Race.
  - Повтор корпусу: `+undo-redo`, `+seed-share`, `+solve-into-undo`, `+move-vs-step` (single-tile vs multi-tile), `+state-string` (game ID).

## Пропозиції до словників
- `+trigger:input` — клік/стрілка/drag; `+trigger:pattern` — `all_in_order` / `centre3x3 == sample`.
- `+cond:same` — плитка і мітка ряду однакові (режим «одне число на ряд»).
- `+effect:swap` (плитка ↔ дірка), `+effect:shift` (ряд/стовпець), `+effect:rotate` (блок і орієнтація плитки), `+effect:wrap` (вихід з протилежного боку ряду), `+effect:counter` (ходи), `+effect:timer` (старт/стоп секундоміра).
- `+role:tile` — уся гра з плиток без аватара.
- `+ui:move-counter` з «(target N)», `+ui:timer-elapsed`, `+ui:par-moves`, `+ui:target-preview` (зразок Rubik's Race).
- `+window:stats-window` (ao5/ao12), `+window:mode-select` (розмір/івент Loopover).
- `+feature:seed-input`, `+feature:mode-speedrun`, `+feature:custom-difficulty` (розмір + глибина перемішування).
- `+axis:move-kind` — один генератор ходу на всю гру: `gap-slide` · `line-shift` · `block-rotate`; саме ця вісь розрізняє ігри парасольки.

## Джерела
- ⭐ [Wikipedia: 15 puzzle](https://en.wikipedia.org/wiki/15_puzzle) — інваріант парності (Johnson & Story 1879), історія Chapman/Rice/Loyd, 80 single-tile / 43 multi-tile, NP-hard оптимум, евристики.
- [Tatham: Fifteen (довідка)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/fifteen.html) — керування, преференс напрямку, підказка `h`.
- [Tatham: Sixteen (довідка)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/sixteen.html) — зсув рядів по колу, Shuffle limit, клавіатурна схема.
- [Tatham: Twiddle (довідка)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/twiddle.html) — розмір блока, орієнтація, «ряд = одне число».
- [Tatham: Netslide](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/netslide.html) — той самий хід Sixteen над задачею Net.
- [Fifteen](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/fifteen.html) · [Sixteen](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/sixteen.html) · [Twiddle](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/twiddle.html) — грати в браузері.
- [Loopover](https://www.loopover.xyz/) — сайт гри (сторінка — SPA, текст не прочитано).
- [Loopover на GitHub](https://github.com/Loopover) — репозиторії God's number (BFS, C++/Python), хешування дошки; активність 2018–2019.
- [Wikipedia: Sliding puzzle](https://en.wikipedia.org/wiki/Sliding_puzzle) — огляд, теорія груп для n×m, Rubik's Slide.
- Код Tatham (дзеркало ghewgill/puzzles: `fifteen.c`, `sixteen.c`, `twiddle.c`) — генерація з виправленням парності, текст статус-рядка.

## Непевне
- (?) Loopover: точний рік (2018 за активністю репозиторіїв), автор (за памʼяттю — carykh), набір розмірів, режими/«івенти», метрика ходу drag, онлайн-лідерборд — сторінку сайту не прочитано (SPA), пошук вичерпано.
- (?) Rubik's Race: рік (~1982), видавець (Ideal (?)), 24 плитки 6 кольорів, скремблер з 9 кубиків, планка «готово» — з памʼяті; Wikipedia-статті немає.
- (?) Інваріант орієнтації Twiddle (сума mod 4) — виведено міркуванням, у коді Tatham не перевіряється; для n=3 поворот — два 4-цикли (парна перестановка), отже досяжні лише парні (?).
- (?) Чи рахує Tatham Fifteen клік, що зсуває кілька плиток, як один хід чи кілька — у довідці не сказано.
