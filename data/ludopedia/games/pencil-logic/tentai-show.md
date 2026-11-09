---
title: Tentai Show (Galaxies, Spiral Galaxies)
slug: tentai-show
aka: [Galaxies, Spiral Galaxies, Tentaisho, Sym-a-Pix, 天体ショー, Галактики]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/tentai_show/", best: true, note: "Nikoli: 4 правила, чорні/білі зірки, картинка з чорних блоків, значення назви"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tentai_Show", note: "назви, правила, NP-повнота (Friedman 2002 та ін.), техніки розвʼязання"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/galaxies.html", note: "Tatham Galaxies: ребра, стрілки-нагадування, автопідсвітка валідних областей, Unreasonable"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html", note: "Galaxies у браузері"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/tentaisho.js", note: "puzz.link: правила EN/JP, Nikoli vol.96, коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tentai+show+galaxies+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, edge-marking, cell-click, keyboard-controls, drag-drop-piece, connectivity-check, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, undo-redo, seed-share, import-open-formats, in-game-editor, +symmetric-region, +region-done-shade, +owner-arrow, +picture-reveal, +solve-into-undo]
proposes: ["+cond:point_symmetric", "+cond:count_in", "+effect:draw_edge", "+ui:owner-arrow", "+ui:region-done-shade", "+window:params-dialog", "+card:symmetric-region", "+card:owner-arrow", "+card:picture-reveal"]
author: opus
date: 2026-11-09
---

# Tentai Show (Galaxies) — розріж поле на області, кожна центрально-симетрична навколо своєї зірки

## Суть
На прямокутній сітці розкидано точки-«зірки»: у центрі клітинки, на ребрі або у вершині. Гравець проводить межі по лініях сітки, ділячи поле на «галактики»: кожна — звʼязна, містить рівно одну зірку і симетрична відносно неї при повороті на 180°. У версії Nikoli зірки чорні й білі: зафарбувавши галактики з чорними зірками, отримуєш картинку. Незвичне: обмеження — **геометрична симетрія області**, а центр симетрії може лежати не в клітинці, а на ребрі чи вершині.

## Поле і час
- Прямокутна сітка W×H (Tatham, Custom: Width/Height).
- Зірки — у трьох видах позицій: центр клітинки, середина ребра, вершина (Wikipedia); зірка на ребрі чи вершині «торкається» кількох клітинок, і всі вони — в одній галактиці.
- Шари: зірки (незмінні) · межі гравця по ребрах · стрілки-нагадування (Tatham) · підсвітка готових областей.
- Межа поля — теж стіна.
- Час статичний; хід = провести/стерти ребро межі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | належність до галактики | має належати рівно одній галактиці |
| Зірка (біла) | static | позиція: клітинка / ребро / вершина | центр симетрії своєї галактики; межа через неї заборонена |
| Зірка (чорна) | static | позиція | те саме + галактику зафарбовують для картинки (Nikoli) |
| Ребро межі | mark | є / нема | гравець проводить по пунктирних лініях сітки |
| Галактика | zone | клітинки, зірка | звʼязна, одна зірка, поворот на 180° навколо зірки переводить її в себе |
| Стрілка-нагадування | mark | клітинка → зірка | показує, до якої зірки гравець відніс клітинку; на перевірку не впливає (Tatham) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge)` → ТО `custom: «провести або стерти межу на ребрі»` (`+effect:draw_edge`) (Tatham).
- КОЛИ `input(right_drag, star → cell)` → ТО `mark(cell, arrow_to_star)` (Tatham: стрілка з точки на клітинку).
- КОЛИ `input(right_drag, arrow → cell)` → ТО `move(arrow, cell)`; кинута за поле → `unmark(arrow)`.
- КОЛИ `tick` під час drag → ТО `rotate(arrow, toward_star)` (Tatham: стрілка весь час крутиться, щоб дивитися на свою зірку).
- КОЛИ `pattern(region_closed)` → ЯКЩО `count(star, ==, 1)` and `custom: «область точково-симетрична навколо зірки»` (`+cond:point_symmetric`) → ТО `custom: «область підсвічується як готова»` (Tatham).
- КОЛИ `constraint_broken(star_edge)` → ЯКЩО `custom: «межа проходить через зірку»` → ТО конфлікт (puzz.link `bdPassStar`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області нема зірки»` (`+cond:count_in`) → ТО конфлікт (puzz.link `bkNoStar`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `custom: «в області дві чи більше зірок»` (`+cond:count_in`) → ТО конфлікт (puzz.link `bkPlStar`).
- КОЛИ `constraint_broken(region)` → ЯКЩО `not custom: «точкова симетрія навколо зірки»` (`+cond:point_symmetric`) → ТО конфлікт (puzz.link `bkNotSymSt`).
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «проведені межі — рівно ребра між клітинками різних галактик»` → ТО `win` (Tatham: зайве ребро всередині галактики теж помилка).
- Картинка (Nikoli): КОЛИ `win` → ТО `paint(region, black)` для галактик з чорними зірками → видно силует.
- Дедукція «сусідні зірки»: між сусідніми клітинками, що містять зірку або її частину від різних зірок, — межа (Wikipedia).
- Дедукція «дзеркальна стіна»: кожна відома межа галактики має симетричну навколо зірки; межа поля — теж стіна, тож віддзеркалюється всередину (Wikipedia).
- Дедукція «досяжність»: клітинку, до якої може дотягнутися лише одна зірка, віддати їй (Wikipedia).
- Дедукція «симетричний образ»: клітинка може належати зірці, лише якщо її образ при повороті навколо зірки теж вільний для неї (Wikipedia).
- Перемога: поле розбито повністю, кожна галактика звʼязна, з однією зіркою в центрі симетрії. Поразки й рахунку нема.

## Керування і ввід
- Tatham: лівий клік по лінії сітки — провести/стерти ребро.
- Права кнопка: drag із зірки на клітинку — стрілка-нагадування; правий клік по стрілці — підняти й перенести; кинути за поле — видалити.
- Клавіатура: стрілки — рух між клітинками й лініями; Return на лінії — ребро; на зірці — підняти стрілку; на іншій зірці/стрілці — опустити (на зірку чи стрілку — видалити).
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve, game ID, seed, save file, Preferences.
- puzz.link: межі по пунктиру мишею (?).

## Вікна, меню, HUD
- `game-screen`: сітка з пунктиром, зірки (чорні/білі в Nikoli), межі гравця, стрілки-нагадування (`+ui:owner-arrow`), підсвітка готових галактик (`+ui:region-done-shade`).
- Tatham: меню Game (Enter game ID…, Enter random seed…, Download save file…, Upload save file…, Preferences…) · Type (пресети + Custom…) · кнопки New game, Restart game, Undo move, Redo move, Solve game.
- `+window:params-dialog` (Custom…): Width, Height, Difficulty (найвища — Unreasonable).
- `help-window` — «Full instructions»; puzz.link — сторінка правил.
- Переходи: Type → Custom → генерація → game-screen; вся сітка підсвічена → розвʼязано.

## Фічі поза полем
- `undo` / `redo`, `auto-solve`, `seed-input`, `share-code`, збереження у файл (Tatham).
- `custom-difficulty`: розмір і складність; Unreasonable може вимагати backtracking.
- puzz.link: `level-editor` (розставити зірки) + URL пазла.
- Nikoli: журнальні пазли з картинкою (Sym-a-Pix у Conceptis-назві (?)).

## Варіації й родичі
- Перша поява — Puzzle Communication Nikoli vol.96 (puzz.link); у Tatham — внесок James Harvey.
- Варіант з картинкою: чорні й білі зірки, зафарбування чорних галактик дає малюнок (Nikoli, Wikipedia: «multicolor»).
- Родичі «розбий на області»: [Shikaku](shikaku.md) (прямокутники заданої площі), [Fillomino](fillomino.md) (області за розміром), [Nurikabe](nurikabe.md), [LITS](lits.md); колекція [Tatham](tatham-collection.md).
- Картинка як підсумок: [Nonogram](nonogram.md).
- **Осі варіацій**: позиції центрів (клітинка / ребро / вершина) · симетрія (поворот 180° / дзеркальна / 90°) (?) · одноколірні / двоколірні зірки з картинкою · межі ребрами / фарбування клітинок за зіркою.

## Цікавинки для курсу
- Перевірка симетрії області: образ клітинки (x, y) навколо центру (cx, cy) — (2cx − x, 2cy − y) у напівцілих координатах — 🌱.
- Розбиття за проведеними ребрами на компоненти (flood fill) + перевірка «одна зірка, симетрія» → автопідсвітка готових — 📎.
- Стрілка-нагадування, що під час drag повертається до своєї зірки, — 📎.
- Розвʼязувач «досяжність + симетричний образ» з пропагацією — 🥇.
- Генератор: випадкове ростання симетричних областей з насінин до покриття + перевірка єдиності — 🥇; задача NP-повна (Friedman 2002) — 👑 як дослідження.
- Картинка з чорних галактик (Sym-a-Pix): генерація пазла під заданий силует — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `edge-marking` ↔ межі по ребрах · `cell-click`, `keyboard-controls` · `drag-drop-piece` ↔ перенос стрілки · `connectivity-check` ↔ галактика звʼязна · `unique-puzzle-generation`, `difficulty-levels`, `level-solver`, `field-size-picker`, `game-settings` · `undo-redo`, `seed-share`, `import-open-formats`, `in-game-editor` (puzz.link).
- Перевикористано: `+region-done-shade` (з Shikaku), `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+symmetric-region` «Область симетрична навколо центру» · game-logic/constraints · 📎 · слот {center: cell|edge|vertex, sym: rot180|mirror}.
  - `+owner-arrow` «Стрілка-нагадування від клітинки до її власника» · interface/input · 📎.
  - `+picture-reveal` «Розвʼязок дає картинку» · game-logic/constraints · 🌱 — Tentai Show з чорними зірками, Nonogram.

## Пропозиції до словників
- `+cond:point_symmetric` — множина клітинок переходить у себе при повороті на 180° навколо точки.
- `+cond:count_in` — кількість сутностей виду в області = N (повтор зі Star Battle).
- `+effect:draw_edge` — провести/стерти межу на ребрі між клітинками.
- `+ui:owner-arrow` — стрілка від клітинки до її власника.
- `+ui:region-done-shade`, `+window:params-dialog` — повтори.
- `+card:symmetric-region`, `+card:owner-arrow`, `+card:picture-reveal` — див. мапу.

## Джерела
- ⭐ [Nikoli: Tentai Show](https://www.nikoli.co.jp/en/puzzles/tentai_show/) — 4 правила, чорні/білі зірки, картинка, значення назви «ten-tai-show».
- [Wikipedia: Tentai Show](https://en.wikipedia.org/wiki/Tentai_Show) — назви (Galaxies, Spiral Galaxies, Sym-a-Pix), позиції зірок, NP-повнота (Friedman 2002; Fertin et al. 2015; Demaine et al. 2021), чотири техніки.
- [Tatham: Galaxies](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/galaxies.html) — керування ребрами й стрілками, автопідсвітка, Unreasonable, James Harvey.
- [Galaxies у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html) — меню й кнопки.
- [puzz.link: tentaisho.js](https://puzz.link/js/pzpr-samples/tentaisho.js) — правила EN/JP, «Nikoli vol. 96», коди помилок.
- YouTube: пошук «tentai show galaxies puzzle».

## Непевне
- (?) Рік першої появи (Nikoli vol.96) — номер бачив, рік — ні.
- (?) Sym-a-Pix — назва Conceptis для кольорового варіанту; сторінку Conceptis не відкривав.
- (?) Варіанти з дзеркальною чи 90°-симетрією — з власних знань.
- (?) Введення меж у puzz.link і права кнопка — не перевіряв.
- (?) Чи Tatham вважає помилкою зайве ребро всередині галактики, чи лише не підсвічує її — документація каже «розвʼязано, коли лінії рівно межі між областями».
