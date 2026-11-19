---
title: Upalu Mundi
slug: upalu-mundi
aka: []
family: program-robots
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows), macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3623200/Upalu_Mundi/", best: true, note: "опис: сітка 8×8, чотири типи стрілок, симуляція на макеті, лінія оптимуму Upalu Mundi; трейлер і скріншоти"}
  - {kind: other, url: "https://david.reviews/articles/upalu-mundi-review/", note: "огляд: ~75 рівнів, стрілки alternating / if empty, сигнали проти deadlock, рахунок = тривалість + вартість, ліміт 999 циклів, без undo"}
  - {kind: other, url: "https://www.gamingonlinux.com/2026/05/keep-goods-moving-along-the-rails-in-mini-puzzler-upalu-mundi/", note: "огляд: запуск дроселем, газети, протоколи нарад; посилання на трейлер"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3623200&count=20&maxlength=4000", note: "Steam News (JSON): патчі — стоп-знаки обʼєктів, зони, UMC, світи 3–4, українська локалізація"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=gmEIGLZZX5E", note: "трейлер (посилання зі статті GamingOnLinux)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Upalu+Mundi+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, time-out, completion-detection, sequential-levels, level-select, leaderboard, help-window, tutorial-window, game-screen, main-menu, save-progress, +run-simulation, +junction-toggle, +conditional-switch, +multi-train, +cargo-route, +facility-stop-sign, +zone-train-limit, +solution-metrics, +optimal-curve-chart, +track-cost-score, +story-chapters, +story-choices, +solution-slots]
proposes: ["+effect:toggle_junction", "+window:memo-briefing", "+window:newspaper", "+window:meeting-minutes", "+window:solution-chart", "+window:blueprints-drawer", "+ui:throttle", "+ui:cost-counter", "+feature:pixel-scaling", "+feature:dev-curated-records", "+card:conditional-switch", "+card:facility-stop-sign", "+card:optimal-curve-chart"]
author: opus
date: 2026-11-19
---

# Upalu Mundi — гномівська залізниця на 8×8: колії, станції й чотири типи стрілок, потім симуляція й гонка за лінією оптимуму

## Суть
Гравець — гном Pyrael, інженер вагонеткової мережі компанії Mountain Mining Industries. На сітці 8×8 він кладе колії, ставить станції й стрілки чотирьох типів (взятих із шахтних вагонеток), щоб потяги перевезли всі вантажі від джерел до приймачів: пшеницю й відвідувачів — до пивоварні, «гу» — до переробного заводу.

Мережу перевіряють на макеті-симуляторі: потяги ходять циклами, і рішення має завершитись швидше за 999 циклів. Розвʼязків кілька, кожен оцінюється тривалістю й вартістю колії, а самоцвіт Upalu Mundi показує лінію оптимуму, до якої тягнешся оптимізацією. По суті це просторове програмування: стрілки — умовні переходи й тригери, стоп-знаки — синхронізація кількох потягів.

## Поле і час
- Сітка 8×8 («neatly arranged 8x8 grid»); графіка — піксельна ізометрія (теги Steam), логіка — квадратні клітини.
- Шари: місцевість (поля й флора — будувати можна, але вартість зростає), заздалегідь покладені колії, індустрії й зони рівня; поверх — колії, станції й стрілки гравця.
- Час `programmed`: розстановка без часу → запуск симуляції дроселем → потяги рухаються дискретними циклами; ліміт 999 циклів, на частині рівнів — ще й часові межі.
- Детерміновано: «multiple deterministic solutions» — та сама мережа завжди дає той самий результат.
- ~75 рівнів у світах (патчі переробляли світи 3 і 4); у кожного рівня свій «твіст» — тіснота, обмежена кількість локомотивів чи вагонів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Потяг (локомотив + вагони) | object | 2–3 вагони; кількість локомотивів і вагонів задає рівень | щоцикл їде колією на наступну клітину; везе вантаж |
| Вантаж (пшениця, відвідувачі, «гу») | resource | тип, кількість на обʼєкті | вантажиться на станції джерела, вивантажується на станції приймача |
| Колія | conduit | 1g за сегмент; штраф на полі чи флорі | веде потяг у сусідню клітину |
| Заздалегідь покладена колія | static | — | частина рівня; потяг їде нею як звичайною |
| Станція | terrain | довжина (є спільна станція довжиною 4) | місце завантаження й розвантаження вагонів |
| Обʼєкт-джерело (поле, джерело «гу») | source | запас вантажу | віддає вантаж потягам |
| Обʼєкт-приймач (пивоварня, переробний завод) | sink | потреба | приймає вантаж; «усе оброблено» — подія для стоп-знаків |
| Стрілка alternating | switch | дві гілки, поточна | пускає потяги гілками по черзі (?) |
| Стрілка if empty | switch | дві кольорові стрілки | порожній потяг — одною гілкою, навантажений — другою |
| Ще два типи стрілок | switch | (?) | у відкритих джерелах не описані |
| Стоп-знак | gate | привʼязаний до обʼєкта; активний / ні | тримає потяг (?); гасне, коли вантажі обʼєкта оброблено |
| Зона / зона одного доступу | zone | номер, ліміт потягів | обмежує кількість потягів (зона 9 — один потяг на головній мережі) |
| Поле, флора | terrain | — | будувати можна, вартість мережі зростає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, rail)` → ЯКЩО `free(cell)` → ТО `place(player, rail)`, `counter(cost, +1)`; ЯКЩО `cell(cell, field|flora)` → ТО ще `counter(cost, +penalty)`.
- КОЛИ `input(place, station|switch[type])` → ЯКЩО `free(cell)` → ТО `place(player, station|switch)`.
- КОЛИ `input(throttle)` → ТО `custom: «запуск симуляції на макеті»`, `timer(start)`.
- КОЛИ `tick` (цикл) → ТО `move(train, next_cell_by_track)`, `counter(cycles, +1)`.
- КОЛИ `enter(train, station)` → ЯКЩО `custom: «станція при джерелі»` and `custom: «є порожній вагон»` → ТО `give(train, cargo)`.
- КОЛИ `enter(train, station)` → ЯКЩО `has(train, cargo)` and `custom: «станція при приймачі цього вантажу»` → ТО `take(train, cargo)`, `counter(goods_left, -1)`.
- КОЛИ `enter(train, switch_alternating)` → ТО `move(train, active_branch)`; `after` → `set_state(switch_alternating, other_branch)` (?).
- КОЛИ `enter(train, switch_if_empty)` → ЯКЩО `not has(train, cargo)` → ТО `move(train, empty_arrow)`; інакше `move(train, loaded_arrow)`.
- КОЛИ `reach(train, stop_sign)` → ЯКЩО `state(stop_sign, active)` → ТО `block` — потяг чекає (?).
- КОЛИ `counter(goods_left[facility], ==, 0)` → ТО `clear_state(stop_signs[facility], active)`, `set_state(neighbor_stop_signs, active)` — знаки сусідніх обʼєктів, прямо звʼязаних із цим (з версії 1.1.4).
- КОЛИ `enter(train, zone)` → ЯКЩО `count(train_in_zone, >=, zone_limit)` → ТО `block` (?).
- КОЛИ `blocked(train)` → ЯКЩО `custom: «потяги чекають один на одного»` → ТО `custom: «deadlock — рішення не завершиться»`; стоп-знаки — інструмент проти цього.
- КОЛИ `counter(cycles, ==, 999)` → ЯКЩО `counter(goods_left, >, 0)` → ТО `lose` (рішення не проходить).
- КОЛИ `counter(goods_left, ==, 0)` → ТО `win`, `score(cycles, cost)`, `custom: «точка рішення на графіку проти кривої Upalu Mundi; UMC-оцінка рівня»`.
- Перемога: усі вантажі доставлено до ліміту циклів · Поразка: ліміт циклів або deadlock — правиш мережу й запускаєш знову · Рахунок: тривалість у циклах і вартість (1g за сегмент + штрафи за поле й флору), порівняння з кривою оптимуму; UMC у відсотках (?).

## Керування і ввід
- Розстановка колій, станцій і стрілок на клітини курсором; точний жест (клік чи протяг) не перевірено; гарячі клавіші пришвидшують редагування.
- Запуск — дросель макета; симуляцію можна зупинити, але точно на потрібному циклі — лише вручну («manual, error-prone»).
- Undo нема: випадковий reset чи стерта розвилка коштують дорого.
- Іконки стрілок кольорові (яка стрілка — для порожнього потяга); їх доводиться звіряти з мануалом.

## Вікна, меню, HUD
- `main-menu` — стартовий екран; у правому верхньому куті — масштаб пікселів Perfect / Full (з 1.1.1).
- `custom-window` «мемо» — записка колег, що відкриває кожен рівень.
- `game-screen`: сітка 8×8 з місцевістю й індустріями; `tool-palette` (колія, станція, стрілки, стоп-знаки (?)); дросель запуску; `turn-counter` циклів і лічильник вартості (?).
- `help-window` — вбудована документація з поясненням іконок.
- `custom-window` графік рішень: тривалість × вартість проти кривої оптимуму Upalu Mundi, UMC-оцінка рівня.
- `custom-window` шухляда креслень (blueprints drawer) з превʼю й гортанням (анімацію перегортання прибрали в 1.1).
- `custom-window` газета між великими розділами (частина статей залежить від твоїх рішень) і протоколи нарад компанії, де колеги коментують твою роботу.
- `tutorial-window` — навчання стоп-знакам і потягам (переробили в 1.0.3).
- Переходи: мемо → game-screen → дросель → симуляція → (успіх) графік і оцінка → наступний рівень; між розділами — газета.

## Фічі поза полем
- `levels-sequential` у світах; сюжетна подача — мемо, газети, протоколи нарад; статті газет реагують на спосіб розвʼязку.
- `leaderboard-online` (Steam Leaderboards) і «лінія Upalu Mundi», яку розробник оновлює світовими рекордами гравців з іменами (патчі «High Score Update» 1.0.1–1.1.6).
- `achievements` (9); найрідкісніше вимагає середнього UMC 80 % (було 90 %).
- `cloud-save` (Steam Cloud); `localization`: англійська, німецька, з 1.1.6 — українська.
- Нема `undo`; підтримка Steam Deck і малих екранів через масштаб пікселів.

## Варіації й родичі
- Патчі змінювали правила й рівні: переробка світів 3 і 4, пересунуті індустрії (старі рішення переставали працювати), стоп-знаки сусідніх обʼєктів (1.1.4), зона 9 з одним потягом (1.0.8).
- У корпусі: [Trainyard](../connect-rotate/trainyard.md) і [Railbound](../connect-rotate/railbound.md) — «план → запуск», стрілки, що перемикаються проїздом; [Rail Route](../connect-rotate/rail-route.md) і [OpenTTD](../build-sim/openttd-rails.md) — сигнали проти зіткнень і deadlock; [Manufactoria](manufactoria.md) — розгалуження за станом обʼєкта; [Turing Tumble](turing-tumble.md) — біт, що перемикається проходом; [Opus Magnum](opus-magnum.md), [SpaceChem](spacechem.md) — оптимізація метрик рішення.
- Осі варіацій: стрілка «ручна / по черзі після проїзду / за станом потяга»; сигнал «блок колії / знак, привʼязаний до обʼєкта»; метрика «цикли / вартість колії / площа»; оцінка «гістограма спільноти / крива оптимуму від гри».

## Цікавинки для курсу
- Симулятор мережі: потяги-агенти щоцикл ідуть колією, стрілки зі станом, вантажі між обʼєктами — 🥈 (кілька агентів і детермінований порядок оновлення).
- Стрілка if empty як умовний перехід, alternating як T-тригер — 📎 кожна.
- Стоп-знаки обʼєктів: «усе оброблено → свої знаки гаснуть, сусідні вмикаються» — 🥉 (подієва синхронізація, як семафор).
- Ліміт 999 циклів і виявлення взаємного блокування потягів — 🥉.
- Рахунок «цикли + вартість колії зі штрафом за місцевість» — 📎; графік рішень із кривою оптимуму (Парето-фронт) — 🥈.
- Автооптимізатор мережі 8×8 під обидві метрики — 👑 (величезний простір розстановок).

## Мапа на каталог
- Є: `cell-click` ↔ розстановка колій, станцій, стрілок · `time-out` ↔ ліміт 999 циклів · `completion-detection` ↔ «усі вантажі доставлено» · `sequential-levels` + `level-select` ↔ ~75 рівнів у світах · `leaderboard` ↔ Steam Leaderboards · `help-window` ↔ вбудований мануал · `tutorial-window` ↔ навчання стоп-знакам і потягам · `game-screen` · `main-menu` · `save-progress` ↔ Steam Cloud.
- **Нема** → пропозиції карток:
  - `+run-simulation` (повтор) · слот {cycles_limit: 999}.
  - `+junction-toggle` (повтор) — стрілка alternating.
  - `+conditional-switch` «Стрілка за станом потяга (порожній / навантажений)» · entities/interact · 📎 · слот {cond: empty|loaded}.
  - `+multi-train` (повтор) — кілька потягів однієї мережі.
  - `+cargo-route` «Вантаж від джерела до приймача» · game-logic/win · 📎 · слот {goods}.
  - `+facility-stop-sign` «Стоп-знак, що гасне, коли обʼєкт оброблено» · entities/state · 🥉.
  - `+zone-train-limit` «Зона з лімітом потягів» · entities/legality · 📎 · слот {n}.
  - `+solution-metrics` (повтор) — цикли й вартість.
  - `+optimal-curve-chart` «Графік рішень проти кривої оптимуму» · interface/results · 🥉.
  - `+track-cost-score` «Вартість колії як метрика, зі штрафом за місцевість» · game-logic/score · 🌱.
  - `+story-chapters` / `+story-choices` (повтори) — газети між розділами, статті залежать від рішень.
  - `+solution-slots` «Кілька збережених креслень рівня» · game-logic/save · 🌱 (?).

## Пропозиції до словників
- `+effect:toggle_junction` — перемкнути гілку стрілки після проїзду (alternating).
- `+window:memo-briefing` — записка перед рівнем; `+window:newspaper` — газета між розділами; `+window:meeting-minutes` — протоколи нарад; `+window:solution-chart` — графік рішень проти кривої оптимуму; `+window:blueprints-drawer` — шухляда збережених креслень.
- `+ui:throttle` — дросель запуску симуляції; `+ui:cost-counter` — вартість мережі.
- `+feature:pixel-scaling` — режими масштабу пікселів (Perfect / Full); `+feature:dev-curated-records` — розробник вносить рекорди гравців у лінію оптимуму патчами.
- `+card:conditional-switch`, `+card:facility-stop-sign`, `+card:optimal-curve-chart` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Upalu Mundi](https://store.steampowered.com/app/3623200/Upalu_Mundi/) — сюжет, сітка 8×8, чотири типи стрілок «від шахтних вагонеток», симуляція на макеті, лінія оптимуму, газети й протоколи; трейлер.
- [david.reviews: огляд](https://david.reviews/articles/upalu-mundi-review/) — ~75 рівнів із «твістами», стрілки alternating та if empty, сигнали проти deadlock, рахунок (тривалість, 1g за сегмент + штрафи), ліміт 999 циклів, графік із кривою оптимуму, без undo, мемо й газети.
- [GamingOnLinux](https://www.gamingonlinux.com/2026/05/keep-goods-moving-along-the-rails-in-mini-puzzler-upalu-mundi/) — дросель запуску, газети, протоколи нарад, Linux-версія; посилання на трейлер.
- [Steam News (JSON)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3623200&count=20&maxlength=4000) — патчноути 1.0.1–1.1.6: стоп-знаки обʼєктів, вагони 2–3, станція довжиною 4, зони, UMC, рекорди лінії, масштаб пікселів, українська локалізація.
- [Трейлер](https://www.youtube.com/watch?v=gmEIGLZZX5E); YouTube: пошук «Upalu Mundi gameplay».

## Непевне
- (?) Ще два типи стрілок із чотирьох і точна поведінка alternating (перемикання після кожного потяга?) — у джерелах названо лише alternating та if empty.
- (?) Семантика стоп-знака: що означає «активний» (потяг стоїть чи проїжджає); правило 1.1.4 переказано з патчноута.
- (?) Що буває при зустрічі потягів — аварія чи очікування; огляд згадує лише «сигнали проти deadlock».
- (?) Що означає абревіатура UMC і як рахується відсоток; як будується крива оптимуму (тривалість × вартість?).
- (?) Керування: клік чи протяг, перелік гарячих клавіш, чи є покрокове виконання.
- (?) Часові межі, менші за 999 циклів, на окремих рівнях (патч 1.1: «within time limits»).
- (?) Кількість світів (щонайменше 4) і точна кількість рівнів (~75 за оглядом; рівень 74 згадано в патчі).
- (?) Чи станції будуються будь-де, чи лише біля обʼєктів; довжина станції в клітинах.
- (?) Шухляда креслень — збережені власні рішення чи заготовки рівня.
