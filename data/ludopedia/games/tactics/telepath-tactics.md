---
title: Telepath Tactics
slug: telepath-tactics
aka: [Telepath Tactics Liberated]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2015
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/357940", note: "оригінал 2015: штовхання в пастки/воду/лаву, руйнування, 23 класи, hotseat 2–6, редактор"}
  - {kind: other, url: "https://sinisterdesign.net/telepath-tactics-24-tips-for-survival", best: true, note: "24 поради від розробника: backstab +50 %, енергія і відпочинок, вода/лава, пастки, рух частинами, ментальні атаки"}
  - {kind: official, url: "https://sinisterdesign.net/telepath-tactics/", note: "висота дає бонус дистанційним, мости, барикади, статуси, моди, кампанії"}
  - {kind: steam, url: "https://store.steampowered.com/app/1849820/Telepath_Tactics_Liberated/", note: "ремейк 2022: 24 класи, ~50 престижних, 150+ скілів, 6 складностей, рандомізовані кампанії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Telepath+Tactics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [push-object, pull-object, height-levels, environment-death, destructible-blocks, cell-transform, floor-types, impassable-cells, hp-damage, melee-vs-ranged, line-of-sight-attack, status-effects, temporary-modes, orientation-state, unit-xp-skills, permadeath, destroy-all-enemies, reach-exit, shop-between-levels, inventory-items, dungeon-generation, difficulty-levels, ai-opponent, hot-seat, in-game-editor, level-exchange, reachable-highlight, threat-range, hover-highlight, game-screen, +backstab-facing, +energy-regen-rest, +split-move, +water-swim, +build-terrain, +trap-placement, +always-hit-damage, +elemental-resistance, +extra-turn-grant]
proposes: ["+trigger:attacked", "+effect:counterattack", "+effect:knockback", "+effect:build", "+cond:from_behind", "+cond:height_above", "+cond:resistant", "+effect:energy", "+ui:resist-panel", "+feature:campaign-editor", "+feature:random-campaign"]
author: opus
date: 2026-11-09
---

# Telepath Tactics — тактика на сітці з висотами, де бій вирішують позиція й середовище: ворога штовхають з урвища в лаву, ламають міст, ставлять пастки й бʼють у спину

## Суть
Покрокова тактика у дусі Fire Emblem: загін сестер Strider проти работорговців. Ядро — **керування полем**: штовхнути чи кинути ворога зі скелі, у воду, лаву, пастку чи в іншого ворога; зламати стіну чи міст, звести барикаду, заморозити річку. Шкода передбачувана (атаки влучають за замовчуванням), тож розрахунок — як у пазлі; ворожий AI робить те саме з тобою. Енергія (EN) — другий ресурс поруч із HP: скіли її витрачають, стояння на місці поновлює.

## Поле і час
- Квадратна сітка з **висотами** (урвища, скелі, мости над водою); клітини: земля, вода, лава, стіни, руйновані обʼєкти (стіни, дерева, мости), барикади, пастки.
- Хід стороною: кожен юніт рухається і діє; рух можна ділити — пройти частину, діяти, дорухатись.
- Висота: зверху — бонус шкоди й дальності дистанційним атакам.
- Карти: ручні сценарії кампанії + процедурні підземелля й ліси; у Liberated — опція рандомізованої кампанії.
- Інформація: поле видно; клік по ворогу показує дальність руху, характеристики, опори, предмети й атаки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт гравця | player | клас, HP, EN, орієнтація, опори стихій, ухилення | рух + атака/скіл; набирає досвід, підвищується до престижного класу |
| Ворожий юніт | enemy | те саме | AI: штовхає, бʼє в спину, ламає барикади, підбирає предмети, полює на цілителів |
| Mentalist | player | — | ментальна атака на відстані (завжди влучає), штовхання/тягнення на відстані, контроль розуму, левітація |
| Assassin | player | великий backstab-бонус | стрибає через ворогів до тилових цілей |
| Cavalier / Bowman | player | — | рух → атака → дорух (Lance / Bow) |
| Engineer | player | — | ставить барикади, створює вузькі проходи |
| Healer (psy-цілитель) | player | — | лікує ментальними щитами; пріоритетна ціль AI |
| Spirit | enemy | — | висмоктує HP і віддає енергію союзникам; вразливий до ментального |
| Stone Golem | enemy | — | вразливий до фото- і кріокінетики |
| Вода | terrain | — | 1 клітина = весь рух; плавець не атакує, втрачає EN, тоне (шкода) |
| Лава | hazard | — | горіння, шкода |
| Урвище / край скелі | hazard | висота | зіштовхнутий падає (?) |
| Стіна | static | руйнується | блокує; можна знести |
| Міст | terrain | руйнується | будується/підривається (Powder Bolt, Place Charges) |
| Барикада | static | руйнується | будує інженер; AI ламає |
| Валун | object | — | перекриває прохід |
| Snare-пастка | hazard | — | хто ступив — оглушений до свого наступного ходу (ні дій, ні контратак); AI її не бачить; свої теж спрацьовують |
| Вибухівка (charges) | hazard | — | підрив руйнує міст / клітини |
| Предмет (bandage, Focus Pill, Adrenaline Pill, Eye drops) | pickup | — | лікування, +EN без дії, +рух, зняти сліпоту |
| Клітина відступу | zone | — | у деяких місіях юніт може втекти через неї |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, cell)` → ЯКЩО `path_exists(unit, cell) and counter(move_left, >=, dist)` → ТО `move(unit, cell)`; решту руху можна витратити після дії.
- КОЛИ `enter(unit, water)` → ТО `custom: «рух закінчується»`, `set_state(unit, swimming)`; ЯКЩО `state(unit, swimming)` → ТО атакувати `block`, `custom: «−EN щохід»`, `damage(n)` (тоне).
- КОЛИ `enter(unit, lava)` → ТО `set_state(unit, burning)`, `damage(n)`.
- КОЛИ `enter(unit, snare_trap)` → ТО `stun(unit, until_own_turn)`; оглушений не контратакує.
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(unit, target, r)` → ТО `damage(n)` — точне число, без розкиду; ЯКЩО `custom: «у цілі dodge > 0 і атака не ментальна»` → ТО `custom: «шанс промаху»`.
- КОЛИ `input(attack, target)` → ЯКЩО `custom: «атака ментальна»` → ТО влучає завжди (навіть проти ухилення і коли атакувальник осліплений).
- КОЛИ `input(attack, target)` → ЯКЩО `custom: «атака ззаду» and not state(target, awareness)` → ТО `damage(n × 1.5)` (assassin — більше).
- КОЛИ `input(ranged_attack, target)` → ЯКЩО `custom: «атакувальник вище за ціль»` → ТО бонус шкоди й дальності.
- КОЛИ `input(attack, target)` → ЯКЩО `custom: «ціль слабка до стихії атаки»` → ТО більша шкода і шанс статусу.
- КОЛИ `custom: «юніта атаковано впритул»` → ЯКЩО `not state(target, stunned|frozen)` → ТО `custom: «контратака»`.
- КОЛИ `input(shove, target)` → ТО `push(target)` на 1 клітину (Shove / Kinetic Gust — на 1 більше).
- КОЛИ `input(pull, target)` → ЯКЩО `custom: «ментальний скіл»` → ТО `pull(target)` на відстані.
- КОЛИ `after(push(target))` → ЯКЩО `cell(dest, water|lava|trap)` → ТО відповідне правило клітини; ЯКЩО `cell(dest, cliff_edge)` → ТО `custom: «падіння з урвища»`.
- КОЛИ `input(throw, target)` → ТО `custom: «перекинути ціль на клітину»` (у воду, лаву, пастку).
- КОЛИ `input(demolish, wall|bridge|tree)` → ТО `set_cell(cell, floor|water|gap)`.
- КОЛИ `input(build, bridge|barricade)` → ТО `set_cell(cell, bridge|barricade)`.
- КОЛИ `input(freeze, water)` → ТО `set_cell(cell, ice)` — прохід через річку.
- КОЛИ `input(place, snare_trap|charges)` → ТО `place(unit, trap)`.
- КОЛИ `turn_start(unit)` → ЯКЩО `custom: «минулого ходу не рухався й не діяв»` → ТО `custom: «+5 EN»`; ЯКЩО `custom: «лише рухався без скілів»` → ТО `custom: «+1 EN»`.
- КОЛИ `input(skill, target)` → ЯКЩО `custom: «EN ≥ вартості скіла»` → ТО ефект, `custom: «−EN»`; інакше `block`.
- КОЛИ `input(motivate, ally)` → ТО `extra_move` (другий хід вибраному юніту).
- КОЛИ `input(mind_control, enemy)` → ТО `set_side(enemy, player)` на час статусу.
- КОЛИ `turn_end(unit)` → ТО `face(unit, dir)`; орієнтація визначає, звідки можна вдарити в спину.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)` (?).
- КОЛИ `all_gone(enemy)` → ТО `win`; у деяких місіях — `reach(unit, retreat_zone)` / врятувати.
- Перемога: виконати ціль місії (зазвичай знищити ворогів) · Поразка: втрата загону / ключового персонажа (?) · Рахунок: —.

## Керування і ввід
- Миша: клік по своєму юніту → підсвітка досяжних клітин → клік клітини; вибір атаки зі списку скілів; клік по цілі.
- Лівий клік по ворогу — дальність його руху; правий — характеристики, статуси, опори, предмети, атаки.
- Рух поетапно: частина руху, дія, решта руху; наприкінці — вибір орієнтації.
- Hotseat 2–6 гравців за одним компʼютером.

## Вікна, меню, HUD
- `main-menu`: кампанія · одиночні сценарії / процедурні карти · hotseat-мультиплеєр · редактор · налаштування.
- `game-screen`: ізометрична сітка з висотами; `hp-bar` і `energy-bar` юнітів; `reachable-highlight`; `threat-range` (дальність руху ворога за кліком); `turn-indicator`.
- `custom-window` «паспорт юніта» (правий клік): характеристики, статуси, опори стихій, предмети, атаки.
- `shop-window` — торговці між битвами: бинти, Focus Pills, броня, зброя.
- `custom-window` «просування» — вибір престижного класу; `inventory-window` — предмети загону.
- `editor-window` — редактор мап і кампаній; `dialogue-window` — сюжетні сцени.
- `difficulty-select` (Liberated: 6 пресетів + свої налаштування).

## Фічі поза полем
- Кампанія з десятками персонажів, досвід → нові атаки → престижні класи (`unit-xp-skills`).
- Економіка: припаси в бою й поза ним, торговці; у мультиплеєрі — випадкові предмети на карті, більше території — більше доступу до них.
- Hotseat 2–6 гравців, кілька режимів, альянси армій; онлайну нема.
- Редактор мап і кампаній, моди (класи, предмети, атаки, тайлсети, руйновані обʼєкти) — `level-editor`, `mod-support`.
- Liberated (2022): ремейк на новому рушії, 6 рівнів складності + custom, рандомізовані кампанії, окремий creator кампаній.

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (штовхання як головна зброя), [fire-emblem](fire-emblem.md) (кампанія й класи), [final-fantasy-tactics](final-fantasy-tactics.md) (висоти, орієнтація й спина), [battle-for-wesnoth](battle-for-wesnoth.md) (ремесло інді-тактики з редактором).
- Поза корпусом: Telepath RPG: Servants of God (попередник), Together in Battle (наступник Sinister Design).
- **Осі варіацій**: шкода — детермінована (TT) / з шансом (XCOM) · переміщення — push / pull / throw / телекінез · рух — суцільний / частинами з дією посередині · ресурс скілів — EN з регеном від бездіяльності / мана / cooldown.

## Цікавинки для курсу
- Штовхання й кидок у клітини з ефектом (вода, лава, пастка, урвище) + AI, що робить те саме — 🥉.
- Енергія, що відновлюється від бездіяльності (+5 стоячи, +1 лише рухаючись) — 🌱.
- Backstab +50 % множником за орієнтацією наприкінці ходу і стан «awareness» — 📎.
- Рух частинами: пройти, вдарити, дорухатись (лишок руху як ресурс) — 📎.
- Будування/руйнування поля: мости, барикади, заморожування річки — 🥉 (тайл як змінний стан).
- Пастка, яку AI не бачить — асиметрична інформація для AI — 📎.
- Детермінована шкода з винятком «ухилення проти не-ментальних атак» — 🌱.

## Мапа на каталог
- Є: `push-object` ↔ shove · `pull-object` ↔ ментальне тягнення · `height-levels` ↔ висоти й урвища · `environment-death` ↔ вода/лава/урвище · `destructible-blocks` ↔ стіни, мости, барикади · `cell-transform` ↔ заморожування води · `floor-types` ↔ вода, лава · `impassable-cells` · `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` (?) · `status-effects` / `temporary-modes` ↔ stun, freeze, blind, burning, mind control · `orientation-state` ↔ орієнтація для backstab · `unit-xp-skills` · `permadeath` (?) · `destroy-all-enemies` · `reach-exit` ↔ клітина відступу · `shop-between-levels` · `inventory-items` · `dungeon-generation` ↔ процедурні підземелля · `difficulty-levels` · `ai-opponent` · `hot-seat` · `in-game-editor` / `level-exchange` ↔ редактор і обмін кампаніями · `reachable-highlight` · `threat-range` · `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+backstab-facing` «Удар у спину за орієнтацією цілі» · entities/combat · 📎 · {mult: 1.5}.
  - `+energy-regen-rest` «Енергія скілів, відновлення від бездіяльності» · game-logic/economy · 🌱 · {rest: 5, move: 1}.
  - `+split-move` «Рух частинами з дією посередині» · entities/movement · 📎.
  - `+water-swim` «Вода: плавання з обмеженнями й утопленням» · entities/state · 📎.
  - `+build-terrain` «Будування мостів і барикад» · entities/terrain · 📎.
  - `+trap-placement` «Пастки, які ставить гравець» · entities/combat · 📎.
  - `+always-hit-damage` «Детермінована шкода без кидка» · entities/combat · 🌱.
  - `+elemental-resistance` «Стихії атак, опори й слабкості» · entities/combat · 📎.
  - `+extra-turn-grant` «Дати союзнику додатковий хід» · game-logic/turns · 🌱.

## Пропозиції до словників
- `+trigger:attacked` — юніта обрано ціллю атаки (контратака).
- `+effect:counterattack` — удар у відповідь після атаки впритул.
- `+effect:knockback` — відкинути на N клітин від атакувальника (push без руху атакувальника).
- `+effect:build` — звести обʼєкт на клітині (міст, барикада) — ширше за `place` з запасу.
- `+cond:from_behind` — атака ззаду відносно орієнтації цілі.
- `+cond:height_above` — атакувальник вище за ціль.
- `+cond:resistant` — ціль має опір/слабкість до стихії атаки.
- `+effect:energy` — ± енергія (EN) юніта як окремий від HP ресурс.
- `+ui:resist-panel` — панель опорів стихій у паспорті юніта.
- `+feature:campaign-editor` — створення цілих кампаній (персонажі, сцени, предмети, скіли).
- `+feature:random-campaign` — рандомізована кампанія з ручних частин.

## Джерела
- ⭐ [Sinister Design: 24 tips for survival](https://sinisterdesign.net/telepath-tactics-24-tips-for-survival) — backstab +50 % множником, awareness, +5/+1 EN, вода й лава, snare-пастки, рух частинами, ментальні атаки завжди влучають, Motivate, торговці.
- [Steam: Telepath Tactics](https://store.steampowered.com/app/357940) — дата 16.04.2015, штовхання, руйнування, 23 класи, 110+ атак, hotseat 2–6, редактор, моди.
- [Sinister Design: Telepath Tactics](https://sinisterdesign.net/telepath-tactics/) — висота дає бонус дистанційним, мости/барикади, статуси, процедурні карти, моди.
- [Steam: Telepath Tactics Liberated](https://store.steampowered.com/app/1849820/Telepath_Tactics_Liberated/) — ремейк 2022, класи й скіли, 6 складностей, рандомізовані кампанії, creator.
- YouTube: пошук «Telepath Tactics gameplay».

## Непевне
- (?) Що саме стається при зіштовхуванні з урвища (миттєва смерть чи шкода від падіння) — не перевірено.
- (?) Тягнення (pull) — лише з фрагмента фан-вікі в пошуку (сторінка віддає 402); Steam і офіційний сайт кажуть лише про shove/fling.
- (?) Permadeath юнітів у кампанії й умови поразки — не перевірено.
- (?) Числа бонусу висоти, вартість скілів у EN, шкода води/лави — не бачив.
- (?) Контратака впритул як загальне правило — виведено з поради «оглушений не контратакує».
- (?) Поле може бути ізометричним за поданням; вісь `layers` обрано через висоти.
