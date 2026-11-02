---
title: OpenTTD / Transport Tycoon — залізничний шар (колія, сигнали, резервування)
slug: openttd-rails
family: build-sim
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2004
platforms: [PC, macOS, Linux, Android, Steam]
links:
  - {kind: fandom, url: "https://wiki.openttd.org/en/Manual/Signals", best: true, note: "офіційна вікі: блок- і path-сигнали, односторонні, пре-сигнали, безпечні точки очікування"}
  - {kind: fandom, url: "https://wiki.openttd.org/en/Manual/Railway%20construction", note: "інструменти колії, autorail, депо, станції, тунелі/мости, типи рейок"}
  - {kind: fandom, url: "https://wiki.openttd.org/en/Manual/Trains", note: "аварії поїздів, переїзди з автомобілями"}
  - {kind: fandom, url: "https://wiki.openttd.org/en/Archive/Manual/Yet%20Another%20Pathfinder", note: "YAPF: сегменти, кеш, штраф за червоні сигнали попереду"}
  - {kind: fandom, url: "https://wiki.openttd.org/en/Manual/Railway%20station", note: "станції RoRo, бухти очікування, вибір платформи"}
  - {kind: other, url: "https://wiki.openttd.org/en/Community/Junctionary/", note: "Junctionary — каталог розвʼязок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/OpenTTD"}
  - {kind: official, url: "https://www.openttd.org/"}
  - {kind: steam, url: "https://store.steampowered.com/app/1536610/OpenTTD/", note: "безкоштовно"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=openttd+path+signals+tutorial", note: "пошук; туторіали сигналів"}
stage: v1
coverage: 60
mechanics: [impassable-cells, multi-cell-size, cell-click, hover-highlight, field-scaling, minimap-radar, game-pause, save-game, ai-opponent, chase-bfs, environment-death, round-currency, game-loop, state-as-data, in-game-editor, +block-signal, +path-reservation, +track-pieces-per-tile, +pathfinder-penalties, +train-crash, +level-crossing, +depot-service, +safe-waiting-position, +one-way-signal, +presignal-logic, +drag-build-line, +context-tile-rules, +entity-rotate, +coverage-area]
proposes: ["+trigger:tick", "+trigger:enter", "+trigger:leave", "+trigger:rng", "+cond:free", "+cond:facing", "+cond:path_exists", "+cond:occupied", "+effect:move", "+effect:set_state", "+effect:crash", "+effect:face", "+effect:speed", "+role:terrain", "+role:conduit", "+role:switch", "+role:gate", "+role:zone", "+ui:tool-palette", "+ui:path-preview", "+ui:minimap", "+ui:toast", "+window:map-window", "+window:orders-window", "+window:depot-window", "+feature:speed-control", "+feature:online-multiplayer", "+feature:mod-support", "+feature:level-editor", "+axis:control", "+card:path-reservation"]
author: opus
date: 2026-11-02
---

# OpenTTD (залізниця) — мережа клітин-колій, де поїзди резервують ділянки, а сигнали ділять граф на блоки

## Суть
Описано **лише рейковий шар** OpenTTD (відкритий ремейк Transport Tycoon Deluxe, 1995): гравець прокладає колію по клітинах, ставить сигнали, депо й станції, а поїзди самі їздять за наказами, шукаючи шлях і **резервуючи** ділянки колії, щоб не зіткнутись. Це мережа клітин із резервуваннями: клітина колії може містити кілька відрізків, сигнали розрізають граф на блоки, а path-сигнал пускає поїзд лише після бронювання шляху до наступної безпечної точки. Погано розставлені сигнали = затори або аварія; уся «гра» — інженерія пропускної здатності. Економіка, дороги, кораблі, літаки, міста — поза описом.

## Поле і час
- Квадратна сітка тайлів (мапа від 64×64 до 4096×4096 (?)), рендер ізометричний; висоти кутів тайла дають схили (колія — на рівному чи на допустимому схилі; тунелі й мости — через рельєф і перешкоди).
- **Тайл колії** містить до 6 відрізків: 2 прямі (X, Y) і 4 «напівтайлові» діагональні (верх/низ/ліво/право); кілька відрізків на тайлі = розвʼязка/стрілка. Діагональна лінія — це ланцюг напівтайлових відрізків.
- Шари: рельєф · колія (тип рейок) · сигнали (на відрізок, до 2 напрямків) · станції/депо/маршрутні точки · поїзди (вагон ≈ пів тайла: «два вагони в одному тайлі»).
- Real-time з фіксованим тіком і календарем (дні/місяці/роки); пауза й прискорення. Поїзди мають прискорення/гальмування, швидкість обмежують повороти, схили, тип рейок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відрізок колії | terrain | тип рейок, напрям (X/Y/4 діагоналі) | поїзд їде лише відрізками; кілька на тайлі — стрілка |
| Тип рейок | terrain | normal / electric / monorail / maglev | поїзд їде лише сумісними (електровоз — лише електрифікованою) |
| Блок-сигнал | gate | однобічний / двобічний | червоний, якщо **будь-який** поїзд у наступному блоці (усі гілки блоку разом) |
| Path-сигнал (дефолт) | gate | двобічний з тильним проходом | зелений, лише якщо поїзду заброньовано шлях до наступної безпечної точки; ззаду проїзд можливий зі штрафом |
| Односторонній path-сигнал | gate | — | як path, але ззаду — «вічно червоний» зустрічний |
| Entry / Exit / Combo пре-сигнал (legacy) | switch | — | entry пускає, лише якщо в наступному блоці є хоч один зелений exit; combo = entry+exit |
| Блок | zone | — | максимальна звʼязна ділянка колії між сигналами |
| Резервування | zone | шлях поїзда | броньовані відрізки (підсвічуються); інший поїзд не може взяти конфліктний |
| Депо | container | напрям виходу (1 вхід) | купівля, ремонт/сервіс, розворот, продаж поїздів |
| Станція (платформи) | static | кількість платформ × довжина в тайлах, напрям | поїзд стає, вантажить; зона збору вантажу довкола |
| Маршрутна точка (waypoint) | static | — | ціль у наказах «via» без зупинки |
| Тупик / буфер | static | — | поїзд розвертається і їде назад (?) |
| Міст / тунель | terrain | довжина, макс. швидкість (мост) | лінк між двома кінцями над/під тайлами |
| Поїзд | object | локомотив + вагони, довжина, макс. швидкість, надійність | їде за наказами, шукає шлях YAPF, бронює, чекає на червоний |
| Автомобіль на переїзді | neutral | — | гине, якщо на переїзді одночасно з поїздом |
| Переїзд (level crossing) | gate | — | вогні зупиняють авто, які ще не заїхали |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, track)` → ЯКЩО `cell(tile, buildable)` і схил допустимий і `currency ≥ cost` → ТО `set_cell(tile, +piece)`, `currency(-cost)`; інакше `message(причина)`.
- КОЛИ `tick` → ТО `move(train, along_track)` зі швидкістю за прискоренням; `speed(train, limit)` на поворотах/схилах/мостах.
- КОЛИ `enter(train, junction_tile)` → ТО `custom: «YAPF вибирає відрізок: A* по сегментах між важливими точками, вартість = довжина + штрафи (повороти, схили, станції, червоні сигнали попереду p0+p1·i+p2·i²)»`.
- КОЛИ `reach(train, block_signal)` → ЯКЩО `occupied(next_block, train)` → ТО `block` (чекає); інакше проїзд.
- КОЛИ `reach(train, path_signal)` → ЯКЩО `path_exists(до safe_wait, не перетинаючи чужі броні)` → ТО `set_state(path, reserved)`, сигнал зелений; інакше `block`.
- Безпечна точка очікування = лицьова сторона будь-якого сигналу або кінець платформи → тому сигнал ставлять **перед** розвʼязкою.
- КОЛИ `leave(train, piece)` → ТО `clear_state(piece, reserved)` (броня знімається за хвостом).
- КОЛИ `reach(train, oneway_path_signal from back)` → ТО `block` (непрохідно ззаду).
- КОЛИ `reach(train, entry_presignal)` → ЯКЩО `count(green exit у наступному блоці, ≥, 1)` → ТО прохід; інакше `block`.
- КОЛИ два поїзди на одному відрізку (нема сигналів або ззаду в блок) → ТО `crash` обох, `disappear_both`, колія тимчасово непрохідна, рейтинги станцій падають.
- КОЛИ `contact(train, road_vehicle)` на переїзді → ТО `disappear_b` (авто знищено, поїзд цілий); вогні вмикаються при бронюванні (path) або перед самим поїздом (без сигналів).
- КОЛИ `reach(train, dead_end)` → ТО `face(train, reverse)` (?).
- КОЛИ `reach(train, station)` за наказом → ТО зупинка, `custom: «вантаж/розвантаж; full load — чекати повного»`, далі наступний наказ.
- КОЛИ `timer(service_interval)` → ЯКЩО депо поруч з маршрутом → ТО заїзд на сервіс; `rng(p)` (за надійністю) → `set_state(train, broken_down)` на кілька днів.
- КОЛИ `not path_exists(train, order_target)` → ТО `message(«поїзд загубився»)`.
- Перемоги як такої нема (пісочниця); рахунок — прибуток компанії, рейтинг компанії, конкуренція з AI. Поразка — банкрутство.

## Керування і ввід
- Курсор по ізометричній сітці: панель «Railway construction» — колія за напрямком (1–4), **Autorail** (тягнеш — гра сама обирає відрізки), депо, waypoint, станція, сигнали, тунель (T), міст (B), конвертер типу рейок (C), видалення (Ctrl/R).
- Drag тягне лінію колії; сигнали drag-ом ставляться через кожні N тайлів; Ctrl+клік на сигнал — циклічно змінює тип; клік — двобічний/однобічний.
- Поїзди не керуються напряму: накази (Go to, Non-stop, Via, Full load, Unload) + кнопки Start/Stop/Reverse/Send to depot.

## Вікна, меню, HUD
- `main-menu`: New Game, Load, Play Scenario, Scenario Editor, Multiplayer, Online Content, Settings, AI/Game Script settings.
- `game-screen`: ізометрична мапа + верхня панель інструментів (пауза, швидкість, налаштування, мапа, міста, фінанси, компанії, транспорт, будівництво); нижній рядок — дата, гроші, новини.
- `tool-palette` колії; вікно вибору сигналу (типи + інтервал drag); вікно станції (напрям, к-сть платформ, довжина, підсвітка зони збору).
- `depot-window` (новий: список поїздів, Buy, Clone, Sell, Start); `orders-window` (новий: список наказів); вікно поїзда (стан, швидкість, «Heading for…»); timetable; vehicle list.
- `map-window` (мінімапа з маршрутами, рельєфом, власниками); `settings-window` (дуже великий: сигнали за замовчуванням, YAPF/NPF, аварії, поломки, прискорення, розвороти).
- `toast` новин: аварія, перший поїзд на станції, поїзд загубився.
- Переходи: main-menu → (нова гра: налаштування мапи) → game-screen; game-screen ↔ будь-яке вікно як немодальне.

## Фічі поза полем
- `speed-control` (fast-forward), `pause`, `save-slots`/`autosave`, `level-editor` (Scenario Editor), `online-multiplayer` (до 255 гравців у 15 компаніях), `mod-support` (NewGRF графіка/транспорт, AI, Game Scripts), `custom-rules` (Advanced Settings: аварії вкл/вимк, тип сигналу за замовчуванням, поломки).
- Junctionary і Rail Designs — спільнотні бібліотеки розвʼязок (аналог `pattern-library`).

## Варіації й родичі
- Transport Tycoon (1994) / TTD (1995) — оригінал з блок-сигналами й пре-сигналами; OpenTTD додав path-сигнали й YAPF.
- Родичі: Factorio (блоки колії й chain-сигнали — `+block-signal`), Simutrans, Railway Empire, Mini Metro (абстрактна мережа без сигналів), Train Valley / Railbound (пазли розкладки колії), реальна АБ/маршрутна централізація.
- **Осі варіацій**: блоки без броні / броня шляху · одна колія на клітину / кілька відрізків · аварії смертельні / вимкнені · пошук шляху на вузлах-тайлах (NPF) / на сегментах (YAPF) · розворот у тупику дозволено / ні.

## Цікавинки для курсу
- Тайл з 6 відрізками колії й переходами «з якого відрізка в який» — 🥉 (граф на сітці: вузли = (тайл, напрям)).
- Блок-сигнали: flood fill звʼязної колії між сигналами + «зайнято/вільно» — 🥈.
- Path-резервування: бронювання шляху до безпечної точки, відмова при конфлікті — 🥇 (A* + атомарне захоплення ресурсу).
- YAPF-штрафи: вартість шляху з червоними сигналами попереду (квадратична формула) — 🥈.
- Аварія як наслідок відсутності сигналу — 📎 (детектор двох поїздів на відрізку).
- Пре-сигнали entry/exit/combo: сигнал дивиться на стан інших сигналів — 🥈.
- Autorail: drag мишею → гра підбирає відрізки за напрямком руху курсора — 🥉.

## Мапа на каталог
- Є: `impassable-cells` (рельєф/вода без мостів) · `multi-cell-size` (станція N×M, поїзд довжиною в кілька тайлів) · `cell-click` · `hover-highlight` · `field-scaling` · `minimap-radar` · `game-pause` · `save-game` · `ai-opponent` (AI-компанії) · `chase-bfs` (пошук шляху поїздом) · `environment-death` (аварія) · `round-currency` · `game-loop` · `state-as-data` · `in-game-editor` (Scenario Editor).
- **Нема** → пропозиції карток:
  - `+block-signal` (з Factorio) — повторно, ядро цієї гри.
  - `+path-reservation` «Бронювання шляху до безпечної точки» · game-logic · 🥇 · слоти {safe_points}.
  - `+track-pieces-per-tile` «Кілька відрізків колії в клітині» · entities/move · 🥉.
  - `+pathfinder-penalties` «Вартість шляху зі штрафами» · entities/move · 🥈 · слоти {curve, slope, red_signal} — дитина `chase-bfs`.
  - `+train-crash` «Зіткнення поїздів без сигналів» · entities/death · 📎.
  - `+level-crossing` «Переїзд двох мереж» · entities/interact · 📎.
  - `+depot-service` «Депо: купівля, сервіс, розворот» · game-logic/economy · 📎.
  - `+safe-waiting-position` «Точка, де дозволено чекати» · game-logic · 🥉 (частина `+path-reservation`).
  - `+one-way-signal` «Сигнал, непрохідний ззаду» · entities/legality · 🌱.
  - `+presignal-logic` «Сигнал дивиться на інші сигнали» · game-logic · 🥈.
  - `+drag-build-line` «Тягни — будуй лінію з автопідбором форми» · interface/input · 🥉 (Autorail; також стіни CoC, фундаменти PA).
  - `+context-tile-rules` (Townscaper), `+entity-rotate`, `+coverage-area` (зона збору станції) — повторно.

## Пропозиції до словників
- `+trigger:tick`, `+trigger:enter` (тайл-розвʼязка), `+trigger:leave` (знято броню), `+trigger:rng` (поломка).
- `+cond:free`, `+cond:facing`, `+cond:path_exists` (є шлях до безпечної точки), `+cond:occupied` (блок зайнятий).
- `+effect:move`, `+effect:set_state` (reserved/broken_down), `+effect:crash` (зіткнення), `+effect:face` (розворот), `+effect:speed`.
- `+role:terrain` (колія), `+role:conduit` (колія як провідник поїздів), `+role:switch` (пре-сигнали), `+role:gate` (сигнали, переїзд), `+role:zone` (блок).
- `+ui:tool-palette`, `+ui:path-preview` (підсвітка броні), `+ui:minimap`, `+ui:toast` (новини).
- `+window:map-window`; нові `+window:orders-window` — список наказів транспорту (схоже на `code-editor`), `+window:depot-window` — гараж транспорту.
- `+feature:speed-control`, `+feature:online-multiplayer`, `+feature:mod-support`, `+feature:level-editor`.
- `+axis:control` = `indirect` (поїзди їздять за наказами).
- `+card:path-reservation` — див. вище.

## Джерела
- ⭐ [OpenTTD wiki: Signals](https://wiki.openttd.org/en/Manual/Signals) — усі типи сигналів, блоки, path-броня, безпечні точки, поради розміщення.
- [OpenTTD wiki: Railway construction](https://wiki.openttd.org/en/Manual/Railway%20construction) — інструменти колії, autorail, типи рейок (normal 1926, electric 1965, monorail 1999, maglev 2022).
- [OpenTTD wiki: Trains](https://wiki.openttd.org/en/Manual/Trains) — аварії поїздів і на переїздах.
- [OpenTTD wiki: YAPF](https://wiki.openttd.org/en/Archive/Manual/Yet%20Another%20Pathfinder) — сегменти, кеш, формула штрафу за червоні сигнали.
- [OpenTTD wiki: Railway station](https://wiki.openttd.org/en/Manual/Railway%20station) — схеми станцій і бухт очікування.
- [Junctionary](https://wiki.openttd.org/en/Community/Junctionary/) — каталог розвʼязок.
- [Wikipedia](https://en.wikipedia.org/wiki/OpenTTD) — історія (0.1 у 2004), платформи, мультиплеєр.
- [openttd.org](https://www.openttd.org/) · [Steam](https://store.steampowered.com/app/1536610/OpenTTD/).

## Непевне
- (?) Діапазон розмірів мапи (64…4096) і «6 відрізків на тайл» — з памʼяті, сторінки вікі цього не формулюють.
- (?) Розворот у тупику й на станції залежить від налаштувань; поведінка за замовчуванням не перевірена.
- (?) Штрафи YAPF за повороти/схили/станції — вікі каже, що сторінка неповна; формула лише для червоних сигналів перевірена.
- (?) Рік: OpenTTD 0.1 — 2004; оригінальний TTD — 1995 (Wikipedia суперечить сама собі: 1994/1995).
