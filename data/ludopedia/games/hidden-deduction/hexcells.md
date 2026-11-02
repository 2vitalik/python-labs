---
title: Hexcells / Hexcells Plus / Hexcells Infinite
slug: hexcells
family: hidden-deduction
also: [pencil-logic]
klass: puzzle
axes:
  field: hex
  time: static
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2014
platforms: [PC (Windows, macOS, Linux), iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hexcells", best: true, note: "правила: сині/чорні, лінійні суми, {} і -, три гри серії"}
  - {kind: steam, url: "https://store.steampowered.com/app/265890/Hexcells/", note: "перша гра, 19–20.02.2014"}
  - {kind: steam, url: "https://store.steampowered.com/app/271900/Hexcells_Plus/", note: "складніше продовження, 2014"}
  - {kind: steam, url: "https://store.steampowered.com/app/304410/Hexcells_Infinite/", note: "36 пазлів + генератор + користувацькі пазли, 01.09.2014"}
  - {kind: official, url: "https://github.com/oprypin/sixcells", note: "SixCells — редактор/плеєр рівнів Hexcells: формат .hexcells, солвер"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hexcells+Infinite+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [cell-click, satisfy-constraints, completion-detection, level-bank, level-select, level-unlock, unique-puzzle-generation, level-solver, in-game-editor, level-exchange, import-open-formats, level-from-txt, game-screen, background-music, +neighbor-count-clue, +line-sum-clue, +contiguity-clue, +no-guess-generation, +mistake-counter, +seeded-generator]
proposes: ["+cond:contiguous", "+effect:mark_safe", "+ui:mistake-counter", "+ui:line-clue", "+feature:seed-input", "+feature:perfect-run", "+card:line-sum-clue", "+card:contiguity-clue", "+card:mistake-counter", "+card:seeded-generator"]
author: opus
date: 2026-11-02
---

# Hexcells — гекс-сапер без вгадувань: знайди всі сині клітини за числами сусідів, ліній і позначками {n} / -n-

## Суть
Поле з гексагональних помаранчевих клітин; під кожною — синя (шукана) або чорна. Гравець лівим кліком відкриває клітину як синю, правим — як чорну; чорні й частина синіх показують числа, а за краєм поля стоять **лінійні підказки** — скільки синіх на стовпці/діагоналі. Позначки `{n}` і `-n-` додають топологію: сині стоять підряд або розірвано. Пазли ручні, кожен розвʼязний логікою; помилка не вбиває, лише рахується.

## Поле і час
- Гексагональна сітка довільної форми (рівень вирізає фігуру з поля 33×33 у форматі SixCells), дірки дозволені.
- Лінійні підказки — у трьох напрямках: вертикаль і дві діагоналі (−60°, 0°, +60°).
- Статичний пазл, без таймера; лічильники «Remaining» (лишилось синіх) і «Mistakes».
- Шари: прихований колір (синя/чорна) + відкрите число + лінійні підказки поза полем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина (помаранчева) | static | прихований колір | відкривається як синя або чорна |
| Синя клітина | mark | — | ціль; іноді з числом радіуса 2 |
| Чорна клітина з числом | mark | n = сині серед 6 сусідів | підказка; може мати `{n}` / `-n-` |
| Чорна клітина «?» | mark | — | без інформації (порожня підказка) |
| Синя клітина з числом | mark | n = сині в радіусі 2 (18 клітин) | «квітка» — підказка більшого радіуса |
| Лінійна підказка | zone | n, напрям, `{n}`/`-n-` | кількість синіх на прямій лінії клітин |
| Позначка `{n}` | mark | — | усі n синіх утворюють один неперервний ланцюжок |
| Позначка `-n-` | mark | — | n синіх **не** утворюють одного ланцюжка |
| Порожнє місце | static | — | дірка в полі; рве лінії й сусідство |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(mark_blue, c)` → ЯКЩО `cell(c, blue)` → ТО `reveal(c)`, `counter(remaining, -1)`; інакше `counter(mistakes, +1)`, клітина лишається закритою.
- КОЛИ `input(mark_black, c)` → ЯКЩО `cell(c, black)` → ТО `reveal(c)` з числом/«?»; інакше `counter(mistakes, +1)`, клітина закрита.
- Число на чорній: `adjacent_count(c, blue, ==, n)` по 6 гекс-сусідах.
- Число на синій: `custom: «кількість синіх у радіусі 2»` (18 клітин).
- Лінійна підказка: кількість синіх на лінії = n.
- `{n}` на чорній: сині серед 6 сусідів (по кільцю) утворюють один звʼязний ланцюжок; `{n}` на лінії: сині на лінії йдуть підряд (дірки лінію не рвуть (?)).
- `-n-`: сині **не** утворюють одного звʼязного ланцюжка (є щонайменше один розрив); для n ≤ 1 не вживається.
- КОЛИ `counter(remaining, ==, 0)` → ТО `win`, решта клітин відкривається, `window(end-screen)` з кількістю помилок.
- Перемога: знайдено всіх синіх. · Поразка: нема — помилки лише рахуються (і впливають на «perfect»). · Рахунок: кількість помилок (0 — ідеально).
- Гарантія дизайну: у кожному стані є клітина, яку можна вивести логікою, — вгадування не потрібне.

## Керування і ввід
- Ліва кнопка — «ця клітина синя», права — «ця клітина чорна»; помилкова дія відхиляється.
- Клік по лінійній підказці / числу — підсвітити його лінію або зону (?); тач на iOS.
- Нема прапорців-нотаток і undo: кожна дія — остаточна відповідь.

## Вікна, меню, HUD
- `game-screen`: поле, лінійні числа по краях, `remaining-counter` «Remaining», `mistake-counter` «Mistakes».
- `level-select` / `puzzle-select`: 6 груп по 6 рівнів (36 на гру), позначки пройдено / ідеально (?).
- `end-screen` рівня: «Level complete», помилки, перехід далі.
- Infinite: `mode-select` — 36 рівнів / Random Puzzle (генератор із seed-ом) / User Level (вставити рівень як текст із буфера (?)).
- `settings-window`: звук, музика, роздільність (?).
- Переходи: main-menu → level-select → game-screen → end-screen → level-select.

## Фічі поза полем
- `puzzle-bank` 36 ручних пазлів на кожну гру (Hexcells, Plus, Infinite), `level-unlock` групами (?).
- Infinite: генератор випадкових пазлів (`seed-display`/`seed-input` — 8 цифр (?)), підтримка користувацьких пазлів (`level-sharing` текстом).
- Спільнота: SixCells (редактор + плеєр + солвер на PuLP, формат `.hexcells` — 38 рядків UTF-8: заголовок, назва, автор, 2 рядки тексту, 33 рядки поля по 33 двосимвольні групи).
- Ембієнт-музика, кожен правильний клік — нота (?); Steam Achievements, Cloud.

## Варіації й родичі
- Hexcells → Hexcells Plus (важчі рівні, ті самі правила) → Hexcells Infinite (генератор, користувацькі рівні).
- Наступники: Tametsi (довільні графи, кольорові групи з лічильником), Patterna, hexceed, Globesweeper: Hex Puzzler; паперовий споріднений — Tentaizu.
- Осі варіацій: **сусідство** 8 (квадрат) / 6 (гекс) / радіус 2 / лінія; **тип підказки** кількість / кількість + топологія ({}/-) ; **помилка**: смерть / лічильник / відмова; **джерело пазлів**: ручні / генератор / користувацькі.

## Цікавинки для курсу
- Гекс-сітка: координати (axial/cube), 6 сусідів, лінії в трьох напрямках — 🥉.
- Перевірка `{n}` / `-n-` на кільці з 6 сусідів (циклічна звʼязність) і на лінії — 📎.
- Помилка не вбиває: лічильник помилок замість поразки — 🌱.
- Солвер обмежень (числа + лінії + {}/-) через перебір/ILP; перевірка «нема вгадувань» — 🥇.
- Генератор пазлів із seed-ом: генеруй розкладку, додавай/прибирай підказки, доки солвер розвʼязує без вгадувань — 👑 (якість «як ручна»).
- Рівень як текстовий формат (SixCells `.hexcells`) і обмін — 📎.

## Мапа на каталог
- Є: `cell-click` · `satisfy-constraints` · `completion-detection` · `level-bank` + `level-select` + `level-unlock` ↔ 36 рівнів групами · `unique-puzzle-generation` + `level-solver` ↔ генератор Infinite · `in-game-editor` + `level-exchange` + `import-open-formats` + `level-from-txt` ↔ SixCells і користувацькі рівні · `game-screen` · `background-music`.
- **Нема** → пропозиції карток:
  - `+line-sum-clue` «Підказка на лінії: скільки цілей у рядку/діагоналі» · game-logic/constraints · 📎 · слот {directions: 2|3}.
  - `+contiguity-clue` «Позначка {n}/-n-: цілі підряд чи розірвано» · game-logic/constraints · 📎.
  - `+mistake-counter` «Помилка рахується, а не вбиває» · game-logic/lose · 🌱 (протилежність `wrong-mark-lose`).
  - `+seeded-generator` «Генератор із seed-ом (повторити пазл)» · levels/generation · 🥉.

## Пропозиції до словників
- `+cond:contiguous` — сині в околі/на лінії утворюють один ланцюжок (для `{n}`; заперечення — `-n-`).
- `+effect:mark_safe` — відповісти «чорна»; на відміну від прапорця в сапері, перевіряється одразу.
- `+ui:mistake-counter` (вже є в ui-elements як `mistake-counter` — тут підтвердження вжитку) · `+ui:line-clue` — числа за краєм поля, привʼязані до лінії.
- `+feature:seed-input` — повторити згенерований пазл за кодом; `+feature:perfect-run` — окрема позначка «пройдено без помилок».

## Джерела
- ⭐ [Wikipedia: Hexcells](https://en.wikipedia.org/wiki/Hexcells) — правила (ліва/права кнопка, лінійні суми, `{}` і `-`), 36 рівнів, дати, Matthew Brown.
- [Steam: Hexcells](https://store.steampowered.com/app/265890/Hexcells/) — «ambient logic puzzle game», 19.02.2014.
- [Steam: Hexcells Plus](https://store.steampowered.com/app/271900/Hexcells_Plus/) — друга гра серії.
- [Steam: Hexcells Infinite](https://store.steampowered.com/app/304410/Hexcells_Infinite/) — 36 пазлів, random puzzle generator, user-made puzzles, 01.09.2014.
- [SixCells (GitHub)](https://github.com/oprypin/sixcells) — редактор/плеєр: лінії в 3 напрямках, формат `.hexcells`, солвер, «помилка лишає клітину закритою».
- YouTube: пошук «Hexcells Infinite gameplay».

## Непевне
- (?) Синя клітина з числом радіуса 2 — з памʼяті; у якій із трьох ігор зʼявляється вперше — не перевірено.
- (?) Формат seed-а Infinite (8 цифр) і ввід користувацького рівня з буфера обміну — з памʼяті.
- (?) Розблокування груп рівнів, «perfect»-позначки, нота на кожен клік — з памʼяті.
- (?) Чи дірки поля рвуть `{n}` на лінії — не перевірено.
- (?) Підсвітка лінії/зони кліком по підказці — з памʼяті.
- Wikipedia каже «six worlds of 36 levels» — читаю як 36 рівнів у 6 групах (а не 216).
