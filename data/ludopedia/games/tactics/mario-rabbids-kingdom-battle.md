---
title: "Mario + Rabbids Kingdom Battle"
slug: mario-rabbids-kingdom-battle
aka: [Mario + Rabbids, "Mario Rabbids", MRKB, "Mario + Rabbids: Donkey Kong Adventure"]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2017
platforms: [Switch]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Mario_%2B_Rabbids_Kingdom_Battle", best: true, note: "Super Mario Wiki: рух 6 клітин, 3 дії, Dash 20, Team Jump 6, труби, укриття 50/100 %, зброя, техніки, цілі, дерева навичок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mario_%2B_Rabbids_Kingdom_Battle", note: "3 з 8 героїв (Маріо + ≥1 Раббід), 3 дії, Honey/Burn, цілі, світи, Skill Orbs, DLC, сиквел"}
  - {kind: fandom, url: "https://www.mariowiki.com/Super_Effect", note: "таблиці зброї з ефектами і шансами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mario+Rabbids+Kingdom+Battle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, legal-move-highlight, reachable-highlight, path-preview, threat-range, height-levels, destroy-all-enemies, reach-exit, ai-opponent, status-effects, telegraphed-intents, difficulty-levels, sequential-levels, world-map, shop-between-levels, character-select, +action-slots, +cover-system, +hit-chance-tiers, +dash-through-damage, +team-jump, +warp-pipe-move, +height-attack-bonus, +overwatch, +reaction-attack, +cooldown-ability, +aura-buff, +knockback-push, +destructible-blocks-cover, +escort-npc, +turn-limit-score, +party-constraints, +skill-tree-respec, +super-effect-proc, +local-coop, +easy-mode-toggle]
proposes: ["+trigger:enemy_moved", "+trigger:attacked", "+effect:dash", "+effect:team_jump", "+effect:bounce_launch", "+cond:cover", "+cond:cooldown_ready", "+ui:hit-chance", "+ui:action-pips", "+window:loadout", "+window:skill-tree", "+window:chapter-result", "+feature:easy-mode-toggle"]
author: opus
date: 2026-11-09
---

# Mario + Rabbids Kingdom Battle — XCOM для всіх: шанс лише 0/50/100 %, а рух сам є атакою і стрибком

## Суть
Покрокова тактика в стилі XCOM: загін із трьох героїв (Маріо обовʼязково, плюс щонайменше один Раббід) проти Раббідів-ворогів на клітинній арені з укриттями. Головне — **рух як зброя**: прохід крізь ворога завдає шкоди тараном (Dash), а стрибок від союзника (**Team Jump**) подовжує рух і закидає на висоту. Влучання спрощено до **0 / 50 / 100 %** за укриттям; ефекти зброї (мед, підпал, відскок, фарба…) спрацьовують з шансом і ламають плани ворога. Кожен герой має три дії: рух, постріл (основна або другорядна зброя), техніка.

## Поле і час
- Квадратна сітка-арена з **висотами** (платформи, сходи, труби-телепорти); з висоти — бонус до шкоди.
- Укриття — блоки на клітинах: низьке (50 % блоку прямого пострілу) і високе (100 %); цеглові блоки руйнуються від промахів і сплеш-шкоди.
- Хід: спочатку всі герої гравця в будь-якому порядку, потім вороги; можна закінчити хід раніше.
- Повна інформація: видно рух і зону атаки ворога при наведенні; шанс влучання показано перед пострілом.
- Випадковість: шанс 50 % за низьким укриттям, шанс суперефекту зброї (10–60 %), критичні влучання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маріо | piece | рух 6, HP, Blaster + Melee | обовʼязковий у загоні; Hero Sight — реакційний постріл; M-Power — аура +шкоди |
| Луїджі | piece | Precision (дальність 15) | Steely Stare — далекий реакційний постріл |
| Піч | piece | Boomshot | Healing Jump (лікує при приземленні), Protection −30 % шкоди |
| Йоші | piece | Blaster | Ground Pound, Egg Beater — реакційний постріл 100 %, Super Chance |
| Раббід Маріо / Піч / Луїджі / Йоші | piece | різна зброя | Magnet Dance (тягне ворогів), щити, Vamp Dash (30 шкоди, 30 % крадіжки HP), Outer Shell |
| Ворог-Раббід (Smasher, Hopper, Buckler, Supporter, Peek-a-Boo, Valkyrie, Ziggy, Summoner…) | enemy | HP, зброя, рух | ховається, фланкує, тараном бʼє героїв так само |
| Бос | boss | фази | великий HP, особливі патерни |
| Низьке укриття | terrain | блок 50 % | ховає від прямого пострілу |
| Високе укриття | terrain | блок 100 % | повністю ховає від прямого пострілу |
| Цегляний блок | terrain | міцність | укриття, що руйнується промахами і вибухами |
| Труба | static | вихід у радіусі 3+ | вхід → вихід у межах дальності труби |
| Пастки (Chain Chomp, Fire Burper, Spitting Statue, Ink Coconut…) | hazard | — | шкода або ефект при наближенні / за ходом |
| Тоад / Тоадетта (ескорт) | ally | HP | не атакує; має дійти/вижити |
| Зона цілі | zone | — | дійти героєм за ліміт ходів |
| Скриня / монета | pickup | — | поза боєм: монети, зброя, Power Orbs |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен герой має 3 дії: рух, зброя, техніка (кожна раз за хід)»`.
- КОЛИ `input(move, hero, cell)` → ЯКЩО `path_exists(hero, cell)` у межах руху (база 6, з навичками 7–9) → ТО `move`.
- КОЛИ `custom: «на шляху руху клітина ворога»` → ЯКЩО `custom: «Dash цього ходу ще не використано»` (?) → ТО `damage(enemy, dash)` (20 у Маріо/Піч/Луїджі/Йоші), рух триває.
- КОЛИ `enter(hero, ally_cell)` під час руху → ТО `custom: «Team Jump: стрибок до 6 клітин від союзника, через перешкоди й на висоту; рух подовжується»`; Маріо — Stomp Jump: `damage(enemy_under, 30)` при приземленні; Піч — `heal(allies_in_range, n)`.
- КОЛИ `enter(hero, pipe)` → ТО `teleport(hero, pipe_exit)` у межах дальності труби (з 3 до 4–6 клітин).
- КОЛИ `input(shoot, hero, target)` → ЯКЩО `in_range(hero, target, weapon_range)` → ТО `custom: «шанс = 100 % без укриття / 50 % за низьким / 0 % за високим (прямий постріл)»`; влучання → `damage(target, rng(min..max))`; промах → `damage(cover, n)`.
- КОЛИ `custom: «постріл з вищої клітини»` → ТО `multiplier(×bonus)` до шкоди.
- КОЛИ `input(secondary, hero)` → ЯКЩО `custom: «перезарядка готова»` → ТО `custom: «ракета / мілі зі сплешем 2–3 клітини / турель / граната»`; `timer(start, 1 хід)`.
- КОЛИ `custom: «влучання зброєю з ефектом»` → ЯКЩО `prob(effect_chance)` → ТО `set_state(target, effect, 1)`: Honey — `custom: «не може рухатися»`; Burn — `custom: «тікає у випадковий бік»`; Push — `push(target)`; Bounce — `custom: «підкидає і переносить ціль»`; Ink — `custom: «не може стріляти»`; Stone — `stun(target, 1)`; Vamp — `heal(attacker, part_of_damage)`; Freeze — `custom: «застигає»` (?).
- КОЛИ `custom: «ворог рухається в лінії огляду героя з реакцією»` → ЯКЩО `state(hero, reaction_ready)` → ТО `custom: «реакційний постріл по першому, хто рухається»` (Hero Sight 80 % шкоди), `timer(start, cooldown)`.
- КОЛИ `input(technique, Mario, M-Power)` → ТО `set_state(heroes_in_range_4, damage_up, 1)`; перезарядка 3 ходи.
- КОЛИ `input(technique, Rabbid_Mario, Magnet_Dance)` → ТО `pull(enemies_in_range)`.
- КОЛИ `input(technique, Peach, Protection)` → ТО `set_state(allies_in_range, shield_30, 1)`.
- КОЛИ `turn_start(enemy)` → ТО `custom: «вороги рухаються, тараном бʼють героїв, стріляють за тими ж правилами»`.
- КОЛИ `hp_zero(hero)` → ТО `set_state(hero, knocked_out)`; КОЛИ `custom: «всі герої вибиті»` → ТО `lose`.
- КОЛИ `all_gone(enemy)` → ЯКЩО `mode(defeat_all)` → ТО `win`; КОЛИ `reach(hero, goal_zone)` → ЯКЩО `mode(reach)` і `counter(turn, ≤, limit)` → ТО `win`; КОЛИ `reach(escort, goal_zone)` → ЯКЩО `mode(escort)` → ТО `win`.
- КОЛИ `died(escort)` → ЯКЩО `mode(escort)` → ТО `lose`.
- КОЛИ `custom: «бій виграно»` → ТО `currency(+coins)`, `counter(power_orbs, +n)` за кількість ходів і вцілілих героїв.
- КОЛИ `input(easy_mode)` на старті бою → ТО `heal(heroes, full)` і `custom: «легший режим цього бою»`.
- Перемога: знищити всіх / дійти до зони / провести ескорт (і ще кілька типів місій) · Поразка: усі герої вибиті або ціль провалено · Рахунок: оцінка бою за ходами й вцілілими → монети й Power Orbs.

## Керування і ввід
- Геймпад: стік — курсор по клітинах; вибір героя → синя зона руху і `path-preview` (з позначками тарану і Team Jump); A — підтвердити.
- Перемикання зброї основна / другорядна / техніка (кнопки дій); наведення на ворога показує шанс влучання 0/50/100 % і прогноз шкоди.
- Наведення на ворога показує його рух і дальність (`threat-range`); Y — кінець ходу раніше; перемикання камери і огляд арени.
- Поза боєм — керування Beep-0 на карті світу: рух загону, головоломки, скрині.

## Вікна, меню, HUD
- `main-menu`: Continue · Load · Options; карта світу як хаб.
- `world-map` (світ з лінійною стежкою) — `game-screen` дослідження: головоломки, скрині, монети, входи в бої.
- `custom-window` «Battle prep» (`+window:loadout`): вибір 3 героїв (Маріо + ≥1 Раббід), зброя кожного, перегляд цілі бою.
- `game-screen` бою: арена, HP-смуги героїв і ворогів (`hp-bar`), іконки дій кожного героя (`+ui:action-pips`), `+ui:hit-chance` над ціллю, `objective-text` і `turn-counter` з лімітом, `telegraph-marker` для пасток.
- `shop-window` — Battle Shop: зброя за монети.
- `custom-window` «Skill tree» (`+window:skill-tree`): 4 гілки (рух / атака / техніка / інше), обовʼязкові перші вузли, безкоштовний скид.
- `end-screen` (`+window:chapter-result`): оцінка за ходи й вцілілих, нагорода.
- `settings-window`; `mode-select` для коопу і versus.

## Фічі поза полем
- 4 світи, розділи по 3 бої, кожен світ відкриває нову здібність Beep-0 для дослідження.
- Прогресія: `meta-progression` через Power Orbs → дерево навичок кожного героя (HP, рух, техніки), скид безкоштовно; монети → зброя.
- Easy mode — вмикається на старті будь-якого бою, лікує загін.
- `mode-coop` (локальний, двоє гравців по 2 героя, окремі арени) · versus (оновлення: 3 дії на всіх трьох героїв).
- DLC Donkey Kong Adventure (2018: новий загін, Sleep), Ultra Challenge, Amiibo-зброя.

## Варіації й родичі
- Сиквел: Mario + Rabbids Sparks of Hope (2022) — вільний рух у зоні замість клітин, Sparks-сили.
- Родичі в корпусі: [XCOM](xcom.md) (укриття, фланг, Overwatch), [Into the Breach](into-the-breach.md) (детермінізм і поштовхи), [Fire Emblem](fire-emblem.md), [Hoplite](hoplite.md) (рух як атака), [Tactical Breach Wizards](tactical-breach-wizards.md).
- **Осі варіацій**: шанс влучання — гладкий % ([xcom](xcom.md)) / 0-50-100 (MRKB) / без шансу ([Into the Breach](into-the-breach.md)) · рух — лише переміщення / таран крізь ворога / стрибок від союзника / труби-телепорти · реакція — Overwatch на всіх / реакційна техніка з перезарядкою.

## Цікавинки для курсу
- Три рівні шансу за типом укриття і напрямком пострілу (прямий / фланг) — 🌱.
- Таран під час руху: шкода кожному ворогу на шляху без зупинки — 📎.
- Team Jump: союзник як трамплін, що перераховує досяжність (BFS з «вузлами-стрибками») — 🥉.
- Суперефекти зброї з шансом: мед, підпал (випадкова втеча), відскок, фарба — 📎.
- Реакційний постріл по першому, хто рухається в лінії огляду + перезарядка — 📎.
- Обмеження складу загону («Маріо + ≥1 Раббід») при виборі — 🌱.
- Труби: телепорт з дальністю виходу як частина руху — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `legal-move-highlight` + `reachable-highlight` · `path-preview` · `threat-range` · `height-levels` · `destroy-all-enemies` · `reach-exit` · `ai-opponent` · `status-effects` · `telegraphed-intents` (пастки) · `difficulty-levels` (Easy mode) · `sequential-levels` · `world-map` · `shop-between-levels` · `character-select`.
- **Нема** → пропозиції карток:
  - `+action-slots` «Дії за типом: рух, зброя, техніка — по одній» · game-logic/turns · 🌱.
  - `+hit-chance-tiers` «Шанс 0/50/100 % за укриттям» · entities/combat · 🌱.
  - `+dash-through-damage` «Таран під час руху крізь ворога» · entities/combat · 📎.
  - `+team-jump` «Стрибок від союзника» · entities/move · 🥉.
  - `+warp-pipe-move` «Труба-телепорт з дальністю виходу» — близька до `teleport-one-way`.
  - `+destructible-blocks-cover` «Укриття ламається від промахів» — близька до `destructible-blocks`.
  - `+super-effect-proc` «Ефект зброї з шансом» · entities/combat · 📎.
  - `+party-constraints` «Обовʼязкові учасники загону» · interface/windows · 🌱.
  - `+skill-tree-respec` «Дерево навичок зі скидом» · game-logic/progress · 📎.
  - `+easy-mode-toggle` «Легкий режим на старті будь-якого бою» · game-logic/settings · 🌱.
  - `+cover-system` / `+overwatch` / `+reaction-attack` / `+cooldown-ability` / `+aura-buff` / `+knockback-push` / `+height-attack-bonus` / `+escort-npc` / `+turn-limit-score` / `+local-coop` — уже в корпусі.

## Пропозиції до словників
- `+trigger:enemy_moved` — ворог зробив крок у полі зору (реакційні постріли).
- `+trigger:attacked` — сутність атакована (щити, контрзахист).
- `+effect:dash` — шкода цілі на шляху руху без зупинки.
- `+effect:team_jump` — стрибок від союзника з новою зоною досяжності.
- `+effect:bounce_launch` — підкинути ціль і перенести в іншу клітину (Bounce).
- `+cond:cover` — ціль за укриттям рівня (none / half / full) відносно стрільця.
- `+cond:cooldown_ready` — здібність перезарядилась.
- `+ui:hit-chance` — шанс влучання над ціллю; `+ui:action-pips` — які дії героя ще доступні.
- `+window:loadout` — вибір загону і зброї перед боєм; `+window:skill-tree` — дерево навичок; `+window:chapter-result` — оцінка розділу.
- `+feature:easy-mode-toggle` — легкий режим на старті бою.

## Джерела
- ⭐ [Super Mario Wiki: Kingdom Battle](https://www.mariowiki.com/Mario_%2B_Rabbids_Kingdom_Battle) — рух 6 (до 7–9), 3 дії, Dash 20, Vamp Dash, Team Jump 6, труби 3→4–6, укриття 50/100 %, висота, зброя й дальності, техніки й перезарядки, типи місій, склад загону, дерева навичок, Easy mode, кооп, versus, вороги й пастки.
- [Wikipedia: Mario + Rabbids](https://en.wikipedia.org/wiki/Mario_%2B_Rabbids_Kingdom_Battle) — 3 з 8 героїв, Honey/Burn, умови поразки, 4 світи, розділи по 3 бої, Skill Orbs, DLC, сиквел.
- [Super Mario Wiki: Super Effect](https://www.mariowiki.com/Super_Effect) — зброя з ефектами і шансами 10–40 %.
- YouTube: пошук «Mario Rabbids Kingdom Battle gameplay».

## Непевне
- (?) Чи таран спрацьовує раз за хід і по скількох ворогах — джерело не каже.
- (?) Опис Bounce, Ink, Stone, Freeze, Sleep — з памʼяті (Honey і Burn підтверджено Wikipedia).
- (?) Чи фланг (не прямий постріл) повністю ігнорує укриття — у вікі лише «прямий постріл».
- (?) Пункти головного меню і назви кнопок — з памʼяті.
- (?) Розмір бонусу за висоту — не бачив.
