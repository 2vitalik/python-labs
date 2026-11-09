---
title: Mewgenics
slug: mewgenics
aka: []
family: tactics
also: [roguelike, build-sim]
klass: figure
axes:
  field: iso
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2026
platforms: [PC, Switch 2, PS5, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mewgenics", note: "цикл бій ↔ дім, розведення, мутації, поранення і смерть, вихід на пенсію, дати"}
  - {kind: fandom, url: "https://mewgenicswiki.org/articles/combat-positioning-terrain-guide", best: true, note: "бій: сітка 10×10, Speed, reach/range, backstab, knockback, терен і його перетворення, погода, Exhaustion"}
  - {kind: fandom, url: "https://mewgenicswiki.org/wiki/classes", note: "14 класів через нашийники, бонуси статів"}
  - {kind: fandom, url: "https://mewgenicswiki.org/wiki/furniture", note: "5 статів дому: Comfort, Stimulation, Health, Mutation, Appeal"}
  - {kind: fandom, url: "https://mewgenicswiki.org/", note: "розділи вікі: 2138 умінь, 291 статус, 59 погод, 789 мутацій…"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Mewgenics", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mewgenics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [push-object, hp-damage, melee-vs-ranged, line-of-sight-attack, impassable-cells, floor-types, cell-transform, inertia-slide, environment-death, chain-detonation, explode-area, status-effects, temporary-modes, orientation-state, unit-xp-skills, inventory-items, permadeath, destroy-all-enemies, timeout-punisher, run-relics, world-map, map-window, placement-screen, character-select, codex-window, achievements-window, reachable-highlight, threat-range, hover-highlight, game-screen, +speed-initiative, +backstab-facing, +knockback-collision, +terrain-reaction-chain, +element-status-combo, +weather-modifiers, +downed-state, +breeding-genetics, +mutations, +house-stats, +class-by-equipment, +aging-retirement]
proposes: ["+trigger:round_start", "+trigger:turn_n", "+effect:knockback", "+effect:level_up", "+cond:from_behind", "+cond:cost", "+role:weather", "+ui:turn-order-bar", "+ui:flatten-view", "+window:house-screen", "+window:breeding-window", "+feature:breeding", "+feature:roster-carryover", "+axis:session"]
author: opus
date: 2026-11-09
---

# Mewgenics — розводиш котів у домі, а потім ведеш четвірку класів у покрокові бої на процедурних сітках, де вода, вогонь і лід реагують між собою

## Суть
Цикл з двох половин: **дім** (коти живуть, паруються, народжують кошенят із генетикою батьків і мутаціями; меблі змінюють статистику дому) і **забіг** — роглайк-похід четвіркою котів через покрокові бої. Клас кота задає **нашийник** (collar): зняв — інший клас, перерозподіл умінь. Бій — ізометрична сітка, де ініціатива від Speed, кожен кіт робить рух і базову атаку плюс скільки завгодно умінь за ману; терен і стихії ланцюжать реакції (мокрий + лід = заморозка, вода + струм = ланцюг). Автори — Edmund McMillen і Tyler Glaiel.

## Поле і час
- Бій: процедурна ізометрична квадратна сітка 10×10; перед боєм — розвідка поля й розстановка на зелені клітини (слот 1 — попереду).
- Тік: раунд; черга юнітів за Speed (швидші першими; Slow зсуває чергу); хід юніта = 1 рух + 1 базова атака + будь-скільки умінь, поки є мана, + предмети.
- Шари клітини: терен (трава / вода / лід / вогонь / колючки / скло / яма) + обʼєкти (камені, бочки) + погода на весь бій.
- Таймер бою: з 10-го ходу всі отримують Exhaustion — неблоковану шкоду, що росте на 1 щоходу.
- Поза боєм: дім із кімнатами (реальний календар днів: старіння, мутації, події); мапа забігу з 18 локаціями (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт | player | STR, DEX, CON, INT, SPD, CHA, LCK; HP; мана = CHA×3, реген від INT; рівень; вік | у бою: рух + атака + уміння; у домі: живе в кімнаті, парується, старіє |
| Нашийник (collar) | container | клас | задає клас і стат-бонуси; зміна — респек умінь |
| Butcher / Fighter / Tank | player | CON+4 у Tank | ближній бій; Tank — базова атака з відкиданням, Chain Knockback |
| Hunter | player | DEX+3, LCK+2 | дальній, найточніший і найкритовіший |
| Mage | player | INT+2, CHA+2 | великий запас мани; Forbidden Flame (0 мани, раз за бій) палить усю мапу — 7 шкоди всім ворогам |
| Psychic | player | +5 мани на старті | контроль позиції: Telekinesis (4 мани) відштовхує ціль у полі зору на 10 клітин |
| Thief | player | SPD+4 | backstab-механіка |
| Cleric / Druid / Necromancer | player | — | лікування / вічний ворон-компаньйон / Leech |
| Monk / Jester / Tinkerer / Collarless | player | — | стійки й додаткова атака / reroll умінь / Tech-стеки й Craft Weapon / базовий без нашийника |
| Ворог | enemy | HP, уміння | AI; 431 вид (вікі) |
| Champion | boss | ×2 HP, сильніше, далі, extra turns | посилений ворог |
| Бос | boss | фази (?) | кінець локації |
| Нейтральні птахи (Bird Migration) | neutral | — | убитий дає All Stats Up і предмет |
| Short Grass | terrain | — | невеликий бонус ухилення; вода → Tall Grass |
| Tall Grass | terrain | +50 % ухилення, укриття | вода → Tall Flower; горить |
| Tall Flower | terrain | +3 HP і мани щохід, +50 % ухилення | — |
| Вода | terrain | вхід = 2 руху | Wet при контакті; струм бʼє всіх у звʼязній воді; лід → Frictionless Ice |
| Frictionless Ice | terrain | — | зрушений юніт ковзає; ковзання по воді заморожує її; вогонь → вода |
| Вогонь | hazard | 1 при проході, 2 на старті ходу | поширюється по траві, павутині, олії; підсмажує сусідню їжу |
| Ice Spikes / Thorns / Glass Shards | hazard | 1–2 шкоди | Thorns: атакувальнику +2 і Bleed; скло — Bleed |
| Floating Glass | hazard | 2 + Bleed | бʼє й літунів, падає після спрацювання |
| Яма (pit) | hazard | — | миттєва (або майже) смерть |
| Бочка | object | — | вогонь підриває; вибух ланцюжиться на сусідні бочки |
| Камінь / Petrified-юніт | static | — | блокує рух і лінію; скамʼянілий — уся шкода 1, але більше відкидання |
| Меблі | object | ± Comfort, Stimulation, Health, Mutation, Appeal | пасивно змінюють статистику дому |
| Ідол | object | великий бонус одному стату | Idol of Chaos: ×2 нагород статів, −Comfort |
| Какашка | hazard | −Comfort, −Health | у домі |
| Бродячий кіт | neutral | рідкість від Appeal | приходить у дім, можна прийняти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «розвідка поля»`, `place(player, cat)` на зелені клітини за порядком слотів.
- КОЛИ `custom: «початок раунду»` → ТО черга ходів за SPD (більший — раніше); `custom: «Slow зсуває юніта в черзі»`.
- КОЛИ `input(move, cell)` → ЯКЩО `path_exists(cat, cell)` → ТО `move(cat, cell)`; ЯКЩО `cell(cell, water)` → ТО `custom: «вхід коштує 2 руху»`; відхід від сусіднього ворога без штрафу.
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(cat, target, reach|range) and line_of_sight(cat, target)` → ТО `damage(n)`; дальність ближнього 1 (2 з бонусом), дальнього 4 (5).
- КОЛИ `input(ability, target)` → ЯКЩО `custom: «мана ≥ вартості»` → ТО ефект, `custom: «−мана»`; умінь за хід — без ліміту.
- КОЛИ `input(attack, target)` → ЯКЩО `custom: «атака ззаду»` → ТО `damage(⌈n × 1.25⌉)`; ЯКЩО `state(cat, backstabber)` → ТО гарантований крит.
- КОЛИ `input(click_empty_cell)` → ТО `face(cat, dir)` без витрати дії.
- КОЛИ `contact(knockback_attack, target)` → ЯКЩО `not state(target, thorns|kinetic_spikes)` → ТО `push(target)` на N клітин від атакувальника.
- КОЛИ `after(push(target))` → ЯКЩО `occupied(next_cell, wall|object|unit)` → ТО `custom: «шкода від зіткнення окремо від базової»`; ЯКЩО `state(attacker, chain_knockback)` → ТО `push(hit_unit)`.
- КОЛИ `after(push(target))` → ЯКЩО `cell(dest, pit)` → ТО `disappear(target)`.
- КОЛИ `enter(unit, frictionless_ice)` → ТО `slide(unit, dir)`; ЯКЩО `cell(next, water)` → ТО `set_cell(next, ice)`.
- КОЛИ `contact(water_effect, short_grass)` → ТО `set_cell(cell, tall_grass)`; КОЛИ `contact(water_effect, tall_grass)` → ТО `set_cell(cell, tall_flower)`.
- КОЛИ `contact(ice_effect, water)` → ТО `set_cell(cell, frictionless_ice)`; КОЛИ `contact(fire_effect, frictionless_ice)` → ТО `set_cell(cell, water)`; КОЛИ `contact(ice_effect, short_grass)` → ТО `set_cell(cell, ice_spikes)`.
- КОЛИ `tick` → ЯКЩО `adjacent_count(fire, flammable, >=, 1)` → ТО `custom: «вогонь перекидається на траву/павутину/олію»`; палаючий юніт підпалює займисті клітини, якими йде.
- КОЛИ `enter(unit, fire)` → ТО `damage(1)`; КОЛИ `turn_start(unit)` → ЯКЩО `cell(cell, fire)` → ТО `damage(2)`; ЯКЩО `state(unit, wet)` → ТО вогонь гасне, `clear_state(unit, wet)`.
- КОЛИ `enter(unit, water)` → ТО `set_state(unit, wet)`; КОЛИ `contact(ice_attack, unit)` → ЯКЩО `state(unit, wet)` → ТО `set_state(unit, frozen)`.
- КОЛИ `contact(electric_attack, unit)` → ЯКЩО `state(unit, wet)` → ТО `custom: «ланцюгова блискавка по сусідніх мокрих, з посиленням»`; ЯКЩО `cell(cell, water)` → ТО `damage` усім у звʼязній воді, і своїм.
- КОЛИ `contact(attack, frozen_unit)` → ТО шкоду дає лише вогонь; удар → `slide(unit)` + шкода від зіткнення.
- КОЛИ `contact(fire, barrel)` → ТО `explode(area)`; `after(explode)` → ЯКЩО `adjacent(barrel, barrel2)` → ТО `custom: «ланцюг вибухів»`.
- КОЛИ `enter(unit, tall_flower)` / `turn_start(unit)` на ній → ТО `heal(unit, 3)`, `custom: «+3 мани»`.
- КОЛИ `custom: «початок раунду»` → ЯКЩО `custom: «погода Windy/Thunderstorm/Hurricane»` → ТО `push(unit)` на 1 у випадковому напрямку; Acid Rain — `damage(2)`; Sandstorm — `damage(1)`; Rain — усі стартують Wet.
- КОЛИ `custom: «хід ≥ 10»` → ТО `set_state(all, exhaustion)`: `damage(turn − 9)` без блоку, −1 лікування й регену мани.
- КОЛИ `hp_zero(cat)` → ТО `set_state(cat, incapacitated)` — лишається на полі; КОЛИ `counter(hits_while_down, >=, 3)` → ТО `disappear(cat)`: кіт гине, предмети втрачено.
- КОЛИ `state_on(cat, incapacitated)` → ТО `custom: «шанс довготривалої травми (зламана лапа: −стати)»`.
- КОЛИ `all_gone(enemy)` → ТО `win` бою; `custom: «випадковий кіт загону отримує рівень»`.
- КОЛИ `custom: «двоє котів в одній кімнаті»` → ЯКЩО `custom: «Comfort дому достатній»` → ТО `spawn(kitten)`: стати й уміння від батьків (Stimulation — більше шансів на найкращі); родичі → `custom: «вроджені вади»`.
- КОЛИ `custom: «минув день»` → ТО `rng(p_mutation)` → `custom: «мутація: обмін одного стату на інший / унікальний ефект»`; Health дому лікує дрібні травми й хвороби; старі коти помирають.
- КОЛИ `custom: «забіг завершено»` → ТО коти, що дійшли, `custom: «на пенсію — більше не беруться в забіг»`; вцілілі повертаються в дім і передають стати й спорядження.
- Перемога: бій — перебити всіх ворогів; забіг — пройти локацію з босом · Поразка: загибель загону (?) · Рахунок: —.

## Керування і ввід
- Миша/геймпад: клік кота (або черга сама дає його) → підсвітка руху → клітина; вибір уміння з панелі → ціль.
- Клік по порожній клітині — розворот (орієнтація) без витрати дії.
- Середня кнопка миші (Y/Triangle) — «сплющити» ізометрію для оцінки загроз; наведення на ворога — його рух і дальність атак.
- У домі: перетягування котів між кімнатами, розстановка меблів (?).

## Вікна, меню, HUD
- `main-menu`: продовжити · новий забіг · налаштування.
- `custom-window` «дім» — кімнати з котами, меблі, статистика дому (Comfort, Stimulation, Health, Mutation, Appeal); вибір пар; бродячі коти.
- `character-select` — збір четвірки на забіг, нашийники, спорядження.
- `map-window` — мапа забігу/локацій.
- `placement-screen` — розвідка поля й розстановка на зелених клітинах.
- `game-screen`: ізометрична сітка; черга ходу за Speed (`turn-indicator`); `hp-bar`, мана; іконки статусів; погода; `reachable-highlight`, `threat-range` при наведенні; панель умінь (`ability-buttons`); кнопка кінця ходу.
- `custom-window` «рівень» — вибір уміння при підвищенні (Jester — додатковий reroll).
- `custom-window` «подія» — 181 подія (вікі), напр. сусіди приймають кота в подарунок за предмет.
- `achievements-window` (269 досягнень за вікі).

## Фічі поза полем
- Розведення: генетика батьків, інбридинг → вади, щоденні мутації (789 мутацій, 136 розладів за вікі); стається лише після першого забігу.
- Дім: 639 меблів (вікі) з бонусами до 5 статів дому; ідоли; загрози нападають на дім.
- Прогресія: рівні котів, вихід на пенсію після забігу, старіння й смерть від віку — `meta-progression`.
- Спорядження: одяг і предмети (1110 за вікі); смерть кота — втрата предметів, включно з рідкісними.
- Консольні порти 2026 (Switch 2, PS5, Xbox Series) — видавець Nicalis.

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (відкидання і зіткнення), [xcom](xcom.md) (загін, поранення, бараки між місіями), [fire-emblem](fire-emblem.md) (пари → діти з успадкуванням), [battle-brothers](battle-brothers.md) (ростер, що старіє й вмирає), [othercide](othercide.md) (ініціатива за швидкістю).
- Поза корпусом: Divinity: Original Sin (поверхні вода/вогонь/лід/струм), The Binding of Isaac (автор, тисячі предметів), Darkest Dungeon (ростер між забігами).
- **Осі варіацій**: клас — фіксований / від предмета-нашийника · нові юніти — найм / розведення з генетикою · поверхні — статичні / реагують стихіями · таймер бою — нема / Exhaustion з наростанням.

## Цікавинки для курсу
- Таблиця реакцій терену: вода→трава→квітка, лід на воді → ковзанка, вогонь → вода, вогонь поширюється займистим — 🥈 (автомат клітин зі стихіями).
- Статус-комбо: Wet + Ice = Freeze, Wet + Electric = ланцюг у звʼязній воді (flood fill) — 🥉.
- Ініціатива від Speed з чергою раунду — 📎.
- Відкидання на N з окремою шкодою від зіткнення і Chain Knockback — 📎.
- Exhaustion: з 10-го ходу шкода росте на 1 — 🌱 (антизатягування).
- Генетика: кошеня = суміш статів/умінь батьків + шанс мутації, інбридинг → вади — 🥈.
- Статистика дому з меблів як модифікатори ймовірностей (Comfort, Stimulation, Mutation, Appeal) — 📎.

## Мапа на каталог
- Є: `push-object` ↔ knockback · `hp-damage` · `melee-vs-ranged` ↔ reach/range · `line-of-sight-attack` ↔ Magic Dart / Lobbed Shot · `impassable-cells` ↔ камені · `floor-types` ↔ вода, трава, вогонь, колючки · `cell-transform` ↔ перетворення терену · `inertia-slide` ↔ Frictionless Ice · `environment-death` ↔ ями · `chain-detonation` / `explode-area` ↔ бочки · `status-effects` / `temporary-modes` ↔ Wet, Frozen, Burning, Bleed, Petrified · `orientation-state` ↔ орієнтація й backstab · `unit-xp-skills` · `inventory-items` · `permadeath` · `destroy-all-enemies` · `timeout-punisher` ↔ Exhaustion · `run-relics` ↔ предмети забігу · `world-map` / `map-window` · `placement-screen` · `character-select` · `codex-window` (?) · `achievements-window` · `reachable-highlight` / `threat-range` / `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+speed-initiative` «Черга ходів юнітів за швидкістю» · game-logic/turns · 📎.
  - `+backstab-facing` «Удар ззаду за орієнтацією» · entities/combat · 📎 · {mult: 1.25}.
  - `+knockback-collision` «Відкидання на N зі шкодою від зіткнення» · entities/combat · 📎.
  - `+terrain-reaction-chain` «Перетворення терену стихіями» · entities/terrain · 🥈 · {table}.
  - `+element-status-combo` «Комбо статусів: мокрий + лід / струм» · entities/state · 🥉.
  - `+weather-modifiers` «Погода бою як глобальні правила» · world/levels · 📎.
  - `+downed-state` «0 HP = недієздатний, добивання N ударами» · entities/death · 🌱.
  - `+breeding-genetics` «Розведення: успадкування статів, інбридинг» · game-logic/progression · 🥈.
  - `+mutations` «Випадкові мутації-обміни статів» · entities/state · 📎.
  - `+house-stats` «Меблі змінюють ймовірності в домі» · game-logic/economy · 📎.
  - `+class-by-equipment` «Клас задається предметом» · entities/state · 🌱.
  - `+aging-retirement` «Старіння, пенсія і смерть від віку» · game-logic/progression · 📎.

## Пропозиції до словників
- `+trigger:round_start` — початок раунду (погода, черга за Speed).
- `+trigger:turn_n` — настав хід бою № N (Exhaustion з 10-го).
- `+effect:knockback` — відкинути на N клітин від джерела.
- `+effect:level_up` — підвищити рівень (випадковому коту після бою).
- `+cond:from_behind` — атака ззаду відносно орієнтації.
- `+cond:cost` — вистачає мани на уміння.
- `+role:weather` — глобальний модифікатор бою.
- `+ui:turn-order-bar` — черга ходів юнітів.
- `+ui:flatten-view` — перемикач ізометрії на плаский вид для читання загроз.
- `+window:house-screen` — дім з кімнатами, мешканцями й меблями; `+window:breeding-window` — пари й прогноз потомства.
- `+feature:breeding` — розведення юнітів між забігами; `+feature:roster-carryover` — вцілілі передають стати/спорядження.
- `+axis:session` — `run`.

## Джерела
- ⭐ [Mewgenics Wiki: Combat positioning & terrain](https://mewgenicswiki.org/articles/combat-positioning-terrain-guide) — сітка 10×10, розстановка, Speed, рух+атака+уміння, reach/range, LOS, backstab +25 %, knockback і зіткнення, мана від CHA/INT, повний список терену й перетворень, статус-комбо, погода, Exhaustion, чемпіони.
- [Wikipedia](https://en.wikipedia.org/wiki/Mewgenics) — дім ↔ бій, 4 коти, incapacitated і травми, рівень після бою, розведення, інбридинг, мутації, пенсія, старість, дати й автори.
- [Mewgenics Wiki: Classes](https://mewgenicswiki.org/wiki/classes) — 14 класів, нашийники, стат-бонуси.
- [Mewgenics Wiki: Furniture](https://mewgenicswiki.org/wiki/furniture) — 5 статів дому, ідоли, какашки.
- [Mewgenics Wiki: Telekinesis](https://mewgenicswiki.org/wiki/abilities/telekinesis) — 4 мани, відштовхнути на 10.
- [Mewgenics Wiki](https://mewgenicswiki.org/) — обсяги контенту.
- Steam і YouTube — пошукові URL.

## Непевне
- (?) Сітка 10×10 — з фан-вікі; Wikipedia каже лише «процедурні ізометричні сітки».
- (?) Умова поразки забігу (загибель усіх чотирьох?) і структура локацій/босів — не перевірено.
- (?) Як саме вибирається пара й скільки кошенят — «Comfort підвищує шанс кількох» без чисел.
- (?) Керування в домі (перетягування котів/меблів) — з памʼяті.
- (?) Codex-вікно в грі — не підтверджено; вікі має бестіарій, але це сторонній сайт.
- (?) Гра вийшла в лютому 2026; механіки могли змінитись патчами (вікі веде історію версій).
