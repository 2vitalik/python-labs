---
title: Rogue Tower
slug: rogue-tower
aka: []
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: survive
year: 2022
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1843760/Rogue_Tower/", best: true, note: "шлях росте у вибраному напрямку, випадково звивається й розгалужується; висота дає шкоду; 400+ карток; мета-XP"}
  - {kind: other, url: "https://nodal.gg/game/rogue-tower-1843760", note: "коротко: unlock, build, upgrade, expand, defend; теги"}
  - {kind: other, url: "https://steamah.com/rogue-tower-basics-for-beginners/", note: "гайд: висота, Ballista/Mortar/Tesla, пріоритети цілей і XP веж, University, Mana Bank, Mine, Haunted House, DoT"}
  - {kind: other, url: "https://gameplay.tips/guides/rogue-tower-tips-for-winning-the-level.html", note: "гайд: кілька входів і довжини гілок, будинки → монети, Banditry, щити з 16-ї хвилі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rogue+tower+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, tower-placement, tower-range, height-levels, round-currency, in-round-upgrades, projectile-shot, shoot-cooldown, explode-area, status-effects, hp-damage, speed-per-type, unit-xp-skills, coverage-area, run-relics, spawner-entity, game-pause, save-progress, +path-grows-per-wave, +path-branching, +tile-expansion-choice, +upgrade-card-draw, +mana-resource, +shield-armor-layers, +targeting-priorities, +adjacency-income, +building-on-node, +meta-xp-unlocks, +card-pool-reset]
proposes: ["+trigger:expand", "+effect:extend_path", "+effect:draw_cards", "+effect:upgrade", "+role:tower", "+role:building", "+ui:range-circle", "+ui:expand-arrows", "+ui:mana-bar", "+window:choice-window", "+window:unlock-tree", "+feature:targeting-priorities"]
author: opus
date: 2026-11-09
---

# Rogue Tower — роглайк-TD, де шлях ворогів не дано, а він росте щохвилі новою плиткою туди, куди скажеш

## Суть
Починаєш з замку і короткого відрізка дороги. Щорівня гравець вибирає, в який бік **продовжити шлях**; нова плитка випадково звивається, повертає й часто **розгалужується**, тож входів (порталів спавну) стає більше. Вежі ставлять уздовж дороги, найкраще — на підвищення (висота дає шкоду й дальність). Нові вежі та апгрейди приходять **випадковими картками**; між забігами — досвід і постійні відкриття. Відмінність від Desktop TD і Fieldrunners: гравець не будує лабіринт веж, а **вирощує саму дорогу**, балансуючи довжину гілок, щоб хвилі з різних входів не прийшли до замку одночасно.

## Поле і час
- Квадратна сітка з рельєфом: плитки-фрагменти шляху з різною висотою клітин; хороших (високих) місць мало.
- Поле росте: щорівня додається плитка на кінці вибраної гілки; гілки = окремі входи ворогів.
- На мапі трапляються будинки, «жили»/вузли під будівлі, святилища (occult shrine) (?).
- Real-time з хвилями; 3D мінімалістична графіка, вільна камера; є пауза (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Замок | static | health | ворог дійшов → шкода замку; 0 → поразка |
| Плитка шляху | terrain | форма (пряма, поворот, розвилка), висоти | додається вибором напрямку; випадкова форма |
| Портал (кінець гілки) | spawner | — | вороги хвилі виходять з кожного кінця |
| Клітина з висотою | terrain | висота | вежа вище → більша шкода й дальність |
| Будинок | static | — | вежі навколо дають монети при кожному розширенні |
| Жила / вузол | resource | (?) | місце під особливу будівлю (University, Mana Siphon) |
| Ballista | tower | старт | одна ціль, сильна по HP, дешевий DPS |
| Mortar | tower | площа | сильна по броні, слабка по щитах; снаряд пропадає, якщо ціль загинула |
| Tesla | tower | мана, малий радіус | бʼє всіх у радіусі, сильна по щитах |
| Poison, Obelisk, Encampment… | tower | картки | Encampment ставить міни у випадкових місцях свого радіусу |
| Mana Siphon | custom | на кристалі (?) | +мана/с |
| Mana Bank | custom | 125g за мана/с | +мана/с і +макс. мана без кристала |
| University | custom | біля святилища | щорівня кидок на +шкоду всім вежам по HP/броні/щиту |
| Mine | custom | — | шанс ремонту замку, +HP |
| Haunted House | custom | мана | приховані апгрейди; окупається за 5–10 рівнів |
| Монстр | enemy | HP, броня, щит | іде гілкою до замку |
| Монстр-лікар / бігун / стрілець / породжувач | enemy | здібність | лікує, ривок, атака, спавн інших; аури посилюють сусідів |
| Щитоносці | enemy | з 16-го рівня | потрібні вежі проти щитів біля входів |
| Фінальний бос | boss | — | наприкінці забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(expand, branch_end)` → ТО `custom: «effect extend_path: на кінці гілки зʼявляється випадкова плитка»`; ЯКЩО `prob(p)` → плитка-розвилка, `spawn(portal)` на новому кінці.
- КОЛИ `custom: «trigger expand»` → ТО `currency(+wave × towers_around_houses)`.
- КОЛИ `schedule(waves)` → ТО `spawn_at(monsters, portals)` — з кожного кінця гілки.
- КОЛИ `tick` → монстр `move(a, next_on_path)` до замку.
- КОЛИ `input(place, tower, cell)` → ЯКЩО `free(cell)` and `custom: «клітина не на дорозі»` and `has(player, gold)` → ТО `place(player, tower)`, `currency(-cost)`.
- КОЛИ `input(place, tower, cell)` → ЯКЩО `custom: «висота клітини h»` → ТО `custom: «бонус шкоди й дальності за h»`.
- КОЛИ `in_range(tower, monster, r)` → ТО `custom: «вибрати ціль за пріоритетами (найбільше броні, найменше щита, найшвидший…), нічия — найближчий»`, `spawn(projectile)`.
- КОЛИ `contact(projectile, monster)` → ЯКЩО `state(monster, shielded)` → ТО `custom: «шкода по щиту, потім броні, потім HP; множник за типом вежі»`; інакше `damage(n)`.
- КОЛИ `contact(mortar_shell, cell)` → ТО `explode(area, n)`.
- КОЛИ `tick` → ЯКЩО `in_range(tesla, monster, r)` and `counter(mana, >=, cost)` → ТО `damage(n)` усім у радіусі, `counter(mana, -cost)`.
- КОЛИ `contact(projectile, monster)` → ЯКЩО `custom: «вежа має DoT-апгрейд»` → ТО `set_state(monster, poison|bleed|burn, dur)`; стеки отрути сповільнюють.
- КОЛИ `custom: «вежа вибрала ціль»` → ТО `custom: «XP вежі за характеристиками цілі — зростають відповідні стати»`.
- КОЛИ `hp_zero(monster)` → ТО `disappear(monster)`, `currency(+bounty)`; з Banditry — `currency(+n)` додатково.
- КОЛИ `custom: «монстр-породжувач»` and `timer(every)` → ТО `spawn(monster)` поруч (?).
- КОЛИ `reach(monster, castle)` → ТО `damage(castle, n)`, `disappear(monster)`.
- КОЛИ `hp_zero(castle)` → ТО `lose`.
- КОЛИ `counter(waves_until_draw, ==, 0)` → ТО `choose(options)` з випадкових карток: нова вежа / апгрейд вежі (шкода, дальність, вміння) / будівля.
- КОЛИ `level_end` → ЯКЩО `custom: «University поруч зі святилищем»` → ТО `custom: «кидок на кожен стат: +шкода всім вежам»`.
- КОЛИ `hp_zero(final_boss)` → ТО `win`.
- КОЛИ `game_over` → ТО `custom: «XP забігу → відкриття веж і карток у пулі; постійні бонуси до старту»`.
- Перемога: убити фінального боса (?) · Поразка: health замку = 0 · Рахунок: досягнутий рівень і XP.

## Керування і ввід
- Миша: стрілки на кінцях гілок — клік обирає напрямок розширення.
- Вибір вежі/будівлі з панелі → клітина (видно висоту й радіус).
- Клік по вежі — апгрейд за гроші, пріоритети цілей (комбінації: «найбільше броні + найменше щита + найповільніший»).
- Вікно картки: вибрати одну з кількох.

## Вікна, меню, HUD
- `main-menu` → `+window:unlock-tree` (постійні відкриття за XP; скидання XP прибирає відкриття з пулу) → `game-screen`.
- `game-screen`: 3D-мапа, `coins` (gold), `+ui:mana-bar`, `hp-bar` замку, `wave-counter`, `+ui:expand-arrows`, `+ui:range-circle`, панель веж і будівель.
- `+window:choice-window` — вибір з випадкових карток апгрейду/відкриття (з «скринь» або щорівня).
- `end-screen` — рівень, отриманий XP.

## Фічі поза полем
- `meta-progression`: XP після забігу відкриває вежі й картки, що можуть випасти; постійні покупки дають невеликий бонус старту.
- Скидання XP — єдиний спосіб прибрати відкриту картку з пулу (`+card-pool-reset`).
- 400+ карток і апгрейдів; картки на кшталт «Increase Draw Frequency» — картки щорівня.
- Одиночна гра, без режимів у джерелах.

## Варіації й родичі
- Родичі: `emberward` (роглайк-TD з картками, але лабіринт з тетроміно), `isle-of-arrows` (плитки-острови з вежами), `wildfrost`/`monster-train` (картки), `desktop-tower-defense` і `fieldrunners` (шлях з веж); з `build-sim` — розширення мапи плитками (Dorfromantik).
- Наступники жанру «шлях росте»: Kingdom-плиткові TD (?).
- **Осі варіацій**: хто формує шлях — дизайнер / вежі гравця / плитки, які обирає гравець · ріст шляху — нема / щохвилі / за ресурс · кількість входів — фіксована / росте з розвилками · нагорода — гроші / випадкові картки / обидва.

## Цікавинки для курсу
- Дорога, що росте плиткою в обраний бік, з випадковими поворотами й розвилками — 🥈 (граф шляху, прибудова плиток, кілька спавнів).
- Балансування довжин гілок, щоб хвилі не приходили разом — 🥉 (довжина шляху = час прибуття).
- Висота клітини як множник шкоди/дальності — 🌱.
- Шари захисту ворога (щит → броня → HP) з множниками за типом вежі — 📎.
- Пріоритети цілей + XP вежі за типом цілі — 🥉.
- Монети за вежі навколо будинку (сусідство) — 🌱.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` · `tower-placement` + `tower-range` · `height-levels` ↔ бонус висоти · `round-currency` · `in-round-upgrades` · `projectile-shot` + `shoot-cooldown` · `explode-area` ↔ Mortar · `status-effects` ↔ отрута/кровотеча/горіння · `hp-damage` · `speed-per-type` · `unit-xp-skills` ↔ XP веж · `coverage-area` ↔ Tesla/Encampment · `run-relics` ↔ картки забігу · `spawner-entity` ↔ монстр-породжувач · `save-progress` ↔ мета-XP.
- **Нема** → пропозиції карток:
  - `+path-grows-per-wave` «Шлях росте щохвилі» · levels/generation · 🥈 · слоти {every, tile_set}.
  - `+path-branching` «Розвилки множать входи» · levels/generation · 🥉.
  - `+tile-expansion-choice` «Гравець обирає, де прибудувати плитку» · interface/input · 📎.
  - `+upgrade-card-draw` «Апгрейди випадковими картками» · game-logic/economy · 📎 · слот {choices}.
  - `+mana-resource` «Мана для веж і будівель» · game-logic/economy · 🌱.
  - `+shield-armor-layers` «Щит → броня → HP» · entities/combat · 📎.
  - `+targeting-priorities` «Пріоритети вибору цілі» · entities/combat · 📎.
  - `+adjacency-income` «Дохід за сусідство» · game-logic/economy · 🌱.
  - `+building-on-node` «Будівля лише на спецвузлі» · entities/legality · 🌱.
  - `+meta-xp-unlocks` «XP між забігами відкриває пул» · game-logic/progression · 📎.
  - `+card-pool-reset` «Скинути пул відкриттів» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+trigger:expand` — гравець розширив поле/шлях (нагороди «за розширення»).
- `+effect:extend_path` — прибудувати плитку шляху до кінця гілки.
- `+effect:draw_cards` — взяти картки на вибір (підтвердження з родини; `draw` у словнику — нічия).
- `+effect:upgrade`, `+role:tower`, `+ui:range-circle` — підтвердження з родини.
- `+role:building` — споруда без атаки з економічним/пасивним ефектом (Siphon, University, House).
- `+ui:expand-arrows` — стрілки на кінцях гілок для вибору розширення.
- `+ui:mana-bar` — запас і приріст мани.
- `+window:choice-window` — вибір однієї з випадкових карток (підтвердження з родини).
- `+window:unlock-tree` — постійні відкриття між забігами.
- `+feature:targeting-priorities` — налаштування пріоритетів цілі вежі.

## Джерела
- ⭐ [Steam: Rogue Tower](https://store.steampowered.com/app/1843760/Rogue_Tower/) — шлях, що постійно росте; вибір напрямку щорівня; «twist turn and split»; бонус шкоди за висоту; 400+ карток; монстри лікують, бігають, атакують, спавнять, аури; мета-XP і постійні бонуси; 28.01.2022, Die of Death Games.
- [nodal.gg](https://nodal.gg/game/rogue-tower-1843760) — коротке резюме і теги.
- [steamah: basics](https://steamah.com/rogue-tower-basics-for-beginners/) — висота (+дальність і шкода), Ballista/Mortar/Tesla, пріоритети цілей і XP веж, University біля святилища, Mana Bank (125g) проти Siphon (100g), Mine, Haunted House, DoT, скидання XP.
- [gameplay.tips](https://gameplay.tips/guides/rogue-tower-tips-for-winning-the-level.html) — входи і різниця довжин гілок (+3), будинки → (хвиля × вежі) монет при розширенні, Banditry, щити з 16-ї хвилі, University за жилами, Encampment.
- YouTube: пошук «rogue tower gameplay».

## Непевне
- (?) Розмір плитки шляху в клітинах і набір форм плиток; ймовірність розвилки.
- (?) Як працюють «жили» (veins) і святилища: University — «біля святилища» (steamah) чи «на жилі» (gameplay.tips).
- (?) Чи є перемога (фінальний бос) чи забіг нескінченний; кількість рівнів.
- (?) Повний список веж (Ballista, Mortar, Tesla, Poison, Obelisk, Encampment… — частина з гайдів, решта не перевірена).
- (?) Чи можна ставити вежі на дорогу і чи вороги колись обирають гілку (кожен портал — своя гілка).
