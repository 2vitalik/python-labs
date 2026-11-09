---
title: "Defender's Quest: Valley of the Forgotten"
slug: defenders-quest
aka: ["Defender's Quest", "Defender's Quest DX", DQ]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2012
platforms: [web (Flash), PC, Mac, Linux, PS4, Xbox One, PS Vita]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/218410/Defenders_Quest_Valley_of_the_Forgotten_DX_edition/", best: true, note: "персонажі замість веж, рівні й навички кожного, спорядження, бій у реальному часі зі швидкістю й наказами на паузі; скриншоти HUD бою й мапи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Defender's_Quest", note: "Level Up Labs, Flash-оригінал, DX (2016), New Game+, сиквел 2025"}
  - {kind: other, url: "https://www.thexboxhub.com/defenders-quest-valley-forgotten-dx-review/", note: "огляд DX: Psi за вбивства, виклик і буст героїв, 5 рівнів сили, класи, дерева навичок, магазини й найманці, 4 складності, NG+"}
  - {kind: other, url: "https://ayumilove.net/defender-quest-walkthrough-guide/", note: "проходження: класи, розстановка від дороги, Lightning, Frenzy, апгрейди зброї, Extreme / Hero mode"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Defender%27s+Quest+Valley+of+the+Forgotten+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, spawn-points, hp-damage, melee-vs-ranged, status-effects, round-currency, unit-xp-skills, shop-between-levels, shop-catalog, world-map, difficulty-levels, game-pause, sequential-levels, level-select, in-game-editor, level-exchange, achievements-window, +party-formation, +summon-creature, +xp-level-up, +equipment-slots, +mana-pool-spells, +call-wave-early, +speed-control, +stars-rating, +boost-in-battle, +recall-refund, +donut-range, +wave-preview-list, +new-game-plus]
proposes: ["+role:unit", "+effect:summon", "+effect:level_up", "+effect:recall", "+effect:cast", "+effect:upgrade", "+cond:cooldown_ready", "+ui:wave-preview-list", "+ui:speed-buttons", "+ui:class-tabs", "+feature:new-game-plus", "+card:boost-in-battle", "+card:recall-refund", "+card:donut-range"]
author: opus
date: 2026-11-09
---

# Defender's Quest — TD, де вежі — члени партії RPG: виклик за Psi, буст рівня в бою, спорядження й навички між боями

## Суть
Гібрид TD і тактичної RPG (Level Up Labs): бібліотекарка Azra стоїть у кінці шляху, а мерці-ревенанти хвилями йдуть до неї. Замість веж вона викликає на клітини мапи своїх героїв — берсерків, рейнджерів, лікарів, лицарів, крижаних магів, драконів. Валюта бою Psi капає за кожне вбивство й витрачається на виклик, **буст** героя (вищий рівень сили відкриває нові атаки), відкликання й закляття самої Azra. Між боями герої отримують досвід, вкладають очки в дерева навичок і вдягають спорядження з магазинів.

## Поле і час
- Мапа бою — сітка тайлів: дорога ворогів (темні клітини) і «суша», де можна ставити героїв; кілька порталів-входів, Azra — на кінцевій точці (скриншот DX).
- Відстань від дороги має значення: ближній бій — впритул до дороги, стрілки — далі; у рейнджера зона атаки — «бублик» із мертвою зоною поруч.
- Real-time з керуванням швидкістю: пауза, ¼, ½, 1, 2, 4, 8, 16; на паузі можна віддавати накази.
- Хвилі видно наперед списком (тип, кількість, рівень); наступну можна викликати раніше кнопкою «Send NEXT».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Azra | player | HP, Psi | стоїть у кінці шляху; кастує закляття за Psi; ревенанти йдуть до неї |
| Берсерк | ally | атака, без броні, рівень сили 1–5 | ближній бій навколо себе, кровотеча |
| Рейнджер | ally | дальність-«бублик», крит, отрута | стріляє далеко, може накривати 2–3 гілки дороги |
| Лікар (Healer) | ally | радіус | лікує поранених союзників поруч |
| Лицар | ally | висока броня, повільний удар | бʼє важко, знижує броню ворога; стоїть попереду берсерків |
| Крижаний маг | ally | дальність | охолоджує, сповільнює й заморожує; вогонь дракона знімає холод |
| Дракон | ally | — | ближній бій, згодом — вогняні кулі з горінням |
| Найманець (recruit) | ally | клас, випадкова зовнішність | безіменний герой із таверни міста |
| Ревенант (різні типи) | enemy | HP, рівень, броня, швидкість | іде дорогою від порталу до Azra; частина має дальні магічні атаки |
| Бос (напр., Super Sheep) | boss | HP | окремий бій зі своїми слабкостями |
| Портал | spawner | колір | звідки виходить хвиля |
| Дорога | terrain | — | шлях ворогів; героїв на неї не ставлять (?) |
| Суша | terrain | — | місце виклику героя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `wave_start` (`schedule(waves)`) → ТО `spawn_at(revenants, portal)`; ревенанти `move(a, next_on_path)` до Azra.
- КОЛИ `input(summon, hero, cell)` → ЯКЩО `counter(psi, >=, class_cost)` and `free(cell)` and `custom: «клітина — не дорога»` → ТО `place(hero)`, `currency(-cost)`.
- КОЛИ `in_range(hero, revenant, r)` → ЯКЩО `custom: «атака перезарядилась»` → ТО `damage(n)`; рейнджер — ЯКЩО `not in_range(hero, revenant, dead_zone)`.
- КОЛИ `hp_zero(revenant)` → ТО `disappear`, `currency(+psi)`, `counter(xp, +n)`.
- КОЛИ `input(boost, hero)` → ЯКЩО `counter(psi, >=, boost_cost)` and `custom: «рівень сили < 5»` → ТО `custom: «рівень сили +1: більше статів, відкривається атака цього тиру»`, `currency(-cost)`.
- КОЛИ `input(recall, hero)` → ТО `disappear`, `currency(+part_of_spent)`, `custom: «рівень сили скидається»`.
- КОЛИ `hp_zero(hero)` → ТО `disappear`; КОЛИ `input(redeploy, hero)` → ЯКЩО `counter(psi, >=, cost)` → ТО `place(hero)` з рівнем сили 1.
- КОЛИ `contact(revenant, hero)` / `in_range(caster, hero, r)` → ТО `damage(hero, n)`; лікар — `heal(ally, n)` у радіусі.
- КОЛИ `contact(ice_attack, revenant)` → ТО `speed(revenant, -k)` / `freeze(revenant, n)`; КОЛИ `contact(fire, chilled)` → ТО `clear_state(revenant, chill)`.
- КОЛИ `contact(attack, revenant)` → ЯКЩО `custom: «у героя навичка кровотечі / отрути»` → ТО `set_state(revenant, bleed|poison, dur)`; КОЛИ `tick` → ЯКЩО `state(revenant, bleed|poison)` → ТО `damage(n)`.
- КОЛИ `input(cast, spell)` → ЯКЩО `counter(psi, >=, cost)` → ТО Lightning — `damage(target, n)`; Frenzy — `custom: «союзники атакують удвічі швидше на час»`; Heal — `heal(allies, n)` (?).
- КОЛИ `reach(revenant, azra)` → ТО `damage(azra, n)` (?); КОЛИ `hp_zero(azra)` → ТО `lose` (?).
- КОЛИ `input(send_next)` → ТО `custom: «наступна хвиля одразу»`.
- КОЛИ `custom: «усі хвилі бою знищено»` → ТО `win`, `custom: «зірки бою за складність»` (?), `give(party, xp)`, `currency(+gold)`.
- КОЛИ `custom: «перемога на Extreme без шкоди Azra»` → ТО `give(player, unique_gear)`.
- Перемога: пережити всі хвилі бою · Поразка: Azra загинула (?) · Рахунок: зірки за бій, золото, досвід.

## Керування і ввід
- Миша (основне), геймпад у консольних версіях (огляди: «незручно»).
- Гарячі клавіші: закляття Azra 1–6, вкладки класів Q W E R T Y, конкретні герої класу A S D F G H; виклик — вибрати героя і клітину.
- Клік по викликаному герою — буст / відкликання / вибір цілі (?); кнопки + і × внизу мапи бою (?).
- Кнопки швидкості й паузи; «Send NEXT» — наступна хвиля раніше.

## Вікна, меню, HUD
- `game-screen` бою: ліворуч — `+ui:wave-preview-list` («3/18 Waves», хвилі з типом ворога, кількістю й рівнем, «6 MORE»), кнопка «Send NEXT»; праворуч — портрет Azra з `hp-bar` і Psi-смугою, `skill-bar` заклять 1–6, `+ui:class-tabs` (клас і скільки героїв викликано: 5/6), ціна виклику «PSI: 50», ряд портретів героїв класу з рівнями; унизу — `+ui:speed-buttons` (пауза, ¼…16) і Options.
- `map-window` / `world-map`: вузли боїв (червоні) і подій (сині) з трьома зірками, місто; меню знизу: Party · Movies · Options · Tips & Tricks · Bonus, лічильник грошей, щоденник Azra (книжка з числом).
- `character-select` / «Party»: склад, спорядження, дерева навичок кожного героя (`inventory-window`, `upgrade-window`).
- `shop-window` у містах: зброя, броня, найм героїв; `difficulty-select` перед боєм; `dialogue-window` — сюжетні сцени; `settings-window` (доступність); `editor-window` (DX: редактор рівнів, Workshop).

## Фічі поза полем
- `xp-level`: герої отримують досвід за бої, рівні → очки навичок у дерево класу (навіть безіменні найманці).
- `meta-progression` через спорядження: зброя з магазину з апгрейдами (кровотеча, отрута, крит, швидкострільність, дальність).
- `difficulty-presets` для кожного бою (огляди: Easy/Normal/Hard/Extreme; гайди: Normal/Advanced/Extreme + Hero mode) (?); `world-map` з опційними боями.
- `+feature:new-game-plus` (Play+): нові бої, торговці, місії, записи щоденника, зброя.
- `speed-control` 1/4–16×, `pause` з наказами; `level-editor` + Workshop, `achievements`, `cloud-save`, 11 мов.

## Варіації й родичі
- Defender's Quest DX (2016) — HD-ремастер, більше сюжету; порти PS4/Xbox One/Vita. Defender's Quest 2: Mists of Ruin (2025) — сиквел.
- Родичі: [arknights](arknights.md) (оператори-персонажі замість веж, ціна виклику), [crystal-defenders-vanguard-storm](crystal-defenders-vanguard-storm.md) (класи Final Fantasy як вежі), [legend-of-keepers](legend-of-keepers.md), [gemcraft](gemcraft.md) (мана як валюта й HP одночасно).
- **Осі варіацій**: «вежа» — споруда / персонаж із рівнем і спорядженням · прокачка — лише в бою / лише між боями / обидві (тут: буст у бою + XP між боями) · відкликання — нема / з частковим поверненням / продаж.

## Цікавинки для курсу
- Буст у бою: рівень сили 1–5 за Psi, кожен рівень відкриває атаку, відкликання скидає рівень і повертає частину Psi — 🥉.
- Дві прогресії однієї сутності: тимчасова (у бою) і постійна (XP, навички, спорядження) — 🥈.
- Зона атаки-«бублик» із мертвою зоною (рейнджер) — 📎.
- Взаємодія статусів: вогонь знімає холод — 📎 (таблиця несумісностей ефектів).
- Швидкість 1/4–16× і накази на паузі — 🌱 (масштаб тіку).
- Список хвиль наперед і «Send NEXT» — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ виклик героя на клітину · `tower-range` ↔ радіуси класів · `enemy-waves` · `spawn-points` ↔ портали · `hp-damage` · `melee-vs-ranged` ↔ класи · `status-effects` ↔ кровотеча, отрута, холод · `round-currency` ↔ Psi · `unit-xp-skills` ↔ XP і дерева навичок · `shop-between-levels` + `shop-catalog` ↔ міста · `world-map` · `difficulty-levels` · `game-pause` · `sequential-levels` · `level-select` · `in-game-editor` + `level-exchange` ↔ редактор і Workshop · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+boost-in-battle` «Апгрейд сутності за валюту бою з відкриттям тиру атаки» · game-logic/economy · 🥉 · слот {max_level: 5}.
  - `+recall-refund` «Відкликати юніт із частковим поверненням і скиданням рівня» · game-logic/economy · 📎.
  - `+donut-range` «Зона атаки з мертвою зоною всередині» · entities/combat · 📎 (дитина `tower-range`).
  - `+wave-preview-list` «Список наступних хвиль: тип, кількість, рівень» · interface/hud · 🌱.
  - `+new-game-plus` «Друге проходження з новим контентом» · levels/progression · 🌱.
  - уже вживані: `+party-formation`, `+summon-creature`, `+xp-level-up`, `+equipment-slots`, `+mana-pool-spells`, `+call-wave-early`, `+speed-control`, `+stars-rating`.

## Пропозиції до словників
- `+role:unit` — бойовий персонаж гравця, що стоїть на клітині як вежа (≠ споруда).
- `+effect:summon` — виклик героя з резерву за валюту; `+effect:recall` — відкликання з поверненням частини ціни.
- `+effect:level_up` — підвищити рівень сили (буст); `+effect:upgrade` — апгрейд зброї між боями.
- `+effect:cast` — закляття Azra за Psi; `+cond:cooldown_ready` — атака/закляття перезарядилось.
- `+ui:wave-preview-list` · `+ui:speed-buttons` (пауза, ¼…16×) · `+ui:class-tabs` (вкладки класів із лічильником викликаних).
- `+feature:new-game-plus`.
- `+card:boost-in-battle`, `+card:recall-refund`, `+card:donut-range`.

## Джерела
- ⭐ [Steam: Defender's Quest DX](https://store.steampowered.com/app/218410/Defenders_Quest_Valley_of_the_Forgotten_DX_edition/) — персонажі замість веж, рівні, навички й спорядження кожного, швидкість і накази на паузі, Workshop і редактор; скриншоти HUD бою (HP/Psi Azra, закляття 1–6, класи, ціна PSI, швидкості, список хвиль) і мапи (вузли, зірки, місто).
- [Wikipedia](https://en.wikipedia.org/wiki/Defender's_Quest) — Level Up Labs, Flash-оригінал, DX 2016 і порти, New Game+, сиквел 2025.
- [TheXboxHub: огляд DX](https://www.thexboxhub.com/defenders-quest-valley-forgotten-dx-review/) — Psi на старті й за вбивства, виклик, буст до 5-го тиру, відкликання й повторний виклик, класи (бублик рейнджера), дерева навичок, міста й найманці, 4 складності, нагорода за Extreme без шкоди Azra, NG+, швидкість до 4×.
- [Ayumilove: проходження](https://ayumilove.net/defender-quest-walkthrough-guide/) — класи й ролі, розстановка від дороги, Psi за вбивства, Lightning, Frenzy подвоює швидкість атаки, вогонь знімає холод, апгрейди зброї, Extreme / Hero mode / Play+.

## Непевне
- (?) Що саме відбувається, коли ревенант доходить до Azra (втрата HP чи Psi), і чи поразка — лише HP Azra = 0; на скриншоті в неї окремі HP і Psi.
- (?) Набір складностей: огляд DX — 4 режими (Easy/Normal/Hard/Extreme), гайди — Normal/Advanced/Extreme і Hero mode; за що даються 3 зірки бою.
- (?) Рівнів сили 5 (огляд DX) чи «максимум чотири бусти» (RPGamer у пошуковому фрагменті) — те саме, якщо базовий рівень = 1.
- (?) Ціни виклику/бусту по класах, частка повернення при відкликанні, чи можна ставити героїв на дорогу.
- (?) Призначення іконок + і × у списку хвиль і кнопок + / × під мапою бою.
