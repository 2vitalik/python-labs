---
title: Stack Machines
slug: stack-machines
aka: []
family: program-robots
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2023
platforms: [PC (Windows, Linux/SteamOS; Steam, itch)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2279060/Stack_Machines/", best: true, note: "опис: 4 стекові машини їздять за модулями на сітці, дошка-тор змінного розміру, 4 метрики, гістограми, відео рішень"}
  - {kind: itch, url: "https://updevgames.itch.io/stack-machines", note: "itch: Godot, демо, девлоги версій 1.0.1–1.1.1"}
  - {kind: other, url: "https://updevgames.itch.io/stack-machines/devlog/1116988/version-11-recording-solution-videos-and-a-tutorial", note: "v1.1: запис відео з вікна гістограм, туторіал у рівні 1"}
  - {kind: other, url: "https://steamcommunity.com/app/2279060/discussions/0/3780246249198121056/", note: "розробник: ліміт стека 20, нулі у вході Filter"}
  - {kind: other, url: "https://steamcommunity.com/app/2279060/discussions/0/4633736089165714614/", note: "оптимум 42 цикли: машина має стояти на вході/виході майже щоцикл"}
  - {kind: other, url: "https://steamcommunity.com/app/2279060/discussions/0/4348869643729237733/", note: "рівень 8: заперечити число лише add/sub/execute; «спеціальна константа»"}
  - {kind: other, url: "https://steamcommunity.com/app/2279060/discussions/0/6361980659850442980/", note: "рівень 7 Add and Sub: входи i3, i4 → вихід o3"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stack+machines+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [wrap-edges, cursor-place, level-select, sequential-levels, leaderboard, game-screen, +stack-machine, +instruction-on-track-cells, +io-test-streams, +stack-height-limit, +solution-metrics, +metric-histograms, +solution-video-record, +resizable-board-metric, +multi-agent-sync]
proposes: ["+effect:stack_push", "+effect:stack_pop", "+cond:stack_top", "+effect:output", "+ui:value-list", "+window:histograms", "+card:resizable-board-metric"]
author: opus
date: 2026-11-09
---

# Stack Machines — чотири стекові машини їздять сіткою-тором і виконують модулі-інструкції, на які наїжджають

## Суть
Відкритий пазл-програмування в дусі Zachtronics: на сітці гравець розставляє **модулі** (інструкції), а до 4 стекових машин рухаються за ними, читають числа з вхідних послідовностей, перетворюють їх на своєму стеку й віддають на виходи. Програма просторова: що зробить машина, залежить від модуля на клітині, куди вона заїхала. Рішення оптимізують за чотирма метриками — розмір дошки, кількість модулів, швидкість (цикли) і вартість — і порівнюють на гістограмах.

## Поле і час
- Квадратна сітка змінного розміру, що **загортається** (тор); розмір — сама метрика (рішення 3×3, 5×5).
- Шари: клітина з модулем або порожня; згори — машини, кожна несе свій стек.
- Час `programmed`, тік = цикл: машини одночасно роблять крок і виконують модуль клітини; цикли «губляться», коли машина не стоїть на вході чи виході.
- Входи `i1…i4` і виходи `o1…o4` — списки чисел; рівень перевіряє вихідні списки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стекова машина (×≤4) | object | стек ≤ 20, напрям | їде сіткою за модулями, виконує модуль під собою |
| Модуль напрямку (стрілка) | terrain | напрям | машина повертає за стрілкою (?) |
| Модуль входу | terrain | номер входу | кладе наступне число з `iN` на стек |
| Модуль виходу | terrain | номер виходу | знімає вершину стека у `oN` |
| Арифметичні модулі (add, sub …) | terrain | операція | операція над вершиною стека |
| `execute` | terrain | — | виконує операцію з стека (?) |
| `isop`-модулі | terrain | умова | розгалуження залежно від операції/значення (?) |
| Спеціальна константа | terrain | значення | дає число, від якого віднімають, щоб змінити знак |
| Вхідна послідовність | resource | список чисел (з нулями-заповнювачами) | подається по одному числу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(machine, dir)`; за край → `wrap(machine)`.
- КОЛИ `enter(machine, arrow)` → ТО `face(machine, arrow_dir)` (?).
- КОЛИ `exec(input(n))` → ТО `custom: «наступне число з iN → на стек»`.
- КОЛИ `exec(output(n))` → ТО `custom: «вершина стека → у oN»`.
- КОЛИ `exec(add)` / `exec(sub)` → ТО `custom: «операція над верхніми значеннями стека, результат на вершину»`.
- КОЛИ `exec(isop)` → ЯКЩО `custom: «умова модуля виконана»` → ТО `custom: «машина йде іншою гілкою»` (?).
- КОЛИ `exec(cmd)` → ЯКЩО `counter(stack, >=, 20)` → ТО `custom: «стек повний»` (без явного сигналу помилки).
- КОЛИ `custom: «усі виходи збіглися з очікуваними списками»` → ТО `win`, `custom: «записати 4 метрики»`, `window(histograms)`.
- Перемога: виходи = специфікація · Поразка: нема (тест не закінчується, якщо програма не встигає) · Рахунок: розмір, модулі, цикли, вартість.

## Керування і ввід
- Ліва кнопка миші ставить символ/модуль на дошку; функції перемикаються клавішами; Esc — вихід з рівня.
- Розмір дошки змінюється; рішення мають імена й слоти.
- Запуск симуляції з показом списку значень (лаг на цикл між машиною і списком — зі скарг гравців).

## Вікна, меню, HUD
- `game-screen`: дошка, машини, список значень входів/виходів, опис задачі рівня.
- `level-select`: послідовні рівні (Add and Sub, Filter, Consecutive …).
- Вікно гістограм (custom «histograms»): розподіл чотирьох метрик спільноти + друзі; звідси запис відео рішення.
- `settings-window`: зокрема тривалість відео.
- Переходи: level-select → game-screen → (розвʼязано) → гістограми → наступний рівень.

## Фічі поза полем
- `leaderboard-online` (Steam Leaderboards, друзі), Steam Achievements (Beginner, Reverse, Advanced, All stacked up), Steam Cloud.
- Запис відео рішення (v1.1), туторіал у рівні 1 (v1.1); раніше гра не мала довідки — головна скарга гравців.

## Варіації й родичі
- У сімʼї: `befunge` (2D-код, стек, указівник напряму), `exapunks` / `tis-100` (Zachtronics-програмування з метриками й гістограмами), `opus-magnum` (просторова програма і три метрики), `human-resource-machine` (входи/виходи-черги).
- Осі варіацій: **памʼять** (регістр / стек / черга); **скільки виконавців** (1 / 4 машини одночасно); **дошка** (фіксована / тор змінного розміру як метрика).

## Цікавинки для курсу
- Інтерпретатор: машини-агенти на торі, модуль клітини як інструкція — 🥉.
- Стекова машина з лімітом глибини 20 — 📎.
- Чотири метрики й гістограма спільноти — 🥉.
- Запис відео рішення з симуляції — 🥈.

## Мапа на каталог
- Є: `wrap-edges` · `cursor-place` · `level-select` · `sequential-levels` · `leaderboard` · `game-screen` · `+stack-machine` · `+instruction-on-track-cells` · `+io-test-streams` · `+stack-height-limit` · `+solution-metrics` · `+metric-histograms` · `+solution-video-record` · `+multi-agent-sync` (уже в корпусі).
- **Нема** → пропозиції карток:
  - `+resizable-board-metric` «Розмір дошки — метрика рішення» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:stack_push`, `+effect:stack_pop`, `+cond:stack_top` — стек як памʼять сутності (уже пропоновані в сімʼї; підтвердження).
- `+effect:output` — віддати значення у вихідний потік.
- `+ui:value-list` — списки входів/виходів з поточним елементом.
- `+window:histograms` — гістограми метрик (з кнопкою запису відео).

## Джерела
- ⭐ [Steam: Stack Machines](https://store.steampowered.com/app/2279060/Stack_Machines/) — UP Development, 24.02.2023; 4 стекові машини, модулі на сітці, дошка-тор змінного розміру, 4 метрики, гістограми, відео рішень.
- [itch.io](https://updevgames.itch.io/stack-machines) і [девлог v1.1](https://updevgames.itch.io/stack-machines/devlog/1116988/version-11-recording-solution-videos-and-a-tutorial) — Godot, туторіал, відео з вікна гістограм.
- [Problem with Filter task](https://steamcommunity.com/app/2279060/discussions/0/3780246249198121056/) — ліміт стека 20, нулі у вході.
- [Optimal solutions](https://steamcommunity.com/app/2279060/discussions/0/4633736089165714614/) — цикли губляться поза входом/виходом; 42 цикли.
- [Level 8](https://steamcommunity.com/app/2279060/discussions/0/4348869643729237733/) — add/sub/execute, «спеціальна константа».
- [Level 7](https://steamcommunity.com/app/2279060/discussions/0/6361980659850442980/) — входи i3/i4, вихід o3.

## Непевне
- (?) Повний список модулів, їхні назви й семантика `execute`, `isop` — у відкритих джерелах не описані; таблиця сутностей — реконструкція з форуму.
- (?) Як машина змінює напрям (модулі-стрілки) — виведено зі скарги «arrows had smoother animations».
- (?) Що таке «вартість» (cost-effectiveness) — ціна модулів?
- (?) Кількість рівнів (є щонайменше 37: «Consecutive»).
