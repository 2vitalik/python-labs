---
title: Sproggiwood
slug: sproggiwood
aka: []
family: roguelike
also: [build-sim]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2014
platforms: [Windows, macOS, Linux]
links:
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2569875660", best: true, note: "Steam-гайд Savage Difficulty: 10 підземель, 6 класів і всі навички, зірки витривалості, предмети, повний бестіарій механік ворогів, Civic Boosts"}
  - {kind: steam, url: "https://store.steampowered.com/app/311720/Sproggiwood/", note: "Freehold Games, 24.10.2014: покроковий роглайк, 6 класів, процедурні підземелля, режим прикрашання міста"}
  - {kind: other, url: "https://steamcommunity.com/app/311720/guides/", note: "список гайдів: Savage, досягнення (19)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sproggiwood+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, hp-damage, item-pickup, inventory-items, inventory-limit, round-currency, shop-catalog, stairs-levels, dungeon-generation, fog-of-war, status-effects, unit-xp-skills, character-select, level-unlock, spawner-entity, explode-area, blast-wave, line-of-sight-attack, teleport, pull-object, player-death, permadeath, achievements-window, +split-on-death, +kill-charged-skills, +linked-enemies-same-turn, +stain-terrain, +single-consumable-slot, +town-decoration, +civic-boosts, +shrine-random-boon]
proposes: ["+effect:stars(±n)", "+cond:same_turn(a, b)", "+trigger:charge_line(a, b)", "+role:shrine", "+window:town-window", "+feature:town-decoration", "+card:kill-charged-skills", "+card:linked-enemies-same-turn", "+card:stain-terrain"]
author: opus
date: 2026-11-09
---

# Sproggiwood — аркадний роглайк від авторів Caves of Qud: короткі підземелля, навички за «зірки» від убивств і ворожі механіки-головоломки

## Суть
Фермер із Clog потрапляє у світ фінської міфології й «цивілізує» ліс: проходить 10 коротких підземель, кожне з босом, і між ними відбудовує місто. Роглайк спрощено до аркадного ядра: рух лише по ортогоналі, один слот витратного предмета, 3 навички + ультимейт класу. Навички коштують **зірки витривалості**, а зірку дає кожне вбивство — тож агресія живить здібності. Головний зміст — вороги з механіками-правилами: желе, що діляться й лишають плями-клітини, пари привидів, яких треба вбити в один хід, жаби, що підтягують язиком.

## Поле і час
- Квадратна сітка, рух лише ортогональний (без діагоналей).
- Забіг: випадкова «наземна» мапа з туманом війни → пошук сходів → поверхи підземелля (кількість різна) → кімната боса.
- Покроково: хід героя = хід ворогів; деякі вороги мають «замах» на хід (єті), деякі плями живуть N ходів.
- Генерація — процедурна («No two dungeon dives are alike»); дроп золота й XP — випадковий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (6 класів) | player | HP, зірки витривалості, рівень, навички | рух 4 напрямки; атака входом у ворога; навички за зірки |
| Велике желе | enemy | колір | при смерті ділиться на 1–3 малих |
| Мале желе | enemy | колір | лишає пляму: жовта — ковзання, синя — шкода, темна — через 6 ходів породжує велике темне желе, червоне — вибух-стазис (лід), фіолетова — ковзання + шкода |
| Гриб | enemy | — | засідка: зʼявляється поруч з героєм |
| Помаранчевий гриб | enemy | — | відкриває Bizarro Doors |
| Bizarro-монстр | enemy | — | удар телепортує героя |
| Кокон | spawner | — | породжує павуків (без XP) |
| Павук / отруйний / крижаний | enemy | — | павутина: не-павук втрачає хід; отруйний вибухає при смерті; крижаний заморожує |
| Козлолюд (Goatman) | enemy | — | таранить, коли герой на одній прямій |
| Жаба | enemy | стоїть | язик підтягує героя до себе |
| Блукаючий вогник (Wisp) | enemy | парний | звʼязаний з клоном: вбити обох в один хід, інакше відроджуються; викликається пасткою-листям |
| Летюча золота рибка | enemy | трійка | убити одну, потім двох інших в один хід |
| Єті | enemy | — | хапає сусіднього ворога й кидає його після замаху на 1 хід |
| Бос підземелля | boss | — | у кінці кожного з 10 підземель (Sapius ×2, фінал Surma) |
| Святиня (shrine) | neutral | випадковий дар | вогонь/лід, повне лікування, вороги → вази, виклик ворогів, телепорт; святиня здоровʼя — з серцем |
| Ваза | container | — | розбити — вміст (спец-вази) |
| Витратний предмет | pickup | 1 слот | зілля (HP, витривалість, невидимість 50 ходів, прискорення 30 ходів, Identity Crisis — переролити навички) або сувій (телепорт, виклик, Blizzard, Wonder, Pottery, Fireball) |
| Спорядження | pickup | зброя/броня/аксесуар | вогняна зброя — шкода, крижана — контроль; Alchemist's Vial — зілля двічі |
| Сходи | static | — | з наземної мапи в підземелля, між поверхами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `damage(enemy, atk)`.
- КОЛИ `died(enemy)` → ТО `custom: «+1 зірка витривалості»` (`+effect:stars`); ЯКЩО `custom: «ворог зі спавнера»` → ТО без XP.
- КОЛИ `input(skill)` → ЯКЩО `custom: «зірок ≥ ціни навички»` → ТО `custom: «навичка класу»`, `custom: «−зірки»`.
- КОЛИ `died(big_jelly)` → ТО `spawn(small_jelly ×1–3)`.
- КОЛИ `died(small_jelly)` → ТО `set_cell(cell, stain[color])`.
- КОЛИ `enter(hero, yellow_stain)` → ТО `slide(hero, dir)`; КОЛИ `enter(hero, blue_stain)` → ТО `damage(hero, n)`.
- КОЛИ `timer(6)` на темній плямі → ТО `spawn(big_dark_jelly)`.
- КОЛИ `died(wisp)` → ЯКЩО `custom: «клон не вбитий цього ж ходу»` → ТО `respawn(wisp)` (`+cond:same_turn`).
- КОЛИ `line_of_sight(goatman, hero)` → ТО `custom: «таран по прямій»` (`+trigger:charge_line`).
- КОЛИ `in_range(frog, hero, tongue)` → ТО `pull(hero)`.
- КОЛИ `enter(hero, web)` → ТО `stun(hero, 1)`.
- КОЛИ `died(poison_spider)` → ТО `explode(cross|3×3 (?), 1)`.
- КОЛИ `contact(bizarro, hero)` → ТО `teleport(hero, random)`.
- КОЛИ `turn_end(yeti)` → ЯКЩО `state(yeti, holding)` → ТО `custom: «кидає ворога»`; інакше `custom: «хапає сусіднього ворога»`.
- КОЛИ `picked(hero, consumable)` → ЯКЩО `has(hero, consumable)` → ТО `choose(Use | Keep (старий → золото) | Cash (новий → золото))`.
- КОЛИ `use(hero, haste_potion)` → ТО `set_state(hero, haste, 30)`: `custom: «вороги не ходять, поки рухаєшся»`.
- КОЛИ `use(hero, pottery_scroll)` → ТО `transform(nearby enemies, vase)`.
- КОЛИ `contact(hero, shrine)` → ТО `custom: «випадковий дар»` (`rng`).
- КОЛИ `counter(xp, >=, next)` → ТО `choose(нова навичка | рівень навички)`; ультимейт на рівні 5, тири 2/3 на рівнях 4/6.
- КОЛИ `died(boss)` → ТО `unlock(next dungeon)`; першого разу — новий клас; перший прохід кожним класом — `currency(+1000)`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (забіг закінчено).
- Перемога: пройти 10 підземель (фінальний бос Surma). Поразка: HP = 0 у забігу. Рахунку нема.

## Керування і ввід
- Крок/атака — напрямком (клавіатура або мишка (?)); навички — вибрати й указати ціль/напрям.
- Вибір при підборі предмета: Use / Keep / Cash.

## Вікна, меню, HUD
- `game-screen`: сітка, `hp-bar`, зірки витривалості, `skill-bar`, слот витратного предмета, `fog-overlay`.
- `character-select`: 6 класів (Farmer, Warrior, Archer, Thief, Vampire, Wizard).
- `world-map` / `level-select`: 10 підземель, відкриваються по черзі.
- `upgrade-window`: вибір навички на рівні.
- `shop-window`: спорядження (асортимент відкривається, коли річ уперше знайдено в підземеллі); Civic Boosts.
- `town-window`: прикрашання міста — будівлі, дерева, дороги, мешканці.
- `achievements-window` (19 досягнень), `difficulty-select` (є складність Savage).

## Фічі поза полем
- `meta-progression`: Civic Boosts — 5 рангів по 750 × ранг: +XP, +стартове HP, знижка, більше святинь, більше спец-ваз.
- `level-unlock` підземель і класів; `town-decoration` (sandbox-місто без впливу на бій (?)).
- `difficulty-presets` (Savage), `achievements`, `cloud-save`.

## Варіації й родичі
- Автори — Freehold Games ([caves-of-qud](caves-of-qud.md)); аркадний сусід — [cardinal-quest](cardinal-quest.md) (2011, 3 класи, навички на перезарядці), [pixel-dungeon](pixel-dungeon.md) (мобільний спрощений роглайк), [desktop-dungeons](desktop-dungeons.md) (короткі підземелля + місто).
- Відмінності від класики [rogue](rogue.md): ресурс навичок наповнюється вбивствами (не маною/часом); інвентар — один слот; вороги — «головоломки з правилом» (поділ, пари одного ходу, плями-клітини).
- Осі варіацій: ресурс навичок (мана / перезарядка / заряди за вбивства) · інвентар (повний / 1 слот) · структура (довге підземелля / короткі «рівні» з босом).

## Цікавинки для курсу
- Желе: поділ при смерті + пляма-клітина з тривалістю та спавном через 6 ходів — 📎.
- Парні вороги «вбий обох в один хід» — 🌱 (лічильник ходу смерті).
- Зірки за вбивства як валюта навичок — 🌱.
- Єті: схопити-і-кинути сусіднього ворога з замахом — 📎 (стан на хід).
- Жаба-язик (притягування) і козлолюд-таран по прямій — 🌱 кожне.
- Один слот витратного з вибором Use/Keep/Cash — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `item-pickup` · `inventory-items` · `inventory-limit` (1 слот) · `round-currency` · `shop-catalog` · `stairs-levels` · `dungeon-generation` · `fog-of-war` · `status-effects` (заморозка, невидимість, прискорення) · `unit-xp-skills` · `character-select` · `level-unlock` · `spawner-entity` (кокон) · `explode-area` / `blast-wave` (гарбузова бомба 3×3, Fire Trap хрестом) · `line-of-sight-attack` (козлолюд) · `teleport` · `pull-object` (жаба) · `player-death` · `permadeath` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+split-on-death` «Ворог ділиться на менших при смерті» · entities/spawn · 🌱 · слот {count}.
  - `+kill-charged-skills` «Навички за заряди від убивств» · entities/combat · 🌱.
  - `+linked-enemies-same-turn` «Звʼязані вороги: вбити всіх за один хід» · entities/death · 🌱.
  - `+stain-terrain` «Мертвий ворог лишає клітину-ефект» · entities/spawn · 📎.
  - `+single-consumable-slot` «Один слот: використати / залишити / продати» · entities/state · 🌱.
  - `+town-decoration` · `+civic-boosts` · `+shrine-random-boon` — місто-пісочниця, постійні апгрейди, святиня з випадковим даром.

## Пропозиції до словників
- `+effect:stars(±n)` — зміна заряду навичок (можна й через `counter`, але це окремий ресурс класу).
- `+cond:same_turn(a, b)` — події сталися в один хід.
- `+trigger:charge_line(a, b)` — B на прямій з A → A кидається (ширше за `line_of_sight`: з рухом).
- `+role:shrine` — обʼєкт одноразового випадкового дару (або ⏳ `neutral`).
- `+window:town-window` — екран міста між забігами.
- `+feature:town-decoration`.
- `+card:kill-charged-skills` · `+card:linked-enemies-same-turn` · `+card:stain-terrain`.

## Джерела
- ⭐ [Steam-гайд Savage Difficulty](https://steamcommunity.com/sharedfiles/filedetails/?id=2569875660) — структура забігу, класи й навички, зірки, предмети, механіки всіх ворогів, Civic Boosts (гайд позначений як знятий, текст видно).
- [Steam: Sproggiwood](https://store.steampowered.com/app/311720/Sproggiwood/) — опис, 6 класів, процедурні підземелля, режим прикрашання міста, теги (Perma Death).
- [Steam: гайди](https://steamcommunity.com/app/311720/guides/).
- YouTube: [пошук](https://www.youtube.com/results?search_query=Sproggiwood+gameplay).

## Непевне
- (?) Черга: «поверх = одна арена» — гайд описує наземну мапу + кілька поверхів + кімнату боса; чи поверх уміщується на один екран, не перевірено.
- (?) Форма вибуху отруйного павука; дальність язика жаби.
- (?) Чи місто дає щось, крім Civic Boosts (декор — схоже, лише косметика).
- (?) Правила складності Savage; чи смерть остаточна для всієї кампанії (гайд: «0 HP закінчує забіг»).
- (?) Керування мишкою/тачем — не підтверджено.
