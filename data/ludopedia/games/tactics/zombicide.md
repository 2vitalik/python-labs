---
title: Zombicide
slug: zombicide
aka: [Зомбіцид, "Zombicide 2nd Edition", "Zombicide: Black Plague", "Zombicide: Invader", "Marvel Zombies"]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: graph
  time: turn
  opponent: coop
  info: partial
  random: runtime
  goal: state
year: 2012
platforms: [board, PC (Zombicide digital адаптації), mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zombicide", best: true, note: "огляд: 1–6 гравців, тайли, колода зомбі, фази ходу, перемога/поразка, сетинги"}
  - {kind: other, url: "https://www.ultraboardgames.com/zombicide/game-rules.php", note: "правила: зони, лінія видимості, 3/4 дії, шум, рівні небезпеки 7/19/43 XP, типи зомбі"}
  - {kind: other, url: "https://www.ultraboardgames.com/zombicide/players-phase.php", note: "дії вцілілих: рух із ціною виходу, пошук, двері, обмін, машини, шум"}
  - {kind: other, url: "https://www.ultraboardgames.com/zombicide/zombies-phase.php", note: "фаза зомбі: атака/рух, розщеплення, раннери, спавн за рівнем небезпеки, extra activation, люки"}
  - {kind: other, url: "https://www.ultraboardgames.com/zombicide/combat.php", note: "бій: дальність min–max, кубики/точність/шкода, пріоритет цілей, friendly fire, коктейль Молотова"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=zombicide+how+to+play", note: "пошук; правила й геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, spawn-points, spawn-schedule, weighted-spawn, reinforcements, speed-per-type, chase-bfs, key-and-door, item-pickup, inventory-items, inventory-limit, unit-xp-skills, explode-area, player-death, mode-select, character-select, sequential-levels, +zone-graph-board, +modular-board, +action-points, +noise-attraction, +danger-level-spawn, +highest-level-scaling, +spawn-card-deck, +extra-activation, +group-split, +target-priority, +friendly-fire, +exit-cost-per-enemy, +search-action, +dice-hit-threshold, +damage-threshold-armor, +dual-wield, +craft-combine, +vehicle-drive, +room-reveal, +coop-shared-win, +mission-objectives]
proposes: ["+trigger:noise", "+cond:noisiest", "+cond:danger_level", "+cond:damage_at_least", "+effect:make_noise", "+effect:extra_activation", "+effect:split_group", "+effect:draw_card", "+role:survivor", "+role:spawn_zone", "+ui:danger-track", "+ui:noise-token", "+ui:action-pips", "+feature:setting-crossover", "+axis:field=zones", "+card:noise-attraction", "+card:danger-level-spawn"]
author: opus
date: 2026-11-09
---

# Zombicide — кооп проти колоди зомбі: шум кличе орду, а сила орди росте з твоїм найсильнішим героєм

## Суть
1–6 гравців разом керують вцілілими в місті, повному зомбі, і виконують цілі місії (взяти предмети, дійти до виходу). Зомбі не мають «гравця»: вони діють за жорстким алгоритмом — бʼють, якщо поруч жертва, інакше йдуть до видимого вцілілого, інакше до **найгучнішої** зони. Нові зомбі приходять з колоди карт, рядок якої обирається за **рівнем небезпеки** найдосвідченішого вцілілого — що сильнішим ти стаєш, то сильніша навала. Поле поділене не на клітини, а на **зони**.

## Поле і час
- Поле — модульне: великі квадратні тайли складаються за мапою місії; на них намальовані вулиці, будинки, двері, цілі.
- **Зона** — кімната всередині будівлі або відрізок вулиці між пішохідними переходами й стінами; зона може лежати на кількох тайлах. Позиція фігурки всередині зони не важить → поле фактично граф зон (`field: graph`).
- Рух — у сусідню зону через спільне ребро, без діагоналей; з вулиці в будинок — лише через двері; всередині будинку — через проходи.
- **Лінія видимості**: на вулиці — пряма паралельно краям поля крізь будь-яку кількість зон до стіни/краю; у будинку — лише в зону зі спільним проходом, на одну зону вглиб; з вулиці в будинок — будь-скільки вуличних зон по прямій і одна зона будинку.
- Хід (раунд): фаза вцілілих (кожен по черзі витрачає дії) → фаза зомбі (атаки, рух, спавн) → кінцева фаза (зняти шум, передати першого гравця).
- Інформація: поле відкрите, поведінка зомбі детермінована; приховано — колоди зомбі й спорядження.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вцілілий (Survivor) | piece (`+role:survivor`) | 3 дії (4 з Yellow), 2 рани = смерть, XP і рівень небезпеки, 5 карт спорядження (2 в руках) | дії: рух, пошук, двері, бій, обмін, шум, ціль; особлива навичка росте з досвідом |
| Walker | enemy | 1 дія, гине від шкоди ≥1 | атакує або йде на 1 зону |
| Runner | enemy | **2 дії**, шкода ≥1 | друга дія: атака, якщо вцілілий у зоні, інакше рух |
| Fatty | enemy | 1 дія, потрібна шкода **≥2** | спавниться з двома Walker-супровідниками |
| Abomination | boss | 1 дія, потрібна шкода **≥3** або Молотов | одна на полі; друга витягнута → Fatty + 2 Walker; не розщеплюється |
| Зона спавну | spawner (`+role:spawn_zone`) | порядок обходу | щокінця фази зомбі — 1 карта зомбі |
| Люк (manhole) | spawner | — | спавн лише за карткою «Manhole» і лише на тайлі з вцілілим |
| Двері | gate | зачинені / відчинені | відчинити — дія зі зброєю «Open a door»; перші двері будинку → спавн у кожній кімнаті |
| Будинок (кімнати) | zone | закритий / відкритий | при першому відкритті — 1 карта зомбі на кожну зону будинку |
| Вулична зона | zone | — | довга лінія видимості, вільний рух |
| Жетон шуму | mark | 1 на дію | лишається до кінця фази зомбі; кожен вцілілий = 1 шум |
| Ціль (Objective) | pickup | XP за взяття | умова місії |
| Карта спорядження | pickup | зброя: дальність min–max, кубики, точність, шкода, шумна/тиха, dual | з пошуку; у руці — для атаки/дверей |
| Коктейль Молотова | pickup | — | крафт: пляшка + бензин; знищує все в цільовій зоні |
| Машина | platform | місця, пошук | кермо: 1–2 вуличні зони за дію, давить усіх у зонах шляху |
| Карта зомбі | supply | 4 рядки за кольором небезпеки | хто й скільки спавниться; спецкарти Extra Activation / Manhole |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(survivor)` → ТО `counter(actions, =3)`; ЯКЩО `custom: «рівень небезпеки ≥ Yellow»` → ТО +1 дія; навички можуть давати безкоштовні дії.
- КОЛИ `input(move, zone)` → ЯКЩО `custom: «зона сусідня через ребро / прохід / відчинені двері»` → ТО `move(survivor, zone)`; ЯКЩО `count(zombies_in_start_zone, >, 0)` → ТО `custom: «+1 дія за кожного зомбі у зоні виходу»`.
- КОЛИ `enter(survivor, zone)` → ЯКЩО `occupied(zone, zombie)` → ТО `end_turn` для руху: `custom: «рух закінчується»`.
- КОЛИ `input(search)` → ЯКЩО `custom: «зона в будинку або машина»` and `not occupied(zone, zombie)` and `first_time` за хід → ТО `custom: «взяти верхню карту спорядження: лишити або скинути»`.
- КОЛИ `input(open_door)` → ЯКЩО `has(survivor, door_opener)` → ТО `set_state(door, open)`; ЯКЩО `custom: «зброя шумна»` → ТО `spawn_at(noise_token, zone)`.
- КОЛИ `after(open_door)` → ЯКЩО `first_time` для будинку → ТО для кожної зони будинку `custom: «витягнути карту зомбі і поставити»`.
- КОЛИ `input(ranged, zone)` → ЯКЩО `line_of_sight(survivor, zone)` and `custom: «відстань у межах min–max зброї»` → ТО `roll(dice)`; кожен кубик ≥ точності = влучання.
- КОЛИ `custom: «влучання дистанційної атаки розподіляються»` → ТО `custom: «за пріоритетом: інші вцілілі → Walker → Fatty/Abomination → Runner; наступна група лише після знищення попередньої»` — friendly fire.
- КОЛИ `input(melee)` → ЯКЩО `custom: «зброя з дальністю 0»` → ТО `roll(dice)`; влучання гравець розподіляє серед зомбі своєї зони сам.
- КОЛИ `custom: «влучання по зомбі»` → ЯКЩО `custom: «шкода зброї ≥ поріг типу (1 / 2 / 3)»` → ТО `disappear_b`, `counter(XP, +1)` (Abomination +5); інакше `block` — зайва шкода згорає.
- КОЛИ `input(ranged, molotov)` → ТО `explode(zone)`: знищено все в зоні, включно з вцілілими й Abomination; карта скидається.
- КОЛИ `input(attack)` → ЯКЩО `custom: «дві однакові dual-зброї в руках»` → ТО `custom: «обидві стріляють однією дією в одну зону»`.
- КОЛИ `input(attack | open_door)` → ЯКЩО `custom: «шумна зброя»` → ТО `spawn_at(noise_token, zone)` — 1 жетон на дію незалежно від влучань.
- КОЛИ `input(make_noise)` → ТО `spawn_at(noise_token, zone)` — приманка.
- КОЛИ `input(trade, ally)` → ЯКЩО `occupied(zone, ally)` → ТО `swap` карт спорядження (будь-яка кількість); КОЛИ `counter(cards, >, 5)` → ТО `custom: «скинути до 5»`.
- КОЛИ `counter(XP, ≥, 7)` → ТО `set_state(survivor, yellow)` (+1 дія); `≥ 19` → Orange (навичка 1 з 2); `≥ 43` → Red (навичка 1 з 3).
- КОЛИ `phase_start(zombies)` → ТО кожен зомбі: ЯКЩО `occupied(zone, survivor)` → ТО `damage(1)` (рана, без кубиків; гравці обирають, хто отримує рану; зомбі можуть забрати спорядження); інакше ЯКЩО `custom: «бачить вцілілого»` → ТО `move(zombie, toward_visible)`; інакше `move(zombie, toward_noisiest)`. Спочатку всі атаки, потім усі рухи.
- КОЛИ `custom: «видимі вцілілі в кількох зонах»` → ТО `custom: «йти до найгучнішої групи (вцілілий = 1 шум)»`.
- КОЛИ `custom: «два однаково короткі шляхи або однаково гучні цілі»` → ТО `split(group)` порівну, `spawn(zombie)` для вирівнювання складу; ЯКЩО `custom: «фігурок бракує»` → ТО `custom: «extra activation для цього типу»`.
- КОЛИ `custom: «Runner після першого раунду дій»` → ТО друга дія: атака, якщо є жертва, інакше рух.
- КОЛИ `custom: «спавн-крок»` → ТО для кожної зони спавну по годинниковій стрілці `custom: «карта зомбі, рядок = колір найвищого рівня небезпеки серед живих вцілілих»`, `spawn_at(zombies, spawn_zone)`.
- КОЛИ `custom: «карта Extra Activation»` → ЯКЩО `custom: «рівень небезпеки ≠ Blue»` → ТО `custom: «усі зомбі вказаного типу діють ще раз»`.
- КОЛИ `custom: «карта Manhole»` → ТО `spawn_at(zombies, manhole)` лише на тайлах з вцілілими.
- КОЛИ `custom: «фігурок типу не вистачає для спавну»` → ТО поставити наявних, `custom: «усі зомбі цього типу отримують extra activation»`.
- КОЛИ `counter(wounds, ≥, 2)` → ТО `disappear_a` — вцілілий вибуває.
- КОЛИ `input(drive)` → ЯКЩО `custom: «місія дозволяє»` → ТО `custom: «машина 1–2 вуличні зони за дію, атакує всіх у зонах шляху»`.
- КОЛИ `phase_start(end)` → ТО `clear(noise_tokens)`, `custom: «перший гравець передається»`.
- КОЛИ `all_constraints_met` (усі цілі місії) → ТО `win` — разом, навіть якщо частина вцілілих загинула. КОЛИ `all_gone(survivors)` → ТО `lose`.
- Перемога: виконати всі цілі місії · Поразка: загинули всі вцілілі (чи умова місії) · Рахунок — немає.

## Керування і ввід
- Настолка: гравці по черзі витрачають дії свого вцілілого (1–4 вцілілих на гравця: соло — до 4, вшістьох — по 1); зомбі «рухає» будь-хто за алгоритмом.
- Цифрова версія: клік по зоні — рух; по зброї в руці → по зоні — атака; кнопки пошуку, дверей, обміну, шуму; drag карт між слотами рюкзака й руками (`inventory-bar`).
- Вибір у спірних випадках (кому рана, куди піде Abomination при рівних шляхах) робить команда гравців.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `level-select` місій (мапа тайлів, цілі, складність) → `character-select` вцілілих (портрети, навички за рівнями) → `game-screen`.
- `game-screen`: поле з зонами; `+ui:noise-token` на зонах; картка вцілілого — `+ui:danger-track` (Blue/Yellow/Orange/Red, XP), `+ui:action-pips`, 2 руки + 3 слоти рюкзака, рани; колода зомбі й спорядження; `objective-text`.
- `inventory-window` — обмін і реорганізація між двома вцілілими в зоні.
- `choose`-вікно навички при переході на Orange/Red.
- `end-screen` місії: виконано / усі загинули.
- `help-window` / `rules-page` — довідка щодо пріоритету цілей і поведінки зомбі.

## Фічі поза полем
- `mode-coop`: усі разом проти «гри»; кількість вцілілих фіксована, гравці ділять їх.
- Сценарії (місії) з різними мапами тайлів, цілями й зонами спавну — від початківської до експертної (~20 хв … 3 год).
- Сетинги з різною механікою (Modern, Fantasy/Black Plague, Sci-Fi/Invader, Western, Marvel Zombies, DCeased, 2nd Edition) — змішувати можна лише в межах сетингу.
- Прогресія всередині партії: XP → рівень небезпеки → навички; між партіями — немає (базово) (?).

## Варіації й родичі
- У корпусі: [descent-journeys-in-the-dark](descent-journeys-in-the-dark.md) (модульні тайли, але є гравець-майстер), [heroquest-space-hulk](heroquest-space-hulk.md) (блипи й лінія видимості в коридорах), [gloomhaven](gloomhaven.md) (кооп, AI ворогів за картами), [memoir-44](memoir-44.md) (кубики з символами).
- Осі варіацій:
  - **поле**: клітини (HeroQuest) / гекси (Gloomhaven) / **зони-графи** (Zombicide, Memoir — секції);
  - **AI ворогів**: майстер-гравець (Descent) / картки ворога (Gloomhaven) / детермінований алгоритм «атакуй → до видимого → до шуму» (Zombicide);
  - **масштаб загрози**: фіксований / за раундами / **за найсильнішим героєм** (Zombicide) / за середнім рівнем партії (Gloomhaven);
  - **friendly fire**: нема / є за пріоритетом цілей (Zombicide) / за кубиком.

## Цікавинки для курсу
- Граф зон замість сітки + пряма лінія видимості на вулицях і «одна кімната вглиб» у будинках — 🥉.
- Алгоритм зомбі (атака → видимий → найгучніша зона, найкоротший шлях, розщеплення групи при рівності) — 🥉; з вирівнюванням складу групи — 🥈.
- Шум як «запах»: жетони на зонах, вцілілий = 1 шум, зняття в кінці раунду — 📎.
- Danger level за найсильнішим героєм обирає рядок карти спавну — 📎 (динамічна складність одним рядком таблиці).
- Пріоритет цілей при стрільбі з friendly fire — 🌱.
- Поріг шкоди проти броні (1/2/3), зайве згорає — 🌱.
- Ціна виходу з зони = +1 дія за зомбі — 🌱.

## Мапа на каталог
- Є: `hp-damage` ↔ 2 рани · `melee-vs-ranged` ↔ дальність 0 vs min–max · `line-of-sight-attack` · `spawn-points` ↔ зони спавну · `spawn-schedule` ↔ щораунду · `weighted-spawn` ↔ колода · `reinforcements` · `speed-per-type` ↔ Runner 2 дії · `chase-bfs` ↔ найкоротший шлях · `key-and-door` · `item-pickup` + `inventory-items` + `inventory-limit` (5 карт, 2 руки) · `unit-xp-skills` · `explode-area` ↔ Молотов · `player-death`.
- **Нема** → пропозиції карток:
  - `+zone-graph-board` «Поле з зон замість клітин» · board/topology · 🥉.
  - `+noise-attraction` «Шум притягує ворогів» · entities/move · 📎 · слоти {decay: end_of_round}.
  - `+danger-level-spawn` «Спавн за рівнем найсильнішого героя» · game-logic/difficulty · 📎 · слоти {levels: [7, 19, 43]}.
  - `+spawn-card-deck` «Колода спавну з рядками складності» · entities/spawn · 📎.
  - `+extra-activation` «Додаткова активація типу ворогів» · entities/spawn · 🌱.
  - `+group-split` «Група ворогів ділиться на рівних шляхах» · entities/move · 🥉.
  - `+target-priority` «Фіксований пріоритет цілей + friendly fire» · entities/combat · 🌱.
  - `+exit-cost-per-enemy` «Вихід із зони коштує дій за ворогів» · entities/legality · 🌱.
  - `+dice-hit-threshold` «Кубик ≥ точність = влучання» · entities/combat · 🌱.
  - `+damage-threshold-armor` «Поріг шкоди для типу ворога» · entities/combat · 🌱.
  - `+dual-wield`, `+craft-combine`, `+vehicle-drive`, `+room-reveal` (з HeroQuest), `+search-action` (з HeroQuest), `+action-points`, `+modular-board` (з Descent), `+coop-shared-win`, `+mission-objectives`.

## Пропозиції до словників
- `+trigger:noise(zone)` — у зоні зʼявився шум (для реакцій ворогів).
- `+cond:noisiest(zone)` — зона з найбільшим шумом; `+cond:danger_level(op, color)` — рівень небезпеки; `+cond:damage_at_least(n)` — шкода зброї ≥ порогу цілі.
- `+effect:make_noise(zone)` — покласти жетон шуму; `+effect:extra_activation(kind)` — тип ворогів діє ще раз; `+effect:split_group(group)` — поділ групи порівну; `+effect:draw_card` — витягнути карту (спавн, спорядження).
- `+role:survivor` — фігура гравця з рюкзаком і рівнем небезпеки; `+role:spawn_zone` — зона, куди приходять вороги за картою.
- `+ui:danger-track` — шкала XP із кольорами; `+ui:noise-token` — жетон на зоні; `+ui:action-pips` — лишок дій.
- вікна вибору місії й вцілілих — наявні `level-select` і `character-select`.
- `+feature:setting-crossover` — змішування наборів у межах сетингу (без змішування між сетингами).
- `+axis:field=zones` — граф зон як окреме значення осі.
- `+card:noise-attraction`, `+card:danger-level-spawn`.

## Джерела
- ⭐ [Wikipedia: Zombicide](https://en.wikipedia.org/wiki/Zombicide) — гравці 1–6, квадратні тайли, колода зомбі, три фази, перемога/поразка, сетинги.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/zombicide/game-rules.php) — зони, лінія видимості (вулиця/будинок), 3/4 дії, шум, рівні Blue/Yellow 7/Orange 19/Red 43, XP, типи зомбі.
- [UltraBoardGames: фаза гравців](https://www.ultraboardgames.com/zombicide/players-phase.php) — рух із ціною виходу, пошук, двері й спавн у будинку, обмін, машини, шум.
- [UltraBoardGames: фаза зомбі](https://www.ultraboardgames.com/zombicide/zombies-phase.php) — атаки й рухи, розщеплення, Runner, спавн за рівнем, Extra Activation, Manhole, брак фігурок.
- [UltraBoardGames: бій](https://www.ultraboardgames.com/zombicide/combat.php) — дальність min–max, кубики/точність/шкода, пріоритет цілей, dual, Молотов.
- YouTube: пошук «zombicide how to play».

## Непевне
- (?) Офіційні цифрові адаптації (Zombicide: Tactics & Shotguns, Zombicide 2nd Ed. app) — платформи й відмінності не перевірені.
- (?) Пріоритет цілей і правила наведені для оригіналу Modern 2012; у 2nd Edition і Black Plague частина змінена (напр., пріоритет Brute/Runner).
- (?) Прогресія між місіями (кампанії Black Plague / Ultimate Survivor) — не перевірено.
