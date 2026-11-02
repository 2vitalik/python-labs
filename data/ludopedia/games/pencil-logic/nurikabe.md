---
title: Nurikabe (Нурікабе, Islands in the Stream)
slug: nurikabe
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
year: 1991
platforms: [paper, web, mobile]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/nurikabe/", best: true, note: "Nikoli: 5 правил, приклад «Sample → Progressing → Solution»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nurikabe_(puzzle)", note: "правила, історія (renin, Nikoli №33, 1991), техніки, NP-повнота"}
  - {kind: play, url: "https://puzz.link/rules.html?nurikabe", note: "puzz.link: плеєр з автоперевіркою (сторінка правил рендериться JS)"}
  - {kind: official, url: "https://puzz.link/js/pzpr-samples/nurikabe.js", note: "текст правил puzz.link і тест вводу (ліва/права кнопка)"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/nurikabe", note: "Conceptis: правила, техніки, туторіал, інтерактив"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/nurikabe/techniques", note: "техніки розвʼязання з картинками"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nurikabe+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, reachability-check, unique-puzzle-generation, level-solver, level-bank, import-open-formats, +cell-shade-toggle, +dot-mark, +region-size-check, +no-2x2-check]
proposes: ["+trigger:pattern(block2x2)", "+cond:connected", "+cond:region_size", "+ui:dot-mark", "+card:cell-shade-toggle"]
author: opus
date: 2026-11-02
---

# Nurikabe — зафарбуй «море» так, щоб острови з числами мали точний розмір

## Суть
На прямокутній сітці частина клітинок містить числа. Гравець зафарбовує клітинки (стіна/море) так, щоб незафарбовані утворили острови: у кожному острові рівно одне число, і воно дорівнює розміру острова. Усе зафарбоване — одна звʼязна стіна без квадратів 2×2. Ядро — бінарне рішення на клітинку, але перевіряються **глобальні** властивості (звʼязність, розмір компонент), а не локальні суми — саме це робить Нурікабе класичним прикладом flood-fill у пазлі.

## Поле і час
- Прямокутна сітка (у Nikoli — від 10×10 до 20×36 (?)); сусідство ортогональне (4 напрямки) і для островів, і для моря.
- Шари клітинки: число (незмінне) · стан гравця: невідомо / зафарбовано / крапка («точно біла»).
- Час статичний, хід = зміна стану однієї клітинки.
- Нема зовнішніх підказок і регіонів — уся інформація в числах і трьох глобальних правилах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | стан unknown / shaded / dot | перемикається кліком; у розвʼязку — shaded або white |
| Число (підказка) | static | N ≥ 1 | завжди біле; = розмір свого острова |
| Зафарбована клітинка (стіна, «море») | mark | — | усі разом — одна 4-звʼязна компонента; без 2×2 |
| Крапка | mark | — | позначка гравця «тут біле»; у перевірці = біле (?) |
| Острів | zone | розмір, кількість чисел | 4-звʼязна компонента білих; рівно одне число, розмір = число |
| Квадрат 2×2 («басейн») | zone | 4 клітинки | заборонений, якщо всі чотири зафарбовані |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not cell(x, number)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)`. На числі — `block`.
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (puzz.link: ліва кнопка — фарба, права — крапка; повтори циклюють стан).
- КОЛИ `pattern(group(shaded, 2×2))` → ТО `constraint_broken(no_pool)`, `custom: «підсвітити басейн»`.
- КОЛИ `constraint_broken(sea_connected)` — зафарбоване розпалось на ≥2 компоненти → ТО конфлікт (перевірка flood fill).
- КОЛИ `constraint_broken(island_one_number)` — острів без числа або з двома → ТО конфлікт острова.
- КОЛИ `constraint_broken(island_size)` — `custom: «розмір компоненти ≠ число»` → ТО конфлікт; ЯКЩО `custom: «острів закритий стіною й уже завеликий/замалий»` → підсвітка одразу (?).
- КОЛИ `input(check)` → ТО `message(перше порушене правило)` — puzz.link показує текст помилки й підсвічує клітинки (?).
- КОЛИ `all_constraints_met` → ТО `win`, `message(«Complete!»)`.
- Перемога: звʼязне море, без 2×2, кожен острів — одне число й точний розмір. Поразки й рахунку нема (лише час у додатках).

## Керування і ввід
- Ліва кнопка — зафарбувати, права — крапка (puzz.link); drag протягує той самий стан по кількох клітинках (?).
- Тач-режим: один тап циклює unknown → shaded → dot → unknown (?).
- Крапки — «олівець» Нурікабе: розмітка впевненості без впливу на перевірку.
- Undo/redo, «очистити відповідь» (`ansclear` у puzz.link), перемикач play/edit у puzz.link (редактор того ж жанру).

## Вікна, меню, HUD
- `game-screen`: сітка + кнопки Check/Undo/Redo/Clear + `timer-elapsed` (puzz.link (?)) + `conflict-highlight` порушених клітинок.
- `help-window` — правила жанру (puzz.link rules, Nikoli «Sample / Progressing / Solution»).
- `editor-window` — puzz.link edit mode: числа з клавіатури, експорт URL.
- `puzzle-select` — банк Conceptis/Nikoli за розміром і складністю.
- `end-screen` — повідомлення про розвʼязання.
- Переходи: puzzle-select → game-screen → Check → (помилка) повідомлення / (ok) end-screen.

## Фічі поза полем
- `auto-check` (puzz.link — за кнопкою, з текстом порушеного правила), `undo`/`redo`, `level-editor` + `share-code` (пазл у URL puzz.link).
- `puzzle-bank` (Nikoli, Conceptis), `difficulty-presets` за розміром і технікою.
- Генерація: у Tatham-колекції Нурікабе нема (?) — генерація з унікальним розвʼязком нетривіальна.

## Варіації й родичі
- LITS, Mochikoro, Atsumari (гекс-сітка) — родичі за Wikipedia; Nuribou, Cave, Yin-Yang, Heyawake — інші зафарбовування з глобальною звʼязністю.
- Відкидання правила звʼязності або правила 2×2 дає варіанти, теж NP-повні.
- **Осі варіацій**: що звʼязне (чорне / біле / обидва) · заборонені форми (2×2 / сусідство / тетраміно) · що несе число (розмір острова / видимість / кількість сусідів).

## Цікавинки для курсу
- Перемикання стану клітинки ліва/права кнопка (фарба/крапка) — 🌱.
- Звʼязність моря через flood fill / BFS — 📎 (картка `reachability-check`).
- Компоненти островів: розмір і кількість чисел у кожній — 📎 (той самий BFS, інша метрика).
- Заборона 2×2 — 🌱, але гарна вправа на вікно 2×2 по сітці.
- Розвʼязувач правилами (обидва сусіди двох чисел → стіна; закритий острів → стіна навколо; L-стіна → біле в куті) — 🥇.
- Генератор з унікальним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ конфлікти · `completion-detection`, `satisfy-constraints` ↔ перемога · `cell-click` ↔ фарба/крапка · `reachability-check` ↔ звʼязність моря · `unique-puzzle-generation`, `level-solver` · `level-bank` · `import-open-formats` ↔ puzz.link URL / pzprv3.
- **Нема** → пропозиції карток:
  - `+cell-shade-toggle` «Перемикання фарба / крапка / порожньо» · interface/input · 🌱.
  - `+dot-mark` «Позначка "точно біле"» · interface/input · 🌱 (родич pencil-marks для бінарних пазлів).
  - `+region-size-check` «Розмір компонент і одна підказка на компоненту» · game-logic/constraints · 📎.
  - `+no-2x2-check` «Заборонений шаблон 2×2» · game-logic/constraints · 🌱 · слот {shape}.

## Пропозиції до словників
- `+trigger:pattern(block2x2)` — нове значення для `pattern(shape)`: заборонений квадрат.
- `+cond:connected` — набір клітинок одного стану утворює одну компоненту.
- `+cond:region_size` — розмір компоненти порівняно з числом.
- `+ui:dot-mark` — крапка «біле» в бінарних пазлах (окремо від `pencil-marks`).
- `+card:cell-shade-toggle` — див. мапу.

## Джерела
- ⭐ [Nikoli: Nurikabe](https://www.nikoli.co.jp/en/puzzles/nurikabe/) — 5 правил і покроковий приклад.
- [Wikipedia: Nurikabe](https://en.wikipedia.org/wiki/Nurikabe_(puzzle)) — renin, Nikoli №33 (березень 1991), техніки, NP-повнота навіть з числами 1 і 2.
- [puzz.link rules](https://puzz.link/rules.html?nurikabe) і [pzpr-samples/nurikabe.js](https://puzz.link/js/pzpr-samples/nurikabe.js) — правила плеєра й тести вводу (mouse left/right).
- [Conceptis: Nurikabe](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/nurikabe) + [техніки](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/nurikabe/techniques).
- YouTube: пошук «nurikabe puzzle how to solve».

## Непевне
- (?) Чи puzz.link рахує крапку як біле при перевірці й як саме підсвічує помилку — тексту повідомлень не бачив.
- (?) Розміри полів Nikoli і наявність таймера в puzz.link — з памʼяті.
- (?) Цикл станів на тачі й drag-фарбування — типова поведінка плеєрів, не перевірено.
