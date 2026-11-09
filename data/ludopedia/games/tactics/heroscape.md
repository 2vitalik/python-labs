---
title: Heroscape
slug: heroscape
aka: [HeroScape, Хероскейп, "Heroscape: Age of Annihilation"]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 2004
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Heroscape", best: true, note: "гекс-плитки з висотою, типи терену, армійські карти, 3 маркери наказів + фальшивий, d20 ініціатива, кубики черепів/щитів, базова і майстер-гра, сети"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=heroscape+how+to+play", note: "пошук; правила й геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, height-levels, floor-types, impassable-cells, line-of-sight-attack, piece-move-patterns, hot-seat, destroy-all-enemies, match-setup, mode-select, +hex-grid-render, +modular-board, +terrain-builder, +army-points-draft, +army-card-stats, +order-markers, +bluff-marker, +initiative-roll, +combat-dice-symbols, +opposed-dice-wounds, +height-attack-bonus, +terrain-move-cost, +climb-cost, +squad-vs-hero, +move-then-attack, +lost-turn, +counterstrike, +scenario-victory, +basic-advanced-rules]
proposes: ["+trigger:round_start", "+trigger:marker_revealed", "+cond:higher_than", "+cond:engaged", "+effect:roll_dice", "+effect:place_marker", "+effect:wound", "+role:squad", "+role:hero", "+role:army_card", "+ui:order-markers", "+ui:wound-markers", "+ui:dice-tray", "+window:army-builder", "+window:map-builder", "+feature:map-sharing", "+axis:field=hex-height", "+card:order-markers", "+card:height-attack-bonus"]
author: opus
date: 2026-11-09
---

# Heroscape — мініатюрний варгейм на зібраному з гекс-плиток ландшафті з висотою, де ходи розписують таємними маркерами наказів

## Суть
Кожен гравець збирає армію з фігурок-героїв і загонів, кожен має **армійську карту** зі статами. Поле будують з взаємозамкових гекс-плиток **кількох рівнів висоти** й різного терену (трава, скеля, вода, лава, лід, дороги, руїни, замки). Раунд: гравці потай кладуть **три маркери наказів** (1-й, 2-й, 3-й, плюс фальшивий) на свої армійські карти, кидають d20 на ініціативу й по черзі активують карти з маркером відповідного номера. Бій — кидок кубиків атаки (черепи) проти кубиків захисту (щити); висота й терен додають кубики.

## Поле і час
- Поле — гекс-сітка, складена з плиток 1/2/3/7/24 гексів (?) у **3D-ландшафт**: плитки ставлять одна на одну → кожен гекс має висоту в рівнях. Карту будують за сценарієм або вільно.
- Терени: grass, rock, sand, water, ruins, molten lava, lava field, snow, ice, swamp, dungeon, shadow, road, concrete, asphalt, дерева, glaciers, джунглі, мости, замки (стіни, вежі, брама).
- Ефекти терену: небезпечний (лава), непрохідний (glacier), сповільнює (сніг), прискорює (дорога), бонусні кубики атаки/захисту.
- Висота: підйом коштує додаткового руху за кожен рівень; спуск — без доплати.
- Раунд: розстановка маркерів → кидок d20 → три «ходи» гравців по черзі (номер 1, потім 2, потім 3), починаючи з переможця ініціативи і далі ліворуч.
- Інформація прихована: маркери наказів лежать лицем донизу до активації; один з них може бути фальшивим.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Армійська карта | supply (`+role:army_card`) | Life, Move, Range, Attack, Defense; у майстер-грі — Points, вид, клас, характер, розмір, здібності | приймає маркери наказів; активує свої фігурки |
| Унікальний герой | piece (`+role:hero`) | кілька Life, одна фігурка | один на армію; рани накопичуються на карті |
| Загальний герой | piece | — | дозволено кілька копій |
| Унікальний загін (squad) | piece (`+role:squad`) | 1 Life на фігурку, кілька фігурок | одна карта рухає всі фігурки, потім усі атакують |
| Загальний загін | piece | — | дозволено кілька копій |
| Маркер наказу 1/2/3 | mark | номер (таємний) | визначає, яку карту активувати в N-й хід раунду |
| Фальшивий маркер (X) | mark | — | нічого не активує; блеф |
| Маркер рани | mark | — | +1 за кожну непогашену влучність; рани = Life → знищено |
| Гекс трави / скелі / піску | terrain | висота | звичайний рух |
| Вода | terrain | — | рух через неї сповільнений або зупиняє (?) |
| Лава | hazard | — | небезпечна: кидок на шкоду (?) |
| Глетчер / скеля-виступ | static | — | непрохідні |
| Сніг / болото | terrain | — | сповільнює рух |
| Дорога / асфальт | terrain | — | прискорює рух |
| Руїни, дерева, замок | static | висота | перешкода, укриття, висока позиція |
| Кубик атаки (1-ше вид.) | supply | 3 грані з черепом | влучання = череп |
| Кубик захисту (1-ше вид.) | supply | 2 грані зі щитом | блок = щит |
| Комбінований кубик (2-ге вид.) | supply | 3 атаки, 2 захисту, 1 порожня | один кубик для обох ролей |
| Гліф (glyph) | pickup | — | «руна» на гексі: бонус тому, хто стоїть (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО кожен гравець `custom: «кладе маркери 1, 2, 3 і фальшивий X лицем донизу на свої армійські карти (кілька на одну — можна)»`.
- КОЛИ `custom: «маркери розставлено»` → ТО `roll(d20)` кожен; найвищий ходить першим, далі ліворуч.
- КОЛИ `turn_start(player)` → ТО `reveal(marker_n)`; активується карта з маркером поточного номера.
- КОЛИ `custom: «карта з маркером N уже знищена»` → ТО `skip_turn(player)` — хід втрачено.
- КОЛИ `input(move, figure, hex)` → ЯКЩО `custom: «сума кроків ≤ Move, кожен підйом на рівень коштує додатково, спуск безкоштовно»` and `free(hex)` → ТО `move(figure, hex)`.
- КОЛИ `enter(figure, slow_terrain)` → ТО `custom: «рух коштує більше»`; КОЛИ `enter(figure, road)` → ТО `custom: «рух коштує менше»` (?).
- КОЛИ `input(move)` → ЯКЩО `cell(hex, glacier | outcrop)` → ТО `block`.
- КОЛИ `enter(figure, lava)` → ТО `custom: «небезпечний терен: кидок кубика на шкоду»` (?).
- КОЛИ `custom: «загін активовано»` → ТО `custom: «спершу рухаються всі фігурки, потім усі атакують»`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, Range)` and `line_of_sight(a, b)` → ТО `roll(attack_dice = Attack)`, `roll(defense_dice = Defense)`.
- КОЛИ `custom: «атакувальник вище за ціль»` → ТО `custom: «+1 кубик атаки»`; КОЛИ `custom: «ціль вище»` → ТО `custom: «+1 кубик захисту»` (?).
- КОЛИ `custom: «терен/здібність дає бонус»` → ТО `custom: «+N кубиків атаки або захисту»`.
- КОЛИ `custom: «кубики кинуто»` → ЯКЩО `custom: «щитів ≥ черепів»` → ТО `block`; інакше `damage(черепи − щити)` — маркери ран.
- КОЛИ `counter(wounds, ≥, Life)` → ТО `disappear_b` (фігурку знято); у базовій грі Life = 1 — будь-яка непогашена влучність знищує.
- КОЛИ `custom: «захисник зі здібністю Counter Strike»` → ЯКЩО `custom: «зайві щити»` → ТО `damage(attacker, n)` (?).
- КОЛИ `custom: «фігурка поруч з ворогом іде геть»` → ТО `custom: «ворог отримує атаку на відході (leaving engagement)»` (майстер-гра) (?).
- КОЛИ `custom: «спуск з висоти ≥ зросту фігурки»` → ТО `custom: «кидок на шкоду від падіння»` (?).
- КОЛИ `enter(figure, glyph)` → ТО `custom: «ефект гліфа (бонус атаки/захисту/руху)»` (?).
- КОЛИ `custom: «кінець третього ходу»` → ТО `custom: «маркери знято, новий раунд»`.
- КОЛИ `all_gone(enemy_figures)` → ТО `win` (last-player-standing); інші сценарії — `custom: «утримати точку / ліміт раундів / квест»`.
- КОЛИ `custom: «турнір: час вичерпано»` → ТО `custom: «перемагає той, у кого лишилось більше очок армії (дробовий підрахунок)»`.
- Перемога: за сценарієм (знищити всіх, утримати місце, квест, ліміт раундів) · Поразка: армію знищено · Рахунок: очки армії в турнірі.

## Керування і ввід
- Настолка 2+ гравців (8+ років): фігурки рухають руками по гексах; маркери кладуть таємно на картки.
- Цифрова версія: клік по армійській карті → розстановка маркерів (drag 1/2/3/X); клік по фігурці → підсвітка досяжних гексів з урахуванням висоти; клік по ворогу в зоні дальності → кидок кубиків з анімацією.
- Між партіями: побудова армії в межах бюджету очок і збір мапи з плиток.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `mode-select` (базова / майстер-гра, сценарій) → `+window:map-builder` (збір ландшафту) → `+window:army-builder` (картки, бюджет очок) → `game-screen`.
- `game-screen`: 3D-гекс-поле з висотами (камера обертається); панель армійських карт з `+ui:order-markers` і `+ui:wound-markers`; `turn-indicator`; `+ui:dice-tray` з черепами/щитами; `reachable-highlight`; висота гекса під курсором.
- `confirm-dialog` перед відкриттям маркера; `end-screen` з переможцем і підрахунком очок.
- `help-window` / `codex-window` армійських карт.

## Фічі поза полем
- Два рівні правил: **базова гра** (лише Move/Range/Attack/Defense, 1 Life, швидко для дітей) і **майстер-гра** (очки, здоров'я, вид, клас, розмір, спецздібності).
- Драфт армії за бюджетом очок сценарію; унікальні юніти — по одному на армію, загальні — без ліміту.
- Мапи-сценарії й вільні мапи; фанатська спільнота ділиться мапами (`+feature:map-sharing`).
- Набори: 4 майстер-сети (Rise of the Valkyrie 2004 — 30 фігурок, 85 плиток терену; Swarm of the Marro; Marvel; D&D Battle for the Underdark), розширення фігурок і терену; перевидання Renegade 2024 (Age of Annihilation).
- Турнірні правила з дробовим підрахунком очок за часом.

## Варіації й родичі
- У корпусі: [memoir-44](memoir-44.md) (гекси, кубики з символами, карти наказів по секторах), [battletech](battletech.md) (гекси з висотою, мехи), [descent-journeys-in-the-dark](descent-journeys-in-the-dark.md) (модульне поле, кубики), [final-fantasy-tactics](final-fantasy-tactics.md) (висота як ресурс атаки), [zombicide](zombicide.md) (теж модульне поле).
- Осі варіацій:
  - **висота**: нема / шари рендеру / справжня 3D-висота з ціною підйому й бонусом кубика (Heroscape, FFT);
  - **черга ходів**: по сторонах / таємні маркери 1-2-3-X + d20 ініціатива щораунду (Heroscape) / карти наказів по секторах (Memoir 44);
  - **бій**: детермінований / кидок проти кидка (Heroscape) / кубик проти порогу (Zombicide);
  - **поле**: друковане / модульні тайли (Descent) / **будований 3D-ландшафт** (Heroscape).

## Цікавинки для курсу
- Таємні маркери наказів 1/2/3 + фальшивий: планування раунду наперед з блефом — 📎.
- Гекс-поле з висотою: ціна підйому, безкоштовний спуск, BFS по гексах з вагами — 🥉.
- Бонус кубика за висоту й терен; розв'язок «черепи − щити» — 🌱.
- Загін: одна карта рухає N фігурок, спершу всі ходять, потім усі б'ють — 📎.
- Редактор ландшафту з плиток кількох розмірів і рівнів — 🥈.
- Драфт армії за бюджетом очок з обмеженням унікальних — 📎.

## Мапа на каталог
- Є: `hp-damage` ↔ Life і рани · `melee-vs-ranged` ↔ Range 1 vs 4+ · `height-levels` · `floor-types` ↔ терени · `impassable-cells` ↔ глетчери · `line-of-sight-attack` · `hot-seat` · `destroy-all-enemies` · `match-setup` · `mode-select` ↔ базова/майстер.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (з Memoir 44) — гексове поле.
  - `+terrain-builder` «Поле, зібране гравцем з плиток кількох рівнів» · levels/editor · 🥈.
  - `+order-markers` «Таємні маркери черговості на картах» · game-logic/opponent · 📎 · слоти {markers: [1, 2, 3], decoy: true}.
  - `+bluff-marker` «Фальшивий маркер» · game-logic/opponent · 🌱.
  - `+initiative-roll` «Кидок на ініціативу щораунду» · game-logic/opponent · 🌱 · слот {die: d20}.
  - `+opposed-dice-wounds` «Черепи мінус щити = рани» · entities/combat · 🌱.
  - `+height-attack-bonus` «Вища позиція дає кубик» · entities/combat · 🌱.
  - `+climb-cost` «Підйом коштує руху, спуск безкоштовний» · entities/legality · 📎.
  - `+army-points-draft` «Армія за бюджетом очок» · levels/progression · 📎.
  - `+army-card-stats`, `+squad-vs-hero`, `+move-then-attack`, `+lost-turn`, `+counterstrike`, `+scenario-victory`, `+basic-advanced-rules`, `+terrain-move-cost` (з Civilization), `+combat-dice-symbols` (з Descent), `+modular-board`.

## Пропозиції до словників
- `+trigger:round_start` — початок раунду (фаза планування маркерів); `+trigger:marker_revealed(n)` — відкрито маркер наказу.
- `+cond:higher_than(a, b)` — A стоїть вище за B; `+cond:engaged(a)` — фігурка в контакті з ворогом.
- `+effect:roll_dice(n, kind)` — кинути кубики з символами; `+effect:place_marker(card, n)` — покласти маркер наказу; `+effect:wound(a, n)` — рани без зменшення статів.
- `+role:squad` — група фігурок під однією картою; `+role:hero` — одна фігурка з кількома Life; `+role:army_card` — карта статів поза полем.
- `+ui:order-markers` — маркери на картах; `+ui:wound-markers` — рани на карті; `+ui:dice-tray` — лоток кидка.
- `+window:army-builder` — драфт армії; `+window:map-builder` — збір ландшафту.
- `+feature:map-sharing` — обмін мапами-ландшафтами.
- `+axis:field=hex-height` — гекс з висотою (зараз лише `hex` або `layers`).
- `+card:order-markers`, `+card:height-attack-bonus`.

## Джерела
- ⭐ [Wikipedia: Heroscape](https://en.wikipedia.org/wiki/Heroscape) — плитки й рівні висоти, повний список теренів і їх ефекти, стати карт (базова/майстер), типи героїв/загонів, 3 маркери + фальшивий, d20 ініціатива, кубики (1-ше і 2-ге видання), «рани = різниця», сценарії перемоги, сети до 2024.
- YouTube: пошук «heroscape how to play».

## Непевне
- (?) Офіційний буклет правил (Hasbro PDF) і heroscapers.com не відкрились (403) — правила engagement / атаки на відході, падіння з висоти, вода, лава, гліфи, Counter Strike — з памʼяті.
- (?) Точний бонус висоти (+1 кубик атаки/захисту за вищу позицію) — Wikipedia лише каже, що висота «додає кубики».
- (?) Розміри плиток (1/2/3/7/24 гекси) — з памʼяті.
- (?) Офіційної цифрової версії немає; вікна описано як «(цифрова версія)».
