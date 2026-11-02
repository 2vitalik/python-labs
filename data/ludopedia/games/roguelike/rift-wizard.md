---
title: Rift Wizard
slug: rift-wizard
family: roguelike
also: [tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2021
platforms: [PC (Windows, Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1271280/", best: true, note: "сторінка гри: опис дизайну («ближче до настолки, ніж до RPG»), скріншоти UI, трейлер"}
  - {kind: other, url: "https://gamepretty.com/rift-wizard-all-spells-list-upgrades-effects-and-costs/", note: "список заклинань: рівень (= ціна SP), теги, заряди, дальність, апгрейди з цінами"}
  - {kind: other, url: "https://turnbasedlovers.com/review/rift-wizard-review/", note: "огляд: рифти, заряди, зілля, Мордред"}
  - {kind: other, url: "https://vaporlens.app/app/1271280/rift_wizard.md", note: "зведення відгуків: повна мапа, превʼю наступного рівня, святилища, UI-скарги"}
  - {kind: steam, url: "https://store.steampowered.com/app/2058570/", note: "Rift Wizard 2 (2025)"}
  - {kind: fandom, url: "https://riftwizard.fandom.com/wiki/Rift_Wizard_Wiki", note: "фан-вікі (WebFetch не відкрився)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rift+wizard+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-8dir, move-by-input, hp-damage, destroy-all-enemies, dungeon-generation, sequential-levels, player-death, projectile-shot, blast-wave, chase-bfs, melee-vs-ranged, item-pickup, inventory-items, temporary-modes, impassable-cells, spawn-schedule, cell-transform, shop-catalog, shop-preview, cell-click, hover-highlight, game-screen, gui-render, keyboard-controls, +spell-charges, +sp-progression, +spell-upgrades, +tag-synergy, +damage-types-resist, +summon-minions, +line-of-sight-cast, +chasm-cells, +rift-choice-preview, +lair-spawner, +shrine-upgrade, +permadeath, +monster-manual]
proposes: ["+trigger:cast", "+trigger:realm_cleared", "+cond:line_of_sight", "+cond:has_tag", "+cond:charges", "+cond:resist", "+effect:cast", "+effect:summon", "+effect:resist", "+effect:upgrade", "+effect:refill_charges", "+role:minion", "+role:rift", "+role:shrine", "+window:spellbook-shop", "+window:realm-preview", "+window:unit-inspect", "+ui:spell-bar-charges", "+ui:resist-panel", "+ui:aoe-preview", "+feature:spell-filter-by-tag", "+feature:permadeath", "+axis:session=run", "+card:rules-as-spells"]
author: opus
date: 2026-11-02
---

# Rift Wizard — роглайк-«настолка»: уся прогресія — це заклинання, а кожен рівень видно цілком, як шахову задачу

## Суть
Безсмертний чарівник проходить 25 «реалмів» — одноекранних рівнів-арен — до суперника Мордреда. Єдина прогресія — **очки навичок (SP)**, які він збирає на рівнях і витрачає на нові заклинання, апгрейди заклинань і пасивні навички; усе каталог доступний з першого ходу. Заклинання мають **заряди** замість мани, теги (Fire, Lightning, Conjuration…) і навички, що підсилюють теги — звідси комбо-збірки (вогонь+блискавка, некромантія+вибухи). Рандому мінімум: рівень і всі вороги видні одразу, у кожного ворога видно здібності й опори — гра як серія тактичних задач.

## Поле і час
- Рівень 28×28 клітин (?) на одному екрані — камера статична, туману нема. Клітини: підлога, стіна (блокує рух і зір), прірва (блокує рух, не зір; літуни перелітають), хмари (шторм, заметіль, вогонь) поверх клітини.
- Покроково, суворо по черзі: хід гравця (рух / заклинання / предмет / чекати) → хід усіх юнітів. Окремі заклинання «канальні» (тривають кілька ходів).
- Рівень генерується з набору тем; вороги розставлені «гніздами» й лігвищами-спавнерами. Після зачистки відкриваються **рифти** — портали в наступні рівні з превʼю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник | player | HP 50 (?), SP, книга заклинань, навички | рух 8 напрямків; дія = 1 заклинання / рух / предмет |
| Заклинання | — (дані) | рівень = ціна SP (1–7), теги, заряди, дальність, радіус, шкода й тип | застосовується на клітину в межах дальності й LOS |
| Апгрейд заклинання | — (дані) | ціна SP | +шкода / +заряди / +радіус / нова властивість (каскад, сліпе чаклування) |
| Навичка (skill) | — (дані) | ціна SP, теги | пасивно підсилює заклинання з тегом або реагує на подію |
| Сфера памʼяті (memory orb) | pickup | +1 SP | лежить на рівні; береться після/під час бою |
| Зілля лікування / мани | pickup | — | HP / поповнити заряди |
| Інші предмети (сувої телепорту тощо) | pickup | — | одноразові дії |
| Ворог | enemy | HP, опори за типами шкоди, здібності з дальністю/кулдауном, теги (living, undead, demon…) | підходить і бʼє / стріляє / кастує; поведінка видна в описі |
| Лігвище (gate/lair) | spawner | HP, період | породжує ворогів кожні N ходів, доки не зруйноване |
| Бос / Мордред | boss | — | фінальний рівень |
| Вампір | enemy | — | помираючи стає кажаном; не добитий — відроджується |
| Прислужник (minion) | ally | HP, атака, тривалість (часто обмежена) | призваний заклинанням; ШІ бʼє ворогів |
| Стіна | static | руйнівна заклинаннями (землетрус) | блокує рух і LOS |
| Прірва | terrain | — | блокує рух наземних, не LOS |
| Хмара (шторм, заметіль, вогонь) | hazard | тривалість | шкода тим, хто в клітині; ланцюгові заклинання можуть «перескакувати» на неї |
| Святилище / коло (shrine) | switch | тег | додає заклинанню з тегом особливий бонус |
| Рифт | static | превʼю наступного рівня | вхід → наступний рівень (активний після зачистки) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(cast spell, target)` → ЯКЩО `charges(spell) > 0` and `in_range(target, range)` and (`line_of_sight` or upgrade «blindcasting») → ТО `cast`, `counter(charges, -1)`, `end_turn`; інакше `block`.
- КОЛИ `cast(spell)` → ТО ефект за даними: `damage(n, type)` у клітину / промінь / радіус (`blast-wave`), `summon(minion)`, `teleport(caster)`, `set_state(target, stun|freeze|poison|blind)`, `set_cell(wall → floor)`.
- КОЛИ `damage(target, n, type)` → ТО `custom: «n × (1 − resist[type]/100)»`; опір може бути від’ємним (вразливість) або 100 % (імунітет).
- КОЛИ `cast(spell)` → ЯКЩО `has_tag(spell, T)` and `has(wizard, skill[T])` → ТО бонус навички (шкода, тривалість прислужників, додатковий ефект) — **синергія тегів**.
- Приклади правил-як-заклинань: Death Bolt — вбитий живий ворог `transform(skeleton ally)`; Flame Gate — кожне вогняне заклинання `summon(fire elemental)` біля цілі, доки не скастуєш не-вогняне; Chain Lightning — промінь `custom: «перескакує на випадкового ворога в радіусі 4, доки є нові цілі»`; Earthquake — кожна клітина в радіусі 7 з p = 50 % `damage` + `set_cell(wall → floor)`; Annihilate — шкода трьох типів по одній цілі.
- КОЛИ `turn_end(player)` → ТО юніти діють за пріоритетом: здібність доступна й ціль у дальності → `cast`; інакше `move` до цілі (`chase-bfs`).
- КОЛИ `timer(every N)` (лігвище) → ТО `spawn_at(monster, near_lair)`; КОЛИ `destroyed(lair)` → спавн зупиняється.
- КОЛИ `hp_zero(vampire)` → ТО `transform(bat)`; ЯКЩО бат живе N ходів → `transform(vampire)`.
- КОЛИ `contact(wizard, memory_orb)` → ТО `counter(SP, +1)`.
- КОЛИ `input(buy spell|upgrade|skill)` → ЯКЩО `counter(SP, >=, cost)` → ТО `counter(SP, -cost)`, `give(wizard, x)`.
- КОЛИ `all_gone(enemies)` → ТО `custom: «рифти активні; лишені предмети можна зібрати»` (`+trigger:realm_cleared`).
- КОЛИ `input(enter rift)` → ТО `next_level`, `refill_charges(all spells)`; HP не відновлюється (RW1) (?).
- КОЛИ `input(drink mana potion)` → ТО `refill_charges`; лікування → `heal(wizard, n)`.
- КОЛИ `hp_zero(wizard)` → ТО `lose` (перманентно).
- Перемога: убити Мордреда на останньому рівні. Поразка: HP = 0. Рахунок: нема — сам факт перемоги й кількість пройдених рівнів (?).

## Керування і ввід
- Numpad/клавіші — рух на 8 напрямків; миша — вибір цілі заклинання, наведення — опис юніта/клітини.
- Цифрові клавіші — вибрати заклинання з панелі, потім клітина-ціль (клік або курсор з клавіатури); підсвічується зона ураження й дальність.
- Клавіші меню: книга заклинань/магазин SP, предмети, «підібрати все» після зачистки (`a` за оглядом) (?), чекати хід.
- Вибір рифта — наведення/клік по рифту → превʼю, вхід.

## Вікна, меню, HUD
- `game-screen`: поле 28×28 (піксель-арт) + ліва панель: HP, SP, `+ui:spell-bar-charges` (заклинання з поточними/макс. зарядами й гарячими клавішами), навички, предмети; права/нижня — `+window:unit-inspect`: наведений юніт — HP, опори за типами (`+ui:resist-panel`), здібності з дальністю, кулдауном і описом, бафи/дебафи.
- `+window:spellbook-shop` (character sheet): каталог усіх заклинань і навичок з цінами в SP, фільтр за тегами (`+feature:spell-filter-by-tag`), сторінка апгрейдів кожного заклинання.
- `+window:realm-preview`: наведення на рифт — мапа наступного рівня, вороги, предмети й сфери памʼяті в ній.
- `+ui:aoe-preview` — підсвітка клітин, які зачепить заклинання, і `threat-range` ворогів.
- `main-menu`, `settings-window` (мінімальні; роздільність не змінюється — скарга гравців), `end-screen` (смерть/перемога).
- Бойового журналу майже нема (скарга гравців) — `log-window` відсутнє.
- Переходи: main-menu → game-screen рівня 1; книга заклинань — модаль у будь-який хід (?); зачистка → рифт → preview → наступний рівень; смерть → end-screen → main-menu.

## Фічі поза полем
- `permadeath`, `+axis:session=run`: один забіг ~25 рівнів; автосейв з продовженням (?).
- Нема мета-прогресії: на старті доступний увесь каталог — сила лише в SP цього забігу.
- Модифікатори/моди (мод-підтримка Python-скриптами в спільноті) (?); `+feature:spell-filter-by-tag`.
- Rift Wizard 2 (2025): HP і заряди відновлюються після кожного рівня, зілля рідші (за оглядом).

## Варіації й родичі
- Впливи (за Steam): NetHack, DCSS, Brogue, ToME. Найближчі за духом: Hoplite (детермінована тактика на маленькій мапі), Into the Breach (повна інформація), Magic: The Gathering (заклинання з тегами як картки) (?).
- Наступники: Rift Wizard 2 (2025), Rift Wizard 3 (2026, крафт).
- Осі варіацій: **ресурс заклинань** (мана / заряди на рівень / кулдауни) · **прогресія** (XP / SP за сфери / предмети) · **інформація** (туман / повна мапа / повна мапа + превʼю наступного) · **синергія** (нема / теги + навички) · **рівень** (великий поверх / одноекранна арена).

## Цікавинки для курсу
- «Правила як заклинання»: заклинання = дані {теги, заряди, дальність, ефект}, апгрейд = патч цих даних — 🥈 (data-driven двіжок ефектів).
- Синергія тегів: навичка підписується на події заклинань з тегом — 🥉 (event bus).
- Типи шкоди й опори у відсотках, від’ємні = вразливість — 📎.
- Line of sight на сітці (Брезенхем/тіньове лиття) для цілі заклинання; прірва — не блокує зір — 🥉.
- Chain Lightning: ланцюг до випадкового ворога в радіусі, без повторів — 📎.
- Превʼю рифтів: генерація кількох наступних рівнів наперед і вибір — 🥉.
- Лігвище-спавнер, яке треба пріоритетно знищити — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `move-by-input` · `hp-damage` · `destroy-all-enemies` · `dungeon-generation` · `sequential-levels` · `player-death` · `projectile-shot` (болти, промені) · `blast-wave` (вогняна куля, землетрус) · `chase-bfs` · `melee-vs-ranged` · `item-pickup` + `inventory-items` (зілля) · `temporary-modes` (бафи/дебафи) · `impassable-cells` · `spawn-schedule` (лігвища) · `cell-transform` (стіна → підлога) · `shop-catalog` + `shop-preview` (книга заклинань за SP) · `cell-click` · `hover-highlight` · `game-screen` · `gui-render` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+spell-charges` «Заклинання із зарядами, поповнення на рівні» · entities/state · 📎 · слоти {charges, refill}.
  - `+sp-progression` «Очки навичок замість досвіду» · game-logic/economy · 🌱.
  - `+spell-upgrades` «Апгрейди як патч параметрів дії» · game-logic/economy · 🥉.
  - `+tag-synergy` «Навички підсилюють дії з тегом» · game-logic/economy · 🥉 · слот {tags}.
  - `+damage-types-resist` «Типи шкоди й опори у %» · entities/combat · 📎.
  - `+summon-minions` «Призов союзників на час» · entities/spawn · 🥉 · слот {duration}.
  - `+line-of-sight-cast` «Дія лише по клітинах у полі зору» · entities/legality · 🥉.
  - `+chasm-cells` «Прірва: не пройти, але видно й можна стріляти» · entities/legality · 🌱.
  - `+rift-choice-preview` «Вибір наступного рівня з превʼю» · levels/progression · 🥉.
  - `+lair-spawner` «Руйнівний спавнер ворогів» · entities/spawn · 🌱.
  - `+shrine-upgrade` «Клітина, що модифікує дію з тегом» · entities/interact · 📎.
  - `+monster-manual` «Повний опис ворога наведенням» (з Magic Tower) · interface/hud · 📎.
  - `+permadeath` (з Rogue).
  - `+card:rules-as-spells` — ідея всієї гри: механіки як каталог дій-даних.

## Пропозиції до словників
- `+trigger:cast` — сутність застосувала заклинання/здібність (на це підписуються навички); `+trigger:realm_cleared` — усі вороги рівня мертві (≈ `all_gone(enemies)`, але з наслідком «відкрити виходи»).
- `+cond:line_of_sight` (є ⏳ як умова — тут ключова); `+cond:has_tag` — дія/юніт має тег; `+cond:charges` — є заряди; `+cond:resist` — опір типу шкоди.
- `+effect:cast` — виконати дію-заклинання як дані; `+effect:summon` — спавн союзника з тривалістю; `+effect:resist` — змінити опір; `+effect:upgrade` — змінити параметри дії; `+effect:refill_charges`.
- `+role:minion` — тимчасовий призваний союзник (вужче за `ally`); `+role:rift` — вихід з превʼю й вибором; `+role:shrine` — модифікатор дій з тегом.
- `+window:spellbook-shop` — магазин дій за очки з фільтром тегів; `+window:realm-preview`; `+window:unit-inspect` — картка юніта з опорами й здібностями.
- `+ui:spell-bar-charges`, `+ui:resist-panel`, `+ui:aoe-preview` (зона ураження перед кастом).
- `+feature:spell-filter-by-tag`, `+feature:permadeath`; `+axis:session=run`.
- `+card:rules-as-spells` — картка-рамка «механіка як набір дій-даних з тегами».

## Джерела
- ⭐ [Steam: Rift Wizard](https://store.steampowered.com/app/1271280/) — опис дизайну, 25 рівнів, 100+ заклинань і навичок, «low randomness», впливи; скріншоти UI.
- [Gamepretty: усі заклинання](https://gamepretty.com/rift-wizard-all-spells-list-upgrades-effects-and-costs/) — рівні, теги, заряди, дальності, апгрейди з цінами.
- [Turn Based Lovers: огляд](https://turnbasedlovers.com/review/rift-wizard-review/) — рифти, заряди, зілля мани, вампір→кажан, Мордред.
- [Vaporlens: зведення відгуків](https://vaporlens.app/app/1271280/rift_wizard.md) — повна мапа, превʼю наступного рівня, святилища й кола, скарги на UI.
- [Steam: Rift Wizard 2](https://store.steampowered.com/app/2058570/) — продовження.
- YouTube: пошук «rift wizard gameplay».

## Непевне
- (?) Розмір рівня 28×28, HP чарівника 50, кількість сфер памʼяті на рівні — з памʼяті, не перевірено.
- (?) HP між рівнями в RW1 не відновлюється, а заряди — так: виведено з огляду RW2 («у RW2 HP і заряди відновлюються після рівня»); огляд RW1 каже про «портали, не на кожному рівні».
- (?) 24 чи 25 рівнів: Steam — 25, огляд — 24 + Мордред.
- (?) Огляд стверджує, що навички потребують рівнів за вбивства — суперечить іншим джерелам (SP за сфери); прийнято SP.
- (?) Фаза розстановки (deploy) на початку рівня, клавіша `a` для збору, автосейв, моди — з памʼяті.
