---
title: Darkest Dungeon
slug: darkest-dungeon
aka: [DD]
family: tower-lanes
also: [roguelike, tactics]
klass: figure
axes:
  field: 1d
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2016
platforms: [Windows, macOS, Linux, PS4, PS Vita, iOS, Switch, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Darkest_Dungeon", best: true, note: "загін з 4 героїв, ранги спереду/ззаду, вороги теж у рангах, стрес і афлікції, permadeath, трупи"}
  - {kind: other, url: "https://lparchive.org/Darkest-Dungeon/Update%2001/", note: "LP Archive «Your Heroes»: вміння за рангами по класах, рух, knockback/pull, guard, mark, riposte, stun, bleed/blight"}
  - {kind: other, url: "https://lparchive.org/Darkest-Dungeon/Update%2002/", note: "LP Archive «The Tides of Battle»: порядок ходів, Death's Door, deathblow, стрес, світло, резисти, UI бою"}
  - {kind: other, url: "https://lparchive.org/Darkest-Dungeon/Update%2004/", note: "LP Archive: ролі рангів 1–4 і склад загону"}
  - {kind: other, url: "https://earlyguides.pages.dev/darkest-dungeon/beginners-guide", note: "приклади вмінь з рангами (Iron Swan 1→4, Blinding Gas 3–4), стан, Death's Door"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Darkest_Dungeon_II", note: "сиквел 2023: та сама позиційна основа, стосунки героїв"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Darkest+Dungeon", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Darkest+Dungeon+combat+positions", note: "пошук; бій і позиції"}
stage: v1
coverage: 60
mechanics: [hp-damage, status-effects, melee-vs-ranged, permadeath, character-select, inventory-items, +party-formation, +rank-restricted-skills, +knockback, +pull-to-front, +initiative-roll, +speed-turn-order, +hit-chance, +death-door, +stress-meter, +guard-ally, +retaliation, +mark-target, +light-source, +corpse-blocker, +multi-target-ranks]
proposes: ["+cond:position", "+cond:rank_in", "+effect:knockback", "+effect:shuffle", "+trigger:hit", "+ui:rank-dots", "+ui:turn-order-bar", "+ui:stress-bar", "+ui:torch-meter", "+card:rank-restricted-skills", "+card:death-door", "+role:unit"]
author: opus
date: 2026-11-09
---

# Darkest Dungeon — бій двох шеренг по 4 ранги: вміння діють лише з певних позицій і по певних позиціях

## Суть
Готичний роглайк Red Hook Studios; тут описано лише **бойову систему рангів**, без міста, ґринду й експедицій. Загін з чотирьох героїв стоїть шеренгою (ранги 1–4), навпроти — шеренга ворогів; кожне вміння можна застосувати лише з певних рангів і лише по певних рангах цілей. Тому головна тактика — тримати героїв на «своїх» місцях, а вороги ламають стрій відкиданням, підтягуванням і перемішуванням. Поверх HP — стрес: високий ламає героя.

## Поле і час
- Поле — дві **1D-лінії по 4 позиції**, лицем одна до одної (вид збоку); ранг 1 — передній (найближчий до ворога), ранг 4 — задній.
- Хід — покроковий по раундах: кожен живий учасник ходить раз за раунд у порядку ініціативи (Speed + випадковий кидок, за LP — автор «не на 100 % певен»).
- Між боями загін рухається коридорами в реальному часі; рівень світла смолоскипа переноситься в бій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | ally (`+role:unit`) | клас (16 у базі, 20 з DLC), HP, Speed, точність, ухилення, захист, крит, резисти, стрес 0–200, 4 бойові вміння з 7 | ходить у свою чергу; вміння — за рангом |
| Ранг (позиція) | zone | 1–4 на бік | визначає доступні вміння й досяжність цілі |
| Ворог | enemy | HP, Speed, ранги вмінь, резисти | своя шеренга 1–4; ті самі обмеження рангів |
| Труп | object | — | лишається на місці вбитого ворога, тримає позицію (опція «corpses») |
| Вміння ближнього бою | — | ранги запуску 1–2, цілі 1–2 | сильніше, але герой спереду отримує більше шкоди |
| Вміння дальнього бою | — | ранги запуску 3–4, цілі будь-які | слабше; захищені задні ранги |
| Вміння-«рейлган» | — | Iron Swan: з рангу 1 по рангу 4 | обхід звичайного обмеження позицій |
| Вміння по кількох | — | Grapeshot: перші 3 · Plague Grenade: ранги 3–4 · Wicked Hack: 1–2 | бʼє групу рангів одночасно, часто зі штрафом шкоди |
| Рух собою | — | Lunge: вперед на 2 · Get Down!: назад на 1 · Solo: у ранг 1 | герой зсувається, інші міняються з ним місцями |
| Knockback / Pull | — | на 1–3 ранги | Uppercut/Purge відкидають ціль назад; Come Hither/Daemon's Pull тягнуть уперед на 2 |
| Перемішування | — | — | Flashbang ставить ціль на випадкову позицію; Disorienting Blast тягне задній ранг уперед, оглушує, прибирає трупи |
| Stun | — | шанс проти резисту | оглушений пропускає наступний хід |
| Bleed / Blight | hazard | шкода за хід | DoT; провокує deathblow |
| Mark | — | — | позначена ціль отримує більше шкоди від окремих вмінь; ворог частіше бʼє позначеного героя (без гарантії) |
| Guard | — | — | охоронець отримує удари замість підопічного (Defender, Guard Dog) |
| Riposte | — | — | контратака у відповідь на кожен удар (Duelist's Advance, Retribution) |
| Death's Door | — | deathblow resist (67 % база, стеля 87 %) | стан на 0 HP: штрафи, кожен новий удар — шанс смерті |
| Смолоскип (світло) | resource | 0–100 | яскраво — менше стресу, частіше заскочиш ворога; темно — більше луту й критів |
| Предмети загону | pickup | смолоскипи, ліки | у бою можна вжити смолоскип і ліки, їжу — ні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО `custom: «черга ходів за Speed + кидок (?)»`.
- КОЛИ `input(skill, target)` → ЯКЩО `legal(skill)` and `custom: «ранг героя ∈ ранги запуску вміння»` and `custom: «ранг цілі ∈ ранги-цілі»` → ТО `custom: «вміння застосовано»`; інакше `block` (вміння сіре).
- КОЛИ `custom: «атака по цілі»` → ЯКЩО `prob(accuracy - dodge)` → ТО `damage(target, roll)`; інакше `custom: «промах»`.
- КОЛИ `custom: «влучання вміння з ефектом-статусом»` → ЯКЩО `prob(chance - resist)` → ТО `set_state(target, stun | bleed | blight | marked)`.
- КОЛИ `turn_start(unit)` → ЯКЩО `state(unit, stunned)` → ТО `skip_turn(unit)`, `clear_state(unit, stunned)`.
- КОЛИ `turn_start(unit)` → ЯКЩО `state(unit, bleed)` or `state(unit, blight)` → ТО `damage(unit, dot)`.
- КОЛИ `custom: «влучання з knockback k»` → ЯКЩО `prob(chance - move_resist)` → ТО `push(target)` на k рангів назад, `swap(target, behind)` k разів.
- КОЛИ `custom: «влучання з pull k»` → ТО `pull(target)` на k рангів уперед.
- КОЛИ `input(skill, self_move)` → ТО `move(hero, forward | back)`, `swap(hero, neighbour)` на кожен крок.
- КОЛИ `custom: «Flashbang влучив»` → ТО `custom: «ціль на випадкову позицію»`, `stun(target, 1)`.
- КОЛИ `custom: «ворог атакує героя під Guard»` → ТО `custom: «удар отримує охоронець»`.
- КОЛИ `custom: «героя з Riposte атаковано»` → ТО `custom: «контратака по нападнику»`.
- КОЛИ `custom: «вміння бʼє позначеного»` → ЯКЩО `state(target, marked)` → ТО `custom: «бонусна шкода»`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `not state(hero, deaths_door)` → ТО `set_state(hero, deaths_door)`, `counter(stress, +big)`.
- КОЛИ `custom: «шкода по герою на Death's Door»` → ЯКЩО `prob(1 - deathblow_resist)` → ТО `disappear(hero)` (назавжди); інакше `custom: «шкоду поглинуто»`.
- КОЛИ `custom: «героя вилікувано»` → ЯКЩО `state(hero, deaths_door)` → ТО `clear_state(hero, deaths_door)`, `set_state(hero, recovering)`.
- КОЛИ `died(enemy)` → ЯКЩО `mode(corpses)` → ТО `transform(enemy, corpse)`; інакше `shift(rank, forward)` (?).
- КОЛИ `died(hero)` → ТО `counter(stress, +n)` для решти загону.
- КОЛИ `custom: «стрес-атака ворога»` → ТО `counter(stress, +n)` (ціль — здебільшого найбільш напружений герой).
- КОЛИ `counter(stress, >=, 100)` → ТО `custom: «афлікція або чеснота (virtue)»`; афлікція — `custom: «герой інколи діє сам, відмовляється від наказів»`.
- КОЛИ `counter(stress, >=, 200)` → ЯКЩО `state(hero, deaths_door)` → ТО `custom: «серцевий напад»`, `disappear(hero)`; інакше `set_state(hero, deaths_door)`.
- КОЛИ `custom: «бій починається»` → ЯКЩО `counter(light, >=, 75)` → ТО `custom: «менше стресу, вищий шанс заскочити ворогів»`; при низькому світлі — `custom: «вищий крит і лут»`.
- КОЛИ `input(item, torch | curative)` → ТО `custom: «вжито без втрати ходу (?)»`.
- КОЛИ `all_gone(enemy)` → ТО `win`.
- КОЛИ `all_gone(hero)` → ТО `lose`.
- КОЛИ `input(retreat)` → ТО `custom: «спроба втекти з бою (?)»`.
- Перемога: знищено всіх ворогів · Поразка: загинув увесь загін (смерть кожного героя остаточна) · Рахунок: —.

## Керування і ввід
- Миша/геймпад: клік по вмінню на панелі героя, що ходить → підсвічуються досяжні цілі → клік по цілі (ворогу, союзнику чи собі).
- Альтернативні дії ходу: пас, переміщення на сусідню позицію (?), використання предмета з інвентаря, відступ.
- Наведення на ворога показує модифіковані точність і шкоду, а також панель резистів і його вмінь.

## Вікна, меню, HUD
- `game-screen` бою (вид збоку): дві шеренги, над героями `hp-bar` і `+ui:stress-bar`, `turn-indicator` (хто ходить), `+ui:torch-meter` угорі.
- Панель героя: стати, спорядження, `skill-bar` з 4 вміннями і `+ui:rank-dots` (з яких рангів можна ходити й по яких бити — підсвічені кружки), кнопки пасу/руху.
- `tooltip` наведення: точність і шкода проти цілі; панель ворога (резисти, атаки, ефекти).
- `inventory-window` у бою — смолоскипи й ліки.
- `popup-text` шкоди/промаху/«Deathblow»/«Resist»; репліки героїв (bark) про стрес.
- Поза боєм (коротко): карта підземелля, табір, місто — не описуються.

## Фічі поза полем
- `permadeath` героїв; прогресія класів і вмінь у місті; вибір 4 з 7 вмінь — підготовка до позицій.
- Налаштування складності: корпуси і серцеві напади стали опційними (`custom-rules`).
- Режим арени гравець-проти-гравця в DLC The Butcher's Circus (`mode-versus`).

## Варіації й родичі
- Darkest Dungeon II (2023) — та сама позиційна основа, «покращена» бойова система, стосунки між героями, що дають перки або блокують вміння.
- Родичі: [legend-of-keepers](legend-of-keepers.md) (підземелля проти героїв, розстановка по кімнатах), [super-auto-pets](super-auto-pets.md) (бій черг, зсув після смерті), [../roguelike/shogun-showdown](../roguelike/shogun-showdown.md) (одна лінія, позиція й поворот), [mega-man-battle-network](mega-man-battle-network.md) (смуги 3×3 на бік).
- **Осі варіацій** позиційного 1D-бою: хто обмежений рангом — лише атака / і запуск, і ціль (DD) · чим ламають стрій — knockback / pull / shuffle / трупи-заглушки · що відбувається після смерті — зсув уперед / труп тримає місце.

## Цікавинки для курсу
- Вміння як дві маски рангів «звідки × куди» + підсвітка досяжних цілей — 📎.
- Шеренга як список: рух, knockback і pull як серії сусідніх обмінів; труп як «заглушка» в списку — 🥉.
- Death's Door: другий шар життя з імовірністю смерті й обмеженим опором — 🌱.
- Стрес як другий ресурс з порогами 100/200 і ефектами на поведінку героя (непокора) — 🥉.
- Ініціатива Speed + кидок щораунду — 🌱.
- Guard/Riposte/Mark як перехоплення атаки — подієва система «до/після удару» — 🥈.

## Мапа на каталог
- Є: `hp-damage` · `status-effects` ↔ stun/bleed/blight/mark · `melee-vs-ranged` ↔ передні проти задніх рангів · `permadeath` · `character-select` ↔ склад загону · `inventory-items` ↔ смолоскипи й ліки в бою.
- **Нема** → пропозиції карток:
  - `+rank-restricted-skills` «Вміння з масками рангів запуску й цілі» · entities/legality · 📎 · слоти {launch, target}.
  - `+death-door` «Стан на 0 HP з шансом смерті від кожного удару» · entities/state · 🌱.
  - `+stress-meter` «Другий ресурс героя з порогами зриву» · entities/state · 🥉.
  - `+corpse-blocker` «Труп займає позицію вбитого» · entities/death · 📎.
  - `+multi-target-ranks` «Удар по групі рангів» · entities/combat · 🌱.

## Пропозиції до словників
- `+cond:position` / `+cond:rank_in` — ранг сутності входить у маску (запуску чи цілі).
- `+effect:knockback` — відкинути назад на k позицій; `+effect:shuffle` — поставити на випадкову позицію.
- `+trigger:hit` — по сутності влучили (для Riposte, Guard, deathblow).
- `+ui:rank-dots` — кружки рангів запуску/цілі на іконці вміння; `+ui:turn-order-bar`; `+ui:stress-bar`; `+ui:torch-meter`.
- `+card:rank-restricted-skills`, `+card:death-door`; `+role:unit`.

## Джерела
- ⭐ [Wikipedia: Darkest Dungeon](https://en.wikipedia.org/wiki/Darkest_Dungeon) — 4 героїв, ранги (спереду ближній бій і більше шкоди, ззаду — слабкі дальні атаки), вороги в рангах, вибивання з позиції, стрес і афлікції/чесноти, серцевий напад, permadeath, трупи як опція, реліз 19.01.2016, платформи.
- [LP Archive: Your Heroes](https://lparchive.org/Darkest-Dungeon/Update%2001/) — вміння по рангах для кожного класу: Mace Bash 1–2, Lunge 3–4 → +2, Iron Swan 1→4, Come Hither, Uppercut, Purge 3, Flashbang, Disorienting Blast, Guard/Mark/Riposte.
- [LP Archive: The Tides of Battle](https://lparchive.org/Darkest-Dungeon/Update%2002/) — порядок ходів (кидок + Speed), 4 бойових вміння, Death's Door і deathblow 67–87 %, стрес 200, світло, резисти, предмети в бою.
- [LP Archive: Team Composition](https://lparchive.org/Darkest-Dungeon/Update%2004/) — ролі рангів 1–4, «по рангах 3/4 бʼють лише вороги з 3/4».
- [Early Guides: beginners](https://earlyguides.pages.dev/darkest-dungeon/beginners-guide) — Blinding Gas 3–4, YAWP 1–2, оглушення забирає хід, Death's Door ≈ 33 % смерті за удар.
- [Wikipedia: Darkest Dungeon II](https://en.wikipedia.org/wiki/Darkest_Dungeon_II) — позиційність у сиквелі, стосунки героїв.

## Непевне
- (?) Точна формула ініціативи (Speed + d8?) — LP-автор не певен.
- (?) Переміщення на сусідню позицію як окрема дія ходу і чи витрачає хід предмет — з памʼяті.
- (?) Великі вороги, що займають два ранги, — з памʼяті, не перевірено.
- (?) Що робить шеренга після смерті без трупів (зсув уперед) і як б'ють по трупах — не перевірено.
- (?) Застрахованість від deathblow: LP — 67 % база (стеля 87 %), гайд — «33 % смерті»; це те саме число з двох боків, але залежить від версії.
- (?) Засідка на загін (surprise) перемішує героїв — з памʼяті; підтверджено лише «світло підвищує шанс заскочити ворога».
- (?) Механіка відступу (шанс, штраф стресу) — не перевірено.
