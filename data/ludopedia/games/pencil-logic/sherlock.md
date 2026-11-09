---
title: Sherlock (Everett Kaser)
slug: sherlock
aka: [Sherlock — The Game of Logic, Kaser Sherlock, Шерлок]
family: pencil-logic
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 1991
platforms: [DOS, Windows, Mac, Android, iOS]
links:
  - {kind: official, url: "https://www.kaser.com/sherwin.html", best: true, note: "Everett Kaser: суть, розміри 3–8 × 3–8 (36), набори A/B, «what if», графіка, ціна, платформи"}
  - {kind: other, url: "https://retro-replay.com/db/dos/sherlock-2", note: "DOS 1991: 36 блоків, вертикальні підказки й 5 горизонтальних типів"}
  - {kind: other, url: "https://www.kaser.com/top.php", note: "каталог ігор Kaser (Games Pack 1)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=everett+kaser+sherlock+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, unique-puzzle-generation, difficulty-levels, theme-select, field-size-picker, gui-render, +attribute-grid, +relation-clues, +what-if-mode, +clue-done-mark, +undo-redo]
proposes: ["+cond:same_slot", "+cond:next_to", "+cond:left_of", "+cond:between", "+effect:eliminate", "+role:clue-card", "+feature:what-if", "+card:what-if-mode"]
author: opus
date: 2026-11-09
---

# Sherlock — сітка картинок 6×6: з графічних підказок визнач, у якому стовпці стоїть кожна

## Суть
Комп'ютер бере кілька рядків картинок (обличчя, будинки, числа, фрукти, літери…), у кожному рядку — свій набір, і перемішує позиції в рядку. Гравець бачить порожню сітку і набір **графічних підказок** про відношення позицій: у тому ж стовпці / не в тому ж; поруч / не поруч; лівіше; між / не між. Мета — визначити стовпець кожної картинки, викреслюючи неможливе. По суті — [Zebra Puzzle](zebra-puzzle.md) з піктограмами й генератором.

## Поле і час
- Сітка рядки × стовпці: класика — 6 × 6 (36 картинок, DOS); у версії 7 — від 3 до 8 рядків і від 3 до 8 стовпців (36 розмірів); мобільна — 4×4, 5×5, 6×6.
- Рядок = категорія картинок; стовпець = позиція; кожна картинка рядка — рівно в одному стовпці.
- У кожній клітинці — набір дрібних кандидатів-картинок свого рядка (?).
- Підказки — поза сіткою: вертикальні (стосуються одного стовпця) і горизонтальні (взаємне розташування стовпців).
- Час статичний; хід = викреслити кандидата або закріпити картинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | рядок, стовпець, множина кандидатів | звужується до однієї картинки |
| Картинка | mark | рядок (категорія) | рівно в одному стовпці свого рядка |
| Кандидат | mark | картинка | викреслений / можливий |
| Вертикальна підказка | static | 2 картинки, так/ні | у тому ж стовпці / не в тому ж |
| Горизонтальна підказка | static | 2–3 картинки, тип | поруч · не поруч · лівіше · між · не між |
| Рядок | zone | N картинок | перестановка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(right_click, candidate)` → ТО `custom: «кандидата викреслено»` (`+effect:eliminate`) (?).
- КОЛИ `input(left_click, candidate)` → ТО `set_value(cell, picture)` (картинку закріплено) (?).
- КОЛИ `after(set_value)` → ТО `custom: «ця картинка зникає з кандидатів інших клітинок рядка»` (?).
- КОЛИ `custom: «у клітинці лишився один кандидат»` → ТО `set_value(cell, picture)` (?).
- КОЛИ `input(right_click, clue)` → ТО `mark(clue, done)` — підказку прибрано як використану (?).
- Вертикальна: ЯКЩО `custom: «a і b в одному стовпці»` (`+cond:same_slot`) / `not` — те саме з запереченням.
- «Поруч»: ЯКЩО `custom: «стовпці a і b сусідні, бік не вказано»` (`+cond:next_to`); «не поруч» — заперечення.
- «Лівіше»: ЯКЩО `custom: «стовпець a лівіше b»` (`+cond:left_of`) (одразу чи будь-де — (?)).
- «Між»: ЯКЩО `custom: «b між a і c, у сусідніх стовпцях»` (`+cond:between`) (?); «не між» — заперечення.
- КОЛИ `custom: «викреслено правильну картинку»` → ТО `custom: «помилка»` (реакція гри — (?)).
- КОЛИ `all_constraints_met` → ТО `win`.
- Набір A: розвʼязується простою логікою, підказки по одній; набір B — треба комбінувати підказки або «what if».
- Перемога: усі картинки на своїх стовпцях · Поразка: — (?) · Рахунок: час розвʼязання (?).

## Керування і ввід
- Миша: ліва кнопка — закріпити кандидата, права — викреслити (огляд 1990-х, через пошук) (?).
- Права кнопка по підказці — сховати використану (?).
- «What if» — режим припущення: спробувати і відкотитись (Kaser).
- Мобільна: тач, масштаб і панорамування на великих полях.

## Вікна, меню, HUD
- `game-screen`: сітка з кандидатами, панель вертикальних підказок, панель горизонтальних підказок.
- `settings-window`: розмір (рядки × стовпці), набір A/B, набори картинок і графіка інтерфейсу.
- `skin-select` — вибір image set (Player-Game Graphics + Player-User Interface).
- `help-window` — пояснення типів підказок (help-файл).
- `end-screen` — розвʼязано, час (?) · `stats-window` (?).

## Фічі поза полем
- `custom-difficulty` — 36 розмірів поля; набори A/B як `difficulty-presets`.
- `+feature:what-if` — тимчасові припущення з відкатом.
- `hint` — підказка була «від початку» (через пошук) (?); `undo` (?).
- `theme-select` / `custom-skins` — набори картинок (версія 7 не бере старі).
- Демо з обмеженою кількістю пазлів; повна — $19.95; входить у Games Pack 1.

## Варіації й родичі
- Версії: DOS (1991) → Windows → Sherlock 7 (поточна; набір A = пазли версії 6) → Mac / Android / iOS.
- Інші ігри Kaser тієї ж логіки — Baker Street, Mrs. Hudson, Inspector Lestrade, Watson's Map, Mycroft's Map (?) за змістом.
- Родичі: [Zebra Puzzle](zebra-puzzle.md) (текстові підказки), Einstein-клони для ПК/мобільних.
- **Осі варіацій**: розмір рядки × стовпці · набір типів підказок (4 / 5 горизонтальних, з запереченнями) · подача (піктограми / текст) · складність (одна підказка за раз / комбінації / припущення).

## Цікавинки для курсу
- Сітка кандидатів з викресленням і автозакріпленням єдиного — 📎.
- Предикати підказок (той самий, поруч, лівіше, між + заперечення) над перестановками — 🌱.
- Генератор: випадкова розстановка → набір підказок до єдиності → прибрати зайві — 🥇.
- Класифікація складності A/B: чи розвʼязується «по одній підказці» (поширення без комбінацій) — 🥇.
- «What if»: гілка стану з відкатом — 📎.
- Підказки як піктограми (рендер відношень картинками) — 🥉.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click` · `unique-puzzle-generation` ↔ генератор Kaser · `difficulty-levels` ↔ A/B · `field-size-picker` ↔ 36 розмірів · `theme-select` ↔ image sets · `gui-render`.
- Перевикористано: `+attribute-grid`, `+relation-clues` (з Zebra), `+clue-done-mark`, `+undo-redo`.
- **Нема** → пропозиції карток:
  - `+what-if-mode` «Режим припущення з відкатом гілки» · game-logic/history · 📎 — Sherlock; споріднено з `undo-redo`.

## Пропозиції до словників
- `+cond:same_slot`, `+cond:next_to`, `+cond:left_of` — повтор із Zebra Puzzle.
- `+cond:between` — b між a і c (сусідні позиції, порядок будь-який).
- `+effect:eliminate` — викреслити кандидата.
- `+role:clue-card` — підказка як окрема сутність поза полем.
- `+feature:what-if` — тимчасове припущення з відкатом.
- `+card:what-if-mode` — див. мапу.

## Джерела
- ⭐ [Everett Kaser: Sherlock](https://www.kaser.com/sherwin.html) — «The Game of Logic», розміри 3–8 × 3–8, набори A/B, «what if», image sets, $19.95, Mac 11.5+, Android/iOS.
- [Retro Replay: Sherlock (DOS)](https://retro-replay.com/db/dos/sherlock-2) — DOS 1991, 36 блоків, вертикальні + «is next to / is not next to / is left of / is between / is not between».
- [Kaser: каталог ігор](https://www.kaser.com/top.php) — Sherlock у Games Pack 1, сусідні ігри.
- YouTube: пошук «everett kaser sherlock gameplay».

## Непевне
- (?) Рік: Retro Replay — DOS 1991, черга куратора — 1992.
- (?) Ліва/права кнопка, сховати підказку, система підказок — з анотації пошуку, першоджерело (help-файл) не відкрилось (404).
- (?) «Лівіше» — одразу чи будь-де; «між» — сусідні стовпці чи будь-які.
- (?) Вигляд клітинки з дрібними кандидатами і реакція на помилкове викреслення — з власних знань.
- (?) Рахунок/час/статистика — сторінка Kaser не описує.
