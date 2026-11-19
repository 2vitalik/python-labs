---
title: Shinro (しんろ)
slug: shinro
aka: [しんろ, Шінро]
family: pencil-logic
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2007
platforms: [paper, web, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shinro", best: true, note: "правила (8×8, 12 лунок, стрілки, лічильники рядків і стовпців), приклад і розвʼязок картинками, Puzzability 2007, Spirit Magazine, варіант Sternenhimmel"}
  - {kind: play, url: "https://plays.org/daily-shinro/", note: "Daily Shinro: клік — хрестик / кулька / порожньо, Pause, Reset, Query, Easy/Hard, пазл на кожен день, автозбереження"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Sternenhimmel/index.htm", note: "Janko Sternenhimmel — варіант: стрілка рівно на одну (або ≥1) зірку, кожна зірка під стрілкою; 200 пазлів 7×7…17×17; Stars and Arrows"}
  - {kind: other, url: "https://www.mscroggs.co.uk/puzzles/120", note: "задача-приклад: 12 лунок, «None of the arrows covers a hole»"}
  - {kind: other, url: "https://upload.wikimedia.org/wikipedia/commons/6/6f/Shinro_start.svg", note: "SVG прикладу з Вікіпедії: 12 стрілок, 6 із них діагональні; числа зверху й ліворуч"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shinro+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, line-sum-clue, daily-puzzle, difficulty-levels, field-size-picker, game-pause, restart-level, music-toggle, sound-effects, save-autosave, level-solver, unique-puzzle-generation, +arrow-count-clue, +cell-shade-toggle, +clue-greying, +mistake-check]
proposes: ["+cond:count_dir", "+card:arrow-count-clue"]
author: opus
date: 2026-11-19
---

# Shinro — знайди 12 схованих лунок на полі 8×8 за лічильниками рядків і стовпців та стрілками

## Суть
Поле 8×8: над стовпцями й ліворуч від рядків — скільки в лінії лунок, у деяких клітинках — стрілки. Гравець відшукує 12 схованих лунок (у цифрових версіях — кульок): кожна стрілка вказує хоча б на одну лунку у своєму напрямку, клітинка зі стрілкою лунки не містить. Вікіпедія порівнює гру із судоку й сапером, але нічого не відкривається — усі підказки видно одразу, тож це чиста дедукція; назва しんろ («курс за компасом») — про стрілки.

## Поле і час
- Квадрат 8×8, рівно 12 лунок (Вікіпедія); plays.org пропонує ще й вибір розміру поля (які розміри — (?)).
- Числа — над стовпцями й ліворуч від рядків (SVG прикладу Вікіпедії); сума чисел рядків = сума чисел стовпців = 12.
- Стрілки стоять у клітинках і дивляться в 8 напрямків: у прикладі Вікіпедії 6 з 12 стрілок діагональні.
- Промінь стрілки — від клітинки до краю поля; стрілка не обовʼязково поруч із лункою (plays.org).
- Не кожна лунка має стрілку (plays.org) — частину знаходять лише лічильники.
- Час статичний; хід — позначити клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | порожньо / хрестик / кулька | цикл станів кліком |
| Лунка (кулька) | mark | — | 12 на полі; рахується у свій рядок і стовпець |
| Хрестик | mark | — | необовʼязкова нотатка «лунки нема» |
| Стрілка | static | 1 з 8 напрямків | у промені до краю ≥ 1 лунки; сама лунки не містить |
| Число рядка / стовпця | static | 0–8 | кількість лунок у лінії; сіріє, коли виконане (plays.org) |
| Рядок / стовпець | zone | 8 клітинок | — |
| Промінь стрілки | zone | клітинки від стрілки до краю | містить ≥ 1 лунку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `not cell(cell, arrow)` → ТО `mark(cell, cross)`; другий клік — `mark(cell, marble)`; третій — `unmark(cell)` (plays.org).
- КОЛИ `input(click, cell)` → ЯКЩО `cell(cell, arrow)` → ТО `block` («None of the arrows covers a hole»).
- КОЛИ `counter(marbles_in_line, ==, n)` → ТО `custom: «число рядка чи стовпця сіріє»` (plays.org).
- КОЛИ `constraint_broken(line_count)` → ЯКЩО `not count(hole_in_line, ==, n)` → ТО `custom: «лінія з хибною кількістю лунок»`.
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `custom: «у промені стрілки до краю поля нема жодної лунки»` (`+cond:count_dir`) → ТО `custom: «стрілка не виконана»`.
- КОЛИ `input(query)` → ТО `custom: «перевірити, чи поставлені кульки правильні»` (plays.org Query).
- КОЛИ `input(pause)` → ТО `timer(stop)`, `custom: «гра на паузі»`.
- КОЛИ `input(reset)` → ТО `restart` (поле до початкового стану).
- КОЛИ `all_constraints_met` → ТО `win`, `window(end-screen)` (кнопка Next — наступний пазл).
- Дедукція «нуль»: лінія з числом 0 → усі її клітинки порожні.
- Дедукція «квота»: у лінії вже n лунок → решта порожні; можливих клітинок рівно n → усі лунки.
- Дедукція «вузький промінь»: у промені стрілки лишилась одна можлива клітинка → там лунка.
- Дедукція «перехрестя»: клітинка поза всіма променями може бути лункою — її виводять лише лічильники ліній.
- Перемога: 12 лунок, усі лічильники й стрілки виконані. Поразки нема; рахунок — час (plays.org: таймер ліворуч).

## Керування і ввід
- plays.org: лівий клік або тап — 1 раз хрестик, 2 — кулька, 3 — порожньо; хрестики необовʼязкові.
- Кнопки: Pause, Reset, Query; перемикачі музики, звуків і повного екрана.
- Вибір дати (щоденний пазл), складності (Easy / Hard) і розміру поля; Next на переможному екрані.
- Папір: Spirit Magazine — PDF з чотирма пазлами (Вікіпедія); олівцем ставлять лунки й хрестики.

## Вікна, меню, HUD
- `game-screen` (plays.org): поле з числами зверху й ліворуч, `timer-elapsed` ліворуч, кнопки Pause / Reset / Query, перемикачі звуку й музики, повний екран; виконані числа сіріють.
- `daily-window`: вибір дати — 365–366 пазлів на кожен розмір і складність.
- `difficulty-select`: Easy / Hard; поруч — вибір розміру поля.
- `pause-menu` — гра зупинена (Pause).
- `end-screen` — перемога з кнопкою Next.
- `help-window` — правила й керування на сторінці гри (plays.org).
- Переходи: сторінка → game-screen пазла дня → Query → перемога → Next / інша дата / інша складність.

## Фічі поза полем
- `daily-puzzle` за датою, `difficulty-presets` (Easy / Hard), вибір розміру поля.
- `autosave` прогресу в браузері; `pause`; `restart-level` (Reset); `auto-check` за кнопкою Query.
- `music-toggle`, `sound-toggle`, `fullscreen`.
- Мобільні версії, названі у Вікіпедії: Shinro Mines, Jabeh (з відеоуроком), Sudoku Shinro (iPhone), Shinro: Minefield (Android) — сторінки не відкривав.

## Варіації й родичі
- **Sternenhimmel** (Janko; WPC — Stars and Arrows; ЗВЕЗДЫ — М. Хотінер і О. Степанов): за умовою стрілка вказує рівно на одну (або ≥1) зірку, і кожну зірку вказує стрілка; 200 пазлів 7×7…17×17.
- [Minesweeper](../hidden-deduction/minesweeper.md), [Sudoku](sudoku.md) — їх називає Вікіпедія; [Battleship](../hidden-deduction/battleship.md) — лічильники рядків і стовпців для схованих обʼєктів.
- [Tents](tents.md), [Star Battle](star-battle.md) — квоти на лінії; [Yajilin](yajilin.md) — стрілка з числом.
- **Осі варіацій**: що каже стрілка (≥1 — Shinro / рівно 1 — Sternenhimmel / число — Yajilin) · чи мусить кожен обʼєкт бути під стрілкою (ні / так) · напрямки (8 / 4) · розмір і кількість (8×8 і 12 / змінні).

## Цікавинки для курсу
- Промінь у 8 напрямках до краю + перевірка «≥ 1 лунки» — 🌱.
- Лічильники рядків і стовпців, що сіріють, коли виконані — 🌱.
- Розвʼязувач: 12 лунок серед ≤ 64 клітинок — C(64,12) ≈ 3,3·10¹² наборів, тож потрібні пропагація квот і стрілок та бектрекінг — 🥉.
- Генератор: розкидати 12 лунок → порахувати числа → додавати стрілки, доки розвʼязок не стане єдиним — 🥈; еволюційна генерація «цікавих» пазлів (стаття Оранчака, лише назва) — 👑.
- Пазл на кожну дату × розмір × складність з автозбереженням — 📎.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `line-sum-clue` ↔ числа рядків і стовпців · `daily-puzzle` · `difficulty-levels` · `field-size-picker` · `game-pause` · `restart-level` ↔ Reset · `music-toggle` · `sound-effects` · `save-autosave` · `level-solver` · `unique-puzzle-generation`.
- Перевикористано: `+arrow-count-clue` (Yajilin, Yajisan-Kazusan) — тут слот {op: ≥1, dirs: 8} · `+cell-shade-toggle` ↔ цикл хрестик / кулька / порожньо · `+clue-greying` ↔ виконані числа сіріють · `+mistake-check` ↔ Query.
- **Нема** → нових карток не треба; розширення — у пропозиціях.

## Пропозиції до словників
- `+cond:count_dir` — кількість сутностей виду в промені від клітинки до краю (повтор з Yajilin, Yajisan); тут «≥ 1» у 8 напрямках.
- `+card:arrow-count-clue` — розширити слотами {op: ==|≥, dirs: 4|8}: Shinro — «хоча б одна» в 8 напрямках, Yajilin — «рівно N» у 4.

## Джерела
- ⭐ [Wikipedia: Shinro](https://en.wikipedia.org/wiki/Shinro) — 8×8, 12 лунок, стрілки «≥ 1», лічильники, японські журнали, Spirit Magazine, назва від Puzzability (2007), しんろ, Sternenhimmel.
- [Приклад Вікіпедії, SVG](https://upload.wikimedia.org/wikipedia/commons/6/6f/Shinro_start.svg) — розташування чисел (зверху, ліворуч) і 12 стрілок, 6 діагональних.
- [plays.org: Daily Shinro](https://plays.org/daily-shinro/) — правила, ввід кліками, кнопки, Easy/Hard, щоденні пазли, автозбереження, таймер.
- [mscroggs: задача 120](https://www.mscroggs.co.uk/puzzles/120) — формулювання: 12 лунок, стрілки вказують хоча б на одну, жодна стрілка не накриває лунку.
- [Janko: Sternenhimmel](https://www.janko.at/Raetsel/Sternenhimmel/index.htm) — варіант «рівно одна», назви, банк 200 пазлів.
- YouTube: [пошук «shinro puzzle»](https://www.youtube.com/results?search_query=shinro+puzzle).

## Непевне
- (?) Чи перекривають інші стрілки промінь — джерела про блокування мовчать; трактую як промінь до краю без перешкод.
- (?) Рік 2007 — коли Puzzability дала назву; японське першоджерело й рік невідомі.
- (?) Які розміри поля дає plays.org і чи там завжди 12 кульок — сказано лише «для кожного розміру поля».
- (?) Що саме показує Query (позначає хибні кульки чи лише «так / ні») — не перевірено.
- (?) Сайти Оранчака (playshinro, стаття про еволюційну генерацію) не відкрились через сертифікат; мобільні версії — лише назви.
