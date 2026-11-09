---
title: Super Puzzle Platformer Deluxe
slug: super-puzzle-platformer-deluxe
aka: [Super Puzzle Platformer, SPPD]
family: falling-match
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2013
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/238530/Super_Puzzle_Platformer_Deluxe/", best: true, note: "суть «стріляй у блоки замість складати», 9 персонажів, 7 світів, челенджі, versus, таблиці"}
  - {kind: other, url: "https://hardcoregamer.com/reviews/review-super-puzzle-platformer-deluxe/42461/", note: "огляд: колодязь 8 блоків, 3 кольори, постріл лише вліво/вправо, групи міцніші, золоті уламки → рівень 1–4, розчавлення знімає рівень, пастки, ракети, зірка"}
  - {kind: other, url: "https://www.destructoid.com/?p=126589", note: "огляд: шипи внизу, очки 1/4/9 за 1/2/3 блоки, самоцвіти по 100 і розблокування рівнів, пастки, костюми"}
  - {kind: other, url: "https://indiegamereviewer.com/?p=14261", note: "огляд: керування геймпадом, рівень як життя, versus на одному екрані"}
  - {kind: other, url: "https://www.honestgamers.com/14499/pc/super-puzzle-platformer-deluxe/review.html", note: "огляд: пришвидшення, шипоносна яма, пастки знімаються лише через сусідній блок"}
  - {kind: other, url: "https://www.gog.com/en/game/super_puzzle_platformer_deluxe", note: "GOG-сторінка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=super+puzzle+platformer+deluxe+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, spawn-random-cell, progress-acceleration, projectile-shot, shoot-forward, destructible-blocks, hp-damage, environment-death, touch-death, item-pickup, drop-on-death, event-points, in-round-upgrades, temporary-modes, chase-player, explode-area, level-unlock, level-select, character-select, achievements-window, leaderboard, simultaneous-versus, game-screen, end-screen, +connected-group-pop, +group-score-quadratic, +shoot-cluster-hp, +garbage-adjacent-clear, +crush-by-fall, +level-as-lives, +platform-jump]
proposes: ["+effect:jump(height)", "+trigger:crushed(a)", "+card:shoot-cluster-hp", "+card:level-as-lives"]
author: opus
date: 2026-11-09
---

# Super Puzzle Platformer Deluxe — герой-платформер у стакані Tetris: стріляє в падаючі блоки, звʼязні одноколірні зникають групою

## Суть
Падаючі блоки трьох кольорів сиплються згори у вузький колодязь, а гравець не керує ними — він бігає й стрибає по купі маленьким героєм і **стріляє вліво/вправо**. Постріл по блоку руйнує всю звʼязну одноколірну групу, але група тим міцніша, чим більша, а очки ростуть квадратично (1 → 1, 2 → 4, 3 → 9). Під купою — шипи, згори падають блоки (розчавлення) і пастки замість блоків; мета — протриматися якнайдовше. Ядро — те саме «зібрати велику групу», що в [puyo-puyo](puyo-puyo.md), але руками аватара, а не курсора.

## Поле і час
- Колодязь шириною 8 блоків (Hardcore Gamer); блоки лежать на сітці, герой рухається вільно (платформерна фізика), висота — (?).
- Дно — шипи: торкнутися — смерть. Купа росте нерівно: гори, ями, ущелини.
- Real-time; блоки падають випадково, зазвичай по одному; швидкість падіння росте з хвилинами.
- 6–7 світів (рівнів), кожен зі своїм набором пасток.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Yellow-guy / сир у плащі) | player | рівень 0–4, костюм | біг, стрибок, постріл вліво/вправо; рівень = сила пострілу й множник |
| Кольоровий блок | tile | колір ×3 | падає, лягає на купу; звʼязні одноколірні — одна група |
| Група блоків | zone | розмір n, міцність ~n | руйнується цілком від кількох пострілів; більша — більше пострілів |
| Золотий уламок (chip) | pickup | 1 очко | вилітає з розбитого блока; наповнює шкалу досвіду |
| Самоцвіт | pickup | 100 очок | іноді з блока; валюта розблокувань |
| Блок-пастка (лазер, бензопила, шипи, TNT, вогняний промінь, шипована куля) | hazard | вид | падає замість блока; дотик — смерть; пострілом не руйнується |
| Ракетна установка | spawner | — | випускає самонавідні ракети |
| Ракета, вогняна куля | projectile | — | летить на героя; дотик — смерть |
| Монстр | enemy | — | вивільняється каскадом, блукає верхом купи |
| Зірка невразливості | pickup | тривалість | з'являється за велике комбо |
| Шипи дна | hazard | — | смерть від дотику |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ТО `spawn_at(block, random_column_top)`, `fall(block)`; з часом `speed(spawn, +n)`.
- КОЛИ `timer(every)` → ЯКЩО `counter(hero_level, >=, 1)` і `prob(p)` → ТО `spawn_at(hazard_block, random_column_top)` замість блока.
- КОЛИ `input(dir)` → ТО `move(player, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок, висота залежить від костюма»`.
- КОЛИ `input(shoot)` → ТО `spawn_at(shot, facing)` — лише горизонтально.
- КОЛИ `contact(shot, block)` → ТО `damage(group, power)`; ЯКЩО `custom: «міцність групи вичерпано (росте з розміром групи)»` → ТО `clear(group)`, `fall(blocks_above)`.
- КОЛИ `after(clear)` → ТО `score(n²)` (n — розмір групи), `spawn_at(chip, cells)`, `rng(p)` → `spawn_at(gem, cell)`.
- КОЛИ `picked(player, chip)` → ТО `score(1)`, `counter(xp, +1)`; КОЛИ `counter(xp, >=, threshold)` → ТО `counter(hero_level, +1)` (до 4): сильніший постріл, множник очок.
- КОЛИ `picked(player, gem)` → ТО `score(100)`, `currency(+1)`.
- КОЛИ `contact(shot, hazard_block)` → ТО `block`; КОЛИ `after(clear)` → ЯКЩО `adjacent(hazard_block, cleared_group)` → ТО `disappear(hazard_block)`.
- КОЛИ `custom: «блок упав герою на голову»` → ТО `counter(hero_level, -1)`; пастка на голову → `lose`.
- КОЛИ `contact(player, spikes|laser|chainsaw|fireball|missile)` → ТО `lose` (Destructoid, Hardcore Gamer); IGR — `counter(hero_level, -1)`, рівень 0 → `lose` (?).
- КОЛИ `timer(every)` → ЯКЩО `custom: «ракетна установка на полі»` → ТО `spawn_at(missile, launcher)`, `custom: «самонаводиться на героя»`.
- КОЛИ `custom: «TNT спрацював»` (?) → ТО `explode(area, n)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «великий каскад»` → ТО `spawn_at(monster, pile_top)` (?).
- КОЛИ `custom: «велике комбо»` → ТО `spawn_at(star, field)`; КОЛИ `picked(player, star)` → ТО `set_state(player, invincible, dur)`.
- КОЛИ `died(player)` → ТО `game_over`, `window(end-screen)`.
- КОЛИ `counter(gems_total, >=, n)` → ТО `unlock(world)` — сума самоцвітів накопичується між забігами.
- Перемоги нема (виживання) · Поразка: смерть героя · Рахунок: n² за групу, уламки, самоцвіти, множник рівня.

## Керування і ввід
- Геймпад (IGR): лівий стік — рух, A — стрибок, правий тригер — основна зброя, лівий — додаткова (?); перепризначення клавіш.
- Стріляти можна лише вліво/вправо; блок під ногами знімається пострілом по одноколірному сусідові, що стоїть поруч на рівні героя.

## Вікна, меню, HUD
- `main-menu` → `level-select` (світи, відкриті самоцвітами) · челенджі (20+) · versus.
- `character-select` — костюми/персонажі (9 за Steam).
- `game-screen`: колодязь, `score`, шкала досвіду й рівень героя, лічильник самоцвітів (?).
- `end-screen` — рахунок забігу; `leaderboard` (Steam); `achievements-window` (30+).

## Фічі поза полем
- `level-unlock` за накопиченими самоцвітами, `unlockables` (костюми, світи, челенджі), `mode-versus` на одному екрані — хто довше протримається, челендж-кімнати з однією пасткою (пройти по шипах, вгадати радіус TNT), `leaderboard-online`, `achievements`.

## Варіації й родичі
- Костюми: плащ (повільне падіння, високий стрибок), ніндзя (подвійний стрибок, слабкі сюрікени), ракетник (сильний постріл; стрибок — суперечать огляди), хатімакі (короткий стрибок, удар на 1 клітину, дуже сильний, швидкі удари).
- Родичі: [puyo-puyo](puyo-puyo.md) і [samegame-flood](samegame-flood.md) (звʼязна група, квадратичні очки), [meteos](meteos.md), [mr-driller](../dig-gravity/mr-driller.md) (аватар серед кольорових блоків, що падають), [quarth](quarth.md) (стріляти в падаючі блоки).
- **Осі варіацій**: хто діє в стакані (курсор / падаюча фігура / **аватар-платформер**) · як знімати групу (автоматично / клік / **постріл з міцністю ~ розміру групи**) · життя (одне / **рівень героя як буфер**).

## Цікавинки для курсу
- Звʼязна одноколірна група з міцністю, що росте з розміром, + очки n² — 📎.
- Аватар-платформер поверх клітинної купи: стояння на блоках, розчавлення падаючим — 🥉.
- Пастки-«сміття», що знімаються лише через сусідній блок, — 🌱.
- Рівень героя як шкала досвіду й буфер життів одночасно — 🌱.
- Розблокування світів сумою самоцвітів між забігами — 🌱.

## Мапа на каталог
- Є: `gravity-fall`; `spawn-random-cell` ↔ випадкова колонка; `progress-acceleration`; `projectile-shot` + `shoot-forward`; `destructible-blocks`; `hp-damage` ↔ міцність групи; `environment-death` ↔ шипи дна; `touch-death` ↔ пастки; `item-pickup`, `drop-on-death` ↔ уламки й самоцвіти з блоків; `event-points`; `in-round-upgrades` ↔ рівень героя; `temporary-modes` ↔ зірка; `chase-player` ↔ самонавідні ракети; `explode-area` ↔ TNT; `level-unlock`, `level-select`, `character-select`, `achievements-window`, `leaderboard`, `simultaneous-versus`, `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+shoot-cluster-hp` «Постріл по групі: міцність = f(розмір), руйнується вся група» · entities/combat · 📎.
  - `+level-as-lives` «Рівень героя — водночас сила й запас життів» · game-logic/lose · 🌱.
  - Повтор чужих: `+connected-group-pop`, `+group-score-quadratic`, `+garbage-adjacent-clear`, `+crush-by-fall`, `+platform-jump`.

## Пропозиції до словників
- `+effect:jump(height)` — стрибок аватара (уже пропоноване корпусом).
- `+trigger:crushed(a)` — сутність розчавлена падаючим (уже пропоноване).
- `+card:shoot-cluster-hp`, `+card:level-as-lives` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Super Puzzle Platformer Deluxe](https://store.steampowered.com/app/238530/Super_Puzzle_Platformer_Deluxe/) — суть, 9 персонажів, 7 світів, 20+ челенджів, versus, таблиці, дата 24.05.2013, Andrew Morrish / Adult Swim Games.
- [Hardcore Gamer review](https://hardcoregamer.com/reviews/review-super-puzzle-platformer-deluxe/42461/) — ширина 8, 3 кольори, постріл лише вбік, міцність груп, рівні 1–4, розчавлення, пастки, монстри, ракети, зірка, костюми.
- [Destructoid review](https://www.destructoid.com/?p=126589) — шипи, очки 1/4/9, уламки, самоцвіти 100 і розблокування, пастки, челендж-кімнати, костюми.
- [IndieGameReviewer](https://indiegamereviewer.com/?p=14261) — керування, рівень як життя, versus на одному екрані, 35 досягнень.
- [HonestGamers review](https://www.honestgamers.com/14499/pc/super-puzzle-platformer-deluxe/review.html) — пришвидшення, рельєф купи, пастки знімаються лише через сусіда.

## Непевне
- (?) Смерть: Destructoid і Hardcore Gamer — дотик пастки/шипів одразу кінець; IGR — удари знімають рівень, кінець на нулі.
- (?) Висота колодязя, чи програш, коли купа дійде до верху; точна міцність групи від розміру.
- (?) Ракетник: «найвищий стрибок» (Hardcore Gamer) проти «нижчий стрибок» (Destructoid).
- (?) Versus — одне спільне поле чи два колодязі на одному екрані.
- (?) Оригінал без «Deluxe» (Flash-версія до 2013) — рік і відмінності не перевірено.
