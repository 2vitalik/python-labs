---
title: Heyawake (Хеявакé, «поділені кімнати»)
slug: heyawake
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
year: 1992
platforms: [paper, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Heyawake", best: true, note: "5 правил, Nikoli №39 (вересень 1992), техніки старту по кімнатах, варіанти Heyawacky і Symmetry, NP-повнота"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/heyawake/", note: "Nikoli: правила, Sample → Progressing → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/heyawake.js", note: "puzz.link: текст правил EN/JA, 5 кодів помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?heyawake", note: "puzz.link: сторінка правил (текст рендериться JS)"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/Heyawake", note: "WPC-вікі: автор, варіанти Heyawacky / Akichiwake, 17 раундів WPC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=heyawake+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, reachability-check, level-solver, unique-puzzle-generation, level-bank, import-open-formats, in-game-editor, +undo-redo, +cell-shade-toggle, +dot-mark, +no-adjacent-check, +global-connectivity, +region-quota, +irregular-regions, +white-run-border-limit]
proposes: ["+cond:run_rooms", "+trigger:pattern(long_white_run)", "+card:white-run-border-limit", "+card:room-symmetry-check"]
author: opus
date: 2026-11-02
---

# Heyawake — зафарбуй клітинки в кімнатах так, щоб жодна біла лінія не прошила три кімнати

## Суть
Сітка поділена товстими лініями на прямокутні «кімнати», частина з них має число — скільки в кімнаті чорних клітинок. Гравець зафарбовує клітинки за трьома глобальними умовами: чорні не торкаються сторонами, білі звʼязні, і жоден прямий горизонтальний чи вертикальний відрізок білих не перетинає дві межі кімнат (тобто не тягнеться через 3 кімнати). Незвичне: останнє правило — **обмеження на довжину білого променя відносно розмітки кімнат**, рідкісний тип обмеження, що поєднує геометрію ліній із регіонами.

## Поле і час
- Прямокутна сітка; кімнати — прямокутники, задані товстими межами (у Heyawacky — довільні поліоміно).
- Сусідство ортогональне (4) для заборони дотику чорних і для звʼязності білих; діагональний дотик чорних дозволено.
- Шари: межі кімнат і числа (незмінні) · стан клітинки гравця: невідомо / зафарбовано / крапка («точно біле»).
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | прямокутник, число N або без числа | рівно N чорних клітинок; без числа — будь-яка кількість, зокрема 0 |
| Число кімнати | static | N | друкується в кутовій клітинці кімнати; сама клітинка може бути чорною (?) |
| Клітинка | mark | стан unknown / shaded / dot | клік змінює стан |
| Зафарбована клітинка | mark | — | не сусідить сторонами з іншою чорною |
| Крапка | mark | — | позначка гравця «тут біле» |
| Межа кімнати | static | ребро сітки | лічильник перетинів для білого відрізка |
| Білий відрізок | zone | клітинки поспіль в рядку/стовпці | перетинає ≤ 1 межу кімнати (охоплює ≤ 2 кімнати) |
| Біла область | zone | кількість компонент | усі білі — одна 4-звʼязна компонента |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (типова схема puzz.link для зафарбовувань) (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (?).
- КОЛИ `constraint_broken(room_count)` — ЯКЩО `not count(shaded in room, ==, N)` → ТО кімната підсвічена (puzz.link `bkShadeNe`).
- КОЛИ `constraint_broken(no_adjacent_shaded)` — ЯКЩО `adjacent_count(shaded, shaded, >, 0)` → ТО конфлікт (`csAdjacent`).
- КОЛИ `constraint_broken(white_connected)` — ЯКЩО `not connected(white)` → ТО конфлікт (`cuDivideRB`; flood fill / BFS).
- КОЛИ `pattern(long_white_run)` — ЯКЩО `custom: «відрізок білих у рядку/стовпці перетинає ≥ 2 межі кімнат»` → ТО `constraint_broken(run_rooms)` (`bkUnshadeConsecGt3`: білий відрізок через ≥ 3 кімнати).
- КОЛИ `constraint_broken(board_not_empty)` — нічого не зафарбовано → ТО конфлікт (`brNoShade`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукції (Wikipedia): чорна → 4 сусіди білі; не можна відрізати білих (чорні не утворюють діагонального «розрізу» поля чи замкненого кільця); кутова кімната 2×2 з «2» — одна чорна в куті й одна навскіс; кімната 1×3 з «2» — обидва кінці чорні; 1×(2n−1) з «n» — через одну; 3×3 з «5» — шахівниця з чорними кутами й центром; важкі пазли — вибір між двома шаховими патернами, один з яких дає «коротке замикання» (розрізає білих).
- Дедукція від правила відрізка: якщо білий ряд уже тягнеться через 2 кімнати і впирається в межу третьої — перша клітинка за межею чорна.
- Перемога: числа кімнат виконані, чорні не торкаються, білі звʼязні, жоден білий відрізок не охоплює 3 кімнати. Поразки й рахунку нема.

## Керування і ввід
- puzz.link (play mode): ліва кнопка — фарба, права — крапка, drag протягує стан; схема `use=1/2` як у Hitori (?).
- puzz.link edit mode: межі кімнат — drag по ребрах сітки, числа — з клавіатури (?).
- Undo/redo, Check (код першого порушення), Clear answer.
- Тач (цифрова версія): тап — цикл unknown → shaded → dot.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами кімнат і числами + `conflict-highlight` (кімната з неправильною кількістю, сусідні чорні, розрізані білі, задовгий білий відрізок).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: межі, числа, експорт URL.
- `help-window` — правила (Nikoli: Sample / Progressing / Solution).
- `puzzle-select` — книги Nikoli (станом на 2013 — 5 окремих збірок Heyawake), банки сайтів (цифрова версія).
- `end-screen` — розвʼязано.
- Переходи: puzzle-select → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo`/`redo`.
- `level-editor` + `share-code` (puzz.link URL / pzprv3).
- `puzzle-bank` (журнал Nikoli з 1992, книги, змагання WPC).
- Генератора у Tatham нема; генерація з унікальним розвʼязком — дослідницька задача (?).

## Варіації й родичі
- **Heyawacky** — кімнати непрямокутні; білий відрізок не може вийти з кімнати й повернутися (новіша редакція: не проходить три різні кімнати); назва — Thomas Snyder, 2009.
- **Symmetry Heyawake** (ekawayeH, Ayeheya) — чорні в кожній кімнаті центрально-симетричні відносно центру кімнати.
- **Akichiwake** (Prasanna Seshadri, 2014) — число в кімнаті = максимальний розмір білої області в ній; відрізок не перетинає дві послідовні межі.
- Starwacky — гібрид зі Star Battle (?).
- Родичі: Hitori, Kurodoko, Yajilin (чорні не торкаються + білі звʼязні), Star Battle (квота на регіон).
- **Осі варіацій**: форма кімнат (прямокутник / поліоміно) · що рахує число (чорні / розмір білої області) · обмеження відрізка (межі / кімнати / нема) · симетрія всередині кімнати.

## Цікавинки для курсу
- Квота чорних у кімнаті — 🌱 (`+region-quota`).
- Заборона сусідства чорних + звʼязність білих — 🌱 + 📎 (спільний «двигун» Hitori, Kurodoko, Heyawake).
- Перевірка білих відрізків: пройти рядок, розбити на білі серії, порахувати перетнуті межі кімнат — 📎 (потрібна модель кімнат як мапа клітинка → id).
- Модель кімнат із ребер (товсті межі → id регіонів через flood fill) — 📎.
- Розвʼязувач: локальні правила + «точка розрізу білих» + шахові патерни — 🥇.
- Генератор з унікальним розвʼязком і NP-повнотою (Holzer, Ruepp 2007) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` ↔ фарба/крапка · `reachability-check` ↔ звʼязність білих · `level-solver`, `unique-puzzle-generation` · `level-bank` · `import-open-formats` ↔ puzz.link URL · `in-game-editor` ↔ edit mode.
- Перевикористано: `+undo-redo`, `+cell-shade-toggle`, `+dot-mark`, `+no-adjacent-check` (Hitori, Yajilin), `+global-connectivity` (Tatham, Hitori), `+region-quota` (Star Battle; тут N своє для кожної кімнати), `+irregular-regions` (Heyawacky).
- **Нема** → пропозиції карток:
  - `+white-run-border-limit` «Біла серія в лінії перетинає ≤ K меж регіонів» · game-logic/constraints · 📎 · слот {max_borders: 1, measure: borders|rooms}.
  - `+room-symmetry-check` «Розмітка в регіоні симетрична відносно його центру» · game-logic/constraints · 📎 · слот {symmetry: rot180|mirror} — Symmetry Heyawake.

## Пропозиції до словників
- `+cond:run_rooms` — скільки регіонів охоплює неперервна серія клітинок одного стану в рядку/стовпці.
- `+trigger:pattern(long_white_run)` — значення для `pattern(shape)`: біла серія задовга відносно меж.
- `+card:white-run-border-limit`, `+card:room-symmetry-check` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Heyawake](https://en.wikipedia.org/wiki/Heyawake) — правила, №39 (вересень 1992), техніки по кімнатах, варіанти, NP-повнота.
- [Nikoli: Heyawake](https://www.nikoli.co.jp/en/puzzles/heyawake/) — офіційні правила («не довше ніж через дві кімнати по прямій»), приклад.
- [puzz.link heyawake.js](https://puzz.link/js/pzpr-samples/heyawake.js) — правила EN/JA, історія vol. 39, коди `brNoShade`, `csAdjacent`, `cuDivideRB`, `bkShadeNe`, `bkUnshadeConsecGt3`.
- [puzz.link rules](https://puzz.link/rules.html?heyawake) — сторінка правил (без JS порожня).
- [WPC unofficial wiki: Heyawake](https://wpcunofficial.miraheze.org/wiki/Heyawake) — автор Hiroyuki Fukushima, Heyawacky, Akichiwake, раунди WPC 2011–2024.
- YouTube: пошук «heyawake puzzle how to solve».

## Непевне
- (?) Дії мишею в puzz.link для Heyawake — тести вводу у файлі порожні; схему взято з Hitori.
- (?) Чи може клітинка з числом кімнати бути чорною — у правилах Nikoli заборони нема, перевірити на прикладі не вдалося.
- (?) Автор Hiroyuki Fukushima — лише WPC-вікі; Wikipedia автора не називає.
- (?) Starwacky — правила на сторінці не наведено.
