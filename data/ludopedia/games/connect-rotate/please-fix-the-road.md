---
title: Please Fix The Road
slug: please-fix-the-road
aka: []
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [Windows, macOS, Linux, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1383250/Please_Fix_The_Road/", best: true, note: "опис: інструменти, типи шляхів, мандрівники; ARIELEK, 10.06.2022"}
  - {kind: other, url: "https://ladiesgamers.com/please-fix-the-road-review/", note: "огляд: ліміт інструментів і плиток, 150 рівнів, undo, підказки, два виходи"}
  - {kind: other, url: "https://www.gameinformer.com/review/please-fix-the-road/clever-construction", note: "огляд Switch: список ходів унизу ліворуч у фіксованому порядку, підказка, 160 пазлів"}
  - {kind: other, url: "https://gameluster.com/review-please-fix-the-road-mentally-under-construction/", note: "огляд: групи плиток різних форм, Ctrl+Z, пропуск пазла, зум"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Please+Fix+The+Road+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tile-rotate, pipe-connectors, cursor-place, multi-select, connectivity-check, destructible-blocks, undo-step, skip-level, sequential-levels, tutorial-window, field-scaling, game-screen, +ordered-tool-list, +tool-budget, +area-copy, +area-swap, +area-push, +tile-height-tool, +multi-network-types, +traveller-by-terrain, +step-hint-replay, +solve-animation]
proposes: ["+cond:order_next", "+ui:tool-charges", "+ui:tool-order-list", "+card:ordered-tool-list", "+card:tool-budget", "+card:area-transform-tools"]
author: opus
date: 2026-11-09
---

# Please Fix The Road — полагодь дорогу заданим набором інструментів у заданому порядку: встав, підірви, поверни, скопіюй, підніми плитки, щоб авто, човни, потяги й тварини дісталися до прапорця

## Суть
Вид згори на маленьку ділянку сітки з поламаними дорогами, річками, стежками й коліями; мандрівники (авто, човни, потяги, кошенята, ламі) чекають, щоб доїхати з точки A до прапорця B. На рівень дано обмежений набір інструментів і запасних плиток, а список дій у кутку ще й **фіксує порядок**, у якому їх треба застосувати. Інструменти діють не лише на плитку, а й на групу плиток певної форми: повернути, скопіювати, поміняти місцями, зсунути, підняти чи опустити ділянку. Ядро — обмежений «скрипт» трансформацій сітки, після якого маршрути мають скластися; рівень пройдено, коли виконано всі кроки й мандрівники доїхали.

## Поле і час
- Квадратна сітка плиток-сегментів (дорога, річка, стежка, колія, порожня земля); у плиток є висота, яку змінюють «підняти» / «опустити» (?).
- Камеру можна зумити й прокручувати.
- Статичний пазл: жодного таймера; після останнього кроку — анімація проїзду, дорога «згортається», наступний рівень.
- 150 рівнів за більшістю оглядів (Game Informer — 160); складність росте до сотень, легші рівні перемежовують складні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сегмент дороги / річки / стежки / колії | conduit | тип мережі, виходи, висота (?) | зʼєднується з сусіднім того ж типу |
| Порожня земля | terrain | — | місце під вставку |
| Старт (точка A) | source | тип мандрівника | звідси вирушає мандрівник |
| Прапорець (точка B) | sink | — | ціль; з двох прапорців досить шляху до одного |
| Авто · човен · потяг | object | мережа: дорога / річка / колія | їде лише своєю мережею |
| Тварина (кіт, пес, лама, корова, олень) | neutral | мережа: стежка (?) | іде до свого прапорця |
| Запасна плитка | supply | тип, кількість | ставиться інструментом «вставити» |
| Інструмент | supply | вид, заряди, місце в черзі | одна дія над плиткою або групою плиток певної форми |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tool, area)` → ЯКЩО `not custom: «інструмент — наступний у списку дій рівня»` → ТО `block`.
- КОЛИ `input(insert, cell)` → ЯКЩО `free(cell)` → ТО `place(player, spare_tile)`, `take(player, spare_tile)`.
- КОЛИ `input(destroy, area)` → ТО `explode(area)`, `set_cell(area, empty_ground)`.
- КОЛИ `input(rotate, area)` → ТО `rotate(area, 90)`.
- КОЛИ `input(copy, area)` → ТО `clone(area)`, `custom: «копію покласти в іншому місці»`.
- КОЛИ `input(swap, area_a)` → ТО `swap(area_a, area_b)`.
- КОЛИ `input(raise, area)` → ТО `set_value(area, height+1)`; КОЛИ `input(lower, area)` → ТО `set_value(area, height-1)`.
- КОЛИ `input(push, area)` → ТО `push(area)`; КОЛИ `input(move, area)` → ТО `move(area, to)`.
- КОЛИ `after(tool)` → ТО `counter(steps_left, -1)`.
- КОЛИ `counter(steps_left, ==, 0)` → ЯКЩО `path_exists(start, flag)` для кожного мандрівника своєю мережею → ТО `win`, `custom: «мандрівники їдуть, дорога згортається»`, `next_level`; інакше `custom: «рівень не зараховано — undo»`.
- КОЛИ `custom: «перевірка шляху»` → ЯКЩО `not same(traveller, segment, network)` → ТО `block` (човен не їде дорогою).
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(hint)` → ТО `custom: «відкотити правильні кроки й показати перший крок розвʼязку»`.
- КОЛИ `input(skip)` → ТО `next_level`.
- Перемога: усі дії списку виконано, і кожен мандрівник має шлях до прапорця своєю мережею. Поразки нема — лише undo/рестарт. Рахунку нема (?).

## Керування і ввід
- Миша або геймпад (повна підтримка): вибрати інструмент зі списку, навести форму-рамку на ділянку, застосувати; для «копіювати» / «поміняти» — друга точка.
- Ctrl+Z — undo; кнопки підказки й пропуску рівня; зум і прокрутка мапи.
- Навчання змушує виконати дію, а не лише показує.

## Вікна, меню, HUD
- `main-menu` — «чисте» меню з простою навігацією (огляд Gameluster).
- `tutorial-window` — інтерактивне навчання в перших рівнях.
- `game-screen`: ділянка сітки, список потрібних дій унизу ліворуч (`tool-order-list`, `tool-palette`) з кількістю (`tool-charges`), маркери маршрутів: прапорці-цілі, лінії руху, чорний слід; `undo-button`, `hint-button`, `zoom-control`.
- Кінець рівня — анімація проїзду й згортання дороги, без окремого екрана рахунку (?).
- `level-select` / `settings-window` — не описані в джерелах (?).

## Фічі поза полем
- `levels-sequential` ~150 рівнів; `skip-level` (огляд Gameluster); `hint` покроковий (додано оновленням); `undo`.
- `achievements` і `cloud-save` (Steam); `gamepad-support`; `localization` — 103 мови.

## Варіації й родичі
- Корпус: [Railbound](railbound.md) (обмежений набір рейок, маршрут до цілі) · [Train Valley](train-valley.md) і [Metro: Iron Horse](metro-iron-horse.md) (колії між станціями) · [Infinity Loop](infinity-loop.md) (обертання до звʼязності) · [Railroad Ink](../board-digital/railroad-ink.md) (кілька мереж: дороги й колії) · [Townscaper](../build-sim/townscaper.md) (затишна іграшкова сітка).
- Осі варіацій: **інструмент** — одна плитка / група форми · **порядок дій** — вільний / зафіксований списком · **мережі** — одна / кілька, кожна для свого мандрівника · **ресурс** — плитки й заряди інструментів.

## Цікавинки для курсу
- Список дій рівня з фіксованим порядком і зарядами: рівень = «скрипт», гравець лише обирає, **де** застосувати — 📎.
- Трансформації групи плиток певної форми: поворот, копія, обмін, зсув — 🥉 (операції над підматрицею з обертанням портів).
- Кілька мереж на одній сітці (дорога, річка, колія, стежка) і мандрівник, що їде лише своєю, — BFS за типом — 📎.
- Висота плитки як параметр звʼязності (підняти / опустити) — 🥉 (?).
- Розвʼязувач: перебір місць застосування для кожного кроку списку — 🥈.
- Підказка, що відкочує до першого правильного кроку, — 🌱.

## Мапа на каталог
- Є: `tile-rotate` · `pipe-connectors` · `cursor-place` (вставити плитку) · `multi-select` (група плиток) · `connectivity-check` (шлях A → B) · `destructible-blocks` (підірвати) · `undo-step` · `skip-level` · `sequential-levels` · `tutorial-window` · `field-scaling` (зум, прокрутка) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+ordered-tool-list` «Дії рівня в заданому порядку» · game-logic/legality · 📎.
  - `+tool-budget` «Обмежений набір інструментів і плиток на рівень» · game-logic · 🌱.
  - `+area-copy` «Скопіювати ділянку сітки» · entities/state · 📎.
  - `+area-swap` «Поміняти дві ділянки місцями» · entities/move · 📎.
  - `+area-push` «Зсунути ділянку» · entities/move · 📎.
  - `+tile-height-tool` «Підняти / опустити плитку» · entities/state · 🌱.
  - `+multi-network-types` «Кілька мереж на одній сітці» · entities/state · 📎.
  - `+traveller-by-terrain` «Мандрівник лише своєю мережею» · entities/legality · 🌱.
  - `+step-hint-replay` «Покрокова підказка з відкатом» · interface/hud · 🌱.
  - `+solve-animation` «Анімація проходження розвʼязку» · interface/graphics · 🌱.

## Пропозиції до словників
- `+cond:order_next(action)` — дія / обʼєкт — наступний у заданій рівнем черзі (тут — інструмент зі списку; Railbound — вагон за номером).
- `+ui:tool-charges` — скільки разів лишилось застосувати інструмент; `+ui:tool-order-list` — список дій рівня з поточною підсвіченою.
- `+card:ordered-tool-list`, `+card:tool-budget`, `+card:area-transform-tools` (сімʼя: поворот / копія / обмін / зсув ділянки) — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Please Fix The Road](https://store.steampowered.com/app/1383250/Please_Fix_The_Road/) — опис: обмежений набір інструментів, «insert, destroy, rotate, copy, swap, raise, lower, push or move», дороги, річки, стежки, колії, мандрівники; кілька плиток одразу.
- [LadiesGamers](https://ladiesgamers.com/please-fix-the-road-review/) — ліміт інструментів і плиток, 150 рівнів, undo/rewind, підказки після оновлення, два виходи, миша / геймпад.
- [Game Informer](https://www.gameinformer.com/review/please-fix-the-road/clever-construction) — список ходів унизу ліворуч, фіксований порядок, підказка відкочує кроки, 160 пазлів.
- [Gameluster](https://gameluster.com/review-please-fix-the-road-mentally-under-construction/) — групи плиток різних форм, Ctrl+Z, пропуск, зум, маркери маршрутів, навчання.
- YouTube: пошук «Please Fix The Road gameplay».

## Непевне
- (?) Що саме дає висота (мости над річкою? перепад, через який не проїхати) — джерела називають лише «raise, lower».
- (?) Тварини ходять стежками — припущення з переліку мереж; не перевірено.
- (?) Кількість рівнів: 150 (LadiesGamers, Gameluster, The Guardian у пошуку) проти 160 (Game Informer).
- (?) Чи можна пропускати рівні без ліміту; чи є вибір рівня й мапа світів — не описано.
- (?) Платформи: Steam (Windows/macOS/Linux) 2022 — точно; Switch — за оглядом Game Informer; PS5 — лише сторінка Metacritic у пошуку.
- (?) Розробник один — ARIELEK / Ariel Jurkowski (за результатами пошуку).
