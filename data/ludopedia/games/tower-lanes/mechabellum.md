---
title: Mechabellum
slug: mechabellum
family: tower-lanes
also: [tactics]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2023
platforms: [PC (Windows, Steam)]
links:
  - {kind: fandom, url: "https://mechabellum.wiki.gg/", best: true, note: "вікі: усі юніти за ціною, спеціалісти, підкріплення, термінологія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mechabellum", note: "раунди, постачання, розстановка без керування, HP гравця, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/669330/Mechabellum/", note: "1v1 ladder, 2v2, FFA, Survival, Rift Mode; тех-дерево юнітів"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Supply", note: "дохід 200×раунд, ціна рангу"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Tower", note: "Command/Research Center, tower debuff"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Reinforcement", note: "4 спільні картки щораунду, рівні карток"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Specialist", note: "16 спеціалістів, ±HP гравця"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/XP", note: "досвід і ранги"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Crawler", note: "приклад юніта: 24 у загоні, 6 технологій, контри"}
  - {kind: fandom, url: "https://mechabellum.wiki.gg/wiki/Category:Terminology", note: "chaff, AA, flank, beacon, tech bar, device"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mechabellum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [round-currency, drag-drop-piece, hp-damage, melee-vs-ranged, projectile-shot, blast-wave, speed-per-type, chase-greedy, in-round-upgrades, shop-catalog, shop-buyback, move-timer, ai-opponent, leaderboard, replay, enemy-waves, +auto-battle, +deployment-phase, +blind-simultaneous-deploy, +persistent-army, +unit-rotate-facing, +tower-range, +unit-counters, +tech-per-unit-type, +cost-escalation, +rank-up-by-xp, +shared-card-offer, +specialist-start, +player-hp-race, +core-building-debuff, +equipment-slots, +waypoint-beacon, +squad-unit, +interest-economy]
proposes: ["+trigger:phase_start", "+trigger:round_end", "+cond:target_type", "+cond:xp_full", "+effect:place", "+effect:rank_up", "+effect:tech", "+effect:sell", "+effect:choose", "+role:unit", "+role:tower", "+role:device", "+ui:deploy-grid", "+ui:range-circle", "+ui:tech-bar", "+ui:card-offer", "+ui:player-hp", "+ui:deploy-timer", "+window:choice-window", "+window:loadout-select", "+window:replay-window", "+feature:mode-versus", "+feature:mode-coop", "+feature:rank-tiers", "+axis:turn-structure=simultaneous"]
author: opus
date: 2026-11-02
---

# Mechabellum — тактика лише розстановкою: став загони на свою половину, обери технології, і дивись автобій

## Суть
Двоє гравців одночасно й наосліп **розставляють загони мехів на своїй половині поля**, купують технології й картки підкріплення за постачання (supply), а потім армії б'ються **самі** — керувати в бою не можна. Армія зберігається між раундами: юніти стоять на тих самих місцях і воскресають щораунду, додаються нові. Програвший раунд втрачає HP гравця; хто перший на нулі — програв. Ядро — передбачити розстановку суперника й поставити контри (анти-повітря проти авіації, «чаф» проти снайперів, анти-гігантів проти титанів).

## Поле і час
- Поле — прямокутна арена, поділена «Лінією» навпіл; кожен гравець розставляє на своїй половині, загін прив'язується до сітки розстановки (?) з поворотом (вертикально/горизонтально).
- Фланги — вузькі краї поля: юніти, поставлені там, з'являються з затримкою 10 с (телепорт).
- Дві фази раунду: **розстановка** (обмежений час, одночасно) → **бій** (real-time автобій, вільні координати, 3D). Тому `time: programmed` — гравець задає стан, бій виконується без вводу.
- Інформація `partial`: у фазі розстановки видно армію суперника з минулого раунду, але не нові покупки, доки не почнеться бій (?).
- Камера: 3D-вид згори з обертанням і зумом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін (squad) | unit (+role) | ціна 100–800, к-сть у загоні, HP, ATK, інтервал, дальність, швидкість, цілі (земля/повітря), ранг | у бою йде до найближчої цілі й атакує; не керується |
| Crawler | unit | 100, 24 шт., ближній бій, лише наземні | чаф: швидкий рій, з'їдає снайперів і гігантів |
| Fang / Marksman / Arclight / Hound / Void Eye / Vortex | unit | 100 | дешеві: рій стрільців, снайпер, ланцюгова блискавка, … |
| Mustang / Wasp / Phoenix / Sledgehammer / Steel Ball / Rhino / Stormcaller / Tarantula / Hacker / Fire Badger / Sabertooth / Phantom Ray | unit | 200 | середні: анти-повітря, авіація, анти-броня, ракети, хакер (переманює юніт) |
| Centurion / Farseer / Scorpion / Typhoon / Wraith | unit | 300 | важкі середні |
| Fortress / Melting Point / Raiden / Sandworm / Vulcan | unit | 400 | гіганти: промінь, що наростає по великих цілях; бур із-під землі; вогнемет |
| Overlord | unit | 500 | повітряний гігант |
| Abyss / Death Knell / Mountain / War Factory | unit | 800 | титани; War Factory виробляє юніти в бою (?) |
| Command Center | tower (+role) | HP за рівнем, апгрейд | ліва вежа; дає разові бусти на раунд |
| Research Center | tower | HP за рівнем | дає постійні апгрейди й навички на матч |
| Defensive Cannon / Wall | static | цінність 100 / 50 | з'являються на мапі, не купуються |
| Пристрій (device) | device (+role) | ≤ 8 на гравця | ставиться на поле, лишається між раундами |
| Наземний вогонь | hazard | — | від запальних бомб і підпаленої нафти, шкодить усім |
| Маяк (Mobile Beacon) | switch | 2 точки | задає загону маршрут із двох точок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(deploy)` → ТО `currency(+200×round)` (+ модифікатори спеціаліста/карток); `timer(start)`.
- КОЛИ `phase_start(deploy)` (раунд ≥ 2) → ТО `choose(4 cards)` — **ті самі 4 картки обом гравцям**; або `custom: «пропустити → постачання замість картки»`. Рівні карток: 0–1 з раунду 2, 2 з раунду 3, 3 з раунду 4.
- КОЛИ `input(place, unit, cell, facing)` → ЯКЩО `custom: «тип відкрито»` and `has(supply, value)` and `custom: «клітина на своїй половині й вільна»` → ТО `place(unit)`, `currency(-value)`.
- КОЛИ `input(unlock, unit_type)` → ЯКЩО `has(supply, unlock_cost)` → ТО `unlock(type)` (Crawler — безкоштовно; спеціалісти знижують).
- КОЛИ `input(tech, unit_type, t)` → ЯКЩО `count(techs(type), <, 4)` and `has(supply, price)` → ТО `custom: «effect tech: технологія діє на всі загони типу»`, `custom: «кожна покупка тех. +200 до цін наступних»` (`cost-escalation`).
- КОЛИ `custom: «cond xp_full(unit)»` and `input(rank_up, unit)` → ЯКЩО `has(supply, base/2)` → ТО `custom: «effect rank_up: HP і ATK лінійно ×ранг (ранг 3 = ×3)»`.
- КОЛИ `input(sell, unit)` (навичка Field Recovery) → ТО `currency(+value)`, `disappear_a`.
- КОЛИ `phase_start(battle)` → ТО обидві армії `custom: «з'являються на збережених позиціях з повним HP»`; гравець не має вводу.
- КОЛИ `tick` → юніт `chase-greedy` до найближчої дозволеної цілі; КОЛИ `in_range(unit, target, r)` → ЯКЩО `custom: «cond target_type: земля/повітря дозволено»` → ТО `damage(atk)` (сплеск, ланцюг — за типом).
- КОЛИ `contact(attacker, victim)` → `custom: «контри як таблиця: чаф проти повільних великих, анти-повітря проти авіації, промінь Melting Point наростає на одній цілі»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`; `custom: «XP: половина — тому, хто добив, решта — живим, хто шкодив»`.
- КОЛИ `hp_zero(enemy_tower)` → ТО армія власника `custom: «tower debuff: −80% швидкості, −90% шкоди, +50% отримуваної шкоди на 9 с (L1) … 1 с (L5)»`.
- КОЛИ `custom: «trigger round_end: одна армія знищена або вийшов час»` → ТО гравець без армії `custom: «HP −= шкода від уцілілих юнітів суперника»` (?).
- КОЛИ `custom: «HP гравця = 0»` → ТО `lose`.
- Між раундами: вежі `respawn` з повним HP; усі юніти повертаються на свої клітини; рух старих юнітів — лише картками/маяком (?).
- Перемога: HP суперника = 0 · Поразка: твоє HP = 0 · Рахунок: MMR, рейтинг ліги.

## Керування і ввід
- Миша: картка юніта з панелі → drag на свою половину (`drag-drop-piece`); привид показує footprint і **коло дальності**; клавіша/ПКМ — поворот на 90°.
- Клік по загону — панель: ранг, XP, технології (`tech bar` з 4 слотами), продаж, обладнання.
- Вибір картки підкріплення з 4 запропонованих; Ready — завершити розстановку раніше таймера.
- Навички (spells) — ціль-точка на полі; маяк — 2 точки маршруту.
- У бою — лише камера, пришвидшення недоступне в PvP (?).

## Вікна, меню, HUD
- `main-menu`: Play (Ranked 1v1, 2v2, FFA, Survival solo/co-op, Rift Mode) · Hangar (тех-дерево юнітів) · Replays · Settings.
- `lobby-window` / пошук суперника; `character-select` (⏳) → вибір спеціаліста: 4 варіанти «спеціаліст + стартовий набір юнітів», 25 с на вибір (`+window:loadout-select`).
- `game-screen` (розстановка): поле з `+ui:deploy-grid` твоєї половини, `+ui:range-circle`, панель юнітів з цінами, `+ui:card-offer` (4 картки), `coins` (supply), `+ui:player-hp` обох гравців, `+ui:deploy-timer`, номер раунду, `+ui:tech-bar` вибраного загону.
- `game-screen` (бій): 3D-автобій, HP-смужки загонів, лічильник армії.
- `end-screen` раунду: шкода по HP, хто переміг; кінець матчу — MMR.
- `replay-window` (⏳): повтори матчів; `leaderboard` / ліги; щотижневі турніри.
- Переходи: main-menu → пошук → вибір спеціаліста → [розстановка ↔ бій]×N → end-screen.

## Фічі поза полем
- `mode-versus` (1v1 Ranked, 2v2, FFA), `mode-coop` (Survival проти хвиль ШІ), Rift Mode (правила змінюються), Star Expedition (інший набір цін) (?).
- `rank-tiers` + MMR, `leaderboard-online`, тижневі турніри, `replay`, `spectator` (?).
- Hangar: мета-налаштування дерева технологій юніта між матчами (?); Credits — валюта відкриття контенту поза матчем; скіни.

## Варіації й родичі
- Auto chess (TFT, Dota Auto Chess): лава/поле, автобій; Mechabellum — без лави, без злиття, армія накопичується.
- Totally Accurate Battle Simulator / Ultimate Epic Battle Sim (розстановка без раундів), Super Auto Pets (асинхронні раунди), Arknights (розстановка в TD), Into the Breach (наміри видно).
- **Осі варіацій**: розстановка — один раз / **щораунду з накопиченням** · інформація — бачиш суперника / **наосліп одночасно** / асинхронний «привид» · керування в бою — пряме / навички / **жодного**.

## Цікавинки для курсу
- Одночасна розстановка наосліп + автобій на сітці (детермінований симулятор, однаковий для обох) — 🥇.
- Таблиця контр (тип атаки × тип цілі: земля/повітря, чаф, гігант) як дані — 🥉 (`interaction-table`).
- Армія зберігається між раундами й воскресає на тих самих клітинах — 📎 (стан = список розстановок).
- Технології на тип юніта з ціною, що росте з кожною покупкою — 🌱.
- XP-ділення (добивання ½, решта — учасникам) і ранг ×N — 📎.
- Однакова пропозиція карток обом гравцям щораунду — 🌱.

## Мапа на каталог
- Є: `round-currency` ↔ supply · `drag-drop-piece` ↔ розстановка · `hp-damage` · `melee-vs-ranged` ↔ ближній/дальній, земля/повітря · `projectile-shot` · `blast-wave` ↔ сплеск · `speed-per-type` · `chase-greedy` ↔ рух до цілі в бою · `in-round-upgrades` ↔ технології, ранги · `shop-catalog` ↔ панель юнітів · `shop-buyback` ↔ Field Recovery · `move-timer` ↔ таймер розстановки · `ai-opponent` (Survival) · `leaderboard` · `replay` · `enemy-waves` (Survival).
- **Нема** → пропозиції карток:
  - `+auto-battle` (є, TFT) · `+deployment-phase` (є, tactics) · `+tower-range` (спільна) · `+cost-escalation` (є) · `+interest-economy` (є, тут — «позика» Rapid Resupply).
  - `+blind-simultaneous-deploy` «Обидва розставляють одночасно, не бачачи нового» · game-logic/opponent · 🥈.
  - `+persistent-army` «Армія зберігається і воскресає на тих самих місцях щораунду» · game-logic/waves · 📎.
  - `+unit-rotate-facing` «Поворот загону при розстановці» · interface/input · 🌱.
  - `+unit-counters` «Таблиця контр тип×тип» · entities/combat · 🥉.
  - `+tech-per-unit-type` «Технологія діє на всі юніти типу (≤4)» · game-logic/economy · 📎.
  - `+rank-up-by-xp` «Ранг відкривається досвідом, купується валютою» · entities/state · 📎.
  - `+shared-card-offer` «Однакові картки обом гравцям» · game-logic/opponent · 🌱.
  - `+specialist-start` «Стартовий модифікатор з балансом HP» · game-logic/difficulty · 🌱.
  - `+player-hp-race` «HP гравця падає за програні раунди» · game-logic/lose · 🌱.
  - `+core-building-debuff` «Знищена вежа накладає дебаф на армію» · entities/state · 📎.
  - `+equipment-slots` «Обладнання на юніт з лімітом слотів» · entities/state · 📎.
  - `+waypoint-beacon` «Маршрут юніту двома точками» · entities/move · 🌱.
  - `+squad-unit` «Загін з N тіл як одна покупка» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:phase_start` (🔥) — розстановка/бій; `+trigger:round_end` — раунд завершено.
- `+cond:target_type` — атакуючий може бити цей тип цілі (земля/повітря); `+cond:xp_full` — досвіду досить для рангу.
- `+effect:place` (🔥) — розстановка з запасу; `+effect:rank_up` — підвищити ранг; `+effect:tech` — технологія на тип; `+effect:sell`; `+effect:choose` — картка з 4.
- `+role:unit` (🔥 у TFT/Arknights), `+role:tower` — тут вежі-ядра, не стріляють (?); `+role:device` — постійний предмет на полі.
- `+ui:deploy-grid` — сітка своєї половини; `+ui:range-circle`; `+ui:tech-bar`; `+ui:card-offer`; `+ui:player-hp`; `+ui:deploy-timer`.
- `+window:choice-window` (вибір картки), `+window:loadout-select` (спеціаліст + стартовий набір), `+window:replay-window`.
- `+feature:mode-versus`, `+feature:mode-coop`, `+feature:rank-tiers`.
- `+axis:turn-structure=simultaneous` (🔥) — розстановка одночасна, бій без вводу.

## Джерела
- ⭐ [Mechabellum Wiki](https://mechabellum.wiki.gg/) — усі юніти за ціною (100…800), лінки на спеціалістів, підкріплення, термінологію.
- [Wikipedia: Mechabellum](https://en.wikipedia.org/wiki/Mechabellum) — раунди, постачання, розстановка без керування, HP гравця, режими, Game River, ранній доступ 2023 / реліз 2024.
- [Steam](https://store.steampowered.com/app/669330/Mechabellum/) — тех-дерево юнітів, контри, 1v1/2v2/FFA/Survival/Rift.
- [Supply](https://mechabellum.wiki.gg/wiki/Supply) — 200×раунд, вартість рангу = база + ½ бази за ранг, продаж за поточною вартістю.
- [Tower](https://mechabellum.wiki.gg/wiki/Tower) — дві вежі, HP за рівнями, tower debuff, відновлення щораунду.
- [Reinforcement](https://mechabellum.wiki.gg/wiki/Reinforcement) · [Specialist](https://mechabellum.wiki.gg/wiki/Specialist) · [XP](https://mechabellum.wiki.gg/wiki/XP) · [Crawler](https://mechabellum.wiki.gg/wiki/Crawler) · [Terminology](https://mechabellum.wiki.gg/wiki/Category:Terminology).
- YouTube: пошук «mechabellum gameplay».

## Непевне
- (?) Формула шкоди по HP гравця в кінці раунду (від цінності уцілілих юнітів?) — вікі не відповіла.
- (?) Чи розстановка прив'язана до сітки клітин, чи вільна з кроком; розмір footprint загонів.
- (?) Що саме видно від суперника в фазі розстановки.
- (?) Чи вежі стріляють; ціна відкриття типів (Crawler 0, решта ?).
- (?) Чи старі юніти можна переставити (крім маяка й карток).
