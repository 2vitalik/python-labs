---
title: Escape from Atlantis
slug: escape-from-atlantis
aka: [Survive!, "Survive: Escape from Atlantis!", The Island]
family: board-digital
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: score
year: 1982
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/survive-escape-from-atlantis/game-rules.php", best: true, note: "базові правила видання Stronghold: склад, 4 кроки ходу, рух людей і човнів, ефекти плиток, істоти, кінець і рахунок"}
  - {kind: other, url: "https://www.ultraboardgames.com/survive-escape-from-atlantis/challenge-rules.php", note: "5 опційних правил, зокрема дельфіни й кубики Dive"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Escape_from_Atlantis", note: "історія видань 1982–2013, кільця острова, різниця правил Parker / Waddingtons / Stronghold, доповнення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Survive+Escape+from+Atlantis+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, carrier-platform, touch-death, reach-exit, hidden-under-block, explode-area, spawn-points, inventory-items, event-points, rule-variants, game-screen, end-screen, help-window, +hex-grid-render, +ring-order-removal, +hidden-value-pieces, +majority-control-boat, +hidden-tile-effect, +reaction-cards, +hand-of-tiles, +creature-die-move, +shared-hazards-any-player, +random-end-trigger, +no-return-to-land, +capsize-to-swimmers]
proposes: ["+effect:roll_dice", "+cond:majority_aboard", "+card:ring-order-removal", "+card:hidden-value-pieces", "+card:majority-control-boat", "+card:hidden-tile-effect", "+card:reaction-cards", "+card:creature-die-move"]
author: opus
date: 2026-11-09
---

# Escape from Atlantis — гекс-острів тоне від берега до вершини: рятуй своїх у човнах, нацьковуй акул на чужих

## Суть
Острів з гексових плиток стоїть посеред моря; кожен гравець розставив на ньому своїх людей з **прихованими цінностями** 1–6 на денці. Хід: пересунути людей і човни (3 кроки на всіх), **зняти одну плитку суші** (від пляжів до гір) і глянути її спід — він дає акулу, кита, човен, вир або картку на потім, — і нарешті кинути кубик істоти та посунути будь-яку акулу, кита чи змія, найчастіше на чужих плавців. Гра закінчується, коли хтось відкриє вулкан під гірською плиткою; перемагає сума цінностей урятованих, а не їхня кількість.

## Поле і час
- Гексова сітка моря; у центрі — острів із плиток трьох типів: пляж, ліс, гора (концентричними кільцями: пляжі ззовні, гори в середині). У кутах поля — безпечні острови, до яких пристають із сусідніх морських клітин.
- Знята плитка лишає звичайну морську клітину — острів тане, море росте; поле змінює топологію щоходу.
- Шари клітини: суша/море + люди (до 3 на плитці у Waddingtons) + човен (не більше одного на клітину) + істоти (між собою не взаємодіють, можуть ділити клітину).
- Хід = 4 кроки одного гравця; кінець — випадковий (вулкан), тож довжина партії непередбачувана.
- Приховане: цінність кожної людини (навіть власник не показує), спід знятих плиток у руці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Людина | piece | колір гравця; цінність 1–6 на денці | ходить сушею, сідає в човен, плаває; з моря на сушу не повертається |
| Плавець | piece | людина в морі | 1 морська клітина за крок; сідає в човен лише у своїй клітині |
| Човен | platform | до 3 людей; 1 на клітину | везе людей; керує більшість на борту (нічия — кожен), порожній — будь-хто |
| Плитка пляжу / лісу / гори | tile | спід: ефект або вулкан | знімається в порядку пляж → ліс → гора; люди з неї падають у море |
| Безпечний острів | static | кут поля | людина, що висадилась, урятована й рахується |
| Морський змій | enemy | 1 клітина за хід | топить човен з людьми й усіх плавців у клітині; порожні човни не чіпає |
| Акула | enemy | 1–2 клітини | зупиняється на першій клітині з плавцями й зʼїдає їх; човни не чіпає |
| Кит | enemy | до 3 клітин | зупиняється на човні з людьми й перевертає його — люди стають плавцями |
| Дельфін | ally | лише в опційному правилі | захищає одного плавця від змія й акули |
| Вир | hazard | одноразовий | прибирає все рухоме в своїй і сусідніх морських клітинах |
| Вулкан | hazard | спід однієї гірської плитки | відкрили — кінець гри |
| Плитка в руці | pickup | «на початку ходу» / «захисна» | дельфін, вітер, переміщення істоти; захист від акули чи кита поза своїм ходом |
| Кубик істоти | — | грані: змій / акула / кит | який вид істоти рухати цього ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «плитки суші випадково»`, гравці по черзі `place(player, person)` на незайняту плитку, потім `place(player, boat)` у море біля суші.
- КОЛИ `turn_start(player)` → ЯКЩО `has(player, start_turn_tile)` і `first_time` (за хід) → ТО `use(player, tile)`: дельфін — `move(own_swimmer, ≤3)`; вітер — `move(controlled_boat, ≤3)`; змій/акула/кит — `teleport(creature, будь-яка вільна морська клітина)`; плитку — геть з гри.
- КОЛИ `input(move(person, land))` → ЯКЩО `state(person, on_land)` → ТО `move(person, adjacent_land)`, `counter(moves, -1)` (3 кроки на всіх своїх).
- КОЛИ `input(move(person, boat))` → ЯКЩО `count(people@boat, <, 3)` → ТО `move`, `attach(person, boat)`; чужі люди в човні не заважають.
- КОЛИ `leave(person, land)` → ТО `set_state(person, at_sea)`; ЯКЩО `state(person, at_sea)` → ТО повернення на сушу — `block`.
- КОЛИ `input(move(swimmer, dir))` → ТО `move(swimmer, dir)` на 1; сісти в човен — лише ЯКЩО `occupied(here, boat)`.
- КОЛИ `input(move(boat, dir))` → ЯКЩО `custom: «човен порожній або гравець має більшість на борту»` (`+cond:majority_aboard`) і `free(target)` (без іншого човна) → ТО `move(boat, dir)`, `carry(people)`; інакше `block`.
- КОЛИ `enter(boat, serpent_cell)` → ЯКЩО `count(people@boat, >, 0)` → ТО `disappear(boat)`, `disappear(people)`.
- КОЛИ `enter(boat, whale_cell)` → ЯКЩО `count(people@boat, >, 0)` → ТО `disappear(boat)`, `set_state(people, swimmer)`; ЯКЩО `occupied(cell, shark)` → ТО `disappear(people)`.
- КОЛИ `enter(swimmer, serpent_cell|shark_cell)` → ТО `disappear(swimmer)`.
- КОЛИ `input(disembark(person, safe_island))` → ЯКЩО `adjacent(boat|swimmer, safe_island)` → ТО `move(person, safe_island)` за 1 крок, `set_state(person, saved)`.
- КОЛИ `phase_start(sink)` → ЯКЩО `custom: «плитка торкається моря»` і `custom: «найнижчий лишений тип: пляж → ліс → гора»` → ТО `set_cell(tile, sea)`, `custom: «гравець таємно дивиться спід»`; люди з плитки — `set_state(person, swimmer)`.
- КОЛИ `custom: «спід — акула»` → ТО `spawn_at(shark, тут)`, `disappear(swimmers@тут)`.
- КОЛИ `custom: «спід — кит»` → ТО `spawn_at(whale, тут)`.
- КОЛИ `custom: «спід — човен»` → ТО `spawn_at(boat, тут)`, `attach(swimmers@тут, boat)` до 3 (кого — вирішує той, хто відкрив).
- КОЛИ `custom: «спід — вир»` → ТО `explode(hex_ring, 1, sea)` — геть усі плавці, човни, люди й істоти тут і в сусідніх морських клітинах.
- КОЛИ `custom: «спід — плитка на потім»` → ТО `give(player, tile)` лицем донизу.
- КОЛИ `contact(shark, own_swimmer)` → ЯКЩО `has(player, shark_defense)` → ТО `disappear(shark)` першим, плавець живий (поза своїм ходом); так само кит і свій човен.
- КОЛИ `phase_start(creature)` → ТО `custom: «кинути кубик істоти»` (`+effect:roll_dice`), `choose(істота цього виду)`.
- КОЛИ `input(move(serpent))` → ТО `move(serpent, 1)`; КОЛИ `enter(serpent, cell)` → ЯКЩО `occupied(cell, boat_with_people)` → ТО `disappear(boat + people)`; `disappear(swimmers@cell)`.
- КОЛИ `input(move(shark))` → ТО `move(shark, ≤2)`; КОЛИ `enter(shark, cell)` → ЯКЩО `occupied(cell, swimmer)` → ТО `disappear(swimmers)`, хід акули скінчено.
- КОЛИ `input(move(whale))` → ТО `move(whale, ≤3)`; КОЛИ `enter(whale, cell)` → ЯКЩО `occupied(cell, boat_with_people)` → ТО `disappear(boat)`, `set_state(people, swimmer)`, хід кита скінчено.
- КОЛИ `custom: «у гравця не лишилось людей на полі»` → ТО `skip_turn(move_phase)` — решту кроків робить далі.
- КОЛИ `custom: «відкрито вулкан»` → ТО `game_over`; усі, хто в морі, втрачені — рахуються лише люди на безпечних островах.
- КОЛИ `game_over` → ТО `reveal(saved_people)`, `score(Σ цінностей)`; найбільша сума — `win`.
- Перемога: найбільша сума прихованих цінностей урятованих · Поразка: — · Рахунок: Σ 1–6 за кожну врятовану людину.

## Керування і ввід
- Настільна: гравець розподіляє 3 кроки між людьми й човнами, знімає плитку за правилом черги, кидає кубик і сам вибирає, яку істоту й куди вести — можна атакувати будь-кого.
- Захисні плитки грають поза своїм ходом — реакція на чужу дію.
- (цифрова версія) Клік по людині/човну — підсвітка сусідніх клітин; клік по плитці, яку дозволено зняти; спід бачить лише активний гравець (екран-«передай пристрій» для hotseat); драг істоти до 1–3 клітин.

## Вікна, меню, HUD
(цифрова версія — офіційної не знайшов)
- `main-menu` → `match-setup`: 2–4 гравці, кольори, опційні правила (Densely Populated, Leave No One Behind, Everyone Is Equal, Atlantis Is Gone, Dolphins & Dive Dice).
- `placement-screen`: по черзі розставити людей (цінність видно лише власнику) і по 2 човни.
- `game-screen`: гекс-поле з островом і морем, `turn-indicator`, крок ходу (рух → зняття → істота), лічильник кроків `action-points` (3), рука плиток (`pocket`), кубик істоти, лічильник урятованих на кожному острові.
- `pass-device` перед ходом (приховані цінності й спід плиток); `confirm-dialog` захисної плитки у відповідь на атаку.
- `end-screen`: відкриття всіх урятованих, суми цінностей, переможець.
- `help-window`: памʼятка ефектів плиток і поведінки істот.

## Фічі поза полем
- `custom-rules`: 5 опційних правил — щільна розстановка (до 2 людей на плитку, крім берегових); «нікого не лишати» (вулкан = вир, гра до останньої людини); «усі рівні» (рахувати кількість, не цінність); «Атлантиди нема» (кінець після останньої плитки); дельфіни й кубики Dive (замість кубика істоти: кубик «хто» з гранню-зірочкою-джокером і кубик «на скільки» 1/1/2/2/3/«D» — будь-яка вільна клітина).
- `hotseat` на 2–4 гравців (доповнення — на 5–6).
- Нема рівнів складності й соло-режиму.

## Варіації й родичі
- Видання: Survive! (Parker Brothers, 1982: випадкові плитки, кубик замість спінера, кити замість гігантського кальмара, без дельфінів) · Escape from Atlantis (Waddingtons, 1986: тривимірний острів, спінер, кальмари й морські чудовиська) · Survive: Escape from Atlantis! (Stronghold, 2011, 30th Anniversary 2012) · The Island (Asmodee, 2012 — та сама гра). Доповнення 2013: 5–6 гравців, Dolphins & Dive Dice, Giant Squid.
- Forbidden Island (`forbidden-island.md`) — острів теж тоне, але кооп і за картками; Hey, That's My Fish! (`hey-thats-my-fish.md`) — поле з гексів зникає під гравцями; Taluva (`taluva.md`) — гекс-острів, що навпаки росте.
- **Осі варіацій**: порядок руйнування поля (кільцями за типом / випадково / вибором гравця) · хто керує загрозами (гра / будь-який гравець кубиком) · рахунок (кількість урятованих / приховані цінності) · кінець (прихована плитка-тригер / останній урятований / останній тайл).

## Цікавинки для курсу
- Поле, що тоне кільцями: «зняти можна лише плитку найнижчого лишеного типу, що торкається моря» — перевірка межі на гекс-сітці — 📎.
- Приховані цінності фігур: власник знає, решта ні — рішення «кого рятувати першим» і блеф — 🌱 (у цифрі — 📎 через pass-device).
- Човен під контролем більшості: власність обʼєкта визначається складом пасажирів, нічия — спільна — 📎.
- Три істоти з різним «правилом зупинки» (змій 1 крок і топить, акула ≤2 і зупиняється на першій жертві, кит ≤3 і перевертає човен) — 🥉 за систему.
- Реактивні плитки поза ходом (захист від акули/кита) — 🥉 (переривання чужого ходу в рушії).
- Плитка-спід з ефектом «одразу / на початку ходу / у відповідь» — 🌱 за кожен вид.
- AI-гравець: оцінка безпечних маршрутів з урахуванням можливих ходів істот наступного кидка — 🥇.

## Мапа на каталог
- Є: `hot-seat` · `turn-enforcement` · `carrier-platform` (човни везуть людей) · `touch-death` (акула, змій) · `reach-exit` (безпечні острови) · `hidden-under-block` (спід плиток) · `explode-area` (вир — радіус 1) · `spawn-points` (істоти зʼявляються на місці знятої плитки) · `inventory-items` (плитки в руці) · `event-points` (цінності 1–6) · `rule-variants` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+ring-order-removal` «Поле руйнується кільцями: спершу клітини найнижчого типу на межі» · levels/generation · 📎.
  - `+hidden-value-pieces` «Фігури з прихованою цінністю, відкриваються наприкінці» · game-logic/score · 🌱.
  - `+majority-control-boat` «Обʼєкт керує той, кого в ньому більше» · entities/state · 📎.
  - `+hidden-tile-effect` «Знята плитка має прихований ефект: одразу / потім / у відповідь» · entities/interact · 🌱.
  - `+reaction-cards` «Хід поза чергою у відповідь на атаку» · game-logic/opponent · 🥉.
  - `+creature-die-move` «Кубик вибирає вид загрози, гравець — конкретну й маршрут» · entities/move · 🌱.
  - `+hex-grid-render` · `+hand-of-tiles` — уже пропонувались; `+shared-hazards-any-player` · `+random-end-trigger` · `+no-return-to-land` · `+capsize-to-swimmers` — дрібні.

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубик і використати грань (тут — вид істоти; у Dive — ще й відстань).
- `+cond:majority_aboard` — гравець має більшість (або нічию) серед пасажирів обʼєкта; порожній — будь-хто.
- `+card:ring-order-removal` · `+card:hidden-value-pieces` · `+card:majority-control-boat` · `+card:hidden-tile-effect` · `+card:reaction-cards` · `+card:creature-die-move` — див. «Мапа на каталог».

## Джерела
- ⭐ [UltraBoardGames: базові правила](https://www.ultraboardgames.com/survive-escape-from-atlantis/game-rules.php) — склад Stronghold (40 плиток: 16 пляж, 16 ліс, 8 гора; по 10 людей 4 кольорів; 5 зміїв, 6 акул, 5 китів, 4 дельфіни, 12 човнів), розстановка, 4 кроки ходу, рух, ефекти плиток трьох видів, істоти, кінець.
- [UltraBoardGames: опційні правила](https://www.ultraboardgames.com/survive-escape-from-atlantis/challenge-rules.php) — 5 варіантів, кубики Dive, захист дельфіном.
- [Wikipedia](https://en.wikipedia.org/wiki/Escape_from_Atlantis) — Julian Courtland-Smith, видання 1982–2012, кільця острова, відмінності правил і компонентів, доповнення 2013.
- YouTube: пошук «Survive Escape from Atlantis how to play».

## Непевне
- (?) Грані кубика істоти (скільки змій / акула / кит) — на сторінці лише картинки.
- (?) У Waddingtons-версії спінер показує і вид, і відстань (1, 2, 3 або 5) — за Wikipedia; у Stronghold відстань фіксована за видом.
- (?) Кількість людей: Stronghold — 10 на колір, Waddingtons — 12; плиток: 40 (Stronghold) проти 37 (Waddingtons, з центральною вершиною).
- (?) Ліміт людей на плитці суші в Stronghold (Wikipedia каже 3 для Waddingtons; UBG при розстановці — по одній).
- (?) Розподіл ефектів на споді 40 плиток (скільки акул, китів, човнів, вирів, захисних) не бачив; вулкан — один, під горою.
- (?) Офіційної цифрової версії не знайшов (пошук Steam без збігів).
