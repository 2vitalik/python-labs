---
title: "XCOM: Enemy Unknown / XCOM 2"
slug: xcom
family: tactics
also: [build-sim]
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2012
platforms: [PC, Mac, Linux, PS3, Xbox 360, PS4, Xbox One, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Cover_(EU2012)", best: true, note: "UFOpaedia: укриття −20/−40, фланг, напрямок укриття, руйнування за типом зброї, огляд 17 клітин"}
  - {kind: wiki, url: "https://www.ufopaedia.org/index.php/Overwatch_(EU2012)", note: "Overwatch: тригер руху, ×0,7 до точності, без критів, усі одночасно"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/XCOM:_Enemy_Unknown", note: "загін 1–6, атака/ривок завершують хід, щити-іконки, класи, Ironman, геоскейп"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/XCOM_2", note: "concealment, таймери місій, процедурні мапи, хакінг, Avenger, Avatar-годинник"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=xcom"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=xcom+2+gameplay+tactical", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, blast-wave, melee-vs-ranged, legal-move-highlight, ai-opponent, inventory-items, difficulty-levels, save-autosave, destroy-all-enemies, time-out, player-death, player-camera, +action-points, +cover-system, +flanking, +overwatch, +hit-chance, +line-of-sight-attack, +destructible-blocks, +fog-of-war, +concealment, +pilot-xp-skills, +status-effects, +death-countdown, +damage-forecast]
proposes: ["+trigger:enemy_moved", "+trigger:sighted", "+trigger:attacked", "+cond:line_of_sight", "+cond:prob", "+cond:status", "+effect:set_status", "+effect:set_cell", "+effect:reveal", "+role:piece", "+role:terrain", "+ui:reachable-highlight", "+ui:hit-chance", "+ui:cover-icon", "+ui:target-icons", "+ui:action-pips", "+ui:turn-timer", "+window:shot-panel", "+window:base-management", "+window:squad-select", "+window:map-window", "+window:upgrade-window", "+feature:roster-carryover", "+axis:session"]
author: opus
date: 2026-11-02
---

# XCOM — стандарт тактики з укриттями: дві дії, щит половинний чи повний, відсоток на пострілі

## Суть
Загін із 4–6 солдатів зачищає мапу від прибульців покроково: кожен солдат має **дві дії** за хід, ховається за укриттям (половинним чи повним) і стріляє з відомим відсотком влучання. Ядро — позиційна гра: укриття знижує шанс по тобі, **обхід із флангу** знімає його повністю, `Overwatch` караючи стріляє по тому, хто рухається. XCOM 2 додає **приховування** загону на старті й таймери місій, що змушують іти вперед. Між місіями — стратегічний шар: база, дослідження, ростер із перманентною смертю.

## Поле і час
- Поле — квадратна сітка з **поверхами** (дахи, балкони, ліфти, висота) у 3D-рендері; камера вільна з поворотом на 90°, перемикання поверхів.
- Укриття — властивість **ребра** між клітинами (стіна, машина, ящик): низьке (half) чи високе (full); більшість обʼєктів руйнуються.
- Хід гравця: усі солдати діють у будь-якому порядку; потім хід прибульців. Прибульці стоять «підами» (групами) й активуються, коли їх побачили; активовані роблять безкоштовний перебіг до укриття (scamper).
- Туман війни: огляд солдата ~17 клітин (EU), бачене загоном — спільне; поза ним — останнє відоме.
- Випадковість: процедурні мапи (XCOM 2) і RNG пострілів/критів/шкоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Солдат | piece | HP, Aim, Will, Mobility, Defense, клас, звання, перки, 2 дії | рух/постріл/граната/навички; набирає звання за вбивства |
| Assault / Ranger | piece | дробовик / меч | Run & Gun: постріл після ривка; Ranger — атака мечем з рухом |
| Heavy / Grenadier | piece | ракетниця / гранатомет | вибухи руйнують укриття, Suppression (пригнічення) |
| Sniper / Sharpshooter | piece | Squadsight | стріляє по цілях, яких бачить будь-хто з загону |
| Support / Specialist | piece | аптечки / дрон Gremlin | лікує, хакає роботів і термінали |
| Psi Operative | piece | Will | контроль розуму, пригнічення |
| SHIV / MEC (EW) | piece | механічний | не панікує, іноді не ховається |
| Прибулець (Sectoid, ADVENT, Muton, Chryssalid…) | enemy | HP, Aim, Defense, під | активується групою, ховається, фланкує; Chryssalid — ближній бій і зараження |
| Робот (Drone, MEC, Sectopod) | enemy | hardened (захист від критів) | можна хакнути (XCOM 2) |
| Укриття низьке | terrain | −20 до шансу по тому, хто за ним | руйнується шкодою середовищу |
| Укриття високе | terrain | −40 | сюди не «визирають» стрільці |
| Руйнівний обʼєкт (машина, бочка) | hazard | HP середовища | горить/вибухає, шкодить сусідам |
| Зона евакуації | zone | — | солдати, що стали, виходять із місії |
| Обʼєкт місії (термінал, VIP, бомба) | switch | таймер | хакнути/врятувати/знешкодити за N ходів |
| Тіло/лут | pickup | таймер зникнення (XCOM 2) | зібрати до кінця відліку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(xcom)` → ТО кожен солдат `custom: «2 дії»`.
- КОЛИ `input(move, s, cell)` → ЯКЩО `custom: «у синій зоні»` → ТО `move`, −1 дія; ЯКЩО `custom: «у жовтій зоні (dash)»` → ТО `move`, −2 дії.
- КОЛИ `input(shoot, s, t)` → ЯКЩО `line_of_sight(s, t)` and `has(s, ammo)` → ТО `prob(hit)`; `end_turn(s)` (постріл завершує хід солдата, крім перків).
- Шанс: `custom: «Aim + модифікатор дальності − Defense цілі − укриття (20 | 40) + висота»`; ЯКЩО `custom: «ціль флангована»` → укриття = 0 і `+50 % криту` по відкритій цілі.
- Фланг: КОЛИ `custom: «лінія від стрільця до цілі не перетинає ребро укриття»` → ТО ціль флангована (іконка щита жовтіє/червоніє).
- КОЛИ влучання → ТО `damage(roll(min..max))`, при криті — більше; КОЛИ промах → ТО `custom: «може зачепити укриття»` (`set_cell(rubble)`).
- КОЛИ `input(overwatch, s)` → ТО `set_status(s, overwatch)`, `end_turn(s)`; КОЛИ `enemy_moved(e)` → ЯКЩО `line_of_sight(s, e)` → ТО постріл з Aim × 0,7 (ціль у ривку — × 0,5), без критів, один раз.
- КОЛИ `input(hunker, s)` → ТО `set_status(s, hunkered)` — бонус укриття ×2 до наступного ходу (?), `end_turn(s)`.
- КОЛИ `input(grenade, s, cell)` → ЯКЩО `in_range` → ТО `damage(area)` без шансу промаху, `custom: «знищує укриття в радіусі»` (шкода середовищу 250).
- КОЛИ `sighted(pod)` → ТО `custom: «scamper: під безкоштовно біжить до укриття»`; далі ходить у фазі прибульців.
- КОЛИ `hp_zero(s)` → ЯКЩО `prob(crit_wound)` → ТО `set_status(s, bleeding_out)` — стабілізувати аптечкою за кілька ходів, інакше смерть; ТО `died(s)` — назавжди (permadeath), спорядження втрачено, якщо не винести тіло (XCOM 2).
- Паніка: КОЛИ `died(ally)` / сильна шкода → ЯКЩО `custom: «перевірка Will не пройдена»` → ТО `set_status(s, panicked)` — гравець втрачає керування на хід.
- XCOM 2 concealment: КОЛИ `level_start` → ТО `set_status(squad, concealed)`; КОЛИ `custom: «солдат зайшов у червону клітину огляду ворога»` або атака → ТО `clear_state(squad, concealed)` (засідка Overwatch’ем з приховування — головна тактика).
- XCOM 2 таймер: КОЛИ `turn_end(xcom)` → ТО `counter(mission_timer, −1)`; КОЛИ `counter(mission_timer, ==, 0)` → ТО `lose` або примусова евакуація (залежить від місії).
- Хакінг: КОЛИ `input(hack, specialist, target)` → ТО `prob(hack)` → вибір нагороди / вимкнення / перехоплення робота.
- Перемога: знищити всіх прибульців / виконати ціль і евакуюватись. Поразка: загін знищено, ціль провалено, таймер вийшов. Кампанія: EU — 8 із 16 країн вийшли; XCOM 2 — шкала Avatar-проєкту заповнилась.

## Керування і ввід
- Курсор/миша по клітинах: наведення показує шлях, іконки укриття на кінцевій клітині (щит половинний/повний) і чи буде солдат фланкований.
- Клік — рух; ПКМ або кнопки дій унизу: Shoot, Overwatch, Hunker Down, Reload, Grenade, Medkit, Hack, навички класу; Tab — перебір солдатів; Q/E — поворот камери; поверхи — окремі клавіші.
- Shoot → вибір цілі серед іконок ворогів у полі зору → панель пострілу з відсотками → підтвердження.
- End Turn — кнопкою, або хід завершується, коли всі витратили дії.

## Вікна, меню, HUD
- `main-menu`: Continue, New Game (вибір складності, Ironman, Second Wave/опції кампанії), Load, Multiplayer, Options, Exit.
- `game-screen`: 3D-поле; `reachable-highlight` синій (1 дія) і жовтий (ривок) контури; `path-preview`; `cover-icon` на клітинах; полоска HP над юнітами з `action-pips` (скільки дій лишилось) (?); `target-icons` — червоні голови видимих ворогів; внизу `ability-buttons`; `turn-timer`/лічильник ходів місії (XCOM 2); `objective-text`.
- `shot-panel`: `hit-chance` %, крит %, розкладка модифікаторів (Aim, дальність, укриття, висота, фланг), прогноз шкоди на полосці HP цілі (`damage-forecast`).
- `squad-select` — вибір і спорядження загону перед місією; `end-screen` — підсумок місії (вбиті, поранені, трофеї, оцінка).
- `base-management` — розріз бази/Avenger: дослідження, інженерія, бараки (`upgrade-window` перків при підвищенні), memorial загиблих.
- `map-window` — геоскейп (Земля, сигнали тривоги, панік-рівень країн / Avatar-шкала).
- `pause-menu`: Save, Load, Options, Restart Mission, Exit; `settings-window`.

## Фічі поза полем
- Кампанія з ростером (`roster-carryover`): звання й перки, поранення = відсутність кілька днів, перманентна смерть; кастомізація солдатів.
- `mode-hardcore` — Ironman (один сейв, перезапис після кожної дії); `difficulty-presets` 4 рівні; Second Wave — `custom-rules` (опції кампанії).
- `autosave`, `save-slots`; `online-multiplayer` 1×1 зі змішаними загонами і таймером ходу (`turn-timer`).
- `mod-support` (XCOM 2, Long War); War of the Chosen — Chosen-боси, фракції-класи, «втома» солдатів.

## Варіації й родичі
- Попередник: X-COM: UFO Defense (1994) — очки часу (TU) замість двох дій, реакційний вогонь за TU.
- Родичі: Phoenix Point (вільне прицілювання частин тіла), Mario + Rabbids (укриття + рух-стрибки, без RNG дальності), Gears Tactics, Xenonauts, Invisible Inc. (приховування, таймер тривоги).
- Осі варіацій:
  - **дії**: 2 дії, атака завершує (XCOM) / очки часу (X-COM, Jagged Alliance) / рух+дія (FFT);
  - **укриття**: від клітини цілі (Wesnoth) / від ребра поруч (XCOM) / від напрямку погляду (FFT);
  - **реакція**: Overwatch по руху / контратака (Wesnoth, FFT) / нема (Polytopia — лише відповідь на атаку);
  - **стелс**: нема / приховування на старті (XCOM 2) / весь рівень стелс (Invisible Inc.).

## Цікавинки для курсу
- Укриття на ребрах клітин + фланг (чи перетинає лінія від стрільця ребро укриття) — 🥈: геометрія ребер на сітці.
- Дві дії з синьою/жовтою зоною досяжності — 📎 (два BFS з порогом).
- Overwatch: подія «ворог рухається в зоні огляду» перериває його рух — 🥉 (переривання ходу іншої сторони).
- Шанс влучання як сума модифікаторів з розкладкою в UI — 📎.
- Руйнування укриття вибухом (`set_cell`) — 🌱.
- Лінія видимості й туман війни зі спільним баченням загону — 🥉 (Bresenham/raycast).
- Приховування з червоними клітинами огляду ворога — 📎.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` ↔ постріл · `blast-wave` ↔ граната (кругла область) · `melee-vs-ranged` ↔ меч Ranger · `legal-move-highlight` + `hover-highlight` · `ai-opponent` · `inventory-items` ↔ гранати/аптечки · `difficulty-levels` · `save-autosave`/`save-multi-slot` · `shop-between-levels` ↔ інженерія бази · `in-round-upgrades` ↔ перки · `destroy-all-enemies` · `time-out` ↔ таймер місії · `player-death` · `field-scaling` + `player-camera` · `game-screen`/`main-menu`/`pause-menu`/`settings-window`/`end-screen`.
- **Нема** → пропозиції карток:
  - `+action-points` «Очки дії за хід» · game-logic/opponent · 📎 · слот {ap: 2, ends_turn: [shoot, overwatch]}.
  - `+cover-system` «Укриття половинне/повне» · entities/combat · 🥈 · слот {half: 20, full: 40}.
  - `+flanking` «Обхід укриття» · entities/combat · 🥉 — дитина `+cover-system`.
  - `+overwatch` «Реакційний постріл по руху» · entities/combat · 🥉 · слот {aim_mult: 0.7}.
  - `+hit-chance` (з Wesnoth) — сума модифікаторів.
  - `+line-of-sight-attack` (з Adventures of Lolo) — постріл лише по видимій цілі.
  - `+destructible-blocks` (з Bomberman) — укриття руйнується.
  - `+fog-of-war` (з Wesnoth) — спільне бачення загону.
  - `+concealment` «Приховування до виявлення» · game-logic/opponent · 📎 · слот {detect_radius}.
  - `+turn-limit-lose` (з Wesnoth) — таймер місії.
  - `+pilot-xp-skills` (з Into the Breach) — звання й перки.
  - `+status-effects` (з Wesnoth) — паніка, кровотеча, отрута, підпал, оглушення.
  - `+death-countdown` (з FFT) — bleeding out.
  - `+damage-forecast` (з Wesnoth) — прогноз шкоди на полосці HP.

## Пропозиції до словників
- `+trigger:enemy_moved(e)` — ворог зробив крок (тригер Overwatch); `+trigger:sighted(a, b)` — B увійшов у поле зору A (активація підів, вихід з приховування); `+trigger:attacked` (з Wesnoth).
- `+cond:line_of_sight` ⏳ — головна умова пострілу; `+cond:prob` ⏳; `+cond:status` / `+effect:set_status` — overwatch, hunkered, concealed, panicked, bleeding_out.
- `+effect:set_cell` ⏳ — укриття → уламки; `+effect:reveal` ⏳ — туман.
- `+role:terrain` ⏳ — тут укриття як властивість ребра (окремий випадок: ребро, а не клітина).
- `+ui:reachable-highlight` (є) — дві зони (1 дія / ривок); `+ui:hit-chance`; `+ui:cover-icon` — щит половинний/повний/фланг; `+ui:target-icons` — ряд видимих цілей; `+ui:action-pips` — скільки дій лишилось; `+ui:turn-timer` — лічильник ходів місії.
- `+window:shot-panel` — панель пострілу з розкладкою модифікаторів; `+window:base-management` — база між місіями; `+window:squad-select` (з Into the Breach); `+window:map-window` ⏳ — геоскейп; `upgrade-window` ⏳ — вибір перка.
- `+feature:roster-carryover` (з Wesnoth); `mode-hardcore` ⏳ = Ironman.
- `+axis:session` = `campaign`.

## Джерела
- ⭐ [UFOpaedia: Cover (EU2012)](https://www.ufopaedia.org/index.php/Cover_(EU2012)) — числа укриття, фланг і напрямок укриття, руйнування за типом зброї, огляд 17 клітин.
- [UFOpaedia: Overwatch (EU2012)](https://www.ufopaedia.org/index.php/Overwatch_(EU2012)) — тригер, ×0,7/×0,5, без критів, перки з кількома пострілами.
- [Wikipedia: XCOM: Enemy Unknown](https://en.wikipedia.org/wiki/XCOM:_Enemy_Unknown) — загін 1–6, «атака або ривок завершують хід», щити-іконки, класи, Ironman, геоскейп і паніка країн.
- [Wikipedia: XCOM 2](https://en.wikipedia.org/wiki/XCOM_2) — приховування, таймери, процедурні мапи, 5 класів, хакінг, Avatar.
- YouTube: пошук «xcom 2 gameplay tactical».

## Непевне
- (?) Hunker Down — «подвоює бонус укриття» (UFOpaedia згадує мимохідь), точна механіка й зняття від фланга.
- (?) Бонус висоти до точності (+20?) і його відсутність у XCOM 2 для частини випадків.
- (?) Bleeding out: кількість ходів до смерті; шанс критичного поранення залежить від складності.
- (?) Наявність окремих «піпсів» дій над юнітом — в EU через колір іконки; деталі UI різняться між EU і XCOM 2.
