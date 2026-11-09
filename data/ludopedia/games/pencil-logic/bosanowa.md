---
title: Bosanowa (ボサノワ)
slug: bosanowa
aka: [ボサノワ, Босанова]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/bosanowa.js", best: true, note: "puzz.link: правила EN/JP, Puzzle Communication Nikoli vol.119, коди nmSumOfDiff / ceNoNum"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzprjs"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bosanowa+puzzle", note: "пошук"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, conflict-highlight, import-open-formats, in-game-editor, +irregular-board-shape, +neighbor-diff-sum, +undo-redo, +seed-share]
proposes: ["+cond:sum_of_diffs", "+card:neighbor-diff-sum", "+card:irregular-board-shape"]
author: opus
date: 2026-11-09
---

# Bosanowa — у кожен кружечок додатне число, що дорівнює сумі різниць із сусідами

## Суть
Поле — фігура з кружечків на квадратній сітці (не обовʼязково прямокутник); у кожен кружечок вписуєш додатне ціле число. Число мусить дорівнювати сумі модулів різниць між ним і кожним ортогональним сусідом-кружечком. Частина чисел дана. Незвичне: **локальна арифметична рівновага** — кожна клітинка «врівноважує» сусідів, а не рахує їх; одне число впливає на перевірку всіх чотирьох сусідів.

## Поле і час
- Квадратна сітка, де клітинки поля — лише кружечки; порожнє місце — не поле (форма довільна).
- Сусіди — лише ортогональні кружечки; кружечок на краю фігури має менше сусідів.
- Шари: форма поля · дані числа · числа гравця · кандидати (цифрова версія).
- Час статичний; хід = вписати/стерти число.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кружечок | mark | додатне ціле або порожньо | n = Σ |n − сусід| по ортогональних сусідах |
| Дане число | static | n | незмінне; бере участь у перевірці |
| Не-поле | static | — | не має числа, не рахується сусідом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, circle)` + `input(key_digit)` → ТО `set_value(circle, n)`; Backspace → `unmark(circle)`.
- КОЛИ `constraint_broken(balance)` → ЯКЩО `not custom: «n = сума |n − m| по всіх ортогональних сусідах m»` (`+cond:sum_of_diffs`) → ТО конфлікт: «Sum of the differences between the number and adjacent numbers is not equal to the number» (nmSumOfDiff).
- КОЛИ `constraint_broken(fill)` → ЯКЩО `custom: «кружечок без числа»` → ТО конфлікт (ceNoNum).
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідок правила: кружечок з одним сусідом мусить мати сусіда 0 або 2n, тобто 2n (числа додатні) (виведено з правила, не з джерела).
- Перемога: усі кружечки заповнені, рівновага в кожному · Поразка: — · Рахунок: —.

## Керування і ввід
- puzz.link play: клік по кружечку, число — клавіатурою або перебором кліком (?).
- puzz.link edit: малювання форми поля (кружечки) і даних чисел (?).
- Папір: вписати числа; типовий прийом — рівняння для кутових/кінцевих кружечків.

## Вікна, меню, HUD
- `game-screen`: поле з кружечків, числа, `conflict-highlight` для кружечка з порушеною рівновагою.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window` — вигляд поля (кружечки / клітинки) (?).
- `help-window` — правила EN/JP.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).

## Варіації й родичі
- Перша поява — Puzzle Communication Nikoli vol. 119.
- Родичі: [Kakuro](kakuro.md), [KenKen](kenken.md) (арифметика в клітинках), [Fillomino](fillomino.md) (число ↔ сусіди), [Ripple Effect](ripple-effect.md) (числа з відстанню) — інші арифметичні Nikoli.
- **Осі варіацій**: форма поля (прямокутник / довільна) · сусідство (4 / 8) · операція (сума різниць / сума / добуток).

## Цікавинки для курсу
- Перевірка рівноваги з урахуванням довільної форми поля — 🌱.
- Поле довільної форми як маска на сітці (рендер кружечків, сусідство лише всередині маски) — 📎.
- Розвʼязувач: обмежений перебір чисел (верхня межа виводиться з даних) + поширення обмежень — 🥇.
- Генератор: задати форму, згенерувати розвʼязок, лишити мінімум чисел — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `conflict-highlight` · `import-open-formats`, `in-game-editor` ↔ puzz.link.
- Перевикористано: `+undo-redo`, `+seed-share`.
- **Нема** → пропозиції карток:
  - `+neighbor-diff-sum` «Число = сума різниць із сусідами» · game-logic/constraints · 🌱 — сестра `neighbor-count-clue`.
  - `+irregular-board-shape` «Поле довільної форми (маска)» · levels/format · 📎.

## Пропозиції до словників
- `+cond:sum_of_diffs` — значення = Σ |значення − сусід| по сусідах.
- `+card:neighbor-diff-sum`, `+card:irregular-board-shape` — див. мапу.

## Джерела
- ⭐ [puzz.link: bosanowa.js](https://puzz.link/js/pzpr-samples/bosanowa.js) — правила EN/JP, Nikoli vol. 119, коди nmSumOfDiff / ceNoNum.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — текст nmSumOfDiff.
- YouTube: пошук «bosanowa puzzle».

## Непевне
- (?) Рік виходу Nikoli vol. 119 і автор жанру — не знайшов; `year: null`.
- (?) Перемикач вигляду поля і схема вводу puzz.link — з власних знань.
- (?) Чи дозволена верхня межа чисел (у правилах — лише «додатне»).
