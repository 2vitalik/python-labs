---
title: Hebi-Ichigo (へびいちご)
slug: hebi-ichigo
aka: [へびいちご, Hebi, Snakes, Strawberry Snake, 1-5-Schlange, Spirits of Serpentine, Змійки 1–5]
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
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/hebi/", best: true, note: "Nikoli: 4 правила EN, картинки Sample / Progressing / Solution, список пазлів"}
  - {kind: other, url: "https://puzz.link/rules.html?hebi", note: "puzz.link: правила EN/JA і плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/hebi.js", note: "puzz.link: текст правил, «Nikoli vol. 126», тестові поля з кодами помилок, тести drag-нумерації"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/hebi.js", note: "pzprjs: граф змійок (сусіди з різницею 1), checkSnakesView, checkArrowNumber"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти bkSizeNe5 / bsSnake / snakeAttack .hebi"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Hebi-Ichigo/index.htm", note: "Janko: правила DE/EN/JA, гра слів ichi-go = 1-5, варіанти Seconds / Cipher / Toroidal / Basilisks, 210 пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hebi+ichigo+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, dot-mark, path-drawing, conflict-highlight, game-settings, in-game-editor, import-open-formats, level-bank, undo-redo, +numbered-path, +no-adjacent-check, +first-seen-clue, +snake-gaze-ban, +drag-number-sequence]
proposes: ["+cond:first_seen", "+cond:consecutive_adjacent(k, k+1, n4)", "+card:snake-gaze-ban", "+card:drag-number-sequence"]
author: opus
date: 2026-11-09
---

# Hebi-Ichigo — розклади по білих клітинках змійок 1-2-3-4-5 так, щоб вони не торкались і жодна голова не дивилась на чужу змійку

## Суть
На сітці — чорні клітинки зі стрілками й числами. Гравець вписує в білі клітинки змійок: кожна — п'ять сусідніх сторонами клітинок з числами 1→5 підряд, 1 — голова, 5 — хвіст. Змійки не торкаються сторонами (по діагоналі можна). Голова «дивиться» в бік від двійки по прямій до чорної клітинки чи краю — на цій лінії не може бути чужої змійки («інакше нападе»). Число на чорній клітинці — перше число, яке видно в напрямку стрілки; 0 — у тому напрямку змійок нема.

## Поле і час
- Прямокутна сітка, ортогональне сусідство; чорні клітинки (дані) ділять рядки й стовпці на відрізки.
- Шари: чорні клітинки зі стрілкою й числом · числа гравця 1–5 · позначки «порожньо» (рожева крапка, `objblank`).
- Кількість змійок не задана; порожні білі клітинки дозволені.
- Час статичний; хід = вписати / стерти число чи крапку.
- Назва: へび — змія, いちご — полуниця, а ichi-go — ще й «1-5» (Janko).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | mark | порожня / 1–5 / крапка | гравець вписує |
| Змійка | piece | 5 клітинок, 1…5 | числа підряд по сусідах; 1 — голова, 5 — хвіст |
| Голова (1) | piece | погляд = від 2 до 1 | бачить по прямій до чорної клітинки чи краю |
| Чорна клітинка | static | стрілка, число 0–5 | зупиняє погляд голів і стрілки підказок |
| Підказка-стрілка | static | напрямок, N | перше число в напрямку = N; 0 — чисел нема |
| Чорна без стрілки | static | — | лише стіна (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(key_1_5, cell)` → ТО `set_value(cell, n)`; `q` або `-` → `mark(cell, dot)` (позначка «порожньо»).
- КОЛИ `input(drag, cells)` → ЯКЩО `custom: «drag почався з клітинки з числом n»` → ТО `custom: «вписати n+1, n+2… уздовж drag»` (режим `dragnum+`); правою — n−1, n−2… (`dragnum-`).
- Змійка: `custom: «компонента клітинок з числами, де сусіди різняться рівно на 1»` (pzprjs `AreaSnakeGraph`, `+cond:consecutive_adjacent`).
- КОЛИ `constraint_broken(empty)` → ЯКЩО `count(number, ==, 0)` → ТО `set_state(board, error)` (`brNoValidNum`: «There are no numbers on the board»).
- КОЛИ `constraint_broken(size)` → ЯКЩО `not region_size(snake, 5)` → ТО `set_state(snake, error)` (`bkSizeNe5`: «The size of a snake is not five»).
- КОЛИ `constraint_broken(duplicate)` → ЯКЩО `not unique(snake)` → ТО `set_state(snake, error)` (`bkDupNum`: «A snake has duplicate numbers»).
- КОЛИ `adjacent(snake_a, snake_b)` → ЯКЩО `custom: «клітинки різних змійок мають спільну сторону»` → ТО `set_state(both, error)` (`bsSnake`: «Different snakes are adjacent»).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «перше число за стрілкою до чорної клітинки чи краю ≠ N»` (`+cond:first_seen`) → ТО `set_state(clue, error)` (`anNumberNe`: «A clue points at the wrong number»); для N = 0 — помилка, якщо число взагалі є.
- КОЛИ `line_of_sight(head, snake_b)` → ЯКЩО `facing(head, from_2_to_1)` and `custom: «перша непорожня клітинка на промені — чужа змійка»` → ТО `set_state(both, error)` (`snakeAttack`: «A snake can see another snake»).
- Погляд на себе: ЯКЩО `custom: «перше число на промені — своя ж змійка»` → ТО помилки нема (pzprjs пропускає `cell.snake === snakes[r]`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірки pzprjs: є числа → розмір 5 → без дублів → не торкаються → підказки → погляди.
- Наслідок графа: 5 клітинок з різними числами 1–5, де ребра лише між сусідніми значеннями, — завжди ланцюжок 1-2-3-4-5.
- Дедукція «нуль»: 0 за стрілкою — увесь промінь до чорної / краю порожній (крапки).
- Дедукція «найближче»: N за стрілкою — промінь до клітинки з N порожній, тож сусіди N по змійці (N−1, N+1) лежать поза цим відрізком променя.
- Дедукція «хвіст і голова»: 1 і 5 на кінцях; 3 завжди має двох сусідів своєї змійки — 2 і 4.
- Перемога: є хоч одне число, усі змійки рівно 1–5, не торкаються, підказки збігаються, жодна голова не бачить чужої змійки. Поразки й рахунку нема.

## Керування і ввід
- Папір: вписати цифри 1–5, крапкою позначити порожні клітинки.
- puzz.link play: цифри з клавіатури (1–5); `q` / `-` — крапка; лівий drag від числа — нумерація вперед, правий — назад; клік без руху — ввід числа з циклом (?); режими `number`, `dragnum+`, `dragnum-`, `objblank`, `clear`.
- puzz.link edit: чорна клітинка — число 0–5 з клавіатури; стрілка — drag у клітинці або `Shift+стрілки`; `-` — чорна без числа.
- Налаштування `snakebd` — малювати межі навколо кожної змійки.

## Вікна, меню, HUD
- `game-screen`: сітка з пунктиром, чорні клітинки з білими числами й стрілками, числа змійок, рожеві крапки, межі змійок (за `snakebd`), `conflict-highlight` (змійка, підказка, лінія погляду).
- `settings-window` (puzz.link): `snakebd`, схема кнопок миші.
- `help-window` — правила (Nikoli з картинками Sample / Progressing / Solution; Janko; puzz.link).
- `puzzle-select` — Nikoli: список пазлів на сторінці жанру; Janko: 210 пазлів.
- Решта — оболонка [puzz.link](puzz-link.md): Check, Undo/Redo, Trial, URL, таймер.

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки; `undo` / `redo`; trial-режим оболонки.
- `level-editor` + `share-code` (URL puzz.link, зразок `5/5/a43g31b40b42g45a`); `export-import` (файл pzprv3; стара назва формату `snakes`).
- `puzzle-bank` — Janko 210 пазлів; Nikoli — добірка на сторінці жанру.

## Варіації й родичі
- Janko-варіанти: **Seconds** (число — друге видиме число змійки, Grant Fikes) · **Cipher** (числа замінені літерами) · **Toroidal** (поле — тор) · **Basilisks** (змійки різних довжин 1…N, Jonah Ostroff 2019).
- Числові ланцюжки: [Hidato](hidato.md), [Signpost](signpost.md); «перше видиме» з краю: [Easy as ABC](easy-as-abc.md); стрілка з числом на чорній клітинці: [Yajilin](yajilin.md) (рахує чорні).
- Заборона торкатися сторонами: [Star Battle](star-battle.md), [Tents](tents.md) (по діагоналі теж).
- **Осі варіацій**: довжина змійок (фіксована 5 / різні 1…N) · що каже підказка (перше / друге видиме число / кількість) · чи є погляд голови · топологія (прямокутник / тор).

## Цікавинки для курсу
- Граф «сусіди з різницею 1» і пошук компонент — 🌱; перевірка «розмір 5 + без дублів = ланцюжок» — 🌱.
- Промінь погляду від голови: напрямок 2→1, зупинка на чорній, краю чи першому числі — 📎.
- Підказка «перше видиме число» з нулем — 🌱, спільна функція з поглядом.
- Drag-нумерація n+1, n+2… уздовж руху миші — 📎 (зручний ввід для будь-яких числових ланцюжків).
- Розвʼязувач: розстановка п'ятиклітинкових поліоміно-змійок з пропагацією підказок і погляду — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` · `dot-mark` ↔ рожева крапка · `path-drawing` ↔ drag-нумерація · `conflict-highlight` · `game-settings` ↔ `snakebd` · `in-game-editor`, `import-open-formats` · `level-bank` (Janko) · `undo-redo`.
- Перевикористано: `+numbered-path` (Hidato) — ланцюжок 1…5; `+no-adjacent-check` — змійки не торкаються; `+first-seen-clue` (Easy as ABC).
- **Нема** → пропозиції карток:
  - `+snake-gaze-ban` «Голова фігури дивиться вздовж тіла; на промені до стіни не можна мати чужої фігури» · game-logic/constraints · 📎 · слот {stop: wall|edge|first-number} — Hebi-Ichigo.
  - `+drag-number-sequence` «Drag від числа вписує наступні числа вздовж руху» · interface/input · 🌱 · слот {dir: up|down} — puzz.link Hebi-Ichigo.

## Пропозиції до словників
- `+cond:first_seen` — повтор (Easy as ABC): перше непорожнє значення на промені = N.
- `+cond:consecutive_adjacent(k, k+1, n4)` — повтор (Hidato) з ортогональним сусідством.
- `+card:snake-gaze-ban` — див. мапу.
- `+card:drag-number-sequence` — див. мапу.

## Джерела
- ⭐ [Nikoli: Hebi](https://www.nikoli.co.jp/en/puzzles/hebi/) — 4 правила: числа 1 (голова) → 5 (хвіст), змійки не торкаються («territorial fights»), погляд 2→1 до чорної чи краю, число на чорній — найближче в напрямку стрілки, 0 — змійок нема.
- [pzpr-samples hebi.js](https://puzz.link/js/pzpr-samples/hebi.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 126», тести drag-нумерації.
- [pzprjs hebi.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/hebi.js) — `AreaSnakeGraph`, checklist, `checkArrowNumber`, `checkSnakesView`, режими вводу, `snakebd`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Hebi-Ichigo](https://www.janko.at/Raetsel/Hebi-Ichigo/index.htm) — правила трьома мовами, назви, варіанти Seconds / Cipher / Toroidal / Basilisks, 210 пазлів.

## Непевне
- (?) Рік: перша поява — Nikoli vol. 126 (pzprjs), рік цього номера не перевіряв; Janko пише «автор і перша публікація невідомі»; `year: null`.
- (?) Janko EN: число підказки «не може бути впритул до чорної клітинки» — у DE/JA і в коді pzprjs цього обмеження нема.
- (?) Janko EN дозволяє змійки «increasing or decreasing», DE — лише «aufsteigend»; для перевірки це однаково.
- (?) Чорна клітинка без стрілки / без числа — з коду редактора (`-`, `hideHatena`), у правилах не описано.
