---
title: Simon Tatham's Portable Puzzle Collection
slug: tatham-collection
family: pencil-logic
also: [hidden-deduction, push-slide, connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2004
platforms: [PC, Linux, web, Android (port), iOS (port)]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/", best: true, note: "усі 40 ігор: грати в браузері, однорядкові правила, завантаження"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільна оболонка: меню Game/Type, game ID, seed, undo, solve"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/index.html", note: "мануал: розділ на кожну гру з правилами, керуванням і параметрами"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/devel/backend.html", note: "API бекенда гри: new_desc, interpret_move/execute_move, solve, status"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/bridges.html", note: "приклад веб-версії (js/<гра>.html)"}
  - {kind: wiki, url: "https://en.wikipedia.org/w/index.php?search=Simon+Tatham%27s+Portable+Puzzle+Collection&ns0=1", note: "пошук; стаття про збірку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simon+tatham+puzzles", note: "пошук; огляди"}
stage: v1
coverage: 65
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, hover-highlight, unique-puzzle-generation, difficulty-rating, difficulty-levels, level-solver, game-settings, field-size-picker, save-game, import-open-formats, state-as-data, logic-render-split, help-window, about-window, event-effects, mines-after-first-click, inertia-slide, +undo-redo, +state-string, +seed-share, +platform-shell, +move-string, +solve-into-undo, +edge-marking, +single-loop-check, +global-connectivity, +multi-select, +print-puzzles]
proposes: ["+trigger:input", "+trigger:constraint_broken", "+trigger:all_constraints_met", "+effect:mark", "+effect:set_value", "+effect:flash", "+role:mark", "+role:zone", "+window:params-dialog", "+window:game-id-dialog", "+window:file-dialog", "+ui:status-bar", "+ui:conflict-highlight", "+feature:seed-input", "+feature:share-code", "+feature:auto-solve", "+feature:print", "+axis:undo", "+card:platform-shell"]
author: opus
date: 2026-11-02
---

# Simon Tatham's Portable Puzzle Collection — 40 логічних ігор в одній оболонці з нескінченною генерацією

## Суть
Збірка з 40 маленьких однокористувацьких головоломок (переважно паперові пазли Nikoli-типу, плюс кілька «рухомих» — Fifteen, Inertia, Cube, Same Game), які ділять **одну оболонку**: нова гра, рестарт, undo/redo, Solve, пресети й Custom-параметри, game ID і seed. Кожен пазл генерується випадково з гарантією розвʼязності (зазвичай — унікальності й «логічного» шляху). Для курсу це еталон не однієї гри, а **платформи**: спільний мід-енд + бекенд на гру з чітким API (опис пазла рядком, хід рядком, `solve()`, `status()`). Ліцензія MIT, з 2004 р.

## Поле і час
- Здебільшого квадратна сітка W×H; винятки: Loopy — десятки плиток (квадрати, трикутники, шестикутники, Penrose тощо (?)), Untangle — вільний граф точок, Cube — граф граней тіла, Map — довільні регіони, Galaxies/Pearl — розмітка на вершинах і ребрах.
- Шари поля: клітини (значення/зафарбування) · ребра між клітинами (лінії, хрестики «тут не можна») · вершини (Slant, Galaxies) · підказки на краях (Pattern, Towers, Tents, Magnets, Undead).
- Час статичний: хід = одна дія розмітки; таймера в класичних пазлах нема. «Рухомі» ігри (Fifteen, Sixteen, Twiddle, Inertia, Cube, Flood, Same Game, Pegs) — покрокові з лічильником ходів у статус-рядку. Mines — `is_timed`: мід-енд веде таймер, заморожує його на першому розвʼязанні.
- Розмір поля і складність — параметри генератора (Type → Custom), не рівні.

## Сутності
Одна строка — одна гра збірки (підтверджено зі списку на сайті, 40 шт.). Роль — домінантна сутність гри; параметри — головні з Custom.

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Black Box | mark | розмір, кількість куль | стріляєш променями з краю; за точками виходу вивести приховані кулі (hidden-deduction) |
| Bridges | mark | max мостів 1–4, allow loops, % островів, expansion | зʼєднати острови мостами; число = кількість мостів, без перетинів, усе зʼєднано |
| Cube | object | тіло (тетраедр/куб/октаедр/ікосаедр (?)) | котиш тіло; грань на синій клітині забирає синю, ціль — зібрати всі на грані |
| Dominosa | mark | max число набору, складність | розбити прямокутник чисел на повний набір доміно, кожне один раз |
| Fifteen | tile | W×H | класичні «пʼятнашки»: зсув плитки в порожнину, впорядкувати |
| Filling | mark | W×H | Fillomino: кожна клітина = розмір її області однакових цифр |
| Flip | tile | W×H, форма перемикачів | клік перевертає групу клітин; засвітити всі (Lights Out-родич) |
| Flood | tile | W×H, кольорів, запас ходів | заливка з кута одним кольором за ліміт ходів |
| Galaxies | zone | W×H, складність | поділити сітку на центрально-симетричні області з точкою в центрі |
| Guess | mark | кольорів, позицій, спроб, дублікати/порожні | Mastermind: вгадати приховану комбінацію за чорно-білими підказками |
| Inertia | player | W×H | кулька ковзає до упору/зупинки; зібрати всі самоцвіти, оминаючи міни |
| Keen | mark | розмір N, складність | латинський квадрат + клітки з арифметикою (KenKen) |
| Light Up | mark | % чорних, симетрія, складність | Akari: лампи світять по рядку/стовпцю до стіни; освітити все, лампи не бачать одна одну, числа на стінах = лампи довкола |
| Loopy | mark | тип плитки, розмір, складність | Slitherlink: одна петля по ребрах; число = скільки ребер клітини в петлі |
| Magnets | mark | W×H, складність | розкласти магніти/нейтральні в доміно-слоти; однакові полюси не торкаються, лічильники +/− на краях |
| Map | zone | кількість регіонів, складність | розфарбувати карту 4 кольорами, сусіди різні |
| Mines | mark | W×H, мін, unique | сапер; перший клік безпечний, генерація без вгадування (hidden-deduction) |
| Mosaic | mark | W×H | число = кількість чорних серед 3×3 довкола клітини (включно) |
| Net | tile | W×H, wrap, бар'єри, unique | крутити плитки-труби, щоб мережа зʼєдналась з центром без петель (connect-rotate) |
| Netslide | tile | W×H, wrap, бар'єри, ходи перемішування | те саме, але рух — зсув цілого ряду/стовпця |
| Palisade | zone | W×H, розмір області | поділити на області однакового розміру; число = скільки стінок клітини є межами |
| Pattern | mark | W×H | Nonogram/Picross: довжини чорних серій у рядку/стовпці |
| Pearl | mark | W×H, складність, allow unsoluble | Masyu: петля через усі перлини; біла — прямо, чорна — поворот |
| Pegs | object | тип дошки | солітер: стрибок через кілок прибирає його; лишити один |
| Range | mark | W×H | Kurodoko: чорні не сусідять, білі зʼєднані; число = скільки клітин видно з неї |
| Rectangles | zone | W×H, expansion, unique | Shikaku: поділити на прямокутники, кожен з одним числом = площа |
| Same Game | tile | W×H, кольорів, мін. група, рахунок | прибирати групи ≥2 однакових; падіння і зсув; очки за квадрат групи (?) |
| Signpost | mark | W×H, показ початку/кінця | пронумерувати шлях 1…N за стрілками-вказівниками |
| Singles | mark | W×H, складність | Hitori: зачорнити дублі; чорні не сусідять, білі зʼєднані |
| Sixteen | tile | W×H, ходи перемішування | впорядкувати плитки зсувом цілого ряду/стовпця по колу |
| Slant | mark | W×H, складність | Gokigen: діагональ у кожній клітині; число на вершині = скільки діагоналей торкаються; без петель |
| Solo | mark | розмір блока, X, jigsaw, killer, симетрія, складність | судоку з варіантами (діагоналі, неправильні регіони, кіллер) |
| Tents | mark | W×H, складність | намет біля кожного дерева 1:1; намети не торкаються навіть по діагоналі; числа на краях |
| Towers | mark | розмір N, складність | Skyscrapers: латинський квадрат висот; числа на краях = скільки веж видно |
| Tracks | mark | W×H, складність | прокласти колію від входу до виходу; числа на краях = кількість клітин колії |
| Twiddle | tile | W×H, розмір блока, орієнтація | обертати блок n×n плиток, щоб упорядкувати |
| Undead | mark | W×H, складність | розставити привидів/вампірів/зомбі; дзеркала; числа = скільки монстрів видно по лінії |
| Unequal | mark | розмір N, режим, складність | Futoshiki: латинський квадрат + знаки «>» між сусідами (режим Adjacent — «різниця 1») |
| Unruly | mark | W×H, unique rows, складність | Binairo/Takuzu: порівну чорних і білих, без трьох підряд |
| Untangle | object | кількість точок | перетягувати вершини графа, доки ребра не перестануть перетинатися (field: free) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільні правила оболонки (однакові для всіх 40 ігор):
- КОЛИ `input(click|drag|key)` → ТО `custom: «interpret_move: перетворити ввід на рядок ходу»`; ЯКЩО рядок не порожній → ТО `custom: «execute_move: новий стан»`, `undo_point`.
- КОЛИ `input(undo)` → ТО `custom: «попередній стан ланцюга»` (до початку сесії); КОЛИ `input(redo)` → ТО наступний.
- КОЛИ `input(restart)` → ТО `restart` — і це теж крок, що відкочується undo.
- КОЛИ `input(solve)` → ЯКЩО `custom: «can_solve»` → ТО `custom: «solve() → рядок ходу»`, стан-розвʼязок додається в кінець undo-ланцюга (undo повертає до власної спроби); інакше `message(помилка)`. Cube Solve не підтримує.
- КОЛИ `input(new_game)` → ТО `custom: «new_desc(params, random_state)»` — генерація нового пазла з гарантіями параметрів.
- КОЛИ `constraint_broken(c)` → ТО `custom: «підсвітити червоним порушення»` (переповнений острів, дубль у рядку, петля де заборонено) — лише очевидні помилки, без підказки правильного.
- КОЛИ `all_constraints_met` → ТО `custom: «status = +1»`, `flash(completion)`, `custom: «зупинити таймер назавжди»`.
- КОЛИ `custom: «status = −1»` (Mines: міна; Guess: спроби скінчились; Flood: ходи скінчились (?)) → ТО `lose`; undo все одно доступне.
Приклади правил окремих ігор:
- Bridges: КОЛИ `constraint_broken(bridges(island) ≠ n)` → ТО острів червоний; КОЛИ `constraint_broken(not connected(all))` → ізольована група червона.
- Light Up: КОЛИ `constraint_broken(lamp sees lamp)` → обидві лампи червоні.
- Solo/Keen/Towers/Unequal: КОЛИ `constraint_broken(duplicate in row|col|block)` → дубль червоний.
- Inertia: КОЛИ `input(dir)` → ТО `slide(ball, dir)` до стіни або клітини-«стоп»; КОЛИ `contact(ball, mine)` → ТО `custom: «смерть, лічильник смертей +1»`, undo повертає. КОЛИ `all_gone(gem)` → ТО `win`.
- Mines: КОЛИ `input(open)` → ЯКЩО `first_time` → ТО міни розставляються вже після кліку (`mines-after-first-click`); `adjacent_count(cell, mine, ==, 0)` → `reveal(каскад)`.
- Перемога: усі обмеження виконані (пазли) / упорядковано (Fifteen, Sixteen, Twiddle) / зібрано (Cube, Inertia) / порожньо (Same Game). Поразка: лише Mines, Guess, Flood (?). Рахунок: лише Same Game (очки) і лічильник ходів у рухомих іграх.

## Керування і ввід
- Миша: лівий клік/drag — головна розмітка (лінія, лампа, цифра після вибору клітини), правий — допоміжна (хрестик «тут не можна», крапка «точно біла»), середній — подекуди третій стан (?).
- Клавіатура скрізь: стрілки рухають курсор, Enter/Space — ліва/права дія, цифри — ввід числа; Ctrl/Shift+стрілка — провести лінію/хрестик у напрямку (Bridges, Pearl).
- Однокнопкові шорткати оболонки: N — нова гра, U/Ctrl+Z — undo, R/Ctrl+R — redo, Q — вихід; у Preferences можна вимкнути однокнопкові (лишаються Ctrl-версії).
- Pencil marks у латинських квадратах (Solo, Keen, Towers, Unequal): правий клік / окремий режим — дрібні кандидати в клітині (?).
- Мультивибір: Filling — drag виділяє кілька клітин, одна цифра заповнює всі.

## Вікна, меню, HUD
- `game-screen`: поле + (у частини ігор) `status-bar` знизу — лічильник ходів, «COMPLETED!», міни, рахунок Same Game; таймер у Mines.
- Меню Game: New game · Restart game · Specific… · Random Seed… · Load… · Save… · Print… (Windows) · Undo · Redo · Copy · Solve · Preferences… · Quit.
- Меню Type: пресети (розмір × складність) → нова гра одразу; Custom… → `params-dialog` (поля, чекбокси, випадні списки параметрів гри).
- `game-id-dialog` ×2: Specific (описовий ID `params:опис`) і Random Seed (`params#seed`); показує поточний ID — ним діляться.
- `file-dialog` Load/Save (зберігається вся історія undo/redo).
- `settings-window` Preferences: спільна опція «однокнопкові шорткати» + опції гри (Bridges: показувати можливі мости; Pearl: Traditional / Loopy-style).
- `help-window` — розділ мануалу гри; `about-window`.
- Переходи: game-screen → Type/Custom → params-dialog → новий пазл на game-screen; game-screen → Specific/Seed → game-id-dialog → той самий пазл.

## Фічі поза полем
- `undo` ∞ + `redo` + `restart-level` (відкочуваний) — розвʼязання без страху; Solve як крок історії (`auto-solve`, `show-solution`).
- `seed-display` + `seed-input` + `share-code`: описовий ID (точний пазл, не залежить від версії) проти seed (15 цифр; та сама генерація лише в тій самій версії).
- `difficulty-presets` + `custom-difficulty`: усі параметри генератора відкриті гравцеві.
- `save-slots`-аналог через файли; `export-import` текстом (Copy) у частині ігор.
- Print (Windows; Unix `--print wxh` → PostScript з розвʼязками, `--generate n` → n game ID) — генератор як фабрика паперових пазлів.
- Нема: рекордів, статистики, рівнів, туторіалу — свідомо мінімалістична «гра на 2–3 хвилини перерви».
- Платформи: Windows, Unix/GTK, веб (JS/WebAssembly); macOS-збірки припинено 2023; порти Android (Chris Boyle), iOS (Greg Hewgill), Rockbox, Windows Store та ін. — сторонні.

## Варіації й родичі
- Майже кожна гра — реімплементація відомого жанру: Pattern = Nonogram, Solo = Sudoku, Loopy = Slitherlink, Pearl = Masyu, Filling = Fillomino, Bridges = Hashiwokakero, Light Up = Akari, Singles = Hitori, Range = Kurodoko, Rectangles = Shikaku, Unruly = Takuzu, Towers = Skyscrapers, Keen = KenKen, Unequal = Futoshiki, Tents = Tents and Trees, Guess = Mastermind, Pegs = Peg solitaire.
- Порти й нащадки: Android-порт Chris Boyle, iOS-порт; сайти puzzle-*.com — те саме ядро жанрів із рекордами й daily.
- **Осі варіацій**, які видно на збірці: що розмічає гравець (клітини / ребра / вершини / області) · де підказки (у клітині / на краю / на ребрі / жодних) · глобальне обмеження (одна петля / зʼєднаність / латинський квадрат / розбиття на області) · чи є прихована інформація (Black Box, Guess, Mines) · чи «рухома» гра (Fifteen…Inertia).

## Цікавинки для курсу
- Оболонка-платформа: один мід-енд (меню, undo, seed, Solve) + бекенд на гру з API `new_desc / validate_desc / interpret_move / execute_move / solve / status` — 🥇 (архітектура, що дає N ігор за ціною однієї оболонки).
- Хід як рядок + undo як список станів + Solve, вставлений у кінець історії — 🥉 (просто, але змушує відділити ввід від логіки).
- Game ID: описовий рядок vs seed; параметри кодуються без `:` і `#` — 📎 (серіалізація стану й відтворюваність генерації).
- Генератор з гарантією унікального логічного розвʼязку для обраної складності (генеруй → розвʼязуй солвером з обмеженими техніками → приймай/відкидай) — 👑 у загальному вигляді, 🥇 для однієї гри.
- Підсвітка лише **очевидних** порушень (Bridges: «недостача» червона, лише якщо вже неминуча) — 🥈 (потрібна часткова дедукція, а не порівняння з відповіддю).
- Однокнопкові шорткати з вимикачем у Preferences — 🌱.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` (червоні порушення) · `completion-detection` (status +1, спалах) · `cell-click` · `keyboard-controls` (курсор у всіх іграх) · `hover-highlight` · `unique-puzzle-generation` · `difficulty-rating` (рівні складності = техніки солвера) · `difficulty-levels` · `level-solver` (Solve) · `game-settings` + `field-size-picker` (Custom) · `save-game` (файл з історією) · `import-open-formats` (game ID як формат) · `state-as-data` · `logic-render-split` (мід-енд/бекенд/фронтенд) · `help-window` · `about-window` · `event-effects` (спалах завершення) · `mines-after-first-click` · `inertia-slide`.
- **Нема** → пропозиції карток:
  - `+undo-redo` (уже є в корпусі) — тут ∞ до старту сесії, restart — теж крок.
  - `+state-string` (уже є) — описовий game ID `params:desc`.
  - `+seed-share` «Пазл із seed і обмін кодом» · levels/generation · 📎 · слот {format: seed|desc}.
  - `+platform-shell` «Спільна оболонка для кількох ігор» · code/architecture · 🥇 — мід-енд + інтерфейс бекенда.
  - `+move-string` «Хід як рядок (interpret → execute)» · code/architecture · 🥉.
  - `+solve-into-undo` «Розвʼязок як крок історії» · game-logic/flow · 📎.
  - `+edge-marking` (є в slitherlink) — лінія / хрестик на ребрі: Loopy, Pearl, Bridges, Tracks.
  - `+single-loop-check` (є в slitherlink) — одна замкнена петля: Loopy, Pearl.
  - `+global-connectivity` «Усе зʼєднано в одну групу» · game-logic/constraints · 📎 — Bridges, Range, Singles, Net.
  - `+multi-select` (є в sudoku) — виділити кілька клітин і заповнити разом: Filling.
  - `+print-puzzles` «Друк/експорт пачки пазлів» · levels/generation · 📎.

## Пропозиції до словників
- `+trigger:input`, `+trigger:constraint_broken`, `+trigger:all_constraints_met` — ядро всіх пазлів збірки (⏳ → кандидати на ✅ за правилом трьох).
- `+effect:mark`, `+effect:set_value` — розмітка клітини/ребра і цифра; `+effect:flash` — спалах завершення (не скорочується наступним вводом).
- `+role:mark` (лінія, лампа, цифра), `+role:zone` (області Galaxies/Rectangles/Palisade/Map).
- `+window:params-dialog` — форма Custom-параметрів генератора; `+window:game-id-dialog` — ввід/показ ID чи seed; `+window:file-dialog` — Load/Save.
- `+ui:status-bar` — текстовий рядок стану під полем; `+ui:conflict-highlight` — червоне порушення.
- `+feature:seed-input`, `+feature:share-code`, `+feature:auto-solve`, `+feature:print` — друк пачки згенерованих пазлів.
- `+axis:undo` — `unlimited` + restart як відкочуваний крок.
- `+card:platform-shell` — див. «Мапа на каталог».

## Джерела
- ⭐ [Simon Tatham's Portable Puzzle Collection](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/) — список 40 ігор з однорядковими правилами, гра в браузері, завантаження, порти.
- [Common features](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — меню Game/Type, undo/redo, Solve, game ID vs seed, параметри командного рядка.
- [Мануал (зміст)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/index.html) — по розділу на кожну гру.
- [Bridges](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/bridges.html) · [Pearl](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pearl.html) · [Filling](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html) — приклади сторінок гри: правила, керування, Custom-параметри.
- [Developer docs: backend](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/devel/backend.html) — API бекенда (`new_desc`, `interpret_move`, `execute_move`, `solve`, `status`, `wants_statusbar`, `is_timed`).
- Wikipedia: [пошук статті](https://en.wikipedia.org/w/index.php?search=Simon+Tatham%27s+Portable+Puzzle+Collection&ns0=1).
- YouTube: [пошук «simon tatham puzzles»](https://www.youtube.com/results?search_query=simon+tatham+puzzles).

## Непевне
- (?) Параметри Custom у таблиці — з памʼяті, крім Bridges, Pearl, Filling (перевірені на сторінках мануалу).
- (?) Набір тіл у Cube, перелік плиток Loopy, формула очок Same Game — не перевіряв.
- (?) Які ігри повертають `status = −1` (поразку): Mines — певно; Guess і Flood — з памʼяті.
- (?) Pencil marks і правий/середній клік у латинських квадратах — деталі керування не перевіряв по сторінках Solo/Keen.
- (?) Рік 2004 — з копірайту «2004–2021» на сайті; окремі ігри (Net, Cube, Fifteen) могли зʼявитися раніше.
