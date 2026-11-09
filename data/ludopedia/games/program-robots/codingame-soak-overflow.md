---
title: "CodinGame Summer Challenge 2025: Soak Overflow"
slug: codingame-soak-overflow
aka: [Soak Overflow, Summer Challenge 2025, Водяний бій]
family: program-robots
also: [tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: territory
year: 2025
platforms: [web]
links:
  - {kind: official, url: "https://github.com/CodinGame/SummerChallenge2025-SoakOverflow", best: true, note: "код судді й умова (HTML GitHub дав 504; сирі файли нижче відкрились)"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/config/statement_en.html.tpl", note: "умова: вологість, дальність, укриття, HUNKER_DOWN, бомби-бризки, контроль клітин, порядок дій, ліги, протокол"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/src/main/java/com/codingame/game/Game.java", note: "фази ходу, рух із конфліктами, формула шкоди, укриття, зони контролю, перевага 600"}
  - {kind: other, url: "https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/src/main/java/com/codingame/game/AgentClass.java", note: "5 класів агентів: перезарядка, сила, дальність, бомби"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+soak+overflow", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, chase-bfs, hp-damage, shoot-cooldown, explode-area, move-timer, replay, leaderboard, state-as-data, game-loop, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +auto-pathfind-command, +league-boss-promotion, +local-referee, +symmetric-map-generation, +unit-classes-stats, +range-falloff-damage, +directional-cover, +hunker-damage-reduction, +friendly-fire-splash, +territory-by-distance, +wounded-weight-distance, +move-conflict-cancel, +point-lead-victory, +tutorial-league-objectives]
proposes: ["+cond:cover_between(target, shooter)", "+cond:cooldown_ready(a)", "+effect:soak(a, n)", "+trigger:timeout(bot)", "+effect:eliminate(bot)", "+ui:debug-message", "+window:replay-viewer", "+feature:bot-upload", "+feature:league-promotion"]
author: opus
date: 2026-11-09
---

# Soak Overflow — водяний бій загонів ботів: укриття з боку пострілу, «пригнутись», бомби-бризки по 3×3 і очки за клітини, ближчі до твоїх агентів

## Суть
Конкурс CodinGame (літо 2025) на двох гравців: кожен керує загоном із 3–5 агентів різних класів на сітці з укриттями. Щохід кожен агент може рухнутись на клітину і зробити одну бойову дію — постріл із водяного пістолета, кидок бомби-бризки або «пригнутись». Вологість ≥ 100 виводить агента з гри. Очки дає **контроль території**: клітина належить тому, чий агент ближчий (мокрий агент рахується вдвічі далі), і щохід гравець з більшою територією отримує різницю клітин. Виграє перевага в 600 очок, знищення загону суперника або більше очок після 100 ходів.

## Поле і час
- Квадратна сітка шириною 12–20 і висотою 6–10; клітина: `0` порожня, `1` низьке укриття, `2` високе укриття; укриття непрохідні.
- Розстановка дзеркальна: агенти другого гравця — на протилежних (`grid.opposite`) клітинах.
- Хід синхронний для обох гравців і всіх агентів, але з пріоритетом фаз: `MOVE` → `HUNKER_DOWN` → `SHOOT` і `THROW` → прибирання промоклих → зони контролю → очки.
- Партія до 100 ходів; 50 мс на хід, 1000 мс на перший.
- Відстані — за Мангеттеном; повна інформація (у вводі є всі агенти з вологістю, перезарядкою й бомбами).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | piece | `agentId`, власник, вологість 0–100, перезарядка, бомби | крок на сусідню клітину + одна бойова дія за хід |
| Gunner | piece | перезарядка 1, сила 16, дальність 4, бомб 1 | універсальний стрілець |
| Sniper | piece | перезарядка 5, сила 24, дальність 6, бомб 0 | далекий рідкий постріл |
| Bomber | piece | перезарядка 2, сила 8, дальність 2, бомб 3 | слабкий постріл, багато бомб |
| Assault | piece | перезарядка 2, сила 16, дальність 4, бомб 2 | середній з бомбами |
| Berserker | piece | перезарядка 5, сила 32, дальність 2, бомб 1 | дуже сильний ближній постріл |
| Низьке укриття `1` | static | множник шкоди 0.5 | непрохідне; захищає сусіда від пострілів з протилежного боку |
| Високе укриття `2` | static | множник шкоди 0.25 | так само, сильніше |
| Бомба-бризки | projectile | кидок до 4 клітин, 30 вологості | бʼє клітину й 8 сусідів, **усіх** агентів, ігнорує укриття |
| Зона контролю | zone | клітини гравця | клітини, де найближчий агент — твій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «бот отримує кількість агентів і рядки agentId x y cooldown splashBombs wetness, потім myAgentCount»`; на старті перезарядка кожного `counter(cooldown, −1)`.
- КОЛИ `input(id; MOVE x y)` → ЯКЩО `path_exists(agent, (x, y))` → ТО `move(agent, dir)` на перший крок найкоротшого шляху в обхід укриттів і агентів.
- КОЛИ `custom: «ціль кроку зайнята агентом, що стоїть»` або `custom: «два кроки в одну клітину чи обмін місцями»` → ТО `block` для обох; `custom: «скасування ланцюгом скасовує кроки в звільнені ними клітини»`.
- КОЛИ `input(id; HUNKER_DOWN)` → ТО `set_state(agent, hunkered, 1)` — −25 % шкоди від пострілів цього ходу.
- КОЛИ `input(id; SHOOT target)` → ЯКЩО `counter(cooldown, ==, 0)` and `in_range(agent, target, 2·optimalRange)` → ТО `damage(target, n)`: `n = round(soakingPower × дальність × (укриття − 0.25·hunker))`; потім `custom: «cooldown = перезарядка класу + 1»`.
- КОЛИ `custom: «дистанція ≤ optimalRange»` → ТО дальність = 1; ≤ 2·optimalRange → 0.5; далі → `custom: «постріл не відбувся, помилка в лог»`.
- КОЛИ `custom: «між ціллю і стрільцем по осі X чи Y понад 1 клітину»` → ЯКЩО `cell(target_neighbor_toward_shooter, cover)` and `custom: «стрілець не сусідить з цим укриттям (Чебишов > 1)»` → ТО множник укриття 0.5 / 0.25; з двох осей береться найкраще.
- КОЛИ `input(id; THROW x y)` → ЯКЩО `in_range(agent, (x, y), 4)` and `has(agent, splash_bomb)` → ТО `explode(square3, 30)`: кожному агенту в клітині й 8 сусідах `damage(agent, 30)` без знижок, свої теж; `take(agent, splash_bomb)`.
- КОЛИ `counter(wetness, >=, 100)` → ТО `custom: «агент позначений dying»`, `disappear(agent)` на початку наступного ходу; у підрахунку зон він уже не бере участі.
- КОЛИ `phase_start(control)` → ТО для кожної клітини `custom: «найближчі агенти за Мангеттеном; у агента з вологістю ≥ 50 відстань ×2»`; ЯКЩО `custom: «усі найближчі — одного гравця»` → ТО `custom: «клітина в зоні цього гравця»`; рівність різних гравців — нічия клітина.
- КОЛИ `turn_end` → ЯКЩО `custom: «мої клітини > клітини суперника»` → ТО `score(+різниця)`.
- КОЛИ `custom: «очки гравця > очки суперника + 600»` → ТО `win`, `game_over`.
- КОЛИ `all_gone(enemy_agent)` → ТО `win`, `game_over`.
- КОЛИ `counter(turn, ==, 100)` → ТО `game_over`; більше очок → `win`.
- КОЛИ `custom: «бот не відповів вчасно або команда хибна»` → ТО `lose`.
- Перемога: +600 очок переваги, знищений загін суперника або більше очок на 100-му ході · Поразка: таймаут, хибна команда, втрата всіх агентів · Рахунок: щоходу + (мої клітини − чужі), якщо різниця додатна.

## Керування і ввід
- Ініціалізація: `myId`; `agentDataCount` рядків `agentId player shootCooldown optimalRange soakingPower splashBombs`; `width height`; клітини `x y tileType`.
- Щоходу: `agentCount` рядків `agentId x y cooldown splashBombs wetness`, потім `myAgentCount`.
- Вивід — рівно один рядок на свого агента: `id;MOVE x y;SHOOT t` — до однієї дії руху, однієї бойової (`SHOOT id` / `THROW x y` / `HUNKER_DOWN`) і `MESSAGE text`; порядок у рядку не важливий, виконання — за фазами.
- Рух — ціль-клітина, шлях будує суддя; бот вирішує «куди», а не «як».

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова з лігами, редактор, консоль, Play testing / Submit.
- `replay-viewer`: поле з укриттями, агенти з вологістю, траєкторії пострілів і бомб, зони контролю (?); наведення на клітину — підказка з даними клітини; шестерня — додаткові налаштування показу; пробіл — пауза, стрілки — кадр.
- `debug-message`: текст `MESSAGE` над агентом.
- `end-screen`: очки гравців («N points»).
- `league-ladder`: 4 навчальні Wood-ліги з окремими цілями → повна гра.

## Фічі поза полем
- **Навчальні ліги з цілями** (проти боса, 3 з 5 спроб): 1 — довести агентів у (6,1) і (6,3); 2 — щоходу стріляти в наймокрішого ворога; 3 — за 1 хід стати за найкраще укриття й стріляти в найменш захищеного; 4 — бомбами знищити три групи ворогів, не зачепивши своїх (40 ходів, стрільба вимкнена).
- `bot-upload`, `leaderboard-online`, `league-promotion`, `replay`.
- `local-referee`: відкритий Java-код судді на CodinGame SDK, рівно 2 гравці.

## Варіації й родичі
- Тактики з укриттями: [xcom](../tactics/xcom.md) (півукриття / повне, «пригнутись»), [frozen-synapse](../tactics/frozen-synapse.md) (одночасні накази); тут — без шансу влучання, шкода детермінована.
- Арени CodinGame: [codingame-hypersonic](codingame-hypersonic.md) (бомби, автошлях), [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md) (територія за присутністю), [codingame-olymbits](codingame-olymbits.md); Splatoon-подібна «фарба як територія» — [splat](../maze-arcade/splat.md) за темою.
- Осі варіацій: **укриття** (за напрямком пострілу / в радіусі / шанс влучання); **територія** (Вороного за відстанню / зафарбовані клітини / присутність); **кінець** (перевага N / час / знищення); **дружній вогонь** (бомби — так, постріли — ні).

## Цікавинки для курсу
- Формула шкоди: дальність × (укриття − hunker), з вибором найкращого укриття по двох осях — 📎.
- Діаграма Вороного на сітці з «вагою» поранених агентів і підрахунок очок — 🥉.
- Рух із розвʼязанням конфліктів: одна клітина / обмін / ланцюг скасувань — 🥉.
- Кидок бомби: перебір клітин у радіусі 4, вигода = мокрі вороги − свої в 3×3 — 📎.
- Позиціювання загону під укриття з оцінкою «мене не дістануть, я дістаю» — 🥈.
- Повний симулятор ходу для пошуку (MCTS / beam search) по 3–5 агентах на обидва боки — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (укриття) · `chase-bfs` (автошлях до цілі) · `hp-damage` (вологість до 100) · `shoot-cooldown` · `explode-area` (бомба 3×3) · `move-timer` · `replay` · `leaderboard` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+league-boss-promotion`, `+local-referee`, `+symmetric-map-generation` — з [bot-arenas](bot-arenas.md); `+auto-pathfind-command` — з [codingame-hypersonic](codingame-hypersonic.md).
  - `+unit-classes-stats` «Класи юнітів — набір чисел (сила, дальність, перезарядка, боєзапас)» · entities/state · 🌱.
  - `+range-falloff-damage` «Повна шкода до дальності D, половина до 2D, далі промах» · entities/combat · 🌱.
  - `+directional-cover` «Укриття діє лише проти пострілу з протилежного боку» · entities/combat · 📎.
  - `+hunker-damage-reduction` «Дія-захист: −25 % шкоди цього ходу» · entities/combat · 🌱.
  - `+friendly-fire-splash` «Площинна атака бʼє і своїх» · entities/combat · 🌱.
  - `+territory-by-distance` «Клітина належить власнику найближчого юніта (Вороного)» · game-logic/score · 🥉.
  - `+wounded-weight-distance` «Поранений юніт контролює менше: відстань ×2» · game-logic/score · 🌱.
  - `+move-conflict-cancel` «Конфліктні кроки скасовуються ланцюгом» · entities/move · 📎.
  - `+point-lead-victory` «Достроковий кінець при перевазі N очок» · game-logic/win · 🌱.
  - `+tutorial-league-objectives` «Навчальні ліги з окремою ціллю й ботом-босом» · interface/menus · 📎.

## Пропозиції до словників
- `+cond:cover_between(target, shooter)` — між ціллю і стрільцем є укриття, що захищає ціль (Soak Overflow, XCOM).
- `+cond:cooldown_ready(a)` — перезарядка завершена (друге підтвердження після kaggle-crawl).
- `+effect:soak(a, n)` — додати вологість/шкоду, що не зменшує HP, а наповнює шкалу до порогу вибування (можна звести до `damage`).
- `+trigger:timeout(bot)` · `+effect:eliminate(bot)` · `+ui:debug-message` · `+window:replay-viewer` · `+feature:bot-upload` · `+feature:league-promotion` — підтвердження з арен.

## Джерела
- ⭐ [CodinGame/SummerChallenge2025-SoakOverflow](https://github.com/CodinGame/SummerChallenge2025-SoakOverflow) — репозиторій судді (README — лише заголовок; HTML недоступний у момент читання).
- [statement_en.html.tpl](https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/config/statement_en.html.tpl) — правила, приклади укриттів, ліги з цілями, умови перемоги, протокол, обмеження (12–20 × 6–10, 6–10 агентів).
- [Game.java](https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/src/main/java/com/codingame/game/Game.java) — порядок фаз, рух і конфлікти, `getCoverModifier`, `getRangeModifier`, бомби `THROW_DAMAGE = 30`, `THROW_DISTANCE_MAX = 4`, `MAX_POINT_DIFF = 600`, зони контролю.
- [AgentClass.java](https://raw.githubusercontent.com/CodinGame/SummerChallenge2025-SoakOverflow/main/src/main/java/com/codingame/game/AgentClass.java) — GUNNER, SNIPER, BOMBER, ASSAULT, BERSERKER; `Agent.java` — ×2 відстань при вологості ≥ 50; `Referee.java` — 100 ходів, 50/1000 мс.

## Непевне
- (?) Як класи розподіляються по агентах: у коді класи беруться по порядку переліку для кожної точки старту, але в умові кількість і склад загону можуть відрізнятись від карти до карти.
- (?) Генератор карт (розставлення укриттів, точки старту) — у файлі, якого не знайшов; дзеркальність — з виклику `grid.opposite`.
- (?) Шкода округлюється `Math.round` — з високим укриттям і hunker множник 0, тобто постріл не шкодить; умова це підтверджує («100 %» захисту).
- (?) Перезарядка: у коді після пострілу `cooldown = max + 1` і −1 на старті ходу, тобто стріляє раз на `max + 1` ходів — умова каже «скільки ходів чекати після пострілу».
- (?) Чи показує переглядач зони контролю кольором — не бачив.
