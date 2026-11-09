---
title: "Neuroshima Hex!"
slug: neuroshima-hex
aka: [Neuroshima Hex, NS Hex, "Neuroshima Hex! 3.0", Нейрошіма Гекс]
family: tactics
also: [board-digital]
klass: hybrid
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: state
year: 2005
platforms: [board, iOS, Android, PC]
links:
  - {kind: other, url: "https://rulespal.com/neuroshima-hex/rulebook", best: true, note: "повні базові правила: поле 19 гексів, типи тайлів, бій за ініціативою, броня, сітка, модулі, миттєві дії, кінець гри, режими 3–4 гравців"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Neuroshima_Hex!", note: "HQ 20 ОЗ, «добери 3 — скинь 1», армії й розширення, цифрова версія iOS/Android"}
  - {kind: wiki, url: "https://pl.wikipedia.org/wiki/Neuroshima_Hex!", note: "польський оригінал: 19 полів, 35 тайлів на армію, видання 2.0 / 3.0 / 4-те"}
  - {kind: steam, url: "https://store.steampowered.com/app/2324150/Neuroshima_Hex/", note: "цифрова версія 2025: AI, кампанія, локальний і онлайн-мультиплеєр, 10 армій + DLC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Neuroshima+Hex+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, orientation-state, tile-rotate, cursor-place, explode-area, coverage-area, hot-seat, ai-opponent, online-multiplayer, sequential-levels, character-select, game-screen, end-screen, +hex-grid-render, +deck-draw, +draw-n-discard-one, +instant-action-tile, +battle-trigger-tile, +initiative-order, +multi-initiative, +simultaneous-resolution, +directional-attacks, +armor-by-facing, +net-disable, +module-adjacency-buff, +knockback, +hq-health-victory, +board-full-trigger, +final-battle-on-deck-end, +asymmetric-sides]
proposes: ["+trigger:board_full", "+trigger:deck_empty", "+trigger:battle_start", "+effect:draw_card", "+effect:discard", "+effect:knockback", "+effect:disable", "+cond:facing_side", "+role:base", "+role:module", "+role:card", "+ui:initiative-tracker", "+ui:hq-health-track", "+ui:hand-of-cards", "+ui:deck-counter", "+axis:turn-structure:place-then-battle", "+card:initiative-battle"]
author: opus
date: 2026-11-09
---

# Neuroshima Hex! — викладай тайли-загони на 19 гексів, а бій вибухне сам, коли хтось зіграє «Бій» або поле заповниться

## Суть
Двоє (до чотирьох) гравців ведуть постапокаліптичні армії; кожна — колода з ~35 гексових тайлів і штабу (HQ) із 20 ОЗ. Хід — добрати до 3 тайлів, один скинути, решту викласти на поле, зіграти як миттєву дію або притримати. Юніти нерухомі після викладання: важать **позиція й поворот** тайла (стрілки атак, броня й сітка — на конкретних гранях). Бій не відбувається щоходу: його запускає тайл «Бій» або повне поле, і тоді всі юніти бʼють фазами ініціативи від старшої до 0. Клас `hybrid`: `cursor` (викладання тайлів рукою) + `figure` (кожен тайл — фігура зі своїм патерном атак); лінія — тактична сутичка, викладання тайлів — `also: board-digital`.

## Поле і час
- Поле — **19 гексів** (шестикутник зі стороною 3); у частині режимів і розширень використовують зовнішнє кільце ще з 18 гексів; розширене поле для 4 гравців — **37 гексів**.
- Шари: гекс → один тайл (юніт, модуль або HQ); маркери ран і сіток лежать поверх тайла. Кожен тайл має **6 граней**, і значки на гранях працюють у свій бік.
- Хід гравця — фаза викладання (без бою). **Бій** — окрема процедура поза ходами: фази ініціативи від найвищої до 0; юніти з однаковою ініціативою діють **одночасно**, знищені знімаються лише в кінці фази.
- Інформація повна: тайли добирають лицем догори, склад армій відомий; випадковий лише порядок колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Штаб (HQ) | base | 20 ОЗ на треку; особлива здібність армії | ставиться першим на будь-який вільний гекс; у бою бʼє melee силою 1 усіх сусідніх ворогів; ніколи не шкодить іншому HQ |
| Воїн (warrior) | piece | ініціатива 0–4 (може бути кілька значків), стрілки melee / ranged із силою, броня на гранях, сітка, toughness, mobility | після викладання стоїть і дивиться, як поклали; бʼє у фазах своєї ініціативи |
| Воїн без значка ініціативи | piece | — | діє одразу після викладання й доки лежить (напр. сітка) |
| Модуль Officer | piece | стрілки зʼєднання | +1 сила melee/ranged своїм зʼєднаним юнітам |
| Модуль Scout | piece | стрілки зʼєднання | +1 ініціатива зʼєднаним юнітам |
| Модуль Medic | piece | стрілки зʼєднання | гасить рани однієї ворожої атаки по зʼєднаному юніту, потім скидається |
| Тайл «Бій» (Battle) | card | — | закінчує хід і запускає бій; заборонений, щойно хтось добрав останній тайл |
| Тайл «Рух» (Move) | card | — | свій юніт — на сусідній вільний гекс та/або довільний поворот |
| Тайл «Відкинути» (Push Back) | card | — | сусідній до свого юніта ворог відлітає на 1 гекс, лишаючи проміжок |
| Тайл «Граната» (Grenade) | card | — | повністю знищує ворожий юніт на гексі поруч зі своїм HQ; не HQ |
| Тайл «Снайпер» (Sniper) | card | — | 1 рана будь-якому ворожому юніту; не HQ |
| Тайл «Авіаудар» (Air Strike) | card | зона 7 гексів | 1 рана цілі й усім сусідам, і своїм, і чужим; не HQ |
| Колода армії | supply | ~34 тайли + HQ | джерело добору; кінець колоди запускає фінал |
| Рука (тайли перед гравцем) | supply | ≤ 3 | що лишилось після скиду; можна притримати на наступний хід |
| Маркер рани | mark | — | рахує рани проти toughness |
| Маркер сітки | mark | — | показує, що юніт / HQ «спутаний» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `place(player, hq)` на вільний гекс: спершу перший гравець, потім другий; HQ можуть сусідити.
- КОЛИ `turn_start(side)` → ЯКЩО `first_time` → ТО `custom: «перший гравець бере 1 тайл і розігрує його, другий — 2; далі звичайно»`.
- КОЛИ `turn_start(side)` → ТО `custom: «добрати тайли лицем догори до 3 у руці»`, потім `custom: «рівно 1 тайл скинути»`; решту — викласти, зіграти або притримати.
- КОЛИ `custom: «усі тайли перед гравцем — миттєві дії»` → ТО `custom: «скинути їх і добрати знову (Unlucky Draw), скільки завгодно разів»`.
- КОЛИ `input(place, unit, hex)` → ЯКЩО `free(hex)` → ТО `place(player, unit)`, `rotate(unit, deg)` — поворот обирається при викладанні й далі не змінюється без спецздібності.
- КОЛИ `input(place, module, hex)` → ЯКЩО `free(hex)` → ТО `place(player, module)`, `custom: «бафи діють одразу й обовʼязково на свої юніти/HQ, у бік яких дивиться стрілка модуля; ефекти кількох модулів сумуються»`.
- КОЛИ `input(play, battle)` → ЯКЩО `not custom: «хтось уже добрав останній тайл»` → ТО `end_turn`, `custom: «почати бій»`.
- КОЛИ `custom: «на полі не лишилось вільного гекса»` → ТО `custom: «почати бій»`; повторювати бої, доки поле повне або гра не скінчилась.
- КОЛИ `phase_start(initiative=N)` (від найбільшої до 0, порожні фази пропускаються) → ЯКЩО `custom: «юніт має значок ініціативи N»` and `not state(unit, netted)` → ТО `custom: «юніт виконує всі свої атаки»`; однакова ініціатива — одночасно.
- КОЛИ `custom: «melee-стрілка юніта»` → ЯКЩО `occupied(adjacent_in_dir, enemy)` → ТО `damage(enemy, strength)` — автоматично, без кидків.
- КОЛИ `custom: «ranged-стрілка юніта»` → ЯКЩО `line_of_sight(unit, enemy)` (перший ворог на прямій у бік стрілки, будь-яка дальність, свої не заважають) → ТО `damage(enemy, strength)`.
- КОЛИ `custom: «ranged-атака влучає»` → ЯКЩО `custom: «у цілі броня на грані, звідки прийшов постріл»` → ТО `custom: «сила −1»` (постріл силою 1 повністю блокується); на melee, снайпера, гранату й авіаудар броня не діє.
- КОЛИ `after(damage(unit, n))` → ЯКЩО `custom: «ран більше, ніж значків toughness»` → ТО `custom: «юніт знищено, але він ще діє до кінця поточної фази»`.
- КОЛИ `custom: «фаза ініціативи завершилась»` → ТО `disappear(destroyed_units)` у скид.
- КОЛИ `after(damage(hq, n))` → ТО `counter(hq_health, −n)`.
- КОЛИ `after(place(player, net_unit))` → ЯКЩО `occupied(net_dir, enemy)` → ТО `set_state(enemy, netted)`: не атакує, не рухається, не штовхає й не штовхається, не дає бафів; діє й на HQ; броню та toughness не знімає.
- КОЛИ `custom: «дві сітки дивляться одна на одну або ≥3 сітки замкнуті в коло»` → ТО `clear_state(all_of_them, netted)`.
- КОЛИ `phase_start(initiative=hq)` → ТО `damage(adjacent_enemies, 1)` по всіх шести гранях; на ворожий HQ не діє; номер фази HQ — (?).
- КОЛИ `custom: «ворожа атака по зʼєднаному з медиком юніту»` → ТО `custom: «рани цієї атаки ігноруються»`, `disappear(medic)`; якщо медика і юніта вдарили одночасно — гине медик, юніт не врятовано.
- КОЛИ `input(play, move, unit)` → ЯКЩО `free(adjacent)` and `not state(unit, netted)` → ТО `move(unit, hex)` та/або `rotate(unit, any)`.
- КОЛИ `input(mobility, unit)` (у свій хід, не в бою) → ЯКЩО `free(adjacent)` → ТО `move(unit, hex)` та/або `rotate(unit, any)`.
- КОЛИ `input(play, push_back, enemy)` → ЯКЩО `adjacent(own_unit, enemy)` and `free(hex_beyond)` and `not state(enemy, netted)` and `not state(own_unit, netted)` → ТО `push(enemy)` на 1 гекс (куди — обирає власник цілі), без повороту; нема куди — тайл не грається.
- КОЛИ `input(play, grenade, enemy)` → ЯКЩО `adjacent(enemy, own_hq)` and `not same(enemy, hq, type)` and `not state(own_hq, netted)` → ТО `disappear(enemy)`.
- КОЛИ `input(play, sniper, enemy)` → ЯКЩО `not same(enemy, hq, type)` → ТО `damage(enemy, 1)`.
- КОЛИ `input(play, air_strike, hex)` → ЯКЩО `custom: «уся зона 7 гексів у межах поля»` → ТО `explode(hex7, 1)` — по 1 рані всім тайлам зони, крім HQ.
- КОЛИ `custom: «гравець добрав останній тайл»` → ТО `custom: «він доводить хід, суперник ходить ще раз, потім фінальний бій»`; далі бій можливий лише від повного поля.
- КОЛИ `hp_zero(hq)` → ТО `win` для іншого гравця; обидва HQ у тому самому бою → `draw`.
- КОЛИ `custom: «фінальний бій завершено, обидва HQ живі»` → ТО `custom: «перемагає більше здоровʼя HQ; рівність — ще по ходу й бій; знову рівність — нічия»`.
- Перемога: знищити ворожий HQ або мати більше ОЗ штабу після фінального бою · Поразка: свій HQ на 0 · Рахунок: лише ОЗ штабів (у 3–4 гравців є опційне правило очок).

## Керування і ввід
- Настільна: взяти тайли з колоди, вибрати скид, покласти тайл на гекс і повернути гранню куди треба; миттєві дії — оголосити й скинути.
- Цифрова версія: рука з 3 тайлів унизу, перетягування тайла на гекс і обертання перед підтвердженням; скид — окремою дією; кнопка «закінчити хід». Під час бою — анімація фаз ініціативи (?).
- Режими: 2 гравці; 3 гравці (deathmatch, deathmatch з очками, 1 проти команди); 4 гравці (deathmatch, команди, з очками); цифрова — соло з AI, кампанія, локально на одному ПК, онлайн PvP.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Кампанія → `chapter-select` (?) · Соло проти AI → `match-setup` · Локальна гра · Онлайн → `lobby-window` · Налаштування → `settings-window`.
- `character-select` (цифрова версія): вибір армії (база: Moloch, Hegemony, Borgo, Outpost, Steel Police, Smart, Vegas, New York, Beasts, Mississippi; DLC — Neojungle, Sharrash, Uranopolis).
- `game-screen`: гексове поле 19 гексів; `hand-of-cards` (3 тайли); зона скиду; `hq-health-track` обох сторін (20 → 0); `deck-counter` (?) — скільки тайлів лишилось; під час бою — `initiative-tracker` (поточна фаза), `popup-text` ран.
- `codex-window` (цифрова версія, ?) — довідка тайлів армії (у настолці — аркуш армії).
- `end-screen`: переможець / нічия, лишок ОЗ штабів.
- Переходи: main-menu → character-select → game-screen ↔ бій (той самий екран) → end-screen.

## Фічі поза полем
- `ai-opponent-levels` (цифрова; рівні — ?), `local-multiplayer`, `online-multiplayer`, `levels-sequential` (сюжетна кампанія Steam-версії).
- `custom-rules`: варіанти Alternative Beginning, Reinforcement, Structures, Leaders, Battle Atlas; розширене поле 37 гексів для 4 гравців.
- `mode-coop`-подібне: командні матчі 2×2 і «1 проти команди» у настолці.
- `rules-page` — аркуш армії з HQ-здібністю й переліком тайлів.

## Варіації й родичі
- Видання: 2005 (PL, Portal), 2-ге (2007 PL / 2008 Z-Man EN, більше поле), 3.0 (2013), Rok Molocha (2021), 4-те (2025, 20-річчя). Розширення-армії: 20+ (Neojungle, Dancer, New York, Steel Police, Sharrash, Mephisto, Doomsday Machine — заборонена на турнірах, …, Wiremen 2025); Babel 13, Duel.
- Цифрові: iOS (2010) і Android (2012) від Big Daddy's Creations — правила «по суті ідентичні», бій автоматизовано, лише соло; Steam-версія Baked Games (2025).
- Родичі в корпусі: [Memoir '44](memoir-44.md) (гекси й кидки замість детермінованих ран), [Faeria](faeria.md) (викладання земель і істот на гекси), [Duelyst](duelyst.md) (карта = юніт на полі), [Into the Breach](into-the-breach.md) (детермінований бій, штовхання); паралельний файл пачки — Summoner Wars (карта = юніт).
- Осі варіацій:
  - **коли бій**: щоходу (більшість тактик) / лише за тригером — тайл «Бій» або повне поле (Neuroshima);
  - **хто рухається**: усі юніти щоходу / юніти нерухомі, рух — лише миттєвою дією або mobility;
  - **влучання**: кидок / детерміновано за силою (Neuroshima) / кидок проти захисту;
  - **порядок атак**: почергово / фази ініціативи з одночасністю й відкладеним зняттям;
  - **броня**: число HP / грань тайла, що гасить лише постріл з того боку.

## Цікавинки для курсу
- Бій фазами ініціативи N → 0 з одночасною дією й відкладеним зняттям знищених — 🥉 (двофазне оновлення стану: спершу всі шкоди, потім видалення).
- Постріл-промінь уздовж однієї з 6 гексових осей, крізь своїх, до першого ворога; броня — за гранню, звідки прийшов — 🥉 (кубічні координати гекса + зворотний напрям).
- Тайл з орієнтацією: значки на 6 гранях і перерахунок під час повороту — 📎.
- Сітки, що скасовують одна одну, і замкнені кола сіток — 🥈 (розвʼязання залежностей у графі «хто кого спутав», пошук циклів).
- Модулі зі стрілками зʼєднання, бафи сумуються, медик гасить одну атаку — 📎.
- «Добери до 3 — скинь 1» + Unlucky Draw + фінальний бій після кінця колоди — 🌱.
- AI, що симулює бій для кожного варіанта викладання й повороту, — 🥇 (пошук за 19 гексами × 6 поворотів × тайли руки).

## Мапа на каталог
- Є: `hp-damage` ↔ ОЗ штабу й toughness · `melee-vs-ranged` ↔ два види стрілок · `line-of-sight-attack` ↔ ranged по прямій до першого ворога · `orientation-state` + `tile-rotate` ↔ поворот тайла задає напрями атак, броні й сітки · `cursor-place` ↔ викладання на вільний гекс · `explode-area` ↔ авіаудар на 7 гексів · `coverage-area` ↔ модулі бафають сусідів у напрямках стрілок · `hot-seat`, `ai-opponent`, `online-multiplayer` · `sequential-levels` ↔ кампанія Steam · `character-select` ↔ вибір армії · `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+initiative-order` «Фази ініціативи з одночасністю» · game-logic/opponent · 🥉 · слот {max_initiative: 4, simultaneous: true, removal: end_of_phase}.
  - `+multi-initiative` — кілька значків ініціативи = атака в кожній з фаз.
  - `+battle-trigger-tile` «Бій за тригером» · game-logic/opponent · 📎 · слот {triggers: [battle_tile, board_full, deck_end]}.
  - `+draw-n-discard-one` «Добери N — скинь 1» · game-logic/random · 🌱 · слот {hand: 3, discard: 1, redraw_if_all_instant}.
  - `+instant-action-tile` — тайл-дія, що не лишається на полі (снайпер, граната, рух, відкидання).
  - `+directional-attacks` «Стрілки атак на гранях фігури» · entities/combat · 📎 · слот {sides: 6}; `+armor-by-facing` (Steel Panthers) — броня гранню.
  - `+net-disable` «Сітка: вимкнути фігуру» · entities/state · 🥈 · слот {mutual_cancel, cycles}.
  - `+module-adjacency-buff` «Модуль-баф сусідів» · entities/state · 📎.
  - `+knockback` (корпус) — відкидання на 1 гекс із вибором клітини власником.
  - `+hq-health-victory` «ОЗ штабу як рахунок» · game-logic/win · 🌱.
  - `+board-full-trigger`, `+final-battle-on-deck-end` — тригери кінця/бою; `+asymmetric-sides` — армії з різними наборами тайлів; `+hex-grid-render`, `+deck-draw`.

## Пропозиції до словників
- `+trigger:board_full` — на полі не лишилось вільних клітин (бій у Neuroshima; уже пропонували інші ігри).
- `+trigger:deck_empty` — останній тайл колоди добрано (фінальний бій).
- `+trigger:battle_start` — почалась окрема процедура бою поза ходами.
- `+effect:draw_card` — добрати тайл/карту з колоди; `+effect:discard` — скинути з руки.
- `+effect:knockback` — відкинути ціль на N клітин від джерела.
- `+effect:disable` — вимкнути сутність (сітка): не діє, не рухається, не дає бафів.
- `+cond:facing_side` — удар прийшов з грані, де є значок (броня).
- `+role:base` — штаб/база з ОЗ, чия загибель = поразка; `+role:module` — тайл, що не бʼється, а бафає сусідів; `+role:card` — одноразовий тайл-дія.
- `+ui:initiative-tracker` — поточна фаза ініціативи; `+ui:hq-health-track` — трек ОЗ штабів; `+ui:hand-of-cards` — тайли в руці; `+ui:deck-counter` — скільки тайлів лишилось у колоді.
- `+axis:turn-structure:place-then-battle` — ходи лише викладають, бій — окрема процедура за тригером.
- `+card:initiative-battle` — картка «бій фазами ініціативи» як завдання.

## Джерела
- ⭐ [RulesPal: Neuroshima Hex rulebook](https://rulespal.com/neuroshima-hex/rulebook) — поле 19/37 гексів, хід «до 3 — скинь 1», Unlucky Draw, перший хід 1/2 тайли, типи тайлів, усі миттєві дії, модулі Officer/Scout/Medic, броня, сітка (взаємне скасування й кола), toughness, mobility, бій від найвищої ініціативи до 0, кінець колоди → фінальний бій, нічиї, режими 3–4 гравців, варіанти.
- [Wikipedia EN: Neuroshima Hex!](https://en.wikipedia.org/wiki/Neuroshima_Hex!) — HQ 20 ОЗ, «три тайли, один скинути», бій від тайла, базові армії, перелік армій-розширень, цифрова версія Big Daddy's Creations (iOS 2010, Android 2012).
- [Wikipedia PL: Neuroshima Hex!](https://pl.wikipedia.org/wiki/Neuroshima_Hex!) — 19 полів, 35 тайлів на армію, видання й кількість армій (25).
- [Steam: Neuroshima Hex](https://store.steampowered.com/app/2324150/Neuroshima_Hex/) — Baked Games, 2 червня 2025: соло з AI, кампанія, локальний і онлайн-мультиплеєр, 10 армій + 3 DLC.
- YouTube: пошук «Neuroshima Hex how to play».

## Непевне
- (?) Кількість тайлів армії: RulesPal одночасно каже «35 тайлів» і «34 інших + HQ»; PL-вікі — 35 разом.
- (?) Ініціатива штабу: RulesPal не називає фазу, в якій бʼє HQ (з памʼяті — 0); у правилі позначено як `initiative=hq`.
- (?) Особливі здібності HQ базових армій (Moloch, Outpost, Borgo, Hegemony) — на аркушах армій, у джерелах не наведено; не описано.
- (?) Вікна цифрових версій (кампанія як вибір глав, довідка тайлів, лічильник колоди, рівні AI) — з опису Steam і припущень; сторінку інтерфейсу не бачив.
- (?) Чи блокує броня постріл силою 2 частково (−1 → 1): так за RulesPal («reduces by 1»); з кількома модулями Officer сила може бути більшою.
