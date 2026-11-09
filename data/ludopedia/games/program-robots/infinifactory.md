---
title: Infinifactory
slug: infinifactory
aka: []
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: 3d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2015
platforms: [PC, Mac, Linux, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Infinifactory", best: true, note: "3D-блоки від першої особи, конвеєри, зварювачі, сенсори, падіння без опори, метрики footprint/cycles/blocks, гістограми, Workshop"}
  - {kind: steam, url: "https://store.steampowered.com/app/300570/Infinifactory/", note: "50+ пазлів, пісочниця, гістограми, Workshop, level editor"}
  - {kind: official, url: "https://www.zachtronics.com/infiniupdate-2", note: "оновлення: лазер, екструдовані входи, Test Zone X, телепортери в редакторі"}
  - {kind: other, url: "https://namu.moe/w/Infinifactory", note: "корейська фан-вікі: опис блоків (зварювач, сенсор, провід, штовхач, ротатор, ліфт, блокер)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=infinifactory+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [row-conveyor, carrier-platform, gravity-fall, push-object, stick-together, multi-cell-size, destructible-blocks, teleport, collect-quota, drag-drop-piece, sequential-levels, level-unlock, level-select, world-map, in-game-editor, editor-playtest, level-exchange, leaderboard, game-screen, end-screen, +block-placement-program, +sensor-signal-wire, +signal-actuator, +weld-adjacent, +block-rotator, +vertical-lifter, +retractable-blocker, +laser-cutter, +input-respawn, +molecule-match-output, +collision-halt, +solution-metrics, +metric-histograms, +sandbox-mode, +first-person-builder, +audio-logs]
proposes: ["+trigger:signal(sensor)", "+cond:signal(port)", "+effect:weld(a, b)", "+effect:lift(a, n)", "+effect:emit_signal(conduit)", "+effect:destroy_line(dir)", "+role:actuator", "+role:sensor", "+role:product", "+window:puzzle-info", "+window:metric-histograms", "+ui:block-hotbar", "+ui:metric-panel", "+feature:workshop", "+feature:sandbox-containers"]
author: opus
date: 2026-11-09
---

# Infinifactory — тривимірна фабрика з блоків-механізмів: програма — це розстановка конвеєрів, сенсорів і зварювачів

## Суть
Гравець (викрадений прибульцями інженер) у вигляді від першої особи з реактивним ранцем ставить у 3D-просторі блоки: конвеєри, штовхачі, сенсори, зварювачі, ротатори. Із входів періодично зʼявляються кубики-деталі; фабрика має провезти їх, повернути, зварити в продукт потрібної форми й доставити на точку видачі. «Програми» як тексту нема: логіка — це геометрія блоків і сигнали від сенсорів по проводах. Розвʼязків багато, а після проходження гра порівнює три метрики з гістограмами інших гравців.

## Поле і час
- Поле — **воксельна 3D-сітка**: кожен блок займає одну клітину; рівень — острів із наперед поставленими входами, виходами й незнімними обʼєктами.
- Гравець вільно літає (ранець) і дивиться від першої особи; поставити блок — у клітину, на яку дивишся.
- **Гравітація**: незакріплені блоки падають; деталь, що не лежить на опорі, падає вниз (і може зникнути за краєм) (?).
- Час `programmed`: розстановка → запуск; цикл (cycle) — усі механізми діють одночасно, деталі рухаються на одну клітину за цикл (?). Під час роботи можна зупинити й оглянути фабрику.
- Детермінізм повний; входи видають деталі за розкладом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | ранець | літає, ставить і знімає блоки; у симуляції не впливає |
| Платформа | static | — | опора; не рахується в метриці blocks |
| Конвеєр | terrain | напрямок | везе блок, що на ньому, на клітину вперед |
| Перевернутий конвеєр | terrain | напрямок | стрічка знизу: везе блок під собою |
| Штовхач (pusher) | switch | напрямок | за сигналом зсуває блок перед собою на 1 |
| Сенсор («око») | switch | напрямок | дає сигнал, коли в клітині перед ним є блок; суміжні блоки отримують сигнал без проводу |
| Провід (conduit) | conduit | — | передає сигнал сенсора далі |
| Зварювач (welder) | terrain | — | склеює блоки, що торкаються його, між собою; зварене не роз'єднати, хіба знищити частину |
| Ротатор | terrain | напрям обертання | повертає блок на собі навколо центру; потрібне вільне місце |
| Ліфт (lifter) | terrain | — | піднімає блок, що на нього заїхав, угору (?) |
| Блокер | gate | сигнал | висувається/ховається, перекриває шлях (з пізніх розділів) |
| Евісцератор | hazard | — | знищує блок, що на нього потрапив |
| Лазер | hazard | порти проводу | за сигналом миттєво знищує всі блоки перед собою |
| Телепортер | terrain | пара | переносить один блок (не зварену групу) |
| Вхід (input) | spawner | форма, розклад | видає деталь/групу кубиків |
| Екструдований вхід | spawner | — | безперервний потік металевих блоків; його треба відрізати й обробити |
| Деталь (cube) | object | тип матеріалу | рухається механізмами, падає без опори |
| Продукт | object | форма з кількох кубиків | зварена група потрібної форми |
| Точка видачі (output) | sink | шаблон, квота | приймає продукт потрібної форми й рахує |
| Наперед поставлені обʼєкти | static | — | не знімаються; допомагають або заважають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `schedule(input)` → ЯКЩО `free(input_cell)` → ТО `spawn_at(part, input)`.
- КОЛИ `tick` → ЯКЩО `occupied(conveyor_top, part)` → ТО `move(part, conveyor_dir)` — разом з усією звареною групою.
- КОЛИ `tick` → ЯКЩО `not supported(part)` → ТО `fall(part)`.
- КОЛИ `enter(part, sensor_front)` → ТО `custom: «сенсор подає сигнал у суміжні блоки й проводи»`.
- КОЛИ `custom: «штовхач отримав сигнал»` → ЯКЩО `free(cell_behind)` → ТО `push(part)`; інакше `block`.
- КОЛИ `custom: «блокер отримав сигнал»` → ТО `set_state(blocker, raised)` — шлях перекрито (?).
- КОЛИ `custom: «лазер отримав сигнал»` → ТО `custom: «знищити всі блоки на лінії перед лазером»`.
- КОЛИ `enter(part, eviscerator)` → ТО `disappear(part)`.
- КОЛИ `adjacent(part_a, part_b)` → ЯКЩО `custom: «обидва торкаються зварювача»` → ТО `attach(part_a, part_b)` — назавжди.
- КОЛИ `enter(part, rotator)` → ЯКЩО `custom: «є вільне місце для обертання»` → ТО `rotate(group, 90°)`.
- КОЛИ `enter(part, lifter)` → ТО `custom: «підняти групу вгору»` (?).
- КОЛИ `enter(part, teleporter)` → ЯКЩО `custom: «одиночний блок»` → ТО `teleport(part, pair)`.
- КОЛИ `custom: «рух у клітину, зайняту нерухомим»` → ТО `block` — деталь стоїть, механізми продовжують.
- КОЛИ `enter(product, output)` → ЯКЩО `same(product, template, shape)` → ТО `disappear(product)`, `counter(delivered, +1)`; інакше `custom: «помилка: неправильний продукт»` (?).
- КОЛИ `counter(delivered, ==, quota)` → ТО `win`, `window(end-screen)` з метриками.
- Перемога: квота продуктів на всіх точках видачі · Поразка: нема — фабрика зупиняється або застрягає, правиш розстановку · Рахунок: **footprint** (площа підлоги під фабрикою), **cycles** (цикли до квоти), **blocks** (кількість не-платформних блоків).

## Керування і ввід
- WASD + миша (вигляд від першої особи), пробіл/ранець — політ угору-вниз (?).
- Панель блоків (гаряча смуга) — вибір типу; ЛКМ — поставити, ПКМ — зняти (?); клавіші повороту блока.
- Лінійна побудова: протягнути ряд конвеєрів/платформ/проводів одним рухом (з оновлення — для більшості блоків); виділення області в редакторі.
- Запуск/пауза/прискорення симуляції; огляд під час паузи.

## Вікна, меню, HUD
- `world-map` / `level-select`: шість світів, у кожному кілька пазлів; відкриття наступного — за кількістю розвʼязаних.
- `game-screen`: 3D-сцена; `block-hotbar` (custom); `objective-text` (продукт і квота); `metric-panel` (custom); індикатор запуску/паузи.
- `puzzle-info` (custom): опис пазлу, форма продукту, кількість.
- `end-screen` + `metric-histograms`: гістограми footprint/cycles/blocks з позицією гравця.
- `editor-window`: редактор власних пазлів (після кампанії), публікація у Workshop лише з робочим розвʼязком.
- `mode-select`: кампанія / пісочниці (Test Zone X) / Workshop.
- Аудіологи загиблих попередників — як знахідки в рівнях (`dialogue-window`) (?).
- `settings-window`, `pause-menu`.

## Фічі поза полем
- `solution-metrics` + гістограми; `leaderboard-online` (друзі).
- `mode-sandbox`: пісочниці; Test Zone X — контейнери з блоками фабрики (фабрики, що будують фабрики).
- `level-editor` + Steam Workshop (`level-sharing`, `user-levels-browser`).
- `level-unlock` за кількістю розвʼязаних у світі; `achievements` (частина — оптимізаційні).
- `step-mode` (?), `speed-control`, `cloud-save`.

## Варіації й родичі
- Предки: Manufactoid (Zachtronics, 2D-попередник, сам Барт називає Infinifactory його 3D-переробкою), Infiniminer (блоки від першої особи), [spacechem](spacechem.md) (стиль пазлів і метрики).
- Родичі в корпусі: [manufactoria](manufactoria.md) (конвеєри як програма), [opus-magnum](opus-magnum.md) (метрики й GIF), [robot-odyssey](robot-odyssey.md) (сигнали від сенсорів до рушіїв); Factorio і Minecraft-редстоун — у `build-sim`.
- Осі варіацій: **програма** (текст / таймлайн / розстановка механізмів); **сигнали** (нема / сенсор → провід → виконавець); **поле** (2D / 3D з гравітацією); **зʼєднання** (звʼязки атомів / зварювання назавжди); **оцінка** (площа / цикли / кількість деталей).

## Цікавинки для курсу
- Синхронний такт: усі конвеєри зсувають деталі одночасно, зварені групи рухаються як ціле, конфлікти — блок — 🥇.
- Сенсор → провід → штовхач: мінімальна сигнальна логіка на клітинах — 🥈.
- Зварювання сусідів у звʼязну групу (union-find) і перевірка форми продукту з точністю до зсуву — 🥈.
- Гравітація для груп кубиків: група падає, якщо жоден кубик не має опори — 🥉.
- Три метрики + гістограма спільноти — 📎 / 🥉.
- 2D-зріз гри (вид збоку або згори) як учбовий проєкт замість 3D — 🥉.

## Мапа на каталог
- Є: `row-conveyor` / `carrier-platform` (конвеєри) · `gravity-fall` · `push-object` (штовхач) · `stick-together` (зварювання) · `multi-cell-size` (продукти) · `destructible-blocks` (лазер, евісцератор) · `teleport` · `collect-quota` · `drag-drop-piece` · `sequential-levels` / `level-unlock` / `level-select` / `world-map` · `in-game-editor` / `editor-playtest` / `level-exchange` · `leaderboard` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+block-placement-program` «Програма = розстановка механізмів» · game-logic/program · 🥈.
  - `+sensor-signal-wire` «Сенсор і провід передають сигнал» · entities/interact · 🥈; `+signal-actuator` «Виконавець діє за сигналом» · 🥉.
  - `+weld-adjacent` «Зварювання сусідніх блоків назавжди» · entities/interact · 🥉.
  - `+block-rotator` · entities/move · 🥉; `+vertical-lifter` · entities/move · 📎; `+retractable-blocker` · entities/state · 📎; `+laser-cutter` · entities/interact · 📎.
  - `+input-respawn`, `+molecule-match-output`, `+collision-halt`, `+solution-metrics`, `+metric-histograms` (запропоновано в Opus Magnum/SpaceChem).
  - `+sandbox-mode` · 📎; `+first-person-builder` · interface/render · 👑 (3D); `+audio-logs` · 🌱.

## Пропозиції до словників
- `+trigger:signal(sensor)` — сенсор подав сигнал (подія сигнальної мережі).
- `+cond:signal(port)` — на вході механізму є сигнал.
- `+effect:weld(a, b)` — постійне зчеплення (≠ `attach`, який можна розірвати).
- `+effect:lift(a, n)` — підняти групу на N угору.
- `+effect:emit_signal(conduit)` — передати сигнал проводом.
- `+effect:destroy_line(dir)` — знищити все на лінії (лазер).
- `+role:actuator`, `+role:sensor`, `+role:product`.
- `+window:puzzle-info`, `+window:metric-histograms`.
- `+ui:block-hotbar`, `+ui:metric-panel`.
- `+feature:workshop`, `+feature:sandbox-containers`.

## Джерела
- ⭐ [Wikipedia: Infinifactory](https://en.wikipedia.org/wiki/Infinifactory) — 3D-блоки, перша особа й ранець, конвеєри, зварювачі, сенсори й штовхачі, падіння незакріплених блоків, footprint/cycles/blocks, гістограми, шість світів, Workshop з доведеним розвʼязком, Manufactoid/Infiniminer.
- [Steam](https://store.steampowered.com/app/300570/Infinifactory/) — 50+ пазлів, пісочниця, гістограми, Workshop, level editor.
- [Zachtronics: Infiniupdate 2](https://www.zachtronics.com/infiniupdate-2) — лазер, екструдовані входи, Test Zone X, телепортери й виділення області в редакторі, лінійна побудова.
- [namu.moe: Infinifactory](https://namu.moe/w/Infinifactory) — опис блоків (через результат пошуку, сторінку не відкривав).
- YouTube: пошук «infinifactory gameplay».

## Непевне
- (?) Фан-вікі (fandom) віддала 402; опис ліфта, блокера, ротатора — з корейської вікі через пошук і памʼяті.
- (?) Швидкість «1 клітина за цикл», поведінка деталі, що впала за край, реакція на неправильний продукт — з памʼяті.
- (?) Точне правило зварювання (які грані, чи зварювач сам приварюється) — з памʼяті.
- (?) Розкладка керування (WASD, ЛКМ/ПКМ) — з памʼяті.
- (?) Як подаються аудіологи і чи є покроковий режим — з памʼяті.
