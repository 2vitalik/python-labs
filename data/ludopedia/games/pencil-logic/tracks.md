---
title: Tracks (Tatham)
slug: tracks
aka: [Train Tracks, Колія]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tracks.html", best: true, note: "мануал Tatham: правила, керування, параметри Custom"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tracks.html", note: "грати в браузері (JS-версія колекції)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simon+tatham+tracks+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, line-sum-clue, edge-marking, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, rule-variants, seed-share, save-game, undo-redo, +track-pieces, +drag-line-fill, +solve-into-undo]
proposes: ["+cond:degree(cell, n)", "+cond:crosses", "+ui:cell-must-mark", "+window:params-dialog", "+window:game-id-dialog", "+card:track-pieces", "+card:drag-line-fill"]
author: opus
date: 2026-11-09
---

# Tracks — доклади залізницю від A до B так, щоб у кожному рядку й стовпці була задана кількість клітинок колії

## Суть
На сітці частина клітинок уже містить шматки колії; на краях позначено вхід A і вихід B. Гравець прокладає одну колію з прямих і поворотів на 90° від A до B, без перехресть. Числа зверху й справа кажуть, скільки клітинок колії в кожному стовпці й рядку. Незвичне: поєднання «шляху» (як у Masyu) з лічильниками рядків і стовпців (як у Nonogram/Kakuro).

## Поле і час
- Прямокутна сітка W×H; підказки-числа над стовпцями й праворуч від рядків.
- A і B — точки на краю поля (вхід і вихід колії) (?: A ліворуч, B знизу).
- Шари: дані шматки колії (незмінні) · сегменти гравця на ребрах між клітинками · мітки клітинок «тут колія» / «нема колії» · хрестики на ребрах.
- Час статичний; хід = позначити ребро або клітинку. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | колії нема або один шматок: пряма чи поворот на 90° |
| Даний шматок колії | static | форма | частина шляху, змінити не можна |
| Вхід A / вихід B | source / sink | позиція на краю | кінці колії |
| Число рядка / стовпця | mark | N | кількість клітинок з колією в лінії |
| Сегмент колії | mark | ребро | зʼєднує центри двох сусідніх клітинок |
| Хрестик на ребрі | mark | — | «тут колії нема» |
| Мітка «є колія» | mark | колір | клітинка точно на колії, напрямок ще невідомий |
| Мітка «нема колії» | mark | хрестик | клітинка порожня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge)` → ТО `mark(edge, track)`.
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, no_track)`.
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, has_track)`.
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, no_track)`.
- КОЛИ `input(drag, cells)` → ТО `custom: «пряма лінія міток "є колія" / "нема колії" по рядку чи стовпцю»`.
- КОЛИ `constraint_broken(piece)` → ЯКЩО `custom: «у клітинці 3+ сегменти — розгалуження або перехрестя»` (`+cond:degree(cell, n)`, `+cond:crosses`) → ТО `set_state(cell, error)` (?).
- КОЛИ `constraint_broken(row_count)` → ЯКЩО `custom: «клітинок з колією в рядку більше за число»` → ТО `set_state(clue, error)` (?).
- КОЛИ `constraint_broken(path)` → ЯКЩО `not path_exists(A, B)` or `custom: «є шматок колії поза шляхом A→B»` → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `all_constraints_met` → ТО `win` + `custom: «спалах перемоги»` (?).
- Генерація: КОЛИ `level_start` → ЯКЩО `custom: «увімкнено Disallow consecutive 1 clues»` → ТО `custom: «нема двох сусідніх рядків/стовпців з 1 і числа 1 у лінії з кінцем колії»`.
- Дедукція «нуль»: число 0 — уся лінія без колії; число, що дорівнює довжині лінії, — уся лінія колії.
- Дедукція «ступінь 2»: кожна клітинка колії має рівно два сегменти; два відомі хрестики поруч з клітинкою «є колія» фіксують її форму.
- Дедукція Tricky: відкидати ходи, що згодом змусять колію перетнути себе (з мануалу).
- Перемога: одна неперервна колія A→B з прямих і поворотів, без перехресть, числа всіх рядків і стовпців збігаються. Поразки й рахунку нема.

## Керування і ввід
- Ліва кнопка по ребру між клітинками — сегмент колії; права — хрестик «нема колії».
- Ліва кнопка по клітинці — кольорова мітка «тут колія»; права — хрестик «нема колії».
- Drag лівою/правою по клітинках — пряма лінія міток (зручно закрити рядок під число).
- Спільні дії колекції Tatham (розд. 2.1): undo/redo, нова гра, рестарт, solve, курсор з клавіатури (?).

## Вікна, меню, HUD
- `game-screen`: сітка, числа над стовпцями й праворуч, A/B на краях, колія, мітки клітинок, хрестики на ребрах.
- Веб-версія (WASM): кнопки New game · Restart game · Undo move · Redo move · Solve game; меню Game: Enter game ID… · Enter random seed… · Download / Upload save file… · Preferences…; поле можна тягнути за кут, щоб змінити розмір.
- Меню Type: пресети розміру й складності; Custom… → `params-dialog` (Width, Height, Difficulty, Disallow consecutive 1 clues).
- `game-id-dialog` — Specific / Random Seed.
- `help-window` — розділ мануалу.
- Переходи: game-screen → Custom → params-dialog → новий пазл.

## Фічі поза полем
- Генератор з унікальним розвʼязком; складність Easy (?) / Tricky (Tricky вимагає глибших дедукцій).
- Параметр «Disallow consecutive 1 clues» (типово увімкнено) — проти довгих нудних прямих.
- `undo` ∞ + `redo`, `restart-level`; Solve (`auto-solve`); `seed-display` / `seed-input` / `share-code`; збереження у файл.

## Варіації й родичі
- У сімʼї: [Tatham collection](tatham-collection.md) (загальна оболонка), [Icebarn](icebarn.md) (шлях IN→OUT), [Masyu](masyu.md), [Slitherlink](slitherlink.md) (лінія на ребрах), [Nonogram](nonogram.md) і [Kakuro](kakuro.md) (підказки рядків/стовпців), [Skyscrapers](skyscrapers.md).
- Жанр «Train Tracks» існує в газетних/онлайн-збірках поза Tatham (?).
- **Осі варіацій**: шлях A→B / петля · дозволені шматки (пряма+поворот / з перехрестями) · що рахує число (клітинки / повороти) · дані шматки (так / ні).

## Цікавинки для курсу
- Модель колії як ребер між клітинками + перевірка «ступінь 0 або 2, кінці лише на A/B» — 🌱.
- Лічильники рядків/стовпців з підсвіткою перевищення — 🌱.
- Перевірка «одна колія A→B без зайвих шматків» (обхід від A) — 📎.
- Чотири види міток (ребро так/ні, клітинка так/ні) і drag-заповнення лінії — 📎.
- Генератор: випадковий шлях A→B → числа → перевірка унікальності розвʼязувачем — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `line-sum-clue` ↔ числа рядків/стовпців · `edge-marking`, `cell-click`, `keyboard-controls` · `unique-puzzle-generation`, `difficulty-levels`, `difficulty-rating`, `level-solver` · `field-size-picker`, `game-settings`, `rule-variants` (Disallow consecutive 1) · `seed-share`, `save-game`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+track-pieces` «Шлях лише з прямих і поворотів на 90°, без перехресть» · game-logic/constraints · 🌱 · слот {pieces: straight+curve|+cross}.
  - `+drag-line-fill` «Drag по рядку ставить однакові мітки на всі клітинки» · interface/input · 🌱.
  - `+solve-into-undo` — повтор з Tatham: Solve як крок історії.

## Пропозиції до словників
- `+cond:degree(cell, n)` — скільки сегментів лінії виходить з клітинки (0/1/2/3+).
- `+cond:crosses` — повтор.
- `+ui:cell-must-mark` — мітка «клітинка точно на шляху, напрямок невідомий».
- `+window:params-dialog`, `+window:game-id-dialog` — повтори з Tatham collection.
- `+card:track-pieces`, `+card:drag-line-fill` — див. мапу.

## Джерела
- ⭐ [Tatham: Tracks (мануал)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tracks.html) — правила («Complete the track from A to B»; лише прямі й повороти 90°; без самоперетину), керування мишею, параметри Custom, «contributed by James Harvey».
- [Tatham: Tracks (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tracks.html) — WASM-версія: меню Game, кнопки, коротка інструкція; пресети Type у тексті сторінки не видно.
- YouTube: пошук «simon tatham tracks puzzle».

## Непевне
- (?) Розташування A і B (ліворуч і знизу) — з памʼяті, у мануалі сказано лише «from A to B».
- (?) Підсвітка помилок (червоні числа, перехрестя) і спалах перемоги — типові для колекції, у мануалі Tracks не описані.
- (?) Назва нижчого рівня складності (Easy) і точні пресети розміру — не бачив; мануал згадує лише Tricky.
- (?) Рік додавання в колекцію не перевірено (`year: null`); походження жанру «Train Tracks» поза Tatham — з памʼяті.
- (?) Керування з клавіатури — лише через спільний розділ 2.1, деталей для Tracks не бачив.
