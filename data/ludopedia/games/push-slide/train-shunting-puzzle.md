---
title: Train shunting puzzle (Inglenook Sidings, Timesaver)
slug: train-shunting-puzzle
aka: [Shunting puzzle, Switching puzzle, Inglenook Sidings, Inglenook, Timesaver, Маневрова головоломка]
family: push-slide
also: [connect-rotate]
klass: avatar
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: setup
  goal: state
year: 1972
platforms: [model railway, PC, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Train_shunting_puzzle", best: true, note: "жанр: колії, обмеження (мінімум зчеплень, перекладів стрілок, час), заборони для типів вагонів, класи задач, комп'ютерні версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Inglenook_Sidings", note: "Alan Wright: 3 тупики на 5/3/3 вагони, витяжка 3+локомотив, 8 вагонів, потяг з 5 у випадковому порядку"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Timesaver", note: "John Allen, Model Railroader 11/1972: 5 стрілок, 5 тупиків, обгінна колія, гра на час, кооперативна пара макетів"}
  - {kind: other, url: "https://www.wymann.info/ShuntingPuzzles/Inglenook/inglenook-rules.html", note: "правила Inglenook: 14 місць, 6 вільних, жеребкування, порядок вибору, стратегії, 40 320 розстановок"}
  - {kind: other, url: "https://www.wymann.info/ShuntingPuzzles/Timesaver/timesaver-rules.html", note: "правила Timesaver: 5 вагонів у пункти A–E, час або мінімум ходів, ємність колій з локомотивом"}
  - {kind: other, url: "https://www.wymann.info/ShuntingPuzzles/sw-inglenook.html", note: "історія Inglenook, «Tiddlywink Computer», варіант 1992 з гальмівним вагоном"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Inglenook+sidings+shunting+puzzle", note: "пошук; розвʼязки на макетах"}
stage: v1
coverage: 60
mechanics: [push-object, pull-object, button-toggle, completion-detection, move-counter, time-bonus, cell-click, level-solver, unsolvable-states, reachability-check, difficulty-levels, game-settings, movement-animation, +rail-graph, +couple-uncouple, +track-capacity, +switch-points, +ordered-train-goal, +random-goal-draw, +vehicle-restriction, +min-couplings-score]
proposes: ["+cond:capacity", "+ui:target-sequence", "+feature:random-goal-draw", "+card:couple-uncouple", "+card:track-capacity", "+card:rail-graph"]
author: opus
date: 2026-11-09
---

# Train shunting puzzle — локомотив тягне й штовхає вагони по графу колій, щоб скласти потяг у заданому порядку

## Суть
Маневрова головоломка з моделізму: є колійна схема (стрілки, тупики, витяжна колія), кілька вагонів і один локомотив, який їде вперед-назад, зчіплює вагони й розчіплює їх. Мета — переставити вагони в цільову конфігурацію: скласти потяг у заданому порядку (Inglenook Sidings) або розставити вагони по пунктах призначення (Timesaver). Складність — від **обмеженої ємності колій** і того, що вагон можна лише штовхнути чи потягнути, але не обійти: це задача перестановки через стеки, як Sokoban на графі. Оцінка — кількість ходів, зчеплень, перекладів стрілок або час.

## Поле і час
- Поле — граф колій: ребра-відрізки з ємністю (у вагонах), вузли — стрілки (переводяться між двома гілками) і тупики-упори. Позиції вагонів — впорядковані черги на відрізках.
- **Inglenook Sidings** (Alan Wright): витяжна колія на локомотив + 3 вагони, дві стрілки, три тупики на 5, 3 і 3 вагони; 8 вагонів, усього 14 місць — 6 завжди вільні.
- **Timesaver** (John Allen, 1972): 5 стрілок (3 ліві, 2 праві), 5 тупиків і обгінна колія в центрі; ємність колій рахується разом із локомотивом (колія D — не більше двох вагонів).
- Зчеплення — звʼязок між сусідніми одиницями: зчеплені рухаються разом; розчепити можна між будь-якими двома (на макетах — над магнітом (?)).
- Хід (цифрова версія) = рух локомотива з причепленим составом в один бік до зупинки, зчеплення / розчеплення або переведення стрілки. Оригінальний Timesaver — real-time: локомотив має фіксовану повільну швидкість, оператор лише міняє напрям; рахується час, і «думати» коштує стільки ж, скільки їхати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Локомотив | player | напрямок; причеплені вагони | їде вперед/назад; штовхає вагони перед собою, тягне зчеплені за собою |
| Вагон | object | номер / тип | сам не рухається; рухається лише в составі з локомотивом |
| Відрізок колії | terrain | ємність N вагонів | у ньому не більше N одиниць |
| Тупик / упор | static | — | кінець колії; за нього не проїхати |
| Стрілка | switch | normal / reverse | визначає, на яку гілку йде рух через вузол |
| Витяжна колія (headshunt) | terrain | ємність (Inglenook: локомотив + 3) | обмежує, скільки вагонів можна винести з тупика за раз |
| Обгінна колія (Timesaver) | terrain | — | дає локомотиву обʼїхати вагони, щоб опинитись з іншого боку |
| Пункт призначення A–E (Timesaver) | zone | ціль 0…n вагонів | вагон, поставлений сюди, вважається доставленим |
| Цільовий потяг (Inglenook) | zone | 5 номерів у порядку | 5 вагонів мають стояти поспіль саме в цьому порядку |
| Обмежений відрізок (низький міст, слабкий міст, тунель) | static | заборонені типи | певний тип вагона / локомотив туди не проходить |
| Гальмівний вагон (Inglenook 1992) | object | — | ніколи не сходить з головної колії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drive, dir)` → ЯКЩО `custom: «увесь состав уміщається в наступний відрізок»` і `free(next_segment)` → ТО `move(train, dir)`; інакше `block`.
- КОЛИ `contact(train, wagon)` (наїзд) → ТО `push` — вагони без зчеплення попереду штовхаються разом із составом (?).
- КОЛИ `input(couple)` → ЯКЩО `in_range(train, wagon, 1)` → ТО `attach(train, wagon)`, `counter(couplings, +1)`.
- КОЛИ `input(uncouple, k)` → ЯКЩО `state(train, coupled)` → ТО `detach(train, wagons_after_k)`, `counter(couplings, +1)`.
- КОЛИ `input(drive, dir)` → ЯКЩО `state(train, coupled)` → ТО `pull(wagons)` — зчеплені за локомотивом їдуть за ним.
- КОЛИ `input(throw, points)` → ЯКЩО `free(points)` (на стрілці нема вагона) → ТО `set_state(points, normal|reverse)`, `counter(throws, +1)`.
- КОЛИ `enter(train, points)` → ТО `custom: «рух іде на гілку за станом стрілки»`.
- КОЛИ `enter(train, segment)` → ЯКЩО `custom: «одиниць у відрізку > ємності»` → ТО `block`.
- КОЛИ `enter(vehicle, restricted_segment)` → ЯКЩО `custom: «тип заборонений для відрізка»` → ТО `block`.
- КОЛИ `blocked(train)` (упор) → ТО `block`.
- КОЛИ `level_start` → ТО `custom: «випадково обрати 5 з 8 вагонів у порядку витягування»` (Inglenook) / `custom: «кожному вагону випадковий пункт A–E»` (Timesaver).
- КОЛИ `all_constraints_met` (Inglenook: 5 вагонів поспіль у порядку вибору; Timesaver: усі вагони у своїх пунктах) → ТО `win`.
- КОЛИ `custom: «аварія — сход, удар»` (фізичний макет) → ТО `timer(+penalty)`.
- Перемога: цільова розстановка. · Поразка: нема; глухий кут — розвʼязок довшає. · Рахунок: Timesaver оригінал — найкоротший час; модифікований — мінімум ходів; загалом — мінімум зчеплень/розчеплень, мінімум перекладів стрілок або ліміт часу.

## Керування і ввід
- Фізичний макет: реверсивний перемикач з центром «стоп» (Timesaver — лише напрям, швидкість фіксована), ручні стрілки, розчеплення магнітами під колією (?).
- Цифрова версія: клік по стрілці — перевести; клік між вагонами — розчепити; стрілки/кнопки — їхати вперед/назад; drag локомотива (?).
- Жеребкування цілі: фішки з номерами з кухля («Tiddlywink Computer» Wright-а), кубик, картки або генератор випадкових списків (з 8 номерів беруть перші 5).

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: вибір схеми (Inglenook / Timesaver / Sam Loyd) → `custom-window` налаштування задачі (кількість вагонів, випадкова чи задана ціль, критерій оцінки).
- `game-screen`: схема колій; HUD — `move-counter` (ходи / зчеплення / перекладання), `timer-elapsed` (режим Timesaver), `target-sequence` — картка цільового потяга чи список «вагон → пункт».
- `end-screen`: ходи/час, порівняння з мінімумом (?).
- `help-window`: правила й ємності колій.
- Переходи: main-menu → налаштування → game-screen → (ціль виконана) end-screen → нове жеребкування.

## Фічі поза полем
- Жеребкування цілі — кожна партія нова; 8! = 40 320 розстановок вагонів Inglenook.
- Режими оцінки: на час (Timesaver 1972) / мінімум ходів (модифіковане правило) / мінімум зчеплень і стрілок.
- Розширене правило Timesaver: випадкова кількість вагонів у випадкові пункти, пункт може отримати кілька або жодного; призначення за «логікою трафіку» (кожне підприємство приймає лише свої типи вагонів).
- Кооператив: два макети Timesaver, зʼєднані неелектрифікованою колією обміну на 1 вагон; гравці обмінюються вихідними вагонами (`mode-coop`).
- Цифрові: доповнення до Trainz і Microsoft Train Simulator, TrainPuzzle, Flash-гра Railroad Shunting Puzzle, застосунок Andy's Trains, онлайн-версія Inglenook від Neil Machin.

## Варіації й родичі
- Класи задач (Wikipedia): скласти потяг у заданому порядку · розформувати потяг по місцях · оптимальна послідовність збирання/розбирання · розминутись двом довгим потягам на одноколійці через обгінний пункт (double saw-by) · обʼїхати вагони на тупиковій станції · розвернути потяг на трикутнику (wye).
- Класичні: Sam Loyd «Primitive Railroading» (два потяги розминаються через тупик на 1 одиницю); «car hop» — поміняти два вагони через тупик на 1 вагон.
- Родичі в корпусі: [sokoban](sokoban.md) (штовхання без тягнення, глухі кути), [rush-hour](rush-hour.md) і [klotski](klotski.md) (перестановка в тісноті), [sliding-tile-permutation](sliding-tile-permutation.md) (перестановка через обмежені ходи); з `connect-rotate` — [railbound](../connect-rotate/railbound.md) (там колії будуєш, тут — керуєш рухом по готових).
- Осі варіацій:
  - **схема**: лінійна з тупиками (Inglenook) / з обгінною колією (Timesaver) / трикутник (wye) / кілька макетів;
  - **ціль**: порядок у потязі / пункти призначення / розминутись / розвернути;
  - **ціна**: ходи / зчеплення / стрілки / час;
  - **обмеження**: ємність колій / заборонені відрізки для типів / вагон, що не сходить з колії.

## Цікавинки для курсу
- Модель колій як графа з відрізками-чергами (deque на відрізок) і стрілками-станами — 🥉.
- Рух составу як цілого: перевірка ємності кожного відрізка, по якому пройде хвіст, і переходу через стрілку — 🥉.
- Зчеплення/розчеплення: состав — список, розчеплення в позиції k ділить його — 📎.
- Жеребкування цілі (5 з 8 у порядку) і перевірка «поспіль у порядку» — 🌱.
- Розвʼязувач Inglenook: BFS по станах (вміст трьох тупиків + витяжки), мінімум ходів — 🥈; з метрикою «мінімум зчеплень» (Дейкстра з вагами) — 🥇.
- Режим Timesaver на час проти режиму «мінімум ходів» — та сама гра, інший `score` — 📎.

## Мапа на каталог
- Є: `push-object` ↔ наїзд і штовхання вагонів; `pull-object` ↔ тягнення зчеплених; `button-toggle` ↔ переведення стрілки; `completion-detection` ↔ цільова розстановка; `move-counter` ↔ ходи/зчеплення; `time-bonus` ↔ гра на час; `cell-click` ↔ клік по стрілці/зчепленню; `level-solver`, `unsolvable-states`, `reachability-check` ↔ розвʼязувач і глухі кути; `difficulty-levels` ↔ кількість вагонів; `game-settings`; `movement-animation`.
- **Нема** → пропозиції карток:
  - `+rail-graph` «Поле — граф колій зі стрілками» · field · 🥉 · слоти {segments, points}.
  - `+couple-uncouple` «Зчеплення й розчеплення состава» · entities/interact · 📎.
  - `+track-capacity` «Ємність відрізка в одиницях» · entities/legality · 📎 · слот {capacity}.
  - `+switch-points` «Стрілка: стан визначає гілку руху» · entities/move · 🌱.
  - `+ordered-train-goal` «Ціль — N обʼєктів поспіль у заданому порядку» · game-logic/win · 🌱.
  - `+random-goal-draw` «Випадкова ціль на старті партії» · levels/generation · 🌱.
  - `+vehicle-restriction` «Відрізок закритий для типу обʼєкта» · entities/legality · 🌱 (родич `impassable-cells` «для типу»).
  - `+min-couplings-score` «Оцінка за мінімумом дій певного виду» · game-logic/score · 📎.

## Пропозиції до словників
- `+cond:capacity` — відрізок/клітина вміщає ще N одиниць (колії Inglenook, тупики); `count` рахує сутності на всьому полі, а тут — у конкретному контейнері.
- `+ui:target-sequence` — картка цільового порядку обʼєктів (потяг 1-2-3-4-5, список «вагон → пункт»).
- `+feature:random-goal-draw` — ціль партії тягнеться випадково (жеребкування, кубик, картки).
- `+card:couple-uncouple`, `+card:track-capacity`, `+card:rail-graph` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Train shunting puzzle](https://en.wikipedia.org/wiki/Train_shunting_puzzle) — визначення, обмеження, заборони для типів вагонів, шість класів задач, Sam Loyd і car hop, цифрові версії.
- [Wikipedia: Inglenook Sidings](https://en.wikipedia.org/wiki/Inglenook_Sidings) — Alan Wright, прототип Kilham Sidings, тупики 5/3/3, витяжка 3 + локомотив, 8 вагонів, потяг з 5.
- [Wikipedia: Timesaver](https://en.wikipedia.org/wiki/Timesaver) — John Allen, 11/1972, 5 стрілок і 5 тупиків, обгінна колія, фіксована швидкість, гра на час, кооперативна пара.
- [Wymann: правила Inglenook](https://www.wymann.info/ShuntingPuzzles/Inglenook/inglenook-rules.html) — 14 місць, жеребкування, порядок, три стратегії («рахуй з кінця»), 40 320.
- [Wymann: правила Timesaver](https://www.wymann.info/ShuntingPuzzles/Timesaver/timesaver-rules.html) — 5 вагонів у пункти A–E, час або мінімум ходів, ємність з локомотивом, розширене правило, логіка трафіку.
- [Wymann: Inglenook](https://www.wymann.info/ShuntingPuzzles/sw-inglenook.html) — «Tiddlywink Computer», варіант 1992 з гальмівним вагоном.

## Непевне
- (?) Що формально вважається «ходом» — джерела не визначають; у цифровій версії вибрано «рух до зупинки / зчеплення / стрілка».
- (?) Де саме формується цільовий потяг Inglenook і який вагон біля локомотива; стратегія «будуй з упору, починаючи з №5» натякає, що №1 — біля локомотива.
- (?) Чи наїзд автоматично зчіплює (на макетах з автозчепами — так), чи зчеплення — окрема дія.
- (?) Чи розчеплювати можна будь-де, чи лише над магнітами; правило «не переводити стрілку під вагоном» і заборона «летючої» маневрової стрілки — загальна практика, у відкритих джерелах не прочитано.
- (?) Точні ємності колій Timesaver, крім «D — не більше двох», і стартові позиції — лише на схемах.
- (?) Рік: Inglenook — 1970-ті (?), Timesaver — 1972; у шапці 1972.
