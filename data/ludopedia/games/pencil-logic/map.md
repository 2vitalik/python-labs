---
title: Map (Tatham)
slug: map
aka: [Four Colour Map, Map Colouring, Розфарбування карти]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/map.html", best: true, note: "мануал Tatham: правила, керування, параметри Custom, рівні складності"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/map.html", note: "грати в браузері (JS-версія колекції)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Four_color_theorem", note: "теорема чотирьох фарб: що таке сусідство, історія"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simon+tatham+map+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, pencil-marks, keyboard-controls, unique-puzzle-generation, no-guess-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, seed-share, save-game, undo-redo, +graph-colouring, +drag-copy-colour, +region-labels]
proposes: ["+cond:shares_border(a, b)", "+ui:region-labels", "+window:params-dialog", "+window:game-id-dialog", "+card:graph-colouring", "+card:drag-copy-colour"]
author: opus
date: 2026-11-09
---

# Map — розфарбуй карту чотирма кольорами так, щоб сусідні регіони відрізнялись

## Суть
Квадратна сітка поділена на неправильні регіони-«країни»; частина вже зафарбована. Гравець фарбує решту одним з чотирьох кольорів так, щоб жодні два регіони зі спільною межею не мали однакового кольору. Розвʼязок єдиний. Незвичне: поле — фактично граф регіонів, а не сітка клітинок; гра — це пазл-версія теореми чотирьох фарб, де дані кольори роблять розфарбування однозначним.

## Поле і час
- Прямокутна сітка W×H квадратів, згрупована в N регіонів (параметр Regions); регіони довільної форми.
- Сусідство — спільна межа ненульової довжини; дотик лише кутом не рахується (і в мануалі, і в теоремі).
- Шари: межі регіонів (незмінні) · дані кольори (незмінні) · кольори гравця · stipple-крапки (олівцеві нотатки «можливо цей колір») · номери регіонів (за бажанням).
- Час статичний; хід = зафарбувати / стерти регіон або поставити крапку. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Регіон | zone | набір квадратів, сусіди | має 0 або 1 колір; вузол графа сусідства |
| Даний колір | static | один з 4 | колір стартового регіону; змінити не можна |
| Колір гравця | mark | один з 4 | ставиться перетягуванням з регіону того ж кольору |
| Stipple-крапка | mark | колір; кілька на регіон | нотатка «регіон може бути цього кольору» |
| Номер регіону | mark | N | підпис для обговорення пазла; вмикається клавішею L |
| Межа регіонів | static | ребра сітки | визначає сусідство |
| Курсор | mark | клітинка | для керування з клавіатури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, region_a → region_b)` → ЯКЩО `custom: «A має колір, B не даний»` → ТО `paint(region_b, color_of(region_a))`.
- КОЛИ `input(left_drag, empty_region|outside → region_b)` → ЯКЩО `custom: «B не даний»` → ТО `unmark(region_b)`.
- КОЛИ `input(left_drag, any → given_region)` → ТО `block` (дані кольори незмінні).
- КОЛИ `input(right_drag, region_a → region_b)` → ТО `custom: «додати / зняти stipple-крапку кольору A в регіоні B»`.
- КОЛИ `input(key_L)` → ТО `custom: «показати / сховати номери регіонів»`.
- КОЛИ `constraint_broken(adjacent_colours)` → ЯКЩО `same(region_a, region_b, color)` and `custom: «A і B мають спільну межу ненульової довжини»` (`+cond:shares_border`) → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(adjacent_colours)` → ЯКЩО `custom: «A і B торкаються лише кутом»` → ТО `custom: «не порушення: колір може збігатися»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «зафарбовано всі регіони»` → ТО `win` + `custom: «спалах перемоги (стиль — у Preferences)»`.
- Генерація: КОЛИ `level_start` → ЯКЩО `difficulty(Easy|Normal|Hard)` → ТО `custom: «пазл розвʼязний без вгадування»`; ЯКЩО `difficulty(Unreasonable)` → ТО `custom: «можуть знадобитись вгадування і бектрекінг»`.
- Дедукція «три сусіди»: регіон, сусіди якого вже мають три різні кольори, однозначно отримує четвертий.
- Дедукція «пара однаково»: два регіони, що обидва межують з тими самими трьома різнокольоровими сусідами, — одного кольору (саме це зручно позначати stipple-крапками).
- Перемога: усі регіони мають колір, сусіди за межею різні. Поразки й рахунку нема.

## Керування і ввід
- Ліва кнопка: тягнути від зафарбованого регіону до порожнього — скопіювати колір; тягнути від порожнього регіону (або з-поза сітки, якщо порожніх нема) — стерти колір цілі.
- Права кнопка: так само перетягуванням ставить або знімає stipple-крапки; у регіоні їх може бути кілька.
- Клавіатура: стрілки рухають курсор; Return починає й завершує перетягування кольору, Space — крапок; двічі Return без руху — стерти регіон; L — номери регіонів.
- Спільні дії колекції Tatham (розд. 2.1): undo/redo, нова гра, рестарт, solve.
- Палітри кольорів нема: колір «береться» з регіону, де він уже є (дані регіони містять усі 4 кольори (?)).

## Вікна, меню, HUD
- `game-screen`: карта регіонів, дані й поставлені кольори, stipple-крапки, номери регіонів (опційно), курсор.
- Веб-версія: кнопки New game · Restart game · Undo move · Redo move · Solve game; меню Game: Enter game ID… · Enter random seed… · Download / Upload save file… · Preferences…; поле можна тягнути за кут, права кнопка повертає типовий розмір.
- Меню Type: пресети; Custom… → `params-dialog` (Width, Height, Regions, Difficulty).
- `settings-window` (Preferences): стиль спалаху перемоги, чи підписувати регіони номерами від старту.
- `game-id-dialog` — Specific / Random Seed; `help-window` — розділ мануалу.
- Переходи: game-screen → Type → Custom → params-dialog → новий пазл.

## Фічі поза полем
- Генератор з єдиним розвʼязком; 4 рівні: Easy · Normal · Hard · Unreasonable (лише останній може вимагати вгадування).
- `undo` ∞ + `redo`, `restart-level`, `auto-solve` (Solve), `seed-display` / `seed-input` / `share-code`, збереження у файл.
- `custom-difficulty`: розмір сітки й кількість регіонів окремо.

## Варіації й родичі
- У сімʼї: [Tatham collection](tatham-collection.md) (оболонка), інші пазли на регіонах — [Heyawake](heyawake.md), [LITS](lits.md), [Star Battle](star-battle.md); двоколірні пазли на клітинках — [Yin-Yang](yin-yang.md), [Takuzu](takuzu.md).
- Математика: теорема чотирьох фарб (Guthrie 1852, доведення Appel і Haken 1976) — будь-яку плоску карту можна розфарбувати 4 кольорами.
- Мануал: ідею запропонувала Alexandra Lanes, натхнення — Nikoli і Verity Allan; автор вважає жанр оригінальним.
- **Осі варіацій**: кількість кольорів (3 / 4) · дані кольори (є / нема — тоді розвʼязків багато) · сусідство (по межі / і по куту) · форма регіонів (з сітки / довільні багатокутники, Voronoi) · топологія (площина / тор — там треба до 7 кольорів).

## Цікавинки для курсу
- Граф сусідства з поділу сітки на регіони (обхід ребер між квадратами різних регіонів) — 🌱.
- Перевірка «сусіди різних кольорів» + підсвітка конфлікту — 🌱.
- UI «колір тягнеться з регіону» замість палітри та stipple-нотатки — 📎.
- Генерація регіонів: випадкове «проростання» N зерен по сітці — 🥉.
- Розвʼязувач розфарбування з бектрекінгом (DSatur / пропагація обмежень) — 🥈.
- Генератор: розфарбувати карту, прибирати дані кольори, доки розвʼязок єдиний, і рейтинг складності за технікою — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `pencil-marks` ↔ stipple-крапки · `keyboard-controls` · `unique-puzzle-generation`, `no-guess-generation`, `difficulty-levels`, `difficulty-rating`, `level-solver` · `field-size-picker`, `game-settings` · `seed-share`, `save-game`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+graph-colouring` «Розфарбування графа k кольорами, сусіди різні» · game-logic/constraints · 📎 · слоти {k, adjacency: edge|edge+corner}.
  - `+drag-copy-colour` «Колір переноситься drag-ом з клітини/регіону, де він уже є» · interface/input · 🌱.
  - `+region-labels` «Перемикач номерів регіонів на полі» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:shares_border(a, b)` — два регіони мають спільну межу ненульової довжини (не лише кут); Map, політичні карти, Hex-подібні.
- `+ui:region-labels` — номери/імена регіонів поверх поля.
- `+window:params-dialog`, `+window:game-id-dialog` — повтори з Tatham collection.
- `+card:graph-colouring`, `+card:drag-copy-colour` — див. мапу.

## Джерела
- ⭐ [Tatham: Map (мануал)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/map.html) — правила (сусідство лише по межі), drag кольорів і stipple-крапок, клавіші, параметри Width/Height/Regions/Difficulty, 4 рівні, Preferences, подяки.
- [Tatham: Map (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/map.html) — коротка інструкція, меню Game, кнопки, ресайз поля.
- [Wikipedia: Four color theorem](https://en.wikipedia.org/wiki/Four_color_theorem) — визначення сусідства, Guthrie 1852, Appel і Haken 1976.
- YouTube: пошук «simon tatham map puzzle».

## Непевне
- (?) Підсвітка конфліктних регіонів — у мануалі Map не описана.
- (?) Чи гарантують дані регіони всі 4 кольори (інакше колір нема звідки тягнути) — не перевірено; ймовірно, перетягування з будь-якого зафарбованого регіону цього досить.
- (?) Пресети меню Type і типові розміри не бачив (на сторінці JS не видно).
- (?) Рік додавання в колекцію не перевірено (`year: null`).
- (?) Дедукції «три сусіди» / «пара однаково» — загальна логіка розфарбування, не з мануалу.
