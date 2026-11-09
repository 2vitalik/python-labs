---
title: Human Resource Machine
slug: human-resource-machine
aka: [HRM]
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: 1d
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2015
platforms: [PC, Mac, Linux, Wii U, iOS, Android, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/375820/Human_Resource_Machine/", best: true, note: "Steam: опис, трейлер, скріншоти; 19 мов, досягнення, Cloud"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Human_Resource_Machine", note: "геймплей: inbox/outbox, підлога-памʼять, непряма адресація, тести на випадкових входах, size/speed"}
  - {kind: official, url: "https://tomorrowcorporation.com/humanresourcemachine", note: "студія: 11 команд, старт з 2, Optimization Challenges"}
  - {kind: other, url: "https://github.com/atesgoral/hrm-solutions", note: "спільнота: розвʼязки-асемблер, формат size.speed, тести hrm-cpu"}
  - {kind: other, url: "https://atesgoral.github.io/hrm-solutions/", note: "таблиця рівнів з par розміру й швидкості"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=human+resource+machine+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [command-program, sensor-predicates, step-execution, code-editor-window, drag-drop-piece, sequential-levels, level-unlock, level-select, tutorial-window, save-progress, game-screen, end-screen, +jump-labels, +inbox-outbox-queues, +floor-memory-cells, +accumulator-hand, +indirect-addressing, +random-test-cases, +solution-metrics, +runtime-error-stop, +hand-drawn-labels, +program-text-clipboard]
proposes: ["+effect:store(cell)", "+effect:load(cell)", "+effect:jump_to(label)", "+cond:held(a, kind|value)", "+feature:random-test-cases", "+feature:solution-metrics", "+feature:program-clipboard", "+ui:hand-drawn-label", "+ui:inbox-outbox-belts", "+window:boss-briefing"]
author: opus
date: 2026-11-09
---

# Human Resource Machine — офісний працівник як процесор: асемблером перенось коробки з inbox в outbox через підлогу-памʼять

## Суть
Кожен рівень — «рік» роботи в офісі: начальник дає завдання (напр. «помнож кожне число на 3», «відкинь нулі», «посортуй рядок») і приклад. Гравець перетягує команди в програму, а працівник її виконує: бере коробку з **inbox** (конвеєр-вхід), кладе в **outbox** (вихід), копіює на нумеровані плитки підлоги (памʼять), додає/віднімає, стрибає за мітками. Руки працівника — **акумулятор** (одна коробка з числом або літерою). Гра — це асемблер з 11 команд у вигляді офісних дій; розвʼязок перевіряється на випадкових входах, а дві необовʼязкові цілі — **розмір** (кількість команд) і **швидкість** (кількість кроків) — часто суперечать одна одній.

## Поле і час
- Кімната вигляду згори: ліворуч конвеєр inbox, праворуч outbox, посередині **нумеровані плитки підлоги** (адреси 0, 1, 2 …), на кожній ≤ 1 коробка. Для програми памʼять — лінійний масив адрес (тому `1d`), фізичне розташування плиток — сітка.
- Коробка: ціле число або одна літера.
- Час `programmed`: крок = одна команда; працівник анімовано ходить між inbox/плиткою/outbox; є регулятор швидкості й покрокове виконання.
- Видимість повна; вхідний набір у тестах — випадковий (перевірка не лише на прикладі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Працівник | player | руки: 0 або 1 коробка (акумулятор) | виконує програму команда за командою |
| Коробка | object | число або літера | з inbox у руки, на плитку, в outbox |
| Inbox | source | черга коробок | `INBOX` бере наступну; порожній — програма завершується |
| Outbox | sink | очікувана послідовність | `OUTBOX` кладе з рук; хибне значення — стоп з помилкою |
| Плитка підлоги | container | адреса, ≤ 1 коробка; можуть бути початкові значення (напр. 0) | памʼять для `COPYTO` / `COPYFROM` / `ADD` … |
| Начальник | — (наратор) | — | дає завдання, приклад, підказки |
| Мітка (jump label) | mark | — | ціль стрибка, стрілка в лістингу |
| Нотатка-малюнок | mark | — | підпис мишею на команді або плитці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(INBOX)` → ЯКЩО `custom: «inbox не порожній»` → ТО `pickup` (наступна коробка → руки; попередня в руках зникає (?)).
- КОЛИ `exec(INBOX)` → ЯКЩО `custom: «inbox порожній»` → ТО `custom: «програма завершується»` → перевірка outbox.
- КОЛИ `exec(OUTBOX)` → ЯКЩО `has(worker, box)` → ТО `custom: «коробка з рук → outbox»`, руки порожні.
- КОЛИ `exec(OUTBOX)` → ЯКЩО `custom: «значення не збігається з очікуваним наступним»` → ТО `crash`, `message(«неправильний вихід»)` — програма зупиняється одразу.
- КОЛИ `exec(COPYTO n)` → ЯКЩО `has(worker, box)` → ТО `custom: «копія значення з рук на плитку n»`.
- КОЛИ `exec(COPYFROM n)` → ЯКЩО `occupied(tile_n, box)` → ТО `custom: «копія значення з плитки n у руки»`.
- КОЛИ `exec(ADD n)` / `exec(SUB n)` → ЯКЩО `has(worker, box)` and `occupied(tile_n, box)` → ТО `set_value(hand, hand ± tile_n)`.
- КОЛИ `exec(BUMP+ n)` / `exec(BUMP− n)` → ЯКЩО `occupied(tile_n, box)` → ТО `set_value(tile_n, ±1)` і копія результату в руки.
- КОЛИ `exec(JUMP label)` → ТО `custom: «перейти на мітку»` — єдиний спосіб циклу.
- КОЛИ `exec(JUMP IF ZERO label)` → ЯКЩО `custom: «у руках 0»` → ТО `custom: «перейти на мітку»`; інакше наступна команда.
- КОЛИ `exec(JUMP IF NEGATIVE label)` → ЯКЩО `custom: «у руках < 0»` → ТО `custom: «перейти на мітку»`.
- КОЛИ `exec(cmd [n])` → ТО `custom: «непряма адресація: адреса = значення на плитці n»` (пізні рівні).
- КОЛИ `exec(cmd)` → ЯКЩО `not has(worker, box)` and `custom: «команда потребує значення в руках»` → ТО `crash`, `message(помилка)` (?).
- КОЛИ `exec(COPYFROM n)` → ЯКЩО `not occupied(tile_n, box)` → ТО `crash` (?).
- КОЛИ `program_end` → ЯКЩО `custom: «outbox = очікуваній послідовності»` → ТО `custom: «прогін на інших випадкових входах»`; провал на будь-якому → `message(«не працює для іншого входу»)` з показом.
- КОЛИ `custom: «усі тестові прогони пройдено»` → ТО `win`, `window(end-screen)`, `next_level` («підвищення»).
- КОЛИ `win` → ТО `custom: «показати розмір (команд) і середню швидкість (кроків) проти цілей начальника»`.
- Перемога: правильний outbox на всіх тестах · Поразка: нема, лише зупинка з помилкою й правка · Рахунок: два бейджі — size і speed; деякі не досяжні одним розвʼязком (у спільноті: Busy Mail Room).

## Керування і ввід
- Drag & drop команд з палітри в програму; параметр (номер плитки) — клік по плитці або вибір.
- Перетягування стрілки `JUMP` до мітки; мітки й стрілки малюються поряд з лістингом.
- Нотатки: малювання мишею/пальцем підписів до команд і плиток.
- Копіювання/вставка програми текстом (асемблероподібний формат — так спільнота обмінюється розвʼязками).
- Виконання: Play, Step (крок), Step back (?), регулятор швидкості, Stop.

## Вікна, меню, HUD
- `level-select` — офісна будівля/ліфт: рівні як роки/поверхи з позначками size/speed (?).
- `boss-briefing` — начальник на початку рівня: завдання і приклад входу/виходу.
- `game-screen`: кімната (inbox ліворуч, плитки, outbox праворуч), `program-listing` з номерами й мітками, `command-palette` з дозволеними командами, `instruction-highlight`, кнопки Play/Step/швидкість, `par-moves` — цілі розміру й швидкості.
- `end-screen` — пройдено, розмір і швидкість проти цілей, бейджі.
- `dialogue-window` — сюжетні катсцени між роками (роботи захоплюють місто).
- `settings-window`: звук, мова (19 мов), повний екран (?).
- Переходи: будівля → рік → брифінг → game-screen ↔ запуск → end-screen → будівля; катсцени після деяких років.

## Фічі поза полем
- `levels-sequential`, `level-unlock` — «підвищення» щороку; починаєш з 2 команд, далі відкриваються інші (усього 11).
- `solution-metrics` — дві незалежні цілі (size, speed), можна повертатись до пройдених рівнів оптимізувати.
- `random-test-cases` — перевірка на рандомізованих входах.
- `hint` — підказки начальника на деяких рівнях; `tutorial` — кожна команда вводиться окремим рівнем.
- `program-clipboard` (export-import текстом), `achievements`, `cloud-save` (Steam), `localization` (19 мов).
- Рівні-катсцени без програмування (у таблиці спільноти без par: Coffee Time, Employee Morale Insertion та ін. (?)).

## Варіації й родичі
- Наступник у корпусі: [7 Billion Humans](7-billion-humans.md) (2018) — багато працівників з однією програмою на 2D-поверсі, сенсори сусідніх клітин, shout/listen.
- Родичі: [SpaceChem](spacechem.md) і [Opus Magnum](opus-magnum.md) (метрики розвʼязку), [Manufactoria](manufactoria.md) (стрічка-вхід і перевірка на тестах), [Befunge](befunge.md) (код як просторова сітка), [Cargo-Bot](cargo-bot.md) (один маніпулятор з одним слотом); поза корпусом — TIS-100, Shenzhen I/O, Little Man Computer (?).
- **Осі варіацій**: регістри (лише руки / руки + памʼять / непряма адресація) · потік керування (лише jump / цикли / процедури) · вхід (черга / поле) · оцінка (пройти / size / speed) · перевірка (приклад / N випадкових).

## Цікавинки для курсу
- Інтерпретатор 11 команд з акумулятором і памʼяттю-плитками — 🥉.
- `JUMP`-мітки й стрілки в лістингу — 📎.
- Непряма адресація `[n]` — 📎.
- Перевірка на випадкових входах з показом контрприкладу — 🥉.
- Метрики size/speed і цілі начальника — 📎.
- Анімація працівника, що ходить між inbox, плитками й outbox, синхронно з кроками — 🥈.
- Текстовий формат програми для copy/paste + парсер — 📎.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ програма працівника; `sensor-predicates` ↔ `JUMP IF ZERO/NEGATIVE`; `step-execution` ↔ Step + підсвітка; `code-editor-window`; `drag-drop-piece` ↔ перетягування команд; `sequential-levels`, `level-unlock`, `level-select`; `tutorial-window`; `save-progress`; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+jump-labels` «Мітки й переходи замість циклів» · game-logic/program · 🥉 (вже з 7 Billion Humans).
  - `+inbox-outbox-queues` «Вхідна й вихідна черги з очікуваним виходом» · game-logic/program · 📎.
  - `+floor-memory-cells` «Нумеровані комірки памʼяті на полі» · entities/state · 📎.
  - `+accumulator-hand` «Руки актора як єдиний регістр» · entities/state · 🌱.
  - `+indirect-addressing` «Адреса з іншої комірки» · game-logic/program · 📎.
  - `+random-test-cases` · levels/solvability · 🥉 (з 7 Billion Humans).
  - `+solution-metrics` · game-logic/score · 📎 (з 7 Billion Humans).
  - `+runtime-error-stop` «Зупинка програми з поясненням помилки» · game-logic/lose · 📎.
  - `+hand-drawn-labels` «Малюнки-підписи до коду й памʼяті» · interface/input · 🥉.
  - `+program-text-clipboard` «Програма текстом у буфер обміну» · levels/format · 📎.

## Пропозиції до словників
- `+effect:store(cell)` / `+effect:load(cell)` — запис/читання значення в комірку памʼяті актором (COPYTO/COPYFROM).
- `+effect:jump_to(label)` — перехід лічильника команд на мітку (спільне для асемблерних ігор).
- `+cond:held(a, kind|value)` — що в руках і з яким значенням (=0, <0) — уже пропонували 7 Billion Humans і Cargo-Bot.
- `+feature:random-test-cases`, `+feature:solution-metrics`, `+feature:program-clipboard`.
- `+ui:hand-drawn-label` — підпис від руки на команді/плитці; `+ui:inbox-outbox-belts` — конвеєри входу/виходу з видимою чергою.
- `+window:boss-briefing` — брифінг завдання з прикладом входу/виходу.

## Джерела
- ⭐ [Steam: Human Resource Machine](https://store.steampowered.com/app/375820/Human_Resource_Machine/) — 15.10.2015, Tomorrow Corporation, Windows/macOS/Linux, 19 мов, досягнення, Steam Cloud.
- [Wikipedia: Human Resource Machine](https://en.wikipedia.org/wiki/Human_Resource_Machine) — inbox/outbox, плитки як памʼять, руки як регістр, add/sub, jump if zero/negative, непряма адресація, нотатки, тести на випадкових входах, зупинка на хибному виході, step і швидкість, size/speed, ~40 «років», дати платформ.
- [Tomorrow Corporation](https://tomorrowcorporation.com/humanresourcemachine) — 11 команд, старт з 2, Optimization Challenges, коробки з літерами й числами.
- [hrm-solutions (GitHub)](https://github.com/atesgoral/hrm-solutions) і [таблиця рівнів](https://atesgoral.github.io/hrm-solutions/) — 42 позиції з par size/speed, size без коментарів і міток, speed у кроках, імпорт розвʼязків через copy/paste.

## Непевне
- (?) Точні назви команд (`BUMP+`, `BUMP−`, `JUMP IF ZERO`, `JUMP IF NEGATIVE`) — з памʼяті; Wikipedia описує їх функції без назв.
- (?) Які дії дають помилку виконання (порожні руки, порожня плитка, переповнення ±999, арифметика з літерами).
- (?) Чи `INBOX` при повних руках просто замінює коробку.
- (?) Вигляд вибору рівнів (будівля/ліфт), Step back, налаштування.
- (?) Які 6 із 42 позицій таблиці спільноти — катсцени без програмування (у таблиці без par).
