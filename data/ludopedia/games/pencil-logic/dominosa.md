---
title: Dominosa (Доміноза)
slug: dominosa
aka: [Dominosa Omnibus, Solitaire Dominoes, Deductomino, Domino Hunt, Dominosuche, Dominosteine, Dominosystem, Dominos]
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
year: 1874
platforms: [paper, PC, web, mobile]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/dominosa.html", best: true, note: "Tatham: правила, миша й клавіатура, підсвітка чисел, параметри (max число, unique)"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/dominosa.html", note: "грати в браузері (Tatham)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Dominos/index.htm", note: "Janko: правила, історія (O. S. Adler 1874, патент 1893, Pijanowski у Гарднера), 600 пазлів, інші назви"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії Tatham"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dominosa+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, edge-marking, keyboard-controls, selection-highlight, multi-cell-size, unique-puzzle-generation, level-solver, field-size-picker, undo-redo, redo, restart-level, seed-share, level-bank, +domino-tiling, +full-set-once, +value-highlight, +non-unique-mode]
proposes: ["+cond:pair_used(a, b)", "+effect:place_domino", "+ui:digit-highlight", "+ui:edge-cross", "+window:params-dialog", "+window:game-id-dialog", "+feature:non-unique-mode", "+card:domino-tiling", "+card:full-set-once", "+card:value-highlight"]
author: opus
date: 2026-11-09
---

# Dominosa — у прямокутнику чисел знайди, де лежить кожна кісточка повного набору доміно

## Суть
Повний набір доміно (усі невпорядковані пари чисел 0…N, кожна рівно один раз) виклали прямокутником, а межі між кісточками стерли — видно лише числа в клітинках. Гравець відновлює розкладку: накриває кожну пару сусідніх клітинок доміно так, щоб усе поле було вкрите і кожна пара чисел зустрілась рівно раз. Незвичне: обмеження **глобальне на набір** — «0-3 уже використана десь» забороняє всі інші сусідні 0 і 3. Головоломка відома з XIX ст. (O. S. Adler, 1874).

## Поле і час
- Прямокутник (N+2) × (N+1) для набору 0…N: при N = 6 — 8×7 = 56 клітинок, 28 кісточок (Tatham).
- Шари: числа в клітинках (незмінні) · доміно (пари сусідніх клітинок) · лінії «не доміно» між сусідами · підсвітка обраних чисел.
- Сусідство ортогональне: доміно горизонтальне або вертикальне.
- Час статичний; хід = покласти/зняти доміно або лінію на ребрі між двома клітинками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка з числом | static | 0…N | покривається рівно одним доміно |
| Доміно (кісточка) | tile | невпорядкована пара {a, b}; 1×2 | займає дві сусідні клітинки; кожна пара — рівно раз у полі |
| Набір | static | усі пари 0…N, (N+1)(N+2)/2 штук | кожна кісточка використана рівно раз |
| Лінія «не доміно» | mark | на ребрі між двома числами | дві клітинки не утворюють одну кісточку |
| Підсвітка числа | mark | до 2 чисел одночасно | показує всі входження числа на полі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge_between(c1, c2))` → ТО `place(player, domino(c1, c2))`; ЯКЩО `occupied(c1 or c2, domino)` → ТО старі доміно, що перекриваються, `disappear`; повторний клік — зняти.
- КОЛИ `input(right_click, edge_between(c1, c2))` → ТО `mark(edge, no_domino)`; повтор → `unmark(edge)`.
- КОЛИ `input(right_click, cell)` або `input(digit_key)` → ТО `custom: «підсвітити всі клітинки з цим числом»` (до двох чисел; повтор знімає).
- КОЛИ `input(enter, edge)` → ТО покласти/зняти доміно; `input(space, edge)` → лінія (курсор між двома числами).
- КОЛИ `constraint_broken(set)` → ЯКЩО `custom: «та сама пара {a, b} покладена двічі»` → ТО конфлікт (?).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(domino)` and `unique(domino_pairs)` → ТО `win`, `flash(completion)`.
- Наслідки: клітинка з єдиним вільним сусідом — доміно з ним вимушене; пара {a, b}, що може стати лише в одному місці поля, кладеться туди, а всі інші сусідні a–b отримують лінію.
- Дедукції: коли пару вже покладено, решта сусідніх входжень тієї самої пари — лінії (`custom: «pair_used»`); клітинка, всі сусіди якої дають уже використані пари, крім одного, — вимушена; «подвійні» (a-a) часто мають мало кандидатів.
- Перемога: поле покрите, кожна кісточка набору рівно раз. Поразки й рахунку нема.

## Керування і ввід
- Tatham, миша: ліва між двома числами — доміно (перекриті знімаються); ліва ще раз — зняти; права між числами — лінія «не доміно»; права по числу — підсвітити всі входження (до двох чисел).
- Tatham, клавіатура: стрілки — курсор; між двома числами Enter — доміно, Space — лінія; цифрові клавіші — підсвітка числа.
- Спільні дії Tatham: N — нова, U/Ctrl+Z — undo, R/Ctrl+R — redo, Restart, Solve, Save/Load, Specific / Random Seed.
- Папір: обвести пари; часто — таблиця-чекліст усіх кісточок збоку.

## Вікна, меню, HUD
- `game-screen`: сітка чисел, покладені доміно, лінії, `+ui:digit-highlight` (обрані числа), `cursor` між клітинками.
- Меню Game (Tatham): New · Restart · Specific… · Random Seed… · Load/Save · Undo/Redo · Solve · Preferences.
- Меню Type: пресети за max числом; Custom… → `+window:params-dialog` (Maximum number on dominoes, Ensure unique solution).
- `+window:game-id-dialog` — ID / seed.
- `help-window` — мануал; `puzzle-select` — 600 пазлів Janko (цифрова версія банку).
- Переходи: Type → новий пазл → розвʼязано → спалах.

## Фічі поза полем
- `custom-difficulty`: max число N задає розмір поля.
- `+feature:non-unique-mode` — Ensure unique solution вимкнено: пазл може мати кілька розвʼязків (важче, швидша генерація, «знайди всі» як челендж).
- `undo` ∞, `redo`, `restart-level`, `auto-solve`, `seed-input`, `share-code`, `export-import` (Save/Load).
- `puzzle-bank` — Janko (001–600).

## Варіації й родичі
- Інші набори доміно й інші форми поля (не прямокутник) — Janko.
- **Shikaku**, **Fillomino** — розбиття на області за числами; Dominosa — розбиття на 1×2 з глобальним «кожна пара раз».
- **Sudoku** — інше обмеження «кожен елемент раз» (латинський квадрат — по рядку; тут — по всьому набору).
- **Осі варіацій**: розмір набору (0…N) · форма поля · розмір плиток (доміно / тріміно) · обмеження набору (кожна раз / з повтором) · гарантія єдиності.

## Цікавинки для курсу
- Генерація повного набору невпорядкованих пар і розкладка в (N+2)×(N+1) — 🌱.
- Валідатор: покриття без накладань + усі пари різні (множина `frozenset`) — 📎.
- Клік між клітинками → доміно; перекриття знімає старі — 📎.
- Підсвітка до двох чисел як інструмент дедукції — 🌱.
- Розвʼязувач: вимушені клітинки + «пара можлива лише в одному місці» (зводиться до точного покриття / паросполучення) — 🥇.
- Режим без гарантії єдиності + пошук усіх розвʼязків — 🥈.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `edge-marking` (лінії «не доміно») · `keyboard-controls` · `selection-highlight` · `multi-cell-size` (кісточка 1×2) · `unique-puzzle-generation` · `level-solver` · `field-size-picker` · `undo-redo` / `redo` / `restart-level` · `seed-share` · `level-bank`.
- **Нема** → пропозиції карток:
  - `+domino-tiling` «Покриття поля доміно 1×2» · entities/legality · 📎.
  - `+full-set-once` «Кожен елемент набору використаний рівно раз» · game-logic/constraints · 📎.
  - `+value-highlight` «Підсвітити всі клітинки з обраним значенням» · interface/hud · 🌱.
  - `+non-unique-mode` «Пазл без гарантії єдиності» · levels/generation · 🌱.

## Пропозиції до словників
- `+cond:pair_used(a, b)` — пару значень {a, b} уже покладено десь на полі.
- `+effect:place_domino` — накрити дві сусідні клітинки однією плиткою, знявши перекриті.
- `+ui:digit-highlight` (пропоновано в sudoku) — тут до двох чисел одночасно.
- `+ui:edge-cross` — лінія «не доміно» на ребрі.
- `+window:params-dialog`, `+window:game-id-dialog`.
- `+feature:non-unique-mode` — вимкнути гарантію єдиності.

## Джерела
- ⭐ [Tatham: Dominosa](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/dominosa.html) — правила, керування мишею/клавіатурою, підсвітка до двох чисел, параметри, «(N+2)×(N+1)», O. S. Adler.
- [Janko: Dominos](https://www.janko.at/Raetsel/Dominos/index.htm) — правила, історія (Adler 1874, патент 1893 «Richard Osa», Pijanowski у «Mathematical Circus» Гарднера), 600 пазлів, інші назви.
- [Tatham: спільні дії](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html).
- YouTube: [пошук](https://www.youtube.com/results?search_query=dominosa+puzzle).

## Непевне
- (?) Стаття Wikipedia «Dominosa» не існує (пошук дає лише «Dominoes») — лінка з черги нема.
- (?) Чи підсвічує Tatham подвійно використані пари як помилку — мануал не каже.
- (?) Рівні складності в Custom Tatham — у поточному мануалі лише два параметри; у старому описі збірки згадано «складність».
- (?) Авторство: Janko подає і Adler (1874), і Pijanowski (через Гарднера, 1979) — суперечність джерел.
- (?) Розвʼязувач Tatham Solve для неунікальних пазлів — поведінка не перевірена.
