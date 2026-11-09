---
title: SpaceChem
slug: spacechem
aka: [Space Chem, "SpaceChem: 63 Corvi"]
family: program-robots
also: [build-sim, thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2011
platforms: [PC, Mac, Linux, iPad, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SpaceChem", best: true, note: "ядро: реактор 10×8, два вальдо, bond/fusion/fission/sense, зіткнення зупиняють, планетний шар, метрики, гістограми, оборонні рівні"}
  - {kind: steam, url: "https://store.steampowered.com/app/92800/SpaceChem/", note: "Steam: понад 50 пазлів, DLC 63 Corvi, досягнення, лідерборди"}
  - {kind: other, url: "https://www.xanthir.com/b4fU0", note: "розбір порядку спрацювання бондерів (Bond+)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spacechem+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [command-program, step-execution, code-editor-window, stick-together, cell-transform, sensor-predicates, collect-quota, drag-drop-piece, sequential-levels, level-unlock, level-select, world-map, leaderboard, in-game-editor, level-exchange, game-screen, end-screen, +swarm-separate-programs, +instruction-on-track-cells, +grab-drop-rotate, +bond-unbond, +bonder-priority, +fusion-fission-nodes, +sync-barrier, +flip-flop-branch, +sense-branch, +molecule-match-output, +output-blocking, +collision-halt, +reactor-pipeline-layer, +solution-metrics, +metric-histograms, +defense-level-timer, +sandbox-mode]
proposes: ["+effect:grab", "+effect:release", "+effect:wait_sync", "+trigger:all_synced", "+effect:redirect(a, dir)", "+cond:sensor_atom(kind)", "+cond:flipflop(state)", "+effect:fuse(a, b)", "+effect:fission(a)", "+effect:output(v)", "+role:waldo", "+role:bonder", "+window:planet-layer", "+window:metric-histograms", "+ui:waldo-path-layer", "+ui:metric-panel", "+feature:solution-metrics", "+feature:user-puzzles", "+axis:actors"]
author: opus
date: 2026-11-09
---

# SpaceChem — розклади команди на треках двох маніпуляторів, щоб реактор збирав молекули з атомів

## Суть
Гравець — інженер хімічного реактора: на сітці реактора працюють **два маніпулятори-вальдо** (червоний і синій), і кожен їде маршрутом, який гравець малює стрілками, виконуючи іконки-команди на клітинах шляху: схопити атом, повернути, віддати на вихід, звʼязати. Мета — збудувати машину, що **повторювано** перетворює вхідні молекули на потрібний продукт до виконання квоти. Два вальдо працюють паралельно: їх треба синхронізувати, інакше атоми зіткнуться, і реактор зупиниться. У великих рівнях реактори стоять на «планетному» полі й передають продукти трубами один одному.

## Поле і час
- Реактор — сітка **10×8**; у ньому до двох вхідних квадрантів (α, β) і двох вихідних (ψ, ω).
- Два шари на одній сітці: шар червоного вальдо і шар синього — у кожному свої стрілки й команди; гравець перемикає шар, щоб редагувати. Вальдо можуть проходити одне крізь одного без шкоди.
- Нерухомі «фічі» реактора — бондери, сенсор, фьюзер/сплітер, тунель (?) — займають клітини; їх кількість і доступність задає рівень, у вільних рівнях їх можна переставляти (?).
- Час `programmed`: симуляція по циклах; за цикл кожне вальдо виконує команду на своїй клітині й робить крок у поточному напрямку. Кнопки швидкості: крок, звичайна, швидка (?).
- Планетний шар: окрема сітка, де стоять кілька реакторів, входи-видобутки й виходи-приймачі, зʼєднані трубами; вихід одного реактора — вхід іншого.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червоне / синє вальдо | player | позиція, напрямок, тримає/ні | їде шляхом зі стрілок, виконує команду клітини; несе захоплену молекулу |
| Стрілка напрямку | terrain | колір вальдо, напрямок | змінює напрямок свого вальдо |
| Start | terrain | колір, напрямок | стартова клітина і напрямок вальдо |
| Атом | object | елемент (H, C, O, N…), макс. кількість звʼязків | рухається лише з вальдо; звʼязаний — разом з молекулою |
| Молекула | object | атоми + звʼязки (одинарні, подвійні, потрійні (?)) | ціле: схопити за будь-який атом — їде вся |
| Вхід α / β | spawner | шаблон молекули, (кілька шаблонів з частотами (?)) | команда Input вкидає нову молекулу в квадрант |
| Вихід ψ / ω | sink | шаблон продукту, квота | Output забирає молекули з квадранта; зараховує, якщо збіг |
| Бондер | switch | номер-пріоритет | Bond+/Bond− діють на пари сусідніх бондерів, на яких лежать атоми |
| Сенсор | switch | елемент для перевірки | Sense: якщо на сенсорі атом потрібного виду — вальдо повертає у вказаний бік |
| Фьюзер (fuser) | switch | 2 клітини | Fuse: зливає два атоми в атом з сумою атомних номерів |
| Сплітер (splitter) | switch | 2 клітини | Fission: ділить атом на два легші (?) |
| Тунель / swapper (63 Corvi, пізні рівні) | switch | пара клітин | Swap: міняє вміст пар місцями (?) |
| Реактор (на планеті) | container | тип: повний / лише розрив звʼязків / … | має свої входи-виходи; програма живе всередині |
| Труба | conduit | — | везе молекули між реакторами на планетному шарі |
| Ворог / база (оборонні рівні) | boss | HP, атаки за таймером (?) | руйнує контрольну структуру, якщо вчасно не доставлено продукт до гармат |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО обидва вальдо `exec(cmd)` на своїй клітині, потім `move(waldo, facing)`.
- КОЛИ `enter(waldo, arrow)` → ТО `face(waldo, arrow_dir)` (стрілки лише свого кольору).
- КОЛИ `exec(input α|β)` → ТО `spawn_at(input_molecule, input_quadrant)`.
- КОЛИ `exec(grab)` → ЯКЩО `occupied(here, atom)` → ТО `custom: «вальдо хапає всю молекулу, якій належить атом»`.
- КОЛИ `exec(drop)` → ТО `custom: «вальдо відпускає молекулу на місці»`; `exec(grab-drop)` — перемикач.
- КОЛИ `exec(rotate cw|ccw)` → ЯКЩО `custom: «вальдо тримає молекулу»` → ТО `rotate(molecule, ±90°)` навколо атома в захваті.
- КОЛИ `exec(bond+)` → ЯКЩО `custom: «атоми на двох сусідніх бондерах і мають вільні валентності»` → ТО `attach(a, b)` (+1 до кратності звʼязку); перевіряються пари в порядку пріоритету бондерів.
- КОЛИ `exec(bond−)` → ЯКЩО `custom: «між атомами на сусідніх бондерах є звʼязок»` → ТО `detach(a, b)` (−1 до кратності).
- КОЛИ `exec(sync)` → ТО `custom: «вальдо стоїть, доки друге теж не дійде до своєї sync»` — барʼєр.
- КОЛИ `exec(sense)` → ЯКЩО `occupied(sensor, atom_kind)` → ТО `face(waldo, sense_dir)`; інакше їде далі.
- КОЛИ `exec(flip-flop)` → ЯКЩО `state(flipflop, a)` → ТО `face(waldo, dir_a)`; інакше `face(waldo, dir_b)`; і `custom: «перемкнути стан flip-flop»` — чергування гілок.
- КОЛИ `exec(fuse)` → ЯКЩО `custom: «атоми на обох клітинах фьюзера»` → ТО `merge(a, b → c)` (атомний номер c = a + b) (?).
- КОЛИ `exec(fission)` → ТО `split(atom)` на два атоми (?).
- КОЛИ `exec(output ψ|ω)` → ЯКЩО `custom: «у вихідному квадранті лише молекули»` → ТО `custom: «молекули покидають реактор»`; поки в квадранті лишаються атоми, Output блокує вальдо.
- КОЛИ `custom: «молекула на виході»` → ЯКЩО `same(molecule, target, topology)` (атоми, звʼязки й кратність; орієнтація не важлива) → ТО `counter(produced, +1)`; інакше `crash` — «wrong output».
- КОЛИ `custom: «два атоми в одній клітині» або «атом на стіні реактора»` → ТО `crash` — симуляція зупиняється, місце підсвічене.
- КОЛИ `counter(produced, ==, quota)` → ТО `win`, `window(end-screen)` з метриками.
- КОЛИ `timer(every)` → ЯКЩО оборонний рівень і `custom: «продукт не доставлено до зброї»` → ТО `damage(n)` по базі; `hp_zero(base)` → `lose` (?).
- Перемога: квота продукту на кожному виході · Поразка: лише в оборонних рівнях; в інших зіткнення/неправильний вихід — зупинка й правка програми · Рахунок: **cycles** (цикли до квоти), **reactors** (кількість реакторів), **symbols** (кількість команд/стрілок) — порівняння з гістограмами всіх гравців.

## Керування і ввід
- Мишею: перетягнути іконку команди з палітри на клітину шару поточного вальдо; стрілки ставлять напрямок; Start перетягується.
- Перемикання шару червоний/синій; клік по команді — налаштувати параметр (який вхід, напрямок sense, елемент сенсора) (?).
- Кнопки симуляції: Stop · Step · Play · Fast-forward (?).
- Планетний шар: drag реактора з запасу на поле, з'єднання входів і виходів трубами, подвійний клік — увійти в реактор (?).

## Вікна, меню, HUD
- `main-menu` → `map-window` (`planet-layer`): планети-світи, на кожній вузли-рівні, відкриваються по черзі; останній — оборонний.
- `game-screen` (реактор): сітка 10×8, квадранти входів/виходів з шаблонами молекул, `waldo-path-layer` двох кольорів, `command-palette`, `instruction-highlight` на поточних клітинах, кнопки симуляції, лічильник циклів і квоти (`progress-bar`).
- `planet-layer` — поле з реакторами й трубами, кнопка запуску всієї фабрики.
- `end-screen` — «Complete» з `metric-panel` (cycles / reactors / symbols) і `metric-histograms` — де ти серед усіх.
- `help-window` / `codex-window` — довідник команд (?).
- Діалоги сюжету між рівнями (`dialogue-window`) (?).
- ResearchNet — вікно користувацьких пазлів; Sandbox — вільний реактор.
- Переходи: main-menu → planet map → рівень → (квота) end-screen → planet map; Esc → `pause-menu`.

## Фічі поза полем
- `solution-metrics` і глобальні гістограми — заохочення оптимізувати без «таблиці топ-гравців» (так пояснив розробник).
- `leaderboard` (Steam), `achievements` (20), трейдинг-картки, хмарні збереження.
- **ResearchNet** — створення й обмін пазлами; пізніше додано `mode-sandbox`.
- Повтор розвʼязаних рівнів для покращення метрик.
- DLC **63 Corvi** — додаткові пазли й механіки (?); TF2-промопазли з предметом у Team Fortress 2.

## Варіації й родичі
- Zachtronics-лінія: [Opus Magnum](opus-magnum.md) (руки на гексах, timeline замість треків, cost/cycles/area), Infinifactory, TIS-100, Shenzhen I/O, Exapunks — те саме «збудуй машину й оптимізуй метрики».
- Родичі в корпусі: [Manufactoria](manufactoria.md) (розкладка на полі = програма), [Befunge](befunge.md) (інструкції лежать на клітинах, вказівник їде), [Robot Odyssey](robot-odyssey.md) (паралельні схеми), [7 Billion Humans](7-billion-humans.md) (кілька виконавців).
- **Осі варіацій**: де програма (команди на клітинах маршруту / timeline рук / текст) · скільки виконавців (2 вальдо / N рук / рій) · синхронізація (sync-барʼєр / спільний такт / нема) · оцінка (одна квота / метрики + гістограми) · масштаб (один реактор / мережа реакторів).

## Цікавинки для курсу
- Симулятор вальдо на треках: стрілки, команди на клітинах, два потоки за один тік — 🥉.
- Sync-барʼєр і виявлення дедлоку (обидва чекають / вічне очікування) — 🥈.
- Молекула як граф атомів зі звʼязками: захват, поворот на 90° навколо атома, рух цілою — 🥈.
- Перевірка продукту «з точністю до ізоморфізму» (орієнтація не важлива) — 🥇 (ізоморфізм малих мічених графів).
- Bond+ з пріоритетом бондерів і валентностями — 🥉.
- Метрики + гістограми розвʼязків — 📎 (зібрати й показати розподіл).
- Планетний шар: реактори як вузли, труби як черги — 🥈.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ команди вальдо; `step-execution` ↔ Step/підсвітка; `code-editor-window` ↔ сітка реактора як редактор; `stick-together` ↔ звʼязані атоми рухаються разом; `cell-transform` ↔ фьюзер/сплітер; `sensor-predicates` ↔ Sense; `collect-quota` ↔ квота продукту; `drag-drop-piece` ↔ розстановка команд; `sequential-levels`/`level-unlock`/`level-select`/`world-map` ↔ планети з вузлами; `leaderboard`; `in-game-editor`/`level-exchange` ↔ ResearchNet; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+swarm-separate-programs` «Кілька виконавців з окремими програмами» · game-logic/program · 🥈.
  - `+instruction-on-track-cells` «Команди лежать на клітинах маршруту виконавця» · game-logic/program · 🥉.
  - `+grab-drop-rotate` «Маніпулятор: схопити, відпустити, повернути» · entities/interact · 📎.
  - `+bond-unbond` «Утворення й розрив звʼязків на спецклітинах» · entities/interact · 🥉.
  - `+bonder-priority` «Порядок спрацювання однакових спецклітин» · entities/interact · 📎.
  - `+fusion-fission-nodes` «Злиття/поділ атомів за атомним номером» · entities/interact · 📎.
  - `+sync-barrier` «Барʼєр синхронізації потоків» · game-logic/program · 🥈.
  - `+flip-flop-branch` «Тригер-перемикач гілок» · game-logic/program · 📎 · `+sense-branch` «Розгалуження за типом обʼєкта на сенсорі» · 🌱.
  - `+molecule-match-output` «Вихід приймає лише продукт-шаблон (з точністю до ізоморфізму)» · game-logic/win · 🥇.
  - `+output-blocking` «Вихід блокує виконавця, доки зайнятий» · game-logic/program · 🌱.
  - `+collision-halt` «Зіткнення зупиняє симуляцію» · game-logic/lose · 🌱.
  - `+reactor-pipeline-layer` «Мережа машин: вихід однієї — вхід іншої» · game-logic/program · 🥈.
  - `+solution-metrics` · `+metric-histograms` · interface/results · 📎.
  - `+defense-level-timer` «Програма мусить встигнути до атаки» · game-logic/lose · 🥉 · `+sandbox-mode` · 🌱.

## Пропозиції до словників
- `+effect:grab` / `+effect:release` — маніпулятор бере/відпускає обʼєкт (Opus Magnum, SpaceChem, Cargo-Bot).
- `+effect:wait_sync` · `+trigger:all_synced` — барʼєр: виконавець чекає, доки всі дійдуть до sync.
- `+effect:redirect(a, dir)` — змінити напрямок руху виконавця командою клітини (≠ `face`, бо рух триває).
- `+cond:sensor_atom(kind)` — на клітині-сенсорі обʼєкт виду.
- `+cond:flipflop(state)` — стан перемикача з чергуванням.
- `+effect:fuse(a, b)` / `+effect:fission(a)` — злиття/поділ за числовою властивістю (атомний номер).
- `+effect:output(v)` — відправити назовні (вихід реактора).
- `+role:waldo` — маніпулятор, що їде маршрутом; `+role:bonder` — спецклітина звʼязування.
- `+window:planet-layer` — поле з'єднаних машин; `+window:metric-histograms`.
- `+ui:waldo-path-layer` — шари маршрутів різних кольорів; `+ui:metric-panel`.
- `+feature:solution-metrics` · `+feature:user-puzzles` (ResearchNet).
- `+axis:actors` — `party` (два вальдо).

## Джерела
- ⭐ [Wikipedia: SpaceChem](https://en.wikipedia.org/wiki/SpaceChem) — реактор 10×8, вальдо, вузли bond/fusion/fission/logic, зіткнення, планетний шар, метрики й гістограми, оборонні рівні, ResearchNet і sandbox.
- [Steam: SpaceChem](https://store.steampowered.com/app/92800/SpaceChem/) — понад 50 пазлів, 20 досягнень, DLC 63 Corvi, платформи.
- [Xanthir: SpaceChem Bonders Explained](https://www.xanthir.com/b4fU0) — пріоритет бондерів, порядок перевірки Bond+.
- Вікі r/spacechem «game mechanics» (дзеркало в результатах пошуку) — sync як барʼєр, flip-flop і sense, Output блокує вальдо.
- YouTube: пошук «spacechem gameplay».

## Непевне
- (?) Точний перелік команд (Grab-Drop, Pause, Swap, Fuse, Split) і їхні іконки — частково з памʼяті; вікі гри (fandom) віддала 402, StrategyWiki — 403.
- (?) Поворот на 90° і чи поворот навколо атома в захваті; максимальна кратність звʼязку (потрійний?).
- (?) Чи бувають випадкові входи (кілька шаблонів з імовірностями) — тому `random: none` під питанням.
- (?) Механіка оборонних рівнів (HP бази, таймінги атак, гармати) — лише загальний опис з Wikipedia; `opponent` поставлено `none`, хоча там є вороги.
- (?) Метрика «symbols» vs «instructions» — Wikipedia пише «instruction count»; назва в UI з памʼяті.
- (?) Що саме додає 63 Corvi крім пазлів.

