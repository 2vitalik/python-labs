---
title: DungeonUp
slug: dungeonup
aka: [DungeonUp无尽魔塔, Dungeon Up]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2014
platforms: [Windows, macOS]
links:
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=617950988", best: true, note: "Gameplay Guide (sfnhltb, 2016): формула порогів атаки, ключі, предмети, спец-монстри, вівтарі, зони й боси, Maze Mode"}
  - {kind: steam, url: "https://store.steampowered.com/app/388620/DungeonUp/", note: "Clewcat Games, 18.11.2014: процедурні поверхи, 50+ рівнів у 5 зонах, 40+ монстрів, 40+ предметів, 3 складності, Maze Mode"}
  - {kind: other, url: "https://steamcommunity.com/app/388620/guides/", note: "список гайдів: сюжетний режим, досягнення, Maze Mode, Infinite Souls stones"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DungeonUp+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, key-and-door, hp-damage, item-pickup, inventory-items, impassable-cells, round-currency, shop-catalog, stairs-levels, sequential-levels, dungeon-generation, difficulty-levels, player-death, cell-transform, teleport, respawn, cell-click, achievements-window, +deterministic-combat, +damage-preview, +critical-value, +rising-price-shop, +stat-gems, +monster-specials, +proximity-strike, +meta-currency-gates, +maze-mode-single-floor]
proposes: ["+trigger:adjacent_enter(a, b)", "+effect:fight(a, b)", "+effect:stat(a, name, ±n)", "+cond:can_damage(a, b)", "+role:npc-merchant", "+ui:breakpoint-list", "+feature:mode-maze", "+card:proximity-strike", "+card:maze-mode-single-floor"]
author: opus
date: 2026-11-09
---

# DungeonUp — Magic Tower з процедурними поверхами: вибирайся з 49-го поверху вгору, рахуючи пороги атаки

## Суть
Лицар підіймається з глибини підземелля поверх за поверхом: двері трьох кольорів, ключі, монстри з фіксованими HP/ATK/DEF, самоцвіти, зілля, вівтарі. Ядро — те саме, що в [magic-tower](magic-tower.md): бій без випадковості, втрата HP видна наперед, ресурси скінченні. Відмінність — **процедурні поверхи** (кожен забіг — нове розташування) і зони з тематичними монстрами, що мають «агресивні» здібності: бʼють, коли ти просто став поруч. Окремий режим Maze Mode — один поверх без сходів на «каву».

## Поле і час
- Поверх — квадратна сітка, видима цілком; поверхи зʼєднані сходами. Сюжетний режим — 5 зон по ~10 поверхів, старт на 49-му, рух угору до 0 (за гайдом); є секретні поверхи (17, 6) і поверх 50 (досяжний сувоєм глибини).
- Генерація «здебільшого випадкова»; маршрут до наступного поверху зазвичай проходить через певних монстрів; є приховані проходи (фальшиві стіни).
- Покроково: монстри стоять; хід = крок героя. Бій — розрахунок раундів за формулою.
- Шари: підлога/стіна/лава + обʼєкт (монстр, двері, предмет, NPC, вівтар).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лицар | player | HP, Attack, Defense, Gold, ключі, Soul stones | рух 4 напрямки; вхід у монстра = бій, у двері = відкрити ключем |
| Монстр | enemy | HP, Attack, Defense, Gold | стоїть; бій ініціює гравець; превʼю показує результат «якщо бʼєш першим» |
| Пекельний пес (Hell Hound) | enemy | — | атакує, коли герой стає поруч (без Cloak of Shadows) |
| Високий маг / Ілюзіоніст | enemy | 200 шкоди / 25 % поточного HP | бʼють, коли герой стає поруч, потім **відступають** на іншу клітину |
| Некромант | enemy | +100 шкоди | додаткова шкода, поки герой поруч |
| Привид | enemy | — | якщо не вбитий одним ударом — зʼявляється деінде на поверсі |
| Біс (Imp, зона 5) | enemy | 200 шкоди | шкодить герою при власній смерті |
| Нежить (зомбі, Vampire King) | enemy | unholy | отримують ×2 атаки від Relic |
| Бос зони | boss | частини / почет | Skeleton King, Vampire King, Lizard Warriors, Illusionist Lord (4 ілюзіоністи хрестом), Zreluhm (голова → частини) |
| Двері жовті / сині / червоні | gate | колір | відкривається ключем кольору, ключ витрачається |
| Ключ | pickup | колір | +1 ключ; Golden Key відкриває всі жовті двері |
| Секретна стіна | static | — | клік перевіряє, чи стіна справжня |
| Мале / велике зілля | pickup | +HP (росте з зоною) | лікування одразу |
| Самоцвіт ATK / DEF | pickup | +1…+10 за зоною | постійне посилення |
| Меч / щит | pickup | Bronze 10 → Iron 20 → Steel 40 → Knight's 80 → Fire 160 | замінює спорядження |
| Кирка (Magic Mattock) | pickup | одноразова | прибирає сусідню стіну (не двері) |
| Бомба | pickup | одноразова | руйнує перешкоду |
| Сувої Height / Depth / Teleport / Earthquake / Chaos | pickup | одноразові | поверх вище / нижче / на протилежний бік поверху / = 2 кирки / відродити монстрів поверху |
| Wand of Freeze | pickup | постійний | лава → підлога |
| Wand of Flight · Crystal Ball | pickup | постійні | бачити предмети/вівтарі інших поверхів · поверх вище |
| Vampire's Fang · Lucky Coin · Water of Life | pickup | постійні | 5 % вампіризму · +10 % золота · лікує тим більше, чим довше несеш |
| Dragon Slayer · Relic · Cross · Anti-magic Ring · Cloak of Shadows | pickup | постійні | ×2 проти драконів · ×2 проти нежиті · проти Vampire King · захист від магів · монстри «на погляд» не бʼють першими |
| Лава | hazard | — | непрохідна без Wand of Freeze (?) |
| Вівтар | neutral | ціна за загальну кількість покупок | золото → +ATK або +DEF; бонус більший на вищих вівтарях |
| Купець / коваль | neutral | ціна в золоті або Soul stones | продає ключі, предмети, кирки; коваль — Mithril Armor (+100 DEF) |
| Сходи | static | — | на сусідній поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(knight, dir)`.
- КОЛИ `contact(knight, monster)` → ТО `custom: «бій: раундів = ceil(mHP / (ATK − mDEF)), лицар бʼє першим; втрата = (раунди − 1) × max(0, mATK − DEF)»`; ЯКЩО `hp_zero(knight)` → ТО `lose`; інакше `disappear(monster)`, `currency(+gold)`.
- Поріг атаки: `custom: «ATK для N раундів = ceil((mDEF × N + mHP) / N)»` — найменша атака, з якою монстр падає на раунд раніше.
- КОЛИ `contact(knight, door[c])` → ЯКЩО `has(knight, key[c])` → ТО `disappear(door)`, `take(knight, key[c])`; інакше `block`.
- КОЛИ `contact(knight, golden_key)` → ТО `custom: «усі жовті двері стають прохідними»`.
- КОЛИ `picked(knight, gem)` → ТО `custom: «+ATK або +DEF на значення зони»`.
- КОЛИ `picked(knight, potion)` → ТО `heal(knight, n)`.
- КОЛИ `adjacent(knight, hell_hound)` → ЯКЩО `not has(knight, cloak_of_shadows)` → ТО `damage(knight, mATK)`.
- КОЛИ `adjacent(knight, high_mage|illusionist)` → ТО `damage(knight, 200 | 25% HP)`, `teleport(mage, custom: «відступ»)`.
- КОЛИ `died(imp)` → ТО `damage(knight, 200)`; КОЛИ `died(zreluhm_wing)` → ТО `damage(knight, 500)`.
- КОЛИ `custom: «бій закінчився, привид живий»` → ТО `respawn(ghost, «інша клітина поверху»)`.
- КОЛИ `contact(knight, altar)` → ТО `window(shop-window)`; купівля → ЯКЩО `counter(gold, >=, price)` → ТО `currency(−price)`, `custom: «+ATK/+DEF; ціна наступної покупки на БУДЬ-ЯКОМУ вівтарі росте 20, 40, 80, 140, 220…»`.
- КОЛИ `use(knight, mattock)` → ЯКЩО `cell(adjacent, wall)` → ТО `set_cell(adjacent, floor)`.
- КОЛИ `use(knight, scroll_height|scroll_depth)` → ТО `custom: «на поверх вище / нижче»`; КОЛИ `use(knight, scroll_teleport)` → ТО `teleport(knight, «протилежний бік поверху»)`.
- КОЛИ `use(knight, scroll_chaos)` → ТО `spawn(monsters)` (фарм золота).
- КОЛИ `use(knight, wand_of_freeze)` → ТО `set_cell(lava, floor)`.
- КОЛИ `custom: «кінець зони»` → ТО `counter(soul_stones, +zone)`.
- КОЛИ `died(final_boss)` → ТО `win`; секретна кінцівка — бій з Джином (пороги AB8–AB30).
- Перемога: вибратися нагору (переможений бос зони 5). Поразка: HP = 0. Рахунку нема — є досягнення (напр., зона 1 за 5 хв).

## Керування і ввід
- Мишка: клік по клітині (в т.ч. перевірка секретної стіни), наведення на монстра — превʼю бою; клавіатура — рух (?).
- Esc під час бою — втеча (зі слів коментатора).
- Предмети — з панелі інвентарю.

## Вікна, меню, HUD
- `game-screen`: поверх, `stat-panel` (HP, ATK, DEF, Gold, ключі, Soul stones), `inventory-bar`; `damage-preview` / `tooltip` при наведенні на монстра.
- `shop-window`: вівтар (+ATK / +DEF), купець (ключі, предмети за золото чи Soul stones).
- `dialogue-window`: NPC і сюжетні поверхи («10+ levels with secrets and plots»).
- `mode-select`: Story · Maze; `difficulty-select`: 3 складності.
- `achievements-window` (Steam), `end-screen`, `main-menu`.
- Переходи: `main-menu` → `mode-select` → `difficulty-select` → `game-screen` ⇄ `shop-window` / `dialogue-window`; смерть → `end-screen`.

## Фічі поза полем
- `difficulty-presets` (3; Easy радять для досягнень — менше ризику лишитися без ключів).
- `mode-maze` — Maze Mode: один поверх без сходів, ключі й предмети не переносяться, Golden Key і Chaos діють лише на видимі двері й монстрів.
- `achievements`; «tons of Player Maps» (Steam) — користувацькі мапи (?).
- Генерація щоразу нова → `seed` не показується (?).

## Варіації й родичі
- Батько — [magic-tower](magic-tower.md) (Tower of the Sorcerer); сучасні сусіди — [tactical-nexus](tactical-nexus.md) (ручні вежі + undo/redo), [h5mota](h5mota.md) (спільнота веж), [towerbound](towerbound.md) (50 ручних поверхів).
- Відмінності від `magic-tower`: процедурні поверхи замість ручних; рух **вгору** з глибини; Soul stones як друга валюта між зонами; монстри з **проксимальними** ударами (бʼють за сусідство, відступають) — тобто маршрут повз монстра коштує HP навіть без бою; ціна вівтаря — спільна для всіх вівтарів.
- Осі варіацій: генерація (ручна / процедурна) · ціна апгрейду (за вівтар / глобальна) · здібності (модифікатори формули / реакції на сусідство) · режим (вежа / один поверх-лабіринт).

## Цікавинки для курсу
- Формула порогів атаки `ceil((mDEF·N + mHP)/N)` і список порогів на панелі — 🌱 (чиста функція, юніт-тести).
- Проксимальні удари: шкода за «став поруч», маг-утікач телепортується — 📎 (тригер сусідства + вибір клітини відступу).
- Привид, що переїжджає, якщо не вбитий з одного удару — 🌱.
- Глобальна зростаюча ціна вівтарів — 🌱.
- Процедурний поверх «Magic Tower», де маршрут проходить через монстрів, а ключів вистачає — 🥇 (генератор з перевіркою прохідності й бюджету ключів/HP).
- Maze Mode: один поверх як пазл на 5 хвилин — 📎.

## Мапа на каталог
- Є: `move-4dir` · `key-and-door` · `hp-damage` · `item-pickup` · `inventory-items` · `impassable-cells` · `round-currency` (золото) · `shop-catalog` · `stairs-levels` · `sequential-levels` · `dungeon-generation` · `difficulty-levels` · `player-death` · `cell-transform` (кирка, лава) · `teleport` (сувій) · `respawn` (привид) · `cell-click` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+deterministic-combat`, `+damage-preview`, `+critical-value`, `+rising-price-shop`, `+stat-gems`, `+monster-specials` — як у `magic-tower`.
  - `+proximity-strike` «Ворог бʼє, коли герой став поруч» · entities/combat · 📎 · слоти {damage, retreat}.
  - `+meta-currency-gates` «Друга валюта між зонами (Soul stones)» · game-logic/economy · 🌱.
  - `+maze-mode-single-floor` «Режим: один поверх без сходів» · levels/generation · 📎.

## Пропозиції до словників
- `+trigger:adjacent_enter(a, b)` — A став сусідом B саме цим кроком (на відміну від `adjacent` як стану): проксимальні удари.
- `+effect:fight(a, b)`, `+effect:stat(a, name, ±n)`, `+cond:can_damage(a, b)` — як у `magic-tower` / `tactical-nexus` (ще не в словнику).
- `+role:npc-merchant` — купець/коваль.
- `+ui:breakpoint-list` — пороги атаки AB1…ABn для монстра.
- `+feature:mode-maze` — окремий режим одного поверху.
- `+card:proximity-strike` · `+card:maze-mode-single-floor`.

## Джерела
- ⭐ [Steam-гайд «Gameplay Guide»](https://steamcommunity.com/sharedfiles/filedetails/?id=617950988) — формула порогів, предмети, спец-монстри, вівтарі й ціни, зони й боси, Maze Mode (гайд 2016, позначений як знятий).
- [Steam: DungeonUp](https://store.steampowered.com/app/388620/DungeonUp/) — опис: «inspired by but different from Tower of the Sorcerer… procedurally generated levels», 50+ рівнів, 5 зон, 3 складності, Maze Mode.
- [Steam: гайди](https://steamcommunity.com/app/388620/guides/) — перелік гайдів (сюжет, досягнення, Maze Mode).
- YouTube: [пошук](https://www.youtube.com/results?search_query=DungeonUp+gameplay).

## Непевне
- (?) Числа (ціни вівтарів, шкода магів, значення мечів, номери поверхів зон) — з гайду 2016; могли змінитися патчами.
- (?) Черга «Magic Tower + прокачка»: гайд **не** описує XP/рівнів — сила лише з самоцвітів, спорядження й вівтарів.
- (?) Керування клавіатурою, автошлях по кліку, сейви/undo — у джерелах не описано.
- (?) Лава непрохідна чи шкодить при вході — не уточнено.
- (?) Мобільна версія: Steam-сторінка показує лише Windows/macOS; черга згадує мобільну.
- (?) «Player Maps» — чи є редактор, не з'ясовано.
