---
title: Robot Odyssey
slug: robot-odyssey
family: program-robots
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 1984
platforms: [Apple II, MS-DOS, TRS-80 CoCo, web (Robot Odyssey Rewired), Java (DroidQuest)]
links:
  - {kind: play, url: "https://robotodyssey.online/", best: true, note: "Robot Odyssey Rewired — грати в браузері: туторіали Robot Anatomy/Wiring/Sensors/Chip Design, лабораторія, швидкість симуляції"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Robot_Odyssey", note: "історія, роботи Sparky/Checkers/Scanner, частини робота, чипи, Innovation Lab"}
  - {kind: other, url: "https://scanlime.org/2009/04/robot-odyssey-chip-disassembler/", note: "як влаштований чип: 8 пінів, байткод AND/OR/XOR/NOT/RS-тригер, вкладені чипи, такт"}
  - {kind: other, url: "https://scanlime.org/2009/04/a-binary-patch-for-robot-odyssey/", note: "патч DOS-версії; копізахист вимикав паяльник"}
  - {kind: other, url: "https://github.com/ThomasFooteDQ/DroidQuest", note: "DroidQuest — Java-клон з усіма рівнями; клавіші, код пристроїв"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rocky%27s_Boots", note: "попередник 1982: ті самі вентилі й «помаранчевий струм»"}
  - {kind: play, url: "https://archive.org/details/msdos_Robot_Odyssey_1985", note: "DOS-версія в емуляторі Internet Archive"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robot+odyssey+1984+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [impassable-cells, key-and-door, item-pickup, sequential-levels, save-game, game-screen, main-menu, help-window, level-exchange, state-as-data, enemy-patrol, +logic-circuit-wiring, +flip-flop-memory, +nested-chips, +chip-burning, +sensor-bumpers, +thruster-propulsion, +grabber-carry, +shared-radio-channel, +robot-ride-inside, +swarm-separate-programs, +signal-visualization, +simulation-speed, +sandbox-lab, +battery-charge, +step-execution]
proposes: ["+trigger:signal_rise(pin)", "+trigger:exec(cmd)", "+cond:signal(pin)", "+effect:emit(pin, v)", "+effect:carry", "+effect:enter_container(a, b)", "+role:circuit-part", "+role:sensor", "+role:actuator", "+role:container", "+window:circuit-interior", "+window:chip-lab", "+ui:signal-color", "+ui:speed-slider", "+feature:simulation-speed", "+feature:chip-library", "+axis:control", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Robot Odyssey — роботи, яких «програмуєш» паяльником: вентилі й тригери всередині корпусу

## Суть
Гравець провалився в підземне місто роботів Robotropolis і має вибратися нагору через пʼять рівнів. Сам він майже нічого не може: проходи відкривають три роботи (Sparky, Checkers, Scanner; пізніше — четвертий), усередині яких гравець **паяє схему** — дроти від бамперів-сенсорів через вентилі AND/OR/XOR/NOT і RS-тригери до рушіїв, захвату й антени. Робот потім діє автономно за цією схемою: обходить стіни, носить предмети, перемовляється радіо з іншими. Ядро — синхронна цифрова логіка як мова програмування; повторювані схеми «пропалюються» в 8-пінові чипи й вкладаються одна в одну.

## Поле і час
- Світ — граф кімнат (вихід за край кімнати → сусідня кімната); кімната — плиткова сітка, у DroidQuest 20×12 клітин матеріалу. Рух сутностей — дрібними кроками (8 пікселів), а не на цілу клітину, тому «клітинність» — у стінах і розкладці, а не в позиціях (?).
- **Два масштаби поля**: кімната міста і **нутрощі робота** — окрема кімната 20×12 зі стінами кольору робота, пінами сенсорів/рушіїв на стінах, батареєю, перископом і вимикачем. Гравець ходить і там, і там.
- Час: реальний, але логіка — `programmed`: на кожен такт симулятор раз проходить байткод кожного чипа й поширює сигнали дротами; рушії рухають робота, доки на них 1. Кожна межа вкладеного чипа додає один такт затримки.
- Видимість — одна кімната на екрані; зсередини робота зовнішній світ видно лише через перископ (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (курсор-аватар) | player | несе 1 предмет | ходить кімнатами, підбирає/кладе предмети й деталі, паяє дроти, заходить у роботів |
| Робот (Sparky / Checkers / Scanner / 4-й) | ally | колір, заряд батареї, вимикач, напрям захвату | рухається й діє лише за своєю схемою; усі три однакові всередині |
| Рушій (thruster) ×4 | actuator | сторона N/E/S/W | вхід = 1 → робот зсувається в протилежний бік; витрачає заряд |
| Бампер ×4 | sensor | сторона | вихід = 1, поки сторона робота торкається стіни/обʼєкта |
| Захват (grabber) | actuator | одна з 4 сторін | вхід = 1 → тримає предмет поруч; 0 → відпускає; іншого робота не бере |
| Антена | sensor + actuator | вхід transmit, вихід receive | будь-яка антена-передавач вмикає прийом на **всіх** антенах роботів (спільний канал) |
| Батарея | resource | заряд | рушії витрачають заряд; 0 → робот стоїть (?) |
| Перископ | static | — | вид назовні, коли гравець усередині |
| Вимикач живлення | switch | on/off | без живлення схема не працює |
| Дріт | conduit | стан 0/1 | несе сигнал від виходу до входу; помаранчевий = 1, білий = 0 |
| Вузол (node) | conduit | — | розгалужує один сигнал на кілька дротів |
| AND · OR · XOR | circuit-part | 2 входи, 1 вихід | логічна функція щотакту |
| NOT | circuit-part | 1 вхід | інверсія |
| RS-тригер (flip-flop) | circuit-part | стан 01/10 | памʼять 1 біт; у чипах не перемикається при обох входах = 1 |
| Малий чип | circuit-part | 8 пінів (вхід/вихід), текст-опис, швидкість | готова схема; знайдений у місті (обхід стіни, годинник, лічильник) або пропалений гравцем |
| Прототип-чип (лабораторія) | container | 8 пінів, нутрощі-кімната | схема всередині збирається як у роботі; потім пропалюється в малий чип |
| Пропалювач (burner) | switch | — | прототип/чип на ньому → запис схеми в малий чип (стирає старий вміст) |
| Ящик з інструментами (toolkit) | spawner | — | видає нові вентилі, тригери, вузли, чипи (?) |
| Паяльник (solder pen) | — (інструмент) | — | режим вводу: тягнути дріт від піна до піна |
| Ключі, кристали, жетони | pickup | колір/тип | відкривають двері, живлять механізми; роботи можуть їх носити (?) |
| Двері / замки | gate | ключ | пропускають гравця/робота з потрібним ключем (?) |
| Вартові (sentries) | enemy | маршрут | блокують прохід, відкидають гравця, якщо той несе певний предмет (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «кожен чип раз виконує свій байткод; виходи вентилів поширюються дротами»`; межа вкладеного чипа → +1 такт затримки.
- КОЛИ `contact(robot_side, wall|object)` → ТО `emit(bumper[side], 1)`; відрив → `emit(bumper[side], 0)`.
- КОЛИ `tick` → ЯКЩО `signal(thruster[side])` and `state(robot, powered)` and `has(robot, charge)` → ТО `move(robot, opposite(side))`, `counter(charge, -n)`.
- Два протилежні рушії одночасно → рухи компенсуються (?); два суміжні → рух по діагоналі (?).
- КОЛИ `signal_rise(grabber)` → ЯКЩО `occupied(grabber_side, item)` → ТО `carry`; КОЛИ сигнал падає → ТО `custom: «відпустити предмет»`.
- КОЛИ `signal(antenna_in)` у будь-якого робота → ТО `emit(antenna_out, 1)` у всіх роботів (спільний канал); окремий канал — для антен поза роботами (DroidQuest).
- КОЛИ `signal(flipflop.S)` → ТО `set_state(ff, 1)`; `signal(flipflop.R)` → ТО `set_state(ff, 0)`; обидва = 1 у чипі → `custom: «стан не змінюється»`.
- КОЛИ `input(enter, robot)` → ТО `enter_container(player, robot)`: гравець у нутрощах, робот може везти його (`carry`) на свою схему.
- КОЛИ `input(drop, chip, burner)` → ТО `custom: «схема прототипу записується в малий чип»`; завантаження чипа з файла стирає попередню схему.
- КОЛИ `input(solder, pin_a, pin_b)` → ТО `custom: «створити дріт»`; вхід можна зʼєднати лише з виходом (?).
- КОЛИ `contact(player, key_door)` → ЯКЩО `has(player|robot, key)` → ТО `disappear_b`; інакше `block` (?).
- КОЛИ `reach(player, room_exit_of_level)` → ТО `next_level` (вихід на рівень вище).
- Перемога: вибратися з Robotropolis нагору (пройти всі пʼять рівнів) · Поразка: явної нема — «застряг» означає перебудувати схему (?) · Рахунку нема.
- Більшість задач розраховані на **автономну** роботу робота без гравця всередині: пройти лабіринт за допомогою чипа wall-hugger, пролетіти повз вартового в потрібний момент, синхронізувати двох роботів антеною.

## Керування і ввід
- Клавіатура: стрілки — рух гравця (Ctrl+стрілки — точний рух); пробіл — взяти/покласти; `[`/`]` — повернути пристрій; `F` — віддзеркалити; `S` — паяльник; `T` — ящик інструментів; `L` — завантажити малий чип з файла; `R` — вмикач радіо (пульт); `E`/`X` — увійти/вийти з робота; `C` — ігровий курсор; `/` — довідка (розкладка DroidQuest; оригінал схожий (?)).
- Режим паяльника: «взяти» паяльник, підвести до піна, тягнути дріт до іншого піна; повторне торкання — видалити дріт (?).
- Програмування = фізичне розставлення деталей у кімнаті-нутрощах і паяння; нема тексту, нема блоків.
- Rewired: перемикач швидкості симуляції Paused · ⅛× … 200×.

## Вікна, меню, HUD
- `main-menu` (Rewired): New Game · New Lab · Saved Games · Saved Labs · Replace Chip · File Import/Export · Copy URL · Fullscreen · палітра (Rewired / Apple ][ / DOS / CGA).
- `mode-select`: Robotropolis (гра) · Innovation Lab (лабораторія) · Odyssey Training — серія туторіалів: Robot Anatomy · Robot Wiring · Sensors · The Toolkit · Robot Circuits · Robot Teamwork · Chip Design.
- `game-screen`: поточна кімната міста; сигнали видно кольором дротів і частин (помаранчевий = 1).
- `circuit-interior` — нутрощі робота як окрема кімната: піни бамперів/рушіїв/захвату/антени на стінах, батарея, вимикач, перископ.
- `chip-lab` — Innovation Lab: прототип-чип з кімнатою всередині, пропалювач, тестер, смітник.
- `help-window`: текст-опис чипа (пінаут) — часто загадковий; гравець вгадує поведінку експериментом.
- HUD: `speed-slider` (Rewired), `signal-color` (стан кожного дроту видно на полі).
- Переходи: меню → місто/лабораторія/туторіал; кімната → (E) нутрощі робота → (X) кімната; лабораторія → Save chip → файл → (L) у грі.

## Фічі поза полем
- `save-slots` (Saved Games, Saved Labs), `export-import` чипів як файлів (CSV-подібний формат 1333 байти: стани пінів, байткод, напрямки пінів, опис).
- `chip-library`: готові чипи на дисках гри (набір залежить від версії) завантажуються в будь-який чип.
- `mode-sandbox` (Innovation Lab) і `tutorial` (п'ять навчальних кімнат + Odyssey Training).
- `simulation-speed` (Rewired) — від паузи до 200×; `share-code` (Copy URL) (?).
- Копізахист оригіналу вимикав паяльник — гра «працювала», але без пайки (цікавий приклад «тихої» деградації).

## Варіації й родичі
- Rocky's Boots (1982) — та сама команда й рушій (Warren Robinett, Leslie Grimm), вентилі й «помаранчевий струм», бутс штовхає обʼєкти з конвеєра. Gertrude's Secrets/Puzzles, Think Quick! — легші ігри на тому ж рушії.
- GATE — духовний наступник (Windows/macOS); DroidQuest — Java-клон з усіма рівнями + секретний; Robot Odyssey Rewired — браузерна версія з сучасним меню.
- Сучасні родичі за ідеєю «схема = програма»: TIS-100, Shenzhen I/O, Turing Complete, Logic World (?).
- Осі варіацій: **мова** (вентилі й тригери / текст / блоки); **де живе програма** (на окремому екрані / у кімнаті-нутрощах, куди заходить аватар); **абстракція** (лише вентилі / вкладені чипи); **комунікація ботів** (нема / спільний радіоканал / адресні повідомлення).

## Цікавинки для курсу
- Симулятор синхронної логіки на сітці: дроти, AND/OR/XOR/NOT, RS-тригер, такт — 🥇 (топологічний порядок/затримки, памʼять, цикли зворотного звʼязку).
- Робот із сенсорами-бамперами й рушіями, керований такою схемою (обхід стіни праворуч з двох вентилів) — 🥈.
- «Пропалювання» схеми в чип з 8 пінами і вкладення чипів (+1 такт на межі) — 🥇: абстракція як у функцій.
- Кімната всередині обʼєкта: аватар заходить у робота, робот везе його світом — 🥉 (два масштаби поля, портал-сутність).
- Спільний радіоканал «хтось передає → усі чують» для синхронізації кількох роботів — 📎.
- Збереження чипа у файл + загадковий текст-опис, поведінку якого гравець перевіряє експериментом — 🥉.
- Швидкість симуляції від паузи до 200× — 📎.

## Мапа на каталог
- Є: `impassable-cells` (стіни кімнат) · `key-and-door` (?) · `item-pickup` (гравець/захват носить предмети) · `sequential-levels` (п'ять рівнів міста) · `save-game` (Saved Games/Labs) · `level-exchange` + `state-as-data` (чип як файл) · `enemy-patrol` (вартові (?)) · `game-screen` · `main-menu` · `help-window`.
- **Нема** → пропозиції карток:
  - `+logic-circuit-wiring` «Схема з вентилів і дротів керує сутністю» · game-logic · 🥇 · слоти {gates: and|or|xor|not, wires}.
  - `+flip-flop-memory` «Тригер як памʼять 1 біт» · entities/state · 🥉.
  - `+nested-chips` «Вкладені чипи з пінами й затримкою на межі» · game-logic · 🥇.
  - `+chip-burning` «Зберегти схему як компонент» · levels/editor · 🥈 — схема → чип, чип → файл.
  - `+sensor-bumpers` «Сенсор дотику з кожного боку» · entities/state · 📎 (дитина `+sensor-predicates`).
  - `+thruster-propulsion` «Рушій штовхає в протилежний бік» · entities/move · 📎.
  - `+grabber-carry` «Захват: тримати, доки сигнал» · entities/interact · 📎.
  - `+shared-radio-channel` «Спільний радіоканал між ботами» · game-logic · 📎.
  - `+robot-ride-inside` «Аватар усередині сутності; кімната-нутрощі» · entities/interact · 🥉.
  - `+swarm-separate-programs` (є пропозиція з Opus Magnum) — у кожного робота своя схема.
  - `+signal-visualization` «Стан дротів кольором» · interface/graphics · 📎.
  - `+simulation-speed` «Пауза…200× для симуляції» · interface/input · 📎.
  - `+sandbox-lab` «Лабораторія без цілі для прототипів» · levels · 🥉.
  - `+battery-charge` «Заряд, що витрачають дії» · entities/state · 🌱.
  - `+step-execution` — пауза/повільна швидкість як покрокове виконання.

## Пропозиції до словників
- `+trigger:signal_rise(pin)` — сигнал на піні змінився 0→1 (захват, антена, лічильник); `+trigger:exec(cmd)` — спільний для сімʼї (тут «такт схеми»).
- `+cond:signal(pin)` — на піні/дроті зараз 1.
- `+effect:emit(pin, v)` — сенсор/вентиль виставляє сигнал; `+effect:carry` — є в 🔥-списку (нести на собі); `+effect:enter_container(a, b)` — A входить у нутрощі B (кімната всередині сутності).
- `+role:circuit-part` (вентиль, тригер, чип), `+role:sensor` (бампер, приймач), `+role:actuator` (рушій, захват, передавач); `+role:container` — уже ⏳, тут робот-кімната; `conduit` 🔥 — дріт, вузол.
- `+window:circuit-interior` — нутрощі сутності як окреме поле; `+window:chip-lab` — лабораторія прототипів.
- `+ui:signal-color` — колір дроту = значення; `+ui:speed-slider` — пропонувався в Manufactoria.
- `+feature:simulation-speed` — множник швидкості симуляції; `+feature:chip-library` — бібліотека готових компонентів з диска.
- `+axis:control` — `programmed` (схема), гравець при цьому — `direct`-аватар; `+axis:actors` — `party` (три роботи, кожен зі своєю схемою).

## Джерела
- ⭐ [Robot Odyssey Rewired](https://robotodyssey.online/) — грати одразу; туторіали Robot Anatomy, Wiring, Sensors, Toolkit, Circuits, Teamwork, Chip Design; швидкість симуляції.
- [Wikipedia: Robot Odyssey](https://en.wikipedia.org/wiki/Robot_Odyssey) — 1984, The Learning Company, Wallace & Grimm, рушій Robinett-а; роботи й частини; чипи й Innovation Lab; GATE, DroidQuest.
- [scanlime: chip disassembler](https://scanlime.org/2009/04/robot-odyssey-chip-disassembler/) — 8 пінів, AND/OR/XOR/NOT/RS-тригер, вкладені чипи, такт і затримка.
- [scanlime: binary patch](https://scanlime.org/2009/04/a-binary-patch-for-robot-odyssey/) — копізахист і паяльник, 8 FPS.
- [DroidQuest (GitHub)](https://github.com/ThomasFooteDQ/DroidQuest) — клавіші; код пристроїв (Thruster, Bumper, Grabber, Antenna, FlipFlop, Node, PrototypeChip, Burner).
- [Wikipedia: Rocky's Boots](https://en.wikipedia.org/wiki/Rocky%27s_Boots) — попередник, помаранчевий/білий = 1/0.
- [Internet Archive: DOS-версія](https://archive.org/details/msdos_Robot_Odyssey_1985) — оригінал в емуляторі.
- YouTube: пошук «robot odyssey 1984 gameplay».

## Непевне
- (?) Назви п'яти рівнів міста (Sewer, Subway, Town, Skyways, Master Control) — з памʼяті; Wikipedia їх не наводить.
- (?) Поведінка вартових, кристалів, ключів і дверей — лише з назв класів DroidQuest (Sentry, Crystal, Key, SonicLock); деталей не читав.
- (?) Комбінації рушіїв (протилежні/суміжні) і наслідок нульового заряду — у коді DroidQuest видно лише окремі зсуви й витрату заряду.
- (?) Чи може гравець «загинути» і чи є поразка взагалі — не знайшов.
- (?) Розміри кімнат 20×12 і крок 8 пікселів — з коду DroidQuest, не з оригіналу.
- (?) Клавіші оригіналу можуть відрізнятися від DroidQuest; правила пайки (вхід лише до виходу) — з памʼяті.
