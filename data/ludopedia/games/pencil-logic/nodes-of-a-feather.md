---
title: Nodes of a Feather
slug: nodes-of-a-feather
aka: []
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [web]
links:
  - {kind: itch, url: "https://sharkwithlasers.itch.io/nodes-of-a-feather", best: true, note: "грати в браузері; правила, керування, приклад розвʼязку, скриншоти рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nodes+of+a+Feather+puzzle", note: "пошук"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, edge-marking, connectivity-check, sequential-levels, restart-level, +node-graph-field, +dual-graph-pairs, +region-size-check, +skip-level-hotkeys]
proposes: ["+role:node", "+role:edge", "+cond:exactly_one(pair)", "+effect:toggle_pair", "+ui:pair-counter", "+card:dual-graph-pairs", "+card:region-size-check"]
author: opus
date: 2026-11-09
---

# Nodes of a Feather — два вкладені графи, синій і червоний: у кожній парі перехресних ребер вмикаєш рівно одне, а число на вузлі — розмір його компоненти

## Суть
Джем-гра sharkwithlasers (Astra Game Jam, весна 2022, тема «ідіоми» — «birds of a feather flock together»). На екрані два графи — синій і червоний — вкладені один в одного так, що кожне синє ребро перетинає рівно одне червоне; це **пара**. У кожній парі треба ввімкнути рівно одне ребро. Число на вузлі каже, скільки вузлів (разом із ним) у його звʼязній компоненті свого кольору. Схоже на Fillomino, але області будуються ребрами, і кожен вибір синього ребра водночас забороняє червоне.

## Поле і час
- Граф на площині: на квадратних рівнях — синя сітка вузлів і червона, зсунута на пів кроку (як дошка Bridg-It); є неквадратні рівні (трикутно-шестикутні, напр. «pidgeondove»).
- Кожна пара = синє ребро + червоне ребро, що його перетинає; лічильник у куті показує «увімкнено пар / всього» (0/12, 0/38, 0/42).
- Назва рівня — пара птахів, половина синім, половина червоним (pidgeondove, chickenstork, duckgoose).
- Час статичний; хід = клік по ребру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синій вузол | mark | може мати число | належить синьому графу |
| Червоний вузол | mark | може мати число | належить червоному графу |
| Число на вузлі | mark | n | компонента вузла (по ввімкнених ребрах його кольору) має рівно n вузлів |
| Ребро | mark | колір; стан on/off | зʼєднує два сусідні вузли свого кольору, коли ввімкнене (товста світла лінія) |
| Пара ребер | zone | синє + червоне, що перетинаються | рівно одне з двох увімкнене |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click edge e)` → ТО `set_state(e, on)`, `clear_state(partner(e), on)` — клік вмикає ребро й вимикає його пару.
- КОЛИ `custom: «пара без увімкненого ребра»` → ТО `custom: «пазл не завершено»` (лічильник < всього).
- КОЛИ `input(click edge e)` → ЯКЩО `not region_size(component(numbered_node), n)` → ТО `constraint_broken(size)`.
- КОЛИ `all_constraints_met` (усі пари вибрані, усі числа справджені) → ТО `win`, `next_level` (?).
- КОЛИ `input(R)` → ТО `restart`; КОЛИ `input(Ctrl+])` / `input(Ctrl+[)` → ТО `next_level` / `custom: «попередній рівень»`.
- Наслідки двоїстості (виводяться з правил): синій цикл відрізає червоні вузли всередині від решти; число 1 на вузлі означає, що всі його ребра вимкнені, а отже ввімкнені всі червоні (сині) ребра-пари навколо.
- Перемога: усі пари визначені й кожне число = розмір компоненти. Поразки й рахунку нема.

## Керування і ввід
- Лівий клік по ребру — ввімкнути (пара вимикається сама).
- R — рестарт рівня; undo/redo нема («sorry, no undo/redo yet»).
- Ctrl+] — наступний рівень, Ctrl+[ — попередній (пропуск дозволено).

## Вікна, меню, HUD
- `game-screen`: граф з двох кольорів, `+ui:pair-counter` (увімкнено/всього, праворуч угорі), назва рівня (ліворуч угорі).
- Інших вікон автор не описує; меню/екран перемоги (?) .

## Фічі поза полем
- `levels-sequential` з вільним перемиканням уперед/назад (`skip-level` гарячими клавішами); `restart-level`.
- Гостьові рівні: chickenstork (pancelor), duckgoose (Patrick Traynor).
- Нема `undo`, збереження, підказок.

## Варіації й родичі
- [fillomino](fillomino.md) — число = розмір області (тут — компоненти графа); [slant](slant.md) — бінарний вибір у кожній клітинці (одна з двох діагоналей), заборона петель.
- [shannon-switching](../connect-rotate/shannon-switching.md) — Bridg-It на тій самій парі зсунутих сіток: міст одного кольору блокує перехресний міст іншого.
- [hashiwokakero](hashiwokakero.md), [tatham-collection](tatham-collection.md) (Net) — ребра графа як розмітка.
- Осі варіацій: **граф** (квадратна пара / трикутно-шестикутна пара) · **що рахує число** (розмір компоненти / степінь вузла / довжина шляху) · **вибір у парі** (рівно одне / не більше одного).

## Цікавинки для курсу
- Двоїсті графи: побудувати пари «ребро ↔ перехресне ребро» для квадратної сітки й для трикутно-шестикутної — 🥉.
- Клік-перемикач пари (одне вмикає, інше вимикає) — 🌱.
- Перевірка розміру компоненти BFS для кожного числа — 📎.
- Автоматичний висновок «цикл одного кольору ізолює вузли іншого» як підказка — 🥈.

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `cell-click` (клік по ребру) · `edge-marking` · `connectivity-check` (BFS компоненти) · `sequential-levels` · `restart-level`.
- **Нема** → пропозиції карток:
  - `+node-graph-field` «Поле — граф вузлів» (повтор).
  - `+dual-graph-pairs` «Два вкладені графи, ребра парами: рівно одне з пари» · game-logic/constraints · 🥉.
  - `+region-size-check` «Число = розмір компоненти» (повтор із fillomino) · game-logic/constraints · 📎.
  - `+skip-level-hotkeys` «Вільний перехід між рівнями клавішами» · levels/progression · 🌱.

## Пропозиції до словників
- `+role:node` / `+role:edge` — вершина й ребро графа як сутності (повтор із hackenbush, sim, slitherlink).
- `+cond:exactly_one(pair)` — рівно одна сутність з пари у стані on.
- `+effect:toggle_pair` — увімкнути одне й вимкнути його пару одним ходом.
- `+ui:pair-counter` — «увімкнено / всього» для пар.
- `+card:dual-graph-pairs` · `+card:region-size-check` — див. мапу.

## Джерела
- ⭐ [itch.io: Nodes of a Feather](https://sharkwithlasers.itch.io/nodes-of-a-feather) — правила дослівно, керування, приклад розвʼязку (сітка 3×3 + дуальна), скриншоти рівнів pidgeondove і chickenstork, коментарі гравців.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Nodes+of+a+Feather+puzzle).

## Непевне
- (?) Кількість рівнів і що стається після розвʼязку (автоперехід чи екран) — сторінка не каже.
- (?) Чи підсвічує гра порушені числа під час гри.
- (?) Рік: джем навесні 2022; дата публікації на itch не показана.
