---
title: SquareCells
slug: squarecells
aka: [Square Cells]
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
year: 2015
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/416770/SquareCells/", best: true, note: "36 пазлів, трейлер; скриншоти пазлів 01 і 05 показують тексти правил на екрані"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SquareCells", note: "серії на рядках/стовпцях, число в клітині = розмір групи, 36 рівнів, критика лічильника «to remove»"}
  - {kind: other, url: "https://www.gamingonlinux.com/2015/12/squarecells-a-new-puzzle-game-from-the-developer-of-hexcells-has-been-released-on-steam", note: "огляд: три типи підказок, лічильник клітин до видалення, рівень можна покинути й повернутись"}
  - {kind: other, url: "https://www.wurb.com/stack/?p=3572", note: "блог The Stack: дужки навпаки до Hexcells, видалення незворотне, виконані числа сіріють, стрілки біля рядка й стовпця під курсором"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=416770&count=20", note: "Steam News: патч 1.1 — темна схема, режим «лише звуки»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SquareCells+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, completion-detection, run-length-clues, line-sum-clue, cell-click, hover-highlight, level-select, sequential-levels, save-autosave, restart-level, theme-select, music-toggle, controls-remap, background-music, +region-size-check, +carve-pattern, +clue-greying, +stars-rating]
proposes: ["+card:carve-pattern", "+card:region-size-check", "+ui:row-column-guide", "+ui:clue-greyed"]
author: opus
date: 2026-11-19
---

# SquareCells — виріж візерунок із квадратної сітки за серіями рядків, сумами в дужках і розмірами груп

## Суть
Друга гра Matthew Brown після Hexcells, але на квадратній сітці й без прихованої інформації: усі підказки видно з початку. Гравець прибирає з поля зайві квадрати, доки не лишиться задуманий візерунок; правою кнопкою можна позначити клітину як «точно частина візерунка». Ядро — три типи підказок, які змішуються в одному пазлі: серії нонограми на рядках і стовпцях, загальна кількість у квадратних дужках і число в клітині, що дорівнює розміру її звʼязної групи (як острів у Nurikabe).

## Поле і час
- Квадратна сітка; на скриншотах — 4×4 (пазли 01, 05), 6×6 (16), 8×8 (09), 10×10 (21), 12×12 (29); розмір підписано під номером пазла.
- Стартово всі клітини зафарбовані кольором світу; відповідь «вирізають», а не малюють.
- Підказки стоять не на всіх лініях: частина рядків і стовпців без підказки, а пазл 05 має лише числа в клітинах.
- Статичний пазл без таймера; 36 пазлів у 6 світах по 6, кожен світ має свій колір (жовтий, блакитний, червоний, бірюзовий, синій…).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина (невідома) | mark | — | стартовий стан: суцільний кольоровий квадрат |
| Позначена клітина | mark | — | ПКМ: світліша верхня половина й крапка в куті; знімається повторно |
| Видалена клітина | mark | — | ЛКМ: лишається малий сірий слід; назад не повертається |
| Серія-підказка «a b c» | static | список довжин | групи візерунка в лінії по порядку; кожне число сіріє, коли його серію виконано |
| Підказка в дужках «[n]» | static | n | лише кількість клітин візерунка в лінії, без порядку й розбиття |
| Число в клітині | static | n | клітина належить візерунку; її ортогональна група має рівно n клітин |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, c)` → ЯКЩО `custom: «c не входить у візерунок»` → ТО `set_cell(c, removed)`, `counter(to_remove, -1)`.
- КОЛИ `input(left_click, c)` → ЯКЩО `custom: «c — частина візерунка»` → ТО (?) `custom: «помилка»` — див. «Непевне».
- КОЛИ `input(right_click, c)` → ЯКЩО `not state(c, marked)` → ТО `mark(c, pattern)`; інакше `unmark(c)`.
- Серія «a b c» на лінії: ЯКЩО `run_lengths(line)` — групи візерунка мають довжини a, b, c саме в цьому порядку (одне число без дужок — одна суцільна група).
- Дужки «[n]» на лінії: ЯКЩО `sum(line, n)` — у лінії рівно n клітин візерунка, як завгодно розкиданих.
- Число n у клітині c: ЯКЩО `region_size(group(c), n)` — групу рахують лише по сторонах клітин, діагональ не зʼєднує.
- КОЛИ `custom: «серію чи групу підказки виконано»` → ТО `set_state(clue, greyed)` — сіріє окреме число всередині «4 1 2», не вся лінія.
- КОЛИ `counter(to_remove, ==, 0)` → ТО `win` (?), `next_level`.
- Перемога: лишився рівно візерунок. · Поразка: нема. · Рахунок: зірки, 3 на пазл, 108 за гру (досягнення «Perfectionist»); за що знімаються — (?).

## Керування і ввід
- Ліва кнопка — прибрати клітину, права — позначити як частину візерунка; на першому пазлі значок інвертує кнопки миші.
- Біля кінців рядка й стовпця під курсором зʼявляються стрілки — щоб знайти потрібні підказки на великому полі.
- EXIT — вийти з пазла (прогрес зберігається), RESET — почати пазл заново.

## Вікна, меню, HUD
- `game-screen`: поле в центрі; ліворуч угорі EXIT і RESET; праворуч угорі «PUZZLE NN» і розмір; під полем `remaining-counter` «N TO REMOVE» над загальною кількістю клітин; на перших пазлах праворуч — текст правила.
- `level-select` (?): 36 пазлів у 6 світах (досягнення «World N Complete: Complete puzzles …») з зірками; вигляд екрана не бачив.
- `settings-window` (?): темна колірна схема й режим «лише звуки» (патч 1.1).
- HUD: `remaining-counter`, `+ui:clue-greyed` (сірі виконані числа), `+ui:row-column-guide` (стрілки), `level-number`.
- Переходи: вибір пазла → `game-screen` → (усе вирізано) наступний пазл; EXIT → вибір пазла.

## Фічі поза полем
- `levels-sequential` у 6 світах; кожен світ — досягнення Steam (7 досягнень разом із «Perfectionist»).
- `autosave`: пазл можна покинути посередині й повернутися, обмеження на кількість відкладених нема.
- `restart-level` (RESET); undo — нема (?), видалення незворотне.
- `theme-select`-подібна темна схема, `music-toggle` («sound only»), `remap-controls` у вигляді інверсії кнопок миші.
- Нема редактора, генератора, таймера й таблиць рекордів.

## Варіації й родичі
- База — [nonogram.md](nonogram.md) (серії); числа в клітинах — з [nurikabe.md](nurikabe.md) і [fillomino.md](fillomino.md); той самий автор — Hexcells (`hidden-deduction/hexcells.md`), де дужки означають протилежне: там `{n}` — «підряд», а просте n — кількість.
- Наступна гра автора — CrossCells (2017, у черзі сімʼї): прибирати клітини з числами до цільових сум.
- Ввід «вирізанням» — 2D-родич молота з Picross 3D ([picross-variants.md](picross-variants.md)).
- **Осі варіацій**: лінійна підказка — серії / лише сума / нема · підказка в клітині — сусіди (сапер) / розмір групи (Nurikabe) / нема · ввід — фарбувати (нонограма) / вирізати зайве (SquareCells) · помилка — нічого / лічильник / поразка.

## Цікавинки для курсу
- Три типи підказок в одному пазлі (серії, `[n]`, розмір групи) і перевірка всіх за прохід по полю — 📎: RLE рядка, сума лінії й BFS групи.
- Посегментне сіріння: які саме числа з «4 1 2» вже виконано, коли рядок ще не завершений — 🥉 (позначати лише однозначні серії).
- Ввід «вирізанням»: стани невідома → видалена (незворотно) / позначена (зворотно) і лічильник «до видалення» — 🌱.
- Розвʼязувач: лінійний солвер нонограми плюс обмеження розміру ортогональних груп — 🥇.
- Генератор: із готового візерунка вибрати мінімальний набір підказок (які лінії лишити без підказки, де поставити числа), щоб розвʼязок був єдиним і без вгадування — 👑.

## Мапа на каталог
- Є: `run-length-clues` ↔ серії; `line-sum-clue` ↔ `[n]`; `satisfy-constraints`, `completion-detection`; `cell-click` ↔ ЛКМ/ПКМ; `hover-highlight` ↔ стрілки біля ліній; `level-select`, `sequential-levels` ↔ 6 світів; `save-autosave`; `restart-level` ↔ RESET; `theme-select` ↔ темна схема; `music-toggle`; `controls-remap` ↔ інверсія кнопок; `background-music` ↔ ембієнт.
- **Нема** → пропозиції карток:
  - `+carve-pattern` «Розвʼязок вирізають: прибирають зайве з повного поля, лічильник до видалення» · interface/input · 🌱 — 2D-родич `+voxel-carve`.
  - `+region-size-check` (повтор: nurikabe, nodes-of-a-feather) «Число в клітині = розмір її звʼязної групи» · game-logic/constraints · 📎.
  - `+clue-greying` (повтор: nonogram) «Виконані числа підказки сіріють поодинці» · interface/hud · 📎.
  - `+stars-rating` (повтор) «1–3 зірки за пазл» · levels/progression · 🌱.

## Пропозиції до словників
- `+card:carve-pattern`, `+card:region-size-check` — див. мапу.
- `+ui:row-column-guide` — стрілки біля кінців рядка й стовпця під курсором (повтор із nonogram).
- `+ui:clue-greyed` — виконане число підказки сіріє (повтор із nonogram).

## Джерела
- ⭐ [Steam: SquareCells](https://store.steampowered.com/app/416770/SquareCells/) — 36 пазлів, трейлер, 6 скриншотів: пазл 01 («Left click to remove … right click to mark», «N TO REMOVE»), пазл 05 («A number inside a square shows it is part of a group of connected squares of that size. Squares do not connect diagonally»), пазли 16, 21, 29 з `[n]`.
- [Wikipedia: SquareCells](https://en.wikipedia.org/wiki/SquareCells) — серії «2 4», числа в клітинах, 36 рівнів, лічильник клітин до видалення як вада.
- [GamingOnLinux](https://www.gamingonlinux.com/2015/12/squarecells-a-new-puzzle-game-from-the-developer-of-hexcells-has-been-released-on-steam) — порядок появи механік (нонограма → числа → дужки), «guesswork is never needed», відкладені рівні.
- [The Stack (wurb.com)](https://www.wurb.com/stack/?p=3572) — дужки навпаки до Hexcells, видалення назавжди, сірі виконані числа, стрілки біля ліній, автозбереження.
- Steam: список досягнень (7: «World 1–6 Complete», «Perfectionist: Earn all 108 stars») і [Steam News](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=416770&count=20) — патч 1.1.
- YouTube: пошук «SquareCells gameplay».

## Непевне
- (?) Що буває, коли гравець прибирає клітину візерунка: за Hexcells-аналогією — дію відхилено й зараховано помилку; лічильника помилок на скриншотах нема.
- (?) За що даються 3 зірки пазла (ймовірно, за помилки) — бачив лише «108 stars» у досягненні.
- (?) Чи пазл завершується, щойно «TO REMOVE» = 0, чи треба ще позначити всі клітини візерунка (блог The Stack каже друге).
- (?) Вигляд екрана вибору пазлів і налаштувань — не бачив; undo, схоже, нема.
