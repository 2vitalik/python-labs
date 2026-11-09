---
title: PixelJunk Monsters
slug: pixeljunk-monsters
aka: [PJM, PixelJunk Monsters Deluxe, PixelJunk Monsters Ultimate]
family: tower-lanes
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2007
platforms: [PS3, PSP, PS Vita, PC, Mac, Linux, Wii U]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/PixelJunk_Monsters", best: true, note: "хатина з дитинчатами, вежі вздовж шляху, монети й самоцвіти, персонаж замість курсора, кооп, Encore"}
  - {kind: steam, url: "https://store.steampowered.com/app/243780/PixelJunk_Monsters_Ultimate/", note: "Ultimate: 8 типів веж, вороги наземні й літаючі, 3 острови, Tum-Tum з генерацією, кооп локальний і онлайн"}
  - {kind: other, url: "https://www.thesixthaxis.com/?p=1153", note: "поради: що робить кожна вежа, шляхи апгрейдів за самоцвіти"}
  - {kind: other, url: "https://gog.com/game/pixeljunk_monsters_hd", note: "GOG: монети зникають, якщо не встиг; веселка за ідеальне проходження"}
  - {kind: steam, url: "https://store.steampowered.com/app/749800/PixelJunk_Monsters_2/", note: "сиквел 2018, 3D"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pixeljunk+monsters+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [tower-placement, tower-range, move-by-input, enemy-waves, spawn-points, enemy-reached-base, round-currency, drop-on-death, item-pickup, timed-despawn, shop-buyback, in-round-upgrades, unit-xp-skills, projectile-shot, shoot-cooldown, explode-area, status-effects, hp-damage, speed-per-type, melee-vs-ranged, level-select, level-unlock, difficulty-levels, leaderboard, achievements-window, online-multiplayer, +build-where-standing, +fixed-build-slots, +stand-to-upgrade, +slot-regrow, +air-ground-split, +per-type-limit, +line-attack, +perfect-clear-rating, +research-per-level]
proposes: ["+trigger:stay", "+effect:upgrade", "+effect:sell", "+role:base", "+ui:ring-menu", "+ui:lives-icons", "+feature:research-per-level", "+card:build-where-standing", "+card:stand-to-upgrade", "+axis:control"]
author: opus
date: 2026-11-09
---

# PixelJunk Monsters — TD без курсора: Тікімен бігає полем, збирає монети й перетворює дерева на вежі, біля яких стоїть

## Суть
Класичний TD (вежі вздовж шляху, вороги йдуть до хатини), але **курсора немає**: гравець веде аватара Тікімена, і будувати можна лише там, де він стоїть — на місці **дерева**. Монети й самоцвіти падають із ворогів і **зникають**, якщо не добігти; тож аватар розривається між збиранням, будуванням і «танцем» на вежі, що повільно її покращує. Кожен ворог, що дійшов до хатини, з'їдає одне дитинча; усі зʼїдені — поразка.

## Поле і час
- 2D-мапа зверху з вільним рухом аватара; шлях ворогів фіксований рельєфом мапи (вежі не перекривають його — без мейзингу).
- Будівельні місця — **дерева** в фіксованих точках мапи: клітинний шар гри = набір слотів-дерев.
- Real-time хвилями від одного чи кількох входів до хатини; темп аватара повільний — відстань до монети чи дерева має значення.
- Вороги наземні й літаючі; літаючі б'ють лише вежі з ППО (Anti-Air, Laser).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тікімен | player | швидкість (повільна) | ходить полем, підбирає монети/самоцвіти, будує на дереві під собою, «танцює» на вежі |
| Хатина з дитинчатами | static (`+role:base`) | N дитинчат | ворог, що дійшов, забирає одне |
| Дерево | static | слот | місце будування; продаж вежі лишає пень, який за кілька секунд знову стає деревом |
| Arrow | tower | далекобійна, швидка | добре проти швидких (павуки); слабка проти босів і щитів |
| Cannon | tower | сплеш, мала дальність | проти скупчених повільних наземних |
| Anti-Air | tower | лише повітря | збиває літаючих |
| Ice | tower | площа | сповільнює ворогів у радіусі; з апгрейдами — більша зона |
| Fire | tower | струмінь | бʼє лінію в одному напрямку; повільна перезарядка |
| Tesla | tower | заряд | накопичує заряд, потім бʼє кількох |
| Laser | tower | лише повітря, промінь | проходить крізь лінію літаючих |
| Mortar | tower | наземна, сплеш, велика дальність | «далекий Cannon» |
| Hive | tower | одна на мапу | породжує міні-істот, що кружляють довкола Тікімена (?) |
| Наземний монстр | enemy | HP, швидкість | іде шляхом до хатини |
| Літаючий монстр | enemy | — | ігнорує наземні вежі |
| Бос / щитоносець | enemy / boss | великий HP, щит | стійкий до Arrow |
| Монета | pickup | живе обмежений час | падає з ворога; платіж за вежі |
| Самоцвіт | pickup | рідкісний | апгрейд вежі негайно або дослідження нового типу вежі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `died(monster)` → ТО `spawn_at(coin, тіло)`; `rng(p)` → `spawn_at(gem, тіло)`.
- КОЛИ `custom: «монета/самоцвіт лежить довше за t»` → ТО `disappear`.
- КОЛИ `contact(player, coin)` → ТО `pickup`, `currency(+n)`; КОЛИ `contact(player, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `input(action)` → ЯКЩО `occupied(cell_under_player, tree)` → ТО `window(+ui:ring-menu)` — вибір доступних веж із цінами.
- КОЛИ `input(build, tower)` → ЯКЩО `occupied(cell_under_player, tree)` and `counter(coins, >=, cost)` and `custom: «тип вежі досліджено в цьому рівні»` → ТО `currency(-cost)`, `transform(tree, tower)`; інакше `block`.
- КОЛИ `input(build, hive)` → ЯКЩО `count(hive, ==, 0)` → ТО як вище; інакше `block`.
- КОЛИ `in_range(tower, monster, n)` → ЯКЩО `custom: «тип цілі дозволений (земля / повітря)»` → ТО `spawn(projectile)` або промінь/струмінь → `damage(n)`.
- КОЛИ `contact(cannon_shell, ground)` → ТО `explode(area)` → `damage(n)` усім у радіусі.
- КОЛИ `in_range(ice, monster, n)` → ТО `speed(monster, ×k)` (`set_state(monster, slowed)`).
- КОЛИ `died(monster)` у радіусі вежі → ТО `counter(tower_xp, +n)`; КОЛИ `counter(tower_xp, >=, threshold)` → ТО `custom: «upgrade: рівень вежі +1»`.
- КОЛИ `custom: «stay(player, tower, n тіків)»` (танець на вежі) → ТО `counter(tower_xp, +n)` — повільний апгрейд.
- КОЛИ `input(upgrade, tower)` → ЯКЩО `counter(gems, >=, cost)` (1–3 за рівень) → ТО `custom: «upgrade негайно: наступний крок фіксованого шляху (дальність / сила / швидкість / сплеш)»`.
- КОЛИ `input(research, tower_type)` у хатині → ЯКЩО `counter(gems, >=, cost)` → ТО `unlock(tower_type)` — лише до кінця цього рівня.
- КОЛИ `input(sell)` → ЯКЩО `occupied(cell_under_player, tower)` → ТО `custom: «sell: рефанд за іконкою»`, `transform(tower, stump)`; КОЛИ `timer(кілька секунд)` → ТО `transform(stump, tree)`.
- КОЛИ `reach(monster, hut)` → ТО `disappear(monster)`, `lives(-1)` (одне дитинча).
- КОЛИ `counter(babies, <=, 0)` → ТО `lose`.
- КОЛИ `custom: «остання хвиля минула»` → ТО `win`; ЯКЩО `custom: «жодне дитинча не втрачене»` → ТО `custom: «веселка над рівнем»`.
- Перемога: пережити всі хвилі · Поразка: усі дитинчата зʼїдені · Рахунок: веселка за ідеальне проходження; очки для лідерборда (?).

## Керування і ввід
- Стік/хрестовина — рух Тікімена (`+axis:control` = direct-avatar для будування); кнопка дії біля дерева/вежі відкриває кільцеве меню; вибір у кільці — стіком.
- Танець — утримання кнопки/стояння на вежі (?).
- Кооп: другий Тікімен на тому самому екрані з власним вводом, гаманець спільний (?).
- PC: геймпад або миша (рецензенти радять геймпад).

## Вікна, меню, HUD
- `main-menu`: одиночна гра · кооп (локальний / онлайн) · лідерборди · досягнення.
- `map-window` — острів із вузлами-рівнями; веселки відкривають нові ділянки (за рецензією GOG).
- `difficulty-select` — 3 рівні складності на рівень.
- `game-screen`: мапа, `coins`, лічильник самоцвітів, `+ui:lives-icons` (дитинчата біля хатини), `wave-counter`, `next-wave-preview` (?), `+ui:ring-menu` над деревом/вежею, `threat-range` обраної вежі (?).
- `pause-menu`; `end-screen` — пройдено / веселка / поразка.
- Переходи: main-menu → map-window → difficulty → game-screen ↔ pause → end-screen → map-window.

## Фічі поза полем
- `world-map` + `level-unlock`: 21 рівень (36 з Encore) на 3 рівнях складності; 3 спецрівні відкривають нові вміння Тікімена.
- `stars-rating` у вигляді веселки (ідеальне проходження).
- `+feature:research-per-level` — досліджені вежі скидаються з кожним новим заходом у рівень.
- `mode-coop` (локальний і онлайн), `leaderboard-online`, `achievements`.
- Tum-Tum Island (Ultimate) — процедурні рівні, `mode-endless`-подібна реіграбельність.
- Trophy Challenges (патч) — окремі виклики (?).

## Варіації й родичі
- Encore (+15 рівнів, Ice доступна з початку кожного рівня, Tesla дешевша), Deluxe (PSP), Ultimate HD (2013), Monsters 2 (2018, 3D), Monsters 3.
- Родичі: [orcs-must-die](orcs-must-die.md) і [locks-quest](locks-quest.md) (герой на полі разом із вежами), [fieldrunners](fieldrunners.md) і [desktop-tower-defense](desktop-tower-defense.md) (курсорний TD), [plants-vs-zombies](plants-vs-zombies.md) (збирати валюту з поля, поки не зникла), Dungeon Defenders.
- **Осі варіацій**: хто будує — курсор / аватар, що має стояти на місці · місце — будь-яка клітинка / фіксовані слоти / слоти, що відновлюються · апгрейд — гроші / досвід від убивств / час присутності гравця · валюта — автоматично / треба підібрати до зникнення.

## Цікавинки для курсу
- Будування «там, де стоїш»: дія аватара читає клітинку під ним (дерево/вежа/пусто) і відкриває відповідне меню — 📎.
- Три шляхи апгрейду однієї вежі: XP за вбивства в радіусі, таймер присутності гравця, миттєво за самоцвіти — 🥉.
- Валюта, що зникає: дроп із таймером життя і повільний аватар — пріоритети руху — 🌱.
- Слот, що відновлюється: продаж → пень → через t знову дерево — 🌱.
- Розподіл цілей земля/повітря між типами веж — 📎.
- Дослідження, що діє лише в межах одного рівня (скидається з рестартом) — 🌱.
- Fire-струмінь і Laser-промінь: шкода по лінії в одному напрямку — 🥉.

## Мапа на каталог
- Є: `tower-placement`, `tower-range` · `move-by-input` ↔ Тікімен · `enemy-waves`, `spawn-points`, `enemy-reached-base` ↔ хатина · `round-currency`, `drop-on-death`, `item-pickup`, `timed-despawn` ↔ монети зникають · `shop-buyback` ↔ продаж на пень · `in-round-upgrades` ↔ самоцвіти · `unit-xp-skills` ↔ вежа росте від убивств · `projectile-shot`, `shoot-cooldown`, `explode-area` (Cannon, Mortar), `status-effects` (Ice) · `hp-damage`, `speed-per-type`, `melee-vs-ranged` · `level-select`, `level-unlock`, `difficulty-levels`, `leaderboard`, `achievements-window`, `online-multiplayer`.
- **Нема** → пропозиції карток:
  - `+build-where-standing` «Будувати лише в клітинці під аватаром» · interface/input · 📎.
  - `+fixed-build-slots` «Будівельні слоти замість вільних клітинок» · entities/legality · 🌱.
  - `+stand-to-upgrade` «Апгрейд за час присутності гравця біля споруди» · entities/state · 📎.
  - `+slot-regrow` «Слот відновлюється через t після продажу» · entities/state · 🌱.
  - `+air-ground-split` «Вежі б'ють лише землю / лише повітря / обидва» · entities/combat · 🌱.
  - `+line-attack` «Атака по лінії в напрямку (струмінь, промінь крізь ворогів)» · entities/combat · 🥉 (`beam-tracing` — про дзеркала, не те).
  - `+per-type-limit` «Не більше N споруд типу на мапі» · entities/legality · 🌱.
  - `+perfect-clear-rating` «Мітка ідеального проходження (без втрат)» · game-logic/score · 🌱.
  - `+research-per-level` «Розблокування, що діє лише до кінця рівня» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:stay` — сутність перебуває на клітинці/біля обʼєкта N тіків поспіль (танець на вежі).
- `+effect:upgrade` — рівень споруди +1 за шляхом апгрейдів (TD-повтор, Fieldrunners).
- `+effect:sell` — продаж з рефандом (TD-повтор).
- `+role:base` — хатина: ціль ворогів з пулом життів.
- `+ui:ring-menu` — кільцеве меню дій навколо аватара/обʼєкта (вибір стіком).
- `+ui:lives-icons` — життя як фігурки на полі біля бази (дитинчата), а не лічильник у HUD.
- `+feature:research-per-level` — дослідження скидаються між заходами в рівень.
- `+card:build-where-standing`, `+card:stand-to-upgrade` — див. «Мапа на каталог».
- `+axis:control` — значення `avatar-build`: дія курсора виконується позицією аватара.

## Джерела
- ⭐ [Wikipedia: PixelJunk Monsters](https://en.wikipedia.org/wiki/PixelJunk_Monsters) — мета (хатина, дитинчата, поразка), монети й самоцвіти, персонаж замість курсора, кооп, 21/36 рівнів × 3 складності, 3 спецрівні, Encore/Deluxe/Ultimate.
- [Steam: PixelJunk Monsters Ultimate](https://store.steampowered.com/app/243780/PixelJunk_Monsters_Ultimate/) — вежі у фіксованих точках, 8 типів, земля й повітря, 3 острови / 47 мап, Tum-Tum з генерацією, кооп, лідерборди.
- [TheSixthAxis: поради](https://www.thesixthaxis.com/?p=1153) — поведінка кожної вежі (Fire-струмінь, Tesla-заряд, Laser і Anti-Air лише повітря, Hive одна), шляхи апгрейдів за самоцвіти.
- [GOG: PixelJunk Monsters HD](https://gog.com/game/pixeljunk_monsters_hd) — монети зникають, повільний рух, апгрейд стоянням біля вежі, веселка відкриває нові ділянки.
- Пошук (2 запити): дерева = будівельні місця, 3 шляхи апгрейду (бій, танець, самоцвіти 1–3), дослідження в хатині не переходять між рівнями, продаж через кільцеве меню лишає пень, що відростає.

## Непевне
- (?) Кількість дитинчат у хатині (лічильник життів) і чи великі вороги забирають більше одного.
- (?) Чи апгрейд за бій — це XP від убивств у радіусі, чи від завданої шкоди.
- (?) Hive: що саме роблять міні-істоти (за порадами — кружляють довкола Тікімена й допомагають збирати).
- (?) Що дають 3 спецрівні (нові вміння Тікімена) і як влаштовані Trophy Challenges.
- (?) Чи є прев'ю наступної хвилі та кнопка раннього виклику.
- (?) Кооп: спільний гаманець чи окремі; хто піднімає монету.
