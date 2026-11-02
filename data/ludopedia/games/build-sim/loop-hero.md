---
title: Loop Hero
slug: loop-hero
family: build-sim
also: [roguelike]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: survive
year: 2021
platforms: [PC, Mac, Linux, Switch, Xbox, Android, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Loop_Hero", note: "огляд: петля, картки-ландшафт, 3×3 гори → пік, відступ 70%/40%, табір, класи"}
  - {kind: other, url: "https://steamah.com/loop-hero-cards-tiles-combo-guide/", best: true, note: "гайд по комбо клітин з числами: Mountain Peak, Blooming Meadow, Ransacked Village, Hungry Grove, Town…"}
  - {kind: official, url: "https://loophero.com/", note: "офіційний сайт"}
  - {kind: steam, url: "https://store.steampowered.com/app/1282730/Loop_Hero/", note: "Steam"}
  - {kind: other, url: "https://www.pcgamer.com/loop-hero-combos-cards-tile/", note: "PC Gamer: усі комбо клітин (фетчер не віддав текст)"}
  - {kind: fandom, url: "https://loophero.fandom.com/wiki/Cards", note: "вікі карток (фетчеру закрита, 402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=loop+hero+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-auto, enemy-patrol, spawn-schedule, spawn-points, hp-damage, cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, cell-transform, inventory, inventory-limit, inventory-items, round-currency, player-death, game-pause, dungeon-generation, save-autosave, +loop-path, +day-tick, +card-placement-zones, +adjacency-buff, +tile-combo-transform, +area-pattern-transform, +coverage-area, +tile-removal-card, +boss-meter, +retreat-keep-fraction, +hand-limit-discard, +town-builder, +loop-difficulty-scale]
proposes: ["+trigger:enter", "+trigger:adjacent", "+trigger:day_start", "+trigger:counter", "+trigger:pattern", "+trigger:hp_zero", "+cond:cell", "+cond:adjacent_count", "+cond:count", "+cond:legal", "+effect:set_cell", "+effect:transform", "+effect:spawn_at", "+effect:heal", "+effect:hp", "+effect:give", "+effect:counter", "+effect:choose", "+role:terrain", "+role:spawner", "+role:zone", "+role:boss", "+ui:hp-bar", "+ui:progress-bar", "+ui:inventory-bar", "+ui:equipment-slots", "+ui:stat-panel", "+ui:tooltip", "+ui:pause-button", "+window:upgrade-window", "+window:character-select", "+window:codex-window", "+feature:meta-progression", "+card:tile-combo-transform", "+card:loop-path"]
author: opus
date: 2026-11-02
---

# Loop Hero — герой сам іде по петлі, а ти будуєш навколо неї світ картками

## Суть
Герой автоматично ходить замкненою петлею доріжки й автоматично бʼється з монстрами, які на ній стоять. Гравець керує лише **світом**: викладає картки-клітини на дорогу, поруч із нею або на пусту землю; клітини породжують ворогів, дають бонуси до статів і **комбінуються за сусідством** (3×3 скелі → гірський пік, мавзолей вампіра біля села → пограбоване село). Експедиція — забіг до смерті, відступу або перемоги над босом; здобуті ресурси (частина) йдуть у табір, де будуються постійні покращення.

## Поле і час
- Квадратна сітка-карта (≈21×12 (?)) з випадково згенерованою **замкненою петлею** порожніх дорожніх клітин (Wasteland); на петлі — клітина табору (вогнище), звідки старт.
- Три зони розміщення: **на дорозі**, **узбіччя** (клітини, суміжні з дорогою), **ландшафт** (будь-яка не-дорожня клітина; частина — і біля дороги).
- Real-time з паузою: герой іде клітина за клітиною; **день** — шкала, що заповнюється з ходом (?) — на початку дня спрацьовують «щоденні» клітини (лікування, спавн).
- **Петля (loop)** — повне коло; номер петлі піднімає рівень ворогів. Бій — окрема сцена-автобій на клітині, куди герой ступив.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, атака, захист, швидкість атаки, вампіризм…; клас | автоматично йде петлею; бій з усіма ворогами на клітині й сусідніх |
| Вогнище (табір) | static | — | старт петлі; прохід — лікування (?), лічильник петель +1; тут зʼявляється бос |
| Дорожня клітина (Wasteland) | terrain | — | порожня дорога; щодня шанс спавну слизня |
| Слизень | enemy | рівень = f(петля) | зʼявляється на дорозі випадково |
| Скеля / Гора (Rock, Mountain) | terrain | ландшафт | +HP героя; 10 шт. → табір гоблінів |
| Гірський пік (Mountain Peak) | terrain | 3×3 скель/гір | +48% HP (+2% за сусідню гору); гарпія кожні 2 дні |
| Луг (Meadow) | terrain | ландшафт | щодня лікує; біля будь-якої не-лугової клітини → квітучий луг |
| Квітучий луг (Blooming Meadow) | terrain | — | +3 HP на початку дня |
| Село (Village) | terrain | дорога | лікує при проході, дає квест (?) |
| Мавзолей вампіра (Vampire Mansion) | spawner | узбіччя | спавнить вампірів; біля села → пограбоване село |
| Пограбоване село (Ransacked Village) | spawner | дорога | до 4 гулів раз на петлю; через 3 петлі → Count's Land |
| Count's Land | terrain | дорога | лікує 15+5×петля при вході |
| Гай (Grove) / Ліс (Forest, Thicket) | terrain / spawner | — | гай спавнить ратвовків (?); ліс/хащі дають швидкість атаки (?) |
| Голодний гай (Hungry Grove) | hazard | узбіччя | зʼявляється, коли сусідній ліс згорів або стертий Забуттям; бʼє героя й зʼїдає ворогів <20% HP |
| Поле бою ×2 → Кривава стежка | spawner | дорога | перекриття двох полів бою; Blood Clot кожні 4 дні |
| Пшеничне поле біля села → Overgrown Fields | spawner | дорога | опудало кожні 4 дні |
| Ріка біля пустки/поля бою/пустелі | terrain | — | → очерет (риболюд кожні 3 дні) / корабельна аварія / оазис |
| Болото біля табору гоблінів | spawner | — | → гоблінська вежа (лучник у бої на сусідніх клітинах) |
| 5 передмість хрестом → Місто (Town) | terrain | — | центр стає містом; +2 XP за вбивство |
| Скарбниця (Treasury) | static | спеціальна | кожна сусідня гора/луг/скеля → випадковий предмет; оточена повністю → порожня скарбниця з горгульєю |
| Забуття (Oblivion) | — | спеціальна картка | стирає клітину (і ворога) з мапи |
| Бос (Lich…) | boss | — | зʼявляється на вогнищі, коли шкала боса повна |
| Предмет (зброя, щит, кільце…) | pickup | стати, рідкість | падає з ворогів; у слот спорядження або в рюкзак |
| Картка | pickup | тип: дорога/узбіччя/ландшафт/спец. | падає з ворогів у руку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(hero, next_road_cell)` (петля, без вибору напрямку).
- КОЛИ `enter(hero, cell)` ЯКЩО `occupied(cell|adjacent, enemy)` → ТО `custom: «автобій героя з усіма ворогами клітини й сусідніх, що приєднуються»`.
- КОЛИ `hp_zero(enemy)` → ТО `give(hero, loot)`: предмет, картка, ресурси.
- КОЛИ `hp_zero(hero)` → ТО `lose` експедиції: у табір іде лише 30% ресурсів (втрата 70%).
- КОЛИ `input(retreat)` ЯКЩО `cell(hero, campfire)` → ТО кінець експедиції, 100% ресурсів; інакше (поза боєм) — 60% (на 40% менше).
- КОЛИ `input(place, card, cell)` ЯКЩО `legal(card_zone, cell)` (дорога / узбіччя / ландшафт) → ТО `set_cell(cell, card_tile)`, `counter(boss_meter, +k)`.
- КОЛИ `counter(boss_meter, ==, full)` → ТО `spawn_at(boss, campfire)`.
- КОЛИ `day_start` → ТО для кожної клітини-спавнера `spawn_at(enemy, cell|adjacent_road)` за своїм періодом (кожен день / кожні 2–4 дні / раз на петлю); для лугу — `heal(hero, n)`.
- КОЛИ `day_start` для дороги ЯКЩО `rng(p)` → ТО `spawn_at(slime, road_cell)`.
- КОЛИ `pattern(group 3×3 of rock|mountain)` → ТО `transform(center → mountain_peak)` (усі 9 стають піком).
- КОЛИ `adjacent(meadow, any_non_meadow)` → ТО `transform(meadow → blooming_meadow)`.
- КОЛИ `adjacent(vampire_mansion, village)` → ТО `transform(village → ransacked_village)`; КОЛИ `counter(loops_since, ==, 3)` → `transform(→ counts_land)`.
- КОЛИ `count(rock|mountain, >=, 10)` → ТО `spawn_at(goblin_camp, random_free_cell)` (?); КОЛИ `count(village, >=, 2)` → бандитський табір.
- КОЛИ `pattern(plus of 5 suburbs)` → ТО `transform(center → town)`.
- КОЛИ `adjacent_count(treasury, any, ==, 8)` → ТО `transform(treasury → empty_treasury)`.
- КОЛИ `input(place, oblivion, cell)` → ТО `set_cell(cell, empty)` (разом із ворогом); сусід-ліс → голодний гай.
- КОЛИ `enter(hero, campfire)` → ТО `counter(loop, +1)`; рівень ворогів = f(loop).
- КОЛИ рука повна ЯКЩО `picked(card)` → ТО найстаріша картка `disappear_b` → `give(hero, resources|xp)`; так само з предметами в рюкзаку (найстаріший викидається).
- Перемога: перемогти боса глави (4 глави) (?). Поразка: смерть героя (з втратою ресурсів). Рахунку нема — є ресурси.

## Керування і ввід
- Перетягнути картку з руки на клітину; клітини, куди можна, підсвічуються.
- Перетягнути предмет із рюкзака в слот спорядження; наведення — порівняння статів.
- Пробіл — пауза («режим планування»): можна викладати картки й міняти спорядження в паузі; є автопауза на подіях (?).
- Кнопка відступу (з підтвердженням), швидкість гри (?).

## Вікна, меню, HUD
- `main-menu` → табір (`custom-window` «Camp»): мапа табору з будівлями, вибір класу, колода експедиції → «Expedition».
- `character-select` — вибір класу (Warrior, Rogue, Necromancer).
- Колода: вибір карток, що підуть в експедицію (`custom-window` «Deck»).
- `game-screen`: мапа з петлею, рука карток унизу, `hp-bar` героя, `equipment-slots`, рюкзак (`inventory-bar`), `stat-panel`, шкала дня, `progress-bar` шкали боса, лічильник петель, ресурси, `tooltip` клітини.
- Сцена бою (оверлей) з HP героя й ворогів.
- `upgrade-window`: вибір перку на рівень героя (з 3?) (?).
- `confirm-dialog` відступу; `end-screen` експедиції з підсумком ресурсів.
- `codex-window` «Енциклопедія» карток/ворогів (?).
- Переходи: camp → deck → expedition (`game-screen`) → (смерть/відступ/бос) end-screen → camp.

## Фічі поза полем
- `meta-progression` — табір: будівлі (кухня, коваль, травник, смелтер…) за ресурси дають постійні бонуси й відкривають картки/класи.
- Колода експедиції — вибір із відкритих карток (мін. кількість).
- `autosave`, `pause`, `speed-control` (?), режими складності після проходження (?).
- Глави сюжету (4) — `levels-sequential`.

## Варіації й родичі
- Родичі: Backpack Hero / Dorfromantik (`build-sim` корпусу — сусідство тайлів), Slay the Spire (картки), автобатлери (бій без керування).
- Осі варіацій: **контроль героя** — нуль (Loop Hero) / непрямий (наміри) / прямий; **комбо тайлів** — пара сусідів (луг + що завгодно) / пара типів (мавзолей + село) / фігура (3×3, хрест з 5) / лічильник на полі (10 скель → табір гоблінів); **ціна відступу** — частка ресурсів залежно від місця.

## Цікавинки для курсу
- Автохід по замкненій петлі + лічильник петель, що масштабує ворогів — 📎.
- Зони розміщення карток (дорога / узбіччя / ландшафт) як правило легальності кліку — 📎.
- Трансформація клітин за сусідством: пара типів (`adjacent`) і фігура (3×3, «плюс» з 5) — 🥉 за пару, 🥈 за пошук фігур на сітці.
- «Щоденні» спавнери з різними періодами (1/2/3/4 дні, раз на петлю) — 📎: один таймер днів + розклад клітин.
- Шкала боса, що росте від кожної викладеної картки (гравець сам кличе фінал) — 🌱.
- Відступ із частковим збереженням ресурсів (100/60/30%) — 🌱, але гарний приклад ризику.
- Ліміт руки/рюкзака з викиданням найстарішого за компенсацію — 📎 (deque).

## Мапа на каталог
- Є: `move-auto` (герой іде сам; ввід не змінює напрям — тому ще `+loop-path`) · `spawn-schedule` + `spawn-points` (спавнери-клітини) · `hp-damage` · `cell-click` + `drag-drop-piece` + `hover-highlight` + `legal-move-highlight` (викладання карток) · `cell-transform` (комбо клітин) · `inventory` + `inventory-limit` + `inventory-items` (рюкзак, спорядження) · `round-currency` (ресурси) · `player-death` · `game-pause` · `dungeon-generation` (випадкова петля) · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+loop-path` «Автохід по замкненій петлі» · entities/move · 📎.
  - `+day-tick` (як у Stardew), `+adjacency-buff` (як у Backpack Hero), `+coverage-area` (бої на сусідніх клітинах, скарбниця), `+town-builder` (табір) — ті самі.
  - `+card-placement-zones` «Зони легального розміщення (на дорозі / поруч / далі)» · entities/legality · 📎.
  - `+tile-combo-transform` «Пара сусідніх типів → нова клітина» · entities/interact · 🥉.
  - `+area-pattern-transform` «Фігура з клітин (3×3, хрест) → нова клітина» · entities/interact · 🥈.
  - `+tile-removal-card` «Картка-гумка стирає клітину» · entities/interact · 🌱.
  - `+boss-meter` «Шкала боса від дій гравця» · game-logic/waves · 🌱.
  - `+retreat-keep-fraction` «Відступ зберігає частку здобичі за місцем» · game-logic/economy · 🌱.
  - `+hand-limit-discard` «Ліміт руки: найстаріше згорає з компенсацією» · entities/state · 📎.
  - `+loop-difficulty-scale` «Сила ворогів росте з номером кола» · game-logic/waves · 🌱 — дитина `progress-acceleration`.

## Пропозиції до словників
- `+trigger:enter`, `+trigger:adjacent` (комбо пари), `+trigger:day_start` (новий: початок дня), `+trigger:counter` (шкала боса, 3 петлі), `+trigger:pattern` (3×3, плюс), `+trigger:hp_zero`.
- `+cond:cell` (зона розміщення), `+cond:adjacent_count` (скарбниця оточена), `+cond:count` (10 скель на полі), `+cond:legal`.
- `+effect:set_cell`, `+effect:transform`, `+effect:spawn_at`, `+effect:heal`, `+effect:hp`, `+effect:give`, `+effect:counter`, `+effect:choose` (перк).
- `+role:terrain`, `+role:spawner`, `+role:zone` (пік 3×3), `+role:boss`.
- `+ui:hp-bar`, `+ui:progress-bar` (шкала боса, шкала дня), `+ui:inventory-bar`, `+ui:equipment-slots`, `+ui:stat-panel`, `+ui:tooltip`, `+ui:pause-button`.
- `+window:upgrade-window`, `+window:character-select`, `+window:codex-window`; табір і колода — `custom-window`.
- `+feature:meta-progression`.
- `+card:tile-combo-transform`, `+card:loop-path`.

## Джерела
- ⭐ [Steamah: Loop Hero cards & tiles combo guide](https://steamah.com/loop-hero-cards-tiles-combo-guide/) — комбо з числами: Mountain Peak, Blooming Meadow, Ransacked Village → Count's Land, Hungry Grove, Blood Path, Town, Goblin/Bandit Camp, Empty Treasury.
- [Wikipedia](https://en.wikipedia.org/wiki/Loop_Hero) — петля, картки, 3×3 → пік, шкала боса, відступ (−70% / −40%), табір, класи, викидання найстарішого предмета.
- [Офіційний сайт](https://loophero.com/) · [Steam](https://store.steampowered.com/app/1282730/Loop_Hero/).
- [PC Gamer: Loop Hero combos](https://www.pcgamer.com/loop-hero-combos-cards-tile/) — повний список комбо (текст фетчеру не віддався).
- [Loop Hero Wiki — Cards](https://loophero.fandom.com/wiki/Cards) — вікі карток (закрита для фетчера).
- YouTube: пошук «loop hero gameplay».

## Непевне
- (?) Розмір мапи (≈21×12), тривалість дня й чи день прив'язаний до кроків героя чи до часу.
- (?) Лікування на вогнищі, квест села, ефекти лісу/гаю, табір гоблінів зʼявляється в довільній клітині — з памʼяті.
- (?) Скільки глав і що саме є перемогою (бос глави vs фінальний бос) — з памʼяті: 4 глави.
- (?) Вибір перку з 3 на рівень, «енциклопедія», регулятор швидкості — з памʼяті.
- (?) Розбіжність джерел: мавзолей вампіра біля села — «пограбоване село» (Steamah) чи «захоплює три села поспіль» (VGTimes).
