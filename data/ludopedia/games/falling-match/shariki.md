---
title: Shariki (Шарики)
slug: shariki
aka: [Шарики, The Marbles, Super Shariki, Shariki for Windows]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 1994
platforms: [MS-DOS, Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shariki", best: true, note: "правила: обмін сусідів лише зі збігом, 3+ в лінію, падіння й поповнення, кінець — нема ходів; вплив на жанр"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Шарики", note: "автор Євген Алемжин (Кемерово), DOS, клони й нащадки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shariki+1994+dos+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [cell-click, keyboard-controls, line-match-clear, gravity-fall, spawn-random-cell, chain-reaction, no-moves-left, event-points, +match-3-swap, +swap-must-match, +no-moves-detection]
proposes: ["+cond:would_match", "+card:swap-must-match"]
author: opus
date: 2026-11-09
---

# Shariki — перша match-3: обміняй дві сусідні кульки, якщо це складе лінію з трьох

## Суть
Поле кольорових кульок; хід — обмін двох сусідніх (по горизонталі чи вертикалі), і він дозволений **лише тоді, коли дає збіг**. Лінія з 3+ однакових кульок зникає, верхні падають, зверху сиплються нові. Гра триває, доки на полі є хоч один можливий збіг; немає — кінець. Це точка відліку жанру: Bejeweled, Candy Crush, Puzzle Quest — нащадки саме цього правила «обмін = збіг».

## Поле і час
- Прямокутне поле кульок кількох кольорів; розміри й кількість кольорів у джерелах не названі.
- Покроково: хід → прибирання → падіння → поповнення згори → нові збіги (каскад) → наступний хід.
- Випадковість — у стартовому полі й у кульках поповнення (`random: both`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор / виділення | player | клітина | вибрати кульку, потім сусідню — спроба обміну |
| Кулька | tile | колір | обмінюється із сусідом; 3+ в лінію одного кольору → зникає; без опори падає |
| Верхній край | spawner | — | породжує нові випадкові кульки в стовпці з порожнечею |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap a, b)` → ЯКЩО `adjacent(a, b)` and `custom: «після обміну складається лінія 3+»` → ТО `swap(a, b)`; інакше `block` (обмін не відбувається).
- КОЛИ `pattern(line(3+))` (горизонталь або вертикаль) → ЯКЩО `same(cells, color)` → ТО `clear(line)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `fall(balls)`, `spawn_at(random_ball, top)`.
- КОЛИ `pattern(line(3+))` → ЯКЩО `custom: «склалась після падіння, а не ходом»` → ТО `clear(line)`, `combo(+1)` (каскад).
- КОЛИ `settled` → ЯКЩО `no_moves(player)` → ТО `game_over`.
- Перемога: нема — гра на рахунок · Поразка: немає жодного можливого обміну зі збігом · Рахунок: зростає за прибрані кульки («progressively higher scores»), точна формула невідома.

## Керування і ввід
- Миша / клавіатура: вибрати кульку, потім сусідню; невдалий обмін просто не виконується (ходу не витрачено).

## Вікна, меню, HUD
- `game-screen`: поле, `score`.
- `end-screen` — кінець гри, коли нема ходів (?).
- Інші вікна (меню, рекорди) у джерелах не описані.

## Фічі поза полем
—

## Варіації й родичі
- Нащадки в корпусі: `bejeweled` (2001, той самий обмін + спецкамені й режими), `candy-crush` (рівні-цілі, ліміт ходів), `puzzle-quest` (match-3 як бій), `puzzle-and-dragons` (вільне тягнення орба), `chuzzle` (зсув ряду замість обміну), `match3-meta-renovation` (мета-шар ремонту).
- Клони й похідні (ru-Wikipedia): Shariki for Windows, Super Shariki, KDiamond, Jewel Quest.
- **Осі варіацій**: хід (обмін сусідів / зсув ряду / обертання 2×2 / вільне тягнення) · легальність (лише зі збігом / будь-який обмін) · що коли нема ходів (кінець / перетасувати).

## Цікавинки для курсу
- Перевірка «обмін легальний, лише якщо дає збіг» (пробний обмін + пошук ліній) — 🌱.
- Пошук усіх ліній 3+ і каскад «прибрати → упасти → поповнити → знову» — 📎.
- Виявлення «нема жодного ходу» — перебір усіх обмінів сусідів — 📎.

## Мапа на каталог
- Є: `cell-click` · `keyboard-controls` · `line-match-clear` · `gravity-fall` · `spawn-random-cell` · `chain-reaction` · `no-moves-left` · `event-points`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` (з Bejeweled / Candy Crush) — обмін двох сусідів.
  - `+swap-must-match` «Обмін дозволено лише зі збігом» · entities/legality · 🌱.
  - `+no-moves-detection` (з Bejeweled) — перевірка, що є хоч один хід.

## Пропозиції до словників
- `+cond:would_match` — хід дав би збіг (пробне виконання ходу без застосування): Shariki, Bejeweled, Candy Crush.
- `+card:swap-must-match` — див. «Мапу».

## Джерела
- ⭐ [Wikipedia: Shariki](https://en.wikipedia.org/wiki/Shariki) — обмін сусідів «each swap must result in a match», 3+ в лінію, падіння, кінець без ходів, автор, рік, вплив.
- [ru-Wikipedia: Шарики](https://ru.wikipedia.org/wiki/Шарики) — Кемерово, DOS/Windows, перелік клонів і нащадків.

## Непевне
- (?) Розмір поля і кількість кольорів; формула очок; чи є рівні або прогрес-смуга.
- (?) Чи нараховуються окремі бонуси за каскад — каскад сам випливає з правил падіння.
- (?) Вікна й меню оригіналу (DOS).
