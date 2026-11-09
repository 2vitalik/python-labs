---
title: Mythgard
slug: mythgard
aka: []
family: tower-lanes
also: []
klass: figure
axes:
  field: 1d
  time: turn
  opponent: online
  info: hidden
  random: both
  goal: state
year: 2019
platforms: [PC, macOS, mobile]
links:
  - {kind: other, url: "https://www.mythgardhub.com/new-player-guide", best: true, note: "Mythgard Hub: 7 смуг, загроза 3 смуг, цикл карти → +1 мана +1 гем, типи карт, ключові слова, правила колоди, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mythgard", note: "хід з 4 кроків, крайні смуги б'ють лише 2, посилення смуги переживає істоту, Path і Pursuit"}
  - {kind: steam, url: "https://store.steampowered.com/app/839910/Mythgard/", note: "режими (Story, 2v2, Draft, Ladder, Puzzles), deck tracker, реплеї, крос-плей"}
  - {kind: official, url: "https://mythgardgame.com/", note: "шість фракцій, гнучкі правила колоди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mythgard+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, pocket, hp-damage, legal-move-highlight, threat-range, status-effects, ai-opponent, online-multiplayer, rating-system, move-timer, mode-select, tutorial-window, replay, +lane-grid, +deck-draw, +deck-builder, +card-collection, +card-keywords, +mana-pool-spells, +card-cycling, +three-lane-threat, +persistent-lane-enchant, +taunt-targeting, +retaliation, +artifact-durability, +go-second-compensation, +deck-passive-path, +hero-power-once, +unit-action-budget, +shared-middle-lane, +draft-mode, +rarity-copy-limit, +deck-tracker, +cross-play]
proposes: ["+effect:draw_card", "+effect:cycle_card", "+effect:banish", "+role:card", "+role:lane", "+cond:lane_has", "+ui:damage-preview", "+ui:deck-tracker", "+ui:gem-pips", "+window:deck-builder", "+window:collection-window", "+feature:cross-play", "+card:card-cycling", "+card:three-lane-threat", "+card:persistent-lane-enchant", "+card:artifact-durability"]
author: opus
date: 2026-11-09
---

# Mythgard — колекційна картярка на 7 смугах: мініон загрожує своїй і двом сусіднім, а посилення смуги переживає мініона

## Суть
Два гравці викладають мініонів у **7 смуг** свого боку; мініон б'є одну з трьох смуг навпроти (пряму або сусідні) і може зсуватися на смугу вбік. Ресурс будується не землями, а **циклом карти**: раз за хід скинути карту в колоду → +1 максимальної мани і +1 гем кольору карти. Окремий тип карт — **зачарування смуги**: бонус лишається на смузі, коли мініон гине, і дістається наступному. Хто першим падає до 0 життя — програє.

## Поле і час
- Поле — **7 смуг на кожен бік** (два ряди по 7 слотів, лінійна сітка); у смузі — один мініон (?), до неї ж прикріплюються зачарування.
- Сусідство лінійне: мініон «бачить» смугу навпроти і дві сусідні (3 смуги); на крайніх смугах — лише 2 (Wikipedia).
- Хід почерговий, з кроками: добір → (необовʼязково) цикл карти → розіграш карт → дії мініонів (атака або рух). Таймер ходу є всюди, крім Brawl проти AI.
- 2v2 Melee: у кожного гравця **6 смуг**, середня смуга спільна з союзником.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мініон | piece (`+role:card`) | Strength, Health, ціна (мана + геми), ключові слова | ставиться у вільну свою смугу; за Standard Action атакує одну з 3 загрожених смуг або рухається на 1 смугу |
| Смуга ×7 | zone (`+role:lane`) | власник, зачарування | тримає мініона; на ній висять зачарування |
| Зачарування (Enchantment) | zone | смуга, ефект | постійне: бафає свого мініона в смузі або карає ворожих навпроти; лишається після смерті мініона |
| Закляття (Spell) | object | ціна, ціль: карта / гравець / смуга | одноразовий ефект, потім у Boneyard |
| Артефакт | object | Durability, ефекти | постійні й активовані ефекти гравця; ≤ 5 у грі; найновіший втрачає 1 Durability за кожне очко прямої шкоди гравцю |
| Гравець (аватар) | player | життя (старт залежить від Path) | 0 життя — поразка |
| Path | static | обирається в колоді | пасивне правило на всю партію; задає стартове життя і бонус Pursuit |
| Power | object | ціна, раз за хід | активована здібність гравця, обрана в колоді (Foresight, Impel, Infuse, Mend, Reconstruct, Smite) |
| Мана | resource | max = кількість циклів | витрачається автоматично, відновлюється до max на початку свого ходу |
| Геми ×6 кольорів | resource | синій Norden · жовтий Aztlan · червоний Oberos · зелений Dreni · помаранчевий Parsa · фіолетовий Harmony | вимога кольору карти; дає цикл карти свого кольору |
| Колода · рука · Boneyard | zone | колода 40–200 | циклована карта вертається в колоду у випадкове місце, не нагору |
| Defender | piece | — | не атакує; вороги мусять бити його першим |
| Lurker | piece | — | вороги мусять бити інших блокерів раніше за нього |
| Agile | piece | — | атакує будь-яку з 3 смуг, ігноруючи обмеження атаки й блоку |
| Swift · Teleport · Immobile | piece | — | додатковий рух · рух у будь-яку смугу · не рухається сам |
| Armor X · Piercing · Fragile X | piece | X | −X отриманої шкоди · ігнорує Armor · +X отриманої шкоди |
| Alpha Strike · Deadly · Overrun | piece | — | б'є першим (вбитий не відповідає) · будь-яка шкода вбиває · надлишок шкоди йде гравцю |
| Slayer X · Focused X · Blast X | piece | X | +X проти мініонів · +X проти смуги навпроти · X шкоди сусіднім ворожим мініонам після удару |
| Life Tap · Breach | piece | — | лікує власника на завдану шкоду · тригер на шкоду гравцю |
| Blight X · Regen X | piece | X | −X/−X на початку свого ходу · +X Health наприкінці свого ходу |
| Stealth · Warded · Immortal | piece | — | особа прихована до взаємодії · без шкоди поза боєм · без шкоди й знищення |
| Stunned · Suppressed | piece | стан | не атакує, не рухається, не активує · знято здібності й бафи |
| Ephemeral · Banish | piece | — | покидає гру замість Boneyard; Banish — без Demise |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «перемішати колоди; хто ходить другим — отримує бонус Pursuit свого Path»`.
- КОЛИ `turn_start(side)` → ТО `custom: «draw_card ×1»`, `custom: «мана й геми відновлюються до максимуму»`, `custom: «мініони отримують Standard Action»`.
- КОЛИ `input(cycle, card)` → ЯКЩО `turn_of(side)` and `custom: «цього ходу ще не циклив»` and `not state(card, cycled)` → ТО `custom: «cycle_card: карта → колода у випадкове місце»`, `counter(max_mana, +1)`, `counter(gem[колір карти], +1)`, `set_state(card, cycled)`.
- КОЛИ `input(play, card)` → ЯКЩО `counter(mana, >=, cost)` and `custom: «є геми потрібних кольорів»` → ТО `custom: «списати ману й геми»`; інакше `block`.
- КОЛИ `input(drag, minion, lane)` → ЯКЩО `free(own_lane)` → ТО `place(player, minion)`; мініон без Standard Action цього ходу (крім Rush).
- КОЛИ `spawned(minion)` → ЯКЩО `custom: «має Awaken»` → ТО `custom: «ефект Awaken»`.
- КОЛИ `input(drag, enchantment, lane)` → ТО `place(player, enchantment)`, `set_state(lane, enchanted)`.
- КОЛИ `input(drag, artifact)` → ЯКЩО `count(own_artifacts, <, 5)` → ТО `place(player, artifact)`; інакше `block`.
- КОЛИ `input(attack, minion, target_lane)` → ЯКЩО `custom: «є Standard Action»` and `in_range(minion, target_lane, 1)` and `occupied(target_lane, enemy_minion)` → ТО `damage(target, strength)`, `damage(minion, target_strength)` (відповідь захисника).
- КОЛИ `input(attack, minion, target_lane)` → ЯКЩО `not occupied(target_lane, enemy_minion)` and `count(enemy_minions_in_threatened_lanes, ==, 0)` → ТО `damage(opponent, strength)`; інакше `block` (спершу мініони).
- КОЛИ `input(attack, minion, target)` → ЯКЩО `custom: «серед загрожених є Defender»` and `not state(minion, agile)` → ТО `custom: «ціль лише Defender»`; Lurker — ціль лише коли інших блокерів нема.
- КОЛИ `input(move, minion, lane)` → ЯКЩО `in_range(minion, lane, 1)` and `free(lane)` and `not state(minion, immobile)` and `custom: «цього ходу не атакував»` → ТО `move(minion, lane)`; Teleport — будь-яка смуга; Swift — ще один рух перед іншими.
- КОЛИ `hp_zero(minion)` → ТО `disappear(minion)`, `custom: «→ Boneyard»`.
- КОЛИ `died(minion)` → ЯКЩО `custom: «має Demise»` → ТО `custom: «ефект Demise»`.
- КОЛИ `died(minion)` → ЯКЩО `state(lane, enchanted)` → ТО `custom: «зачарування лишається; наступний мініон у смузі отримує бонус»`.
- КОЛИ `custom: «пряма шкода гравцю n»` → ЯКЩО `count(own_artifacts, >, 0)` → ТО `counter(durability[найновіший артефакт], -n)`; КОЛИ `counter(durability, ==, 0)` → ТО `disappear(artifact)`.
- КОЛИ `custom: «бойова шкода n»` → ЯКЩО `state(target, armor_x)` and `not state(attacker, piercing)` → ТО `damage(target, n - X)`.
- КОЛИ `custom: «бойова шкода > Health цілі»` → ЯКЩО `state(attacker, overrun)` → ТО `damage(opponent, excess)`.
- КОЛИ `custom: «бойова шкода > 0»` → ЯКЩО `state(attacker, deadly)` → ТО `disappear(target)`; Life Tap — `heal(owner, n)`.
- КОЛИ `after(damage)` → ЯКЩО `state(attacker, blast_x)` → ТО `damage(adjacent_enemy_minions, X)`.
- КОЛИ `turn_start(side)` → ЯКЩО `state(minion, blight_x)` → ТО `custom: «−X/−X»`; КОЛИ `turn_end(side)` → ЯКЩО `state(minion, regen_x)` → ТО `heal(minion, X)`.
- КОЛИ `input(power)` → ЯКЩО `custom: «цього ходу Power ще не вживали»` and `counter(mana, >=, cost)` → ТО `custom: «ефект Power»`.
- КОЛИ `input(divination_x)` → ТО `custom: «глянути X верхніх, одну — нагору, решту — під неї»`.
- КОЛИ `custom: «Banish / Ephemeral покидає гру»` → ТО `custom: «banish: поза грою, без Demise і Boneyard»`.
- КОЛИ `input(end_turn)` або `custom: «таймер ходу вичерпано»` → ТО `end_turn`.
- КОЛИ `counter(life, <=, 0)` → ТО `lose`; суперник `win`.
- Перемога: життя суперника 0 · Поразка: своє життя 0 · Рахунок: RP рангового сходу.

## Керування і ввід
- Миша/тач: drag карти з руки на смугу (мініон, зачарування) або на ціль (закляття); артефакт — на свою панель.
- Drag від мініона: червоні смуги — можна атакувати, зелені — можна піти; утримання над ціллю без відпускання — прев'ю шкоди.
- Цикл карти: drag з руки на колоду (раз за хід); циклована карта позначена «розбитим кільцем».
- Кнопки Power і End Turn; синя рамка карти в руці — можна зіграти.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story (глави, туторіал у главі 1), Casual, Ranked, Melee 2v2, Brawl (проти AI, без таймера, можна відкласти партію), Puzzle, Gauntlet, Arena; турніри в клієнті.
- `+window:deck-builder` — 40–200 карт, ліміт копій за рідкістю, вибір Path і Power; `+window:collection-window` — колекція, крафт із wildcard.
- `game-screen`: 7 смуг з обох боків, рука (`pocket`), життя обох, мана і `+ui:gem-pips` (геми шести кольорів), до 5 артефактів, Path і кнопка Power, `legal-move-highlight` (червоне/зелене), `+ui:damage-preview`, `+ui:deck-tracker` (побачені / цикловані / зіграні карти), таймер ходу, End Turn.
- `end-screen` — результат, RP, нагороди (монети, прогрес).
- `replay-window` — реплеї останніх 100 матчів; живий перегляд рангових матчів.
- `puzzle-select` — пазли з нагородою 30 або 100 монет.
- Переходи: хаб → вибір колоди → пошук суперника → game-screen → end-screen → хаб.

## Фічі поза полем
- `rank-tiers`: Bronze → Silver → Gold → Mythril, по 10 дивізіонів, кожні 100 RP — дивізіон.
- `mode-puzzle` (Puzzle), `mode-versus`, `mode-coop` (Melee 2v2), `ai-opponent-levels` (Brawl), драфт: Gauntlet (5/7/9 матчів, безкоштовно, далі лише з перемогами) і Arena (9 матчів, кулдаун 9 днів).
- `spectator` (живий перегляд), `replay`, `+feature:cross-play` (ПК і мобайл), щотижневі featured-колоди, щотижнева скриня й фракційні місії.
- `unlockables` / колекція: рідкості Common · Uncommon · Rare · Mythic (ліміт копій 4/3/2/1), wildcard крафтить карту тієї ж рідкості, фракції й сету.

## Варіації й родичі
- Родичі в корпусі: [artifact](artifact.md) (3 дошки-смуги, стрілка атаки навпроти або навскіс), [inscryption](inscryption.md) (колонки навпроти), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md) (смуги з типами), [marvel-snap](marvel-snap.md) (локації з правилами), [gwent](gwent.md) (ряди-суми), [wildfrost](wildfrost.md), The Elder Scrolls: Legends — у черзі (2 смуги, тіньова смуга).
- Поза корпусом: Hearthstone (мана-крива, бойові вигуки ≈ Awaken), Magic: The Gathering (кольорові вимоги), Duelyst ([duelyst](../tactics/duelyst.md) — тактика на сітці з картами).
- **Осі варіацій**: смуги — 2 / 3 / 7 / колонки сітки · загроза мініона — лише навпроти / навпроти ±1 / будь-яка (Agile) · ресурс — щохідний ріст / земля-карта / цикл карти з кольором · бонус смуги — зникає з мініоном / лишається на смузі.

## Цікавинки для курсу
- Загроза «своя ±1 смуга» з примусовим блоком (спершу мініони, Defender першим, Lurker останнім, Agile ігнорує) — 🥉: вибір легальних цілей як фільтр.
- Цикл карти: раз за хід → +1 max мана, +1 гем кольору, карта у випадкове місце колоди, кожна — раз за гру — 📎.
- Двокомпонентна ціна (мана + геми кольорів) — 📎.
- Зачарування смуги, що переживає мініона: стан живе на клітині, а не на фігурі — 🌱.
- Артефакти як «броня гравця»: пряма шкода з'їдає Durability найновішого — 📎.
- Набір 30+ ключових слів як тригери й модифікатори шкоди (Armor/Piercing/Overrun/Deadly/Alpha Strike) — порядок застосування — 🥈.
- 2v2 зі спільною середньою смугою — 🥇 (два гравці на одному боці, спільний слот).

## Мапа на каталог
- Є: `drag-drop-piece` ↔ карта на смугу · `pocket` ↔ рука · `hp-damage` ↔ Strength/Health · `legal-move-highlight` / `threat-range` ↔ червоні й зелені смуги · `status-effects` ↔ Blight/Stunned/Regen · `ai-opponent` (Brawl) · `online-multiplayer`, `rating-system` (RP), `move-timer` · `mode-select`, `tutorial-window`, `replay`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+card-keywords`, `+mana-pool-spells`, `+taunt-targeting`, `+retaliation`, `+draft-mode` — уже в корпусі.
  - `+card-cycling` «Скинути карту в колоду → +1 max ресурсу й колір» · game-logic/economy · 📎.
  - `+three-lane-threat` «Мініон загрожує смузі навпроти і двом сусіднім» · entities/combat · 🌱.
  - `+persistent-lane-enchant` «Бонус живе на смузі, не на мініоні» · entities/state · 🌱.
  - `+artifact-durability` «Пряма шкода гравцю з'їдає міцність найновішого артефакту» · entities/state · 📎.
  - `+go-second-compensation` «Бонус гравцю, що ходить другим (Pursuit)» · game-logic/opponent · 🌱.
  - `+deck-passive-path` «Пасивне правило, обране в колоді» · game-logic/economy · 🌱; `+hero-power-once` «Активна здібність гравця раз за хід» · 🌱.
  - `+unit-action-budget` «Дії юніта за хід: Standard / Rush / Move / Swift / Utility» · entities/state · 🥉.
  - `+shared-middle-lane` «Спільна смуга двох союзників у 2v2» · game-logic/opponent · 🥇.
  - `+rarity-copy-limit` «Ліміт копій у колоді за рідкістю» · 🌱; `+deck-tracker` «Трекер побачених/зіграних карт» · interface/hud · 📎; `+cross-play` · 🥈.

## Пропозиції до словників
- `+effect:draw_card` — взяти карту з колоди (`draw` у коді зайнятий нічиєю).
- `+effect:cycle_card` — карта з руки в колоду у випадкове місце з бонусом ресурсу.
- `+effect:banish` — прибрати з гри без «смертних» тригерів і скиду.
- `+role:card`, `+role:lane` — повтори з Inscryption/Gwent.
- `+cond:lane_has` — у смузі є сутність/зачарування (повтор з Inscryption).
- `+ui:damage-preview` — прев'ю результату атаки при наведенні; `+ui:deck-tracker`; `+ui:gem-pips` — лічильники кольорових ресурсів.
- `+window:deck-builder`, `+window:collection-window` — повтори.
- `+feature:cross-play` — одна партія між ПК і мобайлом.
- `+card:card-cycling`, `+card:three-lane-threat`, `+card:persistent-lane-enchant`, `+card:artifact-durability` — див. «Мапа на каталог».

## Джерела
- ⭐ [Mythgard Hub: New Player Guide](https://www.mythgardhub.com/new-player-guide) — 7 смуг, загроза 3 смуг, атака/рух drag-ом із підсвіткою, цикл (раз за хід, раз за гру, +1 мана +1 гем), типи карт, артефакти ≤5 і Durability, кольори фракцій, Paths і Powers за назвами, ~40 ключових слів, колода 40–200 і копії 4/3/2/1, режими, ранги.
- [Wikipedia: Mythgard](https://en.wikipedia.org/wiki/Mythgard) — хід з 4 кроків, крайні смуги б'ють лише 2, посилення смуги лишається наступному мініону, Path → стартове життя й Pursuit, історія (Rhino Games → Monumental).
- [Steam: Mythgard](https://store.steampowered.com/app/839910/Mythgard/) — режими, deck tracker, реплеї 100 матчів, спостереження, крос-плей.
- [Офіційний сайт](https://mythgardgame.com/) — шість фракцій.
- YouTube: пошук «Mythgard gameplay».

## Непевне
- (?) Один мініон на смугу — випливає з «occupying Minion» у гайді, прямо не сказано; так само `free(lane)` для руху.
- (?) Стартове життя, стартова рука, муліган — у відкритих джерелах не знайдено; залежить від Path.
- (?) Розбіжність назв: Wikipedia — «burn» карти, гайд — «cycle»; механіка та сама.
- (?) Brands — згадані в описі Utility Action без пояснення.
- (?) Ефекти конкретних Path (Disk of Circadia, Fires of Creation, Journey of Souls, Rainbow's End, Turn of Seasons) і Power — у гайді лише картинки.
- (?) Відповідь захисника: прямо описано лише через Alpha Strike («вцілілий захисник не відповідає, якщо помер»).
- (?) Статус проєкту після 2021 (Monumental) і чи працюють сервери зараз.
