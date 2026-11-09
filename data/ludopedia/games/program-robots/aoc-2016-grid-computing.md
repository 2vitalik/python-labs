---
title: "Advent of Code 2016, день 22: Grid Computing"
slug: aoc-2016-grid-computing
aka: [AoC 2016 Day 22, Grid Computing]
family: program-robots
also: [push-slide]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2016
platforms: [web]
links:
  - {kind: play, url: "https://adventofcode.com/2016/day/22", best: true, note: "умова ч.1: вузли-диски /dev/grid/node-xX-yY, df з Used/Avail, переміщення всіх даних у сусіда, «viable pairs»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/15_puzzle", note: "пʼятнашки — що насправді ховається в ч.2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=advent+of+code+2016+day+22", note: "пошук; розвʼязки й візуалізації"}
stage: v1
coverage: 65
mechanics: [level-from-txt, move-4dir, impassable-cells, swap-on-contact, chase-bfs, reachability-check, level-solver, console-render, fixture-level-tests, +sliding-hole-puzzle, +capacity-move, +data-to-target, +answer-checksum, +two-part-puzzle]
proposes: ["+cond:fits_capacity(a, b)", "+effect:move_all(a → b)", "+feature:personal-input", "+feature:two-part-reveal"]
author: opus
date: 2026-11-09
---

# AoC 2016/22 Grid Computing — сітка дисків, де дані переливаються в сусіда цілком: насправді це пʼятнашки з однією дірою

## Суть
Задача Advent of Code 2016 (день 22). Ввід — вивід `df` для сітки вузлів-дисків `/dev/grid/node-xX-yY`: розмір, зайнято, вільно. Ч.1 — порахувати «придатні пари» вузлів (A, B), де дані A вміщаються у вільне місце B. Ч.2 — перенести дані з цільового вузла в доступний вузол `x0-y0`, коли дозволена лише одна операція: перелити **всі** дані вузла в сусіда, якщо вміщуються. Виявляється, що придатні пари майже всі вказують на єдиний порожній вузол, а кілька величезних вузлів не рухаються ніколи — тож це пʼятнашки з однією дірою і стінами. Загальна рамка AoC — у [advent-of-code-grids](advent-of-code-grids.md).

## Поле і час
- Квадратна сітка вузлів; координати з імені вузла (`x` вправо, `y` вниз); сусіди — 4 напрямки.
- Кожен вузол: Size, Used, Avail (= Size − Used), Use%.
- Ч.2: крок = одне переміщення даних між сусідами; мета — мінімальна кількість кроків.
- Повна інформація; рівень — персональний ввід (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайний вузол | object | Size, Used | дані переливаються цілком у сусіда з достатнім Avail |
| Порожній вузол (`_`) | player | Used = 0 | фактично «дірка» пʼятнашок: рухається, коли в нього переливають сусіда (?) |
| Великий вузол (`#`) | static | Used ≫ Avail будь-кого | не вміщається нікуди — стіна (?) |
| Цільові дані `G` | object | на вузлі `x_max-y0` (?) | треба довести до `x0-y0` |
| Вузол `x0-y0` | static | доступний напряму | мета ч.2 |

## Правила (КОЛИ → ЯКЩО → ТО)
- Ч.1: КОЛИ `custom: «перебір усіх пар (A, B), A ≠ B, не обовʼязково сусіди»` → ЯКЩО `custom: «Used(A) > 0»` and `custom: «Used(A) ≤ Avail(B)»` → ТО `counter(viable, +1)`; відповідь — кількість.
- Ч.2: КОЛИ `input(move A → B)` → ЯКЩО `custom: «A і B — сусіди»` and `custom: «Used(A) ≤ Avail(B)»` → ТО `custom: «усі дані A переходять у B: Used(B) += Used(A), Used(A) = 0»` — частково переносити не можна.
- КОЛИ `custom: «дані з G переміщено»` → ТО `custom: «G тепер на новому вузлі»` — `swap(G, empty)` по суті.
- КОЛИ `reach(G, x0-y0)` → ТО `win`; відповідь — мінімальна кількість кроків.
- Ключове спостереження (?): майже всі придатні пари мають B = єдиний порожній вузол → `custom: «гра зводиться до руху дірки по сітці з непрохідними великими вузлами»` → BFS дірки до клітини поруч з G, потім цикл «зсунути G на 1 + обійти дірку» (5 кроків на клітину в прямому коридорі).
- Перемога: правильне число в формі · Поразка: нема · Рахунок: дві зірки.

## Керування і ввід
- Ввід — текст `df -h`-подібної таблиці: `Filesystem Size Used Avail Use%`, рядки `/dev/grid/node-x0-y0 …T …T …T …%` (?).
- Гравець пише програму; ч.2 багато хто розвʼязує «руками»: друкує сітку символами `. _ # G` і рахує кроки на око.

## Вікна, меню, HUD
- `puzzle-page` (custom) і `answer-form` — як у [advent-of-code-grids](advent-of-code-grids.md); ч.2 відкривається після першої зірки.

## Фічі поза полем
- `personal-input`, `two-part-reveal` — рамка AoC.
- Візуалізація як підказка: сам формат задачі спонукає вивести сітку в консоль.

## Варіації й родичі
- Пʼятнашки (15 puzzle), Rush Hour, «Klotski» — та сама механіка дірки (сімʼя `push-slide`); парність перестановки робить половину позицій нерозвʼязними.
- AoC-задачі, де ввід ховає просту структуру за «шумним» форматом (2017/21 фрактал, 2018/23 дрони) (?).
- Осі варіацій: **дірок** (одна / кілька); **ємність** (бінарна стіна/не стіна / справжні Size/Used з частковими переливами); **ціль** (одна плитка до кута / упорядкувати все).

## Цікавинки для курсу
- Ч.1: подвійний цикл з умовою або сортування за Avail — 🌱.
- Розпізнати з даних, що «ємнісна» задача — це пʼятнашки (класифікувати вузли на порожній / звичайний / стіну) — 📎.
- BFS стану (позиція дірки, позиція G) по сітці зі стінами — 🥉.
- Загальний розвʼязувач з реальними ємностями (без спрощення) — 🥇 (простір станів вибухає).
- Консольний рендер `. _ # G` як інструмент дослідження — 🌱.

## Мапа на каталог
- Є: `level-from-txt` (вивід df) · `move-4dir` · `impassable-cells` (великі вузли) · `swap-on-contact` (дані G ↔ дірка) · `chase-bfs` (шлях дірки) · `reachability-check` · `level-solver` · `console-render` · `fixture-level-tests` (приклад з умови ч.2 (?)).
- **Нема** → пропозиції карток:
  - `+sliding-hole-puzzle` «Пʼятнашки: рух плиток лише в єдину дірку» · entities/move · 🥉.
  - `+capacity-move` «Перелити вміст у сусіда, якщо вміщується» · entities/interact · 📎.
  - `+data-to-target` «Довести одну виділену плитку до цілі серед інших» · game-logic/win · 📎.
  - `+answer-checksum`, `+two-part-puzzle` — з [advent-of-code-grids](advent-of-code-grids.md).

## Пропозиції до словників
- `+cond:fits_capacity(a, b)` — вміст A вміщається у вільне місце B.
- `+effect:move_all(a → b)` — перенести весь вміст (не обʼєкт) у сусіда.
- `+feature:personal-input`, `+feature:two-part-reveal` — підтвердження з advent-of-code-grids.

## Джерела
- ⭐ [AoC 2016 Day 22](https://adventofcode.com/2016/day/22) — ч.1: вузли `/dev/grid/node-xX-yY`, доступ лише до `x0-y0`, `df` у вводі, переміщення всіх даних у сусіда, визначення viable pair (A не порожній, A ≠ B, Used(A) ≤ Avail(B)).
- [Wikipedia: 15 puzzle](https://en.wikipedia.org/wiki/15_puzzle) — механіка дірки, правило парності.

## Непевне
- (?) Уся ч.2 (ціль `x_max-y0` → `x0-y0`, одна порожня клітина, великі вузли-стіни, 5 кроків на зсув) — з памʼяті: без логіну видно лише ч.1.
- (?) Точний формат рядків df і чи має умова приклад сітки для ч.2.
- (?) Родичі серед інших днів AoC — з памʼяті.
