---
title: POUND SAND
slug: pound-sand
aka: [Pound Sand]
family: dig-gravity
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: collect
year: 2027
platforms: [Windows, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4568000/POUND_SAND/", best: true, note: "опис: усе — falling sand без абстракцій, і машини теж; шаблони машин, які доріжуєш інструментами; 6 тирів рецептів; газ від інструментів забиває машини, його відводять і роблять з нього воду; джетпак, вакуумна гармата; розібрати планету до бедроку; вихід 18.01.2027"}
  - {kind: steam, url: "https://store.steampowered.com/app/4740620/POUND_SAND_Demo/", note: "демо (3.06.2026): 8 рівнів — навчання + фінальний майже як пісочниця; усі 6 тирів, без апгрейдів гравця й просунутих шаблонів; «pollution» замість «gas»"}
  - {kind: other, url: "https://steamcommunity.com/app/4568000/discussions/0/571540929904859362/", note: "відгук на демо: конвеєр як труба (матеріали перемішуються), шар за густиною, grinder/pounder/combiner/furnace/cooler, launcher — єдиний горизонтальний транспорт рідин, drain/vent"}
  - {kind: other, url: "https://steamcommunity.com/app/4568000/discussions/0/564785824625036212/", note: "розгорнутий відгук: шаблони стін/підлог/машин, crusher, вакуум, гумка 8×8, джетпак лише вгору, нема автосейва"}
  - {kind: other, url: "https://steamcommunity.com/app/4568000/discussions/0/664989359334869509/", note: "плейтест: екран формул із вкладками, кодекс із клавішами, коробка-анонсер, шаблони не перезаписують блоки"}
  - {kind: other, url: "https://steamcommunity.com/app/4568000/discussions/0/571540929904860741/", note: "розробник: натхнення — Sandustry, Dig-N-Rig, Noita, Factorio, SteamWorld Dig, Powder"}
  - {kind: official, url: "https://pixelpocalypsegames.com/", note: "сайт студії (лише заставка)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=POUND+SAND+game+gameplay", note: "пошук; трейлери Destruction, Uranium Factory"}
stage: v1
coverage: 45
mechanics: [move-by-input, gravity-fall, cell-transform, interaction-table, dig-terrain, destructible-blocks, cursor-place, drag-drop-piece, row-conveyor, inventory-limit, round-currency, sequential-levels, objective-text, tutorial-window, codex-window, keyboard-controls, player-camera, +falling-sand-cell, +density-displacement, +phase-transition, +gas-diffusion, +pollution-clog, +gas-to-water, +pipe-conveyor-mixing, +launcher-block, +pattern-stamp-carve, +pixel-machine, +recipe-tiers, +free-rebuild, +resource-vacuum, +flight-thrust, +clear-to-bedrock, +day-night-cycle, +light-radius]
proposes: ["+role:material", "+cond:denser", "+cond:clogged", "+effect:sell", "+window:recipe-book", "+ui:hotbar", "+ui:pollution-meter", "+card:pollution-clog", "+card:gas-to-water", "+card:pipe-conveyor-mixing", "+card:pattern-stamp-carve", "+card:pixel-machine", "+card:clear-to-bedrock", "+axis:field-pixel"]
author: opus
date: 2026-11-09
---

# POUND SAND — фабрика всередині falling sand: руда тоне, пісок спливає, а газ від твоїх інструментів забиває машини

## Суть
Бічний піксельний світ чужої планети, де **усе** — ґрунт, рідини, гази й самі машини — живе в одній falling-sand симуляції: «що на конвеєрі, те й є насправді». Гравець — учасник галактичного шоу: копає породу, везе її launcher-ами й конвеєрами нагору, переробляє через 6 тирів рецептів (дробити, палити, морозити, поєднувати) і продає. Машини ставляться готовими **шаблонами**, які потім доріжуєш гумкою під свою схему; перебудова безкоштовна. Фішка — **забруднення**: інструменти виділяють газ, який займає пікселі машин і забиває їх, тож газ треба відводити й перетворювати на воду для просунутих рецептів. Мета планети — вигребти все цінне до бедроку й перейти до наступної.

## Поле і час
- Бічний вид, поле — маска пікселів: кожен піксель має матеріал і фізику (сипуче, рідина, газ, статична сталь, «реактивні» пікселі машин).
- **Густина**: важче тоне крізь легше — «ore sinks and sand rises», пісок лягає на ґрунт; найцінніше найважче, тож найбагатше — найглибше.
- Рельєф високих амплітуд (мало рівних місць під фабрику), печери, світло: день/ніч на поверхні, темні незнайомі ділянки (ліхтар) — звідси `info: partial` (?).
- Real-time; камера за гравцем, колесо миші — зум. Демо: 8 рівнів (7 навчальних + великий фінальний); повна версія — генератор світу з розміром, формою й модифікаторами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Конкурсант | player | джетпак (Space), ходьба A/D | тяга лише вгору, без тяги падає; застрягає на уступах вищих за ~3 px (за відгуком) |
| Порода (камінь) | terrain | — | інструментом розбивається на сипучі блоки |
| Пісок | material | легкий | сиплеться, сповзає зі схилів, спливає над важчим |
| Ґрунт (dirt) | material | важчий за пісок | сиплеться, лягає під пісок; у лінії піску — забруднення |
| Гравій | material | у надлишку | у печі плавиться; баланс рецептів |
| Руда (зокрема уран) | resource | найважча | тоне; забиває grinder — спершу плавлять |
| Вода | material | рідина | тече, калюжиться; гріється → пара |
| Пара / водяний пар | material | газ | піднімається, виходить через vent |
| Газ інструментів (pollution) | hazard | лічильник Pollution у HUD | займає пікселі, забиває машини; відвести й перетворити на воду |
| Розплав (molten) | material | — | з печі; стікає як рідина |
| Сталь: стіна / підлога / стеля | static | шаблони; підлога кратна 30 px | непрохідні; у декоративних ґратах сипуче провалюється |
| Платформа | terrain | — | на ній можна стояти |
| Конвеєр | conduit | напрям | везе матеріал, але пікселі штовхаються й переставляються — працює як труба |
| Launcher | conduit | — | підкидає матеріал/рідину вгору; рідина далі тече діагонально — єдиний горизонтальний транспорт рідин у демо |
| Dropper | conduit | — | ланка S-вигину для перетину ліній (?) |
| Drain | conduit | — | рідини стікають донизу |
| Vent | conduit | — | гази піднімаються вгору |
| Crusher | static | V-шаблон з кількома жовтими активними пікселями | дробить те, що впало в «V» |
| Grinder | static | — | меле пісок/ґрунт; глухий кінець — переповнюється |
| Pounder | static | — | обробляє пісок у змішаній лінії, ґрунт пропускає |
| Combiner | static | — | поєднує інгредієнти; ґрунт → забивається |
| Furnace | static | — | сушить (вода → пара), плавить гравій |
| Cooler | static | — | охолоджує / морозить |
| Лампа | static | X-подібна на платформі | освітлює фабрику |
| Коробка-анонсер | switch | — | наступив — повідомлення ведучого |
| Телепортер | conduit | лише планується | перетин ліній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(walk, dir)` → ТО `move(contestant, dir)`; КОЛИ `blocked(contestant)` → ТО `block` — уступ лише джетпаком.
- КОЛИ `input(jetpack)` → ТО `custom: «тяга вгору»`; КОЛИ `tick` → ЯКЩО `not supported(contestant)` → ТО `fall(contestant)`.
- КОЛИ `input(blast, cell)` → ЯКЩО `cell(target, stone)` → ТО `transform(stone, loose_blocks)`, `spawn(gas)`, `counter(pollution, +n)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(powder)`; інакше ЯКЩО `free(diagonal_below)` → ТО `custom: «сповзає по діагоналі»`.
- КОЛИ `tick` → ЯКЩО `custom: «піксель важчий за сусіда під ним»` → ТО `swap(a, b)` — руда тоне, пісок спливає над ґрунтом.
- КОЛИ `tick` → ЯКЩО `free(side)` → ТО `custom: «рідина розтікається вбік»`; ЯКЩО `free(above)` → ТО `custom: «газ піднімається»`.
- КОЛИ `enter(gas, machine)` → ТО `custom: «газ займає пікселі машини — вона забивається й стоїть»`.
- КОЛИ `enter(gas, vent)` → ТО `move(gas, up)`; КОЛИ `enter(liquid, drain)` → ТО `move(liquid, down)`.
- КОЛИ `custom: «газ проведено через фабрику на перетворення»` → ТО `transform(gas, water)` — вода для просунутих рецептів (?).
- КОЛИ `enter(material, conveyor)` → ТО `move(material, belt_dir)`; ЯКЩО `occupied(next_cell, other_material)` → ТО `custom: «пікселі штовхаються й міняють порядок, як у трубі»`.
- КОЛИ `enter(liquid|material, launcher)` → ТО `custom: «підкинути вгору»`; далі рідина тече діагонально вниз.
- КОЛИ `enter(sand|dirt, grinder)` → ЯКЩО `custom: «вихід вільний»` → ТО `custom: «змолоти»`; інакше `custom: «накопичується до переповнення»`.
- КОЛИ `enter(ore, grinder)` → ТО `block` — руда забиває дробарку; суміш руди й гравію спершу плавлять і зливають.
- КОЛИ `enter(sand, pounder)` → ТО `custom: «обробити пісок»`; КОЛИ `enter(dirt, pounder)` → ТО `move(dirt, through)`.
- КОЛИ `enter(dirt, combiner)` → ТО `custom: «комбайнер забивається»`.
- КОЛИ `enter(material, furnace)` → ЯКЩО `custom: «мокрий»` → ТО `transform(water, steam)`; ЯКЩО `cell(input, gravel)` → ТО `transform(gravel, molten)`.
- КОЛИ `enter(material, cooler)` → ТО `custom: «охолодити / заморозити»`.
- КОЛИ `input(vacuum, cells)` → ЯКЩО `custom: «у баку вакууму є місце»` → ТО `pickup(contestant, material)`; КОЛИ `input(release)` → ТО `place(contestant, material)` — годувати машину напряму.
- КОЛИ `input(place, pattern)` → ЯКЩО `free(pattern_cells)` → ТО `place(contestant, pattern)`; інакше `block` — один піксель у зоні зриває розміщення.
- КОЛИ `input(delete, cells)` → ЯКЩО `custom: «блок поставив гравець»` → ТО `disappear(cells)` — без штрафу; стартові блоки навчальних рівнів не стираються.
- КОЛИ `custom: «продукт пройшов ланцюг рецепту»` → ТО `custom: «продаж за Metallium»` (?), `currency(+n)`.
- КОЛИ `enter(contestant, announcer_box)` → ТО `message(announcer)`.
- КОЛИ `timer(day)` → ТО `custom: «день ↔ ніч»`.
- КОЛИ `custom: «на планеті не лишилось цінного до бедроку»` → ТО `next_level` — наступна планета.
- Перемога: розібрати планету (демо — пройти навчальні рівні). · Поразка: не описана. · Рахунок: Metallium.

## Керування і ввід
- A/D — ходьба; Space — джетпак (лише вгору); миша — приціл інструмента (напівпрозорий конус/ретикль).
- Хотбар на 16 слотів (цифри), набір слотів гравець задає сам; інструменти — бластер, вакуумна гармата, гумка (delete-пензель), ліхтар.
- Шаблони ставляться курсором; підлогу тягнеш drag-ом — довжина кратна 30 px. Колесо миші — зум (у демо конфліктує зі скролом інвентаря).
- Клавіші інструментів — у кодексі; гравці просять Ctrl-заміну блоків і зміну розміру пензля.

## Вікна, меню, HUD
- `game-screen`: піксельний світ; HUD-панель зліва вгорі: Metallium (`coins`), Pollution, Patterns (кількість шаблонів), FPS; внизу `inventory-bar` (хотбар 1–16).
- `inventory-window` — вміст вакууму/інвентаря (скрол).
- `custom-window` «формули» — рецепти з вкладками зверху (`+window:recipe-book`).
- `codex-window` — довідка з клавішами інструментів.
- `tutorial-window` / `objective-text` — завдання навчальних місій; `dialogue-window`-подібні повідомлення ведучого шоу.
- `main-menu`; у демо вихід у меню стирає прогрес без `confirm-dialog` (за відгуком).
- Переходи: main-menu → рівень (навчання 1–8) → game-screen ↔ формули / кодекс / інвентар.

## Фічі поза полем
- `levels-sequential` + `tutorial`: 8 рівнів демо; повна версія — світи-пісочниці.
- Прогресія: апгрейди гравця, нові шаблони машин (просунуті й більші) — `unlockables`; у демо закриті.
- Плани: генератор світу (розмір, форма, модифікатори «ONLY URANIUM», «ONLY DIRT» — `custom-rules`), редактор блупринтів, нові машини, формули й шаблони, телепортери.
- Збереження: у демо нема `autosave` (за відгуком).

## Варіації й родичі
- Пряме натхнення — [Sandustry](sandustry.md) (фабрика на falling sand); також Dig-N-Rig, [Noita](noita.md), [The Powder Toy](the-powder-toy.md), [SteamWorld Dig](steamworld-dig.md), [Factorio](../build-sim/factorio-belts.md). Гази й рідини на клітинах — [Oxygen Not Included](../build-sim/oxygen-not-included-cells.md), [Terraria](../build-sim/terraria-liquids.md); копати по ресурс — [Motherload](motherload.md).
- Відмінність від Sandustry: машини самі складені з пікселів симуляції й ставляться шаблонами, які доріжуєш; є густина й власне забруднення гравця.
- **Осі варіацій**: машина — «іконка з рецептом (Factorio) / блок у світі (Sandustry) / шматок пікселів, що реагує (тут)»; транспорт — «стрічка тримає порядок / пікселі перемішуються (тут)»; відходи — «нема / газ-побічка, що ламає лінії (тут, ONI)».

## Цікавинки для курсу
- Сортування за густиною в falling sand (обмін важчого з легшим під ним) — 📎: одна умова в правилі падіння.
- Конвеєр, що везе фізичні пікселі, які штовхаються й змішуються; домішка забиває машину — 🥈.
- Газ від інструментів: піднімається, займає пікселі машин, відводиться vent-колонами — 🥉.
- Шаблон машини + гумка: розмістити, якщо вся зона вільна, потім стирати пікселі — 📎.
- Launcher як «насос»: рідину підкинути, далі вона сама тече діагонально — 🥉.
- Мета «вигребти планету до бедроку»: лічильник залишку цінного — 🌱.

## Мапа на каталог
- Є: `move-by-input` ↔ ходьба · `gravity-fall` ↔ сипучі й гравець · `cell-transform` + `interaction-table` ↔ піч, кулер, рецепти · `dig-terrain` + `destructible-blocks` ↔ порода → блоки · `cursor-place` + `drag-drop-piece` ↔ шаблони й підлоги · `row-conveyor` ↔ конвеєр · `inventory-limit` ↔ бак вакууму · `round-currency` ↔ Metallium · `sequential-levels` + `tutorial-window` + `objective-text` ↔ навчальні місії · `codex-window` ↔ кодекс · `keyboard-controls` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+falling-sand-cell`, `+density-displacement`, `+phase-transition`, `+gas-diffusion` (вже пропоновані) — сипуче, густина, вода ↔ пара, газ угору.
  - `+pollution-clog` «Побічний газ займає клітини машин і зупиняє їх» · entities/interact · 🥉.
  - `+gas-to-water` «Газ-відходи перетворюються на ресурс» · entities/interact · 📎.
  - `+pipe-conveyor-mixing` «Конвеєр із фізичних частинок, що змішуються» · entities/move · 🥈.
  - `+pattern-stamp-carve` «Шаблон-штамп, далі доріжування гумкою» · entities/legality · 📎.
  - `+pixel-machine` «Машина як група реактивних клітин симуляції» · entities/interact · 🥈.
  - `+recipe-tiers` «Тири рецептів з кількома шляхами до продукту» · game-logic/economy · 📎.
  - `+clear-to-bedrock` «Мета — вибрати все цінне з карти» · game-logic/win · 🌱.
  - `+free-rebuild`, `+launcher-block`, `+resource-vacuum`, `+flight-thrust`, `+light-radius`, `+day-night-cycle` (вже пропоновані).

## Пропозиції до словників
- `+role:material` — піксель речовини з фізикою (повтор: Sandustry, Noita).
- `+cond:denser(a, b)` — A важчий за B (обмін місцями в falling sand).
- `+cond:clogged(machine)` — машина забита сторонніми пікселями.
- `+effect:sell(item)` — продати продукт за валюту (повтор: Motherload, SteamWorld Dig).
- `+window:recipe-book` — екран рецептів/формул із вкладками (повтор).
- `+ui:hotbar` — ряд слотів інструментів/блоків за цифрами (повтор); `+ui:pollution-meter` — глобальний лічильник забруднення.
- `+card:pollution-clog`, `+card:gas-to-water`, `+card:pipe-conveyor-mixing`, `+card:pattern-stamp-carve`, `+card:pixel-machine`, `+card:clear-to-bedrock` — див. «Мапа на каталог».
- `+axis:field-pixel` — поле-маска пікселів (повтор); у шапці `square`.

## Джерела
- ⭐ [Steam: POUND SAND](https://store.steampowered.com/app/4568000/POUND_SAND/) — опис (через `api/appdetails`): машини з пікселів, шаблони, 6 тирів, газ → вода, джетпак, вакуум, бедрок; дата 18.01.2027; скріншоти HUD.
- [Steam: POUND SAND Demo](https://store.steampowered.com/app/4740620/POUND_SAND_Demo/) — склад демо: 8 рівнів, що закрито.
- [Steam-обговорення: My Demo feedback](https://steamcommunity.com/app/4568000/discussions/0/571540929904859362/) — машини, густина, launcher/drain/vent, перетин ліній.
- [Steam-обговорення: Great potential…](https://steamcommunity.com/app/4568000/discussions/0/564785824625036212/) — шаблони, crusher, вакуум, гумка, джетпак, сейви.
- [Steam-обговорення: Playtest Feedback](https://steamcommunity.com/app/4568000/discussions/0/664989359334869509/) — формули, кодекс, анонсер, шаблони.
- [Steam-обговорення: inspired by Sandustry?](https://steamcommunity.com/app/4568000/discussions/0/571540929904860741/) — натхнення від розробника.
- Steam-новини «WELCOME CONTESTANTS» (розробник) — плани: генератор світу з модифікаторами, редактор блупринтів, апгрейди.
- YouTube: пошук «POUND SAND game gameplay».

## Непевне
- (?) Гра не вийшла (план — 18.01.2027); усе — з опису, скріншотів і відгуків на демо/плейтест, механіки можуть змінитись.
- (?) Як саме газ стає водою (кулер? окрема машина?) і що виробляють pounder/combiner — у джерелах без деталей.
- (?) Як продається продукт (зона продажу, ракета?) і повна назва валюти — у HUD видно лише Metallium.
- (?) `info: partial` — з відгуку про ліхтар і темні нові ділянки; туману війни як такого не описано.
- (?) Роль dropper, наявність поразки/шкоди гравцеві, розмір світу, кількість машин — не бачив.
