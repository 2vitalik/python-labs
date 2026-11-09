---
title: Cardinal Quest
slug: cardinal-quest
aka: [Cardinal Quest Classic, CQ, Cardinal Quest 2]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2011
platforms: [Windows, macOS, Linux, Flash (web), iOS]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/Cardinal_Quest", best: true, note: "RogueBasin: «coffeebreak roguelike», 3 класи, рух/атака 4 напрямки, одна клавіша — кілька дій, навички з підлоги з перезарядкою"}
  - {kind: other, url: "http://www.148apps.com/reviews/cardinal-quest-review/", note: "огляд iOS-версії: класи, Shadow Walk, 2 життя, гроші = лише рахунок, мінотавр Asterion"}
  - {kind: steam, url: "https://store.steampowered.com/app/378030/Cardinal_Quest_2/", note: "Cardinal Quest 2 (Randomnine, 2015): 7 героїв, 3 кампанії + нескінченна Tower"}
  - {kind: other, url: "https://www.gamingonlinux.com/2015/11/cardinal-quest-2-a-nofuss-roguelike-now-on-steamos-linux-some-thoughts", note: "CQ2: зони «вбий усіх — іди далі», заклинання з перезарядкою, вибір атрибута на рівні"}
  - {kind: other, url: "https://www.killscreen.com/cardinal-quest-2-simplifies-roguelike-too-much/", note: "CQ2: 5 витратних + 4 слоти спорядження, фіксований набір ворогів етапу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cardinal+Quest+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, hp-damage, item-pickup, inventory-items, inventory-limit, stairs-levels, sequential-levels, dungeon-generation, fog-of-war, character-select, player-death, permadeath, score-records, unit-xp-skills, +ability-pickup-cooldown, +multi-purpose-key, +speed-stat-cooldown]
proposes: ["+effect:recharge(a, skill)", "+cond:ready(skill)", "+feature:coffee-break-run", "+card:ability-pickup-cooldown", "+card:multi-purpose-key"]
author: opus
date: 2026-11-09
---

# Cardinal Quest — «кавова перерва»-роглайк: 3 класи, 4 напрямки, навички з підлоги на перезарядці

## Суть
Аркадна версія роглайку: обираєш одного з трьох героїв (воїн, маг, злодій) і спускаєшся випадковими поверхами до мінотавра Asterion. Усе стиснуто до кількох клавіш: рух і атака лише в 4 напрямки, клавіша очікування водночас спускає сходами, навички й предмети — на цифрах. Навички не вчаться, а **знаходяться на підлозі, як предмети**, і після використання перезаряджаються; швидкість героя прискорює перезарядку. Натхнення — red-box D&D, Gauntlet, [desktop-dungeons](desktop-dungeons.md), [angband](angband.md).

## Поле і час
- Квадратна тайлова сітка; поверхи генеруються випадково, предмети й навички — у випадковому порядку, але сила екіпірування й ворогів росте «за розкладом».
- Покроково; стат швидкості впливає на темп дій і перезарядку (?).
- Туман: видно околицю героя (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Fierce Fighter | player | health, attack, defense, speed | ближній бій; навичка-лють (frenzy / berserk) |
| Mystical Wizard | player | ті самі стати | б'є заклинаннями здалеку |
| Stealthy Thief | player | висока speed | Shadow Walk: невидимість, удар з невидимості — більше шкоди |
| Монстри | enemy | сильнішають з глибиною | атакують у ближньому бою (?) |
| Asterion (мінотавр) | boss | — | фінальний ворог |
| Навичка на підлозі | pickup | перезарядка | береться як предмет, займає цифрову клавішу |
| Спорядження | pickup | стати | покращує героя протягом забігу |
| Зілля / витратні | pickup | — | на цифрових клавішах |
| Золото | pickup | — | лише рахунок |
| Сходи | static | — | униз; спуск — клавішею очікування |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `damage(enemy, attack)`.
- КОЛИ `input(wait)` → ЯКЩО `cell(here, stairs)` → ТО `next_level`; інакше `end_turn`.
- КОЛИ `picked(hero, ability)` → ТО `give(hero, ability)` на вільну цифру.
- КОЛИ `input(ability n)` → ЯКЩО `custom: «навичка заряджена»` → ТО `custom: «ефект навички»`, `custom: «почати перезарядку»`.
- КОЛИ `tick` → ТО `custom: «перезарядка −1 (швидше з вищою speed)»`.
- КОЛИ `input(shadow_walk)` → ТО `set_state(thief, invisible)`; КОЛИ `contact(thief, enemy)` → ЯКЩО `state(thief, invisible)` → ТО `damage(enemy, ×bonus)`.
- КОЛИ `picked(hero, gold)` → ТО `score(value)`.
- КОЛИ `hp_zero(hero)` → ТО `lives(−1)`; ЯКЩО `custom: «життів 0»` → ТО `lose`.
- КОЛИ `died(asterion)` → ТО `win`.
- Перемога: убити мінотавра. Поразка: втрата обох життів. Рахунок: золото.

## Керування і ввід
- Стрілки — рух і атака (4 напрямки); одна клавіша «чекати» = спуск сходами; цифри — навички й предмети; мишка (PC).
- iOS: тап-керування (огляд: на телефоні добре, на планшеті неточно).

## Вікна, меню, HUD
- `game-screen`: тайли, `stat-panel` (health, attack, defense, speed), `skill-bar` з перезарядкою на цифрах, `message-log` (?).
- `character-select`: 3 класи.
- `inventory-window`: спорядження (огляд iOS скаржиться, що перегляд стату переставляє речі).
- `end-screen` з рахунком (золото), `main-menu`.

## Фічі поза полем
- Короткий забіг «на каву»; `permadeath` з 2 життями.
- Безкоштовна «Classic» на Kongregate (Flash) і платна Deluxe (за RogueBasin).

## Варіації й родичі
- **Cardinal Quest 2** (Randomnine, 2015): 7 героїв (Thief, Alchemist, Ranger з собакою, Wizard, Fighter, Paladin, Pugilist), 3 кампанії + нескінченний режим The Tower; зони «вбий усіх ворогів — гра скаже йти далі»; заклинання на перезарядці; на рівні — вибір атрибута / очко навички; інвентар 5 витратних + броня, штани, зброя, кільце; набір ворогів етапу фіксований (місто бандитів, ліс павуків), розкладка — випадкова; клавіша дії = перша літера слова (Trash — T, Equip — E).
- Родичі: [sproggiwood](sproggiwood.md) (аркадні короткі підземелля, класи), [pixel-dungeon](pixel-dungeon.md), [desktop-dungeons](desktop-dungeons.md).
- Осі варіацій: навички (з підлоги / дерево рівнів) · відновлення (перезарядка за часом / мана / заряди) · структура (поверхи / зони-арени з умовою «вбий усіх»).

## Цікавинки для курсу
- Навичка-предмет з перезарядкою, швидкість стату прискорює її — 🌱.
- Одна клавіша — кілька дій за контекстом (чекати / спуститись) — 🌱.
- Удар з невидимості з бонусом шкоди — 🌱.
- Зона «вбий усіх → далі» (CQ2) — 🌱 (`all_gone`).

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `hp-damage` · `item-pickup` · `inventory-items` · `inventory-limit` (CQ2) · `stairs-levels` · `sequential-levels` · `dungeon-generation` · `fog-of-war` · `character-select` · `player-death` (2 життя) · `permadeath` · `score-records` · `unit-xp-skills`.
- **Нема** → пропозиції карток:
  - `+ability-pickup-cooldown` «Навичка знаходиться як предмет і перезаряджається» · entities/combat · 🌱.
  - `+multi-purpose-key` «Одна клавіша — дія за контекстом клітини» · interface/input · 🌱.
  - `+speed-stat-cooldown` «Стат швидкості скорочує перезарядку» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:recharge(a, skill)` — запустити/скинути перезарядку (в коді є характеристика `cooldown`, ефекту нема).
- `+cond:ready(skill)` — навичка заряджена.
- `+feature:coffee-break-run` — забіг на 10–20 хв як заявлена мета дизайну.
- `+card:ability-pickup-cooldown` · `+card:multi-purpose-key`.

## Джерела
- ⭐ [RogueBasin: Cardinal Quest](https://www.roguebasin.com/index.php/Cardinal_Quest) — 2010 прототип, 1.2 (12.2011), класи, керування, спрощення, вплив.
- [148Apps: огляд](http://www.148apps.com/reviews/cardinal-quest-review/) — класи, Shadow Walk, 2 життя, золото = рахунок, Asterion.
- [Steam: Cardinal Quest 2](https://store.steampowered.com/app/378030/Cardinal_Quest_2/) · [GamingOnLinux про CQ2](https://www.gamingonlinux.com/2015/11/cardinal-quest-2-a-nofuss-roguelike-now-on-steamos-linux-some-thoughts) · [Kill Screen про CQ2](https://www.killscreen.com/cardinal-quest-2-simplifies-roguelike-too-much/).
- YouTube: [пошук](https://www.youtube.com/results?search_query=Cardinal+Quest+roguelike+gameplay).

## Непевне
- (?) Черга: «поверх = одна арена» — у джерелах для CQ1 не підтверджено; ближче до цього зони CQ2 («вбий усіх — іди далі»).
- (?) Кількість поверхів, розмір карти, видимість (туман).
- (?) Як саме speed впливає на порядок ходів (лише на перезарядку — підтверджено для Shadow Walk).
- (?) Автор — Ido Yehieli (RogueBasin пише лише «Ido»); видавець CQ2 — Randomnine.
- (?) Як працюють 2 життя (відродження на місці чи на початку поверху).
