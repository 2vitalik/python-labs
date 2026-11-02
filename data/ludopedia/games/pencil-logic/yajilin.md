---
title: Yajilin (Яджилін, Arrow Ring)
slug: yajilin
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1999
platforms: [paper, web, mobile]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/yajilin/", best: true, note: "Nikoli: 4 правила, Puzzle Communication Nikoli Vol. 86 (червень 1999), Sample → Progressing → Solution"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Yajilin", note: "правила, назва (yajirushi + link), Arrow Ring у кваліфікації WPC США 2005"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/yajilin.js", note: "puzz.link: правила (з «?»), тести вводу, 9 кодів помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?yajilin", note: "puzz.link: сторінка правил (текст рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yajilin+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, unique-puzzle-generation, level-solver, level-bank, import-open-formats, in-game-editor, +undo-redo, +cell-shade-toggle, +dot-mark, +drag-draw-path, +single-loop-check, +no-adjacent-check, +arrow-count-clue, +cell-coverage-check]
proposes: ["+cond:count_dir", "+cond:on_loop", "+trigger:pattern(loop_branch)", "+role:clue-arrow", "+card:arrow-count-clue", "+card:cell-coverage-check", "+axis:markup-layers"]
author: opus
date: 2026-11-02
---

# Yajilin — зафарбуй клітинки за стрілками, а крізь усі решту проведи одну петлю

## Суть
Гібрид двох жанрів: зафарбовування (як у Hitori/Heyawake) і петлі (як у Masyu/Slitherlink). Частина клітинок — підказки «число + стрілка»: скільки зафарбованих клітинок лежить у напрямку стрілки. Гравець зафарбовує клітинки (не сусідні сторонами) і проводить одну замкнену петлю через **усі** інші порожні клітинки. Незвичне: два шари розмітки взаємно виключні — кожна вільна клітинка або чорна, або на петлі, тож рішення про петлю «виштовхує» чорні й навпаки.

## Поле і час
- Прямокутна сітка; типи клітинок: підказка (число+стрілка ↑↓←→, або «?» у puzz.link) · порожня.
- Петля йде через центри клітинок ортогонально, повертає на 90°; сусідство 4-звʼязне і для петлі, і для заборони дотику чорних.
- Шари клітинки: тип (незмінний) · стан гравця: невідомо / зафарбовано / крапка · сегменти лінії до сусідів.
- Час статичний; хід = зафарбувати/позначити клітинку або провести/стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Підказка «число + стрілка» | static | N, напрям | рівно N зафарбованих у напрямку до краю поля; сама не фарбується й не на петлі |
| Підказка «?» (puzz.link) | static | — | не фарбується, не на петлі, число невідоме |
| Порожня клітинка | mark | стан unknown / shaded / dot; лінії | у розвʼязку — або чорна, або на петлі |
| Зафарбована клітинка | mark | — | не сусідить сторонами з іншою чорною; петля не проходить |
| Крапка | mark | — | позначка гравця «не чорна» (отже, на петлі) |
| Відрізок петлі | mark | між двома сусідніми клітинками | частина лінії; ступінь кожної клітинки 0 або 2 |
| Петля | zone | клітинки на ній | одна, замкнена, без розгалужень і перетинів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `cell(x, empty)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)`.
- КОЛИ `input(left_drag, path)` → ТО `custom: «провести відрізки лінії між центрами клітинок»`; drag по наявній лінії — стерти (?).
- КОЛИ `constraint_broken(arrow_count)` — ЯКЩО `not count_dir(clue, dir, shaded, ==, N)` → ТО підказка підсвічена (puzz.link `anShadeNe`).
- КОЛИ `constraint_broken(no_adjacent_shaded)` — ЯКЩО `adjacent_count(shaded, shaded, >, 0)` → ТО конфлікт (`csAdjacent`).
- КОЛИ `pattern(loop_branch)` — клітинка зі ступенем 3–4 → ТО `constraint_broken(no_branch)` (`lnBranch`); перетин — `lnCross`.
- КОЛИ `constraint_broken(line_on_shade)` — лінія через чорну клітинку → ТО конфлікт (`lnOnShade`).
- КОЛИ `constraint_broken(dead_end)` — ступінь 1 → ТО конфлікт (`lnDeadEnd`).
- КОЛИ `constraint_broken(single_loop)` — ≥ 2 замкнених петель → ТО конфлікт (`lnPlLoop`).
- КОЛИ `constraint_broken(cover_all)` — порожня клітинка ні чорна, ні на петлі → ТО конфлікт (`ceEmpty`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукції: «0» у напрямку → усі клітинки до краю на петлі; число, що дорівнює максимуму місць (через одну), фіксує чорні; кут поля, обрамлений чорною, — петля мусить повернути; чорна клітинка → її 4 сусіди на петлі.
- Перемога: стрілки виконані, чорні не торкаються, одна петля проходить усі інші вільні клітинки. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: ліва кнопка по клітинці — фарба; права — крапка; ліва з протягуванням — лінія; тести показують і стирання лінії/крапок правим протягуванням (?).
- Режими play/edit у puzz.link: в edit — ставити підказки (стрілка + число з клавіатури).
- Тач: drag — лінія, тап — фарба (типова поведінка плеєрів) (?).
- Undo/redo, `ansclear` — очистити відповідь.

## Вікна, меню, HUD
- `game-screen`: сітка з підказками-стрілками, чорні клітинки, лінія петлі, крапки, `conflict-highlight` (підказка, чорні поруч, кінці лінії, розгалуження), `path-preview` під час drag (?).
- Кнопки: Check (текст першої помилки), Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: стрілки й числа, експорт у URL.
- `help-window` — правила (Nikoli Sample / Progressing / Solution).
- `puzzle-select` — книги/банк Nikoli, GMPuzzles (?).
- `end-screen` — розвʼязано.
- Переходи: puzzle-select → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo`/`redo`; очистити відповідь.
- `level-editor` + `share-code` (puzz.link URL, формат pzprv3).
- `puzzle-bank` (журнал Nikoli з 1999, міжнародні змагання: Arrow Ring у кваліфікації WPC США 2005).
- Генератора у відомих безкоштовних колекціях не бачив (у Tatham жанру нема) (?).

## Варіації й родичі
- Підказка «?» — клітинка-заглушка без числа (puzz.link).
- Родичі: Masyu, Slitherlink (петля), Hitori/Heyawake/Kurodoko (чорні не торкаються), Nurikabe (числа рахують клітинки); варіанти з регіонами, сірими клітинками чи числами без стрілок у спільноті (?).
- **Осі варіацій**: що рахує підказка (чорні / біле / довжину сегмента) · напрям (стрілка / усі 4 / сусіди) · що покриває петля (усі вільні / лише позначені) · заборона дотику чорних (4 / 8 / нема).

## Цікавинки для курсу
- Підрахунок чорних у напрямку стрілки до краю — 🌱 (`count_dir`).
- Перевірка «одна петля без розгалужень, ступінь 2» — 📎 (є пропозиція `+single-loop-check`).
- Покриття: кожна вільна клітинка або чорна, або на петлі — 🌱, але показовий приклад двох взаємовиключних шарів розмітки.
- Ввід лінії drag-ом між центрами клітинок + фарба кліком в одному режимі — 📎 (розрізнити клік і протягування).
- Розвʼязувач: стрілки + «чорна → сусіди на петлі» + заборона малих петель — 🥇.
- Генератор (гамільтонів цикл на частині сітки + чорні + підказки + унікальність) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` ↔ фарба/крапка · `unique-puzzle-generation`, `level-solver` · `level-bank` · `import-open-formats` ↔ puzz.link URL · `in-game-editor` ↔ edit mode.
- Перевикористано: `+undo-redo`, `+cell-shade-toggle`, `+dot-mark`, `+drag-draw-path` (з Masyu), `+single-loop-check` (Masyu, Slitherlink), `+no-adjacent-check` (з Hitori).
- **Нема** → пропозиції карток:
  - `+arrow-count-clue` «Підказка-стрілка: скільки X у напрямку» · game-logic/constraints · 🌱 · слот {counts: shaded|white|segments}.
  - `+cell-coverage-check` «Кожна вільна клітинка покрита одним із шарів» · game-logic/constraints · 🌱 — шлях або чорна.

## Пропозиції до словників
- `+cond:count_dir` — кількість сутностей виду в напрямку від клітинки до краю.
- `+cond:on_loop` — клітинка належить лінії петлі.
- `+trigger:pattern(loop_branch)` — значення для `pattern(shape)`: розгалуження/перетин лінії.
- `+role:clue-arrow` — підказка з напрямком (Yajilin; родич `+role:clue-outside` з Nonogram).
- `+axis:markup-layers` — скільки взаємодіючих шарів розмітки (1: фарба · 2: фарба + лінія).
- `+card:arrow-count-clue`, `+card:cell-coverage-check` — див. мапу.

## Джерела
- ⭐ [Nikoli: Yajilin](https://www.nikoli.co.jp/en/puzzles/yajilin/) — 4 правила, історія Vol. 86 (червень 1999), ілюстрації.
- [Wikipedia: Yajilin](https://en.wikipedia.org/wiki/Yajilin) — правила, етимологія, Arrow Ring.
- [puzz.link yajilin.js](https://puzz.link/js/pzpr-samples/yajilin.js) — правила плеєра з «?», тести вводу, коди `anNoArrow`, `lnBranch`, `lnCross`, `lnOnShade`, `csAdjacent`, `anShadeNe`, `lnDeadEnd`, `lnPlLoop`, `ceEmpty`.
- [puzz.link rules](https://puzz.link/rules.html?yajilin) — сторінка правил (без JS порожня).
- YouTube: пошук «yajilin puzzle how to solve».

## Непевне
- (?) Значення `anNoArrow` (ймовірно, підказка з числом без стрілки) — тексту не бачив.
- (?) Точні дії мишею в puzz.link (що робить повторний клік, стирання лінії) — виведено з тестів без очікуваних результатів.
- (?) Складність (NP-повнота) — Wikipedia не згадує.
- (?) Варіанти з регіонами/сірими клітинками — з памʼяті про спільноту.
