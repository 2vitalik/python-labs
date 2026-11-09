---
title: The Eye of Judgment
slug: eye-of-judgment
aka: [EoJ, "THE EYE OF JUDGMENT: BIOLITH REBELLION", "The Eye of Judgment 神託のウィザード (PSP)"]
family: tower-lanes
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: territory
year: 2007
platforms: [PS3, PSP]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Eye_of_Judgment", best: true, note: "мат 3×3, стихії полів і перевертання, ±2 життя, мана +2/хід, орієнтація істоти, 5 з 9, PlayStation Eye і CyberCode"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/THE_EYE_OF_JUDGMENT", note: "JA: фази ходу, обовʼязкова атака при виклику, контратака, слабкий бік, магічні атаки, виклик поруч зі своїми, «шах» на 4 полях, колода 30, рука ≤ 7"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Eye+of+Judgment+gameplay", note: "пошук; геймплей з AR-картами"}
stage: v1
coverage: 60
mechanics: [hp-damage, cursor-place, threat-range, ai-opponent, online-multiplayer, hot-seat, mode-select, codex-window, +deck-draw, +mulligan-redraw, +hand-limit, +facing-hit-bonus, +armor-by-facing, +retaliation, +summon-adjacent, +elemental-field-bonus, +field-flip, +forced-attack-on-summon, +rotate-costs-action, +control-n-cells-win, +check-warning, +friendly-fire, +ar-card-recognition, +physical-card-input, +mana-on-death, +deck-out-lose]
proposes: ["+effect:draw_card", "+effect:flip_field", "+trigger:summoned_in_range", "+cond:element_match", "+cond:attack_from", "+role:card", "+ui:camera-feed", "+ui:attack-arrows", "+window:card-profile", "+window:camera-calibration", "+feature:physical-cards", "+card:ar-card-recognition", "+card:forced-attack-on-summon", "+card:control-n-cells-win"]
author: opus
date: 2026-11-09
---

# The Eye of Judgment — фізичні карти на маті 3×3 під камерою PS3: стихія клітинки, напрям погляду істоти, хто тримає 5 з 9 — перемагає

## Суть
Колекційна картярка, де карти справжні: гравці кладуть їх на килимок 3×3, а камера PlayStation Eye зчитує код на карті й «оживляє» істоту на екрані. Кожне поле має стихію (вогонь, вода, земля, дерево, Biolith) — своя стихія дає істоті +2 життя, протилежна −2. Істота має **орієнтацію**: атакує у свої напрямки, слабша з боків і ззаду, поворот коштує ману. Перемагає той, хто наприкінці ходу тримає **5 з 9 полів**.

## Поле і час
- Поле — 3×3, дев'ять полів; у кожного поля основна стихія і другорядна на ребрі, що вмикається, коли поле **перевертають** карткою.
- Протилежності: вогонь ↔ вода, земля ↔ дерево; Biolith нейтральний; в офіційному розкладі центр — завжди Biolith. У casual — випадкові або неофіційні розклади.
- Поле контролює гравець, чия істота на ньому стоїть; одна істота на поле.
- Хід почерговий: добір → +2 мани → фаза дій 1 (закляття, повороти, повторні атаки, заміни — у будь-якому порядку) → фаза дій 2 (один звичайний виклик) → перевірка кінця ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Істота | piece (`+role:card`) | стихія (вогонь, вода, земля, дерево, машина, без стихії), життя, атака, зона атаки, слабкий бік, ціна | стоїть на полі з орієнтацією; атакує при виклику й за повторною дією |
| Поле-стихія | terrain | основна + другорядна стихія | своя стихія: +2 життя; протилежна: −2 (≤ 2 → загибель) |
| Поле Biolith | terrain | — | нейтральне |
| Машина / без стихії | piece | — | ігнорують бонус і штраф поля |
| Закляття: мана · стихійне · Grand Magic · звичайне | object | ціна | маніпуляції маною · атака певної стихії · сильний ефект, що завершує хід · інше (у т. ч. перевертання поля) |
| Мана | resource | +2 на початку ходу, +1 за смерть своєї істоти | платить за виклик, закляття, поворот, повторну атаку |
| Колода · рука · скид | zone | колода 30 (≤ 3 копії номера), рука 5 на старті, ≤ 7 наприкінці ходу | порожня колода при доборі — поразка |
| Мат і камера | — | CyberCode на картах | карту на маті — виклик; жести гравця — дії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен бере 5 карт; один муліган»`; перший гравець пропускає добір першого ходу.
- КОЛИ `turn_start(side)` → ТО `custom: «draw_card ×1»`, потім `currency(+2)` (мана).
- КОЛИ `custom: «добір з порожньої колоди»` → ТО `lose`.
- КОЛИ `input(summon, creature, field)` → ЯКЩО `custom: «фаза дій 2, звичайний виклик ще не робили»` and `free(field)` and (`adjacent_count(field, own_creature, >=, 1)` or `count(own_creatures, ==, 0)`) and `counter(mana, >=, cost)` → ТО `place(player, creature)`, `face(creature, dir_on_mat)`, `counter(mana, -cost)`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «стихія поля = стихія істоти»` → ТО `hp(creature, +2)`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «стихія поля протилежна»` → ТО `hp(creature, -2)`; ЯКЩО `custom: «життя ≤ 2»` → ТО `disappear(creature)`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «ворожа істота в зоні атаки»` → ТО `damage(targets, attack)` — атака при виклику обовʼязкова.
- КОЛИ `custom: «фізична атака на ціль»` → ЯКЩО `custom: «атакують зі слабкого боку цілі»` → ТО `damage(target, attack + bonus)`.
- КОЛИ `custom: «фізична атака на ціль»` → ЯКЩО `in_range(target, attacker, зона атаки цілі)` and `custom: «ціль вижила»` → ТО `damage(attacker, target_attack)` — контратака.
- КОЛИ `custom: «магічна атака»` → ТО `damage(target, attack)`; `custom: «ігнорує ухилення й захист, без контратаки, без бонусу за слабкий бік»`.
- КОЛИ `custom: «атака по площі»` → ТО `damage(all_in_area, attack)` — свої теж; свої не контратакують.
- КОЛИ `input(rotate, creature)` → ЯКЩО `custom: «фаза дій 1»` and `custom: «ця істота цього ходу ще не діяла»` and `counter(mana, >=, cost)` → ТО `rotate(creature, 90)`.
- КОЛИ `input(reattack, creature)` → ЯКЩО `custom: «ця істота цього ходу ще не діяла»` and `counter(mana, >=, cost)` → ТО `custom: «атака як при виклику»`.
- КОЛИ `input(replace, creature)` → ЯКЩО `counter(mana, >=, cost)` → ТО `transform(old, new)`; нова цього ходу не діє, хід не закінчується.
- КОЛИ `hp_zero(creature)` → ТО `disappear(creature)`, `custom: «поле вільне»`, власник `currency(+1)`.
- КОЛИ `input(spell, flip, field)` → ТО `custom: «flip_field: активна стихія поля = другорядна»`.
- КОЛИ `input(spell, grand_magic)` → ТО `custom: «ефект»`, `end_turn` (фаза 2 пропускається).
- КОЛИ `input(summon, restricted_creature)` → ЯКЩО `count(creatures_on_mat, <, 4)` → ТО `block`.
- КОЛИ `turn_end(side)` → ЯКЩО `count(hand, >=, 8)` → ТО `custom: «скинути до 7»`.
- КОЛИ `turn_end(side)` → ЯКЩО `count(own_fields, ==, 4)` → ТО `message(«check»)` — суперник мусить знищити істоту.
- КОЛИ `turn_end(side)` → ЯКЩО `count(own_fields, >=, 5)` → ТО `win`; суперник `lose`.
- Перемога: 5 з 9 полів наприкінці ходу · Поразка: суперник тримає 5 або порожня колода · Рахунок: —.

## Керування і ввід
- Фізичний ввід: покласти карту на поле мату під камерою — виклик; кут, під яким лежить карта, — орієнтація істоти.
- Жести перед камерою — дії; повернути карту на маті — поворот (за ману), перекласти — переміщення/заміна.
- Карти заклинань показують камері; онлайн — колода реєструється, добір випадковий з її даних.
- PSP-версія: цифрові карти без камери.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: проти CPU, на двох за одним матом, онлайн (до 30.09.2010), «Камінь-ножиці-папір» для дітей; ranked — лише офіційний розклад.
- `game-screen`: `+ui:camera-feed` — відео мату з 3D-істотами поверх карт; мана обох, рука, контрольовані поля, `+ui:attack-arrows` — зони атаки й слабкий бік.
- `+window:card-profile` (Profile mode) — підняти карту до камери: статистика і здібності; «тицьнути» істоту — атака-демо (`codex-window`).
- `+window:camera-calibration` (?) — налаштування камери й мату.
- `end-screen` — 5 з 9, переможець.

## Фічі поза полем
- `+feature:physical-cards` — колекція фізичних карт з кодами: сети 1 (110), 2 (100), 3 (101, з них 100 у грі).
- `hotseat`-партія за одним матом, `online-multiplayer` (зареєстровані колоди), `ai-opponent-levels` (?).
- `custom-rules`: casual-розклади полів (випадкові/неофіційні) проти офіційного в ranked.
- PSP (神託のウィザード): 20 глав сюжету, вільна гра, 342 цифрові карти.

## Варіації й родичі
- Родичі в корпусі: [inscryption](inscryption.md) (карти проти карт на сітці), [mega-man-battle-network](mega-man-battle-network.md) (чіпи на 3×3 половинах), [mythgard](mythgard.md), [marvel-snap](marvel-snap.md) (контроль більшості зон).
- Поза корпусом: Triple Triad (FF VIII: 3×3, сторони карти, стихії клітин), хрестики-нулики як «5 з 9» без бою.
- **Осі варіацій**: напрям атаки — без орієнтації / фіксовані стрілки / поворот за ресурс · поле — нейтральне / стихійне / перевертається · мета — HP гравця / більшість клітин / ряд · ввід — тач / миша / фізична карта під камерою.

## Цікавинки для курсу
- Орієнтація + слабкий бік + контратака в зоні: одна істота = патерн атаки, що обертається — 🥉.
- Стихія клітини ±2 життя з миттєвою смертю при ≤ 2 — 📎 (`floor-types` для карт).
- Виклик лише поруч зі своїми + обовʼязкова атака при виклику — 📎.
- «5 з 9 наприкінці ходу» і попередження «check» на 4 — 🌱.
- Перевертання поля на другорядну стихію — 🌱.
- AR-зчитування коду з фізичної карти (OpenCV + ArUco як аналог CyberCode) — 🥇.

## Мапа на каталог
- Є: `hp-damage` · `cursor-place` ↔ карта на поле · `threat-range` ↔ зони атаки · `ai-opponent`, `hot-seat`, `online-multiplayer` · `mode-select` · `codex-window` ↔ Profile mode.
- **Нема** → пропозиції карток:
  - `+deck-draw`, `+mulligan-redraw`, `+hand-limit`, `+facing-hit-bonus`, `+armor-by-facing`, `+retaliation`, `+summon-adjacent`, `+friendly-fire` — уже в корпусі.
  - `+elemental-field-bonus` «Стихія клітини ±життя істоти, смерть за порогом» · entities/state · 📎.
  - `+field-flip` «Клітина має другу стихію, що вмикається карткою» · entities/state · 🌱.
  - `+forced-attack-on-summon` «Атака при виклику обовʼязкова, якщо є ціль» · entities/combat · 📎.
  - `+rotate-costs-action` «Поворот фігури — дія за ресурс» · entities/move · 🌱.
  - `+control-n-cells-win` «Перемога — N клітин під контролем наприкінці ходу» · game-logic/win · 🌱; `+check-warning` «Попередження за крок до перемоги» · 🌱.
  - `+ar-card-recognition` «Камера зчитує код фізичної карти» · interface/input · 🥇; `+physical-card-input` · 🥈.
  - `+mana-on-death` «+1 мана власнику за загибель істоти» · 🌱; `+deck-out-lose` «Порожня колода при доборі — поразка» · 🌱.

## Пропозиції до словників
- `+effect:draw_card` — взяти карту (повтор).
- `+effect:flip_field` — поле перемикає активну стихію.
- `+trigger:summoned_in_range` — істоту викликано, і в її зоні є ворог (сьогодні — `spawned` + `custom`).
- `+cond:element_match` — стихія поля збігається / протилежна стихії істоти.
- `+cond:attack_from` — атака прийшла з боку (фронт / бік / тил).
- `+role:card` — повтор.
- `+ui:camera-feed` — живе відео поля з накладеними моделями; `+ui:attack-arrows`.
- `+window:card-profile` — картка на весь екран через камеру; `+window:camera-calibration`.
- `+feature:physical-cards` — колекція фізичних карт як ввід.
- `+card:ar-card-recognition`, `+card:forced-attack-on-summon`, `+card:control-n-cells-win`.

## Джерела
- ⭐ [Wikipedia: The Eye of Judgment](https://en.wikipedia.org/wiki/The_Eye_of_Judgment) — мат 3×3, основна й другорядна стихії, перевертання, протилежності, ±2 і смерть при ≤ 2, центр Biolith, мана +2/хід і +1 за смерть, оплата виклику/закляття/атаки/повороту, 5 з 9, PlayStation Eye і CyberCode, Profile mode, режим «Камінь-ножиці-папір», сети й дати.
- [Wikipedia JA: THE EYE OF JUDGMENT](https://ja.wikipedia.org/wiki/THE_EYE_OF_JUDGMENT) — фази дій 1/2, повторна дія (поворот або атака), заміна, виклик поруч зі своїми, обмежений виклик (≥ 4 істот), обовʼязкова атака при виклику, контратака, слабкий бік, магічні й площинні атаки, check на 4, колода 30, рука 5 + муліган, ≤ 7, порожня колода — поразка, PSP-версія.
- YouTube: пошук «Eye of Judgment gameplay».

## Непевне
- (?) Конкретні ціни виклику, повороту й повторної атаки — у джерелах лише «коштує ману».
- (?) Форми зон атаки (стрілки на карті) і розмір бонусу за слабкий бік.
- (?) Поворот лише на 90° — за JA-статтею для повторної дії; чи можна обирати напрям — неясно.
- (?) Вікно калібрування камери — з типового сценарію PS Eye, не перевірено.
- (?) Рівні складності CPU.
- (?) Чи контратакує ціль, що загинула від удару, — джерела не кажуть; у правилі прийнято «лише вцілілою».
- (?) Біолітові поля: JA-стаття стихію Biolith не пояснює; «машина» в JA ≈ Biolith-істоти в EN (?).
