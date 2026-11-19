---
title: Ichimaga (イチマガ)
slug: ichimaga
aka: [イチマガ, Ічімага]
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?ichimaga", best: true, note: "puzz.link: правила EN/JA з прикладом і вхід у плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/ichimaga.js", note: "4 правила EN і JA текстом, «Nikoli vol. 35», 9 тестових станів з кодами помилок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Ichimaga/index.htm", note: "Janko: 5 правил DE/EN/JA, приклад з кружками у вузлах решітки, 5 пазлів"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/ichimaga.js", note: "код pzprjs: базові правила й варіанти Magnetic / Crossing Ichimaga"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ichimaga+puzzle", note: "пошук"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, completion-detection, markup-validity, path-drawing, edge-marking, connectivity-check, conflict-highlight, undo-redo, in-game-editor, import-open-formats, keyboard-controls, +bend-limited-path, +valence-bonds, +crossing-detection, +wildcard-clue, +link-pair-ban, +trial-mode]
proposes: ["+cond:path_turns", "+cond:degree", "+cond:crosses", "+card:bend-limited-path", "+card:link-pair-ban", "+ui:loop-color-coding"]
author: opus
date: 2026-11-19
---

# Ichimaga — зʼєднай кружки лініями з щонайбільше одним поворотом; число — скільки ліній виходить, усе — одна мережа

## Суть
На сітці стоять кружки з числами. Гравець проводить лінії по пунктирах від кружка до кружка: лінія пряма або з одним поворотом на 90°, лінії не розгалужуються й не перетинаються. Число в кружку — скільки ліній з нього виходить; усі кружки мають злитися в одну мережу. Незвичне: обмежено не довжину, а **кількість поворотів** кожного зʼєднання — граф «як у Hashi», але з L-подібними ребрами. Жанр Nikoli (vol. 35).

## Поле і час
- Квадратна сітка. puzz.link — кружки в клітинках, лінії через центри по пунктирах; Janko — кружки у вузлах решітки, лінії по її лініях (те саме, дуально). Приклад Janko — 10×10 вузлів, числа 1–4.
- Зʼєднання — шлях від кружка до кружка через порожні клітинки: 0 або 1 поворот; на кружку лінія закінчується.
- Через клітинку (вузол) проходить щонайбільше одна лінія; число ≤ 4 — по лінії в кожен бік (у редакторі puzz.link `maxnum: 4`).
- Шари: кружки (з числом / без) · лінії · хрестики «лінії нема» на межах (puzz.link `peke`).
- Час статичний; хід = провести або стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кружок з числом | static | N = 1…4 | з нього виходить рівно N ліній |
| Кружок без числа | static | — | будь-яка кількість ліній, але ≥ 1 (Janko) |
| Лінія (зʼєднання) | mark | 0 або 1 поворот | кінці — два кружки; не розгалужується, не перетинає інші |
| Хрестик | mark | на межі клітинок | «тут лінії нема», допоміжний |
| Мережа | zone | — | у розвʼязку одна звʼязна компонента |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `mark(cells, line)`; протяжка по наявній лінії → `unmark(cells)` (puzz.link) (?).
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)` (puzz.link) (?).
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «у порожній клітинці 3+ відрізки лінії»` (`+cond:degree`) → ТО `set_state(line, error)` («There is a branch line»).
- КОЛИ `constraint_broken(cross)` → ЯКЩО `custom: «дві лінії перетинаються»` (`+cond:crosses`) → ТО `set_state(line, error)`; у Crossing Ichimaga перевірки нема, але кружок перехрестям бути не може.
- КОЛИ `constraint_broken(curves)` → ЯКЩО `custom: «між двома кружками ≥ 2 повороти»` (`+cond:path_turns`) → ТО `set_state(line, error)` («The number of curves is twice or more»).
- КОЛИ `constraint_broken(divided)` → ЯКЩО `not connected(circle)` → ТО `set_state(network, error)` («All lines and numbers are not connected to each other»).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «лінія обривається в порожній клітинці»` → ТО `set_state(line, error)`.
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «ліній з кружка ≠ N»` (`+cond:degree`) → ТО `set_state(circle, error)` («The number is not equal to the number of lines out of the circle»).
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `custom: «з кружка не виходить жодна лінія»` → ТО `set_state(circle, error)` («A circle doesn't start any line»).
- Magnetic Ichimaga: КОЛИ `custom: «лінія зʼєднує два кружки»` → ЯКЩО `same(a, b, number)` → ТО `set_state(line, error)` («Same numbers are connected each other»); кружки без числа — виняток.
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: кожен кружок має свою кількість ліній, кожна лінія — пряма або з одним поворотом, перетинів і розгалужень нема, мережа одна. Поразки й рахунку нема.
- Дедукції: «4» — лінії в усі 4 боки; у кружку в куті поля ≤ 2 лінії, на краю ≤ 3; дві «1», зʼєднані між собою, утворили б замкнену пару — заборонено, якщо кружків більше двох; партнер кружка — лише той, до кого веде пряма або L-шлях через порожні клітинки.

## Керування і ввід
- puzz.link play: протяжка лівою кнопкою по центрах клітинок — лінія; хрестик × на межі — режим `peke`; жанр має `irowake: true` — кнопка перефарбування ліній дає кожній мережі свій колір.
- puzz.link edit: клавіші 1–4 — число, `-` — кружок без числа (тест вводу «numbers and dashes»), клік мишею — значення по колу, правий клік — назад.
- Папір: лінії олівцем по пунктирах; Janko малює кружки у вузлах сітки.

## Вікна, меню, HUD
- `game-screen` (puzz.link): пунктирна сітка, кружки, лінії, хрестики; кнопки Check · Undo · Redo · Erase answer · Erase marks · Irowake · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` на лінії чи кружку з помилкою; `+ui:loop-color-coding` — мережі різними кольорами.
- `help-window` — rules.html?ichimaga.
- `editor-window` — той самий екран у режимі Edit; `+window:game-id-dialog` — URL пазла.
- Переходи: rules → плеєр за URL → Check → «розвʼязано» або текст першої помилки. Варіанти — окремі id жанрів `ichimagam` і `ichimagax`.

## Фічі поза полем
- `auto-check` (off / guarded / simple) і Check з текстом першого порушеного правила.
- `undo` ∞ / `redo`, `+feature:trial-mode`, кольори мереж (`irowake`).
- `level-editor` + `share-code` (URL), файли pzprv3.
- `puzzle-bank`: Janko — 5 пазлів.

## Варіації й родичі
- Magnetic Ichimaga (磁石イチマガ, `ichimagam`) — кружки з однаковим числом не можна зʼєднати напряму.
- Crossing Ichimaga (一回曲がって交差もするの, `ichimagax`) — лінії можуть перетинатися, але не в кружку.
- [Hashiwokakero](hashiwokakero.md) — та сама ідея «число = зʼєднання, одна мережа», але мости прямі й бувають подвійні.
- [Coffee Milk](coffee-milk.md) — прямі лінії між кружками, ціль — групи заданого складу, а не одна мережа.
- [Molekularis](molekularis.md) — літера-валентність, звʼязки лише між сусідами на стільниках.
- [Shisen-Sho](../falling-match/shisen-sho.md) — шлях між плитками з ≤ 2 поворотами.
- **Осі варіацій**: поворотів на зʼєднання (0 / ≤ 1 / ≤ 2) · перетини (заборонені / дозволені поза вузлами) · кратність (1 / 2) · заборонені пари кінців (рівні числа — Magnetic) · ціль (одна мережа / групи).

## Цікавинки для курсу
- Обхід лінії від кружка до кружка з лічильником поворотів — 🌱.
- Ступінь кружка й «≥ 1» для кружка без числа — 🌱.
- Звʼязність мережі (BFS по кружках через лінії) — 📎.
- Кандидати-зʼєднання: пряма або дві L-траєкторії для пари кружків, перевірка вільних клітинок і перетинів — 📎.
- Розвʼязувач: вибір підмножини L-шляхів без перетинів зі ступенями й звʼязністю (Hashi з геометрією) — 🥇.
- Варіанти Magnetic і Crossing як перемикачі в налаштуваннях — 🌱 кожен.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection`, `markup-validity` · `path-drawing` ↔ лінія протяжкою · `edge-marking` ↔ хрестики на межах · `connectivity-check` ↔ одна мережа · `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `keyboard-controls` ↔ редактор і URL.
- Перевикористано: `+bend-limited-path` (Shisen-Sho; слот max_turns: 1) · `+valence-bonds` (Sokobond: число = скільки зʼєднань) · `+crossing-detection` · `+wildcard-clue` (кружок без числа, ≥ 1) · `+trial-mode`.
- **Нема** → пропозиції карток:
  - `+link-pair-ban` «Заборонені пари кінців лінії» · game-logic/constraints · 🌱 · слот {ban: equal-numbers | white-black | same-colour} — Magnetic Ichimaga, [Coffee Milk](coffee-milk.md), Shirokuro-link.

## Пропозиції до словників
- `+cond:path_turns` — повтор (Shisen-Sho): поворотів на шляху ≤ N; тут N = 1.
- `+cond:degree` — повтор: скільки ліній виходить із кружка / сходиться в клітинці.
- `+cond:crosses` — повтор.
- `+card:bend-limited-path` — повтор зі слотом `max_turns: 1`.
- `+card:link-pair-ban` — див. мапу.
- `+ui:loop-color-coding` — повтор: `irowake` фарбує кожну мережу своїм кольором.

## Джерела
- ⭐ [puzz.link: Ichimaga](https://puzz.link/rules.html?ichimaga) — правила й приклад у браузері (текст рендериться JS), вхід у плеєр.
- [pzpr-samples/ichimaga.js](https://puzz.link/js/pzpr-samples/ichimaga.js) — «Draw lines over the dotted lines to connect the circles into one network», ≤ 1 поворот, без розгалужень і перетинів, число = лінії; «Puzzle Communication Nikoli vol. 35»; коди brNoLine · lnBranch · lcCurveGt1 · lnCross · lcDivided · lcDeadEnd · nmLineNe · nmNoLine.
- [pzprjs ichimaga.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/ichimaga.js) — режими `line` / `peke`, `maxnum: 4`, `irowake`, перевірки варіантів (`lcSameNum` для Magnetic, без `lnCross` для Crossing).
- [pzprjs variety.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/pzpr/variety.js) — назви イチマガ / 磁石イチマガ / 一回曲がって交差もするの.
- [Janko: Ichimaga](https://www.janko.at/Raetsel/Ichimaga/index.htm) — 5 правил (кружок без числа — ≥ 1 лінія; через вузол — одна лінія), приклад, 5 пазлів.
- YouTube: [пошук «Ichimaga puzzle»](https://www.youtube.com/results?search_query=Ichimaga+puzzle).

## Непевне
- (?) Рік: Nikoli vol. 35 — за датуванням JA-Вікіпедії (№31 — 06.09.1990, №38 — 01.06.1992, щокварталу) ≈ вересень 1991; `year: null`.
- (?) Назва: Janko вважає її неперекладною; назва варіанта в pzprjs «一回曲がって交差もするの» («той, що повертає раз і ще й перетинається») натякає на イチマガ = 一回曲がる «повертає один раз».
- (?) Janko називає жанр і «Jishaku-Ichimaga» (磁石イチマガ), а його JA-текст має правило «рівні числа не зʼєднуються»; DE/EN-правила й приклад Janko цього не мають (у прикладі «3» зʼєднано з «3»).
- (?) Призначення кнопок миші в puzz.link (стерти, хрестик) — загальна схема pzpr; у коді жанру видно лише режими `line` і `peke`.
- (?) Чи завжди кружок без числа в puzz.link вимагає ≥ 1 лінії — так каже Janko і код `nmNoLine` («A circle doesn't start any line»), явного тесту не бачив.
