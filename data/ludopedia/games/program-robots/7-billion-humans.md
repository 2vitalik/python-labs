---
title: 7 Billion Humans
slug: 7-billion-humans
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2018
platforms: [PC, Mac, Linux, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/7_Billion_Humans", best: true, note: "ядро: одна програма на всіх, step/cycle челенджі, 25 випадкових перевірок"}
  - {kind: official, url: "https://tomorrowcorporation.com/7billionhumans", note: "сайт студії, лінки на всі магазини"}
  - {kind: steam, url: "https://store.steampowered.com/app/792100/7_Billion_Humans/", note: "Steam, 60+ рівнів, hint/skip"}
  - {kind: official, url: "https://www.destructoid.com/reviews/review-7-billion-humans/", note: "огляд Destructoid"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=7+billion+humans+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [item-pickup, impassable-cells, collect-all, all-on-targets, level-select, sequential-levels, level-unlock, game-screen, end-screen, +command-program, +swarm-same-program, +sensor-predicates, +worker-memory, +jump-labels, +runtime-error-stop, +goal-state-check, +random-test-cases, +solution-metrics, +step-execution, +code-editor-window, +shredder-sink, +printer-source]
proposes: ["+trigger:exec(cmd)", "+trigger:program_end", "+cond:nearby(dir, kind)", "+cond:held(a, kind|value)", "+effect:write_value(a, v)", "+effect:crash", "+role:resource", "+window:code-editor", "+ui:program-listing", "+ui:jump-arrows", "+ui:worker-follow", "+feature:solution-metrics", "+feature:random-test-cases", "+feature:skip-level", "+axis:actors"]
author: opus
date: 2026-11-02
---

# 7 Billion Humans — одна програма, десятки офісних працівників виконують її одночасно

## Суть
На клітинному офісному поверсі стоять працівники; гравець пише **одну** програму з асемблероподібних команд (крок, взяти, покласти, умова за сусідньою клітиною, перехід на мітку, обчислення), і всі працівники виконують її **паралельно**, кожен зі свого місця й зі своєю памʼяттю. Предмети на полі — кубики даних із числами; мета рівня — привести поле в потрібний стан (кубики в шредері, відсортовані, підсумовані). Головна складність — думати про рій: однаковий код дає різну поведінку через різне оточення, а працівники заважають одне одному.

## Поле і час
- Квадратна сітка офісу (ізометричний вигляд) зі стінами, діркою/ямою, шредерами, принтерами, кубиками; працівник займає клітину, на клітині може лежати один предмет.
- Сусідство — 8 напрямків + «тут» (c) (?): умови й дії можна адресувати по діагоналі.
- Час `programmed`: тік (cycle) = кожен працівник виконує одну інструкцію-дію одночасно з іншими; переходи/мітки — без витрати тіку (?).
- Видимість повна; варіативність — значення кубиків і їх розстановка, що змінюються між тестовими запусками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Працівник | player | позиція, предмет у руках (0/1), памʼять (комірки mem) | виконує спільну програму зі своїм лічильником інструкцій |
| Кубик даних | object | число або порожній | береться, кладеться, передається; `write` змінює число |
| Шредер | static | — | предмет, покладений/відданий у нього, знищується |
| Принтер | spawner | — | з нього можна взяти новий кубик (?) |
| Дірка / яма | static | — | непрохідна для працівника; кубик туди (?) |
| Стіна | static | — | непрохідна |
| Порожня клітина | terrain | — | прохідна |
| Ціль рівня | mark | опис стану | напр. «усі кубики в шредері», «кожен рядок посортовано» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(step dir)` → ЯКЩО `free(dir)` → ТО `move(worker, dir)`; зайнято іншим працівником/стіною/діркою → `block` (?).
- КОЛИ `exec(pickup dir)` → ЯКЩО `occupied(dir, item)` і руки порожні → ТО `pickup`.
- КОЛИ `exec(drop)` → ЯКЩО `free(here, item)` → ТО предмет кладеться під себе; ЯКЩО `occupied(here, shredder)` → ТО `disappear_b` (знищено).
- КОЛИ `exec(give dir)` → ТО передати предмет працівнику/шредеру в напрямку (?); `exec(takefrom dir)` → ТО взяти предмет у працівника/з принтера (?).
- КОЛИ `exec(write v)` → ЯКЩО `held(worker, datacube)` → ТО `write_value(cube, v)`.
- КОЛИ `exec(calc mem = a op b)` → ТО `counter(mem, = a op b)` (op: + − × ÷ %); `exec(set mem = x)` — присвоєння.
- КОЛИ `exec(nearest kind)` → ТО `custom: «записати в mem найближчий обʼєкт виду (кубик, працівник, шредер, …)»` — ключ до координації рою.
- КОЛИ `exec(if cond)` → ЯКЩО `nearby(dir, kind)` / `held(worker, kind|value)` / порівняння mem → ТО гілка then; інакше else.
- КОЛИ `exec(jump label)` → ТО перейти на мітку (без `while` — цикли лише переходами, як у асемблері).
- КОЛИ `exec(shout word)` → ТО `custom: «сигнал усім»`; `exec(listen word)` → ТО `custom: «чекати сигналу»`; `exec(tell worker word)` (?) — адресний сигнал.
- КОЛИ `exec(foreachdir)` (?) → ТО тіло циклу для кожного з напрямків.
- КОЛИ `exec(end)` або кінець програми → ТО працівник зупиняється.
- КОЛИ `custom: «некоректна дія (покласти без предмета, взяти з порожньої)»` → ТО `crash` з поясненням (?).
- КОЛИ `custom: «усі працівники завершили або досягнуто цілі»` → ЯКЩО `goal-state` → ТО ще **25 запусків** з випадковими кубиками; усі пройдені → `win`; хоч один провалився → `message(«не спрацювало на іншому наборі»)`.
- Рахунок: два необовʼязкові челенджі — **розмір** (кількість команд ≤ середнього) і **швидкість** (кількість тіків ≤ середнього); можуть суперечити одне одному і виконуватись у різних розвʼязках.

## Керування і ввід
- Drag & drop команд з палітри в програму; параметри команд (напрямок, тип предмета, комірка памʼяті, число) — клік по команді → вибір у спливаючому меню.
- Переходи `jump` редагуються перетягуванням мітки; праворуч від коду малюються стрілки.
- Copy/paste програми як тексту (обмін розвʼязками через буфер).
- Коментарі — малюнки мишею (як у Human Resource Machine) (?).
- Виконання: Play, Step (один тік), Fast-forward, Stop; клік по працівнику — **follow**: підсвічується саме його поточна інструкція й памʼять.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` (продовжити, налаштування) (?).
- `level-select` — вертикальний ліфт/будівля: кожен поверх — рівень, з позначками челенджів розміру й швидкості.
- `game-screen`: офіс зліва (ізометрично), справа `program-listing` з номерами рядків і `jump-arrows`; `command-palette` з дозволеними в рівні командами; `objective-text` (завдання від боса); кнопки Play/Step/FF/Stop, `speed-slider` (?).
- HUD челенджів: `par-moves` — цільовий розмір програми і цільова кількість тіків, поточні значення.
- `hints-window` — підказки; кнопка **skip** — пропустити рівень.
- `end-screen` — результат: пройдено/не пройдено, розмір, швидкість, порівняння з ціллю.
- `dialogue-window` — сюжетні «незрозумілі» катсцени між розділами.
- `settings-window`: звук, мова (13 мов), повноекранний режим.
- Переходи: ліфт → поверх → game-screen ↔ (Play) виконання → end-screen → ліфт; катсцена між групами поверхів.

## Фічі поза полем
- `solution-metrics` — дві незалежні метрики (size/speed), бейджі на рівні; `par-target` у двох вимірах.
- `random-test-cases` — 25 перевірок з іншими даними: захист від «підгону» під конкретне поле.
- `hint`, `skip-level`, `tutorial` (кожна команда вводиться окремим рівнем), необовʼязкові складні рівні.
- `export-import` через буфер обміну (текстовий формат програми).
- `step-mode`, `speed-control`, follow-камера окремого працівника.
- `cloud-save`, `achievements` (Steam).

## Варіації й родичі
- Human Resource Machine (2015) — попередник: **один** працівник, вхідна/вихідна черга, памʼять підлоги.
- Родичі: TIS-100 і Shenzhen I/O (паралельні вузли з власними програмами), Opus Magnum (метрики cost/cycles/area), SpaceChem, Robozzle, Lightbot.
- Осі варіацій: **скільки акторів і чи спільна програма** (один / багато з однією програмою / багато з окремими); **комунікація** (нема / shout-listen / спільна памʼять); **метрики** (лише пройти / розмір / швидкість / площа); **перевірка** (одне поле / N випадкових).

## Цікавинки для курсу
- Рій з однією програмою: N акторів, кожен зі своїм PC і памʼяттю, крок у спільному тіку — 🥇 (паралельне виконання + конфлікти за клітини).
- Асемблерна мова з `jump`-мітками і стрілками в UI — 🥈.
- `nearest` — пошук найближчого обʼєкта виду (BFS/манхеттен) як вбудована команда — 🥉.
- Перевірка розвʼязку на 25 випадкових наборах — 📎.
- Метрики size/speed з окремими бейджами — 📎.
- Шредер-«злив» і принтер-«джерело» — 🌱.
- `shout/listen` як примітив синхронізації — 🥉.

## Мапа на каталог
- Є: `item-pickup` (pickup) · `impassable-cells` (стіни, дірки) · `collect-all` / `all-on-targets` (типові цілі рівнів) · `level-select` · `sequential-levels` · `level-unlock` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+swarm-same-program` «Багато акторів виконують одну програму» · entities/move · 🥇 · слоти {actors: N, sync: tick}.
  - `+command-program` · entities/move · 🥉 (спільна з Karel/Lightbot).
  - `+sensor-predicates` · entities/state · 📎 — тут 8 напрямків + «тут».
  - `+worker-memory` «Комірки памʼяті актора» · entities/state · 📎.
  - `+jump-labels` «Мітки й переходи замість циклів» · game-logic · 🥉.
  - `+runtime-error-stop` · game-logic/lose · 📎; `+goal-state-check` · game-logic/win · 📎.
  - `+random-test-cases` «Перевірка розвʼязку на N випадкових варіантах» · levels/solvability · 🥉.
  - `+solution-metrics` «Розмір і швидкість розвʼязку з цілями» · game-logic/score · 📎.
  - `+step-execution` · interface/input · 🥉; `+code-editor-window` · interface/menus · 🥉.
  - `+shredder-sink` «Клітина-злив знищує предмет» · entities/interact · 🌱; `+printer-source` «Клітина-джерело предметів» · entities/spawn · 🌱.

## Пропозиції до словників
- `+trigger:exec(cmd)`, `+trigger:program_end` — спільні для сімʼї.
- `+cond:nearby(dir, kind)` — що лежить/стоїть у сусідній клітині напрямку dir (точніше за `cell(x, type)`).
- `+cond:held(a, kind|value)` — що в руках актора і з яким значенням.
- `+effect:write_value(a, v)` — записати число в предмет (відрізняється від `set_value` плитки тим, що робить актор); `+effect:crash`.
- `+role:resource` — кубик даних як одиниця «вантажу» (або нова `+role:cargo`).
- `+window:code-editor`; `+ui:program-listing` (нумеровані рядки), `+ui:jump-arrows`, `+ui:worker-follow` (стеження за одним актором рою).
- `+feature:solution-metrics`, `+feature:random-test-cases`, `+feature:skip-level`.
- `+axis:actors` — `swarm`: еталонний приклад.

## Джерела
- ⭐ [Wikipedia: 7 Billion Humans](https://en.wikipedia.org/wiki/7_Billion_Humans) — паралельне виконання однієї програми, step/cycle-челенджі, 25 випадкових перевірок, текстовий copy/paste.
- [Tomorrow Corporation](https://tomorrowcorporation.com/7billionhumans) — опис, магазини.
- [Steam](https://store.steampowered.com/app/792100/7_Billion_Humans/) — фічі: 60+ рівнів, hint/skip, 13 мов.
- [Destructoid review](https://www.destructoid.com/reviews/review-7-billion-humans/) — огляд.
- YouTube: пошук «7 billion humans gameplay».

## Непевне
- (?) Пошук вичерпаний, фан-вікі недоступна (402): точні імена й семантика команд (`give`, `takefrom`, `tell`, `foreachdir`, `listen`), кількість комірок памʼяті, 8-сусідство — з памʼяті.
- (?) Що стається при кроці в зайняту клітину (чекає / пропускає) і чи існують помилки виконання (`crash`) — не перевірено.
- (?) Поведінка дірок (непрохідні чи «поглинають» кубики) і принтера — з памʼяті.
- (?) Чи `jump` витрачає тік; вигляд меню (ліфт як `level-select`) і коментарі-малюнки — з памʼяті про HRM/7BH.
