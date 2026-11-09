---
title: The Battle Cats
slug: the-battle-cats
aka: [Battle Cats, "Nyanko Daisensou", にゃんこ大戦争, "The Battle Cats POP!", "Unite! Battle Cats"]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2012
platforms: [iOS, Android, 3DS (POP!), Switch (Unite!)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Battle_Cats", best: true, note: "2D-поле між двома базами, трейти ворогів, ролі юнітів, прокачка XP/Catseye/NP, рідкості, глави й режими, гача"}
  - {kind: other, url: "https://www.bluestacks.com/blog/game-guides/the-battle-cats/tbc-beginners-guide-en.html", note: "гайд новачка: висадка за гроші, гаманець, кулдаун гармати, HP баз, скарби, глави"}
  - {kind: fandom, url: "https://battlecats.miraheze.org/wiki/Knockback", note: "Battle Cats Wiki (Miraheze): knockback, single/area/long distance/omni strike"}
  - {kind: fandom, url: "https://battlecats.miraheze.org/wiki/Worker_Cat", note: "Worker Cat: макс. рівень 8, ~170¢/с на рівні 1, +~5% за рівень"}
  - {kind: fandom, url: "https://battlecats.miraheze.org/wiki/Cat_Cannon", note: "гармата: 10 поділок, мін. 31,67 с, дальність 6000, голови гармати"}
  - {kind: fandom, url: "https://battlecats.miraheze.org/wiki/Cat_(Normal_Cat)", note: "приклад статів: HP 100, 3 knockback, швидкість 10, дальність 140, single, 50¢"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=the+battle+cats+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [round-currency, in-round-upgrades, placement-cooldown, enemy-reached-base, hp-damage, melee-vs-ranged, explode-area, status-effects, spawn-schedule, move-auto, speed-per-type, shoot-cooldown, tower-range, sequential-levels, level-select, level-unlock, world-map, shop-window, unit-xp-skills, save-progress, game-pause, end-screen, +lane-grid, +auto-march-units, +worker-economy, +base-hp-duel, +base-cannon, +hp-threshold-knockback, +single-vs-area, +long-distance-blindspot, +omni-strike, +trait-counters, +base-damage-triggers, +loadout-select, +gacha-units, +unit-evolution, +treasure-buffs, +timed-score-rewards, +stage-energy, +cat-combos]
proposes: ["+trigger:hp_threshold", "+trigger:charge_full", "+cond:trait", "+cond:base_hp", "+effect:knockback", "+effect:wave_attack", "+effect:deploy", "+role:base", "+role:unit", "+ui:unit-deploy-bar", "+ui:wallet", "+ui:cannon-charge", "+window:loadout-select", "+window:gacha-window", "+feature:gacha", "+feature:treasures", "+card:hp-threshold-knockback", "+card:base-cannon"]
author: opus
date: 2026-11-09
---

# The Battle Cats — дуель двох баз на одній лінії: кнопки з кулдауном випускають котів, гаманець росте робітником

## Суть
Між базою котів (праворуч (?)) і ворожою базою — одна горизонтальна лінія. Гравець тапає по іконках юнітів: кожен коштує гроші й має **кулдаун**, після висадки марширує сам і б'є першого ворога в своїй **дальності**. Гроші течуть автоматично; **Worker Cat** у бою прокачується (до рівня 8) і збільшує швидкість доходу та гаманець. Заряджена **гармата бази** б'є хвилею по всій лінії. Перемога — знести HP ворожої бази, поразка — втратити свою.

## Поле і час
- Поле — одновимірна лінія (`field: 1d`) з базами на краях; координата — відстань (одиниці дальності: у кота 140, гармата дістає 6000).
- Real-time: тіки кадрів; атаки мають foreswing/backswing і частоту; knockback триває кадри.
- Ворогів спавнить сценарій стадії: за часом і за порогами HP ворожої бази — пошкодження бази часто викликає сильніших ворогів.
- Камера — горизонтальна прокрутка/зум; уся лінія видима зі скролом (?).
- Інформація повна в бою (видно всіх на лінії); випадковість — у шансах здібностей (knockback, freeze, crit) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| База котів | static (`+role:base`) | HP | падіння = поразка; з неї виходять юніти й б'є гармата |
| Ворожа база | static (`+role:base`) | HP | падіння = перемога; спавнить ворогів за сценарієм |
| Кіт-юніт | ally (`+role:unit`) | ціна, кулдаун, HP, кількість knockback, швидкість, сила, дальність, тип атаки, трейт-контри | після висадки йде до ворожої бази; зупиняється й б'є, коли ціль у дальності |
| Тип атаки Single | — | — | бʼє найближчого ворога в дальності |
| Тип атаки Area | — | — | б'є всіх ворогів у дальності |
| Long Distance | — | мін. і макс. ефективна дальність | не дістає близьких; бʼє далі за «стоячу» дальність |
| Omni Strike | — | мін. дальність ≤ 0 | бʼє і попереду, і позаду себе |
| Ворог | enemy | HP, knockback, трейт (Red, Floating, Black/Dark, Metal, Angel, Alien, Zombie, Aku, Relic, Traitless; підтрейти Behemoth, Colossus, Sage) | іде до бази котів; дзеркальні правила дальності |
| Бос | boss | — | при появі — ударна хвиля (shockwave), відкидає всіх котів далеко |
| Worker Cat | resource | рівень 1–8 | у бою: прокачка за гроші → більше ¢/с і більший гаманець |
| Гроші (¢) | resource | ~170¢/с на рівні 1 (+~5%/рівень) | плата за висадку й прокачку робітника; вороги лишають гроші при загибелі (крім Dojo) |
| Гармата бази (Cat Cannon) | tower | 10 поділок заряду, мін. 31,67 с, дальність 6000 | після заряду — постріл: хвиля по лінії, легкий knockback |
| Голова гармати | tower | тип | Slow Beam, Iron Wall (стіна-юніт), Thunderbolt (freeze), Waterblast (проти Metal), Holy Blast (проти Zombie), Breakerblast (ламає бар'єри), Curseblast |
| Залізна стіна | ally | HP, тривалість | не атакує, займає місце в ліміті котів, тримає ворогів |
| Скарб (Treasure) | pickup | бронза/срібло/золото | поза боєм; пасивні бонуси (гроші, гармата, проти трейтів) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `currency(+rate)` за рівнем Worker Cat; ЯКЩО `custom: «гаманець повний»` → ТО `block`.
- КОЛИ `input(worker_up)` → ЯКЩО `has(money, cost)` and `level(<, 8)` → ТО `currency(−cost)`, `custom: «рівень робітника +1: дохід ~+5%, більший гаманець»`; ціна = базова × поточний рівень.
- КОЛИ `input(deploy, cat)` → ЯКЩО `has(money, cost)` and `custom: «кулдаун іконки скінчився»` and `custom: «ліміт котів на полі не досягнуто»` (?) → ТО `currency(−cost)`, `spawn_at(cat, cat_base)`, `timer(start, recharge)`.
- КОЛИ `spawned(cat)` → ТО `move(cat, toward_enemy_base)` щотіку зі швидкістю юніта.
- КОЛИ `in_range(cat, enemy, range)` → ТО `custom: «зупиняється»`, атака з частотою юніта: Single — `damage(nearest)`, Area — `damage(all_in_range)`.
- КОЛИ `custom: «Long Distance»` → ЯКЩО `custom: «ворог ближче за мін. ефективну дальність»` → ТО `block` — сліпа зона.
- КОЛИ `custom: «Omni Strike»` → ТО `custom: «удар і по ворогах позаду в межах дальності»`.
- КОЛИ `custom: «HP юніта перетнуло поріг (HP / кількість knockback)»` → ТО `custom: «knockback: відштовхнути назад, коротка невразливість/без хітбоксу»`; останній поріг = `disappear_a`.
- КОЛИ `custom: «удар здібністю Knockback»` → ЯКЩО `custom: «ціль має відповідний трейт»` and `prob(p)` → ТО `custom: «knockback цілі»`; %HP-knockback має пріоритет.
- КОЛИ `custom: «атака кота-контри по ворогу його трейту»` → ТО `custom: «більше шкоди і менше отриманої (Strong / Massive / Resistant)»`; інші здібності — `freeze`, `speed(×k)` (slow), `custom: «weaken, curse»` з шансом.
- КОЛИ `counter(cannon_charge, ≥, 10)` → ТО кнопка «Fire!!» активна; КОЛИ `input(fire)` → ТО `custom: «ефект голови гармати: хвиля / сповільнення / стіна / блискавка…»`, `counter(cannon_charge, =0)`.
- КОЛИ `spawned(boss)` → ТО `custom: «shockwave: усі коти відкинуті далеко»`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_b`, `currency(+drop)` (у Catclaw Dojo — 0).
- КОЛИ `custom: «HP ворожої бази нижче порогу стадії»` → ТО `spawn_at(enemies, enemy_base)` — посилення.
- КОЛИ `schedule(stage_spawns)` → ТО `spawn_at(enemy, enemy_base)`.
- КОЛИ `reach(cat, enemy_base)` → ТО `damage(enemy_base, n)`; КОЛИ `reach(enemy, cat_base)` → ТО `damage(cat_base, n)`.
- КОЛИ `hp_zero(enemy_base)` → ТО `win`, `give(XP, items)`; ЯКЩО `prob(p)` → ТО `give(treasure)`.
- КОЛИ `hp_zero(cat_base)` → ТО `lose`.
- КОЛИ `custom: «Into the Future: швидкий прохід»` → ТО `custom: «Timed Score Rewards — краща нагорода за час»`.
- КОЛИ `custom: «Underground Labyrinth»` → ТО `custom: «використаних юнітів не можна прибрати з загону, поки не стануть trapped»`.
- Перемога: зруйнувати ворожу базу · Поразка: зруйновано базу котів · Рахунок: у Dojo — шкода/очки рейтингу; у стадіях — нема.

## Керування і ввід
- Тач: ряд іконок юнітів унизу (2 сторінки по 5 (?)), tap — висадка; сіра іконка = кулдаун або бракує грошей.
- Кнопка Worker Cat (рівень, ціна) і кнопка гармати «Fire!!» з індикатором заряду.
- Свайп/скрол камери вздовж лінії, пауза, прискорення (?).
- Поза боєм: екрани загону (Equip), прокачки, гачі, вибору стадії.

## Вікна, меню, HUD
- `main-menu` (база котів): Battle → `world-map` / `level-select` глав (Empire of Cats, Into the Future, Cats of the Cosmos, Aku Realms, Legend stages, події); Upgrade; Cat Capsule; Equip.
- `+window:loadout-select` (Equip) — до 10 юнітів у загоні на бій (?), збереження наборів.
- `upgrade-window` — рівні котів за XP, Catseyes, таланти за NP, базові апгрейди (гармата, робітник).
- `+window:gacha-window` (Cat Capsule) — квитки, рідкісні квитки, Cat Food; результати.
- `shop-window` — товари за Cat Food.
- `game-screen`: лінія з базами, HP обох баз, `+ui:wallet` (гроші / макс.), `+ui:unit-deploy-bar` з цінами й кулдаунами, `+ui:cannon-charge`, кнопка робітника, `pause-button`.
- `pause-menu`; `end-screen`: перемога (XP, предмети, скарб) / поразка; `+window:treasure-window` (?) — зібрані скарби глави.

## Фічі поза полем
- Прогресія юнітів: XP і Catseyes → рівні (капи 60…20, для колабів 1), еволюція на рівні 10, True Form за Catfruit, Ultra Form, таланти й ультраталанти за NP.
- Рідкості: Normal, Special, Rare, Super Rare, Uber Super Rare, Legend Rare; ексклюзивні юніти — лише з гачі.
- Скарби бронза/срібло/золото як пасивні бафи глави; Treasure Radar гарантує скарб.
- Режими: сюжетні глави по 48 стадій, Stories of Legend (49 підглав), Uncanny/Zero Legends, Catclaw Dojo (рейтинг, вороги без грошей), Underground Labyrinth (100 стадій), події й колаби.
- Енергія на вхід у стадію (?); комбо котів (Cat Combos) дають бонуси, зокрема до робітника.

## Варіації й родичі
- У корпусі: [swords-and-soldiers](swords-and-soldiers.md) (лінія, бази, юніти марширують самі), [plants-vs-zombies](plants-vs-zombies.md) (кулдаун висадки, валюта, що тече сама), [clash-royale](clash-royale.md) (висадка за ресурсом, бази-вежі, але дві смуги й колода), [random-dice](random-dice.md), [legion-td](legion-td.md).
- [age-of-war-stick-war](age-of-war-stick-war.md) — той самий «tug of war» на одній лінії (Age of War, Stick War); поза корпусом — Cartoon Wars.
- Осі варіацій:
  - **економіка**: дохід за часом + апгрейд робітника в бою (Battle Cats) / шахтарі ходять до копальні (Swords & Soldiers) / ресурс, що росте до стелі (Clash Royale);
  - **висадка**: колода і рука (CR) / фіксований загін з кулдауном на іконку (Battle Cats, PvZ);
  - **відкидання**: нема / за порогами HP — N knockback на юніт (Battle Cats) / здібність з шансом;
  - **дальність**: ближній/дальній / + мін. дальність (Long Distance) / + удар назад (Omni Strike).

## Цікавинки для курсу
- Лінія 1D з дальностями: хто зупиняється й кого б'є (найближчий / усі в дальності) — 🌱; з Long Distance і Omni Strike — 📎.
- Knockback за порогами HP (HP/N) з короткою невразливістю — 📎.
- Економіка: дохід/с, стеля гаманця, апгрейд робітника з ціною «база × рівень» — 🌱.
- Кулдаун на кожну іконку юніта + ціна — 🌱.
- Заряд гармати бази (10 поділок) і різні голови гармати — 📎.
- Трейти й контри (сильніший/стійкіший проти Red, Metal…) як матриця множників — 🥉.
- Спавн ворогів за порогами HP ворожої бази (сценарій стадії) — 📎.

## Мапа на каталог
- Є: `round-currency` ↔ гроші в бою · `in-round-upgrades` ↔ Worker Cat · `placement-cooldown` ↔ кулдаун іконки · `enemy-reached-base` · `hp-damage` · `melee-vs-ranged` · `explode-area` ↔ Area/хвиля · `status-effects` ↔ freeze/slow/weaken/curse · `spawn-schedule` · `move-auto` · `speed-per-type` · `shoot-cooldown` ↔ частота атаки · `tower-range` ↔ дальність · `sequential-levels` + `level-select` + `level-unlock` + `world-map` · `shop-window` · `unit-xp-skills` · `save-progress` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+auto-march-units`, `+worker-economy` (з Swords & Soldiers), `+loadout-select` (з PvZ).
  - `+base-hp-duel` «Дві бази з HP на краях лінії» · game-logic/win · 🌱.
  - `+base-cannon` «Заряджувана гармата бази» · entities/combat · 📎 · слоти {bars: 10, head}.
  - `+hp-threshold-knockback` «Відкидання за порогами HP» · entities/combat · 📎 · слот {knockbacks}.
  - `+single-vs-area` «Найближчий проти всіх у дальності» · entities/combat · 🌱.
  - `+long-distance-blindspot` «Мінімальна дальність — сліпа зона» · entities/combat · 🌱.
  - `+omni-strike` «Удар вперед і назад» · entities/combat · 🌱.
  - `+trait-counters` «Трейти ворогів і контр-юніти» · entities/combat · 🥉.
  - `+base-damage-triggers` «Спавн за порогом HP ворожої бази» · entities/spawn · 🌱.
  - `+gacha-units`, `+unit-evolution`, `+treasure-buffs`, `+timed-score-rewards`, `+stage-energy`, `+cat-combos`.

## Пропозиції до словників
- `+trigger:hp_threshold(a, k)` — HP перетнуло k-й поріг (knockback, фази боса, спавн за HP бази); `+trigger:charge_full(x)` — заряд (гармата) повний.
- `+cond:trait(a, t)` — у цілі трейт; `+cond:base_hp(op, n)` — HP бази порівняно з порогом.
- `+effect:knockback(a, dist)` — відкинути назад по лінії; `+effect:wave_attack` — хвиля, що біжить по лінії; `+effect:deploy(unit)` — висадити з кнопки (ціна + кулдаун).
- `+role:base` — база з HP на краю лінії; `+role:unit` — юніт, що діє сам після висадки.
- `+ui:unit-deploy-bar` — іконки з ціною й кулдауном; `+ui:wallet` — гроші / макс.; `+ui:cannon-charge` — заряд гармати.
- `+window:loadout-select` · `+window:gacha-window`; прокачку юнітів показую наявним ⏳ `upgrade-window`.
- `+feature:gacha` — капсули за квитки/валюту; `+feature:treasures` — пасивні бафи за зібрані скарби.
- `+card:hp-threshold-knockback`, `+card:base-cannon`.

## Джерела
- ⭐ [Wikipedia: The Battle Cats](https://en.wikipedia.org/wiki/The_Battle_Cats) — бази, ролі юнітів, трейти й підтрейти, контри (Axe Cat проти Red), прокачка, рідкості, глави й режими, Dojo без грошей, Labyrinth, гача.
- [BlueStacks: гайд новачка](https://www.bluestacks.com/blog/game-guides/the-battle-cats/tbc-beginners-guide-en.html) — висадка за гроші, гаманець, кулдаун гармати, HP баз, спавн від шкоди базі, скарби, глави по 48 стадій, Timed Score Rewards.
- [Battle Cats Wiki: Knockback](https://battlecats.miraheze.org/wiki/Knockback) — knockback за %HP і здібністю, невразливість у кадрах, Single/Area/Long Distance/Omni Strike.
- [Battle Cats Wiki: Worker Cat](https://battlecats.miraheze.org/wiki/Worker_Cat) — макс. рівень 8, ~170¢/с, +~5%/рівень, формула ціни.
- [Battle Cats Wiki: Cat Cannon](https://battlecats.miraheze.org/wiki/Cat_Cannon) — 10 поділок, мін. 31,67 с, дальність 6000, голови гармати.
- [Battle Cats Wiki: Cat](https://battlecats.miraheze.org/wiki/Cat_(Normal_Cat)) — приклад статів юніта.
- YouTube: пошук «the battle cats gameplay».

## Непевне
- (?) З якого боку база котів (праворуч) і розмір загону (10 слотів, 2 ряди по 5) — з памʼяті.
- (?) Ліміт котів на полі й ліміт за вартістю — не перевірено.
- (?) Енергія на вхід у стадію — Wikipedia згадує систему стаміни лише у відгуку на POP!.
- (?) Прискорення бою (speed-up) і шанс критичного удару — з памʼяті.
- (?) Значення гаманця за рівнями робітника — у джерелах немає.
