---
title: Swords & Soldiers
slug: swords-and-soldiers
aka: [Swords & Soldiers HD, Swords and Soldiers]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 2009
platforms: [Wii, PC, Mac, Linux, PS3, iOS, Android, 3DS, Wii U, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Swords_%26_Soldiers", best: true, note: "золото й мана, юніти самі марширують, заклинання, 3 фракції з різним джерелом мани, 30 місій, skirmish, split-screen"}
  - {kind: other, url: "https://www.pocketgamer.com/swords-and-soldiers/review/", note: "рецензія: зліва направо, кілька доріг угору/вниз, шахтарі, дослідження, вежі, рядок кнопок"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=swords+and+soldiers", note: "пошук; HD-версія"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=swords+and+soldiers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [round-currency, hp-damage, melee-vs-ranged, explode-area, status-effects, chase-greedy, move-auto, enemy-reached-base, ai-opponent, sequential-levels, level-unlock, level-select, mode-select, game-pause, end-screen, achievements-window, +lane-grid, +auto-march-units, +worker-economy, +research-unlock, +dual-currency, +spell-targeting, +faction-mana-source, +branching-lanes, +split-screen-versus]
proposes: ["+role:unit", "+role:base", "+role:building", "+trigger:produced", "+effect:produce", "+effect:research", "+effect:sacrifice", "+cond:in_zone", "+ui:build-bar", "+ui:mana-bar", "+window:faction-select", "+feature:local-versus", "+axis:field=lanes"]
author: opus
date: 2026-11-09
---

# Swords & Soldiers — RTS на одній лінії: юніти марширують самі, гравець — економіка, черга найму й заклинання

## Суть
Side-scrolling RTS, де поле — дорога зліва направо між двома базами. Гравець не веде юнітів: купив за золото — юніт сам іде до ворожої бази й бʼється з усім, що зустріне. Руки гравця — це наймання шахтарів (дохід), дослідження нових типів юнітів і заклинання за ману по будь-якій точці лінії. Три фракції (вікінги, ацтеки, китайці) відрізняються саме тим, як добувають ману.

## Поле і час
- Поле — 1D-смуга (вид збоку), прокрутка камерою вздовж; база гравця на одному кінці, ворожа — на іншому.
- Деякі місії мають розгалуження: дороги вгору або вниз, тобто кілька смуг (дерево шляхів) (?).
- Час — realtime; одночасний темп для обох сторін; пауза є (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| База | static (`+role:base`) | HP | точка найму; падіння = поразка/перемога |
| Шахтар (робітник) | ally | ціна в золоті | ходить між базою і золотою копальнею, приносить золото |
| Копальня золота | resource | — | джерело золота поруч з базою |
| Бойовий юніт | ally (`+role:unit`) | ціна, HP, шкода, швидкість, ближній/дальній | після найму марширує до ворожої бази, атакує першого зустрічного |
| «Божественний» юніт | ally | дорогий | сильний юніт, здатний знести цілий загін |
| Вежа | static (`+role:building`) | — | захисна будівля, купує час для контратаки |
| Ворожий юніт | enemy | ті самі параметри | дзеркальна поведінка: іде до бази гравця |
| Заклинання | projectile (`+role:card`) | ціна в мані | ціль — точка/юніт на лінії: лікування, блискавка, щит, отрута тощо |
| Будда (китайці) | static (`+role:building`) | HP | генерує ману, поки не зруйнований — треба захищати |
| Золото | resource | — | на юнітів, шахтарів, дослідження |
| Мана | resource | — | на заклинання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(buy, miner)` → ЯКЩО `has(gold, price)` → ТО `currency(-price)`, `spawn_at(miner, base)`.
- КОЛИ `reach(miner, mine)` → ТО `custom: «набирає золото й несе на базу»`; КОЛИ `reach(miner, base)` → ТО `currency(+n)`.
- КОЛИ `input(buy, unit)` → ЯКЩО `has(gold, price)` and `custom: «тип досліджено»` → ТО `currency(-price)`, `custom: «юніт стає в чергу виробництва»`; після готовності — `spawn_at(unit, base)` (?).
- КОЛИ `spawned(unit)` → ТО `move(unit, toward_enemy_base)` щотіку (без керування гравцем).
- КОЛИ `in_range(unit, enemy, range)` → ТО `custom: «зупиняється»`, `damage(n)` за перезарядкою; ближній бій — впритул, дальній — на відстані.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`; черга юнітів позаду продовжує марш.
- КОЛИ `input(research, unit_type)` → ЯКЩО `has(gold, price)` → ТО `currency(-price)`, `unlock(unit_type)`.
- КОЛИ `input(cast, spell, target)` → ЯКЩО `has(mana, cost)` → ТО `custom: «мана −cost»`, `heal(a, n)` / `damage(n)` / `set_state(a, s, dur)` / `stun(a, n)` за типом заклинання.
- КОЛИ `tick` → ЯКЩО `custom: «фракція отримує ману пасивно (вікінги з апгрейдом, китайці з Буддою)»` → ТО `custom: «мана +rate»`.
- КОЛИ `input(sacrifice, unit)` → ЯКЩО `custom: «фракція ацтеки»` → ТО `disappear_a`, `custom: «HP юніта → мана»`.
- КОЛИ `destroyed(buddha)` → ТО `custom: «китайці втрачають джерело мани»`.
- КОЛИ `reach(unit, enemy_base)` → ТО `damage(base, n)`.
- КОЛИ `destroyed(enemy_base)` → ТО `win`; КОЛИ `destroyed(own_base)` → ТО `lose`.
- КОЛИ `custom: «місія на виживання»` → ЯКЩО `timer(<=, 0)` and `custom: «база ціла»` → ТО `win` (?).
- Перемога: знести ворожу базу; в окремих місіях — вистояти під штурмом або прорватися обмеженим загоном · Поразка: втрата бази · Рахунок — немає (?).

## Керування і ввід
- Wii — вказівник Wii Remote; ПК — миша; тач — палець: кнопки найму й заклинань у постійному рядку вгорі екрана, заклинання цілиться кліком по лінії.
- Камера — прокрутка вздовж лінії (?).
- Керування юнітами нема в оригіналі (у Swords & Soldiers II вже можна вказувати, куди йти).

## Вікна, меню, HUD
- `main-menu` — кампанія, skirmish, мультиплеєр (split-screen), міні-ігри, налаштування.
- `+window:faction-select` / `level-select` — 3 кампанії по 10 місій.
- `game-screen` — лінія з двома базами; `+ui:build-bar` (кнопки юнітів/шахтарів/досліджень/заклинань з цінами), `coins` (золото), `+ui:mana-bar`, HP баз (`hp-bar`), `cooldown`-стан кнопок (?).
- `pause-menu` (?) · `end-screen` — перемога/поразка місії · `achievements-window` (досягнення є).
- Split-screen versus — два поля одне над одним (iPad/консолі).

## Фічі поза полем
- Кампанія з 30 місій (по 10 на фракцію), частина з обмеженим набором юнітів або таймером штурму.
- Skirmish проти AI, `+feature:local-versus` (split-screen), розблоковувані режими й міні-ігри, досягнення.
- Без онлайн-мультиплеєра.

## Варіації й родичі
- Swords & Soldiers II (2015): можна обирати місце бази й командувати рухом юнітів.
- У сімʼї: [plants-vs-zombies](plants-vs-zombies.md) (смуги + валюта на поле), [clash-royale](clash-royale.md) (юніти після висадки діють самі), [legion-td](legion-td.md) (робітники-економіка). Поза корпусом — жанр «lane battler» (Stick War, Age of War (?)).
- **Осі варіацій**: смуга — одна / з розгалуженнями · економіка — шахтарі / пасивний дохід · мана — купити / охороняти генератор / жертвувати юнітами · контроль — нуль / вказати напрям.

## Цікавинки для курсу
- 1D-бій: юніти в черзі зупиняються на першого ворога в дальності — 🌱.
- Робітник-економіка: шахтар ходить копальня ↔ база, кількість шахтарів = дохід — 📎.
- Дві валюти: золото на виробництво, мана на заклинання — 🌱.
- Асиметрія фракцій через різні джерела мани (апгрейд / генератор, що треба захищати / жертва HP) — 🥉.
- Заклинання по точці лінії з радіусом — 📎.

## Мапа на каталог
- Є: `round-currency` ↔ золото/мана · `hp-damage` · `melee-vs-ranged` · `explode-area` ↔ заклинання · `status-effects` ↔ отрута, щит · `chase-greedy` / `move-auto` ↔ марш до ворога · `enemy-reached-base` · `ai-opponent` · `sequential-levels`, `level-unlock`, `level-select` · `mode-select` · `game-pause` · `end-screen` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+auto-march-units` «Куплений юніт сам іде до ворожої бази» · entities/move · 🌱.
  - `+dual-currency` «Дві валюти на різні дії» · game-logic/economy · 🌱.
  - `+faction-mana-source` «Фракції з різними джерелами ресурсу» · game-logic/economy · 🥉.
  - `+spell-targeting` «Заклинання в точку з радіусом» · interface/input · 📎.
  - `+branching-lanes` «Смуга з розгалуженнями» · fields/topology · 📎.
  - `+split-screen-versus` «Два поля на одному екрані» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+role:unit` · `+role:base` · `+role:building`.
- `+trigger:produced` — юніт вийшов з черги виробництва.
- `+effect:produce` (поставити в чергу виробництва) · `+effect:research` (відкрити тип) · `+effect:sacrifice` (знищити свій юніт заради ресурсу).
- `+cond:in_zone`.
- `+ui:build-bar` · `+ui:mana-bar`.
- `+window:faction-select`.
- `+feature:local-versus`.
- `+axis:field=lanes`.

## Джерела
- ⭐ [Wikipedia: Swords & Soldiers](https://en.wikipedia.org/wiki/Swords_%26_Soldiers) — золото й мана, авто-марш юнітів, заклинання, цілі місій, фракції й джерела мани, 30 місій, skirmish, split-screen, сиквел.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/swords-and-soldiers/review/) — зліва направо, дороги вгору/вниз, шахтарі, дослідження, вежі, «божественні» юніти, рядок кнопок, обмеження юнітів у місіях.
- [Steam: пошук](https://store.steampowered.com/search/?term=swords+and+soldiers) · [YouTube: пошук](https://www.youtube.com/results?search_query=swords+and+soldiers+gameplay).

## Непевне
- (?) Списки юнітів і заклинань фракцій (Heal, Lightning, Shield, Poison Bomb, Snowstorm, Cage Trap…) — лише з пошукових сніпетів, по фракціях не розкладено.
- (?) Чи є черга виробництва з часом, чи юніт зʼявляється одразу; чи мають кнопки cooldown.
- (?) Як саме працюють розгалуження доріг — юніт обирає сам чи гравець.
- (?) Як вікінги отримують ману після апгрейду (пасивно?) і чи є мана в інших фракцій пасивно.
- (?) Пауза, рахунок/рейтинг місій.
