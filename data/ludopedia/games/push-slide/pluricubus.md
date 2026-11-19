---
title: Pluricubus
slug: pluricubus
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4866150/Pluricubus/", best: true, note: "опис: рух обертанням полікуба, спецплитки (обмежують рух, кришаться, додають і забирають кубики), кілька фігур одночасно, 3D-рівні по стінах і стелі, телепорт і зміна форми; 11 наборів, 200+ рівнів, редактор, Time Trial, Tile Fix; трейлер і 6 знімків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pluricubus+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, multi-cell-size, orientation-state, reach-exit, gravity-fall, environment-death, teleport, one-way-cell, restart-level, sequential-levels, level-select, in-game-editor, level-exchange, score-records, move-counter, movement-animation, particles, background-music, volume-control, +roll-block, +crumbling-floor, +add-remove-cubes, +sync-avatars, +surface-crawler, +hex-grid-render, +time-trial, +tile-fix-mode, +physics-mode]
proposes: ["+effect:tumble", "+feature:physics-mode", "+feature:tile-fix", "+card:add-remove-cubes", "+card:sync-avatars", "+card:tile-fix-mode", "+card:physics-mode"]
author: opus
date: 2026-11-19
---

# Pluricubus — перекочуй полікуб до виходу, не впавши з краю: плитки додають і забирають кубики, а в 3D-рівнях котишся по стінах і стелі

## Суть
Гравець рухає не героя, а **полікуб** — фігуру з кількох кубиків: кожен хід перекидає її на 90° через нижнє ребро. Мета рівня — дістатися виходу й не зірватися з плиток у порожнечу. Набір Classic — це по суті [Bloxorz](bloxorz.md) (брусок 1×1×2 у дірку), решта 10 наборів додають довільні полікуби, спецплитки, кілька фігур одним вводом і рівні зі стінами й стелею.

Спецплитки, за описом Steam, обмежують рух, кришаться, додають або забирають кубики; ще є телепорт і зміна форми. Окремий перемикач **Physics Mode** (Realistic / Strict / Relaxed) видно в HUD — найімовірніше, він задає правило опори (?). Інді-гра студії Integral Horse Domain, реліз 2 листопада 2026.

## Поле і час
- Плитки-клітини висять над порожнечею; фігура — набір кубиків 1×1×1 зі своєю висотою, тому стан = позиції кубиків + орієнтація граней. Більшість рівнів — квадратна сітка на одному рівні висоти (`field: 3d` — через полікуби й 3D-набори).
- 3D-набори: плитки є й на стінах та стелі, фігура перекочується на них («movement along walls and ceilings»). Окремі набори в оточенні колізею — **гекс-рівні**: фігура з шестигранних призм на гекс-колонах (зі знімків; правило перекидання — (?)).
- Камера — ізометрична 3D (тег Steam «Isometric»), рівень видно цілком; 5 оточень зі своєю музикою: неонова сітка, колізей, річка, космос із Сатурном, майстерня.
- Хід = одне перекидання; без вводу світ стоїть (категорія Steam «Playable without Timed Input»). Таймер у HUD — лише метрика, а в Time Trial — ліміт серії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Полікуб | player | набір кубиків; орієнтація; у деяких наборах грані підписані «1-U … 6-D» | перекидається через нижнє ребро в бік вводу; змінює форму на спецплитках |
| Кілька фігур (Multi, Three) | player | 2–3 окремі полікуби | рухаються одним вводом одночасно; можуть стояти на окремих платформах |
| Звичайна плитка | terrain | — | опора |
| Порожнеча | hazard | — | без опори фігура падає — спроба провалена |
| Вихід | terrain | — | мета рівня; у Classic — квадратна дірка, куди брусок падає стоячи (з трейлера) |
| Крихка плитка | terrain | — | «crumble away»: зникає після використання (?) — у річковому світі, ймовірно, брунатні земляні плитки |
| Плитка «+кубик» | terrain | — | додає кубик до фігури (бірюзові іскри в трейлері) |
| Плитка «−кубик» | terrain | — | забирає кубик (червоні іскри; фігура меншає) |
| Плитка-обмежувач | terrain | позначка-трикутник | «restrict your movement» — забороняє частину напрямків (?) |
| Телепорт | terrain | пара (?) | переносить фігуру (червоні / сині спіралі на знімках (?)) |
| Плитка зміни форми | terrain | — | «change shape» (?) — жовті іскри на плитках із «X» у трейлері |
| Стіни й стеля з плитками | terrain | — | у 3D-наборах — опора на бічних і верхніх гранях |
| Плитки «MOV», «PSH», підписи граней | mark | текст на плитці | набори Floating і Odd; правило не підтверджене (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `custom: «перекинути фігуру на 90° через нижнє ребро в бік dir»`, `counter(moves, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `count(shape, >, 1)` → ТО той самий `custom: «перекинути»` для кожної фігури одночасно.
- КОЛИ `after(перекидання)` → ЯКЩО `not supported(shape)` (за правилом поточного Physics Mode) → ТО `fall(shape)`, `lose`, `restart` (?) — у трейлері фігура зривається з краю, далі кадр рівня з початку.
- КОЛИ `enter(shape, exit)` → ЯКЩО `custom: «фігура стала на вихід так, як вимагає рівень»` (?) → ТО `win`, `next_level`.
- КОЛИ `enter(shape, add_tile)` → ТО `grow(shape, 1)`.
- КОЛИ `enter(shape, remove_tile)` → ТО `shrink(shape, 1)`.
- КОЛИ `leave(shape, crumbling_tile)` → ТО `set_cell(crumbling_tile, void)` (момент руйнування — (?)).
- КОЛИ `enter(shape, teleport)` → ТО `teleport(shape, pair)` (?).
- КОЛИ `input(dir)` → ЯКЩО `cell(under_shape, restrict_tile)` і `custom: «dir заборонено плиткою»` → ТО `block` (?).
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду стіна з плиток»` (3D-набір) → ТО `custom: «перекотитися на стіну; опорою стає її грань»`.
- КОЛИ `enter(shape, shape_tile)` → ТО `transform(shape, new_shape)` (?).
- Time Trial: КОЛИ `level_end` → ТО `next_level` серії.
- Time Trial: КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`, `score(levels_solved)`.
- Tile Fix: КОЛИ `level_start` → ТО `custom: «частину плиток рівня прибрано в запас»`.
- Tile Fix: КОЛИ `input(place)` → ЯКЩО `has(supply, tile)` → ТО `place(tile)`.
- Tile Fix: КОЛИ `level_end` → ТО `score(+tiles_left_in_supply)`.
- КОЛИ `level_end` → ТО `custom: «зберегти найкращий час і найменшу кількість ходів рівня»`.
- Перемога: фігура (усі фігури (?)) на виході. · Поразка: фігура без опори падає. · Рахунок: найкращий час і найефективніший розвʼязок на рівень; у Tile Fix — невикористані плитки; у Time Trial — пройдені рівні за ліміт.

## Керування і ввід
- Кожен ввід напрямку перекидає фігуру (на квадратних рівнях — 4 боки; на гекс-рівнях — (?)); конкретні клавіші в джерелах не названі (?).
- Кнопки HUD Back · Reset · Info · Menu клікабельні; Back — ймовірно, крок назад (?).
- Камера 3D з налаштуваннями (категорія Steam «Camera Comfort»); геймпад у категоріях Steam не заявлено.
- Tile Fix: гравець сам ставить вилучені плитки — як саме (курсором, до чи під час проходження) — (?).

## Вікна, меню, HUD
- `splash-screen` — неонова назва PLURICUBUS у квадратній рамці (трейлер).
- `game-screen`: 3D-поле в оточенні набору. HUD: угорі ліворуч кнопки Back · `restart-button` (Reset) · Info · Menu; унизу ліворуч напис «Physics Mode: Realistic / Strict / Relaxed» (картка каталогу `mode-indicator`); унизу посередині — назва набору й номер (`level-number`: «Floating 7», «Classic 14»); унизу праворуч `move-counter` («10 Moves») і `timer-elapsed` («1:26»).
- `level-select` / `chapter-select`: 11 наборів (Classic, Square, Adding, Floating, Corner, Three, Multi, 3D, Odd та інші (?)).
- `mode-select`: звичайне проходження · Time Trial · Tile Fix (?).
- `editor-window` — вбудований редактор рівнів.
- `settings-window` — гучність окремо (категорія «Custom Volume Controls»), камера (?).
- `achievements-window` — 22 досягнення Steam; `stats-window` — Steam Stats.
- Переходи: splash → меню → вибір набору й рівня → game-screen → (вихід) наступний рівень; (падіння) рестарт рівня (?).

## Фічі поза полем
- `levels-sequential` у 11 наборах, понад 200 рівнів; набір = окреме оточення й нова ідея.
- `level-editor` + `level-sharing` («craft your own levels and share them with your friends»; спосіб обміну — (?)).
- `stats`: для кожного рівня — найкращий час і найефективніший розвʼязок.
- `mode-time-attack` (Time Trial): пройти якомога більше рівнів за обмежений час.
- `+feature:tile-fix`: частину плиток вилучено, гравець повертає їх сам, рахунок — за невикористані.
- `+feature:physics-mode`: три правила опори (Realistic / Strict / Relaxed) як налаштування (?).
- `achievements` (22), `volume-sliders`, безкоштовне демо в Steam.

## Варіації й родичі
- [Bloxorz](bloxorz.md) — набір Classic: той самий брусок 1×1×2 і квадратна дірка; там же Cuboid та Edge.
- [Kula World](../grid-platformer/kula-world.md) і [Spacecaps](spacecaps.md) — рух по бічних і нижніх гранях з поворотом «низу».
- [Tome Tumble Tournament](../thinky/tome-tumble-tournament.md) — блок, що перекидається, з гранями різного змісту.
- [English Country Tune](../thinky/english-country-tune.md) — хода гранями 3D-структури.
- Осі варіацій:
  - **форма**: брусок 1×1×2 / довільний полікуб / фігура з гекс-призм;
  - **опора**: усі нижні кубики / центр мас / хоч один кубик (ймовірний зміст Physics Mode (?));
  - **скільки фігур**: одна / кілька одним вводом (Multi) / кілька з перемиканням (Bloxorz після розщеплення);
  - **поверхні**: лише підлога / стіни й стеля;
  - **форма змінюється**: ніколи / плитками ±кубик / розщепленням.

## Цікавинки для курсу
- Перекидання довільного полікуба через нижнє ребро: поворот кожного кубика на 90° навколо ребра в 3D — 🥉 (геометрія повороту й пошук ребра опори).
- Правило опори з трьох режимів (усі нижні кубики / центр мас над плитками / хоч один) як перемикач — 🥈 (центр мас полікуба й перетин з опорою).
- Плитки ±кубик: фігура росте й меншає, а з нею змінюється, як вона котиться — 🥉.
- Кілька фігур одним вводом; падіння будь-якої — провал (?) — 📎.
- Tile Fix: мінімум плиток, щоб рівень лишився прохідним, — 🥇 (пошук по станах фігури × вибір плиток).
- Розвʼязувач BFS для полікуба (стан = множина кубиків + орієнтація) — 🥇.
- 3D-рух по стінах і стелі зі зміною «низу» — 🥇.

## Мапа на каталог
- Є: `move-by-input` ↔ перекидання за вводом; `multi-cell-size` ↔ полікуб на кількох клітинах; `orientation-state` ↔ грані фігури (у деяких наборах підписані); `reach-exit` ↔ вихід; `gravity-fall` + `environment-death` ↔ падіння з краю; `teleport` ↔ телепорт; `one-way-cell` ↔ плитки, що обмежують рух (?); `restart-level` ↔ Reset; `sequential-levels` + `level-select` ↔ 11 наборів; `in-game-editor` + `level-exchange` ↔ редактор і обмін рівнями; `score-records` ↔ найкращий час і розвʼязок; `move-counter` ↔ «N Moves»; `movement-animation`, `particles` ↔ плавне перекидання й іскри на спецплитках; `background-music`, `volume-control` ↔ саундтрек оточень і гучність.
- **Нема** → пропозиції карток:
  - `+roll-block` (уже пропонована, Bloxorz) — перекидання з грані на грань, тут для довільного полікуба.
  - `+crumbling-floor` (уже пропонована) — плитка кришиться.
  - `+add-remove-cubes` «Плитка додає або забирає кубик фігури» · entities/state · 🥉.
  - `+sync-avatars` «Один ввід рухає кілька аватарів одночасно» · entities/move · 📎 (родич `+twin-boards`).
  - `+surface-crawler` (уже пропонована) — рух по стінах і стелі.
  - `+hex-grid-render` (уже пропонована) — гекс-набори.
  - `+time-trial` (уже пропонована, Flow Free) — серія рівнів на таймер.
  - `+tile-fix-mode` «Полагодь поле: вилучені плитки ставить гравець, рахунок за невикористані» · levels/progression · 🥈.
  - `+physics-mode` «Перемикач правила опори фігури» · game-logic/difficulty · 🥉.

## Пропозиції до словників
- `+effect:tumble` — перекинутися через нижнє ребро на 90° (полікуб, брусок Bloxorz); не плутати з `roll` (скочування з округлого).
- `+feature:physics-mode` — налаштування, що змінює правило опори (Realistic / Strict / Relaxed).
- `+feature:tile-fix` — режим, де частину поля прибрано й гравець сам її відновлює.
- `+card:add-remove-cubes`, `+card:sync-avatars`, `+card:tile-fix-mode`, `+card:physics-mode` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Pluricubus](https://store.steampowered.com/app/4866150/Pluricubus/) — опис механік і режимів, 11 наборів і 200+ рівнів, редактор, рекорди рівня, 5 оточень, категорії Steam (22 досягнення, Stats, «Playable without Timed Input», «Camera Comfort»); 6 знімків і трейлер (переглянуто покадрово: набори Classic, Square, Adding, Floating, Corner, Three, Multi, 3D, Odd; іскри на плитках ±кубик, падіння з краю, гекс-рівні, HUD).
- YouTube: пошук «Pluricubus gameplay».

## Непевне
- (?) Зміст Physics Mode (Realistic / Strict / Relaxed) — гіпотеза «правило опори»; чи це налаштування гравця, чи властивість рівня — у трейлері різні рівні показують різні режими.
- (?) Як саме треба стати на вихід полікубом (кубик над виходом, уся фігура, стоячи); чи мають вийти всі фігури в Multi.
- (?) Значення плиток: трикутники (обмежувач напрямку?), «X» (кришиться чи змінює форму?), «MOV» / «PSH», підписи граней «1-U … 6-D» і плитки «4-L», «3-F»; які спіралі — телепорт, а які — вихід.
- (?) Правило перекидання на гекс-рівнях і кількість напрямків.
- (?) Клавіші керування, чи Back — це undo, як поширюються рівні з редактора, як ставити плитки в Tile Fix.
- (?) Гра вийшла 2.11.2026: відгуків і вікі ще нема, усе поза описом Steam виведено з кадрів трейлера й знімків.
