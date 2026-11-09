---
title: Look-Air (るっくえあ)
slug: look-air
aka: [るっくえあ, Rukkuea, Lookair, Sichtlinie]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Rukkuea/index.htm", best: true, note: "Janko: правила EN/DE/JA, 100 пазлів 6×6–14×14 (грати й друкувати), родич Tasukuea"}
  - {kind: other, url: "https://puzz.link/rules.html?lookair", note: "puzz.link: правила з прикладом (рендер JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/lookair.js", note: "правила EN/JA, Nikoli vol. 136, коди помилок, тест вводу чисел"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/lookair.js", note: "код pzprjs: перевірка квадратів і «погляду»"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzpr"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=look-air+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, neighbor-count-clue, conflict-highlight, keyboard-controls, dot-mark, in-game-editor, import-open-formats, undo-redo, level-bank, +cell-shade-toggle, +input-scheme-toggle, +group-shape-check, +same-size-sight-ban]
proposes: ["+cond:is_square", "+card:group-shape-check", "+card:same-size-sight-ban"]
author: opus
date: 2026-11-09
---

# Look-Air — зафарбуй квадрати так, щоб два однакові квадрати ніколи не «бачили» один одного по прямій

## Суть
Гравець зафарбовує клітинки так, щоб кожна група чорних була суцільним квадратом (1×1, 2×2, 3×3…). Числа рахують чорні клітинки в «хресті» з п'яти клітинок — сама клітинка з числом і чотири її сусіди. Головне правило: два квадрати однакового розміру не можуть стояти в одному рядку чи стовпці з самими білими клітинками між ними, хіба що погляд перекриває квадрат іншого розміру.

## Поле і час
- Прямокутна сітка; Janko — 6×6…14×14.
- Сусідство ортогональне: група = 4-звʼязна; квадрати торкаються лише кутами (Janko: «may touch diagonally»).
- «Погляд» — уздовж рядка чи стовпця, який займає квадрат, крізь білі клітинки до першої чорної або краю поля.
- Шари: числа 0–5 (незмінні) · стан клітинки: невідома / чорна / крапка (біла).
- Звʼязності білих правило **не** вимагає (у pzpr нема такої перевірки).
- Час статичний; хід = зафарбувати / позначити / стерти клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | невідома / чорна / крапка | гравець перемикає стан |
| Число | static | N = 0…5 | чорних у хресті з 5 клітинок рівно N; сама клітинка з числом може бути чорною |
| «?»-підказка | static | — | число невідоме (редактор pzpr: цикл «?, 0…5, порожньо») |
| Квадрат | zone | сторона k | 4-звʼязна група чорних = заповнений k×k |
| Лінія погляду | zone | рядок/стовпець | білі клітинки між двома квадратами; перший чорний на шляху зупиняє погляд |
| Край поля | static | — | обриває погляд без помилки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права кнопка — `mark(cell, dot)`; повтор — `unmark(cell)` (схема `use` puzz.link) (?).
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО помилка (`brNoShade`: «There are no shaded cells on the board»).
- КОЛИ `constraint_broken(square)` → ЯКЩО `custom: «група чорних не є заповненим квадратом: ширина ≠ висота або площа ≠ ширина × висота»` (`+cond:is_square`) → ТО `set_state(group, error)` (`csNotSquare`: «A group of shaded cells is not a square»).
- КОЛИ `line_of_sight(square_a, square_b)` → ЯКЩО `same(square_a, square_b, size)` → ТО `set_state(square_a, error)`, `set_state(square_b, error)` (`lookairBC`: «Two squares of the same size can see each other»).
- КОЛИ `constraint_broken(cross_count)` → ЯКЩО `not count(shaded in cross5(cell), ==, N)` → ТО `set_state(cell, error)` (`nmShade5Ne`: «…the number of shaded cells in the cell and the four adjacent cells»).
- Квадрат іншого розміру між двома однаковими: ЯКЩО `not same(blocker, square_a, size)` → погляд перекрито, помилки нема (JA-правило 4).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «0»: уся п'ятірка хреста біла.
- Дедукція «5»: клітинка і 4 сусіди чорні → вони в одному квадраті зі стороною ≥ 3.
- Дедукція «кути»: дві чорні клітинки, що торкаються лише кутом, належать різним квадратам; спільний бік зробив би групу не-квадратом.
- Дедукція «чергування»: у кожному рядку квадрати, що бачать один одного, мусять мати різні розміри — два 1×1 у рядку потребують між собою квадрата іншого розміру.
- Перемога: усі групи — квадрати, числа виконані, однакові квадрати не бачать один одного. Поразки й рахунку нема.

## Керування і ввід
- Play (puzz.link): режими `shade` / `unshade`; клік — фарба або крапка; схема кнопок `use` (як у Hitori) (?).
- Edit: клік по клітинці циклує «?, 0, 1…5, порожньо» лівою кнопкою вперед, правою назад (тест вводу pzpr); цифри з клавіатури.
- Janko: інтерактивний розвʼязувач — сірі клітинки фарбуються чорним або білим.
- Папір: зафарбувати клітинку, крапкою позначити білу.

## Вікна, меню, HUD
- `game-screen`: пунктирна сітка, числа, чорні клітинки, крапки, `conflict-highlight` — обидва квадрати однакового розміру, не-квадратна група, число з хибним хрестом.
- puzz.link — спільний інтерфейс ([puzz-link](puzz-link.md)): Check, Undo/Redo, Edit/Play, `help-window`, URL input/output, `settings-window` (схема вводу).
- `puzzle-select` — 100 пазлів Janko з сортуванням за датою, розміром і складністю.
- Переходи: puzzle-select → game-screen → Check → повідомлення помилки / розвʼязано.

## Фічі поза полем
- `auto-check` з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko (друк із розвʼязками); генератора не бачив (?).

## Варіації й родичі
- Janko відносить до «Flächenrätsel» поруч із **Tasukuea** (квадрати з числами-площами).
- Заборона «однакові не бачать одне одного» — як у [Light Up](light-up.md) (лампи не освітлюють одна одну), тут — з розміром як ключем.
- Хрест-лічильник із 5 клітинок — родич [Fill-a-Pix](fill-a-pix.md) (квадрат 3×3) і [Light Up](light-up.md) (4 сусіди).
- Форма групи як обмеження: [Shikaku](shikaku.md), [LITS](lits.md), [Statue Park](statue-park.md).
- **Осі варіацій**: форма груп (квадрат / прямокутник / будь-яка) · що забороняє погляд (однаковий розмір / будь-який) · хрест 5 чи 9 клітинок · чи потрібна звʼязність білих.

## Цікавинки для курсу
- «Група = квадрат» через рамку групи: `w == h and w * h == area` — 🌱.
- Хрест-лічильник із самою клітинкою — 🌱.
- Перевірка погляду: від кожного квадрата лише вгору й ліворуч, бо відношення симетричне (так у коді pzpr) — 📎.
- Повний валідатор із підсвіткою пари квадратів — 🥉; розвʼязувач (розміщення квадратів + пропагація хрестів) — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `dot-mark` · `neighbor-count-clue` ↔ хрест із 5 · `conflict-highlight` · `keyboard-controls` (числа в редакторі) · `in-game-editor`, `import-open-formats` · `undo-redo` · `level-bank` (Janko).
- Перевикористано: `+cell-shade-toggle`, `+input-scheme-toggle` (Hitori, Nurimisaki).
- **Нема** → пропозиції карток:
  - `+group-shape-check` «Кожна група зафарбованих має задану форму» · game-logic/constraints · 🌱 · слот {shape: square|rectangle|any}.
  - `+same-size-sight-ban` «Однакові обʼєкти не бачать один одного по прямій» · game-logic/constraints · 📎 · слот {key: size|any, blockers: other-objects} — Look-Air, Light Up.

## Пропозиції до словників
- `+cond:is_square` — група клітинок утворює заповнений квадрат.
- `+card:group-shape-check`, `+card:same-size-sight-ban` — див. мапу.

## Джерела
- ⭐ [Janko: Rukkuea](https://www.janko.at/Raetsel/Rukkuea/index.htm) — правила EN/DE/JA («Squares of the same size must not "see" each other», «may touch diagonally»), 100 пазлів, назви Look-Air / Sichtlinie, автор невідомий.
- [puzz.link rules: lookair](https://puzz.link/rules.html?lookair) — правила з прикладом (рендер JS).
- [pzpr-samples lookair.js](https://puzz.link/js/pzpr-samples/lookair.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 136», коди `brNoShade`, `csNotSquare`, `lookairBC`, `nmShade5Ne`.
- [pzprjs lookair.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/lookair.js) — `countDir5ShadedCell`, `checkSquareShade`, `checkLookair`, режими вводу.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.

## Непевне
- (?) Перша публікація: pzpr — Nikoli vol. 136; Janko — «möglicherweise» Nikoli, без номера. Рік не бачив; за квартальним виходом (Janko: № 163 — червень 2018) vol. 136 ≈ 2011.
- (?) Назва «Sichtlinie» — Janko пише «evtl.».
- (?) Призначення кнопок миші в play-режимі puzz.link (схема `use`).
