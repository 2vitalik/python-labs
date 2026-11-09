---
title: Heroes of Might and Magic III (Герої меча і магії III)
slug: heroes-of-might-and-magic-3
aka: [HoMM3, Heroes 3, H3, Heroes III, "Герої 3", "Герои меча и магии 3", "The Restoration of Erathia"]
family: tactics
also: [build-sim]
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1999
platforms: [PC, Mac, Linux, iOS, Android, GBC]
links:
  - {kind: other, url: "https://heroes.thelazy.net/index.php/Combat", best: true, note: "Heroes 3 wiki: поле 15×11 гексів, фази раунду, wait/defend, тактична фаза, втеча/капітуляція, облога"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Heroes_of_Might_and_Magic_III", note: "загальний опис: карта пригод, міста, 8 фракцій, гекс-бій, кампанії, hot-seat, доповнення"}
  - {kind: other, url: "https://heroes.thelazy.net/index.php/Damage", note: "формула шкоди: стек ≤10 / >10, атака−захист ±5 %/2,5 %, удача, штрафи стрільців"}
  - {kind: other, url: "https://heroes.thelazy.net/index.php/Retaliation", note: "контратака раз на раунд; грифони 2, королівські — без ліміту; істоти «без відповіді»"}
  - {kind: other, url: "https://heroes.thelazy.net/index.php/Morale", note: "мораль −3…+3, шанси дії/паніки, штраф за змішані фракції"}
  - {kind: other, url: "https://heroes.thelazy.net/index.php/War_Machine", note: "балиста, намет першої допомоги, візок з набоями, катапульта"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Heroes+3+combat+gameplay", note: "пошук; геймплей бою"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, piece-move-patterns, legal-move-highlight, reachable-highlight, destroy-all-enemies, ai-opponent, hot-seat, difficulty-levels, save-game, in-game-editor, world-map, inventory-items, status-effects, turn-enforcement, threat-range, +hex-grid-render, +unit-stack-count, +retaliation, +speed-turn-order, +wait-turn, +defend-action, +morale-states, +hidden-luck, +damage-formula, +ranged-penalties, +ammo-limit, +flying-move, +multi-cell-unit, +hero-spell-per-round, +war-machines, +siege-walls, +tactics-deployment, +retreat-surrender, +hero-skills, +mana-pool-spells, +auto-battle]
proposes: ["+trigger:attacked", "+trigger:round_start", "+effect:counterattack", "+effect:wait", "+effect:defend", "+cond:retaliation_left", "+role:stack", "+role:war-machine", "+ui:stack-count", "+ui:turn-order-bar", "+ui:damage-forecast", "+window:spellbook", "+window:creature-info", "+window:battle-result", "+axis:actors=stack"]
author: opus
date: 2026-11-09
---

# Heroes of Might and Magic III — бій стеків на гексах: «скільки × яка істота», контратака раз на раунд

## Суть
Стратегія з двома шарами: карта пригод (герої ходять, збирають ресурси, будують міста) і **тактичний бій** на гекс-полі — тут описано лише бій. Кожна армія — до 7 **стеків** (?): «N істот одного виду» діють як одна фігура, шкода росте з кількістю, а втрати — це вбиті істоти зі стеку. Порядок дій — за швидкістю, кожен стек раз на раунд **контратакує** у відповідь на ближню атаку, тож головна тактика — «зняти відповідь» дрібним стеком і вдарити великим. Герой стоїть збоку поля: дає атаку/захист армії і раз на раунд кастує заклинання.

## Поле і час
- Поле бою — **15 стовпців × 11 рядів гексів**; армії стоять у крайніх стовпцях (розстановка Loose / Tight або вручну в тактичній фазі).
- Перешкоди на полі (камені, дерева) непрохідні для піших (?); облога додає мури, рів, ворота і вежі.
- Раунд — усі стеки обох сторін по черзі за швидкістю, у три фази: початкова (+Defend), фаза моралі й «чекання» (Wait), чекання — у зростаючому порядку швидкості.
- Повна інформація: видно кількість, характеристики й заклинання на стеках ворога.
- Випадковість: діапазон шкоди істоти, удача (подвійна шкода), мораль (зайва дія / паніка), шанс спецздібностей.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стек істот | piece | кількість N, Attack, Defense, Damage min–max, HP, Speed, мораль, удача | рух на Speed гексів, атака; шкода = сума по N; втрати знімають цілих істот |
| Стрілець (лучники, маги, титани…) | piece | Shots (набої) | стріляє через поле; поруч ворог → лише ближній удар зі штрафом ½ (крім винятків) |
| Літаюча істота | piece | flying | перелітає перешкоди й мури облоги |
| Велика істота (2 гекси) | piece | 2-гексова | займає два гекси, атакує з будь-якого (?) |
| Грифон / Королівський грифон | piece | 2 / ∞ контратаки | відповідає двічі / завжди |
| Істоти «без відповіді» (наги, вампіри, гідри…) | piece | no retaliation | атакують, не отримуючи контратаки |
| Нежить / Голем / Елементаль | piece | мораль = 0 | не підлягають моралі |
| Герой | ally | Attack, Defense, Spell Power, Knowledge, мана, навички | не на полі; раз на раунд — заклинання; бонуси до стеків |
| Балиста | object | 250 HP, швидкість 0, 24 постріли | стріляє в кінці раунду; Artillery — керування |
| Намет першої допомоги | object | 75 HP | лікує верхню істоту стеку; першa допомога — вибір цілі |
| Візок з набоями | object | 100 HP | поки цілий — набої стрільців нескінченні |
| Катапульта | object | 1000 HP, 24 постріли | лише в облозі, бʼє мури раз на хід; Ballistics — вибір цілі |
| Мур / ворота | static | міцність | блокує піших; катапульта/Earthquake руйнують |
| Рів | hazard | — | тримає атакувальника щонайменше раунд |
| Вежа міста | enemy | — | стріляє першою в раунді, ігнорує штраф дальності і Defense цілі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(stack)` → ЯКЩО `custom: «мораль < 0»` і `prob(1/12 | 1/6 | 1/4)` → ТО `skip_turn(stack)` (паніка).
- КОЛИ `input(move, stack, hex)` → ЯКЩО `path_exists(stack, hex)` у межах Speed (літаючі — напряму) → ТО `move`.
- КОЛИ `input(melee, stack, target)` → ЯКЩО `adjacent(stack, target)` після руху → ТО `damage(target, dmg)`; ЯКЩО `custom: «у цілі лишилась контратака»` і ціль жива → ТО `custom: «контратака по атакувальнику»`, `counter(retaliations, −1)`.
- КОЛИ `phase_start(round)` → ТО `counter(retaliations, =1)` для всіх (грифони 2, королівські грифони ∞).
- КОЛИ `input(shoot, stack, target)` → ЯКЩО `counter(shots, >, 0)` і `not occupied(adjacent_hex, enemy)` → ТО `damage(target, dmg)`, `counter(shots, −1)`; контратаки нема.
- Шкода: `custom: «база = сума випадкових Damage по N (N > 10: 10 кидків × N/10); × (1 + 0,05·(A−D)) до +300 % або × (1 − 0,025·(D−A)) до −70 %; × навички Offense/Archery/Armorer»`.
- КОЛИ стрілець бʼє → ЯКЩО `custom: «до цілі ≥ 10 гексів»` або `custom: «ціль за муром»` → ТО `custom: «шкода × 0,5 (кожен штраф окремо)»`.
- КОЛИ `custom: «атака»` → ЯКЩО `prob(luck: 1/24 · luck)` → ТО `multiplier(×2)` до шкоди.
- КОЛИ `custom: «стек завершив дію»` → ЯКЩО `custom: «мораль > 0»` і `prob(1/24 | 1/12 | 1/8)` і `first_time` за раунд → ТО `extra_move`.
- КОЛИ `custom: «стек отримав шкоду n»` → ТО `custom: «вбито ⌊(n − HP верхньої) / HP⌋ + …; верхня істота лишається з залишком HP»`; КОЛИ `counter(N, ==, 0)` → ТО `disappear_a`.
- КОЛИ `input(wait, stack)` → ТО `custom: «стек переходить у фазу чекання (діє пізніше, від повільних до швидких)»`.
- КОЛИ `input(defend, stack)` → ТО `set_state(stack, defending, 1)` (+20 % Defense), `end_turn`; висока мораль після цього в тій самій фазі не спрацьовує.
- КОЛИ `input(cast, hero, spell)` → ЯКЩО `first_time` за раунд і `counter(mana, ≥, cost)` → ТО `custom: «ефект заклинання»` (шкода, бафи, Blind, Teleport…), `counter(mana, −cost)`; каст — одразу після активації свого стеку.
- КОЛИ `state_on(stack, blind|paralyzed|stone)` → ТО `skip_turn(stack)`; контратака по ньому слабша (Blind ½, параліч ¼).
- КОЛИ `custom: «кінець раунду»` → ТО `custom: «балиста стріляє»`, намет — `heal(top_creature, n)`.
- КОЛИ `phase_start(round)` → ЯКЩО `mode(siege)` → ТО `custom: «вежі стріляють (центр, верх, низ), потім катапульта бʼє мур»`; КОЛИ `hp_zero(wall)` → ТО `set_cell(wall, rubble)`.
- КОЛИ `enter(stack, moat)` → ТО `custom: «рух зупиняється, стек стоїть у рові до наступного раунду»`.
- Тактична фаза: ЯКЩО `custom: «Tactics героя вища»` → ТО `custom: «розставити свої стеки у кількох стовпцях перед боєм»`; рівні рівні → фази нема.
- КОЛИ `input(retreat, hero)` → ЯКЩО `not custom: «Shackles of War / оборона міста»` → ТО `custom: «герой тікає з артефактами, армія втрачена, досвіду нема»`.
- КОЛИ `input(surrender, hero)` → ЯКЩО `custom: «бій герой проти героя»` → ТО `currency(−½ вартості найму армії)`, армія зберігається (ворог може відмовити).
- КОЛИ `all_gone(enemy_stacks)` → ТО `win`; переможець отримує досвід і артефакти переможеного героя (?).
- Поразка: знищено всі стеки, втеча або капітуляція · Рахунок: досвід героя за вбитих.

## Керування і ввід
- Курсор-підказка змінює форму: стрілка руху, меч з напрямком удару (з якого гекса бити), лук (зламаний — ½ шкоди), заборона.
- Активний стек підсвічено, досяжні гекси затемнено; ПКМ на стеку — вікно характеристик істоти.
- Кнопки: Wait · Defend · Cast (книга заклинань) · Retreat · Surrender · Auto-combat · Options.
- Тактична фаза — перетягування стеків у зоні розстановки; кнопка «почати бій».

## Вікна, меню, HUD
- `main-menu`: New Game (Single Scenario / Campaign / Multiplayer) · Load · High Scores · Credits · Quit.
- `game-screen` (карта пригод) → `custom-window` «Battle»: поле 15×11, `selection-highlight` активного стеку, `legal-move-highlight` / `reachable-highlight`, цифра кількості біля кожного стеку (`+ui:stack-count`), `message-log` знизу (хто кого вдарив, скільки вбито), портрети героїв по боках, кнопки дій.
- `custom-window` «Spellbook» (`+window:spellbook`): закладки шкіл магії, сторінки, ціна мани.
- `custom-window` «Creature info» (`+window:creature-info`): Attack/Defense/Shots/Damage/HP/Speed, мораль, удача, активні заклинання.
- `confirm-dialog` — капітуляція з ціною; `end-screen` бою (`+window:battle-result`): втрати обох сторін, досвід.
- `settings-window`: швидкість анімації бою, авто-бій, сітка гексів вкл/викл (?).
- Переходи: карта пригод → (зустріч з армією) бій → результат → карта.

## Фічі поза полем
- Карта пригод (квадратна сітка з підземним шаром): герої з очками руху, шахти, міста з будівлями, найм істот — окрема стратегічна гра (не описується тут).
- Розвиток героя: рівні, первинні характеристики, вторинні навички (Tactics, Archery, Offense, Armorer, Artillery, Ballistics, First Aid, Diplomacy…), артефакти.
- Режими: кампанії, окремі сценарії (50 skirmish-мап), `hotseat`, мультиплеєр, генератор випадкових мап (з Armageddon's Blade), редактор мап (?).
- Авто-бій, `difficulty-presets`, `save-slots`.

## Варіації й родичі
- Серія: King's Bounty (1990, предок), HoMM I–II (менше фракцій), IV (герої на полі), V–VII; доповнення AB, SoD, Horn of the Abyss (фанатське, нові фракції, зміни удачі); HoMM3 HD+ (одночасні ходи).
- Родичі на гекс-бою стеків: King's Bounty: The Legend, Age of Wonders, Disciples (без гексів), Songs of Conquest; у корпусі — [Battle for Wesnoth](battle-for-wesnoth.md), [Chaos](chaos-battle-of-wizards.md) (маг-кастер).
- **Осі варіацій**: фігура — один юніт / стек N × істота (шкода й HP масштабуються з N) · відповідь — нема / раз на раунд / ∞ · порядок — сторона за стороною / за швидкістю з wait · командир — на полі ([Wargroove](wargroove.md)) / поза полем з закляттям раз на раунд.

## Цікавинки для курсу
- Стек як фігура: N × HP з «верхньою» пораненою істотою; шкода знімає цілих істот — 🥉.
- Формула шкоди: сума кидків до 10, потім масштаб N/10; атака−захист з асиметричними капами — 📎.
- Черга дій за швидкістю + Wait (у зворотному порядку) + Defend — 🥉.
- Контратака раз на раунд і винятки (2, ∞, «без відповіді») — 📎.
- Мораль і удача: ймовірнісні зайва дія / паніка / подвійна шкода — 🌱.
- Стрілець: набої, блокування сусідом, штраф дальності 10 гексів і муру — 📎.
- Облога: мур з міцністю, катапульта, рів-пастка, вежі першими — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `piece-move-patterns` (Speed, політ) · `legal-move-highlight` + `reachable-highlight` · `threat-range` (?) · `destroy-all-enemies` · `ai-opponent` · `hot-seat` · `turn-enforcement` · `difficulty-levels` · `save-game` · `in-game-editor` (?) · `world-map` (карта пригод) · `inventory-items` (артефакти) · `status-effects` (Blind, параліч, бафи).
- **Нема** → пропозиції карток:
  - `+unit-stack-count` «Стек: N однакових у клітині, шкода і втрати від N» · entities/state · 🥉.
  - `+retaliation` / `+speed-turn-order` / `+wait-turn` / `+morale-states` / `+hidden-luck` — уже пропонувались у корпусі.
  - `+defend-action` «Захист: бонус до Defense і кінець ходу» · game-logic/turns · 🌱.
  - `+damage-formula` «Формула шкоди атака−захист з капами» · entities/combat · 📎.
  - `+ranged-penalties` «Штрафи стрільця: дальність, сусід, мур» · entities/combat · 📎.
  - `+multi-cell-unit` «Двогексова істота» — близька до `multi-cell-size`.
  - `+hero-spell-per-round` «Командир поза полем: одне закляття за раунд» · game-logic/turns · 📎.
  - `+war-machines` «Нерухомі машини з власним ходом наприкінці раунду» · entities/state · 📎.
  - `+siege-walls` «Облога: мури, рів, вежі, катапульта» · game-logic/legality · 🥈.
  - `+tactics-deployment` «Розстановка перед боєм за перевагою навички» · interface/windows · 📎.
  - `+retreat-surrender` «Втеча / викуп армії» · game-logic/end · 🌱.

## Пропозиції до словників
- `+trigger:attacked` — сутність атакована (контратака, реакції).
- `+trigger:round_start` — початок раунду (скинути лічильники відповідей).
- `+effect:counterattack` — відповідь захисника.
- `+effect:wait` — відкласти дію в кінець черги раунду; `+effect:defend` — захисна стійка до наступної дії.
- `+cond:retaliation_left` — у захисника лишилась контратака.
- `+role:stack` — фігура «N однакових істот» з кількістю як параметром.
- `+role:war-machine` — нерухомий обʼєкт-учасник бою з власним ходом.
- `+ui:stack-count` — число кількості біля фігури; `+ui:turn-order-bar` — черга ходу (є в HD/HotA (?)); `+ui:damage-forecast` — оцінка вбитих під курсором (HotA (?)).
- `+window:spellbook` — книга заклинань зі школами; `+window:creature-info` — картка істоти; `+window:battle-result` — підсумок бою.
- `+axis:actors=stack` — фігура як група однакових.

## Джерела
- ⭐ [Heroes 3 wiki: Combat](https://heroes.thelazy.net/index.php/Combat) — поле 15×11 гексів, фази, wait/defend, мораль, тактична фаза, втеча/капітуляція, облога, балиста й намет діють останніми.
- [Wikipedia: HoMM III](https://en.wikipedia.org/wiki/Heroes_of_Might_and_Magic_III) — шари гри, фракції, гекс-бій із закляттями, кампанії, 50 skirmish-мап, hot-seat, доповнення, порти.
- [Heroes 3 wiki: Damage](https://heroes.thelazy.net/index.php/Damage) — формула, капи +300 % / −70 %, удача, штрафи стрільців ½.
- [Heroes 3 wiki: Retaliation](https://heroes.thelazy.net/index.php/Retaliation) — раз на раунд, грифони, «без відповіді».
- [Heroes 3 wiki: Morale](https://heroes.thelazy.net/index.php/Morale) — шанси, змішані фракції, нежить.
- [Heroes 3 wiki: War Machine](https://heroes.thelazy.net/index.php/War_Machine) — параметри балисти, намету, візка, катапульти.
- YouTube: пошук «Heroes 3 combat gameplay».

## Непевне
- (?) Ліміт 7 стеків в армії — з памʼяті.
- (?) Великі (двогексові) істоти й перешкоди на полі — з памʼяті, сторінка Combat Grids не відкрилась (404).
- (?) Чи є в оригіналі (без HD/HotA) панель черги ходу та прогноз шкоди — з памʼяті: в оригіналі нема.
- (?) Редактор мап у базовій грі — Wikipedia його не описує (з памʼяті — є).
- (?) Пункти головного меню й налаштувань — з памʼяті.
- (?) Розподіл шкоди по істотах стеку — загальний принцип (верхня істота з залишком HP), точний алгоритм не перевірено.
