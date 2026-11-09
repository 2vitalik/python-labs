---
title: Mage Knight Board Game
slug: mage-knight
aka: [Mage Knight, Mage Knight Ultimate Edition, MKBG]
family: tactics
also: [board-digital, roguelike]
klass: avatar
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: score
year: 2011
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mage_Knight_Board_Game", note: "огляд: колода 16 карт, рука 5, день/ніч, відкриття тайлів, режими, доповнення"}
  - {kind: other, url: "https://www.ultraboardgames.com/mage-knight/game-rules.php", best: true, note: "правила першого сценарію: раунди, хід, відпочинок, мана, села, юніти, рани, слава, тактики, фінальний підрахунок"}
  - {kind: other, url: "https://www.ultraboardgames.com/mage-knight/combat.php", note: "4 фази бою, стихії й опір, Fortified/Swift/Brutal/Poison/Paralyze/Summon, нокаут"}
  - {kind: other, url: "https://www.ultraboardgames.com/mage-knight/movement.php", note: "рух за вартістю тайла, дослідження за 2 Move, провокація rampaging-ворогів"}
  - {kind: other, url: "https://www.ultraboardgames.com/mage-knight/game-elements.php", note: "кольори мани, кристали, типи карт, скіли, рівні, гляди й шахти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mage+Knight+Board+Game+playthrough", note: "пошук; партія"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, impassable-cells, floor-types, fog-of-war, hidden-under-block, inventory, inventory-limit, unit-xp-skills, status-effects, round-currency, shop-catalog, event-points, score-records, destroy-all-enemies, reach-exit, chain-reaction, undo-step, ai-opponent, hot-seat, difficulty-levels, map-window, pocket, objective-text, +deck-building, +deck-draw, +card-dual-use, +sideways-play, +mana-dice-pool, +day-night-cycle, +tile-exploration, +wound-cards, +combat-phases, +elemental-resistance, +provoke-zone, +fame-level-track, +reputation-track, +unit-recruit, +round-end-by-deck, +revert-until-reveal, +end-titles-scoring]
proposes: ["+effect:draw_card", "+effect:discard", "+role:card", "+role:site", "+trigger:round_start", "+trigger:deck_empty", "+trigger:provoked", "+cond:day_night", "+cond:resistant", "+effect:roll_dice", "+effect:spend_mana", "+effect:add_wound", "+effect:explore_tile", "+effect:level_up", "+ui:fame-track", "+ui:reputation-track", "+ui:mana-source", "+ui:day-night-board", "+window:offer-row", "+window:tactic-select", "+axis:session"]
author: opus
date: 2026-11-09
---

# Mage Knight Board Game — один лицар-маг на гексах, що відкриваються: кожна карта колоди — рух, вплив, атака чи блок, а рани засмічують руку

## Суть
Кожен гравець — Mage Knight з колодою з 16 базових дій. За хід він грає карти з руки як **очки руху, впливу, атаки чи блоку** (будь-яку не-рану можна покласти боком за «1» будь-чого), рухається гексами, відкриває нові тайли мапи, б'є ворогів-жетони, вербує загони в селах, захоплює замки. Раунди чергуються **день/ніч** і закінчуються, коли в когось скінчилась колода. Рани — це карти, що лягають у руку й займають місце; ціль сценарію — напр. відкрити/захопити місто, переможець — за славою.

## Поле і час
- Поле — гекс-тайли по 7 гексів, що викладаються під час гри (стартовий тайл із порталом); новий тайл має збігатися з кутовими символами і бути повернутим так само.
- Кожен гекс має терен: вартість входу береться з дошки день/ніч (велике число — день, мале синє — ніч, червоний X — недоступно); озеро недоступне. Платиш за гекс, у який входиш.
- Сайти на гексах: села, монастирі, замки (keep), вежі магів, підземелля, гробниці, лігва, руїни, магічні галявини, кристальні шахти, міста.
- Час: **раунди** = день або ніч по черзі (з дня); у раунді — ходи гравців у порядку тактик. Сценарій «First Reconnaissance» — 3 раунди (день, ніч, день).
- Інформація прихована: невідкриті тайли, жетони ворогів у замках і вежах (не видно до штурму), руїни вночі лежать лицем донизу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mage Knight (герой) | player | броня (2 на старті), ліміт руки (5), command-ліміт, слава, репутація, рівень | рухається гексами; за хід — рух + ≤ 1 дія (бій або взаємодія) |
| Колода Deed / рука / скидання | supply | 16 базових дій | на початку раунду перетасовується вся, добір до ліміту руки |
| Basic Action | supply | ефект + посилений ефект за ману кольору | рух / вплив / атака / блок / лікування |
| Advanced Action | supply | золота рамка | сильніша дія; з вітрини (offer) за рівень/монастир |
| Spell | supply | фіолетова рамка | посилений («ultimate») ефект — лише вночі з чорною маною |
| Artifact | supply | золота рамка | одноразова ultimate-сила знищує артефакт |
| Wound | supply | — | марна карта в руці, займає місце; не скидається без лікування |
| Тактика | supply | номер | обирається на раунд; менший номер ходить раніше |
| Мана-кубики (Source) | resource | 6 кольорів | 1 кубик за хід як мана свого кольору; після ходу перекидається; чорний — у «вичерпані» |
| Кристал | resource | ≤ 3 одного кольору | зберігається між ходами; переводиться в ману |
| Мана-токен | resource | колір | діє лише в цей хід |
| Unit (загін) | ally | рівень, броня, здібності, вартість | вербується в селі/замку тощо; займає command-токен; поранений не активується |
| Rampaging enemy (орки-мародери, драконум) | enemy | броня, атака, стихія, здібності, слава | стоїть на гексі; у його гекс не ввійти; провокується |
| Захисник замку / вежі / міста | enemy | як вище | невідомий до штурму; Fortified |
| Монстр підземелля / лігва | enemy | як вище | тягнеться з коричневого жетон-пулу при вході |
| Село | static | вплив ± репутація | вербування юнітів, лікування за вплив; пограбування |
| Магічна галявина | terrain | — | кінець ходу тут — скинути рану; початок ходу — золотий (вночі чорний) мана-токен |
| Кристальна шахта | terrain | колір | кінець ходу тут — кристал її кольору |
| Руїни | container | жетон | вдень відкриті, вночі закриті до входу |
| Портал | static | — | старт; там можна стояти будь-кому; фігуру знімають із поля, доки не рушиш |
| Місто | static | — | ціль сценарію; відкривається, коли поруч, навіть уночі |
| Щит-токен | mark | колір гравця | позначає захоплений сайт / пройдену пригоду; трекер слави й репутації |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО `custom: «перевернути дошку день/ніч, перекинути всі кубики»`; день — чорні у вичерпані; ніч — золоті у вичерпані.
- КОЛИ `custom: «початок раунду»` → ТО кожен `custom: «перетасовує всю колоду, добирає до ліміту руки»` і `choose(tactic)`; першим обирає той, у кого найменше слави.
- КОЛИ `input(play_card, card, mode)` → ТО `counter(move|influence|attack|block|heal, +n)`.
- КОЛИ `input(play_card_powered, card)` → ЯКЩО `has(hero, mana, card_color)` → ТО `take(hero, mana)` і посилений ефект.
- КОЛИ `input(play_sideways, card)` → ЯКЩО `custom: «карта не рана»` → ТО `counter(move|influence|attack|block, +1)`.
- КОЛИ `input(take_die)` → ЯКЩО `counter(dice_used, <, 1)` → ТО `give(hero, mana_of_die)`; ЯКЩО `custom: «золото вдень»` → ТО мана будь-якого базового кольору.
- КОЛИ `input(cast_spell_strong)` → ЯКЩО `custom: «ніч» and has(hero, black_mana) and has(hero, color_mana)` → ТО ultimate-ефект закляття; вдень `block`.
- КОЛИ `input(move, hex)` → ЯКЩО `counter(move, >=, cost(hex, day|night))` → ТО `move(hero, hex)`, `counter(move, −cost)`; ЯКЩО `cell(hex, lake)` або `occupied(hex, rampaging_enemy)` → ТО `block`.
- КОЛИ `input(explore)` → ЯКЩО `custom: «гекс на краю мапи» and counter(move, >=, 2)` → ТО `counter(move, −2)`, `custom: «викласти новий тайл»`, `reveal(tile)`; на тайлі `spawn_at(enemy_token, sites)`.
- КОЛИ `after(reveal)` → ТО `custom: «попередні дії кроку незмінні»` (до відкриття нової інформації будь-що можна відкотити).
- КОЛИ `custom: «рух з гекса поруч із rampaging-ворогом на інший гекс поруч із ним же»` → ТО `custom: «ворог спровокований»`: рух закінчується, лишок Move згорає, бій обовʼязковий (дія ходу).
- КОЛИ `input(challenge, rampaging_enemy)` → ЯКЩО `adjacent(hero, enemy)` → ТО бій, дія ходу витрачена.
- КОЛИ `phase_start(ranged_siege)` → ЯКЩО `counter(ranged+siege, >=, armor(enemy))` → ТО `disappear(enemy)`, `counter(fame, +fame(enemy))`; ЯКЩО `state(enemy, fortified)` → ТО рахується лише siege; боком грати не можна.
- КОЛИ `phase_start(block)` → ЯКЩО `counter(block, >=, attack(enemy))` → ТО атаку відбито; часткового блоку нема — атака повністю проходить; ЯКЩО `state(enemy, swift)` → ТО потрібно ×2 блоку.
- КОЛИ `phase_start(assign_damage)` → ТО шкода розподіляється: `custom: «непоранений юніт бере 1 рану, шкода − його броня»`; решта — герою: `give(hero, wound)` у руку, шкода − броня героя, повторити; ЯКЩО `state(enemy, brutal)` → ТО шкода ×2.
- КОЛИ `contact(poison_attack, hero)` → ТО за кожну рану в руку ще одна в скидання; юніт — 2 рани.
- КОЛИ `contact(paralyze_attack, hero)` → ТО `custom: «скинути всі не-рани з руки»`; поранений юніт знищується.
- КОЛИ `counter(wounds_this_combat, >=, hand_limit)` → ТО `custom: «нокаут: скинути всі не-рани з руки»`.
- КОЛИ `phase_start(attack)` → ЯКЩО `counter(attack, >=, armor(enemy))` → ТО `disappear(enemy)`, `counter(fame, +n)`; ЯКЩО `custom: «фізичний опір»` → ТО фізична атака ÷2, вогонь/лід — повністю.
- КОЛИ `phase_start(block)` → ЯКЩО `state(enemy, summoner) and custom: «не знищений у фазі ranged»` → ТО `spawn(brown_monster)` замість нього на блок і шкоду; потім зникає без слави.
- КОЛИ `counter(fame, >=, threshold)` → ТО на кінці ходу рівень +1: непарний — command-токен, броня/ліміт руки; парний — `choose(skill)` + `give(hero, advanced_action)`.
- КОЛИ `input(influence, village)` → ТО `custom: «вплив ± репутація»`; ЯКЩО `custom: «щит на червоному X репутації»` → ТО `block`; купити: юніт (command-токен), лікування.
- КОЛИ `input(plunder, village)` → ТО `counter(reputation, −1)`, `custom: «добрати 2 карти»`.
- КОЛИ `input(heal, n)` → ТО `take(hero, wound)` за кожну 1; юніт — вартість = його рівень за рану.
- КОЛИ `turn_end(hero)` → ЯКЩО `cell(hero_hex, magical_glade)` → ТО можна скинути рану; ЯКЩО `cell(hero_hex, crystal_mine)` → ТО `give(hero, crystal)`.
- КОЛИ `turn_end(hero)` → ТО зіграні карти в скидання, кубики перекинуто й повернуто, `custom: «добрати до ліміту руки»` (перед тим можна скинути будь-які не-рани).
- КОЛИ `input(rest)` → ТО ні руху, ні дії: скинути 1 не-рану + будь-які рани (у скидання, не в пул ран).
- КОЛИ `turn_start(hero)` → ЯКЩО `custom: «у руці лише рани»` → ТО виснаження: показати, скинути 1 рану, без руху й дій.
- КОЛИ `turn_start(hero)` → ЯКЩО `custom: «колода порожня»` → ТО можна оголосити кінець раунду (мусить, якщо й рука порожня); решта — по одному останньому ходу.
- КОЛИ `custom: «місто відкрито»` (сценарій) → ТО кожен робить ще 1 хід, потім `game_over`.
- КОЛИ `game_over` → ТО фінальна слава: титули Greatest Knowledge / Loot / Leader / Conqueror / Adventurer (+3, нічия +1) і Greatest Beating (−2 за рану в колоді, найбільший — ще −3); `win` — найбільше слави.
- Перемога: ціль сценарію + найбільше слави (кооп/соло — ціль до кінця відведених днів) · Поразка: не виконати ціль за відведені раунди · Рахунок: слава.

## Керування і ввід
- (Настолка) гравець викладає карти стовпчиками: «рух», «вплив», «атака/блок» по фазах бою; поруч — кубики з Source, кристали, токени.
- Порядок ходу: спершу рух (і дослідження), потім ≤ 1 дія; або «відпочинок».
- Відкат: будь-яку дію можна забрати назад, доки не відкрито нову інформацію (тайл, карта, жетон, кидок) — вбудований `undo` до точки reveal.
- Бойовий «менеджер» — сусідній гравець стежить за правилами, але за ворогів рішень не ухвалює (вороги детерміновані).

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: гекс-мапа; `pocket` — рука; трекер слави/рівня (`+ui:fame-track`) і репутації; дошка день/ніч з вартостями тереномів; Source з кубиками; кристали; ряд юнітів.
- (цифрова версія) `custom-window` «вітрини» — offer Advanced Actions, Spells, Units: щораунду найнижча карта йде, решта зсуваються, зверху нова.
- (цифрова версія) `custom-window` «бій» — 4 колонки фаз: дистанційна/облога → блок → розподіл шкоди → атака; жетони ворогів з бронею, атакою, стихією, опором.
- (цифрова версія) `choose`-вікно тактики на початку раунду; вікно рівня (скіл + Advanced Action).
- (цифрова версія) `end-screen` — підрахунок слави за титулами; `help-window` — опис сайтів (картки Site Description).

## Фічі поза полем
- Режими: соло (solitaire), змагальний, кооперативний; сценарії з різними цілями й кількістю днів (`mode-select`).
- Прогресія в межах партії: слава → рівні до 10, скіли, Advanced Actions, юніти, артефакти, закляття — колода росте (декбілдинг).
- 4 героя в базі; доповнення: The Lost Legion (2012), Krang (2013), Shades of Tezla (2015), The Apocalypse Dragon (2026); Ultimate Edition 2018.
- PvP між гравцями — опційний, не рекомендований у першій партії.

## Варіації й родичі
- Родичі в корпусі: [gloomhaven](gloomhaven.md) (карти як дії в тактиці), [card-hunter](card-hunter.md) (колода з предметів), [heroes-of-might-and-magic-3](heroes-of-might-and-magic-3.md) (герой мандрує мапою з сайтами й наймає загони), [kingdom-death-monster](kingdom-death-monster.md) (важка кооп-настолка).
- Поза корпусом: Mage Knight (мініатюрна гра 2000), Dominion (декбілдинг), Slay the Spire.
- **Осі варіацій**: карта — одна дія (StS) / кілька режимів + «боком за 1» (MK) · ресурс посилення — мана-кубики спільного пулу + кристали · шкода — HP / карти-рани в колоді · кінець раунду — за часом / коли колода скінчилась.

## Цікавинки для курсу
- Карта з кількома режимами + «боком за 1 будь-чого» + посилення маною кольору — 📎 (одна структура карти, три способи зіграти).
- Рани як карти в колоді: шкода зменшує руку, а лікування — це видалення карти — 🥉.
- Спільний пул мана-кубиків: 1 на хід, після ходу перекидається; золото — лише вдень, чорне — лише вночі — 🥉.
- Бій у 4 фази з порогами: дистанційна/облога → повний-або-нічого блок → розподіл шкоди з бронею → атака; Fortified/Swift/Brutal/Poison/Paralyze/Summon — 🥈.
- Відкриття гекс-тайлів зі збігом кутових символів і спавном ворогів на сайтах — 🥉.
- Провокація: рух з одного сусіднього гекса ворога в інший — 📎 (зона контролю без ZOC-вартості).
- Відкат до моменту reveal (undo, що «замерзає», коли відкрито нову інформацію) — 🥈.
- Кінцеві титули (Knowledge, Loot, Leader, Conqueror, Adventurer, Beating) — 📎.

## Мапа на каталог
- Є: `hp-damage` ↔ броня-проти-атаки · `melee-vs-ranged` ↔ ranged/siege проти звичайної атаки · `impassable-cells` ↔ озеро · `floor-types` ↔ вартість терену день/ніч · `fog-of-war` / `hidden-under-block` ↔ невідкриті тайли й закриті жетони · `inventory` / `inventory-limit` ↔ кристали ≤ 3 на колір · `unit-xp-skills` ↔ рівні, скіли · `status-effects` ↔ поранені юніти, отрута, параліч · `round-currency` ↔ вплив і мана · `shop-catalog` ↔ вітрини offer · `event-points` / `score-records` ↔ слава · `destroy-all-enemies` (бій) · `reach-exit` ↔ відкрити місто · `chain-reaction` ↔ Summon · `undo-step` ↔ відкат до reveal · `ai-opponent` ↔ детерміновані вороги · `hot-seat` · `difficulty-levels` ↔ сценарії · `map-window` · `pocket` · `objective-text`.
- **Нема** → пропозиції карток:
  - `+deck-building` «Колода росте картами з вітрини» · entities/state · 🥉.
  - `+deck-draw` «Колода / рука / скидання з перетасовкою» · entities/state · 🥉 · {hand_limit}.
  - `+card-dual-use` «Карта з кількома режимами (рух/вплив/атака/блок)» · entities/state · 📎.
  - `+sideways-play` «Будь-яка карта боком = 1 будь-чого» · game-logic/economy · 🌱.
  - `+mana-dice-pool` «Спільний пул кубиків-ресурсів, перекидання після ходу» · game-logic/economy · 🥉 · {per_turn: 1}.
  - `+day-night-cycle` «Раунди день/ніч змінюють вартості й ресурси» · game-logic/turns · 📎.
  - `+tile-exploration` «Відкриття тайлів мапи з правилом стику» · world/levels · 🥉.
  - `+wound-cards` «Шкода як мертві карти в руці» · entities/combat · 📎.
  - `+combat-phases` «Бій у фіксованих фазах з порогами» · entities/combat · 🥈.
  - `+elemental-resistance` «Стихії атак і опір (÷2)» · entities/combat · 📎.
  - `+provoke-zone` «Рух повз ворога провокує атаку» · entities/combat · 📎.
  - `+fame-level-track` «Трек слави з порогами рівнів» · game-logic/score · 🌱.
  - `+reputation-track` «Репутація змінює ціни/доступ» · game-logic/economy · 🌱.
  - `+unit-recruit` «Найм загонів з command-лімітом» · entities/state · 📎.
  - `+round-end-by-deck` «Раунд закінчується, коли колода порожня» · game-logic/turns · 🌱.
  - `+revert-until-reveal` «Відкат дій до моменту відкриття інформації» · game-logic/undo · 🥈.
  - `+end-titles-scoring` «Фінальні титули за категоріями» · game-logic/score · 📎.

## Пропозиції до словників
- `+effect:draw_card` / `+effect:discard` — добір і скидання карт.
- `+role:card` — карта як сутність поза полем; `+role:site` — сайт на гексі з власними правилами взаємодії (село, вежа, шахта).
- `+trigger:round_start` — початок раунду (раунд ≠ хід гравця); `+trigger:deck_empty` — колода вичерпана на початку ходу.
- `+trigger:provoked` — ворога спровоковано рухом поруч.
- `+cond:day_night` — зараз день / ніч; `+cond:resistant` — ціль має опір стихії атаки.
- `+effect:roll_dice` — кинути кубик(и) (Source, броня); у словнику `roll` = скочування.
- `+effect:spend_mana` — витратити ману кольору на посилення.
- `+effect:add_wound` — покласти карту-рану в руку/скидання.
- `+effect:explore_tile` — викласти новий тайл мапи за правилом стику.
- `+effect:level_up` — підвищити рівень за порогом треку.
- `+ui:fame-track` · `+ui:reputation-track` · `+ui:mana-source` (кубики пулу) · `+ui:day-night-board` (таблиця вартостей терену).
- `+window:offer-row` — вітрина карт/юнітів зі зсувом; `+window:tactic-select` — вибір тактики-порядку на раунд.
- `+axis:session` — `scenario` (партія з кількістю днів).

## Джерела
- ⭐ [UltraBoardGames: Game Rules](https://www.ultraboardgames.com/mage-knight/game-rules.php) — компоненти, раунди, хід/відпочинок/виснаження, мана й боком за Influence 1, села, юніти, рани, слава/репутація, тактики, підготовка раунду, фінальні титули.
- [UltraBoardGames: Combat](https://www.ultraboardgames.com/mage-knight/combat.php) — 4 фази, боком за Attack/Block 1, стихії й опір, здібності ворогів, нокаут.
- [UltraBoardGames: Movement](https://www.ultraboardgames.com/mage-knight/movement.php) — вартість входу, дослідження за 2, провокація.
- [UltraBoardGames: Game Elements](https://www.ultraboardgames.com/mage-knight/game-elements.php) — мана 6 кольорів, кристали ≤ 3, типи карт, скіли, рівні, галявини, шахти, руїни.
- [Wikipedia](https://en.wikipedia.org/wiki/Mage_Knight_Board_Game) — автор, рік, 1–4 гравці, режими, герої, доповнення.
- YouTube: пошук «Mage Knight Board Game playthrough».

## Непевне
- (?) Боком за **Move 1** — у відкритих сторінках бачив лише Influence 1 і Attack/Block 1; Move 1 — з памʼяті.
- (?) Числові вартості терену (рівнина/пагорби/ліс/пустеля/болото, день vs ніч) — на сайті лише в картинках; відомо лише «ліс вночі дорожчий, пустеля вночі дешевша».
- (?) Кольори жетонів ворогів (зелені орки, сірі замки, фіолетові вежі, коричневі підземелля, червоний драконум, білі міста) — з памʼяті, у тексті джерел не названі.
- (?) Стихія «cold fire», правила відступу з бою, PvP — не перевірено.
- (?) Офіційна цифрова версія — у джерелах не згадана; вікна позначено як «(цифрова версія)».
- (?) Шахта на кількох ходах поспіль дає «більше кристалів» — формулювання джерела, точний механізм не перевірено.
