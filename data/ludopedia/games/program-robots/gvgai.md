---
title: GVGAI (General Video Game AI)
slug: gvgai
aka: [General Video Game AI, GVG-AI, VGDL, Video Game Description Language, java-vgdl]
family: program-robots
also: [maze-arcade, push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: both
  goal: score
year: 2014
platforms: [Java, PC]
links:
  - {kind: official, url: "https://github.com/GAIGResearch/GVGAI", best: true, note: "фреймворк змагання: треки Planning / 2-Player / Level Generation / Rule Generation, приклади ігор VGDL, структура пакета агента"}
  - {kind: wiki, url: "https://github.com/GAIGResearch/GVGAI/wiki", note: "вікі: VGDL, спрайти, взаємодії, термінації, forward model, специфікації треків"}
  - {kind: other, url: "https://github.com/GAIGResearch/GVGAI/wiki/VGDL-Language", note: "структура опису гри: BasicGame, SpriteSet, LevelMapping, InteractionSet, TerminationSet; рівень — матриця символів"}
  - {kind: other, url: "https://github.com/GAIGResearch/GVGAI/wiki/Interactions", note: "повний список ефектів взаємодій (killSprite, stepBack, bounceForward, transformTo, undoAll…)"}
  - {kind: other, url: "https://github.com/GAIGResearch/GVGAI/wiki/Planning-Track-Specifications", note: "40 мс на act(), 1 с на конструктор, штрафи за перевищення"}
  - {kind: other, url: "https://arxiv.org/abs/1802.10363", note: "огляд фреймворку (Perez-Liebana, Liu, Khalifa, Gaina, Togelius, Lucas)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=GVGAI+general+video+game+ai+competition", note: "пошук; агенти грають у VGDL-ігри"}
stage: v1
coverage: 65
mechanics: [move-4dir, move-auto, push-object, impassable-cells, projectile-shot, item-pickup, teleport, chase-player, random-walk, spawner-entity, spawn-schedule, timed-despawn, wrap-edges, hp-damage, touch-death, destroy-all-enemies, collect-all, time-out, event-points, interaction-table, level-from-txt, ai-opponent, ai-random, ai-greedy, state-as-data, game-loop, logic-render-split, gui-render, +agent-program-interface, +turn-time-limit, +forward-model, +game-description-language, +general-game-playing, +level-generator-agent, +rule-generator-agent, +playability-constraints, +undo-whole-tick, +ai-mcts]
proposes: ["+trigger:timeout(bot)", "+effect:undo_tick", "+effect:flee", "+effect:chase(a, b)", "+cond:resource(a, name, op, n)", "+feature:agent-api", "+feature:forward-model", "+axis:observation", "+card:forward-model", "+card:game-description-language", "+card:level-generator-agent", "+card:rule-generator-agent", "+card:playability-constraints", "+card:undo-whole-tick"]
author: opus
date: 2026-11-09
---

# GVGAI — бот-програма грає в аркаду, правил якої не знає: ігри описано мовою VGDL, а агент має 40 мс на хід і симулятор майбутнього

## Суть
Дослідницький фреймворк і змагання (з 2014) для «загальної гри»: учасник пише агента на Java, який має грати в багато **невідомих наперед** аркад — Sokoban-подібні, Space Invaders-подібні, Zelda-подібні. Кожна гра — текстовий опис мовою **VGDL**: спрайти, відповідність символів рівня, таблиця взаємодій «A × B → ефект» і умови кінця. Агент правил не бачить, зате отримує **forward model** — може скопіювати стан і «прокрутити» дію наперед. Окремі треки: два гравці, навчання, **генерація рівнів** (дано гру — створи рівні) і **генерація правил** (дано спрайти й рівень — створи гру).

## Поле і час
- Поле — сітка клітин (`square_size` у пікселях, напр. 32 або 50); рівень — 2D-матриця символів, кожен символ мапиться на один або кілька спрайтів (ящик поверх землі).
- Java-рушій підтримує лише **GridPhysics** (клітинний рух); у репозиторії є й тека `contphysics` — ігри з неперервною фізикою (?).
- Тік: рушій щотіку викликає `act()` агента, застосовує дію, рухає всі спрайти й **один раз за тік** обробляє взаємодії.
- Агент бачить стан через `StateObservation` (рахунок, тік, переможець, розміри світу, позиції спрайтів, історію подій), але не текст правил — `info: partial`.
- Випадковість: NPC (RandomNPC, Bomber з `prob`) і спавн; у симуляції forward model випадкові події не обовʼязково збігаються з реальною грою.

## Сутності
Класи спрайтів VGDL — «словник» рушія; конкретна гра будує з них свої сутності.

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| MovingAvatar | player | — | рух у 4 напрямки без зміни орієнтації |
| Horizontal/VerticalAvatar | player | вісь | рух лише по горизонталі / вертикалі |
| OrientedAvatar | player | орієнтація | напрям, куди не дивиться, — спершу поворот без руху |
| ShootAvatar | player | `stype`, `ammo` | OrientedAvatar + USE породжує спрайт (постріл, меч); може витрачати ресурс |
| FlakAvatar | player | `minAmmo`, `ammoCost` | лише ліво-право + стрільба (Space Invaders) |
| OngoingAvatar / OngoingTurningAvatar / OngoingShootAvatar | player | — | рухається сам у поточному напрямку, ввід міняє напрям (Pac-Man) / лише перпендикулярно (Tron) |
| MissileAvatar | player | — | ігнорує ввід, летить у фіксованому напрямку |
| Immovable | static | — | нерухомий (стіни, підлога) |
| Passive | object | — | рухається лише від взаємодій (ящик) |
| Flicker / OrientedFlicker | projectile | `limit` | зникає сам через `limit` оновлень (удар мечем) |
| Missile / RandomMissile | projectile | напрям | летить прямо; напрям фіксований / випадковий |
| RandomNPC | neutral | — | щотіку випадковий напрям |
| Chaser / Fleeing | enemy | `stype` | крок до / від найближчого спрайта виду |
| AlternateChaser / RandomAltChaser | enemy | `stype1`, `stype2`, `prob` | женеться за одним, тікає від іншого; інколи випадково |
| SpawnPoint | spawner | `stype`, `total`, `prob`, `cooldown` | породжує спрайти; після `total` зникає (0 — безкінечно) |
| Bomber / RandomBomber / BomberRandomMissile | spawner | як SpawnPoint | рухомий спавнер: праворуч / випадково; останній кидає випадковий тип |
| Spreader | spawner | `spreadprob` | з імовірністю копіює себе в 4 сусідні клітини (вогонь, плями) |
| Door / Portal | gate | `stype` (вихід) | портал: `teleportToExit` переносить на вихід |
| Resource | pickup | `resource`, `value`, `limit` | при зборі змінює іменований ресурс аватара (ключі, патрони, діаманти) |
| Агент (Agent.java) | player | 1 с на конструктор, 40 мс на `act()` | обирає одну дію з `getAvailableActions()` на тік |

Приклад `aliens`: FlakAvatar стріляє «sam», Bomber-прибульці кидають бомби (`prob=0.01`, `cooldown=3`), два портали випускають по 20 прибульців (кожні 16 і 12 кроків), база руйнується від бомб.

## Правила (КОЛИ → ЯКЩО → ТО)
Агент і середовище:
- КОЛИ `tick` → ТО `custom: «рушій викликає act(stateObs, timer); агент повертає дію з getAvailableActions()»`.
- КОЛИ `custom: «act() повернув за 40–50 мс»` → ТО `custom: «застосовано ACTION_NIL»`.
- КОЛИ `custom: «act() довше 50 мс»` → ТО `lose`, `score(-1000)` — дискваліфікація в цій грі.
- КОЛИ `custom: «конструктор агента довше 1 с»` → ТО `lose` (дискваліфікація на рівні).
- КОЛИ `custom: «агент викликав copy() / advance(action)»` → ТО `custom: «копія стану просувається на тік із дією; реальна гра не змінюється»`.

Аватар:
- КОЛИ `input(ACTION_UP|DOWN|LEFT|RIGHT)` → ЯКЩО `facing(avatar, dir)` → ТО `move(avatar, dir)`; для OrientedAvatar інакше `face(avatar, dir)`.
- КОЛИ `input(ACTION_USE)` → ЯКЩО `has(avatar, ammo)` → ТО `spawn_at(stype, front)`, `custom: «ресурс ammo −ammoCost»`.

NPC і спавн:
- КОЛИ `tick` → ТО `move(missile, dir)`; `custom: «Chaser — крок до найближчого stype; Fleeing — крок від нього»`.
- КОЛИ `timer(cooldown)` → ЯКЩО `prob(p)` → ТО `spawn(stype)`; ЯКЩО `counter(spawned, >=, total)` → ТО `disappear(spawnpoint)`.
- КОЛИ `timer(limit)` → ТО `disappear(flicker)`.
- КОЛИ `rng(spreadprob)` → ТО `spawn_at(spreader, adjacent4)`.

InteractionSet (рядок `A B > ефект`, діє на A; `scoreChange=N` додає очки):
- КОЛИ `contact(a, b)` з `killSprite` → ТО `disappear(a)`; `killAll` → `custom: «зникають усі stype»`.
- КОЛИ `contact(avatar, wall)` з `stepBack` → ТО `block` — відкат останнього кроку A.
- КОЛИ `contact(box, avatar)` з `bounceForward` → ТО `push(box)` — ящик іде на 1 у напрямку B.
- КОЛИ `contact(box, wall)` з `undoAll` → ТО `custom: «відкотити весь тік для всіх спрайтів»` — так Sokoban забороняє заштовхнути ящик у стіну.
- КОЛИ `contact(a, b)` з `transformTo` → ТО `transform(a, stype)`; `transformToRandomChild` — у випадкового нащадка; `transformIfCounts` — ЯКЩО `count(stypeCount, in, [min,max])`.
- КОЛИ `contact(a, b)` з `cloneSprite` → ТО `clone(a)`; `spawnBehind` → `spawn_at(stype, behind_b)`.
- КОЛИ `contact(a, portal)` з `teleportToExit` → ТО `teleport(a, exit)`; виходу нема → `disappear(a)`.
- КОЛИ `contact(resource, avatar)` з `collectResource` → ТО `pickup(avatar, resource)` — значення додається до ресурсу B.
- КОЛИ `contact(a, b)` з `changeResource` → ТО `counter(resource, ±n)`.
- КОЛИ `contact(a, b)` з `killIfHasLess` / `killIfHasMore` → ЯКЩО `custom: «ресурс A ≤ / ≥ limit»` → ТО `disappear(a)`; `killIfOtherHasMore` — перевіряється ресурс B.
- КОЛИ `contact(a, b)` з `killIfFromAbove` → ЯКЩО `custom: «B прийшов згори»` → ТО `disappear(a)` (стрибок на голову).
- КОЛИ `contact(a, b)` з `subtractHealthPoints` / `addHealthPoints` → ТО `hp(a, ±n)`; `addHealthPointsToMax` — не вище максимуму.
- КОЛИ `contact(a, b)` з `reverseDirection` → ТО `bounce(a)`; `flipDirection` → `face(a, random)`; `attractGaze` → `face(a, dir_of_b)`; `turnAround` → `bounce(a)` + `move(a, down)`.
- КОЛИ `contact(a, b)` з `wrapAround` → ТО `wrap(a)`; `pullWithIt` → `custom: «A зсувається разом із B (платформа)»`; `align` → `custom: «A стає на позицію й орієнтацію B»`.
- КОЛИ `contact(a, b)` з `increaseSpeedToAll` / `decreaseSpeedToAll` / `setSpeedForAll` → ТО `speed(all_stype, ±n)`.
- КОЛИ `contact(a, b)` з `removeScore` → ТО `custom: «рахунок аватара = 0»`.

TerminationSet:
- КОЛИ `counter(stype, <=, limit)` (SpriteCounter) → ТО `win` або `lose` за параметром `win`; SpriteCounterMore — `>=`.
- КОЛИ `custom: «сума трьох типів = limit»` (MultiSpriteCounter) → ТО `win`/`lose`; StopCounter — поки умова діє, інші термінації заблоковані.
- КОЛИ `counter(tick, >=, limit)` (Timeout) → ТО `win` або `lose`.
- Перемога/поразка — як задано в TerminationSet гри · Рахунок — сума `scoreChange` · Порівняння агентів — перемоги, потім очки (?), потім час (?).

## Керування і ввід
- Дії `Types.ACTIONS`: `ACTION_NIL`, `ACTION_UP`, `ACTION_LEFT`, `ACTION_DOWN`, `ACTION_RIGHT`, `ACTION_USE`; яка гра які дає — `getAvailableActions()`.
- Агент — клас `Agent.java` (спадкує `core.player.AbstractPlayer`) у пакеті з іменем користувача; вивантажується zip-архівом.
- Таймер `ElapsedCpuTimer`: `elapsedMillis()`, `remainingTimeMillis()` — агент сам стежить за бюджетом.
- Двоє гравців: `StateObservationMulti`, у `scoreChange` — очки через кому для кожного гравця.
- Людина може грати клавіатурою (`key_handler=Pulse` у заголовку гри) (?).

## Вікна, меню, HUD
- `game-screen` (візуальний запуск з `Test.java`): поле спрайтів, рахунок і тік (?).
- Окремих меню нема — запуск з коду/IDE; рейтинги змагання — на сайті організаторів (`leaderboard`) (?).
- Для генераторів рівнів — перегляд згенерованого рівня і гра в нього (?).

## Фічі поза полем
- Треки: Single-Player Planning (`tracks.singlePlayer.Test`), 2-Player Planning, Single-Player Learning (окремий репозиторій GVGAI_GYM), Level Generation, Rule Generation.
- Зразкові агенти: Random, One Step Look-Ahead, Rolling Horizon Evolutionary Algorithm, Random Search, MCTS, Genetic Algorithm (і їхні 2-гравцеві версії).
- Генерація рівнів: генератор отримує VGDL-гру й має видати рівень за 5 годин; судді-люди грають по два рівні від різних генераторів і обирають кращий.
- Генерація правил: дано спрайти й рівень — генератор пише InteractionSet і TerminationSet; оцінка — так само парними вподобаннями людей.
- Обмеження для відсіву рівнів: один аватар; покриття поля в межах; DoNothing-агент не виграє й не гине N кроків; найкращий агент виграє; розвʼязок довший за N кроків; кожен ненароджуваний спрайт присутній.
- Аналізатори: `GameDescription`, `GameAnalyzer` (категорії спрайтів), `LevelAnalyzer` — для генераторів.

## Варіації й родичі
- py-vgdl (оригінальна Python-реалізація VGDL, Schaul) → java-vgdl у GVGAI; PuzzleScript — споріднена ідея «гра як текстовий опис» для пазлів.
- У корпусі: [minigrid](minigrid.md) і [gymnasium-toy-text](gymnasium-toy-text.md) (агент «стан → дія» на сітці), [bot-arenas](bot-arenas.md), [ai-challenge-ants](ai-challenge-ants.md), [pacman-capture-the-flag](pacman-capture-the-flag.md); ігри-прообрази — [sokoban](../push-slide/sokoban.md), [space-invaders](../maze-arcade/space-invaders.md).
- **Осі варіацій:** знання правил (повні / лише forward model / нічого — learning track) · бюджет (40 мс на тік / навчання наперед) · що генерує учасник (дії / рівні / правила) · гравців (1 / 2) · фізика (сітка / неперервна).

## Цікавинки для курсу
- Мінірушій VGDL: таблиця взаємодій «A × B → ефект» з текстового файла + рівень-матриця — 🥈 (дані замість коду, будь-яка аркада з одного рушія).
- `undoAll` / `stepBack`: відкат тіку при забороненій колізії замість перевірки «чи можна» — 📎.
- Forward model: `copy()` + `advance()` і жадібний one-step агент — 🥉.
- MCTS-агент з бюджетом 40 мс на хід — 🥇.
- Генератор рівнів з фільтром «DoNothing не гине, найкращий агент виграє» — 🥇.
- Генератор правил: випадкові взаємодії + перевірка грабельності агентами — 👑.
- Класи NPC (Chaser, Fleeing, Spreader, Bomber) як бібліотека поведінок — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` (Ongoing-аватари) · `push-object` (bounceForward) · `impassable-cells` · `projectile-shot` · `item-pickup` (Resource) · `teleport` (Portal) · `chase-player` · `random-walk` · `spawner-entity` · `spawn-schedule` · `timed-despawn` (Flicker) · `wrap-edges` · `hp-damage` · `touch-death` · `destroy-all-enemies` / `collect-all` (SpriteCounter) · `time-out` (Timeout) · `event-points` (scoreChange) · `interaction-table` (InteractionSet — буквально вона) · `level-from-txt` · `ai-opponent` / `ai-random` / `ai-greedy` (зразкові агенти) · `state-as-data` · `game-loop` · `logic-render-split` · `gui-render`.
- **Нема** → пропозиції карток:
  - `+forward-model` «Копія стану + симуляція дії для агента» · game-logic/opponent · 🥉.
  - `+game-description-language` «Гра описана текстом: спрайти, взаємодії, термінації» · levels/format · 🥈.
  - `+general-game-playing` «Один агент на багато невідомих ігор» · game-logic/opponent · 🥇.
  - `+level-generator-agent` «Програма генерує рівні для заданої гри» · levels/generation · 🥇.
  - `+rule-generator-agent` «Програма генерує правила для заданих спрайтів» · levels/generation · 👑.
  - `+playability-constraints` «Фільтр рівня: агенти-тестери, покриття, довжина розвʼязку» · levels/solvability · 🥈.
  - `+undo-whole-tick` «Заборонена колізія відкочує весь тік» · entities/legality · 📎.
  - `+ai-mcts` «Monte Carlo Tree Search з бюджетом часу» · game-logic/opponent · 🥇.
  - `+agent-program-interface`, `+turn-time-limit` — підтвердження.

## Пропозиції до словників
- `+trigger:timeout(bot)` — агент перевищив бюджет часу (підтвердження з family).
- `+effect:undo_tick` — відкат усього тіку для всіх сутностей (VGDL `undoAll`).
- `+effect:flee` — крок від найближчої сутності виду (підтвердження).
- `+effect:chase(a, b)` — крок до найближчої сутності виду B (VGDL Chaser).
- `+cond:resource(a, name, op, n)` — іменований ресурс сутності порівняно з N (`killIfHasLess`, `spawnIfHasMore`).
- `+feature:agent-api` (підтвердження), `+feature:forward-model` — агент може симулювати хід на копії стану.
- `+axis:observation` — що бачить агент: повний стан / спостереження / пікселі (підтвердження).
- `+card:forward-model`, `+card:game-description-language`, `+card:level-generator-agent`, `+card:rule-generator-agent`, `+card:playability-constraints`, `+card:undo-whole-tick` — див. «Мапа на каталог».

## Джерела
- ⭐ [GitHub: GAIGResearch/GVGAI](https://github.com/GAIGResearch/GVGAI) — README: фреймворк змагання, треки і їхні Test-класи, структура пакета агента, лінк на learning-трек.
- [Вікі GVGAI](https://github.com/GAIGResearch/GVGAI/wiki) — зміст: VGDL, контролери, генератори, forward model.
- [VGDL Language](https://github.com/GAIGResearch/GVGAI/wiki/VGDL-Language) — секції опису гри, приклади Sokoban 1/2 гравці, формат рівня.
- [Interactions](https://github.com/GAIGResearch/GVGAI/wiki/Interactions) · [Avatar Sprites](https://github.com/GAIGResearch/GVGAI/wiki/Avatar-Sprites) · [Other Sprites](https://github.com/GAIGResearch/GVGAI/wiki/Other-Sprites) · [Termination Conditions](https://github.com/GAIGResearch/GVGAI/wiki/Termination-Conditions) — довідник класів.
- [Planning Track Specifications](https://github.com/GAIGResearch/GVGAI/wiki/Planning-Track-Specifications) · [Creating Controllers](https://github.com/GAIGResearch/GVGAI/wiki/Creating-Controllers) · [Advancing and copying the state](https://github.com/GAIGResearch/GVGAI/wiki/Advancing-and-copying-the-state) — бюджети, дії, forward model.
- [Tracks Description](https://github.com/GAIGResearch/GVGAI/wiki/Tracks-Description) · [Constraints](https://github.com/GAIGResearch/GVGAI/wiki/Constraints) — треки генерації й обмеження рівнів.
- [aliens.txt](https://raw.githubusercontent.com/GAIGResearch/GVGAI/master/examples/gridphysics/aliens.txt) — повний приклад гри.
- [arXiv 1802.10363](https://arxiv.org/abs/1802.10363) — огляд фреймворку, старт 2014.

## Непевне
- (?) Як ранжують агентів у planning-треку (перемоги → очки → час, бали «Формули-1») — на відкритих сторінках не знайдено.
- (?) Максимальна кількість тіків гри, кількість ігор і рівнів у наборах змагання — не бачив.
- (?) Візуальний режим і людська гра з клавіатури — з назв `Test.java`/`key_handler`, не перевірено.
- (?) `contphysics` — чи запускається в Java-версії (вікі: java-vgdl підтримує лише GridPhysics).
- (?) Роки проведення змагання після 2014 і чи воно ще триває; сайт gvgai.net агентам не відкривається.
