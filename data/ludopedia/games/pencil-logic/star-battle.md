---
title: Star Battle (Зоряна битва, Two Not Touch)
slug: star-battle
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
year: 2003
platforms: [paper, web, mobile]
links:
  - {kind: official, url: "https://www.gmpuzzles.com/blog/star-battle-rules-and-info/", best: true, note: "GMPuzzles: правила, історія (Hans Eendebak, WPC 2003), Cattle як предок, пазли для початківців"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/tag/starbattle+classic+mondaytuesday/", note: "найпростіші класичні Star Battle"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/tag/starbattle+variation-2/", note: "варіації Star Battle"}
  - {kind: play, url: "https://www.krazydad.com/twonottouch/", note: "Krazydad: 1★/2★/3★, NYT «Two Not Touch»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/starbattle.js", note: "puzz.link: правила, тести вводу, коди помилок"}
  - {kind: other, url: "https://en.wikibooks.org/wiki/Puzzles/Shading", note: "Wikibooks: правила 2★ разом з іншими пазлами зафарбовування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=star+battle+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, level-bank, daily-puzzle, import-open-formats, +undo-redo, +dot-mark, +irregular-regions, +no-adjacent-check, +region-quota, +auto-dot-neighbors, +input-scheme-toggle]
proposes: ["+cond:count_in", "+trigger:pattern(adjacent8)", "+ui:quota-indicator", "+card:region-quota", "+card:auto-dot-neighbors"]
author: opus
date: 2026-11-02
---

# Star Battle — по N зірок у кожному рядку, стовпці й області, і жодні дві не торкаються

## Суть
Квадратна сітка поділена на неправильні області (зазвичай стільки, скільки рядків). Гравець ставить зірки так, щоб у кожному рядку, кожному стовпці й кожній області було рівно N зірок (1, 2 або 3), і щоб жодні дві зірки не торкались — навіть по діагоналі. Чисел у клітинках нема: уся інформація — у формі областей. Незвичне: три накладені розбиття поля (рядки, стовпці, області) з однаковою квотою дають «бухгалтерську» дедукцію — якщо K областей цілком лежать у K рядках, решта цих рядків порожня.

## Поле і час
- Квадратна сітка n×n (класика WPC — 10×10, 2★ (?)); n областей неправильної форми з товстими межами.
- Сусідство для заборони дотику — 8-зв'язне (сторони й кути).
- Шари клітинки: область (незмінна) · стан гравця: порожньо / зірка / крапка «тут не зірка».
- Квота N вказана над сіткою (puzz.link: «number at the top of the grid»).
- Час статичний; хід = поставити/зняти зірку чи крапку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | стан empty / star / dot | приймає зірку чи крапку |
| Зірка | mark | — | рахується в рядок, стовпець і область; 8 сусідів мають бути без зірок |
| Крапка | mark | — | позначка гравця «не зірка»; на перевірку не впливає |
| Рядок / стовпець | zone | квота N | рівно N зірок |
| Область | zone | форма, квота N | рівно N зірок; товста межа |
| Квота N | static | 1 / 2 / 3 | показана над сіткою; одна на весь пазл |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, star)`; повтор → `unmark(cell)` (puzz.link: циклювання за схемою `use` (?)).
- КОЛИ `input(right_click|right_drag, cells)` → ТО `mark(cells, dot)`.
- КОЛИ `adjacent8(star, star)` → ТО `constraint_broken(no_touch)`, обидві підсвічуються (puzz.link `starAround`).
- КОЛИ `constraint_broken(region_quota)` — ЯКЩО `count_in(region, star, >, N)` → ТО конфлікт області (`bkStarGt`); ЯКЩО `<` при перевірці → `bkStarLt`.
- КОЛИ `constraint_broken(line_quota)` — ЯКЩО `count_in(row|col, star, !=, N)` → ТО конфлікт лінії (`lnStarNe`).
- КОЛИ `after(mark(star))` → ТО `custom: «автокрапки в 8 сусідах і в заповнених рядку/стовпці/області»` — допомога в частині застосунків (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукції: область з 1–2 клітинок фіксує зірку; блок 2×2 містить ≤ 1 зірку (звідси «розбити область на 2×2» → оцінка максимуму); K областей усередині K рядків → решта цих рядків без зірок; сусіди зірки — крапки.
- Перемога: квоти рядків, стовпців, областей виконані, зірки не торкаються. Поразки й рахунку нема (час — у застосунках).

## Керування і ввід
- Типово: клік — зірка, правий клік / drag — крапки; тач — тап циклює порожньо → зірка → крапка (?).
- puzz.link: тести показують протягування лівою й правою кнопкою по рядку клітинок; кнопка «Check» з кодом помилки.
- Krazydad / NYT «Two Not Touch»: інтерактив для телефонів і планшетів; iOS-застосунок Star Battle Go.
- Undo/redo, очистити відповідь.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами областей, квота N над полем, `conflict-highlight` (дотик зірок, переповнена область/лінія), `timer-elapsed` (?).
- `+ui:quota-indicator` — квота «★×N» над сіткою; у частині застосунків — підсвітка заповнених ліній (?).
- `puzzle-select` — книги Krazydad (1–100 за складністю), GMPuzzles за днями тижня (понеділок–вівторок = легкі).
- `help-window` — правила й приклад.
- `editor-window` — puzz.link edit mode (межі областей, квота).
- `end-screen` — пазл розвʼязано.
- Переходи: puzzle-select → game-screen → Check → повідомлення / end-screen.

## Фічі поза полем
- `auto-check` (за кнопкою або миттєво), `undo`/`redo`.
- `puzzle-bank` + `difficulty-presets` (Krazydad: книги за складністю; NYT: easy/medium щодня — `daily-puzzle`).
- `level-editor`, `share-code` (puzz.link URL).
- Друковані книги (GMPuzzles: «Star Battle», «Star Battle 2» JinHoo Ahn) — без цифрових фіч.

## Варіації й родичі
- Квота: **1★** (малі сітки, вступ), **2★** (класика WPC), **3★** (великі сітки).
- Варіації GMPuzzles: зміни форм областей, додаткові числові підказки (?); **Cattle** (Tim Peeters) — предок: області й заборона дотику, але без однакових квот рядків, з підказками зовні, як Battleships.
- Родичі: задача n ферзів (одна «фігура» на рядок/стовпець), «7 Queens» Krazydad (ферзі замість зірок), LinkedIn **Queens** — 1★ з кольоровими областями (?), Norinori, Battleships, Tents.
- **Осі варіацій**: квота (1/2/3/змінна) · заборона дотику (4 / 8 / нема) · які розбиття (рядки+стовпці+області / лише області) · форма поля (квадрат / гекс / тор) (?).

## Цікавинки для курсу
- Підрахунок зірок у трьох розбиттях (рядки, стовпці, області) — 🌱; одна функція `count_in(zone)`.
- 8-сусідство «не торкаються» — 🌱 (картка `+no-adjacent-check`, слот 8).
- Автокрапки навколо зірки й у заповнених зонах — 📎 (допомога інтерфейсу як інкрементне правило).
- Генератор областей (розбити сітку на n звʼязних шматків) + розстановка зірок + перевірка унікальності — 👑.
- Розвʼязувач: квоти як задача точного покриття / SAT з кардинальністю — 🥇.
- Режим 1★ як задача n ферзів з областями (backtracking) — 🥉.

## Мапа на каталог
- Є: `markup-validity` ↔ дотик/переповнення · `completion-detection`, `satisfy-constraints` · `cell-click` · `unique-puzzle-generation`, `level-solver`, `difficulty-levels`, `difficulty-rating` ↔ книги за складністю · `level-bank` · `daily-puzzle` ↔ NYT · `import-open-formats` ↔ puzz.link URL.
- Перевикористано: `+undo-redo`, `+dot-mark`, `+irregular-regions` (з sudoku-variants), `+no-adjacent-check`, `+input-scheme-toggle` (з Hitori).
- **Нема** → пропозиції карток:
  - `+region-quota` «Рівно N обʼєктів у кожній зоні» · game-logic/constraints · 🌱 · слот {n, zones: rows|cols|regions}.
  - `+auto-dot-neighbors` «Автомітки неможливих клітинок» · interface/input · 📎 · слот {rules: neighbors|full-zone}.

## Пропозиції до словників
- `+cond:count_in` — кількість сутностей виду в зоні (рядок/стовпець/область) порівняно з N; уточнення глобального `count`.
- `+trigger:pattern(adjacent8)` — два обʼєкти одного виду торкаються сторонами або кутами.
- `+ui:quota-indicator` — показ квоти N на зону над сіткою.
- `+card:region-quota`, `+card:auto-dot-neighbors` — див. мапу.

## Джерела
- ⭐ [GMPuzzles: Star Battle Rules and Info](https://www.gmpuzzles.com/blog/star-battle-rules-and-info/) — правила, Hans Eendebak, WPC 2003 (Арнем), Cattle Тіма Петерса.
- [GMPuzzles: легкі класичні](https://www.gmpuzzles.com/blog/tag/starbattle+classic+mondaytuesday/) і [варіації](https://www.gmpuzzles.com/blog/tag/starbattle+variation-2/).
- [Krazydad: Two Not Touch](https://www.krazydad.com/twonottouch/) — Jim Bumgardner, NYT, 1★/2★/3★, 7 Queens, Star Battle Go.
- [puzz.link starbattle.js](https://puzz.link/js/pzpr-samples/starbattle.js) — правила плеєра, коди `starAround`, `bkStarGt`, `bkStarLt`, `lnStarNe`.
- [Wikibooks: Puzzles/Shading](https://en.wikibooks.org/wiki/Puzzles/Shading) — правила 2★.
- YouTube: пошук «star battle puzzle how to solve».

## Непевне
- (?) Статті Wikipedia «Star Battle» нема (404); історія — лише з GMPuzzles.
- (?) Розміри класики (10×10 2★, 14×14 3★) — з памʼяті.
- (?) LinkedIn Queens як 1★-варіант — не знайшов джерела у Вікіпедії.
- (?) Точна поведінка puzz.link для лівої кнопки (цикл зірка → крапка) і автокрапки в застосунках — не перевірено.
- (?) Які саме додаткові підказки у варіаціях GMPuzzles — сторінка лише лінкує.
