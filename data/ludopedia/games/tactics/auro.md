---
title: "Auro: A Monster-Bumping Adventure"
slug: auro
aka: [Auro]
family: tactics
also: [roguelike, thinky]
klass: avatar
axes:
  field: hex
  time: turn
  opponent: ai
  info: partial
  random: setup
  goal: score
year: 2014
platforms: [iOS, Android, PC]
links:
  - {kind: other, url: "https://theludite.com/2014/10/04/auro-doing-it-right/", best: true, note: "найповніший розбір: bump + оглушення, вода/лід/вогонь/вихори, 5+2 слоти заклять, power-тайли, лічильник очок, ранги"}
  - {kind: steam, url: "https://store.steampowered.com/app/459680/Auro_A_MonsterBumping_Adventure/", note: "9 заклять, суперницькі королівства, процедурні мапи, Dinofarm Games"}
  - {kind: other, url: "https://www.pocketgamer.com/auro/review/", note: "огляд 9/10: гекси, без звичайних атак, множник до ×4"}
  - {kind: other, url: "https://toucharcade.com/?p=164993", note: "огляд TouchArcade"}
  - {kind: other, url: "https://giantbomb.com/wiki/Games/Auro_A_Monster_Bumping_Adventure", note: "картка гри (Giant Bomb)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Auro+Monster+Bumping+Adventure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [push-object, environment-death, inertia-slide, timed-despawn, hp-damage, item-pickup, reach-exit, event-points, combo-multiplier, dungeon-generation, sequential-levels, rating-system, score-records, chase-player, telegraphed-intents, +knockback, +bump-stun, +hex-grid-render, +no-pass-move, +spell-cooldown-pickup, +random-loadout, +free-action, +decaying-kill-value, +ranked-ladder]
proposes: ["+effect:knockback", "+effect:cooldown", "+trigger:bumped", "+cond:cooldown_ready", "+role:power-tile", "+ui:kill-value", "+ui:spell-slots", "+ui:rank-badge", "+window:placement-match", "+feature:ranked-ladder", "+axis:attack:push-only"]
author: opus
date: 2026-11-09
---

# Auro — тактика без атак: штовхни монстра на гекс у воду, поки лічильник очок не згас

## Суть
Принц Auro на гексагональному острові-підземеллі не має звичайної атаки: базова дія — **bump**, удар, що зсуває монстра на один гекс і оглушує його на наступний хід. Вбити можна лише середовищем — вода, вогонь, вихори; лід дає ковзання. Над цим — 5 перезаряджуваних і 2 одноразові слоти заклять, що змінюють або розширюють bump. Бій детермінований (без кубиків), випадкові лише генерація острова й набір заклять, тому кожен хід — маленька задача «як виштовхати всіх у воду до того, як згасне очко».

## Поле і час
- Гексагональна сітка-острів серед води; видима область теж гексагональна (однакова дальність у всі боки) — частина мапи поза нею не видна.
- Покроково: хід гравця (рух на 1 гекс або bump, або закляття) → хід монстрів. **Пас заборонено** — щоходу треба рухатись.
- Закляття — «вільні дії»: монстри не ходять, лічильник очок не падає.
- Рівень = один острів з телепортом; телепорт веде на важчий острів; забіг = серія островів.
- Нові ділянки острова «будять» нових монстрів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Auro | player | HP, 5+2 слоти заклять | рух на сусідній гекс; рух у монстра = bump |
| Rat (щур) | enemy | — | підходить і бʼє поруч (?) |
| Troggle | enemy | — | кидається по прямій лінії |
| Lich | enemy | — | здебільшого стоїть на місці, атакує здалеку (?) |
| Летун (кажан) | enemy | літає | висить над водою — вода його не вбиває |
| Jelly (желе) | enemy | — | хто на нього наступив / впав — відскакує; може штовхнути Auro |
| Огр | enemy | важкий (?) | частину монстрів не зсунути — лише магією |
| Чаклунка-лисиця | enemy | дальність | кидає вогняні кулі |
| Вода | hazard | — | монстр у воді «пірнає» і зникає |
| Лід (крижина) | terrain | тане з часом | тимчасово вкриває воду; монстр ковзає по ній |
| Вогонь (слід) | hazard | — | палить монстра, що його перетнув; вбиває штовхнутого |
| Вихор | hazard | — | лишається після Leap; затягує монстра (?) |
| Power-тайл | pickup | — | зменшує cooldown усіх витрачених заклять |
| Телепорт | static | — | вихід на наступний острів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell)` → ТО `move(auro, dir)`, `counter(kill_value, −1)`.
- КОЛИ `input(move, dir)` → ЯКЩО `occupied(cell, enemy)` → ТО `push(enemy)` на 1 гекс, `stun(enemy, 1)`, `counter(kill_value, −1)`.
- КОЛИ `input(...)` → ЯКЩО `custom: «спроба пропустити хід»` → ТО `block` (пас заборонено).
- КОЛИ `enter(enemy, water)` → ЯКЩО `not state(enemy, flying)` → ТО `disappear_a`, `score(kill_value)`, `counter(kill_value, +1)` (до 4).
- КОЛИ `enter(enemy, fire)` → ТО `disappear_a`, `score(kill_value)`.
- КОЛИ `enter(enemy, ice)` → ТО `slide(enemy, dir)` до упору (?).
- КОЛИ `timer(every)` → ТО `custom: «крижина тане»`; `set_cell(ice, water)`.
- КОЛИ `push(enemy)` → ЯКЩО `occupied(cell_behind, enemy2)` → ТО `custom: «ланцюг поштовхів / зупинка»` (?).
- КОЛИ `enter(a, jelly)` → ТО `bounce(a)` (відскок від желе).
- КОЛИ `input(spell, target)` → ЯКЩО `custom: «слот не на cooldown»` → ТО ефект закляття; `custom: «вільна дія: монстри не ходять, kill_value не падає»`.
- Snowball: `input(spell)` → ТО `custom: «bump на відстані»` + `freeze(enemy, n)`.
- Rotisserie: `input(spell)` → ТО `rotate(adjacent_enemies, 60)` (?) + `set_state(enemy, burning)`.
- Fire Trap: `input(spell)` → ТО `set_cell(cells_around, fire)`.
- Floe: `input(spell)` → ТО `set_cell(water, ice)`.
- Leap: `input(spell, cell)` → ТО `teleport(auro, cell)`, `spawn_at(vortex, start)`.
- КОЛИ `contact(auro, power_tile)` → ТО `pickup`, `custom: «−1 cooldown усім витраченим закляттям»`.
- КОЛИ `turn_end(player)` → ЯКЩО `not state(enemy, stunned)` → ТО `custom: «монстр робить свій хід за власним патерном»`; `adjacent(enemy, auro)` → `damage(1)` (?).
- КОЛИ `custom: «хід без убивства»` → ТО `reset_combo` (множник/лічильник згасає).
- КОЛИ `hp_zero(auro)` → ТО `lose`.
- КОЛИ `counter(score, ≥, goal)` → ТО `win` (матч у ранговій драбині).
- КОЛИ `contact(auro, teleport)` → ТО `next_level` (важчий острів).
- Перемога: набрати цільові очки · Поразка: HP = 0 · Рахунок: кожне вбивство дає поточне значення лічильника (1…4), що падає з кожним рухом/bump і росте з кожним вбивством.

## Керування і ввід
- Тач / мишa: тап по сусідньому гексу — рух туди; тап по сусідньому монстрові — bump.
- Іконки заклять унизу: тап → підсвічені допустимі цілі → тап по цілі.
- Інформація про монстра — довгий тап / наведення (поведінка, наміри) (?).

## Вікна, меню, HUD
- `main-menu`: Грати (ранговий матч) · Довідка/онлайн-мануал → `help-window` · Налаштування → `settings-window`.
- `custom-window` «Placement match» — перший матч визначає стартовий ранг.
- `game-screen`: гексовий острів, `hp-bar`/серця Auro, `score` і цільові очки, лічильник «скільки дасть наступне вбивство» в кутку, панель 5+2 слотів заклять з `skill-bar`-cooldown, `tooltip` монстрів.
- `end-screen` — перемога/поразка матчу, зміна рангових очок.
- `custom-window` «Rank / kingdoms» — драбина рангів і суперницькі королівства (?).
- Діалоги монстрів пояснюють правила — `dialogue-window`/`toast` (?).
- Переходи: main-menu → матч (острови → телепорт → …) → end-screen → main-menu.

## Фічі поза полем
- `rank-tiers`: рангова драбина; перемоги додають очки, поразки віднімають, серії перемог дають прискорення; гра тяжіє тримати гравця на вищому з двох сусідніх рангів.
- Складність = ранг: вищий ранг — важчі комбінації монстрів (а не лише вищі цілі).
- Процедурні острови й випадковий набір 5 заклять з 9 (1 гарантоване «ультимативне»); набір не обирається.
- `tutorial` / онлайн-мануал; без донату, без сюжету.

## Варіації й родичі
- Родичі: Hoplite (один герой на гексах, детермінований бій, ворожі патерни), Into the Breach (поштовх як основна зброя, вбивство середовищем), Sokoban/push-slide (штовхання як дія), 100 Rogues (попередня гра Dinofarm), Michael Brough 868-HACK / Imbroglio (детерміновані мікро-роглайки).
- **Осі варіацій**: атака — шкода HP / лише поштовх / поштовх + середовище · пас — дозволено / заборонено · очки — за вбивство / за вбивство з затуханням і комбо · закляття — обрані / випадковий набір · перезаряд — за ходи / за підібрані тайли.

## Цікавинки для курсу
- Бій лише поштовхом: bump на 1 гекс + оглушення на хід, смерть — тільки від клітини — 📎 (мінімальна механіка, глибина з поля).
- Лід, що тане за таймером, і ковзання по ньому — 🌱.
- Лічильник цінності вбивства, що падає з кожною дією і росте з кожним вбивством — 🌱.
- Закляття як «вільні дії» і перезаряд через підібрані power-тайли (усім витраченим одразу) — 📎.
- Заборона пасу на гексовій сітці — 🌱 (і аналіз «змушених ходів»).
- Детермінованість + видимі патерни монстрів → можна написати пошук оптимального ходу — 🥇 (minimax/beam search по ходах).
- Рангова драбина з «липкістю» до вищого рангу — 🥉.

## Мапа на каталог
- Є: `push-object` (bump) · `environment-death` (вода, вогонь) · `inertia-slide` (лід) · `timed-despawn` (крижина тане) · `hp-damage` (HP Auro) · `item-pickup` (power-тайли) · `reach-exit` (телепорт) · `event-points` + `combo-multiplier` · `dungeon-generation` · `sequential-levels` · `rating-system` (ранги) · `score-records` · `chase-player` (монстри йдуть до Auro) · `telegraphed-intents` (?).
- **Нема** → пропозиції карток:
  - `+knockback` «Відкидання цілі ударом на N клітин» · entities/combat · 📎 — спільна з Into the Breach.
  - `+bump-stun` «Поштовх оглушує на хід» · entities/state · 🌱.
  - `+hex-grid-render` — гексова сітка (є в корпусі).
  - `+no-pass-move` «Пас заборонено, хід обовʼязковий» · entities/legality · 🌱.
  - `+spell-cooldown-pickup` «Cooldown зменшують підібрані тайли» · entities/state · 📎.
  - `+random-loadout` «Випадковий набір здібностей на забіг» · game-logic/difficulty · 🌱.
  - `+free-action` «Дія, після якої ворог не ходить» · game-logic/opponent · 🌱.
  - `+decaying-kill-value` «Цінність вбивства падає з кожною дією» · game-logic/score · 🌱.
  - `+ranked-ladder` «Рангова драбина з очками промоції» · interface/results · 🥉.

## Пропозиції до словників
- `+effect:knockback` — відкинути ціль від атакуючого на N (не `push`: не входимо в клітину).
- `+effect:cooldown` — поставити/зменшити перезаряд здібності; `+cond:cooldown_ready` — здібність готова.
- `+trigger:bumped` — сутність отримала поштовх (для ланцюгів).
- `+role:power-tile` — підбирач, що заряджає здібності (частковий `pickup`).
- `+ui:kill-value` — «скільки дасть наступне вбивство»; `+ui:spell-slots` — слоти здібностей з перезарядом; `+ui:rank-badge` — поточний ранг.
- `+window:placement-match` — кваліфікаційний матч для рангу.
- `+feature:ranked-ladder` — драбина рангів у одиночній грі.
- `+axis:attack:push-only` — атака лише переміщенням (Auro, частково Into the Breach).

## Джерела
- ⭐ [The Ludite: Auro: Doing It Right](https://theludite.com/2014/10/04/auro-doing-it-right/) — детальний розбір правил: bump, вода/лід/вогонь/вихори, слоти, закляття з назвами, монстри, очки, ранги, детермінованість.
- [Steam](https://store.steampowered.com/app/459680/Auro_A_MonsterBumping_Adventure/) — 9 заклять, суперницькі королівства, процедурні мапи, розробник Dinofarm Games, реліз на Steam 13.04.2016.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/auro/review/) — гекси, жодних звичайних атак, множник до 4, вороги (щури, кажани, огри, чаклунки з фаєрболами).
- [TouchArcade](https://toucharcade.com/?p=164993) · [Giant Bomb](https://giantbomb.com/wiki/Games/Auro_A_Monster_Bumping_Adventure) — бачені в пошуку, не відкриті.
- YouTube: пошук «Auro Monster Bumping Adventure gameplay».

## Непевне
- (?) Рік: розбір The Ludite (жовтень 2014) описує вже вийдену iOS-версію; на Steam — 2016; у черзі стоїть 2015. Android — з памʼяті.
- (?) Офіційний сайт dinofarmgames.com/auro тепер переадресовує на сторонній сайт — у шапку не покладено.
- (?) Поведінка щурів, ліча, огра й чаклунки (як саме атакують, скільки шкоди) — джерела називають їх, але без правил.
- (?) Ланцюг поштовхів (монстр штовхає монстра) і що робить вихор — не підтверджено.
- (?) Ковзання по льоду «до упору» чи на 1 гекс — не підтверджено.
- (?) Rotisserie обертає сусідів на 60° чи на інший кут — з опису «rotates adjacent monsters».
- (?) Решта заклять (крім Snowball, Rotisserie, Fire Trap, Floe, Leap) — назви невідомі.
