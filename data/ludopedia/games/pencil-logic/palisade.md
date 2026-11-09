---
title: Palisade (Five Cells, «Частокіл»)
slug: palisade
aka: [Five Cells, Частокіл, Пʼять клітинок]
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
platforms: [paper, PC, web, mobile]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/palisade.html", best: true, note: "Tatham: правила, миша й клавіатура, Custom (Width, Height, Region size), режими курсора"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/palisade.html", note: "грати в браузері (Tatham)"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/five_cells/", note: "Nikoli Five Cells: 4 правила, Sample → Progressing → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/fivecells.js", note: "puzz.link fivecells: правила, коди помилок, Puzzle Communication Nikoli vol. 133"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії Tatham: New, Restart, Undo, Redo, Solve, Save/Load"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=palisade+tatham+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, edge-marking, keyboard-controls, cell-click, connectivity-check, unique-puzzle-generation, level-solver, field-size-picker, undo-redo, redo, restart-level, seed-share, rule-variants, +border-count-clue, +equal-size-partition, +no-dead-end-border]
proposes: ["+cond:border_count(cell, n)", "+cond:no_dead_end(borders)", "+ui:edge-cross", "+ui:cursor-mode-toggle", "+window:params-dialog", "+window:game-id-dialog", "+card:border-count-clue", "+card:equal-size-partition", "+card:no-dead-end-border"]
author: opus
date: 2026-11-09
---

# Palisade — поріж сітку на області однакового розміру; число = скільки стінок навколо клітинки

## Суть
Прямокутна сітка з числами в деяких клітинках і заданим розміром області K. Гравець малює межі по ребрах сітки так, щоб уся сітка розпалась на звʼязні області рівно з K клітинок. Число в клітинці — скільки з її чотирьох сторін є межами (край поля теж рахується). Незвичне: підказка говорить не про вміст, а про **периметр** клітинки, тож дедукція йде через ребра, а не через значення. Nikoli називає жанр Five Cells (K = 5); у Tatham — Palisade з довільним K.

## Поле і час
- Квадратна сітка W×H; розв'язок — розмітка ребер, а не клітинок.
- Шари: клітинки з числами (незмінні) · ребра між клітинками (межа / «не межа» / невідомо) · зовнішня рамка (завжди межа, рахується в числах).
- Області — 4-звʼязні групи клітинок, відокремлені межами; розмір кожної = K.
- Nikoli: межа не може обриватись усередині блоку — кожен відрізок межі розділяє дві різні області.
- Час статичний; хід = змінити стан одного ребра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка з числом | static | N (0–4) | рівно N з чотирьох її сторін — межі (рамка рахується) |
| Порожня клітинка | mark | належність до області | без обмеження на межі; входить рівно в одну область |
| Ребро | mark | невідомо / межа / хрестик «не межа» | перемикається кліком; межі ріжуть сітку |
| Рамка поля | static | — | завжди межа; входить у підрахунок чисел |
| Область | zone | розмір = K | 4-звʼязна група, обмежена межами; рівно K клітинок |
| Розмір області K | static | параметр пазла | однаковий для всіх областей; W·H ділиться на K |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge)` → ТО `mark(edge, border)`; повтор → `unmark(edge)` (Tatham).
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, no_border)`; повтор — зняти хрестик.
- КОЛИ `input(ctrl_arrow, edge)` (full-grid курсор) або `input(enter, edge)` (half-grid) → ТО `mark(edge, border)`; Shift+стрілка / Space → `mark(edge, no_border)`; повтор дії = обернена дія.
- КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «кількість меж навколо клітинки ≠ N»` → ТО конфлікт (puzz.link `nmBorderNe`).
- КОЛИ `constraint_broken(size)` → ЯКЩО `region_size(region, > K)` → ТО конфлікт (`bkSizeGt5`); `< K` у замкненій області → `bkSizeLt5`.
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «відрізок межі обривається всередині області»` → ТО конфлікт (`bdDeadEnd`, Nikoli: «лінії не заходять у блок»).
- КОЛИ `all_constraints_met` (усі області рівно K, усі числа виконані, нема обірваних меж) → ТО `win`, `flash(completion)` (Tatham).
- Наслідки: число 4 можливе лише при K = 1; 0 — уся клітинка всередині області, всі сусіди в ній же; дві сусідні клітинки з 0 і 3 одразу задають, яка сторона межа.
- Дедукції: клітинка, яку відрізали від решти, «тягне» за собою рівно K−1 сусідів; кут поля з числом 2 — обидві сторони рамки вже межі, тож внутрішні сторони вільні; область, що досягла K, закривається межами з усіх боків.
- Перемога: розбиття на області розміру K, числа виконані. Поразки нема. Рахунку нема.

## Керування і ввід
- Tatham, миша: ліва — межа на ребрі, права — хрестик «не межа»; повторний клік знімає.
- Tatham, клавіатура: стрілки рухають курсор; **Preferences → Cursor mode**: full-grid (курсор по клітинках, Ctrl+стрілка ставить межу, Shift+стрілка — знімає) або half-grid (курсор по ребрах, Enter — межа, Space — зняти).
- Спільні дії Tatham: N — нова, U/Ctrl+Z — undo, R/Ctrl+R — redo, Restart, Solve, Save/Load.
- puzz.link (Five Cells): протягування лівою по точкових лініях — межі; права — хрестики (?).

## Вікна, меню, HUD
- `game-screen`: сітка з числами, межі, хрестики, `cursor` (клітинковий або реберний), `conflict-highlight` (?).
- Меню Game (Tatham): New · Restart · Specific… · Random Seed… · Load/Save · Undo/Redo · Solve · Preferences.
- Меню Type: пресети розміру; Custom… → `+window:params-dialog` (Width, Height, Region size).
- `+window:game-id-dialog` — Specific / Random Seed: ділитись пазлом.
- `settings-window` — Preferences: Cursor mode (full-grid / half-grid).
- `help-window` — розділ мануалу; Nikoli — сторінка правил з Sample / Progressing / Solution.
- Переходи: Type/Custom → новий пазл на `game-screen` → розвʼязано → спалах.

## Фічі поза полем
- `custom-difficulty`: Width, Height і **Region size** — сам розмір області як параметр генератора.
- `undo` ∞, `redo`, `restart-level` (відкочуваний), `auto-solve` (Solve у ланцюгу undo).
- `seed-display`, `seed-input`, `share-code` (Tatham game ID).
- `export-import` — Save/Load файлом з усією історією.

## Варіації й родичі
- **Five Cells** (Nikoli, Puzzle Communication Nikoli vol. 133) — K = 5, до 5 чисел у блоці.
- **Fillomino**, **Pentominous**, **Shikaku**, **Tentai Show** — інші «розбий на області» (див. відповідні файли); Pentominous теж ріже на пентаміно, але підказка — форма, а не периметр.
- **Nawabari**, **Four Cells** — родичі Nikoli з підказкою-периметром (?).
- **Осі варіацій**: розмір області (фіксований K / заданий числом / виводиться) · що рахує підказка (межі клітинки / клітинки області / форму) · чи рахується рамка · чи дозволені «глухі» межі.

## Цікавинки для курсу
- Модель «ребро як сутність»: масив горизонтальних і вертикальних ребер окремо від клітинок — 📎.
- Розбиття на області flood-fill'ом за межами + перевірка «усі = K» — 📎.
- Підрахунок меж навколо клітинки з урахуванням рамки — 🌱.
- Виявлення обірваної межі (кінець відрізка без продовження всередині області) — 🥉.
- Два режими клавіатурного курсора (клітинки / ребра) як налаштування — 📎.
- Генератор з гарантією єдиності й довільним K — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `edge-marking` (межі й хрестики) · `keyboard-controls` · `cell-click` · `connectivity-check` (області звʼязні) · `unique-puzzle-generation` · `level-solver` · `field-size-picker` · `undo-redo` / `redo` / `restart-level` · `seed-share` · `rule-variants` (Region size).
- **Нема** → пропозиції карток:
  - `+border-count-clue` «Число = кількість меж навколо клітинки (з рамкою)» · game-logic/constraints · 🌱.
  - `+equal-size-partition` «Розбиття на області однакового заданого розміру» · game-logic/constraints · 📎.
  - `+no-dead-end-border` «Межа не обривається всередині області» · game-logic/constraints · 🥉.

## Пропозиції до словників
- `+cond:border_count(cell, n)` — кількість сторін клітинки, що є межами (Palisade, Five Cells).
- `+cond:no_dead_end(borders)` — жоден відрізок межі не закінчується всередині області.
- `+ui:edge-cross` — хрестик «тут не межа» на ребрі.
- `+ui:cursor-mode-toggle` — курсор по клітинках чи по ребрах.
- `+window:params-dialog`, `+window:game-id-dialog` — Tatham Custom і Specific/Seed.

## Джерела
- ⭐ [Tatham: Palisade](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/palisade.html) — правила, керування, параметри, Preferences; внесок Jonas Kölker; оригінал — Nikoli «Five Cells».
- [Nikoli: Five Cells](https://www.nikoli.co.jp/en/puzzles/five_cells/) — 4 правила видавця (блоки по 5, число = лінії навколо з рамкою, до 5 чисел у блоці, лінії не заходять у блок).
- [puzz.link fivecells.js](https://puzz.link/js/pzpr-samples/fivecells.js) — правила, коди помилок `bkSizeLt5`, `nmBorderNe`, `bdDeadEnd`, `bkSizeGt5`; vol. 133.
- [Tatham: спільні дії](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — New/Restart/Undo/Redo/Solve/Save.
- YouTube: [пошук](https://www.youtube.com/results?search_query=palisade+tatham+puzzle).

## Непевне
- (?) Рік: ні Tatham, ні Nikoli не дають; відомо лише, що Five Cells зʼявився в Puzzle Communication Nikoli vol. 133.
- (?) Підсвітка помилок у Tatham Palisade — у мануалі не описана; у puzz.link є за кнопкою Check.
- (?) Чи вимагає Tatham Palisade відсутності глухих меж, як Nikoli, — у мануалі не сказано (можливо, розвʼязок з такою межею неможливий за побудовою).
- (?) Nawabari і Four Cells як родичі — з памʼяті, не перевіряв.
- (?) Керування puzz.link для fivecells — за загальною схемою puzz.link, не за тестами жанру.
