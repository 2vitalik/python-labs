---
title: "SokoGhost: Unfinished Business"
slug: sokoghost-unfinished-business
aka: [SokoGhost]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows, Linux), web (демо на itch)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4254020/SokoGhost_Unfinished_Business/", best: true, note: "опис: прохід крізь стіни, ящики й ворота, 100 рівнів, зірки за оптимальні haunt-ходи, undo / redo, нелінійний вибір сегментів; 7 знімків і геймплейний трейлер"}
  - {kind: itch, url: "https://dream-jam-games.itch.io/sokoghost-unfinished-business", note: "демо в браузері (Unity, v0.1.5): навчальні рівні haunt-механік, коментар розробника про пояснення ghost-механіки й рахунку"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=RwIQL4AuJ-g", note: "Gameplay Trailer (Dream Jam Games): «Pass through obstacles! But don't get stuck in a wall!»"}
  - {kind: other, url: "https://www.gamespark.jp/article/2026/02/03/162321.html", note: "Game*Spark (JA), 03.02.2026: Kickstarter, Sokoban, де привид проходить крізь стіни й ящики"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, all-on-targets, impassable-cells, beam-tracing, button-toggle, one-way-cell, carrier-platform, move-counter, undo-redo, redo, restart-level, level-select, level-unlock, movement-animation, +haunt-pass-through, +possess-unit, +push-chain, +laser-blocking, +pressure-plate, +wire-power, +exit-unlocks-on-goal, +stars-rating, +branching-campaign]
proposes: ["+trigger:pass_through", "+effect:possess", "+cond:powered", "+ui:haunt-meter", "+card:haunt-pass-through"]
author: opus
date: 2026-11-19
---

# SokoGhost: Unfinished Business — Sokoban за привида: Грег проходить крізь стіни, ящики й ворота, але кожен такий прохід коштує haunt-очко, а від залишку залежать зірки

## Суть
Грег загинув на фабриці коробок і далі виконує норму: штовхає жовті ящики-поставки на цілі, після чого відмикається ліфт на наступний поверх Box Corp. На відміну від Sokoban, привид може пройти крізь стіну, ящик чи ворота — це «haunt», і на рівень їх дано небагато; що більше лишилось, то більше зірок. Згодом Грег учиться вселятися в ящик («Move into a box to haunt it»), а такий ящик теж проходить крізь стіни; сегменти будівлі додають плити й ворота, лазери з дротами, конвеєри, ланцюги й односторонні стіни.

## Поле і час
- Квадратна сітка; у даних рівня — розміри (у демо-збірці 9×10 … 12×9), клітини «підлога / стіна», окремий список сутностей і шар дротів.
- Хід = крок привида (Steam: «Playable without Timed Input»); конвеєри, мабуть, зсувають вантаж раз на хід (`ConveyorTickManager`) (?).
- 100 рівнів у 10 сегментах будівлі (досягнення «Complete Segment 1…10»); після вступу сегменти можна проходити в будь-якому порядку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Грег (привид) | player | haunt-очки рівня | крок у 4 напрямки; штовхає ящики; за haunt-очко заходить у стіну, ящик чи ворота й проходить крізь них |
| Ящик-поставка (жовтий) | object | доставлено / ні | штовхається; на цілі — зелена галочка |
| Ящик (помаранчевий, з хрестом) | object | — | звичайна перешкода, крізь яку привид проходить за haunt; штовхається (?) |
| Ціль доставки | zone | — | жовто-чорна рамка; місце для ящика-поставки |
| Ліфт (End Level Elevator) | gate | закрито / відімкнено | відмикається, коли всі поставки на цілях; зайти — кінець рівня |
| Стіна | static | — | непрохідна для ящиків; привид — за haunt |
| Двері з живленням (Door Powered) | gate | відчинено / зачинено; дріт | перемикаються живленням з дроту (?) |
| Лазер-випромінювач | static | напрям | промінь по прямій до першої перешкоди |
| Лазер-приймач | switch | — | промінь влучив — дріт під живленням |
| Дріт | static | — | веде живлення від приймача чи плити до дверей |
| Натискна плита | switch | — | вантаж на плиті відчиняє ворота (сегмент «Plates and Gates») (?) |
| Конвеєр | terrain | напрям | везе ящик, що на ньому (?) |
| Ланцюги (Chainbound: стіна, ящик, поставка, двері) | static | — | обмотане ланцюгом — привид крізь нього не проходить і в нього не вселяється (?) |
| Одностороння стіна | static | напрям | прохід лише в один бік (?) |
| Вселений ящик (haunted box) | object | привид усередині | рухається з привидом; проходить крізь стіни («Haunted boxes can be pushed through walls») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(ghost, dir)`, `counter(moves, +1)`.
- КОЛИ `contact(ghost, box)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(ghost, dir)` — ряд ящиків штовхається ланцюгом (`TryBuildBoxPushChain`) (?).
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall|closed_gate|box)` → ТО `custom: «заходить усередину твердого, −1 haunt-очко»` (?).
- КОЛИ `input(dir)` → ЯКЩО `counter(haunts, ==, 0)` → ТО `block` — без очок у тверде не зайти, а хто вже в стіні — застряг («But don't get stuck in a wall!»): лише undo чи рестарт.
- КОЛИ `input(dir)` → ЯКЩО `state(next_cell, chainbound)` → ТО `block` (?).
- КОЛИ `contact(ghost, box)` → ЯКЩО `custom: «здібність haunt box відкрито (після 6-го рівня)»` → ТО `attach(ghost, box)`, `set_state(box, haunted)` — «Move into a box to haunt it».
- КОЛИ `input(dir)` → ЯКЩО `state(box, haunted)` → ТО `custom: «вселений ящик рухається разом із привидом і проходить крізь стіни»`; вихід із ящика — окремий хід (`BoxLeaveCommand`).
- КОЛИ `line_of_sight(laser_emitter, laser_receiver)` → ТО `set_state(powered_door, switched)` — живлення йде дротом; ящик на промені обриває його (?).
- КОЛИ `enter(box, pressure_plate)` → ТО `set_state(gate, open)` (?).
- КОЛИ `turn_end` → ЯКЩО `occupied(conveyor, box)` → ТО `move(box, belt_dir)` (?).
- КОЛИ `all_on(delivery_box, delivery_spot)` → ТО `unlock(elevator)`.
- КОЛИ `enter(ghost, elevator)` → ЯКЩО `custom: «ліфт відімкнено»` → ТО `win`, `custom: «1–3 зірки за залишком haunt-очок»`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(redo)` → ТО `custom: «повторити скасований хід»`.
- КОЛИ `input(reset_hold)` → ТО `restart`.
- Перемога: усі поставки на цілях і привид у ліфті. · Поразка: формально нема — застряг у стіні без очок чи загнав ящик у кут → undo / рестарт. · Рахунок: 3 / 2 / 1 зірка за порогами залишку haunt-очок (у даних рівня: `hauntCount`, `hauntCount3Stars`, `hauntCount2Stars`, `hauntCount1Stars`); окремо — найкраща кількість ходів.

## Керування і ввід
- Клавіатура або геймпад (Steam: Full controller support, Keyboard Only Option): рух; Z / B — undo, X — redo, R / Y (утримати) — рестарт; з v0.1.5 утримання повторює рух, undo й redo.
- Діалог: «Press space to continue (Hold to skip all)» / A на геймпаді.
- Лічильник ходів можна сховати (`OnMoveCounterToggled`).

## Вікна, меню, HUD
- `main-menu` — сцена хмарочоса Box Corp із ліфтом і стрічкою ящиків.
- `chapter-select` + `level-select` — сегмент (напр. «PLATES AND GATES»), список рівнів зі смужками зірок і «LOCKED»; праворуч — мінікарта рівня, значки «MAP FEATURES» (які механіки в рівні), «BEST MOVES»; угорі — зірки «75 / 300».
- `game-screen` — кімната; угорі праворуч «LEVEL 005»; ліворуч — підказки кнопок Undo / Redo / Reset; унизу — `+ui:haunt-meter`: сегменти haunt-очок із позначками ★ / ★★ / ★★★ на порогах; праворуч унизу — `move-counter`.
- `dialogue-window` — «Management» (червоний телефон): «WELCOME ROOKIE!…», «…EVEN GHOSTS ARE ALLOWED A BREAK…».
- `tutorial-window` — підказки нових механік у перших рівнях сегмента.
- `end-screen` — нагородження зірками після ліфта.
- Переходи: меню → вибір сегмента → вибір рівня → діалог → рівень → (ліфт) зірки → наступний рівень.

## Фічі поза полем
- `undo` без ліміту (?) + `redo` + `restart-level` утриманням.
- `stars-rating`: зірки за залишком haunt-очок — «Dynamic difficulty»: можна гнатись за трьома, можна просто проходити.
- `level-unlock`; `+branching-campaign` — після вступу будь-який сегмент; застряг — іди в іншу гілку.
- `achievements` (24, серед них «Complete Segment 1…10»), `gamepad-support`, `volume-sliders`; лише англійська.
- Демо: 20–22 рівні, три механіки; Kickstarter (лютий 2026, ціль €500), Steam Next Fest.

## Варіації й родичі
- [Sokoban](sokoban.md) — те саме ядро без проходу крізь тверде.
- [Dig Dug](../dig-gravity/dig-dug.md) — вороги-привиди проходять крізь землю (`+ghost-phase`); тут прохід — у гравця і з лімітом.
- [Helltaker](helltaker.md) — бюджет ходів як ресурс пазла; тут бюджет лише на «нечесні» ходи.
- [Conveyor Con-fusion](conveyor-confusion.md), [Magnet Block](magnet-block.md) — конвеєри й плити в Sokoban.
- Осі варіацій:
  - **хто проходить крізь стіни**: ніхто (Sokoban) / ворог (Dig Dug) / гравець за ресурс (тут) / ящик, у який вселились (тут);
  - **ціна проходу**: безкоштовно / ліміт на рівень (тут) / лише в певному стані;
  - **рахунок**: нема / ходи / залишок «нечесних» ходів (тут).

## Цікавинки для курсу
- Прохід крізь тверде за очки: рух у стіну дозволено, поки є haunt; стан «в стіні» + заборона застрягти — 📎.
- Зірки за залишком ресурсу з порогами в даних рівня (`hauntCount3Stars`…) — 🌱.
- Вселитися в ящик: аватар і ящик зчеплені, правила руху ящика змінюються — 🥉.
- Лазер-випромінювач → приймач → дріт → двері; ящик обриває промінь — 🥉 (трасування променя + граф живлення).
- Рівень як JSON (розміри, клітини, сутності, дроти, haunt-пороги) і читання його грою — 🥉 (картка `level-from-txt`, але JSON).
- BFS-розвʼязувач, що мінімізує витрачені haunt-очки — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `all-on-targets` ↔ поставки на цілях; `impassable-cells` ↔ стіни для ящиків, ланцюги; `beam-tracing` ↔ лазер; `button-toggle` ↔ плита → ворота; `one-way-cell` ↔ одностороння стіна; `carrier-platform` ↔ конвеєр; `move-counter`; `undo-redo` + `redo`; `restart-level`; `level-select` + `level-unlock`; `movement-animation`.
- **Нема** → пропозиції карток:
  - `+haunt-pass-through` «Прохід крізь стіни за ліміт очок» · entities/legality · 📎 · слот {budget: int, stuck: block}.
  - `+possess-unit` (є в корпусі) — тут вселитися в ящик.
  - `+push-chain`, `+laser-blocking`, `+pressure-plate`, `+wire-power`, `+exit-unlocks-on-goal`, `+stars-rating`, `+branching-campaign` (є в корпусі).

## Пропозиції до словників
- `+trigger:pass_through` — сутність заходить у тверде (стіна, ящик, ворота) і проходить крізь нього; тут — `custom`.
- `+effect:possess` — аватар вселяється в обʼєкт і рухає його собою.
- `+cond:powered` — двері / ворота під живленням від дроту (лазер-приймач, плита).
- `+ui:haunt-meter` — смуга ресурсу з позначками порогів зірок прямо на ній.
- `+card:haunt-pass-through` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/4254020/SokoGhost_Unfinished_Business/) — опис (прохід крізь стіни, ящики й ворота; 100 рівнів; «Dynamic difficulty… optimal haunt moves»; undo / redo; нелінійний вибір), 24 досягнення, новини (демо, v0.1.4 — «покращено haunt-механіку», v0.1.5 — «haunt box» після рівня 6, утримання для руху / undo / redo, туторіали), 7 знімків.
- [itch.io: демо](https://dream-jam-games.itch.io/sokoghost-unfinished-business) — Unity WebGL; з даних збірки — рядки туторіалів, назви сутностей і JSON рівнів із haunt-порогами.
- [Gameplay Trailer](https://www.youtube.com/watch?v=RwIQL4AuJ-g) — кадри: привид у стіні, ящик-поставка крізь стіну на ціль, ланцюги, лазер із дротом, плити й ворота, вибір рівнів.
- [Game*Spark](https://www.gamespark.jp/article/2026/02/03/162321.html) — анонс Kickstarter.

## Непевне
- (?) Точна ціна проходу: очко за кожну клітину в стіні чи за весь прохід (`TrySpendHauntOnce`, `enteredViaHaunt` у коді); чи пускає крок у ящик крізь нього, коли його не можна зсунути.
- (?) Що саме роблять ланцюги, односторонні стіни, конвеєри, плити й лазер, що влучив у привида (`OnLaserHitPlayer`) — бачив лише назви й кадри.
- (?) Чи штовхаються помаранчеві ящики і чи штовхається ряд ящиків (у коді є `TryBuildBoxPushChain`).
- (?) Рівні демо в збірці зашифровані — розміри взято з чотирьох тестових рівнів у ресурсах.
- (?) Рядок черги «кожен рівень — свій тип проходу»: за описом Steam кожен рівень вимагає кількох «pass-through»-механік одразу.
