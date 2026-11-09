---
title: Tren
slug: tren
aka: [Parking, Паркінг, Вагончики]
family: pencil-logic
also: [push-slide]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/tren.js", best: true, note: "puzz.link: 6 правил EN/JP, коди помилок, пазл-приклад"}
  - {kind: other, url: "https://gmpuzzles.com/blog/2013/11/puzzle-robot-19-tren", note: "GM Puzzles (Serkan Yürekli): правила, «total possible movement», пазл"}
  - {kind: other, url: "https://puzz.link/rules.html?tren", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок tren"}
  - {kind: other, url: "https://cross-plus-a.com/html/cros7tren.htm", note: "Cross+A: сторінка жанру (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tren+puzzle+blocks", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [polyomino-placement, multi-cell-size, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, edge-marking, cell-click, in-game-editor, undo-redo, +mobility-clue]
proposes: ["+cond:slide_range(a, op, n)", "+card:mobility-clue"]
author: opus
date: 2026-11-09
---

# Tren — розстав вагончики 1×2 і 1×3 так, щоб число в кожному казало, на скільки він може відʼїхати

## Суть
На сітці стоять числа. Гравець обводить навколо кожного числа блок 1×2 або 1×3 (вагончик, авто на парковці). Горизонтальний блок їздить лише ліворуч-праворуч, вертикальний — вгору-вниз, і зупиняється об край поля чи інший блок. Число — загальна кількість клітинок, на які блок може зсунутись в обидва боки разом. Незвичне: підказка описує не фігуру, а її **свободу руху** серед інших — «Rush Hour навпаки».

## Поле і час
- Прямокутна сітка з числами (0 і більше).
- Шари: дані числа · межі блоків по ребрах (контур 1×2/1×3) · порожні клітинки (паркінг).
- Порожні клітинки дозволені: саме вони дають блокам місце для руху.
- Час статичний; рух блоків уявний — перевіряється лише його можливий обсяг.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | порожня або частина блока |
| Блок (вагончик) | object | 1×2 / 1×3, орієнтація | рухається лише вздовж довшої осі, не крізь блоки й край |
| Число | mark | N | лежить у блоці; N = сума можливих зсувів в обидва боки |
| Межа | mark | ребро | контур блока, проведений гравцем |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edges)` → ТО `mark(edge, border)` — контур блока (`edge-marking`) (?).
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «число не всередині блока 1×2 чи 1×3»` → ТО `set_state(number, error)` («A number is not contained inside a 1x2 or 1x3 block»).
- КОЛИ `constraint_broken(block)` → ЯКЩО `count(number, gt, 1)` → ТО `set_state(block, error)` («A block has multiple numbers»).
- КОЛИ `constraint_broken(block)` → ЯКЩО `custom: «блоки накладаються»` → ТО `set_state(block, error)`.
- КОЛИ `constraint_broken(number)` → ЯКЩО `custom: «сума вільних клітинок до упору в обидва боки вздовж осі ≠ N»` (`+cond:slide_range`) → ТО `set_state(block, error)` («A block cannot move in the correct number of spaces»).
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «проведена межа не прилягає до жодного блока»` → ТО `set_state(edge, error)` («A border is not adjacent to a block»).
- КОЛИ `constraint_broken(empty)` → ЯКЩО `not connected(empty_cells)` → ТО `set_state(board, error)` («The unused cells are divided») (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Рух блока — уявний: КОЛИ `custom: «перевірка числа»` → ЯКЩО `free(cell_ahead)` → ТО `slide(block, dir)`; упор — `block`; лічимо клітинки до упору в обидва боки.
- Дедукція «нуль»: блок з 0 затиснутий з обох кінців — краєм чи іншими блоками.
- Дедукція «довжина»: блок 1×3 з N у рядку довжини L мусить мати N ≤ L − 3; для 1×2 — N ≤ L − 2.
- Дедукція «взаємність»: блоки на одній лінії ділять ту саму порожнечу — зсув одного рахує ті ж клітинки, що й сусіда.
- Перемога: кожне число в окремому блоці 1×2/1×3, блоки не накладаються, свобода руху кожного дорівнює числу. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: межі блоків по ребрах між клітинками (?); тести вводу у файлі порожні — точних жестів не бачив.
- Edit mode: курсор + цифри — числа.
- Цифрова версія: undo/redo, перевірка за кнопкою; бажана кнопка «показати рух» для блока.

## Вікна, меню, HUD
- `game-screen`: сітка, числа, контури блоків, `conflict-highlight` після перевірки.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window`.
- `help-window` — правила жанру.

## Фічі поза полем
- `auto-check` за кнопкою (pzprjs).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла).
- Банк авторських пазлів: GM Puzzles (рубрика Puzzle Robot, Serkan Yürekli), Cross+A (?).

## Варіації й родичі
- Поза сімʼєю: [Rush Hour](../push-slide/rush-hour.md) — ті самі вагончики, але рух реальний і мета інша; [Train Shunting](../push-slide/train-shunting-puzzle.md).
- У сімʼї: [Rectangle-Slider](rectangle-slider.md) (зсуви панелей), [Shikaku](shikaku.md) (обвести прямокутник навколо числа), [Kuromasu](kuromasu.md) (число = скільки видно до перешкоди).
- Parking Lot (Serkan Yürekli) — додає блоки без чисел («привиди») і вимогу звʼязності порожніх клітинок; Gridunlocked — гібрид, де цифра рахує видимі порожні клітинки (за видачею пошуку).
- **Осі варіацій**: розміри блоків (1×2/1×3 / довільні) · число = сума обох боків / кожен бік · порожні клітинки звʼязні / ні · блоки без чисел (так / ні).

## Цікавинки для курсу
- Обчислення свободи руху: промінь уздовж осі блока до упору в обидва боки — 🌱.
- Перевірка розкладки: блоки не накладаються, по одному числу в кожному — 🌱.
- Анімація «посунути вагончик» у переглядачі розвʼязку — 📎.
- Розвʼязувач: для кожного числа ≤ 4 орієнтації×довжини×зсуви, пошук з відсіканням — 🥈.

## Мапа на каталог
- Є: `polyomino-placement` ↔ блоки 1×2/1×3 · `multi-cell-size` ↔ обʼєкт 1×2, рух уздовж осі · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `edge-marking`, `cell-click` · `in-game-editor`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+mobility-clue` «Число = на скільки обʼєкт може зсунутись до упору» · game-logic/constraints · 🌱 · слот {count: both|each}.

## Пропозиції до словників
- `+cond:slide_range(a, op, n)` — скільки клітинок сутність може проїхати до упору (сума напрямків уздовж осі).
- `+card:mobility-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: tren.js](https://puzz.link/js/pzpr-samples/tren.js) — 6 правил (блоки 1×2/1×3 без накладання, число в блоці, одне на блок, рух уздовж осі, не за край і не крізь блоки, число = на скільки рухається), коди помилок.
- [GM Puzzles: The Puzzle Robot #19 – Tren](https://gmpuzzles.com/blog/2013/11/puzzle-robot-19-tren) — «Each block is allowed to move in its long direction», число = «total possible movement», 2013.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок tren.
- YouTube: пошук «tren puzzle blocks».

## Непевне
- (?) Автор — пошук приписує жанр Shinichi Aoki, японська назва «паркінг»; сторінки-першоджерела не відкривав (`year: null`).
- (?) Помилка «The unused cells are divided» є в тестах puzz.link, але в англійських правилах вимоги звʼязності порожніх клітинок нема — можливо, опція чи варіант.
- (?) «Дані межі» в умові (код «A border is not adjacent to a block») — чи автор може задавати межі заздалегідь, не перевірено.
- (?) Як саме вводяться блоки в puzz.link — тести вводу порожні.
- (?) Parking Lot і Gridunlocked — зі сніпетів пошуку.
