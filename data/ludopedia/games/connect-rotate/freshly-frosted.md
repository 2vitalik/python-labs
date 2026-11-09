---
title: Freshly Frosted
slug: freshly-frosted
aka: []
family: connect-rotate
also: [build-sim]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2022
platforms: [PC, Mac, Switch, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1070790/Freshly_Frosted/", best: true, note: "сторінка Steam: 144 пазли в 12 коробках; конвеєри, розгалужувачі, штовхачі, злиття, клонери, рандомайзери, телепорти; трейлер"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/freshly-frosted-switch/", note: "eShop Switch: форми пончиків (jelly-filled, maple bar, гарбуз, сніжинка, зірка), диктор, 10.06.2022"}
  - {kind: other, url: "https://cubed3.com/review/6817/1/freshly-frosted-nintendo-switch.html", note: "огляд Switch: глазур/посипка/крем/фрукти, кілька прилавків зі своїми замовленнями, підказка з рестартом, пропуск, Impatient Mode"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2819527521", note: "гайд-проходження: назви пазлів і досягнень (Splitters, Pusher, Frosting Physics, Infinite Loop, 400+ кроків)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2819763923", note: "гайд досягнень: назви 12 коробок, undo/заміна конвеєрів, Show Hint / Skip Puzzle у паузі, fast forward"}
  - {kind: other, url: "https://www.pocketgamer.com/freshly-frosted/out-now/", note: "мобільна версія 2024 (Snapbreak), free-to-play"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Freshly+Frosted+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [path-drawing, cell-click, cursor-place, carrier-platform, cell-transform, teleport, undo-redo, restart-level, skip-level, level-select, puzzle-select, level-unlock, sequential-levels, completion-detection, game-screen, main-menu, pause-menu, settings-window, background-music, volume-control, language-picker, save-progress, +run-simulation, +fast-forward, +hint-reveal, +item-filter-sort, +conveyor-splitter, +clone-on-pass, +random-router, +layered-decoration, +voice-narration, +loop-allowed]
proposes: ["+effect:add_layer", "+trigger:jam", "+ui:fast-forward-button", "+feature:impatient-mode", "+feature:voice-narration", "+card:conveyor-splitter", "+card:layered-decoration"]
author: opus
date: 2026-11-09
---

# Freshly Frosted — проклади конвеєри в пончиковій фабриці, щоб кожен прилавок отримав пончик зі своїм декором

## Суть
Затишний фабричний пазл від The Quantum Astrophysicists Guild: кімната — квадратна сітка з вхідними терміналами, машинами декору і прилавками доставки. Гравець малює конвеєрні стрічки, запускає фабрику, і пончики їдуть стрічками крізь машини (глазур, посипка, крем, фрукти), щоб дійти до прилавка, який приймає лише певний вид. Далі зʼявляються машини маршрутизації — розгалужувач, штовхач-сортувальник, злиття, клонер, рандомайзер, телепорт — і пазл стає задачею про потоки й порядок шарів. Без поразки: кожен рівень розвʼязується спокійно, з диктором і пастельною музикою.

## Поле і час
- Квадратна сітка кімнати; частина клітин зайнята терміналами, машинами, прилавками (?), решта — під конвеєри.
- Конвеєр — намальований відрізок з кількох клітин; може бути з однієї клітини; конвеєри можуть утворювати петлю, де пончики кружляють безкінечно.
- Час: гравець будує (статично), потім фабрика працює по кроках; є пазли на 400+ кроків, швидкість — нормальна / fast forward.
- Після розвʼязання фабрика працює далі (можна дивитися, доки щось не застрягне).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхідний термінал | source | вид тіста/форма | випускає пончики на стрічку (?) |
| Пончик | object | форма (класичний, maple bar, jelly-filled, гарбуз, сніжинка, зірка…); шари декору | їде стрічкою; набирає шари в машинах |
| Конвеєр | conduit | напрям, довжина | ставить гравець; везе пончик на клітину вперед за крок |
| Машина глазурі | terrain | колір глазурі (?) | пончик, що проїхав, отримує глазур |
| Машина посипки | terrain | — | додає посипку (поверх глазурі?) |
| Машина крему / начинки | terrain | — | додає крем або начинку («Filling It Up!») |
| Машина фруктів (вишня) | terrain | — | кладе вишню зверху |
| Розгалужувач (splitter) | switch | 2 виходи | відправляє пончики у два різні напрями |
| Штовхач (pusher) | switch | фільтр: вид пончика | шукає потрібний пончик і зіштовхує його на сусідню стрічку |
| Злиття (merger) | conduit | — | (?) зводить потоки або пончики разом |
| Клонер | spawner | — | (?) дублює пончик, що проїжджає |
| Рандомайзер | switch | — | (?) випадковий вихід або властивість |
| Телепорт | terrain | пара | переносить пончик в іншу точку кімнати |
| Прилавок доставки | sink | замовлення: вид і кількість (?) | приймає лише свій вид пончика |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `free(cell)` → ТО `place(player, conveyor)` уздовж руху курсора (напрям стрічки = напрям drag).
- КОЛИ `input(delete, cell)` → ТО `custom: «прибрати 1–2 клітини конвеєра»`; `input(undo)` → `undo(1)`; `input(clear)` → `custom: «очистити поле»`.
- КОЛИ `input(run)` → ТО `custom: «фабрика запускається; пончики виходять з терміналів»` (?).
- КОЛИ `tick` → ЯКЩО `occupied(cell, conveyor)` → ТО `move(donut, conveyor_dir)`.
- КОЛИ `enter(donut, frosting_machine)` → ТО `custom: «додати пончику шар глазурі»`; так само посипка, крем, фрукти.
- КОЛИ `enter(donut, sprinkles_machine)` → ЯКЩО `state(donut, frosted)` (?) → ТО `custom: «додати шар посипки»`.
- КОЛИ `enter(donut, splitter)` → ТО `custom: «пончик іде в один із двох виходів»` (по черзі, ?).
- КОЛИ `adjacent(pusher, donut)` → ЯКЩО `same(donut, pusher.filter, kind)` → ТО `push(donut)` на сусідню стрічку.
- КОЛИ `enter(donut, cloner)` → ТО `clone(donut)` (?).
- КОЛИ `enter(donut, randomizer)` → ТО `custom: «випадковий вихід»` (?).
- КОЛИ `enter(donut, teleporter)` → ТО `teleport(donut, pair)`.
- КОЛИ `contact(donut, counter)` → ЯКЩО `same(donut, counter.order, kind)` → ТО `disappear(donut)`, `counter(delivered, +1)`; інакше `custom: «прилавок не приймає»` (?).
- КОЛИ `blocked(donut)` → ТО `custom: «затор: стрічка й черга позаду стоять»` (?).
- КОЛИ `all_constraints_met` (кожен прилавок отримав своє) → ТО `win`, `message(narrator)`, `next_level`.
- КОЛИ `input(hint)` → ТО `restart`, `custom: «показати кілька правильних клітин конвеєра»`.
- КОЛИ `input(skip)` → ТО `next_level` (пазл лишається нерозвʼязаним).
- КОЛИ `input(fast_forward)` → ТО `speed(all, ×k)`; з Impatient Mode після перемоги — миттєве завершення.
- Перемога: усі прилавки задоволені. · Поразка: нема. · Рахунок: нема; лічильник доставлених пончиків — для досягнень (1000…5000).

## Керування і ввід
- Миша (ПК) / контролер чи тач (Switch, мобільні): тягнути, щоб покласти конвеєр; видалення по 1–2 клітини; undo; заміна конвеєра поверх.
- Кнопки запуску (?), fast forward; Esc / пауза → Show Hint, Skip Puzzle.

## Вікна, меню, HUD
- `main-menu`: Play → вибір коробки (`level-select`, 12 коробок-світів) → `puzzle-select` (12 пазлів коробки; в кінці показує всі розвʼязані); Settings; Extras → титри.
- `game-screen`: кімната-сітка; HUD — `fast-forward-button`, undo, видалення, повтор репліки диктора; `objective-text` — замовлення прилавків (?).
- `pause-menu`: Show Hint · Skip Puzzle · рестарт (?) · налаштування.
- `settings-window`: геймплей — Impatient Mode, туторіал; аудіо — гучність музики (до «11»), диктор вкл/викл; збільшений текст.
- `credits-window` — титри з окремими досягненнями.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 144 пазли = 12 коробок × 12 (Spring Day … Deepest Midnight), кожна з темою, формою пончика і своєю музикою.
- `hint` (показує частину розвʼязку, але скидає рівень), `skip-level` без ліміту (?), `undo`, `restart-level`, `speed-control` (fast forward).
- `voice-narration` — диктор коментує кожен пазл; вимикається.
- `font-scale`, `localization` (16 мов), `cloud-save`, `achievements` (78: 50 за рівні + 28 інших, напр. «зробити петлю», «симетричний розвʼязок»).
- Мобільна версія (Snapbreak, 2024) — free-to-play з покупками.

## Варіації й родичі
- [Trainyard](trainyard.md) — колії + симуляція, перефарбування й злиття поїздів; [Railbound](railbound.md), [Cosmic Express](cosmic-express.md) — план → запуск; [Pipe Mania](pipe-mania.md) — потік через прокладене.
- build-sim: [shapez](../build-sim/shapez.md), [Factorio belts](../build-sim/factorio-belts.md), [Automachef](../build-sim/automachef.md) — ті самі стрічки, розгалужувачі й машини обробки, але як відкрита економіка, а не пазл.
- Осі варіацій: **що змінюється в предметі**: колір (Trainyard) / шари декору (тут) / форма (shapez) · **маршрутизація**: лише стрічки / розгалужувач / фільтр-штовхач / телепорт · **запуск**: окремо після плану / жива фабрика · **кінець**: потрібна кількість доставок / безкінечний потік.

## Цікавинки для курсу
- Стрічки як граф «клітина → наступна»: крок симуляції для всіх пончиків разом, без колізій на одній клітині — 📎.
- Шари декору як впорядкований список (глазур → посипка → вишня) і порівняння з замовленням прилавка — 🌱.
- Розгалужувач по черзі (round-robin) і штовхач-фільтр — 📎.
- Клонер і рандомайзер: потік, де кількість предметів росте або маршрут випадковий — 🥉 (тест на детермінованість).
- Затор: виявити, що стрічка стала (жоден пончик не рухається N кроків) — 📎; виявити безкінечну петлю — 📎.
- Підказка «показати кілька правильних клітин» з еталонного розвʼязку — 🌱.

## Мапа на каталог
- Є: `path-drawing` + `cursor-place` ↔ малювання конвеєрів; `carrier-platform` ↔ стрічка везе пончик; `cell-transform` ↔ машини декору; `teleport` ↔ телепорти; `undo-redo` + `restart-level` + `skip-level`; `level-select` + `puzzle-select` + `level-unlock` + `sequential-levels` ↔ коробки; `completion-detection`; вікна й звук.
- **Нема** → пропозиції карток:
  - `+run-simulation` (з Trainyard/Cosmic Express) — план → запуск.
  - `+fast-forward`, `+hint-reveal` — уже в корпусі.
  - `+item-filter-sort` — штовхач, що вибирає вид.
  - `+conveyor-splitter` «Розгалужувач стрічки» · entities/move · 📎 · слот {mode: alternate|random}.
  - `+clone-on-pass` «Клонер на шляху» · entities/spawn · 🌱 (?).
  - `+random-router` «Випадковий вихід» · entities/move · 🌱 (?).
  - `+layered-decoration` «Шари на предметі за порядком машин» · entities/state · 📎.
  - `+voice-narration`, `+loop-allowed` (петля стрічок не помилка).

## Пропозиції до словників
- `+effect:add_layer(a, layer)` — додати шар декору, не змінюючи тип (на відміну від `transform`).
- `+trigger:jam` — потік став: предмет не може рухатися, черга позаду теж.
- `+ui:fast-forward-button` — прискорити запущене рішення.
- `+feature:impatient-mode` — після розвʼязання не дивитися анімацію, одразу завершити.
- `+feature:voice-narration` — диктор пояснює кожен пазл, вимикається.
- `+card:conveyor-splitter`, `+card:layered-decoration`.

## Джерела
- ⭐ [Steam: Freshly Frosted](https://store.steampowered.com/app/1070790/Freshly_Frosted/) — 144 пазли, 12 коробок, перелік машин, диктор, розробники, 10.06.2022.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/freshly-frosted-switch/) — форми пончиків, 12 сезонних коробок, перелік машин.
- [Cubed3: огляд Switch](https://cubed3.com/review/6817/1/freshly-frosted-nintendo-switch.html) — глазур/посипка/крем/фрукти, кілька прилавків з різними замовленнями, підказка з рестартом, пропуск, Impatient Mode, текст, диктор.
- [Steam-гайд «Full Walkthrough»](https://steamcommunity.com/sharedfiles/filedetails/?id=2819527521) — назви пазлів і досягнень, 400+ кроків, петля, однакова довжина конвеєрів.
- [Steam-гайд досягнень](https://steamcommunity.com/sharedfiles/filedetails/?id=2819763923) — назви коробок, undo/видалення/заміна, Show Hint/Skip Puzzle, fast forward, гучність до 11.
- [Pocket Gamer: мобільний реліз](https://www.pocketgamer.com/freshly-frosted/out-now/) — Snapbreak, 2024, free-to-play.
- Пошуковий фрагмент огляду Thinky Games (сторінка 403): розгалужувач — у два напрями; штовхач «шукає певний пончик і зіштовхує його на наступну стрічку».
- YouTube: пошук «Freshly Frosted gameplay».

## Непевне
- (?) Поведінка злиття, клонера, рандомайзера й телепорта — у джерелах лише назви; опис у таблиці — здогад з назв.
- (?) Розгалужувач: по черзі чи за правилом; чи є окрема кнопка запуску, чи фабрика працює наживо під час будування.
- (?) Порядок шарів декору (чи можна посипку без глазурі) і що робить прилавок з неправильним пончиком (відкидає / затор).
- (?) Чи прилавок вимагає певну кількість пончиків, чи один; чи є клітини, де конвеєр класти не можна.
- (?) Пропуск пазлів без ліміту — огляди не кажуть про обмеження.
- (?) Пошук (3 запити) і огляди RPS/Thinky/Gamezebo недоступні (403/помилка); правила зібрані з оглядів, eShop і назв досягнень.
