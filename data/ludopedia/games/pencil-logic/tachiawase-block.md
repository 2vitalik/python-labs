---
title: Tachiawase Block
slug: tachiawase-block
aka: [tachibk]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/tachibk.js", best: true, note: "puzz.link: правила, коди помилок, тести (парна ширина, межа центру), vol. 173"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tachiawase+block+puzzle", note: "пошук"}
stage: v1
coverage: 60
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, piece-rotate-flip, conflict-highlight, in-game-editor, undo-redo, +twin-grid-bank, +overlay-size-clash, +no-dead-end-border, +shape-identity-check]
proposes: ["+cond:same_shape(a, b)", "+cond:same_bank(grid_a, grid_b)", "+cond:overlaps(a, b)", "+cond:no_dead_end(borders)", "+axis:field=twin-grids", "+card:twin-grid-bank", "+card:overlay-size-clash"]
author: opus
date: 2026-11-09
---

# Tachiawase Block — розріж дві сітки на однаковий набір блоків так, щоб при накладанні однакові за розміром не збігались

## Суть
Поле — дві однакові за розміром сітки поруч, з числами в деяких клітинках. Гравець малює межі по пунктирних лініях і ділить кожну сітку на блоки; число каже розмір блоку, що його містить. Обидві сітки мусять складатися з **одного й того самого набору блоків** (форми з точністю до поворотів і відбиттів). Якщо накласти сітки одна на одну без повороту, блок не може перекриватися з блоком такого самого розміру з іншої сітки. Незвичне: обмеження звʼязує **два поля** — банк фігур спільний, а накладка забороняє збіг. Nikoli, Puzzle Communication Nikoli vol. 173.

## Поле і час
- Одне поле парної ширини, розрізане по центру на дві сітки W/2 × H; центральну межу малювати не можна (вона завжди є).
- Розвʼязок — межі по ребрах обох сіток.
- Накладка: клітинка (x, y) лівої сітки відповідає клітинці (x, y) правої — без повороту й відбиття.
- Час статичний; хід = змінити стан одного ребра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сітка A / сітка B | zone | W/2 × H, однакові | кожна ділиться на блоки окремо |
| Центральна межа | static | — | завжди межа; редагувати не можна |
| Клітинка з числом | static | N | належить блоку розміру N; блок може мати кілька чисел або жодного |
| Порожня клітинка | mark | належність до блоку | входить рівно в один блок своєї сітки |
| Ребро | mark | невідомо / межа / «не межа» | межі ріжуть сітку |
| Блок | zone | форма, розмір | звʼязна група; має пару тієї ж форми в іншій сітці |
| Банк блоків | static | мультимножина форм | однаковий для обох сіток |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edge)` → ЯКЩО `custom: «ребро не на центральній межі»` → ТО `mark(edge, border)`; повтор → `unmark(edge)` (тест «Don't draw over center grid border»).
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, no_border)` (?).
- КОЛИ `constraint_broken(size)` → ЯКЩО `region_size(block, > N)` → ТО конфлікт (`bkSizeGt`); `< N` → `bkSizeLt`.
- КОЛИ `constraint_broken(bank)` → ЯКЩО `custom: «набори форм блоків сіток A і B різні (повороти й відбиття = одна форма)»` → ТО конфлікт (`bankNe`).
- КОЛИ `constraint_broken(overlay)` → ЯКЩО `custom: «блок A і блок B спільно займають клітинку при накладанні»` and `same(block_a, block_b, size)` → ТО конфлікт (`ceOverlap`).
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «межа обривається всередині блоку»` → ТО конфлікт (`bdDeadEnd`, лише з опцією skiprules) (?).
- Редактор: КОЛИ `input(new_board, w, h)` → ЯКЩО `custom: «w непарне»` → ТО `custom: «ширина вирівнюється до парної»` (тест «Enforce even amount of columns»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідки: сумарні площі однакові автоматично; кількість блоків кожного розміру в A і B однакова; блок розміру, що трапляється в банку один раз, лежить у A і B у місцях без спільних клітинок.
- Дедукції: число N в A і та сама клітинка в B з числом N — різні блоки, що не можуть перекриватися (суперечність, якщо обидва змушені накрити ту саму клітинку); форму, визначену в одній сітці, переносять у банк іншої.
- Перемога: обидві сітки розбиті, банки рівні, числа виконані, однакові за розміром не перекриваються. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: протягування по пунктирних ребрах — межі; права — «не межа»; центральну межу ввід ігнорує.
- puzz.link edit: New board W×H (W парне), числа з клавіатури; тест «Maximum number» перевіряє верхню межу числа (?).
- Папір: лінії поверх пунктиру.

## Вікна, меню, HUD
- `game-screen` (puzz.link): дві сітки з товстою центральною межею, числа, межі, `conflict-highlight` за Check (код помилки текстом).
- Кнопки: Check · Undo · Redo · Erase answer; Edit / Play (див. puzz-link).
- `custom-window` — New board (W парне, H).
- `help-window` — правила англ./япон.
- `end-screen` — розвʼязано.

## Фічі поза полем
- `undo`/`redo`, `auto-check` за кнопкою.
- `level-editor` + `share-code` — пазл кодується URL (puzz.link).

## Варіації й родичі
- **Double Choco** — конгруентні половини всередині одного блоку; тут — між двома сітками.
- **Fillomino** / **Shikaku** — поділ з числом-розміром на одній сітці.
- **Pentominous**, **LITS** — порівняння форм; тут порівнюється мультимножина форм двох полів.
- **Осі варіацій**: скільки сіток (1 / 2 / більше) · що спільне (набір форм / розміри / картинка) · заборона при накладанні (той самий розмір / та сама форма / будь-який збіг меж) · чи можна повертати сітки при накладанні.

## Цікавинки для курсу
- Поле з двох підсіток і фіксованою центральною межею (ввід ігнорує ребро) — 🌱.
- Порівняння мультимножин канонічних форм двох розбиттів — 🥉.
- Перевірка накладки: для кожної клітинки пари блоків (A, B) — розмір рівний → конфлікт — 📎.
- Генерація: розбиття A, перестановка того самого банку в B без збігів — 👑.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` · `piece-rotate-flip` (форма з точністю до поворотів/відбиттів) · `conflict-highlight` · `in-game-editor` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+twin-grid-bank` «Дві сітки з однаковим набором фігур» · game-logic/constraints · 🥉.
  - `+overlay-size-clash` «Заборона перекриття однакових за розміром при накладанні сіток» · game-logic/constraints · 📎.
  - `+no-dead-end-border` (пропоновано в Palisade), `+shape-identity-check` (пропоновано в LITS).

## Пропозиції до словників
- `+cond:same_shape(a, b)` — однакова форма з поворотами й відбиттями.
- `+cond:same_bank(grid_a, grid_b)` — мультимножини форм двох розбиттів рівні.
- `+cond:overlaps(a, b)` — при накладанні полів A і B мають спільну клітинку.
- `+cond:no_dead_end(borders)` — межа не обривається всередині області.
- `+axis:field=twin-grids` — кілька повʼязаних сіток в одному пазлі.

## Джерела
- ⭐ [puzz.link tachibk.js](https://puzz.link/js/pzpr-samples/tachibk.js) — правила (англ./япон.), коди `bkSizeGt`, `bkSizeLt`, `bankNe`, `ceOverlap`, `bdDeadEnd`, тести «Enforce even amount of columns», «Maximum number», «Don't draw over center grid border»; vol. 173.
- YouTube: [пошук](https://www.youtube.com/results?search_query=tachiawase+block+puzzle).

## Непевне
- (?) Єдине відкрите джерело — puzz.link; Nikoli-сторінки жанру нема, пошук (1 запит) нічого не дав.
- (?) Рік і автор: відомо лише «Puzzle Communication Nikoli vol. 173».
- (?) «Maximum number» — тест є, але яке саме обмеження (площа однієї сітки?) — не розшифровано.
- (?) `bdDeadEnd` тут запускається з опцією `skiprules` — можливо, правило глухих меж необовʼязкове.
- (?) Значення назви «Tachiawase» і чи є в ній зміст «накладання» — не перевірено.
