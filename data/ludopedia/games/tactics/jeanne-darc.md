---
title: "Jeanne d'Arc"
slug: jeanne-darc
aka: ["JEANNE D'ARC", ジャンヌ・ダルク]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2006
platforms: [PSP, PS4, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Jeanne_d%27Arc_(video_game)", best: true, note: "Burning Aura за ціллю, Unified Guard, перевтілення, skill gems, Sol/Luna/Stella, умови перемоги/поразки"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/JEANNE_D%27ARC", note: "JA: аура посилюється при повторі, Connection Guard у 8 клітинах, 5/3 слоти браслета, SP, 4 кольори каменів, слоти 3→6"}
  - {kind: other, url: "https://www.rpgfan.com/review/jeanne-darc/", note: "фронт/фланг/спина, контратака завжди, ландшафт, Godspeed, злиття каменів"}
  - {kind: other, url: "https://www.pocketgamer.com/jeanne-darc/review/", note: "перевтілення на 2 ходи, 4 категорії слотів, ~150 навичок, вибір мап на мапі світу"}
  - {kind: other, url: "https://www.game-over.com/reviews/psp/Jeanne_d`Arc.html", note: "бонус захисту сусідам, ліміт ходів, ескорт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Jeanne+d%27Arc+PSP+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, ai-opponent, floor-types, unit-xp-skills, inventory-items, shop-between-levels, shop-window, world-map, map-window, temporary-modes, sequential-levels, save-game, game-screen, +burning-aura, +facing-hit-bonus, +retaliation, +adjacency-buff, +transformation-orbs, +extra-turn-on-kill, +skill-stone-slots, +skill-fusion, +element-triangle, +turn-limit-objectives, +escort-objective]
proposes: ["+cond:from_behind", "+effect:counterattack", "+effect:buff", "+cond:element", "+ui:aura-marker", "+ui:sp-gauge", "+window:skill-stones"]
author: opus
date: 2026-11-09
---

# Jeanne d'Arc — удар лишає «палаючу ауру» на клітині за ціллю, і наступний, хто ступить туди, бʼє сильніше

## Суть
Покрокова тактика Level-5 на PSP: фаза гравця (кожен юніт ходить і діє), потім фаза ворога. Головна знахідка — **Burning Aura**: удар ближнього бою створює кільце на клітині **за ціллю** (протилежно атакувальнику); союзник, що стане в нього й атакує, отримує бонус, а удар з аури лишає ще сильнішу — так будується «естафета» навколо однієї цілі. Поруч — напрям удару (спина > фланг > фронт), гарантована контратака, бонус захисту за звʼязаний строй і перевтілення героїв браслетом із сферами.

## Поле і час
- Квадратна сітка поверх 3D-локацій; ландшафт впливає на шкоду й влучність.
- Хід = фаза гравця (будь-який порядок юнітів: рух + дія) → фаза ворога. У кожної мапи — ліміт ходів.
- Позиція має значення тричі: аура за ціллю, напрям удару відносно фасингу цілі, сусіди для захисту.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жанна | piece | HP, MP/SP, браслет із 5 слотами сфер | героїня; падіння → поразка |
| Носії браслетів | piece | браслет із 3 слотами | можуть перевтілюватись |
| Інші юніти | piece | рівень, слоти каменів 3→6, зброя, броня, елемент | рух + атака / магія / предмет |
| Перевтілена форма | piece | 1–3 ходи, +стати, своя навичка | вбивство → ще одна дія (Godspeed) |
| Ворог | enemy | ті ж + елемент | ШІ; теж контратакує й захищається строєм (?) |
| NPC під охороною | ally | — | ціль ескорту на деяких мапах |
| Burning Aura | zone | рівень посилення, 1 хід | зʼявляється за ціллю удару ближнього бою; бонус атаки тому, хто в ній |
| Сфера (orb) | pickup | ціна SP, бонус, навичка | вставляється в браслет; раз за бій |
| Камінь навички | pickup | колір, вимога рівня | червоний — ультимативний прийом зброї, фіолетовий — пасив зброї, зелений — магія, блакитний — стати |
| Камінь духа «…+n» | pickup | Сонце / Місяць / Зірка, n | один на юніта; задає елемент |
| Ландшафт | terrain | тип | змінює шкоду й влучність |
| Клітина-ціль | zone | — | «довести загін до клітин» — умова перемоги |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `counter(sp, +n)` (SP накопичується з ходами).
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «клітина досяжна за рух юніта»` → ТО `move(unit, cell)`.
- КОЛИ `input(attack_melee, target)` → ТО `damage(target, n)`, `spawn_at(burning_aura, cell_behind_target)`.
- КОЛИ `spawned(burning_aura)` → ЯКЩО `occupied(cell_behind_target, ally)` → ТО `carry(ally, burning_aura)` — союзник носить ауру з собою цей хід.
- КОЛИ `input(attack, target)` → ЯКЩО `occupied(attacker_cell, burning_aura)` → ТО `custom: «шкода ↑»`, нова аура `set_value(aura_level, +1)` — повтор посилює.
- КОЛИ `turn_end(player)` → ТО `disappear(burning_aura)`.
- КОЛИ `input(attack, target)` → ЯКЩО `custom: «атака в спину цілі»` → ТО `custom: «максимум шкоди й влучності»`; фланг — невеликий бонус; фронт — штраф.
- КОЛИ `after(attack)` → ЯКЩО `custom: «ціль вижила й дістає атакувальника»` → ТО `custom: «контратака — завжди»`.
- КОЛИ `custom: «юніта атаковано»` → ЯКЩО `adjacent_count(unit, ally, ≥, 1)` (8 сусідів) → ТО `custom: «захист ↑»`; ЯКЩО `connected(allies)` далі ланцюгом → ТО бонус росте з кількістю.
- КОЛИ `input(transform, orb)` → ЯКЩО `counter(sp, ≥, orb_cost)` і `not state(orb, used)` → ТО `transform(unit, armored_form)`, `set_state(unit, transformed, 1–3)`, `set_state(orb, used)`.
- КОЛИ `died(enemy)` → ЯКЩО `state(attacker, transformed)` → ТО `extra_move`.
- КОЛИ `state_off(unit, transformed)` → ТО `transform(unit, normal_form)`.
- Елементи: ЯКЩО `custom: «Сонце vs Зірка / Місяць vs Сонце / Зірка vs Місяць»` → ТО `custom: «перевага; сила росте з n каменя духа»`.
- КОЛИ `input(skill, target)` → ЯКЩО `counter(mp, ≥, cost)` → ТО `custom: «прийом / магія каменя»`.
- КОЛИ `input(item)` → ТО `custom: «предмет як дія ходу»`.
- КОЛИ `custom: «будь-яка дія юніта»` → ТО `counter(xp, +n)`.
- КОЛИ `all_gone(enemy)` або `all_on(party, target_cells)` (за мапою) → ТО `win`; усім — XP і можливі трофеї.
- КОЛИ `hp_zero(jeanne)` → ТО `lose`; КОЛИ `counter(turn, >, limit)` → ЯКЩО `not custom: «ціль виконано»` → ТО `lose`; ескорт: `hp_zero(npc)` → `lose`.
- Поза боєм: КОЛИ `input(fuse, stone_a + stone_b)` → ТО `merge(stone_a, stone_b → stone_c)`; рецепт записується.
- Перемога: знищити всіх / дійти до клітин · Поразка: Жанна впала, ліміт ходів, ескорт загинув · Рахунок: XP і трофеї.

## Керування і ввід
- Курсор по сітці: юніт → клітина руху → меню Attack · Skill · Item · Transform · Wait (?) з вибором напрямку.
- Кожну мапу гра пояснює новим правилом на старті (вбудовані підказки).
- PSP: хрестовина/стік і кнопки; затримки на чорних екранах завантаження меню.

## Вікна, меню, HUD
- `map-window` — мапа світу: вибір наступної битви, міста.
- `shop-window` у містах: зброя, броня, камені.
- `+window:skill-stones` — слоти каменів юніта (4 категорії), злиття, журнал рецептів.
- `custom-window` браслета: сфери в слотах (5 у Жанни, 3 в інших).
- `game-screen`: сітка, кільця аури (`+ui:aura-marker`), HP/MP, `+ui:sp-gauge`, `turn-counter` з лімітом, ціль мапи (`objective-text`).
- `dialogue-window` — сюжетні сцени; `save-slots` — збереження з меню; `end-screen` — поразка.

## Фічі поза полем
- `levels-sequential` + `world-map`; додаткові бої для прокачки (?).
- `xp-level` за кожну дію; слоти каменів ростуть із рівнем (3 → 6); злиття каменів із рецептами після третини гри.
- Перевидання PS4/PS5 (2024).

## Варіації й родичі
- Родичі в корпусі: [fire-emblem](fire-emblem.md) (контратака, мапа світу, сюжет з одного героя), [final-fantasy-tactics](final-fantasy-tactics.md) (напрям удару, сітка в 3D), [disgaea](disgaea.md) (бонус за сусідів), [hoshigami](hoshigami.md) (позиційні ланцюги).
- **Осі варіацій**: що лишає удар — нічого / ауру за ціллю / відкидання ([hoshigami](hoshigami.md)) · бонус від позиції — напрям удару / сусіди-захисники / аура на клітині · посилення героя — рівень / тимчасове перевтілення з ресурсом.

## Цікавинки для курсу
- Burning Aura: клітина за ціллю (протилежно атакувальнику), бонус тому, хто там, посилення при повторі, носіння разом із юнітом — 🥉.
- Напрям удару відносно фасингу цілі (спина / фланг / фронт) — 📎.
- Connection Guard: бонус захисту за звʼязний строй (BFS по 8 сусідах) — 🥉.
- Перевтілення за SP, раз на сферу за бій, додаткова дія за вбивство — 📎.
- Трикутник Сонце/Місяць/Зірка з силою від n каменя — 🌱.
- Камені в слотах + злиття з журналом рецептів — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (аура лише від ближнього бою) · `ai-opponent` · `floor-types` (ландшафт) · `unit-xp-skills` · `inventory-items` · `shop-between-levels` · `shop-window` · `world-map` · `map-window` · `temporary-modes` (перевтілення) · `sequential-levels` · `save-game` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+burning-aura` «Удар лишає бонус-клітину за ціллю» · entities/combat · 🥉 · слоти {stack, duration: 1}.
  - `+facing-hit-bonus` · `+retaliation` · `+adjacency-buff` · `+turn-limit-objectives` — уже в корпусі.
  - `+transformation-orbs` «Тимчасове перевтілення за ресурс» · entities/state · 📎.
  - `+extra-turn-on-kill` «Додаткова дія за вбивство» · game-logic/opponent · 🌱.
  - `+skill-stone-slots` «Камені навичок у слотах за рівнем» · entities/state · 📎.
  - `+skill-fusion` «Злиття двох навичок у третю» · game-logic/economy · 📎.
  - `+element-triangle` «Трикутник стихій» · entities/combat · 🌱.
  - `+escort-objective` «Довести/вберегти NPC» · game-logic/win · 📎.

## Пропозиції до словників
- `+cond:from_behind` — атака у спину відносно фасингу цілі (уже пропоновано; тут ще «з флангу»).
- `+effect:counterattack` — ціль відповідає ударом (уже пропоновано).
- `+effect:buff` — тимчасово підняти стат (захист від строю, атака з аури) (уже пропоновано).
- `+cond:element` — елемент атакувальника сильніший за елемент цілі (уже пропоновано).
- `+ui:aura-marker` — кільце-маркер на клітині з рівнем; `+ui:sp-gauge` — шкала ресурсу перевтілення.
- `+window:skill-stones` — слоти навичок із кольоровими категоріями й злиттям.

## Джерела
- ⭐ [Wikipedia: Jeanne d'Arc](https://en.wikipedia.org/wiki/Jeanne_d%27Arc_(video_game)) — Burning Aura, Unified Guard, перевтілення, skill gems, Sol/Luna/Stella, умови перемоги/поразки, ліміт ходів.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/JEANNE_D%27ARC) — посилення аури повтором, Connection Guard у 8 клітинах, слоти браслетів 5/3, SP і 1–3 ходи, 4 кольори каменів, трикутник духів.
- [RPGFan](https://www.rpgfan.com/review/jeanne-darc/) — напрям удару, гарантована контратака, ландшафт, Godspeed, злиття каменів.
- [Pocket Gamer](https://www.pocketgamer.com/jeanne-darc/review/) — перевтілення, 4 категорії слотів, ~150 навичок, мапа світу, 14 персонажів.
- [Game Over Online](https://www.game-over.com/reviews/psp/Jeanne_d`Arc.html) — бонус сусідам, ліміт ходів, ескорт.
- YouTube: пошук «Jeanne d'Arc PSP gameplay».

## Непевне
- (?) Тривалість перевтілення: JA — 1–3 ходи, Pocket Gamer — 2 ходи; RPGFan — доступне «після трьох ходів» (накопичення SP).
- (?) Чи гинуть юніти назавжди (крім Жанни) — джерела мовчать.
- (?) Чи посилює аура й магічні/дальні атаки — EN каже «a second character can move into it to strike», JA — аура лише від ближнього бою.
- (?) Чи користується ворог аурою й Connection Guard.
- (?) Команда Wait з вибором напрямку і вільні бої для прокачки — з оглядів побіжно.
