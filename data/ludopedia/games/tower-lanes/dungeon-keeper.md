---
title: Dungeon Keeper
slug: dungeon-keeper
family: tower-lanes
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1997
platforms: [MS-DOS, Windows 95, macOS (GOG 2012), Steam (Gold, 2024)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Keeper", best: true, note: "імпи, копання, власні клітини, кімнати, портали, рука зла, герої, умови перемоги"}
  - {kind: fandom, url: "https://dungeonkeeper.fandom.com/wiki/Room_Flags", note: "формула ефективності кімнати від стін і сусідніх плит"}
  - {kind: fandom, url: "https://dungeonkeeper.fandom.com/wiki/Workshop", note: "кімната виробництва пасток і дверей"}
  - {kind: fandom, url: "https://dungeonkeeper.fandom.com/wiki/Guard_Post_(Room)", note: "сторожовий пост"}
  - {kind: steam, url: "https://store.steampowered.com/app/1996630/Dungeon_Keeper_Gold/", note: "Dungeon Keeper Gold (EA, 2024)"}
  - {kind: steam, url: "https://store.steampowered.com/app/2616460/Dungeon_Keeper_2/", note: "сиквел"}
  - {kind: other, url: "https://gog.com/forum/dungeon_keeper_series/how_to_attract_more_monsters_on_dk1_gold", note: "форум: як приваблювати істот (розміри кімнат)"}
  - {kind: other, url: "https://www.tcrf.net/Proto:Dungeon_Keeper", note: "прототипи й вирізане"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+keeper+1997+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, hover-highlight, impassable-cells, floor-types, enemy-waves, spawn-points, hp-damage, melee-vs-ranged, round-currency, temporary-modes, chase-bfs, destroy-all-enemies, level-select, level-unlock, save-game, game-pause, minimap-radar, player-camera, ai-opponent, +dig-terrain, +zone-paint, +adjacent-to-owned-rule, +room-painting, +room-efficiency, +room-attracts-units, +worker-job-queue, +wall-fortify, +hand-pickup-drop, +slap-boost, +unit-needs-upkeep, +possess-unit, +blueprint-build, +convert-prisoner, +sacrifice-recipe, +research-unlock]
proposes: ["+trigger:payday", "+cond:owned", "+cond:room_capacity", "+effect:claim", "+effect:designate", "+effect:possess", "+effect:pickup_unit", "+effect:drop_unit", "+role:worker", "+role:room", "+ui:room-palette", "+ui:creature-panel", "+ui:hand-slots", "+window:world-map", "+window:query-panel", "+feature:possession-view", "+axis:control=indirect"]
author: opus
date: 2026-11-02
---

# Dungeon Keeper — підземелля як сітка: копай, фарбуй кімнати, приваблюй монстрів, захищай Серце

## Суть
Гравець — Хранитель підземелля: він не керує юнітами напряму, а **позначає клітини** для копання й **фарбує кімнати** на власній підлозі, а імпи й монстри самі виконують роботу. Кімнати (лігво, інкубатор, скарбниця, тренувальна…) приваблюють через портал істот певних видів, ті вимагають місця, їжі й платні. Рука зла бере й кидає істот і золото, ляпас пришвидшує роботу. Герої вторгаються стежками до Серця підземелля; втрата Серця — поразка. Клас `hybrid`: `cursor` (позначання клітин і кімнат) + непряме керування роєм (`indirect`).

## Поле і час
- Мапа — квадратна сітка «плит» (slab), кожна плита — 3×3 субклітини для рендера (?); рівні DK1 — приблизно 85×85 плит (?).
- Типи плит: земля (копається), золота жила, самоцвітна жила (нескінченна), непрохідна скеля, укріплена стіна, вода, лава, незайнята підлога, власна (червона) підлога, чужа підлога, кімнати.
- Шари: плита (тип+власник) → кімната як позначка на плиті → істоти/предмети/пастки поверх.
- Real-time з паузою; темп задають роботи імпів і періодичні події (день платні, прибуття з порталу, хвилі героїв).
- Туман: відкрите лише те, що прокопано або видно власним істотам; заклинання Sight of Evil відкриває ділянку на час.
- Камера: ізометричний вид згори з обертанням і зумом; перехід у перше обличчя при вселенні (possession).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Серце підземелля | static | HP | ядро гравця; знищене → поразка |
| Імп | worker (+role) | швидкість, рівень | копає позначені клітини, носить золото, захоплює підлогу, укріплює стіни, ставить пастки |
| Земля | terrain | — | позначена → імп копає → незайнята підлога |
| Золота жила | resource | запас | копається, імп несе золото в скарбницю |
| Самоцвітна жила | resource | ∞ | дає золото повільно, не зникає |
| Скеля | static | — | непрохідна, не копається |
| Укріплена стіна | static | власник | стіна поруч з власною підлогою, імп укріплює; повільніше ламається ворогом |
| Вода | terrain | — | прохідна, на ній не будують (Міст) |
| Лава | hazard | — | шкодить/вбиває, крім вогнетривких істот; Міст дає прохід |
| Незайнята підлога | terrain | — | імп захоплює, якщо поруч власна |
| Власна підлога | zone | колір гравця | на ній будують кімнати, пастки, двері; сюди можна кидати істот |
| Портал | spawner | захоплюється | після приєднання до мережі коридорів — прибувають істоти |
| Лігво (Lair) | room (+role) | місткість ~ плити | істоти спочивають і відновлюють HP |
| Інкубатор (Hatchery) | room | швидкість ~ ефективність | вирощує курей — їжу |
| Скарбниця (Treasure Room) | room | місткість ~ плити | зберігає золото; у день платні істоти беруть тут гроші |
| Тренувальна | room | ціна за час | істоти набирають досвід → рівень, нові вміння |
| Бібліотека | room | швидкість ~ кількість дослідників | досліджує заклинання й нові кімнати |
| Майстерня | room | — | виробляє пастки й двері (ящик-креслення) |
| В'язниця | room | — | переможені вороги замикаються; померлий в'язень → скелет (?) |
| Камера тортур | room | — | катування переконує ворога перейти на бік гравця |
| Храм | room | — | істоти щасливіші; кинута в басейн істота — жертва з нагородою/карою |
| Кладовище | room | — | трупи → вампір (?) |
| Казарма | room | — | збір загону (?) |
| Сторожовий пост | room | — | істоти стоять на варті |
| Міст | room | — | будується на воді/лаві, робить прохідною |
| Кімната перехоплення (Scavenger) | room | — | переманює чужих/нейтральних істот |
| Двері (дерево, оббиті, залізо, магічні) | gate | HP, замок | стоять у коридорі між двома стінами; ворог мусить ламати |
| Пастки (валун, тривога, газ, блискавка, Word of Power, лава) | hazard | заряди | спрацьовують, коли ворог стає на клітину; валун котиться коридором і вбиває |
| Істоти (муха, павук, біл-демон, дракон, чорнокнижник, вампір, Horned Reaper, скелет…) | ally | HP, рівень 1–10, платня, вподобання | живуть самі: їдять, сплять, тренуються, працюють, б'ються; злі — псують чи тікають |
| Герої (лицар, чарівник, гігант, самурай, гномів-копачі…) | enemy | HP, рівень | приходять у визначені моменти, ідуть до Серця, руйнують |
| Lord of the Land | boss | броня | фінальний ворог більшості рівнів |
| Рука зла | player | ліміт предметів (?) | бере/кидає істот і золото, ляпає |
| Курка | pickup | — | їжа, бігає інкубатором |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(designate_dig, cells)` → ЯКЩО `cell(x, earth|gold|gem)` → ТО `custom: «effect designate: клітина в черзі робіт імпів»`.
- КОЛИ `tick` → імп `custom: «бере найближче завдання з черги (копати > захопити > укріпити)»`, `move(a, path)` (BFS по прохідних).
- КОЛИ `custom: «імп докопав»` → ТО `set_cell(x, unclaimed_floor)`; золото → `give(imp, gold)` → несе в скарбницю → `currency(+n)`.
- КОЛИ `tick` → ЯКЩО `cell(x, unclaimed_floor)` and `custom: «cond adjacent_owned: поруч власна підлога»` → ТО імп `custom: «effect claim: set_side(x, player)»`; чужу підлогу перефарбовує так само (довше).
- КОЛИ `tick` → ЯКЩО `cell(x, earth)` and `custom: «поруч власна підлога»` → ТО імп `custom: «укріплює стіну»` → `set_cell(x, fortified_wall)`.
- КОЛИ `input(paint_room, type, cells)` → ЯКЩО `custom: «cond owned: усі клітини власні й порожні»` and `has(gold, cost×cells)` → ТО `set_cell(cells, room_type)`, `currency(-cost×cells)`; кімнати одного типу, що торкаються, зливаються в одну.
- КОЛИ `custom: «змінились клітини кімнати чи її оточення»` → ТО `custom: «ефективність = сума балів сусідніх плит / максимум: своя плита кімнати, власна укріплена стіна чи двері = 2; нейтральна стіна = 1; підлога/рідина/чужа стіна = 0»`.
- Ефективність → `custom: «місткість лігва/скарбниці і швидкість інкубатора/бібліотеки ×ефективність»`; квадратна кімната обведена укріпленими стінами — 100 %, вузька смуга — низька.
- КОЛИ `timer(arrival)` → ЯКЩО `custom: «портал приєднаний»` and `custom: «є кімнати й розміри, яких вимагає вид (напр. лігво + інкубатор N плит)»` and `custom: «у лігві є місце»` → ТО `spawn_at(creature, portal)`.
- КОЛИ `tick` → істота `custom: «обирає потребу: голод → інкубатор, втома/рана → лігво, інакше робота за вподобанням (тренування, бібліотека, майстерня, варта)»`.
- КОЛИ `custom: «trigger payday»` (періодично) → ТО кожна істота йде по платню: ЯКЩО `has(treasury, wage)` → `currency(-wage)`; інакше `set_state(creature, angry)`.
- КОЛИ `state(creature, angry)` and `timer(op, n)` → ТО `custom: «псує кімнати або йде геть через портал»`.
- КОЛИ `input(pick, creature|gold)` → ТО `custom: «effect pickup_unit: істота/золото в руку»`; КОЛИ `input(drop, cell)` → ЯКЩО `custom: «cond owned(cell)»` → ТО `custom: «effect drop_unit»`, істота приземляється й діє там.
- КОЛИ `input(slap, creature)` → ТО `speed(creature, ×k, duration)`, `hp(creature, -n)`; ляпас по імпу — швидше копає.
- КОЛИ `input(place_trap|door, cell)` → ЯКЩО `has(blueprint)` (виробила майстерня) and `owned(cell)` → ТО `custom: «креслення на клітині»`; імп приносить ящик → `transform(blueprint, trap|door)`.
- КОЛИ `enter(enemy, trap_cell)` → ТО `custom: «спрацювання пастки»`: валун — `custom: «котиться коридором, вбиває всіх на шляху»`; газ/блискавка — `damage(area)`; тривога — `custom: «скликає істот»`.
- КОЛИ `contact(enemy, door)` → ЯКЩО `not custom: «двері свої»` → ТО `block`, ворог `damage(door)`; `hp_zero(door)` → `disappear_b`.
- КОЛИ `schedule(hero_waves)` → ТО `spawn_at(heroes, hero_gate)`; герой `chase-bfs` до Серця або до найближчих істот.
- КОЛИ `hp_zero(enemy)` → ЯКЩО `count(prison, >, 0)` and `custom: «в'язниця має місце»` → ТО `set_state(enemy, prisoner)`, переноситься у в'язницю; інакше `disappear_a`.
- КОЛИ `custom: «катування в'язня»` → ТО `rng(p)` → `set_side(enemy, player)`.
- КОЛИ `custom: «істоту кинули в басейн храму»` → ТО `custom: «рецепт жертви: певні істоти → нагорода (нова істота/заклинання) або кара»`.
- КОЛИ `input(cast, spell, target)` → ЯКЩО `has(gold, cost)` → ТО ефект заклинання: Create Imp (`spawn`), Possess (`custom: «effect possess: вид від першої особи, пряме керування»`), Speed (`speed`), Heal (`heal`), Lightning (`damage`), Call to Arms (`custom: «збір усіх у точці»`), Sight of Evil (`reveal`), Cave-In (`set_cell(rock)`), Chicken (`transform(hero, chicken)`).
- КОЛИ `hp_zero(dungeon_heart)` → ТО `lose`. КОЛИ `all_gone(heroes)` або `all_gone(rival_hearts)` → ТО `win`.
- Перемога: знищити героїв (Лорда землі) або всіх суперників-Хранителів · Поразка: Серце знищено · Рахунок: нема очок; прогресія — 20 регіонів мапи світу.

## Керування і ввід
- Миша: ЛКМ по клітині з інструментом «копати» позначає/знімає позначку; drag — прямокутна позначка кількох клітин (`zone-paint`).
- Вибір кімнати в панелі → ЛКМ по власних клітинах фарбує кімнату (кожна клітина окремо оплачується); «продати» прибирає плиту кімнати з поверненням частини (?).
- Рука зла: ЛКМ по істоті/золоту — підняти (кілька в руці), ПКМ по власній клітині — кинути; ПКМ по істоті — ляпас.
- Заклинання: вибір у панелі → ЛКМ по цілі (клітина/істота).
- Possession: керування істотою від першої особи (миша+клавіатура), атаки й заклинання істоти.
- Клавіші камери: обертання, зум, прокрутка; пауза.

## Вікна, меню, HUD
- `splash-screen` — інтро-відео Bullfrog.
- `main-menu`: Start New Game · Continue · Load Game · Multiplayer · Options · High Score (?) · Quit.
- `map-window` (⏳ `world-map`): 20 регіонів «країни щастя»; захоплені стають похмурими; вибір наступного регіону.
- `game-screen`: ізометричне поле + ліва панель — `minimap`, вкладки Info / Rooms / Research (Spells) / Workshop (Traps & Doors) / Creatures, `coins` (золото), лічильник істот; `+ui:room-palette` (кімнати з ціною за плиту), `+ui:creature-panel` (список видів, кількість, стан — працює/б'ється/злий), `+ui:hand-slots` (що в руці).
- `custom-window` «query»: клік по істоті — HP, рівень, досвід, платня, вподобання (?).
- `pause-menu` — Save / Load / Options / Quit (?); `settings-window` — звук, графіка, керування.
- `end-screen` — перемога/поразка рівня зі статистикою (?).
- `lobby-window` (⏳) — мультиплеєр до 4 гравців (модем/LAN).
- Переходи: main-menu → map-window → game-screen → end-screen → map-window; game-screen ↔ possession (вид від першої особи).

## Фічі поза полем
- `world-map` + `levels-sequential` + `level-unlock`: 20 регіонів; перші рівні — навчальні; приховані бонусні рівні через знайдені предмети.
- `save-slots`, `pause`, `speed-control` (?).
- Дослідження в Бібліотеці відкривають заклинання й кімнати (`+research-unlock`); Майстерня — пастки й двері.
- `online-multiplayer`/`local-multiplayer`: до 4 Хранителів на 20 мапах (модем, LAN); ті самі мапи грабельні в одиночному режимі.
- `mod-support` спільноти: KeeperFX (відкритий перезапуск з редактором мап) (?).

## Варіації й родичі
- Dungeon Keeper 2 (1999): ті самі ідеї, 3D, Combat Pit, Casino; вимоги для істот — конкретні розміри кімнат.
- Родичі: War for the Overworld, KeeperRL (роглайк-симулятор підземелля), Dungeons, Legend of Keepers, Evil Genius; від копання й кімнат — Dwarf Fortress, Rimworld, Oxygen Not Included (позначки робіт + черга).
- **Осі варіацій**: кімната — `зона з ефективністю від стін` (DK1) / `з мінімальним розміром` (DK2) / `з обʼєктами всередині` (Rimworld) · робота — пряма / позначка → черга робітників · захист — пастки на клітинах / самі істоти / вежі.

## Цікавинки для курсу
- Позначка клітин → черга робіт → імпи беруть найближче досяжне завдання (BFS, пріоритети) — 🥇 (планувальник задач для рою).
- Захоплення підлоги лише суміжно з власною + перефарбування чужої — 🥉 (flood-подібне зростання території).
- Ефективність кімнати як сума балів 8 сусідів по периметру — 🥈 (обхід периметра зони, злиття сусідніх кімнат в одну).
- Кімнати приваблюють види істот за вимогами (набір кімнат × розміри) — 📎 (таблиця правил).
- Рука зла: підняти/кинути лише на власну клітину, ляпас = прискорення ціною HP — 🥉.
- Пастка-валун: котиться коридором до упору й вбиває всіх — 📎 (ковзання + `touch-death`).

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` ↔ позначки · `impassable-cells` ↔ скеля/стіни · `floor-types` ↔ вода/лава/підлога · `enemy-waves` + `spawn-points` ↔ герої з воріт · `hp-damage` · `melee-vs-ranged` · `round-currency` ↔ золото · `temporary-modes` ↔ ляпас/Speed · `chase-bfs` ↔ герої до Серця, імпи до роботи · `destroy-all-enemies` ↔ перемога · `level-select`/`level-unlock` ↔ мапа регіонів · `save-game` · `game-pause` · `minimap-radar` · `player-camera` · `ai-opponent` ↔ суперники-Хранителі.
- **Нема** → пропозиції карток:
  - `+dig-terrain` (є в корпусі) — тут копання за позначкою, не аватаром.
  - `+zone-paint` (є в корпусі) — drag-прямокутник позначки копання.
  - `+adjacent-to-owned-rule` (є в корпусі) — захоплення лише поруч із власним.
  - `+room-painting` «Кімната = зафарбовані власні клітини одного типу; сусідні зливаються» · entities/state · 🥉.
  - `+room-efficiency` «Ефективність кімнати від периметра (стіни, двері)» · game-logic/economy · 🥈 · слот {weights}.
  - `+room-attracts-units` «Кімнати приваблюють види юнітів» · entities/spawn · 📎 · слот {requirements}.
  - `+worker-job-queue` «Черга робіт для робітників з пріоритетами» · entities/move · 🥇.
  - `+wall-fortify` «Робітник укріплює стіну поруч із власним» · entities/interact · 🌱.
  - `+hand-pickup-drop` «Рука бере юніта й кидає на дозволену клітину» · interface/input · 🥉.
  - `+slap-boost` «Ляпас: швидше ціною HP» · entities/state · 🌱.
  - `+unit-needs-upkeep` «Юніт має потреби: їжа, сон, платня; злий — іде» · entities/state · 🥈.
  - `+possess-unit` «Вселитись у юніта: пряме керування» · interface/input · 🥉.
  - `+blueprint-build` «Креслення на клітині, робітник добудовує» · entities/spawn · 📎.
  - `+convert-prisoner` «Полонений ворог переходить на твій бік» · entities/interact · 📎.
  - `+sacrifice-recipe` «Жертва в храмі за рецептом» · entities/interact · 📎.
  - `+research-unlock` «Дослідження відкриває кімнати/заклинання» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:payday` — періодична подія виплат (варіант `schedule`, але з економікою).
- `+cond:owned` — клітина належить гравцеві (будувати, кидати істот); `+cond:room_capacity` — у кімнаті є місце.
- `+effect:claim` — перефарбувати клітину у власника (родич `set_side` для клітин); `+effect:designate` — поставити клітину в чергу робіт; `+effect:possess` — пряме керування юнітом; `+effect:pickup_unit` / `+effect:drop_unit` — рука бере/кидає сутність.
- `+role:worker` — робітник, що виконує позначені гравцем завдання (імп); `+role:room` — зона з функцією й ефективністю (відрізняти від `zone`, бо має поведінку).
- `+ui:room-palette` — палітра кімнат з ціною за клітину; `+ui:creature-panel` — список видів зі станом; `+ui:hand-slots` — вміст руки.
- `+window:world-map` — мапа кампанії регіонами (= `map-window`); `+window:query-panel` — картка істоти.
- `+feature:possession-view` — перемкнути вид на першу особу юніта.
- `+axis:control=indirect` — гравець позначає, виконують інші.

## Джерела
- ⭐ [Wikipedia: Dungeon Keeper](https://en.wikipedia.org/wiki/Dungeon_Keeper) — імпи, позначки копання, власні клітини, кімнати й портали, рука зла, ляпас, вселення, герої, Серце, 20 регіонів, мультиплеєр до 4.
- [DK Wiki: Room Flags](https://dungeonkeeper.fandom.com/wiki/Room_Flags) — ефективність кімнати: власна плита/укріплена стіна/двері = 2, нейтральна стіна = 1, решта = 0; квадратні кімнати найкращі (бачив у результатах пошуку, сторінку не відкрив — 402).
- [DK Wiki: Workshop](https://dungeonkeeper.fandom.com/wiki/Workshop) · [Guard Post](https://dungeonkeeper.fandom.com/wiki/Guard_Post_(Room)) — сторінки кімнат.
- [Steam: Dungeon Keeper Gold](https://store.steampowered.com/app/1996630/Dungeon_Keeper_Gold/) — перевидання 2024, одиночна гра.
- [GOG forum: how to attract more monsters](https://gog.com/forum/dungeon_keeper_series/how_to_attract_more_monsters_on_dk1_gold) — розміри кімнат для приваблення.
- [TCRF: Proto Dungeon Keeper](https://www.tcrf.net/Proto:Dungeon_Keeper) — прототипи.
- YouTube: пошук «dungeon keeper 1997 gameplay».

## Непевне
- (?) Розмір мап і субклітини 3×3 на плиту — з памʼяті.
- (?) Повний список кімнат DK1 (Казарма, Кладовище, Scavenger) і що робить кожна — Wikipedia називає лише 6; решта з памʼяті.
- (?) Вимоги приваблення: «біл-демон — 25 плит лігва і 25 інкубатора» — лише форум спільноти.
- (?) Скільки предметів тримає рука, ціна продажу кімнати, чи є кнопка прискорення часу.
- (?) В'язень помирає → скелет; трупи на кладовищі → вампір — з памʼяті.
- (?) Формула ефективності з DK Wiki: чи стосується DK1, чи KeeperFX.
