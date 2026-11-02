---
title: Centipede (Багатоніжка)
slug: centipede
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1981
platforms: [arcade, Atari 2600, Atari 5200, PC, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Centipede_(video_game)", best: true, note: "правила, усі вороги й очки, отруєні гриби, відновлення поля"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=centipede+1981+arcade+gameplay", note: "пошук; геймплей оригіналу"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=centipede", note: "пошук; збірки Atari"}
stage: v1
coverage: 70
mechanics: [move-8dir, impassable-cells, projectile-shot, shoot-forward, body-queue, cell-transform, spawn-schedule, enemy-waves, touch-death, player-death, event-points, progress-acceleration, score-records, leaderboard, hot-seat, +descend-and-reverse, +segment-split, +destructible-blocks, +poison-cell, +density-triggered-spawn, +player-zone, +distance-score, +restore-on-death, +extra-life-threshold, +shot-leaves-obstacle]
proposes: ["+trigger:blocked", "+trigger:edge", "+trigger:died", "+trigger:counter", "+cond:count", "+cond:in_range", "+cond:state", "+effect:split", "+effect:set_cell", "+effect:set_state", "+effect:hp", "+effect:spawn_at", "+effect:lives", "+role:terrain", "+card:segment-split", "+ui:lives", "+axis:control"]
author: opus
date: 2026-11-02
---

# Centipede — стріляй у багатоніжку, що спускається крізь грибне поле, не даючи їй дійти до тебе

## Суть
Гравець керує «Bug Blaster» у нижній смузі екрана й стріляє вгору. Згори повзе багатоніжка-ланцюг: біжить по рядку, біля гриба чи краю спускається на рядок і розвертається. Постріл у середину розрізає її на дві — хвіст отримує власну голову; кожен збитий сегмент стає грибом, тож гравець сам будує лабіринт, який прискорює спуск. Павук, блоха й скорпіон по-різному псують поле: їдять гриби, сиплють нові, труять наявні.

## Поле і час
- Поле — сітка клітин (≈ 30×32 по 8 px) (?); гриби стоять у клітинах, багатоніжка рухається по рядках сітки.
- Нижні кілька рядків — **зона гравця**: Bug Blaster ходить лише в ній (трекбол дає майже вільний рух у межах зони).
- Багатоніжка, що дійшла до низу, розвертається вгору в межах зони і знову вниз; поки вона там, збоку періодично заповзають нові одиночні голови.
- Real-time; темп хвиль і спавну зростає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Bug Blaster | player | 3 життя (?) | рух у зоні гравця; постріл угору, 1 на екрані, автовогонь |
| Постріл | projectile | — | летить угору; 1 влучання = 1 удар |
| Голова багатоніжки | enemy | 100 очок | по рядку; гриб/край → вниз на рядок і розворот |
| Сегмент тіла | enemy | 10 очок | повторює шлях голови (`body-queue`) |
| Гриб | terrain | 4 удари, 1 очко | непрохідний для багатоніжки (змушує спуститись); перешкода для пострілу |
| Отруєний гриб | terrain | 4 удари | багатоніжка, що його торкнулась, пірнає прямо вниз |
| Павук | enemy | 300/600/900 за відстанню | зигзаги в зоні гравця; їсть гриби, через які проходить |
| Блоха | enemy | 2 удари, 200 очок | падає вертикально, лишає гриби; після 1-го удару прискорюється (?) |
| Скорпіон | enemy | 1000 очок | перетинає верхню частину поля горизонтально; труїть гриби на шляху |
| Нова голова | enemy | 100 очок | заповзає збоку в зону гравця, поки там є багатоніжка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(head, dir)`; КОЛИ `blocked(head)` (гриб) або `edge(head)` → ТО `move(head, down)`, `face(head, reverse)`; тіло — `custom: «кожен сегмент займає попередню клітину сусіда попереду»`.
- КОЛИ `contact(shot, head)` → ТО `disappear_b`, `score(100)`, `set_cell(cell, mushroom)`; наступний сегмент стає головою.
- КОЛИ `contact(shot, body_segment)` → ТО `disappear_b`, `score(10)`, `set_cell(cell, mushroom)`, `split(centipede)` — сегмент за збитим стає головою нової багатоніжки.
- КОЛИ `contact(shot, mushroom)` → ТО `hp(mushroom, -1)`; ЯКЩО `hp == 0` → ТО `disappear_b`, `score(1)`.
- КОЛИ `contact(head, poisoned_mushroom)` → ТО `set_state(centipede, diving)` — рух прямо вниз до зони гравця, далі звичайний.
- КОЛИ `reach(head, bottom)` → ТО `face(head, up)` у межах зони; і `timer(every)` → `spawn_at(head, side_of_player_zone)`, поки багатоніжка в зоні.
- КОЛИ `rng` → ЯКЩО `count(mushrooms_in_player_zone, <, N)` → ТО `spawn_at(flea, top)`; блоха падає й `spawn(mushroom)` за собою з ймовірністю.
- КОЛИ `contact(spider, mushroom)` → ТО `disappear_b`; КОЛИ `contact(shot, spider)` → ТО `score(300|600|900)` за `in_range(spider, player)` (ближче — дорожче).
- КОЛИ `contact(scorpion, mushroom)` → ТО `transform(poisoned_mushroom)`; КОЛИ `contact(shot, scorpion)` → ТО `score(1000)`.
- КОЛИ `contact(player, centipede|spider|flea)` → ТО `lose` (мінус життя).
- КОЛИ `died(player)` → ТО `custom: «кожен пошкоджений чи отруєний гриб відновлюється»`, `score(5)` за кожен.
- КОЛИ `all_gone(centipede)` → ТО нова хвиля: багатоніжка на 1 сегмент коротша + на 1 швидку окрему голову більше; коли всі сегменти — окремі голови, цикл повторюється; змінюються кольори (?).
- КОЛИ `counter(score, +=, 12000)` → ТО `lives(+1)` (кожні 12 000).
- Перемога: нема (рекорд). Поразка: 0 життів. Рахунок: голова 100, тіло 10, гриб 1, блоха 200, павук 300–900, скорпіон 1000, відновлений гриб 5.

## Керування і ввід
- Трекбол — швидкий аналоговий рух у межах зони гравця; кнопка вогню (утримання = безперервна стрільба одним снарядом).
- Два гравці по черзі; кнопки 1P/2P Start.
- У портах без трекбола — джойстик/клавіші 8 напрямків.

## Вікна, меню, HUD
- `splash-screen` / атракт: демо-гра і таблиця рекордів.
- `game-screen` — грибне поле; згори `score` гравців, `hi-score`, `lives` (іконки бластерів).
- `leaderboard` — таблиця рекордів з ініціалами (введення трьох літер після GAME OVER).
- Після смерті — анімація відновлення грибів з нарахуванням очок.
- Переходи: атракт → (монета, Start) → гра → (смерть) відновлення грибів → гра → … → (0 життів) введення ініціалів → атракт.

## Фічі поза полем
- `+feature:operator-settings` (DIP): кількість життів, поріг бонусного життя, складність (?).
- `hotseat` (по черзі); `leaderboard-local` з ініціалами.
- Нема паузи, збережень, рівнів.

## Варіації й родичі
- Millipede (1982): дзвіночки-DDT вибухи, більше комах, гриби зсуваються вниз; Centipede 3D/2000-ні римейки.
- Родичі: Space Invaders (строй, що спускається), Snake (`body-queue`), Galaga (стрільба вгору).
- **Осі варіацій:** ланцюг ворога (цілий / ділиться / кожен сегмент — окремий); перешкоди (статичні / гравець їх створює / вороги створюють і труять); зона гравця (весь екран / смуга).

## Цікавинки для курсу
- Розщеплення ланцюга: новий «голова» з хвоста, рекурсивні шматки — 🥉.
- `descend-and-reverse` у сітці з грибами: що щільніше поле, то швидший спуск — 📎.
- Збитий сегмент → гриб: гравець сам будує лабіринт — 🌱 (ефект `set_cell` наслідком смерті).
- Отруєний гриб змінює поведінку ворога (пірнання) — 📎.
- Спавн за щільністю (блоха, коли в зоні мало грибів) — 📎.
- Відновлення поля після смерті з бонусом по одному грибу — 🌱 + анімація 📎.
- Очки за павука від відстані — 🌱.

## Мапа на каталог
- Є: `move-8dir` (рух у зоні) · `impassable-cells` (гриби для багатоніжки) · `projectile-shot` · `shoot-forward` · `body-queue` (тіло) · `cell-transform` (скорпіон труїть гриб) · `spawn-schedule` (голови з боку, павук) · `enemy-waves` · `touch-death` · `player-death` · `event-points` · `progress-acceleration` · `score-records` · `leaderboard` · `status-panel` · `hot-seat` · `game-screen` · `splash-screen`.
- **Нема** → пропозиції карток:
  - `+descend-and-reverse` «Біля перешкоди/краю — вниз і розворот» · entities/move · 📎 (Space Invaders).
  - `+segment-split` «Ланцюг ділиться на два з новою головою» · entities/state · 🥉.
  - `+destructible-blocks` «Руйнівні блоки» · entities/combat · 🌱 (Bomberman) — гриб з 4 HP.
  - `+shot-leaves-obstacle` «Збитий ворог лишає перешкоду» · entities/death · 🌱.
  - `+poison-cell` «Отруєна клітина змінює поведінку ворога» · entities/interact · 📎.
  - `+density-triggered-spawn` «Спавн, коли перешкод замало» · entities/spawn · 📎 · слот {zone, min}.
  - `+player-zone` «Гравець обмежений зоною поля» · entities/legality · 🌱.
  - `+distance-score` «Очки від відстані до цілі» · game-logic/score · 🌱.
  - `+restore-on-death` «Відновлення поля після смерті з бонусом» · game-logic/score · 📎.
  - `+extra-life-threshold` «Додаткове життя за очки» · game-logic/score · 🌱 · слот {every: 12000}.

## Пропозиції до словників
- `+trigger:blocked` — голова вперлась у гриб; `+trigger:edge` — край поля; `+trigger:died` — смерть гравця запускає відновлення; `+trigger:counter` — кожні 12 000 очок.
- `+cond:count` — грибів у зоні гравця < N; `+cond:in_range` — відстань павука до гравця; `+cond:state` — гриб отруєний.
- `+effect:split` — ланцюг ділиться (є ⏳ `split(a)`, потрібна семантика «нова голова»); `+effect:set_cell` — сегмент → гриб; `+effect:set_state` — пірнання; `+effect:hp` — удари по грибу; `+effect:spawn_at`; `+effect:lives`.
- `+role:terrain` — гриб і отруєний гриб.
- `+ui:lives` — іконки бластерів.
- `+axis:control` — `analog`: трекбол дає вільний рух у зоні (не клітина за клавішу).

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Centipede_(video_game)) — повний опис ворогів, очок, розщеплення, отрути, відновлення грибів і бонусного життя.
- YouTube: пошук «centipede 1981 arcade gameplay».
- Steam: пошук «centipede» (збірки Atari).

## Непевне
- (?) Розмір сітки 30×32 і висота зони гравця — з памʼяті.
- (?) Поріг появи блохи (кількість грибів у зоні) і що він росте з хвилями — Wikipedia лише «коли мало грибів».
- (?) Блоха прискорюється після першого удару; скорпіон не зʼявляється в першій хвилі — з памʼяті.
- (?) Кількість сегментів першої багатоніжки — Wikipedia: «10 або 12»; кількість життів за замовчуванням — 3 (?).
- (?) Зміна палітри з кожною хвилею — не перевірено.
- StrategyWiki і пошук були недоступні (403 / вичерпаний ліміт).
