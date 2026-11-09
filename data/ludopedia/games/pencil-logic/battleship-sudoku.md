---
title: Battleship Sudoku (Судоку «Морський бій»)
slug: battleship-sudoku
aka: [Battleships Sudoku, Судоку-морський бій]
family: pencil-logic
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2006
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.gmpuzzles.com/blog/category/sudoku/battleship-sudoku/", best: true, note: "GM Puzzles: категорія жанру, 5 пазлів (Snyder 2013, Fikes 2013 «No Radar», Yürekli 2022), стандартні правила"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/battleship-sudoku-rules-and-info/", note: "правила й історія: Thomas Snyder, 2006, блог The Art of Puzzles; приклад «Easy as Pi?»; формат відповіді"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/2022/06/sunday-stumper-battleship-sudoku-by-serkan-yurekli/", note: "Sunday Stumper (тема Dominoes): правила дослівно"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/2013/07/from-the-foxgers-den-39-battleship-sudoku/", note: "варіант No Radar — без зовнішніх лічильників"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battleship+sudoku", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, pencil-marks, cell-click, keyboard-controls, line-sum-clue, multi-cell-size, +latin-square, +fleet-placement, +no-touch-placement, +outside-clues, +constraint-overlay, +numbered-pieces, +given-is-sea]
proposes: ["+cond:duplicate_in_line", "+cond:no_touch8", "+cond:fleet_matches", "+card:numbered-pieces", "+card:given-is-sea"]
author: opus
date: 2026-11-09
---

# Battleship Sudoku — судоку, у якому ще треба сховати флот кораблів із цифрами на палубах

## Суть
Гібрид двох паперових жанрів в одній сітці 9×9. Як у [Sudoku](sudoku.md): у кожній клітинці цифра 1–9, без повторів у рядку, стовпці й блоці. Як у пазлі Battleships (Bimaru, див. [Battleship](../hidden-deduction/battleship.md)): у тій самій сітці треба розмістити заданий флот так, щоб кораблі не торкалися навіть кутами, а числа за краями показували, скільки палуб у рядку/стовпці. Сегменти кораблів пронумеровані, і ці цифри мусять узгоджуватись із судоку; дані цифри в сітці — це «море». Жанр вигадав Thomas Snyder (2006).

## Поле і час
- Квадратна сітка 9×9 з блоками 3×3 (стандарт GM Puzzles); на сторінці правил — «number from the indicated range», тож бувають інші розміри (?).
- Над сіткою / збоку — зображення флоту: кораблі різної довжини з цифрами на сегментах (?).
- За краями — «радар»: числа палуб у рядку/стовпці; у варіанті No Radar їх нема.
- Шари: дані цифри (море) · цифри гравця · розмітка кораблів (палуба / море) · pencil marks.
- Час статичний; хід = вписати цифру або позначити клітинку кораблем/морем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | цифра 1–9; палуба / море | одна цифра; або частина корабля, або море |
| Дана цифра | static | 1–9 | завжди море, не може бути палубою |
| Корабель | piece | довжина k, цифри сегментів | прямий відрізок 1×k; можна повертати; цифри стають цифрами судоку |
| Палуба (сегмент) | mark | цифра | належить рівно одному кораблю |
| Флот | supply | набір кораблів | усі кораблі розміщені рівно раз |
| Радар | static | N | у рядку/стовпці рівно N палуб |
| Рядок / стовпець / блок | zone | 9 клітинок | цифри 1–9 без повторів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` + `input(key_digit)` → ТО `set_value(cell, d)` (цифрова версія).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, ship | sea)` (цифрова версія) (?).
- КОЛИ `constraint_broken(sudoku)` → ЯКЩО `custom: «цифра повторюється в рядку, стовпці чи блоці»` (`+cond:duplicate_in_line`) → ТО конфлікт.
- КОЛИ `constraint_broken(touch)` → ЯКЩО `custom: «палуби різних кораблів сусідять стороною чи кутом»` (`+cond:no_touch8`) → ТО конфлікт.
- КОЛИ `constraint_broken(radar)` → ЯКЩО `custom: «палуб у рядку/стовпці ≠ числу радара»` → ТО конфлікт.
- КОЛИ `constraint_broken(given_sea)` → ЯКЩО `occupied(cell, given)` and `state(cell, ship)` → ТО конфлікт («Numbers inside the grid at the start should be treated like 'seas'»).
- КОЛИ `constraint_broken(fleet)` → ЯКЩО `custom: «розміщені кораблі не збігаються з флотом за довжинами й цифрами»` (`+cond:fleet_matches`) → ТО конфлікт.
- Поворот: ЯКЩО `custom: «корабель лежить горизонтально чи вертикально, у будь-якому з двох напрямків»` → ТО порядок цифр читається відповідно (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «море з даних»: кожна дана цифра — море, тож рядок з багатьма даними має мало місця для палуб; радар 0 — увесь рядок море.
- Дедукція «цифри палуб»: корабель з цифрами {a, b, c} може стати лише туди, де жодна з цих цифр ще не стоїть у тих самих рядку/стовпці/блоці.
- Дедукція «ореол»: навколо поставленої палуби 8 сусідів — море або той самий корабель.
- Дедукція «найдовший першим»: найдовший корабель має найменше місць — його ставлять першим, як у Bimaru.
- Перемога: валідне судоку + флот розміщено за радаром без дотиків. Поразки й рахунку нема; у змаганнях — рядок відповіді «A, B».

## Керування і ввід
- Папір: вписати цифри; обвести або заштрихувати палуби; крапкою позначити море.
- GM Puzzles: розвʼязок перевіряється введенням рядка A і стовпця B як 9-значних кодів («517649328,742365891» у прикладі).
- Цифрова версія: два режими — цифра / корабель; pencil marks для кандидатів.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка 9×9 з блоками, радар за краями, панель флоту з галочками розміщених кораблів, `pencil-marks`, `conflict-highlight`.
- `help-window` — правила (сторінка GM Puzzles).
- `puzzle-select` — категорія GM Puzzles за датами.
- `+ui:fleet-status` — повтор з Battleship: які кораблі вже стоять.
- Переходи: категорія → пазл → ввід відповіді → перевірка.

## Фічі поза полем
- GM Puzzles: `puzzle-bank` за категорією; рядок відповіді як `auto-check` (`+feature:answer-code`) (?).
- Книга Thomas Snyder на основі жанру (сторінка правил: «the basis for his first book of puzzles»).

## Варіації й родичі
- **No Radar** (Grant Fikes, 2013) — без зовнішніх лічильників.
- Тематичні флоти: Dominoes (лише двопалубні), Even Steven («the fleet has only certain kinds of numbers»), Four Islands, Twister.
- Родичі: [Sudoku](sudoku.md), [Sudoku variants](sudoku-variants.md) (накладання обмежень), [Battleship](../hidden-deduction/battleship.md) (пазл Bimaru), [Star Battle](star-battle.md) (заборона дотику), [Tents](tents.md).
- **Осі варіацій**: чи є радар · цифри на кораблях (задані / вільні) · дотик кутами (заборонено / дозволено) · розмір сітки й діапазон цифр.

## Цікавинки для курсу
- Валідатор судоку + валідатор флоту окремими функціями, що працюють на одній сітці — 📎; добра вправа на композицію перевірок.
- Розпізнати кораблі з розмітки палуб (компоненти 4-звʼязності, кожна — пряма) і порівняти з флотом як мультимножину — 📎.
- Перевірка «без дотиків кутами» між різними компонентами — 🌱.
- Розвʼязувач: перебір розміщень флоту з перевіркою цифр палуб проти кандидатів судоку — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `pencil-marks`, `cell-click`, `keyboard-controls` · `line-sum-clue` ↔ радар · `multi-cell-size` ↔ кораблі різної довжини.
- Перевикористано: `+latin-square`, `+fleet-placement`, `+no-touch-placement` (Battleship), `+outside-clues`, `+constraint-overlay` (Sudoku variants).
- **Нема** → пропозиції карток:
  - `+numbered-pieces` «Фігури з цифрами, що входять у сітку» · game-logic/constraints · 📎 · слот {rotate: yes|no} — Battleship Sudoku, доміно-пазли.
  - `+given-is-sea` «Дана підказка забороняє фігуру в клітинці» · game-logic/constraints · 🌱 — Battleship Sudoku.

## Пропозиції до словників
- `+cond:duplicate_in_line` — повтор з KenKen/Easy as ABC.
- `+cond:no_touch8` — дві фігури не мають спільної сторони чи кута.
- `+cond:fleet_matches` — множина розміщених фігур = заданому набору.
- `+card:numbered-pieces`, `+card:given-is-sea` — див. мапу.
- Повтор: `+ui:fleet-status` (Battleship); `+feature:answer-code` — перевірка розвʼязку рядком відповіді (GM Puzzles).

## Джерела
- ⭐ [GM Puzzles: Battleship Sudoku](https://www.gmpuzzles.com/blog/category/sudoku/battleship-sudoku/) — «standard Battleship Sudoku rules», 5 пазлів: Snyder (Dr. Sudoku Prescribes #44, #46, #48, лютий 2013), Fikes (No Radar, липень 2013), Yürekli (Sunday Stumper, червень 2022).
- [GM Puzzles: rules and info](https://www.gmpuzzles.com/blog/battleship-sudoku-rules-and-info/) — правила, Snyder 2006, The Art of Puzzles, перша книга автора, приклад «Easy as Pi?», формат відповіді.
- [Sunday Stumper (Yürekli)](https://www.gmpuzzles.com/blog/2022/06/sunday-stumper-battleship-sudoku-by-serkan-yurekli/) — правила: «cannot be placed in adjacent cells that share an edge or corner», дані цифри = море.
- [Foxger's Den #39 (No Radar)](https://www.gmpuzzles.com/blog/2013/07/from-the-foxgers-den-39-battleship-sudoku/) — варіант без радара.

## Непевне
- (?) Чи цифри палуб задані на картинці флоту, чи вільні: текст «Each ship segment is numbered, and these numbers must also fit into a valid Sudoku solution» і тема Even Steven радше кажуть «задані»; картинок не бачив.
- (?) Склад стандартного флоту (скільки кораблів якої довжини) — у тексті нема, лише на зображеннях.
- (?) Розміри, відмінні від 9×9 («indicated range»).
- (?) Назва й рік першої книги Snyder.
- (?) Розмітка палуб у цифровій версії — GM Puzzles дає PDF/картинку, інтерактиву не бачив.
