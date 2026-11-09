---
title: Train Valley
slug: train-valley
aka: []
family: connect-rotate
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2015
platforms: [PC, macOS, Linux, iOS, PS4, Switch, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Train_Valley", best: true, note: "колії між містами, знесення дороге, стрілки й перехрестя, мета — доставити кожен поїзд без банкрутства, 3 додаткові цілі на рівень, 4 глави × 6 рівнів + Germany, Sandbox"}
  - {kind: other, url: "https://www.thesixthaxis.com/?p=253942", note: "огляд: колії drag-ом, поїзди зʼявляються й чекають відправки, колір = ціль, start/stop/reverse, швидше = дорожче, податок, банкрутство"}
  - {kind: other, url: "https://nintendoworldreport.com/review/61084/train-valley-switch-review", note: "огляд Switch: 2–3 станції на старті, індикатор наступного поїзда, ціна падає з часом, 5 режимів курсора, ліміт 5–10 хв, 6-й випадковий рівень епохи"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Train+Valley", note: "пошук Steam (пряма сторінка app/345600 редиректить на головну)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Train+Valley+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [path-drawing, cell-click, impassable-cells, destructible-blocks, spawn-schedule, spawn-random-cell, move-auto, round-currency, time-bonus, time-out, progress-acceleration, game-pause, sequential-levels, level-unlock, level-select, world-map, mode-select, end-screen, goal-counter, objective-text, +junction-toggle, +train-dispatch, +delivery-value-decay, +bankruptcy-lose, +optional-objectives, +crash-on-mismatch]
proposes: ["+effect:extend_path", "+effect:toggle_junction", "+effect:dispatch", "+effect:reverse", "+cond:bankrupt", "+ui:next-train-gauge", "+ui:cursor-mode-bar", "+ui:money", "+feature:optional-objectives", "+card:train-dispatch", "+card:delivery-value-decay", "+card:bankruptcy-lose", "+card:optional-objectives"]
author: opus
date: 2026-11-09
---

# Train Valley — прокладай колії між станціями в реальному часі, перемикай стрілки й зупиняй поїзди, щоб кожен доїхав до станції свого кольору

## Суть
На клітинній мапі долини стоять 2–3 станції, згодом зʼявляються нові. На станції виникає поїзд з кольоровою позначкою станції-цілі й чекає; гравець прокладає колії, ставить стрілки, відправляє поїзд і веде його до цілі, зупиняючи й розвертаючи, щоб не було зіткнень. Ядро — **диспетчеризація на живій мережі**: колії дешеві, знесення лісів і будинків дороге, швидка доставка дає більше грошей, а банкрутство — кінець. Ближчий до Trainyard/Railbound, ніж до OpenTTD: економіка мінімальна, головне — маршрути й таймінг.

## Поле і час
- Квадратна сітка плиток (?) з рельєфом: ліс, села, гори, вода блокують маршрут; знести можна за гроші.
- Real-time з паузою: на паузі можна ставити колії, стрілки й відправляти поїзди без тиску.
- Рівень (Classic) обмежений часом 5–10 хв; календар йде роками історичного періоду глави (Європа 1830–1980 тощо), поїзди з часом стають швидшими й довшими (пар → дизель → електро).
- Індикатор наступного поїзда показує, коли станція згенерує новий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Станція | source (custom) | колір/символ; бік виходу | породжує поїзди до інших станцій; приймає поїзди свого кольору |
| Поїзд | object | колір цілі; швидкість, довжина (за епохою) | чекає на станції; після відправки їде коліями; можна зупинити й розвернути |
| Колія | conduit (custom) | пряма / поворот | прокладається drag-ом за гроші; можна прибрати |
| Стрілка (junction) | switch | активна гілка | гравець перемикає; визначає, куди поверне поїзд |
| Перехрестя | conduit (custom) | 2 прямі навхрест | поїзди проходять, не зʼєднуючись; одночасно — зіткнення (?) |
| Ліс / село / гора | static | ціна знесення | блокує колію; знесення платне, дороге на старті |
| Вода | static | — | блокує (?) колію; міст — (?) |
| Бюджет | resource | гроші | старт за рівнем; дохід за доставки; витрати на колії, знесення, податок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `free(cell)` and `has(player, money)` → ТО `custom: «покласти колію»`, `currency(-price)`.
- КОЛИ `input(demolish, cell)` → ЯКЩО `cell(x, forest|house|rock)` → ТО `set_cell(x, empty)`, `currency(-demolish_price)`.
- КОЛИ `input(click, junction)` → ТО `custom: «перемкнути стрілку»`.
- КОЛИ `schedule(next_train)` → ТО `spawn_at(train, station)` з випадковою (?) ціллю серед інших станцій.
- КОЛИ `input(dispatch, train)` → ТО `custom: «поїзд вирушає»`; КОЛИ `timer(wait)` вичерпано → ТО поїзд вирушає сам.
- КОЛИ `input(click, train)` → ТО `custom: «стоп / рушити / розворот»`.
- КОЛИ `tick` → ТО `move(train, next_cell_by_track)`.
- КОЛИ `contact(train, junction)` → ТО `custom: «їде активною гілкою»`.
- КОЛИ `contact(train_a, train_b)` → ТО `crash`, обидва зникають (?), `custom: «ціль "без аварій" провалена»`.
- КОЛИ `blocked(train)` (кінець колії) → ТО `crash` (?).
- КОЛИ `contact(train, station)` → ЯКЩО `same(train, station, color)` → ТО `disappear_a`, `currency(+value(t))`; інакше `disappear_a` без оплати і `custom: «ціль "без чужих станцій" провалена»`.
- КОЛИ `tick` під час рейсу → ТО `custom: «вартість доставки падає з часом»`.
- КОЛИ `timer(tax)` → ТО `currency(-tax)` (?).
- КОЛИ `counter(money, <, 0)` → ТО `lose`.
- КОЛИ `timer(level, ==, 0)` → ЯКЩО `counter(money, >=, 0)` → ТО `win`, `custom: «зарахувати виконані з 3 додаткових цілей»`, `unlock(next_level)`.
- КОЛИ `mode(sandbox)` → ТО `custom: «без грошей і ліміту часу»`.
- Перемога: дожити до кінця часу рівня без банкрутства · Поразка: банкрутство · Рахунок: гроші; 3 додаткові цілі (не зупиняти поїзди, не знищувати колій, без аварій, ліміт витрат/знесень).

## Керування і ввід
- ПК: клік-і-drag — колія за траєкторією; клік по стрілці — перемкнути; клік по поїзду — стоп/рушити/розворот; окремий інструмент знесення.
- Консолі: L/R перемикають п'ять режимів курсора — Junction, Track Build, Demolish, Dispatch, Train; стік обирає обʼєкт.
- Пауза — основний інструмент планування; регулятора швидкості поїздів нема.

## Вікна, меню, HUD
- `main-menu`: Play → `world-map` / `level-select` (глави Europe, America, USSR, Japan, + Germany DLC; по 6 рівнів, 6-й — випадковий); Sandbox; Settings.
- `game-screen`: мапа, `money`, рік/дата з `progress-bar` часу, `next-train-gauge` (коли зʼявиться наступний поїзд), `objective-text` (3 цілі), `cursor-mode-bar` (консолі).
- `pause-menu`: пауза з можливістю будувати.
- `end-screen`: результат рівня, виконані цілі (зірки ?), наступний рівень відкрито.
- `tutorial-window`: перші рівні; огляд Switch каже, що про індикатор поїзда не сказано.
- Переходи: main-menu → level-select → game-screen ⇄ pause-menu → end-screen → level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 4 глави × 6 рівнів (24), з Germany — 30; рівні відкриваються виконанням цілей.
- `mode-sandbox` (без грошей і часу), Classic/Story з додатковими цілями.
- Наступники: Train Valley 2 (2018), Train Valley World (2024), Train Valley Origins (2025).

## Варіації й родичі
- Родичі: Trainyard і Railbound (план → запуск, без real-time), Mini Metro (абстрактні лінії, пасажири самі), OpenTTD (сигнали, економіка), Pipe Mania (тиск часу на прокладання), Unrailed! (колія перед поїздом руками аватара).
- **Осі варіацій:** коли будуєш — до запуску / під час руху / на паузі · хто керує поїздом — розклад / гравець (стоп, реверс) · ціна — колія / знесення / час доставки · програш — аварія / банкрутство / переповнення.

## Цікавинки для курсу
- Колія drag-ом по клітинах: тип плитки (пряма/поворот) із сусідів шляху — 📎.
- Стрілка з двома гілками, поїзд обирає активну — 📎.
- Real-time рух кількох поїздів по графу колій + виявлення зіткнень (в одній клітині / на зустрічних) — 🥉.
- Вартість доставки, що спадає з часом, бюджет і банкрутство — 🌱.
- Знесення перешкод за ціною, залежною від типу клітини — 🌱.
- Додаткові цілі рівня як предикати над історією (без аварій, витрати ≤ N) — 📎.

## Мапа на каталог
- Є: `path-drawing` ↔ колія drag-ом · `cell-click` ↔ стрілки, поїзди · `impassable-cells` · `destructible-blocks` ↔ платне знесення · `spawn-schedule` ↔ поїзди за індикатором · `spawn-random-cell` (?) нові станції · `move-auto` ↔ поїзд · `round-currency` · `time-bonus` ↔ швидше = більше · `time-out` ↔ кінець рівня · `progress-acceleration` ↔ швидші поїзди епох · `game-pause` · `sequential-levels` · `level-unlock` · `level-select` · `world-map` · `mode-select` · `end-screen` · `goal-counter` · `objective-text`.
- **Нема** → пропозиції карток:
  - `+junction-toggle` «Стрілка з двома гілками» · entities/state · 📎 (з Trainyard).
  - `+train-dispatch` «Відправка/стоп/реверс рухомої сутності гравцем» · entities/move · 🌱.
  - `+delivery-value-decay` «Нагорода падає з часом доставки» · game-logic/score · 🌱.
  - `+bankruptcy-lose` «Програш при бюджеті < 0» · game-logic/lose · 🌱.
  - `+optional-objectives` «3 додаткові цілі рівня» · levels/progression · 📎.
  - `+crash-on-mismatch` «Аварія при зіткненні/обриві» · game-logic/lose · 🌱 (з Trainyard).

## Пропозиції до словників
- `+effect:extend_path` — подовжити шлях/колію (з Flow Free / Trainyard).
- `+effect:toggle_junction` — перемкнути гілку стрілки (з Trainyard).
- `+effect:dispatch` — відправити поїзд зі станції; `+effect:reverse` — розвернути рух сутності (для поїзда ≠ `bounce`).
- `+cond:bankrupt` — бюджет < 0 (можна `count`/`counter`, але частий стан економік).
- `+ui:next-train-gauge` — індикатор часу до наступного спавну; `+ui:cursor-mode-bar` — режими курсора на геймпаді; `+ui:money` — баланс.
- `+feature:optional-objectives` — додаткові цілі рівня (три на рівень).
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Train Valley — Wikipedia](https://en.wikipedia.org/wiki/Train_Valley) — колії, дороге знесення, стрілки й перехрестя, мета «доставити без банкрутства», 3 цілі на рівень, глави й роки, Sandbox, дати, сиквели.
- [TheSixthAxis](https://www.thesixthaxis.com/?p=253942) — колії drag-ом, поїзди чекають відправки, колір = ціль, start/stop/reverse, ціна падає з часом, податок, банкрутство, перешкоди, 24 рівні.
- [Nintendo World Report](https://nintendoworldreport.com/review/61084/train-valley-switch-review) — 2–3 станції на старті, індикатор наступного поїзда, ліміт 5–10 хв, 5 режимів курсора, 6-й рівень епохи випадковий, Sandbox.

## Непевне
- (?) Сітка — квадратні плитки (з памʼяті й скриншотів не бачив); вода і мости — не звірено.
- (?) Що саме відбувається з поїздами при зіткненні (зникають обидва?), чи обрив колії — аварія, податок як періодичний.
- (?) Ціль поїзда — випадкова серед станцій чи за розкладом рівня; автовідправка після очікування — огляд каже «dispatch, causing havoc», без деталей.
- (?) Зірки за цілі на `end-screen` — не звірено.
- Пряма Steam-сторінка (app/345600) у WebFetch редиректила на головну — у шапці пошуковий URL.
