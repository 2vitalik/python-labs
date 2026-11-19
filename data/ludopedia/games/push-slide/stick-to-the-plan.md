---
title: Stick to the Plan
slug: stick-to-the-plan
aka: [过木不汪]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC, Switch]
links:
  - {kind: itch, url: "https://deadpixeltales.itch.io/stick-to-the-plan-jam", best: true, note: "безкоштовна джем-версія (HTML5 / Windows): WASD, Q/E — поворот, Space — взяти / покласти, R — рестарт; порада авторів «покладіть палицю й візьміть з іншого боку»"}
  - {kind: steam, url: "https://store.steampowered.com/app/2334280/", note: "повна гра (12.09.2023): рух, поворот, взяти / покласти; ≈70 рівнів, 5 світів; демо; 9 скріншотів"}
  - {kind: itch, url: "https://deadpixeltales.itch.io/stick-to-the-plan", note: "повна гра на itch: 5 локацій, 60+ рівнів, інтерактивне навчання, режим Textless"}
  - {kind: other, url: "https://www.pcgamer.com/heres-a-puzzle-game-about-a-small-dog-with-a-very-long-stick/", note: "PC Gamer: палиці, тростини, жердини, труби; ≈70 рівнів; джем-версія кінця 2022"}
  - {kind: other, url: "https://gamegrin.com/reviews/stick-to-the-plan-review", note: "огляд: палиця на 2 і на 3 клітини, сітчастий паркан, кожен світ — нова «фішка»"}
  - {kind: other, url: "https://ladiesgamers.com/stick-to-the-plan-review/", note: "огляд: не зачепити палицею жодного предмета, гра рахує «бемки», підказок нема, кнопка гавкоту"}
  - {kind: other, url: "https://ec.nintendo.com/NZ/en/titles/70010000074534", note: "Switch-версія (видавець SpaceJazz), ≈70 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stick+to+the+Plan+Roberto+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, multi-cell-size, impassable-cells, reach-exit, undo-step, restart-level, sequential-levels, level-unlock, world-map, controls-remap, language-picker, sound-effects, +attached-tool, +rotating-tool-sweep, +carry-goal-object, +drop-and-regrip, +tool-only-passage, +bump-counter]
proposes: ["+cond:sweep_free", "+card:drop-and-regrip", "+card:tool-only-passage", "+feature:object-outlines"]
author: opus
date: 2026-11-19
---

# Stick to the Plan — пес Роберто несе довгу палицю крізь перешкоди: крок, поворот, покласти й узяти з іншого кінця

## Суть
Покрокова 3D-головоломка на клітинах від Dead Pixel Tales (2023): пес Роберто тримає в зубах довгу палицю — тростину, жердину, трубу — і має донести її до клітини з лапкою. Палиця стирчить убік і зачіпає перешкоди, тож шлях планується для всього тіла «пес + палиця», а не для самого пса. Огляди називають це Sokoban-подібним пазлом: пройти рівень, не зачепивши палицею жодного предмета.

Дієслів чотири: крок, поворот на 90°, покласти палицю і взяти її знову — з іншого кінця, і тоді вона стирчить в інший бік. Кожен із 5 світів додає свою «фішку»: сітчастий паркан, крізь який палиця пролазить, а пес — ні, палиці різної довжини, кнопки й стовпчики. Близько 70 рівнів; повна гра виросла з безкоштовної джем-версії кінця 2022 року.

## Поле і час
- Квадратна сітка з окремих плиток-кубиків, між ними — порожнеча; камера 3/4 згори.
- Хід = одна дія (крок, поворот, узяти / покласти); без вводу світ не змінюється.
- Тіло гравця займає кілька клітин: пес + палиця довжиною 2 або 3 клітини (з клітиною пса), спрямована вбік від пса.
- Світи на скріншотах: місто (Downtown — конуси, світлофор, «зебра»), нічний ліс зі світлячками (Firefly Forest — мости з дощок, вогнище), сад із парканами й вазонами, пустир із бочками, шинами й висувними стовпчиками, вольєр із сітки й каналізаційними ґратками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Роберто (пес) | player | — | крок 4 напрямки, поворот на 90°, узяти / покласти палицю, гавкіт |
| Палиця (тростина, жердина, труба, шпажка з маршмелоу) | object | довжина 2 / 3 клітини; бік | у зубах — жорстко зчеплена з псом; на землі — лежить, доки не піднімуть |
| Лапка | terrain | — | ціль: сюди треба прийти з палицею |
| Плитка підлоги | terrain | — | прохідна |
| Порожнеча між плитками | static | — | пес туди не ступає |
| Перешкода (конус, бочка, шини, вазон, дерево, поштова скринька, світлофор, труба з вентилем, коробки) | static | — | блокує і пса, і палицю |
| Сітчастий паркан | static | — | блокує пса, палиця проходить крізь сітку |
| Дерев'яний паркан | static | на ребрі клітини | перешкода між клітинами |
| Жовта кнопка | switch | — | біля висувних стовпчиків (скріншот) |
| Висувний стовпчик | gate | висунутий / схований | стоїть у гнізді на металевій плиті (скріншот) |
| Каналізаційна ґратка | hazard | — | табличка «DON'T STEP ON SEWERS» |
| Міст із дощок | terrain | — | прохід між плитками |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` і `custom: «клітини палиці після зсуву вільні»` → ТО `move(dog, dir)`, `move(stick, dir)` — палиця не обертається; інакше `block`.
- КОЛИ `input(rotate_left)` → ЯКЩО `custom: «клітини, які замітає палиця при повороті на 90° навколо пса, вільні»` → ТО `rotate(dog, -90)`, `rotate(stick, -90)`; інакше `block`.
- КОЛИ `input(rotate_right)` → ЯКЩО `custom: «замітання при повороті вільне»` → ТО `rotate(dog, 90)`, `rotate(stick, 90)`; інакше `block`.
- КОЛИ `input(pick_drop)` → ЯКЩО `has(dog, stick)` → ТО `place(dog, stick)` — палиця лягає на ті самі клітини.
- КОЛИ `input(pick_drop)` → ЯКЩО `in_range(dog, stick_end, 1)` → ТО `pickup(dog, stick)`, `attach(dog, stick)` — хват за той кінець, біля якого стоїть пес, тож палиця тепер стирчить в інший бік.
- КОЛИ `contact(stick, obstacle)` → ТО `block`, `counter(bonks, +1)` — гра рахує предмети, у які палиця «бемкнула».
- КОЛИ `contact(dog, mesh_fence)` → ТО `block`.
- КОЛИ `contact(stick, mesh_fence)` → ТО `custom: «палиця проходить крізь сітку»`.
- КОЛИ `enter(dog, paw_goal)` → ЯКЩО `has(dog, stick)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)` — додано в демо квітня 2023 на прохання гравців джем-версії.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `input(bark)` → ТО `sound(bark)`.
- Перемога: пес із палицею в зубах на лапці. · Поразка: нема (глухий кут → undo / рестарт). · Рахунок: нема; рахуються «бемки».

## Керування і ввід
- WASD — крок у напрямках відносно камери (у джем-версії гравці просили «танкове» керування, тобто воно не таке); Q / E — поворот на 90°; Space — узяти / покласти палицю; R — рестарт.
- Undo — з демо 2023; окрема кнопка гавкоту.
- Повна підтримка геймпада; перепризначення клавіш і кнопок — з оновлення 18.09.2023.

## Вікна, меню, HUD
- `level-select` / `world-map`: намальована від руки мапа світу (Downtown) зі стежкою вузлів-рівнів 1, 2, 3, 4…, замкнені вузли з замком, стрілки ‹ › між світами.
- `game-screen`: 3D-поле з плитками, без помітного HUD на скріншотах.
- `custom-window` — ілюстровані комікс-вставки між рівнями з історією Роберто.
- `settings-window`: контури Роберто й палиць, вимкнення вібрації, вікно / повний екран, перепризначення, 12 мов (зокрема каталонська).
- `tutorial-window` — інтерактивне навчання; режим «Textless» (itch).
- `loading-screen` — анімація лапки (General Update 1, листопад 2023).
- Переходи: мапа світу → рівень → (пес із палицею на лапці) → наступний вузол; між світами — комікс.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map`: 5 світів, ≈70 рівнів.
- `undo`, `restart-level`; підказок нема.
- Контури персонажа й палиць (доступність), `remap-controls`, `gamepad-support`, `localization` (12 мов), Steam Deck Verified.
- Досягнення Steam (напр. «A stick to govern them all»); сезонний відьомський капелюх на Хелловін 2023.
- Безкоштовна джем-версія (джем «Thinky games are for everyone»), демо в Steam і на itch.

## Варіації й родичі
- Джем-версія → повна гра: ≈50 нових рівнів, нові механіки й світи, undo (devlog 27.01.2023).
- Родичі за «тілом з інструментом»: [stephens-sausage-roll](../thinky/stephens-sausage-roll.md) (виделка попереду, поворот замітає клітини), [raking-sokoban](raking-sokoban.md) (граблі зчеплені з гравцем), [kwirk](kwirk.md) (турнікет: замітання при повороті), [bloxorz](bloxorz.md) (тіло на 2 клітини).
- Осі варіацій:
  - **де інструмент**: попереду (Sausage Roll, Raking Sokoban) / збоку від пса (Stick to the Plan);
  - **чи можна його відпустити**: ні (Sausage Roll) / покласти й узяти з іншого кінця (Stick to the Plan);
  - **що пропускає інструмент, але не тіло**: нічого / сітчастий паркан;
  - **довжина**: 1 клітина / 2–3 клітини, змінюється між рівнями.

## Цікавинки для курсу
- Тіло «пес + палиця» як жорстка фігура: крок перевіряє всі клітини палиці — 🌱.
- Поворот на 90° навколо пса з перевіркою замітання (клітини між старим і новим положенням палиці) — 🥉.
- Покласти й узяти з іншого кінця: зміна точки хвату як окремий хід — 📎.
- Перешкода-фільтр: сітка пропускає палицю, але не пса (дві маски колізій) — 🌱.
- Лічильник «бемків» як вторинна метрика — 🌱.
- Розвʼязувач BFS: стан = (клітина пса, бік палиці або де вона лежить) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ WASD; `multi-cell-size` ↔ палиця на 2–3 клітини; `impassable-cells` ↔ перешкоди; `reach-exit` ↔ лапка; `undo-step` + `restart-level` ↔ undo / R; `sequential-levels` + `level-unlock` + `world-map` ↔ мапа світів; `controls-remap`; `language-picker` ↔ 12 мов; `sound-effects` ↔ гавкіт.
- **Нема** → пропозиції карток:
  - `+attached-tool` (є в корпусі: Raking Sokoban) · слоти {side: perpendicular, length: 2|3}.
  - `+rotating-tool-sweep` (є в корпусі: Sausage Roll) · слот {trigger: command}.
  - `+carry-goal-object` (є в корпусі) — донести палицю до лапки.
  - `+drop-and-regrip` «Покласти інструмент і взяти з іншого кінця» · entities/interact · 📎.
  - `+tool-only-passage` «Перешкода пропускає інструмент, але не аватара» · entities/legality · 🌱 — сітчастий паркан.
  - `+bump-counter` «Лічильник зіткнень як метрика» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:sweep_free` — клітини, які замітає поворот довгого тіла, вільні (у Kwirk і Sausage Roll — через `custom`).
- `+card:drop-and-regrip`, `+card:tool-only-passage` — див. «Мапа на каталог».
- `+feature:object-outlines` — контури персонажа й ключових предметів як опція доступності (не те саме, що high-contrast).

## Джерела
- ⭐ [itch.io: Stick to the Plan [Jam]](https://deadpixeltales.itch.io/stick-to-the-plan-jam) — грати безкоштовно; керування; коментарі: порада «drop the stick and pick it up from the other side», прохання undo, баг із поворотом крізь камінь.
- [Steam](https://store.steampowered.com/app/2334280/) — «move, rotate, pick up & drop your stick», ≈70 рівнів, 5 світів; новини: undo в демо, перепризначення, General Update 1, хотфікс «goal without stick».
- [itch.io: повна гра](https://deadpixeltales.itch.io/stick-to-the-plan) — 5 локацій, 60+ рівнів, навчання, Textless.
- [PC Gamer](https://www.pcgamer.com/heres-a-puzzle-game-about-a-small-dog-with-a-very-long-stick/) — палиці, тростини, жердини, труби; контури; джем-версія 2022 (Dead Pixel Tales, Rocket Raw, Naburo, Delunado).
- [GameGrin](https://gamegrin.com/reviews/stick-to-the-plan-review) — палиця на 2 і на 3 клітини, сітчастий паркан, «фішка» на світ.
- [LadiesGamers](https://ladiesgamers.com/stick-to-the-plan-review/) — «не зачепити палицею жодного предмета», підрахунок «бемків», кнопка гавкоту, контури, підказок нема.
- [Nintendo eShop NZ](https://ec.nintendo.com/NZ/en/titles/70010000074534) — Switch, SpaceJazz.
- YouTube: пошук «Stick to the Plan Roberto gameplay».

## Непевне
- (?) Геометрія хвату: зі скріншотів палиця стирчить убік від пса за один кінець; чи завжди перпендикулярно погляду і як саме обирається бік при підйомі — не перевірено.
- (?) Чи блокує удар палиці хід, чи лише рахується як «бемк» і хід усе ж відбувається; чи може палиця висіти над порожнечею (на одному скріншоті звисає за край).
- (?) Що стається, якщо прийти на лапку без палиці (до хотфіксу першого дня це ламало гру).
- (?) Поведінка кнопок і висувних стовпчиків, каналізаційних ґраток, вогнища, мостів і дерев'яних парканів для палиці — лише зі скріншотів.
- (?) Число рівнів: Steam, PC Gamer і eShop — ≈70, GameGrin — «понад 100»; іспанський огляд IGN не відкрився.
