---
title: Zahlenlabyrinth (Magic Labyrinth, Магічний лабіринт)
slug: zahlenlabyrinth
aka: [Magic Labyrinth, Magisches Labyrinth, Magic Maze, Magische Spirale, Magic Spiral, Zahlenspirale, Number Spiral, Магічний лабіринт]
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
year: 2008
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Zahlenlabyrinth/index.htm", best: true, note: "Janko: правила DE/EN, назви, 180 пазлів 5×5–11×11, рейтинг 1–8, джерела пазлів"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Zahlenlabyrinth/001.a.htm", note: "грати (applet Numbermaze); у коді — size, depth, [problem], [lines], [solution], [moves]"}
  - {kind: wiki, url: "http://wiki.logic-masters.de/index.php?title=Magisches_Labyrinth", note: "Puzzle-Wiki DE: Бернхард Зекінгер, листопад 2008, узагальнення Magische Spirale; тег WPC-2012"}
  - {kind: wiki, url: "http://wiki.logic-masters.de/index.php?title=Magicmaze/en", note: "Puzzle-Wiki EN: правила (цифри 1–3, лабіринт «ззовні всередину»)"}
  - {kind: wiki, url: "http://wiki.logic-masters.de/index.php?title=Zahlenspirale/de", note: "предок Zahlenspirale (Magische Spirale): теги WPC-2011, WPC-2013"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Zahlenlabyrinth/Bedienung.htm", note: "керування applet-ом: × «точно без числа», ? «точно число, ще невідоме»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=magic+labyrinth+number+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, level-rating, puzzle-select, help-window, save-game, undo-redo, replay, +latin-square, +empty-cells-in-latin, +path-cyclic-sequence, +dot-mark, +hint-reveal, +cell-coloring]
proposes: ["+cond:cyclic_order(path, n)", "+card:path-cyclic-sequence", "+ui:solved-frame", "+ui:value-popup-menu", "+window:puzzle-info"]
author: opus
date: 2026-11-09
---

# Zahlenlabyrinth (Magic Labyrinth) — латинський квадрат з дірками, де вздовж коридору лабіринту числа йдуть по колу 1, 2, …, N

## Суть
Сітка S×S розділена стінами на коридор, що проходить через усе поле; початок позначено колом. Гравець вписує числа 1…N (N < S) так, щоб кожне було рівно раз у кожному рядку й стовпці, а решта клітинок лишалась порожньою. Ідучи коридором від кола, зустрічаєш числа строго в циклі 1, 2, …, N, 1, 2, … — порожні клітинки пропускаються. Незвичне: латинське обмеження рядків і стовпців схрещене з **порядковим** обмеженням уздовж одновимірного шляху, що петляє полем.

## Поле і час
- Квадратна сітка S×S; у Janko — 5×5 (20), 6×6 (27), 7×7 (92), 8×8 (23), 9×9 (8), 10×10 (7), 11×11 (3).
- Діапазон 1…N задано окремо (у даних Janko — `depth`: пазл №1 — S = 5, N = 3; №100 — S = 8, N = 4).
- Стіни — товсті лінії; у даних Janko шлях задано нумерацією клітинок 1…S² (`[lines]`): коридор нерозгалужений і покриває все поле.
- Початок — клітинка з колом (номер 1 у `[lines]`); вона містить 1 або лишається порожньою.
- Ранні пазли — спіраль ззовні всередину, пізніше — довільні коридори (Janko).
- Шари: стіни й коло (незмінні) · дані числа (сині) · числа гравця · позначки × / ? · кандидати.
- Час статичний; хід = вписати число / позначку / стерти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | 1…N / порожньо / × / ? | одне значення |
| Дане число | mark | n, синє | незмінне |
| Стіна | static | між сусідніми клітинками | формує коридор |
| Коридор (шлях) | zone | S² клітинок у порядку | непорожні значення йдуть циклом 1…N |
| Коло | static | початок шляху | 1 або порожньо |
| Позначка × | mark | «точно без числа» | лише для гравця |
| Позначка ? | mark | «точно число, ще невідоме» | лише для гравця |
| Рядок / стовпець | zone | S клітинок | 1…N рівно раз, S − N порожніх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `window(+value-popup-menu)` → `set_value(cell, n)`; «•» → `unmark(cell)` (Janko).
- КОЛИ `input(key_digit, cell)` → ТО `set_value(cell, n)`; `X` або `,` → `mark(cell, ×)`; `o`, `.`, `?` → `mark(cell, ?)`; `-`, Del, ⌫ → `unmark(cell)` (Janko).
- КОЛИ `input(enter|space|ins, cell)` → ТО `mark(cell, …)` по колу порожньо → ? → × → порожньо (Janko).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, symbol|color)`; F7 — режим кандидатів (Janko).
- Латинське: КОЛИ `constraint_broken(latin)` → ЯКЩО `not unique(row)` or `not unique(col)` → ТО конфлікт.
- Повнота: ЯКЩО `custom: «у кожному рядку й стовпці є всі 1…N»` → решта S − N клітинок лінії порожні.
- Шлях: КОЛИ `constraint_broken(path)` → ЯКЩО `not custom: «наступне число на шляху після k — це k mod N + 1»` (`+cond:cyclic_order`) → ТО конфлікт.
- Старт: ЯКЩО `custom: «перше число на шляху від кола»` → ТО `custom: «воно дорівнює 1»`; коло — 1 або порожньо.
- КОЛИ `input(F6)` → ТО `custom: «усі порушення — червоним»`; F3 — режим підказки, F4 — розвʼязок з логічним шляхом (Janko).
- КОЛИ `all_constraints_met` → ТО `custom: «зелена рамка»` + `win` (Janko).
- КОЛИ `input(ctrl_z|pgup)` → ТО `undo(1)`; `input(pos1)` → `undo(all)`; Ctrl+Y / End — повернути (Janko).
- Дедукція «кінець»: чисел на полі S·N — кратно N, тож останнє число шляху — N (наслідок правил).
- Дедукція «сусіди по шляху»: дві непорожні клітинки, між якими на шляху лише порожні, мають значення k і k+1 (mod N) (наслідок правил).
- Дедукція «дірки»: коли в лінії вже S − N клітинок позначено ×, решта — числа (наслідок правил).
- Перемога: латинське заповнення з дірками + цикл 1…N уздовж усього шляху · Поразка: — · Рахунок: —.

## Керування і ввід
- Миша (Janko applet): лівий клік — меню чисел, ×, ? і «•»; правий клік — меню символьних і кольорових позначок.
- Дотик: тап — меню значень; утримання — меню позначок.
- Клавіатура: стрілки — рамка; Enter / Space / Ins — цикл порожньо → ? → × → порожньо; цифри; X , o . ? - Del ⌫.
- Наведення без кліку + клавіша; Ctrl+Q…D — символи; Alt/Ctrl+0…9 — кольори; F7 — кандидати.
- Масштаб: Ctrl+стрілки, два пальці; вибір пазла — випадне меню або Ctrl+PgDn / PgUp.
- Папір: друк картинки; журнал «Logisch» регулярно друкує жанр (Janko).

## Вікна, меню, HUD
- `game-screen`: сітка зі стінами коридору, коло старту, числа, × і ?, кандидати (`pencil-marks`), `conflict-highlight` (F6), `+ui:solved-frame`, `+ui:value-popup-menu`.
- `puzzle-select` — індекс Janko: 180 пазлів за датою, розміром, складністю.
- `help-window` — Regeln (приклад + розвʼязок), Bedienungsanleitung, сторінка Beispiel.
- `+window:puzzle-info` (F1) — інфо про пазл і лист вебмайстру.

## Фічі поза полем
- `auto-check` (F6), автовизнання розвʼязку.
- `undo` / `redo` по одному й усі; збереження стану Ctrl+S / Ctrl+L.
- `hint` (F3), `show-solution` (F4) з логічним шляхом у списку ходів (дані `[moves]`).
- `puzzle-bank` — рейтинг 1–8 лише за часом розвʼязання; нові пазли без оцінки; пазли з відтворюваним шляхом — кольором.

## Варіації й родичі
- **Magische Spirale / Zahlenspirale** (Number Spiral) — предок: шлях — спіраль ззовні всередину; у Puzzle-Wiki теги WPC-2011 і WPC-2013.
- **Magisches Labyrinth** — узагальнення Бернхарда Зекінгера (листопад 2008); тег WPC-2012.
- Джерела пазлів у Janko: Alberto Fabris (Puzzle Fountain), Otto Janko, Andreas Bolota, Sachsentext, Croco-Puzzle (офлайн), журнал «Logisch».
- Родичі: [Easy as ABC](easy-as-abc.md) (латинський з дірками + порядок «перша видима»), [Hidato](hidato.md) і [Signpost](signpost.md) (послідовність уздовж шляху), [Doppelblock](doppelblock.md) (латинський з «дірками»-блоками), [Ziegelmauer](ziegelmauer.md), [Sudoku](sudoku.md).
- **Осі варіацій**: форма шляху (спіраль / довільний коридор) · старт (вхід із краю / коло) · N відносно S · дані числа (є / нема).

## Цікавинки для курсу
- Рендер стін з нумерації `[lines]`: стіна між сусідами, чиї номери не відрізняються на 1 — 📎.
- Перевірка шляху: пройти масив клітинок у порядку, пропустити порожні, звірити цикл 1…N — 🌱.
- Латинська перевірка з дірками (кожне 1…N раз, решта порожні) — 🌱.
- Генерація коридору — гамільтонів шлях на сітці (спіраль або випадковий) — 🥈.
- Розвʼязувач: кандидати {порожньо, 1…N} + пропагація вздовж шляху + латинські виключення + backtracking — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select`, `help-window` · `save-game`, `undo-redo` · `replay` ↔ логічний шлях F4.
- Перевикористано: `+latin-square`, `+empty-cells-in-latin` (Easy as ABC), `+dot-mark` ↔ × і ?, `+hint-reveal` ↔ F3, `+cell-coloring`.
- **Нема** → пропозиції карток:
  - `+path-cyclic-sequence` «Числа вздовж заданого шляху йдуть циклом 1…N» · game-logic/constraints · 📎 · слот {path: spiral|maze, start: edge|circle}.

## Пропозиції до словників
- `+cond:cyclic_order(path, n)` — непорожні значення вздовж шляху йдуть циклом 1…n.
- `+card:path-cyclic-sequence` — див. мапу.
- `+ui:solved-frame`, `+ui:value-popup-menu`, `+window:puzzle-info` — повтори (Detektivschach, Ziegelmauer).

## Джерела
- ⭐ [Janko: Zahlenlabyrinth](https://www.janko.at/Raetsel/Zahlenlabyrinth/index.htm) — правила DE/EN («коло не обовʼязково 1, може бути порожнім»), назви, 180 пазлів за розмірами, рейтинг, джерела.
- [Janko: Zahlenlabyrinth №1](https://www.janko.at/Raetsel/Zahlenlabyrinth/001.a.htm) — дані `numbermaze`: `size`, `depth`, `[lines]` (порядок шляху), `[moves]`; також переглянуто №100.
- [Puzzle-Wiki: Magisches Labyrinth](http://wiki.logic-masters.de/index.php?title=Magisches_Labyrinth) — Зекінгер, 11.2008, предок, теги змагань.
- [Puzzle-Wiki: Magicmaze](http://wiki.logic-masters.de/index.php?title=Magicmaze/en) — правила EN.
- [Puzzle-Wiki: Zahlenspirale](http://wiki.logic-masters.de/index.php?title=Zahlenspirale/de) — предок, теги WPC.
- [Janko: Bedienung](https://www.janko.at/Raetsel/Zahlenlabyrinth/Bedienung.htm) — керування, значення × і ?.
- YouTube: пошук «magic labyrinth number puzzle».

## Непевне
- (?) Хто вигадав Magische Spirale і коли — Puzzle-Wiki каже лише, що перший приклад — у Rätselportal.
- (?) Puzzle-Wiki формулює старт «ззовні всередину», Janko — «від кола»; чи коло завжди на краю — у №1 і №100 воно на лівому краю, інших не дивився.
- (?) Чи коридор завжди нерозгалужений і покриває все поле — так у даних №1 і №100; правила прямо цього не кажуть.
- (?) Що означають теги WPC на Puzzle-Wiki (жанр був на чемпіонаті) — сторінки не пояснюють.
