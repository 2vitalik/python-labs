---
title: Araf (相ダ部屋, Aidabeya)
slug: araf
aka: [Aidaheya, Aidabeya, 相ダ部屋, Араф, «Чистилище»]
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
year: 2007
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/araf.js", best: true, note: "puzz.link/pzpr: правила EN/JP, «?» як будь-яке число, коди помилок, тестові поля"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Araf/index.htm", note: "Janko: правила, походження (16-й JPC 2007 як 相ダ部屋), назва Araf від Serkan Yürekli, 120 пазлів"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок `.araf`"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=araf+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, edge-marking, conflict-highlight, level-bank, in-game-editor, import-open-formats, +undo-redo, +region-size-check, +input-scheme-toggle, +sum-between-clue, +two-clues-per-region, +wildcard-clue]
proposes: ["+cond:region_size", "+cond:clues_in(region, n)", "+cond:size_between", "+card:two-clues-per-region", "+card:wildcard-clue"]
author: opus
date: 2026-11-09
---

# Araf — розріж поле на області з рівно двома числами, площа кожної строго між ними

## Суть
У частині клітинок сітки стоять числа. Гравець проводить межі по лініях сітки й ділить усе поле на області. Кожна область містить рівно два числа, а її площа (у клітинках) строго більша за менше і строго менша за більше: A < площа < B. Незвичне: підказка — не розмір, а **інтервал**, і задають його два числа, яких треба ще й правильно спарувати.

## Поле і час
- Прямокутна сітка; межі проводяться по пунктирних лініях між клітинками.
- Клітинки: порожня · з числом · з «?» (будь-яке число).
- Кожна клітинка належить рівно одній області (Janko).
- Шари: числа (незмінні) · межі гравця · допоміжні хрестики на ребрах (?).
- Час статичний; хід = провести/стерти відрізок межі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | належить одній області |
| Число | static | N | одне з двох чисел своєї області; задає межу інтервалу |
| «?» | static | будь-яке N | рахується як число в області, межа інтервалу вільна |
| Межа (ребро) | mark | є / нема | ділить сусідні клітинки між областями |
| Область | zone | площа S, два числа A < B | A < S < B |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, edges)` → ТО `mark(edge, border)`; drag повторно — стерти (?).
- КОЛИ `constraint_broken(too_many)` → ЯКЩО `custom: «в області більше двох чисел»` (`+cond:clues_in(region, n)`) → ТО `set_state(region, error)` (`bkMoreThan2Num`: «An area has more than two numbers»).
- КОЛИ `constraint_broken(too_few)` → ЯКЩО `custom: «в області менше двох чисел»` → ТО `set_state(region, error)` (`bkLessThan2Num`).
- КОЛИ `constraint_broken(equal)` → ЯКЩО `custom: «площа дорівнює одному з чисел»` (`+cond:region_size`) → ТО `set_state(region, error)` (`bkArafEqual`: «An area is equal to a number»).
- КОЛИ `constraint_broken(small)` → ЯКЩО `custom: «площа менша за обидва числа»` → ТО `set_state(region, error)` (`bkArafTooSmall`).
- КОЛИ `constraint_broken(big)` → ЯКЩО `custom: «площа більша за обидва числа»` → ТО `set_state(region, error)` (`bkArafTooBig`).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «відрізок межі закінчується всередині поля, нічого не відокремлюючи»` → ТО `set_state(edge, error)` (`bdDeadEnd`: «There is a dead-end line»).
- Задоволена область: ЯКЩО `custom: «A < площа < B»` (`+cond:size_between`) → ТО область без помилки.
- «?»: ЯКЩО `occupied(cell, wildcard)` → ТО `custom: «число підбирається так, щоб інтервал виконався»`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «сусідні числа»: два числа, що різняться на 1 (або рівні), не можуть бути в одній області — між ними нема цілого.
- Дедукція «двійка»: число 2 можна спарувати лише з числом ≥ 4 у області площі 3…B−1; число 1 — з будь-яким B ≥ 3.
- Дедукція «відстань»: дві клітинки з числами в одній області мусять бути зʼєднані шляхом ≤ B − 1 клітинок; далекі числа не спаровуються.
- Дедукція «парування»: кожне число має рівно одного партнера — це паросполучення на графі допустимих пар.
- Перемога: усе поле розбите, кожна область — два числа й площа строго між ними. Поразки й рахунку нема.

## Керування і ввід
- Папір: обвести межі областей по лініях сітки.
- puzz.link play: drag по лініях — межа; хрестик на ребрі «тут не межа» (?).
- puzz.link edit: цифри в клітинках, «?» — окремий символ.
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка з пунктирними лініями, числа, межі гравця, `conflict-highlight` на області чи кінці межі.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window`.
- `help-window` — правила (pzpr EN/JP, Janko).
- `puzzle-select` — 120 пазлів Janko.
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko.

## Варіації й родичі
- Розбиття за числами: [Fillomino](fillomino.md) (число = площа), [Shikaku](shikaku.md) (одне число = площа прямокутника), [Double Choco](double-choco.md), [Palisade](palisade.md), [Pentominous](pentominous.md).
- «Між»: [Doppelblock](doppelblock.md) — сума між двома чорними; там інтервал позиційний, тут — числовий.
- **Осі варіацій**: скільки чисел на область (1 / 2 / N) · що задають числа (площу / межі інтервалу / суму) · строгість (строго між / включно) · форма областей (довільна / прямокутники).

## Цікавинки для курсу
- Розбиття поля за ребрами → області (flood fill по клітинках з урахуванням меж) — 🌱.
- Перевірка «два числа + площа строго між» з окремим кодом на кожну ваду — 🌱.
- Межа з тупиком: ступінь вершин графа меж — 📎.
- Граф допустимих пар чисел (різниця ≥ 2, досяжність) + паросполучення — 🥉.
- Розвʼязувач розбиття з відкатом — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `edge-marking` ↔ межі · `conflict-highlight` · `level-bank` (Janko) · `in-game-editor`, `import-open-formats` (puzz.link).
- Перевикористано: `+undo-redo`, `+region-size-check` (Fillomino), `+input-scheme-toggle`, `+sum-between-clue` (Doppelblock — родинна ідея «між»).
- **Нема** → пропозиції карток:
  - `+two-clues-per-region` «Область містить рівно N підказок» · game-logic/constraints · 🌱 · слот {n: 1|2} — Araf (2), Shikaku/Fillomino (1).
  - `+wildcard-clue` «Підказка "?" — будь-яке значення» · game-logic/constraints · 🌱 — Araf, багато жанрів pzpr.

## Пропозиції до словників
- `+cond:region_size` — повтор з Fillomino/Shikaku.
- `+cond:clues_in(region, n)` — в області рівно n підказок.
- `+cond:size_between` — площа строго між двома числами області.
- `+card:two-clues-per-region`, `+card:wildcard-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link araf.js](https://puzz.link/js/pzpr-samples/araf.js) — правила EN/JP («exactly two numbers», «between the two numbers, exclusive», «Question marks can be replaced by any number»), коди `bkMoreThan2Num`, `bkLessThan2Num`, `bkArafEqual`, `bkArafTooSmall`, `bkArafTooBig`, `bdDeadEnd`.
- [Janko: Araf](https://www.janko.at/Raetsel/Araf/index.htm) — походження: півфінал 16-го Japanese Puzzle Championship (2007) як 相ダ部屋; назва Araf (тур. «чистилище») від Serkan Yürekli для 19-го WPC у Польщі; 120 пазлів.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.

## Непевне
- (?) Рік 19-го WPC (Польща) — не перевіряв; автор оригінального 相ダ部屋 невідомий.
- (?) Ввід межі в play-режимі puzz.link (drag по лініях, хрестики) — за аналогією з іншими жанрами розбиття.
- (?) Дедукція «двійка» й «відстань» — виведені з правил, у джерелах не бачив.
- ⭐ — сторінка `puzz.link/rules.html?araf` віддала порожній шаблон, тому ⭐ — файл правил pzpr.
