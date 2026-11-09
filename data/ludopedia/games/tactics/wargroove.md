---
title: Wargroove
slug: wargroove
aka: [Варгрув]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: none
  goal: state
year: 2019
platforms: [PC, Switch, Xbox One, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wargroove", best: true, note: "огляд: Nintendo Wars-подібна, 15 командирів, редактори кампаній і світу, мультиплеєр"}
  - {kind: fandom, url: "https://wargroovewiki.com/Rules", note: "правила з ігрового кодексу: groove, крити 1.35–2.5×, захват, дохід, найм, підкріплення, місцевість, контратака, туман, погода"}
  - {kind: fandom, url: "https://wargroovewiki.com/Unit", note: "список юнітів за будівлями, крити мага й лучника"}
  - {kind: fandom, url: "https://wargroovewiki.com/Commander", note: "командир: groove 100 %, швидкості заряду, поразка при загибелі"}
  - {kind: fandom, url: "https://wargroovewiki.com/Dog", note: "крит пса, нюх крізь місцевість, тікає замість смерті"}
  - {kind: fandom, url: "https://wargroovewiki.com/Cavalry", note: "крит після 6 клітин від старту"}
  - {kind: fandom, url: "https://wargroovewiki.com/Giant", note: "крит при ≤40 % HP, ×2.5"}
  - {kind: fandom, url: "https://wargroovewiki.com/Spearman", note: "крит поруч з іншим списником"}
  - {kind: fandom, url: "https://wargroovewiki.com/Mage", note: "крит при захисті ≥3, лікування 20 %"}
  - {kind: fandom, url: "https://wargroovewiki.com/Mercia", note: "приклад командира: Healing Aura"}
  - {kind: other, url: "https://news.xbox.com/en-us/2019/02/08/wargroove-tips-and-tricks/", note: "поради: командир як сила і слабке місце, кодекс з інфо клітини"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Wargroove"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wargroove+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, impassable-cells, floor-types, hp-damage, melee-vs-ranged, legal-move-highlight, threat-range, reachable-highlight, fog-of-war, round-currency, ai-opponent, hot-seat, online-multiplayer, in-game-editor, editor-playtest, level-exchange, sequential-levels, world-map, mode-select, codex-window, save-game, +commander-unit, +groove-meter, +positional-crit, +capture-income, +recruit-from-base, +terrain-bonus, +retaliation, +leader-death-lose, +structure-reinforce, +weather-modifiers, +ambush-stop, +damage-forecast, +summon-creature]
proposes: ["+trigger:attacked", "+trigger:sighted", "+cond:moved", "+cond:hp_ratio", "+cond:terrain_defense", "+effect:counterattack", "+role:site", "+role:commander", "+ui:groove-meter", "+ui:damage-forecast", "+ui:crit-indicator", "+ui:terrain-shields", "+window:commander-select", "+window:recruit-window", "+window:arcade-ladder", "+feature:branching-campaign"]
author: opus
date: 2026-11-09
---

# Wargroove — Advance Wars з командиром на полі, який і найсильніша фігура, і король, а кожен юніт має свою умову крита

## Суть
Покрокова стратегія на квадратній сітці в стилі Nintendo Wars: захоплюєш села заради золота, наймаєш юнітів у казармах, вежах і портах, тиснеш на ворожу фортецю. Головна відмінність — **командир** стоїть на полі як юніт: найсильніший боєць і водночас слабке місце, бо його загибель — поразка. Командир накопичує **Groove** — суперздібність (лікування, призов, телепорт), що заряджається від боїв. Кожен тип юніта має **позиційну умову критичного удару** (списник поруч зі списником, кавалерія після довгого розгону, лучник без руху), тож розстановка важить не менше за вибір цілі. 15 командирів, кожен зі своєю кампанією.

## Поле і час
- Квадратна сітка, клітина = тип місцевості (рівнина, дорога, ліс, гора, вода, риф, міст, стіна, пляж…) з іконками захисту-щитів чи штрафу-черепів; будівлі (фортеця, села, казарма, вежа, порт, схованка) мають власне HP.
- Покроково по сторонах: за хід кожен юніт може рухатись і потім виконати дію (атака, захват, лікування…); найм — раз на будівлю за хід.
- Туман війни (опційно на мапі): юніт бачить у межах дальності огляду, гори/стіни/ліси блокують погляд; ліс і риф приховані, доки поруч нема свого юніта; будівлі видно завжди.
- Погода — модифікатор мапи (сприятливий вітер / буря, сніг, піщана буря).
- Бій детермінований: шкода залежить від HP атакувальника, ефективності проти типу цілі, погоди, місцевості й крита — без кубиків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Командир (Mercia, Valder, Sigrid, Emeric…) | piece | рух 4, дальність 1, огляд 4, захват; groove зі швидкістю заряду | найсильніший юніт; не наймається; загибель = поразка; groove при 100 % |
| Солдат (Soldier) | piece | рух 4; захват | крит поруч зі своїм командиром |
| Пес (Dog) | piece | 150 золота; рух 5 | крит, якщо ціль поруч з іншим псом (×1.5); бачить крізь гори, ліси й рифи в межах огляду; переможений тікає, а не гине |
| Списник (Spearman) | piece | 250 золота; рух 3 | крит, якщо поруч інший свій списник (×1.5) |
| Маг (Mage) | piece | 400 золота; рух 5 | крит, коли його захист ≥3 (ліс, гора) (×1.5); Heal: клітина в межах 2 + сусідні союзники +20 % HP |
| Лучник (Archer) | piece | дальність | крит, якщо атакує, не рухаючись |
| Кавалерія (Cavalry) | piece | 600 золота; рух 6 (riding) | крит, якщо атакує з клітини за 6 від старту ходу (×1.5) |
| Велетень (Giant) | piece | 1200 золота; рух 5 | завжди крит при HP ≤40 % (×2.5 — найбільший) |
| Віз (Wagon) / транспорти | piece | — | везуть юнітів; без крита |
| Балиста, требушет | piece | дальність | не контратакують |
| Повітряні (Air Trooper, Balloon, Aeronaut, Sky Rider, Dragon) | piece | вежа | огляд не блокується місцевістю |
| Морські (Barge, Riverboat, Amphibian, Turtle, Harpoon Ship, Frog, Kraken, Warship) | piece | порт | рух водою; погода змінює рух ±2 |
| Злодій, стрілець (Thief, Rifleman) | piece | схованка | спецюніти схованки |
| Призвані (Sparrow Bomb, Vine, Crystal, Shadow Sister…) | ally | — | створює groove; атака/вбивство призваних не дає заряду |
| Фортеця (Stronghold) | zone | HP; −50 % шкоди | 100 золота/хід; знищення = поразка власника |
| Село (Village) | zone | HP, власник | 100 золота/хід; захоплюється; підкріплює сусідній юніт |
| Казарма / вежа / порт / схованка | zone | — | найм наземних / повітряних / морських / спецюнітів, раз за хід |
| Місцевість | terrain | щити −10 % кожен до −40 %; черепи +10 % до +40 % | ціна руху за типом руху; гори дають огляд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «ціна шляху за типом руху ≤ рух юніта»` and `free(cell)` → ТО `move(unit, cell)`; далі одна дія або очікування.
- КОЛИ `custom: «рух через прихованого ворога»` → ТО `custom: «засідка: рух зупинено»`; наслідок за клітиною (на нейтральній — знищення, на ворожій — відкидання) (?).
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, range(a))` → ТО `damage(f(HP a, ефективність a→b, погода, щити клітини b, крит))`.
- КОЛИ `input(attack, soldier, b)` → ЯКЩО `custom: «поруч зі своїм командиром»` → ТО `custom: «крит»`.
- КОЛИ `input(attack, dog, b)` → ЯКЩО `adjacent_count(b, own_dog, ≥, 2)` → ТО `custom: «крит ×1.5»` (атакувальник + ще один пес поруч цілі).
- КОЛИ `input(attack, spearman, b)` → ЯКЩО `adjacent_count(spearman, own_spearman, ≥, 1)` → ТО `custom: «крит ×1.5»`.
- КОЛИ `input(attack, mage, b)` → ЯКЩО `custom: «захист клітини мага ≥3»` → ТО `custom: «крит ×1.5»`.
- КОЛИ `input(attack, archer, b)` → ЯКЩО `custom: «цього ходу не рухався»` → ТО `custom: «крит»`.
- КОЛИ `input(attack, cavalry, b)` → ЯКЩО `custom: «атакує з клітини за 6 від стартової»` → ТО `custom: «крит ×1.5»`.
- КОЛИ `input(attack, giant, b)` → ЯКЩО `custom: «HP ≤ 40 %»` → ТО `custom: «крит ×2.5»`.
- КОЛИ `custom: «атаку завершено»` → ЯКЩО `custom: «b вижив»` and `in_range(b, a, range(b))` and `custom: «b може бити тип a, b не балиста/требушет»` → ТО `custom: «контратака»`.
- КОЛИ `hp_zero(unit)` → ЯКЩО `same(unit, dog, type)` → ТО `custom: «тікає»`; інакше `disappear_a`.
- КОЛИ `custom: «командир атакує / атакований / вбив»` → ТО `counter(groove, +n)`; КОЛИ `turn_start(side)` → ТО `counter(groove, +rate)` (20 / 10 / 7 / 5 % за швидкістю).
- КОЛИ `input(groove, commander)` → ЯКЩО `counter(groove, ≥, 100)` → ТО `custom: «ефект groove командира»`, `counter(groove, =0)`; приклад — Mercia Healing Aura `heal(allies in radius, 50 %)`.
- КОЛИ `input(capture, unit, structure)` → ЯКЩО `has(unit, capture)` and `custom: «будівля нейтральна»` → ТО `set_side(structure, unit.side)`; HP будівлі = половина HP юніта.
- КОЛИ `hp_zero(enemy_structure)` → ТО `set_side(structure, neutral)`; фортеця отримує лише половину шкоди.
- КОЛИ `turn_start(side)` → ТО `currency(+100 × (села + фортеця))`, `custom: «будівлі +10 % HP»`.
- КОЛИ `input(recruit, building, type)` → ЯКЩО `has(side, gold ≥ cost)` and `custom: «будівля ще не наймала цього ходу»` → ТО `currency(−cost)`, `spawn_at(unit, building)`.
- КОЛИ `input(reinforce, unit)` → ЯКЩО `custom: «поруч своя будівля»` → ТО `heal(unit, n)`, `custom: «будівля −n HP»`; командир — до еквівалента 500 золота.
- КОЛИ `custom: «погода: сприятливий вітер»` → ТО `custom: «наземна дальність +1, повітря отримує ×1.2, морський рух +2»`; буря — навпаки (×0.8, −2; стрільця не стосується).
- КОЛИ `died(commander)` or `custom: «фортецю знищено»` → ТО `lose` для власника; КОЛИ `custom: «усі суперники вибули»` → ТО `win`.
- Перемога: вибити всіх суперників (командир або фортеця) або ціль сценарію · Поразка: свій командир чи фортеця · Рахунок: зірки/оцінка в аркаді (?).

## Керування і ввід
- Курсор по клітинах (геймпад / миша): вибір юніта → підсвітка досяжних клітин і зони атаки → клітина → меню дії (Attack, Capture, Heal, Groove, Wait, Load).
- Перед атакою — прогноз шкоди й контратаки, позначка крита, якщо умова виконана.
- Кнопка інфо клітини → кодекс юніта/місцевості; End Turn; скасування руху до підтвердження дії (?).
- Локально hotseat і онлайн, PvP і кооп.

## Вікна, меню, HUD
- `main-menu`: Story (кампанія) → `world-map`; Arcade; Puzzle; Multiplayer → `lobby-window`; Custom Content (редактори, завантаження); Codex → `codex-window`; Options → `settings-window`.
- `match-setup`: мапа, сторони, командири (`commander-select`), туман, погода, AI/людина.
- `game-screen`: сітка, `turn-counter`, `coins` і дохід, портрет командира з `groove-meter`, інфо клітини з `terrain-shields`, `legal-move-highlight`, `threat-range`; `damage-forecast` і `crit-indicator` при виборі цілі.
- `recruit-window`: список юнітів будівлі з ціною і коротким описом.
- `editor-window`: редактор мап і кампаній, світовий редактор зі звʼязками місій; `end-screen` з оцінкою.
- `dialogue-window` — сюжетні сцени між ходами.

## Фічі поза полем
- `level-editor` — власні мапи, катсцени, тригери; `branching-campaign` — світовий редактор звʼязує місії гілками й умовами розблокування; `level-sharing` онлайн.
- `mode-puzzle` — задачі «перемогти за один хід» (?); `mode-select` (Story / Arcade / Puzzle).
- `hotseat`, `online-multiplayer`, `mode-coop`; `ai-opponent-levels`.
- `difficulty-presets` / `custom-difficulty` для кампанії (шкода, дохід, швидкість groove) (?).
- `codex` — довідка юнітів, командирів, місцевості з будь-якої клітини.

## Варіації й родичі
- Wargroove 2 (2023) — groove до 200 % з другим рівнем, роглайт-режим (?).
- Родичі: [Advance Wars](advance-wars.md) (CO поза полем, сила CO, без критів за позицією), [Fire Emblem](fire-emblem.md) (лорд — поразка при загибелі), Tiny Metal.
- Осі варіацій:
  - **командир**: поза полем (Advance Wars) / на полі як найсильніша фігура-король (Wargroove);
  - **крит**: нема / випадковий (Fire Emblem) / детермінований за позицією юніта;
  - **захват**: N ходів захвату (Advance Wars) / вибити HP будівлі і зайняти (Wargroove);
  - **місцевість**: зірки захисту / щити −10 % і черепи +10 %.

## Цікавинки для курсу
- Позиційні крити: у кожного типу свій предикат (сусід того ж типу, відстань від старту, не рухався, захист клітини, HP%) — 📎; таблиця предикатів = гарний тест на дизайн умов.
- Командир-король на полі з поразкою при загибелі — 🌱.
- Groove-шкала: заряд від подій і пасивно, з різною швидкістю — 🌱.
- Будівлі з HP: захват через знищення в нейтраль, регенерація, підкріплення за рахунок будівлі — 📎.
- Детермінований прогноз шкоди з контратакою — 📎.
- Туман з засідкою, що зупиняє рух, і псом, який бачить крізь ліс — 🥉.
- Редактор кампаній з гілками місій — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух за типом · `impassable-cells`, `floor-types` ↔ вода, гори, ліс · `hp-damage` · `melee-vs-ranged` ↔ контратака лише в межах дальності · `legal-move-highlight`, `threat-range`, `reachable-highlight` · `fog-of-war` · `round-currency` ↔ золото · `ai-opponent`, `hot-seat`, `online-multiplayer` · `in-game-editor`, `editor-playtest`, `level-exchange` · `sequential-levels`, `world-map` ↔ кампанія · `mode-select`, `codex-window`, `save-game`.
- **Нема** → пропозиції карток:
  - `+commander-unit` «Командир на полі» · entities/combat · 🌱 · слот {lose_on_death, groove}.
  - `+groove-meter` «Шкала суперздібності» · entities/state · 🌱 · слот {rate, sources}.
  - `+positional-crit` «Крит за позицією» · entities/combat · 📎 · слот {predicate, multiplier}.
  - `+capture-income`, `+recruit-from-base`, `+retaliation`, `+leader-death-lose`, `+damage-forecast`, `+terrain-bonus`, `+summon-creature` — як у корпусі.
  - `+structure-reinforce` «Підкріплення від будівлі» · game-logic/economy · 🌱.
  - `+weather-modifiers` «Погода мапи» · game-logic/difficulty · 🌱.
  - `+ambush-stop` «Засідка в тумані» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:attacked` — атака як подія (groove, контратака); `+trigger:sighted` — ворога виявлено в тумані (засідка).
- `+cond:moved` — юніт рухався цього ходу (лучник); `+cond:hp_ratio` — HP у відсотках від максимуму (велетень); `+cond:terrain_defense` — захист клітини ≥ N (маг).
- `+effect:counterattack` — відповідний удар захисника (вжито як `custom`).
- `+role:site` — захоплювана будівля з HP; `+role:commander` — фігура-король із суперздібністю.
- `+ui:groove-meter` · `+ui:damage-forecast` · `+ui:crit-indicator` · `+ui:terrain-shields`.
- `+window:commander-select` · `+window:recruit-window` · `+window:arcade-ladder`.
- `+feature:branching-campaign` — світовий редактор: місії звʼязані гілками й умовами розблокування.

## Джерела
- ⭐ [Wikipedia: Wargroove](https://en.wikipedia.org/wiki/Wargroove) — жанр, 15 командирів, редактори, мультиплеєр, дати й платформи, Wargroove 2.
- [Wargroove Wiki: Rules](https://wargroovewiki.com/Rules) — кодекс гри: groove, крити 1.35–2.5×, захват, дохід 100, найм, підкріплення, щити/черепи, контратака, туман, погода.
- [Unit](https://wargroovewiki.com/Unit), [Commander](https://wargroovewiki.com/Commander), [Dog](https://wargroovewiki.com/Dog), [Cavalry](https://wargroovewiki.com/Cavalry), [Giant](https://wargroovewiki.com/Giant), [Spearman](https://wargroovewiki.com/Spearman), [Mage](https://wargroovewiki.com/Mage), [Mercia](https://wargroovewiki.com/Mercia) — умови критів, ціни, рух, groove.
- [Xbox Wire: Tips and Tricks](https://news.xbox.com/en-us/2019/02/08/wargroove-tips-and-tricks/) — командир як сила й слабкість, кодекс з інфо клітини.
- Steam: пошук «Wargroove»; YouTube: пошук «Wargroove gameplay».

## Непевне
- (?) Множник крита солдата й лучника — сторінки не відкривав; загальний діапазон 1.35–2.5×.
- (?) Умови критів решти юнітів (повітряні, морські, балиста, требушет, злодій, стрілець) — не перевірено, тому не наведено.
- (?) Режими Arcade і Puzzle («перемогти за один хід»), налаштування складності кампанії — за памʼяттю.
- (?) Засідка: «знищення на нейтральній клітині / відкидання на ворожій» — переказ кодексу, механіка неочевидна.
- (?) Wargroove 2: роглайт-режим — за памʼяттю.
- (?) Чи можна скасувати рух до підтвердження дії.
