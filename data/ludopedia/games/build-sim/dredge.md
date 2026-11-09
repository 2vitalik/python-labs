---
title: Dredge
slug: dredge
aka: [DREDGE, Дредж]
family: build-sim
also: [roguelike]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2023
platforms: [PC, Switch, PS4, PS5, Xbox One, Xbox Series, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dredge_(video_game)", best: true, note: "суть: риболовля, Tetris-трюм, день/ніч, паніка, аберації, апгрейди"}
  - {kind: fandom, url: "https://dredge.wiki.gg/wiki/Boat", note: "вікі: місткість трюму і слоти обладнання за рівнями корпусу"}
  - {kind: fandom, url: "https://dredge.wiki.gg/wiki/Fish", note: "свіжість (12 год на рівень), трофеї, сітки й пастки, типи риби"}
  - {kind: fandom, url: "https://dredge.wiki.gg/wiki/Equipment", note: "двигуни/ліхтарі/вудки/сітки: розмір у клітинах і характеристики"}
  - {kind: fandom, url: "https://dredge.wiki.gg/wiki/Panic", note: "паніка: що піднімає і знижує, наслідки"}
  - {kind: fandom, url: "https://dredge.wiki.gg/wiki/Dredge_(game_mechanic)", note: "драгування: запас точки High/Medium/Low, матеріали, частини досліджень"}
  - {kind: other, url: "https://gamepressure.com/dredge-pc/can-lost-items-be-recovered/za10a71", note: "пошкоджена клітина викидає вміст за борт"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Dredge", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dredge+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [inventory, inventory-items, inventory-limit, multi-cell-size, polyomino-placement, piece-rotate-flip, drag-drop-piece, hover-highlight, hp-damage, timed-despawn, weighted-spawn, chase-player, environment-death, round-currency, shop-between-levels, shop-catalog, shop-window, in-round-upgrades, map-window, codex-window, objective-text, save-autosave, player-camera, fog-of-war, +shaped-items, +damaged-cells, +typed-slots, +item-freshness, +sanity-meter, +time-on-action, +passive-trap-inventory, +timing-bar-minigame, +tech-tree]
proposes: ["+card:damaged-cells", "+card:typed-slots", "+card:item-freshness", "+card:sanity-meter", "+card:time-on-action", "+card:passive-trap-inventory", "+card:timing-bar-minigame", "+trigger:hull_hit", "+trigger:day_start", "+effect:discard", "+effect:decay", "+role:slot", "+ui:panic-eye", "+ui:clock-dial", "+feature:passive-mode"]
author: opus
date: 2026-11-09
---

# Dredge — трюм-сітка рибальського човна: улов різних форм, обладнання в тих самих клітинах, а удар об скелю ламає клітину разом із вмістом

## Суть
Гравець веде рибальський човен архіпелагом, ловить рибу й драгує матеріали, продає улов і поліпшує човен. Клітинне ядро — **трюм**: квадратна сітка нерегулярної форми, де улов (поліміно різних форм і розмірів) треба вмістити Tetris-способом, а **обладнання (двигуни, ліхтарі, вудки, сітки) займає ті самі клітини** у типізованих слотах. Удар корпусу ламає клітини трюму: що в них лежало — за борт, обладнання на пошкодженій клітині перестає працювати. Друга вісь — час: він іде лише під час плавання й риболовлі, ніч приносить туман, паніку й чудовиськ. Клас `hybrid`: `avatar` (човен у морі) + `cursor` (перекладання предметів у сітці).

## Поле і час
- **Головне клітинне поле — трюм**: квадратна сітка, форма якої залежить від рівня корпусу; місткість вантажу 36 → 41 → 54 → 73 → 88 клітин (рівні 1–5), міцність корпусу 3 → 4 → 5 → 6 → 6.
- У сітці є **типізовані зони**: клітини під ліхтарі (1/2/3/4/4), вудки (7/9/12/14/20), сітки (0/4/4/6/6), двигуни (4/6/7/8/10) — решта для вантажу. Обладнання ставиться лише у свою зону.
- Окремі **сітки-контейнери**: трал (свій інвентар від 5×5 до 9×10) і краб-пастки (свій запас), заповнюються пасивно.
- Світ — вільне 3D-море з островами (не клітинне), камера за човном; туман і темрява вночі — `info: partial`.
- **Час іде лише від дій**: плавання і риболовля просувають годинник; стоячи на місці, час не йде (?). Сон у порту переводить на ранок.
- День/ніч: вдень спокійно; вночі туман, паніка, ворожі події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Човен | player | рівень корпусу, міцність (hull), швидкість | пливе під керуванням; удар — мінус міцність і пошкоджена клітина |
| Клітина трюму | slot | тип (вантаж / ліхтар / вудка / сітка / двигун), стан (ціла / пошкоджена) | тримає частину предмета; пошкоджена — не тримає нічого |
| Риба | object | форма-поліміно, розмір, тип (8 базових), час доби, свіжість, трофей | кладеться в трюм; псується з часом; продається |
| Аберація | object | форма, вища ціна | мутований варіант риби; гарантована при зеленому сяйві над точкою |
| Гниль (Rot) | object | 1 клітина, ціна 0 | що лишилось від зіпсованої риби; займає місце |
| Матеріал (деревина, метал, тканина, очищений метал) | resource | форма | з драгування; витрачається на апгрейди корпусу |
| Частина досліджень | resource | — | рідкісна, не відновлюється; відкриває вузли дерева обладнання |
| Дрібничка, сюжетний предмет, реліквія | pickup | форма | продається / потрібен для квесту; сюжетні не губляться при пошкодженні (?) |
| Двигун | object | розмір 1–6 клітин, вузли | ставиться в зону двигунів; дає швидкість; виходить з ладу, якщо будь-яка його клітина пошкоджена |
| Ліхтар | object | люмени, дальність | світло вночі, знижує паніку |
| Вудка / талісман | object | % швидкості лову, типи риби | без вудки потрібного типу рибу не зловити |
| Трал | container | тривалість, улов/день, власна сітка, типи | скидається як здібність; ловить пасивно; риба в ньому не псується; треба лагодити |
| Краб-пастка | container | місткість, улов/день, бонус аберацій, тривалість | ставиться в морі; збирає пасивно; ламається, якщо лишити надовго |
| Точка лову (збурена вода) | spawner | тип, запас High/Medium/Low | дає рибу через міні-гру, вичерпується |
| Точка драгування | spawner | запас | дає матеріали/частини/дрібнички через міні-гру |
| Скеля / уламки | hazard | — | удар → пошкодження корпусу |
| Чудовиська (акули-фантоми, скат, щупальце, ангели ночі…) | enemy | — | нападають/женуться вночі або при високій паніці |
| Ворони | enemy | — | крадуть улов з трюму (Wikipedia) |
| Міраж | neutral | — | ілюзорні острови/кораблі при високій паніці |
| Порт / торговці (рибар, корабельня, мандрівний торговець) | static | — | продаж, ремонт, апгрейди, сон |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fish, spot)` → ЯКЩО `has(boat, rod_of_type)` → ТО `custom: «міні-гра: смуга обертається, клік на зеленому сегменті прискорює заповнення шкали»`; без робочої вудки — повільне заповнення без зелених.
- КОЛИ `counter(catch_meter, >=, full)` → ТО `give(boat, fish)` → `window(inventory-window)` для розміщення.
- КОЛИ `input(click_gold_segment)` → ЯКЩО `prob(7.5%)` на позначку → ТО `set_state(fish, trophy)`; після трофея 4 риби без нового трофея.
- КОЛИ `input(drag_item, cells)` → ЯКЩО `fits(item, cells)` and `custom: «усі клітини цілі й потрібного типу»` → ТО `place(boat, item)`; інакше `block`.
- КОЛИ `input(rotate_item)` → ТО `rotate(item, 90)`.
- КОЛИ `input(discard, item)` → ТО `custom: «викинути предмет за борт»` (`+effect:discard`).
- КОЛИ `contact(boat, hazard)` → ТО `hp(boat, -1)`, `custom: «випадкова клітина трюму стає пошкодженою»` (`+trigger:hull_hit`).
- КОЛИ `custom: «клітина стала пошкодженою»` → ЯКЩО `occupied(cell, item)` → ТО `take(boat, item)` — предмет за борт назавжди.
- КОЛИ `tick` → ЯКЩО `custom: «хоч одна клітина обладнання пошкоджена»` → ТО `set_state(equipment, broken)` — двигун/вудка/ліхтар не діє.
- КОЛИ `hp_zero(boat)` → ТО `lose` (човен тоне) (?) → завантаження збереження.
- КОЛИ `input(repair, shipwright)` → ЯКЩО `has(boat, money)` → ТО `custom: «відновити міцність і клітини»`, `currency(-cost)`; ремкомплект лагодить до 2 зон, спершу обладнання.
- КОЛИ `timer(12h)` → ЯКЩО `not state(fish, in_net)` → ТО `custom: «свіжість −1 рівень: Fresh → Stale → Rotting → Rot»` (`+effect:decay`); у DLC-рибі — 24 год; лід сповільнює.
- КОЛИ `state_on(fish, rot)` → ТО `transform(fish, rot_1x1)`.
- КОЛИ `input(sell, fish)` → ТО `currency(+price × freshness)` — Fresh 100 %, Stale 70 %, Rotting/Infected 35 %; трофей і аберація дорожчі; макс. розмір +25 %.
- КОЛИ `timer(day)` → ЯКЩО `state(net, deployed)` → ТО `spawn_at(fish, net_grid)` (улов за день, лише типи сітки).
- КОЛИ `timer(day)` → ЯКЩО `state(pot, placed)` → ТО `spawn_at(crab, pot_grid)`; ЯКЩО `counter(pot.days, >, duration)` → ТО `set_state(pot, broken)`.
- КОЛИ `tick` → ЯКЩО `custom: «ніч і човен у темряві»` → ТО `counter(panic, +n)`; КОЛИ атака ворога → ТО `counter(panic, +big)`.
- КОЛИ `tick` → ЯКЩО `custom: «день або човен у доброму світлі»` → ТО `counter(panic, -n)`; сон у порту — `set_value(panic, 0)` (?).
- КОЛИ `rng(p)` → ЯКЩО `counter(panic, >, threshold)` → ТО `spawn_at(rock|monster|mirage, near_boat)`; ворони — `take(boat, fish)`.
- КОЛИ `custom: «зелене сяйво над точкою»` → ТО `custom: «наступна риба — аберація»`; ніч і прокляте обладнання підвищують шанс.
- КОЛИ `input(dredge, spot)` → ТО `custom: «міні-гра драгування»` → `give(boat, material|research_part|trinket)`, `counter(spot.stock, -1)`.
- КОЛИ `input(upgrade_hull, dry_dock)` → ЯКЩО `has(boat, materials)` and `has(boat, money)` → ТО `custom: «нова, більша форма сітки трюму»`, `hp(boat, +max)`.
- КОЛИ `input(research, node)` → ЯКЩО `has(boat, research_parts)` → ТО `unlock(equipment)`, далі купівля в корабельні.
- Перемога: сюжетна — зібрати реліквії (кілька кінцівок) (?). Поразки як такої нема, крім затоплення. Рахунок — гроші й заповнена енциклопедія (`Master Angler` — уся риба).

## Керування і ввід
- Човен: WASD/стік — газ і поворот; кнопка взаємодії біля точки лову/драгування/порту.
- Колесо здібностей: скинути трал, поставити пастку, ліхтар, форсаж двигуна (?).
- Міні-гра лову: клік (кнопка) у момент, коли бігунець на зеленому/золотому сегменті; форма міні-гри залежить від типу точки (?).
- Трюм: drag предмета, поворот (клавіша/правий клік (?)), викинути, перекласти між трюмом і тралом/пасткою/складом порту.

## Вікна, меню, HUD
- `main-menu`: Продовжити · Нова гра · Налаштування · Вийти; вибір слота збереження (?).
- `game-screen`: море з човном; HUD — `+ui:clock-dial` (годинник доби), `+ui:panic-eye` (око паніки: закрите → відкрите, червоніє), колесо здібностей, підказки взаємодії.
- `inventory-window` (трюм): сітка з типізованими зонами, пошкоджені клітини, предмет з характеристиками (`tooltip`: тип, розмір, свіжість, ціна); поруч — сітка тралу/пастки.
- `shop-window`: рибар (продаж), корабельня (ремонт, обладнання), мандрівний торговець; док — апгрейд корпусу (`upgrade-window`).
- `upgrade-window`: дерево досліджень обладнання за частинами.
- `map-window`: мапа архіпелагу з позначками.
- `codex-window`: енциклопедія риби (зловлені/невідомі, де і коли) (?).
- `dialogue-window`: розмови з мешканцями й квести; `objective-text` — журнал завдань.
- `pause-menu`, `settings-window`.
- Переходи: море ↔ порт (меню торговців); трюм — оверлей поверх гри, час не йде (?).

## Фічі поза полем
- `autosave` при сні/в порту (?); `save-slots` (?).
- `+feature:passive-mode` — режим, у якому вороги не полюють (Wikipedia: «game mode that stops enemies from hunting you»).
- `meta-progression` у межах гри: корпус, дерево обладнання, книжки-навички рибалки.
- `achievements` (Master Angler, Unwanted — викинути 25 риб), `codex`.
- DLC: The Pale Reach (лід, сповільнює гниття), The Iron Rig (корпус 5, ^-типи риби).

## Варіації й родичі
- У корпусі: `backpack-hero`, `backpack-battles` (сітка-рюкзак як бій), `wilmots-warehouse` (склад-сітка), `luck-be-a-landlord`; Save Room (C036) — чисте пакування; RE4 attaché case, Diablo II — прообрази.
- **Осі варіацій «інвентар-сітка»**: форма предметів (1×1 / прямокутники / поліміно) · поворот (нема / 90°) · сітка (прямокутна / нерегулярна / росте) · клітини мають тип (Dredge — зони обладнання) · клітини мають стан (Dredge — пошкоджена) · вміст має стан у часі (свіжість) · сусідство важить (Backpack Hero) / ні (Dredge).
- Осі «час»: real-time / час іде лише від дій (Dredge) / покроковий.

## Цікавинки для курсу
- Трюм-сітка з поліміно, поворотом і перевіркою «вміщується» — 📎 (`fits` + поворот матриці).
- Типізовані зони в тій самій сітці: обладнання лише у свої клітини — 🌱 (тип клітини як маска).
- Пошкодження: випадкова клітина → блок, вміст за борт, обладнання на ній зламане — 📎.
- Свіжість улову: стан предмета за годинником, ціна множиться на рівень — 🌱.
- Паніка: лічильник, що росте в темряві й вмикає ворожі події з ймовірністю — 📎.
- Час, що йде лише від дій (рух/лов), і день/ніч від нього — 📎.
- Міні-гра «смуга з сегментами» з трофейним шансом і «перезарядкою» трофея — 🥉.
- Пасивні контейнери (трал, пастка) з власною сіткою й улов/день — 📎.

## Мапа на каталог
- Є: `inventory` + `inventory-items` + `inventory-limit` (трюм) · `multi-cell-size` · `polyomino-placement` · `piece-rotate-flip` · `drag-drop-piece` + `hover-highlight` · `hp-damage` (міцність корпусу) · `timed-despawn` (гниття — близько) · `weighted-spawn` (трофей/аберація) · `chase-player` (скат) · `environment-death` (затоплення) · `round-currency` · `shop-between-levels` + `shop-catalog` + `shop-window` · `in-round-upgrades` · `map-window` · `codex-window` · `objective-text` · `save-autosave` · `player-camera` · `fog-of-war` (нічний туман).
- **Нема** → пропозиції карток:
  - `+shaped-items` (уже пропоновано Backpack Hero) — предмети-поліміно в сітці.
  - `+damaged-cells` «Пошкоджені клітини інвентаря» · entities/state · 📎 · слоти {on_hit, drop_content, disable_equipment}.
  - `+typed-slots` «Клітини сітки мають тип: обладнання лише у свої» · entities/legality · 🌱.
  - `+item-freshness` «Предмет псується за годинником, ціна за рівнем» · entities/state · 🌱 · слоти {levels, period, multipliers}.
  - `+sanity-meter` «Лічильник страху/божевілля вмикає події» · game-logic · 📎.
  - `+time-on-action` «Час іде лише від дій гравця» · game-logic · 📎.
  - `+passive-trap-inventory` «Пасивний контейнер з уловом за день» · entities/spawn · 📎.
  - `+timing-bar-minigame` «Міні-гра: натисни на сегменті смуги» · interface/input · 🥉.
  - `+tech-tree` «Дерево досліджень за ресурс» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+card:damaged-cells`, `+card:typed-slots`, `+card:item-freshness`, `+card:sanity-meter`, `+card:time-on-action`, `+card:passive-trap-inventory`, `+card:timing-bar-minigame` — див. вище.
- `+trigger:hull_hit` — корпус/контейнер отримав удар (Dredge; ушкодження рюкзака).
- `+trigger:day_start` — календарний тік «новий день» (Dredge, Stardew, Harvest Moon).
- `+effect:discard` — викинути предмет з інвентаря (не `take`: дія гравця).
- `+effect:decay` — стан предмета падає на рівень (свіжість, міцність).
- `+role:slot` — клітина-контейнер інвентаря зі своїм типом і станом.
- `+ui:panic-eye` — індикатор страху/паніки; `+ui:clock-dial` — годинник доби.
- `+feature:passive-mode` — режим без нападів ворогів.

## Джерела
- ⭐ [Wikipedia: Dredge](https://en.wikipedia.org/wiki/Dredge_(video_game)) — Tetris-подібний трюм, час іде від плавання/риболовлі, паніка, ворони, скелі, чудовиська, аберації, апгрейди, пасивний режим.
- [Dredge Wiki: Boat](https://dredge.wiki.gg/wiki/Boat) — місткість 36/41/54/73/88, міцність 3/4/5/6/6, слоти ліхтарів/вудок/сіток/двигунів за рівнями.
- [Dredge Wiki: Fish](https://dredge.wiki.gg/wiki/Fish) — міні-гра лову, трофей 7,5 % на позначку, свіжість кожні 12 год, ціни 100/70/35 %, трал не дає гнити, пастки ламаються.
- [Dredge Wiki: Equipment](https://dredge.wiki.gg/wiki/Equipment) — розміри обладнання в клітинах (двигуни 1–6), сітки тралів 5×5…9×10, ремкомплект на 2 зони.
- [Dredge Wiki: Panic](https://dredge.wiki.gg/wiki/Panic) — око паніки, джерела і наслідки.
- [Dredge Wiki: Dredging](https://dredge.wiki.gg/wiki/Dredge_(game_mechanic)) — запас точки, матеріали, частини досліджень.
- [Gamepressure: lost items](https://gamepressure.com/dredge-pc/can-lost-items-be-recovered/za10a71) — вміст пошкодженої клітини губиться назавжди (бачив у результатах пошуку).

## Непевне
- (?) Яка саме клітина пошкоджується при ударі (випадкова? біля місця удару?) і скільки клітин за удар — джерела кажуть лише «деякі клітини».
- (?) Що стається при затопленні: кінець гри з завантаженням чи повернення в порт без вантажу.
- (?) Чи стоїть час, коли човен нерухомий і коли відкритий трюм.
- (?) Сон обнуляє паніку чи лише знижує; пороги паніки для подій — у вікі нема чисел.
- (?) Клавіші повороту предмета, колесо здібностей і форсаж двигуна — з памʼяті.
- (?) Форма міні-гри залежить від типу точки — з памʼяті.
- (?) Енциклопедія як окреме вікно, слоти збережень, кінцівки — з памʼяті.
