---
title: GemCraft
slug: gemcraft
family: tower-lanes
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2008
platforms: [web (Flash), iOS (Labyrinth), Steam (Chasing Shadows 2015, Frostborn Wrath 2020, Legacy Collection 2026)]
links:
  - {kind: official, url: "https://www.gameinabottle.com/gcl.php", best: true, note: "Labyrinth: керування й поради — комбінування, дуальні/потрійні самоцвіти, пастки, підсилювачі, мана, вигнання від сфери"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/GemCraft", note: "серія, роки, мана = життя й валюта"}
  - {kind: official, url: "https://www.gameinabottle.com/", note: "студія Game in a Bottle: усі частини"}
  - {kind: official, url: "https://www.gameinabottle.com/gemcraft0.php", note: "Chapter 0: чисті/дуальні/призматичні самоцвіти, пастки, хвилі, гем-бомби"}
  - {kind: official, url: "https://www.gameinabottle.com/gemcraft1.php", note: "Chapter One: траншеї, отрута ігнорує броню"}
  - {kind: steam, url: "https://store.steampowered.com/app/296490/GemCraft_Chasing_Shadows/", note: "9 типів самоцвітів, вежі/пастки/підсилювачі, камені хвиль, battle traits"}
  - {kind: steam, url: "https://store.steampowered.com/app/1106530/GemCraft_Frostborn_Wrath/", note: "6 типів, enraging slot, linked waves, талісман-пазл"}
  - {kind: steam, url: "https://store.steampowered.com/app/4207990/GemCraft_Legacy_Collection/", note: "перші три частини"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gemcraft+chasing+shadows+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [round-currency, enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, hp-damage, projectile-shot, shoot-cooldown, blast-wave, temporary-modes, speed-per-type, inventory, inventory-limit, drag-drop-piece, game-pause, level-select, level-unlock, difficulty-levels, event-points, score-records, +tower-placement, +tower-range, +maze-by-towers, +call-wave-early, +item-combine, +socket-item, +gem-grade-combine, +mixed-specials, +aura-buff, +status-stacks, +mana-as-life, +banish-cost-growth, +pool-level-up, +throw-bomb-item, +enrage-wave, +skill-tree-meta, +battle-traits, +talisman-puzzle]
proposes: ["+trigger:wave_start", "+trigger:reach", "+cond:same", "+cond:in_range", "+effect:combine", "+effect:socket", "+effect:unsocket", "+effect:banish", "+effect:enrage", "+role:tower", "+role:gem", "+role:socket", "+ui:gem-inventory", "+ui:wave-stones", "+ui:mana-pool-bar", "+ui:range-circle", "+window:skill-tree", "+window:map-window", "+feature:meta-progression", "+feature:mode-endless", "+feature:battle-modifiers"]
author: opus
date: 2026-11-02
---

# GemCraft — TD, де зброя — самоцвіти: зливай однакові в старший ґрейд, змішуй кольори, вставляй у вежі, пастки й підсилювачі

## Суть
Гравець-маг за **ману** створює самоцвіти (gems) різних кольорів, кожен колір — свій спецефект (отрута, сповільнення, ланцюг, критичний удар, роздирання броні, крадіжка мани…). Два самоцвіти **комбінуються в один вищого ґрейду**; змішування кольорів дає дуальні/потрійні з усіма спецефектами, але слабшими. Самоцвіт вставляють у **вежу** (стріляє), **пастку** на дорозі (сильний спецефект) або **підсилювач** (бафає сусідні вежі/пастки). Мана — водночас валюта й життя: монстр, що дійшов до сфери, «вигнаний» назад ціною мани; мана < 0 — поразка.

## Поле і час
- Поле — сітка клітин з дорогою від точок появи до Сфери мага (Wizard Orb); вежі, пастки, стіни займають клітини (вежа 2×2 (?)). Вежі будуються поза дорогою, пастки — на дорозі.
- Стіни (Labyrinth, CS) дозволяють перегородити й подовжити шлях на відкритих мапах (`maze-by-towers`) (?).
- Real-time з паузою й прискоренням; хвилі йдуть каменями хвиль (wave stones) за таймером або раніше за кліком.
- Камера: уся мапа на екрані, без туману; поверх — сфера, монстри, ворожі споруди (маяки, гнізда, гробниці в CS).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Самоцвіт | gem (+role) / tile | колір(и), ґрейд 1–N, шкода, дальність, швидкість, сила спецефекту | лежить в інвентарі або в гнізді; два → один вищого ґрейду |
| Вежа | tower (+role) | гніздо 1, дальність від самоцвіта | стріляє самоцвітом по монстрах у радіусі; цілі — за пріоритетом |
| Пастка | socket (+role) | на клітині дороги | бʼє монстрів, що проходять; спецефект підсилений, шкода нижча |
| Підсилювач (amplifier) | socket | 8 сусідів (?) | додає частку характеристик свого самоцвіта сусіднім вежам і пасткам |
| Стіна | static | — | непрохідна; змінює шлях (Labyrinth/CS) |
| Траншея (Chapter One) | terrain | вода | сповільнює монстрів |
| Святиня (shrine) | tower | заряд | одноразовий потужний удар: блискавка, заряджені болти (?) |
| Сфера мага | static | — | монстр дійшов → вигнання за ману |
| Камінь хвилі | spawner | склад хвилі | хвиля стартує за таймером або кліком (бонус мани) |
| Ворожі споруди (маяк, гніздо, гробниця, монолітний шард) | enemy | HP | бафають монстрів або породжують їх; знищуються вежами (?) |
| Монстр звичайний | enemy | HP, броня, швидкість | йде дорогою до сфери |
| Рій (swarmling) | enemy | мало HP, багато | масово |
| Гігант | enemy | багато HP, повільний | — |
| Рейвер / Тінь / Спектр / Призрак (apparition) | enemy | особливі | тінь стріляє, привид з'являється поза дорогою (?) |
| Мана | resource | запас, рівень пулу | валюта й життя водночас |

Кольори (Chasing Shadows, 9 (?)): чорний — bloodbound (шкода росте з убивствами) · червоний — chain hit (ланцюг) · помаранчевий — mana leeching (мана за влучання) · жовтий — critical hit · білий — poolbound (шкода від розміру пулу мани) · зелений — poison (ігнорує броню, стекується) · блакитний — suppressing · синій — slowing · фіолетовий — armor tearing. Frostborn Wrath — 6 типів (bleeding, crit, mana leech, armor tearing, poison, slowing) (?).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(create_gem, color)` → ЯКЩО `has(mana, cost(grade))` → ТО `currency(-cost)`, `custom: «самоцвіт ґрейду g у вільну клітину інвентаря»`; ціна росте ≈ подвоєнням за ґрейд (?).
- КОЛИ `input(combine, a, b)` → ЯКЩО `has(mana, combine_cost)` → ТО `merge(a, b → c)`: ЯКЩО `same(a, b, grade)` → `c.grade = g+1`; інакше — `c.grade` ≈ старший з меншим приростом (?); кольори `c = a ∪ b`.
- КОЛИ `custom: «c має кілька кольорів»` → ТО `custom: «кожен спецефект слабшає; базові шкода/дальність/швидкість — бонус (дуальний > чистий, потрійний ще більше)»`.
- КОЛИ `input(duplicate, gem)` → ТО `custom: «копія за ману»`; `input(upgrade, gem)` = дублювати + комбінувати (+1 ґрейд одним кліком).
- КОЛИ `input(drag, gem, building)` → ЯКЩО `free(slot)` → ТО `custom: «effect socket»`; зайнято → `swap`.
- КОЛИ `in_range(tower, monster, r(gem))` → ТО `spawn(projectile)` з періодом `1/firing_speed`; КОЛИ `contact(projectile, monster)` → `damage(max(dmg − armor, min))` + спецефекти кольорів.
- Спецефекти: poison — `custom: «DoT, ігнорує броню, стекується»`; slowing — `speed(monster, ×k, t)`; chain hit — `custom: «удар перескакує на k сусідів»`; armor tearing — `custom: «броня −n назавжди»`; mana leech — `currency(+n)` за влучання; crit — `rng(p)` → `damage × m`; bloodbound — `custom: «шкода росте з кількістю вбивств самоцвіта»`.
- КОЛИ `enter(monster, trap_cell)` → ТО `custom: «пастка застосовує спецефект (×сильніше) і малу шкоду»`.
- КОЛИ `adjacent(amplifier, tower|trap)` → ТО `custom: «сусід отримує +частку характеристик самоцвіта підсилювача»` (`aura-buff`).
- КОЛИ `hp_zero(monster)` → ТО `disappear_a`, `currency(+mana)`, `score(+n)`.
- КОЛИ `counter(mana, ==, pool_max)` → ТО `custom: «зайва мана пропадає»`; КОЛИ `input(expand_pool)` → ЯКЩО `counter(mana, ==, pool_max)` → ТО `custom: «pool_level +1: більший максимум і множник надходження мани»`.
- КОЛИ `reach(monster, orb)` → ТО `custom: «effect banish: currency(−ціна); монстр телепортується на старт; ціна його наступного вигнання росте»`.
- КОЛИ `custom: «ціна вигнання > мана»` → ТО `lose`.
- КОЛИ `input(call_wave, stone)` → ТО `wave_start` негайно, `currency(+bonus)` / `score(+bonus)` за ранній виклик.
- КОЛИ `input(drop_gem, wave_stone)` → ТО `custom: «effect enrage: монстри хвилі сильніші (броня/HP), більше досвіду й очок; ґрейд самоцвіта = сила»`; FW — enraging slot для всіх хвиль.
- КОЛИ `input(gem_bomb, gem, cell)` → ТО `disappear_a` (самоцвіт), `explode(area)` зі шкодою від ґрейду; по ворожій споруді — ламає її.
- КОЛИ `all_gone(waves)` and `all_gone(monsters)` → ТО `win`, `score` → досвід → рівень мага → очки навичок.
- Перемога: пережити всі хвилі · Поразка: мана не покриває вигнання · Рахунок: очки → досвід; рамка рівня «glowing frame» за поріг очок.

## Керування і ввід
- Миша: вибір будівлі в панелі (або клавіша T/R/A/W — вежа, пастка, підсилювач, стіна) → клік по клітині; Shift — кілька підряд.
- Самоцвіти: кнопки кольорів (клавіші 1–9) створюють самоцвіт в інвентарі; drag самоцвіта на вежу/пастку/підсилювач — вставити; drag на інший самоцвіт у режимі combine (G) — злити; D — дублювати, U — апгрейд, X — повернути ману, B — гем-бомба.
- Колесо миші (FW) — +ґрейд у інвентарі; клік по монстру — пріоритетна ціль; N — наступна хвиля; Q — пауза/розморозка; M — розширити пул мани.

## Вікна, меню, HUD
- `main-menu` → `map-window` (⏳): мапа світу з полями-рівнями, позначки пройденості/рамок.
- `mode-select` (⏳): Journey · Endurance (вижити якомога довше) · Trial (фіксований набір самоцвітів, складність) (FW).
- `custom-window` підготовки рівня: складність, battle traits (модифікатори), доступні кольори (?).
- `+window:skill-tree`: пасивні навички (~24) за очки рівня, перерозподіл; майстерність кольорів, дуальних/потрійних.
- `game-screen`: поле; праворуч — `+ui:gem-inventory` (сітка слотів), кнопки створення самоцвітів і будівель з цінами, `+ui:mana-pool-bar` (мана / максимум / рівень пулу), `+ui:wave-stones` (камені хвиль з іконками монстрів зліва), `pause-button`, `fast-forward`, `+ui:range-circle`, `tooltip` самоцвіта (ґрейд, шкода, дальність, спецефекти).
- `end-screen`: очки, досвід, рамка; `stats-window` (?).
- Талісман (FW/CS): `custom-window` з гніздами-фрагментами, що складаються як пазл.
- Переходи: main-menu → map-window → підготовка → game-screen → end-screen → map-window; map-window ↔ skill-tree.

## Фічі поза полем
- `world-map` + `level-unlock`; приховані рівні за рамками; `meta-progression`: рівень мага → очки навичок → навички; талісман із фрагментів.
- `+feature:battle-modifiers` (battle traits): стекувані ускладнення за більші нагороди; `difficulty-presets`.
- `mode-endless` (Endurance, камені хвиль розширюють наступний забіг), Trial, хвилі «linked» (дві хвилі одночасно, FW).
- `pause`, `speed-control`, `save-progress`, досягнення (Steam).

## Варіації й родичі
- Chapter One (2008) → Chapter 0 (2009, 8 кольорів, призматичні) → Labyrinth (2011, стіни й лабіринти) → Chasing Shadows (2014, 9 кольорів, тіні) → Frostborn Wrath (2020, 6 типів, лампади й пілони).
- Родичі: Desktop Tower Defense і Fieldrunners (лабіринт із веж), Bloons (апгрейд веж гілками), Random Dice (злиття як апгрейд), Kingdom Rush.
- **Осі варіацій**: апгрейд — гілками в меню / **злиттям предметів** / злиттям веж на полі · спецефект — від типу вежі / **від вставленого предмета** (предмет переносний між вежами) · життя — окреме / **мана = життя**.

## Цікавинки для курсу
- Комбінування: два однакові → ґрейд +1, різні → змішані спецефекти зі штрафом — 🥉 (злиття як дані, ціна ≈ 2^g).
- Самоцвіт як переносний предмет у гніздах веж/пасток/підсилювачів — 📎 (сутність-контейнер і перенесення).
- Підсилювач: аура на сусідні клітини з часткою характеристик — 🥉.
- Мана = валюта + життя, вигнання з ростом ціни для того самого монстра — 📎.
- Ранній виклик хвилі й «розлючення» хвилі самоцвітом — 🌱 кожне (ризик ↔ нагорода).
- Стеки отрути/сповільнення й броня з роздиранням — 🥈 (`status-stacks`, порядок застосування ефектів).

## Мапа на каталог
- Є: `round-currency` ↔ мана · `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` ↔ сфера · `hp-damage` · `projectile-shot` + `shoot-cooldown` · `blast-wave` ↔ гем-бомба · `temporary-modes` ↔ сповільнення/отрута · `speed-per-type` · `inventory` + `inventory-limit` ↔ сітка самоцвітів · `drag-drop-piece` · `game-pause` · `level-select` / `level-unlock` · `difficulty-levels` · `event-points` + `score-records`.
- **Нема** → пропозиції карток:
  - `+tower-placement`, `+tower-range`, `+maze-by-towers` (стіни Labyrinth), `+call-wave-early` — спільні з Fieldrunners.
  - `+item-combine` (є) — тут комбінування самоцвітів; `+aura-buff` (є) — підсилювач; `+status-stacks` (є) — отрута/сповільнення.
  - `+socket-item` «Предмет у гнізді визначає поведінку споруди» · entities/state · 📎.
  - `+gem-grade-combine` «Два однакові → ґрейд +1, ціна ≈ 2^g» · entities/legality · 🥉 (дитина `tile-merge`).
  - `+mixed-specials` «Змішаний предмет несе всі спецефекти, кожен слабший» · entities/state · 🥉.
  - `+mana-as-life` «Валюта = життя» · game-logic/lose · 🌱.
  - `+banish-cost-growth` «Ворог біля бази відкидається на старт за ціну, що росте» · game-logic/lose · 📎.
  - `+pool-level-up` «Розширення пулу ресурсу: більший максимум і дохід» · game-logic/economy · 🌱.
  - `+throw-bomb-item` «Кинути предмет як бомбу» · entities/combat · 🌱.
  - `+enrage-wave` «Посилити хвилю за більшу нагороду» · game-logic/waves · 🌱.
  - `+skill-tree-meta` «Навички між рівнями за очки, перерозподіл» · game-logic/economy · 📎.
  - `+battle-traits` «Стекувані модифікатори складності за нагороду» · game-logic/difficulty · 📎.
  - `+talisman-puzzle` «Гнізда-фрагменти складаються як пазл» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+trigger:wave_start` — уже ⏳; підтвердження (камінь хвилі); `+trigger:reach` — монстр біля сфери.
- `+cond:same` (🔥) — ґрейд; `+cond:in_range` (🔥) — радіус від самоцвіта.
- `+effect:combine` — злиття предметів поза полем (інвентар), відрізняти від `merge` плиток; `+effect:socket` / `+effect:unsocket` — вставити/вийняти предмет; `+effect:banish` — відкинути ворога на старт за ціну; `+effect:enrage` — посилити хвилю.
- `+role:tower` (підтвердження), `+role:gem` — переносний предмет-модуль, `+role:socket` — споруда, чия поведінка задана вставленим.
- `+ui:gem-inventory`, `+ui:wave-stones` (черга хвиль з іконками й кліком «раніше»), `+ui:mana-pool-bar`, `+ui:range-circle`.
- `+window:skill-tree`, `+window:map-window`.
- `+feature:meta-progression` (🔥), `+feature:mode-endless`, `+feature:battle-modifiers`.

## Джерела
- ⭐ [GemCraft Labyrinth (Game in a Bottle)](https://www.gameinabottle.com/gcl.php) — клавіші й поради: чисті vs дуальні/потрійні, комбінування/дублювання/апгрейд/повернення мани, пастки зі сповільненням, підсилювачі, святині, стіни, пул мани, вигнання сферою з ростом ціни, камені хвиль.
- [Wikipedia: GemCraft](https://en.wikipedia.org/wiki/GemCraft) — серія і роки, мана як життя й валюта, комбінування двох у сильніший.
- [Chapter 0](https://www.gameinabottle.com/gemcraft0.php) — призматичні з 8 кольорів, самоцвіт на камінь хвилі посилює броню хвилі, гем-бомби.
- [Chapter One](https://www.gameinabottle.com/gemcraft1.php) — траншеї з водою, фіолетовий = броня, отрута стекується й ігнорує броню.
- [Steam: Chasing Shadows](https://store.steampowered.com/app/296490/GemCraft_Chasing_Shadows/) · [Frostborn Wrath](https://store.steampowered.com/app/1106530/GemCraft_Frostborn_Wrath/) · [Legacy Collection](https://store.steampowered.com/app/4207990/GemCraft_Legacy_Collection/).
- YouTube: пошук «gemcraft chasing shadows gameplay».

## Непевне
- (?) Повна палітра 9 кольорів CS і 6 типів FW — з памʼяті; Steam підтверджує лише кількість.
- (?) Формула ціни й результату комбінування різних ґрейдів.
- (?) Розмір веж на сітці, радіус підсилювача (8 сусідів?), що саме дає підсилювач.
- (?) Чи стіни є в усіх частинах (точно — Labyrinth за клавішею W).
- (?) Вороги CS (тіні, спектри, привиди, маяки, гнізда) — назви з поради Labyrinth, поведінка з памʼяті.
