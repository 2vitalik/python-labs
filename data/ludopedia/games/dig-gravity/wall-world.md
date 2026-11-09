---
title: Wall World
slug: wall-world
aka: []
family: dig-gravity
also: [tower-lanes, roguelike]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2187290/Wall_World/", best: true, note: "Steam: робопавук-база, шахти в Стіні, хвилі, будівлі, апгрейди, день/ніч"}
  - {kind: other, url: "https://gamepretty.com/?p=89216", note: "гайд: зони й ресурси за висотою, таймер хвилі, зброя, обладнання, аномалії, бос, крипто-ключі, мета-прогрес"}
  - {kind: other, url: "https://gematsu.com/games/wall-world", note: "картка гри (лише з результатів пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wall+World+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [dig-terrain, impassable-cells, enemy-waves, round-currency, in-round-upgrades, item-pickup, hp-damage, player-camera, inventory-limit, tower-placement, telegraph-marker, run-relics, fog-of-war, status-panel, game-pause, +dig-wall, +mobile-base, +dock-undock, +resource-vacuum, +core-deposit, +phase-cycle, +wave-timer-on-clear, +depth-biomes, +blueprint-unlock, +meta-progression, +boss-phases, +key-gate-final]
proposes: ["+trigger:wave_start", "+trigger:wave_cleared", "+effect:deposit", "+effect:dock", "+cond:inside_base", "+role:resource", "+role:platform", "+ui:wave-timer", "+ui:base-hp", "+window:upgrade-window", "+window:loadout-select", "+card:mobile-base", "+card:dock-undock", "+card:resource-vacuum", "+card:wave-timer-on-clear"]
author: opus
date: 2026-11-09
---

# Wall World — копай печери в нескінченній Стіні, поки твоя база-павук на ній висить, і встигни назад до хвилі

## Суть
Гігантський робопавук ходить уздовж вертикальної Стіни й зупиняється біля входів у шахти; з нього висаджується пілот в екзокостюмі й видовбує ресурси в процедурних печерах. Між вилазками тикає таймер хвилі: коли він спливає, на павука нападають монстри, і пілот має повернутися, щоб керувати зброєю бази. Ресурси йдуть на апгрейди костюма й павука, креслення з глибини відкривають будівлі (турелі, ремонтні станції, комбайни). Найближчий родич у корпусі — [dome-keeper.md](dome-keeper.md); головна різниця — **база рухома**, а «глибина» — це відстань від центру вздовж Стіни. `hybrid`: `avatar` у шахті + база-турель (`tower-lanes`).

## Поле і час
- Два масштаби: Стіна — довга вертикальна смуга, вздовж якої павук ходить угору/вниз (по суті `1d`-трек з точками-шахтами); шахта — 2D-печера з руйнованих клітин-скель, у яку заходить пілот (клітинний шар — тут).
- Зони Стіни за висотою від центру (Ground): угору Cubic → Ice → High-tech, униз Sponge → Blood → Magma, окремо Mossy; кожна зона — свій ресурс, далі від центру — твердіші скелі й сильніші вороги.
- Печери процедурні й невидимі до прокопування (`info: hidden`); склад хвилі випадковий (`random: both`).
- Real-time; цикл = вилазка в шахту під таймером + бій біля павука; день/ніч і погода змінюють середовище.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пілот в екзокостюмі | player | швидкість, сила копання | ходить печерою, видовбує скелі, збирає й «жонглює» ресурсами |
| Робопавук | ally | HP, зброя, швидкість | рухома база: ходить Стіною, стоїть біля шахти (dock) або вільно рухається в бою (undock); з апгрейдом топче ворогів на стіні |
| Скеля | terrain | твердість за зоною | руйнується копанням; далі від центру твердіша |
| Ресурс-руда (Energy, Amethyst, Cubes, Diamonds, Emeralds, Pearl, Cells, Bones) | resource | зона | випадає з руди; пілот тягне/скидає біля павука, звідти — «пилосос» |
| Аномалія-зброя | container | — | розбитий павук у вузькому тунелі: відкриває зброю на цей забіг |
| Аномалія-обладнання | container | — | захоплений модуль: звільнити й принести — обладнання на забіг |
| Скарбниця | container | — | апгрейд зброї/обладнання, креслення або крипто-ключ |
| Креслення (blueprint) | pickup | 1 тир | відкриває один рівень апгрейда/будівлі |
| Крипто-ключ | pickup | 5 потрібно | відмикає браму над зоною High-tech |
| Будівлі: турель, ремонтна станція, комбайн | ally | рівень | ставляться біля шахт; автоматично стріляють / лікують / добувають |
| Зброя павука (Machine Gun, Railgun, Laser MG, Shotgun, Stake/Bomb Thrower, Cluster Grenade, Singularity) | ally | — | стріляє по хвилі; Machine Gun — стартова |
| Обладнання (Drone System, Turret/Repair Replicator, Overdrive, Barrage Mortar, Cluster Bomb, Docking Station) | ally | — | дрон-стрілець, автобудівлі біля шахт, прискорення, мінометний залп на старті хвилі, бомби при низькому HP |
| Вороги-хвилі: смертники, літаючі «цибулини»-спавнери, стрибуни зі слабкими точками | enemy | — | йдуть на павука; літаючі породжують інших; стрибун гине, коли пробито обидві бульбашки |
| Хмара переходу зони | spawner | — | кличе додаткових ворогів; під час хвилі зливається з нею |
| Бос | boss | 3 фази | таймер угорі екрана; фази 1–2 — знищити нариви, фаза 3 — лазерне око; удар щупальцем підсвічує зону червоним |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `state(spider, docked)` → ТО `move(pilot, dir)` у печері; інакше `move(spider, up|down)` уздовж Стіни.
- КОЛИ `input(mine, cell)` → ЯКЩО `cell(target, rock)` → ТО `damage(rock, mining_power)`; міцність 0 → `set_cell(empty)`; руда → `spawn(resource)`.
- КОЛИ `input(collect)` → ТО `carry(pilot, resource)`; ЯКЩО `count(carried, >, n)` → ТО `speed(pilot, −k)`.
- КОЛИ `input(vacuum)` → ЯКЩО `in_range(resource, spider)` → ТО `custom: «павук всмоктує ресурс»` → `currency(resource, +n)`.
- КОЛИ `wave_cleared` → ТО `timer(start, wave)` — таймер наступної хвилі стартує лише після загибелі останнього ворога.
- КОЛИ `timer(wave)` спливає → ТО `wave_start`: `spawn_at(enemies, wall)`.
- КОЛИ `enter(pilot, zone_cloud)` → ТО `spawn(enemies)`; ЯКЩО `state(wave, active)` → ТО `custom: «приєднуються до хвилі»`.
- КОЛИ `contact(enemy_attack, spider)` → ТО `hp(spider, −n)`; КОЛИ `hp_zero(spider)` → ТО `lose` (кінець забігу).
- КОЛИ `input(undock)` → ТО `clear_state(spider, docked)` — павук вільно рухається й ухиляється в бою.
- КОЛИ `input(buy, upgrade)` → ЯКЩО `has(player, price)` → ТО `set_value(stat)` (швидкість і копання костюма, бойові параметри павука).
- КОЛИ `picked(pilot, blueprint)` → ТО `unlock(upgrade_tier | building)`.
- КОЛИ `input(build, building)` → ЯКЩО `has(blueprint)` and `has(price)` → ТО `place(building, mine_entrance)`.
- КОЛИ `custom: «аномалію-модуль донесено до павука»` → ТО `give(spider, equipment)` на забіг.
- КОЛИ `custom: «таймер боса = 0»` → ТО `spawn(boss)`; КОЛИ `all_gone(boils)` → ТО `custom: «наступна фаза»`.
- КОЛИ `counter(crypto_keys, =, 5)` → ТО `unlock(gate)` над High-tech → фінальна фаза боса.
- КОЛИ `destroyed(boss)` у фінальній фазі → ТО `win`.
- КОЛИ `custom: «кінець забігу»` → ТО `currency(meta_points, +n)` за видобуте (більше з далеких зон).
- Перемога: 5 крипто-ключів, брама, фінал боса. Поразка: павук знищено. Рахунок: очки мета-прогресу.

## Керування і ввід
- Миша + клавіатура: рух пілота, копання утриманням (?); «жонглювання» ресурсами — рух мишею вгору-вниз; пилосос — окрема дія (?).
- У бою — наведення зброї павука й рух павука вздовж Стіни; dock/undock.

## Вікна, меню, HUD
- `main-menu` → `upgrade-window` мета-прогресу (сторінка 1 відкрита, сторінка 2 — за кресленнями) → забіг.
- `game-screen`: Стіна з павуком і входами в шахти; печера в окремому виді (?); HUD — `wave-timer`, `base-hp`, лічильники ресурсів (`coins`), таймер боса вгорі.
- `upgrade-window` у павуку: апгрейди костюма й павука; будівництво біля шахт.
- `end-screen` забігу з нарахованими очками; `pause-menu`, `settings-window`.

## Фічі поза полем
- `meta-progression`: очки за видобуток → постійні апгрейди між забігами; креслення відкривають тири.
- Процедурні шахти й аномалії; день/ніч і погода.
- `difficulty-presets` (?) — не підтверджено.

## Варіації й родичі
- [dome-keeper.md](dome-keeper.md) — нерухомий купол, глибина вниз; тут база ходить, глибина — вздовж Стіни.
- [motherload.md](motherload.md), [steamworld-dig.md](steamworld-dig.md) — копай-неси-продавай без оборони.
- **Осі варіацій**: база — «нерухома / рухома, стає біля шахти / вільно в бою»; доставка — «несеш сам / пилосос біля бази / комбайни»; таймер хвилі — «від початку циклу / лише після зачистки (можна затягнути, лишивши ворога)»; «глибина» — «вниз / від центру в обидва боки».

## Цікавинки для курсу
- Таймер хвилі стартує лише після загибелі останнього ворога — недоліком користуються, лишаючи слабкого ворога — 🌱 (вчить думати про стан тригера).
- Рухома база з режимами docked/undocked: одна сутність — і склад, і турель, і транспорт — 📎.
- Зони за відстанню від центру (симетрично вгору/вниз) зі своїм ресурсом і твердістю — 📎.
- Хмара переходу зони: спавн зливається з активною хвилею або ні — 📎.
- Креслення відкривають тири апгрейдів + мета-валюта між забігами — 🥉.
- Бос із фазами «знищити всі нариви» і телеграфованим ударом — 🥉.

## Мапа на каталог
- Є: `dig-terrain` · `impassable-cells` · `enemy-waves` · `round-currency` ↔ ресурси · `in-round-upgrades` · `item-pickup` · `hp-damage` ↔ HP павука · `player-camera` · `inventory-limit` ↔ скільки ресурсів у руках · `tower-placement` ↔ будівлі біля шахт · `telegraph-marker` ↔ червона зона удару боса · `run-relics` ↔ зброя/обладнання з аномалій · `fog-of-war` · `status-panel` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+mobile-base` «База, що переміщується полем» · entities/move · 📎.
  - `+dock-undock` «База пришвартована / вільна: різні дії» · entities/state · 📎.
  - `+resource-vacuum` «Ресурс біля бази всмоктується сам» · game-logic/economy · 🌱.
  - `+wave-timer-on-clear` «Таймер хвилі після зачистки попередньої» · game-logic/waves · 🌱.
  - Повтори: `+dig-wall`, `+core-deposit`, `+phase-cycle`, `+depth-biomes`, `+blueprint-unlock`, `+meta-progression`, `+boss-phases`, `+key-gate-final`.

## Пропозиції до словників
- `+trigger:wave_start` / `+trigger:wave_cleared` — повтори (уже в коді; тут — тригер старту таймера).
- `+effect:deposit` — повтор: ресурс у базу = валюта.
- `+effect:dock` — пришвартувати/відшвартувати рухому базу (можна `set_state`, слабка).
- `+cond:inside_base` — повтор (Dome Keeper).
- `+role:resource` — повтор; `+role:platform` — повтор (павук везе базу).
- `+ui:wave-timer` — повтор; `+ui:base-hp` — HP бази окремо від аватара.
- `+window:upgrade-window` / `+window:loadout-select` — повтори.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2187290/Wall_World/) — Alawar, 5 квітня 2023; робопавук, шахти, біоми, хвилі, турелі/ремонт/комбайни за кресленнями, апгрейди костюма й павука, день/ніч і погода.
- [GamePretty: Complete Guide](https://gamepretty.com/?p=89216) — таблиця зон і ресурсів, таймер хвилі після останнього ворога, хмари переходу, зброя, обладнання, аномалії, бос 3 фази, 5 крипто-ключів, мета-прогрес.
- [Gematsu](https://gematsu.com/games/wall-world) — картка (бачив у результатах пошуку).

## Непевне
- (?) Точна схема керування (клавіші копання, пилососа, dock); чи печера — окремий екран.
- (?) Чи є режими складності й кооп — у Steam не згадано.
- (?) Таймінги хвиль, ціни, HP — у джерелах нема.
- (?) Оцінки «тирів» зброї в гайді — суб'єктивні, у файл не взяті.
- (?) Консольні версії — не перевіряв, у шапці лише PC.
