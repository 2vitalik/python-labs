---
title: Polimines / Polimines 2
slug: polimines
aka: [Polimines Deluxe]
family: hidden-deduction
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2022
platforms: [PC (Windows, macOS, Linux), Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2328730/", best: true, note: "Polimines 2: 60 ручних рівнів різної форми, без вгадувань, без таймерів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1892790/", note: "Polimines (1): 30 рівнів, 29.03.2022"}
  - {kind: official, url: "https://moltergames.com/", note: "Molter Games — обидві гри"}
  - {kind: other, url: "https://buried-treasure.org/?p=4837", note: "огляд з поясненням правил: рядкові підказки, числа під видаленими, розриви поля"}
  - {kind: other, url: "https://steamcommunity.com/app/2328730/reviews/?browsefilter=toprated", note: "огляди P2: лічильник помилок, нотатки малюванням"}
  - {kind: other, url: "https://steamcommunity.com/app/1892790/reviews/?browsefilter=toprated", note: "огляди P1: інверсія кнопок, що відміняється"}
  - {kind: other, url: "https://ec.nintendo.com/AU/en/titles/70010000083615", note: "Polimines Deluxe (Switch), 90 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Polimines+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, run-length-clues, neighbor-count-clue, satisfy-constraints, completion-detection, level-bank, sequential-levels, hover-highlight, theme-select, achievements-window, game-screen, +clue-gaps-break-line, +hidden-clue-under-safe, +mistake-counter, +invert-buttons, +free-draw-notes]
proposes: ["+cond:same_segment", "+effect:mark_safe", "+feature:invert-buttons", "+feature:free-draw-notes", "+card:clue-gaps-break-line", "+card:hidden-clue-under-safe", "+card:invert-buttons"]
author: opus
date: 2026-11-09
---

# Polimines — нонограма, у якій «зафарбовані» клітини — міни, а під стертими ховаються числа сапера

## Суть
Поле — сітка плиток довільної форми з числами біля рядків і стовпців, як у нонограмі: скільки «бомб» іде підряд у лінії. Гравець позначає плитку як бомбу або видаляє як безпечну; під видаленою може відкритись число сапера — скільки бомб серед 8 сусідів. Розриви у формі поля обривають дію рядкових чисел, тож одна підказка може стосуватись лише шматка лінії. Рівні ручні, кожен розвʼязний без вгадувань; таймерів нема.

## Поле і час
- Квадратна сітка, але форма рівня довільна: дірки й розриви ділять рядки/стовпці на відрізки.
- Підказки рядків і стовпців — поза полем або в розривах; одна підказка може слугувати двом рядкам і стовпцю під ними (огляд Buried Treasure).
- Шари: прихований стан (бомба / безпечна) + числа-нонограми ліній + числа сапера під безпечними + «?» (P1, пізніші рівні; суть — (?)).
- Статичний пазл без таймера; P1 — 30 рівнів, P2 — 60, Deluxe (Switch) — 90.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита плитка | static | прихований стан | позначається як бомба або видаляється |
| Бомба (позначена) | mark | — | ціль; для перемоги треба позначити всі |
| Видалена плитка | mark | — | безпечна; може відкрити число |
| Число сапера | mark | n | бомб серед 8 сусідів (діагоналі теж) |
| Підказка лінії | zone | послідовність довжин | блоки бомб підряд у відрізку лінії |
| Розрив поля | static | — | обриває дію підказки лінії |
| «?» | mark | — | зʼявляється в пізніших рівнях; правило не встановлено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(mark_bomb, c)` → ЯКЩО `custom: «c — бомба»` → ТО `mark(c, bomb)`, `counter(bombs_left, -1)` (?).
- КОЛИ `input(delete, c)` → ЯКЩО `custom: «c безпечна»` → ТО `reveal(c)`; ЯКЩО під нею число → ТО показати `adjacent_count(c, bomb, ==, n)` за 8 сусідами.
- КОЛИ `input(*, c)` → ЯКЩО відповідь хибна → ТО `counter(mistakes, +1)`; поразки нема (P2: «не карають за хибні», треба позначити всі бомби).
- Підказка лінії: `run_lengths(segment)` — довжини блоків бомб у відрізку лінії = послідовність чисел.
- Відрізок: `custom: «підказка не переходить через розрив поля»` — лінія ділиться формою рівня.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «усі бомби позначено»` → ТО `win`, `next_level`.
- Перемога: позначено всі бомби. · Поразка: нема. · Рахунок: лічильник помилок (досягнення «0 помилок на всіх рівнях»).
- Гарантія дизайну: кожен рівень розвʼязний без вгадувань.

## Керування і ввід
- Ліва / права кнопка миші — «бомба» / «видалити»; перемикач інвертує кнопки («щоб було як у пікросі»).
- Наведення на клітину показує, які зовнішні числа на неї впливають.
- P1: зелена позначка бомби відміняється, жовта «видалено» — ні (огляд).
- P2: нотатки малюванням мишею (лише чорний і білий) — крапку не поставиш, треба «почеркати».
- Нема виділення кількох клітин чи протягування по лінії (огляди).

## Вікна, меню, HUD
- `game-screen`: поле довільної форми, числа рядків і стовпців, числа сапера на видалених, `mistake-counter` (P2).
- `level-select` / `puzzle-select`: 30 / 60 рівнів; пропускати рівні не можна (огляд) (?).
- `settings-window`: інверсія кнопок, кольори (налаштовувані), звук (?); P1 забував налаштування після закриття (огляд).
- `end-screen` рівня (?).
- HUD: `line-clue` (числа ліній), `hover-highlight` впливу підказок, `mistake-counter`.

## Фічі поза полем
- `puzzle-bank` ручних рівнів, `levels-sequential`; без таймерів, «relaxing atmosphere».
- `achievements` Steam (у т.ч. «0 помилок на всіх рівнях», «30 з 60»), картки Steam (P2).
- `theme-select`/кольори; `+feature:invert-buttons`; `+feature:free-draw-notes` (P2).
- `localization`: EN, ES (P2 — з озвученням).

## Варіації й родичі
- Polimines (2022, 30 рівнів) → Polimines 2 (2023, 60 рівнів, нові механіки, більші поля) → Polimines Deluxe (Switch, 90 рівнів — імовірно обидві разом (?)).
- Родичі: [lizzi-crossing](lizzi-crossing.md) (та сама пара нонограма+сапер, але з героєм і генератором), [sudo-sweep](sudo-sweep.md) (сапер у парі з судоку), [hexcells](hexcells.md) і [tametsi](tametsi.md) (лінійні підказки-кількості), [14-minesweeper-variants](14-minesweeper-variants.md) (правило-варіант «довжини блоків»).
- Нонограма без сапера — `pencil-logic/nonogram.md`.
- Осі варіацій: **лінійна підказка** кількість (Hexcells) / довжини блоків (Polimines) / сума; **число в клітині** немає / сапер-8; **форма поля** прямокутник / довільна з розривами; **помилка** лічильник / смерть.

## Цікавинки для курсу
- Перевірка рядка нонограми (`run_lengths`) на відрізках між розривами — 📎.
- Одне поле — два види обмежень (лінії + 8-сусідство) і спільний солвер — 🥈.
- Форма рівня як маска: лінії ріжуться дірками — 🌱.
- Інверсія кнопок миші в налаштуваннях — 🌱.
- Ручний дизайн «без вгадувань» → автоматична перевірка солвером — 🥇.

## Мапа на каталог
- Є: `cell-click` · `run-length-clues` ↔ числа рядків/стовпців · `neighbor-count-clue` ↔ числа сапера · `satisfy-constraints` · `completion-detection` · `level-bank` + `sequential-levels` · `hover-highlight` ↔ які підказки впливають · `theme-select` ↔ кольори · `achievements-window` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+clue-gaps-break-line` «Розрив у формі поля обриває підказку лінії» · game-logic/constraints · 🌱.
  - `+hidden-clue-under-safe` «Число відкривається лише під безпечною клітиною» · game-logic/constraints · 🌱.
  - `+invert-buttons` «Інверсія кнопок миші» · interface/settings · 🌱.
  - `+mistake-counter`, `+free-draw-notes` — як у Hexcells/Tametsi; «без вгадувань» тут — ручний дизайн, картка `no-guess-generation` (генератор) не підходить.

## Пропозиції до словників
- `+cond:same_segment(a, b)` — клітини в одному відрізку лінії (не розділені розривом).
- `+effect:mark_safe` — відповісти «безпечна» з перевіркою (як у Hexcells; тут — «видалити»).
- (`line-clue` уже є в ui-elements — лише вжиток: числа ліній за краєм і в розривах.)
- `+feature:invert-buttons` · `+feature:free-draw-notes` — нотатки малюванням поверх поля.

## Джерела
- ⭐ [Steam: Polimines 2](https://store.steampowered.com/app/2328730/) — нонограма + сапер, 60 ручних рівнів різної форми, «every level … can be solved without guessing», без таймерів; Molter Games, 01.11.2023.
- [Steam: Polimines](https://store.steampowered.com/app/1892790/) — 30 рівнів, «different level shapes allow new mechanics to emerge», 29.03.2022.
- [Buried Treasure: огляд](https://buried-treasure.org/?p=4837) — правила: блоки бомб підряд у лінії, числа під видаленими (8 сусідів), розриви поля, «?».
- [Steam-огляди P2](https://steamcommunity.com/app/2328730/reviews/?browsefilter=toprated) і [P1](https://steamcommunity.com/app/1892790/reviews/?browsefilter=toprated) — лічильник помилок, інверсія кнопок, нотатки, наведення.
- [Molter Games](https://moltergames.com/) · [Nintendo eShop: Polimines Deluxe](https://ec.nintendo.com/AU/en/titles/70010000083615) — 90 рівнів.

## Непевне
- (?) Що робить «?» (P1 пізні рівні; у P2 «?» застосовується в обидва боки — огляд), і які саме «нові механіки» додає P2.
- (?) Чи є лічильник лишених бомб; чи помилкова відповідь лишає клітину закритою.
- (?) Розміщення підказок усередині поля (у розривах) — з одного огляду.
- (?) Deluxe = P1 + P2 — висновок з кількості рівнів (30+60=90).
- (?) Вигляд меню, вибір рівня, екран кінця рівня — не бачив.
