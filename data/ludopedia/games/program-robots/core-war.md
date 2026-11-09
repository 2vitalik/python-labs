---
title: Core War
slug: core-war
aka: [Core Wars, CoreWar, Redcode, MARS, Корові війни]
family: program-robots
also: [chess-abstract]
klass: cursor
axes:
  field: 1d
  time: programmed
  opponent: online
  info: partial
  random: setup
  goal: survive
year: 1984
platforms: [PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Core_War", best: true, note: "кільцева памʼять, відносна адресація, черга процесів, SPL/DAT, 8 режимів адресації, стратегії paper/scissors/stone/imp"}
  - {kind: other, url: "https://esolangs.org/wiki/Redcode", note: "Redcode-94: опкоди з семантикою, модифікатори, Imp і Dwarf"}
  - {kind: other, url: "https://corewar.info/lexicon/94draft.htm", note: "ICWS-94 draft: стандартні параметри (CORESIZE 8000…), семантика модифікаторів .A…/.I"}
  - {kind: other, url: "https://corewar.co.uk/", note: "хаб спільноти (гайди, пагорби, інструменти); відкривається через перевірку на бота"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=core+war+redcode+pmars", note: "пошук; бої в pMARS"}
stage: v1
coverage: 55
mechanics: [command-program, step-execution, code-editor-window, wrap-edges, state-as-data, level-from-txt, leaderboard, rating-system, replay, console-render, ai-opponent, +self-modifying-playfield, +shared-memory-battle, +relative-addressing, +addressing-modes, +instruction-modifiers, +process-queue-split, +round-robin-scheduler, +illegal-instruction-death, +random-load-distance, +cycle-limit-draw, +persistent-private-memory, +hill-tournament, +warrior-archetypes-rps, +core-visualizer]
proposes: ["+trigger:program_dead(side)", "+effect:fork(process, at)", "+effect:skip_next", "+effect:jump(to)", "+cond:field_value(op, n)", "+role:process", "+role:instruction-cell", "+window:core-view", "+window:hill-table", "+ui:process-counter", "+feature:hill-submission", "+feature:p-space", "+axis:turn-structure:round-robin"]
author: opus
date: 2026-11-09
---

# Core War — дві програми-воїни в одній кільцевій памʼяті переписують одна одну, доки в суперника не лишиться живих процесів

## Суть
Гравець пише на асемблері **Redcode** програму-«воїна». Два (або більше) воїни завантажуються у спільну кільцеву памʼять **MARS**, і віртуальна машина по черзі виконує по одній інструкції кожного. Програма може писати будь-куди: бомбити памʼять інструкціями `DAT`, копіювати себе, сканувати чужий код. Процес, що виконав `DAT` (або ділення на нуль), гине; воїн без процесів програв. Ввід/вивід у грі немає — лише результат бою.

## Поле і час
- Поле — **1D-кільце** з `CORESIZE` клітин (стандарт ICWS-94 — 8000); кожна клітина — одна інструкція (опкод, модифікатор, два поля з режимами адресації). Кінець памʼяті зшитий з початком.
- Адресація лише **відносна**: 0 — поточна інструкція, 1 — наступна; абсолютної адреси програма дізнатись не може.
- На старті вся памʼять заповнена `DAT 0, 0`; воїнів кладуть у випадкові позиції не ближче за `MINDISTANCE` (стандарт — 100) одне до одного.
- Тік (цикл) = одна інструкція одного процесу; воїни чергуються, а процеси одного воїна ділять його частку часу (воїн з 10 процесами виконує кожен у 10 разів рідше).
- Бій обмежено `MAXCYCLES` (стандарт — 80000); не встигли — нічия. Параметри (розмір памʼяті, кількість процесів 8000, довжина воїна 100) — налаштування турніру/пагорба.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина памʼяті (core cell) | terrain | опкод, модифікатор, поле A, поле B, режими | зберігає інструкцію; читається й переписується будь-ким |
| Воїн (warrior) | player | ≤ MAXLENGTH інструкцій, черга процесів | завантажується в памʼять; живий, поки є хоч один процес |
| Процес (instruction pointer) | object | адреса поточної інструкції | виконує інструкцію, переходить на наступну/ціль стрибка |
| Черга процесів (task queue) | container | ≤ MAXPROCESSES | FIFO: процес після кроку стає в кінець; SPL додає новий |
| `DAT` | hazard | два поля даних | виконання вбиває процес; водночас — «бомба» і комірка даних |
| `MOV` | object | A → B | копіює поле або всю інструкцію (`.I`) — основа бомб і копіювання |
| `ADD` / `SUB` / `MUL` | object | A, B | арифметика над полями B (MUL — лише '94) |
| `DIV` / `MOD` | object | A, B | ділення/залишок; на нуль — процес гине |
| `JMP` | object | A | безумовний стрибок |
| `JMZ` / `JMN` | object | A, B | стрибок, якщо B нуль / не нуль |
| `DJN` | object | A, B | зменшити B, стрибок, якщо не нуль — цикл-лічильник |
| `SEQ` (`CMP`) / `SNE` / `SLT` | object | A, B | пропустити наступну інструкцію, якщо рівні / не рівні / A < B — основа сканерів |
| `SPL` | spawner | A | новий процес з адресою A у черзі воїна |
| `NOP` | object | — | нічого |
| `LDP` / `STP` | object | A, B | читати/писати приватну P-space (лише на пагорбах з P-space) |
| P-space | container | 1/16 CORESIZE клітин | приватна памʼять воїна, що переживає раунди серії |
| Режими адресації | mark | `#` `$` `*` `@` `{` `<` `}` `>` | безпосередній, прямий, непрямий через A/B, з пред-декрементом і пост-інкрементом |
| Модифікатори | mark | `.A` `.B` `.AB` `.BA` `.F` `.X` `.I` | які поля читати/писати: одне, обидва, навхрест, уся інструкція |
| Imp | player | 1 інструкція `MOV 0, 1` | копіює себе на крок уперед і там виконується — «повзе» памʼяттю |
| Dwarf | player | 4 інструкції | кидає `DAT`-бомбу кожні 4 клітини — перший «stone» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «памʼять заповнено DAT 0,0»`, `spawn_at(warrior, random)` ЯКЩО `custom: «відстань до інших ≥ MINDISTANCE»`.
- КОЛИ `tick` → ТО `custom: «наступний воїн за колом бере перший процес зі своєї черги й виконує одну інструкцію»`.
- КОЛИ `exec(cmd)` → ТО `custom: «обчислити адреси A і B за режимами адресації; пред-декремент до, пост-інкремент після»`.
- КОЛИ `custom: «адреса виходить за 0..CORESIZE−1»` → ТО `wrap(address)` — усі адреси за модулем CORESIZE.
- КОЛИ `exec(MOV)` → ТО `set_value(cell_B, value_A)` — поле, пара полів або вся інструкція за модифікатором.
- КОЛИ `exec(ADD|SUB|MUL)` → ТО `set_value(cell_B, B ± A | B × A)`.
- КОЛИ `exec(DIV|MOD)` → ЯКЩО `custom: «дільник = 0»` → ТО `crash` (процес гине); інакше `set_value(cell_B, B / A | B mod A)`.
- КОЛИ `exec(DAT)` → ТО `crash` — процес знято з черги.
- КОЛИ `exec(JMP)` → ТО `custom: «процес переходить на адресу A»`.
- КОЛИ `exec(JMZ|JMN)` → ЯКЩО `counter(B, ==|!=, 0)` → ТО `custom: «перехід на A»`; інакше на наступну.
- КОЛИ `exec(DJN)` → ТО `counter(B, −1)`; ЯКЩО `counter(B, !=, 0)` → ТО `custom: «перехід на A»`.
- КОЛИ `exec(SEQ|SNE|SLT)` → ЯКЩО `same(A, B, value)` (або протилежне / A < B) → ТО `custom: «пропустити наступну інструкцію»`.
- КОЛИ `exec(SPL)` → ЯКЩО `count(process, <, MAXPROCESSES)` → ТО `clone(process)` — новий процес на адресі A стає в кінець черги після поточного.
- КОЛИ `exec(LDP|STP)` → ТО `custom: «обмін значенням між памʼяттю і приватною P-space»`.
- КОЛИ `custom: «процес виконав крок і не загинув»` → ТО `custom: «процес повертається в кінець черги»`.
- КОЛИ `all_gone(process_of_warrior)` → ТО `custom: «воїн вибуває»`.
- КОЛИ `count(alive_warrior, ==, 1)` → ТО `win` для того, хто вижив.
- КОЛИ `counter(cycles, ==, MAXCYCLES)` → ЯКЩО `count(alive_warrior, >, 1)` → ТО `draw`.
- КОЛИ `custom: «новий воїн надіслано на пагорб»` → ТО `custom: «серія раундів проти кожного з пагорба, таблиця за очками, останній вибуває»`.
- Перемога: у суперника не лишилось процесів · Поразка: усі твої процеси загинули · Нічия: MAXCYCLES вичерпано · Рахунок: очки за серію раундів на пагорбі; вік (скільки воїнів пережив на пагорбі).

## Керування і ввід
- Гравець пише текст Redcode у будь-якому редакторі: мітки, `ORG`/`END` (точка старту), `EQU` (константи), `FOR`/`ROF` (макроповтор) (?).
- Запуск — симулятор MARS (pMARS, SDL pMARS, веб-реалізації): вибір воїнів, параметри (CORESIZE, MAXCYCLES, кількість раундів), режим з графікою або «тихий» підрахунок.
- Під час бою — нуль вводу; у дебагері pMARS (?) — покрокове виконання, перегляд клітин і черги.
- Турнір — надсилання файла воїна на сервер пагорба (історично — e-mail) (?).

## Вікна, меню, HUD
- `code-editor` (будь-який текстовий): програма воїна.
- `core-view` (custom): памʼять як прямокутник точок-клітин; колір — хто останнім писав/виконував; видно бомби, копії, імпи.
- HUD бою: `process-counter` (кількість процесів кожного воїна), `turn-counter` (поточний цикл), імена воїнів, `step-button`, `speed-slider`.
- `end-screen`: результати серії раундів (перемоги/поразки/нічиї кожного).
- `hill-table` (custom, веб-сторінка пагорба): місце, очки, % перемог, вік воїна.
- `settings-window` / командний рядок: параметри MARS.
- Переходи: редактор → симулятор (бій) → результати → правка; редактор → пагорб → таблиця.

## Фічі поза полем
- `custom-rules`: параметри пагорба (розмір памʼяті, довжина воїна, кількість процесів, стандарт '88/'94, P-space так/ні) — окремі «ліги» (nano, tiny, standard…).
- `leaderboard-online`: пагорби King of the Hill; новий воїн грає проти всіх, найслабший вилітає.
- `step-mode`, `speed-control` у симуляторах.
- `export-import`: воїн — текстовий файл `.red`; архіви воїнів спільноти.
- Еволюційні «evolvers» — генетичні алгоритми, що вирощують воїнів (nano, tiny).

## Варіації й родичі
- Стандарти: Dewdney 1984 (8 інструкцій), ICWS-86 (10), ICWS-88 (11), ICWS-94 draft (16 + модифікатори + 8 режимів) — де-факто чинний.
- Варіанти ігор: CoreWars 8086 (воїни на машинному коді x86) (?), Tierra/Avida — «штучне життя» з тією ж ідеєю памʼяті як середовища.
- Предки: Darwin (Bell Labs, 1961), Creeper/Reaper.
- Родичі в корпусі: [befunge](befunge.md) (програма = поле, що може себе переписати), [bot-arenas](bot-arenas.md) (бої ботів, рейтинг, автоматичні турніри), [human-resource-machine](human-resource-machine.md) і TIS-100 (асемблер як гра), [screeps](screeps.md) (код воює без гравця).
- Осі варіацій: **поле** (1D-кільце / 2D-сітка в Befunge / арена ботів); **смерть** (нелегальна інструкція / HP); **паралелізм** (черга процесів зі SPL / один потік); **памʼять між раундами** (нема / P-space); **адресація** (відносна / абсолютна).
- Архетипи-«камінь-ножиці-папір»: paper (реплікатор) бʼє stone (бомбер), stone бʼє scissors (сканер), scissors бʼє paper; плюс imp, vampire (пастка-«яма»), quickscanner, core clear.

## Цікавинки для курсу
- Міні-MARS: кільцева памʼять, 5–6 опкодів (`DAT MOV ADD JMP JMZ SPL`), черга процесів, два воїни — 🥈 (інтерпретатор + планувальник).
- Режими адресації й модифікатори як окрема таблиця «що читати/куди писати» — 🥉 / 🥈 за повний набір '94.
- Справедливий round-robin: воїн з N процесами виконує кожен N-кратно рідше — 📎.
- Візуалізатор памʼяті: смуга клітин з кольором автора запису — 🥉.
- Турнір «кожен з кожним» з очками й випаданням найслабшого (пагорб) — 🥉.
- Еволюція воїнів генетичним алгоритмом (мутації інструкцій, фітнес = бої з пагорбом) — 🥇.

## Мапа на каталог
- Є: `command-program` (воїн — програма) · `step-execution` (дебагер) · `code-editor-window` · `wrap-edges` (кільце памʼяті) · `state-as-data` (памʼять = стан) · `level-from-txt` (воїн з файла `.red`) · `leaderboard` / `rating-system` (пагорби) · `replay` · `console-render` · `ai-opponent` (воїн як суперник).
- **Нема** → пропозиції карток:
  - `+self-modifying-playfield` «Програма переписує поле, на якому живе» · game-logic/program · 🥈 (спільна з Befunge).
  - `+shared-memory-battle` «Бій програм у спільній памʼяті» · game-logic/opponent · 🥈.
  - `+relative-addressing` · game-logic/program · 📎; `+addressing-modes` «Режими адресації операндів» · game-logic/program · 🥉; `+instruction-modifiers` · 🥉.
  - `+process-queue-split` «Розгалуження процесу в черзі» · game-logic/program · 🥉; `+round-robin-scheduler` · 📎.
  - `+illegal-instruction-death` «Виконав DAT — загинув» · game-logic/lose · 🌱.
  - `+random-load-distance` «Випадкове розміщення з мінімальною відстанню» · levels/generation · 🌱; `+cycle-limit-draw` · game-logic · 🌱.
  - `+persistent-private-memory` «P-space між раундами» · game-logic/program · 📎.
  - `+hill-tournament` «Пагорб: новий учасник грає з усіма, слабший вибуває» · interface/results · 🥉.
  - `+warrior-archetypes-rps` — «камінь-ножиці-папір» стратегій (текст, не код) · 🌱; `+core-visualizer` · interface/render · 🥉.

## Пропозиції до словників
- `+trigger:program_dead(side)` — у сторони не лишилось процесів (ширше за `all_gone`: подія для сторони, не виду).
- `+effect:fork(process, at)` — створити паралельний потік виконання (SPL; ≠ `clone` сутності на полі).
- `+effect:skip_next` — пропустити наступну інструкцію (SEQ/SNE/SLT; також Befunge `#`).
- `+effect:jump(to)` — перенести вказівник програми (JMP/JMZ/DJN; ≠ `teleport` сутності).
- `+cond:field_value(op, n)` — значення поля інструкції порівняно з N.
- `+role:process`, `+role:instruction-cell`.
- `+window:core-view`, `+window:hill-table`; `+ui:process-counter`.
- `+feature:hill-submission`, `+feature:p-space`.
- `+axis:turn-structure:round-robin` — нове значення наявної осі (по інструкції на воїна, процеси діляться часткою).

## Джерела
- ⭐ [Wikipedia: Core War](https://en.wikipedia.org/wiki/Core_War) — історія (Dewdney, Jones, 1984), кільцева памʼять, черга процесів, DAT/ділення на нуль, кількість інструкцій у стандартах, 8 режимів адресації, стратегії, pMARS.
- [Esolangs: Redcode](https://esolangs.org/wiki/Redcode) — семантика опкодів '94, список модифікаторів, Imp і Dwarf.
- [corewar.info: ICWS-94 draft](https://corewar.info/lexicon/94draft.htm) — стандартні параметри й семантика модифікаторів.
- [corewar.co.uk](https://corewar.co.uk/) — хаб спільноти (віддав лише перевірку на бота).
- YouTube: пошук «core war redcode pmars».

## Непевне
- (?) Очки на пагорбах (типово 3 за перемогу, 1 за нічию) і кількість раундів у серії — з памʼяті; джерела, що відкрились, цього не кажуть.
- (?) MINDISTANCE = 100 — дефолт драфту '94; на конкретних пагорбах може відрізнятись.
- (?) Псевдоопи `EQU`, `FOR/ROF`, `ORG`, `PIN` і правила модифікаторів за замовчуванням — з памʼяті.
- (?) Деталі дебагера pMARS і веб-симуляторів, формат надсилання на пагорби — з памʼяті.
- (?) CoreWars 8086 як окремий варіант — з памʼяті.
