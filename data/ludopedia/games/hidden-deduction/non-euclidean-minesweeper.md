---
title: Non-Euclidean Minesweeper
slug: non-euclidean-minesweeper
aka: [Неевклідів сапер, Hyperbolic Minesweeper]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: hyperbolic
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2024
platforms: [PC (Windows, Linux/SteamOS, Steam Deck), "iOS (?)"]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3380320/NonEuclidean_Minesweeper/", best: true, note: "CTRL Studio, 23.12.2024; гіперболічні 5-/7-кутні й евклідові 4-/6-кутні сітки, без вгадувань, undo, теми, TATE; скріншоти з вікном нової гри"}
  - {kind: steam, url: "https://store.steampowered.com/app/3432790", note: "безкоштовне демо"}
  - {kind: other, url: "https://export.arxiv.org/abs/2002.09534", note: "E. Kopczyński, «Hyperbolic Minesweeper is in P» (FUN 2021) — чому гіперболічний сапер простіший за класичний"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Non-Euclidean+Minesweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, neighbor-count-clue, no-guess-generation, level-solver, difficulty-levels, field-size-picker, game-settings, seed-share, undo-step, save-autosave, theme-select, tutorial-window, remaining-counter, goal-counter, mode-indicator, gui-render, field-scaling, sound-effects, background-music, achievements-window, game-screen, +hyperbolic-grid, +tiling-select, +mixed-tiling, +poincare-disk-view, +flag-mode-toggle, +portrait-tate-mode, +logic-level-select]
proposes: ["+window:new-game-dialog", "+ui:must-open-counter", "+feature:problem-id", "+feature:tate-mode", "+card:tiling-select", "+card:mixed-tiling", "+card:poincare-disk-view", "+card:flag-mode-toggle", "+card:portrait-tate-mode", "+card:logic-level-select"]
author: opus
date: 2026-11-09
---

# Non-Euclidean Minesweeper — сапер на плитках гіперболічної площини (і на звичайних квадратах/гексах), завжди без вгадувань

## Суть
Класичний [minesweeper](minesweeper.md): відкрити всі безпечні клітини, числа кажуть, скільки мін серед сусідів. Поле — не прямокутник, а **диск із гіперболічних плиток** (4-, 5-, 6-, 7-кутники та змішані 4/5 і 6/7), показаний у моделі «диска», де клітини дрібнішають до краю; для порівняння є евклідові квадрати й гекси. Власний солвер гарантує розвʼязання лише логікою на двох рівнях складності («Easy» і «Hard»). Гравця цікавить не нова логіка підказки, а **інша геометрія сусідства** — у гіперболічній площині кожне кільце клітин помітно більше за попереднє.

## Поле і час
- Вибір тесселяції (вікно нової гри): Hyp 4-gon · Hyp 5-gon · Hyp 6-gon · Hyp 7-gon · Euc 4-gon · Hyp 4/5-gon · Hyp 6/7-gon · Euc 6-gon.
- Розмір поля 1–6 (радіус «диска» з клітин навколо центру): скріншоти — Euc-4 розміру 1 = 81 клітина / 24 міни; Hyp-5 розміру 1 = 51 / 10; Euc-6 розміру 6 = 1063 / 372; Hyp-7 розміру 6 = 1058 клітин.
- Гіперболічне поле малюється в колі (модель диска Пуанкаре (?)): центр великий, край стискається; камеру можна зсувати — на скріншоті центр огляду не збігається з центром поля (?).
- Статичний пазл; годинник у HUD (0:59 на всіх скріншотах — лічить час партії (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | многокутник 4–7 сторін; прихований вміст | відкривається кліком/дотиком |
| Міна | hazard | — | відкрив — помилка (є undo) |
| Число | mark | кількість мін серед сусідів | підказка; сусідство — за ребром і/або вершиною (?) |
| Прапорець | mark | — | ставиться в режимі прапорця (кнопка вгорі) |
| Поле-диск | zone | тесселяція, розмір 1–6 | скінченна ділянка плитки; за межею — сіра «хмара» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «згенерувати розкладку, яку солвер розвʼязує без вгадувань на обраному рівні логіки (Easy/Hard)»`.
- КОЛИ `input(open, c)` → ЯКЩО `not occupied(c, mine)` → ТО `reveal(c)` (число = міни серед сусідів), `counter(must_open, -1)`.
- КОЛИ `input(open, c)` → ЯКЩО `occupied(c, mine)` → ТО `custom: «помилка — наслідок не описано»` (?); `undo` скасовує випадковий хід.
- КОЛИ `input(flag_mode)` → ТО `set_state(input, flag)` / `clear_state(input, flag)` — далі клік ставить прапорець замість відкриття.
- КОЛИ `input(open, c)` → ЯКЩО `state(input, flag)` → ТО `mark(c, flag)`, `counter(mines_left, -1)` / `unmark(c)`, `counter(mines_left, +1)` (?).
- КОЛИ `counter(must_open, ==, 0)` → ТО `win`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(problem_id)` → ТО `custom: «відтворити задачу за її ID»`.
- Гарантія генератора: на кожному кроці існує логічно виведений хід (солвер, «no guessing is required»).
- Перемога: `Must open` = 0. · Поразка: (?) відкрита міна. · Рахунок: (?) час.

## Керування і ввід
- Миша або тач (з 2.6.26): клік — відкрити; кнопка-прапорець вгорі перемикає режим «ставити прапорці» (`mode-toggle`).
- Повзунок збоку/знизу екрана — масштаб або зсув поля (?).
- TATE: портретна орієнтація для повернутого монітора / handheld (з 2.6.29 — без повороту екрана системою).

## Вікна, меню, HUD
- `game-screen`: поле; HUD — `Cells: N`, `Mines: M`, мітка задачі `Hyp-5 Hard-1` (тесселяція-логіка-розмір), `+ui:must-open-counter` «Must open: K» (скільки безпечних лишилось), `timer-elapsed`, `remaining-counter` (судячи зі скріншотів = міни − прапорці (?)), `mode-toggle` (кнопка-прапорець), повзунок (?), кнопка «Menu».
- `+window:new-game-dialog`: превʼю плитки в колі; Tessellation (8 варіантів), Logic (Easy / Hard), Field size (1–6), Game mode (Normal / Customize / Enter problem ID); підсумок «Cells / Mines»; Cancel / OK. У Customize кількість мін змінна (на скріншоті 1058 клітин і 5 мін).
- `tutorial-window` — анімовані туторіали.
- `settings-window` (?) — тема (light / dark / classic / modern), звук, музика.
- `achievements-window` — Steam-досягнення (з 2.7.8).
- `end-screen` — (?) не бачив.

## Фічі поза полем
- `difficulty-presets` = Logic Easy/Hard × Field size 1–6; `custom-difficulty` у режимі Customize.
- `seed-input` — «Enter problem ID»; `undo`; `autosave` прогресу.
- `theme-select` — 4 теми; `music-toggle` (фонова музика з 2.7.0); `localization` — 20 мов.
- Steam Deck / handheld / Ubuntu сумісність, `touch-controls`, TATE-режим.

## Варіації й родичі
- [hyperrogue](../roguelike/hyperrogue.md) — той самий гіперболічний простір {7,3}, там є «Minefield» як земля; [globesweeper](globesweeper.md) — сапер на сфері (додатна кривина) — пара «сфера ↔ гіпербола».
- [hexcells](hexcells.md), [tametsi](tametsi.md), [minesweeper-dimensions](minesweeper-dimensions.md) — інші «геометрії сусідства» + no-guess.
- Осі варіацій:
  - **кривина поля**: площина (квадрати, гекси) / сфера (Globesweeper) / гіпербола (тут);
  - **плитка**: одна {p,q} / змішана (4/5, 6/7);
  - **сусідство**: ребро / ребро+вершина;
  - **логіка генератора**: випадкова / no-guess Easy / no-guess Hard.

## Цікавинки для курсу
- Поле як граф сусідства: той самий код сапера працює на квадратах, гексах і будь-якій плитці — 🥉.
- Генерація гіперболічної плитки {p,q} кільцями навколо центру (комбінаторно, без координат) — 🥇.
- Рендер у диску Пуанкаре з панорамуванням (перетворення Мебіуса) — 👑.
- No-guess генератор із двома рівнями логіки: Easy — висновки з однієї підказки, Hard — з пар/множин підказок (моє прочитання (?)) — 🥇.
- ID задачі → відтворення генерації (seed) — 📎.
- Чому гіперболічний сапер «у P» (Kopczyński, FUN 2021): обмежена ширина дерева локальних обмежень — 👑 як тема для доповіді.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` · `no-guess-generation` + `level-solver` ↔ власний солвер · `difficulty-levels` ↔ Easy/Hard · `field-size-picker` ↔ 1–6 · `game-settings` · `seed-share` ↔ problem ID · `undo-step` · `save-autosave` · `theme-select` · `tutorial-window` · `remaining-counter` · `goal-counter` ↔ Must open · `mode-indicator` ↔ кнопка-прапорець · `gui-render` · `field-scaling` ↔ великі поля на 1000+ клітин · `sound-effects` + `background-music` · `achievements-window` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+hyperbolic-grid` (вже пропонована HyperRogue) — плитка {p,q} як граф.
  - `+tiling-select` «Вибір тесселяції поля» · levels/generation · 📎 · слот {tilings: list}.
  - `+mixed-tiling` «Змішана плитка з двох типів многокутників» · levels/generation · 🥈.
  - `+poincare-disk-view` «Рендер гіперболічного поля в диску з панорамуванням» · interface/graphics · 👑.
  - `+flag-mode-toggle` «Кнопка: клік ставить прапорець замість відкриття» · interface/input · 🌱.
  - `+portrait-tate-mode` «Портретна розкладка інтерфейсу» · interface/settings · 📎.
  - `+logic-level-select` «Рівень логіки no-guess генератора» · levels/generation · 🥈.

## Пропозиції до словників
- `+window:new-game-dialog` — одне вікно: тесселяція + логіка + розмір + режим.
- `+ui:must-open-counter` — лишилось безпечних клітин (на відміну від `remaining-counter` мін).
- Примітка: `field: hyperbolic` (⏳ у `classes.md`) — друге вживання в корпусі після HyperRogue.
- `+feature:problem-id` — відтворення задачі за кодом; `+feature:tate-mode` — портретна орієнтація.

## Джерела
- ⭐ [Steam: Non-Euclidean Minesweeper](https://store.steampowered.com/app/3380320/NonEuclidean_Minesweeper/) — опис і фічі (Escher, власний рендер і солвер, 5-/7-кутні гіперболічні, 4-/6-кутні евклідові, undo, autosave, 4 теми, тач, TATE), CTRL Studio, 23.12.2024; 5 скріншотів — HUD (Cells/Mines/Must open, таймер, лічильник, кнопка-прапорець) і вікно нової гри.
- [Steam API: новини гри](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3380320&count=40&maxlength=1500) — версії 2.6.20–2.7.25: тач, Steam Deck, Ubuntu, портретні режими, музика, досягнення.
- [Steam: демо](https://store.steampowered.com/app/3432790) — безкоштовне демо (з результатів пошуку).
- [arXiv 2002.09534](https://export.arxiv.org/abs/2002.09534) — Kopczyński, «Hyperbolic Minesweeper is in P».
- YouTube: пошук «Non-Euclidean Minesweeper gameplay».

## Непевне
- (?) Визначення сусідства на гіперболічних плитках (лише за ребром чи й за вершиною) — ні опис, ні скріншоти однозначно не кажуть.
- (?) Що стається при відкритті міни (програш, штраф чи лише пропозиція undo); чи є каскад нулів і акорд-клік.
- (?) Значення правого лічильника HUD (за скріншотами збігається з «міни − прапорці») і призначення повзунка.
- (?) iOS-версія: у видачі пошуку є App Store id1450066199 з тією ж назвою, сторінка віддала 404 — автор і рік не перевірені.
- (?) Модель диска Пуанкаре чи інша проєкція — за виглядом схоже на Пуанкаре.
