---
title: Robo Instructus
slug: robo-instructus
aka: []
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: partial
  random: none
  goal: state
year: 2019
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1032170/Robo_Instructus/", best: true, note: "Big AB Games, 16.07.2019; опис, скриншоти, демо"}
  - {kind: official, url: "https://www.roboinstruct.us/", note: "сайт гри: Steam, itch.io, devblog"}
  - {kind: itch, url: "https://bigabgames.itch.io/robo-instructus", note: "сторінка на itch.io"}
  - {kind: other, url: "https://blog.roboinstruct.us/2019/06/21/dark-stages.html", note: "етапи рівня, «сир» (хардкод під етап), темні етапи"}
  - {kind: other, url: "https://blog.roboinstruct.us/2018/06/15/probo-instructus.html", note: "зонд, детермінована конкурентність, time units і run score"}
  - {kind: other, url: "https://blog.roboinstruct.us/2017/12/15/introducing-new-game-solution-metrics.html", note: "метрики: час, solution size у вузлах AST, run size"}
  - {kind: other, url: "https://blog.roboinstruct.us/2018/07/13/robo-usables-2.html", note: "robo_use(), плитки-дані з напрямком, лаунчер"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robo+instructus+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, impassable-cells, reach-exit, sequential-levels, level-unlock, level-select, save-progress, tutorial-window, help-window, game-screen, achievements-window, +text-language-interpreter, +multi-stage-validation, +hidden-test-stages, +solution-size-metrics, +function-unlock-progression, +inline-stack-view, +concurrent-agents-lockstep, +location-id-api, +random-world-variants, +fall-off-edge]
proposes: ["+feature:multi-stage-tests", "+feature:hidden-test-stages", "+feature:solution-metrics", "+feature:function-unlocks", "+ui:inline-stack-values", "+ui:api-reference", "+ui:stage-tabs", "+cond:returned(call, value)", "+effect:sync_wait(call)", "+axis:control"]
author: opus
date: 2026-11-09
---

# Robo Instructus — одна текстова програма має провести робота через усі варіанти мапи, навіть ті, яких не видно

## Суть
Гравець пише код власною мовою гри, щоб робот на клітинній мапі дійшов до виходу. Головна відмінність від Karel/Lightbot: рівень складається з **кількох етапів** — варіантів тієї самої задачі, і одна програма мусить пройти всі. Хардкод під конкретний етап («сир») автор свідомо ламає **темними етапами** — прихованими варіантами, яких не видно, тож працює лише загальний алгоритм. Нові функції робота (`robo_scan`, `robo_use`, локації, зонд) відкриваються поступово разом із рівнями.

## Поле і час
- Квадратна сітка з безпечними клітинами, стінами й «порожнечею» за краєм; робот може впасти з краю мапи (зонд — ні, про це окремо каже автор).
- Рівень = кілька етапів (stages), кожен — своя мапа-варіант; частина етапів «темна» (план не показується).
- Час `programmed`: ціле число **time units (tu)** — сума тривалостей викликів `robo_*`; чистий код (обчислення, цикли) вважається миттєвим, тож швидкість інтерпретатора на рахунок не впливає.
- Пізні рівні: робот і зонд виконують **два окремі коди одночасно**; світ іде «lock-step» — просувається на найменшу тривалість серед очікуваних синхронних викликів (як одночасні ходи роглайка з різною довжиною ходу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | позиція, орієнтація | виконує виклики `robo_forward()`, `robo_left()` …; може впасти з краю |
| Зонд (probe, «Probo») | ally | позиція, орієнтація, швидший за робота | свій код тією ж мовою, `probo_forward()`, `probo_left()`; не падає з краю |
| Безпечна клітина | terrain | — | по ній можна ходити; `robo_scan()` бачить її як «невідомо» (?) |
| Стіна / перешкода | static | — | непрохідна |
| Порожнеча за краєм | hazard | — | крок туди — падіння, етап провалено (?) |
| Вихід | static | — | ціль етапу; у частині рівнів його не видно сканером |
| Usable-плитка «location» | switch | — | `robo_use()` повертає location id безпечної клітини (часто виходу) |
| Плитка-дані з напрямком | switch | — | `robo_use()` повертає абсолютний напрямок числом (1 — вгору, 2 — праворуч, …) |
| Лаунчер | terrain | — | перекидає робота; змушує відстежувати орієнтацію (деталі (?)) |
| Етап (stage) | zone | видимий / темний | окремий прогін тієї самої програми |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(run)` → ЯКЩО `custom: «код без синтаксичних помилок»` → ТО `custom: «програма запускається по черзі на кожному етапі рівня»`; інакше `message(error)` (відступи, імена).
- КОЛИ `exec(robo_forward)` → ЯКЩО `free(ahead)` → ТО `move(robot, facing)`, `counter(tu, +duration)`.
- КОЛИ `exec(robo_forward)` → ЯКЩО `cell(ahead, void)` → ТО `custom: «робот падає з мапи»`, `lose` для етапу (?).
- КОЛИ `exec(robo_left)` → ТО `rotate(robot, -90)`; `robo_right` — дзеркально (?).
- КОЛИ `exec(robo_scan)` → ТО `custom: «повертає ціле число про клітину попереду; у стеку видно напр. scan: -999»`; вихід сканер знаходить, але є рівні, де виходу не видно.
- КОЛИ `exec(robo_use)` → ЯКЩО `cell(robot, location_tile)` → ТО `custom: «повернути location id безпечної клітини»`.
- КОЛИ `exec(robo_use)` → ЯКЩО `cell(robot, direction_tile)` → ТО `custom: «повернути абсолютний напрямок (1 — вгору, 2 — праворуч …)»` — гравець сам переводить його у відносний за `facing`.
- КОЛИ `exec(robo_current_location)` / `exec(robo_forward_location)` → ТО `custom: «повернути id поточної / передньої клітини»`; `var` зберігає id для порівняння потім.
- КОЛИ `exec(robo_detect_adjacent)` → ТО `custom: «відомості про сусідні клітини»` (?).
- КОЛИ `enter(robot, launcher)` → ТО `custom: «робота перекинуто; орієнтація змінюється»` (?).
- КОЛИ `exec(probo_forward)` → ЯКЩО `cell(ahead, void)` → ТО `block` (зонд не падає).
- КОЛИ `exec(cmd)` (синхронний виклик robo_ / probo_) → ТО `custom: «виклик чекає, доки світ не відміряє його тривалість»`; світ просувається на мінімум серед очікуваних.
- КОЛИ `exec(cmd)` (чисте обчислення) → ТО `custom: «0 tu, але +1 до run size»`.
- КОЛИ `enter(robot, exit)` → ТО `custom: «етап пройдено, запуск наступного етапу»`.
- КОЛИ `custom: «усі етапи, включно з темними, пройдено»` → ТО `win`, `custom: «зарахувати метрики: tu, solution size, run size»`.
- КОЛИ `custom: «пройдено лише видимі етапи»` → ТО `unlock(next_level)`, але рахунок не зараховано.
- КОЛИ `level_end` → ТО `unlock(functions)` (нові `robo_*` і підказка-фрагмент коду на наступному рівні).
- Перемога: усі етапи рівня · Поразка: падіння / таймаут етапу (?) — лише невдалий прогін · Рахунок: менше = краще — time units, solution size (вузли AST без літералів і присвоєнь), run size (кількість виконаних операцій).

## Керування і ввід
- Ввід — **текстова мова гри** у вбудованому редакторі: відступи як блоки (помилки відступів — окреме повідомлення), `var`, цикли, умови, власні функції; усі значення — цілі числа.
- Редактор: автодоповнення, гарячі клавіші, буфер обміну системи, збереження/завантаження розвʼязків.
- Запуск, керування швидкістю виконання; під час виконання значення стеку показуються **inline поруч із кодом**.
- Кнопка довідки API — список доступних функцій з коротким описом.
- Прямого керування роботом нема.

## Вікна, меню, HUD
- `main-menu` → `level-select` (мапа «об'єкта»-полігону з рівнями (?)).
- `game-screen` = `code-editor` + світ: етапи вкладками (`stage-tabs`), робот і зонд на мапі, `instruction-highlight`, `inline-stack-values`, кнопка запуску, `speed-slider`.
- `help-window` — довідка API (`api-reference`), посилання на туторіали.
- `tutorial-window` / повідомлення рівня — частковий код-заготовка й пояснення нової функції.
- `end-screen` — метрики розвʼязку й порівняння (з друзями (?)).
- `achievements-window` (Steam-досягнення).
- `settings-window`: повноекранний / віконний режим, масштаб під DPI.

## Фічі поза полем
- `levels-sequential` з `level-unlock`; відкриття функцій мови як прогресія (`function-unlocks`).
- `multi-stage-tests` + `hidden-test-stages`: один розвʼязок перевіряється на наборі варіантів, частина прихована.
- `solution-metrics`: час, розмір коду, розмір прогону; детерміноване виконання гарантує однаковий рахунок на будь-якій машині.
- Збереження розвʼязків (`save-progress`), Steam Cloud, досягнення, 14 мов інтерфейсу.
- Демо-версія.

## Варіації й родичі
- [Karel](karel.md) — `+random-world-variants`: та сама ідея «програма для багатьох світів», але світи генеруються, а не задані етапами.
- [Untrusted](untrusted.md) і [The Farmer Was Replaced](the-farmer-was-replaced.md) — текстовий код замість іконок.
- [7 Billion Humans](7-billion-humans.md) — кілька виконавців одного коду; тут — два різні коди в lock-step.
- [Lightbot](lightbot.md), [RoboZZle](robozzle.md) — іконкові команди без тестів на варіантах.
- Осі варіацій: **перевірка** (одна мапа / кілька видимих / приховані тест-кейси); **мова** (іконки / текст / блоки); **сенсори** (нема / скан попереду / запит до плитки); **виконавці** (один / копії / різні з синхронізацією); **метрика** (зірки за розмір / час / операції).

## Цікавинки для курсу
- Прогін однієї програми на N варіантах мапи з прихованими кейсами — як автотести лабораторних — 🥈.
- Інтерпретатор невеликої мови з відступами, `var`, циклами й функціями — 🥇.
- Метрики: час у tu, розмір у вузлах AST (без літералів), кількість виконаних операцій — 🥈.
- Lock-step двох виконавців з різною тривалістю дій (світ іде на мінімум очікуваного) — 🥇.
- Inline-значення стеку поруч із рядком коду — 🥉.
- Плитка-дані з абсолютним напрямком і переклад у відносний за орієнтацією — 📎.

## Мапа на каталог
- Є: `command-program` ↔ програма робота; `user-procedures` ↔ власні функції; `sensor-predicates` ↔ `robo_scan`/`robo_use` у розгалуженнях; `step-execution` ↔ виконання з підсвіткою; `code-editor-window`; `reach-exit`; `sequential-levels`/`level-unlock`/`level-select`; `save-progress`; `tutorial-window`, `help-window`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+text-language-interpreter` «Власна текстова мова з інтерпретатором» · game-logic/program · 🥇.
  - `+multi-stage-validation` «Одна програма на кількох варіантах рівня» · game-logic/win · 🥈.
  - `+hidden-test-stages` «Приховані варіанти проти хардкоду» · game-logic/win · 🥉.
  - `+solution-size-metrics` «Метрики розвʼязку: час, розмір AST, операції» · game-logic/score · 🥈.
  - `+function-unlock-progression` «Нові команди відкриваються з рівнями» · levels/progression · 📎.
  - `+inline-stack-view` «Значення змінних поруч із кодом під час виконання» · interface/hud · 🥉.
  - `+concurrent-agents-lockstep` «Два коди одночасно в lock-step» · game-logic/program · 🥇.
  - `+location-id-api` «Клітини як id, що їх можна зберегти й порівняти» · game-logic/program · 📎.
  - `+fall-off-edge` «Крок за край — падіння» · entities/death · 🌱.

## Пропозиції до словників
- `+feature:multi-stage-tests` — розвʼязок перевіряють на кількох варіантах рівня.
- `+feature:hidden-test-stages` — частина варіантів невидима гравцеві (темні етапи).
- `+feature:solution-metrics` — час/розмір/операції як рахунок розвʼязку.
- `+feature:function-unlocks` — нові команди мови як прогресія.
- `+ui:inline-stack-values` — значення змінних поруч із рядком коду.
- `+ui:api-reference` — список доступних функцій з описами.
- `+ui:stage-tabs` — перемикач етапів одного рівня.
- `+cond:returned(call, value)` — значення, яке повернув сенсорний виклик (`robo_scan() is …`).
- `+effect:sync_wait(call)` — дія чекає синхронізації світу (lock-step двох виконавців).
- `+axis:control` — значення `programmed-text` (текстова мова) проти `programmed` іконками (?).

## Джерела
- ⭐ [Steam: Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus/) — опис («simple programming language», нові функції з прогресом), дата, платформи, демо.
- [Сайт гри](https://www.roboinstruct.us/) — лінки на Steam, itch.io і devblog.
- [Dark Stages & The Fight Against Cheese](https://blog.roboinstruct.us/2019/06/21/dark-stages.html) — етапи як варіанти задачі, хардкод, темні етапи, прогрес без повного рахунку.
- [Probo Instructus — Deterministic Concurrency](https://blog.roboinstruct.us/2018/06/15/probo-instructus.html) — зонд, lock-step, tu та run score.
- [Introducing New Game Solution Metrics](https://blog.roboinstruct.us/2017/12/15/introducing-new-game-solution-metrics.html) — час, solution size у вузлах, run size.
- [Robo Usables](https://blog.roboinstruct.us/2018/07/06/robo-usables.html) і [More Robo Usables](https://blog.roboinstruct.us/2018/07/13/robo-usables-2.html) — `robo_use()`, location id, плитки з напрямком, лаунчер, `var`.
- [A Window To The Stack](https://blog.roboinstruct.us/2017/11/03/a-window-to-the-stack.html) — inline-значення стеку (`scan: -999`).
- [Robo Concurrency](https://blog.roboinstruct.us/2018/03/09/robo-concurrency.html) — другий виконавець у пізній грі.

## Непевне
- (?) Точний синтаксис мови (ключові слова `fun`, `loop`, `if`, `while`, `for`, `seq`, `is`, `return`) — з памʼяті; у відкритих дописах видно лише ілюстративний сніпет і `var`.
- (?) Значення, які повертає `robo_scan()`, і чи є `robo_right()` — не підтверджено.
- (?) Що буває при падінні / таймауті етапу; чи є ліміт часу прогону.
- (?) Поведінка лаунчера й `robo_detect_adjacent()`; що таке `robo_translate()` (лише назва допису).
- (?) Вигляд `level-select` (мапа полігону) і порівняння метрик з друзями (лише назва допису «Compare Against Your Friends»).
- (?) Кількість рівнів і етапів на рівень.
