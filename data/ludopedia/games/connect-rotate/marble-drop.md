---
title: Marble Drop
slug: marble-drop
aka: [Il Codex Mozione]
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1997
platforms: [Windows 95]
links:
  - {kind: other, url: "https://lupine.dev/marble-drop/", best: true, note: "фан-сторінка: скріни всіх 50 машин, мануал, довідка, розвʼязки"}
  - {kind: other, url: "https://lupine.dev/marble-drop/in-game-help/qzywi-17b6h_files/i0ksp2.html", note: "внутрішня довідка гри: усі компоненти, ціни, рахунок, меню, клавіші"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Marble_Drop", note: "кольори, сталеві й чорні кульки, 50 пазлів, бонусні"}
  - {kind: other, url: "https://homeoftheunderdogs.net/game.php?id=4601", note: "огляд: пристрої від кнопок до генераторів, економіка кульок"}
  - {kind: other, url: "https://archive.org/download/Marble_Drop/Marble_Drop.pdf", note: "PDF-мануал (лінк зі сторінки lupine.dev, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Marble+Drop+Maxis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [drag-drop-piece, gravity-fall, button-toggle, teleport-one-way, interaction-table, event-points, score-records, leaderboard, level-select, level-bank, puzzle-select, save-multi-slot, restart-level, game-pause, help-window, settings-window, game-screen, end-screen, sound-effects, +marble-routing, +junction-toggle, +signal-wire, +color-mixing, +recolor-station, +heat-twice-destroy, +holding-tube-release, +marble-splitter, +glue-knock-free, +score-as-currency, +overload-limit, +ordered-bin-slots, +efficiency-bonus, +bonus-puzzle-unlock, +speed-control]
proposes: ["+trigger:signal", "+role:wire", "+ui:overload-light", "+feature:player-profiles", "+card:marble-routing", "+card:signal-wire", "+card:score-as-currency", "+card:ordered-bin-slots", "+card:overload-limit"]
author: opus
date: 2026-11-09
---

# Marble Drop — кидай кольорові кульки у воронки машини да Вінчі, щоб кожна докотилась до свого кошика, а кожна попередня перемкнула шлях наступній

## Суть
На екрані — механічна машина з доріжок, перемикачів, пасток, ліфтів і гармат; угорі воронки, унизу кошики з кольоровими слотами. Гравець бере кульку з резервуара й перетягує у воронку — далі все робить фізика і стан машини: кожна кулька, проходячи перемикач, змінює дорогу для наступної. Мета — заповнити всі слоти кошиків кульками правильного кольору, втративши якнайменше кульок. Ядро — **машина станів на кульках**: розвʼязок — це послідовність «яка кулька, у яку воронку, коли», часто з навмисною «жертвою» дешевої сталевої кульки, щоб перемкнути механізм.

## Поле і час
- Поле — не сітка, а **граф доріжок**: від стартових воронок угорі до кошиків унизу; вузли — компоненти зі станом (перемикач, бар'єр, лічильник), ребра — доріжки різного вигляду (спіралі, штопори, жолоби, закриті труби, стрибки, обриви — лише вигляд). Окремий шар — **електричні дроти** від тригерів до компонентів.
- Ліворуч — вежа з резервуарами (запас поза полем), угорі — лампа перевантаження, над вежею — табло рахунку.
- Real-time: кульки котяться одночасно, швидкість машини задає гравець (повільно/середньо/швидко, `+`/`−`). Тайминг важливий: друга кулька, кинута, поки перша ще в машині, — інколи єдиний спосіб розвʼязку.
- 50 пазлів від простого до складного, 5 із них бонусні; 50-й — «невидимий» пазл.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кольорова кулька | object | колір: red, orange, yellow, green, blue, violet; ціна 500 | котиться доріжками під гравітацією, змінює стан компонентів |
| Сталева кулька | object | ціна 100 | «гарматне мʼясо» для перемикання; не фарбується; у звичайному кошику знищується, годиться лише для сталевого слота (фінальний пазл) |
| Чорна кулька | object | ціна 1500 | хамелеон: у кошику стає потрібного кольору; не займе сталевий слот; пофарбована — втрачає здатність |
| Резервуар ×8 | supply | старт: 7 кульок кожного з 6 кольорів; чорний і сталевий — порожні | джерело кульок для перетягування; кнопка «+» докуповує |
| Стартова воронка | source | 1+ на пазл | лише тут кулька входить у машину |
| Доріжка (варіанти) | conduit | спіраль, штопор, жолоб, труба, стрибок, обрив | веде кульку; вигляд не змінює логіку |
| Перемикач (diverter) | switch | 2 виходи | кожна кулька, що проходить, перемикає його на інший вихід |
| Тригерний перемикач | switch | 2 виходи | перемикається лише імпульсом з дроту, не кулькою |
| Трипозиційний перемикач | switch | 3 виходи, «світлофор» над входом | перемикається кулькою; світло показує поточний вихід |
| Тригер | switch | дріт до компонента | кулька проїхала → імпульс дротом |
| Дріт | conduit | — | несе імпульс від тригера до компонента |
| Запобіжник | conduit | на дроті | пропускає один імпульс, потім «перегорає» |
| Таймер | conduit | на дроті, ~10 с | тримає імпульс, потім пропускає далі |
| Лічильник | conduit | 2 або 5 імпульсів | накопичує імпульси, пропускає далі на N-му |
| Бар'єр (blocker) | gate | піднятий / опущений | закриває або відкриває доріжку; перемикається тригерами |
| Мішень (target) | static | може вимикатися | кулька відскакує назад; деякі після удару вимикаються |
| Поворотна мішень | gate | — | змінює напрям кульки з обох боків; тригер піднімає її з дороги |
| Маятник | platform | бік: біля входу / по той бік | переносить кульку через прогалину й лишається там — наступна з того ж боку падає в прірву |
| Ліфт | platform | довжина | стрічка з черпаками піднімає кульку на іншу доріжку |
| Пружина (арбалет) | platform | кошик-приймач | кидає кульку в приймач деінде на полі |
| Гармата | container | ствол угору після заряду | приймає кульку; постріл у приймач — за імпульсом тригера |
| Кошик-приймач | terrain | — | ловить кульку від пружини чи гармати, випускає на доріжку |
| Нагрівач | hazard | — | перший прохід — кулька «гаряча», мідна; другий — плавиться |
| Холодильник | hazard | — | перший прохід — «холодна», змінює колір; другий — розбивається |
| Фарбувальник | terrain | колір баків | перефарбовує кульку; сталеву — ні |
| Клей | terrain | — | кулька прилипає, доки інша не виб'є її, ставши на її місце |
| Телепорт-відправник | terrain | біле світло | переносить кульку до активного приймача |
| Телепорт-приймач | terrain | темний / жовтий (активний) | активний лише один одночасно |
| Розщеплювач | spawner | — | ділить кульку на дві однакові |
| Генератор кульок | spawner | колір смуги | за імпульсом випускає кульку свого кольору |
| Злиттєвик (merger) | container | таблиця кольорів | перша кулька чекає (світиться), з другою виходить одна |
| Трубка-накопичувач | container | 2–4 кульки | тримає кульки, заповнилась — випускає всі разом |
| Гальмо | terrain | — | сповільнює кульку у вертикальному падінні |
| Вертушка (spinner) | static | — | лише візуальний ефект |
| Деструктор | hazard | — | знищує кульку |
| Кошик (exit bin) | sink | слоти кольорів, по одній кульці | слоти заповнюються зліва направо; чужий колір — знищено |
| Пилка (buzz saw) | hazard | — | піднімається, коли набір кошиків повний; зайві кульки знищує |
| Секретний бонус-пристрій | static | — | «розберися сам» (у довідці без опису) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, marble)` → ЯКЩО `cell(target, start_funnel)` → ТО `place(player, marble)`, `fall(marble)`; інакше `custom: «кулька повертається в резервуар»`.
- КОЛИ `input(click, purchase_button[c])` → ТО `score(-price[c])` (500 / 1500 / 100), `give(reservoir[c], marble[c])`; рахунок може стати відʼємним.
- КОЛИ `enter(marble, diverter)` → ТО `move(marble, diverter.exit)`, `set_state(diverter, other_exit)`, `score(+n)`.
- КОЛИ `enter(marble, three_way_diverter)` → ТО `move(marble, exit)`, `set_state(diverter, next_exit)`, `custom: «світлофор над входом показує новий вихід»`.
- КОЛИ `enter(marble, trigger)` → ТО `custom: «імпульс іде дротом до звʼязаного компонента»`, `score(+10)`.
- КОЛИ `custom: «імпульс дійшов до компонента»` → ЯКЩО `state(component, triggered_diverter)` → ТО `set_state(diverter, other_exit)`; бар'єр → `set_state(blocker, raised|lowered)`; поворотна мішень → `set_state(target, tilted_up)`; генератор → `spawn(marble[band_color])`.
- КОЛИ `custom: «імпульс дійшов до запобіжника»` → ЯКЩО `not state(fuse, blown)` → ТО `custom: «пропустити»`, `set_state(fuse, blown)`; інакше `block`.
- КОЛИ `custom: «імпульс дійшов до таймера»` → ТО `timer(start, 10)`, `custom: «після відліку імпульс іде далі»`.
- КОЛИ `custom: «імпульс дійшов до лічильника»` → ТО `counter(pulses, +1)`; КОЛИ `counter(pulses, ==, n)` → ТО `custom: «імпульс іде далі»` (n = 2 або 5).
- КОЛИ `contact(marble, target)` → ТО `bounce(marble)`, `score(+25)`; деякі мішені — `set_state(target, off)`.
- КОЛИ `enter(marble, pendulum)` → ЯКЩО `state(pendulum, near_side)` → ТО `carry(pendulum, marble)`, `set_state(pendulum, far_side)`; інакше `fall(marble)`, `disappear(marble)`.
- КОЛИ `enter(marble, lift)` → ТО `carry(lift, marble)`, `custom: «висадка на верхню доріжку»`.
- КОЛИ `enter(marble, spring)` → ТО `throw(marble, basket)`, `score(+10)`.
- КОЛИ `enter(marble, cannon)` → ЯКЩО `not state(cannon, loaded)` → ТО `set_state(cannon, loaded)`; інакше `fall(marble)`, `disappear(marble)` («падає зі столу»).
- КОЛИ `custom: «імпульс дійшов до гармати»` → ЯКЩО `state(cannon, loaded)` → ТО `throw(marble, basket)`, `clear_state(cannon, loaded)`, `score(+200)`.
- КОЛИ `enter(marble, heater)` → ЯКЩО `not state(marble, hot)` → ТО `set_state(marble, hot)`, `transform(marble, copper)`; інакше `disappear(marble)`.
- КОЛИ `enter(marble, freezer)` → ЯКЩО `not state(marble, cold)` → ТО `set_state(marble, cold)`, `transform(marble, cold_color)`; інакше `disappear(marble)`.
- КОЛИ `enter(marble, painter[c])` → ЯКЩО `not same(marble, steel, kind)` → ТО `set_value(marble, c)`; чорна → `clear_state(marble, chameleon)`.
- КОЛИ `enter(marble, glue)` → ЯКЩО `free(glue)` → ТО `set_state(marble, stuck)`; ЯКЩО `occupied(glue, marble)` → ТО `push(stuck_marble)`, `set_state(marble, stuck)`.
- КОЛИ `enter(marble, teleport_sender)` → ТО `teleport(marble, active_receiver)`, `score(+50)`.
- КОЛИ `enter(marble, splitter)` → ТО `clone(marble)`.
- КОЛИ `enter(marble, merger)` → ЯКЩО `not occupied(merger, marble)` → ТО `set_state(merger, waiting)`; інакше `merge(waiting, marble, into=merge_table)`.
- Таблиця злиття: `same(a, b, color)` → той самий · чорна домінує · сталева рецесивна · два основні → вторинний (red+yellow = orange) · два вторинні → сталева · основний + вторинний → основний.
- КОЛИ `enter(marble, holding_tube)` → ТО `set_state(marble, held)`; КОЛИ `counter(held, ==, capacity)` → ТО `custom: «випустити всі кульки разом»`.
- КОЛИ `contact(marble, destructor)` → ТО `disappear(marble)`.
- КОЛИ `enter(marble, bin)` → ЯКЩО `counter(free_slots, ==, 0)` → ТО `set_state(buzz_saw, up)`, `disappear(marble)`.
- КОЛИ `enter(marble, bin)` → ЯКЩО `same(marble, next_slot, color) or (state(marble, chameleon) and not same(next_slot, steel, color))` → ТО `custom: «заповнити наступний слот зліва»`, `score(+500)`; інакше `disappear(marble)`.
- КОЛИ `counter(marbles_in_machine, >, limit)` → ТО `set_state(warning_light, red)`, `sound(warning)`; якщо кидати далі → `custom: «знищено всі кульки, включно з кошиками»`, `restart`.
- КОЛИ `input(click, reset_button)` → ТО `custom: «кульки в машині знищено, рахунок лишається»`, `restart`.
- КОЛИ `counter(empty_slots, ==, 0)` → ТО `score(+efficiency_bonus)` (100…5000 за кількістю витрачених кульок), `window(end-screen)`; уцілілі кульки — сортувальною трубкою назад у резервуари.
- Бонус-пазл: КОЛИ `enter(marble, black_slot)` → ЯКЩО `not same(marble, steel, kind)` → ТО `transform(marble, black)`; сталева — `disappear(marble)`.
- Перемога: усі слоти всіх кошиків заповнено правильно. Поразки нема — лише втрата кульок і очок. Рахунок: + за кожне використання компонента, +500 за кульку в слоті, бонус ефективності, − ціна докуплених кульок.

## Керування і ввід
- Миша: затиснути кульку в резервуарі й перетягнути у воронку; кинута повз воронку повертається назад.
- Клік по «+» біля резервуара — купити кульку за очки; червона кнопка внизу вежі — скинути пазл.
- Клавіші: F1 довідка · F2 нова гра · F3 пауза · F4 повний екран · F5 скинути пазл · F6 вибір пазла · F8 рекорди · F9 новий гравець · F10 змінити гравця · F11 завантажити · F12 зберегти · Ctrl+S звук · Ctrl+V «про гру» · `+`/`−` швидкість.
- Ввід — лише «яка кулька, куди, коли»: компоненти напряму не клікаються.

## Вікна, меню, HUD
- Старт: діалог «Enter Player Name» → `game-screen` з останнім пазлом останнього гравця.
- `game-screen`: машина; ліворуч вежа з 8 резервуарами й кнопками «+» (`inventory-bar`-подібно), зверху `score` (Score Box, червоні цифри = мінус), лампа перевантаження (`overload-light`), кнопка скидання (`restart-button`); нотатки й ескізи «Леонардо» пояснюють нові компоненти.
- `puzzle-select` (Select Puzzle): список від легкого до складного зі значками: закрита книга (не відкривали), відкрита (бачили), перо (розвʼязано), золотий перстень (знайдений бонус).
- `end-screen` Score Breakdown: Components Used, # Of Marbles Purchased, Efficiency Bonus, Puzzle Score, Beginning Score, Cumulative Score, Cost Of Marbles; кнопка CONTINUE.
- `leaderboard` View High Scores: по пазлу або загалом, з очищенням.
- `save-slots`: 10 іменованих слотів (Save / Load Game).
- `profile-window`: New Player / Select Player / Edit Player.
- Меню-бар: Game (New Game, Load, Save, Reset Puzzle, Select Puzzle, View High Scores, Demo Mode, Pause/Resume, Exit) · Player · Options (Full Screen, Sounds, Resolution 640×480 / 800×600 / 1024×768 / Maximum, Speed) · Help (`help-window` «Il Codex Mozione», `about-window`).

## Фічі поза полем
- `puzzle-bank` з 50 пазлів, вільний вибір будь-якого; `level-unlock` бонусних — за додаткове випробування в певних пазлах (у Wikipedia — «кодові замки»).
- Економіка: очки = валюта кульок; уцілілі кульки повертаються, втрачені треба докуповувати — рахунок наскрізний між пазлами.
- `speed-control` (зберігається між сесіями), `pause`, `restart-level`, `save-slots` ×10, профілі гравців, `leaderboard-local` по пазлах, `sound-toggle`, `fullscreen`, `window-size`.
- Demo Mode у меню Game (?).

## Варіації й родичі
- Корпус: [Trainyard](trainyard.md) (кольори змішуються при злитті, фарбувальники, розщеплювачі) · [Railbound](railbound.md) і [Train Valley](train-valley.md) (стрілки, що перемикає рух) · [Pipe Mania](pipe-mania.md) (потік по зʼєднаннях) · [Minecraft redstone](../build-sim/minecraft-redstone.md) і [Factorio circuit network](../program-robots/factorio-circuit-network.md) (сигнал по дроту, затримка, лічильник).
- Поза корпусом: механічні «компʼютери» на кульках (Turing Tumble, Digi-Comp II) — той самий перемикач-тригер як біт (?).
- Осі варіацій: **хто змінює стан перемикача** — сама кулька / імпульс тригера / гравець · **ресурс кульок** — безліміт / запас із докупівлею · **мета** — кольори в кошики / порядок слотів / мінімум витрат · **сигнали** — без дротів / дроти з модифікаторами (запобіжник, таймер, лічильник).

## Цікавинки для курсу
- Перемикач, що перемикається кожною кулькою (T-flip-flop): машина рахує в двійковому — 🥉 (граф компонентів зі станом + симуляція черги кульок).
- Дроти з модифікаторами: запобіжник (одноразовий), таймер (затримка), лічильник (кожен N-й) — 🥈 (подієва модель з відкладеними імпульсами).
- Таблиця злиття кольорів (домінантний чорний, рецесивний сталевий, основні/вторинні) — 📎 (таблиця як дані).
- Нагрівач/холодильник «вдруге — знищує»: стан кульки як памʼять про пройдений шлях — 🌱.
- Кошик зі слотами зліва направо: ціль задає не лише кольори, а й **порядок** приходу — 📎.
- Очки як валюта на запасні кульки й бонус ефективності — 📎.
- Розвʼязувач: пошук послідовності «кулька × воронка» в детермінованій машині станів (без фізики) — 🥇.

## Мапа на каталог
- Є: `drag-drop-piece` (кулька у воронку) · `gravity-fall` · `button-toggle` (тригер → бар'єр, мішень, перемикач) · `teleport-one-way` · `interaction-table` (компонент × кулька) · `event-points` (очки за компонент) · `score-records` + `leaderboard` · `level-select` + `level-bank` + `puzzle-select` · `save-multi-slot` · `restart-level` · `game-pause` · `help-window` · `settings-window` · `game-screen` · `end-screen` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+marble-routing` «Кульки котяться графом доріжок зі станами» · game-logic · 🥉 · слоти {components}.
  - `+junction-toggle` «Стрілка, що перемикає рух» · entities/interact · 📎 (як у Trainyard/Railbound) · слот {by: marble|signal}.
  - `+signal-wire` «Сигнальний дріт тригер → компонент» · entities/interact · 🥈 · слоти {fuse, delay, count}.
  - `+color-mixing` «Таблиця змішування кольорів» · entities/state · 📎.
  - `+recolor-station` «Клітина-фарбувальник» · entities/state · 🌱.
  - `+heat-twice-destroy` «Другий прохід знищує» · entities/state · 🌱.
  - `+holding-tube-release` «Накопичувач на N, випускає разом» · entities/interact · 📎.
  - `+marble-splitter` «Розщеплювач: одна кулька → дві» · entities/spawn · 🌱.
  - `+glue-knock-free` «Клей: нова кулька вибиває стару» · entities/interact · 🌱.
  - `+score-as-currency` «Очки як валюта» · game-logic/economy · 📎.
  - `+overload-limit` «Ліміт одночасних обʼєктів, перевищив — скидання» · game-logic/lose · 🌱.
  - `+ordered-bin-slots` «Ціль зі слотами в порядку» · game-logic/win · 🌱.
  - `+efficiency-bonus` «Бонус за мінімум ресурсів» · game-logic/score · 🌱.
  - `+bonus-puzzle-unlock` «Прихований бонус-рівень за додаткову умову» · levels/progression · 📎.
  - `+speed-control` «Швидкість симуляції» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:signal(component)` — імпульс по дроту дійшов до компонента (тригер → перемикач, бар'єр, гармата, генератор).
- `+role:wire` — провідник сигналу між тригером і компонентом, з модифікаторами (запобіжник, таймер, лічильник); не `conduit` потоку кульок.
- `+ui:overload-light` — лампа «забагато обʼєктів у грі», після якої все скидається.
- `+feature:player-profiles` — іменовані профілі гравців (новий / вибрати / редагувати) зі своїм прогресом.
- `+card:marble-routing`, `+card:signal-wire`, `+card:score-as-currency`, `+card:ordered-bin-slots`, `+card:overload-limit` — див. «Мапа на каталог».

## Джерела
- ⭐ [lupine.dev: Marble Drop](https://lupine.dev/marble-drop/) — скріни всіх 50 машин з назвами, мануал, довідка, розвʼязки Derek Kisman.
- [Довідка гри (In-Game Help)](https://lupine.dev/marble-drop/in-game-help/qzywi-17b6h_files/i0ksp2.html) — опис кожного компонента, ціни кульок, таблиця злиття, рахунок, меню, клавіші, збереження; звідси вся таблиця сутностей.
- [Wikipedia: Marble Drop](https://en.wikipedia.org/wiki/Marble_Drop) — 6 кольорів, сталеві/чорні кульки, 50 пазлів із 5 бонусними, нотатки да Вінчі, Maxis 1997.
- [Home of the Underdogs](https://homeoftheunderdogs.net/game.php?id=4601) — огляд: кнопки й плунжери → телепорти, розщеплювачі, генератори; критика купівлі кульок.
- [PDF-мануал (archive.org)](https://archive.org/download/Marble_Drop/Marble_Drop.pdf) — лінк зі сторінки lupine.dev.
- YouTube: пошук «Marble Drop Maxis gameplay».

## Непевне
- (?) Очки за перемикач: сторінка «Scoring» каже 50, таблиця «Individual Component Scores» — 25; за телепорт 100 проти 50.
- (?) Сталева кулька коштує 20 % ціни кольорової (Wikipedia) чи 10 % (огляд); довідка дає 100 проти 500.
- (?) Як саме вмикається інший приймач телепорта (імпульсом чи по черзі) — довідка каже лише «активний один».
- (?) Ліміт кульок, після якого вмикається лампа перевантаження, — числа в довідці нема.
- (?) Demo Mode у меню Game — що показує, не перевірено.
- (?) Як відкриваються бонус-пазли: «кодові замки» (Wikipedia) і «додаткове випробування» (довідка) — деталі сховані в спойлерах.
- (?) Розробник: Maxis (Austin, колишня Cinematronics) за довідкою й Wikipedia; дата виходу різниться (28.02 чи 30.03.1997).
