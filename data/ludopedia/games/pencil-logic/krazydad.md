---
title: Krazydad (банк друкованих пазлів)
slug: krazydad
aka: [KrazyDad, krazydad.com, Logic Pic]
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
year: null
platforms: [web, paper]
links:
  - {kind: official, url: "https://www.krazydad.com/sudoku/", best: true, note: "Krazydad Sudoku: 7 рівнів Easy…Insane, до 26 томів на рівень, буклет з 8 пазлів + підказки + відповіді, друк 1 або 4 на сторінку"}
  - {kind: official, url: "https://www.krazydad.com/", note: "головна: жанри (Sudoku-варіанти, Konograms, Kakuro, Akari, Train Tracks…), daily puzzles, безкоштовно без реклами"}
  - {kind: play, url: "https://www.krazydad.com/play/", note: "інтерактив: Konograms, Killer Sudoku"}
  - {kind: other, url: "https://apps.apple.com/us/app/id867654947", note: "Nonogram — IQ Logic Pic Puzzle (iOS): daily levels, hint packs, монети, підписка"}
stage: v1
coverage: 55
mechanics: [level-bank, level-rating, difficulty-levels, difficulty-select, puzzle-select, daily-puzzle, satisfy-constraints, completion-detection, level-solver, +printable-booklet, +solve-order-hint, +visited-mark]
proposes: ["+feature:print-layout", "+feature:solve-order-hint", "+window:volume-select", "+card:printable-booklet", "+card:solve-order-hint"]
author: opus
date: 2026-11-09
---

# Krazydad — не гра, а банк пазлів: рівні складності, томи, друк буклетами й підказка «порядок розвʼязання»

## Суть
Сайт Jim Bumgardner з тисячами безкоштовних пазлів багатьох жанрів сімʼї, переважно для друку. Нової механіки на полі нема — правила жанрів описані в їхніх файлах. Файл фіксує **оболонку банку**: як пазли розкладено за рівнями й томами, як друкуються буклети і як влаштована підказка — сітка з номерами клітинок у порядку, в якому їх розвʼязав компʼютер. Logic Pic (iOS) — звичайний застосунок нонограм, окремого файла не варт.

## Поле і час
- Поле — як у жанрі (судоку 9×9, Konograms, Kakuro, Akari, Train Tracks тощо).
- Одиниця контенту — **буклет** (том): 8 пазлів + інструкції + сторінка підказок + відповіді в кінці.
- Тома на рівень — до 26; рівнів у судоку — 7.
- Час статичний; на папері — без часу, онлайн — як у жанровому інтерактиві.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пазл | mark | жанр, рівень, номер | розвʼязується за правилами жанру |
| Буклет (том) | container | 8 пазлів, рівень | друкується одним PDF з підказками й відповідями |
| Рівень складності | zone | Easy · Novice · Intermediate · Challenging · Tough · Super-Tough · Insane | визначає техніки, потрібні для розвʼязання |
| Сітка-підказка | mark | номер на клітинку | номер = крок, на якому розвʼязувач заповнив клітинку |
| Відповідь | mark | — | повна сітка в кінці буклета |
| Відвіданий том | mark | — | посилання стає червоним |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, volume)` → ТО `window(custom: «PDF буклета»)`; ЯКЩО `custom: «том уже відкривали»` → ТО `custom: «посилання червоне»` (сторінка: «Volumes you've opened appear in red»).
- КОЛИ `input(print_option)` → ЯКЩО `custom: «1 пазл на сторінку»` → ТО `custom: «великі сітки»`; інакше `custom: «4 на сторінку»`.
- КОЛИ `custom: «гравець застряг»` → ТО `custom: «відкрити сітку-підказку й заповнити клітинку з наступним номером»` — без повного розвʼязку.
- Рівні Easy і Novice: ЯКЩО `difficulty(easy|novice)` → ТО `custom: «є зайві підказки»`.
- Рівень Intermediate: ЯКЩО `difficulty(intermediate)` → ТО `custom: «зайвих підказок нема»`.
- Рівні Tough і Super-Tough: ЯКЩО `difficulty(tough)` → ТО `custom: «потрібні просунуті техніки»` + `custom: «поле для чернетки»`.
- Рівень Insane: ЯКЩО `difficulty(insane)` → ТО `custom: «без вгадування не розвʼязати»`.
- КОЛИ `custom: «новий день»` → ТО `custom: «три daily puzzles — надрукувати або грати онлайн»`.
- КОЛИ `all_constraints_met` → ТО `custom: «звірити з відповіддю в кінці буклета»` (папір).
- Перемога, поразка, рахунок — за жанром; банк сам рахунку не веде.

## Керування і ввід
- Сайт: вибір жанру → рівня → тому; кнопки друку (1 / 4 на сторінку).
- Онлайн-грання — у браузері на компʼютері, телефоні чи iPad (судоку), окремі інтерактиви Konograms і Killer Sudoku.
- Logic Pic: тач-ввід нонограм, daily levels, підказки за монети (сторінка App Store).

## Вікна, меню, HUD
- `main-menu` — список жанрів на головній (+ Books, Play, Daily Puzzles).
- `difficulty-select` — 7 рівнів судоку.
- `+window:volume-select` — сітка томів 1…26 рівня, відвідані червоні.
- `custom-window` — PDF буклета: титул з інструкцією, 8 пазлів, сторінка підказок, відповіді.
- `puzzle-select` — daily puzzles (3 на день).
- `game-screen` — онлайн-інтерактив жанру.
- Переходи: головна → жанр → рівень → том → PDF / play.

## Фічі поза полем
- `puzzle-bank` · `difficulty-presets` (7 рівнів) · `daily-puzzle` (три на день).
- `+feature:print-layout` — 1 або 4 пазли на сторінку; чернетка для важких рівнів.
- `+feature:solve-order-hint` — підказка як номери кроків розвʼязувача.
- Безкоштовно, без реклами, донати (PayPal); друковані книги автора.

## Варіації й родичі
- Жанри банку мають свої файли: [Sudoku](sudoku.md), [Sudoku variants](sudoku-variants.md) (Killer), [Nonogram](nonogram.md) (Konograms), [Kakuro](kakuro.md), [Light Up](light-up.md) (Akari), [Star Battle](star-battle.md) (Two Not Touch).
- Logic Pic (Aliens L.L.C-FZ) — нонограми, тематичні набори за складністю, daily, монети й підписка; механіки — як у [Nonogram](nonogram.md) / [Picross variants](picross-variants.md).
- Інші банки корпусу: Janko (у файлах жанрів), [puzz.link](puzz-link.md), [Tatham Collection](tatham-collection.md) (генератор замість банку).
- **Осі варіацій** банку: генерований на льоту / заздалегідь (Krazydad — томи) · одиниця (пазл / буклет) · підказка (одна клітинка / порядок кроків / техніка) · носій (PDF / інтерактив).

## Цікавинки для курсу
- Генерація PDF-буклета: 4 сітки на сторінку + сторінка відповідей — 📎.
- Сітка «порядку розвʼязання»: логічний розвʼязувач записує номер кроку для кожної клітинки — 🥉 (потрібен розвʼязувач без вгадування).
- Рейтинг складності за найважчою технікою, яку використав розвʼязувач, і розкладка в 7 кошиків — 🥇.
- Позначка «відвідано» для томів (стан у браузері) — 🌱.

## Мапа на каталог
- Є: `level-bank`, `level-rating`, `difficulty-levels`, `difficulty-select`, `puzzle-select`, `daily-puzzle` · `satisfy-constraints`, `completion-detection` ↔ звірка з відповіддю · `level-solver` ↔ сітка-підказка.
- **Нема** → пропозиції карток:
  - `+printable-booklet` «Друк пазлів буклетом з відповідями» · levels/bank · 📎 · слот {per_page: 1|4} — Krazydad.
  - `+solve-order-hint` «Підказка = номери кроків розвʼязувача» · interface/hud · 🥉 — Krazydad.
  - `+visited-mark` «Позначка відкритого тому/рівня» · levels/bank · 🌱 — Krazydad.

## Пропозиції до словників
- `+feature:print-layout` — друк N пазлів на сторінку, чернетка.
- `+feature:solve-order-hint` — сітка з номерами кроків розвʼязання.
- `+window:volume-select` — вибір тому/буклета в межах рівня.
- `+card:printable-booklet`, `+card:solve-order-hint` — див. мапу.

## Джерела
- ⭐ [Krazydad: Sudoku](https://www.krazydad.com/sudoku/) — 7 рівнів і їхній опис, до 26 томів, буклет «eight puzzles, instructions, hints and answers», підказка-нумерація «in the order a computer solved the squares», друк 1/4 на сторінку, відвідані томи червоні.
- [Krazydad](https://www.krazydad.com/) — жанри, daily puzzles (три на день), без реклами, донати, Jim Bumgardner.
- [Krazydad: Play](https://www.krazydad.com/play/) — інтерактивні Konograms і Killer Sudoku.
- [Nonogram — IQ Logic Pic Puzzle](https://apps.apple.com/us/app/id867654947) — App Store (бачив у пошуку): daily levels, hint packs, coin packs, підписка.

## Непевне
- (?) Рік запуску сайту — не перевіряв (`year: null`).
- (?) Чи всі жанри мають ту саму схему 7 рівнів / 26 томів — бачив лише сторінку судоку.
- (?) Інтерфейс онлайн-інтерактиву (undo, олівець, таймер) — сторінка Play його не описує.
- (?) Logic Pic — у черзі без уточнення; ототожнено з iOS-застосунком Aliens L.L.C-FZ за пошуком.
