---
title: Dungeon of the Endless
slug: dungeon-of-the-endless
family: roguelike
also: [tower-lanes]
klass: hybrid
axes:
  field: graph
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2014
platforms: [PC, Mac, iOS, Xbox One, PS4, Switch, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_of_the_Endless", best: true, note: "двері = хід, три ресурси, живлення кімнат Dust-ом, спавн у темних кімнатах, кристал до виходу, 12 поверхів"}
  - {kind: steam, url: "https://store.steampowered.com/app/249050/Dungeon_of_the_ENDLESS/", note: "опис: minor/major modules, co-op до 4"}
  - {kind: fandom, url: "https://dungeonoftheendless.fandom.com/wiki/Dungeon_of_the_Endless_Wiki", note: "вікі модулів і героїв; WebFetch отримав 402 — вміст не читав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+of+the+endless+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [dungeon-generation, enemy-waves, spawn-points, hp-damage, inventory-items, round-currency, shop-catalog, in-round-upgrades, reach-exit, sequential-levels, player-death, game-pause, temporary-modes, chase-bfs, minimap-radar, keyboard-controls, cell-click, +permadeath, +door-turn, +room-power-grid, +dark-room-spawn, +module-slots, +carry-objective, +per-turn-income, +research-unlock, +hero-skills, +recruit-ally, +wave-clear-heal]
proposes: ["+trigger:door_opened", "+trigger:wave_cleared", "+trigger:lifted(crystal)", "+cond:powered(room)", "+cond:connected", "+effect:power(room)", "+effect:unpower(room)", "+effect:build(module, slot)", "+effect:carry", "+role:tower", "+role:zone", "+role:spawner", "+role:slot", "+ui:resource-counters", "+ui:power-meter", "+ui:door-marker", "+window:research-window", "+window:character-select", "+window:pod-select", "+feature:mode-coop", "+feature:permadeath", "+axis:turn-structure=event"]
author: opus
date: 2026-11-02
---

# Dungeon of the Endless — хід = відчинити двері: живи кімнати Dust-ом, бо з темряви лізуть хвилі

## Суть
Загін з 2–4 героїв розбився на кораблі й несе його кристал угору крізь поверхи-підземелля. Поверх — мережа кімнат за дверима; **кожне відчинення дверей — це хід**: приносить ресурси (Industry, Science, Food) і може запустити хвилю монстрів, що вилазять із **неживлених (темних) кімнат**. Гравець витрачає Dust, щоб живити звʼязну множину кімнат від кристала, будує в живлених кімнатах генератори й турелі, а коли знайде вихід — несе кристал крізь темряву під безперервними хвилями. Гібрид роглайка (дослідження, permadeath, герої) і tower defense (модулі на слотах, хвилі) — `klass: hybrid` (avatar-загін + cursor-будівництво).

## Поле і час
- Поверх = **граф кімнат** (вузли), зʼєднаних дверима (ребра); всередині кімнати — клітинний план із **слотами під модулі**: великі (major) і малі (minor). Герої й монстри ходять вільно в межах кімнат і коридорів (?), але вся логіка (живлення, спавн, будівництво) — на рівні кімнат.
- Видимість: нові кімнати відкриваються лише відчиненням дверей (`info: hidden`); живлені кімнати світлі, неживлені — темні.
- Час — **real-time з паузою**, але економічний «тік» — подія: відчинення дверей (WP: «each turn starts when a new door opens»). Між дверима можна будувати й переставляти героїв без обмежень — час ресурсів не йде.
- 12 поверхів до перемоги; генерація поверху й вміст кімнат випадкові (`random: both` — і спавн хвиль, і знахідки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, атака, захист, швидкість, рівень, активні/пасивні вміння (?), спорядження | рухається за наказом (окремо чи загоном), сам бʼє ворогів у кімнаті |
| Кристал | object | Dust (= «HP» і бюджет живлення) | стоїть у стартовій кімнаті; ворог атакує → −Dust; 0 → поразка; на виході його несе герой |
| Кімната | zone | живлена/темна, слоти major/minor, вміст | живлена: працюють модулі; темна: точка спавну хвиль |
| Двері | gate | зачинені/відчинені | відчинити = хід (ресурси + шанс хвилі) |
| Слот major / minor | static | розмір | місце під модуль відповідного класу |
| Генератор Industry / Science / Food | static (major) | рівень | +ресурс щоходу, лише в живленій кімнаті |
| Турель / захисний модуль | tower (minor) | шкода, радіус, вартість Industry | атакує / лікує / сповільнює ворогів у кімнаті (?) |
| Монстр | enemy | HP, атака, тип цілі (?) | зʼявляється хвилею, іде до героїв і кристала |
| Темна кімната | spawner | — | на хвилі породжує монстрів |
| Купа Dust | resource | кількість | забрати → +Dust (більше кімнат живлення) |
| Обʼєкт для обшуку | container | — | дає ресурси (WP: «scavengeable objects») |
| Уцілілий | ally | герой | можна найняти в загін (до 4) |
| Торговець | neutral | товар, ціна | продає спорядження (?) за Dust (?) |
| Руїни Endless / артефакт | container | — | дослідження дає технологію/модуль (Steam: «decode Endless ruins») |
| Вихід (ліфт) | static | — | коли всі вцілілі там і кристал принесено → наступний поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open door)` → ТО `reveal(room)`, `custom: «хід +1»`, `currency(industry|science|food, +production)`; `rng(p)` → `spawn_at(wave, dark rooms)`.
- КОЛИ `input(power room)` → ЯКЩО `connected(room, crystal_rooms)` і `count(dust, >=, cost)` → ТО `set_state(room, powered)`; кімната світла, модулі в ній працюють.
- КОЛИ `input(unpower room)` → ТО `clear_state(room, powered)`, бюджет Dust повертається (?) — модулі в кімнаті вимикаються (WP: «reroute power»).
- КОЛИ `wave_start` → ТО для кожної темної кімнати `spawn_at(monster, room)` (WP: спавн у кімнатах «not activated or lacking its own power source»).
- КОЛИ `input(build module, slot)` → ЯКЩО `state(room, powered)` і `count(industry, >=, cost)` і слот потрібного розміру → ТО `place(module)`, `currency(industry, −cost)`.
- КОЛИ `input(research)` → ЯКЩО `count(science, >=, cost)` → ТО `unlock(module_type)`.
- КОЛИ `input(spend food on hero)` → ТО `heal(hero, n)` або `custom: «level +1 → стати + вміння»`.
- КОЛИ `in_range(turret, monster)` → ЯКЩО `state(room, powered)` → ТО `damage(n)`.
- КОЛИ `contact(monster, crystal)` → ТО `counter(dust, −n)`; КОЛИ `counter(dust, ==, 0)` → ТО `lose`.
- КОЛИ `hp_zero(monster)` → ТО `disappear_b`; `rng(p)` → `spawn(dust)`.
- КОЛИ `wave_cleared` → ТО `heal_full(all heroes)` (WP).
- КОЛИ `hp_zero(hero)` → ТО `disappear_a` назавжди; КОЛИ `all_gone(hero)` → ТО `lose`.
- КОЛИ `input(lift crystal)` → ЯКЩО `revealed(exit)` → ТО `carry(hero, crystal)`, `custom: «швидкість носія ↓»`, хвилі безперервні (?) — кімнати лишаються без живлення кристала (?).
- КОЛИ `hp_zero(carrier)` → ТО `lose` (WP).
- КОЛИ `all_on(alive heroes + crystal, exit)` → ТО `next_level`; КОЛИ поверх 12 пройдено → ТО `win`.
- КОЛИ `contact(hero, survivor)` → ЯКЩО `count(party, <, 4)` → ТО `custom: «найняти»`.
- Перемога: пройти 12 поверхів. Поразка: Dust кристала = 0, загинув носій кристала або всі герої. Рахунку як такого нема — прогрес = поверх і розблокування.

## Керування і ввід
- Миша: вибрати героя/усіх → клік по кімнаті — йти туди (автошлях, `control: indirect`); клік по дверях — відчинити.
- Режим будівництва: клік по слоту → меню доступних модулів з цінами; клік по кімнаті — живити/вимкнути.
- Кнопки вмінь героя (cooldown) і пауза (пробіл (?)) — real-time з тактичною паузою.
- Co-op онлайн до 4 гравців: кожен керує своїм героєм (?).

## Вікна, меню, HUD
- `game-screen` — розріз поверху «ляльковий будинок»; `resource-counters` Industry/Science/Food + Dust, `power-meter` (скільки кімнат ще можна живити), портрети героїв з `hp-bar` і `skill-bar`, мітки дверей, `minimap` (?).
- `custom-window` дослідження (`research-window`) — вибір технології за Science.
- `shop-window` — торговець.
- `inventory-window` героя — спорядження.
- `character-select` — вибір двох стартових героїв; `pod-select` — вибір рятувальної капсули (модифікатор забігу / складність) (?).
- `pause-menu`, `settings-window`, `end-screen` (смерть / поверх пройдено), `main-menu`, `lobby-window` для co-op.
- Переходи: `main-menu` → `pod-select` → `character-select` → `game-screen` ↔ модалі будівництва/дослідження/торгівлі → `end-screen`.

## Фічі поза полем
- `permadeath` (забіг до смерті), `meta-progression` — нові стартові герої відкриваються наймом і перемогами/3 поверхами (WP).
- `mode-coop` (онлайн до 4), `difficulty-presets` через капсули (?), `pause`, `achievements`, `cloud-save`.
- DLC додає модулі й героїв (WP: «Organic Matters» — нові модулі).

## Варіації й родичі
- Endless-всесвіт Amplitude: Endless Space / Endless Legend (ті самі ресурси й Dust).
- Родичі: FTL (кімнати корабля, живлення систем), Into the Breach (хід як подія), класичні TD (Kingdom Rush) — модулі на фіксованих слотах; Dungeon Keeper (кімнати як будівлі).
- Осі варіацій: **що рухає час** (кожен крок / таймер / подія-двері) · **де спавн** (точки рівня / темні зони / по краю) · **живлення** (усе / бюджет звʼязних кімнат / дроти) · **об'єкт захисту** (стоїть / його несуть).

## Цікавинки для курсу
- «Хід = відчинення дверей»: real-time бій, але економіка й спавн тікають лише від обраної події — 🥈 (два годинники в одному двіжку).
- Бюджет живлення на графі кімнат з умовою звʼязності з кристалом — 🥈 (BFS/компонента звʼязності + перерахунок при вимкненні).
- Спавн лише з темних кімнат: гравець малює карту спавну світлом — 🥉 (spawner = функція стану кімнати).
- Фаза «нести кристал»: глобальний перемикач стану рівня (усі правила спавну/живлення міняються) + повільний носій — 🥉.
- Генератори з доходом «за двері», а не «за секунду» — 📎.
- Слоти major/minor у кімнаті: TD без вільної розстановки — 📎.

## Мапа на каталог
- Є: `dungeon-generation` (граф кімнат) · `enemy-waves` · `spawn-points` (темні кімнати) · `hp-damage` · `inventory-items` · `round-currency` (3 ресурси + Dust) · `shop-catalog` (торговець) · `in-round-upgrades` (рівні героїв, дослідження) · `reach-exit` · `sequential-levels` · `player-death` · `game-pause` · `temporary-modes` (вміння героїв) · `chase-bfs` (монстри йдуть до кристала) · `cell-click`.
- **Нема** → пропозиції карток:
  - `+door-turn` «Хід = відчинити двері» · game-logic/waves · 🥈 · слоти {income_per_door, wave_chance}.
  - `+room-power-grid` «Живлення звʼязних кімнат з бюджету» · game-logic/economy · 🥈 · слот {budget}.
  - `+dark-room-spawn` «Спавн у неживлених зонах» · entities/spawn · 🥉.
  - `+module-slots` «Будівництво лише на слотах кімнати (major/minor)» · game-logic/economy · 📎.
  - `+carry-objective` «Нести обʼєкт до виходу, носій уповільнений» · game-logic/win · 🥉.
  - `+per-turn-income` «Генератори дають ресурс за хід» · game-logic/economy · 📎.
  - `+research-unlock` «Дослідження відкриває нові типи будівель» · game-logic/economy · 📎.
  - `+hero-skills` «Активні вміння з cooldown» · entities/state · 📎.
  - `+recruit-ally` «Найняти NPC у загін» · entities/interact · 📎.
  - `+wave-clear-heal` «Кінець хвилі лікує загін» · entities/state · 🌱.
  - `+permadeath` — як у Rogue.

## Пропозиції до словників
- `+trigger:door_opened` — гравець відчинив двері (тут — тік економіки й хвиль); `+trigger:wave_cleared` — ⏳, вжито; `+trigger:lifted(crystal)` — обʼєкт-ціль підняли (зміна фази рівня).
- `+cond:powered(room)` — кімната живлена; `+cond:connected` — ⏳ (🔥), вжито: кімната звʼязна з кристалом.
- `+effect:power(room)` / `+effect:unpower(room)` — можна як `set_state`, але з бюджетом; `+effect:build(module, slot)` — близько до `place`; `+effect:carry` — 🔥 нове, вжито.
- `+role:tower` (🔥), `+role:zone`, `+role:spawner` — вжито; `+role:slot` — місце під будівлю (не `static`, бо приймає обʼєкт).
- `+ui:resource-counters` (як у 868-HACK) · `+ui:power-meter` — вільний бюджет живлення · `+ui:door-marker` — значок дверей, які можна відчинити.
- `+window:research-window` — вибір технології; `+window:character-select` (⏳); `+window:pod-select` — модифікатор забігу.
- `+feature:mode-coop` (⏳), `+feature:permadeath`.
- `+axis:turn-structure=event` — real-time, але «хід» відлічується подією гравця.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Dungeon_of_the_Endless) — ресурси за двері, Dust і живлення «continuous room sets», спавн у темних кімнатах, лікування після хвилі, носій кристала, 12 рівнів, платформи.
- [Steam](https://store.steampowered.com/app/249050/Dungeon_of_the_ENDLESS/) — «minor and major modules», Endless ruins, co-op до 4.
- [Fandom-вікі](https://dungeonoftheendless.fandom.com/wiki/Dungeon_of_the_Endless_Wiki) — модулі й герої (не відкрилось ботом, 402).
- YouTube: пошук «dungeon of the endless gameplay».

## Непевне
- (?) Ціна живлення кімнати в Dust і чи повертається Dust при вимкненні — з памʼяті.
- (?) Типи minor-модулів (атакувальні / захисні / підтримки), стат «Wit» і «операція» модуля героєм — вікі не прочитано.
- (?) Що відбувається з живленням під час перенесення кристала (усе гасне чи лише спавн безперервний).
- (?) Торговець продає за Dust; капсули як модифікатори складності; пауза пробілом — з памʼяті.
- (?) Рух героїв всередині кімнат — вільний чи клітинний; поле позначене `graph` за логікою кімнат.
