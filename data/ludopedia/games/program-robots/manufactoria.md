---
title: Manufactoria
slug: manufactoria
family: program-robots
also: [build-sim, thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2010
platforms: [web (Flash), PC (Manufactoria 2022)]
links:
  - {kind: other, url: "https://www.jayisgames.com/review/manufactoria.php", best: true, note: "огляд + проходження: деталі, стрічка, accept/drop, керування в коментарях"}
  - {kind: official, url: "https://pleasingfungus.com/Manufactoria/", note: "сторінка автора (Flash); при перевірці — помилка SSL"}
  - {kind: other, url: "https://nayuki.io/page/manufactoria-solutions", note: "розвʼязки всіх 31 рівня з кількістю деталей і алгоритмами"}
  - {kind: other, url: "https://www.404techsupport.com/2010/05/manufactoria-making-turing-machines-fun-again/", note: "огляд 2010: конвеєри, розгалуження red/blue/кінець, автор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Queue_automaton", note: "модель: скінченний автомат + черга; Manufactoria у See also"}
  - {kind: steam, url: "https://store.steampowered.com/app/1276070/Manufactoria_2022/", note: "Manufactoria 2022 — сиквел (8 типів машин, 100+ пазлів)"}
  - {kind: other, url: "https://www.metafilter.com/92162/Manufactoria", note: "обговорення 2010"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=manufactoria+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [row-conveyor, cell-click, drag-drop-piece, sequential-levels, level-unlock, level-select, game-pause, game-screen, end-screen, +queue-tape, +branch-reader, +tape-writer, +conveyor-bridge, +accept-reject-spec, +random-test-cases, +failing-test-view, +solution-metrics, +part-count-score, +level-code-share, +step-execution, +level-editor-custom-spec]
proposes: ["+trigger:enter", "+trigger:exec(cmd)", "+cond:tape_head(c)", "+effect:pop_tape", "+effect:push_tape(c)", "+effect:accept", "+effect:reject", "+role:terrain", "+role:cargo", "+window:test-results", "+window:spec-window", "+ui:tape-view", "+ui:part-counter", "+ui:speed-slider", "+feature:random-test-cases", "+feature:share-code", "+axis:control"]
author: opus
date: 2026-11-02
---

# Manufactoria — фабрика конвеєрів як машина Тюрінга: читай кольори зі стрічки робота й сортуй

## Суть
Гравець будує на сітці «тестувальну фабрику» з конвеєрів і розгалужувачів; через неї проходять роботи, кожен несе **стрічку-чергу** кольорових точок. Розгалужувач читає перший колір і знімає його зі стрічки, письмак дописує колір у кінець. Робот, що дійшов до виходу, прийнятий; той, що впав з конвеєра на підлогу, — відбракований. Завдання рівня — специфікація мови («прийняти, якщо закінчується синім», «прийняти, якщо стрічка — паліндром», «вивести вхід задом наперед»): гравець фактично програмує черговий автомат, еквівалентний машині Тюрінга.

## Поле і час
- Квадратна сітка фабрики, розмір росте з рівнями (?); вхід робота — згори по центру, вихід (accept) — знизу.
- Кожна клітина містить одну деталь з напрямком (4 повороти + дзеркальне відображення для розгалужувачів); порожня клітина — «підлога».
- Час `programmed`: «програма» — розставлені деталі; на тік робот переходить на одну клітину й деталь діє на нього та його стрічку.
- Стрічка — черга символів red/blue (пізніше green/yellow); red/blue часто кодують 0/1.
- Тести: гра проганяє набір роботів з різними стрічками (згенеровані), рішення приймається, лише якщо всі тести пройдено.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | object | стрічка-черга кольорів | їде за конвеєрами; на підлозі — відбракований |
| Стрічка | mark | послідовність red/blue/green/yellow | читається з голови, пишеться в хвіст |
| Конвеєр | terrain | напрямок | переносить робота на клітину в напрямку |
| Міст / перехрестя конвеєрів | terrain | дві осі | два потоки перетинаються без змішування (?) |
| Розгалужувач red/blue | terrain | орієнтація, дзеркало | голова red → в одну сторону, blue → в іншу (символ знято); інше/порожньо → прямо |
| Розгалужувач green/yellow | terrain | орієнтація, дзеркало | те саме для green/yellow (пізніші рівні) |
| Письмак red/blue/green/yellow | terrain | колір, напрямок | дописує колір у кінець стрічки, робот їде далі |
| Вхід | spawner | — | випускає наступного тестового робота |
| Вихід (accept) | static | — | робот прийнятий; на output-рівнях порівнюється стрічка |
| Підлога | hazard | — | робот падає → відбракований (reject) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(robot)` → ТО `spawn_at(robot, entry)` зі стрічкою тесту.
- КОЛИ `enter(robot, conveyor)` → ТО `move(robot, conveyor_dir)`.
- КОЛИ `enter(robot, branch_rb)` → ЯКЩО `tape_head(red)` → ТО `pop_tape`, `move(robot, side_a)`; ЯКЩО `tape_head(blue)` → ТО `pop_tape`, `move(robot, side_b)`; інакше (інший колір або порожня) → ТО `move(robot, straight)` без зняття.
- КОЛИ `enter(robot, branch_gy)` → аналогічно для green/yellow.
- КОЛИ `enter(robot, writer[c])` → ТО `push_tape(c)`, `move(robot, writer_dir)`.
- КОЛИ `enter(robot, floor)` → ТО `reject` (робот скинуто на підлогу).
- КОЛИ `enter(robot, exit)` → ТО `accept`.
- КОЛИ `custom: «робот не рухається / цикл без кінця»` → ТО тест провалено (?) (ліміт кроків).
- КОЛИ тест закінчився → ЯКЩО рішення фабрики (accept/reject, на output-рівнях — ще й вміст стрічки) = специфікація → ТО наступний тест; інакше `message(«failed»)` + показати стрічку провального тесту.
- КОЛИ `all_constraints_met` (усі тести) → ТО `win`, `message(кількість деталей)`, відкрити наступні рівні.
- Типові рівні (з Nayuki): прийняти, якщо закінчується синім; дописати три red (×8 у двійковій); інкремент/декремент двійкового числа; перевірка «≥16»; парність нулів; баланс пар blue-red; реверс стрічки; порівняння першого й останнього символу; фінальні Seraphim/Ophanim/Metatron — багатопрохідні алгоритми з маркерами green/yellow.
- Перемога: усі тести відповідають специфікації · Поразка: нема — помилка лише показує провальний тест, штрафів нема · Рахунок: кількість деталей (менше — краще).

## Керування і ввід
- Палітра деталей зліва → клік/перетяг на клітину; клавіші повертають деталь (4 напрямки), **пробіл** дзеркалить розгалужувач.
- Видалення деталі; деталей необмежено.
- Запуск тестів (Play), стоп (червоний квадрат), повзунок швидкості; покрокового режиму в оригіналі нема (?).
- Збереження/завантаження рішення (іконка дискети); вставка коду рівня/рішення (Shift+V).

## Вікна, меню, HUD
- `splash-screen` / інтро-екрани (D або → гортає).
- `level-select` — дерево рівнів-«замовлень» (Robotoast!, Robocoffee! …) з розгалуженням: нижня гілка відкриває письмаків і нові кольори.
- `game-screen`: сітка фабрики; `tool-palette` деталей; `spec-window`/`objective-text` — умова рівня; `tape-view` поточного робота (кольорові кружечки); кнопки Play/Stop; `speed-slider`.
- `test-results` (custom): поточний тест, стрічка, результат; при помилці — стрічка, на якій фабрика помилилась.
- `end-screen`: «успіх» + кількість використаних деталей.
- `editor-window`: створення власного рівня з умовою й тестами, обмін кодом (?).
- Переходи: дерево рівнів → рівень → Play → (помилка) показ тесту → правка → (успіх) екран результату → дерево.

## Фічі поза полем
- `random-test-cases`: набір тестових стрічок, у тому числі згенерованих; рішення не можна «підігнати» під один приклад.
- `solution-metrics`: кількість деталей; спільнота (Nayuki) змагається за мінімум.
- `share-code` / `export-import`: рішення і власні рівні як текстові коди в коментарях.
- `level-editor` з власною специфікацією (?).
- `speed-control`, `restart-level`.
- Manufactoria 2022: 8 типів машин, 100+ пазлів, сюжетний режим «гаражний стартап → корпорація», медалі, глобальні лідерборди, ачивки.

## Варіації й родичі
- Сиквел Manufactoria 2022 (PleasingFungus Games); родичі автора — Silicon Zeroes.
- Родичі: Turing Tumble (механічні біти), TuringKara (машина Тюрінга на 2D-аркуші), Factorio-розподільники (фільтри як розгалужувачі), SpaceChem/Opus Magnum (просторове програмування).
- Осі варіацій: **памʼять** (нема — DFA / черга — Manufactoria / стек / 2D-аркуш — TuringKara); **результат** (accept/reject / вихідна стрічка); **алфавіт** (2 / 4 кольори); **метрика** (деталі / площа / такти).

## Цікавинки для курсу
- Черговий автомат на сітці: розгалужувач = `pop` + умовний перехід, письмак = `push` — 🥈 (симулятор + перевірка).
- Генератор тестових стрічок для специфікації мови й порівняння з еталонним предикатом — 🥉.
- Показ провального тесту (контрприклад) — 📎.
- Дзеркальне відображення деталі (chirality) поряд з поворотом — 🌱.
- Рівні як формальні мови (паліндром, баланс, двійкова арифметика) — 🥇 за повний набір з генерацією тестів.
- Код рішення/рівня для обміну — 📎.

## Мапа на каталог
- Є: `row-conveyor` (конвеєри) · `cell-click` / `drag-drop-piece` (розстановка) · `sequential-levels` / `level-unlock` / `level-select` (дерево замовлень) · `game-pause` (стоп) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+queue-tape` «Стрічка-черга на обʼєкті» · entities/state · 🥉 · слот {alphabet}.
  - `+branch-reader` «Розгалужувач за символом голови» · entities/interact · 🥉 · слоти {colors, consume: yes}.
  - `+tape-writer` «Письмак дописує символ» · entities/interact · 📎.
  - `+conveyor-bridge` «Перехрестя потоків» · entities/move · 📎.
  - `+accept-reject-spec` «Прийняти/відбракувати за специфікацією» · game-logic/win · 🥉.
  - `+random-test-cases` (спільна з 7 Billion Humans) · levels/solvability · 🥉; `+failing-test-view` · interface/hud · 📎.
  - `+solution-metrics` / `+part-count-score` · game-logic/score · 🌱.
  - `+level-code-share` · levels/editor · 📎; `+level-editor-custom-spec` · levels/editor · 🥈.
  - `+step-execution` · interface/input · 🥉.

## Пропозиції до словників
- `+trigger:enter` — робот став на деталь; `+trigger:exec(cmd)` — деталь як інструкція.
- `+cond:tape_head(c)` — перший символ стрічки = c (порожня — окремий випадок).
- `+effect:pop_tape`, `+effect:push_tape(c)` — черга як памʼять обʼєкта.
- `+effect:accept` / `+effect:reject` — вердикт тесту замість win/lose одного запуску.
- `+role:terrain` (деталі під роботом), `+role:cargo` — робот як вантаж зі станом.
- `+window:test-results`, `+window:spec-window`; `+ui:tape-view`, `+ui:part-counter`, `+ui:speed-slider`.
- `+feature:random-test-cases`, `+feature:share-code`.
- `+axis:control` — `programmed` (просторова програма).

## Джерела
- ⭐ [JayIsGames: Manufactoria](https://www.jayisgames.com/review/manufactoria.php) — огляд (2010), checkpoint знімає прочитаний колір, accept/drop, пробіл дзеркалить, Shift+V, дискета-збереження.
- [Nayuki: розвʼязки](https://nayuki.io/page/manufactoria-solutions) — 31 рівень з назвами, кількістю деталей і алгоритмами; метрика — кількість деталей.
- [404 Tech Support](https://www.404techsupport.com/2010/05/manufactoria-making-turing-machines-fun-again/) — red → праворуч, blue → ліворуч, кінець стрічки → вниз; автор Nicholas Feinberg; Kongregate.
- [Wikipedia: Queue automaton](https://en.wikipedia.org/wiki/Queue_automaton) — формальна модель.
- [Steam: Manufactoria 2022](https://store.steampowered.com/app/1276070/Manufactoria_2022/) — сиквел.
- [pleasingfungus.com/Manufactoria](https://pleasingfungus.com/Manufactoria/) — оригінал (Flash).
- [MetaFilter](https://www.metafilter.com/92162/Manufactoria) — обговорення.

## Непевне
- (?) Сторінка автора не відкрилась (SSL); Wikipedia-статті про гру нема.
- (?) «Вісь malfunctioning» з брифу куратора: у джерелах роботи — «дефектні» (з «murder sprees»), яких треба скидати; окремої механіки «malfunction» не знайдено.
- (?) Наявність мосту/перехрестя як окремої деталі, розмір поля по рівнях, ліміт кроків тесту — з памʼяті.
- (?) Редактор власних рівнів в оригіналі 2010 (у коментарях JayIsGames є коди рівнів) — назва й можливості не перевірені.
- (?) Яка сторона розгалужувача для red, яка для blue, залежить від орієнтації й дзеркала — у 404 Tech Support дано для базової орієнтації.
