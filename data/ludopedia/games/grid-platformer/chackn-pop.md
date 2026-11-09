---
title: Chack'n Pop
slug: chackn-pop
aka: [ちゃっくんぽっぷ, チャックンポップ, "Chack'n Chack"]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1984
platforms: [arcade, MZ-2000, PC-8801, X1, MSX, FM-7, PC-6001mkII, Famicom, SG-1000, IBM JX, Wii VC, 3DS VC, Arcade Archives (PS4, Switch)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chack%27n_Pop", best: true, note: "підлога і стеля, гранати вліво/вправо, дим убиває героя, серця в клітках відкривають стіни, Mighta з каменем — таймер"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ちゃっくんぽっぷ", note: "деталі: стрибок, ромб диму, яйця за кольором, 4 види Monsta, лід, рухомі блоки, вода, фрукти, Super Heart, бонуси 20000/5000"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chack%27n+Pop+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, bomb-fuse, explode-area, environment-death, touch-death, player-death, destructible-blocks, enemy-patrol, chase-player, visited-trail, temporary-modes, speed-per-type, item-pickup, time-out, reach-exit, event-points, sequential-levels, hot-seat, game-screen, +egg-hatch-timer, +sealing-exit-timer, +ceiling-walk, +self-damage-blast, +one-bomb-limit, +freed-heart-opens-block, +multi-kill-fruit, +pacifist-bonus, +flee-from-bomb, +water-release, +crush-moving-block, +leftover-enemies-carry-over]
proposes: ["+trigger:multi_kill", "+cond:feet_on_floor", "+effect:stick_ceiling", "+effect:release_water", "+card:ceiling-walk", "+card:self-damage-blast", "+card:pacifist-bonus", "+card:multi-kill-fruit"]
author: opus
date: 2026-11-09
---

# Chack'n Pop — жовтий Chack'n ходить по підлозі й по стелі, кидає гранати, дим яких убиває і його самого, і визволяє серця, що відчиняють дорогу до виходу

## Суть
Однокранова аркада Taito: лабіринт з блоків, у ньому серця в клітках, яйця, з яких вилуплюються Monsta, і вихід угорі праворуч. Chack'n ходить і по підлозі, і по стелі (по стінах — ні) та котить гранату вліво чи вправо; граната вибухає хмарою диму ромбом, яка вбиває Monsta, ламає клітки й лід — і самого героя. Визволене серце летить угору й руйнує один блок на шляху до виходу. Таймер — Mighta, що котить камінь по верху екрана й урешті замуровує вихід.

## Поле і час
- Один екран-лабіринт з плиток-блоків; рух піксельний (?), але блоки, клітки й дим вирівняні по сітці — тому `square` з (?).
- Дві «опори»: підлога знизу і стеля зверху; стрибнув під стелю — прилип і ходиш догори ногами.
- Real-time; час раунду показує Mighta на верхньому краї (зліва → праворуч).
- Дим поширюється ромбом (манхеттенська відстань), стіни його обрізають; два перекриті вибухи — трохи далі.
- Вода (з розбитих пляшок) стікає вниз і стоїть калюжею; у ній можна плавати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Chack'n | player | життя; стан Super | ходить по підлозі й стелі; стрибок; кидає гранату вліво/вправо; дим — смерть |
| Граната | projectile | запал | котиться в бік кнопки, вибухає димом; одночасно лише одна (нова — коли дим розвіявся); дотик безпечний |
| Дим | hazard | ромб; час існування | убиває Chack'n і Monsta; ламає клітки, лід, яйця, пляшки; крізь лід проходить |
| Яйце | spawner | колір блакитний → жовтий → пурпуровий | нерухоме; пурпурове падає й вилуплює Monsta; дим знищує |
| Monsta-патрульний | enemy | — | блукає звичними маршрутами |
| Monsta-втікач (Nigenige) | enemy | — | біля гранати тікає в протилежний бік |
| Monsta-переслідувач (Oikake) | enemy | — | іде слідом Chack'n, гранати ігнорує |
| Злий Monsta | enemy | червоний, з другого кола | коли Monsta мало, один стає швидким переслідувачем по пройденому шляху (не біля виходу) |
| Клітка із серцем | container | — | дим ламає → серце летить угору |
| Серце | pickup | — | вилітаючи, руйнує один блок, що закриває шлях |
| Блок | static | — | закриває дорогу до виходу; гранатою не ламається |
| Крижаний блок | static | — | гранатою ламається; дим проходить крізь нього |
| Рухомий блок | object | — | розчавлює Chack'n або Monsta; не ламається |
| Пляшка з водою | container | — | дим розбиває → вода стікає вниз |
| Вода | terrain | — | Chack'n плаває; граната у воді вибухає без диму |
| Mighta | neutral | непереможний | іде по верху зліва направо; дійшов — новий Mighta штовхає каміння |
| Камені Mighta | object | — | повністю закрили вихід — програш раунду |
| Вихід | static | угорі праворуч | дійти — раунд пройдено |
| Фрукт (червоне яблуко, вишня, полуниця…) | pickup | цінність за кількістю вбитих | з'являється, коли граната вбила кількох Monsta разом |
| Синє яблуко | pickup | — | Chack'n повільнішає |
| Жовте яблуко | pickup | — | +1 життя |
| Super Heart | pickup | — | замість фрукта на певних номерах кидка; дає стан Super |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(chackn, dir)` — по підлозі або по стелі; стіною вгору не йде.
- КОЛИ `input(up)` → ЯКЩО `custom: «обидві ноги на підлозі»` → ТО `custom: «стрибок на висоту тіла»`; одна нога — на половину.
- КОЛИ `custom: «у стрибку над головою стеля»` → ТО `set_state(chackn, on_ceiling)` — далі ходить по стелі.
- КОЛИ `tick` → ЯКЩО `not supported(chackn)` → ТО `fall(chackn)`.
- КОЛИ `input(bomb_left|bomb_right)` → ЯКЩО `count(bomb, ==, 0)` і `count(smoke, ==, 0)` → ТО `spawn(bomb, side)`, `custom: «котиться в бік кнопки»`.
- КОЛИ `timer(fuse)` → ЯКЩО `not occupied(here, water)` → ТО `explode(diamond, r, smoke)`; у воді — `custom: «вибух без диму»`.
- КОЛИ `contact(chackn, smoke)` → ЯКЩО `not state(chackn, super)` → ТО `lives(-1)`, `restart` (?).
- КОЛИ `contact(monsta, smoke)` → ТО `disappear(monsta)`, `score(n)`.
- КОЛИ `contact(smoke, egg|cage|ice|bottle)` → ТО `disappear` — яйце, клітка, лід, пляшка руйнуються.
- КОЛИ `destroyed(cage)` → ТО `spawn(heart)`, `custom: «серце летить угору й руйнує один блок шляху»`.
- КОЛИ `destroyed(bottle)` → ТО `custom: «вода стікає вниз і стає калюжею»`.
- КОЛИ `timer(hatch)` → ТО `set_state(egg, next_color)`; ЯКЩО `state(egg, magenta)` → ТО `fall(egg)`, `transform(egg, monsta)`.
- КОЛИ `in_range(nigenige, bomb, n)` → ТО `custom: «тікає від гранати»`.
- КОЛИ `tick` → ТО `custom: «Oikake йде слідом Chack'n»`.
- КОЛИ `counter(monsta_left, <=, n)` → ЯКЩО `level(>=, loop2)` і `custom: «кандидат не біля виходу»` → ТО `transform(monsta, angry)`, `speed(monsta, +1)`.
- КОЛИ `contact(chackn, monsta)` → ЯКЩО `state(chackn, super)` → ТО `disappear(monsta)`; інакше `lives(-1)` (?).
- КОЛИ `contact(moving_block, chackn|monsta)` → ТО `custom: «розчавлено»` — Chack'n втрачає життя, Monsta зникає.
- КОЛИ `custom: «одна граната вбила ≥ 2 Monsta»` → ТО `spawn(fruit)` (дорожчий за більше вбитих); ЯКЩО `custom: «певний номер кидка від початку раунду»` → ТО `spawn(super_heart)` замість фрукта.
- КОЛИ `picked(chackn, super_heart)` → ТО `set_state(chackn, super, dur)` — швидше, стрибок з будь-якого положення, таран Monsta, імунітет до диму.
- КОЛИ `picked(chackn, yellow_apple)` → ТО `lives(+1)`; КОЛИ `picked(chackn, blue_apple)` → ТО `speed(chackn, -1)`.
- КОЛИ `reach(mighta, right_edge)` → ТО `spawn_at(mighta, left_edge)`, `custom: «новий Mighta штовхає каміння»`.
- КОЛИ `custom: «каміння повністю закрило вихід»` → ТО `lives(-1)`.
- КОЛИ `reach(chackn, exit)` → ТО `next_level`.
- КОЛИ `level_end` → ЯКЩО `counter(monsta_killed, ==, 0)` → ТО `score(20000)`, `lives(+1)`.
- КОЛИ `level_end` → ЯКЩО `custom: «знищено всіх вилуплених Monsta і жодного яйця»` → ТО `score(5000)`.
- КОЛИ `level_end` → ЯКЩО `custom: «не всіх Monsta знищено»` → ТО `custom: «наступний раунд — більше Monsta»`.
- Перемога раунду: дійти до виходу · Поразка: дим, Monsta (?), рухомий блок, вихід замурований · Рахунок: Monsta, фрукти, бонуси «нікого» / «усіх вилуплених без яєць».

## Керування і ввід
- 8-позиційний джойстик: ліворуч/праворуч — хід, угору — стрибок.
- Дві кнопки: граната вліво і граната вправо.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `game-screen`: лабіринт; угорі — Mighta з каменем як таймер; рахунок і життя (?).
- `attract-demo` і таблиця рекордів — як в аркадах Taito того часу (?).
- `end-screen` / game over (?).

## Фічі поза полем
- Аркада: 2 гравці по черзі; кола раундів (злі Monsta з другого кола).
- Перевидання: i-appli (2003), Wii VC (2008), 3DS VC (2013), Arcade Archives PS4/Switch (2022), Taito Egret II Mini.

## Варіації й родичі
- Походження: «Chack'n Chack» Хіросі Сакаї для Hitachi Basic Master Level 3 (1983) → аркада Taito.
- Chack'n і Monsta живуть далі в Bubble Bobble (Monsta — вороги), Bubble Symphony, Puzzle Bobble 2, Pop'n Pop.
- Родичі: [space-panic](space-panic.md) (пастки для ворогів у одноекранному лабіринті), Bomberman (`maze-arcade/bomberman`: бомба із запалом, вибух шкодить і собі), [that-gravity-glow](that-gravity-glow.md) (зміна «низу»).
- Осі варіацій: **по яких поверхнях ходить герой** (підлога / підлога і стеля / будь-яка, як у гравітаційних іграх); **форма вибуху** (хрест Bomberman / ромб диму / радіус); **таймер** (лічильник / персонаж, що замуровує вихід).

## Цікавинки для курсу
- Ходьба по стелі після стрибка під неї: два стани опори на одній сітці — 📎.
- Дим ромбом з обрізанням стінами і посиленням перекриття — 🥉 (BFS на відстань r з перешкодами).
- Одна граната на екрані, поки дим не розвіявся — 🌱.
- Серце з клітки руйнує блок шляху — ланцюг «зламав клітку → відкрився вихід» — 📎.
- Яйця з таймером кольору → вилуплення; Monsta-втікач і Monsta-слідопит по пройденому шляху — 🥉.
- Бонус «пацифіста» (нікого не вбив — 20000 і життя) проти бонусу «всіх» — 🌱.
- Mighta як фізичний таймер: камені поступово замуровують вихід — 📎.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `bomb-fuse` (одна граната, запал) · `explode-area` (ромб) · `environment-death` (дим, розчавлення) · `touch-death` · `player-death` · `destructible-blocks` (лід, клітки, пляшки) · `enemy-patrol` · `chase-player` + `visited-trail` (Oikake по сліду) · `temporary-modes` (Super Chack'n) · `speed-per-type` · `item-pickup` · `time-out` (Mighta) · `reach-exit` · `event-points` · `sequential-levels` · `hot-seat` (2 гравці по черзі) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+egg-hatch-timer` «Яйце змінює колір і вилуплює ворога; знищене — ворога нема» · entities/spawn · 📎 (`spawner-entity` — генератор без ліку, тут — одноразово).
  - `+sealing-exit-timer` «Таймер-персонаж поступово замуровує вихід» · game-logic/lose · 📎 (`timeout-punisher` спавнить ворогів — не те).
  - `+ceiling-walk` «Ходьба по стелі» · entities/move · 📎.
  - `+self-damage-blast` «Власний вибух шкодить гравцеві» · entities/combat · 🌱.
  - `+one-bomb-limit` «Нова бомба лише після зникнення диму» · entities/combat · 🌱 (родич слота max_bombs у `bomb-fuse`).
  - `+freed-heart-opens-block` «Визволена сутність руйнує перешкоду» · entities/interact · 📎.
  - `+multi-kill-fruit` «Бонус-предмет за кількох ворогів одним вибухом, дорожчий за більше вбитих» · game-logic/score · 🌱 (`escalating-kill-points` — серія в часі, тут — одним вибухом).
  - `+pacifist-bonus` «Бонус за раунд без жодного вбивства» · game-logic/score · 🌱.
  - `+flee-from-bomb` «Ворог тікає від загрози» · entities/move · 📎.
  - `+water-release` «Розбита посудина дає воду, що стікає» · entities/interact · 🥉.
  - `+crush-moving-block` «Рухомий блок розчавлює» · entities/death · 🌱.
  - `+leftover-enemies-carry-over` «Недобиті вороги переходять у наступний раунд» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:multi_kill(n)` — один вибух/удар знищив ≥ n ворогів (фрукти, Super Heart).
- `+cond:feet_on_floor(a, n)` — скільки ніг/кутів спирається (висота стрибка).
- `+effect:stick_ceiling(a)` — прилипнути до стелі й ходити догори ногами.
- `+effect:release_water(cell)` — рідина з'являється й стікає вниз до опори.
- `+card:ceiling-walk`, `+card:self-damage-blast`, `+card:pacifist-bonus`, `+card:multi-kill-fruit` — див. вище.

## Джерела
- ⭐ [Wikipedia: Chack'n Pop](https://en.wikipedia.org/wiki/Chack%27n_Pop) — підлога й стеля, ноги-«телескоп» для сходинок, гранати вліво/вправо окремими кнопками, дим убиває героя, серця з кліток відчиняють стіни, Monsta з яєць, Mighta з каменем, бонус «усі або жодного», порти, автори.
- [Wikipedia JA: ちゃっくんぽっぷ](https://ja.wikipedia.org/wiki/ちゃっくんぽっぷ) — стрибок на 1 / ½ висоти, прилипання до стелі, одна граната до зникнення диму, ромб диму, вода без диму, кольори яєць, 4 види Monsta, лід, рухомі блоки, пляшки, Mighta і камені, фрукти, сині/жовті яблука, Super Heart, 20000 + 1UP / 5000, 1–2 гравці по черзі, перевидання.
- YouTube: пошук «Chack'n Pop arcade gameplay».

## Непевне
- (?) Чи дотик Monsta вбиває звичайного Chack'n — джерела кажуть лише «перешкода» і що Super-форма таранить; припущення «так».
- (?) Ноги-«телескоп» (EN-вікі: «витягує ноги, щоб піднятися на сходинку») і стрибок (JA-вікі) — можливо, один механізм, описаний по-різному.
- (?) Кількість раундів, очки за Monsta і фрукти, тривалість диму, Super-стану й запалу — не названо.
- (?) Сітковість руху — візуально блоки на сітці, рух героя, ймовірно, піксельний.
- (?) Чи Chack'n після смерті починає раунд спочатку чи продовжує з місця.
- (?) HUD, атракт-режим і таблиця рекордів — не описані в джерелах.
- JA-вікі сама позначена як стаття з недостатніми джерелами.
