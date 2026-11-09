---
title: Easy as ABC (ABC End View)
slug: easy-as-abc
aka: [ABC End View, Buchstabensalat, Last Man Standing, Geometrie, "Легко як ABC"]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/easyasabc.js", best: true, note: "puzz.link: правила EN/JP, коди помилок nmDupRow / nmSightNe / nmMissRow"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Abc-End-View/index.htm", note: "Janko: правила DE/EN/JP, назви, 5 варіантів, 630 пазлів 3×3–8×8"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzprjs"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=easy+as+abc+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, level-rating, import-open-formats, in-game-editor, +latin-square, +empty-cells-in-latin, +first-seen-clue, +undo-redo, +seed-share]
proposes: ["+cond:first_seen", "+cond:duplicate_in_line", "+card:first-seen-clue", "+card:empty-cells-in-latin"]
author: opus
date: 2026-11-09
---

# Easy as ABC — у кожному рядку й стовпці по одній літері A…K, решта порожні; ззовні — перша видима літера

## Суть
Сітка N×N і діапазон літер (напр. A–C на 5×5): у кожен рядок і стовпець треба поставити кожну літеру рівно раз, а клітинок, що лишились, — порожні. Літера на краю поля каже, яку літеру першою побачиш, дивлячись у цей рядок/стовпець з цього боку (порожні клітинки пропускаються). Незвичне: латинський квадрат **з дірками** — позиції порожніх клітинок теж треба вивести, а підказка — про порядок, не про значення.

## Поле і час
- Квадратна сітка N×N; літер k < N, порожніх у кожній лінії N − k.
- Janko: 3×3 (3 пазли), 4×4 (27), 5×5 (320), 6×6 (147), 7×7 (87), 8×8 (46).
- Підказки — у рамці навколо поля (до 4N); частина літер може бути дана всередині (?).
- Шари: підказки рамки · літери гравця · позначка «порожньо» · кандидати (цифрова версія).
- Час статичний; хід = вписати/стерти літеру або позначку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | літера / порожньо / не визначено | одне значення |
| Літера | mark | ∈ діапазону A…k | рівно раз у рядку й стовпці |
| Позначка «порожньо» | mark | — | клітинка свідомо без літери (цифрова версія, ·/×) (?) |
| Підказка рамки | static | літера, сторона, лінія | перша непорожня клітинка з цього боку = ця літера |
| Рядок / стовпець | zone | N клітинок | містить кожну літеру рівно раз |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `set_value(cell, letter)` (перебір A…k → порожньо) (?).
- КОЛИ `input(key_letter)` → ТО `set_value(cell, letter)`; Backspace → `unmark(cell)`.
- КОЛИ `input(mark_empty, cell)` → ТО `mark(cell, empty)`.
- КОЛИ `constraint_broken(latin)` → ЯКЩО `custom: «літера повторюється в рядку чи стовпці»` (`+cond:duplicate_in_line`) → ТО конфлікт: «There are equal letters in a row or column» (nmDupRow).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `not custom: «перша непорожня з цього боку = літера підказки»` (`+cond:first_seen`) → ТО конфлікт: «The letter is not the closest» (nmSightNe).
- КОЛИ `constraint_broken(row_full)` → ЯКЩО `custom: «у лінії бракує літери діапазону»` → ТО конфлікт: «There are missing letters in a row or column» (nmMissRow).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: кожна лінія містить усі k літер по разу й усі підказки рамки виконані · Поразка: — · Рахунок: — (Janko — час розвʼязання в рейтингу складності).

## Керування і ввід
- puzz.link play: клік по клітинці + клавіатура для літери; окремий символ для «порожньо» (крапка / хрестик) (?).
- puzz.link edit: задати N, діапазон літер, підказки рамки й дані літери (?).
- Папір: вписати літеру або хрестик «порожньо»; кандидати олівцем.

## Вікна, меню, HUD
- `game-screen`: сітка, рамка з літерами-підказками, `conflict-highlight` на рядку/підказці з помилкою.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window` (схема вводу).
- `puzzle-select` — архів Janko (630 пазлів), сортування за датою/розміром/складністю.
- `help-window` — правила DE/EN/JP (Janko), EN/JP (puzz.link).
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko з рейтингом 1–8 (лише за часом розвʼязання, не за розміром); пазли з покроковим логічним шляхом позначені кольором.

## Варіації й родичі
- Janko-варіанти: **Second** (підказка = друга видима літера) · **Negative / Not-Seen** (літера, якої з цього боку *не* видно першою) · **No-Touch / Anti-Diagonal** (однакові не торкаються по діагоналі) · **Palindrome** (кожна літера двічі, лінія читається паліндромом, напр. ACBBCA; Ashu Gupta, 2010) · **Regional** (N регіонів по N клітинок, у кожному кожна літера раз); комбінації (Negative-Regional).
- Родичі: [Skyscrapers](skyscrapers.md) (підказка рамки про видимість), [Doppelblock](doppelblock.md) (латинський квадрат із дірками і підказкою рамки), [Sudoku](sudoku.md), [KenKen](kenken.md).
- **Осі варіацій**: що каже підказка (перша / друга / невидима) · дірки (так / ні) · додаткові зони (регіони, діагоналі) · повторення літер (раз / двічі).

## Цікавинки для курсу
- Перевірка латинського квадрата з порожніми клітинками — 🌱.
- Підказка «перша непорожня з боку»: прохід по лінії з чотирьох боків — 🌱.
- Варіанти Second / Negative як прапорці правила в одному перевіряльнику — 📎.
- Розвʼязувач: перелік розстановок k літер у N клітинок рядка, сумісних з двома підказками, і перетин зі стовпцями — 🥇.
- Генератор з єдиним розвʼязком і мінімумом підказок — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ повтори · `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks` · `conflict-highlight` · `level-bank`, `level-rating` ↔ архів Janko · `import-open-formats`, `in-game-editor` ↔ puzz.link edit.
- Перевикористано: `+latin-square`, `+undo-redo`, `+seed-share`.
- **Нема** → пропозиції карток:
  - `+first-seen-clue` «Підказка рамки: перше видиме значення» · game-logic/constraints · 🌱 — ABC, варіанти Second/Negative.
  - `+empty-cells-in-latin` «Латинський квадрат з порожніми клітинками» · game-logic/constraints · 📎 — ABC, Doppelblock.

## Пропозиції до словників
- `+cond:first_seen` — перше непорожнє значення в лінії з боку = X.
- `+cond:duplicate_in_line` — повтор значення в рядку/стовпці (повтор з KenKen, Skyscrapers).
- `+card:first-seen-clue`, `+card:empty-cells-in-latin` — див. мапу.

## Джерела
- ⭐ [puzz.link: easyasabc.js](https://puzz.link/js/pzpr-samples/easyasabc.js) — правила EN/JP, коди nmDupRow / nmSightNe / nmMissRow.
- [Janko: ABC End View](https://www.janko.at/Raetsel/Abc-End-View/index.htm) — правила, назви (Buchstabensalat, Geometrie, Last Man Standing), 5 варіантів, 630 пазлів за розмірами, рейтинг 1–8.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- YouTube: пошук «easy as abc puzzle how to solve».

## Непевне
- (?) Винахідник і перша публікація невідомі (Janko прямо так пише); `year: null`.
- (?) Схема вводу puzz.link (перебір кліком, символ «порожньо») — не перевіряв на живій сторінці.
- (?) Чи бувають дані літери всередині поля — у правилах не сказано.
