---
title: Fillomino (Filling, «Заповнення»)
slug: fillomino
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
year: 1980
platforms: [paper, PC, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fillomino", best: true, note: "правила, області без підказок, техніки, варіанти (гекс, Nikoji, Filling)"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/fillomino/", note: "правила Nikoli з прикладом"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html", note: "Tatham Filling: ввід цифр, мультивибір drag"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html", note: "грати в браузері (Tatham)"}
  - {kind: play, url: "https://polyodaily.com", note: "щоденний Fillomino (лінк із Wikipedia)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fillomino+puzzle+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, hover-highlight, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, +undo-redo, +multi-select, +region-size-check, +auto-borders, +seed-share]
proposes: ["+trigger:input", "+trigger:constraint_broken", "+trigger:all_constraints_met", "+effect:set_value", "+effect:fill", "+cond:region_size", "+cond:same", "+role:mark", "+role:zone", "+ui:conflict-highlight", "+ui:region-borders", "+feature:auto-check"]
author: opus
date: 2026-11-02
---

# Fillomino — розбий сітку на поліоміно: число в клітині = розмір її області

## Суть
Сітка з кількома числами-підказками; треба заповнити кожну порожню клітину числом так, щоб кожна ортогонально звʼязна група однакових чисел мала рівно стільки клітин, скільки написано (п'ятірки — п'ятиклітинні області). Дві області однакового розміру не можуть торкатися стороною (інакше вони злилися б в одну). Підступ — **області без жодної підказки**: розмір і число такої області гравець виводить сам. Nikoli, 1980-ті.

## Поле і час
- Прямокутна сітка, часто з пунктирними внутрішніми лініями; межі областей не задані — вони наслідок значень.
- Звʼязність лише ортогональна; по діагоналі однакові числа можуть торкатися (це різні області).
- Два еквівалентні способи розмітки: числа в клітинах (Nikoli, Tatham) або межі між клітинами (папір); цифрова версія сама малює межі між різними значеннями.
- Час статичний; хід = записати число в клітину (або кілька відразу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Підказка (given) | static | число N ≥ 1 | незмінна; клітина належить області розміру N |
| Клітина | mark | число або порожньо | значення = розмір області, до якої належить |
| Область (поліоміно) | zone | розмір = значення | ортогонально звʼязна група однакових чисел; розмір рівно N |
| Область без підказки | zone | розмір виводиться | легальна; її число визначає гравець |
| Межа | mark | між сусідами з різними значеннями | малюється автоматично (цифрова версія) або олівцем (папір) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(cell, digit)` → ЯКЩО `not cell(cell, given)` → ТО `set_value(cell, digit)`; `0`/Space/Backspace — стерти.
- КОЛИ `input(selection, digit)` → ТО `set_value(each selected, digit)` (мультивибір, Tatham).
- КОЛИ `constraint_broken(region_size(r) > value(r))` → ТО область червона (переповнена — завжди помилка).
- КОЛИ `constraint_broken(region_size(r) < value(r))` → ЯКЩО `custom: «область замкнена — нема порожніх сусідів для росту»` → ТО область червона.
- КОЛИ `adjacent(region_a, region_b)` → ЯКЩО `same(a, b, value)` → ТО `custom: «це одна область»` — злиття автоматичне, тож дві «окремі» рівні області по стороні неможливі за означенням; помилка проявляється як переповнення.
- Наслідки (Tatham): нуля нема; дві сусідні 1 неможливі; у цифровій версії з цифрами 1–9 область більше 9 неможлива.
- КОЛИ `all_constraints_met` (усі клітини заповнені, кожна область має розмір = значення) → ТО `win`, `flash(completion)`.
- Перемога: розбиття сітки на області з розміром = значення. Поразки нема. Рахунок нема.
- Дедукції: межа між різними підказками; область, «закрита» підказками, завершена (одинична 1, пара 2); «переповнення» — діагональні 2-ки ставлять межі, щоб не злитись у 4; «обмежений домен» — число, оточене з трьох боків, росте у четвертий; замкнена порожня клітина = 1, замкнені дві = 2 (доміно).

## Керування і ввід
- Tatham: клік по порожній клітині й цифра; drag виділяє кілька клітин → одна цифра заповнює всі; 0/Space/Backspace/Enter — стерти; стрілки — курсор; Enter + стрілки — виділення з клавіатури; Space — додати/прибрати клітину з виділення; Escape — скинути виділення.
- Межі між різними числами малює програма — гравець думає числами, а бачить області.
- Папір: числа й/або лінії меж олівцем.

## Вікна, меню, HUD
- `game-screen`: сітка, підказки жирним, `region-borders` (автомежі), `conflict-highlight` (переповнені/закриті недостатні області), `selection-highlight` для мультивибору.
- Tatham: Type (розмір W×H) і Custom, Specific/Random Seed, Solve, Undo/Redo, Help — оболонка збірки (див. tatham-collection).
- Онлайн-щоденники (Polyo): один пазл на день (?).
- Переходи: Type → новий пазл → розвʼязано → спалах.

## Фічі поза полем
- `difficulty-presets` за розміром; `undo`/`redo`, `auto-solve`, `seed-input`/`share-code` (Tatham).
- `auto-check` — лише явні помилки (переповнення, замкнена недостача).
- `daily-puzzle` (Polyo) (?).

## Варіації й родичі
- **Nikoji** (Nikoli): літери замість чисел — однакові літери = області однакові за розміром, формою, орієнтацією й положенням літери.
- **Гекс-Fillomino**: те саме з поліхексами.
- **Allied Occupation** — назва у Чемпіонаті світу з пазлів (круглі клітини, суто естетика) (?).
- **Filling** (Tatham) — цифрова версія; **Fields** (iOS, 2013) — мобільний варіант.
- Родичі «розбий на області»: Palisade (однаковий розмір, числа = стінки), Rectangles/Shikaku (прямокутники = площа), Galaxies (симетрія), Nurikabe (острови з числом = розмір).
- **Осі варіацій**: що задає підказка (розмір області / форму / площу прямокутника) · чи можуть рівні області торкатися (ні — Fillomino; так — розділені стінками в Palisade) · чи є області без підказок · форма клітин (квадрат / гекс).

## Цікавинки для курсу
- Обчислення областей flood-fill по однакових значеннях і перевірка «розмір = значення» — 📎.
- Розрізнення «переповнена» (помилка одразу) і «недостатня, але ще може рости» (помилка лише якщо замкнена) — 🥉.
- Автомалювання меж між різними значеннями як окремий шар рендера — 📎.
- Мультивибір drag + одна цифра на всі — 📎.
- Солвер (межі, домени, «замкнені» клітини) + генератор з єдиністю розвʼязку й прихованими областями — 🥇/👑.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `hover-highlight` · `unique-puzzle-generation` · `difficulty-levels` · `level-solver` · `field-size-picker`.
- **Нема** → пропозиції карток:
  - `+undo-redo` (уже є в корпусі).
  - `+multi-select` (є в sudoku) — тут виділення + одна цифра на всі.
  - `+region-size-check` (є в nurikabe) — тут область = звʼязна група однакових значень, розмір = значення.
  - `+auto-borders` «Автоматичні межі між різними значеннями» · interface/render · 📎.
  - `+seed-share` (пропоновано).

## Пропозиції до словників
- `+trigger:input`, `+trigger:constraint_broken`, `+trigger:all_constraints_met`.
- `+effect:set_value`; `+effect:fill` — заповнити виділену групу однією цифрою.
- `+cond:region_size(r, op, n)` — розмір звʼязної області порівняно з N; `+cond:same` — однакові значення сусідів (злиття).
- `+role:mark` (число в клітині), `+role:zone` (поліоміно).
- `+ui:conflict-highlight`; `+ui:region-borders` — автомежі областей.
- `+feature:auto-check`.

## Джерела
- ⭐ [Wikipedia: Fillomino](https://en.wikipedia.org/wiki/Fillomino) — правила, області без підказок, техніки (overloads, limited domains), варіанти (гекс, Nikoji, Filling, Fields).
- [Nikoli: Fillomino](https://www.nikoli.co.jp/en/puzzles/fillomino/) — чотири правила від видавця.
- [Tatham: Filling](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/filling.html) — правила, ввід із мультивибором; [грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html).
- [Polyo](https://polyodaily.com) — щоденний Fillomino (з зовнішніх лінків Wikipedia).
- YouTube: [пошук «fillomino puzzle solve»](https://www.youtube.com/results?search_query=fillomino+puzzle+solve).

## Непевне
- (?) Рік 1980 — Wikipedia каже лише «1980-ті», точний випуск Puzzle Communication Nikoli не знайдено.
- (?) Polyo — сторінку не відкривав, лише лінк зі статті.
- (?) «Allied Occupation» — на Wikipedia з позначкою «citation needed».
- (?) Обмеження «область ≤ 9» — особливість вводу однією цифрою в Tatham; у паперових Fillomino трапляються числа ≥ 10 (?).
