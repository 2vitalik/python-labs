---
title: Isle of Arrows
slug: isle-of-arrows
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: runtime
  goal: survive
year: 2022
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1946970/Isle_of_Arrows/", best: true, note: "опис механік від автора: плитки, дороги, прапорці, таверни, сади, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=isle+of+arrows+gameplay", note: "пошук; геймплей"}
  - {kind: wiki, url: "https://en.wikipedia.org/w/index.php?search=Isle+of+Arrows&ns0=1", note: "пошук; статті нема"}
stage: v1
coverage: 55
mechanics: [enemy-waves, enemy-reached-base, round-currency, projectile-shot, shoot-cooldown, daily-puzzle, shop-between-levels, spawn-random-cell, goal-counter, status-panel, +tile-draw-place, +path-by-tiles, +adjacency-bonus, +island-expand, +skip-tile, +tower-placement, +tower-range, +run-relics]
proposes: ["+trigger:tile_drawn", "+cond:adjacent_to", "+effect:place_tile", "+effect:extend_path", "+effect:expand_area", "+effect:skip", "+role:tower", "+role:building", "+ui:next-tile-preview", "+ui:start-wave-button", "+window:upgrade-window", "+window:daily-window", "+feature:mode-daily", "+feature:run-relics", "+axis:session"]
author: opus
date: 2026-11-02
---

# Isle of Arrows — tower defense з викладанням плиток: ти сам будуєш і оборону, і дорогу ворогам

## Суть
Щораунду гравець отримує випадкову плитку (дорога, вежа, будівля, прапорець) і кладе її на острів. Дороги подовжують шлях, яким прийдуть вороги, вежі стріляють по них, будівлі дають бонуси сусідам або монети, прапорці розширюють сушу. Коли готовий — запускає хвилю й дивиться, чи витримає оборона. Незвичне: гравець **не вибирає, що ставити** (колода плиток), лише де — гібрид Carcassonne і TD від автора Hitman GO / Lara Croft GO.

## Поле і час
- Квадратна сітка-острів, що росте: на старті малий клаптик суші навколо замку, решта — вода; ставити можна лише на сушу (?).
- Дорога — ланцюг плиток-сегментів від замку назовні; вороги йдуть нею до замку. Кожна нова дорожня плитка подовжує шлях (і може розгалужувати його (?)).
- Покрокова фаза будування + real-time фаза хвилі без участі гравця (лише спостереження).
- Видно все поле; невідомо наперед — порядок плиток (є гарантія «N веж/доріг/будівель на кожні X плиток»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Замок (база) | static | HP / серця (?) | ворог дійшов → шкода базі |
| Плитка дороги | terrain | форма: пряма/поворот (/розвилка ?) | подовжує маршрут ворогів; кінець дороги — точка появи хвилі (?) |
| Лучна вежа | ally (tower) | радіус, швидкість | стріляє стрілами по ворогах у радіусі |
| Інші вежі | ally (tower) | тип (?) | різні снаряди/радіуси (?) |
| Таверна | ally (building) | — | підсилює сусідні лучні вежі |
| Сад | ally (building) | — | дає монети |
| Прапорець | object | — | розширює острів: додає сушу навколо |
| Монети | resource | — | витрачаються на пропуск плитки (і покупки між хвилями ?) |
| Ворог | enemy | HP, швидкість, тип | іде дорогою до замку |
| Бонусні карти · реліквії | pickup | — | ресурси, апгрейди, бафи на забіг |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «trigger tile_drawn: зняти верхню плитку з перемішаної колоди»` (з гарантованою квотою типів на кожні X плиток).
- КОЛИ `input(place, tile, cell)` → ЯКЩО `free(cell)` and `cell(x, land)` and `custom: «дорога стикується з кінцем дороги»` (для дорожніх) → ТО `custom: «effect place_tile»`.
- КОЛИ `placed(road)` → ТО `custom: «effect extend_path»` — маршрут ворогів довшає.
- КОЛИ `placed(flag)` → ТО `custom: «effect expand_area: суша навколо прапорця»`.
- КОЛИ `input(skip)` → ЯКЩО `has(coins, price)` → ТО `currency(-price)`, `custom: «скинути плитку, взяти наступну»`.
- КОЛИ `wave_start` (`input(start_wave)`) → ТО `spawn_at(enemies, path_end)` (?), вороги `move(a, next_on_path)` до замку.
- КОЛИ `in_range(tower, enemy, r)` → ТО `spawn(arrow)`; бонус від таверни — `custom: «cond adjacent_to(tavern) → сильніша/частіша стрільба»`.
- КОЛИ `contact(arrow, enemy)` → ТО `damage(n)`; КОЛИ `hp_zero(enemy)` → ТО `disappear_a`.
- КОЛИ `reach(enemy, castle)` → ТО `hp(castle, -n)`; КОЛИ `hp_zero(castle)` → ТО `lose`.
- КОЛИ `wave_cleared` → ТО сади `currency(+n)`, `choose(bonus_cards)` (?), наступний раунд будування.
- КОЛИ `custom: «остання хвиля острова відбита»` → ТО `win`.
- Перемога: пережити всі хвилі острова/забігу · Поразка: замок зруйновано · Рахунок: кількість хвиль (Daily — таблиця результатів (?)).

## Керування і ввід
- Миша: плитка висить біля курсора → клік по клітині = покласти; поворот плитки клавішею/правою кнопкою (?).
- Кнопка «пропустити плитку» за монети; кнопка «почати хвилю».
- Під час хвилі гравець не діє (?) — лише спостерігає.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Campaign · Gauntlet · Daily Defense; налаштування; вихід.
- `game-screen`: острів, поточна плитка (`+ui:next-tile-preview`), `coins`, HP замку, `wave-counter`, кнопки skip і `+ui:start-wave-button`.
- `upgrade-window` (⏳) — вибір бонусної карти/реліквії між хвилями (?).
- `daily-window` — щоденний острів з однаковим seed (?).
- `end-screen` — результат забігу; `pause-menu`; `settings-window` (мова: 6 мов).

## Фічі поза полем
- Режими: Campaign (набір островів), Gauntlet (серія з реліквіями — роглайк-забіг), Daily Defense (`mode-daily`).
- Процедурні забіги: випадкові плитки, вороги, нагороди, події; реліквії й бонус-карти — `run-relics` у межах забігу.
- `localization` (EN, FR, DE, ES, ZH, JA).

## Варіації й родичі
- Родичі «шлях будує гравець»: Fieldrunners (лабіринт із веж), Dorfromantik (викладання плиток без ворогів), Carcassonne, Kingdom Rush (фіксований шлях), Rogue Tower, Against the Storm (?).
- **Осі варіацій**: хто будує шлях — дизайнер / гравець вежами / гравець плитками · вибір юніта — магазин / колода / випадкова плитка · поле — фіксоване / росте · бонус — сусідство / глобальний.

## Цікавинки для курсу
- Колода плиток із гарантованою квотою типів («на кожні X — N веж») — 🥉 (контрольований рандом, `shuffle bag`).
- Дорога як граф-ланцюг плиток: стикування країв і перерахунок довжини маршруту — 🥈.
- Бонус за сусідство (таверна → лучні вежі) — 📎.
- Поле, що росте від прапорців — 📎.
- Пропуск плитки за монети — 🌱.
- Daily з однаковим seed для всіх — 📎 (`daily-puzzle`).

## Мапа на каталог
- Є: `enemy-waves` · `enemy-reached-base` · `round-currency` ↔ монети садів · `projectile-shot` + `shoot-cooldown` ↔ стріли · `daily-puzzle` ↔ Daily Defense · `shop-between-levels` ↔ бонуси між хвилями (?) · `spawn-random-cell` (лише як «випадкова плитка») · `goal-counter` + `status-panel`.
- **Нема** → пропозиції карток:
  - `+tile-draw-place` «Тягни-і-клади плитку» · entities/spawn · 🥉 · слот {bag: guaranteed_quota}.
  - `+path-by-tiles` «Маршрут ворогів зі стикованих плиток» · entities/move · 🥈.
  - `+adjacency-bonus` «Бонус сусідству» · game-logic/economy · 📎 · слот {radius}.
  - `+island-expand` «Будівна площа росте» · levels/generation · 📎.
  - `+skip-tile` «Пропуск за ресурс» · game-logic/economy · 🌱.
  - `+run-relics` «Реліквії забігу» · game-logic/economy · 🥉 (роглайк-мета).
  - `+tower-placement`, `+tower-range` — див. fieldrunners.

## Пропозиції до словників
- `+trigger:tile_drawn` — гравець отримав нову плитку з колоди.
- `+cond:adjacent_to` — сутність має сусіда виду (таверна поруч з вежею); `adjacent_count` ⏳ схожа, але тут достатньо ≥1.
- `+effect:place_tile` · `+effect:extend_path` · `+effect:expand_area` · `+effect:skip`.
- `+role:tower` (див. fieldrunners) · `+role:building` — нерухома сутність з пасивним ефектом (таверна, сад).
- `+ui:next-tile-preview` (≈ `next-piece-preview`, але для плиток) · `+ui:start-wave-button`.
- `+window:upgrade-window` ⏳ · `+window:daily-window` ⏳ — підтвердження.
- `+feature:mode-daily` · `+feature:run-relics` — реліквії/бонуси діють до кінця забігу.
- `+axis:session` — `level` (Campaign) і `daily` в одній грі.

## Джерела
- ⭐ [Steam: Isle of Arrows](https://store.steampowered.com/app/1946970/Isle_of_Arrows/) — опис механік від автора: випадкові плитки з гарантованою квотою, дороги як шлях ворогів, прапорці розширюють острів, таверни підсилюють лучні вежі, сади дають монети, монети — пропуск плитки, режими Campaign/Gauntlet/Daily Defense; реліз 8.09.2022, Gridpop (Daniel Lutz).
- YouTube: пошук «isle of arrows gameplay».
- Wikipedia: статті нема (пошук).

## Непевне
- (?) Повний список типів веж і будівель (крім лучної вежі, таверни, саду, прапорця) — джерела не відкрились (Thinky Games 403), WebSearch вичерпано.
- (?) Де зʼявляються вороги (кінець дороги?), чи бувають розвилки, чи можна повертати плитку.
- (?) Скільки плиток між хвилями (одна чи кілька), HP замку, чи є покупки між хвилями.
- (?) Мобільні версії (iOS/Android) — не перевірено.
