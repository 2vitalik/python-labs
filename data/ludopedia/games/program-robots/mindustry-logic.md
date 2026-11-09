---
title: Mindustry — logic (mlog)
slug: mindustry-logic
aka: [mlog, Mindustry Logic, World processor, Логіка Mindustry]
family: program-robots
also: [build-sim, tower-lanes]
klass: hybrid
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: 2020
platforms: [PC, Mac, Linux, Android, iOS]
links:
  - {kind: official, url: "https://mindustrygame.github.io/wiki/logic/0-introduction/", best: true, note: "офіційна вікі: що вміє mlog (блоки, юніти, дисплеї, повідомлення, памʼять, перемикачі, математика); натхнення асемблером"}
  - {kind: official, url: "https://mindustrygame.github.io/wiki/logic/3-variables/", note: "set, @this, @counter, @ipt (2/8/25), @links, @unit, @tick (60/с), імена лінкованих будівель"}
  - {kind: official, url: "https://mindustrygame.github.io/wiki/logic/2-editing/", note: "візуальний блоковий редактор і текстовий експорт/імпорт"}
  - {kind: official, url: "https://mindustrygame.github.io/wiki/logic/1-glossary/", note: "типи: number (double), Building, Unit, content @…, senseable, target, comp у jump"}
  - {kind: other, url: "https://raw.githubusercontent.com/Anuken/Mindustry/master/core/assets/bundles/bundle.properties", note: "рядки lst.* — офіційні описи всіх інструкцій (зокрема світові)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mindustry+logic+tutorial", note: "пошук; туторіали"}
stage: v1
coverage: 55
mechanics: [command-program, sensor-predicates, step-execution, code-editor-window, user-procedures, fsm-program, coverage-area, gui-render, in-game-editor, +ipt-speed-tiers, +building-link, +unit-bind-control, +print-buffer-flush, +draw-buffer-display, +memory-cell, +program-counter-variable, +privileged-world-processor, +block-code-editor, +text-code-export]
proposes: ["+trigger:exec(cmd)", "+effect:jump(to)", "+effect:wait", "+effect:bind(unit_type)", "+effect:flush(target)", "+role:processor", "+role:memory", "+window:block-code-editor", "+ui:link-lines", "+feature:code-export-text", "+card:privileged-world-processor"]
author: opus
date: 2026-11-09
---

# Mindustry, логіка — процесор-будівля з асемблероподібним кодом читає й керує сусідніми будівлями та юнітами на мапі

## Суть
Шар програмування поверх TD-фабрики [mindustry](../build-sim/mindustry.md) (з v6, 2020): гравець ставить процесор, лінкує до нього будівлі (турелі, конвеєри, перемикачі, дисплеї, комірки памʼяті) і пише код у стилі асемблера — одна інструкція за раз. Код читає стан будівель і юнітів (`sensor`, `radar`), керує ними (`control`, `ucontrol`), малює на дисплеях і друкує в повідомлення. Типові задачі: автоприцілювання турелей, балансування ресурсів, рої юнітів-шахтарів. Для мапмейкерів — невразливий світовий процесор з привілейованими інструкціями (спавн, зміна клітин, правила).

## Поле і час
- Поле — клітинна мапа Mindustry; процесор — будівля 1×1 (?) із радіусом лінкування (?).
- Час: 60 тіків/с (`@tick`); процесор виконує фіксовану кількість інструкцій за тік — `@ipt`: Micro 2, Logic 8, Hyper 25.
- Програма циклічна: після останнього рядка або `end` — знову з першого.
- `@counter` — номер наступного рядка; запис у нього = перехід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Micro / Logic / Hyper Processor | player | ipt 2 / 8 / 25 | виконує код циклічно; «швидший» — більше інструкцій за тік |
| World Processor | spawner | лише в редакторі мап | невразливий; привілейовані інструкції (spawnunit, setblock, setrule, explosion, cutscene…) |
| Змінна | container | number (double) / Object / String | створюється першим `set`; неіснуюча = null = 0 |
| Лінкована будівля | object | імʼя `тип+N` (scatter1, ripple3) | читається `sensor`, керується `control`; `getlink i` з 0 |
| Memory Cell / Memory Bank | container | ємність мала / велика | `read`/`write` за індексом; також змінні інших процесорів |
| Message | sink | текст | показує буфер `print` після `printflush` |
| Logic Display / Large / Tiled; Canvas | sink | растр | виконує буфер `draw` після `drawflush` |
| Switch | switch | вкл/викл | стан читається й задається з коду; клік гравця перемикає |
| Юніт | ally | тип, @unit | `ubind` привʼязує наступного юніта типу; `ucontrol` рухає/будує/копає |
| Інструкції вводу/виводу | — | `read` `write` `print` `printchar` `format` `draw` `drawflush` `printflush` | буфери тексту й малювання, памʼять |
| Інструкції блоків | — | `getlink` `control` `radar` `sensor` | лінк за індексом, керування будівлею, пошук юнітів у радіусі будівлі, читання властивості |
| Операції | — | `set` `op` `select` `lookup` `packcolor` `unpackcolor` | присвоєння, математика над 1–2 значеннями, умовний вибір, тип за ID |
| Потік | — | `wait` `stop` `end` `jump` | пауза в секундах, зупинка, на початок, умовний стрибок (comp або `always`) |
| Інструкції юнітів | — | `ubind` `ucontrol` `uradar` `ulocate` | привʼязка, керування, радар навколо юніта, пошук будівлі/руди на всій мапі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «процесор виконує @ipt інструкцій від @counter»`.
- КОЛИ `exec(end)` → ТО `custom: «@counter = 0»`; після останнього рядка — так само.
- КОЛИ `exec(jump)` → ЯКЩО `custom: «comp(a, b) істинне або always»` → ТО `jump(line)`.
- КОЛИ `exec(set)` → ЯКЩО `custom: «змінної нема»` → ТО `custom: «створити й присвоїти»`.
- КОЛИ `exec(op)` → ТО `set_value(dst, a op b)`; `custom: «бітові зсуви — над int64»`.
- КОЛИ `exec(sensor)` → ТО `custom: «записати властивість будівлі/юніта (@totalAmmo, @health, @type…)»`.
- КОЛИ `exec(control)` → ТО `custom: «увімкнути / прицілити / вистрілити будівлею»`.
- КОЛИ `exec(radar)` → ЯКЩО `in_range(building, unit, range)` → ТО `custom: «повернути юніта за фільтром і сортуванням»`.
- КОЛИ `exec(ubind)` → ТО `custom: «@unit = наступний юніт типу»`; КОЛИ `exec(ucontrol)` → ТО `move(@unit, to)` або `custom: «копати / будувати / взяти предмет»`.
- КОЛИ `exec(ulocate)` → ЯКЩО `has(@unit, bound)` → ТО `custom: «знайти будівлю/руду на всій мапі»`.
- КОЛИ `exec(print)` → ТО `custom: «додати текст у буфер»`; КОЛИ `exec(printflush)` → ТО `custom: «вивести буфер у Message»`.
- КОЛИ `exec(draw)` → ТО `custom: «додати фігуру в буфер»`; КОЛИ `exec(drawflush)` → ТО `custom: «намалювати на дисплеї»`.
- КОЛИ `exec(read|write)` → ТО `custom: «комірка памʼяті за індексом / змінна іншого процесора»`.
- КОЛИ `exec(wait)` → ТО `custom: «пауза N секунд»`; КОЛИ `exec(stop)` → ТО `custom: «процесор зупинено»`.
- КОЛИ `custom: «тип не той: число замість Object»` → ТО `custom: «null; Object замість числа → 1 або 0»`.
- Світовий процесор: КОЛИ `exec(spawnunit|setblock|explosion|spawnwave|setrule)` → ТО `spawn_at(unit, xy)` / `set_cell(xy, block)` / `explode(area)` / `custom: «хвиля, правило гри»`.
- Перемога / поразка — від мапи Mindustry (ядро ціле), не від коду.

## Керування і ввід
- Поставити процесор → клік по будівлях у радіусі — лінк (лінія від процесора) (?); повторний клік знімає (?).
- Кнопка-олівець у вікні процесора → візуальний редактор: кольорові блоки-інструкції, drag-drop, вибір параметрів, стрілки стрибків; працює на мобільних.
- Експорт у текст / імпорт з буфера: код пишуть у зовнішньому редакторі (є підсвітка для VS Code, Vim, Emacs, Sublime).

## Вікна, меню, HUD
- `game-screen`: мапа з лініями лінків від процесора (custom-ui `link-lines`).
- `block-code-editor` (custom): список кольорових блоків-інструкцій із полями параметрів, стрілки `jump`, кнопки Add / Edit (Copy/Import) (?).
- `code-editor-window` для текстового імпорту/експорту (через буфер обміну).
- Message — спливний текст над блоком; дисплеї — растр на мапі.
- Переходи: мапа → процесор → редактор → назад; код працює одразу.

## Фічі поза полем
- `code-export-text` — код як рядок; ділитись у Discord, вставляти в схеми (?).
- Редактор мап зі світовими процесорами, world cell / world message / world switch — сценарії й туторіали на логіці.
- `sync` змінної в мультиплеєрі (≤ 20 разів/с на змінну); маркери світу (до 20 000).

## Варіації й родичі
- [factorio-circuit-network](factorio-circuit-network.md) — схеми без коду; [tis-100](tis-100.md) — асемблер на сітці вузлів; [screeps](screeps.md) — JS керує юнітами на мапі; [core-war](core-war.md).
- Компілятори вищого рівня до mlog від спільноти (mindcode тощо) (?).
- **Осі варіацій:** звідки дані (лінковані будівлі / весь світ) · швидкість (ipt за рівнем процесора) · вивід (повідомлення / растровий дисплей) · привілеї (звичайний / світовий процесор).

## Цікавинки для курсу
- Інтерпретатор mlog-підмножини (`set`, `op`, `jump`, `end`, `print`) з `@counter` і ipt — 🥉.
- Буфери `print`/`draw` з явним flush — 📎.
- Будівля-процесор, що лінкує сусідів у радіусі й дає їм імена `тип+N` — 📎.
- `ubind`-цикл: процесор по черзі керує всіма юнітами типу (рій шахтарів) — 🥈.
- Візуальний блоковий редактор ↔ текст (серіалізація в обидва боки) — 🥈.
- Світовий процесор як скриптовий рушій сценаріїв — 🥇.

## Мапа на каталог
- Є: `command-program` · `sensor-predicates` (`sensor` + `jump`) · `step-execution` (ipt) · `code-editor-window` · `user-procedures` (через `@counter`) (?) · `fsm-program` · `coverage-area` (радіус лінку/радара) · `gui-render` · `in-game-editor` (мапи зі світовими процесорами).
- **Нема** → пропозиції карток:
  - `+ipt-speed-tiers` «Швидкість процесора — інструкцій за тік» · game-logic/program · 🌱.
  - `+building-link` «Процесор лінкує будівлі в радіусі, імена тип+N» · entities · 📎.
  - `+unit-bind-control` · 🥈; `+print-buffer-flush` · 📎; `+draw-buffer-display` · 🥉; `+memory-cell` · 📎.
  - `+program-counter-variable` «Лічильник команд як звичайна змінна» · 🌱; `+privileged-world-processor` · 🥇.
  - `+block-code-editor` · 🥈; `+text-code-export` · 📎.

## Пропозиції до словників
- `+trigger:exec(cmd)` — уже в 🔥, тут підтвердження (кілька сутностей-процесорів).
- `+effect:jump(to)`, `+effect:wait` — як у TIS-100 (підтвердження).
- `+effect:bind(unit_type)` — програма привʼязує зовнішню сутність для керування.
- `+effect:flush(target)` — вивести накопичений буфер на пристрій.
- `+role:processor`, `+role:memory`.
- `+window:block-code-editor`, `+ui:link-lines`, `+feature:code-export-text`, `+card:privileged-world-processor`.

## Джерела
- ⭐ [Mindustry Wiki: Logic introduction](https://mindustrygame.github.io/wiki/logic/0-introduction/) — що вміє mlog, натхнення асемблером, v6.
- [Mindustry Wiki: Variables and Constants](https://mindustrygame.github.io/wiki/logic/3-variables/) — `set`, `@counter`, `@ipt` 2/8/25, `@links`, `@unit`, `@tick`, імена лінків.
- [Mindustry Wiki: Writing and Editing Code](https://mindustrygame.github.io/wiki/logic/2-editing/) — візуальний редактор, експорт у текст.
- [Mindustry Wiki: Glossary](https://mindustrygame.github.io/wiki/logic/1-glossary/) — типи, senseable, target, comp.
- [bundle.properties (GitHub)](https://raw.githubusercontent.com/Anuken/Mindustry/master/core/assets/bundles/bundle.properties) — офіційні описи всіх інструкцій `lst.*` і блоків.
- YouTube: пошук «mindustry logic tutorial».

## Непевне
- (?) Радіус лінкування процесорів, розмір процесора, ємність Memory Cell (64?) / Bank (512?), роздільність дисплеїв (80×80? / 176×176?) — сторінки блоків віддали 404.
- (?) Деталі `ucontrol` (move, approach, mine, build, itemTake…) і `radar` (фільтри enemy/ally/flying, сортування distance/health) — з памʼяті.
- (?) Як саме знімається лінк і чи будівлі лінкуються автоматично при постановці поруч.
- (?) Компілятори спільноти (mindcode) — з памʼяті.
