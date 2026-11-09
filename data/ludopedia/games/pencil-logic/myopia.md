---
title: Myopia (Короткозорість)
slug: myopia
aka: [Короткозорість, Myopia loop]
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
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?myopia", best: true, note: "puzz.link: правила з прикладом (сторінку малює JS; текст правил — у pzpr-samples)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/myopia.js", note: "правила EN, 7 кодів помилок, тести вводу стрілок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/myopia.js", note: "код pzprjs: режими вводу, відстань до лінії, перевірки стрілок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzpr"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/2021/04/myopia-by-ashish-kumar/", note: "GM Puzzles: правила, пазл Ashish Kumar, PDF і відео-розвʼязок"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/?p=6069", note: "GM Puzzles 2016: Yajilin (Myopia) — ті самі стрілки, ціль — чорні клітинки"}
  - {kind: other, url: "https://dailykrownundrum.blogspot.com/2023/08/32-myopia.html", note: "блог: жанр новий на puzz.link, реалізація Mitchell «DireKrow» Clarke з X_Sheep"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=myopia+loop+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, single-loop-check, edge-marking, path-drawing, conflict-highlight, keyboard-controls, in-game-editor, import-open-formats, undo-redo, rule-variants, +inside-outside-coloring, +nearest-in-direction-clue, +multi-arrow-clue, +outline-from-coloring]
proposes: ["+cond:nearest_dist(cell, dir, kind)", "+cond:dead_end", "+trigger:pattern(loop_branch)", "+card:nearest-in-direction-clue", "+card:multi-arrow-clue", "+card:outline-from-coloring"]
author: opus
date: 2026-11-09
---

# Myopia — петля по ребрах, а стрілки в клітинках «короткозоро» показують, з якого боку петля найближча

## Суть
Гравець проводить одну замкнену петлю по ребрах сітки, як у Slitherlink, але підказки — не числа, а клітинки з 1–4 стрілками. Стрілки вказують усі напрямки, у яких найближче ребро петлі (якщо стрілок кілька — відстані однакові); у напрямках без стрілки петля далі або її нема зовсім. Незвичне: підказка задає не кількість, а **порядок відстаней** у чотирьох напрямках — «бачу лише найближче».

## Поле і час
- Прямокутна сітка клітинок; лінії петлі лежать на ребрах між вузлами решітки.
- Підказка — клітинка з будь-якою непорожньою комбінацією стрілок ↑ → ↓ ← (pzpr зберігає маску 1–15); «?» — клітинка-підказка з невідомими стрілками (редактор pzpr), перевірками ігнорується.
- Відстань (код `getLineDirs`): промінь із клітинки в напрямку перетинає ребра поперек; власне ребро клітинки = 1, ребро наступної клітинки = 2 і т. д.; ребра петлі, паралельні променю, не враховуються.
- Шари: стрілки (незмінні) · ребро: лінія / хрестик / порожнє · допоміжний фон клітинок «всередині / зовні».
- Час статичний; хід = поставити/стерти лінію чи хрестик на ребрі або колір фону клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка-підказка | static | маска стрілок 1–15 | визначає відстані до петлі в 4 напрямках |
| Стрілка | mark | напрям | у її напрямку є ребро петлі, і воно найближче серед усіх напрямків |
| Напрям без стрілки | mark | — | ребро петлі строго далі за відстань стрілок або його нема |
| «?»-підказка | static | — | клітинка позначена як підказка, обмежень не дає |
| Ребро сітки | mark | лінія / хрестик / порожнє | гравець перемикає стан |
| Вузол решітки | static | ступінь 0 або 2 | 1 — тупик, 3 — розгалуження, 4 — перетин |
| Петля | zone | — | рівно один цикл |
| Колір фону | mark | всередині / зовні | допоміжний; «outline» проводить лінії на межах кольорів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edges)` → ТО `mark(edge, line)` уздовж протяжки; клік без руху — `mark(edge, cross)`; права кнопка протяжкою — хрестики (pzpr `mouseinput_auto`).
- КОЛИ `input(bgcolor, cell)` → ТО `paint(cell, inside|outside)` (режими `bgcolor1` / `bgcolor2`).
- КОЛИ `input(outlineshaded)` → ТО `custom: «на кожному ребрі між клітинками різних кольорів — лінія, між однаковими — нема; поза полем вважається "зовні"»` (pzpr `outlineShaded`).
- КОЛИ `pattern(loop_branch)` → ТО `set_state(vertex, error)` (`lnBranch`: «There is a branch line»).
- КОЛИ `pattern(loop_cross)` → ТО `set_state(vertex, error)` (`lnCross`: «There is a crossing line»).
- КОЛИ `constraint_broken(arrow_seen)` → ЯКЩО `custom: «промінь у напрямку стрілки не перетинає жодного ребра петлі»` (`+cond:nearest_dist`) → ТО `set_state(arrow, error)` (`arNoLineSeen`: «There is no line in the direction of an arrow»).
- КОЛИ `constraint_broken(arrow_nearest)` → ЯКЩО `custom: «у напрямку без стрілки ребро петлі на відстані ≤ відстані стрілок»` → ТО `set_state(clue, error)` (`arDistanceGt`: «There is a line closer to a clue in an unmarked direction»).
- КОЛИ `constraint_broken(arrow_equal)` → ЯКЩО `not same(arrow_rays, distance)` → ТО `set_state(arrow, error)` (`arDistanceNe`: «The lines pointed to by a clue are at different distances»).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «у вузлі рівно одна лінія»` (`+cond:dead_end`) → ТО `set_state(vertex, error)` (`lnDeadEnd`).
- КОЛИ `constraint_broken(one_loop)` → ЯКЩО `not single_loop` → ТО `set_state(board, error)` (`lnPlLoop`: «There are multiple loops»).
- КОЛИ `constraint_broken(full)` → ЯКЩО `mode(slither_full)` and `custom: «вузол без лінії»` → ТО помилка (варіант «All vertices must be visited», `checkNoLineIfVariant`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «власні ребра»: ребро самої клітинки-підказки в напрямку без стрілки має відстань 1, а відстань стрілок ≥ 1 — тож воно ніколи не лінія (хрестик одразу).
- Дедукція «рівні відстані»: стрілки ↑ і ↓ разом — петля перетинає стовпець на однаковій відстані вгору й униз; чотири стрілки — однакова відстань у всіх напрямках.
- Дедукція «далі за найближче»: якщо стрілка ↑ уже бачить ребро на відстані d, у напрямках без стрілки d ребер поспіль — хрестики.
- Блог-порада: «try shading the loop» — розфарбування всередині/зовні часто відкриває наступний крок.
- Перемога: одна петля без розгалужень і перетинів, усі стрілки правдиві. Поразки й рахунку нема.

## Керування і ввід
- Play (puzz.link): ліва протяжка по ребрах — лінія; клік по ребру — хрестик; права протяжка — хрестики; режими панелі `line`, `peke`, `bgcolor`, `bgcolor1`, `bgcolor2`, `clear`, `info-line`.
- Edit: протяжка з клітинки в бік — перемикає стрілку цього напрямку; клавіші `1`/`w`/Shift+↑ — ↑, `2`/`s`/Shift+→ — →, `3`/`z`/Shift+↓ — ↓, `4`/`a`/Shift+← — ←; `5`/`q`/`-` — «?»; `6`/`e`/пробіл/BS — стерти.
- Звичайні стрілки клавіатури рухають курсор; з Shift — ставлять стрілку.
- Папір: лінії олівцем по ребрах, хрестики на «точно ні».

## Вікна, меню, HUD
- `game-screen`: сітка з крапками-вузлами, клітинки зі стрілками-вістрями біля країв клітинки, лінії петлі (кольорові `irowake`), хрестики, `conflict-highlight` — окремо на кожній помилковій стрілці й на клітинках/ребрі, що «ближчі» за неї.
- Решта — спільний інтерфейс puzz.link ([puzz-link](puzz-link.md)): Check, Undo/Redo, перемикач Edit/Play, `help-window` (rules.html з прикладом), URL input/output, прапорець варіанта «full».
- Переходи: rules.html → p?myopia (edit) → URL → play → Check → текст першої помилки.

## Фічі поза полем
- `auto-check` з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL; прапорець `f` = варіант `slither_full`).
- `custom-rules`: варіант «петля проходить через усі вузли».
- `puzzle-bank` — GM Puzzles (PDF + відео), блог Daily Krown Undrum; генератора не бачив (?).

## Варіації й родичі
- [Slitherlink](slitherlink.md) — та сама петля по ребрах, підказка = кількість ребер навколо клітинки.
- Стрілки Myopia як тип підказки в інших жанрах: Yajilin (Myopia) — стрілки на найближчі чорні клітинки (GM Puzzles, 2016); [Pentopia](pentopia.md) — стрілки на найближчі пентаміно; у видачі пошуку також Star Battle Myopia, Cave Myopia (GM Puzzles) і Anableps (Myopia + Aquarium, Logic Masters) (?).
- Родичі «напрямок → найближче»: [Kuromasu](kuromasu.md) (рахує видиме), [Yajilin](yajilin.md) (стрілка + кількість).
- **Осі варіацій**: що шукає стрілка (ребро петлі / чорна клітинка / фігура) · петля по ребрах чи по центрах клітинок · чи має петля пройти всі вузли (full) · одна стрілка чи комбінації.

## Цікавинки для курсу
- Промінь від клітинки до першого ребра петлі з підрахунком відстані — 🌱: цикл із кроком у подвоєних координатах.
- Перевірка підказки: мінімум по стрілках, рівність стрілок, «строго далі» для решти — 📎 (три окремі помилки з підсвіткою саме тієї стрілки).
- Комбінація стрілок як бітова маска 1–15 і поворот поля таблицею перетворення масок (pzpr `getTranslateDir`) — 📎.
- Розфарбування «всередині/зовні» → петля на межах кольорів — 📎: дуальність «петля = межа області».
- Повний валідатор (ступені вузлів, одна компонента + стрілки) — 🥉; розвʼязувач із пропагацією і перебором — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `single-loop-check` ↔ одна петля · `edge-marking` ↔ лінія/хрестик на ребрі · `path-drawing` ↔ протяжка лінії · `conflict-highlight` · `keyboard-controls` ↔ стрілки з клавіатури · `in-game-editor`, `import-open-formats` (URL/pzprv3) · `undo-redo` · `rule-variants` ↔ прапорець full.
- Перевикористано: `+inside-outside-coloring` (Slitherlink), `+nearest-in-direction-clue`, `+multi-arrow-clue` (Pentopia, Zeiger).
- **Нема** → пропозиції карток:
  - `+outline-from-coloring` «Лінії на межах розфарбованих областей одним дійством» · interface/input · 📎 · слот {outside: board-edge-colour} — Myopia, Slitherlink-подібні у pzpr.

## Пропозиції до словників
- `+cond:nearest_dist(cell, dir, kind)` — повтор із Pentopia: відстань до першої сутності виду в напрямку.
- `+cond:dead_end` — повтор із Nurimisaki: вузол/клітинка мережі має рівно одного сусіда.
- `+trigger:pattern(loop_branch)` — повтор (Yajilin, Moon or Sun).
- `+card:nearest-in-direction-clue`, `+card:multi-arrow-clue` — повтор із Pentopia.
- `+card:outline-from-coloring` — див. мапу.

## Джерела
- ⭐ [puzz.link rules: Myopia](https://puzz.link/rules.html?myopia) — правила з інтерактивним прикладом (без JS сторінка порожня).
- [pzpr-samples myopia.js](https://puzz.link/js/pzpr-samples/myopia.js) — текст правил, коди `lnBranch`, `lnCross`, `lnPlLoop`, `lnDeadEnd`, `arNoLineSeen`, `arDistanceGt`, `arDistanceNe`, тести вводу.
- [pzprjs myopia.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/myopia.js) — режими вводу, `outlineShaded`, маска стрілок до 15, `getLineDirs`, порядок перевірок.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [GM Puzzles: Myopia by Ashish Kumar](https://www.gmpuzzles.com/blog/2021/04/myopia-by-ashish-kumar/) — правила («all the directions where the nearest loop segments are located»), 2 зірки, збірка «Loop Variety Collection».
- [GM Puzzles: Yajilin (Myopia)](https://www.gmpuzzles.com/blog/?p=6069) — 24.08.2016, Murat Can Tonta; стрілки Myopia в Yajilin.
- [Daily Krown Undrum #32](https://dailykrownundrum.blogspot.com/2023/08/32-myopia.html) — серпень 2023, жанр додано в puzz.link, порада «shade the loop».

## Непевне
- (?) Автор і рік появи жанру не знайдено: найраніше бачене — підказки Myopia в Yajilin (GM Puzzles, 2016); окремий жанр на GM Puzzles — 2021, у puzz.link — 2023.
- (?) Сенс «?»-підказки в pzpr: клітинка без стрілок, яку перевірки пропускають; чи вживається в пазлах — не бачив.
- (?) Правила «full» (усі вузли) — лише коментар у `Config.js` і назва перевірки `checkNoLineIfVariant`; код перевірки не читав.
- (?) Star Battle Myopia, Cave Myopia, Anableps — бачив лише назви у видачі пошуку.
