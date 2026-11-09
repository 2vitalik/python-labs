---
title: Railway Islands - Puzzle (+ Railway Islands 2)
slug: railway-islands
aka: [Railway Islands, Railway Islands 2 - Puzzle]
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: hex
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2021
platforms: [PC (Steam), Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1807930/Railway_Islands_Puzzle/", best: true, note: "Rising Moon Games, 18.11.2021: безпечний шлях через станції, 50 островів у 4 середовищах, лише мишка, редактор і Workshop; трейлер і скріншоти"}
  - {kind: steam, url: "https://store.steampowered.com/app/2621900/Railway_Islands_2_Puzzle/", note: "сиквел 20.11.2023: 40 островів, редактор рівнів, Workshop"}
  - {kind: other, url: "https://steamcommunity.com/app/1807930/reviews/?browsefilter=toprated&filterLanguage=english", note: "відгуки: обмін і поворот гексів, стрілки й знаки з числами на стрілках, кнопка запуску, аварія без скидання розкладки, 2× швидкість, 50 рівнів"}
  - {kind: other, url: "https://steamcommunity.com/app/2621900/reviews/?browsefilter=toprated&filterLanguage=english", note: "відгуки на сиквел: кілька потягів і тунелів, кольоровий вантаж, висоти, рампи, мости, ручні стрілки, автосейв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Railway+Islands+Puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [tile-rotate, pipe-connectors, cell-click, selection-highlight, hover-highlight, impassable-cells, item-pickup, collect-all, reach-exit, move-auto, goal-counter, restart-level, sequential-levels, level-unlock, level-select, in-game-editor, editor-palette, editor-playtest, level-exchange, save-autosave, field-scaling, movement-animation, game-screen, main-menu, editor-window, achievements-window, +hex-grid-render, +tile-swap, +run-simulation, +junction-toggle, +switch-pass-counter, +train-crash, +crash-keeps-layout, +speed-control, +bridge-cell, +multi-train, +color-matched-cargo]
proposes: ["+effect:toggle_junction", "+cond:ports_match", "+ui:run-button", "+ui:cargo-strip", "+ui:switch-pass-sign", "+card:tile-swap", "+card:switch-pass-counter", "+card:crash-keeps-layout"]
author: opus
date: 2026-11-09
---

# Railway Islands — переставляй і крути гекси з коліями, щоб потяг обʼїхав усі станції острова й пірнув у вихідний тунель

## Суть
Затишна головоломка Rising Moon Games: острів складено з гексів, на багатьох — шматки колії. Гравець **міняє гекси місцями** і **повертає** їх, щоб з тунелю-входу через усі станції з вантажем вела цілісна колія до тунелю-виходу. Потім натискає кнопку — потяг їде сам; зіткнувся чи злетів з колії — розкладка лишається, правиш і запускаєш знову. Від Pipe Mania / Infinity Loop відрізняється тим, що шматки не лише крутяться, а й переставляються, а стрілки на колії перемикаються за кількістю проходів.

## Поле і час
- Гекс-сітка, острів довільної форми серед води, ізометричний вигляд; камера панорамується й наближається.
- Шари гекса: рельєф (трава, скелі, ліс, лід, місто), колія (пряма, дуга, хрестовина, стрілка, рампа/міст), обʼєкти (тунелі, станції з вантажем); у сиквелі — висоти рельєфу.
- Дві фази: **розкладка** (статична, без часу) → **запуск** (потяг рухається тіками по колії; `time: programmed`); паузи під час руху нема, у Railway Islands 1 додали 2× швидкість.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гекс з колією | tile | форма колії, поворот | міняється місцями з іншим гексом; повертається колесом миші |
| Хрестовина | tile | — | дві колії перетинаються; потяг їде прямо |
| Стрілка (розвилка) | switch | стрілка напрямку | перший прохід — за стрілкою; далі перемикається (?) |
| Знак stop/go з числом | switch | N | скільки проходів потрібно, щоб стрілка перемкнулась (RI1) |
| Рампа / міст | tile | висота | колія проходить над іншою колією |
| Скеля / гора | static | — | непрохідний гекс без колії |
| Ліс, місто | static | — | декор; чи можна переставляти — (?) |
| Тунель-вхід (червона арка) | source | 1 або кілька (RI2) | звідси виїжджає потяг після запуску |
| Тунель-вихід (синя арка) | sink | — | мета: заїхати сюди з усім вантажем |
| Станція з вантажем | pickup | значок вантажу; колір (RI2) | потяг, що проїхав крізь неї, забирає вантаж |
| Потяг | object | колір (RI2) | їде сам по колії до краю шматка й далі в сусідній гекс |
| Небезпечні гекси | hazard | — | на деяких рівнях підривають потяг (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Розкладка:
- КОЛИ `input(click, tile_a)` → ЯКЩО `not state(tile_a, fixed)` → ТО `set_state(tile_a, selected)`.
- КОЛИ `input(click, tile_b)` → ЯКЩО `state(tile_a, selected)` and `not state(tile_b, fixed)` → ТО `swap(tile_a, tile_b)`.
- КОЛИ `input(wheel, tile)` → ЯКЩО `not state(tile, fixed)` → ТО `rotate(tile, 60)`.
- RI2: КОЛИ `input(click, switch)` → ТО `custom: «вручну задати гілку стрілки»` (+effect:toggle_junction).

Запуск:
- КОЛИ `input(launch)` → ТО `spawn_at(train, entry_tunnel)`, `custom: «перехід до фази руху»`.
- КОЛИ `tick` → ЯКЩО `custom: «колія виходить з гекса через порт, і сусідній гекс має зустрічний порт»` (+cond:ports_match) → ТО `move(train, along_track)`.
- КОЛИ `tick` → ЯКЩО `not custom: «зустрічний порт є»` → ТО `crash`, `lose` — колія обірвалась або потяг злетів.
- КОЛИ `enter(train, switch)` → ЯКЩО `counter(passes, <, n_sign)` → ТО `move(train, arrow_dir)`; інакше `custom: «стрілка перемкнулась — інша гілка»` (+effect:toggle_junction) (?).
- КОЛИ `enter(train, crossing)` → ТО `move(train, straight)`.
- КОЛИ `enter(train, station)` → ЯКЩО `state(station, has_cargo)` → ТО `pickup(train, cargo)`, `counter(cargo_left, -1)`.
- RI2: КОЛИ `enter(train, station)` → ЯКЩО `same(train, cargo, color)` → ТО `pickup(train, cargo)` — червоний потяг бере лише червоний вантаж, синій — синій.
- RI2: КОЛИ `contact(train_a, train_b)` → ТО `crash` (?).
- КОЛИ `enter(train, exit_tunnel)` → ЯКЩО `counter(cargo_left, ==, 0)` → ТО `win`, `next_level`; інакше `lose` (?).
- КОЛИ `custom: «аварія»` → ТО `restart` — розкладка гексів лишається як була (RI1; RI2 — «перезавантажує останні зміни»).
- Перемога: усі вантажі зібрано, усі потяги у своїх тунелях · Поразка: аварія → повтор без втрати розкладки · Рахунку нема.

## Керування і ввід
- Лише миша: ЛКМ — вибрати / обміняти гекси, колесо над гексом — повернути, СКМ — панорама.
- Запуск потяга — кнопка з паровозом (RI1) / Space (RI2); R — рестарт; W/S — зум (RI2); Esc — меню.
- Підтримка геймпада (RI1 — повна, DualShock / DualSense).

## Вікна, меню, HUD
- `main-menu`: Play → `level-select` (номери рівнів видно лише тут), налаштування (?), редактор, вихід.
- `game-screen`: острів; угорі — смуга вантажів, які треба зібрати (`+ui:cargo-strip`, `goal-counter`); ліворуч / праворуч угорі — меню й рестарт; праворуч унизу — запуск (`+ui:run-button`); на колії — знаки з числом проходів (`+ui:switch-pass-sign`); рамка підсвічує вибраний гекс (`selection-highlight`).
- `editor-window` (RI1 після оновлення, RI2): палітра гексів унизу (тунелі 1/2/3, станції, прямі, дуги, хрестовини, стрілки, рампи), угорі — додому, грати, зберегти, видалити, вибір пори року (Summer…); Workshop.
- `end-screen` — перехід до наступного острова (?).
- Переходи: main-menu → level-select → game-screen → (запуск) рух → win → наступний острів / аварія → game-screen.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 50 островів у 4 середовищах (RI1), 40 (RI2), відкриваються по одному.
- `level-editor` + `level-sharing` через Steam Workshop; `autosave` (RI2), `cloud-save`, `achievements`.
- `speed-control`: 2× (RI1, додано після релізу; у RI2 на прискоренні потяги, за відгуком, сходять з колії).
- `restart-level` без втрати розкладки — експеримент без штрафу.

## Варіації й родичі
- **Railway Islands 2 - Puzzle** (2023) — лише відмінності: кілька потягів у той самий або різні тунелі; кольорові потяги й вантажі (червоний ↔ червоний); рельєф різної висоти, рампи й мости; стрілки можна перемкнути вручну; 40 островів; автосейв.
- Корпус: [Infinity Loop](infinity-loop.md) і [Pipe Mania](pipe-mania.md) — поворот плиток з портами; [Klocki](klocki.md) — теж обмін плиток; [Trainyard](trainyard.md), [Railbound](railbound.md), [Train Valley](train-valley.md) — потяг їде після розкладки, стрілки перемикаються проходом; [Tricky Tangled Train Tracks](tricky-tangled-train-tracks.md) — колія через усі станції острова.
- Осі варіацій: **що робить гравець з колією** — малює (Trainyard) / кладе з ліміту (Railbound) / крутить (Infinity Loop) / міняє й крутить (Railway Islands) · **стрілка** — перемикається кожним проходом / після N проходів / вручну · **потягів** — один / кілька кольорових.

## Цікавинки для курсу
- Гекс-сітка з 6 портами на гекс, поворот на 60° як циклічний зсув маски портів — 📎.
- Обмін двох гексів кліком + поворот колесом — 🌱.
- Симуляція потяга по портах з детекцією обриву (аварія) і збором вантажу — 🥉.
- Стрілка з лічильником проходів (знак N) — 📎: стан на клітині, що змінює маршрут.
- Кілька кольорових потягів одночасно, зіткнення — 🥈.
- Розвʼязувач: перебір перестановок і поворотів гексів з відсіканням по портах — 🥇.
- Редактор островів з палітрою й плейтестом — 🥈.

## Мапа на каталог
- Є: `tile-rotate` + `pipe-connectors` ↔ гекси з колією; `cell-click`, `selection-highlight`, `hover-highlight`; `impassable-cells` ↔ скелі; `item-pickup` + `collect-all` ↔ вантажі; `reach-exit` ↔ вихідний тунель; `move-auto` ↔ потяг їде сам; `goal-counter` ↔ смуга вантажів; `restart-level`; `sequential-levels`, `level-unlock`, `level-select`; `in-game-editor`, `editor-palette`, `editor-playtest`, `level-exchange` ↔ Workshop; `save-autosave`; `field-scaling` ↔ зум і панорама; `movement-animation`; `game-screen`, `main-menu`, `editor-window`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+tile-swap` (Klocki) — обмін двох плиток; підтвердження.
  - `+switch-pass-counter` «Стрілка перемикається після N проходів» · entities/state · 📎 · слот {n}.
  - `+crash-keeps-layout` «Провал симуляції не скидає розкладку» · game-logic/history · 🌱.
  - `+run-simulation`, `+junction-toggle`, `+train-crash`, `+speed-control`, `+hex-grid-render`, `+bridge-cell` — підтвердження наявних пропозицій.
  - `+multi-train` «Кілька потягів в одній симуляції» · entities/move · 🥈; `+color-matched-cargo` «Потяг бере лише вантаж свого кольору» · entities/interact · 🌱.

## Пропозиції до словників
- `+effect:toggle_junction` — перемкнути гілку стрілки (підтвердження: Trainyard, Train Valley).
- `+cond:ports_match` — порт гекса стикується з портом сусіда (підтвердження: Infinity Loop, Pipe Mania).
- `+ui:run-button` — кнопка запуску симуляції (підтвердження: Trainyard, Railbound).
- `+ui:cargo-strip` — смуга значків вантажу, що лишився (угорі екрана).
- `+ui:switch-pass-sign` — знак на колії з числом проходів до перемикання.
- `+card:tile-swap`, `+card:switch-pass-counter`, `+card:crash-keeps-layout`.

## Джерела
- ⭐ [Steam: Railway Islands - Puzzle](https://store.steampowered.com/app/1807930/Railway_Islands_Puzzle/) — опис (безпечний шлях через станції, 50 островів, 4 середовища, лише миша), теги (Hex Grid, Isometric, Level Editor), скріншоти: тунелі-вхід і вихід, станції з вантажем, смуга вантажів угорі, стрілки, хрестовини, мости, знаки з числами.
- [Steam: Railway Islands 2 - Puzzle](https://store.steampowered.com/app/2621900/Railway_Islands_2_Puzzle/) — 40 островів, редактор; скріншоти редактора з палітрою гексів.
- [Відгуки Steam RI1](https://steamcommunity.com/app/1807930/reviews/?browsefilter=toprated&filterLanguage=english) — ЛКМ обмін, колесо поворот, СКМ панорама; стрілки «напрям першого проходу»; знаки stop/go з числом проходів; запуск кнопкою; аварія не скидає розкладку; 2× швидкість; 50 рівнів, level select; редактор.
- [Відгуки Steam RI2](https://steamcommunity.com/app/2621900/reviews/?browsefilter=toprated&filterLanguage=english) — кілька потягів і тунелів, кольоровий вантаж, висоти, рампи, мости, ручні стрілки, автосейв, 40 рівнів.
- YouTube: пошук «Railway Islands Puzzle gameplay».

## Непевне
- (?) Точна логіка стрілок RI1: «стрілка — напрям першого проходу», «знак з числом — скільки проходів до перемикання»; чи стрілка без знака перемикається після кожного проходу — не перевірено.
- (?) Які гекси нерухомі (скелі, тунелі, станції, ліс) і чи можна переставляти гекси без колії.
- (?) Що буває, коли потяг доїхав до виходу, не зібравши все; що саме підриває потяг на окремих рівнях.
- (?) Зіткнення потягів у RI2 — за аналогією, у відгуках не сказано.
- (?) Розробник: у розділі About — «Moraes Tecnologia LTDA», у полях Steam — Rising Moon Games.
