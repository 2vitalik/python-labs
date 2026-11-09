---
title: Mage Wars
slug: mage-wars
aka: [Mage Wars Arena]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 2012
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/mage-wars-arena/rulebook", best: true, note: "RulesPal: повні правила — зони, стіни на межах, рух і дії, guard, атака покроково, захист d12, приховані чари, стани, фази раунду, книга заклять"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mage_Wars", note: "Bryan Pope, Arcane Wonders 2012; 2 закляття на раунд, книга на 120 очок, 12 зон, кубики 0/0/1/1*/2/2*, d12, маркери, маги й школи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mage+Wars+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, impassable-cells, status-effects, hot-seat, character-select, pocket, +mana-pool-spells, +spellbook-choice, +prepare-two-spells, +zone-grid, +edge-walls, +guard-intercept, +hindered-zone, +combat-dice-symbols, +armor-absorb, +defense-roll, +hidden-enchantment, +upkeep-cost, +summon-creature, +flying-move, +initiative-order, +quick-full-actions, +deck-building, +status-stacks]
proposes: ["+trigger:round_start", "+effect:prepare_spell", "+effect:roll_dice", "+effect:reveal_card", "+effect:pay_upkeep", "+cond:guarded", "+cond:mana", "+cond:same_zone", "+role:card", "+role:enchantment", "+ui:mana-counter", "+ui:action-markers", "+ui:prepared-spells", "+window:deck-builder", "+feature:apprentice-mode"]
author: opus
date: 2026-11-09
---

# Mage Wars — дуель магів на арені з 12 зон: закляття не тягнуть з колоди, а обирають із власної книги, по два на раунд

## Суть
Кожен гравець — маг зі **збіркою заклять** (spellbook), складеною наперед на 120 очок: на початку раунду він таємно **готує два закляття** з будь-яких у книзі, а потім викликає істот, ставить споруди, накладає чари сорочкою вниз і атакує. Мана приходить щораунду (channeling), шкода рахується кубиками з критами, що ігнорують броню. Поле — 12 зон, між якими можуть стояти стіни; рух і дальність — по зонах ортогонально. Перемога — шкода на ворожому магу ≥ його життя.

## Поле і час
- Арена — сітка з 12 квадратних зон; маги стартують у протилежних кутах. Суміжність лише по ребру (не по куту); дальність рахується ортогонально.
- Стіни — на межах зон: Passage Blocked (непрохідна без Climbing/Flying), Passage Attacks (прохід із атакою), Blocks LoS.
- Раунд = Ready Stage (Initiative → Reset → Channel → Upkeep → Planning → Deployment) + Action Stage (First Quickcast → Action Phases → Final Quickcast).
- Action Phases — гравці по черзі активують по одній своїй істоті, починаючи з власника маркера ініціативи; хто має менше активних істот, може пасувати; раунд закінчується, коли всі діяли.
- Приховане: підготовлені закляття, чари сорочкою вниз, книга суперника.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маг | piece | Life, Channeling, Armor, школи; маркер quickcast | діє як істота + окреме швидке закляття за раунд |
| Істота (creature) | ally | Life, Armor, атаки, швидкість, риси (Fast, Flying, Elusive, Reach…) | одна дія за раунд: рух + швидка дія або повна дія |
| Споруда (conjuration) | object | Life | стоїть у зоні; стіни — на межі зон |
| Стіна | static | Passage Blocked / Passage Attacks / Blocks LoS | на межі зон |
| Чари (enchantment) | object | ціна накладання 2, ціна відкриття | прихована, поки не відкрита; не сплатив — знищено |
| Спорядження (equipment) | object | — | на магові |
| Атакувальне закляття / інкантація | object | — | одноразові: після дії — у скид |
| Зона | zone | — | одиниця руху й дальності |
| Кубик атаки | object | грані 0, 0, 1, 1*, 2, 2* | * — крит, ігнорує Armor |
| Кубик ефектів d12 | object | 1–12 | спецефекти, захист, зняття станів, випадковий напрямок, ініціатива |
| Маркер guard | mark | — | вартовий: ближні атаки в зоні мають бити його |
| Маркер дії / ready / quickcast | mark | активний / витрачений | хто вже діяв; захисти «1X» на раунд |
| Маркери станів | mark | Burn, Rot, Daze, Stun, Weak, Restrained… | ефекти на сутності |
| Маркер ініціативи | mark | — | переходить щораунду |
| Книга заклять | supply | 120 очок збірки | звідси готують 2 закляття на раунд |
| Мана | resource | — | платять ціну заклять і утримання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(initiative)` → ТО `custom: «раунд 1 — кидок d12; далі маркер ініціативи переходить до суперника»`.
- КОЛИ `phase_start(channel)` → ТО `currency(mage, +channeling)`.
- КОЛИ `phase_start(upkeep)` → ЯКЩО `custom: «у обʼєкта є ціна утримання»` → ТО `custom: «сплатити, інакше обʼєкт знищено»`; тут же `damage` від Burn і Rot, Regenerate → `heal`.
- КОЛИ `phase_start(planning)` → ТО `choose(spellbook, ≤ 2)` сорочкою вниз; `custom: «невикористані повертаються в книгу на наступному Planning»`.
- КОЛИ `input(move, c, zone)` → ЯКЩО `custom: «зона ортогонально суміжна»` and `custom: «на межі нема Passage Blocked (або Climbing/Flying)»` → ТО `move(c, zone)`; повна дія — без руху перед нею, швидка — після 1 руху (2 рухи за раунд); Fast — 2 рухи перед швидкою.
- КОЛИ `custom: «вхід у зону з ворогами або вихід із неї»` → ТО `set_state(c, hindered)` — `custom: «лише один рух»` (крім Flying, Elusive, Teleport, Push…).
- КОЛИ `input(cast, mage, spell)` → ЯКЩО `custom: «спел підготовлено»` and `custom: «мана ≥ ціни»` and `custom: «ціль у дальності 0–N зон»` → ТО `currency(−cost)`, `custom: «ефект за типом закляття»`; атака й інкантація → скид.
- КОЛИ `input(cast, mage, creature)` → ТО `place(mage, creature)` у зону; `input(cast, mage, wall)` → `place(mage, wall)` на межі.
- КОЛИ `input(enchant, mage, target)` → ТО `custom: «сорочкою вниз за 2 мани»`; КОЛИ `input(reveal, ench)` → ЯКЩО `custom: «сплачено ціну відкриття»` → ТО `custom: «чари діють»`; інакше `disappear(ench)`; обовʼязкові чари (Block) відкриваються на свій тригер.
- КОЛИ `input(quickcast, mage)` → ЯКЩО `not state(mage, quickcast_used)` → ТО `custom: «швидке закляття до/після дії будь-якої істоти або у фазах Quickcast»`, `set_state(mage, quickcast_used)`.
- КОЛИ `input(guard, c)` → ТО `set_state(c, guard)` (швидка дія).
- КОЛИ `input(melee, a, t)` → ЯКЩО `custom: «t у тій самій зоні»` → ЯКЩО `custom: «у зоні є ворожий вартовий»` → ТО `custom: «ціль — лише вартовий»`.
- КОЛИ `input(ranged, a, t)` → ЯКЩО `line_of_sight(a, t)` and `custom: «t у дальності»` → ТО атака; `custom: «вартових ігнорує»`.
- Атака: КОЛИ `custom: «атаку оголошено, ціну сплачено»` → ТО `custom: «Roll to Miss → Avoid → кидок кубиків → шкода і ефекти → додаткові удари → Damage Barrier → Counterstrike»`.
- Захист: КОЛИ `custom: «атака по t з Defense»` → ЯКЩО `custom: «d12 ≥ числа щита»` and `not state(defense, used)` → ТО `block`; Unavoidable — без захисту.
- Шкода: КОЛИ `custom: «кидок кубиків атаки»` → ТО `damage(t, звичайні − Armor)` + `damage(t, крити)`; КОЛИ `custom: «d12 ≥ порогу ефекту»` → ТО `set_state(t, condition)`.
- КОЛИ `custom: «шкода на t ≥ Life»` → ТО `disappear(t)`; ЯКЩО `custom: «t — ворожий маг»` → ТО `win`.
- КОЛИ `state_on(c, stun)` → ТО `custom: «не діє до кінця свого наступного Action Phase»`; КОЛИ `custom: «кінець Action Phase істоти»` → ЯКЩО `custom: «d12 = порогу втечі»` → ТО `clear_state(c, condition)`.
- Flying: `custom: «ігнорує стіни й нелітаючих під час руху; нелітаючі без Reach не бʼють його в ближньому»`; літаюча, що бʼє нелітаючу в ближньому, тимчасово втрачає Flying.
- Перемога: ворожий маг знищений · Поразка: свій маг знищений · Рахунок: —.

## Керування і ввід
- Настільна: гравець бере картки з теки-книги, кладе 2 сорочкою на планшет, у свою фазу активує істоту (маркер дії перевертається) і оголошує дію; кубики кидає сам.
- Режими дії: швидка (рух + дія) / повна (лише дія) / quickcast мага / guard.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): арена 12 зон зі стінами на межах; `+ui:mana-counter` і Life обох магів; `+ui:prepared-spells` — 2 слоти підготовлених заклять; `+ui:action-markers` — хто вже діяв; маркери станів на картках; `turn-indicator` з маркером ініціативи; лоток кубиків; `pocket` — книга заклять.
- `character-select` (цифрова версія): вибір мага (Beastmaster, Priestess, Warlock, Wizard + маги доповнень).
- `+window:deck-builder` (цифрова версія): збірка книги на 120 очок за школами мага.
- `help-window` — кодекс риc і станів; `end-screen` — переможець.

## Фічі поза полем
- `+feature:apprentice-mode` — навчальний режим на половині арени (2×3) з готовими книгами.
- Повна гра — власні книги на 120 очок; 6 основних шкіл (Holy, Nature, Dark, Mind, Arcane, War) і 4 стихійні (Fire, Earth, Air, Water); у кожного закляття — ціна в очках книги.
- 2–6 гравців, ~90 хвилин; доповнення додають магів (Forcemaster, Warlord, Druid, Necromancer, Siren, Paladin).

## Варіації й родичі
- Родичі: [Chaos: The Battle of Wizards](chaos-battle-of-wizards.md) (дуель магів на клітинах, виклик істот), [Summoner Wars](summoner-wars.md) (призивач і колода фракції), [Mage Knight](mage-knight.md), [Card Hunter](card-hunter.md).
- **Осі варіацій** доступу до заклять: випадкова рука з колоди ([summoner-wars](summoner-wars.md)) / книга на вибір, 2 на раунд (тут) / фіксований список із перезарядкою ([battlecon](battlecon.md) — картки повертаються через 2 біти) · **поле**: клітини / зони з межами-стінами (тут).

## Цікавинки для курсу
- Поле з 12 зон зі стінами як властивістю ребра між зонами — 📎 (граф зон + атрибути ребер).
- Підготовка 2 заклять із повної книги з поверненням невикористаних — 🌱.
- Приховані чари: два стани картки, ціна відкриття, «не сплатив — згорає» — 📎.
- Guard: ближні атаки в зоні примусово йдуть у вартового, дальні — ігнорують — 🌱.
- Кубики з критами, що ігнорують броню, + d12 ефектів — 🌱.
- Фазова структура раунду з утриманням і поперемінною активацією — 🥉 (машина станів фаз).
- Конструктор книги на бюджет очок зі школами — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ ближні в зоні / дальні з дальністю · `line-of-sight-attack` · `impassable-cells` ↔ Passage Blocked · `status-effects` ↔ Burn, Rot, Stun, Daze… · `hot-seat` · `character-select` ↔ вибір мага · `pocket` ↔ книга.
- **Нема** → пропозиції карток:
  - `+mana-pool-spells`, `+edge-walls`, `+combat-dice-symbols`, `+armor-absorb`, `+summon-creature`, `+flying-move`, `+initiative-order`, `+deck-building`, `+status-stacks` — уже в корпусі.
  - `+spellbook-choice` «Закляття з книги на вибір, не з колоди» · game-logic/economy · 📎.
  - `+prepare-two-spells` «Таємно підготувати N заклять на раунд» · game-logic/opponent · 🌱 · слот {n: 2}.
  - `+zone-grid` «Поле зонами, рух і дальність по зонах» · entities/legality · 📎.
  - `+guard-intercept` «Вартовий перехоплює ближні атаки в зоні» · entities/combat · 🌱.
  - `+hindered-zone` «Вхід/вихід із зони з ворогами — лише один рух» · entities/legality · 🌱.
  - `+defense-roll` «Захист кидком d12 ≥ порогу, раз на раунд» · entities/combat · 🌱.
  - `+hidden-enchantment` «Чари сорочкою з ціною відкриття» · entities/state · 📎.
  - `+upkeep-cost` «Утримання обʼєкта щораунду, інакше знищено» · game-logic/economy · 🌱.
  - `+quick-full-actions` «Швидка дія з рухом / повна без руху» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+trigger:round_start` (з card-hunter) — початок раунду з фазами.
- `+effect:prepare_spell` — покласти закляття з книги сорочкою; `+effect:roll_dice` (з card-hunter); `+effect:reveal_card` — відкрити приховану картку за ціну; `+effect:pay_upkeep` — сплатити утримання.
- `+cond:guarded` — у зоні є вартовий; `+cond:mana` — мана ≥ ціни; `+cond:same_zone` — у тій самій зоні.
- `+role:card` (з summoner-wars); `+role:enchantment` — прихована картка-чари на сутності.
- `+ui:mana-counter`; `+ui:action-markers` — хто вже діяв у раунді; `+ui:prepared-spells` — слоти підготовлених заклять.
- `+window:deck-builder` (з summoner-wars) — збірка книги; `+feature:apprentice-mode` — спрощений режим на половині поля з готовими книгами.

## Джерела
- ⭐ [RulesPal: Mage Wars Arena rulebook](https://rulespal.com/mage-wars-arena/rulebook) — 12 зон, суміжність по ребру, стіни трьох видів, рух/швидка/повна дія, Fast, Hindered, дальність, guard, кроки атаки, захист d12, Flying, приховані чари з ціною 2, стани, утримання, фази, 2 закляття на Planning, Apprentice Mode.
- [Wikipedia: Mage Wars](https://en.wikipedia.org/wiki/Mage_Wars) — автор, рік, 2–6 гравців, 120 очок книги, типи заклять, quickcast, кубики 0/0/1/1*/2/2*, d12, маркери, маги й школи.
- YouTube: пошук «Mage Wars how to play».

## Непевне
- (?) Розклад зон 4×3 — джерела кажуть лише «12 зон» і «Apprentice — половина, 2×3».
- (?) Що відбувається у фазі Deployment (у прочитаному тексті без опису).
- (?) Ціна закляття в очках книги для «чужих» шкіл (подвійна?) — з памʼяті.
- (?) Mage Wars Academy — окрема спрощена гра без арени (з памʼяті).
- (?) Наявність офіційної цифрової версії.
