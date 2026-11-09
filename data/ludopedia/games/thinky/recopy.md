---
title: "RE:COPY"
slug: recopy
aka: [RECOPY, "RE:COPY Demo"]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5230820/RECOPY/", best: true, note: "опис механіки: сканер → принтер за кнопкою, копії робота ходять разом, копіювання самих пристроїв; 100+ рівнів"}
  - {kind: play, url: "https://masasgames.itch.io/recopy-demo", note: "безкоштовне демо в браузері (Unity WebGL); 7 скриншотів із HUD"}
  - {kind: itch, url: "https://masasgames.itch.io/", note: "сторінка розробника masasgames"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=RE%3ACOPY+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, pipe-connectors, connectivity-check, undo-step, restart-level, sequential-levels, level-select, game-screen, pause-menu, achievements-window, save-progress, +copy-region, +copy-merge, +self-copy, +device-copy, +target-pattern-panel, +multi-agent-sync, +print-preview-ghost]
proposes: ["+effect:copy_region", "+trigger:print", "+role:scanner", "+role:printer", "+ui:target-panel", "+ui:print-preview", "+card:copy-region", "+card:copy-merge", "+card:self-copy", "+card:device-copy"]
author: opus
date: 2026-11-09
---

# RE:COPY — Sokoban з ксероксом: кнопка копіює все з пунктирної рамки в суцільну, разом із роботом і самими копіювальними пристроями

## Суть
Робот штовхає ящики-зʼєднувачі на квадратній сітці, але головна дія — **копіювання ділянки поля**: стати на кнопку, і вміст пунктирної рамки сканера друкується в суцільну рамку принтера того самого кольору. Мета рівня — скласти з зеленими «трубками» ящиків і стін фігуру, показану на панелі TARGET. Далі копіюється сам робот (усі копії ходять одним вводом), кілька сканерів зливають копії в один принтер, а згодом копіюються й самі сканери та принтери — копії запускають нові копії. Ядро — операція «прямокутник/фігура A → B» як хід гри, а не як інструмент редактора.

## Поле і час
- Квадратна сітка, один екран на рівень (на скриншотах від 5×7 до 11×11); темні плитки — стіни, світлі — підлога.
- Шари клітини: підлога / рамка сканера (пунктир) / рамка принтера (суцільна) / обʼєкт (робот, ящик, кнопка, пристрій). Рамки бувають багатоклітинні й фігурні (хрест), кольорові: червоний, жовтий, блакитний — канал звʼязку кнопка → сканер → принтер.
- Покроково: тік = крок; часу нема («no time limits»).
- Сектори з назвами-темами: 01 FIRST COPY · 03 SELF COPY · 04 CHAIN COPY · 05 MERGE · 06 DEVICE COPY; рівні нумеровані, є додаткові `EX01`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | — | крок 4 напрямки; штовхає ящики; натискає кнопки |
| Копія робота | player | — | зʼявляється друком; ходить тим самим вводом, що й усі роботи |
| Ящик-зʼєднувач | object | 0–4 зелені «трубки» по сторонах | штовхається; трубки сусідніх клітин, що торкаються, утворюють фігуру |
| Стіна | static | може мати трубку (?) | непрохідна; бере участь у візерунку («patterns on boxes and walls») |
| Сканер | spawner | колір каналу, напрямок стрілки | позначає пунктирну ділянку, вміст якої копіюється |
| Ділянка сканування | zone | пунктирна рамка, форма, колір | «FROM»: що лежить усередині — те й друкується |
| Принтер | spawner | колір каналу, напрямок стрілки | позначає суцільну ділянку друку |
| Ділянка друку | zone | суцільна рамка, форма, колір | «TO»: показує напівпрозору примару того, що буде надруковано |
| Кнопка | switch | колір каналу | робот став → копіювання свого каналу |
| Панель TARGET | mark | фігура з трубок | ціль рівня поза полем |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(robot, dir)` для **кожного** робота одночасно.
- КОЛИ `contact(robot, wall)` → ТО `block` (для цього робота) (?).
- КОЛИ `contact(robot, box)` → ЯКЩО `free(cell_behind)` → ТО `push(box)`; інакше `block`.
- КОЛИ `enter(robot, button[c])` → ТО `custom: «вміст ділянки сканера c копіюється в ділянку принтера c»`.
- КОЛИ `custom: «копіювання»` → ЯКЩО `occupied(scan_area, robot)` → ТО `clone(robot)` у ділянці друку — далі він ходить разом з усіма.
- КОЛИ `custom: «копіювання»` → ЯКЩО `occupied(scan_area, scanner|printer)` → ТО `spawn(device)` у ділянці друку — новий пристрій працює, як оригінал.
- КОЛИ `custom: «два сканери одного кольору ведуть в один принтер»` → ТО `merge(copy_a, copy_b → print_area)` — трубки накладаються (сектор MERGE).
- КОЛИ `custom: «ділянка друку одного каналу перекриває ділянку сканування іншого»` → ТО `trigger(rule)` — ланцюг копій за одним натисканням (сектор CHAIN COPY) (?).
- КОЛИ `after(move)` → ЯКЩО `connected(pipes)` and `custom: «фігура з трубок збігається з TARGET»` → ТО `win`, `next_level`.
- Перемога: візерунок трубок на ящиках і стінах = TARGET · Поразки нема — глухий кут знімає undo / restart · Рахунку нема.

## Керування і ввід
- `WASD` / стрілки — крок (Move); `Z` — Undo; `R` — Restart; `Esc` — Menu (підказки на екрані гри).
- Ввід: клавіатура, миша, будь-який геймпад (itch); повна підтримка контролерів (Steam).

## Вікна, меню, HUD
- `game-screen`: ліворуч — назва сектора й номер рівня (колір номера: жовтий / блакитний / червоний `EX`), легенда клавіш і легенда рамок «FROM ⋯ → TO ▢»; по центру поле; праворуч — панель `TARGET` з цільовою фігурою.
- HUD на полі: кольорові рамки сканування/друку, примара майбутнього друку в рамці принтера, підсвічена кнопка під роботом.
- `level-select` — стрічка вибору рівнів по секторах (коментар до демо) (?).
- `pause-menu` за `Esc` (?); `tutorial-window` — інтерактивне навчання (itch: «Interactive tutorial»).
- `achievements-window` (Steam Achievements).

## Фічі поза полем
- `undo` (по кроку), `restart-level`.
- 100+ рівнів у секторах, додаткові `EX`-рівні; `save-progress` + `cloud-save` (Steam Cloud).
- `localization` EN/JA; браузерне демо; «Playable without Timed Input».

## Варіації й родичі
- Родичі: [Sokobond](sokobond.md) (зʼєднання як мета), [Mirror Isles](mirror-isles.md) і [Order of the Sinking Star](order-of-the-sinking-star.md) (копії героя, що ходять разом), [Patrick's Parabox](patricks-parabox.md) (клон як посилання), [Baba Is You](baba-is-you.md) (кілька YOU одним вводом).
- **Осі варіацій** копіювання: що копіюється — ящики / робот / пристрої; скільки джерел — один сканер / злиття кількох; ланцюг — одна копія / копія запускає наступну; форма рамки — прямокутник / фігура.

## Цікавинки для курсу
- Копіювання ділянки сітки A → B як хід гри — 📎 (зріз двовимірного масиву + вставка).
- Примара друку в рамці принтера — 🌱 (превʼю результату дії до виконання).
- Копія робота й синхронний рух усіх роботів — 🥉 (порядок обробки, колізії між копіями).
- Злиття двох сканів в один друк — 🥉 (правило накладання: OR трубок чи заміна).
- Пристрої, що копіюють пристрої, і ланцюг копій — 🥈 (каскад подій з захистом від нескінченності).
- Перевірка «фігура з трубок = TARGET» з точністю до зсуву — 🥉 (нормалізація фігури + звʼязність).

## Мапа на каталог
- Є: `move-4dir`, `move-by-input`, `keyboard-controls` ↔ крок · `push-object` ↔ ящики · `impassable-cells` ↔ стіни · `pipe-connectors` ↔ трубки ящиків · `connectivity-check` ↔ фігура зʼєднана · `undo-step`, `restart-level` · `sequential-levels`, `level-select`, `save-progress` · `game-screen`, `pause-menu`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+copy-region` «Кнопка копіює ділянку A в ділянку B» · entities/interact · 🥉 · слоти {shape, overwrite: replace|merge}.
  - `+copy-merge` «Кілька сканерів в один друк» · entities/interact · 🥉.
  - `+self-copy` «Аватар копіюється разом із ділянкою» · entities/spawn · 🥉 (дитина `copy-region`).
  - `+device-copy` «Копіювальні пристрої теж копіюються; копії запускають копії» · entities/spawn · 🥈.
  - `+target-pattern-panel` «Цільова фігура на панелі поза полем» · interface/hud · 🌱.
  - `+print-preview-ghost` «Примара результату дії на полі» · interface/hud · 🌱.
  - `+multi-agent-sync` (уже пропонована) ↔ усі роботи ходять разом.

## Пропозиції до словників
- `+effect:copy_region(from, to)` — вміст ділянки-джерела зʼявляється в ділянці-цілі (копія, не переміщення).
- `+trigger:print(channel)` — спрацювала операція копіювання каналу (для ланцюгів CHAIN COPY).
- `+role:scanner` / `+role:printer` — пристрої-кінці копіювання (не `spawner`: породжують не свій тип, а знімок ділянки).
- `+ui:target-panel` — панель цільового стану поза полем; `+ui:print-preview` — примара результату в зоні дії.
- `+card:copy-region`, `+card:copy-merge`, `+card:self-copy`, `+card:device-copy` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/5230820/RECOPY/) — повний опис: scan/print, кнопка, копії робота, копії пристроїв, 100+ рівнів, без таймера; реліз 26.10.2026; EN/JA.
- [Демо на itch.io](https://masasgames.itch.io/recopy-demo) — грати в браузері; скриншоти секторів FIRST COPY, SELF COPY, CHAIN COPY, MERGE, DEVICE COPY з легендою клавіш і TARGET; коментар гравця про стрічку вибору рівнів.
- [masasgames на itch.io](https://masasgames.itch.io/) — розробник (також Tilnize Demo).
- YouTube: [пошук «RE:COPY puzzle gameplay»](https://www.youtube.com/results?search_query=RE%3ACOPY+puzzle+gameplay).

## Непевне
- Рецензій і вікі нема (реліз за два тижні до опису); механіка — з опису Steam і скриншотів демо, не з власної гри.
- (?) Друк замінює вміст ділянки чи накладається; що буває, якщо в ділянці друку стоїть робот або стіна.
- (?) Чи ціль — фігура з точністю до зсуву, чи в конкретному місці поля.
- (?) Чи всі роботи блокуються, якщо один уперся, чи лише той.
- (?) Як саме працює CHAIN COPY — одне натискання запускає каскад чи кожна кнопка окремо.
- (?) Чи стіни мають власні трубки (на скриншоті сектора 06 трубка видна на темній плитці).
