---
title: Bloxorz
slug: bloxorz
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2007
platforms: [web (Flash), mobile, PS3 (Cuboid), iOS (Edge)]
links:
  - {kind: play, url: "https://www.coolmathgames.com/0-bloxorz", best: true, note: "інструкція: стоячий/лежачий блок, помаранчеві плитки, soft/heavy-перемикачі, split-телепорт, 6-значні коди, 33 рівні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cuboid_(video_game)", note: "Cuboid (PS3, 2009) — та сама механіка + ліміт ходів, порівняння з Bloxorz"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Edge_(video_game)", note: "Edge (Mobigame, 2008) — котячий куб у реальному часі, висіти на ребрі"}
  - {kind: fandom, url: "https://flashgaming.fandom.com/wiki/Bloxorz", note: "фан-вікі Flash-ігор (сторінка закрита для бота, не прочитано)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bloxorz+gameplay+all+levels", note: "пошук; проходження всіх 33 рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=bloxorz", note: "пошук; клони й наступники"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, multi-cell-size, orientation-state, environment-death, reach-exit, sequential-levels, level-from-txt, level-solver, reachability-check, movement-animation, event-effects, time-bonus, fixture-level-tests, +level-password, +button-toggle, +undo-redo, +move-limit, +multi-avatar-switch, +height-levels, +roll-block, +state-gated-switch, +fragile-under-state, +split-merge, +bridge-toggle]
proposes: ["+trigger:input", "+trigger:enter", "+cond:state", "+cond:supported", "+effect:roll", "+effect:fall", "+effect:restart", "+effect:set_state", "+effect:split", "+effect:attach", "+effect:set_cell", "+role:switch", "+role:gate", "+role:terrain", "+window:level-password", "+ui:level-code", "+ui:move-counter", "+feature:level-password", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Bloxorz — перекочуй брусок 1×1×2 у квадратну дірку, не впавши з плиток

## Суть
Гравець котить прямокутний брусок 1×1×2 по плитках, що висять у порожнечі: кожен хід — перекидання на 90°, і брусок по черзі **стоїть** (займає 1 клітину) або **лежить** (займає 2). Мета — поставити його вертикально над квадратною діркою. Уся головоломка — у геометрії перекочування: щоб опинитися стоячим у потрібній клітині, треба правильно «розфазувати» стани; додаткові плитки (крихкі, перемикачі мостів, телепорт-розщеплювач) ставлять вимоги до **стану**, а не лише до позиції. Flash-гра Damien Clarke, 2007, 33 рівні.

## Поле і час
- Квадратна сітка плиток над порожнечею (рендер — ізометричний 3D, але логіка — 2D-сітка + орієнтація бруска). Поле видно цілком.
- Стан бруска: позиція + орієнтація `standing` / `lying_x` / `lying_y`; після розщеплення — дві незалежні кубики 1×1×1.
- Шари: плитка (тип) + брусок; мости — плитки зі станом «є / нема».
- Хід = одне перекидання; світ без вводу не змінюється (`static`). Час іде як метрика (рекорд проходження всіх рівнів), правила від нього не залежать (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Брусок | player | орієнтація standing / lying_x / lying_y | перекочується на 90° у 4 напрямках; займає 1 або 2 клітини |
| Кубик (половинка) ×2 | player | 1×1×1, активний / ні | після розщеплення; рухається по 1 клітині (лише перекочування куба), Space перемикає активний |
| Сіра плитка | terrain | — | звичайна опора |
| Помаранчева (крихка) плитка | terrain | — | витримує лежачий брусок; під стоячим проламується → падіння |
| Soft-перемикач (восьмикутник) | switch | дія: toggle / on / off; цілі — мости | спрацьовує від будь-якої частини бруска чи кубика |
| Heavy-перемикач (X) | switch | дія: toggle / on / off; цілі | спрацьовує лише від бруска, що стоїть на ньому вертикально |
| Міст (плитки-міст) | gate | стан є / нема | при «нема» — порожнеча; спрацьовування перемикача підсвічує цілі зеленим/червоним |
| Split-телепорт `( )` | switch | дві цільові клітини | стоячий брусок → дві кубики у заданих клітинах |
| Дірка-вихід | static | — | стоячий брусок над нею — перемога; кубики не проходять |
| Порожнеча (за краєм) | hazard | — | будь-яка частина без опори → падіння, рестарт рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(block, standing)` → ТО `roll(block, dir)`: лягає на дві клітини в напрямку `dir` (`lying` уздовж осі `dir`).
- КОЛИ `input(dir)` → ЯКЩО `state(block, lying)` і вісь лежання ∥ `dir` → ТО `roll`: встає на клітину за дальнім кінцем (`standing`).
- КОЛИ `input(dir)` → ЯКЩО `state(block, lying)` і вісь ⊥ `dir` → ТО `roll`: перекочується боком, лишається лежачим, зсув на 1.
- Після кожного кроку: КОЛИ `custom: «будь-яка зайнята клітина без плитки (край, вимкнений міст)»` → ТО `fall(block)`, `restart`. Лежачий брусок над порожнечею однією половиною теж падає (?).
- КОЛИ `enter(block, orange_tile)` → ЯКЩО `state(block, standing)` → ТО `set_cell(void)`, `fall`, `restart`; лежачий — безпечно.
- КОЛИ `enter(block|cube, soft_switch)` → ТО `set_state(bridges[i], toggle|on|off)`.
- КОЛИ `enter(block, heavy_switch)` → ЯКЩО `state(block, standing)` → ТО `set_state(bridges[i], …)`; лежачий/кубик — нічого.
- Перемикачі бувають «toggle» (кожне натискання міняє) і «постійні» (лише створюють міст) — з довідки Coolmath; чи є «лише прибирає» (?).
- КОЛИ `enter(block, split_switch)` → ЯКЩО `state(block, standing)` (?) → ТО `split(block → cube_a@A, cube_b@B)`; керування — `cube_a`.
- КОЛИ `input(space)` → ЯКЩО `state(split)` → ТО `custom: «перемкнути активний кубик»`.
- КОЛИ `adjacent(cube_a, cube_b)` → ТО `attach(cube_a, cube_b) → block(lying)` — кубики, поставлені поруч, зʼєднуються назад у лежачий брусок.
- КОЛИ `enter(cube, heavy_switch)` → ТО нічого (кубик «легкий»); КОЛИ `contact(cube, exit)` → ТО нічого (не провалюється).
- КОЛИ `enter(block, exit)` → ЯКЩО `state(block, standing)` → ТО `win`, `next_level` (брусок провалюється в дірку); лежачий — проходить над діркою (?).
- Перемога: стоячий брусок у дірці. · Поразка: падіння за край / крізь крихку плитку → рестарт рівня (життів нема). · Рахунок: лічильник ходів і/або часу (?); Cuboid — ліміт ходів на деяких рівнях.

## Керування і ввід
- Стрілки (або WASD) — перекидання в напрямку; Space — перемкнути активний кубик після розщеплення.
- Миші, undo, drag — нема (рестарт лише через падіння або меню) (?).
- Ввід коду рівня — 6 цифр у меню «Load Stage».

## Вікна, меню, HUD
- `splash-screen` — титул / Miniclip-заставка (?).
- `main-menu`: New Game · Load Stage → `level-password` · Instructions → `help-window` (?).
- `level-password`: поле вводу 6-значного коду рівня (код показується у правому верхньому куті під час гри).
- `game-screen`: ізометричне поле; HUD — `level-number` («Stage NN»), `level-code`, `move-counter`, `timer-elapsed` (?), кнопки звуку/музики (?).
- `end-screen`: анімація провалювання в дірку → наступний рівень; фінал після 33-го (?).
- Переходи: main-menu → (New Game) game-screen рівня 1 → (дірка) game-screen наступного; (падіння) → той самий рівень; main-menu → Load Stage → level-password → game-screen рівня.

## Фічі поза полем
- `level-password` — прогресія 6-значними кодами (без збереження стану).
- `levels-sequential` 33 рівні; `restart-level` автоматичний після падіння.
- `sound-toggle`, `music-toggle` (?).
- Undo, підказок, редактора в оригіналі нема; спільнота має текстові формати рівнів і BFS-солвери (класичне студентське завдання) (?).
- Cuboid (PS3/iOS): пауерапи «розщепити блок» і «+кілька ходів» на рівнях з лімітом ходів, дерев'яні платформи, телепорти.

## Варіації й родичі
- **Cuboid** (Creat Studios, PS3 2009, iOS 2012): брусок удвічі вищий за ширину; стоячи «ходить на дві клітини», лежачи — на одну; крихкі платформи, перемикачі (частина — лише стоячи), телепорти, ліміт ходів; критики прямо порівнюють із Bloxorz.
- **Edge** (Mobigame, 2008): куб котиться в реальному часі по ізометричних платформах, може «висіти» на ребрі над прірвою; призми, ранг за час/призми/падіння; 48 + 17 бонусних рівнів, режим Turbo.
- [Stephen's Sausage Roll](../thinky/stephens-sausage-roll.md) — перекочування 1×2 сосисок з орієнтацією граней (смажених/сирих).
- Осі варіацій перекочування:
  - **розмір**: 1×1×1 (куб, Edge) · 1×1×2 (Bloxorz) · 1×2 зі сторонами (Sausage Roll) · довільний полікуб (?);
  - **що важливо в орієнтації**: лише зайняті клітини (Bloxorz) · яка грань знизу (кубик-кістка, Sausage Roll) · вага/тиск (heavy-перемикач);
  - **розщеплення**: нема / на дві половини з перемиканням (Bloxorz split) / з'єднання при дотику;
  - **час**: покроково (Bloxorz, Cuboid) / реальний (Edge).

## Цікавинки для курсу
- Перекочування бруска: таблиця переходів (орієнтація × напрям → нові клітини й орієнтація) — 📎 (6 випадків, але треба їх вивести).
- Перевірка опори «кожна зайнята клітина — плитка» + крихка плитка, що залежить від стану — 🌱.
- Перемикачі мостів (soft / heavy, toggle / on) як `switch→targets` з умовою на стан — 🥉.
- Розщеплення на два кубики, перемикання активного, злиття при сусідстві — 🥈 (два аватари, нормалізація при злитті).
- BFS-розвʼязувач: стан = (x, y, орієнтація, маска мостів, позиції кубиків) — 🥈; оптимальний за ходами з візуалізацією шляху — 🥈.
- Рівень із txt (символи для плиток, перемикачів, цілей перемикачів у метаданих) — 🥉; коди рівнів — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `multi-cell-size` ↔ брусок 1×2; `orientation-state` ↔ стоїть/лежить; `environment-death` ↔ падіння з краю / крізь крихку плитку; `reach-exit` ↔ дірка; `sequential-levels` ↔ 33 рівні; `level-from-txt` + `level-solver` + `reachability-check` ↔ BFS по станах; `movement-animation` + `event-effects` ↔ перекидання, провалювання; `fixture-level-tests` ↔ рівні-фікстури для таблиці переходів.
- **Нема** → пропозиції карток:
  - `+roll-block` «Перекочування бруска» · entities/move · 🥉 · слот {size: 1x1x1|1x1x2} — таблиця переходів орієнтації (дитина `orientation-state`).
  - `+state-gated-switch` «Перемикач, що вимагає стану» · entities/interact · 📎 · слот {needs: any|standing|heavy} — heavy-X.
  - `+fragile-under-state` «Плитка ламається під станом» · entities/interact · 📎 — помаранчева під стоячим (родич `+crumble-floor`, але тригер — вага, а не крок).
  - `+split-merge` «Розщеплення аватара й злиття при дотику» · entities/state · 🥈 — два кубики, Space, злиття.
  - `+bridge-toggle` «Міст, що зʼявляється/зникає за перемикачем» · entities/interact · 📎 · слот {mode: toggle|on|off}.
  - Повтор корпусу: `+level-password` (6 цифр), `+button-toggle`, `+multi-avatar-switch` (кубики), `+move-limit` (Cuboid), `+height-levels` (Edge), `+undo-redo` (для студентської версії).

## Пропозиції до словників
- `+trigger:input`, `+trigger:enter` — брусок став на плитку типу.
- `+cond:state` — standing / lying; `+cond:supported` — усі зайняті клітини мають плитку (є й у Sausage Roll).
- `+effect:roll` — перекидання з зміною орієнтації (є в Sausage Roll); `+effect:fall`; `+effect:restart`; `+effect:set_state` (мости); `+effect:split` / `+effect:attach` — розщеплення й злиття; `+effect:set_cell` (крихка → порожнеча).
- `+role:switch`, `+role:gate` (міст), `+role:terrain` (крихка плитка).
- `+window:level-password`, `+ui:level-code` — код поточного рівня в куті HUD; `+ui:move-counter`.
- `+feature:level-password`.
- `+axis:actors` — `single`, що тимчасово стає `party` з двох кубиків.

## Джерела
- ⭐ [Coolmath Games: Bloxorz](https://www.coolmathgames.com/0-bloxorz) — повна інструкція: стрілки/WASD, Space, крихкі плитки, soft/heavy, toggle/постійні мости, split `( )`, кубики не тиснуть heavy і не проходять дірку, 6-значні коди «Load Stage», 33 рівні, автор Damien Clarke.
- [Wikipedia: Cuboid](https://en.wikipedia.org/wiki/Cuboid_(video_game)) — механіка PS3-аналога, пауерапи, ліміт ходів, порівняння GameSpot з Bloxorz.
- [Wikipedia: Edge](https://en.wikipedia.org/wiki/Edge_(video_game)) — real-time куб, висіння на ребрі, ранги, Turbo.
- [Flash Gaming Wiki](https://flashgaming.fandom.com/wiki/Bloxorz) — фан-вікі (не прочитано: доступ закрито).
- YouTube: пошук «Bloxorz gameplay all levels».

## Непевне
- (?) Склад HUD (лічильник ходів, таймер) і головного меню, крім «Load Stage», — не перевірено (гра Flash, сторінка Miniclip не відкрилась, пошук вичерпано).
- (?) Чи є перемикачі «лише прибрати міст» і чи split спрацьовує лише від стоячого бруска.
- (?) Чи лежачий брусок над діркою провалюється (за памʼяттю — ні, проходить як по підлозі).
- (?) Студія DX Interactive і видавець Miniclip — з памʼяті; Coolmath називає лише Damien Clarke.
