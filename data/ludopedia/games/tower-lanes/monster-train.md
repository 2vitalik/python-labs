---
title: Monster Train
slug: monster-train
aka: [Monster Train First Class]
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: layers
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2020
platforms: [PC, Xbox One, Switch, iOS, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Monster_Train", best: true, note: "потяг з 4 поверхів, піра нагорі, призов істот на 3 нижні поверхи"}
  - {kind: official, url: "https://themonstertrain.com", note: "вороги піднімаються на поверх щоходу, 5 кланів, DLC Wurmkin"}
  - {kind: steam, url: "https://store.steampowered.com/app/1102190/Monster_Train/", note: "клани основний+допоміжний, чемпіони, 25 рівнів Covenant, Hell Rush на 8, Daily, Custom Challenge"}
  - {kind: other, url: "https://www.bluestacks.com/blog/game-guides/monster-train/mstn-beginners-guide-en.html", note: "гайд: ember, capacity, Dark Forge, апгрейди піри, trials, крамниці"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=monster+train+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [enemy-waves, spawn-schedule, enemy-reached-base, hp-damage, status-effects, run-relics, round-currency, shop-catalog, shop-between-levels, inventory-limit, telegraphed-intents, ai-opponent, map-window, character-select, difficulty-select, daily-puzzle, leaderboard, online-multiplayer, permadeath, +deck-draw, +lane-grid, +floor-ascend, +floor-capacity, +champion-upgrade, +dual-clan-deck, +card-upgrade-slots, +pyre-core, +front-unit-combat, +run-meta-carry]
proposes: ["+role:card", "+role:floor", "+trigger:combat_phase", "+trigger:ascend", "+effect:ascend", "+effect:draw_cards", "+effect:relocate", "+cond:capacity_free", "+ui:capacity-meter", "+ui:pyre-hp", "+ui:wave-preview", "+window:choice-window", "+window:forge-window", "+feature:run-map", "+feature:mutators", "+axis:session"]
author: opus
date: 2026-11-09
---

# Monster Train — вертикальний tower defense картами: вороги піднімаються поверхами потяга до піри

## Суть
Потяг у пекло має 4 поверхи: на трьох нижніх гравець картами **призиває істот-захисників** і кидає заклинання, на верхньому горить Піра — її HP і є життям забігу. Вороги заходять на нижній поверх і після кожного ходу, якщо вижили, **піднімаються на поверх вище**. На кожному поверсі бій іде сам: передні юніти сторін бʼють одне одного. Глибина — у розподілі ember (енергії) і місткості поверхів між трьома «смугами» та в синергіях двох обраних кланів.

## Поле і час
- Поле — 4 поверхи один над одним (`field: layers`): поверхи 1–3 мають місткість (capacity) для юнітів, поверх 4 — кімната Піри. Кожен поверх — ряд «спереду назад» для своїх і ворожих юнітів.
- Хід: гравець отримує ember і бере карти → грає юніти/заклинання на будь-який поверх → натискає «бій» → на поверхах, де є вороги, юніти атакують → вороги, що вижили, піднімаються на поверх вище → нова хвиля заходить знизу.
- Битва = серія хвиль; остання — бос, якого треба бити на кількох поверхах, поки він підіймається. Забіг — ланцюг битв з вибором маршруту між ними.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піра | static | HP (= HP забігу), атака | на верхньому поверсі; бʼє ворогів, що дійшли; HP 0 — кінець забігу |
| Поверх 1–3 | zone (`+role:floor`) | capacity | вміщує юнітів, сумарний розмір ≤ capacity |
| Кімната Піри (4-й) | zone | — | вороги тут атакують Піру |
| Чемпіон | ally | клан, гілки апгрейдів | особливий юніт-лідер; апгрейдиться в Dark Forge |
| Юніт-істота | ally (`+role:unit`) | атака, HP, розмір, ціна в ember, ключові слова | стоїть на поверсі; бʼється, доки не загине; сам не піднімається |
| Заклинання | supply (`+role:card`) | ціна в ember | разовий ефект: шкода, баф, дебаф; місця не займає |
| Ember | resource | на хід | енергія для карт; невитрачене — (?) |
| Ворог | enemy | атака, HP, ключові слова | заходить знизу; після бою, якщо вижив, піднімається на поверх |
| Бос | boss | великий HP, фази (?) | остання хвиля битви; повільно піднімається, бити на кількох поверхах |
| Колода/рука | supply | рука N карт (?) | беруть щохід; апгрейд піри може дати +карту |
| Артефакт | pickup | — | пасивне правило на забіг |
| Золото | resource | — | для крамниць: апгрейди карт, видалення карт |
| Клан | neutral | основний + допоміжний | пул карт і механік (Hellhorned, Awoken, Stygian Guard, Umbra, Melting Remnant, Wurmkin у DLC) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `currency(+ember)`, `custom: «взяти карти до розміру руки»`.
- КОЛИ `input(play, unit, floor)` → ЯКЩО `has(ember, cost)` and `custom: «на поверсі вистачає capacity під розмір юніта»` and `custom: «поверх 1–3»` → ТО `place(unit, floor)`, `currency(-cost)`; інакше `block`.
- КОЛИ `input(play, spell, floor|target)` → ЯКЩО `has(ember, cost)` → ТО ефект заклинання (`damage(n)`, `set_state(target, buff|debuff)`), `currency(-cost)`.
- КОЛИ `input(end_turn)` → ТО `custom: «trigger combat_phase»`: на кожному поверсі з ворогами передній юніт кожної сторони атакує переднього юніта іншої (`damage(atk)`), раунди атак тривають до загибелі однієї сторони (?).
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`, `custom: «наступний юніт стає переднім»`.
- КОЛИ `custom: «бій на поверсі завершено»` → ЯКЩО `count(enemies_on_floor, >, 0)` → ТО `move(enemies, floor+1)` (вороги піднімаються).
- КОЛИ `enter(enemy, pyre_room)` → ТО `custom: «Піра і ворог бʼються»`: `damage(pyre, atk)`; КОЛИ `hp_zero(pyre)` → ТО `lose`.
- КОЛИ `schedule(waves)` → ТО `spawn_at(wave, floor_1)`; наступну хвилю видно наперед (превʼю).
- КОЛИ `wave_cleared` and `custom: «була остання хвиля і бос знищений»` → ТО `choose(card_rewards)`, `currency(+gold)`, `custom: «перехід до вибору маршруту»`.
- КОЛИ `custom: «ключове слово Sweep»` → ТО `damage(all_enemies_on_floor)`; Trample — надлишок шкоди переходить на наступного; Multistrike — додаткова атака; Quick — бʼє першим (?).
- КОЛИ `custom: «статуси Armor/Damage Shield»` → ТО поглинають шкоду; Spikes — `damage(attacker)`; Regen — `heal` на початку ходу; Frostbite — шкода за хід (?).
- КОЛИ `custom: «чекпоінт піри»` → ТО `choose(+ember | +card_draw | +capacity)` (апгрейд піри між битвами).
- КОЛИ `enter(player, dark_forge)` → ТО `choose(champion_upgrade_path)`.
- КОЛИ `enter(player, merchant)` → ЯКЩО `has(gold, price)` → ТО `custom: «апгрейд карти в один з вільних слотів»` або `custom: «видалити карту»`.
- КОЛИ `input(choose, trial)` → ТО `custom: «посилити бій модифікатором»` + більша нагорода.
- Перемога: пройти всі битви й останнього боса · Поразка: HP Піри = 0 · Рахунок: Covenant-рівень, рахунок Daily/Hell Rush.

## Керування і ввід
- Миша/геймпад/тач: drag карти з руки на поверх (юніт) або на ціль (заклинання); вибір поверху стрілками; кнопка «Fight!»/кінець ходу.
- Перемикання камери між поверхами; наведення — `tooltip` юніта з ключовими словами й намірами ворога.

## Вікна, меню, HUD
- `main-menu`: забіг, Daily, Custom Challenge, Hell Rush, налаштування, вихід.
- `character-select` — вибір основного й допоміжного клану, чемпіона; `difficulty-select` — рівень Covenant 0–25; мутатори (Wild Mutations).
- `game-screen`: розріз потяга з 4 поверхами, `+ui:capacity-meter` кожного поверху, `+ui:pyre-hp`, `energy-bar` (ember), рука карт, `+ui:wave-preview`/`wave-counter` (лічильник хвиль доданий у Friends & Foes), `end-turn-button`, `tooltip`.
- `map-window` — дві гілки маршруту між битвами з вузлами (крамниці, події, кузня).
- `+window:choice-window` — драфт карт/юнітів після бою; `+window:forge-window` — Dark Forge (гілки чемпіона), апгрейд карт.
- `shop-window` — торговці (апгрейди, видалення); `stats-window` — run records; `end-screen`; `leaderboard` (Daily, Custom).
- Hell Rush: `lobby-window` на 8 гравців.

## Фічі поза полем
- `meta-progression`: рівні кланів (по 10) відкривають карти, артефакти, альтернативних чемпіонів.
- `difficulty-presets` — 25 рівнів Covenant; `+feature:mutators` — 35 мутаторів у Custom.
- `mode-daily` — Daily Challenge з мутаторами й таблицею; `level-sharing` — Custom Challenge з кодом і своєю таблицею.
- `online-multiplayer` — Hell Rush: 8 гравців одночасно з однаковими картами, виборами й ворогами.
- `mod-support` — Steam Workshop (Herzal's Workshop); `autosave`, `achievements`.

## Варіації й родичі
- Monster Train 2 (2025): той самий каркас, нові клани.
- Родичі в сімʼї: [plants-vs-zombies](plants-vs-zombies.md) (смуги, захисники на клітинах), [inscryption](inscryption.md) і [wildfrost](wildfrost.md) (карти-істоти на полі), [dungeon-warfare](dungeon-warfare.md) (вороги йдуть до ядра); поза сімʼєю — Slay the Spire (каркас декбілдера).
- **Осі варіацій**: смуги — горизонтальні (PvZ) / вертикальні поверхи з підйомом (MT) · захисник — вежа на клітині / юніт-карта з місткістю · ціль ворога — край поля / ядро-Піра з HP.

## Цікавинки для курсу
- Вертикальні смуги з підйомом ворогів після кожного ходу — 🥉 (стан = список поверхів, черга юнітів).
- Місткість поверху + розмір юніта (рюкзак у кожній смузі) — 📎.
- Бій «передній проти переднього» з Sweep/Trample/Multistrike — 🥉.
- Піра як ядро з HP і власною атакою — 🌱.
- Колода з двох кланів + слоти апгрейду карт — 🥉.
- Hell Rush: синхронний забіг 8 гравців з однаковим seed — 🥈.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` ↔ хвилі знизу · `enemy-reached-base` ↔ ворог у кімнаті Піри · `hp-damage` · `status-effects` ↔ ключові слова · `run-relics` ↔ артефакти · `round-currency` ↔ ember · `shop-catalog` + `shop-between-levels` ↔ торговці · `inventory-limit` ↔ capacity поверху · `telegraphed-intents` ↔ превʼю хвилі · `map-window` · `character-select` · `difficulty-select` · `daily-puzzle` · `leaderboard` · `online-multiplayer` ↔ Hell Rush · `permadeath`.
- **Нема** → пропозиції карток:
  - `+floor-ascend` «Вороги піднімаються поверхами після ходу» · entities/move · 🥉.
  - `+floor-capacity` «Місткість смуги під розміри юнітів» · entities/legality · 📎 · слот {capacity}.
  - `+champion-upgrade` «Чемпіон з гілками апгрейдів» · game-logic/economy · 📎.
  - `+dual-clan-deck` «Колода з двох пулів-кланів» · game-logic/economy · 📎.
  - `+card-upgrade-slots` «Карта зі слотами апгрейдів» · game-logic/economy · 📎.
  - `+pyre-core` «Ядро-база з HP і атакою» · game-logic/lose · 🌱.
  - `+front-unit-combat` «Бій передніх у черзі» · entities/combat · 📎.

## Пропозиції до словників
- `+role:card` — карта руки/колоди; `+role:floor` — поверх-смуга з місткістю; `+role:unit` — бойовий юніт загону.
- `+trigger:combat_phase` — фаза автоматичного бою після кінця ходу; `+trigger:ascend` — ворог перейшов на поверх вище.
- `+effect:ascend` — перемістити ворога на поверх вище; `+effect:relocate` — перемістити свій юніт на інший поверх; `+effect:draw_cards` — взяти N карт.
- `+cond:capacity_free` — на поверсі є місце під розмір.
- `+ui:capacity-meter` · `+ui:pyre-hp` · `+ui:wave-preview`.
- `+window:choice-window` · `+window:forge-window` (кузня апгрейдів).
- `+feature:run-map` · `+feature:mutators` (модифікатори правил забігу) · `+axis:session` — `run`.

## Джерела
- ⭐ [Wikipedia: Monster Train](https://en.wikipedia.org/wiki/Monster_Train) — вертикальний потяг з 4 поверхів, піра нагорі, призов лише на 3 нижні; Shiny Shoe, 2020; платформи; Monster Train 2 (2025).
- [Офіційний сайт](https://themonstertrain.com) — вороги піднімаються на поверх щоходу, шкодять Пірі; 5 кланів; DLC The Last Divinity (Wurmkin).
- [Steam](https://store.steampowered.com/app/1102190/Monster_Train/) — основний+допоміжний клан, 10 рівнів клану, чемпіони, 220+ карт, апгрейд карти двічі, 25 Covenant, Hell Rush, Daily, Custom, 35 мутаторів, Workshop.
- [BlueStacks: гайд для новачків](https://www.bluestacks.com/blog/game-guides/monster-train/mstn-beginners-guide-en.html) — ember, capacity, Dark Forge, апгрейди піри (ember / карта / capacity), trials, торговці.

## Непевне
- (?) Точний порядок бою на поверсі (хто бʼє першим, скільки раундів) — з памʼяті; Fandom-вікі віддає 402.
- (?) Значення: ember на хід, розмір руки, capacity поверху, HP Піри, кількість битв у забігу.
- (?) Перелік і точні ефекти ключових слів (Sweep, Trample, Multistrike, Quick, Armor, Spikes, Regen, Frostbite, Rage, Dazed, Rooted) — з памʼяті.
- (?) Чи переноситься невитрачений ember (здається, ні).
