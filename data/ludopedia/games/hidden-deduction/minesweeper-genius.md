---
title: Minesweeper Genius
slug: minesweeper-genius
aka: [«Геній-сапер»]
family: hidden-deduction
also: [pencil-logic]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2018
platforms: [iOS, Xbox One, Xbox Series X|S, Switch]
links:
  - {kind: other, url: "http://www.148apps.com/reviews/minesweeper-genius-review/", best: true, note: "огляд 148Apps: Аристотель іде полем, числа на рядках/стовпцях, зелені й фіолетові стрілки, джамп-пади, прапорці"}
  - {kind: other, url: "https://www.imore.com/minesweeper-genius-modernizes-classic-computer-game", note: "огляд iMore: хід на сусідню клітину, long-press = прапорець, процедурні рівні, 3 зірки, iCloud"}
  - {kind: official, url: "https://xbox.com/en-US/games/store/1/9NQF1WZL3RC9", note: "Xbox Store: MGaia / Blowfish Studios, 12.02.2019, «дійти до порталу», генератор нескінченних рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Minesweeper+Genius+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [line-sum-clue, reach-exit, touch-death, no-guess-generation, sequential-levels, save-progress, game-screen, end-screen, achievements-window, +avatar-on-minefield, +line-shift-tile, +line-swap-tile, +jump-pad, +stars-by-mistakes]
proposes: ["+effect:rotate_line", "+effect:swap_lines", "+effect:jump_over", "+card:avatar-on-minefield", "+card:line-shift-tile", "+card:line-swap-tile", "+card:jump-pad", "+card:stars-by-mistakes"]
author: opus
date: 2026-11-09
---

# Minesweeper Genius — сапер з аватаром: веди Аристотеля мінним полем до порталу за числами рядків і стовпців

## Суть
Замість кліку будь-куди гравець **веде персонажа** (Аристотель із мітлою) по сусідніх клітинах до порталу; кожна клітина, на яку він стає, мусить бути безпечною. Підказки — не числа сусідів, а **кількість мін у кожному рядку й стовпці**, написана за краєм поля (як у Picross / Voltorb Flip). Спецплитки зсувають і міняють місцями рядки/стовпці разом із мінами — числа на краю перераховуються, і вже виведені міни треба відстежувати. Автори називають гру сумішшю сапера, судоку й японського кросворда, без вгадувань.

## Поле і час
- Квадратна сітка «кімнати» з фіксованою кількістю рядків і стовпців; ранні кімнати малі, далі більші, з більшою кількістю мін і нових плиток.
- Шари: прихований вміст (міна / порожньо / спецплитка) + лінійні числа поза полем + прапорці гравця.
- Покроковий: тік = один крок аватара; без таймера (?).
- Рівні процедурні (iMore, Xbox Store: «unlimited number of random levels»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аристотель | player | — | крок на сусідню клітину; на міні — вибух |
| Закрита клітина | static | прихований вміст | відкривається, коли на неї стає аватар (?) |
| Міна | hazard | — | крок на неї → вибух, спроба провалена |
| Лінійне число | mark | n = міни в рядку / стовпці | підказка за краєм поля; змінюється після зсуву ліній |
| Прапорець | mark | — | позначка гравця «тут міна» |
| Портал | static | — | вихід: дійти → рівень пройдено |
| Зелена стрілка | switch | рядок або стовпець, напрям | переносить крайню клітину лінії на протилежний бік (циклічний зсув) |
| Фіолетова стрілка | switch | пара рядків / стовпців | міняє місцями цілі рядки або стовпці |
| Джамп-пад | terrain | напрям | аватар перестрибує рядок/стовпець (iMore: «на клітину вперед») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` → ТО `move(player, dir)`, `reveal(target)` (?).
- КОЛИ `enter(player, mine)` → ТО `explode(player)`, `custom: «спроба провалена, зірки знижуються»`, `restart` (?).
- Лінійне число: `custom: «n = кількість мін у рядку / стовпці»` — `adjacent_count` тут не діє, сусідів ніхто не рахує.
- КОЛИ `input(flag, c)` → ТО `mark(c, flag)`.
- КОЛИ `enter(player, green_arrow)` → ТО `custom: «циклічний зсув рядка/стовпця на 1: крайня клітина — на інший бік»`, числа ліній перераховуються.
- КОЛИ `enter(player, purple_arrow)` → ТО `custom: «обміняти місцями два рядки або стовпці разом із вмістом»`.
- КОЛИ `enter(player, jump_pad)` → ТО `custom: «перестрибнути через клітину/лінію, не стаючи на неї»`.
- КОЛИ `enter(player, portal)` → ТО `win`, `window(end-screen)` з зірками.
- КОЛИ `level_start` → ТО `custom: «згенерувати кімнату, прохідну без вгадувань»`.
- Перемога: дійти до порталу. · Поразка: стати на міну (спроба, не гра). · Рахунок: до 3 зірок за рівень, усі три — лише якщо не вибухнув жодного разу.

## Керування і ввід
- Тач: тап по сусідній з Аристотелем клітині — крок туди; довге натискання — прапорець.
- Xbox: геймпад (?) — рух і прапорець кнопками.
- Шлях не задається наперед: кожен крок — окреме рішення «тут безпечно».

## Вікна, меню, HUD
- `game-screen`: кімната, числа рядків/стовпців по краях, аватар, портал, прапорці.
- `end-screen`: рівень пройдено, 1–3 зірки.
- `level-select` або карта рівнів (?).
- `achievements-window` (Xbox achievements).

## Фічі поза полем
- Процедурний генератор нескінченних рівнів; поступове введення нових плиток (`onboarding-hints` (?)).
- `stars-rating` за рівень (3 — без вибухів).
- `cloud-save` (iCloud на iOS, Xbox cloud saves), `achievements`.

## Варіації й родичі
- [minesweeper](minesweeper.md) — оригінал: курсор, числа сусідів; тут аватар і числа ліній.
- [voltorb-flip](voltorb-flip.md) — теж числа на рядках/стовпцях; [hexcells](hexcells.md) — лінійні підказки на гекс-полі; [mined-out](mined-out.md) і [lizzi-crossing](lizzi-crossing.md) — аватар, що йде мінним полем; [triangulation](triangulation.md).
- Осі варіацій: **хто відкриває** курсор / аватар (крок = відкриття) · **підказка** сусіди / рядок і стовпець · **поле** статичне / з плитками, що переставляють лінії · **помилка** кінець гри / втрата зірок.

## Цікавинки для курсу
- Аватар на мінному полі: відкриття лише сусідньої клітини, шлях до виходу — 🌱.
- Лінійні числа замість сусідських (рахунок мін у рядку/стовпці) — 🌱.
- Циклічний зсув рядка і обмін двох рядків разом зі схованим вмістом + перерахунок підказок — 📎.
- Генератор кімнат «без вгадувань» для аватара, що йде шляхом (дедукція з урахуванням досяжності й майбутніх зсувів) — 🥇.
- Зірки за рівень за кількістю вибухів — 🌱.

## Мапа на каталог
- Є: `line-sum-clue` ↔ числа рядків і стовпців · `reach-exit` ↔ портал · `touch-death` ↔ крок на міну · `no-guess-generation` ↔ «no guessing or luck» · `sequential-levels` · `save-progress` ↔ iCloud · `game-screen` · `end-screen` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+avatar-on-minefield` «Аватар іде мінним полем: відкриття = крок» · entities/move · 🌱.
  - `+line-shift-tile` «Плитка циклічно зсуває рядок/стовпець» · entities/interact · 📎 · слот {axis: row|col}.
  - `+line-swap-tile` «Плитка міняє місцями два рядки/стовпці» · entities/interact · 📎.
  - `+jump-pad` «Плитка-трамплін: перестрибнути клітину» · entities/move · 🌱.
  - `+stars-by-mistakes` «1–3 зірки за рівень за кількістю помилок» · interface/results · 🌱.

## Пропозиції до словників
- `+effect:rotate_line` — циклічний зсув рядка/стовпця з вмістом (ширше за `shift`, який зсуває до упору).
- `+effect:swap_lines` — обмін двох рядків/стовпців цілком.
- `+effect:jump_over` — переміщення через клітину без входу в неї.

## Джерела
- ⭐ [148Apps: огляд](http://www.148apps.com/reviews/minesweeper-genius-review/) — Аристотель, тап для кроку, числа рядків/стовпців, зелені стрілки (крайня клітина на інший бік), фіолетові (обмін ліній), джамп-пади, прапорці, «одна правильна стежка».
- [iMore: огляд](https://www.imore.com/minesweeper-genius-modernizes-classic-computer-game) — хід на сусідню клітину, long-press прапорець, процедурні рівні, до 3 зірок, iCloud, $1.99 на iOS.
- [Xbox Store](https://xbox.com/en-US/games/store/1/9NQF1WZL3RC9) — MGaia / Blowfish Studios, 12.02.2019, «move the minesweeper to the portal», sudoku + picross + Minesweeper, генератор, achievements, cloud saves.
- Дата iOS-релізу 16.05.2018 і розробник — з результатів пошуку (MobyGames 403).
- YouTube: пошук «Minesweeper Genius gameplay».

## Непевне
- (?) Steam-сторінки нема: app 838890 з черги веде на головну Steam, пошук Steam гри не знаходить; черга помилялась.
- (?) Чи клітина відкривається вже при кроці на неї, чи раніше (по сусідству з аватаром) — джерела не кажуть.
- (?) Що відбувається після вибуху: рестарт кімнати чи продовження — відомо лише, що 3 зірки дають тільки без вибухів.
- (?) Джамп-пад: перестрибує «цілий рядок/стовпець» (148Apps) чи «одну клітину» (iMore) — джерела розходяться.
- (?) Суперечність: 148Apps каже «більшість рівнів мають одну правильну стежку», iMore/Xbox — процедурні рівні; можливо, є і ручні, і згенеровані.
- (?) Версії для Switch/PlayStation — лише з агрегатора; розміри кімнат і кількість рівнів не знайдено.
