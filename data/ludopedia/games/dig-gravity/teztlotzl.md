---
title: Teztlotzl
slug: teztlotzl
aka: []
family: dig-gravity
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2026
platforms: [web, PC (Windows), Android]
links:
  - {kind: itch, url: "https://petri-dish-games.itch.io/teztlotzl", best: true, note: "опис прототипу 0.3.14: 84 карти, 17 матеріалів, сезон-турніри, нейромережі-суперники, онлайн за кодом кімнати, повне керування; грати в браузері"}
  - {kind: other, url: "https://itch.io/post/17583876", note: "коментар гравця: арена горить, затоплюється, обвалюється"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Teztlotzl+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-by-input, gravity-fall, projectile-shot, destructible-blocks, cell-transform, interaction-table, environment-death, ai-opponent, online-multiplayer, shop-between-levels, in-game-editor, keyboard-controls, particles, +falling-sand-cell, +fire-spread, +phase-transition, +deck-builder, +deck-draw, +mana-pool-spells, +summon-creature, +card-rebake-modifier, +electrified-pool, +persistent-terrain-damage, +double-elimination-season, +neuroevolution-ai, +lockstep-netcode, +local-versus, +ragdoll-body, +double-jump]
proposes: ["+cond:mana", "+cond:conductive", "+effect:draw_card", "+effect:kick", "+effect:electrify", "+role:card", "+role:material", "+ui:mana-bar", "+ui:card-hand", "+window:deck-builder", "+window:pack-opening", "+window:tournament-bracket", "+feature:room-code", "+feature:ai-trainer", "+card:card-rebake-modifier", "+card:electrified-pool", "+card:persistent-terrain-damage", "+card:neuroevolution-ai"]
author: opus
date: 2026-11-09
---

# Teztlotzl — дуель двох магів картами-закляттями на арені falling sand, де кожне закляття ще й ламає рельєф

## Суть
Два маги, у кожного своя колода, бʼються на повністю симульованій falling-sand арені: витрачаєш ману, щоб спалити, втопити, розчленувати й засипати суперника. Ядро — **закляття = шкода рельєфу**: вогонь біжить по розлитій нафті, лава застигає новим укриттям, кислота підїдає опору під колоною, блискавка у воду бʼє струмом усю калюжу. Поверх — роглайт-сезон: турніри з подвійним вибуванням, бустери між раундами, а рельєф лишається пошкодженим на весь забіг.

## Поле і час
- Арена — піксельна сітка матеріалів (17 видів з «реальною хімією»), маги — регдол-тіла поверх сітки (як у [Noita](noita.md)); фізика — 5× гравітація, удари при приземленні.
- Real-time: біг, стрибки, каст у точку курсора; рука з 4 карт.
- Рельєф між матчами сезону не відновлюється.
- Онлайн — детермінований lockstep (обидва клієнти однієї версії); браузер — 60 fps з v0.2.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маг гравця | player | колода ≥ 15, рука 4, мана | біг, стрибок і подвійний стрибок, присід, прискорення, удар ногою; каст у курсор |
| Маг-суперник | enemy | нейромережа | той самий набір дій; мережа еволюціонує між матчами |
| Карта-атака | supply | вартість мани | породжує закляття (снаряд, стихію) |
| Модифікатор | supply | — | «перепікає» карту, якої торкнувся |
| Призов | supply | — | викликає істоту на арену (?) щодо поведінки |
| Спорядження · уміння | supply | — | архетипи карт (?) щодо дії |
| Пісок · камінь · скло · дерево | object | матеріал | порошок / тверді; руйнуються закляттями (?) щодо деталей |
| Вода | object | рідина | блискавка в неї → струм у всій калюжі; топить |
| Нафта | object | рідина | вогонь біжить по ній |
| Лава | object | рідина | застигає в нове укриття |
| Кислота | object | рідина | їсть підлогу й опори |
| Кров | object | рідина | з розчленування |
| Вогонь | hazard | — | поширюється по пальному; палить мага |
| Мана | resource | запас мага | витрачається на карти (?) щодо відновлення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(cast, slot)` → ЯКЩО `custom: «мани ≥ вартість карти»` → ТО `use(mage, card)`, `counter(mana, -cost)`, `custom: «закляття в точку курсора»`.
- КОЛИ `after(use)` → ТО `custom: «добрати карту в руку до 4»` (?) щодо моменту добору.
- КОЛИ `contact(modifier, card)` → ТО `transform(card, card_rebaked)`.
- КОЛИ `contact(spell, b)` → ТО `damage(b, n)` і `custom: «шкода рельєфу в точці влучання»`.
- КОЛИ `adjacent(fire, oil)` → ТО `transform(oil, fire)` — вогонь іде вздовж нафти.
- КОЛИ `custom: «лава охолола»` → ТО `transform(lava, solid)` — нове укриття.
- КОЛИ `contact(acid, solid)` → ТО `disappear(b)`; КОЛИ `custom: «опора зникла»` → ТО `fall(pillar)`.
- КОЛИ `contact(lightning, water)` → ТО `custom: «струм по всій звʼязній калюжі»`; ЯКЩО `occupied(pool, mage)` → ТО `damage(mage, n)`.
- КОЛИ `custom: «маг у вогні / під водою / засипаний»` → ТО `damage(mage, n)` — burn, drown, bury.
- КОЛИ `input(jump)` → ЯКЩО `custom: «у повітрі, подвійний не витрачено»` → ТО `custom: «другий стрибок»`.
- КОЛИ `input(kick)` → ТО `custom: «удар ногою»` (?) щодо ефекту.
- КОЛИ `custom: «приземлення з висоти»` → ТО `custom: «удар при приземленні»` (?) щодо шкоди.
- КОЛИ `died(mage_opponent)` → ТО `win`, `custom: «один із 4 стилів добивання»` (?) щодо умови перемоги.
- КОЛИ `level_end` → ТО `custom: «турнірна сітка з подвійним вибуванням: 8 → 16 → 32 бійці»`, `window(shop)`.
- КОЛИ `level_end` → ТО `custom: «пошкодження рельєфу зберігаються до кінця сезону»`.
- КОЛИ `level_end` → ТО `custom: «цикл навчання еволюціонує нейромережі суперників»`.
- Перемога: знищити мага навпроти; сезон — пройти сітку турнірів. Поразка: загинути (у сезоні — два програші через подвійне вибування (?)). Рахунку нема (?).

## Керування і ввід
- Клавіатура й миша: A/D — рух, W/Space — стрибок (ще раз у повітрі — подвійний), S — присід, Shift — біг, ЛКМ — каст у курсор, 1–4 — каст карти зі слота, F — удар ногою.
- Геймпад: лівий стік — рух (флік угору — стрибок), правий — приціл, LT/LB/RB/RT — слоти 1–4, A — стрибок, X — удар.
- Тач (Android): лівий стік — рух, тап по картах — у чергу, тап по світу — приціл і каст.
- Локальний мультиплеєр: другий геймпад + START на екрані колоди.

## Вікна, меню, HUD
- `game-screen`: арена; `card-hand` з 4 карт, `mana-bar` (?) щодо вигляду, HP магів (?).
- `deck-builder` — екран колоди (≥ 15 карт); тут же вхід другого гравця (START).
- `shop-window` / `pack-opening` — бустери між раундами сезону.
- `tournament-bracket` — сітка подвійного вибування (?) щодо окремого екрана.
- `lobby-window` — онлайн-дуель за анонімним кодом кімнати з 6 символів, без акаунтів.
- `editor-window` (мапи) і тренер AI — лише в десктоп-версії.

## Фічі поза полем
- Сезон-роглайт: `meta-progression` колоди (бустери, редагування) + незворотний рельєф.
- `online-multiplayer` (коди кімнат, lockstep) · `local-multiplayer` (2 геймпади) · `touch-controls` · `gamepad-support`.
- `level-editor` (мапи) + `+feature:ai-trainer` (тренер нейромереж) — десктоп за $5+; браузерна версія безкоштовна.
- Автор розкриває, що код писали AI-агенти (Claude Code та ін.), дизайн і маги — його.

## Варіації й родичі
- Арена-симуляція — як [Noita](noita.md) і [the-powder-toy](the-powder-toy.md); дуель на руйнованому рельєфі — [Liero](liero.md), [Scorched Earth](scorched-earth.md).
- Карткова сторона — deckbuilder-роглайти (`+deck-builder` у корпусі); сезон-сітка — як турніри файтингів.
- **Осі варіацій**: рельєф — «статичний / руйнується в матчі (Liero) / руйнування переходить у наступні матчі (Teztlotzl)»; зброя — «арсенал (Liero) / жезл-програма (Noita) / рука з колоди»; суперник — «скриптовий AI / нейромережа, що вчиться між матчами».

## Цікавинки для курсу
- Закляття як реакція матеріалів: вогонь по нафті, лава → укриття, кислота під опорою — 🥉 на готовому falling-sand.
- Блискавка у воду: flood-fill по звʼязній рідині й шкода всім у ній — 📎.
- Рука з 4 карт, колода, мана — 🥉.
- Модифікатор, що «перепікає» карту-ціль, — 📎.
- Рельєф, що зберігається між матчами сезону, — 🌱 (серіалізація поля).
- Нейроеволюція суперників між матчами — 👑.
- Детермінований lockstep для онлайн-дуелі — 🥇.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `projectile-shot` · `destructible-blocks` · `cell-transform` (лава → укриття, нафта → вогонь) · `interaction-table` · `environment-death` (втопити, спалити, засипати) · `ai-opponent` · `online-multiplayer` · `shop-between-levels` (бустери) · `in-game-editor` (мапи) · `keyboard-controls` · `particles`.
- **Нема** → пропозиції карток:
  - Повтори з корпусу: `+falling-sand-cell`, `+fire-spread`, `+phase-transition`, `+deck-builder`, `+deck-draw`, `+mana-pool-spells`, `+summon-creature`, `+local-versus`.
  - `+card-rebake-modifier` «Модифікатор змінює карту, якої торкнувся» · entities/state · 📎.
  - `+electrified-pool` «Струм по всій звʼязній рідині» · entities/interact · 📎.
  - `+persistent-terrain-damage` «Поле не відновлюється між матчами забігу» · game-logic/history · 🌱.
  - `+double-elimination-season` «Сезон із турнірних сіток подвійного вибування» · game-logic/goals · 📎.
  - `+neuroevolution-ai` «Суперники — нейромережі, що еволюціонують між матчами» · ai · 👑.
  - `+lockstep-netcode` «Детермінований lockstep онлайн» · network · 🥇.
  - `+ragdoll-body` «Тіло-регдол поверх клітинного світу» · entities/move · 🥈 · `+double-jump` «Подвійний стрибок» · entities/move · 🌱.

## Пропозиції до словників
- `+cond:mana(a, op, n)` — вистачає мани (повтор корпусу).
- `+cond:conductive(cell)` — клітина проводить струм (повтор).
- `+effect:draw_card(n)` — добрати карту (повтор).
- `+effect:kick(a, dir)` — удар ногою (повтор з Noita).
- `+effect:electrify(region)` — струм по звʼязній рідині.
- `+role:card` · `+role:material` — карта в руці; матеріал арени (повтори; у таблиці поки `supply` і `object`).
- `+ui:mana-bar` · `+ui:card-hand` (повтори).
- `+window:deck-builder` · `+window:pack-opening` · `+window:tournament-bracket` (повтори).
- `+feature:room-code` (повтор) · `+feature:ai-trainer` — тренер AI як інструмент гравця.
- `+card:…` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Teztlotzl](https://petri-dish-games.itch.io/teztlotzl) — прототип 0.3.14 від Petri Dish Games: 84 карти у 8 архетипах, колода ≥ 15, рука 4; 17 матеріалів (названо 9); приклади реакцій; сезон 8 → 16 → 32; нейромережі; lockstep і коди кімнат; керування для клавіатури, геймпада й тачу.
- [Коментар на itch](https://itch.io/post/17583876) — арена «горить, затоплюється, обвалюється».

## Непевне
- (?) Рік: на сторінці дати релізу нема; коментар — «27 днів тому», оновлення — «5 днів тому»; ставлю 2026.
- (?) Ще 8 матеріалів і 3 архетипи карт не названі; поведінка призовів, спорядження й умінь — невідома.
- (?) Як відновлюється мана, чи є в магів HP і що саме вирішує дуель (смерть? раунди?).
- (?) У що застигає лава («нове укриття» — камінь чи скло).
- (?) Чи завдає шкоди удар при приземленні і що робить удар ногою (відштовхує мага? матеріал?).
- (?) Правила добору карт у руку.
