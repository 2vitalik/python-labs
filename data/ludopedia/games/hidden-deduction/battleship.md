---
title: Battleship (Морський бій)
slug: battleship
family: hidden-deduction
also: [pencil-logic, board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1931
platforms: [paper, board (Milton Bradley 1967), Electronic Battleship (1977), PC, web, mobile, Nintendo DS (Clubhouse Games)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battleship_(game)", best: true, note: "правила, склади флоту за виданнями, Salvo, історія 1931 → 1967 → 1977"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battleship_(puzzle)", note: "соло-пазл (Bimaru): лічильники рядів, заборона дотику, NP-повнота"}
  - {kind: other, url: "https://www.datagenetics.com/blog/december32011/", note: "DataGenetics: стратегії AI — random / hunt-target / парність / щільність імовірностей, медіани пострілів"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=battleship", note: "пошук BGG; видання й варіанти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battleship+board+game+how+to+play", note: "пошук; правила настолки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battleship+puzzle+bimaru+solving", note: "пошук; розвʼязування пазла"}
stage: v1
coverage: 75
mechanics: [cell-click, hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, destroy-all-enemies, multi-cell-size, drag-drop-piece, game-screen, end-screen, main-menu, settings-window, help-window, difficulty-levels, field-size-picker, satisfy-constraints, completion-detection, unique-puzzle-generation, level-solver, sound-effects, +fleet-placement, +shot-feedback, +sunk-announce, +salvo-shots, +hunt-target-ai, +probability-density-ai, +line-sum-clue, +no-touch-placement, +dual-board-view]
proposes: ["+trigger:placement_done", "+cond:all_cells_hit", "+effect:mark", "+effect:reveal", "+effect:announce", "+role:piece", "+role:mark", "+ui:own-board", "+ui:target-board", "+ui:fleet-status", "+ui:line-clue", "+window:placement-screen", "+window:pass-device", "+feature:salvo-mode", "+card:fleet-placement", "+card:shot-feedback", "+card:sunk-announce", "+card:salvo-shots", "+card:hunt-target-ai", "+card:probability-density-ai", "+card:no-touch-placement", "+card:dual-board-view"]
author: opus
date: 2026-11-02
---

# Battleship — сховай флот, стріляй по клітинах і топи кораблі суперника за відповідями «мимо/влучив/потопив»

## Суть
Двоє гравців таємно розставляють кораблі різної довжини на своїх сітках 10×10 і по черзі називають клітину-постріл; суперник чесно відповідає «мимо», «влучив» або «потопив». Перемагає той, хто першим потопить увесь флот. Ядро — дедукція за бінарним відгуком із відомими формами кораблів: після влучання шукаєш продовження, а промахи звужують, де ще може ховатися корабель. Паперова соло-гілка (пазл Bimaru) робить те саме без суперника: позиції флоту виводяться з лічильників рядів/стовпців і правила «кораблі не торкаються».

## Поле і час
- Кожен гравець має **дві сітки** 10×10 (A–J × 1–10): «свою» (флот + куди стріляв суперник) і «прицільну» (власні постріли й результати). У цифровій версії обидві на екрані поруч або перемикаються.
- Шари клітини на своїй сітці: корабель/вода + слід пострілу (пусто / промах / влучання); на прицільній — лише слід пострілу (невідомо / промах / влучання / потоплено).
- Покроково: хід = один постріл (у Salvo — кілька). Дві фази: **розстановка** (одночасна, прихована) → **обстріл** (почергово).
- Пазл: одна сітка 10×10 + числа за краями (скільки клітин ряду/стовпця зайнято кораблями) + кілька відкритих клітин-підказок; часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Авіаносець (Carrier) | piece | 5 клітин | лежить прямо (гор./верт.), не рухається |
| Лінкор (Battleship) | piece | 4 | те саме |
| Крейсер (Cruiser; з 2002 — Destroyer) | piece | 3 | те саме |
| Підводний човен (Submarine) | piece | 3 | те саме |
| Есмінець / патрульний катер | piece | 2 | те саме (1990: Destroyer 2; 2002: Patrol Boat 2) |
| Вода | static | — | порожня клітина своєї сітки |
| Промах (біла фішка) | mark | — | клітина обстріляна, корабля нема |
| Влучання (червона фішка) | mark | корабель | клітина корабля обстріляна |
| Потоплений корабель | mark | форма | усі клітини корабля влучені; у цифровій версії показується силует |
| Пазл: флот Bimaru | piece | 1×4, 2×3, 3×2, 4×1 | 10 кораблів, не торкаються навіть по діагоналі |
| Пазл: лічильник ряду/стовпця | mark | число | скільки клітин лінії зайнято кораблями |
| Пазл: клітина-підказка | mark | вода / підводний човен / кінець / середина | відкрита наперед; кінець показує, куди продовжується корабель |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(place_ship)` → ЯКЩО `free(cells)` і корабель прямий у межах поля → ТО `custom: «поставити корабель на N клітин»`; інакше `block`. Перекриття й діагональ заборонені; дотик у класичних правилах Milton Bradley — не заборонений (?), у пазлі — заборонений.
- КОЛИ `custom: «обидва флоти розставлено»` → ТО `turn_start(first_player)`.
- КОЛИ `input(shoot, cell)` → ЯКЩО `turn_of(side)` і клітина ще не обстріляна → ТО постріл; повторний постріл у ту саму клітину — `block` (цифрова версія; на папері — просто втрачений хід).
- КОЛИ постріл → ЯКЩО `occupied(cell, ship)` → ТО `mark(cell, hit)`, `custom: «оголосити: влучив (у настолці — назвати корабель)»`; інакше `mark(cell, miss)`.
- КОЛИ влучання → ЯКЩО `custom: «усі клітини корабля влучені»` → ТО `custom: «оголосити: потопив <корабель>»`, на прицільній сітці — силует.
- КОЛИ постріл завершено → ТО `pass_turn` (у деяких цифрових версіях влучання дає `extra_move` (?)).
- КОЛИ `all_gone(enemy_ships)` → ТО `win`.
- Salvo (1931 і варіант MB): КОЛИ `turn_start(side)` → ТО кількість пострілів = кількість живих кораблів стрільця (1931: старт із 5, менше з кожною втратою); суперник відповідає про результати всієї серії разом.
- AI hunt/target (цифрова версія): КОЛИ нема незавершених влучань → `custom: «hunt: стріляти випадково (з парністю — лише клітини однієї «шахової» кольоровості)»`; КОЛИ є влучання → `custom: «target: стріляти в 4 сусідів влучання, потім уздовж лінії»`.
- AI щільності: КОЛИ хід AI → ТО `custom: «для кожної клітини порахувати, скільки розміщень живих кораблів її покривають з урахуванням промахів/влучань; стріляти в максимум»`.
- Пазл: КОЛИ `input(mark, cell)` → ТО `mark(cell, ship|water)`; КОЛИ `custom: «сума корабельних клітин ряду ≠ число»` або `custom: «два кораблі торкаються»` → ТО `constraint_broken`; КОЛИ `all_constraints_met` і флот збігається зі складом → ТО `win`.
- Перемога: потопити весь флот першим (пазл — знайти розміщення всього флоту) · Поразка: твій флот потоплено · Рахунок: зазвичай нема; у цифрових — кількість пострілів/влучність.

## Керування і ввід
- Розстановка: перетягнути корабель на сітку (`drag-drop-piece`), кнопка/правий клік — повернути гор./верт.; кнопка «Випадково» розставляє флот сама.
- Обстріл: клік по клітині прицільної сітки (або назвати координату «B7» на папері/голосом); у Salvo — вибрати N клітин, потім «Вогонь».
- Hotseat на одному пристрої: між ходами екран-завіса «передай пристрій», щоб не підглядати.
- Пазл: клік циклічно ставить «корабель / вода / порожньо»; часто є режим малювання лінією.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати з AI → `difficulty-select`; Удвох (hotseat/online); Пазли → `puzzle-select`; Налаштування → `settings-window`; Правила → `help-window`.
- `placement-screen` (кандидат): своя сітка + «док» з кораблями, кнопки «Повернути», «Випадково», «Готово».
- `game-screen`: `own-board` (свій флот, сліди пострілів суперника) + `target-board` (свої постріли) + `fleet-status` (які кораблі суперника ще живі) + `turn-indicator` + `message-log` («B7 — мимо», «потоплено есмінець»); у Salvo — `remaining-counter` пострілів цього ходу.
- `pass-device` (кандидат, hotseat): завіса між ходами.
- `end-screen`: переможець, кількість пострілів, точність, кнопка «Ще раз»; часто показ флоту суперника повністю.
- Пазл (цифрова версія): `game-screen` з `line-clue` за краями, `conflict-highlight` переповнених рядів, `check-button`, `undo-button`.
- Переходи: main-menu → placement-screen → game-screen ↔ pass-device → end-screen → main-menu.

## Фічі поза полем
- `ai-opponent-levels`: random → hunt/target → hunt/target з парністю → щільність імовірностей (за DataGenetics медіани: 96 / ~65 / 64 / 42 пострілів).
- `custom-rules`: склад флоту за виданням (1990 vs 2002), Salvo, «влучив — стріляєш ще», дозвіл дотику кораблів; `custom-difficulty` — розмір сітки (Clubhouse Games DS «Grid Attack» — 7×7).
- `hotseat` з завісою, `online-multiplayer`, `stats` (перемоги, середня кількість пострілів).
- Пазл: `puzzle-bank`, `daily-puzzle`, `undo`, `auto-check`.
- Electronic Battleship (1977): компʼютер в коробці приймає координати з клавіатури й озвучує «hit/miss» — приклад того, що «рушій правил» відділений від поля.

## Варіації й родичі
- Історія: Basilinda (1890, паралель), паперовий Salvo (Starex, 1931, бланки), пластиковий Milton Bradley (1967), Electronic Battleship (1977), Z80 Compucolor (1979, одна з перших компʼютерних ігор).
- Склади флоту: MB 1990 — 5/4/3/3/2 (17 клітин); Hasbro 2002 — Cruiser → Destroyer 3 + Patrol Boat 2; радянський «Морський бій» — 1×4, 2×3, 3×2, 4×1 і заборона дотику (той самий флот, що в пазлі).
- Пазл Battleship / Bimaru / Yubotu: Batalla Naval (Аргентина, 1982, Jaime Poniachik), World Puzzle Championship 1992, Games 1993; варіанти — гекс, 3D, діагональні кораблі, частина чисел прихована, «стріляєш трьома і отримуєш відсортовані розміри влучених».
- **Осі варіацій**: відгук «влучив / потопив / назвав корабель / лише мимо-влучив»; постріли на хід «1 / за живими кораблями / додатковий за влучання»; дотик кораблів «можна / не можна»; поле «спільне невидиме / дві сітки / пазл з лічильниками».
- Родичі: Mastermind (дедукція за відгуком), Minesweeper (приховане поле, але без суперника), Stratego (приховані фігури, але вони рухаються).

## Цікавинки для курсу
- Розстановка флоту з валідацією (прямо, в межах, без перекриття, опційно без дотику) + кнопка «Випадково» — 📎 (генерація з перевіркою через повторні спроби).
- Дві сітки одного гравця: власна (з кораблями) і прицільна (лише відгуки) — 🥉: перший досвід «двох поглядів на один стан» і приховування інформації в рендері.
- AI hunt/target з парністю — 🥉 (стан «полюю / добиваю» + черга сусідів).
- AI щільності імовірностей — 🥇 (перебір усіх розміщень живих кораблів з урахуванням промахів/влучань; добре видно на теплокарті).
- Salvo: постріли = живі кораблі, відгук пакетом — 📎.
- Пазл Bimaru: лічильники рядів + «не торкатися навіть діагонально» + генератор з унікальним розвʼязком — 🥈 (розвʼязувач) / 👑 (генератор, NP-повна задача).

## Мапа на каталог
- Є: `cell-click` (постріл) · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-random` / `ai-greedy` (hunt/target — жадібний) · `destroy-all-enemies` (потопити флот) · `multi-cell-size` (кораблі 2–5 клітин) · `drag-drop-piece` (розстановка) · `difficulty-levels` + `field-size-picker` · `satisfy-constraints` + `completion-detection` + `unique-puzzle-generation` + `level-solver` (пазл) · `game-screen` / `end-screen` / `main-menu` / `settings-window` / `help-window` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+fleet-placement` «Розстановка флоту» · entities/legality · 📎 · слоти {fleet: list, touch: allow|deny} — ручна і випадкова.
  - `+shot-feedback` «Постріл з відгуком» · game-logic/opponent · 🌱 · слот {feedback: hit-miss|name-ship} — клітина → мимо/влучив.
  - `+sunk-announce` «Повідомлення про потоплення» · interface/hud · 🌱 — коли всі клітини обʼєкта влучені.
  - `+salvo-shots` «Серія пострілів за живими кораблями» · game-logic/opponent · 📎.
  - `+hunt-target-ai` «AI полювання/добивання» · game-logic/opponent · 🥉 · слот {parity: bool} (дитина `ai-opponent`).
  - `+probability-density-ai` «AI за щільністю імовірностей» · game-logic/opponent · 🥇 (дитина `ai-opponent`).
  - `+line-sum-clue` «Підказка-лічильник лінії» (є як `+` у Hexcells, Voltorb Flip) — пазл Bimaru.
  - `+no-touch-placement` «Обʼєкти не торкаються (вкл. діагональ)» · game-logic/constraints · 📎.
  - `+dual-board-view` «Свій і прицільний вигляд» · interface/render · 🥉 — дві проєкції стану з різним приховуванням.

## Пропозиції до словників
- `+trigger:placement_done` — завершено фазу розстановки (обидві сторони «Готово»); фазові ігри (Stratego теж).
- `+cond:all_cells_hit` — усі клітини багатоклітинного обʼєкта влучені (потоплення); `hp_zero` близько, але HP тут — набір клітин, а не число.
- `+effect:mark` / `+effect:reveal` — уже ⏳ у словнику; тут вживаються як основні.
- `+effect:announce` — оголосити результат супернику (у мережевій/hotseat-грі: не те саме, що `message`, бо адресат — інша сторона).
- `+role:piece` (кораблі), `+role:mark` (фішки промаху/влучання, лічильники пазла).
- `+ui:own-board` · `+ui:target-board` — дві сітки одного гравця; `+ui:fleet-status` — список кораблів суперника з позначкою «потоплено»; `+ui:line-clue` (див. Hexcells).
- `+window:placement-screen` — фаза розстановки фігур/кораблів перед грою; `+window:pass-device` — завіса hotseat між ходами з прихованою інформацією.
- `+feature:salvo-mode` — режим кількох пострілів за хід.

## Джерела
- ⭐ [Wikipedia: Battleship (game)](https://en.wikipedia.org/wiki/Battleship_(game)) — правила, склади флоту 1990/2002, Salvo, історія, Electronic Battleship, Grid Attack 7×7.
- [Wikipedia: Battleship (puzzle)](https://en.wikipedia.org/wiki/Battleship_(puzzle)) — флот 1×4/2×3/3×2/4×1, заборона дотику по діагоналі, лічильники, підказки, Poniachik 1982, NP-повнота (Sevenster 2004).
- [DataGenetics: Battleship](https://www.datagenetics.com/blog/december32011/) — порівняння стратегій AI з медіанами пострілів.
- [BGG пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=battleship) — видання й варіанти.
- YouTube: пошук «battleship board game how to play», «battleship puzzle bimaru solving».

## Непевне
- (?) Чи дозволяють офіційні правила Milton Bradley кораблям торкатися — Wikipedia мовчить; у радянській/східноєвропейській традиції дотик заборонений.
- (?) «Влучив — стріляєш ще» — поширене домашнє/цифрове правило, офіційним не перевірено.
- (?) Медіана hunt/target ~65 — у DataGenetics лише графік, число оцінене з нього; точні 96 / 64 / 42 — з тексту.
- (?) Склад флоту Salvo 1931 — відомо лише «старт із 5 пострілів».
