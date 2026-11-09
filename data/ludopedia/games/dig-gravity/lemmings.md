---
title: Lemmings
slug: lemmings
aka: [Лемінги, Lemmings 1991]
family: dig-gravity
also: [grid-platformer, program-robots]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1991
platforms: [Amiga, MS-DOS, Atari ST, C64, ZX Spectrum, SNES, Mega Drive, NES, Game Boy, Lynx, 3DO, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lemmings_(video_game)", best: true, note: "вісім умінь, смерті, release rate, нюк, рейтинги Fun–Mayhem, режим на двох, порти й сиквели"}
  - {kind: other, url: "https://ar5iv.arxiv.org/html/1202.6581", note: "Viglietta «Lemmings Is PSPACE-Complete»: формальна модель — піксельний рельєф, маска сталі 4×4, падіння >63, крок <8, будівник 12×6"}
  - {kind: other, url: "https://rk.nvg.ntnu.no/sinclair/instructions/lemmdemo.html", note: "інструкція демо (ZX): панель із 12 іконок, призначення вміння кліком, клавіші"}
  - {kind: wiki, url: "https://www.c64-wiki.com/wiki/Lemmings", note: "C64: лічильники над панеллю, паролі за рейтингами, меню 1–4, нюк подвійним натиском"}
  - {kind: other, url: "https://www.lemmingsforums.net/", note: "форум спільноти: Tech & Research (фізика), NeoLemmix, Lix"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lemmings+1991+Amiga+gameplay", note: "пошук; геймплей Amiga"}
stage: v1
coverage: 60
mechanics: [gravity-fall, move-auto, turn-when-blocked, dig-terrain, dig-hole, destructible-blocks, impassable-cells, one-way-cell, bomb-fuse, explode-area, environment-death, time-out, reach-exit, collect-quota, spawn-points, spawn-schedule, cell-click, hover-highlight, game-pause, level-password, sequential-levels, difficulty-levels, status-panel, goal-counter, minimap-radar, +auto-walker-guide, +tool-allotment, +place-bridge, +fall-height-death, +assign-skill, +release-rate, +nuke-all, +pixel-terrain-mask, +trap-cooldown, +shared-field-versus]
proposes: ["+trigger:landed", "+cond:fall_height", "+effect:excavate", "+effect:rescue", "+ui:skill-counts", "+card:assign-skill", "+card:release-rate", "+card:nuke-all", "+card:pixel-terrain-mask", "+card:trap-cooldown", "+card:shared-field-versus", "+axis:field-pixel", "+axis:control", "+axis:actors"]
author: opus
date: 2026-11-09
---

# Lemmings — юрба йде сама; ти лише роздаєш уміння: копати, будувати, блокувати

## Суть
Із люка безперервно виходять лемінги й тупо крокують уперед: падають з уступів, розвертаються біля стін, гинуть у воді й пастках. Гравець не керує жодним із них напряму — він **курсором призначає окремим лемінгам уміння** з обмеженого запасу рівня (вісім типів: копати вниз, вбік, по діагоналі, будувати сходи, блокувати, лазити, планерувати, вибухнути) і так перекроює рельєф і маршрут юрби. Мета — довести до виходу заданий відсоток лемінгів до кінця часу. Рельєф — піксельна маска, яку вміння вигризають і добудовують; саме це робить гру родичем Boulder Dash і falling-sand, а не лише платформерів.

## Поле і час
- Бічний вид, рівень ширший за екран; камера скролиться курсором уліво/вправо, вертикального скролу нема (?).
- Поле — **бітова маска рельєфу** (піксель = клітина: є/нема), поверх неї — **маска сталі** блоками 4×4: сталеві блоки не копаються. Окремо — обʼєкти: люк(и), вихід(и), смертельні зони (вода/лава — миттєві, пастки — з паузою після вбивства), односторонні стіни.
- Real-time: кожен лемінг — автомат зі станом (іде / падає / копає / будує / блокує…); гравцеві можна поставити паузу й роздивитися.
- Ходьба: якщо попереду підйом нижчий за поріг (у моделі — найближча порожня клітина вгорі нижче за 8), лемінг піднімається плавно; вищий — розворот. Падіння довше за поріг (у моделі >63) — смерть при приземленні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лемінг | ally | напрямок; стан-дія; постійні прапорці climber/floater | іде вперед, падає без опори, розвертається біля стіни; інших лемінгів ігнорує, крім Blocker |
| Люк (entrance) | spawner | загальна кількість; release rate 1–99 | випускає лемінгів по одному з інтервалом за release rate |
| Вихід (exit) | gate | — | лемінг, що зайшов, зникає й рахується врятованим |
| Рельєф | terrain | піксель є/нема | по ньому ходять; уміння-копачі й вибух його знищують, будівник додає |
| Сталь | static | блок 4×4 | не копається, не руйнується вибухом |
| Одностороння стіна | terrain | напрям-стрілка | у напрямку стрілки копається, у зворотному — як сталь |
| Вода, лава | hazard | затримка 0 | лемінг, що потрапив, гине |
| Пастка (давилка, вогонь тощо) | hazard | затримка після вбивства | вбиває лемінга в зоні, потім кілька тіків безпечна, поки «перезаряджається» |
| Нижній край екрана | hazard | — | падіння за край — смерть |
| Climber | — (стан лемінга) | постійний | біля стіни лізе вгору замість розвороту; під навісом падає |
| Floater | — (стан лемінга) | постійний | падає повільно з парасолькою, виживає з будь-якої висоти |
| Bomber | — (стан лемінга) | відлік 5 с | вибухає, вигризаючи довкола рельєф (не сталь); інших лемінгів і пастки не вбиває |
| Blocker | — (стан лемінга) | постійний | стоїть; ходоки, будівники, шахтарі, що торкнулися, розвертаються; зняти — лише вбити або підкопати |
| Builder | — (стан лемінга) | 12 цеглин | кладе сходинки (цеглина 1 px заввишки, 6 завширшки) вгору-вперед; стоп — стеля, кінець цеглин, перешкода |
| Basher | — (стан лемінга) | — | б'є тунель горизонтально; стоп — вийшов у порожнечу, сталь, падіння |
| Miner | — (стан лемінга) | — | копає тунель по діагоналі вниз; сталь зупиняє |
| Digger | — (стан лемінга) | — | копає шахту прямо вниз; сталь зупиняє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(release_interval)` → ЯКЩО `counter(released, <, total)` → ТО `spawn_at(lemming, entrance)`, `counter(released, +1)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, walker)` and `free(ahead)` → ТО `move(lemming, facing)`; підйом нижчий за поріг → `custom: «піднятися на сходинку»`.
- КОЛИ `blocked(lemming)` → ЯКЩО `not state(lemming, climber)` → ТО `face(lemming, reverse)`; climber → `custom: «лізе вгору по стіні; навіс → падає»`.
- КОЛИ `tick` → ЯКЩО `not supported(lemming)` → ТО `fall(lemming)`; floater → `custom: «повільне падіння з парасолькою»`.
- КОЛИ `custom: «лемінг приземлився»` → ЯКЩО `custom: «висота падіння > поріг»` and `not state(lemming, floater)` → ТО `disappear`, `counter(dead, +1)`.
- КОЛИ `input(skill, lemming)` → ЯКЩО `counter(skill_left, >, 0)` and `custom: «лемінг може прийняти вміння (не падає для копачів, ще не має прапорця)»` → ТО `set_state(lemming, skill)`, `counter(skill_left, -1)`.
- КОЛИ `contact(walker|builder|miner, blocker)` → ТО `face(a, reverse)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, builder)` and `counter(bricks, >, 0)` → ТО `set_cell(brick_row, terrain)`, `move(lemming, step_up)`, `counter(bricks, -1)`; стеля / перешкода / 0 цеглин → `set_state(lemming, walker)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, basher)` and `not cell(ahead, steel)` → ТО `custom: «вигризти удар тунелю вперед»`, `move(lemming, facing)`; попереду порожнеча або сталь → `set_state(lemming, walker)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, miner)` and `not cell(diag_down, steel)` → ТО `custom: «вигризти крок по діагоналі вниз-вперед»`; сталь → `set_state(lemming, walker)`.
- КОЛИ `tick` → ЯКЩО `state(lemming, digger)` and `not cell(below, steel)` → ТО `set_cell(below, empty)`, `move(lemming, down)`; під ним порожнеча → `fall`.
- КОЛИ `custom: «копач б'є в односторонню стіну проти стрілки»` → ТО `block`, `set_state(lemming, walker)`.
- КОЛИ `input(bomber, lemming)` → ТО `set_state(lemming, countdown, 5s)`; КОЛИ `state_off(lemming, countdown)` → ТО `explode(circle, into: empty)` (крім сталі), `disappear`.
- КОЛИ `custom: «рельєф під Blocker прибрано»` → ТО `fall(blocker)`, `set_state(blocker, walker)` (?).
- КОЛИ `enter(lemming, water|lava)` → ТО `disappear`, `counter(dead, +1)`.
- КОЛИ `enter(lemming, trap)` → ЯКЩО `not state(trap, rearming)` → ТО `disappear`, `set_state(trap, rearming, delay)`.
- КОЛИ `edge(lemming)` (низ) → ТО `disappear`, `counter(dead, +1)`.
- КОЛИ `enter(lemming, exit)` → ТО `disappear`, `counter(saved, +1)`.
- КОЛИ `input(release_plus|release_minus)` → ЯКЩО `custom: «нове значення між мінімумом рівня і 99»` → ТО `counter(release_rate, ±1)`.
- КОЛИ `input(nuke)` → ТО `custom: «усі лемінги на полі й ще не випущені стають Bomber; випуск припиняється»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «усі лемінги на полі вибухають»`, `window(end-screen)`.
- КОЛИ `custom: «лемінгів на полі нема й люк порожній»` → ЯКЩО `counter(saved_pct, >=, target_pct)` → ТО `win`, `next_level`; інакше `lose`, `restart`.
- Перемога: врятовано ≥ заданого відсотка. Поразка: відсоток не набрано (через смерті, Blocker-ів, що лишились, або час). Рахунок: лише відсоток врятованих; очок нема (?).

## Керування і ввід
- Миша (або джойстик/клавіші): клік по іконці вміння на панелі → клік по лемінгу. Курсор над лемінгом показує його поточний стан (текст у панелі), щоб влучити в потрібного в купі.
- Мінус/плюс — release rate; не нижче стартового значення рівня, не вище 99.
- Пауза («Paws»), нюк (C64 — подвійний натиск, щоб не випадково).
- Скрол поля — курсором до краю екрана (ZX: клавіші L/Enter).
- Керування **непряме**: гравець ніколи не задає напрямок руху — лише змінює стан однієї сутності з юрби в потрібний момент. Головна навичка — таймінг і вибір конкретного лемінга.

## Вікна, меню, HUD
- `main-menu`: 1 гравець · 2 гравці · пароль (`level-password`) · музика/звуки · вибір рейтингу (Fun/Tricky/Taxing/Mayhem — `difficulty-select`).
- `custom-window` «брифінг рівня»: номер і назва, кількість лемінгів, % до порятунку, release rate, час, рейтинг (?).
- `game-screen`: поле зі скролом + нижня панель: рядок стану (тип лемінга під курсором, OUT — на полі, IN — врятовано, у % , `timer-countdown`) і 12 кнопок: −/+ release rate, вісім умінь з лишком на кожній (`ability-buttons` з числом), пауза, нюк; праворуч `minimap` рівня (?).
- `end-screen` «підсумок»: врятовано X % при потрібних Y %; при успіху — пароль наступного рівня; повтор / далі (?).
- `game-screen` двох гравців: екран навпіл по вертикалі, у кожного своя панель і свої лемінги кольору.
- Переходи: main-menu → брифінг → game-screen → підсумок → брифінг наступного або той самий рівень.

## Фічі поза полем
- `levels-sequential` у чотирьох рейтингах-складностях (120 рівнів Amiga-версії); рейтинг відображає перешкоди, набір умінь, час, мінімальний release rate і % порятунку.
- `level-password` на кожен рівень (C64: таблиця на рейтинг).
- `pause`; аварійний вихід із рівня — нюк.
- `local-multiplayer`: 20 рівнів на двох, дві миші (Amiga) або миша+джойстик (ST); кожен призначає вміння лише своїм лемінгам, але в базу можна завести будь-яких; хто завів більше — перемагає; рівні по колу, доки ніхто нікого не заведе.
- Ремейк PSP (2006) — `level-editor` і обмін рівнями; фанатські двіжки NeoLemmix і Lix — редактори, мультиплеєр.
- `custom-rules` неявно: кожен рівень — свій набір дозволених умінь і їх кількості, тобто «правила» гри задаються рівнем.

## Варіації й родичі
- Продовження: Oh No! More Lemmings (100 рівнів, 5 нових рейтингів), Christmas Lemmings, Lemmings 2: The Tribes (12 племен і десятки умінь (?)), All New World of Lemmings, 3D Lemmings, Lemmings Revolution, Lemmings Touch; фанатські Lix (мультиплеєр) і NeoLemmix.
- Родичі в корпусі: [Troddlers](../grid-platformer/troddlers.md) і [Krusty's Fun House](../grid-platformer/krustys-fun-house.md) (автоходці + аватар), [Toki Tori](../grid-platformer/toki-tori.md) (обмежені інструменти на рівень), [Pushover](../grid-platformer/pushover.md) (підготуй і дивись), [Survivors](survivors.md) (дроїди з різними вміннями), [Noita](noita.md) (піксельний рельєф), [Dig Dug](dig-dug.md) і [Boulder Dash](boulder-dash.md) (копання як основа).
- **Осі варіацій**: керування — «аватар (Troddlers) / роздача умінь (Lemmings) / лише будуєш середовище (Krusty)»; вміння — «одноразова дія / постійний прапорець (climber, floater)»; рельєф — «тайли / піксельна маска / маска + сталь»; ціль — «% порятунку / усіх / знищити (Krusty)».
- Складність: розвʼязність рівня PSPACE-повна навіть для одного лемінга з будівниками й копачами без ліміту (Viglietta, 2012) — приклад «проста механіка — важка задача».

## Цікавинки для курсу
- Автоходець-автомат «іде → падає → розвертається» з порогом сходинки й висоти падіння — 🥉: скінченний автомат на піксельній масці.
- Призначення вміння сутності з юрби кліком (з лічильником на кнопці й умовою «чи може прийняти») — 📎.
- Будівник: сходинки з цеглин зі стопом за трьома умовами — 🥉; басер/шахтар/копач — одна механіка «вигризти форму в напрямку» з трьома векторами — 🥉 за сімʼю.
- Маска сталі й одностороння стіна як другий шар над рельєфом — 📎.
- Release rate як ручка темпу спавну + нюк як «аварійна кнопка» — 🌱 кожне.
- Відсоток порятунку як ціль (а не «всі») — 🌱; дає простір для жертв (Blocker, Bomber).
- Розвʼязувач рівня Lemmings — 👑: доведено PSPACE-повноту, лише перебір з евристиками.

## Мапа на каталог
- Є: `gravity-fall` ↔ падіння лемінгів · `move-auto` ↔ хода без вводу · `turn-when-blocked` ↔ розворот біля стіни · `dig-terrain` ↔ басер/копач · `dig-hole` ↔ шахтар по діагоналі · `destructible-blocks` ↔ рельєф під вибухом · `impassable-cells` ↔ сталь · `one-way-cell` ↔ одностороння стіна (тут — для копання, не для ходи) · `bomb-fuse` + `explode-area` ↔ Bomber · `environment-death` ↔ вода, лава, пастки, падіння · `time-out` · `reach-exit` + `collect-quota` ↔ % до виходу · `spawn-points` + `spawn-schedule` ↔ люк і release rate · `cell-click` + `hover-highlight` ↔ клік по лемінгу, стан під курсором · `game-pause` · `level-password` · `sequential-levels` + `difficulty-levels` ↔ рейтинги · `status-panel` + `goal-counter` · `minimap-radar`.
- **Нема** → пропозиції карток:
  - `+auto-walker-guide` (з Troddlers/Krusty) — тут {control: assign-skill, quota: percent}.
  - `+tool-allotment` (з Toki Tori) — вісім лічильників умінь на рівень.
  - `+place-bridge` (з Toki Tori) — тут будівник сходинками, 12 цеглин.
  - `+fall-height-death` (з Leap Year) — поріг висоти; floater скасовує.
  - `+assign-skill` «Призначити вміння сутності з юрби» · entities/state · 📎 · слоти {skills, permanent?} — змінює автомат поведінки однієї сутності.
  - `+release-rate` «Ручка темпу спавну» · entities/spawn · 🌱 · слоти {min, max} — гравець прискорює/сповільнює генератор у межах.
  - `+nuke-all` «Нюк: усі підриваються» · game-logic/lose · 🌱 — аварійне завершення рівня.
  - `+pixel-terrain-mask` «Рельєф як бітова маска + маска незнищенного» · entities/interact · 🥈 · слоти {steel_block} — копання формою, а не клітиною.
  - `+trap-cooldown` «Пастка перезаряджається після вбивства» · entities/state · 🌱 · слот {delay}.
  - `+shared-field-versus` «Двоє на спільному полі, кожен зі своїми юнітами» · game-logic/opponent · 🥉 — розділений екран, переманювати чужих.

## Пропозиції до словників
- `+trigger:landed` — сутність приземлилась після падіння (тут — перевірка висоти); повтор з Troddlers/Leap Year.
- `+cond:fall_height(a, op, n)` — висота падіння порівняно з N; повтор з Leap Year.
- `+effect:excavate(a, shape, dir)` — вигризти форму рельєфу в напрямку (басер, шахтар, копач; вибух — `explode`).
- `+effect:rescue` — сутність іде у вихід і рахується врятованою (не `pickup`); повтор з Survivors.
- `+ui:skill-counts` — кнопки умінь з лишком на кожній (варіант `ability-buttons` без cooldown).
- `+card:assign-skill`, `+card:release-rate`, `+card:nuke-all`, `+card:pixel-terrain-mask`, `+card:trap-cooldown`, `+card:shared-field-versus` — див. «Мапа на каталог».
- `+axis:field-pixel` — поле-маска пікселів (повтор з Noita); у шапці `square` як найближче.
- `+axis:control` = `indirect` (призначення умінь, не напрямок); `+axis:actors` = `swarm`.

## Джерела
- ⭐ [Wikipedia: Lemmings](https://en.wikipedia.org/wiki/Lemmings_(video_game)) — вісім умінь, поведінка за замовчуванням, причини смерті, release rate 1–99, нюк, рейтинги, режим на двох, 120 рівнів, порти, сиквели.
- [Viglietta: Lemmings Is PSPACE-Complete](https://ar5iv.arxiv.org/html/1202.6581) — формальна модель: рельєф-клітини, сталь блоками 4×4, односторонні стіни, пастки з затримкою, падіння >63, крок <8, будівник 12 цеглин 6×1, басер 5 клітин за удар; складність.
- [ZX demo instructions](https://rk.nvg.ntnu.no/sinclair/instructions/lemmdemo.html) — 12 іконок панелі, «вибери іконку → клікни лемінга», Blocker знімається лише бомбою, клавіші.
- [C64-Wiki: Lemmings](https://www.c64-wiki.com/wiki/Lemmings) — рядок стану над панеллю, лічильник на кожному вмінні, паролі за рейтингами, меню, нюк подвійним натиском.
- [Lemmings Forums](https://www.lemmingsforums.net/) — спільнота: Tech & Research, NeoLemmix, Lix.

## Непевне
- (?) Числа порогів (падіння >63, крок <8, сталь 4×4, басер 5 за удар) — з формальної моделі Viglietta, що «зберігає механіку оригіналу»; одиниця — піксель DOS/Amiga-версії, у портах може відрізнятись.
- (?) Мінімапа праворуч на панелі, брифінг-екран із переліком параметрів і підсумковий екран з паролем — з памʼяті про Amiga/DOS; у відкритих джерелах не описані.
- (?) Вертикального скролу немає — з памʼяті.
- (?) Blocker, під яким підкопали, падає й знову стає ходоком — модель каже лише «знімається вбивством або розкопуванням клітини».
- (?) Climber+Floater разом («athlete») — пізніша назва, не з оригіналу.
- (?) Lemmings 2: кількість умінь і племен — з памʼяті.
- (?) Формула «release rate → інтервал спавну» не знайдена; рахунку в очках, найімовірніше, нема.
