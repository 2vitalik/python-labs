---
title: Oxyd (+ Enigma)
slug: oxyd
aka: [Oxyd Magnum, Oxyd Extra, per.Oxyd, Oxyd 2, Enigma, Оксид]
family: connect-rotate
also: [push-slide, maze-arcade]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1990
platforms: [Atari ST, Amiga, Macintosh, MS-DOS, NeXT, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Oxyd", best: true, note: "кулька мишею, пари Oxyd-каменів, предмети, пастки, кооператив двох кульок, сиквели"}
  - {kind: official, url: "https://www.nongnu.org/enigma/", note: "Enigma — вільний клон (GPL), понад 1000 рівнів, читає рівні Oxyd"}
  - {kind: other, url: "https://github.com/Enigma-Game/Enigma", note: "репозиторій Enigma: README, doc/manual, doc/reference"}
  - {kind: other, url: "https://raw.githubusercontent.com/Enigma-Game/Enigma/master/doc/manual/enigma.texi", note: "мануал гравця Enigma: керування, мета, предмети, камені, підлоги, меню рівнів"}
  - {kind: other, url: "https://raw.githubusercontent.com/Enigma-Game/Enigma/master/doc/reference/enigma-ref.texi", note: "довідник рівнів Enigma: st_oxyd, st_laser, st_mirror та ін. — точна поведінка каменів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Enigma_(2007_video_game)", note: "Enigma: ≈2500 рівнів, par, рекорд, перемішування кольорів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Oxyd+Atari+ST+gameplay", note: "пошук; геймплей Oxyd"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Enigma+marble+game+gameplay", note: "пошук; геймплей Enigma"}
stage: v1
coverage: 50
mechanics: [beam-tracing, mirror-reflect, one-way-cell, swap-on-contact, push-object, fill-hole, destructible-blocks, bomb-fuse, item-pickup, inventory, inventory-items, inventory-duration, key-and-door, floor-types, environment-death, touch-death, player-death, respawn, checkpoint, party-switch, restart-level, level-bank, level-select, level-rating, score-records, difficulty-levels, game-pause, game-screen, main-menu, pause-menu, settings-window, help-window, language-picker, volume-control, theme-select, +marble-physics, +memory-pair-open, +pair-shuffle-on-death, +connected-block-move, +knight-move-stone, +item-mail-pipe, +laser-transforms-item, +linked-machine-coop, +copy-protection-code]
proposes: ["+axis:physics", "+trigger:beam_hit", "+effect:emit_beam", "+effect:impulse", "+effect:shuffle", "+cond:open_unpaired", "+role:actor", "+window:level-inspector", "+feature:world-record-hunt", "+card:marble-physics", "+card:memory-pair-open", "+card:pair-shuffle-on-death", "+card:connected-block-move", "+card:laser-transforms-item"]
author: opus
date: 2026-11-09
---

# Oxyd — кулька на фізиці відкриває пари однакових каменів серед лазерів, дзеркал і пасток

## Суть
Гравець мишею котить маленьку чорну кульку по полю з каменів. Мета — знайти й відкрити всі Oxyd-камені, а вони відкриваються лише парами однакового кольору/візерунку: торкнувся одного, потім не того — перший закривається. Тобто ядро — гра «Memory», розкладена по лабіринту з пастками. Між кулькою й Oxyd-ами стоять пазли: дзеркала й лазери, камені-перемикачі, ящики для мостів, предмети в інвентарі. Клас `hybrid`: `avatar` (кулька) + клітинний пазл-шар (камені, промені), фізика кульки — неперервна.

## Поле і час
- Два шари: **клітинний** (підлога на кожній клітині, на ній — предмет або камінь) і **неперервний** (актор-кулька з координатами, швидкістю, інерцією). Камені займають рівно клітину; кулька котиться між ними.
- Рівень («landscape») — одна або кілька екранних кімнат; у Oxyd екран перемикається, коли кулька доходить до краю (?).
- Real-time: миша задає прискорення кульки, а не позицію; тертя залежить від підлоги.
- Промінь лазера — клітинний: іде 4 напрямками від каменя-лазера, ламається на дзеркалах.
- Кольори Oxyd-ів призначаються на старті рівня і перемішуються при смерті (Enigma: коли вичерпано життя, рівень рестартує з перемішаними кольорами).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чорна кулька | player | швидкість, інвентар | котиться від руху миші; торкання активує камені, удар зсуває рухомі |
| Біла кулька | player | — | друга кулька в кооперативі; деякі камені реагують лише на свій колір |
| Малі білі кульки (meditation) | object | — | рухаються всі разом за мишею; мета — кожна у свою ямку |
| Oxyd-камінь | switch | колір (Enigma: 12), візерунок, стан CLOSED/OPEN/OXYDPAIR | удар відкриває; пара однакових лишається відкритою; невідповідний закриває одиночний відкритий |
| Fake-Oxyd | static | — | виглядає як Oxyd, лишається пасивним (непарна кількість) |
| Quake-Oxyd / st_quake | switch | — | удар закриває всі відкриті Oxyd-и (Enigma) |
| Bold-Oxyd | switch | — | відкриття перемішує кольори решти закритих (Enigma) |
| Magic Token | gate | код | блокує ключові проходи з 11-го рівня; знімається кодом з Oxyd Book (захист від копіювання) |
| Лазер | source (custom) | напрям 4, on/off | випромінює промінь; вмикається/вимикається/повертається сигналом (Enigma) |
| Дзеркало плоске / трикутне | object | орієнтація, прозорість, рухоме | відбиває промінь; удар кульки повертає на 90°; рухоме дзеркало ще й зсувається |
| Дерев'яний камінь (box) | object | wood / hay / rock | штовхається; у воді/прірві/болоті стає мостом |
| Swap-камінь | object | — | штовхнутий у камінь міняється з ним місцями |
| Boulder (стрілка) | object | напрям | їде за стрілкою до упору; розбиває кульку; б'ючи в Oxyd — відкриває; лазер розвертає |
| Puzzle-камені | object | звʼязність | зчеплені блоки рухаються як одне ціле; чарівна паличка підриває повний блок або зсуває ряд |
| Chess-камінь | object | колір | ходить конем у напрямку удару; рухається лише від кульки свого кольору |
| One-way камінь | gate | напрям | прохідний лише в одному напрямку |
| Mail-камінь | switch | труба | відправляє перший предмет інвентаря трубою, якщо вона вільна |
| Shogun-камені | object | розмір отвору | ставляться стопкою на сині точки (активують їх) |
| Skull / death-камінь | hazard | видимий / невидимий | розбиває кульку від дотику |
| Bumper (actorimpulse) | static | — | відштовхує кульку від свого центру |
| Breakable stone | object | flavor | розбивається за умовою flavor; laser-flavor — лише променем |
| Двері | gate | open/closed | відкриваються сигналом/ключем; відкриті пропускають промінь |
| Chameleon | static | — | маскується під підлогу, ховає предмети й кульку; пропускає промінь |
| Прихований прохід | static | — | виглядає як стіна, кулька проходить |
| Прірва (abyss) | hazard | — | кулька падає й розбивається |
| Вода, болото, сипучий пісок | hazard | — | топлять кульку; ящик робить міст |
| Підлога, що кришиться | terrain | лічильник | після кількох проїздів обвалюється |
| Лід / space | terrain | тертя | лід — мале тертя; space — тертя нема, швидкість не змінюється |
| Red floor | terrain | — | важко розігнатись і загальмувати |
| Inverse floor | terrain | — | рух миші інвертовано |
| Схил (slope) | terrain | напрям | штовхає кульку вниз схилом |
| Ямка (meditation pit) | zone | — | ціль для малої кульки |
| Прапорець чорний/білий | pickup | колір | ставить точку респавну кульки свого кольору |
| Динаміт | pickup | — | кинутий горить і вибухає; руйнує деякі камені, підпалює бомби |
| Чорна / біла бомба | pickup | сила (біла = 5 чорних) | руйнує підлогу й обʼєкти |
| Парасолька | pickup | ~10 c | неуразливість; ореол блимає останні 3 c |
| Ключ, лопата, паличка, ложка, дискета, папірець | pickup | — | відкрити двері, засипати/викопати яму, діяти на камені; папірець — текстова підказка |
| Монета, молоток, меч | pickup | — | можуть виникати з інших предметів під променем лазера |
| Coin slot | switch | час за номінал | монета вмикає на час, залежний від монети |
| Extra life | pickup | — | +1 запасна кулька |
| Yin-Yang | pickup | — | перемикає керування між чорною і білою кулькою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(mouse_move)` → ТО `custom: «додати прискорення кульці пропорційно руху миші; тертя за типом підлоги»`.
- КОЛИ `contact(marble, oxyd)` → ЯКЩО `state(oxyd, closed)` → ТО `set_state(oxyd, open)`.
- КОЛИ `state_on(oxyd, open)` → ЯКЩО `open_unpaired(other)` and `same(oxyd, other, color)` → ТО `set_state(oxyd, pair)`, `set_state(other, pair)`.
- КОЛИ `state_on(oxyd, open)` → ЯКЩО `open_unpaired(other)` and `not same(oxyd, other, color)` → ТО `set_state(other, closed)` — у пам'яті лишається лише щойно відкритий.
- КОЛИ `custom: «усі звичайні Oxyd-и у стані pair»` → ТО `win`.
- КОЛИ `all_on(small_marble, pit)` → ТО `win` (meditation-рівні).
- КОЛИ `contact(marble, quake_oxyd)` → ТО `custom: «закрити всі відкриті Oxyd-и»`.
- КОЛИ `state_on(bold_oxyd, open)` → ТО `shuffle(closed_oxyds)` — `custom: «перемішати кольори закритих»`.
- КОЛИ `contact(marble, mirror)` → ТО `rotate(mirror, 90)`; ЯКЩО `state(mirror, movable)` → ТО також `push`.
- КОЛИ `tick` → ЯКЩО `state(laser, on)` → ТО `emit_beam(laser)`: `custom: «промінь іде прямо, на дзеркалі відбивається, на sheets-дзеркалі вздовж площини проходить, на непрозорому камені зупиняється»`.
- КОЛИ `beam_hit(oxyd)` → ТО `set_state(oxyd, open)` (промінь відкриває як удар).
- КОЛИ `beam_hit(item)` → ТО `transform(item)` — `custom: «лазер перетворює предмет на інший (так зʼявляються монети, молотки, мечі)»`.
- КОЛИ `beam_hit(boulder)` → ТО `custom: «розвернути стрілку на протилежну»`.
- КОЛИ `beam_hit(laser_breakable)` → ТО `disappear_b`.
- КОЛИ `contact(marble, switch)` → ТО `custom: «надіслати сигнал цілі: on/off/turn лазера, відкрити двері»`.
- КОЛИ `contact(marble, box)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `enter(box, water)` or `enter(box, abyss)` → ТО `set_cell(cell, floor)`, `disappear_a` — міст.
- КОЛИ `contact(marble, swap_stone)` → ЯКЩО `occupied(cell_behind, stone)` → ТО `swap(swap_stone, stone)`.
- КОЛИ `contact(marble, chess_stone)` → ЯКЩО `same(marble, chess_stone, color)` → ТО `custom: «хід конем: 2 клітини в напрямку удару + 1 убік»`.
- КОЛИ `contact(marble, puzzle_stone)` → ЯКЩО `connected(puzzle_group)` → ТО `custom: «група рухається як одне ціле»`.
- КОЛИ `timer(every)` → ТО `move(boulder, dir)`; КОЛИ `contact(boulder, marble)` → ТО `lives(-1)`; КОЛИ `contact(boulder, oxyd)` → ТО `set_state(oxyd, open)`.
- КОЛИ `contact(marble, bumper)` → ТО `impulse(marble, away)`.
- КОЛИ `contact(marble, death_stone)` or `enter(marble, abyss)` or `enter(marble, water)` → ЯКЩО `not state(marble, protected)` → ТО `lives(-1)`, `respawn(marble, flag)`.
- КОЛИ `custom: «кулька проїхала по крихкій підлозі N разів»` → ТО `set_cell(cell, abyss)`.
- КОЛИ `enter(marble, inverse_floor)` → ТО `invert_controls(n)`.
- КОЛИ `contact(marble, item)` → ЯКЩО `not custom: «затиснута кнопка миші»` → ТО `pickup`.
- КОЛИ `input(left_click)` → ТО `use(marble, first_item)`; КОЛИ `input(right_click)` → ТО `custom: «прокрутити інвентар по колу»`.
- КОЛИ `use(marble, dynamite)` → ТО `place`, `timer(start)`; КОЛИ `timer(fuse)` → ТО `explode(area)`.
- КОЛИ `use(marble, umbrella)` → ТО `set_state(marble, protected, 10s)`.
- КОЛИ `picked(marble, flag)` → ТО `checkpoint`.
- КОЛИ `use(marble, mail)` → ЯКЩО `free(pipe)` → ТО `custom: «перший предмет інвентаря їде трубою до її кінця»`.
- КОЛИ `contact(marble, magic_token)` → ЯКЩО `custom: «введено код з Oxyd Book»` → ТО `disappear_b`.
- КОЛИ `counter(lives, ==, 0)` → ТО `restart`, `shuffle(oxyd_colors)`.
- КОЛИ `contact(marble_black, marble_white)` → ТО `custom: «обидві кульки розбиваються» (пізніші частини, кілька кульок)`.
- Перемога: усі пари Oxyd відкрито (meditation — усі малі кульки в ямках). Поразка: кулька розбилась → запасна кулька; без запасних — рестарт. Рахунок: час проходження проти par і світового рекорду (Enigma).

## Керування і ввід
- Лише миша: рух миші = прискорення кульки (не координата курсора); чутливість налаштовується (Enigma: також стрілками під час гри).
- ЛКМ — застосувати перший предмет інвентаря; ПКМ або колесо (Enigma: також Tab) — прокрутити інвентар.
- Затиснута кнопка під час руху — котитись, не підбираючи предметів.
- Enigma: Esc — меню, F1 — довідка, F3 — розбити поточну кульку, Shift-F3 — рестарт рівня, F4 — наступний рівень, F5 — наступний нерозвʼязаний, F10 — скріншот, Alt-X — до меню рівнів.
- Кооператив: один гравець перемикає кульки предметом Yin-Yang, або два гравці на звʼязаних компʼютерах (Atari ST — через MIDI, інші — через послідовний порт).

## Вікна, меню, HUD
- `game-screen`: поле; рядок інвентаря (`inventory-bar`), запасні кульки (`lives`), `timer-elapsed` (?).
- `pause-menu` (Esc): продовжити, рестарт, до меню рівнів (Enigma).
- `level-select` (Enigma): групи паків (Enigma, Déjà-vu, Sokoban, Facets, User, Development, All Packs), прев'ю рівнів, позначки розвʼязано/par; пошук за автором/назвою/файлом; History — автосписок зіграних.
- `level-inspector` (custom, Enigma): правий клік на превʼю — світовий рекорд, par, рахунок автора, статистика розвʼязань, власна нотатка, оцінка 0–10, свої скріншоти.
- `settings-window` (Enigma): мова, повноекранний, роздільність, розмір вікна, тайлсет; середня кнопка миші (пауза / рестарт / нічого), швидкість миші; гучність звуку й музики, звуковий набір, стерео; імʼя користувача, шляхи.
- `help-window` (F1).
- Oxyd (оригінал): вікно введення коду Magic Token з Oxyd Book (`custom-window`).
- Переходи: level-select → game-screen → win → наступний рівень за режимом (strictly next / next unsolved / par / world record hunt).

## Фічі поза полем
- `level-bank`: тисячі рівнів у паках, вільний порядок (Enigma ≈2500 — Wikipedia про Enigma).
- Режими «наступного рівня»: strictly next, next unsolved, par (рівні гірше par), world record hunt — рівень повторюється, доки не поб'єш рекорд.
- `difficulty-presets`: easy (срібна медаль з пером) і normal (золота); частина рівнів має спрощену easy-версію.
- `par-target` — par = середній час професіоналів; світовий рекорд; рахунки надсилаються файлом `enigma.score`.
- `level-rating` — оцінка рівня гравцем 0–10; `stats` розвʼязань.
- Збереження — лише прогрес і рахунки (`state.xml`), сейва посеред рівня нема; прапорці — респавн у рівні.
- `mode-coop`: двокулькові рівні; Oxyd — мережа двох машин.
- Захист від копіювання Oxyd: коди Magic Token з окремо проданої книжки Oxyd Book.
- Enigma: `level-editor` через Lua-API рівнів (довідник), читає рівні оригінальних Oxyd-паків.

## Варіації й родичі
- Лінія: Esprit (похідна від Bolo) → Oxyd (1990) → Oxyd Magnum, Oxyd Extra, per.Oxyd (Oxyd 2); вільна Oxyd extra v2.0 (Mad Data); Enigma — фанатський клон, натхненний також Rock'n'Roll (Amiga).
- Лазерні родичі в сімʼї: [deflektor](deflektor.md) (дзеркала курсором, real-time), [laser-tank](laser-tank.md) (промінь з танка, покроково), [khet](khet.md) (дзеркала-фігури), [chromatron](chromatron.md), [lasergoose](lasergoose.md) — у них промінь є ядром, у Oxyd — лише одним із пазлів дорогою до Oxyd-ів.
- Штовхання ящиків у воду як мости — як [kwirk](../push-slide/kwirk.md) (`fill-hole`).
- Осі варіацій: **мета: пари Oxyd (memory) / кульки в ямки (meditation)** · **актор: одна кулька / дві кольорові / зграя малих** · **підлога: звичайна / лід / space / inverse / схил** · **хто відкриває Oxyd: кулька / промінь / boulder** · **кольори: фіксовані / перемішуються при смерті / bold-перемішування**.

## Цікавинки для курсу
- Memory-пара на полі: стан CLOSED/OPEN/PAIR і правило «невідповідний закриває одиночний» — 🌱.
- Неперервна кулька з інерцією поверх клітинної мапи каменів (колізія круга з квадратами) — 🥈.
- Типи підлоги як коефіцієнт тертя (лід, space без тертя, red, inverse) — 📎.
- Лазер із 4 напрямками + дзеркала, що повертаються від удару, + промінь відкриває Oxyd — 🥉.
- Предмет під променем перетворюється на інший (таблиця трансформацій) — 📎.
- Chess-камінь (хід конем від удару) і puzzle-камені (звʼязна група рухається разом) — 🥉.
- Перемішування кольорів пар після втрати всіх життів — 🌱.

## Мапа на каталог
- Є: `beam-tracing`, `mirror-reflect` ↔ лазер і дзеркала · `one-way-cell` ↔ oneway-камінь · `swap-on-contact` ↔ swap-камінь · `push-object`, `fill-hole` ↔ дерев'яний камінь і мости · `destructible-blocks`, `bomb-fuse` ↔ динаміт/бомби · `inventory`, `inventory-items`, `inventory-duration` (парасолька) · `item-pickup` · `key-and-door` · `floor-types` · `environment-death` (прірва, вода), `touch-death` (skull) · `player-death`, `respawn`, `checkpoint` (прапорці) · `party-switch` (Yin-Yang) · `restart-level`, `level-bank`, `level-select`, `level-rating`, `score-records`, `difficulty-levels`, `game-pause` · вікна `game-screen`, `main-menu`, `pause-menu`, `settings-window`, `help-window`, `language-picker`, `volume-control`, `theme-select` (тайлсет).
- **Нема** → пропозиції карток:
  - `+marble-physics` «Кулька з інерцією на клітинній мапі» · entities/move · 🥈 · слоти {friction, max_speed}.
  - `+memory-pair-open` «Відкрити пару однакових (Memory на полі)» · game-logic/win · 🌱 · слот {pairs}.
  - `+pair-shuffle-on-death` «Перемішати кольори пар після поразки» · game-logic/lose · 🌱.
  - `+connected-block-move` «Звʼязна група блоків рухається як одне» · entities/move · 🥉.
  - `+knight-move-stone` «Камінь ходить конем від удару» · entities/move · 📎.
  - `+item-mail-pipe` «Поштова труба для предмета» · entities/interact · 📎.
  - `+laser-transforms-item` «Промінь перетворює предмет» · entities/interact · 📎 · слот {table}.
  - `+linked-machine-coop` «Кооператив двох машин по кабелю» · game-logic/opponent · 🥈.
  - `+copy-protection-code` «Код з паперової книжки відкриває прохід» · interface/menus · 🌱.

## Пропозиції до словників
- `+axis:physics` — значення `rolling` (кулька з інерцією й тертям поверх клітинної мапи); підтримую наявну пропозицію осі.
- `+trigger:beam_hit(a)` — промінь торкнувся сутності (Oxyd відкривається, предмет трансформується, boulder розвертається).
- `+effect:emit_beam(src)` — перерахувати промінь від джерела.
- `+effect:impulse(a, dir)` — короткий поштовх актора (bumper).
- `+effect:shuffle(set)` — перемішати значення множини сутностей (кольори Oxyd).
- `+cond:open_unpaired(x)` — є відкрита сутність без пари (Memory-стан).
- `+role:actor` — неперервна сутність з фізикою поверх клітин (кулька) на відміну від клітинного `player`.
- `+window:level-inspector` — картка рівня: рекорд, par, статистика, нотатка, оцінка.
- `+feature:world-record-hunt` — рівень повторюється, доки не побито рекорд.

## Джерела
- ⭐ [Wikipedia: Oxyd](https://en.wikipedia.org/wiki/Oxyd) — кулька мишею, пари Oxyd, Magic Token і Oxyd Book, рухомі блоки, лазери, дзеркала, пастки (прірва, крихка підлога, вода, пісок), предмети, кооператив двох кульок (MIDI/serial), сиквели, Enigma.
- [Мануал Enigma (texi)](https://raw.githubusercontent.com/Enigma-Game/Enigma/master/doc/manual/enigma.texi) — керування мишею, мета Oxyd/meditation, предмети, камені (swap, mirror, oneway, shogun, boulder, puzzle, mail, chess, wood), підлоги, par/рекорд, меню рівнів, налаштування.
- [Довідник рівнів Enigma (texi)](https://raw.githubusercontent.com/Enigma-Game/Enigma/master/doc/reference/enigma-ref.texi) — st_oxyd (12 кольорів, fake, quake, bold, shuffle, промінь відкриває), st_laser (4 напрями, on/off/turn), st_mirror (slab/sheets/triangle, поворот 90° від удару), st_box, st_boulder, st_death, st_actorimpulse, st_break, st_chameleon, st_door.
- [Wikipedia: Enigma (2007)](https://en.wikipedia.org/wiki/Enigma_(2007_video_game)) — ≈2500 рівнів, лише миша, Oxyd- і Meditation-рівні, par і світовий рекорд, рестарт з перемішаними кольорами після втрати життів.
- [GitHub: Enigma](https://github.com/Enigma-Game/Enigma) — README: Oxyd + Rock'n'Roll як натхнення, >1000 рівнів, GPL.
- [Enigma (офіційний сайт)](https://www.nongnu.org/enigma/) — завантаження (сторінка віддала 429 під час дослідження).
- YouTube: пошук «Oxyd Atari ST gameplay», «Enigma marble game gameplay».

## Непевне
- (?) Частина каменів (quake/bold/fake Oxyd, chess, puzzle, mail, shogun, chameleon, bumper, coin slot) описана за Enigma; чи всі вони були в оригінальному Oxyd 1990 — не перевірено (Wikipedia називає лише блоки, лазери, дзеркала, приховані проходи, пастки).
- (?) Перемикання екранів-кімнат у Oxyd проти скролу в Enigma — з памʼяті.
- (?) Кількість рівнів оригіналу (Oxyd Book, «з 11-го рівня») і розмір інвентаря — джерела не дають.
- (?) Перемішування кольорів при смерті — правило Enigma (Wikipedia про Enigma); в Oxyd — не перевірено.
- (?) Кількість запасних кульок: мануал Enigma — чорна + дві запасні; в Oxyd — не перевірено.
- (?) Таблиця, на що лазер перетворює які предмети, — лише згадка «монети, молотки, мечі створюються променем».
- (?) HUD: чи показується час рівня під час гри.
