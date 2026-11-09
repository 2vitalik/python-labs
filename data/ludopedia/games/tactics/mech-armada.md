---
title: Mech Armada
slug: mech-armada
aka: []
family: tactics
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2022
platforms: [PC, Switch, PS4, Xbox One]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1389360/Mech_Armada/", best: true, note: "офіційний опис: 80+ частин, покрокова сітка, процедурні рівні, смерть = кінець забігу, боси областей, Sandbox; Early Access 10.08.2021, реліз 16.06.2022"}
  - {kind: other, url: "https://gamechronicles.com/mech-armada-review-pc", note: "огляд: мех = шасі + корпус + зброя; Energy / Credits / Meta-Energy; місії Eliminate / Survive 5 раундів / Boss; шкода переходить між місіями"}
  - {kind: other, url: "https://www.pcgamer.com/mecha-armada-stomps-kaiju-all-the-way-out-of-early-access", note: "PC Gamer: вихід з раннього доступу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mech+Armada+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, ai-opponent, reachable-highlight, threat-range, impassable-cells, destroy-all-enemies, permadeath, shop-between-levels, round-currency, mode-select, +modular-unit-builder, +part-slots, +movement-pattern-by-part, +terrain-move-cost, +turn-limit-survive, +run-meta-carry, +hp-carryover, +scrap-refund, +rising-research-cost, +map-pickup-race, +procedural-levels]
proposes: ["+effect:assemble(mech, parts)", "+effect:scrap(mech)", "+role:chassis", "+role:body-part", "+window:mech-builder", "+window:research-window", "+feature:sandbox-parts", "+card:modular-unit-builder", "+card:map-pickup-race"]
author: opus
date: 2026-11-09
---

# Mech Armada — Into the Breach-подібна тактика, де мех збирається з трьох частин: шасі визначає рух, корпус — HP і слоти, зброя — атаку

## Суть
Роглайт-тактика проти чужинського Рою (the Swarm) на процедурних сітках. Ядро — **конструктор юніта**: кожен мех складається з **шасі** (ноги, павучі ноги, гусениці, реактивний ранець — скільки й куди ходить і яку місцевість долає), **корпусу** (HP, кількість слотів зброї, аури) і **зброї** у слотах (вогнемет, ракетні пускові, дрони, промені). Частини (80+) досліджують і покращують за дві валюти забігу; третя валюта лежить на мапі й переходить між забігами, якщо Рій не забере її першим. Черга, що в корпусі помилково звучала як «збирання на сітці», насправді — збирання зі слотів; сітка — поле бою.

## Поле і час
- Квадратна покрокова сітка з ізометричним рендером; місцевість впливає на прохідність залежно від шасі.
- Хід: гравець вводить рух і атаки всіх мехів, потім Рій робить свої (за оглядом — по черзі сторін).
- Рівні й оточення процедурні; кожна область закінчується босом.
- Типи місій: **Eliminate** (знищити всіх), **Survive** (протриматись 5 раундів), **Boss**.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мех | piece | HP (з корпусу), рух (з шасі), слоти зброї | рух за патерном шасі + атаки зброєю |
| Шасі: двоногі / павучі ноги / гусениці / реактивне | object | дальність, напрямки, місцевість | визначає, куди мех може піти |
| Корпус | object | HP, слоти, аура/ефект | несе зброю; дає особливий ефект |
| Зброя (вогнемет, ракети, дрони, промені…) | object | шкода, патерн | атака з власною формою зони |
| Рій (різні види) | enemy | рух, шкода, здібності | різний тип руху й атаки |
| Бос області | boss | — | фінальний бій області, може бути з супроводом |
| Meta-Energy на мапі | pickup | — | збирає мех; якщо першим дійде Рій — втрачено |
| Місцевість | terrain | прохідність | частина клітин доступна лише окремим шасі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, parts)` → ЯКЩО `has(player, energy)` → ТО `spawn(mech)` з `custom: «HP і слоти з корпусу, рух з шасі»`, `take(energy)`.
- КОЛИ `input(transform, mech, part)` → ТО `custom: «заміна частини існуючого меха»`, `take(energy)`.
- КОЛИ `input(scrap, mech)` → ТО `disappear_a`, `currency(+part_of_cost)`.
- КОЛИ `input(research, part)` → ЯКЩО `has(player, credits)` and `has(player, energy)` → ТО `unlock(part)`; `custom: «кожне наступне дослідження дорожче»`.
- КОЛИ `input(upgrade, part)` → ТО `take(credits)`, `custom: «покращені параметри частини»`.
- КОЛИ `input(move, mech, cell)` → ЯКЩО `custom: «клітина в патерні шасі і місцевість прохідна для шасі»` → ТО `move`; інакше `block`.
- КОЛИ `input(attack, mech, weapon, cell)` → ЯКЩО `custom: «клітина в патерні зброї»` → ТО `damage(area)`.
- КОЛИ `contact(mech, meta_energy)` → ТО `pickup`; КОЛИ `contact(swarm, meta_energy)` → ТО `disappear_b` (ресурс втрачено).
- КОЛИ `level_end` → ТО `custom: «шкода мехів зберігається на наступну місію»`.
- КОЛИ `hp_zero(mech)` → ТО `disappear_a`; КОЛИ `all_gone(mech)` → ТО `lose` — «disconnect», кінець забігу.
- КОЛИ `all_gone(swarm)` → ЯКЩО `mode(eliminate)` → ТО `win`; КОЛИ `counter(rounds, ==, 5)` → ЯКЩО `mode(survive)` → ТО `win`; КОЛИ `died(boss)` → ТО `win` (з умовою знищити супровід, коли він є).
- КОЛИ `game_over` → ТО `custom: «Meta-Energy → постійні бонуси: старт Credits/Energy, параметри частин, стартові предмети (знижують ціну в Credits, не в Energy)»`.

## Керування і ввід
- Миша: вибір меха → підсвітка досяжних клітин (форма залежить від шасі) → клік; вибір зброї → підсвітка зони атаки → ціль.
- Між місіями — конструктор: перетягування/вибір частин у слоти шасі/корпусу/зброї (?), дослідження нових частин.
- Sandbox: будь-які частини без ризику для тестування збірок.

## Вікна, меню, HUD
- `main-menu`: New Run, Continue, Sandbox, Options, Exit.
- `game-screen`: сітка, мехи й Рій, HP-смуги, `reachable-highlight`, зона атаки, `turn-counter` (для Survive), `objective-text`.
- `mech-builder` — збірка: три частини, характеристики, вартість у Energy.
- `research-window` — дерево/список частин з ціною в Credits.
- `map-window` / вибір наступної місії (?).
- `end-screen` — кінець забігу і нарахування Meta-Energy; `upgrade-window` — постійні апгрейди.

## Фічі поза полем
- Роглайт: смерть усіх мехів = новий забіг з новими мехами; `meta-progression` за Meta-Energy.
- `mode-sandbox` — тестовий режим із повним набором частин.
- Ранній доступ 2021, реліз 2022; демо на Steam.

## Варіації й родичі
- Родичі: [into-the-breach](into-the-breach.md) (рецензенти порівнюють прямо: мехи проти комах на сітці), [battletech](battletech.md) (мех із частин, але з бронею по зонах), [mewgenics](mewgenics.md) і [the-last-spell](the-last-spell.md) (роглайт-тактика), [mechabellum](../tower-lanes/mechabellum.md) (автобій: збирання армії, а не меха).
- **Осі варіацій «юніт із частин»:**
  - **гранулярність**: фіксований юніт / 3 слоти (шасі-корпус-зброя, Mech Armada) / броня і зброя по зонах тіла (Battletech) / сітка-рюкзак (Backpack Hero);
  - **що дає частина**: патерн руху / HP і слоти / атака;
  - **ціна**: одна валюта / дві (будівництво vs дослідження) / мета-валюта між забігами.

## Цікавинки для курсу
- Юніт = композиція трьох частин; параметри збираються з частин — 📎 (класична задача ООП: композиція замість спадкування).
- Патерн руху від шасі (ноги / павук / гусениці / реактивне) з прохідністю за типом місцевості — 🥉.
- Ресурс на мапі, який можна втратити, якщо ворог дійде першим — 🌱.
- Шкода, що переходить між місіями, і розбирання меха на частину вартості — 🌱.
- Ціна дослідження, що росте з кожним відкриттям — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `ai-opponent` · `reachable-highlight` / `threat-range` · `impassable-cells` ↔ місцевість · `destroy-all-enemies` ↔ Eliminate · `permadeath` ↔ кінець забігу · `shop-between-levels` ↔ дослідження · `round-currency` ↔ Energy/Credits · `mode-select` ↔ Run / Sandbox.
- **Нема** → пропозиції карток:
  - `+modular-unit-builder` «Юніт збирається з частин» · entities/state · 🥉 · слот {slots: [chassis, body, weapon]}.
  - `+part-slots` «Корпус задає кількість слотів зброї» · entities/state · 📎.
  - `+movement-pattern-by-part` «Патерн руху задає частина» · entities/legality · 📎.
  - `+terrain-move-cost` (вже в черзі) — тут прохідність за типом шасі.
  - `+turn-limit-survive` (з Into the Breach) — Survive 5 раундів.
  - `+run-meta-carry` (вже в черзі) — Meta-Energy між забігами.
  - `+hp-carryover` «HP зберігається між місіями» · entities/state · 🌱.
  - `+scrap-refund` «Розібрати юніт — частина вартості назад» · game-logic/economy · 🌱.
  - `+rising-research-cost` «Кожне дослідження дорожче» · game-logic/economy · 🌱.
  - `+map-pickup-race` «Ресурс на мапі, який може забрати ворог» · entities/interact · 🌱.
  - `+procedural-levels` «Процедурна тактична мапа» · levels/generation · 🥇.

## Пропозиції до словників
- `+effect:assemble(mech, parts)` — створити сутність із частин (поряд із ✅ `spawn`).
- `+effect:scrap(mech)` — розібрати з поверненням ресурсу.
- `+role:chassis` / `+role:body-part` — частина юніта, що не існує на полі окремо.
- `+window:mech-builder` — конструктор юніта; `+window:research-window` (вже в черзі) — дослідження частин.
- `+feature:sandbox-parts` — режим з усіма частинами (окремий випадок `mode-sandbox` ⏳).
- `+card:modular-unit-builder`, `+card:map-pickup-race` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Mech Armada](https://store.steampowered.com/app/1389360/Mech_Armada/) — 80+ частин (вогнемети, ракети, дрони, промені), покрокова сітка, процедурні рівні, the Swarm, боси областей, смерть = кінець забігу, Sandbox, дати раннього доступу й релізу.
- [Game Chronicles: Mech Armada Review (PC)](https://gamechronicles.com/mech-armada-review-pc) — шасі/корпус/зброя, 4 типи шасі, три валюти, місії Eliminate/Survive/Boss, шкода між місіями, Meta-Energy, яку може забрати Рій.
- [PC Gamer: вихід з раннього доступу](https://www.pcgamer.com/mecha-armada-stomps-kaiju-all-the-way-out-of-early-access) — бачено в пошуку, не відкривав.
- YouTube: пошук «Mech Armada gameplay».

## Непевне
- (?) Чи видно наміри Рою наперед (як в Into the Breach) — тоді `info: partial`; не перевірено.
- (?) Порядок ходів (по черзі сторін чи по юнітах) і чи є AP у меха.
- (?) Розмір поля, кількість областей і структура вибору місій між боями.
- (?) Тег Steam «Deckbuilding» — що саме в грі «колодне» (можливо, вибір частин).
- (?) Платформи окрім PC (Switch/PS/Xbox — за сторінками магазинів у пошуку, не відкривав).
