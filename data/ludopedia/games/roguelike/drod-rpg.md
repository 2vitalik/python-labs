---
title: "DROD RPG: Tendry's Tale (+ DROD RPG 2)"
slug: drod-rpg
aka: [DROD RPG, "Tendry's Tale", "DROD RPG 2: A Courageous Rescue"]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: none
  goal: score
year: 2008
platforms: [PC (Windows, Linux, Mac), Steam]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/351330/", best: true, note: "Tendry's Tale (Steam 2016): огляд — вибір, кого бити, детерміновані дуелі, 13 рівнів, 25 предметів, редактор, рекорди"}
  - {kind: steam, url: "https://store.steampowered.com/app/3661610/", note: "DROD RPG 2: A Courageous Rescue (25.08.2025) — «грається як Magic Tower», 3 глави, складність"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Deadly_Rooms_of_Death", note: "DROD RPG — 12.09.2008, Mike Rimer; HP, спорядження, ключі замість старих умов дверей"}
  - {kind: official, url: "https://github.com/CaravelGames/drod", note: "відкритий код DROD і DROD RPG (тека drodrpg/)"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/elements.html", note: "довідка гри: усі елементи — двері, ключі, зілля, лопати, туман, стрілки, сфери, бомби, тунелі"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/equipment.html", note: "довідка: мечі/щити/аксесуари з ATK/DEF і властивостями"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/monster.html", note: "довідка: бестіарій"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/hints.html", note: "поради Тендрі: удар мечем — перший удар твій, тілом — монстра; гобліни, очі, мізки"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/keyboard.html", note: "усі клавіші й дії мишею: undo кімнати, рестарт, рахунок, статистика монстрів, мапа"}
  - {kind: other, url: "https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/DRODLib/Combat.cpp", note: "точний алгоритм дуелі: тіки, ініціатива, подвоєння ATK/DEF, прогноз шкоди симуляцією"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DROD+RPG+Tendry%27s+Tale+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-8dir, keyboard-controls, cell-click, key-and-door, hp-damage, item-pickup, inventory-items, impassable-cells, round-currency, line-of-sight-attack, button-toggle, one-way-cell, teleport, push-object, mirror-reflect, chain-reaction, stairs-levels, sequential-levels, player-death, undo-redo, undo-unlimited, restart-level, save-multi-slot, save-autosave, state-as-data, minimap-radar, map-window, codex-window, leaderboard, achievements-window, in-game-editor, level-exchange, +deterministic-combat, +damage-preview, +sword-cell, +first-strike-by-weapon, +equipment-swap-drop, +combat-clock, +weighted-resource-score, +stat-gems, +money-door, +aura-buff]
proposes: ["+trigger:bump(a, b)", "+trigger:combat_end", "+cond:can_damage(a, b)", "+cond:from_behind(a, b)", "+effect:fight(a, b, first)", "+effect:stat(a, name, ±n)", "+role:weapon", "+ui:expected-damage", "+window:monster-stats", "+window:score-breakdown", "+feature:room-undo", "+feature:quick-backtrack", "+card:combat-clock"]
author: opus
date: 2026-11-09
---

# DROD RPG — кімнати DROD з дуелями Magic Tower: меч дає перший удар, а кожен бій — рішення «зараз чи пізніше»

## Суть
Тендрі пробирається підземеллям із кімнат DROD: рівень — мережа взаємоповʼязаних кімнат, мета — вихід (сходи). Монстри **розставлені вручну й здебільшого стоять**: гравець сам обирає, з ким битися, а бій — **детермінована дуель** за HP/ATK/DEF, результат якої видно заздалегідь. Ресурси (ключі трьох кольорів, гроші-«грекли», лопати, зілля, кристали ATK/DEF) скінченні, тож гра — оптимізація маршруту й порядку боїв, як у [Magic Tower](magic-tower.md). Від DROD лишились меч у сусідній клітині (ним бити — значить бити першим), сфери, стрілки, тунелі, туман і бомби. DROD RPG 2 (2025) — те саме ядро, нова кампанія.

## Поле і час
- Квадратна сітка; кімната = один екран DROD, кімнати зʼєднані краями (вихід за край → сусідня кімната). Розмір кімнати як у DROD (38×32 (?)).
- Рівень — набір кімнат зі сходами-виходом; кампанія (hold) — 13 рівнів у Tendry's Tale, 15+ у RPG 2 (за Steam).
- `info: partial`: кімнату видно цілком, щойно ввійшов; невідвідані кімнати лише на мінімапі (і то після предмета-мапи), є приховані кімнати.
- Хід = крок на 1 з 8 напрямків, поворот меча на 45° або очікування. Без вводу світ стоїть.
- Дуель розігрується всередині одного ходу як симуляція «тіків»: кожна сторона накопичує тіки до 1000 і тоді бʼє; швидкість гравця подвоює зілля швидкості, монстри бʼють рівномірно (код `Combat.cpp`).
- **Годинник боїв**: туманні вентилі й кущі шипшини реагують не на кроки, а **на кожен бій** (кожна дуель — «тік» для них).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тендрі | player | HP (без верхньої межі), ATK, DEF, GR (грекли), REP; ключі Y/G/B/скелетні; лопати | 8 напрямків; меч займає сусідню клітину в напрямку погляду |
| Меч (слот зброї) | object | +ATK 10…220, властивості (метал, проти гоблінів, проти змієв, ігнор DEF…) | клітина меча — зона удару; поворот Q/W на 45° |
| Щит (слот броні) | object | +DEF 10…220, властивості (захист від туману, від променів) | пасивно |
| Аксесуар (слот) | object | одна здібність | гак (стрибок через яму), ласти (вода), щаслива монета ×2 GR, VIP ×2 REP, зілля невидимості/швидкості, ручна бомба, кайло, варп, переносна сфера, прохід крізь стіну |
| Монстр (загальний) | enemy | HP, ATK, DEF, GR, REP, слабкість | стоїть; дуель починає гравець (мечем чи тілом) |
| Гоблін | enemy | — | повертається обличчям до Тендрі; бʼє першим, щойно той стане до нього спиною |
| Зле око | enemy | — | атакує, коли Тендрі перетинає його лінію погляду; зненацька ззаду — пропускає удар |
| Мізок | enemy | — | кожен мізок у кімнаті подвоює ATK усіх монстрів |
| Аумтліх | enemy | — | погляд ділить HP Тендрі навпіл; дзеркало відбиває погляд |
| Королева тарганів | spawner | — | відкладає яйця; яйця — барʼєр, не шкодять |
| Мімік | ally | — | повторює рухи Тендрі; ним можна бити монстрів на відстані |
| Мечник / Різник (Slayer) | boss | великі ATK | «дуже небезпечні», їх треба вбити швидко |
| Смола / бруд / гель | enemy | — | вразливі лише в певних точках краю; мати-смола робить небезпечним увесь згусток |
| Інші (тарган, мурашиний лев, водомірка, сіп у стіні, змії, голем, ...) | enemy | — | власні реакції; більшість не ходить |
| Двері жовті / зелені / сині | gate | колір | відкриває ключ того ж кольору (витрачається) або скелетний ключ |
| Червоні двері | gate | — | відчиняються, коли всі люки в кімнаті провалились |
| Чорні двері | gate | — | відчиняються, коли в кімнаті не лишилось смоли |
| Грекльова брама (money door) | gate | ціна в GR | плата грошима; можна зачинити назад (Lock) |
| Ключ Y/G/B / скелетний | pickup | колір | +1 ключ |
| Зілля мале / середнє / велике / величезне | pickup | +15 / +50 / +200 / +1000 HP | лікує одразу |
| Кристал ATK / DEF | pickup | +1 / +3 / +10 × множник рівня | постійно |
| Лопата 1 / 3 / 10 | pickup | × множник рівня | +лопати |
| Брила землі 1 / 3 / 5 | static | ціна в лопатах | зникає, якщо лопат вистачає |
| Предмет спорядження на підлозі | pickup | меч / щит / аксесуар | обмін зі слотом, старий лягає на клітину |
| Гаряча плитка | hazard | % HP (за замовч. 5 %) | шкода щоразу при вході |
| Туман / туманний вентиль | terrain / spawner | — | у тумані DEF → 0; вентиль додає туман після кожного бою, туман розростається |
| Яма / вода | terrain | — | Тендрі не падає, але не пройде; літуни / плавці проходять |
| Люк | terrain | — | провалюється в яму/воду після того, як з нього зійшли |
| Силова стрілка | terrain | напрям | забороняє рух проти стрілки; сфера/плита вмикає й вимикає |
| Сфера / натискна плита | switch | одноразова / багаторазова / вкл-викл | відкриває, закриває чи перемикає двері, стрілки, вогняні пастки, світло |
| Бомба / порохова бочка | object | радіус 3 / 1 | вибух від удару мечем або запалу; ланцюг; бочку можна штовхати |
| Запал | object | — | горить від кінця або вибуху; не горить проти стрілки |
| Тунель | terrain | напрям | рух у напрямку тунелю → найближчий тунель у ряду/стовпці |
| Ящик / дзеркало | object | — | штовхаються тілом; стоячи на ящику — імунітет до туману й гарячих плиток |
| Вогняна пастка | hazard | вкл/викл | увімкнена шкодить кожному, хто стане |
| Шипшина (корінь) | hazard | — | росте після кожного бою, суха — просто стіна |
| Сувій / мапа | pickup | — | текст; мапа відмічає кімнати рівня |
| Сходи | static | — | вихід з рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(tendry, dir)` (меч рухається разом).
- КОЛИ `input(rotate_cw|rotate_ccw)` → ТО `rotate(sword, 45)`; меч, що входить у клітину монстра, атакує.
- КОЛИ `contact(sword, monster)` → ЯКЩО `custom: «ATK Тендрі > DEF монстра»` → ТО `custom: «дуель, Тендрі бʼє першим»`.
- КОЛИ `contact(tendry, monster)` (тілом) → ТО `custom: «дуель, монстр бʼє першим»`; Тендрі лишається на місці.
- КОЛИ `custom: «спроба атаки»` → ЯКЩО `custom: «ATK ≤ DEF монстра і монстр може поранити»` → ТО `block`, `message(«Can't harm enemy»)` (хід скасовано).
- Дуель (симуляція тіків):
  - удар Тендрі: `damage(monster, ATK − DEF_m)`; ATK ×2 від невидимості, сильної проти виду зброї або удару ззаду (backstab) першим ударом;
  - удар монстра: `damage(tendry, ATK_m×2^мізків − DEF)`, не менше 0; DEF = 0 у тумані, ×2 від «сильного» щита;
  - тричі поспіль нікому нема шкоди → бій скінчено без переможця.
- КОЛИ `hp_zero(monster)` → ТО `disappear(monster)`, `currency(+GR)`, `counter(REP, +n)`.
- КОЛИ `hp_zero(tendry)` → ТО `lose`; ЯКЩО `custom: «ще звучить крик смерті»` → `undo(1)` повертає хід.
- КОЛИ `custom: «Тендрі стоїть спиною до гобліна поруч»` → ТО `custom: «гоблін ініціює дуель і бʼє першим»`.
- КОЛИ `line_of_sight(evil_eye, tendry)` → ТО `custom: «око ініціює дуель»`; ЯКЩО `custom: «удар ззаду»` → монстр пропускає перший удар.
- КОЛИ `line_of_sight(aumtlich, tendry)` → ТО `custom: «HP Тендрі / 2»`; дзеркало між ними `bounce` погляд.
- КОЛИ `contact(tendry, door[c])` → ЯКЩО `has(tendry, key[c])` → ТО `take(tendry, key[c])`, `set_cell(door, open)`; ЯКЩО `has(tendry, skeleton_key)` → те саме зі скелетним; інакше `block`.
- КОЛИ `all_gone(trapdoor)` → ТО `set_cell(red_door, open)` · КОЛИ `all_gone(tarstuff)` → ТО `set_cell(black_door, open)`.
- КОЛИ `contact(tendry, money_door)` → ЯКЩО `counter(GR, >=, cost)` → ТО `currency(−cost)`, `set_cell(money_door, open)`.
- КОЛИ `input(lock)` → ЯКЩО `occupied(cell_under, open_door)` → ТО `custom: «зачинити двері, витративши ключ / гроші»`.
- КОЛИ `contact(tendry, potion)` → ТО `pickup`, `heal(tendry, 15|50|200|1000)` (стелі HP нема).
- КОЛИ `contact(tendry, gem)` → ТО `pickup`, `custom: «ATK або DEF + n × множник рівня»`.
- КОЛИ `contact(tendry, dirt_k)` → ЯКЩО `counter(shovels, >=, k)` → ТО `counter(shovels, −k)`, `set_cell(dirt, floor)`, `move(tendry, dir)`; інакше `block`.
- КОЛИ `enter(tendry, equipment)` → ТО `swap(slot, equipment)` — старий предмет лягає на клітину.
- КОЛИ `enter(tendry, hot_tile)` → ЯКЩО `not state(tendry, on_crate)` → ТО `damage(tendry, 5%)`.
- КОЛИ `leave(tendry, trapdoor)` → ТО `set_cell(trapdoor, pit)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «рух проти силової стрілки»` → ТО `block`.
- КОЛИ `contact(sword, orb)` або `enter(any, pressure_plate)` → ТО `trigger(rule)` (відкрити / закрити / перемкнути двері, стрілки, пастки).
- КОЛИ `contact(sword, bomb)` → ТО `explode(square, 3)`; бомби й бочки в радіусі детонують ланцюгом.
- КОЛИ `enter(tendry, tunnel)` → ЯКЩО `moving(tendry, tunnel_dir)` → ТО `teleport(tendry, nearest_tunnel_in_line)`.
- КОЛИ `custom: «завершилась дуель»` → ТО `spawn_at(mist, vent)`, `custom: «туман і шипшина розростаються на крок»`.
- КОЛИ `count(brain, >=, 1)` → ТО `custom: «ATK кожного монстра ×2 за кожен мізок»`.
- КОЛИ `enter(tendry, stairs)` → ТО `next_level`; ЯКЩО `custom: «наступного входу нема»` → `win`.
- КОЛИ `input(backspace)` → ТО `undo(1)` (лише в межах поточної кімнати) · КОЛИ `input(R)` → ТО `restart` (кімнати).
- Перемога: вийти з останнього рівня. Поразка: HP = 0 (або «софтлок» без ключів/сил). Рахунок (за замовч., холд може змінити): HP/40 + 5·ATK + 3·DEF + 10·жовтий ключ + 20·зелений + 30·синій + 30·скелетний + 1·лопата.

## Керування і ввід
- Цифровий блок 1–9 — крок у 8 напрямках, 5 — чекати; Q / W — повернути меч проти / за годинниковою (колесо миші теж).
- Клік по клітині — Тендрі йде туди, якщо є прямий шлях; клік за краєм кімнати — у сусідню.
- Tab — використати аксесуар; Shift-Tab / Ctrl-Tab — спецздібність зброї / броні; 0 — замкнути двері під собою.
- Backspace — undo в кімнаті; R — рестарт кімнати; Ctrl+напрям — швидкий біг до вже відомого виходу.
- Правий клік: по клітині — що на ній; по монстру — стати, властивості, **очікувана шкода** і нагорода; по сфері — які двері вона перемикає.

## Вікна, меню, HUD
- `game-screen`: кімната + бічна панель — `stat-panel` (HP, ATK, DEF, GR, REP), лічильники ключів Y/G/B/S і лопат, `equipment-slots` (меч, щит, аксесуар; клік — використати), `minimap` (кольори: золото — лишились бонуси, червоний — лише монстри, синій — лише зачинені двері, білий — очищено), портрет-обличчя, `move-counter` (F7).
- `monster-stats` (кнопка + на цифровому блоці) — усі монстри кімнати: HP/ATK/DEF, нагорода, очікувана шкода; працює й для віддалених кімнат з мапи.
- `score-breakdown` (−) — поточний рахунок і з чого він складається; «New personal best!».
- `map-window` — клік по мінімапі: відвідані кімнати в поточному стані; правий клік — позначити кімнату одним із трьох кольорів.
- `save-slots` — F2/F3 збереження/завантаження, F5/F9 швидкі; Esc — у `main-menu` зі збереженням у слот «continue».
- `dialogue-window` — історія діалогів кімнати (подвійний клік по портрету), сувої.
- `help-window` (F1), `settings-window` (F6), `editor-window` (редактор кампаній), `custom-window` вибору холду й гравця, чат CaravelNet.
- `end-screen` — фінал холду; `achievements-window` і `leaderboard` — через Steam.
- Переходи: `main-menu` → вибір холду → `game-screen` ⇄ `monster-stats` / `score-breakdown` / `map-window` / `save-slots` / `help-window`.

## Фічі поза полем
- `undo` без ліміту, але **лише в межах поточної кімнати** (стан кімнати відтворюється з команд від входу); `restart-level` для кімнати; смерть можна відкотити.
- `save-slots` + `autosave` (не під час бою); швидкі сейви; «чекпоінти рахунку» для відправки рекорду.
- `leaderboard-online` (Steam: рахунок проти інших гравців), `achievements`, `cloud-save`.
- `level-editor` + скрипти персонажів, `user-levels-browser` (холди спільноти через CaravelNet), `mod-support`.
- DROD RPG 2: `difficulty-presets` (регульована складність), опції «лише миша / лише клавіатура / лише дотик» за Steam.

## Варіації й родичі
- **DROD RPG 2: A Courageous Rescue** (2025): та сама механіка; кампанія з 3 глав, 15+ рівнів, 25+ предметів, регульована складність, розширені скрипти редактора.
- Батьки: [DROD](../thinky/drod.md) (меч у сусідній клітині, сфери, стрілки, смола, мізки — там вони вбивають, тут лише посилюють) і [Magic Tower](magic-tower.md) (дуель за формулою, ключі як бюджет).
- Родичі: [Tactical Nexus](tactical-nexus.md), [h5mota](h5mota.md), [DungeonUp](dungeonup.md), [Towerbound](towerbound.md), Towers of Scale ([towers-of-scale](towers-of-scale.md)).
- Осі варіацій: **ініціатива** (завжди герой — Magic Tower / залежить від способу атаки — DROD RPG) · **бій** (закрита формула / симуляція тіків зі швидкістю) · **годинник світу** (кроки / бої) · **undo** (сейви / кімната / усе) · **спорядження** (стек бонусів / один слот з обміном).

## Цікавинки для курсу
- Дуель як симуляція тіків з ініціативою й подвоєннями — 📎 (чиста функція, легко тестувати).
- Прогноз шкоди: запуск тієї ж симуляції на копії стану (з екстраполяцією, якщо бій задовгий) — 🥉.
- Ініціатива залежить від способу атаки (меч — твій перший удар, тіло — монстра; удар ззаду — ×2) — 🌱.
- Обмін спорядженням зі «скиданням» старого на клітину — 🌱.
- Годинник боїв: туман і шипшина ростуть після кожної дуелі, а не кроку — 📎.
- Рахунок як зважена сума ресурсів (від'ємний множник = «1 очко за N одиниць») — 🌱.
- Undo кімнати як повторне програвання списку команд від входу — 🥉.

## Мапа на каталог
- Є: `move-8dir`, `keyboard-controls`, `cell-click` ↔ рух і автошлях; `key-and-door` ↔ двері трьох кольорів; `hp-damage`, `item-pickup`, `inventory-items` ↔ зілля, кристали, аксесуари; `round-currency` ↔ GR; `line-of-sight-attack` ↔ зле око, аумтліх; `button-toggle` ↔ сфери й плити; `one-way-cell` ↔ силові стрілки; `teleport` ↔ тунелі; `push-object` ↔ ящики, дзеркала, бочки; `mirror-reflect` ↔ дзеркало проти погляду; `chain-reaction` ↔ бомби; `stairs-levels` + `sequential-levels` ↔ рівні холду; `undo-redo` + `undo-unlimited` + `restart-level` ↔ undo кімнати; `save-multi-slot` + `save-autosave`; `state-as-data` ↔ стан як список команд; `minimap-radar` + `map-window`; `codex-window` ↔ статистика монстрів; `leaderboard`, `achievements-window`; `in-game-editor` + `level-exchange` ↔ редактор і холди.
- **Нема** → пропозиції карток:
  - `+deterministic-combat` (Magic Tower) — тут варіант-симуляція тіків · слот {initiative, speed}.
  - `+damage-preview` — очікувана шкода на правий клік і у вікні статистики.
  - `+sword-cell` (DROD) — зброя займає клітину поруч.
  - `+first-strike-by-weapon` «Хто бʼє першим — залежить від способу атаки» · entities/combat · 🌱.
  - `+equipment-swap-drop` «Один слот на тип, старе лягає на підлогу» · entities/state · 🌱.
  - `+combat-clock` «Світ тікає від боїв, не від кроків» · entities/spawn · 📎.
  - `+weighted-resource-score` «Рахунок = зважена сума ресурсів на виході» · game-logic/score · 🌱.
  - `+stat-gems` (Magic Tower), `+money-door` «Двері за гроші» · entities/interact · 🌱, `+aura-buff` «Сутність посилює інших у зоні (мізок ×2 ATK)» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:bump(a, b)` — гравець «входить» у зайняту клітину (тут — тілом, з іншою ініціативою, ніж мечем).
- `+trigger:combat_end` — після кожної дуелі (годинник туману й шипшини).
- `+cond:can_damage(a, b)` — ATK > DEF; `+cond:from_behind(a, b)` — атака ззаду (backstab, «surprised from behind»).
- `+effect:fight(a, b, first)` — атомарна дуель з указаним першим ударом; `+effect:stat(a, name, ±n)` — змінити ATK/DEF.
- `+role:weapon` — меч як сутність у клітині (вже з DROD).
- `+ui:expected-damage` — очікувана шкода в підказці монстра.
- `+window:monster-stats`, `+window:score-breakdown` — окремі вікна.
- `+feature:room-undo` — undo лише в межах кімнати; `+feature:quick-backtrack` — біг до відомого виходу однією командою.
- `+card:combat-clock`.

## Джерела
- ⭐ [Steam: DROD RPG: Tendry's Tale](https://store.steampowered.com/app/351330/) — суть: вибір боїв, «бий зараз або пізніше сильнішим», детерміновані дуелі, 13 рівнів, 25 предметів, редактор, рекорди.
- [Steam: DROD RPG 2](https://store.steampowered.com/app/3661610/) — 2025, «грається як Magic Tower», 3 глави, складність, 15+ рівнів.
- [Wikipedia: Deadly Rooms of Death](https://en.wikipedia.org/wiki/Deadly_Rooms_of_Death) — DROD RPG 2008, HP і спорядження, ключі замість старих умов дверей.
- [GitHub CaravelGames/drod](https://github.com/CaravelGames/drod) — відкритий код; `drodrpg/DRODLib/Combat.cpp` (тіки, ініціатива, подвоєння, прогноз), `CurrentGame.cpp` (рахунок, двері, лопати, обмін спорядженням, undo), `TileConstants.h` (усі клітини).
- Довідка гри `drodrpg/Data/Help/1/`: [elements](https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/elements.html), [equipment](https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/equipment.html), [monster](https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/monster.html), [hints](https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/hints.html), [keyboard](https://raw.githubusercontent.com/CaravelGames/drod/master/drodrpg/Data/Help/1/keyboard.html).
- YouTube: пошук «DROD RPG Tendry's Tale gameplay».

## Непевне
- (?) Розмір кімнати 38×32 — перенесено з DROD; для RPG не перевірено.
- (?) Які саме монстри ходять: у коді тарган без логіки руху, гоблін лише розвертається; мімік повторює рухи; темп кладки яєць королевою не перевірено.
- (?) Ціна грекльової брами: довідка каже 10 GR, код бере значення рівня (`getItemAmount`) — у холдах може відрізнятися; так само множники зіль/кристалів.
- (?) Backstab (×2 ATK першим ударом ззаду) — властивість певної зброї чи загальне правило: у коді — `DoesPlayerBackstab()`, деталі не дочитано.
- (?) Чи відрізняється в RPG 2 щось у формулі бою — Steam описує лише нові вміст і складність.
- (?) Рік: черга вказує 2016 — це реліз у Steam; оригінал — 2008 (Wikipedia).
