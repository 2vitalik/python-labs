---
title: TetraVex
slug: tetravex
aka: [Tetravex, GNOME Tetravex, Тетравекс]
family: falling-match
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 1991
platforms: [PC (Windows), Linux (GNOME)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/TetraVex", best: true, note: "правила, Кнут, Scott Ferguson, NP-повнота, кількість полів"}
  - {kind: official, url: "https://help.gnome.org/users/gnome-tetravex/stable/", note: "довідка GNOME Tetravex: дві половини поля, таймер = рахунок"}
  - {kind: other, url: "https://help.gnome.org/users/gnome-tetravex/stable/move.html", note: "рух плиток: клік-клік, drag, зсув усіх"}
  - {kind: other, url: "https://help.gnome.org/users/gnome-tetravex/stable/size.html", note: "розміри 2×2…6×6, типово 3×3"}
  - {kind: other, url: "https://help.gnome.org/users/gnome-tetravex/stable/hint.html", note: "автоматичне розвʼязання, без рекорду"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetravex+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [drag-drop-piece, cell-click, satisfy-constraints, score-records, field-size-picker, difficulty-levels, game-pause, level-solver, unique-puzzle-generation, time-bonus, swipe-all-shift, game-screen, leaderboard, +edge-match-tiles, +tile-tray-source, +solve-no-record]
proposes: ["+cond:edges_match", "+card:edge-match-tiles", "+card:tile-tray-source", "+feature:solve-no-record"]
author: opus
date: 2026-11-09
---

# TetraVex — розклади квадратні плитки з цифрами на ребрах так, щоб сусідні ребра збігалися

## Суть
Є n×n квадратних плиток; на кожній — чотири цифри, по одній на ребро (плитка поділена діагоналями на 4 трикутники). Плитки лежать на правій половині вікна, а гравець переносить їх на ліву сітку n×n так, щоб кожне дотичне ребро двох сусідів мало однакову цифру. Плитки **не обертаються**. Розвʼязок існує завжди (пазл генерується з готової розкладки); рахунок — час. Задача «чи розкладається набір» у загальному випадку NP-повна.

## Поле і час
- Дві сітки n×n поруч: ліва — цільова, права — «склад» з перемішаними плитками.
- Розмір: 2×2 … 6×6 (GNOME), типово 3×3 (9 плиток).
- Таймер стартує одразу з появою гри; час = рахунок (менше — краще).
- Випадковість лише в генерації (`random: setup`); усе видно (`info: full`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | 4 цифри 0–9 (верх, право, низ, ліво) | переноситься в клітину; не обертається |
| Клітина цільової сітки | zone | позиція | тримає одну плитку; перевіряє ребра з сусідами |
| Клітина складу | supply | позиція | початкове місце плиток; можна класти назад |
| Ребро | mark | дві цифри | виконане, якщо цифри сусідніх плиток рівні |
| Таймер | resource | секунди | рахує від старту; зупиняється на розвʼязку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag tile, cell)` → ЯКЩО `free(cell)` → ТО `move(tile, cell)`.
- КОЛИ `input(drag tile, occupied cell)` → ТО `swap(tile, other)` (?).
- КОЛИ `input(click tile)` → ТО `set_state(tile, selected)`; КОЛИ `input(click cell)` → ЯКЩО `state(tile, selected)` → ТО `move(tile, cell)`.
- КОЛИ `input(shift all, dir)` → ЯКЩО `custom: «у напрямку є вільний ряд/стовпець»` → ТО `shift(all, dir)` — усі плитки лівої сітки зсуваються разом.
- Ходи не остаточні: будь-яку плитку можна забрати назад (`move(tile, store)`).
- КОЛИ `after(move)` → ЯКЩО `custom: «edges_match — цифри на дотичних ребрах сусідніх плиток рівні»` для всіх сусідів → ТО ребро виконане; інакше `custom: «плитка не стає / підсвічується»` (?).
- КОЛИ `all_constraints_met` (ліва сітка повна і всі ребра збігаються) → ТО `win`, таймер зупинено, `score(time)`.
- КОЛИ `input(solve)` → ТО `custom: «автор розкладає плитки сам»`, `win` без запису в рекорди.
- Поразки нема; рахунок — час розвʼязання, менший кращий.

## Керування і ввід
- Миша: клік по плитці → клік по цільовій клітині, або drag-n-drop.
- Зсув усіх плиток лівої сітки в одному напрямку — щоб звільнити край (GNOME; клавіші/кнопки (?)).
- Кнопка «?» внизу праворуч — розвʼязати.
- Меню (кнопка вгорі праворуч): нова гра, розмір, пауза (?), клавіатурні скорочення.

## Вікна, меню, HUD
- `game-screen`: дві сітки (ціль + склад), таймер (`timer-elapsed`), кнопка розвʼязку (`auto-solve-button`), кнопка паузи (`pause-button`) (?).
- `settings-window`/меню: розмір 2×2…6×6 (`custom-difficulty`).
- `leaderboard`: найкращі часи для кожного розміру (?).
- `help-window`: довідка GNOME (правила, рух, розмір, підказки, як виграти).
- `end-screen`: розвʼязано, час, рекорд (?).
- Windows Entertainment Pack: меню Game (New, Pause, Options: розмір, кольори) (?).

## Фічі поза полем
- `custom-difficulty` — розмір сітки.
- `auto-solve` — з виключенням з рекордів.
- `leaderboard-local` — час за розміром (?).
- `pause` — ховає поле, щоб не думати на паузі (?).

## Варіації й родичі
- Edge-matching puzzles: Eternity II (кольори ребер з обертанням, 16×16), MacMahon squares, Kadon-пазли — ширша сімʼя.
- Mahjong Solitaire (`mahjong-solitaire.md`) і Shisen-Sho (`shisen-sho.md`) — інші «класичні Windows-пазли» з плиток у сімʼї.
- Dominoes / Triominoes — збіг числа на стику.
- Межа з `pencil-logic`: поле статичне, обмеження на сусідах — радше пазл обмежень, ніж падаючі блоки.
- **Осі варіацій**: обертання (нема / дозволено — Eternity II) · символи ребер (цифри / кольори / форми) · рамка (нема / кольоровий край) · розмір (2×2…16×16) · підказки (жодних / фіксовані плитки) · рахунок (час / ходи).

## Цікавинки для курсу
- Модель плитки з 4 ребрами й перевірка збігу з сусідами — 🌱.
- Генератор: випадкова сітка цифр на ребрах → нарізати плитки → перемішати (розвʼязок гарантований) — 📎.
- Розвʼязувач backtracking (рядок за рядком, фільтр за лівим і верхнім ребром) — 🥈.
- Генерація з **єдиним** розвʼязком (перевірка солвером, перегенерація) — 🥇.
- Зсув усієї розкладки на 1 клітину — 🌱.
- Варіант з обертанням (×4 стани плитки) — 📎.

## Мапа на каталог
- Є: `drag-drop-piece` · `cell-click` · `satisfy-constraints` · `score-records` + `leaderboard` · `field-size-picker` + `difficulty-levels` · `game-pause` · `level-solver` · `unique-puzzle-generation` (якщо робити варіант з єдиним розвʼязком) · `swipe-all-shift` (зсув усіх) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+edge-match-tiles` «Плитки з мітками на ребрах: сусіди мають збігатися» · game-logic/constraints · 📎.
  - `+tile-tray-source` «Склад плиток поряд із полем, можна класти назад» · interface/input · 🌱.
  - `+solve-no-record` «Автовирішення без запису рекорду» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:edges_match` — мітки на дотичних ребрах сусідніх плиток рівні (TetraVex, Eternity II, доміно).
- `+card:edge-match-tiles` · `+card:tile-tray-source` — див. «Мапа на каталог».
- `+feature:solve-no-record` — авторозвʼязання доступне, але результат не йде в рекорди (GNOME Tetravex).

## Джерела
- ⭐ [Wikipedia: TetraVex](https://en.wikipedia.org/wiki/TetraVex) — правила (ребра збігаються, без обертання), 3×3 типово, натхнення з Кнута (TAOCP т. 1, с. 382), Scott Ferguson, Windows Entertainment Pack 3, NP-повнота (Takenaga, Walsh 2006), 10^(2n(n+1)) полів.
- [GNOME Tetravex: довідка](https://help.gnome.org/users/gnome-tetravex/stable/) — час = рахунок, дві половини поля.
- [GNOME: рух плиток](https://help.gnome.org/users/gnome-tetravex/stable/move.html) — клік-клік або drag, ходи зворотні, зсув усіх плиток лівої частини.
- [GNOME: розмір](https://help.gnome.org/users/gnome-tetravex/stable/size.html) — 2×2…6×6, типово 3×3.
- [GNOME: підказки](https://help.gnome.org/users/gnome-tetravex/stable/hint.html) — «?» розвʼязує, результат не в рекордах.
- YouTube: пошук «tetravex gameplay».

## Непевне
- (?) Рік: Windows Entertainment Pack 3 — 1991 за памʼяттю (черга: 1990); Wikipedia дати не дає.
- (?) Чи дозволяє гра покласти плитку з невідповідними ребрами (WEP — ні, GNOME — так?).
- (?) Обмін плиток при скиданні на зайняту клітину; пауза з прихованим полем; таблиця рекордів за розміром.
- (?) У довідці GNOME ліва/права половини описані по-різному на різних сторінках («place on the left» vs «move from one side to the other»).
