---
title: Nansuke (Number Skeleton)
slug: nansuke
aka: [Number Skeleton, ナンスケ, Nanba Sukereton, Number Fill-In]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper (Puzzle Communication Nikoli)]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/nansuke/", best: true, note: "правила Nikoli (2 пункти), приклад, хід розвʼязку, відповідь; походження з «скелетних» пазлів"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/スケルトン_(パズル)", note: "словесний предок Skeleton / Criss Cross: правила, конкурсний варіант Nikoli 15×15"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fill-In_(puzzle)", note: "Fill-In: список слів за довжиною, числовий варіант"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/パズル通信ニコリのパズル一覧", note: "список пазлів Nikoli: ナンスケ● — зараз не друкується регулярно"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nansuke+number+skeleton+puzzle", note: "пошук"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, unique-puzzle-generation, game-screen, help-window, +number-list-fill, +word-list-checkoff, +entry-run-detection]
proposes: ["+cond:in_list", "+ui:fill-list", "+card:number-list-fill", "+card:entry-run-detection"]
author: opus
date: 2026-11-09
---

# Nansuke — кросворд без питань: впиши числа зі списку в скелет так, щоб усі перетини зійшлися

## Суть
Дано сітку-скелет із білих і чорних клітин і список чисел. Треба вписати всі числа зі списку в білі відрізки — зліва направо або згори вниз, по цифрі в клітину. Визначень нема: єдина інформація — довжини чисел і цифри на перетинах. Це числовий двійник словесного Skeleton / Fill-In; Nikoli виділила «скелетну» логіку в окремий тип.

## Поле і час
- Прямокутна сітка: білі клітини утворюють горизонтальні й вертикальні відрізки, чорні їх розділяють.
- Запис = максимальний відрізок білих клітин уздовж ряду (→) або стовпця (↓); перетин — спільна клітина двох записів.
- Поза полем: список чисел (на папері — під сіткою), який викреслюють у міру вписування.
- Статичний пазл без часу; один розвʼязок (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітина | terrain | порожня / цифра | приймає рівно одну цифру |
| Чорна клітина | static | — | розділяє записи |
| Запис (відрізок) | zone | довжина, напрям → / ↓ | має збігтися з одним числом списку |
| Цифра | mark | 0–9 (?) | спільна для обох записів, що перетинаються |
| Список чисел | zone | числа різної довжини | кожне вписати рівно раз; вписане викреслюється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «показати скелет і список чисел»`.
- КОЛИ `input(digit, cell)` → ЯКЩО `free(cell)` → ТО `mark(cell, digit)`.
- КОЛИ `input(erase, cell)` → ТО `unmark(cell)`.
- Запис: `custom: «кожен максимальний відрізок ≥ 2 білих клітин читається зліва направо або згори вниз як одне число»` (?).
- КОЛИ `constraint_broken(custom: «заповнений запис — число не зі списку або вже використане»)` → ТО `custom: «підсвітити конфлікт»` (цифрова версія).
- Перетин: `custom: «одна клітина — одна цифра, і вона входить в обидва записи»`.
- КОЛИ `input(strike list number)` → ТО `mark(list item, used)` — порада Nikoli: викреслюй використане.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «кожне число списку вписане рівно раз і всі білі клітини заповнені»` → ТО `win`.
- Перемога: усе вписано без конфліктів · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Папір: олівцем цифри в клітини, викреслення чисел у списку.
- Цифрова версія: клік по клітині + цифра з клавіатури; стрілки — перехід; клік по числу в списку — позначити використаним (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка, список чисел з викресленням (`fill-list`), `conflict-highlight`, `check-button`.
- `help-window`: два пункти правил і приклад.
- `puzzle-select`: збірка/журнал пазлів (як у книжках Nikoli) (?).

## Фічі поза полем
- `puzzle-bank` — журнал і збірки Nikoli; тип зараз позначений ● (не друкується регулярно).
- Цифрова версія — `auto-check`, `undo`, `pencil-marks` для кандидатів (?).

## Варіації й родичі
- Skeleton / Criss Cross / Kreuzgitter / Fill-In — те саме зі словами (часто тематичний список); конкурсний варіант Nikoli: вмістити 40 слів у 15×15 з максимумом сумарної вартості.
- [codeword.md](codeword.md) — числа замість літер у кросворді, ключ підстановки; [cross-figure.md](cross-figure.md) — числовий кросворд з арифметичними підказками; [dropquote.md](dropquote.md) — літери стовпця без визначень.
- Kakuro (pencil-logic) — числовий кросворд, де замість списку — суми.
- **Осі варіацій:** що вписується (слова / числа) · підказка (список / визначення / сума / нічого) · стартова підказка (одне слово вписано / нема) · список (за довжиною / суцільний).

## Цікавинки для курсу
- Виділення записів із маски сітки (відрізки ≥ 2 по рядах і стовпцях) — 🌱.
- Перевірка заповнення: кожен запис у мультимножині списку рівно раз — 🌱.
- Розвʼязувач: CSP з бектрекінгом, групування за довжиною, перетини як обмеження (exact cover) — 🥉.
- Генератор з унікальним розвʼязком: вибір чисел так, щоб перетини однозначно фіксували розміщення — 🥇.

## Мапа на каталог
- Є: `cell-click` · `keyboard-controls` · `satisfy-constraints` · `markup-validity` · `completion-detection` · `conflict-highlight` · `unique-puzzle-generation` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+number-list-fill` «Вписати всі елементи списку в скелет» · game-logic/constraints · 🌱 · слоти {list}.
  - `+word-list-checkoff` — див. словесні пазли корпусу; тут — числа списку.
  - `+entry-run-detection` «Записи = максимальні відрізки білих клітин» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:in_list` — значення є в заданому списку й ще не використане.
- `+ui:fill-list` — список елементів для вписування з викресленням.
- `+card:number-list-fill`, `+card:entry-run-detection`.

## Джерела
- ⭐ [Nikoli: Nansuke](https://www.nikoli.co.jp/en/puzzles/nansuke/) — правила, приклад з розвʼязком, поради, походження назви (Nanba Sukereton).
- [ja.wikipedia: スケルトン (パズル)](https://ja.wikipedia.org/wiki/スケルトン_(パズル)) — словесний Skeleton, конкурсний варіант Nikoli.
- [Wikipedia: Fill-In](https://en.wikipedia.org/wiki/Fill-In_(puzzle)) — словесний аналог, числовий варіант.
- [ja.wikipedia: список пазлів Nikoli](https://ja.wikipedia.org/wiki/パズル通信ニコリのパズル一覧) — ナンスケ з позначкою ●.

## Непевне
- (?) Чи може запис мати 1 клітину і чи дозволено 0 на початку числа — у правилах Nikoli не сказано.
- (?) Чи список згрупований за довжиною, як у Fill-In, — видно лише на зображенні прикладу.
- (?) Рік появи в Puzzle Communication Nikoli і єдиність розвʼязку (для Nikoli типова, але не названа).
- Цифрова версія від Nikoli не знайдена; вікна й фічі — «(цифрова версія)», як у паперових пазлів корпусу.
