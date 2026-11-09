---
title: Befunge (Befunge-93)
slug: befunge
aka: [Befunge-93, Funge-98, Funge]
family: program-robots
also: [thinky]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: none
year: 1993
platforms: [PC, web]
links:
  - {kind: other, url: "https://esolangs.org/wiki/Befunge", best: true, note: "esolangs: повний список інструкцій, приклади (Hello World, quine, FizzBuzz, решето), компілятори"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Befunge", note: "історія, тор 80×25, Funge-98, bef2c і Betty"}
  - {kind: other, url: "https://github.com/catseye/Befunge-93/blob/master/doc/Befunge-93.markdown", note: "оригінальна специфікація Chris Pressey: тор, порожній стек дає 0"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=befunge+interpreter+visualization", note: "пошук; візуальні інтерпретатори"}
stage: v1
coverage: 60
mechanics: [wrap-edges, command-program, step-execution, code-editor-window, console-render, level-from-txt, state-as-data, +instruction-grid-2d, +instruction-pointer-direction, +stack-machine, +self-modifying-playfield, +string-mode, +random-direction-cell, +branch-on-pop, +bridge-skip-cell, +stack-view]
proposes: ["+effect:stack_push(v)", "+effect:stack_pop(n)", "+cond:stack_top(op, v)", "+effect:write_cell(x, y, v)", "+effect:read_cell(x, y)", "+effect:skip_cell", "+effect:output(v)", "+trigger:input_wait", "+role:pointer", "+ui:stack-view", "+ui:pointer-trail", "+window:output-console", "+feature:self-modifying-code", "+card:instruction-grid-2d"]
author: opus
date: 2026-11-09
---

# Befunge — програма, що лежить на сітці: вказівник їде клітинами, а стрілки його повертають

## Суть
Befunge — езотерична мова Chris Pressey (1993), де програма — не рядки, а **2D-поле символів**. Вказівник інструкцій (IP) стартує в лівому верхньому куті й їде вправо; кожна клітина під ним — команда: стрілки міняють напрямок, `_` і `|` розгалужують за значенням зі стека, `p` переписує клітини поля просто під час роботи. Для корпусу це «гра-робот навпаки»: сутність, що їде сіткою, — не робот, а сам потік керування, а «рівень» — це текст програми. Мову задумано як найважчу для компіляції — через самозміну коду й 2D-потік.

## Поле і час
- Befunge-93: поле **80×25** символів ASCII, **тор** — вихід за край переносить IP на протилежний бік (специфікація: «an 80x25 torus»).
- Funge-98: поле без обмежень розміру, довільна кількість вимірів (Unefunge 1D, Trefunge 3D (?)), кілька IP — паралельні потоки.
- Шари стану: поле (код = дані), стек цілих (signed long), напрямок IP, прапорець string mode.
- Час `programmed`: один тік = IP виконує клітину під собою й робить крок у поточному напрямку. Візуальні інтерпретатори показують IP курсором на полі й стек поруч.
- Камера: усе поле видно цілком (80×25 вміщується в термінал).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вказівник інструкцій (IP) | player | (x, y), напрямок, string mode | виконує клітину під собою, крок у напрямку; на краю — `wrap` |
| Стек | supply | цілі числа | push/pop; pop з порожнього дає 0 (без underflow) |
| Клітина-стрілка `> < ^ v` | terrain | напрямок | ставить напрямок IP |
| Клітина `?` | terrain | — | випадковий з 4 напрямків |
| Клітина `_` | switch | — | pop: 0 → вправо, інакше вліво |
| Клітина `\|` | switch | — | pop: 0 → вниз, інакше вгору |
| Клітина `#` (місток) | terrain | — | пропустити наступну клітину |
| Клітина `"` | switch | — | перемкнути string mode: далі кожен символ пушиться як ASCII-код до наступної `"` |
| Цифра `0`–`9` | source | значення | push цифри |
| Арифметика `+ - * / %` | conduit | — | pop a, pop b → push b∘a (ділення цілочисельне) |
| Логіка `!` і `` ` `` | conduit | — | `!` — NOT (0 → 1, інакше 0); `` ` `` — push 1, якщо b > a |
| Стекові `: \ $` | conduit | — | дублювати вершину · обміняти дві верхні · викинути |
| Вивід `. ,` | sink | — | pop і вивести як число / як символ |
| Ввід `& ~` | source | — | прочитати число / символ і push |
| `g` (get) | conduit | — | pop y, x → push код символу клітини (x, y); поза полем — 0 |
| `p` (put) | conduit | — | pop y, x, v → записати символ v у клітину (x, y) — самозміна коду |
| `@` | static | — | кінець програми |
| Пробіл | terrain | — | нічого (no-op), IP їде далі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `not state(ip, string_mode)` → ТО `exec(cell_under_ip)` → `move(ip, facing)`.
- КОЛИ `exec(arrow)` → ТО `face(ip, arrow_dir)`.
- КОЛИ `exec(?)` → ТО `face(ip, custom: «випадковий з N/E/S/W»)`.
- КОЛИ `exec(_)` → ЯКЩО `custom: «pop == 0»` → ТО `face(ip, east)`; інакше `face(ip, west)`.
- КОЛИ `exec(|)` → ЯКЩО `custom: «pop == 0»` → ТО `face(ip, south)`; інакше `face(ip, north)`.
- КОЛИ `exec(#)` → ТО `custom: «IP перестрибує наступну клітину в напрямку руху»`.
- КОЛИ `exec(")` → ТО `set_state(ip, string_mode)` / `clear_state(ip, string_mode)` (перемикач).
- КОЛИ `tick` → ЯКЩО `state(ip, string_mode)` і `not cell(here, quote)` → ТО `custom: «push ASCII-коду клітини»`.
- КОЛИ `exec(digit)` → ТО `custom: «push(digit)»`.
- КОЛИ `exec(op)` → ТО `custom: «pop a, pop b, push b op a»` (`-` дає b−a, `/` і `%` — ліве b).
- КОЛИ `exec(:)` → ТО `custom: «дублювати вершину»`; `exec(\)` → `custom: «обміняти дві верхні»`; `exec($)` → `custom: «викинути вершину»`.
- КОЛИ `custom: «pop з порожнього стека»` → ТО `custom: «повертає 0, помилки нема»`.
- КОЛИ `exec(.)` / `exec(,)` → ТО `message(custom: «вивести число / символ»)`.
- КОЛИ `exec(&)` / `exec(~)` → ТО `custom: «чекати ввід користувача, push»`.
- КОЛИ `exec(g)` → ЯКЩО `custom: «(x, y) у межах поля»` → ТО `custom: «push коду символу клітини»`; інакше `custom: «push 0»`.
- КОЛИ `exec(p)` → ТО `set_cell(cell(x, y), custom: «символ з кодом v»)` — нова інструкція діє, коли IP до неї доїде.
- КОЛИ `edge(ip)` → ТО `wrap(ip)`.
- КОЛИ `exec(@)` → ТО `custom: «зупинити програму»` (далі спрацьовує `program_end`).
- Перемоги/поразки нема: результат — вивід програми. У «гральній» постановці (code golf) рахунок — розмір прямокутника коду або кількість символів (?).

## Керування і ввід
- Програміст редагує поле як текстову сітку (будь-який редактор, режим «overwrite» зручніший за вставку — щоб не зсувати стовпці).
- Запуск у інтерпретаторі; візуальні інтерпретатори дають крок / біг / швидкість, підсвітку IP, вивід стека (?).
- Під час виконання — лише ввід `&`/`~`; керування потоком — тільки геометрією поля.
- Прийом розкладки: цикл — це замкнений «маршрут» стрілками; коментар — текст, який IP обʼїжджає (окремого синтаксису коментарів нема).

## Вікна, меню, HUD
(цифрова версія — типовий візуальний інтерпретатор (?))
- `code-editor`: сітка 80×25 моноширинним шрифтом, курсор редагування.
- `game-screen` під час виконання: те саме поле з IP-курсором (`instruction-highlight`), напрямок IP, `stack-view` (вміст стека), вивід.
- `output-console` — stdout програми й поле вводу для `&`/`~`.
- HUD: `step-button`, `speed-slider`, `restart-button`, `turn-counter` (кількість тіків).
- Переходи: редагування → Run/Step → (`@`) зупинка з виводом → назад у редагування.

## Фічі поза полем
- `step-mode`, `speed-control` — у візуальних інтерпретаторах.
- Компілятори: bef2c (кожна інструкція → шматок C; не підтримує `p` і string mode), Betty (прямі ділянки як підпрограми, перекомпіляція при `p`), Befunjit/Bejit (статичні шляхи) — уся складність саме в самозміні.
- `export-import`: програма — звичайний текстовий файл (`level-from-txt`).
- Спільнота: code golf, quine-змагання, «бібліотека» класичних програм (Hello World, cat, truth machine, factorial, Fibonacci, FizzBuzz, решето Ератосфена, хрестики-нулики).

## Варіації й родичі
- Befunge-93 → Befunge-96 → Funge-97 → **Funge-98**: необмежене поле, далекі стрибки, кілька IP, «fingerprints»-розширення (?), `;` як обмежувач коментаря (?).
- Родина «fungeoids»: 1D/3D варіанти; інші 2D-мови — ><> (Fish), Orthagonal, PATH, Piet (кольорові пікселі як інструкції) (?).
- Родичі в корпусі: [Kara](kara.md) (2D-поле + автомат, але робот окремо від програми), [Manufactoria](manufactoria.md) (програма — розкладка конвеєрів на полі, «вказівник» — робот на стрічці), [Opus Magnum](opus-magnum.md) і [SpaceChem](spacechem.md) (інструкції лежать на треках/полі), [RoboZZle](robozzle.md).
- **Осі варіацій**: де лежить програма (окремо від світу / на полі світу) · розмір поля (фіксований тор / нескінченне) · кількість вказівників (1 / багато потоків) · памʼять (стек / стрічка / саме поле) · самозміна (заборонена / `p`).

## Цікавинки для курсу
- Інтерпретатор Befunge-93 на сітці: IP, напрямок, тор, стек, string mode — 🥉 (повний набір з ~30 інструкцій за вечір-день).
- Візуальний покроковий дебагер: поле з курсором IP, стек, вивід, швидкість — 🥈 (UI + стан виконання).
- `p`/`g` — самозмінний код, поле як памʼять — 📎 при готовому інтерпретаторі, але пастка для компіляції.
- Детектор нескінченного циклу (повтор стану IP + стек + поле) — 🥇 (стан може рости; евристики).
- Компілятор/JIT прямих ділянок з інвалідацією при `p` (як Betty) — 👑.
- «Пазл-режим»: дано вхід → очікуваний вивід, обмеження розміру поля (як Zachtronics-рівні) — 🥈.

## Мапа на каталог
- Є в каталозі: `wrap-edges` ↔ тор 80×25; `command-program` ↔ програма як набір команд; `step-execution` ↔ покроковий інтерпретатор; `code-editor-window` ↔ редактор сітки; `console-render` ↔ поле символами; `level-from-txt` ↔ програма — txt-файл; `state-as-data` ↔ поле+стек+IP як стан.
- **Нема** → пропозиції карток:
  - `+instruction-grid-2d` «Програма як 2D-сітка інструкцій» · game-logic/program · 🥉.
  - `+instruction-pointer-direction` «Вказівник з напрямком, стрілки його повертають» · game-logic/program · 📎.
  - `+stack-machine` «Стекова машина: push/pop, арифметика над вершиною» · game-logic/program · 📎.
  - `+self-modifying-playfield` «Програма переписує клітини поля» · game-logic/program · 🥉.
  - `+string-mode` «Режим, у якому клітини читаються як дані» · game-logic/program · 🌱.
  - `+random-direction-cell` «Клітина випадкового напрямку» · entities/move · 🌱.
  - `+branch-on-pop` «Розгалуження за значенням зі стека» · game-logic/program · 🌱.
  - `+bridge-skip-cell` «Перестрибнути наступну клітину» · entities/move · 🌱.
  - `+stack-view` «Панель вмісту стека» · interface/hud · 📎.

## Пропозиції до словників
- `+effect:stack_push(v)` / `+effect:stack_pop(n)` — операції зі стеком (Befunge, Cargo-Bot-стек викликів, стекові мови).
- `+cond:stack_top(op, v)` — порівняння вершини стека (розгалуження `_`/`|`).
- `+effect:write_cell(x, y, v)` / `+effect:read_cell(x, y)` — запис/читання клітини за координатами (самозмінний код; `set_cell` не передає «за координатами з даних»).
- `+effect:skip_cell` — перестрибнути наступну клітину (`#`).
- `+effect:output(v)` — вивести значення назовні (stdout, конвеєр виходу).
- `+trigger:input_wait` — виконання чекає на ввід користувача.
- `+role:pointer` — абстрактна сутність потоку керування (IP), не робот.
- `+ui:stack-view` · `+ui:pointer-trail` (слід пройдених клітин).
- `+window:output-console` — вікно виводу програми (уже пропонували The Farmer Was Replaced і Screeps).
- `+feature:self-modifying-code`.
- `+card:instruction-grid-2d`.

## Джерела
- ⭐ [Esolangs: Befunge](https://esolangs.org/wiki/Befunge) — усі інструкції Befunge-93, приклади, компілятори, розділ про Funge-98.
- [Wikipedia: Befunge](https://en.wikipedia.org/wiki/Befunge) — автор, мета «важко компілювати», тор, bef2c і Betty.
- [Специфікація Befunge-93](https://github.com/catseye/Befunge-93/blob/master/doc/Befunge-93.markdown) — тор 80×25, pop з порожнього стека дає 0, комірка стека = signed long.
- YouTube: пошук «befunge interpreter visualization».

## Непевне
- (?) Ділення на нуль: специфікація просить спитати користувача, JS-інтерпретатор на esolangs повертає 0 — реалізації розходяться; поведінка `&`/`~` на EOF не задана.
- (?) Деталі Funge-98 (`j`, `k`, `;`, fingerprints, дельта IP) — сторінки Funge-98 не відкривав.
- (?) Unefunge/Trefunge та інші fungeoids (><>, Piet) — з памʼяті.
- (?) Набір контролів «типового» візуального інтерпретатора — узагальнення, не конкретний продукт.
- (?) Метрики code golf (площа прямокутника vs кількість символів) — залежать від змагання.
