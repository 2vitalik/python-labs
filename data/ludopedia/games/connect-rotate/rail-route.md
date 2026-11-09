---
title: Rail Route
slug: rail-route
aka: [Rail Route — The Train Dispatcher Simulator]
family: connect-rotate
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: score
year: 2024
platforms: [PC (Windows, macOS, Linux), Steam, GOG]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1124180/Rail_Route/", best: true, note: "опис: колія, сигнали, сенсори й автороутери, контракти, режими Endless / Timetable / Rush Hour, редактор, Workshop"}
  - {kind: official, url: "https://railroute.eu/", note: "офіційний сайт, блог, прес-кит (EA 23.06.2021, 1.0 22.02.2024)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2792736784", note: "гайд Rush Hour: маршрут = клік по сигналу → клік по цілі, черга маршрутів, perpetual, автоблоки"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3167192631", note: "гайд Green: ручні/авто сигнали, сенсори прибуття/відправлення, токени й дослідження, контракти, затримки"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3173201893", note: "гайд Game Basics: словник — sink, типи поїздів і швидкості, офіси, токени, платформи"}
  - {kind: other, url: "https://bitrich.itch.io/railroute/devlog/188792/a-train-dispatcher-simulator-update-010", note: "0.10: сенсори читають ціль поїзда й керують автосигналом"}
  - {kind: other, url: "https://bitrich.itch.io/railroute/devlog/156472/rail-route-graphics-tunnels-and-more", note: "черга маршрутів сигналу, perpetual route, тунелі"}
  - {kind: other, url: "https://railroute.eu/2026/07/16/waypoints-for-everyone/", note: "DLC Expect Delays: редактор маршрутів «signal by signal», waypoints, години роботи, час будівництва на клітину"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rail+Route+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, hover-highlight, impassable-cells, round-currency, spawn-schedule, game-pause, sequential-levels, level-select, mode-select, in-game-editor, level-exchange, leaderboard, score-records, time-bonus, game-screen, +dispatch-waves, +sensor-trigger, +block-signal, +path-reservation, +route-by-click, +route-queue, +perpetual-route, +timetable-contracts, +research-tree, +platform-wait-queue, +train-reverse, +shunting-couple, +infrastructure-wear, +build-time, +online-coop]
proposes: ["+effect:set_route(signal, target)", "+effect:clear_route(signal)", "+effect:reverse", "+cond:route_free(signal, target)", "+trigger:sensor(train)", "+ui:route-highlight", "+ui:delay-risk-label", "+ui:schedule-overlap-warning", "+window:timetable-window", "+window:research-window", "+feature:degradation-speed", "+feature:construction-time-toggle", "+card:route-by-click", "+card:route-queue", "+card:perpetual-route", "+card:timetable-contracts"]
author: opus
date: 2026-11-09
---

# Rail Route — диспетчер залізниці: будуєш колію й сигнали, клацаєш маршрути, потім автоматизуєш

## Суть
Гравець — диспетчер: на карті-сітці за мотивами реальних міст будує колію, платформи й сигнали, а потяги за контрактами входять із країв мапи й мають вчасно пройти свій маршрут. Головна дія — **маршрут**: клік по сигналу, потім по цілі (платформа / інший сигнал), і колія між ними бронюється для поїзда. Рахунок і прогрес — за пунктуальність: вчасні поїзди дають гроші й токени, токени відкривають дослідження — автоматичні сигнали, сенсори, черги маршрутів, perpetual-маршрути, — і мережа поступово «їде сама». Лінія гри — зʼєднання й маршрутизація (Railbound, Train Valley), але з економікою й дослідженнями (`also: build-sim`).

## Поле і час
- Квадратна сітка: колія кладеться по клітинах («Track takes about 2 in-game minutes per square»), з діагоналями (?); платформи будуються прямо на колії; тунелі — після дослідження.
- Real-time з годинником гри: контракти мають розклад (прибуття/відправлення, період 10 хв…4 год); швидкість гри — (?).
- Границі мапи — **sink**-станції: тут поїзди зʼявляються і зникають.
- Шари: колія (стан зношення в DLC) + сигнали/сенсори на колії + будівлі (офіси, депо) + поїзди + броньовані маршрути.
- DLC Expect Delays (2026): зношення колії/стрілок/сигналів, поломки, шторми, відключення живлення, запізнення з-за меж мапи — випадкові події (базова гра — `random: none` (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Колія | conduit | клітина, швидкість (basic / advanced tracks), стан (DLC) | поїзд їде лише нею; зношена — повільніша, але прохідна |
| Стрілка (points/switch) | switch | положення | перекладається маршрутом; зношена — до ~15 с на переклад (DLC) |
| Ручний сигнал | gate | червоний / зелений | зелений лише після маршруту, заданого гравцем |
| Автосигнал (трикутник) | gate | черга маршрутів, perpetual | виконує маршрути з черги; perpetual — повторює щойно можливо (значок ∞) |
| Автоблок | gate | сегмент | тримає один поїзд на сегмент (?) — «autoblocks hold one train per segment» |
| Сенсор прибуття / відправлення | switch | ціль/вихід («Other», «All others», «Finished») | поїзд проїжджає → сенсор читає його ціль і замовляє маршрут у підʼєднаного автосигналу |
| Waypoint (DLC) | static | — | точка, через яку мусить пройти кожен рейс контракту, без зупинки |
| Sink-станція (край мапи) | spawner | напрям | поїзди входять і виходять |
| Станція: наскрізна / тупикова | static | платформи | тупикова — вхід з одного боку; поїзд чекає перед станцією, якщо платформа зайнята |
| Платформа | static | колір станції | поїзд стоїть заданий час; у Timetable/Endless — лише своя, у Rush Hour — будь-яка |
| Поїзд | object | тип, довжина, швидкість вперед/назад, контракт | їде маршрутом; розворот правим кліком або автоматично в тупику |
| Типи поїздів | object | Commuter 120 / Intercity 200 / Regional 160 / Freight 80 / Urban Transit 100 км/год | різні патерни контрактів (A>B>A, A>C, …) і час стоянки |
| Офіс (Conductor / Dispatch) | spawner | колір токенів | генерує контракти зелених / червоних поїздів; продається за повну ціну |
| Coach yard | static | — | потрібен Urban Transit і розвороту регіональних у тупику |
| Депо + сервісний локомотив SL-01 (DLC) | container | maintenance mode | ремонтує все, що проїжджає; буксирує зламані поїзди |
| Контракт | resource | патерн, період, оплата | без контракту рейс не існує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, track)` → ЯКЩО `counter(money, >=, cost)` → ТО `set_cell(cell, track)`, `currency(-cost)`; будівництво триває ігровий час (вимикається в налаштуваннях).
- КОЛИ `input(click, signal)` потім `input(click, target)` → ЯКЩО `path_exists(signal, target) and custom: «секція не зайнята іншим поїздом»` → ТО `custom: «маршрут броньовано, стрілки перекладено, сигнал зелений»`; цілі підсвічуються оранжевим.
- КОЛИ `input(click, target)` → ЯКЩО `not path_exists(signal, target)` → ТО `block` — маршрут лише туди, куди веде колія.
- КОЛИ `input(right_click, signal)` → ТО `custom: «скасувати перший маршрут у черзі сигналу»`.
- КОЛИ `input(shift_click, track)` після сигналу → ТО `custom: «perpetual-маршрут: відтворюється щоразу, коли можливо»`.
- КОЛИ `custom: «маршрут у черзі автосигналу стає можливим»` → ТО `custom: «створити маршрут автоматично»` (Routing Queue).
- КОЛИ `contact(train, sensor)` → ТО `custom: «прочитати ціль поїзда й замовити відповідний маршрут у підʼєднаного автосигналу»`.
- КОЛИ `reach(train, signal)` → ЯКЩО `state(signal, red)` → ТО `block` — поїзд чекає, алерт «Train waiting at signal».
- КОЛИ `reach(train, station)` → ЯКЩО `occupied(platform, train)` → ТО `block` — чекає перед станцією; з дослідженням Auto-accept — впуск FIFO.
- КОЛИ `reach(train, dead_end_platform)` → ЯКЩО `has(player, auto_reverse)` → ТО `face(train, back)`; інакше — правий клік по поїзду.
- КОЛИ `input(click, train_icon)` над sink → ТО `custom: «впустити поїзд на обрану платформу»` (Rush Hour; доступні — оранжеві).
- КОЛИ `reach(train, sink)` → ТО `disappear`, `custom: «рейс завершено»`.
- КОЛИ `custom: «рейс завершено вчасно»` → ТО `currency(+pay)`, `counter(tokens[color], +1)`; оплата залежить від швидкості колії (40 км/год < 120 км/год).
- КОЛИ `custom: «рейс запізнився з вини гравця»` → ТО `custom: «нема токена/оплати, мінус до рахунку»`; запізнення не з вини гравця (DLC) на рахунок не йде.
- КОЛИ `counter(tokens, >=, cost)` → ТО `unlock(research)` — напр. Auto-accept 3, Automatic Routing 5, Perpetual Circuit 5, Auto-reverse 5, Basic Tracks 10 (tier 2).
- КОЛИ `counter(tokens_per_cycle, >=, threshold)` → ТО `custom: «зірка мапи»` — перша золота за 20 токенів/год повністю автоматично.
- КОЛИ `wave_cleared` (Rush Hour) → ТО `give(player, station + track + signal)`; поїзди хвилі не випадкові й повертаються в наступних.
- КОЛИ `program_end` (Rush Hour: остання інструкція поїзда) → ТО `next_level`, `score(time)` — швидше = більше.
- КОЛИ `timer(every)` → ЯКЩО `custom: «поїзд проїхав елемент»` → ТО `custom: «стан колії/стрілки/сигналу погіршується»` (DLC; healthy → degraded → critical → malfunctioned).
- КОЛИ `custom: «відключення живлення»` → ТО `custom: «сенсори зони не маршрутизують — лише вручну»` (DLC).
- Перемога: Timetable — рахунок за пунктуальність, Rush Hour — час, Endless — без кінця. · Поразка: формально нема; затори й запізнення зʼїдають рахунок. · Зіткнення поїздів — (?) (маршрути бронюють колію).

## Керування і ввід
- Миша: режим будівництва (колія протягом, сигнали, сенсори, будівлі) і режим диспетчера (сигнали не працюють у buy mode).
- Маршрут: клік по сигналу → клік по цілі; Shift — perpetual; правий клік по сигналу — скасувати; правий клік по поїзду — розворот.
- G — shunting mode (зчеплення/розчеплення); M — мапа стану мережі (DLC).
- Повна підтримка геймпада (DualShock, DualSense).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Endless · Timetable · Rush Hour · Editor; вибір мапи (офіційні й Workshop).
- `game-screen`: мапа-сітка, поїзди, сигнали з кількістю маршрутів у черзі, оранжеві підсвітки цілей, `path-preview` броньованого маршруту, алерти (поїзд чекає, Delay Risk).
- `custom-window` розкладу (timetable) з жовтим попередженням про перекриття часу.
- `custom-window` контрактів (прийняти / відхилити / видалити) і `custom-window` дослідження (дерева технологій, tier 1–2, зелені й червоні).
- `custom-window` налаштування сенсора / автоматизації (ціль, «preserve created routes»).
- `editor-window` — редактор мап; `leaderboard` — Steam-рекорди; `tutorial-window` (провідник Jozic, туторіал сигналізації).
- `settings-window`: швидкість деградації (DLC), час будівництва, звук; DLC Soundtrack — музичний плеєр.
- `lobby-window` — кооператив (онлайн / LAN, 2025).

## Фічі поза полем
- `mode-sandbox`-подібний Endless, `mode-puzzle`-подібний Timetable (готові мапи й розклади, рахунок), Rush Hour — хвилі з нагородами між ними.
- `level-editor` + Steam Workshop (2000+ мап), `leaderboard-online`, `achievements` (76), trading cards, `cloud-save`.
- `meta-progression` у межах мапи: токени → дослідження → автоматизація.
- `mode-coop` (онлайн і LAN, оновлення 2025).
- DLC Expect Delays: зношення, сервісний локомотив, waypoints, години роботи (до 8 вікон), періоди контрактів.

## Варіації й родичі
- [OpenTTD — залізничний шар](../build-sim/openttd-rails.md) — блок- і path-сигнали, бронювання, але поїзди шукають шлях самі; [Train Valley](train-valley.md) — стрілки на льоту; [Railbound](railbound.md) — пазл на колію без сигналів; [Mini Metro](mini-metro.md) — лінії, не колія.
- Реальні системи: централізація (CTC/ЕЦ) — «клік від сигналу до сигналу» і є маршрутне керування диспетчера.
- Осі варіацій: **хто веде поїзд** — гравець кліком (Rail Route) / pathfinder (OpenTTD) / стрілки на льоту (Train Valley) · **автоматизація** — нема / черга сигналу / сенсори за ціллю / perpetual · **мета** — пунктуальність / прибуток / виживання · **середовище** — статичне / зношення й інциденти (DLC).

## Цікавинки для курсу
- Маршрут «сигнал → ціль»: BFS по графу колії + бронювання сегментів + перевірка, що секція вільна — 🥉.
- Черга маршрутів сигналу і perpetual-маршрут (відтворити щойно можливо) — 📎.
- Сенсор, що читає ціль поїзда й замовляє маршрут — правило «подія → команда» (міні-автоматизація) — 🥉.
- Платформи з FIFO-впуском і чеканням перед станцією — 📎.
- Розклад контрактів з періодом і перевіркою перекриття (жовте попередження) — 🥉.
- Токени → дерево досліджень з порогами — 📎.
- Зношення: стан елемента падає з трафіком, швидкість і час перекладу залежать від стану — 📎.
- Повна мережа з кількома поїздами в real-time без дедлоків (виявлення взаємного очікування) — 🥇.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` ↔ клік по сигналу й оранжеві цілі; `impassable-cells` ↔ забудова мапи; `round-currency` ↔ гроші; `spawn-schedule` ↔ поїзди за розкладом із sink; `game-pause`; `sequential-levels` + `level-select` + `mode-select` ↔ мапи й режими; `in-game-editor` + `level-exchange` ↔ редактор і Workshop; `leaderboard` + `score-records` + `time-bonus` ↔ рекорди й «швидше = більше»; `game-screen`.
- **Нема** → пропозиції карток:
  - `+dispatch-waves` «Хвилі поїздів з нагородою між ними (Rush Hour)» · game-logic/waves · 📎 — `enemy-waves` про ворогів.
  - `+sensor-trigger` «Сенсор на колії: подія проїзду → команда сигналу» · entities/interact · 🥉 — `sensor-predicates` про умови в програмі.
  - `+block-signal`, `+path-reservation` (OpenTTD) — сегменти й бронювання.
  - `+route-by-click` «Маршрут кліком від сигналу до цілі» · entities/interact · 🥉.
  - `+route-queue` «Черга маршрутів на сигналі, виконання щойно можливо» · entities/state · 📎.
  - `+perpetual-route` «Маршрут, що відтворюється сам» · entities/state · 📎.
  - `+timetable-contracts` «Рейси за розкладом з оплатою за вчасність» · game-logic/score · 🥉.
  - `+research-tree` «Дерево досліджень за токени» · game-logic/economy · 📎.
  - `+platform-wait-queue` «Чекання перед зайнятою платформою, FIFO» · entities/move · 📎.
  - `+train-reverse`, `+shunting-couple` — розворот і зчеплення.
  - `+infrastructure-wear` «Зношення від трафіку, ремонт» · entities/state · 📎.
  - `+build-time` «Будівництво триває ігровий час» · game-logic/economy · 🌱.
  - `+online-coop` — кооператив.

## Пропозиції до словників
- `+effect:set_route(signal, target)` / `+effect:clear_route(signal)` — забронювати / скасувати маршрут (зараз — `custom`).
- `+effect:reverse` — поїзд змінює напрям руху (вже просить Train Valley).
- `+cond:route_free(signal, target)` — шлях існує і не перетинає чужі броні.
- `+trigger:sensor(train)` — поїзд проїхав сенсор (подія з даними поїзда).
- `+ui:route-highlight` · `+ui:delay-risk-label` · `+ui:schedule-overlap-warning`.
- `+window:timetable-window` · `+window:research-window`.
- `+feature:degradation-speed` · `+feature:construction-time-toggle`.

## Джерела
- ⭐ [Steam: Rail Route](https://store.steampowered.com/app/1124180/Rail_Route/) — опис і режими (через appdetails: 1.0 22.02.2024, 76 досягнень, co-op, Workshop, лідерборди).
- [railroute.eu](https://railroute.eu/) + [прес-кит](https://railroute.eu/press/) — EA 23.06.2021, 1.0 22.02.2024, Bitrich.info (Кіпр).
- [Steam-гайд Rush Hour](https://steamcommunity.com/sharedfiles/filedetails/?id=2792736784) — клік по сигналу → по цілі, оранжеві підсвітки, черга й perpetual, правий клік, автоблоки, нагороди між хвилями, рахунок за час.
- [Steam-гайд Green](https://steamcommunity.com/sharedfiles/filedetails/?id=3167192631) — ручні/авто сигнали, Shift-perpetual, сенсори прибуття/відправлення, токени й ціни досліджень, Delay Risk, жовте перекриття, оплата від швидкості, зірки.
- [Steam-гайд Game Basics](https://steamcommunity.com/sharedfiles/filedetails/?id=3173201893) · [Steam-гайд Red](https://steamcommunity.com/sharedfiles/filedetails/?id=3166727037) — sink, типи станцій і поїздів, швидкості, офіси, FIFO, auto-reverse, coach yard, shunting (G).
- [Devlog 0.10](https://bitrich.itch.io/railroute/devlog/188792/a-train-dispatcher-simulator-update-010) · [Devlog graphics/tunnels](https://bitrich.itch.io/railroute/devlog/156472/rail-route-graphics-tunnels-and-more) — сенсори → автосигнали, Routing Queue, perpetual, тунелі.
- [Блог: Waypoints](https://railroute.eu/2026/07/16/waypoints-for-everyone/) · [Things Fall Apart](https://railroute.eu/2026/06/03/expect-delays-things-fall-apart-slowly/) · [What Goes Wrong](https://railroute.eu/2026/06/20/expect-delays-what-actually-goes-wrong/) · [Service Loco](https://railroute.eu/2026/06/12/meet-the-service-loco/) — DLC Expect Delays.
- YouTube: пошук «Rail Route gameplay».

## Непевне
- (?) Чи можливі зіткнення поїздів (маршрути бронюють колію; явного правила не знайшов); що таке «автоблок» точно і чим відрізняється від автосигналу.
- (?) Діагоналі на сітці, керування швидкістю часу, чи базова гра має випадкові події без DLC.
- (?) Як саме рахується рахунок Timetable-мап і запізнення; що дають зірки; роль «automatic routers» з опису Steam (у гайдах — лише Automatic Routing / Routing Queue).
- (?) Ціни досліджень і швидкості поїздів — з фан-гайдів, могли змінитися в патчах.
- Рядок черги: рік «2024 (EA 2021)» підтверджено.
