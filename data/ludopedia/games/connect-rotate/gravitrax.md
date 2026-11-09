---
title: GraviTrax (+ THE GAME)
slug: gravitrax
aka: [Gravitrax, GraviTrax PRO, GraviTrax POWER, GraviTrax THE GAME]
family: connect-rotate
also: [build-sim, thinky]
klass: puzzle
axes:
  field: hex
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [toy, mobile]
links:
  - {kind: other, url: "https://www.zeuthen.desy.de/~friebel/gravitemp/gravi_en.pdf", best: true, note: "W. Friebel: нотація трас — базова плита на 27 гексів, висоти, усі елементи з символами й орієнтаціями a–f, рейки, прозорі рівні, кульки, розширення, програма-перевірка gravi"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/GraviTrax", note: "Ravensburger 2017, лінії Core / PRO (2020) / POWER (2022), 22 action-елементи, застосунок, нагорода TOMMI 2019"}
  - {kind: official, url: "https://www.ravensburger.de/de-DE/entdecken/gravitrax/gravitrax-the-game-tutorial", note: "THE GAME: 5 кроків розвʼязку картки-завдання, підказки на звороті, розвʼязки 1–28, 29–30 відкриті"}
  - {kind: official, url: "https://ravensburger-en.mindtouch.us/Product_Information/Ravensburger/GraviTrax/GraviTrax_Game", note: "видання THE GAME: Flow, Impact, Course, PRO Splitter"}
  - {kind: other, url: "https://github.com/wofr06/marblerun", note: "Perl-модуль Game::MarbleRun: таблиця входів/виходів кожного елемента, стани перемикача"}
  - {kind: other, url: "https://officialgamerules.org/game-rules/gravitrax/", note: "огляд: складання, тестові запуски, картки-завдання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=GraviTrax+challenge", note: "пошук; траси й завдання"}
stage: v1
coverage: 60
mechanics: [pipe-connectors, tile-rotate, height-levels, gravity-fall, button-toggle, connectivity-check, satisfy-constraints, level-bank, sequential-levels, state-string, level-from-txt, map-validation, in-game-editor, editor-palette, editor-playtest, level-exchange, movement-animation, game-screen, help-window, editor-window, +marble-routing, +junction-toggle, +height-stack, +gauss-cannon, +build-then-run, +parts-inventory, +challenge-card-setup]
proposes: ["+cond:height_diff", "+effect:launch", "+trigger:ball_lands", "+feature:parts-inventory", "+card:gauss-cannon", "+card:height-stack", "+card:challenge-card-setup"]
author: opus
date: 2026-11-09
---

# GraviTrax — будуєш кулькову трасу з гекс-плиток на стопках висоти, зʼєднуєш їх рейками, і кулька сама проходить «програму» перемикачів, падінь і гармат

## Суть
Конструктор Ravensburger (2017): на базових плитах із гекс-гніздами ставлять стовпчики висоти, на них — плитки-елементи (крива, перехрестя, перемикач, магнітна гармата, вихор, вільне падіння…), а сусідні плитки зʼєднують рейками. Потім кулька стартує й, підкоряючись лише гравітації, проходить трасу: шлях задано орієнтацією плиток (6 поворотів), висотами і станами перемикачів. **GraviTrax THE GAME** перетворює конструктор на соло-пазл: картка задає плиту, позиції старту й фінішу (з висотами) і набір дозволених елементів — треба скласти трасу, якою кулька дійде до фінішу. Сіткова суть — граф зʼєднань на гекс-полі з третьою координатою-висотою.

## Поле і час
- Базова плита: 6 стовпців гекс-гнізд по 5/4/5/4/5/4 — разом 27; плити стикуються в прямокутник (або будь-яку фігуру з пропусками), половинки гексів на краях двох плит утворюють спільне гніздо.
- Третя вимірність — висота: велика сіра плитка = 1 одиниця, мала чорна = ½; стовпчики складаються довільно; колона (PRO/vertical) = 7 одиниць; прозорий рівень (на 3 стовпчиках) має власні позиції — «поверх» поля; є й малий прозорий рівень.
- Орієнтація кожної плитки — 6 напрямків (a–f, як сторони гекса); рейка теж має напрям a–f і довжину (коротка / середня / довга, мости, наддовгі).
- Час: фаза будування статична; запуск — фізичний real-time, але детермінований: кулька виконує «програму» траси (`time: programmed`). Тест-запуски повторювані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Базова плита | static | 27 гнізд | поле; плити стикуються |
| Плитка висоти (велика / мала) | terrain | 1 / ½ одиниці | стопкою піднімає плитку-елемент |
| Колона / тунельна колона | terrain | 7 одиниць; тунельна має отвір | висота; тримає прозорі стінки з балконами (vertical / PRO) |
| Прозорий рівень (великий / малий) | terrain | на 3 стовпчиках, висота як ½ | другий шар поля з власними гніздами |
| Старт (Launch Pad) | source | до 3 кульок | важіль випускає кульки по одній |
| Крива | conduit | 2 дуги (тісна й широка) | веде кульку між двома суміжними парами сторін |
| Перехрестя (Junction) | conduit | 2 прямі шляхи навхрест | кулька йде прямо, шляхи не взаємодіють |
| 2 в 1 / 3 в 1 | conduit | 2 або 3 входи, 1 вихід | зводить потоки в один; у зворотний бік «непередбачувано» |
| Перемикач (Switch) | switch | гойдалка +/− | кулька зі «стовбура» йде в одну з двох гілок і перекидає гойдалку → наступна йде в іншу |
| Магнітна гармата | object | заряджена кульками | вхідна кулька бʼє в магніт — кулька з іншого боку вилітає швидко (gauss) |
| Вільне падіння (Freefall) | conduit | — | кулька падає крізь отвір униз |
| Ловець (Catcher) | conduit | — | ловить кульку, що падає згори, і випускає в рейку |
| Вихор (Vortex) | conduit | 1–2 входи | кулька кружляє й падає крізь центр на плитку нижче |
| Splash | object | кульки поверх | кулька згори розкидає покладені кульки у виходи |
| Посадка (Landing) / фінішна рейка | sink | — | кулька зупиняється — кінець траси |
| Рейка | conduit | довжина s/m/l, напрям a–f | зʼєднує дві плитки; має спадати вниз |
| Кулька | object | колір R/G/B/срібна/золота | котиться під гравітацією; єдиний «виконавець» траси |
| Розширення Core | object | Flip, Hammer, Jumper, Cascade, Catapult, Tiptube, Volcano, Looping, Transfer, Dipper, Spinner, Color Swap, Spiral, Lift, Zipline, Flextube, Trampoline, Bridge, Tunnel | кожне — своє правило входу/виходу (див. нижче вибрані) |
| Color Swap | container | 1 кулька всередині | нова кулька лишається, а та, що була, їде далі |
| Dipper / Tunnel switch | switch | гойдалка +/− | як перемикач |
| Міст (Bridge) | gate | 2 кульки-противаги, розкладні секції | секції розкладаються під вагою; лише тоді кулька проходить (6 секцій) |
| Ліфт / Спіраль | conduit | висота = кількість секцій | підіймає / опускає кульку на задану висоту |
| Батут | object | 0–2 похилі підставки | відбиває кульку; напрям — від нахилу |
| PRO: Mixer, Splitter, Helix, Turntable, Carousel | switch | поворотні частини | напрям виходу залежить від стану рухомої деталі |

## Правила (КОЛИ → ЯКЩО → ТО)
- Будування: КОЛИ `input(place, height_tile, cell)` → ТО `custom: «висота стовпчика += 1 або ½»` (стовпчик з колон — +7).
- КОЛИ `input(place, tile, cell, dir)` → ЯКЩО `free(cell)` → ТО `place(p, tile)`, `face(tile, dir)` — одна з 6 орієнтацій.
- КОЛИ `input(place, rail, tile_a, dir)` → ЯКЩО `custom: «на відстані довжини рейки в напрямку dir стоїть плитка з входом назустріч»` and `custom: «перепад висот підходить цій рейці»` (+cond:height_diff) → ТО `place(p, rail)`; інакше `block`.
- THE GAME, старт: КОЛИ `level_start` → ТО `custom: «плиту орієнтовано як на картці»`, `place(start, cell)`, `place(finish, cell)` з указаними висотами; `custom: «доступні лише елементи з картки»`.
- Запуск: КОЛИ `input(release, launch_pad)` → ТО `move(ball, start_exit)` — одна кулька з указаного виходу.
- КОЛИ `enter(ball, rail)` → ТО `move(ball, rail_end)` — униз за нахилом.
- КОЛИ `enter(ball, curve|junction|2in1)` → ТО `move(ball, exit)` — вихід визначено входом і орієнтацією плитки.
- КОЛИ `enter(ball, switch)` → ЯКЩО `state(switch, minus)` → ТО `move(ball, exit_left)`, `set_state(switch, plus)`; інакше `move(ball, exit_right)`, `set_state(switch, minus)` — потік кульок чергується.
- КОЛИ `enter(ball, switch)` з гілки → ЯКЩО `custom: «гойдалка відкрита до цієї гілки»` → ТО `move(ball, stem)`, `set_state(switch, flip)`; інакше `block` — кулька застрягає.
- КОЛИ `enter(ball, freefall)` → ТО `fall(ball)` крізь отвір; КОЛИ `custom: «кулька впала згори в ловця»` (+trigger:ball_lands) → ТО `move(ball, catcher_exit)`.
- КОЛИ `enter(ball, vortex)` → ТО `custom: «кружляє»`, `fall(ball)` крізь центр на плитку нижче.
- КОЛИ `enter(ball, magnetic_cannon)` → ЯКЩО `has(cannon, loaded_balls)` → ТО `custom: «вхідна кулька зупиняється біля магніту, крайня кулька з протилежного боку вилітає»` (+effect:launch); інакше `custom: «кулька прилипає й заряджає гармату»` (?).
- КОЛИ `custom: «кулька впала на Splash»` → ТО `custom: «покладені на Splash кульки розкочуються у виходи»`.
- КОЛИ `enter(ball, color_swap)` → ЯКЩО `occupied(color_swap, ball)` → ТО `custom: «нова лишається, стара виходить»`; інакше `custom: «кулька лишається всередині»`.
- КОЛИ `enter(ball, trampoline)` → ТО `bounce(ball)` у напрямку нахилу підставок.
- КОЛИ `reach(ball, landing|finish_line)` → ТО `custom: «кулька зупинилась»`; THE GAME: ЯКЩО `custom: «усі елементи з картки вбудовано»` → ТО `win`.
- КОЛИ `custom: «кулька злетіла з траси / застрягла / не дійшла»` → ТО `custom: «завдання не розвʼязане — перебудувати й запустити знову»` (`restart`).
- Перемога (THE GAME): кулька від старту до фінішу з дозволеним набором елементів · Поразка: нема, лише нова спроба · Рахунку нема; у вільному будуванні мети нема.

## Керування і ввід
- Фізично: ставити стовпчики й плитки в гнізда, повертати плитку на 60°, чіпляти рейки між плитками, виставляти гойдалки перемикачів у потрібне положення, заряджати гармату, натискати важіль старту.
- Застосунок (iOS/Android): проєктувати трасу віртуально, потім відтворити її з деталей; траси можна відправити на сервер і завантажити чужі.
- Нотація Friebel: траса як текст «позиція висота Символ орієнтація рейка-напрям», напр. `43 5Ac sc` (старт на 5 висотах, орієнтація c, коротка рейка в напрямку c).

## Вікна, меню, HUD
- (застосунок, деталі не бачив) `main-menu` → `editor-window`: палітра елементів, 3D-поле з плитами, симуляція кульки; бібліотека трас (свої / спільноти) — `level-select` (?).
- (THE GAME, цифрова версія) `puzzle-select` — 30 карток-завдань; `game-screen`: плита, зафіксовані старт і фініш, `inventory-bar` дозволених елементів, кнопка «запустити кульку»; `hints-window` — підказка зі звороту картки; `solutions-window` — розвʼязок з буклета (1–28).
- (gravi, консоль) список трас з позначкою «маєш усі деталі» (OK Y/N), інструкція збирання, SVG-малюнок траси з анімацією.

## Фічі поза полем
- `level-bank`: книжечки трас у наборах; THE GAME — 30 завдань у порядку складності, підказки на звороті карток, розвʼязки 1–28, 29–30 — відкриті (#GraviTraxTHEGAME30).
- Видання THE GAME: Flow (flextube + малий прозорий рівень), Impact (молот), Course (спецкриві + друга кулька), PRO Splitter, Multiform; адвент-календар (завдання + 1–2 картки-підказки + картка розвʼязку).
- `level-editor` / `level-sharing`: застосунок; нотація як `export-import`; gravi перевіряє, що плитки й рейки сходяться, малює схему й рахує, чи вистачає деталей у власних наборах (+feature:parts-inventory).
- Лінії сумісні: Core (білі основи), PRO (2020, стіни й балкони), POWER (2022, електроніка, електроліфт; Bluetooth-блок Connect з відкритою Python-бібліотекою).

## Варіації й родичі
- Родичі в корпусі: [marble-drop](marble-drop.md) (маршрутизація кульок перемикачами), [logical](logical.md), [cogs](cogs.md), [pipe-mania](pipe-mania.md) (труби як зʼєднання), [trainyard](trainyard.md) (траса виконується як програма); Turing Tumble, Rube Goldberg-пазли.
- Осі варіацій:
  - **поле**: плоска сітка / гекс із висотами (GraviTrax) / вертикальна дошка (Marble Drop);
  - **стан елементів**: без станів / перемикач-гойдалка, що чергує виходи / контейнери (Color Swap, Tiptube);
  - **енергія**: лише гравітація / гармата-гаусс, батут, катапульта / електроліфт (POWER);
  - **мета**: пісочниця / картка-завдання «старт → фініш з даним набором» (THE GAME).

## Цікавинки для курсу
- Гекс-поле з 6 орієнтаціями і таблицею «вхід → вихід» для кожного типу плитки (дані з Game::MarbleRun) — 📎.
- Висота як третя координата: рейка лише вниз, перевірка перепаду за довжиною — 📎.
- Перемикач-гойдалка як 1-бітовий стан: потік кульок розподіляється по черзі (бінарний лічильник із кількох перемикачів) — 🥉.
- Симуляція кількох кульок з контейнерами (Color Swap, гармата, Splash) у дискретних тіках — 🥈.
- Текстова нотація траси + валідатор «усі рейки сходяться» + рендер SVG — 🥉.
- Розвʼязувач THE GAME: перебір розміщень дозволених плиток з орієнтаціями й висотами, поки кулька не дійде до фінішу — 🥇.

## Мапа на каталог
- Є: `pipe-connectors` ↔ плитки з входами/виходами; `tile-rotate` ↔ орієнтації a–f; `height-levels` ↔ стовпчики висоти; `gravity-fall` ↔ рух кульки, Freefall; `button-toggle` ↔ гойдалка перемикача; `connectivity-check` ↔ неперервна траса старт → фініш; `satisfy-constraints` ↔ лише дозволені елементи; `level-bank` + `sequential-levels` ↔ 30 завдань; `state-string` + `level-from-txt` ↔ нотація Friebel; `map-validation` ↔ gravi перевіряє, що рейки й плитки сходяться; `in-game-editor` + `editor-palette` + `editor-playtest` + `level-exchange` ↔ застосунок; `movement-animation` ↔ анімація SVG; `game-screen` · `help-window` · `editor-window`.
- **Нема** → пропозиції карток:
  - `+marble-routing` (Marble Drop) — кулька як виконавець траси.
  - `+junction-toggle` (Marble Drop) — перемикач чергує виходи.
  - `+height-stack` «Стовпчик висоти під плиткою, рейка лише вниз» · entities/legality · 📎.
  - `+gauss-cannon` «Удар кульки вибиває іншу з протилежного боку» · entities/interact · 📎.
  - `+build-then-run` «Збудував — запустив — подивився; повтор без штрафу» · game-logic · 🌱.
  - `+parts-inventory` «Обмежений набір деталей; перевірка, чи вистачає на трасу» · levels/format · 📎.
  - `+challenge-card-setup` «Завдання = фіксовані старт/фініш + дозволені деталі» · levels/bank · 🌱.

## Пропозиції до словників
- `+cond:height_diff` — перепад висот між плитками підходить рейці.
- `+effect:launch` — сутність вилітає з великою швидкістю (гармата, катапульта).
- `+trigger:ball_lands` — кулька впала згори на плитку.
- `+feature:parts-inventory` — облік наявних наборів і деталей.
- `+card:gauss-cannon` · `+card:height-stack` · `+card:challenge-card-setup`.

## Джерела
- ⭐ [W. Friebel: Notation of building instructions (PDF)](https://www.zeuthen.desy.de/~friebel/gravitemp/gravi_en.pdf) — геометрія плити (27 гнізд, стикування), висоти (1, ½, колона 7), усі плитки й рейки з символами, орієнтації a–f, гойдалка +/−, прозорі рівні, кульки (до 3 на старті, до 6 на Spinner), розширення Core/PRO, Color Swap, Bridge, програма gravi.
- [Wikipedia DE: GraviTrax](https://de.wikipedia.org/wiki/GraviTrax) — Ravensburger 2017, Core/PRO/POWER, 22 action-елементи (17 Core + 5 PRO, 2023), застосунок, Python-бібліотека, TOMMI 2019.
- [Ravensburger: THE GAME Tutorial](https://www.ravensburger.de/de-DE/entdecken/gravitrax/gravitrax-the-game-tutorial) — що на картці, 5 кроків, підказки, розвʼязки 1–28, видання.
- [Ravensburger Help: GraviTrax Game](https://ravensburger-en.mindtouch.us/Product_Information/Ravensburger/GraviTrax/GraviTrax_Game) — Flow, Impact, Course, PRO Splitter.
- [GitHub: wofr06/marblerun](https://github.com/wofr06/marblerun) — `MarbleRun.pm`: таблиця «символ, вхід, вихід, висоти, умова-стан → новий стан» для Curve, Switch, Junction, 2in1, Cannon, Catcher, Freefall, Splash, Vortex, Landing.
- [officialgamerules.org: GraviTrax](https://officialgamerules.org/game-rules/gravitrax/) — загальний порядок складання й тест-запусків.

## Непевне
- (?) Точна фізика магнітної гармати (скільки кульок заряджати, що з вхідною кулькою) — з кодової таблиці й памʼяті, не з інструкції.
- (?) Splash: які саме виходи отримують кульки — у таблиці 0/2/4, з інструкцією не звірено.
- (?) Максимальний перепад висот для кожної рейки — у коді є колонки z_min/z_max, але для перевірки не використовуються; чисел не наводжу.
- (?) Інтерфейс застосунку (меню, бібліотека, симуляція) — не бачив, вікна описані як припущення.
- (?) Чи THE GAME вимагає використати **всі** показані елементи: туторіал каже «лише показані елементи мають бути вбудовані» — трактовано як «усі показані й лише вони».
