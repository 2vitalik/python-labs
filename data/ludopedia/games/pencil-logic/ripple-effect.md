---
title: Ripple Effect (Hakyuu Kouka)
slug: ripple-effect
aka: [Hakyuu Kouka, 波及効果, Hakyuu, Ripple, Хвильовий ефект]
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
year: 1998
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/ripple_effect/", best: true, note: "Nikoli: три правила, приклад «Sample → Progressing → Solution»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ripple_Effect_(puzzle)", note: "правила, Nikoli #73 (травень 1998), книжки"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/ripple.js", note: "pzpr.js: правила EN/JA, коди помилок bkDupNum/nmSmallGap/ceNoNum"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ripple+effect+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, undo-redo, import-open-formats, +irregular-regions, +region-1-to-n, +same-value-min-gap]
proposes: ["+cond:min_gap(value, line)", "+cond:region_values_1_to_n", "+card:region-1-to-n", "+card:same-value-min-gap"]
author: opus
date: 2026-11-09
---

# Ripple Effect — кожна кімната містить 1…k, а однакові числа N у рядку чи стовпці стоять не ближче ніж через N клітинок

## Суть
Прямокутна сітка розбита жирними лініями на «кімнати» (поліоміно); частину чисел дано. Гравець заповнює всі клітинки так, щоб кімната з k клітинок містила числа 1…k по одному. Друге правило — «хвиля»: якщо однакове число N повторюється в рядку чи стовпці, між ними має бути щонайменше N клітинок. Незвичне: обмеження відстані **залежить від значення** — велике число «відштовхує» свою копію далі.

## Поле і час
- Прямокутна сітка W×H, повністю розбита на кімнати довільної форми (поліоміно).
- Кімната з 1 клітинки — там завжди 1.
- Шари: межі кімнат і дані числа (незмінні) · числа гравця · кандидати (цифрова версія).
- Час статичний; хід = вписати/стерти число.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | число 1…k або порожньо | k — розмір її кімнати |
| Дане число | mark | n | закріплене |
| Кімната | zone | розмір k | містить кожне з 1…k рівно раз |
| Рядок / стовпець | zone | — | однакові N у ньому — на відстані > N |
| «Хвиля» числа N | zone | радіус N | N клітинок у кожен бік по рядку і стовпцю, де іншого N бути не може |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` + `input(key_digit)` → ТО `set_value(cell, n)` (цифрова версія).
- КОЛИ `input(pencil, cell)` → ТО `mark(cell, candidate n)` (цифрова версія).
- Кімната: ЯКЩО `custom: «кімната розміру k містить 1…k, кожне раз»` (`+cond:region_values_1_to_n`) → задоволена.
- КОЛИ `constraint_broken(room)` → ЯКЩО `custom: «число повторюється в кімнаті»` → ТО конфлікт (pzpr: `bkDupNum`).
- Хвиля: ЯКЩО `custom: «між двома N в одному рядку чи стовпці щонайменше N клітинок»` (`+cond:min_gap`) → задоволено.
- КОЛИ `constraint_broken(gap)` → ЯКЩО `custom: «два N ближче, ніж через N клітинок»` → ТО конфлікт (pzpr: `nmSmallGap`).
- КОЛИ `constraint_broken(fill)` → ЯКЩО `custom: «порожня клітинка»` → ТО не завершено (pzpr: `ceNoNum`).
- Обмеження значення: ЯКЩО `custom: «n > розміру кімнати»` → ТО `block` — таке число неможливе (pzpr: «between 1 and N, where N is the region size»).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(numbers)` → ТО `win`.
- Дедукція «1 у кімнаті-одиничці»: розмір 1 → число 1; дві 1 не можуть стояти поруч у рядку/стовпці.
- Дедукція «тінь хвилі»: кожне N викреслює N з N клітинок у кожен бік рядка і стовпця.
- Дедукція «останнє місце»: якщо в кімнаті для числа лишилась одна клітинка поза всіма хвилями цього числа — воно там.
- Перемога: усі клітинки заповнені, кімнати містять 1…k, хвилі не перетинаються. Поразки й рахунку нема.

## Керування і ввід
- Паперова гра: олівцем числа в клітинках.
- Цифрова версія (puzz.link): клік по клітинці + цифра; кандидати, перевірка відповіді з кодом помилки.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка з жирними кімнатами, дані числа, числа гравця, `pencil-marks`, `conflict-highlight` (два N занадто близько, дубль у кімнаті).
- `puzzle-select` — банк пазлів (книжки Nikoli, цифрова версія).
- `end-screen` / повідомлення «Розвʼязано» (цифрова версія).
- `help-window` — правила з прикладом.

## Фічі поза полем
- Книжки Nikoli: дві збірки на 2007 рік, друга — 4 жовтня 2007 (Wikipedia).
- puzz.link (pzpr): редактор і перевірка відповіді, URL-код пазла (`import-open-formats`), `undo`.
- `auto-check` з кодами помилок (pzpr).

## Варіації й родичі
- У сімʼї: [Fillomino](fillomino.md) (числа й регіони, але регіони малює гравець), [Sudoku](sudoku.md) / Jigsaw у [Sudoku variants](sudoku-variants.md) (нерегулярні кімнати з 1…9), [KenKen](kenken.md), [Heyawake](heyawake.md) (кімнати Nikoli), [puzz.link](puzz-link.md).
- **Осі варіацій**: правило відстані (≥ N / рівно N / по діагоналі теж) · вміст кімнати (1…k / задана множина) · дані числа (є / лише кімнати).

## Цікавинки для курсу
- Перевірка кімнати «1…k без повторів» через словник множин — 🌱.
- Перевірка хвилі: для кожного N сканувати N клітинок у 4 напрямках — 🌱.
- Підсвічування «тіні хвилі» при наведенні на число — 📎.
- Розвʼязувач: кандидати кімнат + викреслювання хвилями + backtracking — 🥈.
- Генератор: розбиття поля на поліоміно + заповнення з хвилями + мінімізація даних з перевіркою єдиності — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `level-bank` ↔ книжки · `undo-redo`, `import-open-formats` ↔ pzpr URL.
- Перевикористано: `+irregular-regions` ↔ кімнати-поліоміно.
- **Нема** → пропозиції карток:
  - `+region-1-to-n` «Регіон розміру k містить 1…k» · game-logic/constraints · 🌱 — Ripple Effect, Suguru/Tectonic, Jigsaw Sudoku (k = 9).
  - `+same-value-min-gap` «Однакові значення N на лінії — не ближче за N» · game-logic/constraints · 📎 · слот {gap: ≥N|=N, diagonal: no|yes}.

## Пропозиції до словників
- `+cond:min_gap(value, line)` — дві однакові клітинки зі значенням N на лінії розділені щонайменше N клітинками.
- `+cond:region_values_1_to_n` — регіон розміру k містить 1…k (уточнення `unique` + `region_size`).
- `+card:region-1-to-n`, `+card:same-value-min-gap` — див. мапу.

## Джерела
- ⭐ [Nikoli: Ripple Effect](https://www.nikoli.co.jp/en/puzzles/ripple_effect/) — три правила («Rooms», «consecutive numbers starting from 1», «space… equal to or larger than the value»), приклад у трьох кроках.
- [Wikipedia: Ripple Effect](https://en.wikipedia.org/wiki/Ripple_Effect_(puzzle)) — поліоміно, правила, Puzzle Communication Nikoli #73 (травень 1998), 波及効果, дві книжки до 2007.
- [pzpr.js: ripple](https://puzz.link/js/pzpr-samples/ripple.js) — правила EN/JA, коди помилок, Nikoli vol. 73.
- YouTube: пошук «ripple effect nikoli puzzle».

## Непевне
- (?) Автор жанру — не названий ні Nikoli, ні Wikipedia.
- (?) Suguru/Tectonic як родич (лише правило кімнат 1…k + заборона однакових сусідів) — з памʼяті.
- (?) Як цифрові версії Nikoli показують хвилю/помилки — не перевіряв; опис `game-screen` — за pzpr-кодами помилок.
