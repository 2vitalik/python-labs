---
title: Toki Tori
slug: toki-tori
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2001
platforms: [Game Boy Color, WiiWare (2008), iOS (2009), PC Steam (2010)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Toki_Tori", best: true, note: "інструменти, вороги, світи, rewind у PC-версії, платформи"}
  - {kind: steam, url: "https://store.steampowered.com/app/38700/", note: "Toki Tori (2010) на Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=toki+tori+gameplay+walkthrough", note: "пошук; проходження рівнів"}
stage: v1
coverage: 70
mechanics: [move-4dir, gravity-fall, collect-all, touch-death, player-death, enemy-patrol, inventory-items, inventory-limit, teleport, temporary-modes, sequential-levels, level-unlock, level-select, time-out, status-panel, goal-counter, +tool-allotment, +place-bridge, +place-block, +freeze-into-block, +floor-collapse-for-enemy, +redirect-enemy, +ladder-climb, +look-around-mode, +rewind]
proposes: ["+effect:use_tool", "+effect:place", "+cond:charges", "+trigger:turn_at_obstacle", "+window:tool-select", "+ui:tool-charges", "+feature:rewind", "+axis:undo", "+card:tool-allotment"]
author: opus
date: 2026-11-02
---

# Toki Tori — курча збирає яйця, маючи на рівень лише кілька зарядів кожного інструмента

## Суть
Курча Toki Tori ходить платформним рівнем і має зібрати всі яйця. Стрибати по-справжньому не вміє (лише півкроку вгору), тому прохід будує **інструментами з обмеженим числом зарядів на рівень**: міст через прірву, телепорт крізь стіну, ящик у яму, заморозка ворога в лід-блок, пастка для привидів, відсмоктувач слимаків. Рівень — головоломка «в якому порядку й де витратити заряди»; неправильне використання робить рівень нерозвʼязним. Вороги патрулюють і вбивають дотиком, але є й будівельним матеріалом (заморожений ворог = блок).

## Поле і час
- Бічний вид, квадратна сітка платформ (рівні більші за екран — камера слідує; інструмент Eyes дозволяє оглянути).
- Гравітація: без опори курча падає; є драбини (?) і уступи на 1 клітину, на які можна вийти «півстрибком».
- Час: real-time, але рівень детермінований (жодного рандому) — по суті пазл: розвʼязок відтворюваний покроково. Таймер рівня згаданий у Wikipedia (?).
- Світ «Bubble Barrage» — під водою: інша фізика (вільний рух у Bubble Suit, лід спливає).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Toki Tori | player | 1 дотик = смерть | ходить ліво/право, піввисотний «стрибок» на уступ, падає, лазить (?) |
| Яйце | pickup | — | зібрати всі на рівні |
| Стіна/платформа | static | — | опора, непрохідна |
| Кам'яна підлога | terrain | — | під привидом провалюється, якщо поставлено Ghost Trap |
| Міст (Bridge) | object | заряди N | ставиться над прірвою перед курчам — нова опора |
| Telewarp | — (інструмент) | заряди N | переносить курча крізь стіни в обрану точку (?) |
| InstantRock / Crate | object | заряди N | блок у клітину: заповнює яму, стає опорою або барикадою |
| Freeze-O-Matic | — (інструмент) | заряди N | ворог → крижаний блок (опора/перешкода); під водою лід спливає |
| Ghost Trap | — (інструмент) | заряди N | кам'яна підлога провалюється, коли на неї ступає привид |
| Snail Sucker | — (інструмент) | заряди N | повне всмоктування прибирає слимака; часткове — розвертає без витрати заряду |
| Bubble Suit | — (інструмент) | 5/10/15 зарядів | під водою: зсув на пів клітини в 4 напрямки; підзарядка в точках |
| Brick Switch | — (інструмент) | заряди N | перемикає певні блоки (?) |
| Eyes | — (інструмент) | ∞ | пауза курчати й ворогів, огляд рівня камерою |
| Слимак | enemy | напрям | повзе, на перешкоді розвертається |
| Привид | enemy | напрям | патрулює; знищується лише Ghost Trap-провалом |
| Інші вороги (по світах) | enemy | напрям | патруль «до перешкоди → розворот» (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(toki, dir)`; ЯКЩО уступ висотою 1 → `custom: «вийти на уступ півстрибком»`; вище — `block`.
- КОЛИ `tick` → ЯКЩО `not supported(toki)` → ТО `fall(toki)`.
- КОЛИ `contact(toki, egg)` → ТО `pickup`, `counter(eggs_left, -1)`.
- КОЛИ `counter(eggs_left, ==, 0)` → ТО `win`, `next_level`.
- КОЛИ `contact(toki, enemy)` → ТО `lose` → рестарт рівня.
- КОЛИ `input(tool=bridge)` → ЯКЩО `has(toki, bridge)` і `custom: «перед курчам прірва»` → ТО `spawn_at(bridge, edge_ahead)`, `take(toki, bridge)`.
- КОЛИ `input(tool=crate, cell)` → ЯКЩО `has` і `free(cell)` → ТО `spawn_at(block, cell)`, `take`.
- КОЛИ `input(tool=telewarp, cell)` → ЯКЩО `has` і `free(cell)` → ТО `teleport(toki, cell)`, `take`.
- КОЛИ `input(tool=freeze, dir)` → ЯКЩО `has` і `line_of_sight(toki, enemy)` (?) → ТО `transform(enemy → ice_block)`, `take`; під водою `custom: «блок спливає»`.
- КОЛИ `input(tool=ghost_trap, cell)` → ЯКЩО `cell(cell, stone_floor)` → ТО `set_state(cell, trap)`; КОЛИ `enter(ghost, trap)` → ТО `set_cell(cell, empty)`, `fall(ghost)`.
- КОЛИ `input(tool=snail_sucker)` → ЯКЩО повне смоктання → ТО `disappear(slug)`, `take`; ЯКЩО коротке → ТО `face(slug, reverse)` без `take`.
- КОЛИ `input(tool=bubble_suit, dir)` → ТО `move(toki, dir, ½)`, `take`; `enter(toki, recharge_point)` → ТО `custom: «заряди = 5/10/15»`.
- КОЛИ `input(eyes)` → ТО `freeze(all)` окрім таймера; камера вільна.
- Вороги щотік: `blocked(a)` → `face(a, reverse)` (`enemy-patrol`).
- КОЛИ `custom: «рівень став нерозвʼязним»` → гравець сам тисне рестарт (або rewind на PC).
- Поразка: дотик ворога; таймер нуль (?). Рахунок: нема — мета рівня бінарна.

## Керування і ввід
- GBC: хрестовина — рух, кнопки — вибір і застосування інструмента.
- Wii: пульт-вказівник: клік — куди йти, вибір інструмента з панелі й ціль кліком (?).
- PC: миша/клавіатура + **rewind** (утримання — час назад, вперед — перемотка) як заміна рестарту.
- Інструмент застосовується в напрямку погляду або в клітину-ціль залежно від типу (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Play → `level-select` (світ → рівні, позначки пройдено) · Options → `settings-window` · Exit.
- `game-screen` — рівень, камера за курчам; HUD: `remaining-counter` яєць, панель інструментів з кількістю зарядів (`custom: «tool-charges»`), `timer-countdown` (?).
- `tutorial-window` — навчальні рівні з підказками до кожного інструмента.
- `pause-menu`: Continue · Restart level · Quit to map.
- `end-screen` рівня: короткий підсумок, далі.
- Переходи: main-menu → level-select → game-screen → (усі яйця) end-screen → level-select; game-screen → pause-menu → restart.

## Фічі поза полем
- Прогресія: 4 світи × 15 рівнів + навчальні; щоб відкрити наступний світ, треба 10 рівнів, останні 5 — складні необовʼязкові (`level-unlock`, `collectibles`-подібно).
- `rewind` (лише PC) — безперервне скасування замість рестарту.
- `restart-level`, `pause`, Eyes як вбудований режим огляду.
- Нема редактора в оригіналі; Toki Tori 2 (2013) — зовсім інший дизайн (без інструментів, «пісні» курчати).

## Варіації й родичі
- GBC (2001) → римейк WiiWare/PC/iOS (графіка 2D-HD, rewind на PC); Toki Tori 2/2+ (метроїдванія, механіки через тварин).
- Родичі: Lemmings (обмежені навички на рівень), Catrap і Kwirk (бічні клітинні пазли), Mario vs. Donkey Kong, Lode Runner (бічна сітка з гравітацією).
- Осі: **бюджет дій** (інструменти поштучно / загальний ліміт / необмежено); **відкат** (рестарт / undo / rewind); **вороги як ресурс** (заморожений ворог = блок).

## Цікавинки для курсу
- Бюджет інструментів на рівень, заданий у файлі рівня — 📎 (+ HUD з лічильниками).
- Заморожений ворог → блок-опора: ворог як будівельний матеріал — 🥉.
- Міст/блок/телепорт — три способи «створити клітину» під одним інтерфейсом `use_tool(tool, target)` — 🥉.
- Rewind як стек станів з безперервним прокручуванням — 🥈 (state-as-data + історія).
- Ghost Trap: відкладений ефект «клітина провалиться, коли на неї стане ворог певного типу» — 📎.
- Перевірка «рівень став нерозвʼязним» (заряди скінчились, яйце недосяжне) — 🥇 через пошук у просторі станів.

## Мапа на каталог
- Є: `move-4dir` (ліво/право + уступ) · `gravity-fall` · `collect-all` · `touch-death` · `player-death` · `enemy-patrol` · `inventory-items` + `inventory-limit` (заряди) · `teleport` (Telewarp) · `temporary-modes` (Eyes) · `sequential-levels` · `level-unlock` · `level-select` · `time-out` (?) · `game-pause` · `status-panel` · `goal-counter`.
- **Нема** → пропозиції карток:
  - `+tool-allotment` «Бюджет інструментів на рівень» · entities/state · 📎 · слот {tools: map}.
  - `+place-bridge` «Міст над прірвою» · entities/interact · 📎.
  - `+place-block` «Поставити блок у клітину» · entities/interact · 📎.
  - `+freeze-into-block` «Ворог → блок» · entities/interact · 🥉.
  - `+floor-collapse-for-enemy` «Підлога-пастка для типу ворога» · entities/interact · 📎.
  - `+redirect-enemy` «Розвернути ворога без знищення» · entities/move · 🌱.
  - `+ladder-climb` «Драбини» · entities/move · 📎 (спільна з Lode Runner).
  - `+look-around-mode` «Режим огляду рівня з паузою» · interface/render · 📎.
  - `+rewind` «Безперервний відкат часу» · game-logic/save · 🥈.

## Пропозиції до словників
- `+effect:use_tool(tool, target)` — застосувати інструмент з інвентаря до клітини/ворога (зменшує заряд).
- `+effect:place(cell, kind)` — поставити обʼєкт-клітину (міст, блок) — ширше за `spawn_at`, бо змінює прохідність.
- `+cond:charges(tool, op, n)` — лишилось зарядів (окремо від `has`, бо важить число).
- `+trigger:turn_at_obstacle` — як `blocked(a)`, але для патрулів, що розвертаються; можна лишити `blocked`.
- `+window:tool-select` — панель/колесо вибору інструмента (Wii).
- `+ui:tool-charges` — іконки інструментів із числом зарядів.
- `+feature:rewind` ↔ є в `features.md`; `+axis:undo` = `rewind` для PC-версії, `none` для GBC.
- `+card:tool-allotment` — див. вище.

## Джерела
- ⭐ [Wikipedia: Toki Tori](https://en.wikipedia.org/wiki/Toki_Tori) — усі інструменти з описом, Eyes, Bubble Suit, світи 4×15, rewind лише на PC, дати платформ.
- [Steam: Toki Tori](https://store.steampowered.com/app/38700/) — PC-версія (2010), 80+ рівнів у 4 світах.
- YouTube: пошук «toki tori gameplay walkthrough».

## Непевне
- (?) Таймер рівня: Wikipedia про нього пише, але в PC/Wii-версіях таймера, здається, нема — перевірити.
- (?) Brick Switch — назва з брифу куратора, у Wikipedia не знайдено; ефект невідомий.
- (?) Як цілиться Telewarp (вільна точка в радіусі чи фіксована дистанція) і Freeze-O-Matic (по прямій?).
- (?) Драбини й точна висота «півстрибка»; назви ворогів, окрім слимаків і привидів.
- (?) Wii-керування вказівником.
- Пошуковий ліміт сесії вичерпано до глибшої перевірки — опис спирається переважно на Wikipedia і Steam.
