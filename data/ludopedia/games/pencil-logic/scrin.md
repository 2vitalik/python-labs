---
title: Scrin (スクリン, «Екран»)
slug: scrin
aka: [スクリン, Sukurin, Screen, Екран]
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
  - {kind: other, url: "https://puzz.link/rules.html?scrin", best: true, note: "puzz.link: правила EN/JA з прикладом і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/scrin.js", note: "правила EN/JA текстом, «Nikoli vol. 165», 12 тестових станів з кодами помилок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Scrin/index.htm", note: "Janko: 5 правил DE/EN/JA, приклад 6×6, 90 пазлів від 6×6 до 15×15"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/scrin.js", note: "код pzprjs: ввід зафарбуванням, перевірки, сусідній жанр Ant Mill"}
  - {kind: other, url: "https://maybepuzzles.com/2019/04/17/puzzle-173-scrin-and-release-pzprjs-v0-11-0/", note: "Robert Vollmert: Scrin у pzprjs v0.11.0 (17.04.2019) і пазл 6×6"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Scrin+puzzle+nikoli", note: "пошук"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, completion-detection, markup-validity, cell-click, single-loop-check, connectivity-check, conflict-highlight, undo-redo, in-game-editor, import-open-formats, keyboard-controls, +rect-shape-check, +region-size-check, +diagonal-chain, +wildcard-clue, +cell-shade-toggle, +auto-borders, +trial-mode]
proposes: ["+cond:is_rectangle", "+cond:corner_touch", "+cond:region_has", "+card:diagonal-chain"]
author: opus
date: 2026-11-19
---

# Scrin — намалюй прямокутники, що торкаються лише кутами й складають одне кільце

## Суть
Гравець малює на сітці прямокутники вздовж ліній. Кружок має опинитися в прямокутнику (щонайбільше один на прямокутник), число в кружку — площа, порожній кружок — площа невідома; прямокутники без кружків дозволені. Прямокутники не мають спільних ребер, торкаються лише кутами й разом утворюють **одне замкнене кільце** без розгалужень. Незвичне: петлю складають не лінії, а фігури, «зчеплені» кутами. Жанр Nikoli (vol. 165).

## Поле і час
- Квадратна сітка з точками у вузлах; Janko — 90 пазлів від 6×6 до 15×15 (і один 18×10); приклад — 6×6 з чотирма числами й двома порожніми кружками.
- Прямокутник — вирівняний по сітці блок w×h (квадрат теж); частина клітинок лишається поза прямокутниками.
- Дотик кутом — спільна вершина: у вікні 2×2 дві діагональні клітинки в різних прямокутниках, дві інші порожні (pzprjs `countConn`); дотик кута до середини сторони неможливий — він дав би спільне ребро.
- Кільце — граф «прямокутник ↔ кутовий дотик»: кожна вершина має степінь 2, граф звʼязний.
- Час статичний; у puzz.link хід = зафарбувати клітинку (вона стає частиною прямокутника) або поставити ×.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кружок з числом | static | N = площа | лежить у прямокутнику площі N |
| Порожній кружок | static | — | лежить у прямокутнику будь-якої площі |
| Прямокутник | zone | w×h | ≤ 1 кружок; без спільних ребер з іншими; рівно 2 кутові дотики |
| Зафарбована клітинка | mark | — | частина прямокутника (puzz.link: зелена) |
| Хрестик | mark | — | «поза прямокутниками», допоміжний (puzz.link `qsub`) |
| Межа прямокутника | mark | — | у puzz.link малюється сама між зафарбованою й порожньою клітинкою |
| Кільце | zone | — | усі прямокутники в одному циклі через кути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `paint(cell, rect)`; протяжка фарбує кілька клітинок; повтор → `unmark(cell)` (puzz.link) (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, cross)` (puzz.link) (?).
- КОЛИ `constraint_broken(clue_outside)` → ЯКЩО `custom: «кружок поза прямокутником»` → ТО `set_state(clue, error)` («A clue is not inside a rectangle»).
- КОЛИ `constraint_broken(two_clues)` → ЯКЩО `custom: «у прямокутнику ≥ 2 кружки»` (`+cond:region_has`) → ТО `set_state(rect, error)`.
- КОЛИ `constraint_broken(size)` → ЯКЩО `not region_size(rect, N)` → ТО `set_state(rect, error)`.
- КОЛИ `constraint_broken(shape)` → ЯКЩО `custom: «зафарбована область не прямокутник»` (`+cond:is_rectangle`) → ТО `set_state(area, error)` — так ловиться і спільне ребро: два прямокутники злилися б в одну область.
- КОЛИ `constraint_broken(divided)` → ЯКЩО `not connected(rect)` (8-сусідство зафарбованих) → ТО `set_state(rect, error)` («not connected to the other rectangles»).
- КОЛИ `constraint_broken(loop)` → ЯКЩО `custom: «кутових дотиків у прямокутника 0 / 1 / ≥ 3»` (`+cond:corner_touch`) → ТО `set_state(rect, error)` (isolated / dead-end / branch).
- КОЛИ `constraint_broken(phantom)` → ЯКЩО `custom: «порожня область, що не торкається краю, сама має форму прямокутника»` → ТО `set_state(area, error)` («A rectangle is not part of the solution», лише puzz.link).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: кожен кружок у своєму прямокутнику потрібної площі, спільних ребер нема, усі прямокутники — одне кільце. Поразки й рахунку нема.
- Дедукції: «1» — одна клітинка; просте p — смужка 1×p; клітинки, що прилягають ребром до готового прямокутника, порожні; у кожного прямокутника рівно 2 з 4 кутів «зайняті» сусідами.

## Керування і ввід
- puzz.link play: клік або протяжка по клітинках — зафарбувати (прямокутник «наливається» зеленим, межі видно одразу); × — допоміжна позначка «порожньо»; кнопки миші й схема вводу міняються в Settings (LR invert, `use` 1/2 — див. [puzz.link](puzz-link.md)).
- puzz.link edit: курсор і цифри — число в кружку; найбільше число в редакторі — (ширина − 2)·(висота − 2).
- Папір: прямокутники обводять олівцем по лініях сітки.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з точками, кружки, зелені прямокутники; кнопки Check · Undo · Redo · Erase answer · Erase marks · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` на прямокутнику чи кружку з помилкою; `timer-elapsed`.
- `help-window` — rules.html?scrin: правила з прикладом.
- `editor-window` — той самий екран у режимі Edit; `+window:game-id-dialog` — URL пазла.
- Переходи: rules → плеєр за URL → Check → «розвʼязано» або текст першої помилки.

## Фічі поза полем
- `auto-check` (puzz.link: off / guarded / simple) і Check з текстом першого порушеного правила.
- `undo` ∞ / `redo`, `+feature:trial-mode` (шар припущень; у коді scrin.js клітинки спроби сірі).
- `level-editor` + `share-code` (URL), файли pzprv3.
- `puzzle-bank`: Janko — 90 пазлів, найбільше 10×10 (42 шт.).

## Варіації й родичі
- Ant Mill — сусідній жанр у тому ж файлі pzprjs: кільце через кути складають зафарбовані доміно (області рівно з 2 клітинок), а підказки стоять на межах: квадрат — по обидва боки різні кольори, хрестик — однакові.
- [Shikaku](shikaku.md) — прямокутники з числом-площею, але покривають усе поле й межують ребрами.
- [Chained Block](chained-block.md) — блоки, що торкаються кутами, складають ланцюги; [Look-Air](look-air.md) — чорні квадрати торкаються лише кутами.
- [Nagenawa](nagenawa.md) — прямокутні петлі в регіонах; [Slitherlink](slitherlink.md), [Masyu](masyu.md) — одна петля, але з ліній.
- **Осі варіацій**: з чого кільце (лінія / прямокутники / доміно) · форма фігур (будь-які прямокутники / лише доміно) · підказки (площа / порожній кружок / межові квадрат і хрестик) · фігури без підказок (дозволені / ні).

## Цікавинки для курсу
- Чи область — прямокутник: площа = ширина × висота обмежувального прямокутника — 🌱.
- Кутові дотики вікном 2×2 «у шаховому порядку» + степінь кожного прямокутника = 2 — 📎.
- Одне кільце з фігур: граф «прямокутник ↔ дотик», степені 2 і звʼязність (BFS) — 🥉.
- Перевірка puzz.link «внутрішня порожня область не прямокутник» — 🌱.
- Розвʼязувач: для кожного кружка — усі розміщення прямокутника площі N, відкат з перевіркою кільця; прямокутники без кружків роблять пошук важким — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection`, `markup-validity` · `cell-click` ↔ зафарбування · `single-loop-check` ↔ кільце (цикл на графі дотиків, а не на ребрах сітки) · `connectivity-check` ↔ 8-звʼязність зафарбованого · `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `keyboard-controls` ↔ редактор і URL.
- Перевикористано: `+rect-shape-check` (Shikaku) · `+region-size-check` · `+diagonal-chain` (Chained Block; слот {shape: loop, degree: 2}) · `+wildcard-clue` (порожній кружок) · `+cell-shade-toggle` (фарба / × / порожньо) · `+auto-borders` (межі між зафарбованим і порожнім) · `+trial-mode`.
- **Нема** → нових карток не треба; нове — лише слот «кільце» в `+diagonal-chain`.

## Пропозиції до словників
- `+cond:is_rectangle` — повтор (Shikaku): область збігається зі своїм обмежувальним прямокутником.
- `+cond:corner_touch` — повтор: фігура торкається іншої лише кутом; тут важить кількість таких дотиків.
- `+cond:region_has` — повтор: щонайбільше один кружок у прямокутнику.
- `+card:diagonal-chain` — повтор (Chained Block) зі слотом `shape: loop`.

## Джерела
- ⭐ [puzz.link: Scrin](https://puzz.link/rules.html?scrin) — правила й приклад у браузері (текст рендериться JS), вхід у плеєр.
- [pzpr-samples/scrin.js](https://puzz.link/js/pzpr-samples/scrin.js) — правила EN/JA (кути прямокутників на точках, без накладань і спільних меж, ≤ 1 кружок, одна петля через діагональні дотики без розгалужень), «Puzzle Communication Nikoli vol. 165», перевірки bkNumUnshade · bkNumGe2 · bkSizeNe · bkNotRect · csdDivide · rmDeadend · rmBranch · rmIsolated · rmRectUnshade.
- [pzprjs scrin.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/scrin.js) — ввід `shade` / `unshade`, межі між зафарбованим і порожнім, `countConn` за кутами, межа числа в редакторі, жанр Ant Mill.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок («An area is not a rectangle», «There is a dead-end rectangle», «A rectangle is not part of the solution»).
- [Janko: Scrin](https://www.janko.at/Raetsel/Scrin/index.htm) — 5 правил DE/EN/JA, スクリン ≈ «екран», 90 пазлів із розмірами.
- [maybepuzzles: Puzzle 173](https://maybepuzzles.com/2019/04/17/puzzle-173-scrin-and-release-pzprjs-v0-11-0/) — Scrin додано в pzprjs v0.11.0, 17.04.2019.
- YouTube: [пошук «Scrin puzzle nikoli»](https://www.youtube.com/results?search_query=Scrin+puzzle+nikoli).

## Непевне
- (?) Рік: Nikoli vol. 165 — за датуванням JA-Вікіпедії (№150 — весна 2015, №174 — весна 2021, щокварталу) ≈ грудень 2018; узгоджується з появою в pzprjs у квітні 2019; `year: null`.
- (?) Автор жанру невідомий; Janko пише «Puzzle Communication Nikoli», але номер і дату лишає порожніми.
- (?) Що робить правий клік у puzz.link (×) і як стерти фарбу — за загальною схемою pzpr; у коді жанру видно лише режими `shade` / `unshade` і хрестики `qsub`.
- (?) Перевірка `rmRectUnshade` — особливість puzz.link (порожня внутрішня область-прямокутник виглядала б як ще одна фігура); у правилах Nikoli / Janko такого пункту нема.
- (?) Як у редакторі ставиться порожній кружок — імовірно `-`, як в інших жанрах pzpr.
