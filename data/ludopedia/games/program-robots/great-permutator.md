---
title: Great Permutator
slug: great-permutator
aka: []
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2014
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/319270/Great_Permutator/", best: true, note: "Ripatti Software, 15.09.2014: конвеєри й пристрої везуть кольорові ящики в потрібні місця в потрібному порядку; 50 + 15 рівнів, 10+ блоків дій, редактор з обміном, глобальна таблиця; 6 знімків, 3 трейлери, демо"}
  - {kind: other, url: "https://www.steamcardexchange.net/index.php?gamepage-appid-319270", note: "картки Steam = блоки дій: Trigger, Swapper, Accumulator, Duplicator, Analyzer, Reactor; фон «Action Blocks»"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=341018015", note: "гайд-розвʼязки картинками: Level 1–50, бонус-набори MT / RND / BB по 5 рівнів, назви досягнень; у коментарях — UT знищує ящики"}
  - {kind: other, url: "https://steamcommunity.com/app/319270/discussions/0/2271447149946038913/", note: "щоденник гравця з топ-10: розвʼязок міряють «tiles covered» і «cycles», рівні розкладено сторінками"}
  - {kind: other, url: "https://steamcommunity.com/app/319270/discussions/0/4939872515506592770/", note: "розробник: гра «на інсайт», нові типи блоків урізноманітнюють рівні, змагання — мінімум деталей у таблиці"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Great+Permutator+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [row-conveyor, path-drawing, tile-rotate, drag-drop-piece, cursor-place, cell-click, teleport-pair, cell-transform, game-pause, undo-redo, objective-text, sequential-levels, level-select, level-rating, leaderboard, score-records, in-game-editor, editor-palette, editor-playtest, level-exchange, game-settings, game-screen, +alternating-router, +ordered-output, +collision-halt, +solution-metrics, +metric-histograms, +grade-threshold, +limited-blocks, +item-destroyer, +randomizer-block, +input-lock-test, +multi-port-device]
proposes: ["+role:device", "+effect:route(a, port)", "+effect:toggle(a)", "+cond:next_expected(sink, color)", "+ui:tiles-counter", "+feature:input-lock", "+feature:grade-threshold", "+card:alternating-router", "+card:ordered-output"]
author: opus
date: 2026-11-19
---

# Great Permutator — конвеєрами й блоками дій переставити кольорові ящики так, щоб унизу вони склались у задані стоси

## Суть
Пазл-«фабрика» на сітці 11×11: згори в поле заходять черги кольорових ящиків (червоні, жовті, сині), а внизу кожен вихід чекає стос певних кольорів **у певному порядку**. Гравець прокладає конвеєри й ставить багатоклітинні блоки дій з обмеженого запасу: тригер почергово розводить ящики ліворуч і праворуч, обмінник міняє колір, телепорт переносить. Play — і ящики їдуть тактами; зіткнення, ящик не на тому виході чи забутий на полі — провал. Розробник називає гру «на інсайт»: ідея рівня проста, коли вже побачив її, а повторна гра — мінімізувати кількість зайнятих клітин у світовій таблиці.

## Поле і час
- Поле 11×11 клітин (огляд Steam і знімки). Над верхнім краєм — 1–6 вхідних стовпчиків з чергою ящиків, під нижнім — вихідні стовпчики з еталонним стосом кольорів.
- Шари: підлога (звичайна або тріснута, на тріснутій будувати не можна) · конвеєри зі стрілкою напрямку · блоки дій на кілька клітин (на знімках SWA і ACC займають 3×2) з портами-стрілками входу й виходу · ящики.
- Час `programmed`: будуєш у спокої, Play запускає такти (лічильник «Cycles elapsed»), ▶▶ прискорює, ‖ ставить на паузу, ■ повертає до розстановки.
- Основні 50 рівнів детерміновані; бонусний набір RND має блок-рандомізатор — звідси `random: runtime`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ящик | object | колір: червоний / жовтий / синій | їде конвеєрами й крізь блоки дій; зіткнення двох ящиків зупиняє запуск |
| Вхід | source | черга кольорів | згори подає ящики в поле по одному, у фіксованому порядку |
| Вихід | sink | еталонний стос кольорів | приймає ящики знизу; має отримати точну послідовність |
| Конвеєр | terrain | напрямок (клік повертає) | везе ящик на сусідню клітину за стрілкою |
| Тріснута клітина | static | — | на ній не можна нічого поставити |
| Закріплений елемент | static | — | поставлений рівнем заздалегідь, не прибирається |
| Trigger (TR) | switch | стан: наступний вихід лівий або правий | почергово відправляє вхідні ящики ліворуч і праворуч (підказка в грі) |
| Exchanger (EXCH) | terrain | — | змінює колір ящика, що проходить крізь нього |
| Телепорт IN → OUT | terrain | пара блоків | ящик, що заїхав в IN, зʼявляється біля OUT («працює як портал») |
| Utilizer (UT) | sink | — | знищує ящики, які в нього заходять |
| Swapper (SWA) | container | 3×2, два входи й два виходи (знімок) | поведінку не перевірено — див. «Непевне» |
| Accumulator (ACC) | container | 3×2 (знімок) | поведінку не перевірено; огляди кажуть про пристрої, що «збирають і випускають» ящики |
| Duplicator (DUP) | spawner | — | поведінку не перевірено |
| Analyzer (ANLYZR) | switch | — | поведінку не перевірено |
| Randomizer (RND) | switch | — | є в бонус-рівнях RND; поведінку не перевірено |
| Reactor | — | — | назва лише з картки Steam; вигляд і поведінка невідомі |
| Запас блоків | supply | ×N для кожного типу | кількість блоків рівня обмежена, лічильник у пулі праворуч |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, path)` → ЯКЩО `free(cell)` і `not cell(cell, cracked)` → ТО `place(player, conveyor)` у кожну клітину шляху, `counter(tiles_covered, +1)` за клітину.
- КОЛИ `input(click, conveyor)` → ТО `rotate(conveyor, 90)`.
- КОЛИ `input(drag, action_block)` → ЯКЩО `has(pool, block)` і `fits(block, cells)` → ТО `place(player, block)`, `take(pool, block)`.
- КОЛИ `input(right_drag)` → ТО `disappear(part)` — стерти конвеєри й блоки під курсором.
- КОЛИ `input(click, action_block)` → ТО `set_state(block, output_order)` — перемкнути, з якого виходу піде наступний ящик (огляд Steam).
- КОЛИ `input(click, input)` → ТО `set_state(input, locked)` — заблокований вхід не подає ящиків; так тестують частину машини.
- КОЛИ `input(play)` → ТО `timer(start)`; щотакт `counter(cycles, +1)`.
- КОЛИ `tick` → ЯКЩО `cell(cell_under_box, conveyor)` → ТО `move(box, conveyor_dir)`.
- КОЛИ `enter(box, trigger)` → ТО `custom: «ящик виходить з порту, на який вказує стан»`, `set_state(trigger, other_side)`.
- КОЛИ `enter(box, exchanger)` → ТО `transform(box, other_color)`.
- КОЛИ `enter(box, teleport_in)` → ТО `teleport(box, teleport_out)`.
- КОЛИ `enter(box, utilizer)` → ТО `disappear(box)`.
- КОЛИ `contact(box, box)` → ТО `crash` — діалог «Crash! collision of boxes», місце позначено знаком ⊘.
- КОЛИ `enter(box, output)` → ЯКЩО `custom: «колір збігається з наступним у еталонному стосі виходу»` → ТО `counter(delivered, +1)`; інакше спроба провалена.
- КОЛИ `custom: «ящик лишився на полі, а входи порожні»` → ТО спроба провалена (огляд JIG: «left behind»).
- КОЛИ `all_on(box, output)` → ТО `win`, `message(tiles covered, cycles)`.
- КОЛИ `level_end` → ЯКЩО `counter(tiles_covered, <=, a_plus_limit)` → ТО оцінка A+ і досягнення рівня.
- Перемога: усі виходи отримали свої стоси в правильному порядку · Поразка: краш, хибний вихід або забутий ящик — правиш машину й запускаєш знову · Рахунок: «Tiles covered» (основна метрика й поріг A+), «Cycles» (друга), світова таблиця за клітинами.

## Керування і ввід
- Миша: клік і перетягування кладуть стрічку конвеєра; клік по конвеєру повертає його; права кнопка з перетягуванням стирає.
- Блоки дій перетягують з пулу праворуч; під пулом видно, скільки лишилось (×0, ×1).
- Клік по будівлі перемикає її вихід; клік по входу блокує його для часткового тесту.
- Кнопки: ▶ запуск · ▶▶ швидше · ‖ пауза · ■ стоп · Undo · Redo · Best. Гарячі клавіші додано у v1.18 (для німецької розкладки можна поміняти Z і Y).

## Вікна, меню, HUD
- `game-screen`: поле 11×11 з входами згори й виходами знизу; HUD — `custom: «Tiles covered N/M»` (M — поріг A+), `custom: «Cycles elapsed»`, `level-number` зі зірками складності (0–4), `tool-palette` блоків з лічильниками, `objective-text` — зелена панель підказки рівня («Build conveyors to move boxes from the top side to the bottom one»).
- `custom-window` краху: «Crash! collision of boxes» + OK; місце зіткнення позначено на полі.
- `level-select`: сторінки рівнів (page 1, page 2…) і бонусні набори MT, RND, BB по 5 рівнів.
- `editor-window`: рівень «[no name]», кнопки новий / відкрити / зберегти / зберегти як / ▶ тест / вихід; Undo · Redo · Share; перемикач «Fixed Supplies»; палітра всіх блоків (TR, SWA, EXCH, ACC, DUP, UT, ANLYZR, фіолетовий блок з маніпулятором, RND); конструктор входів і виходів — стовпчики кольорів з хрестиком «прибрати»; поле «Tiles for A+ grade: N».
- `settings-window`: Options, перероблене у v1.18 — режими для дальтоніків, заміна Z/Y.
- `leaderboard`: глобальна таблиця за клітинами (гравці пишуть про топ-10 рівня).
- Переходи: level-select → game-screen → (▶) симуляція → краш-діалог або перемога → level-select; меню → editor-window → ▶ тест.

## Фічі поза полем
- `levels-sequential`: 50 рівнів сторінками + 15 бонусних (MT, RND, BB); новий тип блока зʼявляється кожні кілька рівнів, складність іде «пилкою» (відгук RAWG).
- `undo` / `redo`; `pause`; блокування входів як налагодження.
- `leaderboard-online` + метрики tiles / cycles; гравці згадують гістограму кількості блоків (обговорення Steam).
- `level-editor` з обміном через інтернет (Share) — за сторінкою Steam.
- `colorblind-palette` (v1.18), `remap-controls` у мінімумі (Z/Y).
- `achievements`: 16 у Steam (рівні Easy / Medium / Hard / Very Hard); назви з гайду — exact cover, three in a row, unnecessary parts, why so slow?, triple crash, synchronization, oops no more boxes, box overflow.
- Картки Steam «розкривають будову кожного стандартного блока дій» (анонс 2015) — довідник блоків через колекцію.
- Безкоштовне демо з першими рівнями.

## Варіації й родичі
- [manufactoria](manufactoria.md) — конвеєри й кольорові сортувальники, але перевіряється стрічка-рядок, а не стоси на виходах.
- [spacechem](spacechem.md), [lightbot](lightbot.md) — Steam сам ставить їх поруч як «інженерні пазли».
- [turing-tumble](turing-tumble.md) — «біт», що почергово кидає кульку ліворуч і праворуч, — те саме, що Trigger.
- [factorio-belts](../build-sim/factorio-belts.md), [shapez](../build-sim/shapez.md) — стрічки й сортувальники без жорсткого порядку на виході.
- Осі варіацій: **маршрутизатор** — почерговий (Trigger) / за кольором (?) / випадковий (RND); **перевірка виходу** — стос у точному порядку / множина / потік; **метрика** — клітини / такти / кількість блоків; **запас блоків** — фіксований рівнем / вільний (редактор, «Fixed Supplies»).

## Цікавинки для курсу
- Симуляція конвеєрної сітки тактами з виявленням зіткнень двох ящиків — 🥉: черга руху й конфлікти за клітину.
- Trigger як маршрутизатор зі станом (почергово L/R, клік задає початок) — 📎: один біт стану на блок.
- Вихід як стек з еталоном: перевірка кожного ящика на льоту й «забутий ящик» наприкінці — 📎.
- Задача перестановки: з порядку на вході зробити заданий порядок на виході — 🥇: сортувальні мережі з обмеженим набором операцій.
- Редактор рівня з конструктором входів/виходів, запасом блоків і порогом A+ — 🥉.
- Метрики «клітини / такти» з порогом оцінки й світовим рекордом — 📎.

## Мапа на каталог
- Є: `row-conveyor` ↔ конвеєри · `path-drawing` ↔ стрічка перетягуванням · `tile-rotate` ↔ клік повертає конвеєр · `drag-drop-piece` ↔ блоки з пулу · `cursor-place` ↔ тріснуті клітини · `cell-click` ↔ перемикання виходу / блокування входу · `teleport-pair` ↔ IN/OUT · `cell-transform` ↔ Exchanger · `game-pause` · `undo-redo` · `objective-text` ↔ панель підказки · `sequential-levels` / `level-select` ↔ сторінки й бонус-набори · `level-rating` ↔ зірки складності · `leaderboard` / `score-records` · `in-game-editor` / `editor-palette` / `editor-playtest` / `level-exchange` ↔ редактор із Share · `game-settings` ↔ Options · `game-screen`.
- **Нема** → пропозиції карток:
  - `+alternating-router` «Маршрутизатор, що почергово міняє вихід» · entities/interact · 📎 · слот {outputs: 2, start: left|right}.
  - `+ordered-output` «Вихід приймає стос у заданому порядку» · game-logic/win · 📎.
  - `+collision-halt` «Зіткнення зупиняє симуляцію» (Opus Magnum) · game-logic · 📎.
  - `+solution-metrics` + `+metric-histograms` · interface/results · 📎 / 🥉.
  - `+grade-threshold` «Оцінка A+ за порогом метрики» · game-logic/score · 🌱 · слот {limit: N клітин}.
  - `+limited-blocks` «Обмежений запас деталей рівня» · game-logic/constraints · 🌱.
  - `+item-destroyer` «Пристрій-знищувач предметів» · entities/interact · 🌱.
  - `+randomizer-block` «Блок випадкового вибору» · entities/interact · 📎.
  - `+input-lock-test` «Вимкнути вхід, щоб перевірити частину машини» · interface/input · 🌱.
  - `+multi-port-device` «Пристрій на кілька клітин з портами входу й виходу» · entities/state · 🥉.

## Пропозиції до словників
- `+role:device` — блок дій на кілька клітин з портами (Trigger, Swapper, Accumulator); ширше за `switch`.
- `+effect:route(a, port)` — пристрій відправляє предмет у свій вихідний порт; `+effect:toggle(a)` — перемкнути двостановий стан (Trigger після кожного ящика).
- `+cond:next_expected(sink, color)` — вихід чекає саме цей колір наступним.
- `+ui:tiles-counter` — «Tiles covered N/M» з порогом оцінки.
- `+feature:input-lock` — заблокувати вхід для часткового тесту; `+feature:grade-threshold` — оцінка A+ за порогом клітин.
- `+card:alternating-router`, `+card:ordered-output`.

## Джерела
- ⭐ [Steam: Great Permutator](https://store.steampowered.com/app/319270/Great_Permutator/) — опис, 50 + 15 рівнів, 10+ блоків, редактор з обміном, таблиця; 6 знімків: поле 11×11, «Tiles covered N/M», «Cycles elapsed», краш-діалог, блоки IN/OUT, SWA, ACC, DUP, TR, ANLYZR, RND, вікно редактора з палітрою всіх блоків, підказка «Trigger: sends incoming boxes to the left or to the right in turns».
- Steam API: appdetails (розробник, дата, офіційний сайт) і новини — оновлення v1.18 (режими для дальтоніків, гарячі клавіші, нова таблиця, «black box 4 bug») та анонс карток 2015.
- [Steam Card Exchange](https://www.steamcardexchange.net/index.php?gamepage-appid-319270) — назви 6 карток = блоків дій.
- [Гайд Steam: розвʼязки й досягнення](https://steamcommunity.com/sharedfiles/filedetails/?id=341018015) — розділи Level 1–50 і MT / RND / BB 1–5, назви досягнень, коментар про UT.
- [Обговорення: щоденник топ-10](https://steamcommunity.com/app/319270/discussions/0/2271447149946038913/) і [«Чи для програмістів гра?»](https://steamcommunity.com/app/319270/discussions/0/4939872515506592770/) — метрики tiles і cycles, відповідь розробника, рівні «1-star / 2-star».
- Відгуки Steam — поле 11×11, ящики згори вниз, обмежений запас блоків, клік по будівлі міняє вихід, undo/redo, поріг A+, світовий рекорд на сервері.
- Огляд JayIsGames (jayisgames.com/review/great-permutator.php; сторінка тепер обросла спамом) — конвеєри перетягуванням, клік повертає, права кнопка стирає, тріснуті клітини, закріплені блоки, Trigger / Exchanger / Teleporter, три кольори, провал через зіткнення, хибний вихід або забутий ящик, блокування входів, A+ за лімітом клітин.
- YouTube: пошук «Great Permutator gameplay».

## Непевне
- (?) Поведінка Swapper, Accumulator, Duplicator, Analyzer, Randomizer і Reactor у відкритих джерелах не описана; з назв — переставляє пару ящиків, накопичує й випускає пачкою, подвоює ящик, розводить за кольором, вибирає вихід випадково. Чи фіолетовий блок з маніпулятором у палітрі редактора — це Reactor, невідомо.
- (?) Що означають набори MT і BB: BB — імовірно «black box» (у патчі v1.18 згадано «black box 4 bug»), MT — невідомо.
- (?) Чи ящик на хибному виході одразу зупиняє запуск, чи помилку видно лише наприкінці; швидкість — 1 клітина за такт — не перевірено.
- (?) Огляд JIG на старті казав, що редактора нема, а Steam перелічує редактор і обмін рівнями — певно, додано оновленням; гравець у 2023 скаржився, що нормального обміну так і нема.
- (?) Зірки біля номера рівня — складність (так їх називають розробник і гравці), а не оцінка гравця.
- (?) Кнопка Best і гістограма кількості блоків — з обговорень; точний вигляд не бачив. Що таке «Challenge 3000 → 2900» з патчу (сумарний рекорд клітин?) — невідомо.
- (?) Офіційний сайт ripattisoftware.com/greatpermutator/ і мануал Steam не відкрились (ECONNREFUSED), тож повного списку блоків з описами нема.
