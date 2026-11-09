---
title: Елементарні клітинні автомати (Rule 110, Rule 30, Rule 90)
slug: elementary-cellular-automata
aka: [Elementary cellular automaton, ECA, Rule 110, Rule 30, Rule 90, коди Вольфрама, 1D-автомати]
family: build-sim
also: [program-robots]
klass: cursor
axes:
  field: 1d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: 1983
platforms: [web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rule_110", best: true, note: "таблиця правила 01101110, клас 4, доказ Тюрінг-повноти (Cook, 2004), ефір 14 клітин / 7 кроків, кораблі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Elementary_cellular_automaton", note: "код Вольфрама, 256 правил, дзеркало/доповнення, 88 нееквівалентних, 4 класи з прикладами, час униз"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rule_30", note: "1983, p XOR (q OR r), генератор випадкових чисел у Mathematica, станція Cambridge North"}
  - {kind: official, url: "https://golly.sourceforge.io/", note: "Golly — симулятор КА"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=elementary+cellular+automaton+rule+110+rule+30", note: "пошук; просторово-часові діаграми"}
stage: v1
coverage: 80
mechanics: [cell-click, game-loop, game-pause, state-as-data, field-scaling, rule-variants, logic-render-split, unit-tests, property-tests, console-render, gui-render, field-size-picker, +cellular-automaton-rule, +rule-string, +rule-number-bits, +spacetime-diagram, +toroidal-wrap, +step-run-speed, +random-soup, +rule-equivalence]
proposes: ["+ui:rule-input", "+ui:rule-table-preview", "+ui:generation-counter", "+cond:neighborhood_is", "+card:rule-number-bits", "+card:spacetime-diagram", "+card:rule-equivalence"]
author: opus
date: 2026-11-09
---

# Елементарні клітинні автомати — ряд з 0 і 1, правило = 8-бітне число, час тече вниз; Rule 110 — Тюрінг-повний

## Суть
Одновимірний ряд клітин зі станами 0/1; новий стан клітини залежить лише від неї та двох сусідів (радіус 1). Таких трійок 8, тому правило — 8 біт, тобто **номер від 0 до 255** (код Вольфрама). Кожне нове покоління малюють рядком під попереднім — виходить просторово-часова діаграма: трикутники Серпінського (Rule 90), хаос (Rule 30), взаємодійні «кораблі» (Rule 110). Гравець обирає номер і стартовий ряд — і дивиться картину; Rule 110 при правильному фоні емулює будь-яку обчислювану функцію.

## Поле і час
- Поле — 1D-ряд (нескінченний теоретично; на практиці фіксованої ширини з тором або нулями на краях).
- Час — вертикаль: рядок t+1 під рядком t; на екрані видно всю історію (2D-картинка = 1D-простір × час).
- Тік = одне покоління, синхронно з повного старого ряду.
- Типові старти: одна клітина 1 посередині або випадковий ряд.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина 0 | tile | — | новий стан = біт правила за трійкою (лівий, сам, правий) |
| Клітина 1 | tile | — | те саме |
| Правило | static | 8 біт, номер 0–255 | таблиця «трійка → біт»; трійки впорядковано 111…000 |
| Ефір Rule 110 | object | ширина 14, період 7: `00010011011111` | періодичний фон, на якому живуть кораблі |
| Корабель (glider) | object | зсув, період | локалізована структура: у доказі Кука — +2/3, −8/30, 0/7 (зсув клітин / покоління) |
| Трикутник (Rule 90/60) | object | — | емерджентний трикутник Серпінського з однієї 1 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «трійка (лівий, сам, правий) = k»` → ТО `set_cell(x, bit_k(rule))` (пропозиція `+cond:neighborhood_is`).
- Rule 110: трійки 110, 101, 011, 010, 001 → 1; 111, 100, 000 → 0 (двійково 01101110 = 110).
- Rule 30: КОЛИ `tick` → ТО `set_cell(x, custom: «лівий XOR (сам OR правий)»)` (00011110 = 30).
- Rule 90: КОЛИ `tick` → ТО `set_cell(x, custom: «лівий XOR правий»)` — з однієї 1 дає трикутник Паскаля mod 2 (?).
- КОЛИ `edge(x)` → ЯКЩО `mode(torus)` → ТО `wrap(x)`; інакше сусід поза рядом = 0.
- Еквівалентність: дзеркало (110 ↔ 124), доповнення (110 ↔ 137), дзеркальне доповнення (110 ↔ 193); з 256 правил нееквівалентних 88.
- КОЛИ `input(click, cell)` у стартовому ряду → ТО `set_cell(cell, 1 − v)`; КОЛИ `input(set_rule, n)` → ТО `set_value(rule, n)`.
- Перемоги/поразки нема; «ціль» — дослідження: до якого класу належить правило.

## Керування і ввід
- Поле вводу номера правила (0–255) або 8 перемикачів-бітів під 8 картинками трійок.
- Старт: одна 1 / випадковий / намальований ряд; ширина ряду; межі (тор / нулі).
- Run / Step / кількість поколінь; зум картинки.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): діаграма простір×час, `custom: «таблиця 8 трійок з бітами»` над нею, поле номера, Run/Step/Clear, `speed-slider`, `zoom-control`.
- HUD: номер правила, `generation-counter`.
- `custom-window` галерея 256 (або 88) правил мініатюрами — як таблиці у статті Wikipedia.
- Експорт картинки (`custom-window`).

## Фічі поза полем
- `custom-rules` — сам номер правила; `step-mode`, `speed-control`; `seed-input` для випадкового старту.
- Галерея/каталог правил з класами — `codex`-подібна довідка.
- Нема рахунку й прогресу.

## Варіації й родичі
- **Осі варіацій:** радіус сусідства (1 → r: 2^(2^(2r+1)) правил) · кількість станів (2 → k, тотальні правила) · межі (тор / нулі / нескінченність) · старт (одна клітина / випадковий) · клас поведінки Вольфрама: I — однорідний (0, 32, 160, 232), II — стабільний/періодичний (4, 108, 218, 250), III — хаос (22, 30, 126, 150, 182), IV — взаємодійні структури (110, 54).
- Родичі в корпусі: [game-of-life](game-of-life.md) (2D, Мур-8; теж Тюрінг-повна), [brians-brain-seeds](brians-brain-seeds.md), [wireworld](wireworld.md), [langtons-ant](langtons-ant.md) (одна «голова» на стрічці — ближче до машини Тюрінга), [cell-machine](cell-machine.md).
- Реальні сліди: Rule 30 — генератор випадкових чисел у Mathematica; фасад станції Cambridge North; Rule 184 — модель трафіку (?).

## Цікавинки для курсу
- Двіжок ECA: номер → таблиця через біти, крок по ряду, діаграма — 🌱 (ідеальна перша задача на біти).
- Межі тор/нулі + випадковий старт із seed — 🌱.
- Галерея 256 мініатюр + групування в 88 класів еквівалентності (дзеркало, доповнення) — 📎.
- Автокласифікатор I–IV (стиснення історії, період, ентропія) — 🥈.
- Rule 30 як генератор: центральний стовпець як біти, перевірка рівномірності — 📎.
- Детектор кораблів Rule 110 на ефірі (знайти структуру зі зсувом і періодом) — 🥇.
- Емуляція циклічної тег-системи на Rule 110 (ідея доказу Кука) — 👑.

## Мапа на каталог
- Є: `cell-click` · `game-loop` + `game-pause` · `state-as-data` · `rule-variants` (номер правила) · `field-size-picker` · `console-render` (рядок за рядком — природно в консолі) · `gui-render` · `field-scaling` · `logic-render-split` · `unit-tests` + `property-tests` (властивості: дзеркальне правило дає дзеркальну історію).
- **Нема** → пропозиції карток:
  - `+rule-number-bits` «Правило як число: біт за кожною конфігурацією сусідства» · game-logic · 🌱 · слоти {radius, states}.
  - `+spacetime-diagram` «Історія 1D-поля як 2D-картинка (час униз)» · interface/render · 🌱.
  - `+rule-equivalence` «Групування правил за симетріями (дзеркало, доповнення)» · game-logic · 📎.
  - Перевикористано: `+cellular-automaton-rule`, `+rule-string`, `+toroidal-wrap`, `+step-run-speed`, `+random-soup`.

## Пропозиції до словників
- `+cond:neighborhood_is` — конфігурація сусідства дорівнює шаблону (рядок таблиці правила); `adjacent_count` тут не підходить, бо важить порядок сусідів.
- `+ui:rule-input` — поле номера/рядка правила.
- `+ui:rule-table-preview` — 8 картинок трійок з бітами під ними.
- `+ui:generation-counter` — номер покоління.
- `+card:rule-number-bits`, `+card:spacetime-diagram`, `+card:rule-equivalence` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rule 110](https://en.wikipedia.org/wiki/Rule_110) — таблиця, клас 4, доказ Кука (CA98, Complex Systems 2004) через циклічну тег-систему, ефір і три кораблі; гіпотеза Вольфрама 1985.
- [Wikipedia: Elementary cellular automaton](https://en.wikipedia.org/wiki/Elementary_cellular_automaton) — означення, код, симетрії (64/16/16, 88), класи з прикладами, «time increasing downwards», розвʼязні правила (Fukś).
- [Wikipedia: Rule 30](https://en.wikipedia.org/wiki/Rule_30) — 1983, формула, Mathematica, Cambridge North.
- [Golly](https://golly.sourceforge.io/) — симулятор.

## Непевне
- (?) Rule 90 = «лівий XOR правий» — з памʼяті; стаття дає лише формулу mod 2 через біноміальні коефіцієнти.
- (?) Rule 184 як модель трафіку — у відкритому тексті лише згадка лінком.
- (?) `year: 1983` — рік Rule 30 і статті Вольфрама; система нумерації могла зʼявитися в тій самій роботі — не перевірено.
