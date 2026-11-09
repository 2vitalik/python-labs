---
title: Castle Doombad
slug: castle-doombad
aka: [Castle Doombad Classic, "Castle Doombad: Free to Slay", Касл Думбад]
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
year: 2014
platforms: [iOS, Android, PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2888470/Castle_Doombad_Classic/", best: true, note: "Classic (2024): автоматичні й ручні пастки на таймінг, 30+ пасток і міньйонів, 150+ апгрейдів, лут героїв зі слотами, 90 етапів кампанії, роглайт Roguevenge; скриншоти поверхів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Castle_Doombad", note: "Dr. Lord Evilstein, пастки автоматичні й ручні, міньйони; дати, сиквел, ремейк"}
  - {kind: official, url: "https://www.castledoombad.com", note: "Classic, Free to Slay, анонс Castle Doombad 2 з кооперативом"}
  - {kind: other, url: "https://www.pocketgamer.com/castle-doombad/review/", note: "огляд: герої йдуть на передостанній поверх, хапають принцесу й тікають через нижній вихід; списомети біля драбин"}
  - {kind: other, url: "https://www.gmanetwork.com/news/scitech/content/346083/game-review-it-s-good-to-be-bad-in-castle-doombad/story", note: "огляд: валюта — крики принцеси, ручні пастки з перезарядкою, міньйони, типи героїв"}
  - {kind: other, url: "https://destructoid.com/?p=139187", note: "огляд: сітка поверхів, драбини у вікна й підкопи, Scream/Gold/Doom Points, корона за рівень без дотику до принцеси"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Castle+Doombad+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, spawn-points, hp-damage, projectile-shot, shoot-cooldown, status-effects, speed-per-type, melee-vs-ranged, ladder-climb, round-currency, shop-between-levels, in-round-upgrades, sequential-levels, level-select, run-relics, achievements-window, +summon-creature, +manual-trap-cooldown, +trap-mount-surface, +princess-carry-escape, +passive-cry-income, +trap-dismantle, +breach-entry-points, +equipment-slots, +pre-level-boosters, +no-touch-crown]
proposes: ["+role:trap", "+trigger:attacked", "+effect:sell", "+effect:upgrade", "+effect:manual_trigger", "+cond:cooldown_ready", "+cond:on_surface", "+ui:trap-tray", "+ui:waves-remain-bar", "+feature:trap-reskins", "+card:manual-trap-cooldown", "+card:princess-carry-escape", "+card:trap-mount-surface"]
author: opus
date: 2026-11-09
---

# Castle Doombad — TD від лиходія: пастки на підлозі, стелі й стінах поверхів замку, ручні пастки б'ють на таймінг

## Суть
Гравець — лиходій Dr. Lord Evilstein, що викрав принцесу. Герої хвилями лізуть у замок (вид збоку, кілька поверхів), піднімаються драбинами до кімнати з принцесою, хапають її й несуть до нижнього виходу. Лиходій ставить у клітини поверхів **автоматичні пастки** (шипи, гарпуни, бігова доріжка), **ручні** (стомпер, піратська гармата — тапнути вчасно, потім перезарядка) і **міньйонів**, що ходять своїм поверхом. Валюту «Scream» генерують крики принцеси, тобто дохід іде сам собою.

## Поле і час
- Вид збоку: замок — стос поверхів-коридорів, з'єднаних драбинами; кожен поверх — ряд клітин під пастки (Destructoid: «the fortress is a grid across multiple floors»).
- Місця для пасток трьох типів: підлога (шипи), стеля (щупальця, кислотні краплі, пилка), стіна/кут (гарпун, списомет) (?). Міньйона можна поставити будь-де на поверсі.
- Входи: парадні двері, а також драбини до вікон і підкопи, які герої роблять посеред хвилі; Classic додає бур-машину, що пробиває стіну (скриншот).
- Над замком — кімната управління лиходія. Принцеса сидить у капсулі на одному з верхніх поверхів (Pocket Gamer: «second-to-top floor»), на скриншотах Classic — також нижче.
- Real-time: перед хвилею ~хвилина на розстановку (GMA), далі хвилі за смугою «Waves remain».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-рука | — | вибрана пастка з лотка | ставить, тапає ручні пастки, прибирає в смітник |
| Поверх (клітина підлоги) | terrain | — | шлях героїв; місце підлогових пасток |
| Стеля / стіна поверху | static | — | місце стельових і настінних пасток |
| Драбина | terrain | — | перехід між поверхами для героїв |
| Вхід (двері, драбина до вікна, підкоп) | spawner | — | звідси заходять герої хвилі |
| Принцеса в капсулі | object | — | джерело Scream; ціль героїв; виноситься на собі |
| Нижній вихід | static | — | герой із принцесою дійшов — поразка |
| Шипи (floor spikes) | trap | авто | шкодять тим, хто наступив; ніндзя їх оминають |
| Гарпунна гармата, списомет | tower | авто, дальність | стріляють уздовж поверху; біля драбини — і вниз (Pocket Gamer) |
| Бігова доріжка смерті | trap | авто | сповільнює героїв під обстрілом |
| Пилка (buzzsaw) | trap | стеля | бʼє по тих, хто на стелі (ніндзя) |
| Кислотні краплі | trap | стеля | капають униз, сумуються зі шипами |
| Щупальця | trap | стеля | зривають із героя щит і шолом |
| Лазер, AC-сповільнювач | trap | авто | шкода по лінії / сповільнення |
| Стомпер, піратська гармата | trap | ручна, перезарядка | сильний удар за тапом; гармата чистить цілий поверх |
| Тролль | ally | — | перекриває коридор |
| Міньйон-демон | ally | HP | бачить героя — атакує; ходить своїм поверхом |
| Медик-міньйон | ally | — | лікує міньйонів і пастки |
| Міньйон-бомба | ally | — | ставиться під ноги героя й вибухає |
| Scream generator | resource | — | підсилює приплив Scream |
| Лицар | enemy | HP | базове «мʼясо» |
| Ніндзя | enemy | — | бігає стелею, підлогові пастки не діють |
| «Sexy knight» | enemy | — | зупиняється на селфі; товстий |
| Rambo-клон, «eye-beam» герої | enemy | дальня атака | розстрілюють пастки й міньйонів |
| Герой-механік (Indiana Jones-подібний) | enemy | — | розбирає пастки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `wave_start` → ТО `spawn_at(heroes, entry)`; КОЛИ `rng(p)` → ТО `custom: «герой приставляє драбину до вікна або робить підкоп — новий вхід посеред хвилі»`.
- КОЛИ `tick` → ЯКЩО `not has(hero, princess)` → ТО `move(hero, to_princess)` драбинами вгору; інакше `move(hero, to_exit)`.
- КОЛИ `timer(every)` → ТО `currency(+scream)` («крики принцеси живлять машину смерті»); scream generator → `multiplier(×k)` (?).
- КОЛИ `input(place, trap, cell)` → ЯКЩО `counter(scream, >=, cost)` and `free(cell)` and `custom: «поверхня клітини відповідає пастці: підлога / стеля / стіна»` → ТО `place(trap)`, `currency(-cost)`.
- КОЛИ `enter(hero, spikes)` → ЯКЩО `not state(hero, on_ceiling)` → ТО `damage(n)`.
- КОЛИ `in_range(harpoon, hero, r)` → ТО `spawn(projectile)`; КОЛИ `contact(projectile, hero)` → ТО `damage(n)`.
- КОЛИ `enter(hero, treadmill)` → ТО `speed(hero, -n)`.
- КОЛИ `in_range(tentacles, hero, 1)` → ТО `take(hero, shield)`, `take(hero, helmet)`.
- КОЛИ `input(tap, manual_trap)` → ЯКЩО `not state(manual_trap, recharging)` → ТО `damage(n)` по зоні, `set_state(manual_trap, recharging, dur)`.
- КОЛИ `line_of_sight(minion, hero)` → ТО `move(minion, to_hero)`, `damage(n)`; медик — `heal(neighbor, n)`.
- КОЛИ `input(drop, bomb_minion, hero_cell)` → ТО `explode(area, n)`.
- КОЛИ `in_range(hero, trap, r)` → ЯКЩО `custom: «тип героя руйнує пастки (механік, стрілець)»` → ТО `damage(trap, n)`; КОЛИ `hp_zero(trap)` → ТО `disappear`.
- КОЛИ `contact(hero, princess)` → ТО `carry(hero, princess)`, `custom: «рівень втрачає корону»`.
- КОЛИ `reach(hero, exit)` → ЯКЩО `has(hero, princess)` → ТО `lose`.
- КОЛИ `hp_zero(hero)` → ТО `disappear`, `custom: «принцеса повертається в капсулу»` (?), `custom: «шанс луту-спорядження»`.
- КОЛИ `custom: «усі хвилі відбиті»` → ТО `win`, `currency(+gold)`; ЯКЩО `custom: «ніхто не торкнувся принцеси»` → ТО `custom: «корона рівня»`.
- КОЛИ `level_start` → ЯКЩО `has(player, doom_points)` → ТО `choose(super_power)` — тимчасова надсила на рівень.
- Перемога: пережити всі хвилі етапу · Поразка: герой виніс принцесу через нижній вихід · Рахунок: золото за етап (більше за кращу гру), корона за «чистий» етап.

## Керування і ввід
- Тач (оригінал) / миша (Classic, уперше в серії): перетягнути пастку з лотка в клітину поверху; тап по ручній пастці — спрацювання; тап по міньйону-бомбі — підкласти під героя.
- Смітник праворуч від лотка — прибрати пастку (з поверненням Scream?) (?).
- Steam Deck — тач; кнопки й стік — «скоро».

## Вікна, меню, HUD
- `game-screen`: розріз замку з поверхами; угорі праворуч — Scream (лічильник із «!»), монети, токени-черепи; угорі ліворуч — Nightmare powers із лічильниками; угорі — `+ui:waves-remain-bar` (смуга хвиль із фігуркою героя); унизу — `+ui:trap-tray` (5–6 карток пасток із ціною Scream, закриті — сірі) і смітник; банер «HEROES INCOMING!».
- `level-select` / мапа етапів кампанії (90 етапів у Classic) (?).
- `shop-window`: покупка й апгрейд пасток/міньйонів/замку за монети; `inventory-window` — спорядження лиходія зі слотами й «Baddie Bonus».
- `custom-window` кімнати управління: косметика лиходія й кімнати, рескіни пасток.
- `mode-select`: Campaign · Dr. Lord Evilstein's Roguevenge.
- `end-screen` з монетами й короною; `achievements-window` (Steam); `settings-window` (15 мов).

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 90 етапів-«пазлів» кампанії.
- `meta-progression`: монети → відкриття й апгрейди 30+ пасток і міньйонів (150+ апгрейдів), апгрейд міняє вигляд і функцію пастки (Destructoid).
- Лут героїв → `equipment-slots` лиходія з обмеженою кількістю слотів; кожен предмет має свій «Baddie Bonus» апгрейд.
- Doom Points за челенджі (убити N лицарів) → тимчасові надсили на рівень («cheat codes basically»).
- `mode-endless`-подібний роглайт Roguevenge: щоразу інший замок, гравець сам вибирає, як замок розростається, збирає арсенал і Nightmare powers за забіг.
- `custom-skins` (`+feature:trap-reskins`), `achievements`, `cloud-save`; без реклами й IAP у Classic.

## Варіації й родичі
- Серія: Castle Doombad (2014, iOS/Android, Adult Swim) → Castle Doombad: Free to Slay (2014, f2p) → Castle Doombad Classic (Steam 2024, ремастер + Roguevenge) → Castle Doombad 2: Muahaha! (у розробці, кооп на двох).
- Родичі: [dungeon-warfare](dungeon-warfare.md) (пастки на підлозі й стінах коридорів), [orcs-must-die](orcs-must-die.md) (пастки + герой), [legend-of-keepers](legend-of-keepers.md), [my-life-as-a-darklord](my-life-as-a-darklord.md) і [what-did-i-do-to-deserve-this](what-did-i-do-to-deserve-this.md) (лиходій-оборонець), [dungeon-keeper](dungeon-keeper.md).
- **Осі варіацій**: поверхня пастки — підлога / стеля / стіна · спрацювання — авто / ручне з перезарядкою · ціль ворога — дійти до бази / вкрасти й винести (тут — «туди й назад») · входи — фіксовані / герої відкривають нові посеред хвилі.

## Цікавинки для курсу
- Ручна пастка: тап → удар по зоні → стан «перезарядка» N секунд — 🌱 (таймер стану + ввід).
- Три поверхні монтажу (підлога / стеля / стіна) з різними пастками й ворог-ніндзя, якого підлога не бачить — 📎.
- Ціль «вкрасти й винести»: шлях ворога змінюється, коли він несе принцесу, і поразка — лише на виході — 🥉 (дві фази маршруту, BFS у дві цілі).
- Поверхи + драбини як граф для пошуку шляху героїв, нові входи посеред хвилі — 🥉.
- Вороги, що руйнують пастки (HP у пастки, лікар-міньйон її лікує) — 📎.
- Пасивний дохід «криками» замість винагороди за вбивства — 🌱.

## Мапа на каталог
- Є: `tower-placement` ↔ пастки в клітинах поверхів · `tower-range` ↔ гарпуни, списомети · `enemy-waves` · `spawn-points` ↔ двері, вікна, підкопи · `hp-damage` · `projectile-shot` + `shoot-cooldown` · `status-effects` ↔ сповільнення доріжкою, AC · `speed-per-type` · `melee-vs-ranged` ↔ стрільці розстрілюють пастки · `ladder-climb` ↔ герої лізуть драбинами · `round-currency` ↔ Scream · `shop-between-levels` ↔ апгрейди за монети · `in-round-upgrades` (?) · `sequential-levels` · `level-select` · `run-relics` ↔ Nightmare powers у Roguevenge · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+manual-trap-cooldown` «Ручна пастка: тап і перезарядка» · entities/combat · 🌱 · слот {cooldown}.
  - `+trap-mount-surface` «Поверхня монтажу: підлога / стеля / стіна» · entities/legality · 📎 (родич `+wall-trap` з Dungeon Warfare).
  - `+princess-carry-escape` «Ворог несе ціль назад до виходу» · game-logic/lose · 🥉.
  - `+passive-cry-income` «Дохід, що капає сам» · game-logic/economy · 🌱.
  - `+trap-dismantle` «Вороги руйнують пастки» · entities/combat · 📎.
  - `+breach-entry-points` «Нові входи посеред хвилі» · entities/spawn · 📎.
  - `+no-touch-crown` «Нагорода за рівень без жодного дотику до цілі» · game-logic/score · 🌱.
  - `+summon-creature`, `+equipment-slots`, `+pre-level-boosters` — уже вживані в корпусі.

## Пропозиції до словників
- `+role:trap` — пастка гравця на клітині шляху (тут три поверхні монтажу).
- `+trigger:attacked` — пастка/міньйон отримали удар героя.
- `+effect:sell` — прибрати свою пастку в смітник; `+effect:upgrade` — апгрейд пастки за монети (міняє функцію).
- `+effect:manual_trigger` — гравець вручну спрацьовує пастку; `+cond:cooldown_ready` — пастка перезарядилась.
- `+cond:on_surface` — клітина має потрібну поверхню (підлога / стеля / стіна).
- `+ui:trap-tray` — лоток карток пасток із цінами; `+ui:waves-remain-bar` — смуга «скільки хвиль лишилось» з маркером.
- `+feature:trap-reskins` — косметичні рескіни пасток і міньйонів.
- `+card:manual-trap-cooldown`, `+card:princess-carry-escape`, `+card:trap-mount-surface` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Castle Doombad Classic](https://store.steampowered.com/app/2888470/Castle_Doombad_Classic/) — автоматичні й ручні («precision timing») пастки, 30+ пасток і міньйонів, 150+ апгрейдів, лут героїв, Baddie Bonus і ліміт слотів, 90 етапів, Roguevenge, керування мишею; скриншоти поверхів, драбин, лотка й HUD.
- [Wikipedia](https://en.wikipedia.org/wiki/Castle_Doombad) — Grumpyface Studios, Adult Swim (2014), автоматичні (trap doors) й ручні (spikes) пастки, міньйони, Free to Slay, ремейк.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/castle-doombad/review/) — маршрут героїв «нагору, схопити принцесу, вниз до виходу», списомети біля драбин бʼють униз, ніндзя оминають шипи, типи героїв.
- [GMA News: огляд](https://www.gmanetwork.com/news/scitech/content/346083/game-review-it-s-good-to-be-bad-in-castle-doombad/story) — Scream із криків принцеси, scream generators, монети за місію, ручні пастки з перезарядкою, медик і міньйон-бомба, ніндзя на стелі.
- [Destructoid: огляд](https://destructoid.com/?p=139187) — сітка поверхів, драбини у вікна й підкопи, щупальця зривають щити, Gold / Evilness Tokens / Doom Points, корона за рівень без дотику до принцеси.
- [castledoombad.com](https://www.castledoombad.com) — лінійка ігор, Castle Doombad 2 з кооперативом.

## Непевне
- (?) Що відбувається з принцесою, коли героя з нею вбито (повертається одразу чи падає на поверсі) — джерела не кажуть.
- (?) Точне правило «trap door» з Вікіпедії (скидає героя на нижчий поверх?) — описів механіки не знайшов.
- (?) Розподіл пасток за поверхнями й назва «тролль/слот-машина» — з оглядів одним реченням.
- (?) Смітник: продаж із поверненням чи просто прибирання; призначення токенів-черепів у HUD (Evilness Tokens?).
- (?) Кількість поверхів і клітин на поверсі; чи є зірки/корони в Classic — не перевірено.
