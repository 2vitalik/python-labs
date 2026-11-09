---
title: Battle Brothers
slug: battle-brothers
aka: [BB, Бойові брати]
family: tactics
also: [roguelike]
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: survive
year: 2017
platforms: [PC, Switch, PS4, PS5, Xbox]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Battle_Brothers", best: true, note: "огляд: найманці, контракти, травми, пермасмерть, кризи, ironman"}
  - {kind: official, url: "https://battlebrothersgame.com/?p=389", note: "Dev Blog #4: ZoC і вільні удари, мораль, висота, overwhelm, голова/тіло, щити, spearwall, riposte"}
  - {kind: official, url: "https://battlebrothersgame.com/character-stats", note: "Game Mechanics 101: характеристики, ініціатива, втома, мораль"}
  - {kind: other, url: "https://battlebrothersgame.com/?p=21868", note: "форум: Automatic Attack and Zone of Control; footwork, rotation, відштовхування"}
  - {kind: other, url: "https://battlebrothersgame.com/?p=4150", note: "форум: удари по тих, хто тікає; втома"}
  - {kind: steam, url: "https://store.steampowered.com/app/365360/Battle_Brothers/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Battle+Brothers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, impassable-cells, floor-types, height-levels, status-effects, permadeath, unit-xp-skills, inventory-items, shop-between-levels, world-map, difficulty-levels, save-game, fog-of-war, threat-range, reachable-highlight, path-preview, message-log, +hex-grid-render, +zone-of-control, +reaction-attack, +action-points, +fatigue-pool, +initiative-queue, +morale-states, +hit-chance, +overwhelm-bonus, +head-body-hitzones, +armor-pools, +shieldwall-stack, +retaliation, +injury-table, +ironman-save, +mercenary-wages]
proposes: ["+trigger:leave_zone", "+trigger:enter_zone", "+trigger:attacked", "+trigger:ally_died", "+trigger:round_start", "+cond:in_zone", "+cond:fatigue", "+effect:free_attack", "+effect:morale_check", "+effect:roll_dice", "+ui:initiative-bar", "+ui:hit-chance", "+ui:morale-icon", "+ui:fatigue-bar", "+window:company-roster", "+window:contract-window", "+window:perk-select", "+window:battle-result", "+feature:roster-carryover", "+axis:turn-structure:initiative-queue"]
author: opus
date: 2026-11-09
---

# Battle Brothers — найманці на гексах, де відійти від ворога коштує удару в спину, а страх ширший за рани

## Суть
Гравець веде загін найманців у світі, схожому на середньовічну Німеччину: бере контракти на світовій мапі, платить людям і годує їх, а бої відбуваються на гексовому полі. Кожен персонаж має очки дій і втому; ворог із мечем тримає **зону контролю** — сусідні гекси, вихід з яких провокує вільний удар: влучив — утікач лишається на місці. **Мораль** падає від ран, загибелі друзів і чисельної переваги ворога — персонаж вагається, потім тікає, і паніка ширяться. Смерть остаточна, травми калічать назавжди; найняти можна лише тих, на кого вистачає грошей — пияків, злодіїв, калік.

## Поле і час
- Бій — гексова мапа з місцевістю (трава, ліс, болото, пагорби різної висоти, перешкоди). Висота дає довший огляд, дальність пострілу вниз і бонус у ближньому бою.
- Видимість: кожен персонаж має дальність огляду; висока точка бачить за перешкоди. Ворог поза оглядом прихований.
- Час — раунди; у раунді **усі** персонажі обох сторін ходять у спільній черзі за ініціативою (за спаданням), без фаз «гравець/ворог». Ініціативу перераховують щораунду з очок дій, накопиченої втоми й типу броні.
- Поза боєм — світова мапа в реальному часі з паузою (?): загін їде між містами, контракти, події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Найманець (brother) | piece | HP; броня голови й тіла; AP; втома (макс. від витривалості й броні); мораль; ініціатива; влучність і захист ближній/дальній; передісторія; перки | рух і дії за AP, втома росте; зона контролю, якщо в руках ближня зброя |
| Ворог (бандити, орки, нежить, гобліни, звірі…) | enemy | ті самі характеристики | ШІ за типом; нежить не знає втоми й моралі |
| Зона контролю (ZoC) | zone | 1 гекс навколо | вихід провокує вільний удар; немає у стрілків, оглушених, утікачів |
| Щит | pickup | бонус захисту | Shieldwall — великий бонус + малий за кожного сусіда з Shieldwall; сокири розколюють щит |
| Списи (Spearwall) | pickup | — | бʼють будь-кого, хто входить у ZoC, і можуть не впустити |
| Однорука / дворука зброя | pickup | вартість AP | однорука — 2 удари за хід, важка дворука — 1 |
| Лук / арбалет | pickup | дальність | постріл потребує лінії бачення; не стріляє, коли в ворожій ZoC |
| Тупа зброя | pickup | — | може оглушити: ціль не діє, але захищається |
| Пагорб (висота) | terrain | рівень | огляд, дальність, бонус/штраф у ближньому бою, шанс удару в голову |
| Болото | terrain | дорожчий рух; штраф захисту в ближньому | — |
| Ліс, трава, дорога | terrain | ціна руху в AP і втомі | ліс заважає огляду (?) |
| Перешкода (камінь, віз, стіна) | static | — | непрохідна; блокує постріли (?) |
| Місто / замок / табір ворога | zone | — | на світовій мапі: найм, крамниці, контракти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(round)` → ТО `custom: «ініціатива кожного = f(AP, втома, броня); черга за спаданням»`.
- КОЛИ `turn_start(unit)` → ТО `custom: «AP поновлено повністю»`, `custom: «втома −фіксована величина»`.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `custom: «AP ≥ ціна шляху і втома + ціна ≤ максимум»` → ТО `move(unit, hex)`, `custom: «−AP, +втома за місцевістю»`.
- КОЛИ `leave(unit, zoc(enemy))` → ТО `custom: «вільний удар власника зони»`; ЯКЩО влучив → ТО `block` (лишається на місці, AP і втому сплачено); промах → `move`. Кожна зона, з якої виходять, бʼє окремо.
- КОЛИ `enter(unit, zoc(spearwall))` → ТО `custom: «удар списом»`; ЯКЩО влучив → ТО `block`.
- КОЛИ `input(shoot, unit, target)` → ЯКЩО `custom: «стрілець у ворожій ZoC»` → ТО `block`; інакше ЯКЩО `line_of_sight(unit, target)` → постріл.
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, reach)` and `prob(влучність a − захист b ± висота + overwhelm)` → ТО `custom: «удар влучив»`.
- КОЛИ `custom: «влучання»` → ТО `custom: «зона: тіло (частіше) або голова (більша шкода)»`, `damage(n)` спершу по броні тієї зони, потім по HP; броня на 0 — знята до кінця бою.
- КОЛИ `custom: «атака з вищої клітини»` → ТО `custom: «бонус до влучання і шансу в голову»`; з нижчої — штраф.
- КОЛИ `custom: «атака по цілі, яку вже атакували цього раунду»` → ТО `custom: «бонус overwhelm за кожного попереднього атакувальника»`; фасінгу нема.
- КОЛИ `input(skill, shieldwall)` → ТО `set_state(unit, shieldwall)`; ЯКЩО `adjacent_count(unit, ally_shieldwall, ≥, 1)` → ТО `custom: «малий бонус захисту за кожного»`.
- КОЛИ `input(skill, riposte)` → ТО `set_state(unit, riposte, 1 round)`; КОЛИ `custom: «ворог промахнувся по unit»` → ЯКЩО `state(unit, riposte)` → ТО `custom: «автоматична контратака»`.
- КОЛИ `custom: «влучання тупою зброєю»` → ЯКЩО `prob(p)` → ТО `stun(b, 1)`; оглушений не має ZoC і не робить вільних ударів.
- КОЛИ `custom: «ворога вбито / союзник загинув / союзник тікає / поранення / оточення»` → ТО `custom: «мораль ±»`.
- КОЛИ `turn_start(unit)` → ЯКЩО `custom: «мораль нижча за базову»` → ТО `custom: «перевірка моралі»`; провал → `set_state(unit, wavering)`; повторний провал → `set_state(unit, fleeing)`.
- КОЛИ `state_on(unit, fleeing)` → ТО `custom: «біжить від ворогів, без ZoC; інші перевіряють мораль»`; ЯКЩО `custom: «поруч нема ворогів»` → ТО `custom: «шанс оговтатися»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`; найманця втрачено назавжди; ЯКЩО `prob(p)` → ТО `custom: «вижив з постійною травмою»` (?).
- КОЛИ `all_gone(enemy)` → ТО `win` бою, `give(company, loot)`; КОЛИ `all_gone(own)` → ТО `lose` (кінець кампанії).
- КОЛИ `input(retreat)` → ЯКЩО `custom: «персонажі на краю мапи»` → ТО `custom: «вийти з бою»` (?).
- КОЛИ `timer(day)` → ТО `currency(−wages)`, `take(company, food)`; ЯКЩО `custom: «нема їжі / грошей»` → ТО `custom: «мораль падає, дезертирство»` (?).
- КОЛИ `custom: «пізня гра»` → ТО `custom: «криза (війна знаті, навала зеленошкірих, нежить)»`; тип першої кризи — налаштування.
- Перемога: умовна — вижити й розбагатіти, здолати кризи · Поразка: загін знищено / зник капітан у деяких походженнях (?) · Рахунок: —.

## Керування і ввід
- Миша: вибір персонажа (той, чия черга), наведення на гекс — шлях і ціна в AP/втомі; клік — рух. Наведення на ворога — шанс влучання й очікувана шкода.
- Панель навичок унизу: атаки зброї, Shieldwall, Spearwall, Riposte, перемкнути зброю, «Wait» (перенести хід на кінець раунду) і «End Turn» (?).
- Камера вільна, перемикання висоти рельєфу (?).
- Світова мапа: клік — їхати; пауза й прискорення часу (?).

## Вікна, меню, HUD
- `main-menu`: Нова кампанія → налаштування кампанії (складність, економіка, перша криза, ironman); Load → `save-slots`; Options → `settings-window`.
- `game-screen` (бій): гекси з висотою, `initiative-bar` (черга раунду), портрет і `stat-panel` активного, `action-points`, `fatigue-bar`, `hp-bar`, броня голови/тіла, `morale-icon`, `ability-buttons`, `hit-chance` при наведенні, `message-log`.
- `map-window` — світова мапа з загоном, містами, ворожими загонами; `contract-window` — опис і плата контракту.
- `company-roster` — склад загону, спорядження (`inventory-window`), перки при новому рівні (`perk-select`).
- `shop-window` — крамниці міст, найм рекрутів з передісторією.
- `battle-result` — здобич, загиблі, травмовані; `end-screen` кампанії.

## Фічі поза полем
- `mode-hardcore` (ironman) — автосейв без вибору слота, без перезавантаження; інакше `save-slots`.
- `roster-carryover` — загін живе всю кампанію; `xp-level` і перки; постійні травми.
- `difficulty-presets` бою й економіки; вибір першої кризи; `seed-input` світу (?).
- `meta-progression` нема; розширення (Lindenwood, Beasts & Exploration, Warriors of the North, Blazing Deserts, Of Flesh and Faith) — нові походження, ворогі, крафт (?).

## Варіації й родичі
- Родичі в корпусі: [Battle for Wesnoth](battle-for-wesnoth.md) (ZOC зупиняє рух, а не бʼє), [Blood Bowl](blood-bowl.md) (вихід із зони — кидок), [XCOM](xcom.md) (мета-кампанія, пермасмерть), [Final Fantasy Tactics](final-fantasy-tactics.md) (порядок за швидкістю).
- Осі варіацій:
  - **зона контролю**: нема / зупиняє (Wesnoth) / кидок на вихід (Blood Bowl) / вільний удар з утриманням при влучанні (Battle Brothers);
  - **черга ходів**: сторона за стороною / спільна черга за ініціативою, що залежить від втоми;
  - **виснаження**: нема / втома як другий ресурс поряд з AP;
  - **мораль**: нема / стани до втечі з поширенням паніки;
  - **позиція**: фасінг (FFT) / overwhelm без фасінгу (BB).

## Цікавинки для курсу
- Вільний удар при виході з ZoC з утриманням на місці — 📎 (подія на `leave` і переривання руху).
- Спільна черга ініціативи, що перераховується з AP і втоми щораунду — 📎.
- AP + втома: два ресурси на кожну дію, втома відновлюється частково — 🌱.
- Мораль як автомат станів (впевнений → вагається → тікає) з тригерами від подій поруч і ланцюговою панікою — 🥉.
- Броня двома пулами (голова/тіло), що поглинає першою — 🌱.
- Overwhelm: бонус за кожного попереднього атакувальника тієї ж цілі — 🌱.
- Світова мапа з контрактами, зарплатою й їжею — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ стрільці без ZoC і без пострілів у ZoC · `impassable-cells`, `floor-types` ↔ болото, ліс · `height-levels` ↔ висота з бонусами · `status-effects` ↔ оглушення, вагання · `permadeath` · `unit-xp-skills` ↔ рівні й перки · `inventory-items` · `shop-between-levels` ↔ крамниці міст · `world-map` · `difficulty-levels` · `save-game` · `fog-of-war` ↔ дальність огляду · `threat-range`, `reachable-highlight`, `path-preview` · `message-log`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` (уже в корпусі) зі слотом {effect: free_attack, hold_on_hit}.
  - `+reaction-attack` «Атака-реакція» · entities/combat · 📎 — вільний удар, spearwall, riposte.
  - `+action-points`, `+hit-chance`, `+retaliation`, `+injury-table` — як у корпусі.
  - `+fatigue-pool` «Втома» · entities/state · 🌱 · слот {max_by_armor, recover}.
  - `+initiative-queue` «Спільна черга ініціативи» · game-logic/opponent · 📎.
  - `+morale-states` «Мораль і втеча» · entities/state · 🥉 · слот {states, triggers, spread}.
  - `+overwhelm-bonus` «Бонус за повторну атаку цілі» · entities/combat · 🌱.
  - `+head-body-hitzones` «Зони влучання» · entities/combat · 🌱.
  - `+armor-pools` «Броня як окремий пул» · entities/state · 🌱.
  - `+shieldwall-stack` «Стіна щитів» · entities/combat · 🌱 — бонус за сусідів у тому ж стані.
  - `+ironman-save` «Ironman» · game-logic/save · 🌱.
  - `+mercenary-wages` «Утримання загону» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:leave_zone` / `+trigger:enter_zone` — вихід із / вхід у зону іншої сутності (ZoC, spearwall).
- `+trigger:attacked` — початок атаки як подія; `+trigger:ally_died` — загинув союзник поруч (мораль).
- `+trigger:round_start` — початок раунду спільної черги (не `turn_start` сторони).
- `+cond:in_zone` — сутність у зоні контролю ворога; `+cond:fatigue` — втома нижча за поріг.
- `+effect:free_attack` — вільний удар поза чергою; `+effect:morale_check` — кидок моралі зі зміною стану; `+effect:roll_dice`.
- `+ui:initiative-bar` · `+ui:hit-chance` · `+ui:morale-icon` · `+ui:fatigue-bar`.
- `+window:company-roster` · `+window:contract-window` · `+window:perk-select` · `+window:battle-result`.
- `+feature:roster-carryover` — загін і його травми живуть усю кампанію.
- `+axis:turn-structure:initiative-queue` — нове значення осі: спільна черга обох сторін за ініціативою.

## Джерела
- ⭐ [Wikipedia: Battle Brothers](https://en.wikipedia.org/wiki/Battle_Brothers) — найманці, контракти, травми, пермасмерть, кризи, ironman, дати й платформи.
- [Dev Blog #4: тактичний бій](https://battlebrothersgame.com/?p=389) — ZoC і вільні удари, ініціатива, мораль, висота, overwhelm, голова/тіло, броня, щити, spearwall, riposte, оглушення.
- [Game Mechanics 101: Character Stats](https://battlebrothersgame.com/character-stats) — AP, втома, ініціатива, мораль, пермасмерть.
- [Форум: Automatic Attack and Zone of Control](https://battlebrothersgame.com/?p=21868) і [форум: атаки по тих, хто тікає](https://battlebrothersgame.com/?p=4150) — footwork, rotation, відштовхування щитом.
- [Steam](https://store.steampowered.com/app/365360/Battle_Brothers/).
- YouTube: пошук «Battle Brothers gameplay».

## Непевне
- (?) Усі числа (AP 9, ціни руху, відновлення втоми, бонуси висоти й overwhelm, шанс удару в голову) — офіційні тексти чисел не дають, fandom-вікі агенту закрита.
- (?) Назви станів моралі (Confident / Steady / Wavering / Breaking / Fleeing) — за памʼяттю; dev blog каже лише «wavering → panic and flee».
- (?) Шанс вижити при HP 0 з постійною травмою, дія «Wait», відступ з бою через край мапи — за памʼяттю.
- (?) Зарплата щодня, їжа, дезертирство; світова мапа в реальному часі з паузою — за памʼяттю.
- (?) Список розширень і що вони додають.
- (?) Чи блокують перешкоди постріли (dev blog не описує, як снаряди взаємодіють з перешкодами чи союзниками на лінії).
