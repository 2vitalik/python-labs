---
title: Hidato (Хідато)
slug: hidato
aka: [Hidoku, Number Snake, Snakepit, Jadium, Numbrix, Beehive Hidato, Хідато]
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
platforms: [paper, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hidato", best: true, note: "правила, автор Gyora Benedek, форми поля, Numbrix/Jadium, техніки Naked/Hidden Single"}
  - {kind: official, url: "https://www.hidato.com/", note: "офіційний сайт (вміст сторінки не прочитався)"}
  - {kind: other, url: "https://inkl.com/news/can-you-solve-it-is-beehive-hidato-the-new-sudoku", note: "Guardian «Can you solve it?» про beehive-Hidato і походження ідеї"}
  - {kind: other, url: "https://www.nearly42.org/vdisk/cstheory/hidatonpc.pdf", note: "стаття про NP-повноту Hidato (лише бачив у пошуку)"}
  - {kind: other, url: "https://puzzler.com/puzzles-a-z/hidato", note: "Puzzler: Hidato у газетах і книжках"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hidato+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, path-drawing, unique-puzzle-generation, difficulty-levels, level-solver, daily-puzzle, level-bank, undo-redo, +numbered-path, +irregular-board-mask, +auto-candidates]
proposes: ["+cond:consecutive_adjacent(k, k+1, n8)", "+card:numbered-path", "+card:irregular-board-mask"]
author: opus
date: 2026-11-09
---

# Hidato — впиши 1…N так, щоб кожне наступне число було сусідом попереднього, включно з діагоналлю

## Суть
Поле з клітинок довільної форми, частину чисел дано, завжди — найменше й найбільше. Гравець заповнює решту так, щоб числа 1, 2, …, N утворили неперервний ланцюжок: k і k+1 стоять у сусідніх клітинках по горизонталі, вертикалі чи діагоналі. По суті — гамільтонів шлях з 8-сусідством, де дані числа — контрольні точки. Ідея автора — «відновити шлях риби» після дайвінгу (Guardian).

## Поле і час
- Зазвичай квадратна сітка, але Wikipedia допускає гекси й будь-які мозаїки; «beehive» — гексагональна версія.
- Нерівний контур і внутрішні дірки дозволено; поле має бути **однією звʼязною частиною**.
- N = кількість клітинок поля; кожна отримує рівно одне число.
- Шари: маска поля (є клітинка / дірка) · дані числа (незмінні) · числа гравця · кандидати.
- Час статичний; хід = вписати/стерти число.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка поля | mark | число 1…N або порожньо | одне число; рахується у ланцюжку |
| Дірка / поза контуром | static | — | не входить у шлях, через неї не можна «пройти» |
| Дане число | mark | k | закріплене; 1 і N — завжди дані |
| Число гравця | mark | k | має сусіда з k−1 і k+1 (крім кінців) |
| Ланцюжок | zone | 1…N | шлях через усі клітинки, сусідство — 8 напрямків |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` + `input(key_digits)` → ЯКЩО `free(cell)` → ТО `set_value(cell, k)` (цифрова версія).
- КОЛИ `input(pencil, cell)` → ТО `mark(cell, candidate k)` (цифрова версія).
- Ланцюжок: ЯКЩО `custom: «клітинки з k і k+1 сусідні по 8 напрямках»` (`+cond:consecutive_adjacent`) → крок задоволений.
- Унікальність: ЯКЩО `unique(board)` → кожне число 1…N рівно раз.
- КОЛИ `constraint_broken(chain)` → ЯКЩО `custom: «k і k+1 вписані не поруч»` → ТО конфлікт (цифрова версія, ?).
- КОЛИ `constraint_broken(duplicate)` → ЯКЩО `custom: «одне число двічі»` → ТО конфлікт (?).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(numbers)` → ТО `win`.
- Варіант «без позицій кінців»: дано лише значення min і max, а не місця; різниця max − min = кількість клітинок − 1 (Wikipedia).
- Дедукція «Naked Single»: у клітинку підходить лише одне число — вписати (Wikipedia).
- Дедукція «Hidden Single»: число має лише одну можливу клітинку — вписати (Wikipedia).
- Дедукція «відстань»: між даними k і k+m клітинки мусять бути досяжні рівно за m кроків короля; клітинки поза цим «ромбом» відпадають.
- Розвʼязок не обовʼязково будувати по порядку — він росте від кількох даних чисел одночасно; складні пазли потребують ланцюгів, як у судоку (Wikipedia).
- Перемога: усі клітинки заповнено одним ланцюжком 1…N. Поразки й рахунку нема.

## Керування і ввід
- Паперова гра; цифрова версія: клік по клітинці + цифри з клавіатури або екранного блоку, стерти — Backspace.
- Альтернатива в застосунках: drag-шлях від числа до числа з автонумерацією (?).
- Pencil marks — кілька кандидатів у клітинці.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): поле з маскою, дані числа виділені, числа гравця, `pencil-marks`, `conflict-highlight`, `selection-highlight`.
- `puzzle-select` / `daily-window` (цифрова версія) — банк пазлів за розміром і складністю.
- `end-screen` — пазл розвʼязано (цифрова версія).
- `help-window` — правила.

## Фічі поза полем
- `puzzle-bank` і `daily-puzzle` — газетний і книжковий формат (Puzzler, Andrews McMeel syndication у пошуку).
- `difficulty-presets` — кількість даних чисел і розмір поля; `hint`, `auto-check` (цифрова версія, ?).
- Генератор: кожен коректний Hidato має рівно один розвʼязок (Wikipedia) → потрібна перевірка єдиності.

## Варіації й родичі
- **Numbrix** (Parade, Marilyn vos Savant) — те саме, але без діагоналей (4-сусідство); 7×7 і 9×9 (Wikipedia).
- **Jadium** (Jeff Marchant, Parade з 2014) — Numbrix з меншою кількістю даних.
- **Beehive Hidato** — гексагональне поле (6 сусідів).
- Варіант з даними min/max без позицій.
- Родичі в сімʼї: [Signpost](signpost.md) — той самий ланцюжок 1…N, але наступник задається стрілкою й може бути далеко; [Fillomino](fillomino.md), [Kakuro](kakuro.md) — числові пазли; [Masyu](masyu.md) — шлях через клітинки.
- Поза сімʼєю: «тур коня» (`chess-abstract`) — той самий гамільтонів шлях, інше сусідство.
- **Осі варіацій**: сусідство (8 / 4 / гекс 6 / кінь) · форма поля (прямокутник / маска з дірками) · кінці (з позицією / лише значення) · кількість даних чисел.

## Цікавинки для курсу
- Перевірка: «для кожного k сусідами є k−1 і k+1» за словником позицій — 🌱.
- Поле-маска з дірками і нерівним контуром (рендер + сусідство) — 📎.
- Кандидати клітинок через відстань Чебишова між даними числами — 🥉.
- Розвʼязувач: backtracking від даних чисел з відсіканням за відстанню — 🥈.
- Генератор: випадковий гамільтонів шлях на масці + мінімізація даних з перевіркою єдиності — 🥇 (NP-повна задача, див. статтю nearly42).
- Перемикач сусідства 8 / 4 / гекс як параметр — Hidato, Numbrix, Beehive одним кодом — 📎.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks` · `path-drawing` ↔ drag-шлях у застосунках (?) · `unique-puzzle-generation`, `difficulty-levels`, `level-solver` · `daily-puzzle`, `level-bank` · `undo-redo`.
- Перевикористано: `+auto-candidates` (Sudoku/KenKen) ↔ авто-кандидати.
- **Нема** → пропозиції карток:
  - `+numbered-path` «Числа 1…N утворюють шлях через сусідні клітинки» · game-logic/constraints · 📎 · слот {neighborhood: 4|8|hex|knight} — Hidato, Numbrix, Signpost (з напрямком).
  - `+irregular-board-mask` «Поле довільної форми з дірками» · field/topology · 📎 — Hidato, Beehive, пазли з маскою.

## Пропозиції до словників
- `+cond:consecutive_adjacent(k, k+1, n8)` — клітинки з послідовними числами сусідні у заданому сусідстві.
- `+card:numbered-path`, `+card:irregular-board-mask` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Hidato](https://en.wikipedia.org/wiki/Hidato) — правила (горизонталь/вертикаль/діагональ), 1 і N дані, гекс і будь-які мозаїки, дірки, одна звʼязна частина, рівно один розвʼязок, варіант min/max, Numbrix/Jadium, Naked/Hidden Single.
- [Guardian через inkl: Beehive Hidato](https://inkl.com/news/can-you-solve-it-is-beehive-hidato-the-new-sudoku) — у пошуку: ідея з дайвінгу, гексагональна версія.
- [hidato.com](https://www.hidato.com/) — офіційний сайт; вміст не прочитався.
- [nearly42: Hidato NP-complete](https://www.nearly42.org/vdisk/cstheory/hidatonpc.pdf) — бачив у результатах пошуку, не відкривав.
- YouTube: пошук «hidato puzzle how to solve».

## Непевне
- (?) Рік: черга каже 2008; Guardian 2015 пише «близько десяти років тому» (≈2005), Puzzler — «з 2005»; точного року не знайдено (`year: null`).
- (?) Торгова марка Hidato — Wikipedia позначає твердження як «failed verification».
- (?) Як цифрові версії підсвічують конфлікти й чи є drag-шлях — не перевіряв.
- (?) Дедукція «відстань Чебишова» — стандартна для жанру, у відкритих джерелах прямо не бачив.
